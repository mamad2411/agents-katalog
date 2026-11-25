---
name: design-model-based-reinforcement-learning
description: Use when training a reinforcement-learning agent where real-environment interaction is expensive, slow, or limited — robotics, game-playing agents, or any control task — by training a model of the environment's dynamics from real interaction data, then planning or training the policy against simulated rollouts from that learned model rather than requiring real-environment interaction for every training step.
source: 'Ha & Schmidhuber "World Models" (2018); Hafner et al. "Dream to Control: Learning Behaviors by Latent Imagination" (Dreamer, 2020) and DreamerV2/DreamerV3 (2022/2023); Schrittwieser et al. "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model" (MuZero, Nature, 2019/2020)'
tags: [reinforcement-learning, world-model, model-based-rl, sample-efficiency, planning, ai]
related: [design-ml-pipeline, design-numerical-simulation]
---

# Design Model-Based Reinforcement Learning

Train a model of the environment's dynamics from real interaction data, then plan or train the policy against simulated rollouts from that learned model — reducing how much real-environment interaction the agent needs, rather than requiring a real environment step for every unit of training.

## Why This Is Best Practice

**Adopted by:** DeepMind's MuZero (Nature, 2019/2020) learned a model of game dynamics and achieved superhuman play in Go, chess, and shogi, plus state-of-the-art results across 57 Atari games — without ever being given the actual rules of any of these games, only a learned model of how the game state changes. Hafner et al.'s Dreamer line of work (2020, DreamerV2 2022, DreamerV3 2023) trains agents almost entirely inside a learned latent world model, with DreamerV3 solving the long-standing open Minecraft "collect diamond" benchmark from scratch with no human demonstration data. Ha & Schmidhuber's original 2018 "World Models" paper demonstrated an agent trained almost entirely inside its own learned "dream" of a car-racing and VizDoom environment.

**Impact:** DreamerV1 was the first model-based agent to match top model-free reinforcement-learning algorithms on the Atari-100k sample-efficiency benchmark — achieving comparable performance with a small fraction of the real-environment interaction model-free methods require. MuZero matched or exceeded AlphaZero's superhuman performance in Go, chess, and shogi despite AlphaZero having access to the actual game rules and MuZero only having a learned approximation — demonstrating that a sufficiently accurate learned model can substitute for ground-truth environment access.

**Why best:** Model-free reinforcement learning requires a real (or fully-specified simulated) environment step for every unit of training experience, which is often expensive, slow, or physically limited — a robot can't take millions of real physical actions to train a policy the way a game emulator can generate millions of frames. Learning a dynamics model from a comparatively small amount of real interaction, then generating additional simulated experience from that model, breaks this bottleneck. This differs from `design-numerical-simulation`, which simulates a system whose governing equations or sampling distributions are already known and specified analytically — model-based RL instead *learns* the dynamics model itself from data when the governing equations aren't known or are too complex to specify directly.

Sources: Ha & Schmidhuber, "World Models" (2018); Hafner et al., "Dream to Control" (2020); Schrittwieser et al., "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model" (2019/2020).

## Steps

### 1. Define the state, action, and reward space

Specify what the agent observes (state), what it can do (action), and what signal it's optimizing (reward) — this must be defined before any data collection, since the dynamics model will be trained to predict transitions within this specific space.

### 2. Collect real-environment interaction data

Gather (state, action, next state, reward) transitions from real interaction with the environment — this can start from a random or simple baseline policy, since the goal at this stage is covering enough of the state-action space for the dynamics model to learn accurate transitions, not yet achieving good task performance.

### 3. Train a dynamics (and reward) model from the collected data

Train a model — commonly a recurrent or latent-variable neural network (as in Dreamer's recurrent state-space model, or MuZero's learned dynamics function) — to predict the next state and reward given the current state and action. This model is the "world model": an approximation of how the environment actually behaves, learned from data rather than specified analytically.

### 4. Generate simulated rollouts from the learned model

