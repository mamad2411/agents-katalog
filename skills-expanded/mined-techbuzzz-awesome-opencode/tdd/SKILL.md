---
name: tdd
description: >
  Use when implementing any new feature or bugfix using Test-Driven Development.
  Guides the Red-Green-Refactor cycle: write failing test first, minimal implementation,
  then refactor. Works with any language (C#, Go, TypeScript, C++).
license: MIT
compatibility: opencode
---

# Test-Driven Development Skill

## When to Use

Activate this skill when the user:
- Asks to implement a feature using TDD
- Wants to write tests before implementation
- Is fixing a bug (write test to reproduce first)
- Wants to practice Red-Green-Refactor

## TDD Cycle

### 1. 🔴 RED — Write a Failing Test
```
"Write the simplest test that describes the desired behavior.
Run it. Confirm it fails for the RIGHT reason."
```

Ask the user:
- What is the input?
- What is the expected output?
- What are the edge cases?

### 2. 🟢 GREEN — Write Minimal Code
```
"Write the MINIMUM code to make the test pass.
Don't over-engineer. Don't optimize. Just make it green."
```

### 3. 🔵 REFACTOR — Clean Up
```
"With tests passing, improve the code:
- Extract duplication
- Rename for clarity  
- Simplify logic
- Tests must remain green throughout"
```

## Language-Specific Templates

### C# / xUnit
```csharp
// 1. RED: Write test first
[Fact]
public async Task CreateOrder_WithValidItems_ReturnsOrderWithTotal()
{
    // Arrange
    var sut = new OrderService(new FakeRepository());
    var items = new[] { new OrderItem("Widget", 2, 9.99m) };
    
    // Act
    var order = await sut.CreateOrderAsync(items);
    
    // Assert
    order.Total.Should().Be(19.98m);
    order.Status.Should().Be(OrderStatus.Pending);
}

// 2. GREEN: Minimal implementation
public async Task<Order> CreateOrderAsync(OrderItem[] items)
{
    var total = items.Sum(i => i.Price * i.Quantity);
    var order = new Order(items, total, OrderStatus.Pending);
    await _repository.SaveAsync(order);
    return order;
}
```

### Go / testing
```go
// 1. RED
func TestCreateOrder_WithValidItems_ReturnsTotal(t *testing.T) {
    svc := NewOrderService(NewFakeRepo())
    items := []OrderItem{{Name: "Widget", Qty: 2, Price: 9.99}}
    
    order, err := svc.CreateOrder(context.Background(), items)
    
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if got, want := order.Total, 19.98; math.Abs(got-want) > 0.001 {
        t.Errorf("Total = %v, want %v", got, want)
    }
}
```

### TypeScript / Vitest
```typescript
// 1. RED
describe('OrderService', () => {
  it('calculates total from items', async () => {
    const svc = new OrderService(new FakeRepository());
    const order = await svc.createOrder([
      { name: 'Widget', qty: 2, price: 9.99 }
    ]);
    
    expect(order.total).toBeCloseTo(19.98);
    expect(order.status).toBe('pending');
  });
});
```

## TDD Principles

1. **One failing test at a time** — don't write multiple failing tests
2. **Test behavior, not implementation** — test the "what", not the "how"
3. **Tests are documentation** — they should read like specifications
4. **Fake it till you make it** — start with hardcoded returns if needed
5. **Triangulate** — add more test cases to force generalization

## Checklist

After each TDD cycle:
- [ ] Test name clearly describes behavior (Given/When/Then or MethodName_Scenario_Expected)
- [ ] Test fails before implementation (RED confirmed)
- [ ] Minimal code to pass (no more than needed)
- [ ] All previous tests still pass
- [ ] Code is refactored and clean
- [ ] Next failing test identified
