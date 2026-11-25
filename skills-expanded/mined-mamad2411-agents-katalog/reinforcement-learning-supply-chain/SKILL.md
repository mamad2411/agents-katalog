---
name: reinforcement-learning-supply-chain
description: When the user wants to apply reinforcement learning to supply chain problems, learn optimal policies, or solve sequential decision-making under uncertainty. Also use when the user mentions "reinforcement learning," "Q-learning," "deep Q-networks," "policy gradient," "actor-critic," "RL for inventory," "dynamic pricing with RL," "warehouse robot control," or "sequential optimization." For forecasting, see neural-networks-forecasting. For static optimization, see optimization-modeling.
---

# Reinforcement Learning for Supply Chain

You are an expert in applying reinforcement learning to supply chain sequential decision-making problems. Your goal is to help design, train, and deploy RL agents that learn optimal policies for inventory control, pricing, routing, and resource allocation through interaction with environments.

## Initial Assessment

1. **Problem Type**: Sequential decisions? (inventory orders, pricing adjustments, routing)
2. **State Space**: What information available? (inventory levels, demand, prices)
3. **Action Space**: What decisions? (order quantities, prices, routes)
4. **Reward Function**: How measure performance? (profit, service level, cost)
5. **Environment**: Simulator available or real system?

---

## RL Fundamentals

**Markov Decision Process (MDP):**
- States (S): system conditions
- Actions (A): available decisions  
- Transitions (P): state dynamics
- Rewards (R): immediate feedback
- Policy (π): state → action mapping

**Goal:** Learn policy π that maximizes expected cumulative reward

---

## Q-Learning for Inventory Control

```python
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class InventoryEnvironment:
    """
    Inventory control environment
    
    State: current inventory level
    Action: order quantity
    Reward: -holding_cost - backorder_cost + revenue
    """
    
    def __init__(self,
                 max_inventory=50,
                 holding_cost=1.0,
                 backorder_cost=10.0,
                 order_cost=2.0,
                 price=15.0):
        
        self.max_inventory = max_inventory
        self.h_cost = holding_cost
        self.b_cost = backorder_cost
        self.o_cost = order_cost
        self.price = price
        
        # Demand distribution (Poisson)
        self.mean_demand = 10
        
        self.state = 20  # Initial inventory
    
    def reset(self):
        """Reset environment"""
        self.state = 20
        return self.state
    
    def step(self, action):
        """
        Take action (order quantity), observe demand, get reward
        
        Returns: next_state, reward, done
        """
        
        # Order arrives
        inventory_after_order = min(self.state + action, self.max_inventory)
        
        # Demand occurs (stochastic)
        demand = np.random.poisson(self.mean_demand)
        
        # Satisfy demand
        sales = min(inventory_after_order, demand)
        backorder = max(0, demand - inventory_after_order)
        
        next_inventory = inventory_after_order - sales
        
        # Calculate reward
        revenue = self.price * sales
        holding = self.h_cost * next_inventory
        backorder_penalty = self.b_cost * backorder
        ordering = self.o_cost * action
        
        reward = revenue - holding - backorder_penalty - ordering
        
        self.state = next_inventory
        done = False
        
        return next_inventory, reward, done


class QLearningAgent:
    """
    Q-Learning agent for inventory control
    """
    
    def __init__(self,
                 state_space,
                 action_space,
                 learning_rate=0.1,
                 discount_factor=0.95,
                 epsilon=0.1):
        
        self.states = state_space
        self.actions = action_space
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        # Q-table: Q(s, a)
        self.Q = defaultdict(lambda: defaultdict(float))
    
    def select_action(self, state):
        """
        Epsilon-greedy action selection
        """
        
        if np.random.random() < self.epsilon:
            # Explore: random action
            return np.random.choice(self.actions)
        else:
            # Exploit: best action
            q_values = [self.Q[state][a] for a in self.actions]
            best_action = self.actions[np.argmax(q_values)]
            return best_action
    
    def update(self, state, action, reward, next_state):
        """
        Q-learning update rule
        
        Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') - Q(s,a)]
        """
        
        # Current Q-value
        current_q = self.Q[state][action]
        
        # Best Q-value for next state
        next_q_values = [self.Q[next_state][a] for a in self.actions]
        max_next_q = max(next_q_values)
        
        # TD target
        target = reward + self.gamma * max_next_q
        
        # Update
        self.Q[state][action] = current_q + self.lr * (target - current_q)
    
    def get_policy(self):
        """Extract greedy policy from Q-values"""
        
        policy = {}
        for state in self.states:
            q_values = [self.Q[state][a] for a in self.actions]
            best_action = self.actions[np.argmax(q_values)]
            policy[state] = best_action
        
        return policy


# Training
env = InventoryEnvironment()
agent = QLearningAgent(
    state_space=list(range(51)),
    action_space=list(range(21)),  # Order 0-20 units
    learning_rate=0.1,
    discount_factor=0.95,
    epsilon=0.1
)

n_episodes = 10000
episode_rewards = []

for episode in range(n_episodes):
    state = env.reset()
    total_reward = 0
    
    for t in range(30):  # 30-day horizon
        action = agent.select_action(state)
        next_state, reward, done = env.step(action)
        
        agent.update(state, action, reward, next_state)
        
        total_reward += reward
        state = next_state
        
        if done:
            break
    
    episode_rewards.append(total_reward)
    
    if (episode + 1) % 1000 == 0:
        avg_reward = np.mean(episode_rewards[-100:])
        print(f"Episode {episode+1}: Avg Reward = {avg_reward:.2f}")

# Extract learned policy
policy = agent.get_policy()

print("\nLearned Policy (Inventory → Order Quantity):")
for inventory in range(0, 51, 5):
    order = policy.get(inventory, 0)
    print(f"  Inventory {inventory}: Order {order}")
```

