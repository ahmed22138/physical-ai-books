---
sidebar_position: 2
---

# Week 2: Robot Anatomy & Sensors

## Introduction to Robot Hardware

Welcome to Week 2! Last week, we explored the philosophical foundations of embodied AI. This week, we ground ourselves in the physical reality of robots—the hardware systems that give embodied AI systems their power to perceive and act.

### What You'll Learn

In this lesson, we'll examine:
- **Robotic kinematics**: How robots move and position themselves
- **Sensor types**: The eyes, ears, and touch receptors of robots
- **Actuators**: The muscles that make robots move
- **Real-world robot architectures**: Complete systems built from these components

## Part 1: Robotic Kinematics & Structure

### Degrees of Freedom (DOF)

A robot's **degree of freedom** is each independent way it can move. Understanding DOF is critical for understanding what tasks a robot can accomplish.

**Example: A robot arm picking up a water bottle**

```
Joint 1 (Base rotation)     → Rotate around vertical axis
Joint 2 (Shoulder)          → Move arm up/down
Joint 3 (Elbow)             → Bend/extend forearm
Joint 4 (Wrist rotation)    → Twist wrist
Joint 5 (Wrist bend)        → Tilt wrist up/down
Joint 6 (Gripper rotation)  → Rotate end effector
Gripper (End effector)      → Open/close fingers
```

This arm has **7 DOF** (6 joints + gripper), making it highly dexterous.

### Common Robot Morphologies

| Robot Type | DOF | Example | Common Tasks |
|-----------|-----|---------|--------------|
| **Industrial Arm** | 6-7 | FANUC CRX | Assembly, welding, palletizing |
| **Mobile Manipulator** | 7-12 | Boston Dynamics Stretch | Bin picking, shelf organization |
| **Humanoid** | 20-40 | Tesla Optimus | General manipulation, navigation |
| **Quadruped** | 12-16 | Boston Dynamics Spot | Inspection, rough terrain, mapping |
| **Aerial (Drone)** | 4-6 | DJI M300 | Inspection, delivery, surveillance |

### Kinematic Chains

A robot's joints form a **kinematic chain**—a sequence of connected links. Two main types exist:

**1. Serial Chains** (most common in manipulators)
```
Base ← Joint1 ← Link1 ← Joint2 ← Link2 ← ... ← End Effector
```
- Advantages: Simple control, long reach
- Disadvantages: Less stiff, can only reach positions in workspace

**2. Parallel Chains** (found in specialized systems)
```
      ← Joint1 ←
Base ←  Joint2  ← End Effector
      ← Joint3 ←
```
- Advantages: Higher stiffness, faster
- Disadvantages: Limited workspace, complex control

### Workspace Analysis

Every robot has a **workspace**—the region in 3D space its end effector can reach.

```python
# Pseudo-code: Computing robot workspace
class RobotArm:
    def compute_workspace(self, joint_limits):
        """
        Calculate reachable positions by sampling joint configurations
        """
        workspace_points = []

        # Sample all joint angle combinations
        for theta1 in range(-90, 90, 5):
            for theta2 in range(-45, 135, 5):
                for theta3 in range(-90, 90, 5):
                    # Forward kinematics: calculate end-effector position
                    end_effector = self.forward_kinematics(
                        [theta1, theta2, theta3]
                    )
                    workspace_points.append(end_effector)

        return workspace_points

    def forward_kinematics(self, joint_angles):
        """Calculate end-effector position from joint angles"""
        # Use Denavit-Hartenberg parameters to compute positions
        pass
```

## Part 2: Robot Sensors

Sensors are how robots perceive their world. They convert physical phenomena into digital signals.

### Vision Systems

**RGB Cameras**
- Capture color images at 30-60 FPS
- Used for object detection and scene understanding
- Passive (no active illumination needed)
- Challenge: Doesn't directly measure depth

**Depth Cameras** (RGB-D)
- Measure distance to objects using infrared or time-of-flight (ToF)
- Return 3D point clouds (~30,000 points per frame)
- Examples: Intel RealSense, Azure Kinect
- Challenge: Struggles with reflective or transparent surfaces

**Example: Object Detection from RGB-D**

