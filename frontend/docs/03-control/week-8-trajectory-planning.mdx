---
sidebar_position: 2
---

# Week 8: Trajectory Planning & Collision Avoidance

## Beyond Path to Trajectory

A **path** is a sequence of poses. A **trajectory** adds timing: when the robot should be at each pose.

This matters because:
- Physical robots can't instantly change direction
- Actuators have acceleration limits
- Collision avoidance requires speed management

## Part 1: Trajectory Generation

### Time-Optimal Trajectories

Maximize speed while respecting acceleration limits.

```python
class TrajectoryPlanner:
    def __init__(self, max_velocity=1.0, max_acceleration=0.5):
        """Initialize trajectory planner"""
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration

    def generate_trajectory(self, waypoints):
        """Generate time-optimal trajectory through waypoints"""

        trajectory = []

        for i in range(len(waypoints)-1):
            start = waypoints[i]
            end = waypoints[i+1]

            distance = np.linalg.norm(np.array(end) - np.array(start))

            # Compute time to traverse segment
            # Phase 1: Accelerate to max velocity
            time_to_max_v = self.max_velocity / self.max_acceleration
            distance_accel = 0.5 * self.max_acceleration * time_to_max_v**2

            if distance <= 2 * distance_accel:
                # Can't reach max velocity
                t_max = 2 * np.sqrt(distance / self.max_acceleration)
                v_max = self.max_acceleration * t_max / 2
            else:
                # Can reach max velocity
                distance_cruise = distance - 2 * distance_accel
                time_cruise = distance_cruise / self.max_velocity
                t_max = 2 * time_to_max_v + time_cruise
                v_max = self.max_velocity

            # Generate waypoints along trajectory
            dt = 0.01  # 100 Hz
            for t in np.arange(0, t_max, dt):
                if t <= time_to_max_v:
                    # Acceleration phase
                    v = self.max_acceleration * t
                    s = 0.5 * self.max_acceleration * t**2

                elif t <= t_max - time_to_max_v:
                    # Cruise phase
                    s = distance_accel + v_max * (t - time_to_max_v)
                    v = v_max

                else:
                    # Deceleration phase
                    t_decel = t_max - t
                    v = self.max_acceleration * t_decel
                    s = distance - 0.5 * self.max_acceleration * t_decel**2

                # Interpolate position
                direction = (np.array(end) - np.array(start)) / distance
                pose = np.array(start) + direction * s

                trajectory.append({
                    'pose': pose,
                    'velocity': v,
                    'time': t
                })

        return trajectory
```

## Part 2: Dynamic Window Approach (DWA)

For reactive collision avoidance at high frequencies (e.g., 20 Hz).

```python
class DynamicWindowApproach:
    def __init__(self, max_velocity=1.0, max_rotation=np.pi, max_accel=0.5):
        self.max_velocity = max_velocity
        self.max_rotation = max_rotation
        self.max_accel = max_accel
        self.last_velocities = (0, 0)  # (linear, angular)

    def compute_velocity_command(self, robot_pose, goal, obstacles, dt=0.1):
        """Compute optimal velocity command"""

        # 1. Dynamic Window: velocities robot can reach in next dt
        min_v = max(self.last_velocities[0] - self.max_accel * dt, -self.max_velocity)
        max_v = min(self.last_velocities[0] + self.max_accel * dt, self.max_velocity)

        min_w = max(self.last_velocities[1] - self.max_accel * dt, -self.max_rotation)
        max_w = min(self.last_velocities[1] + self.max_accel * dt, self.max_rotation)

        # 2. Sample velocity combinations
        best_score = -float('inf')
        best_velocity = (0, 0)

        for v in np.linspace(min_v, max_v, 5):
            for w in np.linspace(min_w, max_w, 5):

                # 3. Evaluate trajectory
                collision_risk = self.collision_risk(robot_pose, v, w, obstacles)

                if collision_risk > 0.5:  # Too risky
                    continue

                # Distance to goal
                goal_dist = self.trajectory_distance_to_goal(
                    robot_pose, v, w, goal, dt
                )

                # Score: minimize distance, avoid obstacles
                score = (1.0 - collision_risk) - goal_dist / 10

                if score > best_score:
                    best_score = score
                    best_velocity = (v, w)

        self.last_velocities = best_velocity
        return best_velocity

    def collision_risk(self, pose, v, w, obstacles, time_horizon=1.0):
        """Compute collision risk for velocity command"""

        x, y, theta = pose
        min_distance = float('inf')

        # Simulate trajectory
        for t in np.linspace(0, time_horizon, 10):
            # Kinematic model
            x_t = x + v * np.cos(theta) * t
            y_t = y + v * np.sin(theta) * t

            # Check distance to obstacles
            for obs in obstacles:
                obs_x, obs_y, obs_r = obs
                distance = np.sqrt((x_t - obs_x)**2 + (y_t - obs_y)**2)
                min_distance = min(min_distance, distance - obs_r)

        # Convert to risk [0, 1]
        risk = max(0, 1 - min_distance / 0.5)  # 0.5m safety margin
        return risk
```

