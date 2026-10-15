---
name: aspnet-testing
description: Testing de aplicaciones ASP.NET Core. Cubre integration testing con WebApplicationFactory, testing de Minimal APIs y Controllers, testing de Razor Pages, bUnit para Blazor, E2E con Playwright, test containers para servicios externos, mocking de HttpClient y SignalR, y testing de middleware y filtros. Actívala al escribir tests de integración, configurar CI/CD, o implementar test harness.
disable-model-invocation: true
---

# Testing de ASP.NET Core

Guía de testing para aplicaciones web ASP.NET Core. Stack: **xUnit + WebApplicationFactory + Testcontainers + Playwright**.

---

## Integration Testing con WebApplicationFactory

### Setup

```csharp
public class OrdersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;

    public OrdersApiTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureAppConfiguration((context, config) =>
            {
                // Configuración de test
                config.AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["ConnectionStrings:Default"] = _testConnectionString,
                    ["Stripe:ApiKey"] = "sk_test_fake"
                });
            });

            builder.ConfigureServices(services =>
            {
                // Reemplazar servicios reales por fakes
                var emailDescriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(IEmailSender));
                if (emailDescriptor is not null)
                    services.Remove(emailDescriptor);

                services.AddScoped<IEmailSender, FakeEmailSender>();
            });
        });

        _client = _factory.CreateClient();
    }
}
```

### Test de endpoint

```csharp
[Fact]
public async Task CreateOrder_WithValidData_ReturnsCreated()
{
    // Arrange
    var request = new
    {
        customerId = "CUST-001",
        items = new[]
        {
            new { sku = "SKU-001", quantity = 2, price = 100m }
        }
    };

    // Act
    var response = await _client.PostAsJsonAsync("/api/orders", request);

    // Assert
    response.StatusCode.Should().Be(HttpStatusCode.Created);
    var body = await response.Content.ReadFromJsonAsync<OrderResponse>();
    body!.Id.Should().NotBeEmpty();
    body.Status.Should().Be("Pending");
}

[Fact]
public async Task GetOrder_WithInvalidId_ReturnsNotFound()
{
    var response = await _client.GetAsync($"/api/orders/{Guid.NewGuid()}");
    response.StatusCode.Should().Be(HttpStatusCode.NotFound);
}

[Fact]
public async Task CreateOrder_WithInvalidData_ReturnsValidationError()
{
    var request = new { customerId = "", items = Array.Empty<object>() };

    var response = await _client.PostAsJsonAsync("/api/orders", request);
    response.StatusCode.Should().Be(HttpStatusCode.BadRequest);

    var problem = await response.Content
        .ReadFromJsonAsync<ValidationProblemDetails>();
    problem!.Errors.Should().ContainKey("customerId");
}
```

### Custom WebApplicationFactory (reutilizable)

```csharp
public class TestWebApplicationFactory<TProgram> : WebApplicationFactory<TProgram>
    where TProgram : class
{
    private readonly MsSqlContainer _sqlContainer;
    private string _connectionString = string.Empty;

    public TestWebApplicationFactory()
    {
        _sqlContainer = new MsSqlBuilder()
            .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
            .WithPassword("Test@Pass123")
            .Build();
    }

    public async Task InitializeAsync()
    {
        await _sqlContainer.StartAsync();
        _connectionString = _sqlContainer.GetConnectionString();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Reemplazar DbContext con test DB
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor is not null) services.Remove(descriptor);

            services.AddDbContext<AppDbContext>(options =>
                options.UseSqlServer(_connectionString));

            // Migrar esquema
            using var scope = services.BuildServiceProvider().CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.Database.EnsureCreated();
        });
    }

    public new async Task DisposeAsync()
    {
        await _sqlContainer.DisposeAsync();
        await base.DisposeAsync();
    }
}
```

---

## Testing de Minimal APIs

```csharp
public class CreateOrderEndpointTests
{
    [Fact]
    public async Task Handle_WithValidRequest_ReturnsCreated()
    {
        // Arrange
        var orderService = Substitute.For<IOrderService>();
        orderService.CreateAsync(Arg.Any<CreateOrderCommand>(), Arg.Any<CancellationToken>())
            .Returns(new OrderResult(Guid.NewGuid(), "Pending", 150m));

        var linker = Substitute.For<LinkGenerator>();
        linker.GetPathByName("GetOrder", Arg.Any<object>())
            .Returns("/api/orders/123");

        var request = new CreateOrderEndpoint.Request("CUST-1", [new("SKU1", 2, 100m)]);

        var httpContext = new DefaultHttpContext();
        httpContext.RequestServices = new ServiceCollection()
            .AddSingleton(orderService)
            .BuildServiceProvider();

        // Act — llamar al método directamente
        var result = await (IResult)typeof(CreateOrderEndpoint)
            .GetMethod("HandleAsync", BindingFlags.NonPublic | BindingFlags.Static)!
            .Invoke(null, [request, orderService, linker, httpContext, CancellationToken.None])!;

        // Assert
        result.Should().BeOfType<Created<IResult>>();
    }
}
```

