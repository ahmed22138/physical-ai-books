---
sidebar_position: 1
---

# Week 4: Computer Vision Fundamentals

## Introduction to Robot Vision

Welcome to Module 2! This week begins our deep dive into **perception systems**—how robots understand the visual world around them. Computer vision is one of the most critical capabilities for embodied AI systems, enabling object recognition, spatial understanding, and scene comprehension.

### Why Vision Matters for Robots

Vision provides the richest information about the environment. While sensors like LIDAR measure distance well, cameras capture:
- **Color information** for object identification
- **Texture and edges** for shape understanding
- **Semantic meaning** through learned patterns
- **High-resolution detail** for precise manipulation

But vision is computationally expensive. This week, we explore the fundamental algorithms that make robot vision practical.

## Part 1: Image Fundamentals

### Representing Images as Data

A digital image is fundamentally a **matrix of pixel values**. For an RGB color image:

```
Image: 640×480 pixels (width × height)
├─ Red channel: 640×480 matrix of values [0-255]
├─ Green channel: 640×480 matrix of values [0-255]
└─ Blue channel: 640×480 matrix of values [0-255]

Example pixel (100, 200) = [R=255, G=128, B=0] → Orange color
```

**Image dimensions:**
- Grayscale: Height × Width × 1
- RGB Color: Height × Width × 3
- RGBA: Height × Width × 4 (with transparency)
- Typical resolution: 640×480 (0.3MP), 1920×1080 (2MP), 4K (8MP)

### Basic Image Operations

```python
import numpy as np
from PIL import Image

class ImageProcessor:
    def load_image(self, path):
        """Load image from file"""
        img = Image.open(path)
        # Convert to numpy array: shape (height, width, 3)
        return np.array(img)

    def convert_to_grayscale(self, image):
        """Convert RGB to grayscale"""
        # Weighted average: 0.299×R + 0.587×G + 0.114×B
        gray = np.dot(image[...,:3], [0.299, 0.587, 0.114])
        return gray.astype(np.uint8)

    def resize_image(self, image, new_height, new_width):
        """Resize image using bilinear interpolation"""
        from scipy.ndimage import zoom
        h, w = image.shape[:2]
        scale_y = new_height / h
        scale_x = new_width / w
        return zoom(image, (scale_y, scale_x, 1), order=1)

    def crop_image(self, image, y1, y2, x1, x2):
        """Crop rectangular region from image"""
        return image[y1:y2, x1:x2, :]

    def apply_blur(self, image, kernel_size=5):
        """Apply Gaussian blur to reduce noise"""
        from scipy.ndimage import gaussian_filter
        return np.stack([
            gaussian_filter(image[:,:,i], sigma=kernel_size)
            for i in range(image.shape[2])
        ], axis=2).astype(np.uint8)
```

## Part 2: Feature Detection & Matching

### Image Gradients and Edges

The **gradient** of an image measures how quickly pixel intensity changes. Large gradients indicate edges.

**Edge detection using Sobel operator:**

```python
class EdgeDetector:
    def compute_sobel(self, image):
        """Compute image gradients using Sobel operator"""

        # Grayscale image
        gray = self.convert_to_grayscale(image)

        # Sobel kernels detect edges in X and Y directions
        sobel_x = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]) / 8

        sobel_y = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]) / 8

        # Convolve image with kernels (simplified)
        gx = self.convolve_2d(gray, sobel_x)
        gy = self.convolve_2d(gray, sobel_y)

        # Magnitude of gradient
        magnitude = np.sqrt(gx**2 + gy**2)

        # Direction of gradient (angle)
        direction = np.arctan2(gy, gx) * 180 / np.pi

        return magnitude, direction

    def convolve_2d(self, image, kernel):
        """Apply 2D convolution (simplified for clarity)"""
        from scipy.signal import convolve2d
        return convolve2d(image, kernel, mode='same')

    def detect_edges(self, image, threshold=100):
        """Threshold gradient magnitude to find edges"""
        magnitude, _ = self.compute_sobel(image)
        edges = (magnitude > threshold).astype(np.uint8) * 255
        return edges
```

### Keypoint Detection

**Keypoints** are distinctive locations in an image that can be reliably detected and matched across images.

