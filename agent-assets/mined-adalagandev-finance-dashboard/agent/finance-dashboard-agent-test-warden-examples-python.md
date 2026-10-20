# Unit Test Rules — Python Examples

**Framework basis:** Python 3.11+, pytest 7.x+, unittest.mock (stdlib).
The rules themselves are framework-agnostic — these examples only show one
concrete stack.
**Translation hints:** unittest → TestCase methods, subTest ≈ parametrize
(weaker: cases don't report individually by default); nose2 → similar to
unittest; Hypothesis → complements rule 12 for property-based cases.
**Version-sensitive:** pytest 7.x+ shown (`pytest.raises` as context manager,
modern `parametrize`). `unittest.mock` syntax is stable across 3.8+.

## Rule 1 — Test behavior, not implementation
Violation:
```python
def test_place_order():
    service.place_order(cmd)
    service._validate.assert_called_once()      # internal call sequence
    assert service._last_validated == cmd       # private state
```
Correct:
```python
def test_placed_order_is_persisted_with_pending_status():
    order = service.place_order(cmd)
    assert repo.get(order.id).status == Status.PENDING   # observable effect
```

## Rule 2 — One logical assertion per test
Violation:
```python
def test_coupon_logic():                 # which behavior failed? unclear
    assert apply(expired).rejected
    assert apply(valid).discount == 10
    assert apply(used).rejected
```
Correct:
```python
def test_expired_coupon_is_rejected(): ...
def test_valid_coupon_applies_its_discount(): ...
def test_already_used_coupon_is_rejected(): ...
```

## Rule 3 — Arrange-Act-Assert
Violation:
```python
def test_cart():
    cart = Cart()
    cart.add(item_a)                     # act
    assert cart.total == 10              # assert
    cart.add(item_b)                     # act again — second test hiding
    assert cart.total == 25
```
Correct:
```python
def test_adding_one_item_sets_total_to_its_price():
    cart = Cart()                        # arrange
    cart.add(item_a)                     # act
    assert cart.total == 10              # assert
def test_adding_second_item_accumulates_total(): ...
```

## Rule 4 — Deterministic and isolated
Violation:
```python
def test_fetch_rates():
    rates = client.fetch("https://api.fx.example")   # real network
    time.sleep(2)                                    # timing hope
    assert rates["EUR"] > 0
```
Correct:
```python
def test_conversion_uses_fetched_rate():
    client = StubFxClient({"EUR": 1.1})              # fake at the port
    assert Converter(client).convert(100, "EUR") == 110
```

## Rule 5 — Fake the ports, not the internals
Violation:
```python
service._calculate_discount = Mock(return_value=5)   # mocking the unit itself
money = Mock(spec=Money)                             # mocking a value object
```
Correct:
```python
repo = InMemoryOrderRepo()                # injected boundary dependency
service = OrderService(repo=repo, clock=fixed_clock)
```

## Rule 6 — Control time/randomness/IDs via injection
Violation:
```python
@freeze_time("2026-01-01")                # patching module internals
def test_expiry(): ...
```
Correct:
```python
def test_order_expires_after_ttl():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    service = OrderService(repo, now=lambda: now)    # injected clock
    ...
# if the code can't take a clock, flag it: production design defect
```

## Rule 7 — Cover the edges
Violation:
```python
def test_average(): assert average([1, 2, 3]) == 2   # happy path only
```
Correct:
```python
def test_average_of_empty_list_raises_domain_error(): ...
def test_average_of_single_item_is_that_item(): ...
def test_average_handles_negative_values(): ...
```

## Rule 8 — Keep the unit suite fast
Violation:
```python
@pytest.fixture
def app():
    return create_app(real_db_url)        # boots app + real DB per test
```
Correct:
```python
# unit test: no app, no DB — construct the unit with fakes directly
service = OrderService(InMemoryOrderRepo(), now=fixed_now)
# DB-backed variants live in tests/integration/, separate suite
```

## Rule 9 — Tests are production code
Violation:
```python
def test_a():
    o = Order(id=1, cust=7, lines=[...], addr=..., ...)   # 12 lines of setup
def test_b():
    o = Order(id=1, cust=7, lines=[...], addr=..., ...)   # copy-pasted
```
Correct:
```python
def make_order(**overrides) -> Order:      # builder with valid defaults
    return Order(**{**VALID_ORDER, **overrides})
def test_a(): o = make_order()
def test_b(): o = make_order(status=Status.SHIPPED)
```

## Rule 10 — A new test must fail first
Violation:
```python
def test_discount_applied():
    result = apply_discount(order)
    # no assert — always green, proves nothing
```
Correct:
```python
def test_ten_percent_discount_reduces_total():
    assert apply_discount(make_order(total=100)).total == 90
# written before the fix / verified red by reverting the fix once
```

## Rule 11 — No logic in tests
Violation:
```python
def test_statuses():
    for s in statuses:                    # loop
        if s.is_final():                  # branch — test can be wrong
            assert not can_edit(s)
```
Correct:
```python
@pytest.mark.parametrize("status", FINAL_STATUSES)
def test_final_status_blocks_editing(status):
    assert not can_edit(status)
```

## Rule 12 — Parameterize input families
Violation:
```python
def test_email_a(): assert not valid("no-at-sign")
def test_email_b(): assert not valid("@no-local")
def test_email_c(): assert not valid("spaces in@x.com")   # copy-paste family
```
Correct:
```python
@pytest.mark.parametrize("bad", ["no-at-sign", "@no-local", "spaces in@x.com"])
def test_malformed_email_is_rejected(bad):
    assert not valid(bad)                 # each case reports individually
```

## Rule 13 — Every bug fix ships with a regression test
Violation:
```python
# commit: "fix: rounding error on 3-way split"  — no test in the diff
```
Correct:
```python
def test_three_way_split_of_100_loses_no_cents():   # reproduces bug #482
    assert sum(split(Money(100), 3)) == Money(100)
# lands in the same commit as the fix; was red before it
```

## Rule 14 — Minimal, intention-revealing test data
Violation:
```python
order = Order(id=9, customer=Customer("Ann", "ann@x", "CZ", tier="GOLD"),
              lines=[...], shipping=..., billing=..., notes="...")
assert discount(order) == 15              # which of the 14 fields mattered?
```
Correct:
```python
order = make_order(customer_tier="GOLD")  # only the field under test
assert discount(order) == 15
```

## Rule 15 — Assert the contract, not the incidentals
Violation:
```python
with pytest.raises(InsufficientStock) as e:
    service.reserve(cmd)
assert str(e.value) == "Insufficient stock for SKU-1: wanted 5, have 2"  # prose
assert result.tags == ["a", "b", "c"]     # unordered collection, exact order
```
Correct:
```python
with pytest.raises(InsufficientStock) as e:
    service.reserve(cmd)
assert e.value.sku == "SKU-1"             # contract fields
assert e.value.requested == 5
assert set(result.tags) == {"a", "b", "c"}
```

## Rule 16 — Don't test the framework
Violation:
```python
def test_model_saves():
    session.add(order); session.commit()
    assert session.get(Order, order.id)   # tests SQLAlchemy, not your logic
```
Correct:
```python
def test_order_total_sums_line_prices():  # your logic at its seam
    assert make_order(lines=[line(10), line(5)]).total == 15
# persistence round-trips belong to the integration suite, if anywhere
```