---

## Testing de Razor Pages

```csharp
public class CreateOrderPageTests
{
    [Fact]
    public async Task OnPostAsync_WithValidModel_RedirectsToIndex()
    {
        // Arrange
        var orderService = Substitute.For<IOrderService>();
        var logger = NullLogger<CreateModel>.Instance;

        var pageModel = new CreateModel(orderService, logger)
        {
            Input = new CreateOrderInput
            {
                CustomerName = "Test User",
                Email = "test@example.com",
                Quantity = 5
            }
        };

        orderService.CreateAsync(Arg.Any<CreateOrderInput>(), Arg.Any<CancellationToken>())
            .Returns(new OrderResult(Guid.NewGuid(), "Pending", 500m));

        // Act
        var result = await pageModel.OnPostAsync(CancellationToken.None);

        // Assert
        result.Should().BeOfType<RedirectToPageResult>()
            .Which.PageName.Should().Be("./Index");

        pageModel.SuccessMessage.Should().NotBeNull();
    }
}
```

---

## Testing de Controllers

```csharp
public class OrdersControllerTests
{
    [Fact]
    public async Task GetById_WhenOrderExists_ReturnsOk()
    {
        // Arrange
        var orderService = Substitute.For<IOrderService>();
        var order = new OrderDto(Guid.NewGuid(), "CUST-1", 150m, "Pending");
        orderService.GetByIdAsync(order.Id, Arg.Any<CancellationToken>()).Returns(order);

        var controller = new OrdersController(orderService);

        // Act
        var result = await controller.GetById(order.Id, CancellationToken.None);

        // Assert
        result.Should().BeOfType<OkObjectResult>()
            .Which.Value.Should().BeEquivalentTo(order);
    }
}
```

---

## Testing de Blazor con bUnit

```csharp
// Paquete: bUnit
public class OrderCardTests : TestContext
{
    [Fact]
    public void Renders_OrderInformation()
    {
        // Arrange
        var order = new OrderDto
        {
            Id = Guid.NewGuid(),
            CustomerName = "Test Customer",
            Total = 150m,
            Status = "Pending"
        };

        // Act
        var cut = RenderComponent<OrderCard>(parameters => parameters
            .Add(p => p.Order, order));

        // Assert
        cut.Markup.Should().Contain("Test Customer");
        cut.Markup.Should().Contain("$150.00");
        cut.Find(".badge").TextContent.Should().Be("Pending");
    }

    [Fact]
    public void OnClick_InvokesEventCallback()
    {
        Guid? clickedId = null;
        var order = new OrderDto { Id = Guid.NewGuid(), CustomerName = "Test", Total = 100m };

        var cut = RenderComponent<OrderCard>(parameters => parameters
            .Add(p => p.Order, order)
            .Add(p => p.OnSelected, id => clickedId = id));

        cut.Find("button").Click();

        clickedId.Should().Be(order.Id);
    }

    [Fact]
    public void AuthorizedView_ShowsContent()
    {
        // Arrange: simular usuario autenticado
        var authContext = this.AddTestAuthorization();
        authContext.SetAuthorized("testuser");
        authContext.SetRoles("Admin");

        // Act
        var cut = RenderComponent<AdminPanel>();

        // Assert
        cut.Markup.Should().Contain("Admin Controls");
    }
}
```

---

## Mocking HttpClient

```csharp
// Usar HttpMessageHandler mockeado para simular APIs externas
public class FakeHttpMessageHandler : HttpMessageHandler
{
    private readonly Func<HttpRequestMessage, HttpResponseMessage> _handler;

    public FakeHttpMessageHandler(Func<HttpRequestMessage, HttpResponseMessage> handler)
        => _handler = handler;

    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken ct)
        => Task.FromResult(_handler(request));
}

// Uso con IHttpClientFactory
var handler = new FakeHttpMessageHandler(request =>
{
    if (request.RequestUri!.PathAndQuery.Contains("charges"))
    {
        return new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(@"{""id"": ""ch_123"", ""status"": ""succeeded""}")
        };
    }
    return new HttpResponseMessage(HttpStatusCode.NotFound);
});

var client = new HttpClient(handler) { BaseAddress = new Uri("https://api.stripe.com/v1/") };

// Inyectar via IHttpClientFactory
services.AddHttpClient<IStripeService, StripeService>()
    .ConfigurePrimaryHttpMessageHandler(() => handler);
```

---

## E2E con Playwright