Use the trained dynamics model to simulate trajectories — sequences of states, actions, and rewards — without requiring further real-environment interaction for each one. These simulated rollouts are what make the method sample-efficient: many more rollouts can be generated from the model than could be collected from the real environment in the same time.

### 5. Plan or train the policy against the simulated rollouts

Either use the rollouts directly for planning (MuZero's Monte Carlo Tree Search over model-predicted trajectories) or use them as training data for a policy network (Dreamer's approach of training the policy inside the learned latent model, "imagining" ahead without needing the real environment at each training step).

### 6. Periodically re-ground the model against fresh real-environment data

Collect additional real interaction data using the current policy and use it to refine the dynamics model — a model trained only on early, less-competent-policy data can become inaccurate for the state-action regions a more competent policy visits, and needs periodic re-grounding to stay accurate where it matters.

## Rules

- Never train the policy indefinitely against a static, un-refreshed dynamics model — the model needs to be periodically updated with fresh real-environment data collected under the current policy, or the policy will start exploiting inaccuracies in stale parts of the model.
- Match model capacity and training data volume to the complexity of the actual dynamics — an undertrained or under-capacity dynamics model produces systematically biased simulated rollouts, which the policy will learn to exploit rather than learning genuinely good behavior.
- Use the model appropriately for the algorithm's design — MuZero-style planning uses the model at decision time (search over predicted futures); Dreamer-style approaches train the policy inside the model ahead of time. Don't conflate the two without deliberately choosing which structure fits the problem.

## Examples

**Trigger:** A robotics team needs to train a manipulation policy, but each real-world trial takes significant physical setup time and risks hardware wear.
→ Collect a moderate amount of real robot interaction data across a range of actions. Train a dynamics model predicting how the robot's state changes given an action. Generate a much larger volume of simulated rollouts from this learned model, and train the policy primarily against those simulated rollouts, using real robot time only for periodic re-grounding of the model rather than for every training step.

**Trigger:** A game-playing agent needs to learn strong play in a domain where the exact game engine/rules aren't directly exposed to the training algorithm.
→ Following MuZero's approach: learn a model that predicts the game's own internal dynamics (state transitions and rewards) purely from observed play, without access to the actual rules. Use Monte Carlo Tree Search over the learned model's predicted futures to select actions, achieving strong play without the algorithm ever being told the actual rules.

## Common Mistakes

- **Letting the policy exploit an inaccurate or stale dynamics model.** A policy trained against a model with systematic prediction errors will learn to exploit those errors rather than learning genuinely good real-environment behavior — this is the most common and consequential failure mode in model-based RL.
- **Under-investing in dynamics-model accuracy relative to policy training effort.** The entire method's value depends on the learned model being a reasonably faithful approximation of the real environment; treating model training as a lesser concern than policy optimization undermines the whole approach.
- **Never re-grounding the model against fresh real-environment data.** A model trained only on early data becomes progressively less accurate for the state-action regions a more competent, evolving policy visits.
- **Confusing this technique with first-principles numerical simulation.** Model-based RL learns the dynamics model from data specifically because the governing equations aren't known or specified — using this approach when the dynamics are already fully known analytically is unnecessary; direct simulation (`design-numerical-simulation`) is more appropriate there.

## When NOT to Use

- When the environment's dynamics are already fully known and specified analytically — direct numerical simulation (`design-numerical-simulation`) is more appropriate and doesn't carry the risk of a learned model's approximation error.
- When real-environment interaction is cheap and fast enough that model-free reinforcement learning's simplicity outweighs the sample-efficiency gain — the added complexity of learning and maintaining a dynamics model isn't worth it if real interaction was never the bottleneck.
- When the environment's dynamics are highly stochastic or chaotic in a way that makes them fundamentally difficult to model accurately — a dynamics model that can't achieve reasonable prediction accuracy will produce simulated rollouts too unreliable to train or plan against usefully.
