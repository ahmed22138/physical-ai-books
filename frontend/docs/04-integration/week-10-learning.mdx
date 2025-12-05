---
sidebar_position: 1
---

# Week 10: Learning from Data & Imitation Learning

## From Programming to Learning

So far we've programmed robots explicitly: write control laws, planning algorithms, vision pipelines. But many real-world tasks are too complex to program by hand.

**Machine learning** enables robots to learn from data. This week focuses on **imitation learning**: learning by observing humans.

## Part 1: Behavior Cloning

Simplest form of imitation learning: supervised learning on human demonstrations.

```python
class BehaviorCloner:
    def __init__(self, state_dim, action_dim):
        """Initialize behavior cloning model"""
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Simple neural network: state → action
        self.model = self.build_model()

    def build_model(self):
        """Build neural network"""
        # Simplified; real implementations use PyTorch/TensorFlow

        class SimpleNet:
            def __init__(self, input_dim, output_dim):
                self.w1 = np.random.randn(input_dim, 128) * 0.01
                self.b1 = np.zeros(128)
                self.w2 = np.random.randn(128, output_dim) * 0.01
                self.b2 = np.zeros(output_dim)

            def forward(self, x):
                # ReLU hidden layer
                h = np.maximum(0, x @ self.w1 + self.b1)
                # Linear output
                y = h @ self.w2 + self.b2
                return y

        return SimpleNet(self.state_dim, self.action_dim)

    def train(self, states, actions, epochs=100, learning_rate=0.001):
        """Train on human demonstrations"""

        for epoch in range(epochs):
            # Batch gradient descent
            predictions = self.model.forward(states)

            # Mean squared error loss
            loss = np.mean((predictions - actions)**2)

            # Backprop (simplified)
            gradient = 2 * (predictions - actions) / len(states)

            # Update weights
            # (Real implementations use automatic differentiation)

            if epoch % 10 == 0:
                print(f"Epoch {epoch}: Loss = {loss:.4f}")

    def predict(self, state):
        """Predict action for given state"""
        return self.model.forward(state)
```

**Problem**: **Distribution shift**. Robot might encounter states not in training data.

## Part 2: DAgger (Dataset Aggregation)

Iteratively collect failures and have human correct them.

```python
class DAggerTrainer:
    def __init__(self, behavior_cloner, environment, expert_policy):
        self.cloner = behavior_cloner
        self.env = environment
        self.expert = expert_policy
        self.aggregate_states = []
        self.aggregate_actions = []

    def train_with_dagger(self, num_iterations=10, num_rollouts=5):
        """DAgger algorithm"""

        for iteration in range(num_iterations):
            print(f"\\nDAgger iteration {iteration+1}/{num_iterations}")

            # 1. Collect rollouts with current policy
            for rollout in range(num_rollouts):
                state = self.env.reset()
                rollout_states = []

                for step in range(100):
                    # Use learned policy
                    action = self.cloner.predict(state)

                    rollout_states.append(state)
                    state, reward, done = self.env.step(action)

                    if done:
                        break

                # 2. Ask expert to label trajectory
                # In real systems: human watches and corrects

                # 3. Add to aggregate dataset
                for s in rollout_states:
                    expert_action = self.expert.get_action(s)
                    self.aggregate_states.append(s)
                    self.aggregate_actions.append(expert_action)

            # 4. Retrain on all data collected so far
            self.cloner.train(
                np.array(self.aggregate_states),
                np.array(self.aggregate_actions),
                epochs=50
            )

            # Evaluate
            success_rate = self.evaluate()
            print(f"Success rate: {success_rate:.1%}")

    def evaluate(self, num_episodes=10):
        """Evaluate learned policy"""
        successes = 0

        for episode in range(num_episodes):
            state = self.env.reset()

            for step in range(100):
                action = self.cloner.predict(state)
                state, reward, done = self.env.step(action)

                if done and reward > 0:  # Successful completion
                    successes += 1
                    break
                if done:
                    break

        return successes / num_episodes
```

## Part 3: Learning for Manipulation

Real example: learning to grasp from demonstrations.

```python
class GraspingLearner:
    def __init__(self):
        self.demo_states = []  # RGB images
        self.demo_actions = []  # Grasp positions

    def collect_demonstrations(self, num_demos=100):
        """Collect human grasping demonstrations"""

        for demo in range(num_demos):
            # Show object from multiple angles
            rgb_images = self.capture_from_angles(num_angles=6)

            # Ask human: where to grasp?
            # In real system: human teleoperates robot

            for image in rgb_images:
                self.demo_states.append(image)
                # Grasp location: (x, y, angle)
                grasp = self.get_human_grasp()
                self.demo_actions.append(grasp)

    def train_grasp_network(self):
        """Train CNN to predict grasp location"""

        # Input: RGB image
        # Output: Heatmap of grasp quality

        model = self.build_grasp_cnn()

        # Train on demonstrations
        model.train(self.demo_states, self.demo_actions, epochs=100)

        return model

    def predict_grasps(self, rgb_image, num_grasps=5):
        """Predict top 5 grasp candidates"""

        model = self.trained_model

        # Get heatmap of grasp quality
        heatmap = model.predict(rgb_image)

        # Find peaks
        grasps = self.find_peaks(heatmap, k=num_grasps)

        return grasps

    def build_grasp_cnn(self):
        """Build CNN for grasp prediction"""

        # Input: 224×224 RGB image
        # → Conv layers extract features
        # → Output: 28×28 heatmap of grasp quality

        class GraspCNN:
            def __init__(self):
                # Simplified CNN structure
                pass

            def train(self, images, actions, epochs):
                # Training loop
                pass

            def predict(self, image):
                # Forward pass
                pass

        return GraspCNN()
```

## Week 10 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** behavior cloning and distribution shift problem
2. **Implement** DAgger for iterative learning
3. **Train** neural networks on robot demonstrations
4. **Apply** imitation learning to manipulation tasks
5. **Evaluate** learned policies and diagnose failure modes
6. **Understand** limitations of supervised learning for robotics

## Key Terminology

| Term | Definition |
|------|-----------|
| **Imitation learning** | Learning by observing and copying expert behavior |
| **Behavior cloning** | Supervised learning: state → action from demonstrations |
| **Distribution shift** | Robot encounters states not in training data |
| **DAgger** | Dataset Aggregation - iterative correction from expert |
| **Teleoperati** | Remote control by human (used for data collection) |
| **Trajectory** | Sequence of (state, action, reward) tuples |
| **Heatmap** | 2D visualization of predicted values |

---

**Next**: Week 11 - System Integration & Real-World Deployment

💡 **Tip**: DAgger is more robust than behavior cloning because it addresses distribution shift!
