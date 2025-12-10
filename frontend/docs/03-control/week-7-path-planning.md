---
sidebar_position: 1
---

# Week 7: Path Planning

## The Navigation Problem

Your mobile robot stands in a warehouse filled with obstacles. It needs to reach a distant goal without crashing. How does it find a safe path?

**Path planning** is the algorithm that computes a collision-free path from start to goal. This week covers the fundamental algorithms that power robot navigation.

## Part 1: Configuration Space

Before we plan, we need to understand the **robot's configuration space** (C-space)—the space of all possible robot poses.

### 2D Mobile Robot C-Space

```python
class ConfigurationSpace:
    def __init__(self, world_map, robot_radius=0.25):
        """Initialize C-space from occupancy grid"""
        self.world_map = world_map  # 2D binary grid
        self.robot_radius = robot_radius

    def inflate_obstacles(self):
        """Expand obstacles by robot radius for safety"""
        # Dilate obstacles: any cell within robot_radius of obstacle
        # becomes obstacle

        inflated = np.zeros_like(self.world_map)

        for y in range(self.world_map.shape[0]):
            for x in range(self.world_map.shape[1]):
                if self.world_map[y, x]:  # Is obstacle
                    # Mark all cells within radius as inflated
                    for dy in range(-int(self.robot_radius), int(self.robot_radius)+1):
                        for dx in range(-int(self.robot_radius), int(self.robot_radius)+1):
                            if dy**2 + dx**2 <= self.robot_radius**2:
                                ny = y + dy
                                nx = x + dx
                                if 0 <= ny < inflated.shape[0] and 0 <= nx < inflated.shape[1]:
                                    inflated[ny, nx] = 1

        return inflated

    def is_collision_free(self, x, y):
        """Check if robot at (x, y) is collision-free"""
        grid_x = int(x)
        grid_y = int(y)

        if 0 <= grid_x < self.world_map.shape[1] and \
           0 <= grid_y < self.world_map.shape[0]:
            return not self.world_map[grid_y, grid_x]
        return False
```

## Part 2: Graph-Based Planning

### Dijkstra's Algorithm

Find shortest path on a graph using greedy exploration.

```python
class DijkstraPlanner:
    def plan(self, start, goal, cspace):
        """Plan path using Dijkstra's algorithm"""

        import heapq

        # Priority queue: (distance, node)
        queue = [(0, tuple(start))]
        distances = {tuple(start): 0}
        parents = {}

        while queue:
            current_distance, current = heapq.heappop(queue)

            # Skip if already processed
            if current in parents:
                continue

            # Found goal
            if current == tuple(goal):
                return self.reconstruct_path(parents, goal)

            # Explore neighbors
            for neighbor in self.get_neighbors(current, cspace):
                distance = current_distance + 1

                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current
                    heapq.heappush(queue, (distance, neighbor))

        return None  # No path found

    def get_neighbors(self, cell, cspace, resolution=0.1):
        """Get collision-free neighboring cells"""
        x, y = cell
        neighbors = []

        for dx in [-resolution, 0, resolution]:
            for dy in [-resolution, 0, resolution]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if cspace.is_collision_free(nx, ny):
                    neighbors.append((nx, ny))

        return neighbors

    def reconstruct_path(self, parents, goal):
        """Reconstruct path from parent pointers"""
        path = []
        current = tuple(goal)

        while current in parents:
            path.append(current)
            current = parents[current]

        path.append(current)
        return list(reversed(path))
```

**Characteristics**: Optimal but slow. Explores all directions equally.

### A* Algorithm

Like Dijkstra but uses **heuristics** to guide search toward goal.

