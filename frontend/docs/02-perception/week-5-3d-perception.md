---
sidebar_position: 2
---

# Week 5: 3D Perception & Point Clouds

## From 2D Images to 3D Understanding

Last week we explored 2D vision—detecting objects in flat images. This week, we extend to **3D perception**, enabling robots to understand spatial relationships, depth, and complete 3D structures.

### Why 3D Matters

- **Manipulation**: A robot arm needs 3D coordinates to reach objects
- **Navigation**: Understanding 3D obstacles prevents collisions
- **Grasping**: Knowing object shape in 3D improves grasp planning
- **Scene understanding**: Full 3D models enable reasoning about space

## Part 1: Depth Sensing Technologies

### Depth Camera Types

**Stereo Vision**
- Two cameras viewing same scene from different angles
- Like human eyes → enables depth perception
- Compute disparity (difference in pixel positions)
- Pros: Passive, high resolution
- Cons: Fails in texture-less areas, computationally intensive

**Time-of-Flight (ToF)**
- Emit light pulse, measure return time
- Distance = (speed of light × time) / 2
- Pros: Works on any surface, real-time
- Cons: Limited range, affected by ambient light

**Structured Light**
- Project known pattern (checkerboard, dots)
- Measure pattern deformation to compute depth
- Pros: Works on texture-less surfaces
- Cons: Fails in sunlight (infrared interferes)

**LIDAR**
- Laser-based scanning (covered in Week 2)
- Returns millions of 3D points
- Pros: Long range, accurate
- Cons: Expensive, overkill for close manipulation

```python
class DepthCamera:
    def __init__(self, camera_type='rgb-d'):
        """Initialize depth camera"""
        self.camera_type = camera_type

        if camera_type == 'stereo':
            self.baseline = 0.065  # 65mm between stereo cameras
            self.focal_length = 525  # Pixels

        elif camera_type == 'tof':
            self.speed_of_light = 3e8  # m/s
            self.modulation_freq = 20e6  # Hz

    def stereo_depth(self, left_image, right_image):
        """Compute depth from stereo pair"""

        # 1. Rectify images (align to same rows)
        left_rect, right_rect = self.rectify_stereo(left_image, right_image)

        # 2. Compute disparity map
        disparity_map = self.compute_disparity(left_rect, right_rect)

        # 3. Convert disparity to depth
        # depth = (baseline × focal_length) / disparity
        depth = (self.baseline * self.focal_length) / (disparity_map + 1e-6)

        return depth

    def compute_disparity(self, left, right):
        """Find matching pixels between stereo images"""
        # For each pixel in left, find best match in right
        # Simplified: actual implementations use more sophisticated matching

        disparity = np.zeros((left.shape[0], left.shape[1]))

        for y in range(left.shape[0]):
            for x in range(left.shape[1]):
                left_patch = left[y:y+9, x:x+9]  # 9×9 patch

                best_distance = float('inf')
                best_disparity = 0

                # Search window (typically ±60 pixels)
                for dx in range(-60, 61):
                    x_right = x + dx
                    if 0 <= x_right < right.shape[1]:
                        right_patch = right[y:y+9, x_right:x_right+9]

                        # Sum squared differences (SSD)
                        distance = np.sum((left_patch - right_patch)**2)

                        if distance < best_distance:
                            best_distance = distance
                            best_disparity = abs(dx)

                disparity[y, x] = best_disparity

        return disparity
```

## Part 2: Point Clouds

A **point cloud** is a 3D representation: a collection of (x, y, z) points in 3D space.

### Point Cloud Representation