```csharp
// Paquete: Microsoft.Playwright
public class OrdersE2ETests : IAsyncLifetime
{
    private IPlaywright _playwright = null!;
    private IBrowser _browser = null!;

    public async Task InitializeAsync()
    {
        _playwright = await Playwright.CreateAsync();
        _browser = await _playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = true
        });
    }

    public async Task DisposeAsync()
    {
        await _browser.DisposeAsync();
        _playwright.Dispose();
    }

    [Fact]
    public async Task CreateOrder_FromUI_CreatesSuccessfully()
    {
        // Arrange
        var page = await _browser.NewPageAsync(new BrowserNewPageOptions
        {
            BaseURL = "https://localhost:5001"
        });

        // Act
        await page.GotoAsync("/orders/create");
        await page.FillAsync("#customer-name", "E2E Test User");
        await page.FillAsync("#email", "e2e@test.com");
        await page.FillAsync("#quantity", "3");
        await page.ClickAsync("button[type='submit']");

        // Assert
        await page.WaitForURLAsync("**/orders");
        var message = await page.TextContentAsync(".alert-success");
        message.Should().Contain("created successfully");
    }
}
```

---

## Testing de Middleware

```csharp
public class RequestLoggingMiddlewareTests
{
    [Fact]
    public async Task LogsRequestInfo()
    {
        // Arrange
        var logger = Substitute.For<ILogger<RequestLoggingMiddleware>>();
        var middleware = new RequestLoggingMiddleware(
            next: context => Task.CompletedTask,
            logger: logger);

        var context = new DefaultHttpContext();
        context.Request.Method = "GET";
        context.Request.Path = "/api/orders";
        context.Response.StatusCode = 200;

        // Act
        await middleware.InvokeAsync(context);

        // Assert
        logger.Received(1).Log(
            LogLevel.Information,
            Arg.Any<EventId>(),
            Arg.Is<object>(o => o.ToString()!.Contains("/api/orders")),
            null,
            Arg.Any<Func<object, Exception?, string>>());
    }
}
```

---

## Testing de SignalR

```csharp
public class OrderHubTests
{
    [Fact]
    public async Task SubscribeToOrder_AddsToGroup()
    {
        // Arrange
        var hub = new OrderHub(NullLogger<OrderHub>.Instance);
        var mockClients = Substitute.For<IHubCallerClients>();
        var mockGroups = Substitute.For<IGroupManager>();
        var mockContext = Substitute.For<HubCallerContext>();
        mockContext.ConnectionId.Returns("conn-123");

        hub.Clients = mockClients;
        hub.Groups = mockGroups;
        hub.Context = mockContext;

        // Act
        await hub.SubscribeToOrder("order-456");

        // Assert
        await mockGroups.Received(1)
            .AddToGroupAsync("conn-123", "order-order-456", Arg.Any<CancellationToken>());
    }
}
```

---

## Test data builders específicos para ASP.NET

```csharp
// Builder para HttpContext
public static HttpContext CreateTestHttpContext(IServiceProvider? services = null)
{
    var context = new DefaultHttpContext();
    context.RequestServices = services ?? new ServiceCollection().BuildServiceProvider();
    context.Response.Body = new MemoryStream();
    return context;
}

// Builder para ClaimsPrincipal
public static ClaimsPrincipal CreateTestUser(
    string userId = "test-user",
    string role = "User",
    params string[] permissions)
{
    var claims = new List<Claim>
    {
        new(ClaimTypes.NameIdentifier, userId),
        new(ClaimTypes.Name, "Test User"),
        new(ClaimTypes.Role, role)
    };

    foreach (var permission in permissions)
        claims.Add(new Claim("permissions", permission));

    return new ClaimsPrincipal(new ClaimsIdentity(claims, "Test"));
}
```

---

## CI/CD testing pipeline

```yaml
# .github/workflows/dotnet-tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      sqlserver:
        image: mcr.microsoft.com/mssql/server:2022-latest
        env:
          ACCEPT_EULA: Y
          MSSQL_SA_PASSWORD: Test@Pass123
        ports:
          - 1433:1433

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'

      - run: dotnet test --configuration Release --collect:"XPlat Code Coverage"
      - run: dotnet reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coverage
```

---

## Anti-patrones de testing ASP.NET

| Anti-patrón | Corrección |
|-------------|------------|
| Mockear DbContext | WebApplicationFactory + Testcontainers |
| No limpiar BD entre tests | `Respawn` o `EnsureDeleted`/`EnsureCreated` |
| Testear solo el happy path | Al menos 1 test de error por endpoint |
| `async void` en tests | `async Task` siempre |
| Hardcodear URLs | Usar `_client` del WebApplicationFactory |
| Tests con `Thread.Sleep` | `await Task.Delay` o polling con timeout |
| Sin test de auth | Testear endpoints con usuario autenticado y sin autenticar |

---

## Checklist testing ASP.NET

- [ ] Integration tests con WebApplicationFactory
- [ ] BD de test con Testcontainers (no InMemory)
- [ ] Fakes para servicios externos (email, payment gateway)
- [ ] Mock de HttpClient para APIs externas
- [ ] Tests cubren happy path + errores + auth
- [ ] E2E tests con Playwright para flujos críticos
- [ ] bUnit para componentes Blazor
- [ ] Tests de Razor Pages (model state validation)
- [ ] Tests de SignalR hubs
- [ ] Tests de middleware y filtros
- [ ] CI ejecuta tests en cada PR
- [ ] Cobertura medida y visible