```python
class AStarPlanner:
    def plan(self, start, goal, cspace):
        """Plan path using A* algorithm"""

        import heapq

        def heuristic(a, b):
            """Euclidean distance heuristic"""
            return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

        start_tuple = tuple(start)
        goal_tuple = tuple(goal)

        # Priority queue: (f_score, node)
        # f_score = g_score (distance from start) + h_score (heuristic to goal)
        queue = [(heuristic(start, goal), start_tuple)]
        g_scores = {start_tuple: 0}
        f_scores = {start_tuple: heuristic(start, goal)}
        parents = {}

        while queue:
            _, current = heapq.heappop(queue)

            if current == goal_tuple:
                return self.reconstruct_path(parents, goal)

            # Explore neighbors
            for neighbor in self.get_neighbors(current, cspace):
                tentative_g = g_scores[current] + 1

                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    parents[neighbor] = current
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    f_scores[neighbor] = f_score

                    heapq.heappush(queue, (f_score, neighbor))

        return None

    def get_neighbors(self, cell, cspace, resolution=0.1):
        """Get collision-free neighbors"""
        x, y = cell
        neighbors = []

        for dx in [-resolution, 0, resolution]:
            for dy in [-resolution, 0, resolution]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if cspace.is_collision_free(nx, ny):
                    neighbors.append((nx, ny))

        return neighbors
```

**Characteristics**: Faster than Dijkstra, optimal with admissible heuristic. Most commonly used.

## Part 3: Sampling-Based Planning

For high-dimensional spaces (robotic arms with 7+ DOF), grid-based methods become impractical. **Sampling-based planners** work in high dimensions.

### Rapidly-exploring Random Tree (RRT)

Incrementally build a tree by randomly sampling the C-space.

```python
class RRTPlanner:
    def __init__(self, cspace, step_size=0.5, max_iterations=5000):
        """Initialize RRT planner"""
        self.cspace = cspace
        self.step_size = step_size
        self.max_iterations = max_iterations

    def plan(self, start, goal, goal_bias=0.1):
        """Plan using RRT"""

        class Node:
            def __init__(self, config):
                self.config = config
                self.parent = None
                self.children = []

        root = Node(start)
        goal_node = Node(goal)

        for iteration in range(self.max_iterations):
            # Random sample: 10% goal, 90% random
            if np.random.random() < goal_bias:
                random_config = goal
            else:
                random_config = self.random_sample()

            # Find nearest node in tree
            nearest = self.nearest_node(root, random_config)

            # Try to extend toward random config
            new_config = self.extend(nearest.config, random_config)

            if new_config is not None:
                new_node = Node(new_config)
                new_node.parent = nearest
                nearest.children.append(new_node)

                # Check if reached goal
                if self.distance(new_config, goal) < self.step_size:
                    new_node.parent = nearest
                    nearest.children.append(new_node)
                    goal_node.parent = new_node
                    return self.extract_path(goal_node)

        return None

    def random_sample(self):
        """Sample random configuration in C-space"""
        # For 2D: random (x, y) in bounds
        x = np.random.uniform(0, 50)  # World bounds
        y = np.random.uniform(0, 50)
        return (x, y)

    def nearest_node(self, root, config):
        """Find node in tree nearest to config"""
        min_distance = float('inf')
        nearest = None

        # BFS/DFS through tree
        queue = [root]
        while queue:
            node = queue.pop(0)
            distance = self.distance(node.config, config)

            if distance < min_distance:
                min_distance = distance
                nearest = node

            queue.extend(node.children)

        return nearest

    def extend(self, from_config, to_config):
        """Extend from_config toward to_config by step_size"""
        direction = np.array(to_config) - np.array(from_config)
        norm = np.linalg.norm(direction)

        if norm < 1e-6:
            return None

        direction = direction / norm

        # Take step of size step_size
        new_config = np.array(from_config) + direction * self.step_size

        # Check collision
        if self.cspace.is_collision_free(new_config[0], new_config[1]):
            return tuple(new_config)

        return None

    def distance(self, config1, config2):
        """Euclidean distance"""
        return ((config1[0]-config2[0])**2 + (config1[1]-config2[1])**2)**0.5

    def extract_path(self, goal_node):
        """Extract path by following parent pointers"""
        path = []
        current = goal_node

        while current is not None:
            path.append(current.config)
            current = current.parent

        return list(reversed(path))
```

**Characteristics**: Works in high dimensions, fast, probabilistically complete (will find path if one exists).