```python
class VisionSystem:
    def detect_bottle(self, rgb_image, depth_image):
        """Detect water bottle in scene"""

        # 1. Convert RGB to HSV for color-based segmentation
        hsv = convert_rgb_to_hsv(rgb_image)

        # 2. Segment blue pixels (water bottle color)
        bottle_mask = extract_color_range(hsv,
            hue_min=200, hue_max=240,  # Blue range
            sat_min=50, sat_max=255,
            val_min=50, val_max=255
        )

        # 3. Find contours in mask
        contours = find_contours(bottle_mask)

        # 4. For each contour, extract 3D position from depth
        bottles_in_3d = []
        for contour in contours:
            # Get depth values within contour
            depths = depth_image[contour]
            avg_depth = mean(depths)

            # Convert pixel coordinates to 3D world position
            x, y = get_centroid(contour)
            position_3d = pixel_to_world(x, y, avg_depth)

            bottles_in_3d.append({
                "position": position_3d,
                "confidence": calculate_confidence(contour),
                "size": get_bounding_box(contour)
            })

        return bottles_in_3d
```

### Tactile Sensors

**Force/Torque Sensors** (F/T sensors)
- Measure forces (Fx, Fy, Fz) and torques (Rx, Ry, Rz)
- Typically mounted at wrist or gripper
- Enable **compliant manipulation** (soft, adaptive grasping)
- Sampling rate: 100-1000 Hz

**Tactile Array Sensors**
- Multiple pressure sensors on gripper fingers
- Detect contact pressure distribution
- Help determine if object is slipping
- Used for in-hand manipulation

**Tactile Sensor Application: Delicate Grasping**

```python
class GripperController:
    def grasp_fragile_object(self, target_force=5.0):
        """Grasp object while monitoring force feedback"""

        # Start with open gripper
        self.gripper.open()

        while True:
            # Read current force
            current_force = self.force_sensor.read_force()

            # Check for slipping (force increase without gripper closing)
            if self.force_sensor.is_slipping():
                # Object slipping! Close gripper slightly more
                self.gripper.close(increment=0.1)
                continue

            # Check for successful grasp
            if current_force >= target_force:
                # Successfully grasped
                return True

            # Not yet sufficient force - close gripper more
            self.gripper.close(increment=0.2)
```

### Proprioceptive Sensors

**Joint Encoders**
- Measure the angle of each joint
- Absolute: Report actual position (even after power-off)
- Incremental: Track changes from reference position
- Resolution: 12-16 bits typically

**Inertial Measurement Unit (IMU)**
- Measures acceleration (accelerometer: 3 axes)
- Measures rotation rate (gyroscope: 3 axes)
- Measures magnetic field (magnetometer: 3 axes)
- Critical for mobile robots and humanoids to estimate orientation

**IMU in Mobile Robot Navigation**

```python
class MobileRobotIMU:
    def estimate_orientation(self):
        """Use IMU to estimate robot's current orientation"""

        # Read sensor values
        accel = self.imu.read_accelerometer()  # [x, y, z] m/s²
        gyro = self.imu.read_gyroscope()       # [x, y, z] rad/s

        # Accelerometer gives gravity direction (down)
        # Use it to estimate pitch and roll
        pitch = atan2(accel.x, sqrt(accel.y² + accel.z²))
        roll = atan2(accel.y, sqrt(accel.x² + accel.z²))

        # Gyroscope gives rotation rates
        # Integrate to get yaw (heading)
        self.yaw += gyro.z * dt

        # Combine for robust orientation
        orientation = {
            "roll": roll,
            "pitch": pitch,
            "yaw": self.yaw
        }

        return orientation
```

### LIDAR (Light Detection and Ranging)

- Active laser scanning to measure distances
- Returns point cloud of entire environment
- High precision and range (up to 200m)
- Mostly unaffected by lighting conditions
- Used for SLAM (Simultaneous Localization and Mapping)

**Advantages over RGB-D:**
- Longer range
- Works in bright sunlight
- Better for outdoors

**LIDAR Application: Obstacle Detection**

