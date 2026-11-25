# Skill: HTN Planner

## Description
A Hierarchical Task Network (HTN) planner and visualizer. It allows defining domains and problems in JSON, visualizing the plan decomposition tree using Mermaid, and simulating execution.

## Usage
```bash
# Visualize a plan
node skills/htn-planner/index.js --action visualize --domain domain.json --problem problem.json --output plan.mmd

# Simulate execution
node skills/htn-planner/index.js --action simulate --domain domain.json --problem problem.json
```

## Input Format (JSON)
### Domain
```json
{
  "tasks": {
    "root": { "type": "compound", "methods": ["m1", "m2"] },
    "m1": { "type": "method", "subtasks": ["t1", "t2"] },
    "t1": { "type": "primitive", "action": "do_something" }
  }
}
```

### Problem
```json
{
  "state": { "loc": "home" },
  "goal": ["root"]
}
```
