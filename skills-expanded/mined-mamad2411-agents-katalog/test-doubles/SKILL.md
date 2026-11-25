---
name: test-doubles
description: "xUnit test patterns, test doubles, and test smells"
---

# Gerard Meszaros - xUnit Test Patterns

Apply Gerard Meszaros' patterns for writing maintainable, reliable tests.

## Core Philosophy

### Goals of Test Automation

1. **Tests as Documentation** - Tests show how code is meant to be used
2. **Tests as Safety Net** - Catch regressions immediately
3. **Tests as Design Feedback** - Hard-to-test code is poorly designed
4. **Defect Localization** - When a test fails, you know exactly what broke

### The Ideal Test

- **Fully automated** - No manual steps
- **Self-checking** - Pass/fail is obvious
- **Repeatable** - Same result every run
- **Independent** - No test affects another
- **Deterministic** - No flaky tests

---

## Test Doubles

### The Test Double Taxonomy

```
Test Double (generic term)
├── Dummy      - Passed but never used
├── Stub       - Provides canned answers
├── Spy        - Records calls for verification
├── Mock       - Verifies expected interactions
└── Fake       - Working implementation (simplified)
```

### 1. Dummy Object

**Purpose:** Fill required parameters that won't be used.

```java
// The logger is required but not relevant to this test
@Test
void calculateTotal_ignoresLogger() {
    Logger dummyLogger = null;  // Or a no-op logger
    Calculator calc = new Calculator(dummyLogger);

    assertEquals(10, calc.add(4, 6));
}
```

### 2. Test Stub

**Purpose:** Provide predetermined responses.

```java
// Stub returns canned data - no verification
public class StubPriceService implements PriceService {
    @Override
    public double getPrice(String productId) {
        return 99.99;  // Always returns this
    }
}

@Test
void order_calculatesWithPrice() {
    PriceService stubPrices = new StubPriceService();
    Order order = new Order(stubPrices);

    order.addItem("WIDGET", 2);

    assertEquals(199.98, order.getTotal(), 0.01);
}
```

### 3. Test Spy

**Purpose:** Record interactions for later verification.

```java
public class SpyEmailService implements EmailService {
    private final List<String> sentTo = new ArrayList<>();

    @Override
    public void send(String to, String message) {
        sentTo.add(to);  // Record the call
    }

    // Inspection method
    public boolean wasSentTo(String email) {
        return sentTo.contains(email);
    }

    public int getSendCount() {
        return sentTo.size();
    }
}

@Test
void orderConfirmation_sendsEmail() {
    SpyEmailService spy = new SpyEmailService();
    OrderService orders = new OrderService(spy);

    orders.complete(testOrder);

    assertTrue(spy.wasSentTo("customer@test.com"));
    assertEquals(1, spy.getSendCount());
}
```

### 4. Mock Object

**Purpose:** Verify expected behavior (pre-programmed expectations).

```java
// Using Mockito
@Test
void checkout_chargesCard() {
    PaymentGateway mockGateway = mock(PaymentGateway.class);
    when(mockGateway.charge(any(), any())).thenReturn(true);

    Checkout checkout = new Checkout(mockGateway);
    checkout.process(order, card);

    // Verify interaction happened
    verify(mockGateway).charge(card, Money.of(99.99));
}
```

### 5. Fake Object

**Purpose:** Working but simplified implementation.

```java
// Fake in-memory database
public class FakeUserRepository implements UserRepository {
    private final Map<Long, User> users = new HashMap<>();
    private long nextId = 1;

    @Override
    public User save(User user) {
        if (user.getId() == null) {
            user.setId(nextId++);
        }
        users.put(user.getId(), user);
        return user;
    }

    @Override
    public Optional<User> findById(Long id) {
        return Optional.ofNullable(users.get(id));
    }

    @Override
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
}

@Test
void userService_savesAndRetrieves() {
    UserRepository fakeRepo = new FakeUserRepository();
    UserService service = new UserService(fakeRepo);

    User saved = service.createUser("alice@test.com");
    User found = service.findById(saved.getId());

    assertEquals("alice@test.com", found.getEmail());
}
```

### When to Use Which

| Double | Use When | Verify |
|--------|----------|--------|
| Dummy | Parameter needed but irrelevant | Nothing |
| Stub | Need controlled indirect inputs | State only |
| Spy | Need to verify calls happened | After exercise |
| Mock | Behavior verification is primary | During exercise |
| Fake | Need realistic behavior | State only |

---

## Test Patterns

### Four-Phase Test

```java
@Test
void withdraw_reducesBalance() {
    // 1. SETUP (Arrange)
    Account account = new Account();
    account.deposit(100);

    // 2. EXERCISE (Act)
    account.withdraw(30);

    // 3. VERIFY (Assert)
    assertEquals(70, account.getBalance());

    // 4. TEARDOWN (Cleanup) - often implicit
}
```

### Fresh Fixture

Each test creates its own test data.

```java
@Test
void test1() {
    User user = createTestUser();  // Fresh for this test
    // ...
}

@Test
void test2() {
    User user = createTestUser();  // Fresh for this test too
    // ...
}
```

### Shared Fixture (use carefully)

```java
@BeforeEach
void setUp() {
    this.testUser = createTestUser();  // Shared setup
}

@Test
void test1() {
    // Uses testUser
}

@Test
void test2() {
    // Uses same testUser structure, but reset state
}
```

### Minimal Fixture

Only set up what the test actually needs.

