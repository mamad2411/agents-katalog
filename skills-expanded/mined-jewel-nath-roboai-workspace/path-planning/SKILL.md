---
name: path-planning
description: Path planning algorithms including A*, Dijkstra, RRT/RRT*, PRM, hybrid A*, lattice planners, and costmap-based planning. Use for custom navigation, coverage planning, and motion planning.
category: navigation
tags: [planning, path-planning, a-star, rrt, motion-planning, algorithms]
version: "1.0.0"
---

# Path Planning

Path planning computes collision-free trajectories from start to goal configurations. This skill covers sampling-based planners (RRT, PRM), search-based planners (A*, Dijkstra), and their application in robotics navigation.

## When to Use

- Implementing custom path planners beyond Nav2 defaults
- Developing coverage planning for area inspection/cleaning
- Creating lattice-based planners for non-holonomic robots
- Implementing anytime/replanning algorithms
- Tuning heuristics for optimal planning
- Designing multi-goal planners (TSP, vehicle routing)
- Implementing kinodynamic motion planning
- Developing sampling strategies for complex environments

## Quick Start

```bash
# Install OMPL (Open Motion Planning Library)
sudo apt install ros-$ROS_DISTRO-ompl

# Python example with simple A*
pip install networkx shapely

# Run OMPL demo
ros2 launch ompl_demo ompl_demo.launch.py
```

**Minimal A* Example:**
```python
import heapq
import numpy as np

def astar(grid, start, goal):
    """A* pathfinding on a 2D grid."""
    rows, cols = grid.shape
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current, rows, cols):
            if grid[neighbor] == 1:  # Obstacle
                continue
            
            tentative_g = g_score[current] + 1
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

def heuristic(a, b):
    """Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

## Core Concepts

### 1. Planning Taxonomy

| Category | Algorithms | Characteristics |
|----------|------------|-----------------|
| Search-based | A*, Dijkstra, Theta* | Complete, optimal, discrete |
| Sampling-based | RRT, RRT*, PRM, FMT* | Probabilistically complete, anytime |
| Optimization-based | CHOMP, TrajOpt, GPMP | Smooth paths, local minima |
| Lattice-based | Hybrid A*, State Lattice | Kinodynamic constraints |
| Potential fields | APF, VFH | Fast, local minima issues |

### 2. Search-Based Planning

**A* Algorithm:**
```python
import heapq
import numpy as np
from typing import List, Tuple, Set