```python
class LidarObstacleDetector:
    def detect_obstacles(self, lidar_scan):
        """Find obstacles from LIDAR point cloud"""

        obstacles = []

        for point in lidar_scan.points:
            x, y, z = point.position

            # Check if point is at robot height (z ≈ 0.5m)
            if 0.2 < z < 1.0:
                # Convert to grid cell
                grid_x = int(x / 0.1)  # 10cm resolution
                grid_y = int(y / 0.1)

                # Mark as occupied
                self.occupancy_grid[grid_x, grid_y] = 1

                # If cluster of occupied cells, it's an obstacle
                if self.is_large_cluster(grid_x, grid_y):
                    obstacle = {
                        "position": point.position,
                        "distance": sqrt(x² + y²),
                        "size": self.estimate_size(grid_x, grid_y)
                    }
                    obstacles.append(obstacle)

        return obstacles
```

## Part 3: Robot Actuators

Actuators convert electrical signals into physical motion.

### Motor Types

| Motor Type | Torque Range | Speed | Efficiency | Use Case |
|-----------|--------------|-------|-----------|----------|
| **DC Motor** | Low-Medium | High | 80-90% | Wheels, simple joints |
| **Servo Motor** | Medium | Medium | 70-80% | Precise positioning |
| **Stepper Motor** | Low | Low-Medium | 50-70% | Accurate steps, 3D printers |
| **BLDC Motor** | Medium-High | High | 85-95% | Drones, fast joints |
| **Harmonic Drive** | Very High | Low | 75-85% | Robot arms, precision |

### Gripper Types

**Parallel Jaw Gripper**
```
Finger ←―――→ Finger
        Object
```
- Simple, fast (0.5-2 sec close)
- Limited grasp strategies
- Best for: Box picking, bin picking

**Adaptive Gripper**
```
   ╱─╲
  ╱   ╲    Fingers conform to object shape
 ╱     ╲
```
- Fingers adjust to object shape
- Slower but more robust
- Best for: Unknown objects, delicate items

**Suction Gripper**
```
  ╔════╗
  ║Pump║→ Vacuum
  ╚════╝

  ╱─────╲
 │Suction │ Creates adhesion
 │ Cups   │
  ╲─────╱
```
- Fast, gentle
- Works on smooth surfaces
- Best for: Flat objects, food, boxes

### Control Architecture

```
┌──────────────────────────────────┐
│   High-Level Planning Layer      │
│  (Goal: Pick up water bottle)    │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│   Mid-Level Motion Planning      │
│  (Generate arm trajectory)       │
└────────────┬─────────────────────┘
             │
┌────────────▼──────────────────────┐
│  Low-Level Joint Control (PID)   │
│  (Command motor speeds/torques)  │
└────────────┬──────────────────────┘
             │
┌────────────▼──────────────────────┐
│    Motor Drivers & Hardware       │
│  (Power electronics)              │
└──────────────────────────────────┘
```

## Real-World Example: Picking a Bottle

Let's tie everything together with a complete picking scenario:

```python
class BottlePickingRobot:
    def __init__(self):
        self.vision = VisionSystem()
        self.arm = RobotArm()
        self.gripper = Gripper()
        self.force_sensor = ForceSensor()

    def pick_bottle(self):
        """Complete picking sequence"""

        # 1. SENSE: Perceive bottle location
        print("📷 Capturing image...")
        rgb, depth = self.vision.capture()
        bottles = self.vision.detect_bottle(rgb, depth)

        if not bottles:
            return False

        target = bottles[0]  # Pick closest bottle
        print(f"🔍 Found bottle at {target['position']}")

        # 2. THINK: Plan trajectory to bottle
        print("🤖 Planning trajectory...")
        approach_pose = self._compute_approach_pose(target)
        grasp_pose = self._compute_grasp_pose(target)

        # 3. ACT: Move arm to bottle
        print("➡️  Moving to approach pose...")
        self.arm.move_to(approach_pose, duration=2.0)

        # 4. SENSE: Verify we're close
        current_depth = self.vision.get_depth_at_center()
        if abs(current_depth - target['distance']) > 0.05:
            print("⚠️  Distance mismatch - recalibrating...")
            target = self.vision.detect_bottle(rgb, depth)[0]

        # 5. ACT: Move to grasp pose
        print("➡️  Moving to grasp pose...")
        self.arm.move_to(grasp_pose, duration=1.0)

        # 6. ACT: Close gripper
        print("✋ Grasping...")
        success = self.gripper.grasp_fragile_object(target_force=5.0)

        if not success:
            print("❌ Grasp failed - object too small or slipped")
            self.gripper.open()
            return False

        # 7. SENSE: Verify grasp with force sensor
        grasp_force = self.force_sensor.read_force()
        print(f"✅ Grasped with force: {grasp_force} N")

        # 8. ACT: Lift bottle
        print("⬆️  Lifting...")
        self.arm.move_to(grasp_pose + [0, 0, 0.3], duration=1.0)

        return True

    def _compute_approach_pose(self, target):
        """Compute pose 15cm above bottle"""
        return target['position'] + [0, 0, 0.15]

    def _compute_grasp_pose(self, target):
        """Compute pose for grasping bottle"""
        return target['position']
```

