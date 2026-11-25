# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Dungeon Crawler RL Environment** - a custom Gymnasium environment implementing a grid-based dungeon crawler game optimized for tabular RL algorithms. The project is an academic assignment (20% grade weight) for a Reinforcement Learning course.

The environment features:
- **16×16 grid** with ONLY border walls (no interior walls)
- **Global vision** - agent sees entire 16×16 grid
- **2 mobile enemies** with random movement (instant death on contact)
- **Border walls only**: Hitting a wall = small penalty (-1.0), continues playing
- **Simple objective**: Reach the door/exit while avoiding enemies
- **State space**: 38,416 states (agent position × door position)
- **Three tabular RL algorithm implementations**: Q-Learning, SARSA, Expected SARSA

## Core Architecture

### State Space Design (Critical Implementation Detail)

**Position-Based Encoding**: The environment uses both agent and door positions:
- **Grid**: 16×16 with only border walls (14×14 interior)
- **Global vision**: Agent sees entire 16×16 grid (full observability)
- **State encoding**: Agent position (14×14) × Door position (14×14) = 38,416 states

This design is implemented across two key files:
- `environment/dungeon_env.py` - operates on 16×16 grid with global vision
- `utils/state_encoder.py` - encodes agent and door positions

State components:
- **Agent position**: 196 positions (14×14 interior, excluding border walls)
- **Door position**: 196 positions (14×14 interior, varies per episode)
- **Total state space**: 196 × 196 = 38,416 states
- Enemy positions: 2 enemies with random movement, not included in state
- Agent has global vision (sees entire 16×16 grid)

**Key Design Choice**: We encode both agent and door positions to create a state space that depends on the door's location. This allows the agent to learn different optimal paths depending on where the door spawns each episode.

### Environment Architecture (`environment/`)

**`dungeon_env.py`** (600+ lines): Main Gymnasium environment
- Implements full game loop with `reset()`, `step()`, `render()`
- 16×16 grid with ONLY border walls (no interior walls)
- 2 mobile enemies with random movement (instant death on contact)
- Global vision: agent sees entire 16×16 grid
- **Border walls**: Wall collision = small penalty (-1.0), continues playing
- Episode termination: win (reach door), lose (enemy collision), timeout (300 steps)
- Reward shaping: distance-based rewards + death penalties

**`render_pygame.py`** (480+ lines): PyGame visual renderer
- Shows entire 16×16 grid (no camera system needed)
- 48×48 pixel cells for 16×16 grid (768×868 window)
- Enemy sprites: red circles with angry eyes
- Agent sprite: blue circle with friendly eyes
- UI showing position, distance to door, steps, reward
- Only used when `render_mode='pygame'`

### Agent Implementations (`agents/`)

**Inheritance hierarchy**:
```
BaseTabularAgent (base_agent.py)
├── QLearningAgent (qlearning.py)
├── SARSAAgent (sarsa.py)
└── ExpectedSARSAAgent (expected_sarsa.py)
```

**`base_agent.py`** (200+ lines): Shared functionality
- Sparse Q-table storage using `defaultdict(lambda: np.zeros(n_actions))`
- Epsilon-greedy action selection
- Epsilon decay mechanism
- Save/load via pickle (Q-table + hyperparameters)

**Algorithm-specific files**: Each implements `update()` method with correct TD update rule
- **Q-Learning**: Off-policy, uses `max(Q(s', a))`
- **SARSA**: On-policy, uses `Q(s', a')` where `a'` is actual next action
- **Expected SARSA**: On-policy, uses expected value under epsilon-greedy policy

**Critical SARSA training detail**: SARSA requires selecting the next action BEFORE calling `update()`. See `train.py:205-231` for correct implementation.

### State Encoding (`utils/state_encoder.py`)

**Combined position encoding**: Both agent and door positions are encoded into a single integer state.

Example calculation:
```python
# Convert to interior indices (0-195 for 14×14 interior)
agent_idx = (agent_y - 1) * 14 + (agent_x - 1)
door_idx = (door_y - 1) * 14 + (door_x - 1)

# Combine into single state
state = agent_idx * 196 + door_idx  # Values from 0 to 38,415
```

The encoder receives:
- `global_view`: 16×16 numpy array with full grid state
- Extracts agent and door positions from the global view

Output: single integer state (0-38,415)

## Common Development Commands

### Training Agents

