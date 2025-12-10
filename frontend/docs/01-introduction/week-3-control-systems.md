---
sidebar_position: 3
---

# Week 3: Control Systems Basics

## Introduction to Robot Control

You now understand robot anatomy and sensors. This week, we explore the **control systems** that coordinate all these components into purposeful action. Control theory is the bridge between sensing and acting.

### The Fundamental Challenge

Imagine you command a robot arm to move to a target position. What actually happens?

1. You specify: "Move to position [0.5m, 0.3m, 0.8m]"
2. The controller computes: "Joint 1 should rotate 45°, Joint 2 should extend 0.2m, etc."
3. The motors receive power and start rotating
4. But motors don't stop exactly where they should—they overshoot or undershoot
5. Sensors report actual position, which differs from target

**This is where control systems come in:** They continuously adjust motor commands based on sensory feedback to reach and maintain desired positions.

## Part 1: Closed-Loop Control Fundamentals

### The PID Controller

The most common control algorithm in robotics is the **PID controller** (Proportional-Integral-Derivative).

```
Desired State → [PID Controller] → Motor Command → [Robot Actuator] → Actual State
                      ↑                                                    ↓
                      └────────────── Sensor Feedback ──────────────────┘
```

### How PID Works

**Proportional (P) Term:**
```
Error = Desired Position - Actual Position
Command = Kp × Error
```

If the robot is 10cm away from target:
- Proportional term says: "Push harder the farther away you are"
- Problem: Steady-state error (robot stops slightly before reaching target)

**Integral (I) Term:**
```
IntegratedError = sum of all past errors over time
Command += Ki × IntegratedError
```

- Accumulates error over time
- Eliminates steady-state error
- Problem: Can cause oscillations if Kp is too high

**Derivative (D) Term:**
```
ErrorRate = (Current Error - Previous Error) / dt
Command += Kd × ErrorRate
```

- Predicts future error based on rate of change
- Dampens oscillations (like adding friction)
- Makes system respond smoothly

### Complete PID Formula

```
Command = Kp × Error + Ki × ∫Error + Kd × (dError/dt)
```

### PID Control Example

```python
class PIDController:
    def __init__(self, kp, ki, kd):
        """Initialize PID gains"""
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.integral = 0
        self.prev_error = 0
        self.dt = 0.01  # Control loop runs at 100 Hz

    def compute(self, desired, actual):
        """Compute motor command based on error"""

        # Calculate error
        error = desired - actual

        # Proportional term
        p_term = self.kp * error

        # Integral term (with anti-windup)
        self.integral += error * self.dt
        if abs(self.integral) > 10:  # Limit integral wind-up
            self.integral = 10 if self.integral > 0 else -10
        i_term = self.ki * self.integral

        # Derivative term
        d_term = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error

        # Compute command
        command = p_term + i_term + d_term

        # Saturate command to motor limits
        command = max(-1.0, min(1.0, command))

        return command
```

### Tuning PID Gains

Tuning Kp, Ki, Kd is both art and science. **Ziegler-Nichols method** is a systematic approach:

```
1. Set Ki=0, Kd=0
2. Increase Kp until system oscillates continuously
3. Note the oscillation period (Pu) and critical gain (Kcu)
4. Apply formula:
   Kp = 0.6 × Kcu
   Ki = 1.2 × Kcu / Pu
   Kd = 0.075 × Kcu × Pu
```

**Visual Tuning Guide:**

| Issue | Solution |
|-------|----------|
| System undershoots (too slow) | Increase Kp |
| System oscillates (overshoot) | Decrease Kp or increase Kd |
| Steady-state error exists | Increase Ki |
| Response too slow | Increase Kd |
| System unstable/jerky | Decrease all gains |

## Part 2: Multi-Joint Coordination

Real robots have multiple joints. Each joint needs its own PID controller, but they must coordinate.

### Independent Joint Control

The simplest approach: one PID per joint, no coordination.

