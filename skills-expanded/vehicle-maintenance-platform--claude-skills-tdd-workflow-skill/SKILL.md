---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code in Verendar. Enforces test-driven development with 80%+ coverage using xUnit, FluentAssertions, NSubstitute, and Testcontainers. Activate proactively whenever the user is about to write new application code, fix a bug, or add an endpoint — tests must come first.
---

# TDD Workflow — .NET / Verendar

## The Cycle

**RED → GREEN → REFACTOR** — always in that order. Never write implementation before a failing test exists.

---

## Step 1: Define the Behaviour (User Story)

```
As a [role], I want to [action], so that [benefit].

Example:
As a user, I want to cancel a booking,
so that I can get a refund if my plans change.
```

---

## Step 2: Write Failing Tests (RED)

```csharp
// Verendar.Garage.Tests/Services/BookingServiceTests.cs
[Fact]
public async Task CancelAsync_PendingBooking_PublishesCancelledEvent()
{
    // Arrange
    var booking = BookingFaker.Pending();
    _bookingRepo.FindByIdAsync(booking.Id).Returns(booking);

    // Act
    var result = await _sut.CancelAsync(booking.Id, booking.UserId, CancellationToken.None);

    // Assert
    result.IsSuccess.Should().BeTrue();
    await _publishEndpoint.Received(1)
        .Publish(Arg.Any<BookingCancelledEvent>(), Arg.Any<CancellationToken>());
}

[Fact]
public async Task CancelAsync_AlreadyCancelled_ReturnsFailure()
{
    var booking = BookingFaker.Cancelled();
    _bookingRepo.FindByIdAsync(booking.Id).Returns(booking);

    var result = await _sut.CancelAsync(booking.Id, booking.UserId, CancellationToken.None);

    result.IsSuccess.Should().BeFalse();
}
```

Run: `task test PROJECT=Garage/Verendar.Garage.Tests` → tests must **fail**.

---

## Step 3: Implement Minimally (GREEN)

Write the least code needed to make the tests pass. No extras.

---

## Step 4: Refactor

Clean up while keeping all tests green. Only after GREEN.

---

## Step 5: Verify Coverage

```bash
task test:all
dotnet test --collect:"XPlat Code Coverage"
```

Minimum 80% overall. 100% for payment and auth logic.

---

## Test Types

| Type        | Tool                                   | Purpose                                     |
| ----------- | -------------------------------------- | ------------------------------------------- |
| Unit        | xUnit + FluentAssertions + NSubstitute | Service logic, domain rules, pure functions |
| Integration | WebApplicationFactory + Testcontainers | API endpoints against real PostgreSQL       |
| Consumer    | MassTransit TestHarness                | Event consumers in isolation                |

---

## Unit Test Setup

```csharp
public class BookingServiceTests
{
    private readonly IUnitOfWork _uow = Substitute.For<IUnitOfWork>();
    private readonly IPublishEndpoint _pub = Substitute.For<IPublishEndpoint>();
    private readonly BookingService _sut;

    public BookingServiceTests()
    {
        _uow.Bookings.Returns(Substitute.For<IBookingRepository>());
        _sut = new BookingService(_uow, _pub, NullLogger<BookingService>.Instance);
    }
}
```

---

## Integration Test Setup

```csharp
public class BookingApiTests(GarageWebFactory factory) : IClassFixture<GarageWebFactory>
{
    private readonly HttpClient _client = factory.CreateClient();

    [Fact]
    public async Task POST_Cancel_Returns200()
    {
        _client.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", factory.GenerateUserToken(Guid.NewGuid()));

        var response = await _client.PostAsync($"/api/bookings/{bookingId}/cancel", null);

        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
```

See [`references/dotnet-patterns.md`](references/dotnet-patterns.md) for the full `GarageWebFactory` with Testcontainers setup.

---

## Anti-Patterns

| Wrong                             | Right                                                       |
| --------------------------------- | ----------------------------------------------------------- |
| Write implementation first        | Tests first — always RED before GREEN                       |
| In-memory DB in integration tests | Testcontainers (real PostgreSQL)                            |
| Moq                               | NSubstitute                                                 |
| Test internal state               | Test observable behaviour (return values, published events) |
| Tests that depend on each other   | Each test sets up its own data                              |

---

## Run Commands

```bash
task test:all                                         # all tests
task test PROJECT=Garage/Verendar.Garage.Tests        # single project
dotnet test --filter "FullyQualifiedName~CancelAsync" # single test
```