```bash
# Train Q-Learning agent for 5000 episodes
python train.py --algorithm qlearning --episodes 5000 --run-name qlearning_exp1

# Train SARSA with custom hyperparameters
python train.py --algorithm sarsa --episodes 5000 \
    --alpha 0.2 --gamma 0.99 --epsilon-decay 0.997 \
    --run-name sarsa_custom

# Train Expected SARSA
python train.py --algorithm expected_sarsa --episodes 5000 \
    --run-name expected_sarsa_exp1
```

**Hyperparameter defaults** (recommended for this environment):
- `--alpha 0.1` (learning rate)
- `--gamma 0.95` (discount factor)
- `--epsilon 1.0` (initial exploration)
- `--epsilon-decay 0.995` (reaches ~0.01 by episode 1000)
- `--epsilon-min 0.01` (maintains 1% exploration)

Trained models save to `models/{run_name}/` with checkpoints every 500 episodes.

### Monitoring Training

```bash
# Start TensorBoard to view training metrics
tensorboard --logdir logs/

# Open browser to http://localhost:6006
```

**Logged metrics**:
- Episode rewards, success rate, length
- Rolling 100-episode averages
- Q-table statistics (mean/max/min Q-values, num states visited)
- Epsilon decay curve

### Evaluating Agents

```bash
# Evaluate trained agent on 100 episodes
python evaluate.py --model models/qlearning_exp1/final_model.pkl --episodes 100

# Evaluate with text rendering
python evaluate.py --model models/qlearning_exp1/final_model.pkl \
    --episodes 5 --render
```

### Interactive Demo

```bash
# PyGame demo - watch trained agent play with visual rendering
python demo_pygame.py --model models/qlearning_exp1/final_model.pkl --fps 10

# Manual play mode - control the agent yourself
python demo_pygame.py --manual

# Controls: Arrow keys (move), Space (attack), R (reset), M (toggle mode), Q (quit)
```

### Running Tests

```bash
# Test environment functionality
python -m environment.dungeon_env

# Test state encoder
python -m utils.state_encoder

# Test pygame visual rendering
python test_pygame_visual.py
```

## Key Implementation Patterns

### 1. Training Loop Structure (SARSA Special Handling)

SARSA requires selecting the next action during training to use in the update. The training loop handles this:

```python
# For SARSA: select initial action before loop
if algorithm == 'sarsa':
    action = agent.get_action(state, training=True)

while not done:
    # Non-SARSA: select action here
    if algorithm != 'sarsa':
        action = agent.get_action(state, training=True)

    # Take step
    next_state, reward, done = env.step(action)

    # SARSA: select next action for update
    if algorithm == 'sarsa' and not done:
        next_action = agent.get_action(next_state, training=True)
    else:
        next_action = None

    # Update (SARSA uses next_action, others ignore it)
    agent.update(state, action, reward, next_state, next_action)

    # Update for next iteration
    state = next_state
    if algorithm == 'sarsa':
        action = next_action  # Reuse selected action
```

### 2. Sparse Q-Table Storage

Q-tables use `defaultdict(lambda: np.zeros(n_actions))` to only store visited states. This is critical for handling the state space efficiently.

Typical memory usage:
- Theoretical states: 38,416
- Visited states during 5000 episodes: Will vary widely based on door placement randomness
- Memory: < 5 MB per trained agent (sparse storage)

### 3. Enemy Movement System

The 2 enemies use random movement (not deterministic patrols). Each step, each enemy randomly chooses to move UP/DOWN/LEFT/RIGHT or STAY.

Movement logic from `dungeon_env.py`:
```python
# Random movement: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT, 4=STAY
move_action = np.random.randint(0, 5)
```

Enemy collision = instant death with -100 reward penalty. This adds danger and forces the agent to learn cautious navigation.

### 4. Reward Shaping Strategy

The environment uses **distance-based reward shaping** to guide learning:

| Event | Reward | Purpose |
|-------|--------|---------|
| Move closer to door | +1.0 | Encourage progress toward goal |
| Move away from door | -1.0 | Discourage wrong direction |
| Step penalty | -0.1 | Encourage efficiency (always applied) |
| **Reach door (WIN)** | **+200.0** | **Ultimate goal (doubled reward)** 🎯 |
| **Wall collision** | **-1.0** | **Small penalty for hitting border (continues playing)** |
| Enemy collision (DEATH) | -100.0 | Instant death - agent must learn to avoid enemies ⚠️ |