## Sensor Fusion

Real robots don't rely on a single sensor. They combine multiple sensor inputs for robust perception.

```python
class SensorFusion:
    def estimate_robot_state(self):
        """Combine multiple sensors for robust state estimate"""

        # From IMU: rough orientation
        imu_yaw = self.imu.estimate_yaw()

        # From wheel encoders: rough distance traveled
        encoder_x, encoder_y = self.encoders.get_displacement()

        # From LIDAR: precise position relative to known map
        lidar_pose = self.lidar_localization.get_pose()

        # Fuse with weights: LIDAR most reliable, IMU supplements
        fused_pose = {
            "x": 0.8 * lidar_pose.x + 0.2 * encoder_x,
            "y": 0.8 * lidar_pose.y + 0.2 * encoder_y,
            "theta": 0.7 * lidar_pose.theta + 0.3 * imu_yaw
        }

        return fused_pose
```

## Week 2 Learning Outcomes

By the end of this week, you should be able to:

1. **Define** degrees of freedom and explain how they constrain robot capabilities
2. **Calculate** the forward kinematics for a simple 2-DOF robot arm
3. **Compare** different sensor types and explain when to use each (RGB-D vs LIDAR vs IMU)
4. **Design** a sensor suite for a specific robotic task (e.g., bin picking, navigation)
5. **Implement** basic sensor fusion to combine multiple sensor inputs
6. **Analyze** a robot architecture and identify sensing and actuation bottlenecks

## Key Terminology

| Term | Definition |
|------|-----------|
| **Degree of Freedom (DOF)** | Independent way a robot can move; each joint contributes 1 DOF |
| **End Effector** | Tool at the end of robot arm (gripper, sensor, etc.) |
| **Workspace** | All positions reachable by robot's end effector |
| **Kinematics** | Study of motion without considering forces |
| **Point Cloud** | 3D data represented as collection of points (x, y, z) |
| **SLAM** | Simultaneous Localization and Mapping—navigating while building a map |
| **Actuator** | Device that converts electrical signal to mechanical motion |
| **Sensor Fusion** | Combining multiple sensor inputs for robust estimates |

## Discussion Questions

1. **Tradeoffs**: Why might an engineer choose a 6-DOF arm for a task instead of a 7-DOF arm? What's the advantage of fewer joints?

2. **Sensor Selection**: You're designing a robot to pick ripe tomatoes in a greenhouse. What sensors would you use and why? What about picking boxes in a warehouse?

3. **Real-time Constraints**: A robot's sensor captures depth images at 30 Hz. Why might processing all images in real-time be impossible? What strategies could help?

4. **Graceful Degradation**: If your LIDAR fails, how could your robot continue moving safely using only wheel encoders and IMU?

## Hands-On Activity

**Reverse Engineering a Robot**

Find a YouTube video of an industrial robot (e.g., FANUC, ABB, KUKA) performing a task. Watch carefully and:
1. Count the number of joints (DOF)
2. Identify the sensors you can observe
3. Sketch the kinematic chain
4. Describe the gripper type and actuation
5. Estimate the workspace size

Document your analysis in a short paragraph (200 words).

## Resources for Deeper Learning

- **Book**: "Introduction to Robotics" - John J. Craig (Chapters 2-3 on kinematics)
- **Video**: "Robot Arm Kinematics Explained" - MATLAB Tech Talks
- **Tool**: ROS Visualization Tools (`rviz`) for point clouds and sensor data
- **Paper**: "A Survey of Robot Manipulation" - Siciliano & Khatib
- **Interactive**: OpenDynamics - simulate kinematics in browser

---

**Next**: Week 3 - Control Systems Basics

💡 **Tip**: Try computing forward kinematics by hand for a 2-joint arm. Use simple trigonometry to find the end effector position for different joint angles!