class AStarPlanner:
    """Grid-based A* planner with diagonal movement."""
    
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.rows, self.cols = grid.shape
        
    def plan(self, start: Tuple[int, int], 
             goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Find path from start to goal."""
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}
        closed_set: Set[Tuple[int, int]] = set()
        
        # 8-connected grid
        neighbors = [(-1,-1), (-1,0), (-1,1), (0,-1), 
                     (0,1), (1,-1), (1,0), (1,1)]
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
                
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            closed_set.add(current)
            
            for dy, dx in neighbors:
                neighbor = (current[0] + dy, current[1] + dx)
                
                if not self._is_valid(neighbor):
                    continue
                
                # Diagonal cost = sqrt(2)
                cost = 1.414 if dy != 0 and dx != 0 else 1.0
                
                tentative_g = g_score[current] + cost
                
                if neighbor in closed_set:
                    continue
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # No path found
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Euclidean distance heuristic."""
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def _is_valid(self, pos: Tuple[int, int]) -> bool:
        """Check if position is valid and free."""
        y, x = pos
        if y < 0 or y >= self.rows or x < 0 or x >= self.cols:
            return False
        return self.grid[y, x] == 0
    
    def _reconstruct_path(self, came_from, current):
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
```

**Theta* (Any-Angle Planning):**
```python
class ThetaStarPlanner(AStarPlanner):
    """Theta* - any-angle path planning."""
    
    def _update_vertex(self, s, neighbor, goal, open_set, came_from, g_score, f_score):
        """Theta* line-of-sight optimization."""
        if self._line_of_sight(came_from.get(s, s), neighbor):
            # Path through parent of s is better
            if g_score[came_from[s]] + self._dist(came_from[s], neighbor) < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = came_from[s]
                g_score[neighbor] = g_score[came_from[s]] + self._dist(came_from[s], neighbor)
                f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
        else:
            # Standard A* update
            if g_score[s] + self._dist(s, neighbor) < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = s
                g_score[neighbor] = g_score[s] + self._dist(s, neighbor)
                f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    def _line_of_sight(self, s1, s2):
        """Bresenham line-of-sight check."""
        if s1 is None:
            return False
        
        y1, x1 = s1
        y2, x2 = s2
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        sy = 1 if y1 < y2 else -1
        sx = 1 if x1 < x2 else -1
        err = dx - dy
        
        while True:
            if self.grid[y1, x1] == 1:
                return False
            if x1 == x2 and y1 == y2:
                return True
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def _dist(self, a, b):
        """Euclidean distance."""
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
```

### 3. Sampling-Based Planning

**RRT (Rapidly-exploring Random Tree):**
```python
import numpy as np
from typing import List, Tuple

class RRTPlanner:
    """RRT path planner."""
    
    def __init__(self, bounds: Tuple[float, float, float, float],
                 max_iter: int = 10000,
                 step_size: float = 0.5):
        self.bounds = bounds  # (xmin, xmax, ymin, ymax)
        self.max_iter = max_iter
        self.step_size = step_size
        self.obstacles = []
        
    def plan(self, start: np.ndarray, 
             goal: np.ndarray,
             obstacles: List[Tuple[np.ndarray, float]]) -> List[np.ndarray]:
        """Find path using RRT."""
        self.obstacles = obstacles
        tree = {tuple(start): None}  # node -> parent
        nodes = [start]
        
        for _ in range(self.max_iter):
            # Sample random point
            if np.random.random() < 0.1:
                random_point = goal
            else:
                random_point = self._random_sample()
            
            # Find nearest node
            nearest_idx = self._nearest(nodes, random_point)
            nearest = nodes[nearest_idx]
            
            # Steer towards random point
            new_node = self._steer(nearest, random_point)
            
            if self._collision_free(nearest, new_node):
                tree[tuple(new_node)] = tuple(nearest)
                nodes.append(new_node)
                
                # Check if goal reached
                if np.linalg.norm(new_node - goal) < self.step_size:
                    # Connect to goal
                    if self._collision_free(new_node, goal):
                        tree[tuple(goal)] = tuple(new_node)
                        return self._reconstruct_path(tree, start, goal)
        
        return None
    
    def _random_sample(self) -> np.ndarray:
        """Sample random point in bounds."""
        xmin, xmax, ymin, ymax = self.bounds
        return np.array([
            np.random.uniform(xmin, xmax),
            np.random.uniform(ymin, ymax)
        ])
    
    def _nearest(self, nodes: List[np.ndarray], point: np.ndarray) -> int:
        """Find index of nearest node."""
        distances = [np.linalg.norm(n - point) for n in nodes]
        return np.argmin(distances)
    
    def _steer(self, from_node: np.ndarray, 
               to_point: np.ndarray) -> np.ndarray:
        """Steer from node towards point with step_size."""
        direction = to_point - from_node
        distance = np.linalg.norm(direction)
        
        if distance < self.step_size:
            return to_point
        
        return from_node + (direction / distance) * self.step_size
    
    def _collision_free(self, from_node: np.ndarray, 
                        to_node: np.ndarray) -> bool:
        """Check if edge is collision-free."""
        for center, radius in self.obstacles:
            if self._segment_circle_intersection(from_node, to_node, center, radius):
                return False
        return True
    
    def _segment_circle_intersection(self, p1, p2, center, radius):
        """Check line segment - circle intersection."""
        # Vector from p1 to p2
        d = p2 - p1
        # Vector from p1 to circle center
        f = p1 - center
        
        a = np.dot(d, d)
        b = 2 * np.dot(f, d)
        c = np.dot(f, f) - radius * radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return False
        
        discriminant = np.sqrt(discriminant)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        
        return (0 <= t1 <= 1) or (0 <= t2 <= 1)
    
    def _reconstruct_path(self, tree, start, goal):
        """Reconstruct path from tree."""
        path = [goal]
        current = tuple(goal)
        
        while current != tuple(start):
            current = tree[current]
            path.append(np.array(current))
        
        return path[::-1]
```

**RRT* (Optimal RRT):**
```python
class RRTStarPlanner(RRTPlanner):
    """RRT* - asymptotically optimal variant."""
    
    def __init__(self, bounds, max_iter=10000, step_size=0.5, 
                 rewire_radius=1.0):
        super().__init__(bounds, max_iter, step_size)
        self.rewire_radius = rewire_radius
        self.costs = {}
        
    def plan(self, start, goal, obstacles):
        """RRT* planning with rewiring."""
        self.obstacles = obstacles
        tree = {tuple(start): []}  # node -> children
        parents = {tuple(start): None}
        nodes = [start]
        self.costs = {tuple(start): 0.0}
        
        for _ in range(self.max_iter):
            random_point = self._random_sample()
            if np.random.random() < 0.1:
                random_point = goal
            
            nearest_idx = self._nearest(nodes, random_point)
            nearest = nodes[nearest_idx]
            
            new_node = self._steer(nearest, random_point)
            
            if self._collision_free(nearest, new_node):
                # Find near nodes
                near_nodes = self._near(nodes, new_node)
                
                # Choose best parent
                min_cost = self.costs[tuple(nearest)] + np.linalg.norm(nearest - new_node)
                best_parent = nearest
                
                for near in near_nodes:
                    if self._collision_free(near, new_node):
                        cost = self.costs[tuple(near)] + np.linalg.norm(near - new_node)
                        if cost < min_cost:
                            min_cost = cost
                            best_parent = near
                
                # Add node
                tree[tuple(new_node)] = []
                parents[tuple(new_node)] = tuple(best_parent)
                tree[tuple(best_parent)].append(new_node)
                self.costs[tuple(new_node)] = min_cost
                nodes.append(new_node)
                
                # Rewire
                for near in near_nodes:
                    if near is new_node:
                        continue
                    if self._collision_free(new_node, near):
                        new_cost = self.costs[tuple(new_node)] + np.linalg.norm(new_node - near)
                        if new_cost < self.costs[tuple(near)]:
                            # Rewire
                            old_parent = parents[tuple(near)]
                            tree[old_parent].remove(near)
                            parents[tuple(near)] = tuple(new_node)
                            tree[tuple(new_node)].append(near)
                            self._update_costs(tree, parents, near)
                
                # Check goal
                if np.linalg.norm(new_node - goal) < self.step_size:
                    if self._collision_free(new_node, goal):
                        if tuple(goal) not in parents:
                            parents[tuple(goal)] = tuple(new_node)
                            self.costs[tuple(goal)] = self.costs[tuple(new_node)] + np.linalg.norm(new_node - goal)
                            return self._reconstruct_path_rrtstar(parents, start, goal)
        
        return None
    
    def _near(self, nodes, point):
        """Find nodes within rewire radius."""
        near = []
        for node in nodes:
            if np.linalg.norm(node - point) < self.rewire_radius:
                near.append(node)
        return near
    
    def _update_costs(self, tree, parents, node):
        """Update costs after rewiring."""
        node_tuple = tuple(node)
        for child in tree.get(node_tuple, []):
            self.costs[tuple(child)] = self.costs[node_tuple] + np.linalg.norm(node - child)
            self._update_costs(tree, parents, child)
    
    def _reconstruct_path_rrtstar(self, parents, start, goal):
        """Reconstruct path."""
        path = [goal]
        current = tuple(goal)
        while current != tuple(start):
            current = parents[current]
            path.append(np.array(current))
        return path[::-1]
```

### 4. Lattice-Based Planning (Hybrid A*)

For car-like robots with non-holonomic constraints:

```python
import numpy as np
import heapq
from typing import List, Tuple
from scipy.spatial.transform import Rotation

class HybridAStarPlanner:
    """Hybrid A* for car-like robots."""
    
    def __init__(self, grid_resolution=0.5, 
                 theta_resolution=16,  # 16 angles = 22.5 deg
                 step_size=0.5,
                 max_steering_angle=0.6):  # radians
        self.grid_res = grid_resolution
        self.theta_res = theta_resolution
        self.step_size = step_size
        self.max_steering = max_steering_angle
        self.wheelbase = 0.5  # meters
        
    def plan(self, start: Tuple[float, float, float],
             goal: Tuple[float, float, float],
             obstacles: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        """
        Plan path for car-like robot.
        State: (x, y, theta)
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}
        closed_set = set()
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
            
            # Check if goal reached
            if self._goal_reached(current, goal):
                return self._reconstruct_path(came_from, current)
            
            closed_set.add(current)
            
            # Generate motion primitives
            for steering in [-self.max_steering, 0, self.max_steering]:
                next_state = self._simulate_motion(current, steering)
                
                if self._collision(next_state, obstacles):
                    continue
                
                if next_state in closed_set:
                    continue
                
                tentative_g = g_score[current] + self.step_size
                
                if tentative_g < g_score.get(next_state, float('inf')):
                    came_from[next_state] = current
                    g_score[next_state] = tentative_g
                    f_score[next_state] = tentative_g + self._heuristic(next_state, goal)
                    heapq.heappush(open_set, (f_score[next_state], next_state))
        
        return None
    
    def _simulate_motion(self, state, steering):
        """Simulate forward motion with bicycle model."""
        x, y, theta = state
        
        # Simple Euler integration
        dx = self.step_size * np.cos(theta)
        dy = self.step_size * np.sin(theta)
        dtheta = self.step_size * np.tan(steering) / self.wheelbase
        
        x_new = x + dx
        y_new = y + dy
        theta_new = theta + dtheta
        
        # Discretize theta
        theta_disc = round(theta_new / (2 * np.pi / self.theta_res)) * (2 * np.pi / self.theta_res)
        theta_disc = theta_disc % (2 * np.pi)
        
        # Discretize x, y
        x_disc = round(x_new / self.grid_res) * self.grid_res
        y_disc = round(y_new / self.grid_res) * self.grid_res
        
        return (x_disc, y_disc, theta_disc)
    
    def _heuristic(self, state, goal):
        """Non-holonomic heuristic (Reeds-Shepp distance)."""
        # Simplified: use Euclidean for now
        return np.sqrt((state[0]-goal[0])**2 + (state[1]-goal[1])**2)
    
    def _goal_reached(self, state, goal):
        """Check if close enough to goal."""
        pos_dist = np.sqrt((state[0]-goal[0])**2 + (state[1]-goal[1])**2)
        angle_dist = abs(state[2] - goal[2])
        return pos_dist < self.grid_res and angle_dist < np.pi / self.theta_res
    
    def _collision(self, state, obstacles):
        """Check collision with obstacles."""
        for ox, oy, radius in obstacles:
            dist = np.sqrt((state[0]-ox)**2 + (state[1]-oy)**2)
            if dist < radius:
                return True
        return False
    
    def _reconstruct_path(self, came_from, current):
        """Reconstruct path."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
```

## Common Patterns

### Pattern 1: Costmap-Based Planning

```python
class CostmapPlanner:
    """Planner using ROS2 costmap."""
    
    def __init__(self, node):
        self.node = node
        self.costmap_sub = node.create_subscription(
            OccupancyGrid, '/global_costmap/costmap', 
            self.costmap_callback, 1)
        self.costmap = None
        
    def costmap_callback(self, msg):
        """Convert OccupancyGrid to numpy array."""
        width = msg.info.width
        height = msg.info.height
        self.costmap = np.array(msg.data).reshape((height, width))
        self.resolution = msg.info.resolution
        self.origin = (msg.info.origin.position.x, 
                       msg.info.origin.position.y)
        
    def world_to_grid(self, x, y):
        """Convert world coordinates to grid indices."""
        gx = int((x - self.origin[0]) / self.resolution)
        gy = int((y - self.origin[1]) / self.resolution)
        return gy, gx
    
    def grid_to_world(self, gy, gx):
        """Convert grid indices to world coordinates."""
        x = gx * self.resolution + self.origin[0]
        y = gy * self.resolution + self.origin[1]
        return x, y
    
    def get_cost(self, gy, gx):
        """Get cost at grid cell."""
        if self.costmap is None:
            return 255
        
        h, w = self.costmap.shape
        if gy < 0 or gy >= h or gx < 0 or gx >= w:
            return 255  # Unknown/occupied outside bounds
        
        return self.costmap[gy, gx]
    
    def is_free(self, gy, gx, threshold=50):
        """Check if cell is free (below threshold)."""
        cost = self.get_cost(gy, gx)
        return cost >= 0 and cost < threshold
```

### Pattern 2: Coverage Planning (Boustrophedon)

```python
class CoveragePlanner:
    """Boustrophedon coverage path planning."""
    
    def __init__(self, grid_resolution=0.5):
        self.resolution = grid_resolution
        
    def plan_coverage(self, polygon, obstacles=None):
        """
        Generate coverage path for a polygon area.
        Returns: List of waypoints
        """
        # Decompose into cells
        cells = self._boustrophedon_decomposition(polygon, obstacles)
        
        # Generate path through cells
        waypoints = []
        for i, cell in enumerate(cells):
            cell_path = self._cover_cell(cell, direction=i % 2)
            waypoints.extend(cell_path)
        
        return waypoints
    
    def _boustrophedon_decomposition(self, polygon, obstacles):
        """Simple cell decomposition."""
        # Simplified: return bounding box cells
        # Full implementation requires trapezoidal decomposition
        min_x, min_y = polygon.min(axis=0)
        max_x, max_y = polygon.max(axis=0)
        
        cells = []
        y = min_y
        while y < max_y:
            cell = np.array([
                [min_x, y],
                [max_x, y],
                [max_x, y + self.resolution * 5],
                [min_x, y + self.resolution * 5]
            ])
            cells.append(cell)
            y += self.resolution * 5
        
        return cells
    
    def _cover_cell(self, cell, direction):
        """Generate back-and-forth path in cell."""
        min_x, min_y = cell.min(axis=0)
        max_x, max_y = cell.max(axis=0)
        
        waypoints = []
        y = min_y + self.resolution / 2
        
        while y < max_y:
            if direction == 0:  # Left to right
                waypoints.append([min_x + self.resolution/2, y])
                waypoints.append([max_x - self.resolution/2, y])
            else:  # Right to left
                waypoints.append([max_x - self.resolution/2, y])
                waypoints.append([min_x + self.resolution/2, y])
            
            y += self.resolution
            direction = 1 - direction
        
        return waypoints
```

### Pattern 3: ROS2 Path Publisher

```python
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class PathPublisher(Node):
    """Publish planned path for visualization and execution."""
    
    def __init__(self):
        super().__init__('path_publisher')
        self.path_pub = self.create_publisher(Path, '/planned_path', 10)
        
    def publish_path(self, waypoints, frame_id='map'):
        """Convert waypoints to Path message."""
        path = Path()
        path.header.frame_id = frame_id
        path.header.stamp = self.get_clock().now().to_msg()
        
        for i, (x, y, yaw) in enumerate(waypoints):
            pose = PoseStamped()
            pose.header = path.header
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            
            # Convert yaw to quaternion
            q = self._yaw_to_quaternion(yaw)
            pose.pose.orientation.x = q[0]
            pose.pose.orientation.y = q[1]
            pose.pose.orientation.z = q[2]
            pose.pose.orientation.w = q[3]
            
            path.poses.append(pose)
        
        self.path_pub.publish(path)
        return path
    
    def _yaw_to_quaternion(self, yaw):
        """Convert yaw angle to quaternion."""
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        return [0, 0, sy, cy]
```

## Anti-Patterns

### ❌ Not considering robot dynamics
Planning paths with sharp turns that the robot cannot execute.

**What happens:** Controller oscillates, path tracking fails, robot stalls.

### ✅ Use kinodynamic planners for constrained robots
```python
# Use Hybrid A* or lattice planner for car-like robots
planner = HybridAStarPlanner(
    max_steering_angle=0.6,  # Respect vehicle limits
    wheelbase=2.5
)
```

### ❌ Ignoring costmap inflation
Planning through narrow gaps smaller than robot footprint.

**What happens:** Collisions with obstacles, planner oscillates.

### ✅ Respect robot footprint
```python
def is_valid(self, gy, gx):
    # Check all cells within robot radius
    radius_cells = int(self.robot_radius / self.resolution)
    for dy in range(-radius_cells, radius_cells+1):
        for dx in range(-radius_cells, radius_cells+1):
            if not self.is_free(gy+dy, gx+dx):
                return False
    return True
```

### ❌ No path smoothing
Outputting raw A* path with jagged edges.

**What happens:** Jerky robot motion, high motor wear.

### ✅ Smooth paths with spline interpolation
```python
from scipy.interpolate import CubicSpline

def smooth_path(path):
    """Smooth path with cubic spline."""
    t = np.linspace(0, 1, len(path))
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    
    cs_x = CubicSpline(t, x)
    cs_y = CubicSpline(t, y)
    
    t_smooth = np.linspace(0, 1, len(path) * 10)
    return list(zip(cs_x(t_smooth), cs_y(t_smooth)))
```

## Configuration Reference

### Heuristic Functions

| Heuristic | Formula | Best For |
|-----------|---------|----------|
| Manhattan | \|x₁-x₂\| + \|y₁-y₂\| | Grid, 4-connected |
| Euclidean | √((x₁-x₂)² + (y₁-y₂)²) | Any-angle, smooth paths |
| Diagonal | max(\|dx\|, \|dy\|) + (√2-1)min(\|dx\|, \|dy\|) | 8-connected grids |
| Dubins/Reeds-Shepp | Shortest path with curvature | Car-like robots |

### Planning Algorithm Selection

| Scenario | Recommended Algorithm | Why |
|----------|----------------------|-----|
| Small grid | A* | Optimal, fast |
| Large grid | Jump Point Search | 10x speedup over A* |
| High-dof arm | RRT-Connect | Handles many dimensions |
| Car-like robot | Hybrid A*, RRT* | Respects non-holonomic constraints |
| Real-time replanning | D*, ARA* | Reuse previous search |
| Smooth paths | CHOMP, TrajOpt | Optimization-based |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Planner too slow | Large search space | Use hierarchical planning, reduce resolution |
| Jerky paths | No smoothing | Apply spline smoothing or optimization |
| Path through obstacles | Wrong costmap or footprint | Verify costmap inflation, robot radius |
| Sharp turns | Euclidean distance heuristic | Use Dubins/Reeds-Shepp for car-like |
| Incomplete coverage | Poor decomposition | Use proper cell decomposition |
| Planner oscillates | Goal too close to obstacle | Increase goal tolerance or clear obstacles |
| RRT not converging | Narrow passages | Increase sampling near obstacles (RRT-Connect) |

## Workflow Integration

- **Before this:** Use `nav2` for standard navigation, `sensor-fusion-slam` for localization
- **After this:** Use `control-systems` for trajectory following
- **Parallel with:** Use `gazebo` for testing planners in simulation
- **For deployment:** Use `safety-systems` for collision checking

## Further Reading

- [Planning Algorithms by LaValle](http://planning.cs.uiuc.edu/)
- [OMPL Documentation](https://ompl.kavrakilab.org/)
- [Hybrid A* Paper](https://ai.stanford.edu/~ddolgov/papers/dolgov_gpp_stair08.pdf)
- Related skills: `nav2`, `control-systems`, `robot-modeling`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering A*, RRT/RRT*, Hybrid A*, coverage planning