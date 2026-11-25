name: find-edge-cases
description: Finds boundary conditions, invalid inputs, rare states, and surprising combinations in Python functions, classes, services, or scripts. Use this when you need to discover edge cases that could cause bugs or unexpected behavior.

---

# Find Edge Cases

## Purpose

Discover boundary conditions, invalid inputs, rare states, and surprising combinations in Python code that could cause bugs or unexpected behavior. This skill helps identify test cases that go beyond the "happy path."

## Use when

- Designing test cases for a Python function or method
- Reviewing code for potential bugs
- Creating comprehensive test suites
- Debugging intermittent issues
- Performing code reviews

## Do not use when

- You need high-level test strategy (use `identify-critical-scenarios` instead)
- You're writing implementation code
- You're debugging a specific failure (use `fix-failing-tests` instead)

## Inputs

- Python source code (functions, methods, classes)
- Type hints and annotations
- Documentation or docstrings (if available)

## Outputs

- List of edge cases with descriptions
- Priority ranking (high, medium, low)
- Suggested test assertions for each edge case

## Method

1. **Analyze input parameters**
   - Check for None vs empty vs missing values
   - Identify boundary values (0, -1, max int, empty strings)
   - Look for type coercion possibilities
   - Find optional parameters and their combinations

2. **Examine control flow**
   - Identify all branches (if/else, match/case)
   - Find loop conditions and termination cases
   - Look for exception handling paths
   - Note early returns and guard clauses

3. **Consider Python-specific behaviors**
   - Mutable default arguments
   - Truthiness of values (0, "", [], {}, None, False)
   - Iterator exhaustion
   - Generator side effects
   - Async/await edge cases

4. **Identify state-dependent behavior**
   - Object initialization states
   - Race conditions in concurrent code
   - Resource cleanup scenarios
   - Session/connection lifecycle

5. **Look for combination explosions**
   - Multiple optional parameters together
   - Nested data structures with varying depths
   - Error recovery paths
   - Retry logic scenarios

## Guardrails

- Focus on realistic edge cases, not theoretical extremes
- Consider the code's actual usage context
- Don't over-specify; focus on cases that could cause real bugs
- Prioritize edge cases that are likely to occur in production

## Example prompts

```
Find edge cases for this Python function:

```python
def parse_integers(values: list[str]) -> list[int]:
    result = []
    for v in values:
        result.append(int(v.strip()))
    return result
```

---

Identify edge cases for this async function:

```python
async def fetch_with_retry(url: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            return await api_call(url)
        except TimeoutError:
            continue
    raise ConnectionError("All retries failed")
```

---

What edge cases should I test for this class method?

```python
class ConfigLoader:
    def __init__(self, path: Path, default: dict | None = None):
        self.path = path
        self.default = default or {}
        self._config = {}
    
    def load(self) -> dict:
        # ...
```