```
RRT Growth:
┌─────────────────┐
│    Goal         │
│     *           │
│  ╱  │╲          │
│ ╱   │ ╲         │
│╱    │  ╲        │
│     │   ╲       │
│     │    ╲      │
│  Start    Tree  │
│     *            │
└─────────────────┘
```

## Part 4: Real-World Planning

### Handling Dynamic Obstacles

Real environments change. A path valid at planning time might not be valid later.

```python
class DynamicPathPlanner:
    def __init__(self, cspace, replanning_frequency=10):
        """Planner that replans when obstacles change"""
        self.cspace = cspace
        self.replanning_frequency = replanning_frequency
        self.current_path = None
        self.step_count = 0

    def execute(self, robot_pose, goal, dynamic_obstacles):
        """Execute path with replanning"""

        # Every N steps, replan
        if self.step_count % self.replanning_frequency == 0:
            self.current_path = self.plan(robot_pose, goal)

        # Follow current path
        if self.current_path:
            next_waypoint = self.current_path[0]

            # Check if path is still valid
            if not self.is_path_valid(self.current_path, dynamic_obstacles):
                print("Path blocked! Replanning...")
                self.current_path = self.plan(robot_pose, goal)

            self.step_count += 1
            return next_waypoint

        return None

    def is_path_valid(self, path, obstacles):
        """Check if path collides with any obstacle"""
        for pose in path:
            for obstacle in obstacles:
                distance = np.linalg.norm(
                    np.array(pose) - np.array(obstacle['position'])
                )

                if distance < obstacle['radius']:
                    return False

        return True
```

## Week 7 Learning Outcomes

By the end of this week, you should be able to:

1. **Explain** configuration spaces and obstacle inflation
2. **Implement** Dijkstra's algorithm for grid-based planning
3. **Apply** A* with heuristics for faster planning
4. **Use** RRT for high-dimensional path planning
5. **Compare** graph-based vs. sampling-based methods
6. **Handle** dynamic obstacles with replanning

## Key Terminology

| Term | Definition |
|------|-----------|
| **Configuration space (C-space)** | Space of all possible robot configurations |
| **Collision-free** | Configuration with no overlap with obstacles |
| **Heuristic** | Estimate of distance to goal (A* uses this) |
| **Admissible heuristic** | Never overestimates distance to goal |
| **Dijkstra's algorithm** | Optimal path finding, explores equally in all directions |
| **A* algorithm** | Optimal path finding using heuristics (faster) |
| **RRT** | Rapidly-exploring Random Tree for high-dimensional planning |
| **Probabilistically complete** | Will find path if one exists (given infinite time) |

## Discussion Questions

1. **Heuristics**: Why does A* use Euclidean distance as a heuristic? What happens if heuristic overestimates?

2. **Dimensions**: Dijkstra works on 2D grids. Can you use it for a 7-DOF robot arm? Why or why not?

3. **Optimality**: RRT finds *a* path but not necessarily optimal. How would you modify it to find better paths?

4. **Real-time**: Robot must plan at 10 Hz (100ms per decision). Which algorithm is suitable?

## Hands-On Activity

**Implement A* path planner**

1. Create 20×20 grid with obstacles
2. Implement A* with Euclidean heuristic
3. Visualize: grid, start, goal, obstacles, planned path
4. Measure: path length and number of nodes explored
5. Compare A* vs. Dijkstra (how many more nodes did Dijkstra explore?)

## Resources for Deeper Learning

- **Book**: "Computational Geometry" - de Berg, Cheong, van Kreveld, Overmars
- **Course**: "Robot Motion Planning" - UC Davis (YouTube)
- **Paper**: "RRT-Connect: An Efficient Approach to Single-Query Path Planning" - Kuffner & LaValle
- **Tool**: OMPL (Open Motion Planning Library) - free software
- **Visualization**: "Path Planning Visualizer" - interactive web tool

---

**Next**: Week 8 - Trajectory Planning & Collision Avoidance

💡 **Tip**: A* explores fewer nodes than Dijkstra. Visualize which cells each algorithm visits!