```java
// WRONG: Over-specified fixture
@Test
void getName_returnsName() {
    User user = new User();
    user.setId(1L);
    user.setEmail("test@example.com");
    user.setName("Alice");
    user.setAge(30);
    user.setCreatedAt(new Date());
    user.setRole(Role.ADMIN);

    assertEquals("Alice", user.getName());  // Only name matters!
}

// RIGHT: Minimal fixture
@Test
void getName_returnsName() {
    User user = new User();
    user.setName("Alice");

    assertEquals("Alice", user.getName());
}
```

---

## Test Smells

### Fragile Test

**Symptom:** Test breaks when unrelated code changes.

```java
// FRAGILE: Tests internal structure
@Test
void order_hasItems() {
    order.addItem(item);
    assertEquals(1, order.items.size());  // Breaks if items becomes List
}

// ROBUST: Tests behavior
@Test
void order_hasItems() {
    order.addItem(item);
    assertTrue(order.containsItem(item));
}
```

### Obscure Test

**Symptom:** Can't understand what test does without reading deeply.

```java
// OBSCURE
@Test
void test1() {
    X x = new X(1, 2, 3, "a", true, null);
    assertEquals(6, x.calc());
}

// CLEAR
@Test
void calc_sumsPriceQuantityAndTax() {
    Product product = aProduct()
        .withPrice(1)
        .withQuantity(2)
        .withTax(3)
        .build();

    assertEquals(6, product.calculateTotal());
}
```

### Eager Test

**Symptom:** One test verifies too many things.

```java
// EAGER: Testing everything at once
@Test
void userWorkflow() {
    User user = userService.create("alice@test.com");
    assertNotNull(user.getId());
    assertEquals("alice@test.com", user.getEmail());

    user.setName("Alice");
    userService.update(user);
    assertEquals("Alice", userService.findById(user.getId()).getName());

    userService.delete(user.getId());
    assertNull(userService.findById(user.getId()));
}

// FOCUSED: One behavior per test
@Test void create_assignsId() { /* ... */ }
@Test void create_setsEmail() { /* ... */ }
@Test void update_changesName() { /* ... */ }
@Test void delete_removesUser() { /* ... */ }
```

### Mystery Guest

**Symptom:** Test depends on external data not visible in test.

```java
// MYSTERY: Where does "user-123" come from?
@Test
void findUser_returnsUser() {
    User user = userService.findById("user-123");
    assertEquals("Alice", user.getName());
}

// EXPLICIT: Test data is visible
@Test
void findUser_returnsUser() {
    User alice = userService.create("Alice");

    User found = userService.findById(alice.getId());

    assertEquals("Alice", found.getName());
}
```

### Test Logic in Production

**Symptom:** Production code has `if (testing)` checks.

```java
// WRONG: Test mode in production
public class PaymentService {
    public void charge(Card card, Money amount) {
        if (System.getProperty("test.mode") != null) {
            return;  // Skip in tests
        }
        gateway.charge(card, amount);
    }
}

// RIGHT: Inject the dependency
public class PaymentService {
    private final PaymentGateway gateway;

    public PaymentService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public void charge(Card card, Money amount) {
        gateway.charge(card, amount);
    }
}
// In tests: new PaymentService(fakeGateway)
```

---

## Assertion Patterns

### State Verification

```java
// Verify the resulting state
@Test
void deposit_increasesBalance() {
    account.deposit(50);

    assertEquals(150, account.getBalance());  // Check state
}
```

### Behavior Verification

```java
// Verify interactions occurred
@Test
void transfer_callsBothAccounts() {
    Account from = mock(Account.class);
    Account to = mock(Account.class);

    transferService.transfer(from, to, 50);

    verify(from).withdraw(50);  // Check behavior
    verify(to).deposit(50);
}
```

### Delta Assertion

```java
// Verify the change, not absolute value
@Test
void deposit_increasesBalanceByAmount() {
    int before = account.getBalance();

    account.deposit(50);

    assertEquals(before + 50, account.getBalance());  // Delta
}
```

### Custom Assertion

```java
// Encapsulate complex assertions
public static void assertValidOrder(Order order) {
    assertNotNull(order.getId(), "Order must have ID");
    assertFalse(order.getItems().isEmpty(), "Order must have items");
    assertTrue(order.getTotal() > 0, "Order total must be positive");
}

@Test
void createOrder_returnsValidOrder() {
    Order order = orderService.create(items);

    assertValidOrder(order);
}
```

---

## Code Review Checklist

### Test Structure
- [ ] Four-phase pattern clear (setup/exercise/verify/teardown)?
- [ ] Minimal fixture - only what's needed?
- [ ] One logical assertion per test?

### Test Doubles
- [ ] Using appropriate double type?
- [ ] Fakes over mocks for complex interactions?
- [ ] Stubs for indirect inputs?
- [ ] Spies only when verification needed?

### Test Smells
- [ ] No fragile tests (testing behavior, not structure)?
- [ ] No obscure tests (clear naming, visible data)?
- [ ] No eager tests (one behavior per test)?
- [ ] No mystery guests (all data visible)?

### Independence
- [ ] Tests can run in any order?
- [ ] No shared mutable state?
- [ ] Each test sets up its own data?

---

## Quick Reference

| Smell | Solution |
|-------|----------|
| Fragile test | Test behavior, not structure |
| Obscure test | Better names, test builders |
| Eager test | Split into focused tests |
| Mystery guest | Inline test data |
| Slow test | Use fakes instead of real deps |
| Erratic test | Remove shared state |

---

## Resources

- [xUnit Test Patterns](http://xunitpatterns.com/) (2007)
- [xUnit Test Patterns Book](https://www.amazon.com/xUnit-Test-Patterns-Refactoring-Code/dp/0131495054)
- [Test Double Patterns](http://xunitpatterns.com/Test%20Double%20Patterns.html)