**SIFT (Scale-Invariant Feature Transform) algorithm:**
1. Build image pyramid (multiple scales)
2. Find candidate keypoints at local extrema
3. Refine with sub-pixel accuracy
4. Compute orientation-invariant descriptors

```python
class KeypointDetector:
    def detect_sift_keypoints(self, image):
        """Detect SIFT keypoints in image"""

        # Build image pyramid (scale space)
        pyramid = self.build_gaussian_pyramid(image, num_levels=5)

        keypoints = []

        # Find local extrema (minima/maxima)
        for level in range(1, len(pyramid)-1):
            prev_level = pyramid[level-1]
            curr_level = pyramid[level]
            next_level = pyramid[level+1]

            # For each pixel in current level
            for y in range(1, curr_level.shape[0]-1):
                for x in range(1, curr_level.shape[1]-1):

                    # Get 3×3×3 neighborhood
                    value = curr_level[y, x]

                    # Check if local extremum
                    neighborhood_prev = prev_level[y-1:y+2, x-1:x+2]
                    neighborhood_curr = curr_level[y-1:y+2, x-1:x+2]
                    neighborhood_next = next_level[y-1:y+2, x-1:x+2]

                    is_extremum = (
                        np.all(value > np.concatenate([
                            neighborhood_prev.flatten(),
                            neighborhood_curr.flatten(),
                            neighborhood_next.flatten()
                        ])) or
                        np.all(value < np.concatenate([
                            neighborhood_prev.flatten(),
                            neighborhood_curr.flatten(),
                            neighborhood_next.flatten()
                        ]))
                    )

                    if is_extremum:
                        keypoints.append({
                            'x': x,
                            'y': y,
                            'scale': level,
                            'magnitude': abs(value)
                        })

        return keypoints

    def build_gaussian_pyramid(self, image, num_levels=5):
        """Build Gaussian pyramid for scale-space analysis"""
        pyramid = [image]
        for _ in range(num_levels-1):
            # Blur and downsample
            blurred = gaussian_filter(pyramid[-1], sigma=1.0)
            downsampled = blurred[::2, ::2]  # Every other pixel
            pyramid.append(downsampled)
        return pyramid
```

### Feature Matching

Once keypoints are detected, we match them across images to track objects or estimate motion.

```python
class FeatureMatcher:
    def match_keypoints(self, keypoints1, descriptors1,
                       keypoints2, descriptors2):
        """Match keypoints between two images"""

        matches = []

        for i, desc1 in enumerate(descriptors1):
            # Find closest descriptor in image 2
            distances = np.linalg.norm(
                descriptors2 - desc1, axis=1
            )
            closest_idx = np.argmin(distances)
            distance_closest = distances[closest_idx]

            # Find second closest (for Lowe's ratio test)
            sorted_indices = np.argsort(distances)
            distance_second = distances[sorted_indices[1]]

            # Lowe's ratio test: reject if closest is not clearly better
            if distance_closest / distance_second < 0.7:
                matches.append({
                    'idx1': i,
                    'idx2': closest_idx,
                    'distance': distance_closest,
                    'keypoint1': keypoints1[i],
                    'keypoint2': keypoints2[closest_idx]
                })

        return matches
```

## Part 3: Object Detection

### Bounding Box Detection

The simplest object detection: find rectangular regions containing objects.

```python
class ObjectDetector:
    def detect_by_color(self, image, target_color, tolerance=30):
        """Detect objects by color"""

        # Define color range in HSV
        # (HSV is more robust than RGB for color)
        target_hsv = self.rgb_to_hsv(target_color)

        hsv_image = self.rgb_to_hsv_image(image)

        # Find pixels within color range
        mask = self.create_color_mask(
            hsv_image, target_hsv, tolerance
        )

        # Find connected components (clusters of pixels)
        labeled, num_objects = self.label_connected_components(mask)

        bounding_boxes = []
        for obj_id in range(1, num_objects+1):
            # Find bounding box for this object
            coords = np.where(labeled == obj_id)
            if len(coords[0]) > 50:  # Minimum size
                y_min, y_max = coords[0].min(), coords[0].max()
                x_min, x_max = coords[1].min(), coords[1].max()

                bounding_boxes.append({
                    'x_min': int(x_min),
                    'y_min': int(y_min),
                    'x_max': int(x_max),
                    'y_max': int(y_max),
                    'width': int(x_max - x_min),
                    'height': int(y_max - y_min),
                    'center_x': int((x_min + x_max) / 2),
                    'center_y': int((y_min + y_max) / 2),
                    'area': len(coords[0])
                })

        return bounding_boxes, mask

    def draw_bounding_boxes(self, image, boxes, color=(0, 255, 0)):
        """Draw detected bounding boxes on image"""
        import cv2
        img_copy = image.copy()
        for box in boxes:
            cv2.rectangle(
                img_copy,
                (box['x_min'], box['y_min']),
                (box['x_max'], box['y_max']),
                color, 2
            )
            cv2.putText(
                img_copy,
                f"A={box['area']}",
                (box['x_min'], box['y_min']-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
            )
        return img_copy
```

