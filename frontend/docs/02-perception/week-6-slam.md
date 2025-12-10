---
sidebar_position: 3
---

# Week 6: SLAM & Localization

## The Navigation Challenge

Imagine deploying a robot in a warehouse it has never seen before. Two fundamental questions arise:

1. **Where am I?** (Localization)
2. **What does the world around me look like?** (Mapping)

This week, we tackle **SLAM** (Simultaneous Localization and Mapping)—the foundation of autonomous robot navigation.

### Why SLAM Matters

- **Unknown environments**: Robots must navigate without pre-built maps
- **Error accumulation**: Dead reckoning (wheel encoders) drifts over time
- **Real-time requirements**: Navigation decisions happen continuously
- **Resource constraints**: Mobile robots have limited computation

## Part 1: Localization Problem

### Dead Reckoning (Odometry)

The simplest approach: track robot position using wheel encoders.

```python
class RobotOdometry:
    def __init__(self, wheel_radius=0.05, wheel_base=0.3):
        """Initialize odometry"""
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base

        self.x = 0
        self.y = 0
        self.theta = 0  # Heading angle

        self.last_left_ticks = 0
        self.last_right_ticks = 0

    def update(self, left_encoder_ticks, right_encoder_ticks, dt=0.01):
        """Update robot pose from encoder ticks"""

        # Compute distance traveled by each wheel
        left_distance = (left_encoder_ticks - self.last_left_ticks) * \
                       self.wheel_radius
        right_distance = (right_encoder_ticks - self.last_right_ticks) * \
                        self.wheel_radius

        self.last_left_ticks = left_encoder_ticks
        self.last_right_ticks = right_encoder_ticks

        # Compute forward and rotational motion
        forward = (left_distance + right_distance) / 2
        rotation = (right_distance - left_distance) / self.wheel_base

        # Update heading
        self.theta += rotation

        # Update position
        self.x += forward * np.cos(self.theta)
        self.y += forward * np.sin(self.theta)

        return self.x, self.y, self.theta

    def get_pose(self):
        """Return current pose estimate"""
        return np.array([self.x, self.y, self.theta])
```

**Problem**: Wheel slip, uneven terrain, and systematic errors cause **drift** over time.

```
Ideal path:     ┌─────┐
                │     │
                └─────┘

Actual (drift):  ┌─────┐
                 │     └──  ← Accumulating error
```

### Probabilistic Localization

Instead of trusting a single estimate, maintain a **probability distribution** over possible robot positions.

```python
class ParticleFilter:
    def __init__(self, n_particles=1000, world_size=(10, 10)):
        """Initialize particle filter for 2D localization"""

        self.n_particles = n_particles
        self.world_size = world_size

        # Create particles at random initial positions
        self.particles = np.random.uniform(
            [0, 0, -np.pi],
            [world_size[0], world_size[1], np.pi],
            (n_particles, 3)
        )

        # Initialize weights uniformly
        self.weights = np.ones(n_particles) / n_particles

    def predict(self, control_linear, control_angular, noise_level=0.1):
        """Predict particles given control commands"""

        for i in range(self.n_particles):
            # Add control
            x, y, theta = self.particles[i]

            x += control_linear * np.cos(theta)
            y += control_linear * np.sin(theta)
            theta += control_angular

            # Add process noise (Gaussian)
            x += np.random.normal(0, noise_level)
            y += np.random.normal(0, noise_level)
            theta += np.random.normal(0, noise_level * 0.1)

            self.particles[i] = [x, y, theta]

    def update(self, sensor_reading, measurement_model):
        """Update particle weights based on sensor observation"""

        for i in range(self.n_particles):
            # Compute likelihood of observation given particle pose
            self.weights[i] *= measurement_model(
                self.particles[i], sensor_reading
            )

        # Normalize weights
        self.weights /= np.sum(self.weights)

    def resample(self):
        """Resample particles (discard low-weight, duplicate high-weight)"""

        indices = np.random.choice(
            self.n_particles,
            self.n_particles,
            p=self.weights,
            replace=True
        )

        self.particles = self.particles[indices]
        self.weights = np.ones(self.n_particles) / self.n_particles

    def estimate_pose(self):
        """Compute expected pose from particle distribution"""

        # Weighted average
        mean_pose = np.average(self.particles, axis=0, weights=self.weights)
        return mean_pose
```

## Part 2: Mapping Problem

### Occupancy Grid Maps

Divide the world into a 2D grid. Each cell is either **occupied** (obstacle) or **free** (traversable).

