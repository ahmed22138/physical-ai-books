---
sidebar_position: 3
---

# Week 9: Mobile Robot Navigation

## Putting It All Together

Weeks 7-8 covered the individual components. This week, we integrate them into a complete **autonomous navigation system** that plans, follows trajectories, and reacts to obstacles in real-time.

## Part 1: Complete Navigation Stack

```
User Goal (x, y)
     ↓
[PERCEPTION LAYER]
  SLAM: Localization + Mapping
  → Robot pose estimate
  → Local occupancy grid
     ↓
[PLANNING LAYER]
  Path Planning: Find collision-free path
  → Waypoint sequence
     ↓
[CONTROL LAYER]
  Trajectory Planning: Add timing
  Collision Avoidance: React to obstacles
  → Velocity commands (v, ω)
     ↓
[EXECUTION LAYER]
  Motor Control: Apply commands
  → Wheel speeds, steering angles
     ↓
Robot Movement
```

### Complete Navigation System

```python
class AutonomousNavigator:
    def __init__(self):
        # Perception
        self.slam = SimpleSLAM()
        self.occupancy_grid = OccupancyGrid(width=50, height=50)

        # Planning
        self.path_planner = AStarPlanner()
        self.trajectory_planner = TrajectoryPlanner()

        # Control
        self.collision_avoider = DynamicWindowApproach()
        self.odometry = RobotOdometry()

        # State
        self.current_goal = None
        self.current_path = None
        self.path_index = 0
        self.last_replan_time = 0
        self.replan_interval = 1.0  # Replan every 1 second

    def navigate(self, goal_x, goal_y, sensors, dt=0.05):
        """Main navigation loop (20 Hz)"""

        # 1. PERCEPTION: Update pose and map
        pose, map_grid = self.update_perception(sensors, dt)

        # 2. PLANNING: Compute or update path
        if self.path_needs_replanning(pose, map_grid):
            self.current_path = self.path_planner.plan(
                pose[:2], (goal_x, goal_y), map_grid
            )
            self.path_index = 0
            self.last_replan_time = time.time()

        # 3. CONTROL: Compute velocity command
        if self.current_path:
            next_waypoint = self.current_path[self.path_index]

            # Get velocity that:
            # - Follows the path
            # - Avoids obstacles
            # - Respects acceleration limits

            v_cmd = self.collision_avoider.compute_velocity_command(
                pose, next_waypoint, sensors['obstacles']
            )

            # Check if waypoint reached
            distance_to_waypoint = np.linalg.norm(
                np.array(next_waypoint) - np.array(pose[:2])
            )

            if distance_to_waypoint < 0.2:  # Within 20cm
                self.path_index += 1

            # Check if goal reached
            distance_to_goal = np.linalg.norm(
                np.array([goal_x, goal_y]) - np.array(pose[:2])
            )

            if distance_to_goal < 0.3:
                return 'goal_reached', (0, 0)

            return 'navigating', v_cmd

        else:
            return 'no_path', (0, 0)

    def update_perception(self, sensors, dt):
        """Update SLAM and get current estimate"""

        lidar_scan = sensors['lidar']
        left_encoder = sensors['encoders']['left']
        right_encoder = sensors['encoders']['right']

        # Update SLAM
        pose = self.slam.step(left_encoder, right_encoder, lidar_scan)

        # Get current map
        map_grid = self.slam.occupancy_grid

        return pose, map_grid

    def path_needs_replanning(self, current_pose, map_grid):
        """Check if path is still valid"""

        time_since_replan = time.time() - self.last_replan_time

        if time_since_replan > self.replan_interval:
            return True

        if self.current_path is None:
            return True

        # Check if current path hits new obstacles
        for waypoint in self.current_path:
            if not map_grid.is_occupancy_free(waypoint[0], waypoint[1]):
                return True

        return False
```

## Part 2: Behavior-Based Navigation

For complex scenarios, use **behavior hierarchies**:

```python
class BehaviorTree:
    def __init__(self):
        self.behaviors = {
            'reach_goal': self.reach_goal,
            'avoid_obstacle': self.avoid_obstacle,
            'get_unstuck': self.get_unstuck,
            'idle': self.idle
        }

        self.stuck_timer = 0
        self.last_pose = None

    def execute(self, robot_state, sensors):
        """Execute behavior tree"""

        # Priority-based execution
        # Try behaviors in order, use first that returns valid command

        # Highest priority: Avoid immediate collision
        if self.is_in_danger(sensors):
            return self.avoid_obstacle(robot_state, sensors)

        # Check if stuck
        if self.is_stuck(robot_state):
            return self.get_unstuck(robot_state, sensors)

        # Normal operation: reach goal
        if robot_state['goal'] is not None:
            return self.reach_goal(robot_state, sensors)

        # Nothing to do
        return self.idle()

    def is_in_danger(self, sensors):
        """Check for imminent collision"""
        min_distance = np.min([obs['distance'] for obs in sensors['obstacles']])
        return min_distance < 0.3  # Less than 30cm

    def avoid_obstacle(self, robot_state, sensors):
        """Emergency obstacle avoidance"""
        # Find clear direction
        for angle in np.linspace(-np.pi, np.pi, 16):
            direction = (np.cos(angle), np.sin(angle))

            if self.direction_clear(sensors, direction):
                return (0.5, 0.5 * angle)  # Move and turn

        return (0, 1.0)  # Spin in place if trapped

    def is_stuck(self, robot_state):
        """Detect if robot is stuck"""
        if self.last_pose is None:
            self.last_pose = robot_state['pose']
            return False

        movement = np.linalg.norm(
            np.array(robot_state['pose'][:2]) -
            np.array(self.last_pose[:2])
        )

        if movement < 0.01:  # Less than 1cm movement
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0

        self.last_pose = robot_state['pose']

        return self.stuck_timer > 30  # Stuck for 1.5 seconds

    def get_unstuck(self, robot_state, sensors):
        """Recover from stuck state"""
        return (-0.5, 1.0)  # Back up and turn

    def reach_goal(self, robot_state, sensors):
        """Navigate to goal"""
        # Use path planning + collision avoidance
        # (Calls methods from AutonomousNavigator)
        pass

    def idle(self):
        """Do nothing"""
        return (0, 0)
```