## Part 4: Deep Learning for Vision (Neural Networks)

While traditional computer vision (edges, features) works well for specific tasks, **deep learning** enables learning what features matter for your task.

### Convolutional Neural Networks (CNNs)

A CNN learns **filters** (like our Sobel edge detector) automatically from data.

```python
class SimpleCNN:
    def __init__(self):
        """Initialize simple CNN architecture"""
        # This is pseudo-code; real implementation uses PyTorch/TensorFlow

        # Layer 1: Convolution (32 filters, 3×3 kernel)
        self.conv1 = ConvLayer(input_channels=3, output_channels=32,
                              kernel_size=3, activation='relu')

        # Layer 2: Max pooling (2×2)
        self.pool1 = MaxPoolLayer(kernel_size=2)

        # Layer 3: Convolution (64 filters, 3×3 kernel)
        self.conv2 = ConvLayer(input_channels=32, output_channels=64,
                              kernel_size=3, activation='relu')

        # Layer 4: Max pooling (2×2)
        self.pool2 = MaxPoolLayer(kernel_size=2)

        # Layer 5: Fully connected (128 neurons)
        self.fc1 = FullyConnectedLayer(input_size=64*56*56,
                                       output_size=128,
                                       activation='relu')

        # Layer 6: Output (10 classes)
        self.fc2 = FullyConnectedLayer(input_size=128,
                                       output_size=10,
                                       activation='softmax')

    def forward(self, image):
        """Forward pass through network"""
        # Input: 224×224×3 image
        x = self.conv1(image)      # → 224×224×32
        x = self.pool1(x)          # → 112×112×32
        x = self.conv2(x)          # → 112×112×64
        x = self.pool2(x)          # → 56×56×64
        x = x.flatten()            # → 200704
        x = self.fc1(x)            # → 128
        x = self.fc2(x)            # → 10
        return x
```

### Pre-trained Models

Most practitioners use **pre-trained models** trained on massive datasets:
- **ResNet-50**: Trained on ImageNet (1M images, 1000 classes)
- **YOLO**: Trained for real-time object detection
- **MobileNet**: Optimized for mobile/embedded devices

```python
class PretrainedDetector:
    def __init__(self, model_name='yolo-v8'):
        """Load pre-trained model"""
        from ultralytics import YOLO

        # Download and load model
        self.model = YOLO(f'{model_name}.pt')

    def detect_objects(self, image):
        """Detect objects using pre-trained model"""

        # Run inference
        results = self.model.predict(image, conf=0.5)

        detections = []
        for result in results:
            for box in result.boxes:
                detection = {
                    'class_name': self.model.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'x_min': int(box.xyxy[0, 0]),
                    'y_min': int(box.xyxy[0, 1]),
                    'x_max': int(box.xyxy[0, 2]),
                    'y_max': int(box.xyxy[0, 3]),
                }
                detections.append(detection)

        return detections
```

## Real-World Example: Picking Ripe Tomatoes