---

## Deep Q-Network (DQN) for Complex States

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

class DQN(nn.Module):
    """
    Deep Q-Network
    """
    
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(DQN, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, state):
        return self.network(state)


class DQNAgent:
    """
    DQN Agent with Experience Replay and Target Network
    """
    
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99):
        
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        
        # Main network
        self.q_network = DQN(state_dim, action_dim)
        
        # Target network
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        
        # Experience replay buffer
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
    
    def select_action(self, state, epsilon=0.1):
        """Epsilon-greedy action selection"""
        
        if random.random() < epsilon:
            return random.randint(0, self.action_dim - 1)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.q_network(state_tensor)
            return q_values.argmax().item()
    
    def store_transition(self, state, action, reward, next_state, done):
        """Store experience in replay buffer"""
        self.memory.append((state, action, reward, next_state, done))
    
    def train(self):
        """Train on mini-batch from replay buffer"""
        
        if len(self.memory) < self.batch_size:
            return
        
        # Sample mini-batch
        batch = random.sample(self.memory, self.batch_size)
        
        states = torch.FloatTensor([t[0] for t in batch])
        actions = torch.LongTensor([t[1] for t in batch])
        rewards = torch.FloatTensor([t[2] for t in batch])
        next_states = torch.FloatTensor([t[3] for t in batch])
        dones = torch.FloatTensor([t[4] for t in batch])
        
        # Current Q-values
        q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        
        # Target Q-values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            targets = rewards + self.gamma * next_q_values * (1 - dones)
        
        # Loss and update
        loss = self.loss_fn(q_values.squeeze(), targets)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def update_target_network(self):
        """Copy weights from main network to target network"""
        self.target_network.load_state_dict(self.q_network.state_dict())
```

---

## Policy Gradient for Continuous Actions

```python
class PolicyNetwork(nn.Module):
    """
    Policy network for continuous actions
    """
    
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(PolicyNetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh()
        )
        
        # Mean and std for Gaussian policy
        self.mean_layer = nn.Linear(hidden_dim, action_dim)
        self.log_std_layer = nn.Linear(hidden_dim, action_dim)
    
    def forward(self, state):
        features = self.network(state)
        mean = self.mean_layer(features)
        log_std = self.log_std_layer(features)
        std = torch.exp(log_std)
        
        return mean, std


class PolicyGradientAgent:
    """
    REINFORCE algorithm for policy gradient
    """
    
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.99):
        
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma
        
        self.saved_log_probs = []
        self.rewards = []
    
    def select_action(self, state):
        """Sample action from policy"""
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        mean, std = self.policy(state_tensor)
        
        # Sample from Gaussian
        dist = torch.distributions.Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum()
        
        self.saved_log_probs.append(log_prob)
        
        return action.numpy()[0]
    
    def update(self):
        """Update policy using REINFORCE"""
        
        # Calculate returns
        returns = []
        R = 0
        
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        returns = torch.tensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)
        
        # Policy gradient
        policy_loss = []
        for log_prob, R in zip(self.saved_log_probs, returns):
            policy_loss.append(-log_prob * R)
        
        policy_loss = torch.stack(policy_loss).sum()
        
        # Update
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()
        
        # Clear buffers
        self.saved_log_probs = []
        self.rewards = []
```

---

## Applications

### 1. Dynamic Pricing

```python
# State: inventory, time, competitor prices, demand signals
# Action: price adjustment
# Reward: revenue - costs
```

### 2. Warehouse Robot Control

```python
# State: robot position, item locations, orders
# Action: movement and pick decisions
# Reward: -time - collisions + items picked
```

### 3. Supply Chain Network Optimization

```python
# State: inventory at all nodes, pipeline inventory, demand
# Action: shipment quantities between nodes
# Reward: -costs + service level bonuses
```

### 4. Order Fulfillment

```python
# State: orders, inventory, capacity, time
# Action: order-to-warehouse assignment
# Reward: -shipping cost - delay penalties
```

---

## Tools & Libraries

**Python RL:**
- `stable-baselines3`: RL algorithms
- `Ray RLlib`: Distributed RL
- `TensorFlow Agents`: TF-based RL
- `PyTorch`: Custom implementations

**Simulation:**
- `SimPy`: Discrete-event simulation
- `Gym`: RL environments
- Custom simulators

---

## Related Skills

- **optimization-modeling**: traditional optimization
- **optimization-ml-hybrid**: RL + optimization
- **dynamic-pricing`: pricing applications
- **inventory-optimization**: inventory control
- **route-optimization`: VRP with RL