```python
class RobotArm:
    def __init__(self):
        self.joint_controllers = [
            PIDController(kp=10, ki=2, kd=1),
            PIDController(kp=8, ki=1.5, kd=0.8),
            PIDController(kp=7, ki=1, kd=0.5),
        ]
        self.joint_angles = [0, 0, 0]

    def move_to_angles(self, target_angles):
        """Move all joints to target angles"""

        # Control loop
        for _ in range(1000):  # Run for 10 seconds at 100 Hz

            # For each joint, compute and apply PID command
            joint_commands = []
            for i, controller in enumerate(self.joint_controllers):
                command = controller.compute(
                    target_angles[i],
                    self.joint_angles[i]
                )
                joint_commands.append(command)
                self.motors[i].set_command(command)

            # Read back actual angles from encoders
            self.joint_angles = self.read_joint_angles()

            time.sleep(0.01)  # 100 Hz control rate
```

### Cartesian Control (Inverse Kinematics)

Sometimes you want to control the robot's **end effector** in Cartesian space (x, y, z) rather than joint angles.

```
Goal: Move end effector to [0.5m, 0.3m, 0.8m]
↓ Inverse Kinematics
Target Joint Angles: [45°, 60°, 30°]
↓ Joint PID Controllers
Joint Commands sent to motors
```

**Inverse Kinematics Challenge:**

```python
class InverseKinematics:
    def solve_ik(self, target_position):
        """
        Find joint angles that result in target end effector position
        This is computationally expensive!
        """

        # For 3-joint arm: multiple solutions can exist
        # You need to choose one (e.g., minimum joint motion)

        # Method 1: Analytical solution (if math is tractable)
        # For specific robot geometry, may have closed-form equations
        joint_angles = self.analytical_solution(target_position)

        # Method 2: Numerical optimization (if no closed form exists)
        # Use gradient descent to find angles that match target
        joint_angles = self.numerical_optimize(target_position)

        return joint_angles

    def analytical_solution(self, target_pos):
        """Closed-form solution for 3-joint planar arm"""
        x, y = target_pos[0], target_pos[1]

        # Using law of cosines and trigonometry
        # (specific to this robot's geometry)
        theta3 = acos((x**2 + y**2 - L1**2 - L2**2) / (2*L1*L2))
        theta2 = atan2(y, x) - atan2(L2*sin(theta3), L1+L2*cos(theta3))
        theta1 = 0  # Simplified

        return [theta1, theta2, theta3]
```

## Part 3: Practical Control Architectures

### Trajectory Tracking Control

Moving smoothly from point A to point B while avoiding jerky motions:

```python
class TrajectoryController:
    def move_smoothly(self, start_pos, end_pos, duration=2.0):
        """
        Generate smooth trajectory and track it
        Uses 5th-order polynomial for smooth acceleration/deceleration
        """

        # Generate trajectory: position, velocity, acceleration over time
        timestamps = []
        positions = []
        velocities = []

        for t in range(int(duration * 100)):  # 100 Hz
            tau = t / (duration * 100)  # Normalized time [0, 1]

            # 5th order polynomial: smooth acceleration
            s = 10*tau**3 - 15*tau**4 + 6*tau**5
            s_dot = (30*tau**2 - 60*tau**3 + 30*tau**4) / duration
            s_ddot = (60*tau - 180*tau**2 + 120*tau**3) / (duration**2)

            pos = start_pos + s * (end_pos - start_pos)
            vel = s_dot * (end_pos - start_pos)

            timestamps.append(t * 0.01)
            positions.append(pos)
            velocities.append(vel)

        # Now track this trajectory with feedback control
        for i, (pos_target, vel_target) in enumerate(zip(positions, velocities)):

            # Feedforward: use desired velocity to improve tracking
            # Feedback: use PID to correct for errors

            error = pos_target - self.get_actual_position()
            feedforward = vel_target
            feedback = self.pid_controller.compute(error)

            command = feedforward + feedback

            self.set_motor_command(command)
            time.sleep(0.01)
```

### Impedance Control (Compliant Robots)

