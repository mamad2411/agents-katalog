---
name: integration-testing
description: Integration testing — Contract testing, E2E strategies, test environments, test data, CI/CD validation
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Integration Testing Standards

Integration tests validate that multiple components work together correctly. Use contract testing for APIs, E2E tests for workflows, and test data management for repeatable tests.

---

## Integration Testing Pyramid

```
        ┌─────────────────┐
        │   E2E Tests     │  5-10% (UI, browser, full workflow)
        ├─────────────────┤
        │  Integration    │  20-30% (APIs, databases, services)
        │    Tests        │
        ├─────────────────┤
        │  Unit Tests     │  70-80% (individual functions, fast)
        └─────────────────┘
```

**ALWAYS**:
- Unit tests: ~70% coverage (fast, isolated)
- Integration tests: ~20% coverage (APIs, DBs, services)
- E2E tests: ~10% coverage (workflows, critical paths)
- Integration tests use real/test databases (not mocks)
- Contract testing for API boundaries
- Test data in version control (seed scripts)

**NEVER**:
- Mock database in integration tests (defeats purpose)
- Skip integration tests (critical for real-world scenarios)
- Ignore flaky tests (fix root cause)

---

## Contract Testing (API Contracts)

**ALWAYS**:
- Define API contracts (request/response schemas)
- Test provider (API) implements contract
- Test consumer (client) respects contract
- Share contracts via OpenAPI or JSON Schema
- Catch breaking changes before deployment

**NEVER**:
- Change API without updating contract
- Ignore consumer contract expectations
- Deploy breaking changes (catch in contract test)

### ✅ GOOD Contract Testing

```csharp
// Provider Test (API - SmartWorkz)
[TestFixture]
public class OrderApiContractTests
{
    private HttpClient _httpClient;
    
    [OneTimeSetUp]
    public void Setup()
    {
        // Start test API
        var factory = new WebApplicationFactory<Startup>();
        _httpClient = factory.CreateClient();
    }
    
    [Test]
    public async Task CreateOrder_ReturnsValidContract()
    {
        // Act
        var response = await _httpClient.PostAsJsonAsync(
            "/api/v1/orders",
            new CreateOrderRequest { CustomerId = Guid.NewGuid(), Amount = 100 }
        );
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        
        var content = await response.Content.ReadAsAsync<CreateOrderResponse>();
        
        // Verify contract (schema validation)
        content.Should().NotBeNull();
        content.OrderId.Should().NotBeEmpty();
        content.Status.Should().Be("Created");
        content.CreatedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }
}

// Consumer Test (Client using API)
[TestFixture]
public class OrderClientContractTests
{
    private OrderApiClient _client;
    
    [OneTimeSetUp]
    public void Setup()
    {
        _client = new OrderApiClient("https://api.smartworkz.local");
    }
    
    [Test]
    public async Task CreateOrder_ParsesResponseCorrectly()
    {
        // Act
        var response = await _client.CreateOrderAsync(
            new CreateOrderRequest { CustomerId = Guid.NewGuid(), Amount = 100 }
        );
        
        // Assert (verify consumer can handle response)
        response.Should().NotBeNull();
        response.OrderId.Should().NotBeEmpty();
        response.Status.Should().Be("Created");  // Must match provider
        response.CreatedAt.Should().BeOfType<DateTime>();
    }
}
```

---

## End-to-End (E2E) Testing

**ALWAYS**:
- Test complete workflows (create order → pay → ship)
- Use real/staging environment
- Test UI interactions (browser automation)
- Test critical paths only (not all scenarios)
- Use test data (separate from production)
- Clean up after test (teardown)

**NEVER**:
- Run E2E tests on production (staging only)
- Use production data in tests (create test data)
- Test everything (too slow, focus on critical)

### ✅ GOOD E2E Testing (Playwright)

```csharp
[TestFixture]
public class OrderWorkflowE2ETests
{
    private IBrowser _browser;
    private IPage _page;
    
    [OneTimeSetUp]
    public async Task SetupAsync()
    {
        var playwright = await Playwright.CreateAsync();
        _browser = await playwright.Chromium.LaunchAsync();
    }
    
    [SetUp]
    public async Task SetupPageAsync()
    {
        _page = await _browser.NewPageAsync();
    }
    
    [TearDown]
    public async Task CleanupPageAsync()
    {
        await _page.CloseAsync();
    }
    
    [Test]
    public async Task CompleteOrderWorkflow_OrderCreatedAndPaid()
    {
        // Navigate to order form
        await _page.GotoAsync("https://staging.smartworkz.local/orders/new");
        
        // Fill form
        await _page.FillAsync("input[name='customerId']", Guid.NewGuid().ToString());
        await _page.FillAsync("input[name='amount']", "100");
        
        // Submit
        await _page.ClickAsync("button[type='submit']");
        
        // Wait for order created (polling)
        await _page.WaitForSelectorAsync("text=Order Created", new() { Timeout = 5000 });
        
        // Verify order details displayed
        var orderId = await _page.TextContentAsync(".order-id");
        orderId.Should().NotBeNullOrEmpty();
        
        // Navigate to payment
        await _page.ClickAsync("button:has-text('Pay Now')");
        
        // Fill payment
        await _page.FillAsync("input[name='cardNumber']", "4111111111111111");
        await _page.FillAsync("input[name='expiry']", "12/25");
        await _page.FillAsync("input[name='cvv']", "123");
        
        // Submit payment
        await _page.ClickAsync("button[type='submit']");
        
        // Wait for payment success
        await _page.WaitForSelectorAsync("text=Payment Successful", new() { Timeout = 5000 });
        
        // Verify order status changed to Paid
        var status = await _page.TextContentAsync(".order-status");
        status.Should().Contain("Paid");
    }
}
```

