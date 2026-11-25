---
name: property-based-testing
description: Hypothesis property-based testing strategies for Python with custom strategies for financial data, API responses, and stateful testing
triggers:
  - property based testing
  - hypothesis
  - fuzzing
  - mutation testing
  - mutmut
  - generative testing
---

# Property-Based Testing

Use Hypothesis to find edge cases automatically. Includes custom strategies for financial data, API responses, and stateful testing.

## Core Patterns

```python
from hypothesis import given, strategies as st, settings, assume
import hypothesis.extra.numpy as npst

# Basic property test
@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.text(min_size=1))
def test_string_roundtrip(s):
    encoded = s.encode("utf-8")
    assert encoded.decode("utf-8") == s
```

## Custom Strategies for Financial Data

```python
from hypothesis import strategies as st
from decimal import Decimal

# Price strategy (realistic trading range)
prices = st.decimals(min_value=Decimal("0.01"), max_value=Decimal("1000000"),
                     places=8, allow_nan=False, allow_infinity=False)

# Order quantity
quantities = st.decimals(min_value=Decimal("0.001"), max_value=Decimal("10000"),
                         places=3, allow_nan=False, allow_infinity=False)

# OHLCV candle
@st.composite
def candles(draw):
    open_price = draw(prices)
    close_price = draw(prices)
    high = max(open_price, close_price) + draw(st.decimals(
        min_value=Decimal("0"), max_value=Decimal("100"), places=8))
    low = min(open_price, close_price) - draw(st.decimals(
        min_value=Decimal("0"), max_value=min(open_price, close_price), places=8))
    volume = draw(quantities)
    return {"open": open_price, "high": high, "low": low, "close": close_price, "volume": volume}

@given(candle=candles())
def test_candle_invariants(candle):
    assert candle["high"] >= candle["low"]
    assert candle["high"] >= candle["open"]
    assert candle["high"] >= candle["close"]
    assert candle["low"] <= candle["open"]
    assert candle["low"] <= candle["close"]
```

## Stateful Testing

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, initialize

class AgentPoolMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.pool = AgentPool(max_size=5)
        self.expected_count = 0

    @rule(name=st.text(min_size=1, max_size=50))
    def add_agent(self, name):
        if self.expected_count < 5:
            self.pool.add(Agent(name=name))
            self.expected_count += 1

    @rule()
    def remove_random(self):
        if self.expected_count > 0:
            self.pool.remove_oldest()
            self.expected_count -= 1

    @invariant()
    def count_matches(self):
        assert len(self.pool) == self.expected_count

    @invariant()
    def never_exceeds_max(self):
        assert len(self.pool) <= 5

TestAgentPool = AgentPoolMachine.TestCase
```

## Mutation Testing with mutmut

```bash
# Run mutation testing
mutmut run --paths-to-mutate=src/coremind/core/ --tests-dir=tests/unit/

# View surviving mutants
mutmut results

# Show specific mutant
mutmut show 42

# Apply mutant to see what changed
mutmut apply 42
```

Surviving mutants = code that can be changed without test failure = missing test coverage.

## pytest Integration

```ini
# pyproject.toml
[tool.hypothesis]
max_examples = 200
deadline = 5000  # ms
database_backend = "directory"
suppress_health_check = ["too_slow"]

[tool.pytest.ini_options]
markers = [
    "hypothesis: property-based tests",
]
```

```bash
# Run with statistics
pytest -v -k "hypothesis" --hypothesis-show-statistics

# Run with specific seed (reproduce failure)
pytest --hypothesis-seed=12345
```
