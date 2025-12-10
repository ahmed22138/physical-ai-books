"""
Content Ingestion Script
Reads lesson files, chunks them, creates embeddings, and stores in Qdrant
"""

import asyncio
import os
import re
from pathlib import Path
from typing import List, Dict, Any
import hashlib
import logging

from backend.config import settings
from backend.services.rag_service import rag_service
from backend.qdrant_client import qdrant_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Chunk text into overlapping segments

    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)

            if break_point > chunk_size // 2:  # Only break if it's reasonable
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks


def extract_metadata(content: str, file_path: str) -> Dict[str, str]:
    """
    Extract metadata from MDX content

    Args:
        content: File content
        file_path: Path to file

    Returns:
        Dict with chapter_id, title, module
    """
    # Extract chapter ID from filename
    filename = os.path.basename(file_path)
    chapter_id = filename.replace('.mdx', '').replace('.md', '')

    # Extract module from directory
    module = "general"
    if "01-introduction" in file_path:
        module = "module-1-introduction"
    elif "02-perception" in file_path:
        module = "module-2-perception"
    elif "03-control" in file_path:
        module = "module-3-control"
    elif "04-integration" in file_path:
        module = "module-4-integration"

    # Extract title from first heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else chapter_id

    return {
        "chapter_id": chapter_id,
        "title": title,
        "module": module
    }


def extract_sections(content: str) -> List[Dict[str, str]]:
    """
    Extract sections from MDX content

    Args:
        content: File content

    Returns:
        List of dicts with section name and text
    """
    # Split by H2 headers
    sections = []
    current_section = "Introduction"
    current_text = []

    lines = content.split('\n')
    for line in lines:
        # Check for H2 header
        if line.startswith('##'):
            # Save previous section
            if current_text:
                sections.append({
                    "section": current_section,
                    "text": '\n'.join(current_text).strip()
                })
                current_text = []

            # Start new section
            current_section = line.lstrip('#').strip()
        else:
            current_text.append(line)

    # Add final section
    if current_text:
        sections.append({
            "section": current_section,
            "text": '\n'.join(current_text).strip()
        })

    return sections


async def ingest_lesson_file(file_path: str) -> int:
    """
    Ingest a single lesson file

    Args:
        file_path: Path to MDX/MD file

    Returns:
        Number of chunks ingested
    """
    logger.info(f"Processing file: {file_path}")

    # Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        return 0

    # Extract metadata
    metadata = extract_metadata(content, file_path)
    logger.info(f"  Chapter: {metadata['chapter_id']}, Module: {metadata['module']}")

    # Extract sections
    sections = extract_sections(content)
    logger.info(f"  Found {len(sections)} sections")

    # Prepare chunks for ingestion
    all_chunks = []

    for section_data in sections:
        section_name = section_data["section"]
        section_text = section_data["text"]

        # Skip very short sections
        if len(section_text) < 100:
            continue

        # Chunk the section
        chunks = chunk_text(section_text, chunk_size=1000, overlap=200)

        for i, chunk in enumerate(chunks):
            # Create unique ID for chunk
            chunk_id = hashlib.md5(
                f"{metadata['chapter_id']}-{section_name}-{i}".encode()
            ).hexdigest()

            all_chunks.append({
                "id": chunk_id,
                "text": chunk,
                "chapter_id": metadata["chapter_id"],
                "section": section_name,
                "metadata": {
                    "title": metadata["title"],
                    "module": metadata["module"],
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })

    # Ingest chunks
    if all_chunks:
        success = await rag_service.ingest_content(all_chunks)
        if success:
            logger.info(f"  ✓ Ingested {len(all_chunks)} chunks")
            return len(all_chunks)
        else:
            logger.error(f"  ✗ Failed to ingest chunks")
            return 0
    else:
        logger.warning(f"  No chunks to ingest")
        return 0


async def ingest_all_lessons():
    """
    Ingest all lesson files from frontend/docs
    """
    # Find content directory
    content_dir = Path(settings.content_path)

    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        return

    logger.info(f"Scanning content directory: {content_dir}")

    # Find all MDX/MD files
    lesson_files = list(content_dir.rglob("*.mdx")) + list(content_dir.rglob("*.md"))
    lesson_files = [f for f in lesson_files if "node_modules" not in str(f)]

    logger.info(f"Found {len(lesson_files)} lesson files")

    # Initialize Qdrant collection
    logger.info("Initializing Qdrant collection...")
    await qdrant_service.init_collection()

    # Ingest each file
    total_chunks = 0
    for file_path in sorted(lesson_files):
        chunks_count = await ingest_lesson_file(str(file_path))
        total_chunks += chunks_count

    logger.info(f"\n{'='*60}")
    logger.info(f"Ingestion complete!")
    logger.info(f"Total files processed: {len(lesson_files)}")
    logger.info(f"Total chunks ingested: {total_chunks}")
    logger.info(f"{'='*60}\n")


async def main():
    """Main entry point"""
    logger.info("Starting content ingestion...")
    await ingest_all_lessons()
    logger.info("Content ingestion finished!")


if __name__ == "__main__":
    asyncio.run(main())