```python
class PointCloud:
    def __init__(self, points_xyz, colors_rgb=None):
        """
        Initialize point cloud

        Args:
            points_xyz: N×3 array of (x, y, z) coordinates
            colors_rgb: N×3 array of (r, g, b) colors (optional)
        """
        self.points = points_xyz  # N×3
        self.colors = colors_rgb  # N×3 or None
        self.n_points = len(points_xyz)

    def from_depth_image(self, depth_image, camera_intrinsics):
        """Convert depth image to point cloud"""

        height, width = depth_image.shape
        fx, fy = camera_intrinsics['focal_x'], camera_intrinsics['focal_y']
        cx, cy = camera_intrinsics['center_x'], camera_intrinsics['center_y']

        points = []

        for y in range(height):
            for x in range(width):
                z = depth_image[y, x]

                if z > 0:  # Valid depth
                    # Back-project pixel to 3D
                    x_3d = (x - cx) * z / fx
                    y_3d = (y - cy) * z / fy

                    points.append([x_3d, y_3d, z])

        return np.array(points)

    def downsample_voxel(self, voxel_size=0.01):
        """Reduce points by averaging in voxels"""

        # Divide space into voxels
        voxel_grid = {}

        for point in self.points:
            # Compute voxel key
            voxel_key = tuple((point / voxel_size).astype(int))

            if voxel_key not in voxel_grid:
                voxel_grid[voxel_key] = []

            voxel_grid[voxel_key].append(point)

        # Average points in each voxel
        downsampled = np.array([
            np.mean(points, axis=0)
            for points in voxel_grid.values()
        ])

        return downsampled

    def remove_outliers_statistical(self, n_neighbors=20, std_ratio=2.0):
        """Remove noise points using statistical outlier removal"""

        from scipy.spatial import cKDTree

        tree = cKDTree(self.points)
        distances, indices = tree.query(self.points, k=n_neighbors+1)

        # Compute mean distance for each point
        mean_distances = np.mean(distances[:, 1:], axis=1)

        # Compute global statistics
        global_mean = np.mean(mean_distances)
        global_std = np.std(mean_distances)

        # Remove outliers
        threshold = global_mean + std_ratio * global_std
        inliers = mean_distances < threshold

        return self.points[inliers]
```

### Point Cloud Processing Pipeline

```python
class PointCloudProcessor:
    def process_lidar_scan(self, raw_points):
        """Process raw LIDAR points"""

        # 1. Remove points beyond range (outdoors, reflections)
        filtered = raw_points[np.linalg.norm(raw_points, axis=1) < 30]

        # 2. Remove ground plane points
        # (Assuming ground is roughly z=0)
        ground_removal = filtered[np.abs(filtered[:, 2]) > 0.1]

        # 3. Remove outliers
        clean_points = self.remove_outliers_statistical(
            ground_removal, n_neighbors=10, std_ratio=2.0
        )

        # 4. Downsample for efficiency
        downsampled = self.downsample_voxel(clean_points, voxel_size=0.02)

        return downsampled

    def cluster_points(self, points, distance_threshold=0.05):
        """Segment point cloud into clusters (objects)"""

        from scipy.spatial.distance import pdist, squareform

        # Compute pairwise distances
        distances = squareform(pdist(points, metric='euclidean'))

        # DBSCAN clustering
        clusters = self.dbscan(distances, eps=distance_threshold, min_samples=5)

        return clusters

    def dbscan(self, distances, eps, min_samples):
        """Simple DBSCAN clustering"""

        n_points = distances.shape[0]
        labels = -1 * np.ones(n_points)
        cluster_id = 0

        for i in range(n_points):
            if labels[i] != -1:
                continue

            neighbors = np.where(distances[i] <= eps)[0]

            if len(neighbors) < min_samples:
                labels[i] = -1  # Noise point
                continue

            # Start new cluster
            labels[i] = cluster_id
            queue = list(neighbors)

            while queue:
                j = queue.pop(0)

                if labels[j] == -1:
                    labels[j] = cluster_id

                    neighbors_j = np.where(distances[j] <= eps)[0]
                    if len(neighbors_j) >= min_samples:
                        queue.extend(neighbors_j[labels[neighbors_j] == -1])

            cluster_id += 1

        return labels
```

## Part 3: 3D Object Recognition

Once you have a point cloud, you can recognize objects by shape.

### Iterative Closest Point (ICP) Alignment

ICP matches a point cloud to a 3D model by iteratively aligning them.

```python
class PointCloudMatcher:
    def icp_align(self, source, target, max_iterations=50):
        """Align source point cloud to target"""

        source_current = np.copy(source)
        total_transform = np.eye(4)

        for iteration in range(max_iterations):
            # 1. Find nearest point in target for each source point
            from scipy.spatial import cKDTree
            tree = cKDTree(target)
            distances, indices = tree.query(source_current)

            target_matched = target[indices]

            # 2. Compute optimal rotation and translation
            rotation, translation = self.compute_rigid_transform(
                source_current, target_matched
            )

            # 3. Apply transform
            transform = np.eye(4)
            transform[:3, :3] = rotation
            transform[:3, 3] = translation

            source_current = (rotation @ source_current.T).T + translation
            total_transform = transform @ total_transform

            # 4. Check convergence
            mean_error = np.mean(distances)
            if mean_error < 0.001:
                break

        return source_current, total_transform, mean_error

    def compute_rigid_transform(self, source, target):
        """Compute optimal rotation and translation"""

        # Center both point clouds
        source_centered = source - np.mean(source, axis=0)
        target_centered = target - np.mean(target, axis=0)

        # Compute cross-covariance matrix
        H = source_centered.T @ target_centered

        # SVD to find rotation
        U, S, Vt = np.linalg.svd(H)
        rotation = Vt.T @ U.T

        # Ensure proper rotation (det = 1)
        if np.linalg.det(rotation) < 0:
            Vt[-1, :] *= -1
            rotation = Vt.T @ U.T

        # Compute translation
        translation = (np.mean(target, axis=0) -
                      rotation @ np.mean(source, axis=0))

        return rotation, translation
```