## Part 3: MPC (Model Predictive Control)

Plan ahead while respecting constraints.

```python
class ModelPredictiveController:
    def __init__(self, prediction_horizon=10, control_horizon=3):
        self.prediction_horizon = prediction_horizon
        self.control_horizon = control_horizon

    def compute_control(self, current_state, reference_trajectory, constraints):
        """
        Solve optimal control problem:
        minimize: trajectory_tracking_error + control_effort
        subject to: dynamics, velocity limits, collision avoidance
        """

        # This is simplified; real MPC uses optimization solvers (CVXPY, Gurobi)

        optimal_control = []

        for i in range(self.control_horizon):
            # Predict next states
            predicted_states = self.predict_states(
                current_state, i, reference_trajectory
            )

            # Find control minimizing cost
            for u_candidate in self.candidate_controls():

                cost = self.compute_cost(predicted_states, u_candidate)

                if self.satisfies_constraints(predicted_states, constraints):
                    optimal_control.append(u_candidate)
                    break

        return optimal_control[0] if optimal_control else (0, 0)
```

## Real-World: Mobile Robot Navigation

```python
class MobileRobotNavigator:
    def __init__(self):
        self.path_planner = AStarPlanner()
        self.trajectory_planner = TrajectoryPlanner()
        self.collision_avoider = DynamicWindowApproach()

    def navigate_to_goal(self, robot_pose, goal, map_grid, dynamic_obstacles):
        """Complete navigation pipeline"""

        # 1. PLAN: Path planning (static obstacles)
        path = self.path_planner.plan(robot_pose[:2], goal, map_grid)

        if not path:
            return None

        # 2. TRAJECTORY: Generate smooth trajectory
        trajectory = self.trajectory_planner.generate_trajectory(path)

        # 3. EXECUTE: Follow trajectory with collision avoidance
        control_commands = []

        for waypoint in trajectory:
            # Get velocity command that follows trajectory
            # but avoids dynamic obstacles
            v_cmd = self.collision_avoider.compute_velocity_command(
                robot_pose, waypoint['pose'], dynamic_obstacles
            )

            control_commands.append(v_cmd)

        return control_commands
```

## Week 8 Learning Outcomes

By the end of this week, you should be able to:

1. **Design** time-optimal trajectories respecting limits
2. **Implement** reactive collision avoidance (DWA)
3. **Apply** Model Predictive Control for constrained motion
4. **Combine** path planning + trajectory planning + collision avoidance
5. **Analyze** tradeoffs between optimality and real-time performance
6. **Test** navigation in dynamic environments

## Key Terminology

| Term | Definition |
|------|-----------|
| **Trajectory** | Path with timing information |
| **Dynamic Window** | Set of velocities robot can reach |
| **Collision risk** | Probability of collision given trajectory |
| **MPC** | Model Predictive Control - look-ahead optimization |
| **Kinematic model** | How velocity commands translate to pose changes |
| **Smoothing** | Removing sharp turns from paths |
| **Reactive control** | High-frequency feedback response to obstacles |

## Discussion Questions

1. **Real-time vs optimal**: Would you use time-optimal planning (slow, optimal) or reactive DWA (fast, suboptimal)?

2. **Prediction**: DWA predicts 1 second into future. What happens with faster obstacles?

3. **Safety margin**: How much clearance should robot maintain from obstacles?

---

**Next**: Week 9 - Mobile Robot Navigation

💡 **Tip**: Test your trajectory planner on recorded robot logs. Compare planned vs. actual paths!