## Part 3: Performance Metrics

How do we measure navigation quality?

```python
class NavigationMetrics:
    @staticmethod
    def path_length(path):
        """Total distance traveled"""
        length = 0
        for i in range(1, len(path)):
            length += np.linalg.norm(
                np.array(path[i]) - np.array(path[i-1])
            )
        return length

    @staticmethod
    def success_rate(trials):
        """Percentage of successful navigations"""
        successful = sum(1 for trial in trials if trial['reached_goal'])
        return successful / len(trials) * 100

    @staticmethod
    def average_time(trials):
        """Average time to reach goal"""
        successful_trials = [t for t in trials if t['reached_goal']]
        times = [t['time_taken'] for t in successful_trials]
        return np.mean(times) if times else float('inf')

    @staticmethod
    def smoothness(path):
        """Measure path smoothness (lower = smoother)"""
        angles = []

        for i in range(1, len(path)-1):
            v1 = np.array(path[i]) - np.array(path[i-1])
            v2 = np.array(path[i+1]) - np.array(path[i])

            angle = np.arccos(
                np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            )
            angles.append(angle)

        return np.std(angles)  # Standard deviation of turning angles

    @staticmethod
    def clearance(path, obstacles, min_margin=0.2):
        """Minimum clearance from obstacles"""
        min_clearance = float('inf')

        for pose in path:
            for obs in obstacles:
                distance = np.linalg.norm(
                    np.array(pose) - np.array(obs['position'])
                ) - obs['radius']

                min_clearance = min(min_clearance, distance)

        return max(0, min_clearance - min_margin)
```

## Real-World Deployment Checklist

```python
class NavigationValidator:
    @staticmethod
    def validate_navigation_system():
        """Checklist before real robot deployment"""

        checks = {
            'perception': {
                'slam_accuracy': self.test_slam_accuracy(),
                'map_quality': self.test_map_quality(),
                'localization_drift': self.test_drift(),
            },
            'planning': {
                'path_feasibility': self.test_paths_feasible(),
                'computation_time': self.test_planner_speed(),
                'completeness': self.test_completeness(),
            },
            'control': {
                'collision_avoidance': self.test_collision_avoidance(),
                'tracking_accuracy': self.test_trajectory_tracking(),
                'response_time': self.test_response_latency(),
            },
            'integration': {
                'end_to_end': self.test_end_to_end(),
                'failure_modes': self.test_failure_recovery(),
                'long_term_stability': self.test_long_duration(),
            }
        }

        all_pass = all(
            all(v for v in category.values())
            for category in checks.values()
        )

        return all_pass, checks
```

## Week 9 Learning Outcomes

By the end of this week, you should be able to:

1. **Integrate** perception, planning, and control into single system
2. **Design** behavior hierarchies for complex navigation
3. **Measure** navigation performance (success rate, path length, smoothness)
4. **Debug** navigation failures (stuck detection, replanning)
5. **Deploy** navigation to real robots safely
6. **Validate** system before field deployment

## Key Terminology

| Term | Definition |
|------|-----------|
| **Navigation stack** | Complete system: perception → planning → control |
| **Behavior tree** | Hierarchical decision structure for complex tasks |
| **Stuck detection** | Recognizing when robot makes no progress |
| **Replanning** | Recomputing path when obstacles block original path |
| **Clearance** | Minimum distance to obstacles along path |
| **Success rate** | Percentage of navigation attempts that reach goal |
| **Latency** | Delay between sensing and control command |

## Discussion Questions

1. **Safety**: A robot navigates near humans. How would you ensure safe behavior?

2. **Failure modes**: List 5 ways navigation could fail (sensor failure, stuck, etc.). How do you detect and recover from each?

3. **Real-time constraints**: Navigation must run at 20 Hz (50ms per cycle). Where would you optimize?

4. **Scalability**: Does the stack scale to large warehouses or complex urban environments?

## Hands-On Activity

**Test navigation in simulation**

1. Use Gazebo/ROS simulator with mobile robot
2. Create warehouse environment with obstacles
3. Command robot to 10 different goals
4. Measure for each: time, path length, success/failure
5. Report average metrics

## Resources for Deeper Learning

- **Framework**: ROS Navigation Stack - free, industry standard
- **Course**: "Mobile Robots" - UC Berkeley
- **Simulator**: Gazebo - free physics simulator
- **Paper**: "The Dynamic Window Approach to Collision Avoidance" - Fox et al.
- **Tool**: RViz - ROS visualization

---

**Next**: Module 4 - Integration & Advanced Topics

💡 **Tip**: Always test your navigation stack in simulation before deploying to a real robot!
