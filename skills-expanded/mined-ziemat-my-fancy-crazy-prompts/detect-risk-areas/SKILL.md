name: detect-risk-areas
description: Identifies Python code most likely to break or cause regressions. Use this when analyzing a codebase to prioritize testing efforts and understand where bugs are most likely to occur.

---

# Detect Risk Areas

## Purpose

Identify Python code most likely to break or cause regressions. This skill analyzes code to find high-risk areas that deserve extra testing attention, based on complexity, change frequency, and failure impact.

## Use when

- Prioritizing test coverage for a large codebase
- Planning testing efforts for a new feature
- Performing code reviews for risky changes
- Deciding where to add regression tests
- Assessing technical debt and testing gaps

## Do not use when

- You need to identify specific test cases (use `find-edge-cases` instead)
- You're debugging a specific failure
- You're writing new tests for a small, isolated function

## Inputs

- Python source code or entire modules
- Git history or change information (optional but helpful)
- Test coverage data (optional but helpful)
- Error logs or incident reports (optional but helpful)

## Outputs

- Ranked list of risk areas with risk scores
- Risk category for each area (complexity, change-prone, impact, etc.)
- Specific recommendations for testing each risk area

## Method

1. **Analyze code complexity**
   - Count cyclomatic complexity (branches, loops, conditionals)
   - Identify deeply nested code
   - Find long functions (>50 lines)
   - Note complex type unions and optional chains

2. **Identify change-prone areas**
   - Look for code with many recent changes (if history available)
   - Find "TODO" and "FIXME" comments
   - Identify code that handles multiple error paths
   - Note workarounds and hacks

3. **Assess failure impact**
   - Code affecting external systems (DB, API, filesystem)
   - Data transformation logic
   - Validation and sanitization code
   - Security-sensitive operations

4. **Find integration points**
   - Module boundaries and imports
   - Third-party library usage
   - Protocol implementations (HTTP, database, file formats)
   - Async boundaries and concurrency

5. **Look for anti-patterns**
   - Global state and mutable defaults
   - Silent exception swallowing
   - Long try/except blocks
   - Complex conditional logic without tests

## Risk Categories

- **Complexity**: Code is hard to understand and maintain
- **Change-prone**: Code changes frequently, increasing regression risk
- **Impact**: Failure would cause significant business or technical damage
- **Integration**: Code interacts with external systems or complex dependencies
- **Legacy**: Old code with unclear behavior or missing tests

## Guardrails

- Don't just flag complex code; consider whether it's well-tested
- Account for code that's intentionally simple but high-impact
- Consider the team's familiarity with the code
- Balance risk assessment with available testing resources

## Example prompts

```
Analyze this module and identify risk areas:

```python
# data_processor.py
import json
from typing import Any, Optional

class DataProcessor:
    _instances: dict[str, Any] = {}
    
    def __init__(self, config: Optional[dict] = None):
        if config is None:
            config = {}
        self.config = config
        self._cache = {}
    
    def process(self, data: Any) -> Any:
        # Complex processing logic...
        pass
```

---

Which parts of this codebase are most likely to cause regressions?

```
src/
├── auth.py       (recently changed, handles JWT)
├── payments.py   (integrates with Stripe, complex retry logic)
├── utils.py      (small helper functions, stable)
└── models.py     (database schemas, frequently modified)
```

---

Identify risk areas in this function based on its complexity:

```python
def validate_and_transform(data: dict) -> dict:
    result = {}
    try:
        if 'user' in data:
            user = data['user']
            if isinstance(user, dict):
                if 'id' in user:
                    result['user_id'] = int(user['id'])
                if 'email' in user:
                    result['email'] = validate_email(user['email'])
            elif isinstance(user, str):
                result['user_id'] = int(user)
        if 'items' in data:
            for item in data['items']:
                # ... complex logic
    except Exception as e:
        logger.warning(f"Validation failed: {e}")
    return result
```
