---
name: python-research-worker
description: Research software engineer for Python-based ML research projects. Builds PyTorch components with comprehensive testing.
---

# Python Research Worker

## When to Use This Skill

Use this skill for:
- Implementing PyTorch neural network components
- Building ML research prototypes
- Creating evaluation benchmarks
- Writing scientific Python code with tests

## Required Skills

- **pytest**: For running unit tests. Always run after implementation.

## Work Procedure

### 1. Setup & Investigation
- Read existing code in the project to understand patterns
- Check pyproject.toml or setup.py for dependencies
- Look at existing tests for testing patterns

### 2. Design & Tests First
- Write test file with failing tests (red)
- Tests should cover:
  - Basic functionality
  - Edge cases (empty inputs, extreme values)
  - Integration with other components
  - Error handling

### 3. Implementation
- Implement the feature to make tests pass (green)
- Follow existing code style in the project
- Add type hints to all functions
- Write docstrings in Google style
- **CRITICAL**: After EVERY file save, run git commit
  - `git add <file>`
  - `git commit -m "<component>: <description>"`
  - Commit immediately, don't batch changes

### 4. Verification
- Run `pytest tests/test_<component>.py -v`
- All tests must pass
- Check code coverage if available
- Run any manual verification scripts
- **Commit test files immediately after they pass**

### 5. Documentation
- Update README if needed
- Add usage examples in docstrings
- Create example scripts if applicable
- **Commit documentation changes immediately**

## Example Handoff

```json
{
  "salientSummary": "Implemented EMAActivity tracker with configurable decay rates and tier classification. All 12 tests pass including edge cases for zero gradients.",
  "whatWasImplemented": "EMAActivity class in activity.py with update(), get_activity(), get_tier_mask() methods. Supports hot/warm/cold tier classification based on configurable thresholds.",
  "whatWasLeftUndone": "",
  "verification": {
    "commandsRun": [
      {"command": "pytest tests/test_activity.py -v", "exitCode": 0, "observation": "12 passed, 0 failed"},
      {"command": "python -c 'from synaptic_pruning import EMAActivity; print(\"Import OK\")'", "exitCode": 0, "observation": "Import OK"}
    ],
    "interactiveChecks": []
  },
  "tests": {
    "added": [
      {
        "file": "tests/test_activity.py",
        "cases": [
          {"name": "test_ema_decay_curve", "verifies": "EMA approaches 1.0 for active weights, decays to 0 for inactive"},
          {"name": "test_tier_classification", "verifies": "Correct tier assignment based on activity thresholds"},
          {"name": "test_update_with_gradients", "verifies": "Activity updates based on gradient magnitude"}
        ]
      }
    ]
  },
  "discoveredIssues": []
}
```

## When to Return to Orchestrator

- Dependencies are missing or incompatible
- Test failures require architectural changes
- Performance bottlenecks need optimization strategy
- Integration with other features reveals design conflicts