```python
class TomatoRobotVision:
    def __init__(self):
        self.color_detector = ObjectDetector()
        self.ripeness_classifier = PretrainedDetector('tomato-ripeness')
        self.camera = CameraInterface()

    def find_ripe_tomatoes(self):
        """Detect ripe tomatoes in greenhouse"""

        # Capture image
        image = self.camera.capture()

        # Step 1: Detect red objects (tomato color range)
        red_color = np.array([0, 100, 255])  # HSV red
        tomato_regions, mask = self.color_detector.detect_by_color(
            image, red_color, tolerance=30
        )

        # Step 2: Classify ripeness for each candidate
        ripe_tomatoes = []

        for region in tomato_regions:
            # Crop region around potential tomato
            y1 = max(0, region['y_min']-10)
            y2 = min(image.shape[0], region['y_max']+10)
            x1 = max(0, region['x_min']-10)
            x2 = min(image.shape[1], region['x_max']+10)

            crop = image[y1:y2, x1:x2, :]

            # Classify ripeness
            ripeness = self.ripeness_classifier.detect_objects(crop)

            if ripeness and ripeness[0]['class_name'] == 'ripe':
                ripe_tomatoes.append({
                    **region,
                    'ripeness_score': ripeness[0]['confidence']
                })

        return ripe_tomatoes

    def visualize_results(self, image, tomatoes):
        """Draw results on image"""
        img_vis = image.copy()

        for tom in tomatoes:
            # Draw green box for ripe tomato
            cv2.rectangle(
                img_vis,
                (tom['x_min'], tom['y_min']),
                (tom['x_max'], tom['y_max']),
                (0, 255, 0), 2
            )
            cv2.putText(
                img_vis,
                f"Ripe ({tom['ripeness_score']:.2f})",
                (tom['x_min'], tom['y_min']-5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

        return img_vis
```

## Performance Considerations

Real-time vision on robots requires **balancing accuracy and speed**.

| Approach | Speed | Accuracy | Suitable For |
|----------|-------|----------|-------------|
| Color segmentation | 100+ FPS | Low | Simple environments |
| Edge detection | 50+ FPS | Low-Medium | Feature-rich scenes |
| Traditional features (SIFT) | 10-30 FPS | Medium | Tracking, matching |
| Small CNN (MobileNet) | 30-60 FPS | Medium-High | Edge devices |
| Large CNN (ResNet-50) | 5-15 FPS | High | GPU-enabled systems |
| YOLO (real-time detector) | 30-60 FPS | High | Object detection |

## Week 4 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** how digital images are represented as matrices of pixel values
2. **Implement** basic image processing (resize, crop, blur, threshold)
3. **Detect** edges using gradient-based methods (Sobel operator)
4. **Identify** keypoints and match them across images
5. **Apply** color-based object detection for structured environments
6. **Compare** traditional and deep learning approaches to vision

## Key Terminology

| Term | Definition |
|------|-----------|
| **Pixel** | Single point in image; RGB image has 3 values per pixel |
| **Kernel** | Small matrix (filter) convolved with image for feature extraction |
| **Convolution** | Mathematical operation to apply filter across image |
| **Edge** | Location where pixel intensity changes rapidly |
| **Keypoint** | Distinctive, repeatable location in image (SIFT, SURF) |
| **Descriptor** | Feature vector describing appearance around keypoint |
| **Bounding box** | Rectangular region marking object location |
| **CNN** | Convolutional Neural Network with learned filters |

## Discussion Questions

1. **Tradeoffs**: Why is color-based detection faster but less robust than CNN-based detection? When would you use each?

2. **Real-time constraints**: A robot must detect objects at 30 FPS. If processing takes 100ms per frame, what percentage of time budget is spent on vision?

3. **Robustness**: A tomato detector works perfectly indoors under controlled lighting. What happens outdoors? How would you make it more robust?

4. **Pre-trained models**: When should you use pre-trained models vs. train your own? What are the tradeoffs?

## Hands-On Activity

**Build a simple color detector**

1. Capture or download an image with distinct colored objects
2. Implement color-based object detection (no deep learning)
3. Draw bounding boxes around detected objects
4. Test robustness by:
   - Changing lighting
   - Rotating image
   - Adding objects with similar colors
5. Document detection accuracy (true positives / total objects)

## Resources for Deeper Learning

- **Book**: "Computer Vision: Algorithms and Applications" - Richard Szeliski
- **Course**: "Computer Vision Basics" - OpenCV tutorials
- **Tool**: OpenCV (C++/Python) for traditional vision
- **Framework**: PyTorch or TensorFlow for deep learning
- **Dataset**: COCO dataset for training object detectors
- **Pre-trained models**: Hugging Face Model Hub

---

**Next**: Week 5 - Advanced Vision & 3D Perception

💡 **Tip**: Start with color-based detection before diving into neural networks. Understanding traditional vision builds intuition for why deep learning works!
