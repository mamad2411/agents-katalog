# Decision Scoring & Orchestration Guide

## 🎯 Decision Scoring System

### Purpose
The decision scoring system evaluates and ranks potential next actions based on multiple criteria to ensure optimal workflow progression.

### Scoring Criteria
**Decision Factors**:
1. **Intent Alignment** - How well action matches current goal
2. **State Relevance** - Appropriateness for current workflow state
3. **Evidence Strength** - Quality of supporting data
4. **Recency** - Timeliness of the action
5. **Preference** - User/system preferences

### Scoring Thresholds
```bash
# Check scoring configuration
cat tools/decision_scoring/advanced_score.py | grep -A 10 "thresholds"
```

**Gate Levels**:
- **EXPLORE** (0.3-0.6) - Experimental actions
- **EXECUTE** (0.6-0.8) - Standard actions
- **PRIORITY** (0.8-1.0) - High-priority actions

## 🔄 Orchestration Workflow

### Execution Flow
```bash
# 1. Generate decision candidates
python3 tools/run_role.py [role_name]

# 2. Score candidates
python3 tools/decision_scoring/advanced_score.py

# 3. Trigger next action
python3 tools/orchestrator/trigger_next.py
```

### State Engine
```bash
# Check current state
cat workflow_state.json

# Monitor state transitions
tail -f logs/state_transitions.log
```

**State Management**:
- **Idempotent transitions** - Safe state changes
- **Provenance tracking** - Artifact history
- **Rollback support** - State recovery

## 🛠️ Decision Scoring Tools

### Advanced Score Calculator
```bash
# Run scoring with calibration
python3 tools/decision_scoring/advanced_score.py --calibrate

# Run with exploration mode
python3 tools/decision_scoring/advanced_score.py --explore

# Run with shadow mode (comparison)
python3 tools/decision_scoring/advanced_score.py --shadow
```

### Output Analysis
```bash
# Check decision results
cat decision_candidates.json

# View scoring trace
cat logs/decision_scoring/trace.json

# Check metrics
cat logs/observability/summary.json
```

## 🎭 AI Persona Orchestration

### Role Execution Modes
```bash
# Standard execution
python3 tools/run_role.py [role_name]

# Peer review mode
python3 tools/run_role.py principal_engineer_ai --mode PEER_REVIEW

# Synthesis mode
python3 tools/run_role.py principal_engineer_ai --mode SYNTHESIS
```

### Execution Orchestrator
```bash
# Check orchestrator status
cat .cursor/rules/orchestrator/execution_orchestrator.md

# View memory bridge
cat .cursor/rules/orchestrator/framework_memory_bridge.md
```

## 📊 Observability & Metrics

### Metrics Collection
```bash
# Aggregate metrics
python3 tools/observability/aggregate.py

# View summary
cat logs/observability/summary.json

# Check performance
cat logs/observability/performance.json
```

### Provenance Tracking
```bash
# Generate artifact index
python3 tools/artifacts/hash_index.py

# Check artifact history
cat memory-bank/artifacts_index.json
```

## 🔧 Configuration & Customization

### Scoring Weights
```bash
# Adjust scoring weights
vim tools/decision_scoring/advanced_score.py

# Key parameters:
# - INTENT_WEIGHT
# - STATE_WEIGHT  
# - EVIDENCE_WEIGHT
# - RECENCY_WEIGHT
# - PREFERENCE_WEIGHT
```

### Threshold Adjustment
```bash
# Modify gate thresholds
vim tools/decision_scoring/advanced_score.py

# Key thresholds:
# - EXPLORE_THRESHOLD
# - EXECUTE_THRESHOLD
# - PRIORITY_THRESHOLD
```

## 🚀 Quick Start Commands

### Complete Pipeline
```bash
# Run full orchestration
python3 tools/quickstart.py
```

### Manual Orchestration
```bash
# 1. Generate candidates
python3 tools/run_role.py product_owner_ai

# 2. Score decisions
python3 tools/decision_scoring/advanced_score.py

# 3. Execute next action
python3 tools/orchestrator/trigger_next.py
```

### Monitoring
```bash
# Watch orchestration progress
tail -f logs/orchestrator/execution.log

# Check decision flow
tail -f logs/decision_scoring/flow.log
```

## 🔍 Troubleshooting

### Common Issues
1. **Scoring Failures**: Check input data quality
2. **State Conflicts**: Validate workflow_state.json
3. **Role Failures**: Check role execution logs
4. **Memory Issues**: Verify artifacts_index.json

### Debug Commands
```bash
# Enable debug mode
export ADVANCEDRULES_DEBUG=1

# Run with verbose output
python3 tools/decision_scoring/advanced_score.py --verbose

# Check specific component
python3 tools/orchestrator/trigger_next.py --debug
```

## 📚 Related Documentation

### Core Components
- **Execution Orchestrator** - `.cursor/rules/orchestrator/execution_orchestrator.md`
- **Memory Bridge** - `.cursor/rules/orchestrator/framework_memory_bridge.md`
- **Rules Master Toggle** - `.cursor/rules/orchestrator/rules_master_toggle.md`

### Decision System
- **Decision Gate** - `.cursor/rules/decision_gate.mdc`
- **Decision Scoring** - `.cursor/rules/decision_scoring.mdc`
- **Decision Scoring Tool** - `.cursor/rules/decision_scoring_tool.mdc`
description:
globs:
alwaysApply: true
---
