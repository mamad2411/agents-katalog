---
name: brain-curiosity
version: 1.0.0
description: Autonomous exploration. Tests untested skill combinations, probes knowledge gaps, experiments with alternative chains. 5% random exploration (epsilon-greedy). Triggers: connectome gaps, idle periods, heartbeat signal.
---

# Brain Curiosity — Autonomous Exploration

> **"不是被迫学。是主动想知道。"**

## Curiosity Drivers

### 1. Connectome Gaps
Two skills connected through chains but never directly tested → test the direct path

### 2. Knowledge Frontier
KB entry exists but never connected to a memory → try applying it

### 3. Counterfactual
Proven chain → reverse the order and test: "what if reasoning-lora runs BEFORE thinking-dimensions?"

### 4. Epsilon-Greedy (5%)
5% of time → random valid chain instead of highest-weight. Biological brains discover through randomness.

### 5. Underdog Bonus
Rarely-used skills get temporary +0.15 exploration boost. Prove useful → permanent. Fail → boost removed.

## Safety
- NEVER explore on L5 (high-risk) or production tasks
- Failed explorations logged but don't punish connectome
- Exploration = L2-L3 tasks only

## Integration
- **neural-orchestrator**: New chains feed back to connectome
- **brain-heartbeat**: Identifies gaps → curiosity fills them
- **memory-lora**: Exploration results stored