---

## Test Data Management

**ALWAYS**:
- Use seed scripts (create test data consistently)
- Store test data in version control
- Use factories for test object creation
- Clean up after tests (isolation)
- Use separate test database
- Use unique identifiers (GUIDs) to avoid conflicts

**NEVER**:
- Use production data in tests
- Hardcode test data (use factories)
- Leave test data after test (cleanup)

### ✅ GOOD Test Data Setup

```csharp
// Test data factory
public class TestOrderFactory
{
    public static Order CreateOrder(
        Guid? customerId = null,
        decimal? amount = null,
        OrderStatus? status = null)
    {
        return new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId ?? Guid.NewGuid(),
            Amount = amount ?? 100m,
            Status = status ?? OrderStatus.Created,
            CreatedAt = DateTime.UtcNow
        };
    }
}

// Test data seed
[SetUp]
public async Task SeedTestDataAsync()
{
    // Create test customers
    _testCustomer1 = new Customer
    {
        Id = Guid.NewGuid(),
        Name = "Test Customer 1",
        Email = "test1@example.com"
    };
    
    _testCustomer2 = new Customer
    {
        Id = Guid.NewGuid(),
        Name = "Test Customer 2",
        Email = "test2@example.com"
    };
    
    await _db.Customers.AddRangeAsync(_testCustomer1, _testCustomer2);
    
    // Create test orders
    var order1 = TestOrderFactory.CreateOrder(
        customerId: _testCustomer1.Id,
        amount: 100m,
        status: OrderStatus.Created
    );
    var order2 = TestOrderFactory.CreateOrder(
        customerId: _testCustomer2.Id,
        amount: 200m,
        status: OrderStatus.Paid
    );
    
    await _db.Orders.AddRangeAsync(order1, order2);
    await _db.SaveChangesAsync();
}

[TearDown]
public async Task CleanupAsync()
{
    // Delete all test data
    _db.Orders.RemoveRange(_db.Orders.ToList());
    _db.Customers.RemoveRange(_db.Customers.ToList());
    await _db.SaveChangesAsync();
}

[Test]
public async Task GetCustomerOrders_ReturnsAllOrders()
{
    // Use seeded data
    var orders = await _orderService.GetCustomerOrdersAsync(_testCustomer1.Id);
    
    orders.Should().HaveCount(1);
    orders.First().Amount.Should().Be(100m);
}
```

---

## CI/CD Integration Testing

**ALWAYS**:
- Run integration tests on every commit
- Use test containers (Docker for databases)
- Parallel test execution (faster feedback)
- Report coverage & results
- Fail build on test failure
- Keep tests fast (< 5 minutes for integration suite)

**NEVER**:
- Skip integration tests (commit to main)
- Ignore test failures (fix before merging)
- Run E2E tests on every commit (too slow)

### ✅ GOOD CI/CD Integration Testing

```yaml
# GitHub Actions - Integration Testing
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '7.0.x'
      
      - name: Run integration tests
        run: |
          dotnet test --filter "Category=Integration" \
            --logger "trx;LogFileName=integration-results.trx" \
            --collect:"XPlat Code Coverage"
        env:
          ConnectionStrings__DefaultConnection: "Host=localhost;Database=test;Username=postgres;Password=postgres"
          Redis__Connection: "localhost:6379"
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.cobertura.xml
          flags: integration
          fail_ci_if_error: false
      
      - name: Publish test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: integration-test-results
          path: integration-results.trx
```

---

## Integration Testing Checklist

- [ ] Contract tests for APIs (provider & consumer)
- [ ] E2E tests for critical workflows
- [ ] Test data factories & seeds (version controlled)
- [ ] Test database separate from production
- [ ] Cleanup after tests (no data leakage)
- [ ] Integration tests run on every commit (CI/CD)
- [ ] Coverage reports generated
- [ ] Parallel test execution configured
- [ ] Test containers for services (Docker)
- [ ] Flaky tests identified & fixed
- [ ] Documentation (test scenarios, setup)

---

## Summary

Good integration testing:
1. **Contract testing** — APIs honor contracts
2. **E2E testing** — Critical workflows end-to-end
3. **Test data** — Factories, seeds, isolation
4. **CI/CD** — Every commit tested, parallel execution
5. **Coverage** — Measure & track
6. **Reliability** — No flaky tests, repeatable results
7. **Performance** — Keep integration tests fast

Integration tests catch real-world failures that unit tests miss.