## Real-World Example: Bin Picking

```python
class BinPickingRobot:
    def __init__(self):
        self.depth_camera = DepthCamera()
        self.point_processor = PointCloudProcessor()
        self.arm = RobotArm()
        self.gripper = Gripper()

    def pick_from_bin(self):
        """Complete bin picking sequence"""

        # 1. Acquire depth image
        depth_image = self.depth_camera.capture()

        # 2. Convert to point cloud
        cloud = self.depth_camera.from_depth_image(depth_image)

        # 3. Process: remove noise, ground, downsample
        clean_cloud = self.point_processor.process_lidar_scan(cloud)

        # 4. Cluster points to find individual objects
        cluster_labels = self.point_processor.cluster_points(
            clean_cloud, distance_threshold=0.05
        )

        # 5. For each cluster, compute grasp pose
        best_grasp = None
        best_score = 0

        for cluster_id in np.unique(cluster_labels):
            if cluster_id == -1:
                continue

            cluster_points = clean_cloud[cluster_labels == cluster_id]

            # Compute centroid and approach direction
            centroid = np.mean(cluster_points, axis=0)

            # Try grasp from above
            grasp_pose = {
                'position': centroid + np.array([0, 0, 0.05]),
                'orientation': np.eye(3),
                'confidence': len(cluster_points) / 100  # More points = easier
            }

            if grasp_pose['confidence'] > best_score:
                best_grasp = grasp_pose
                best_score = grasp_pose['confidence']

        if best_grasp is None:
            return False

        # 6. Execute grasp
        self.arm.move_to(best_grasp['position'])
        self.gripper.close()

        return True
```

## Week 5 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** how depth cameras measure 3D structure
2. **Convert** depth images into point clouds
3. **Process** point clouds (downsampling, outlier removal, clustering)
4. **Implement** ICP for aligning point clouds
5. **Recognize** 3D objects by comparing point cloud shapes
6. **Apply** 3D perception to robotic bin picking

## Key Terminology

| Term | Definition |
|------|-----------|
| **Depth image** | 2D array where each pixel contains distance to surface |
| **Point cloud** | 3D representation as collection of (x, y, z) points |
| **Disparity** | Difference in pixel position between stereo images |
| **Voxel** | 3D grid cell (volumetric pixel) |
| **Outlier** | Noise point that doesn't fit with other points |
| **Cluster** | Group of connected points representing single object |
| **ICP** | Iterative Closest Point - algorithm for cloud alignment |
| **Occlusion** | Object hidden behind another object |

## Discussion Questions

1. **Sensor selection**: For a warehouse robot picking boxes, would you use stereo vision, LIDAR, or RGB-D cameras? Why?

2. **Computational load**: Converting a 640×480 depth image to point cloud requires ~300K 3D transformations per frame. At 30 FPS, that's 9M calculations/second. How would you optimize?

3. **Robustness**: Point cloud clustering can fail when objects touch. How would you handle densely packed bins?

4. **Multi-sensor fusion**: Why fuse LIDAR + stereo? What does each sensor contribute?

## Hands-On Activity

**Process a simulated point cloud**

1. Generate synthetic 3D data (download KITTI dataset or generate noise)
2. Implement point cloud pipeline:
   - Downsample voxel grid
   - Remove statistical outliers
   - Cluster points
3. Visualize results using Open3D or PyVista
4. Measure clustering accuracy (precision/recall)

## Resources for Deeper Learning

- **Library**: Open3D - Python 3D data processing
- **Library**: Point Cloud Library (PCL) - C++ point cloud processing
- **Dataset**: KITTI dataset - autonomous driving with 3D data
- **Course**: "3D Vision" - UC Berkeley (YouTube available)
- **Paper**: "A Method for Registration of 3-D Shapes" - ICP algorithm

---

**Next**: Week 6 - SLAM & Localization

💡 **Tip**: Visualizing point clouds is essential! Use tools like CloudCompare or Open3D's visualizer to understand your data.
