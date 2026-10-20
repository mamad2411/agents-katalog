# Unit Test Rules — Java Examples

**Framework basis:** Java 17+, JUnit 5 (Jupiter) 5.9+, Mockito 5.x,
AssertJ 3.x. The rules themselves are framework-agnostic — these examples
only show one concrete stack.
**Translation hints:** JUnit 4 → `@Test(expected=...)` and rules instead of
`assertThrows`/extensions, no native parameterized-per-method support;
TestNG → `@DataProvider` ≈ `@ParameterizedTest`; Kotlin → same stack plus
kotest/mockk equivalents.
**Version-sensitive:** JUnit 5 uses `org.junit.jupiter.*` — JUnit 4 uses
`org.junit.*` and different annotations (`@BeforeEach` vs `@Before`).
Mockito 5.x requires Java 11+; static mocking needs mockito-inline behavior
(default in 5.x, separate artifact in 4.x).

## Rule 1 — Test behavior, not implementation
Violation:
```java
@Test void placeOrder() {
    service.placeOrder(cmd);
    verify(service, times(1)).validate(cmd);        // internal call sequence
    InOrder io = inOrder(repo, stock); ...          // choreography, not behavior
}
```
Correct:
```java
@Test void placedOrderIsPersistedWithPendingStatus() {
    Order order = service.placeOrder(cmd);
    assertThat(repo.get(order.id()).status()).isEqualTo(Status.PENDING);
}
```

## Rule 2 — One logical assertion per test
Violation:
```java
@Test void couponLogic() {                // first failure hides the rest
    assertThat(apply(expired).rejected()).isTrue();
    assertThat(apply(valid).discount()).isEqualTo(10);
    assertThat(apply(used).rejected()).isTrue();
}
```
Correct:
```java
@Test void expiredCouponIsRejected() { ... }
@Test void validCouponAppliesItsDiscount() { ... }
@Test void alreadyUsedCouponIsRejected() { ... }
```

## Rule 3 — Arrange-Act-Assert
Violation:
```java
@Test void cart() {
    var cart = new Cart();
    cart.add(itemA);                              // act
    assertThat(cart.total()).isEqualTo(10);       // assert
    cart.add(itemB);                              // act again — hidden test
    assertThat(cart.total()).isEqualTo(25);
}
```
Correct:
```java
@Test void addingOneItemSetsTotalToItsPrice() {
    var cart = new Cart();                        // arrange
    cart.add(itemA);                              // act
    assertThat(cart.total()).isEqualTo(10);       // assert
}
@Test void addingSecondItemAccumulatesTotal() { ... }
```

## Rule 4 — Deterministic and isolated
Violation:
```java
@Test void fetchRates() throws Exception {
    var rates = client.fetch(URI.create("https://api.fx.example")); // network
    Thread.sleep(2000);                                             // timing hope
    assertThat(rates.get("EUR")).isPositive();
}
```
Correct:
```java
@Test void conversionUsesFetchedRate() {
    FxClient client = sku -> Map.of("EUR", 1.1);   // stub at the port
    assertThat(new Converter(client).convert(100, "EUR")).isEqualTo(110);
}
```

## Rule 5 — Fake the ports, not the internals
Violation:
```java
OrderService spy = spy(service);                   // mocking the unit itself
doReturn(5).when(spy).calculateDiscount(any());
Money money = mock(Money.class);                   // mocking a value object
```
Correct:
```java
OrderRepositoryPort repo = new InMemoryOrderRepo();  // boundary fake
var service = new OrderService(repo, Clock.fixed(T0, UTC));
```

## Rule 6 — Control time/randomness/IDs via injection
Violation:
```java
try (var mocked = mockStatic(Instant.class)) {     // static time mocking
    mocked.when(Instant::now).thenReturn(T0);
}
```
Correct:
```java
var service = new OrderService(repo, Clock.fixed(T0, UTC));  // injected clock
// if the code can't take a Clock, flag it: production design defect
```

## Rule 7 — Cover the edges
Violation:
```java
@Test void average() { assertThat(average(List.of(1, 2, 3))).isEqualTo(2); }
```
Correct:
```java
@Test void averageOfEmptyListThrowsDomainError() { ... }
@Test void averageOfSingleItemIsThatItem() { ... }
@Test void averageHandlesNegativeValues() { ... }
```