```python
class OccupancyGrid:
    def __init__(self, width=100, height=100, resolution=0.1):
        """Initialize occupancy grid map"""

        self.width = width          # meters
        self.height = height        # meters
        self.resolution = resolution  # meters/cell

        self.cells_x = int(width / resolution)
        self.cells_y = int(height / resolution)

        # Store occupancy as log-odds
        # log(p / (1-p)) where p = probability occupied
        self.grid = np.zeros((self.cells_y, self.cells_x))

    def world_to_grid(self, x, y):
        """Convert world coordinates to grid cell"""
        cell_x = int(x / self.resolution)
        cell_y = int(y / self.resolution)

        # Clamp to valid range
        cell_x = max(0, min(self.cells_x - 1, cell_x))
        cell_y = max(0, min(self.cells_y - 1, cell_y))

        return cell_x, cell_y

    def update_cell(self, x, y, occupied, confidence=1.0):
        """Update cell occupancy"""

        cell_x, cell_y = self.world_to_grid(x, y)

        # Update log-odds
        if occupied:
            self.grid[cell_y, cell_x] += confidence
        else:
            self.grid[cell_y, cell_x] -= confidence

        # Clamp log-odds to reasonable range
        self.grid[cell_y, cell_x] = np.clip(self.grid[cell_y, cell_x], -5, 5)

    def update_from_lidar(self, robot_pose, lidar_points, max_range=10):
        """Update grid from LIDAR scan"""

        robot_x, robot_y, robot_theta = robot_pose

        # Mark all LIDAR hits as occupied
        for point in lidar_points:
            # Transform LIDAR point to world frame
            point_x = point[0]
            point_y = point[1]

            world_x = robot_x + point_x * np.cos(robot_theta) - \
                     point_y * np.sin(robot_theta)
            world_y = robot_y + point_x * np.sin(robot_theta) + \
                     point_y * np.cos(robot_theta)

            self.update_cell(world_x, world_y, occupied=True, confidence=0.9)

        # Raycasting: mark cells between robot and hits as free
        for point in lidar_points:
            point_x = point[0]
            point_y = point[1]

            world_x = robot_x + point_x * np.cos(robot_theta) - \
                     point_y * np.sin(robot_theta)
            world_y = robot_y + point_x * np.sin(robot_theta) + \
                     point_y * np.cos(robot_theta)

            # Raycasting: walk from robot to point
            distance = np.sqrt(point_x**2 + point_y**2)
            for d in np.arange(0, distance, self.resolution):
                ray_x = robot_x + d * np.cos(robot_theta)
                ray_y = robot_y + d * np.sin(robot_theta)

                self.update_cell(ray_x, ray_y, occupied=False, confidence=0.1)

    def is_occupied(self, x, y):
        """Query if cell is occupied"""
        cell_x, cell_y = self.world_to_grid(x, y)
        # Positive log-odds → likely occupied
        return self.grid[cell_y, cell_x] > 0

    def visualize(self):
        """Visualize map as image"""
        # Convert log-odds to probabilities
        prob = 1 / (1 + np.exp(-self.grid))
        return (prob * 255).astype(np.uint8)
```

## Part 3: Complete SLAM System

Now we combine localization + mapping:

```python
class SimpleSLAM:
    def __init__(self):
        self.particle_filter = ParticleFilter(n_particles=500)
        self.occupancy_grid = OccupancyGrid(width=50, height=50)
        self.odometry = RobotOdometry()

    def step(self, left_encoder_ticks, right_encoder_ticks, lidar_scan):
        """Single SLAM update step"""

        dt = 0.1  # 10 Hz

        # 1. PREDICT: Update particle positions using odometry
        # (Odometry gives control commands from encoder differences)
        forward, rotation = self.odometry.estimate_motion(
            left_encoder_ticks, right_encoder_ticks
        )

        self.particle_filter.predict(
            control_linear=forward,
            control_angular=rotation
        )

        # 2. UPDATE: Correct particles using LIDAR observation
        def measurement_model(particle_pose, lidar_scan):
            """Compute likelihood of LIDAR scan given pose"""

            # For simplicity: scan matching
            # (In real SLAM: use feature-based or ICP matching)

            predicted_scan = self.occupancy_grid.predict_lidar(
                particle_pose
            )

            # Compare to actual scan
            distance_error = np.sum((predicted_scan - lidar_scan)**2)

            # Convert to probability (smaller error = higher probability)
            likelihood = np.exp(-distance_error / 100)

            return likelihood

        self.particle_filter.update(lidar_scan, measurement_model)

        # 3. RESAMPLE: Eliminate low-probability particles
        self.particle_filter.resample()

        # 4. MAP UPDATE: Update occupancy grid with best estimate
        best_pose = self.particle_filter.estimate_pose()
        self.occupancy_grid.update_from_lidar(best_pose, lidar_scan)

        return best_pose

    def get_map(self):
        """Return current map estimate"""
        return self.occupancy_grid.visualize()
```

## Real-World: Visual SLAM (Feature-Based)

Modern SLAM often uses **visual features** instead of LIDAR:

