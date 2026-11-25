---
name: python-refactoring
description: Suggest Python code improvements and refactoring for LocalShift
triggers:
  - "refactor this"
  - "improve this code"
  - "simplify this"
  - "make this cleaner"
  - "reduce complexity"
  - "extract method"
  - "code review this"
actions:
  - analyze_complexity
  - suggest_refactoring
  - identify_duplication
  - improve_type_hints
  - extract_patterns
---

## What I Do

Analyze Python code in the LocalShift codebase and suggest improvements for readability, maintainability, performance, and adherence to Python best practices. I help keep the codebase clean as it grows.

## When to Use Me

- "Refactor this function"
- "This code is too complex"
- "Can you simplify this?"
- "Review this module"
- "Extract this into a method"
- "This looks like duplication"
- "Improve the type hints here"
- "Make this more Pythonic"

## Analysis Capabilities

### 1. Complexity Analysis

Identify overly complex functions:

```python
# High complexity - consider refactoring
def evaluate_state_machine(self, data: CoordinatorData) -> ChargingDecision:
    # 50+ lines with nested if/else
    # Multiple nested loops
    # High cyclomatic complexity
    pass
```

**Suggested refactoring:**
- Extract decision branches into separate methods
- Use early returns to reduce nesting
- Apply Strategy pattern for different modes

### 2. Code Duplication Detection

Find repeated patterns:

```python
# Duplicated pattern in multiple places
price_with_markup = base_price * (1 + MARKUP_PERCENTAGE / 100)

# Should be: Extract to method or constant
```

### 3. Type Hint Improvements

```python
# Before - vague types
def calculate(self, data):
    return result

# After - specific types
def calculate(self, data: CoordinatorData) -> ChargingDecision:
    return result
```

### 4. Performance Optimizations

Identify inefficient patterns:

```python
# Inefficient - creates new list each iteration
for i in range(len(items)):
    process(items[i])

# Better - iterator
for item in items:
    process(item)

# Inefficient - multiple dict lookups
if key in data and data[key] is not None:
    value = data[key]

# Better - single lookup
value = data.get(key)
if value is not None:
    ...
```

## Common Refactoring Patterns

### Pattern 1: Extract Method

**Before:**
```python
def process_battery_data(self, data):
    # Validate
    if not data:
        raise ValueError("No data")
    if data.percent < 0 or data.percent > 100:
        raise ValueError("Invalid percent")
    
    # Calculate
    remaining = data.capacity * (data.percent / 100)
    hours = remaining / data.discharge_rate
    
    # Store
    self.remaining_capacity = remaining
    self.hours_remaining = hours
```

**After:**
```python
def process_battery_data(self, data: BatteryData) -> None:
    self._validate_battery_data(data)
    self._calculate_remaining(data)
    self._store_results()

def _validate_battery_data(self, data: BatteryData) -> None:
    if not data:
        raise ValueError("No data")
    if not 0 <= data.percent <= 100:
        raise ValueError("Invalid percent")

def _calculate_remaining(self, data: BatteryData) -> None:
    self._remaining = data.capacity * (data.percent / 100)
    self._hours = self._remaining / data.discharge_rate

def _store_results(self) -> None:
    self.remaining_capacity = self._remaining
    self.hours_remaining = self._hours
```

### Pattern 2: Replace Conditional with Polymorphism

**Before:**
```python
def execute_mode(self, mode: BatteryMode):
    if mode == BatteryMode.SELF_CONSUMPTION:
        self._run_self_consumption()
    elif mode == BatteryMode.GRID_CHARGING:
        self._run_grid_charging()
    elif mode == BatteryMode.BOOST_CHARGING:
        self._run_boost_charging()
    # ... more modes
```

**After:**
```python
# Use strategy pattern
class ModeStrategy(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SelfConsumptionStrategy(ModeStrategy):
    def execute(self) -> None:
        ...

# In coordinator
self._strategies: dict[BatteryMode, ModeStrategy] = {
    BatteryMode.SELF_CONSUMPTION: SelfConsumptionStrategy(),
    # ...
}

def execute_mode(self, mode: BatteryMode) -> None:
    strategy = self._strategies.get(mode)
    if strategy:
        strategy.execute()
```

### Pattern 3: Simplify Boolean Expressions

**Before:**
```python
if (price < threshold and mode != BatteryMode.MANUAL and 
    automation_enabled and not dry_run):
    do_something()
```

**After:**
```python
@property
def can_execute_automation(self) -> bool:
    return (
        self.mode != BatteryMode.MANUAL
        and self.automation_enabled 
        and not self.dry_run
    )

if price < threshold and self.can_execute_automation:
    do_something()
```

## LocalShift-Specific Patterns

### Entity Platform Refactoring

Many entity platforms follow similar patterns. Extract common functionality:

```python
# Base class for LocalShift entities
class LocalShiftEntity(Entity):
    """Base entity for LocalShift integration."""
    
    def __init__(self, coordinator: LocalShiftCoordinator) -> None:
        self.coordinator = coordinator
        self._attr_should_poll = False
    
    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success
```

### Coordinator Data Access

Simplify coordinator data access patterns:

```python
# Before - verbose
data = self.coordinator.data
if data is not None:
    battery_percent = data.battery_percent
    grid_price = data.grid_price

# After - property
@property
def data(self) -> CoordinatorData | None:
    return self.coordinator.data

# Usage
if self.data:
    battery_percent = self.data.battery_percent
```

## Tools Integration

Use with existing tools:

```bash
# Check complexity with radon
uv run radon cc custom_components/localshift -a

# Check maintainability index
uv run radon mi custom_components/localshift

# Find code smells with pylint
uv run pylint custom_components/localshift

# Format with ruff
uv run ruff check --select I custom_components/localshift
uv run ruff format custom_components/localshift
```

## Refactoring Checklist

Before suggesting refactoring:

- [ ] Is the code currently working? (Don't refactor broken code)
- [ ] Are there tests covering this code? (Refactor with safety net)
- [ ] Is the improvement significant? (Don't refactor for style alone)
- [ ] Will this improve maintainability?
- [ ] Will this make the code more readable?

## Tips

1. **Test first:** Always have tests before refactoring
2. **Small steps:** One refactoring at a time
3. **Behavior preservation:** Functionality should remain identical
4. **Use type hints:** They make refactoring safer
5. **Check ruff:** Run linting after changes
6. **Update docs:** If refactoring affects public APIs

## Command Reference

```bash
# Check complexity
uv run radon cc custom_components/localshift --average

# Check specific file complexity
uv run radon cc custom_components/localshift/coordinator.py -s

# Format code
uv run ruff format custom_components/localshift

# Check imports
uv run ruff check --select I custom_components/localshift

# Run all checks
uv run ruff check custom_components/localshift
```