When robots must work near humans or handle delicate objects, they need **compliant control**—they should give way when touched, like a spring.

```python
class ImpedanceController:
    def __init__(self):
        self.stiffness = 1000      # Spring constant (N/m)
        self.damping = 100         # Friction coefficient (N⋅s/m)
        self.target_pos = 0

    def compute_command(self, actual_pos, actual_vel, external_force):
        """
        Like a spring-damper system:
        Force = -Stiffness × Error - Damping × Velocity
        """

        # Calculate desired force based on position error
        error = self.target_pos - actual_pos
        spring_force = self.stiffness * error

        # Add damping to smooth motion
        damping_force = -self.damping * actual_vel

        # Account for external forces (contact with human)
        total_force = spring_force + damping_force + external_force

        # Convert force to motor command
        command = total_force / self.motor_constant

        return command
```

**Benefits of Impedance Control:**
- If human pushes on robot, it moves away (safety)
- If robot pushes against wall, it stops (contact awareness)
- Energy efficient (robot absorbs disturbances rather than fighting them)

## Part 4: Stability & Performance Metrics

### Stability

A **stable** system converges to desired state and doesn't oscillate forever.

```
Unstable:              Marginally Stable:      Stable (Underdamped):
   │                        │                          │
   │      ╱                  │  ──────                  │    ╱‾‾‾
   │    ╱                    │                         │  ╱╱
   │  ╱                      │                         │╱
   └──────────              └──────────               └──────────
```

**Nyquist Criterion** and **Bode Plots** are mathematical tools for analyzing stability, but practically:
- If gains are too high → oscillations (instability)
- If gains are too low → slow response, won't reach target
- Balanced tuning → stable, fast response

### Performance Metrics

| Metric | Definition | Ideal Value |
|--------|-----------|------------|
| **Rise Time (tr)** | Time to reach 90% of target | Fast (0.1-1s) |
| **Overshoot (OS)** | Max excess beyond target | &lt;5% |
| **Settling Time (ts)** | Time to stay within 2% of target | Fast (&lt; 10 × tr) |
| **Steady-State Error (ess)** | Final error after settling | 0 |

```python
class PerformanceAnalyzer:
    def analyze_response(self, time_series, target_value):
        """Measure control performance metrics"""

        steady_state_value = time_series[-1]
        peak_value = max(time_series)
        overshoot = ((peak_value - target_value) / target_value) * 100

        # Rise time: when does signal reach 90% of target?
        rise_indices = [i for i, v in enumerate(time_series)
                       if v >= 0.9 * target_value]
        rise_time = rise_indices[0] * dt if rise_indices else float('inf')

        # Settling time: when does signal stay within 2% of target?
        settled_indices = [i for i, v in enumerate(time_series[int(rise_time/dt):])
                          if abs(v - target_value) < 0.02 * target_value]
        settling_time = (int(rise_time/dt) + settled_indices[0]) * dt

        steady_state_error = abs(steady_state_value - target_value)

        return {
            "rise_time": rise_time,
            "overshoot": overshoot,
            "settling_time": settling_time,
            "steady_state_error": steady_state_error
        }
```

## Real-World Example: Walking Robot Control

Let's see control systems in action for a quadruped robot walking:

