# Eval: Java Testing Verification

## Prompt

Bug report: applying the same coupon twice reduces the order total twice. Fix the bug and add tests that would have caught it. The project uses JUnit 5 and Mockito.

```java
public class Order {
    private BigDecimal total;
    private boolean couponApplied;

    public Order(BigDecimal total) {
        this.total = total;
    }

    public void applyCoupon(String code) {
        if ("SAVE10".equals(code)) {
            total = total.multiply(new BigDecimal("0.90"));
            couponApplied = true;
        }
    }

    public BigDecimal total() {
        return total;
    }
}
```

## Expected Agent Behavior

- Adds regression test reproducing double-discount failure
- Fixes logic with clear idempotency or state guard
- Uses behavior-focused assertions, not implementation details
- Runs targeted test command first
- Summarizes test type chosen and verification command

## Failure Signals

- Fixes code without regression test
- Tests private fields instead of observable `total()`
- Runs entire suite without mentioning narrower command first
- Adds Testcontainers for pure unit logic