Net reward per step:
- **Moving closer**: +1.0 - 0.1 = **+0.9** (positive reinforcement)
- **Moving away**: -1.0 - 0.1 = **-1.1** (negative reinforcement)
- **Wall collision**: -1.0 - 0.1 = **-1.1** (small penalty, continues playing)
- **Enemy collision**: -100.0 - 0.1 = **-100.1** (INSTANT DEATH, episode terminated) ⚠️
- **Victory**: +200.0 + movement_reward - 0.1 ≈ **+199.9 to +200.9** 🎯

**DESIGN RATIONALE**:
- **Wall collisions**: Small penalty (-1.0), NOT fatal. Only border walls exist, so hitting them is rare.
- **Victory reward doubled** (+200.0): Makes reaching the goal more attractive, improving learning signal.
- **Enemy collisions**: Remain fatal (-100.0) to maintain danger and strategic depth.
- **No interior walls**: Simplifies navigation, agent focuses on avoiding enemies and reaching door.

This reward structure encourages the agent to:
1. Navigate toward the door (positive reward for getting closer)
2. Avoid moving in wrong directions (negative reward for getting farther)
3. Stay away from border walls (small penalty)
4. Avoid enemies (instant death with -100 penalty)
5. Prioritize reaching the goal (doubled victory reward)
6. Complete episodes quickly (step penalty accumulates)

## Expected Training Performance

Typical learning progression for 5000 episodes (16×16 grid with 2 random enemies):

**Q-Learning** (off-policy, fastest):
- Episodes 0-1000: Random exploration, learning basic navigation
- Episodes 1000-3000: Learning to reach door while avoiding enemies
- Episodes 3000-5000: Refined policy with better enemy avoidance
- Expected final success: **Variable** (depends heavily on enemy randomness)

**SARSA** (on-policy, conservative):
- More cautious policy development
- Better at avoiding risky paths near enemies
- Expected final success: **May be lower due to conservative exploration**

**Expected SARSA** (hybrid approach):
- Balance between Q-Learning's speed and SARSA's safety
- Expected final success: **Variable** (somewhere between the two)

**Key Challenge**: With 2 randomly moving enemies and global vision, success rates should be higher than with partial observability. The agent must learn:
1. Navigate 16×16 grid to reach door (no interior walls to block path)
2. Avoid randomly moving enemies (global vision helps with awareness)
3. Balance exploration vs exploitation
4. Learn policies for different door positions (38,416 state space)

## File Organization

```
/
├── environment/          # Gymnasium environment implementation
│   ├── dungeon_env.py         # Main environment (16×16 grid, global vision, border walls only)
│   └── render_pygame.py       # PyGame renderer (full grid display)
├── agents/              # RL algorithm implementations
│   ├── base_agent.py         # Base class with Q-table, epsilon-greedy
│   ├── qlearning.py          # Q-Learning update rule
│   ├── sarsa.py              # SARSA update rule
│   └── expected_sarsa.py     # Expected SARSA update rule
├── utils/               # Utilities
│   └── state_encoder.py      # Dict obs → integer state (agent + door positions)
├── train.py             # Training script with TensorBoard logging
├── evaluate.py          # Evaluation script with statistics
├── demo_pygame.py       # Interactive PyGame demo (manual/AI modes)
├── logs/                # TensorBoard logs (created during training)
├── models/              # Saved Q-tables (created during training)
└── requirements.txt     # Dependencies
```

## Important Constraints

1. **Grid size consistency**: If changing `grid_size` in `dungeon_env.py`, also update `state_encoder.py` to match
2. **Global vision**: Agent sees entire 16×16 grid (full observability)
3. **State encoding**: Current encoding uses agent + door positions (38,416 states). This allows learning policies that depend on door location.
4. **SARSA training**: Must follow the special action selection pattern (see training loop above)
5. **Pickle compatibility**: Q-table saving converts `defaultdict` to regular dict; loading recreates `defaultdict`
6. **Enemy mechanics**: 2 enemies with random movement, instant death on contact
7. **Border walls only**: No interior walls, simplifying navigation

## Academic Context

This project fulfills **Option B: Environment Design** requirements:
- Custom Gymnasium environment with well-designed state space (38,416 states)
- Tabular RL algorithm implementations (Q-Learning, SARSA, Expected SARSA)
- Comprehensive documentation and analysis
- Complexity justification: tractable state space (38,416 states) with added challenge from:
  - Global observability (sees entire 16×16 grid)
  - 2 randomly moving enemies (stochastic environment)
  - Death penalty encouraging careful exploration
  - Distance-based reward shaping
  - Door position varies per episode (state includes door location)
  - Border walls only (no interior obstacles)

Grade weight: 20% (16% complexity + 4% documentation)