```python
class QuadrupedGaitController:
    def __init__(self):
        # Each leg has 3 joints: hip, knee, ankle
        # Each joint has a PID controller
        self.leg_controllers = [
            [PIDController(10, 2, 1) for _ in range(3)]
            for _ in range(4)  # 4 legs
        ]

    def walk_forward(self, speed=0.5):  # 0.5 m/s
        """Generate walking gait and control legs"""

        phase = 0
        while True:
            # Compute desired joint angles for each leg
            # based on gait phase (0 to 1)

            for leg_id in range(4):
                # Quadruped trot gait:
                # - Front-left and back-right legs move together
                # - Then front-right and back-left legs move together

                if leg_id in [0, 3]:  # Front-left, back-right
                    leg_phase = phase
                else:  # Front-right, back-left
                    leg_phase = (phase + 0.5) % 1.0

                # Compute desired angles using gait function
                target_angles = self.compute_gait_angles(leg_phase)

                # Control each joint to reach target
                for joint_id, target_angle in enumerate(target_angles):
                    actual_angle = self.get_joint_angle(leg_id, joint_id)
                    command = self.leg_controllers[leg_id][joint_id].compute(
                        target_angle, actual_angle
                    )
                    self.set_motor_command(leg_id, joint_id, command)

            # Advance phase
            phase = (phase + 0.01) % 1.0
            time.sleep(0.01)

    def compute_gait_angles(self, phase):
        """
        Compute desired joint angles for current gait phase
        phase: 0 to 1 (0 = stance start, 1 = stance end)
        """

        if phase < 0.6:  # Stance phase (60% of cycle)
            # Leg pushes backward
            hip_angle = -30 + 30 * phase    # From -30° to 0°
            knee_angle = -45                # Mostly fixed
            ankle_angle = 0                 # Mostly fixed

        else:  # Swing phase (40% of cycle)
            # Leg swings forward
            swing_progress = (phase - 0.6) / 0.4
            hip_angle = 30 * sin(swing_progress * π)
            knee_angle = -90 + 60 * sin(swing_progress * π)
            ankle_angle = 0

        return [hip_angle, knee_angle, ankle_angle]
```

## Week 3 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** how closed-loop control uses feedback to correct errors
2. **Design** and tune a PID controller for a robotic joint
3. **Compare** proportional, integral, and derivative terms and their effects
4. **Implement** multi-joint coordination for a robot arm
5. **Analyze** control system performance using metrics like rise time and overshoot
6. **Apply** impedance control for compliant robot behavior

## Key Terminology

| Term | Definition |
|------|-----------|
| **Closed-loop Control** | System adjusts actions based on feedback to reach goal |
| **PID Controller** | Proportional-Integral-Derivative controller for error correction |
| **Setpoint** | Desired state the control system tries to achieve |
| **Error Signal** | Difference between desired and actual state |
| **Transient Response** | How quickly system reaches desired state |
| **Steady-State Error** | Final error after system settles |
| **Impedance** | System's resistance to external forces (spring-like) |
| **Overshoot** | Exceeding target value before settling |

## Discussion Questions

1. **Tuning Tradeoffs**: Why is fast control (high Kp) sometimes bad? What problems does it cause?

2. **Multi-Joint Coordination**: A robot arm must reach a target position quickly but smoothly. Should you control the joints independently or use inverse kinematics? What are the tradeoffs?

3. **Human-Robot Interaction**: Why would a surgical robot need different impedance control than an industrial assembly robot?

4. **Performance vs Safety**: A PID controller can be tuned for fast response OR for stability. Why is this a tradeoff? Can both be achieved?

## Hands-On Activity

**Simulate PID Control**

Using a physics simulation or online tool:
1. Set up a mass on a spring
2. Implement PID controller to move mass to target position
3. Try different Kp, Ki, Kd values and observe:
   - How fast does it reach target?
   - Does it overshoot?
   - Does it oscillate?
4. Document your best tuning and explain why it works

Tools:
- Online: [Control Systems Simulator](https://en.wikipedia.org/wiki/PID_controller)
- Python: `control` library

## Resources for Deeper Learning

- **Book**: "Modern Control Systems" - Richard Dorf & Robert Bishop
- **Video**: "PID Control Explained" - Brian Douglas (Control System Lectures)
- **Tool**: MATLAB/Simulink for control system design and simulation
- **Paper**: "The Ziegler–Nichols Tuning Method" - classic reference
- **Interactive**: Interactive PID tuning simulator with visualizations

---

**Next**: Module 1 Capstone - Building a Complete Embodied AI System

💡 **Tip**: Real robots almost never use "pure" PID. They combine feedforward (expected commands), feedback (error correction), and sometimes learning (neural networks) for optimal control!
