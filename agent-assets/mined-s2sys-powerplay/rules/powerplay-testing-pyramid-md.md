---
name: testing-pyramid
description: Testing pyramid — 70% unit, 20% integration, 10% e2e; proper mocking strategy
globs: ["**/*Tests.cs", "**/*.spec.ts", "**/*.test.ts"]
alwaysApply: false
---

# Testing Pyramid

Follow the testing pyramid: many unit tests, some integration tests, few e2e tests. Mock at the boundary, not inside. All tests follow AAA pattern.

## Testing Pyramid Ratios

**ALWAYS**:
- 70% unit tests (fast, focused, isolated from dependencies)
- 20% integration tests (realistic, test multiple components)
- 10% e2e/acceptance tests (slow, test full workflows)

**WHY**: Unit tests are fast (milliseconds), integration tests are slower (seconds), e2e tests are slowest (minutes). Optimize for speed in the bulk of your suite.

**NEVER**:
- 80% e2e tests (too slow, fragile, maintenance burden)
- 10% unit tests (miss bugs, false confidence)
- Mock internal business logic (defeats the purpose of testing)

---

## Unit Testing

**ALWAYS**:
- Test a single method or small behavior
- Mock all external dependencies (database, HTTP, file system, cache)
- AAA pattern (Arrange/Act/Assert)
- Test names describe scenario and expected result
- All assertions in one test (don't split across tests)

**NEVER**:
- Test multiple scenarios in one test (use `[Theory]` / `@parametrize`)
- Leave setup code untested (test setup in unit tests too)
- Test implementation, test behavior
- Mock internal dependencies (only mock across boundaries)

### ✅ GOOD Example
```csharp
// xUnit + Moq + FluentAssertions
public class UserServiceTests
{
  [Fact]
  public async Task GetUserAsync_WithValidId_ReturnsUserWithCorrectData()
  {
    // Arrange
    var userId = 123;
    var mockRepository = new Mock<IUserRepository>();
    mockRepository
      .Setup(r => r.GetUserAsync(userId, It.IsAny<CancellationToken>()))
      .ReturnsAsync(new User { Id = userId, Name = "Alice", Email = "alice@example.com" });
    
    var service = new UserService(mockRepository.Object);
    
    // Act
    var result = await service.GetUserAsync(userId, CancellationToken.None);
    
    // Assert
    result.Should().NotBeNull();
    result.Id.Should().Be(userId);
    result.Name.Should().Be("Alice");
  }
  
  [Fact]
  public async Task GetUserAsync_WithInvalidId_ThrowsUserNotFoundException()
  {
    // Arrange
    var userId = -1;
    var mockRepository = new Mock<IUserRepository>();
    mockRepository
      .Setup(r => r.GetUserAsync(userId, It.IsAny<CancellationToken>()))
      .ThrowsAsync(new UserNotFoundException(userId));
    
    var service = new UserService(mockRepository.Object);
    
    // Act & Assert
    await service.Invoking(s => s.GetUserAsync(userId, CancellationToken.None))
      .Should()
      .ThrowAsync<UserNotFoundException>();
  }
}
```

### ❌ BAD Example
```csharp
// Testing implementation, multiple scenarios, no AAA
public class UserServiceTests
{
  [Fact]
  public void TestGetUser()
  {
    var service = new UserService();
    var user = service.GetUser(123);
    Assert.NotNull(user);
    Assert.Equal(123, user.Id);
    // More assertions mixed together
  }
  
  // No mocking - tests external system directly
  // No clear scenario description
}
```

---

## Integration Testing

**ALWAYS**:
- Test multiple components working together
- Use real database (or test container)
- Mock external services (HTTP APIs)
- Test realistic workflows
- Still use AAA pattern

**NEVER**:
- Mock the database (defeats the purpose)
- Test the same scenario as unit tests
- Forget to clean up test data (leave database dirty)
- Make integration tests too slow (should still be < 5 seconds each)

### ✅ GOOD Example
```csharp
public class UserServiceIntegrationTests : IAsyncLifetime
{
  private SqliteConnection _connection;
  private UserRepository _repository;
  private UserService _service;
  
  public async Task InitializeAsync()
  {
    _connection = new SqliteConnection("DataSource=:memory:");
    await _connection.OpenAsync();
    // Create schema
    await _connection.ExecuteAsync("CREATE TABLE Users (Id INT, Name TEXT)");
    _repository = new UserRepository(_connection);
    _service = new UserService(_repository);
  }
  
  public async Task DisposeAsync()
  {
    await _connection.CloseAsync();
    _connection.Dispose();
  }
  
  [Fact]
  public async Task CreateAndRetrieveUser_RoundTrip_SuccessfullyPersists()
  {
    // Arrange
    var newUser = new User { Name = "Bob", Email = "bob@example.com" };
    
    // Act
    await _service.CreateUserAsync(newUser);
    var retrieved = await _service.GetUserAsync(newUser.Id);
    
    // Assert
    retrieved.Should().NotBeNull();
    retrieved.Name.Should().Be("Bob");
  }
}
```

---

## E2E / Acceptance Testing

**ONLY**:
- Test full user workflows (login → create → delete)
- Use real browser (Selenium, Playwright)
- Mock external services (payments, emails)
- For critical paths only (not every scenario)
- Expect these to be slow (10+ seconds each)

**NEVER**:
- Write e2e tests for every unit test scenario
- Leave e2e tests flaky (they should be reliable)
- Test UI minutiae (button exact color) — test behavior

### ✅ GOOD Example
```typescript
// Playwright e2e test
test('User can register and login', async ({ page }) => {
  // Arrange
  page.goto('https://app.example.com');
  
  // Act — Registration flow
  await page.click('button:has-text("Sign Up")');
  await page.fill('input[type="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'Password123!');
  await page.click('button:has-text("Create Account")');
  
  // Assert — Registration succeeded
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.locator('text=Welcome')).toBeVisible();
  
  // Act — Logout
  await page.click('button:has-text("Logout")');
  
  // Act — Login again
  await page.click('button:has-text("Sign In")');
  await page.fill('input[type="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'Password123!');
  await page.click('button:has-text("Login")');
  
  // Assert — Login succeeded
  await expect(page).toHaveURL(/\/dashboard/);
});
```

---

## Mocking Strategy

**Mock at the Boundary** (between your code and external systems):
- ✅ Database queries (mock repository)
- ✅ HTTP calls (mock HTTP client)
- ✅ File system (mock file service)
- ✅ Email/SMS (mock notification service)
- ❌ Business logic (don't mock)

### ✅ GOOD Mocking
```csharp
// Mock crosses boundary (database layer)
var mockRepository = new Mock<IUserRepository>();
mockRepository.Setup(r => r.GetUserAsync(id, It.IsAny<CancellationToken>()))
  .ReturnsAsync(user);

var service = new UserService(mockRepository.Object);
// Test business logic, not repository implementation
```

### ❌ BAD Mocking
```csharp
// Mocking internal business logic — defeats the test
var mockValidator = new Mock<IUserValidator>();
mockValidator.Setup(v => v.IsValidEmail(It.IsAny<string>())).Returns(true);

// Now we're not testing email validation at all!
```

---

## AAA Pattern (Always)

**Arrange**: Set up test data and mocks  
**Act**: Execute the method being tested  
**Assert**: Verify the result

```csharp
[Fact]
public void Example_WithScenario_ExpectsBehavior()
{
  // Arrange
  var input = SetupTestData();
  var mock = CreateMocks();
  var sut = new SystemUnderTest(mock);
  
  // Act
  var result = sut.MethodToTest(input);
  
  // Assert
  result.Should().Be(expected);
}
```

---

## Test Naming Convention

Pattern: `MethodName_Scenario_ExpectedResult`

### ✅ GOOD Names
- `GetUser_WithValidId_ReturnsUser`
- `ValidateEmail_WithInvalidEmail_ThrowsException`
- `CreateOrder_WhenStockEmpty_RejectsOrder`
- `ProcessPayment_WithExpiredCard_ReturnsDeclined`

### ❌ BAD Names
- `TestGetUser`
- `Test1`
- `ValidateEmailTest`
- `Process`

---

## Testing Checklist

- [ ] 70% unit tests (fast, focused)
- [ ] 20% integration tests (realistic)
- [ ] 10% e2e tests (critical paths)
- [ ] AAA pattern in all tests
- [ ] Descriptive test names
- [ ] Mock at boundary only
- [ ] Test cleanup in place
- [ ] All assertions in one test (don't spread across)
- [ ] No testing framework details in test names
- [ ] Happy path + edge cases + error cases