## Rule 8 — Keep the unit suite fast
Violation:
```java
@SpringBootTest                            // boots the container per class
class OrderServiceTest { @Autowired OrderService service; ... }
```
Correct:
```java
class OrderServiceTest {                   // plain JUnit, no context
    OrderService service =
        new OrderService(new InMemoryOrderRepo(), Clock.fixed(T0, UTC));
}
// @SpringBootTest variants live in the integration suite
```

## Rule 9 — Tests are production code
Violation:
```java
@Test void a() { var o = new Order(1L, 7L, lines, addr, ...); }  // 12-arg setup
@Test void b() { var o = new Order(1L, 7L, lines, addr, ...); }  // copy-pasted
```
Correct:
```java
static OrderBuilder anOrder() { return Order.builder().withValidDefaults(); }
@Test void a() { var o = anOrder().build(); }
@Test void b() { var o = anOrder().status(SHIPPED).build(); }
```

## Rule 10 — A new test must fail first
Violation:
```java
@Test void discountApplied() {
    applyDiscount(order);                  // no assertion — always green
}
```
Correct:
```java
@Test void tenPercentDiscountReducesTotal() {
    assertThat(applyDiscount(anOrder().total(100).build()).total())
        .isEqualTo(90);                    // verified red before the fix
}
```

## Rule 11 — No logic in tests
Violation:
```java
@Test void statuses() {
    for (Status s : statuses) {            // loop
        if (s.isFinal()) {                 // branch — test can be wrong
            assertThat(canEdit(s)).isFalse();
        }
    }
}
```
Correct:
```java
@ParameterizedTest
@EnumSource(value = Status.class, names = {"SHIPPED", "CANCELLED"})
void finalStatusBlocksEditing(Status status) {
    assertThat(canEdit(status)).isFalse();
}
```

## Rule 12 — Parameterize input families
Violation:
```java
@Test void emailA() { assertThat(valid("no-at-sign")).isFalse(); }
@Test void emailB() { assertThat(valid("@no-local")).isFalse(); }
@Test void emailC() { assertThat(valid("spaces in@x.com")).isFalse(); }
```
Correct:
```java
@ParameterizedTest
@ValueSource(strings = {"no-at-sign", "@no-local", "spaces in@x.com"})
void malformedEmailIsRejected(String bad) {
    assertThat(valid(bad)).isFalse();      // each case reports individually
}
```

## Rule 13 — Every bug fix ships with a regression test
Violation:
```java
// commit: "fix: rounding error on 3-way split" — no test in the diff
```
Correct:
```java
@Test void threeWaySplitOfHundredLosesNoCents() {   // reproduces bug #482
    assertThat(sum(split(Money.of(100), 3))).isEqualTo(Money.of(100));
}   // lands in the same commit as the fix; was red before it
```

## Rule 14 — Minimal, intention-revealing test data
Violation:
```java
var order = new Order(9L, new Customer("Ann", "ann@x", "CZ", Tier.GOLD),
                      lines, shipping, billing, "notes...");
assertThat(discount(order)).isEqualTo(15);  // which field mattered?
```
Correct:
```java
var order = anOrder().customerTier(Tier.GOLD).build();  // only what matters
assertThat(discount(order)).isEqualTo(15);
```

## Rule 15 — Assert the contract, not the incidentals
Violation:
```java
var e = assertThrows(InsufficientStockException.class, () -> service.reserve(cmd));
assertThat(e.getMessage())
    .isEqualTo("Insufficient stock for SKU-1: wanted 5, have 2");   // prose
assertThat(result.tags()).containsExactly("a", "b", "c");  // unordered set
```
Correct:
```java
var e = assertThrows(InsufficientStockException.class, () -> service.reserve(cmd));
assertThat(e.sku()).isEqualTo("SKU-1");            // contract fields
assertThat(e.requested()).isEqualTo(5);
assertThat(result.tags()).containsExactlyInAnyOrder("a", "b", "c");
```

## Rule 16 — Don't test the framework
Violation:
```java
@Test void entitySaves() {
    em.persist(order); em.flush();
    assertThat(em.find(Order.class, order.id())).isNotNull();  // tests JPA
}
```
Correct:
```java
@Test void orderTotalSumsLinePrices() {    // your logic at its seam
    assertThat(anOrder().lines(line(10), line(5)).build().total())
        .isEqualTo(15);
}   // persistence round-trips belong to the integration suite, if anywhere
```