```python
class VisualSLAM:
    def __init__(self):
        self.feature_extractor = SIFT()  # Or ORB, AKAZE
        self.pose_graph = {}  # Poses and observations
        self.landmark_map = {}  # 3D landmark positions
        self.current_pose = np.eye(4)  # 4×4 transformation matrix

    def process_image(self, image, depth_image):
        """Process image for visual SLAM"""

        # 1. Extract features
        keypoints, descriptors = self.feature_extractor.detect_and_compute(image)

        # 2. Match to previous frame
        if hasattr(self, 'last_descriptors'):
            matches = self.match_features(descriptors, self.last_descriptors)

            # 3. Estimate motion (PnP: Perspective-n-Point)
            motion = self.estimate_motion_from_matches(
                matches, depth_image
            )

            # 4. Update pose
            self.current_pose = motion @ self.current_pose

        # 5. Create or update landmarks
        self.update_landmarks(keypoints, depth_image)

        # Store for next frame
        self.last_descriptors = descriptors

    def estimate_motion_from_matches(self, matches, depth_image):
        """Estimate camera motion from feature matches"""

        # Use matched features and depth to get 3D positions
        # Solve PnP problem to find camera transformation

        from cv2 import solvePnP

        object_points = []
        image_points = []

        for match in matches:
            kp1, kp2 = match
            # Get 3D position from depth
            x, y = int(kp1.pt[0]), int(kp1.pt[1])
            z = depth_image[y, x]

            if z > 0:
                object_points.append([x * z / 500, y * z / 500, z])
                image_points.append([kp2.pt[0], kp2.pt[1]])

        if len(object_points) > 4:
            success, rvec, tvec = solvePnP(
                np.array(object_points),
                np.array(image_points),
                camera_matrix=self.camera_intrinsics,
                distCoeffs=None
            )

            if success:
                # Convert rotation vector to matrix
                rotation_matrix, _ = cv2.Rodrigues(rvec)

                # Create 4×4 transformation matrix
                transformation = np.eye(4)
                transformation[:3, :3] = rotation_matrix
                transformation[:3, 3] = tvec

                return transformation

        return np.eye(4)  # No motion
```

## SLAM Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Loop closure** | Detect when robot revisits location, correct accumulated drift |
| **Dynamic environments** | Filter out moving objects, track only static features |
| **Low texture areas** | Use LIDAR + cameras for redundancy |
| **Computational cost** | Keyframe-based SLAM (process sparse subset of images) |
| **Initialization** | Stereo baseline or IMU for initial depth/motion |

## Week 6 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** why localization and mapping are coupled problems
2. **Implement** dead reckoning and understand its limitations
3. **Design** particle filter for probabilistic localization
4. **Build** occupancy grid maps from sensor data
5. **Integrate** localization + mapping into complete SLAM system
6. **Apply** SLAM to autonomous navigation

## Key Terminology

| Term | Definition |
|------|-----------|
| **SLAM** | Simultaneous Localization And Mapping |
| **Odometry** | Robot pose estimate from wheel encoders (drifts over time) |
| **Particle filter** | Probabilistic localization maintaining distribution over poses |
| **Occupancy grid** | 2D map grid where cells are occupied or free |
| **Loop closure** | Detecting revisited locations to correct drift |
| **Pose graph** | Network of robot poses connected by constraints |
| **Landmark** | Distinctive feature used for localization and mapping |
| **Scan matching** | Aligning sensor scans to estimate motion (ICP variant) |

## Discussion Questions

1. **Comparison**: When would you use particle filter SLAM vs. visual SLAM? What are tradeoffs?

2. **Error growth**: Dead reckoning error grows with distance (~1% per meter). What happens after 100m of travel?

3. **Loop closure**: Robot explores a square room and returns to start. How do you detect this? How do you use it to correct drift?

4. **Computational limits**: A robot processes 10 Hz LIDAR scans. Each scan takes 5ms to process. Is SLAM feasible?

## Hands-On Activity

**Implement simple particle filter localization**

1. Download a dataset with robot odometry + landmarks (KITTI, Freiburg dataset)
2. Implement particle filter:
   - Initialize particles randomly
   - Predict step (add odometry + noise)
   - Update step (compute likelihood based on landmarks)
   - Resample particles
3. Plot particle cloud over true trajectory
4. Measure accuracy (RMS error in meters)

## Resources for Deeper Learning

- **Book**: "Probabilistic Robotics" - Thrun, Burgard, Fox (definitive SLAM reference)
- **Framework**: ROS with package: `slam_toolbox`, `cartographer`
- **Course**: "Robot Mapping" - University of Freiburg (freely available)
- **Dataset**: Freiburg SLAM dataset with ground truth
- **Paper**: "ORB-SLAM: a Versatile and Accurate Monocular SLAM System" - Mur-Artal et al.

---

**Next**: Module 3 - Motion Planning & Navigation

💡 **Tip**: Visualize your particles! In low-quality visualizations, particles spread out uniformly. With good sensor data, they converge to the true pose.
