---
name: dotnet-solid
description: Principios SOLID, DRY, KISS, YAGNI aplicados a .NET y C#. Cada principio con ejemplos de violación vs corrección, patrones .NET que los implementan naturalmente, y cuándo es razonable romperlos. Incluye Separation of Concerns, Law of Demeter, Composition over Inheritance, y otros principios complementarios. Actívala al diseñar clases, revisar acoplamiento o refactorizar código legacy.
disable-model-invocation: true
---

# SOLID y Principios de Diseño en .NET

Guía práctica. Cada principio responde **qué es**, **violación típica en .NET**, **corrección idiomática**, y **cuándo ignorarlo**.

---

## SOLID

### S — Single Responsibility Principle (SRP)

> Una clase debe tener una sola razón para cambiar.

#### Violación

```csharp
// ❌ Esta clase cambia si cambia: lógica de negocio, formato de reporte, o envío de email
public class OrderProcessor
{
    public async Task ProcessAsync(Order order)
    {
        // Lógica de negocio
        if (order.Items.Count == 0)
            throw new InvalidOperationException("Empty order");
        order.Total = order.Items.Sum(i => i.Price * i.Quantity);

        // Reporte
        var html = $"<h1>Order {order.Id}</h1><p>Total: {order.Total:C}</p>";
        await File.WriteAllTextAsync($"report_{order.Id}.html", html);

        // Notificación
        await SendEmailAsync(order.CustomerEmail, "Order processed", html);
    }
}
```

#### Corrección

```csharp
// ✅ Una razón para cambiar cada una
public class OrderCalculator
{
    public Money CalculateTotal(Order order) =>
        order.Items.Aggregate(Money.Zero, (sum, item) => sum + item.LineTotal);
}

public class OrderHtmlReportGenerator
{
    public string Generate(Order order) => $"""
        <h1>Order {order.Id}</h1>
        <p>Total: {order.Total}</p>
        <p>Items: {order.Items.Count}</p>
        """;
}

public class OrderProcessor(
    OrderCalculator calculator,
    OrderHtmlReportGenerator reportGenerator,
    IEmailSender emailSender)
{
    public async Task ProcessAsync(Order order, CancellationToken ct)
    {
        order.Total = calculator.CalculateTotal(order);
        var report = reportGenerator.Generate(order);
        await emailSender.SendAsync(order.CustomerEmail, "Order processed", report, ct);
    }
}
```

#### Señales de violación

- La clase tiene más de ~200 líneas
- El nombre contiene "And" u "Or" (`OrderProcessorAndNotifier`)
- Los métodos no usen los mismos campos
- Tests de la clase mockean cosas no relacionadas

#### Cuándo ignorar SRP

- **Endpoints Minimal API**: un archivo que agrupa handler + request + response + ruta es aceptable. La "responsabilidad" es el endpoint completo.
- **DTOs anémicos**: no hay lógica que separar.
- **Configuración**: `appsettings.json` agrupa settings por sección, no es SRP pero es práctica estándar.

---

### O — Open/Closed Principle (OCP)

> Abierto a extensión, cerrado a modificación.

#### Estrategias .NET para OCP

**1. Strategy Pattern + DI**

```csharp
// Cerrado a modificación — no tocas esta interfaz
public interface IDiscountStrategy
{
    bool AppliesTo(Order order);
    Money Apply(Order order);
}

// Extensiones como nuevas clases
public class PercentageDiscount(decimal percentage) : IDiscountStrategy
{
    public bool AppliesTo(Order order) => order.Total > 100;
    public Money Apply(Order order) => order.Total * (1 - percentage);
}

public class FixedDiscount(decimal amount) : IDiscountStrategy
{
    public bool AppliesTo(Order order) => order.CustomerTier == Tier.Vip;
    public Money Apply(Order order) => order.Total - amount;
}

// El discountService no cambia al agregar nuevas estrategias
public class DiscountService(IEnumerable<IDiscountStrategy> strategies)
{
    public Money ApplyBestDiscount(Order order) =>
        strategies
            .Where(s => s.AppliesTo(order))
            .Select(s => s.Apply(order))
            .DefaultIfEmpty(order.Total)
            .Min()!;
}

// DI auto-descubre nuevas implementaciones
services.Scan(s => s
    .FromAssemblyOf<IDiscountStrategy>()
    .AddClasses(c => c.AssignableTo<IDiscountStrategy>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

**2. Middleware pipeline (ASP.NET Core)**

```csharp
// Cada middleware extiende el pipeline sin modificar los demás
app.UseExceptionHandler();
app.UseAuthentication();    // ← agregar autenticación no modifica nada existente
app.UseAuthorization();
app.UseRequestLogging();    // ← nuevo middleware, sin tocar los anteriores
```

**3. Extension methods**

```csharp
// Extiendes string sin modificar System.String
public static class StringExtensions
{
    public static string Truncate(this string value, int maxLength) =>
        value.Length <= maxLength ? value : value[..maxLength] + "...";

    public static bool IsValidEmail(this string value) =>
        Regex.IsMatch(value, @"^[^@\s]+@[^@\s]+\.[^@\s]+$");
}
```

#### Cuándo NO aplicar OCP

No envolver en abstracción si:
- El comportamiento es parte del core y **no cambia** (ej. `CalculateTotal` en un carrito)
- Hay solo 2 variantes conocidas y no se prevén más
- La abstracción duplica el código sin beneficio claro

```csharp
// ❌ Sobre-ingeniería OCP: interfaz para algo que nunca variará
public interface IMathAdd { int Add(int a, int b); }
public class MathAdd : IMathAdd { public int Add(int a, int b) => a + b; }
```

---

### L — Liskov Substitution Principle (LSP)

> Las subclases deben ser sustituibles por sus clases base sin romper el sistema.

#### Violación clásica: Rectángulo y Cuadrado

```csharp
// ❌ Cuadrado rompe el contrato de Rectángulo
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }
    public int Area() => Width * Height;
}

public class Square : Rectangle
{
    public override int Width  { set { base.Width = value; base.Height = value; } }
    public override int Height { set { base.Width = value; base.Height = value; } }
}

// Test que falla con Square
void TestArea(Rectangle rect)
{
    rect.Width = 5;
    rect.Height = 10;
    Assert.Equal(50, rect.Area()); // ❌ Square devuelve 100
}
```

#### Corrección: Preferir composición

```csharp
// ✅ No heredar. Usar una abstracción común inmutable
public interface IShape
{
    int Area();
}

public record Rectangle(int Width, int Height) : IShape
{
    public int Area() => Width * Height;
}

public record Square(int Side) : IShape
{
    public int Area() => Side * Side;
}
```

#### Violaciones comunes en .NET

```csharp
// ❌ Lanzar NotImplementedException en métodos heredados
public class ReadOnlyOrderRepository : IOrderRepository
{
    public Task SaveAsync(Order order, CancellationToken ct)
        => throw new NotImplementedException(); // Rompe LSP

    public Task<Order?> GetByIdAsync(Guid id, CancellationToken ct) { ... }
}

// ✅ Solución: dos interfaces segregadas
public interface IOrderReader { Task<Order?> GetByIdAsync(Guid id, CancellationToken ct); }
public interface IOrderWriter { Task SaveAsync(Order order, CancellationToken ct); }

public class ReadOnlyOrderRepository : IOrderReader { ... }
public class EfOrderRepository : IOrderReader, IOrderWriter { ... }
```

#### LSP Checklist

| Señal de violación | Acción |
|-------------------|--------|
| `NotImplementedException` en override | Separar interfaz (ISP) |
| `if (obj is DerivedType)` en código cliente | La abstracción no es suficiente |
| Subclase lanza excepciones que la base no declara | Repensar jerarquía |
| Subclase ignora parámetros o retorna `null` donde la base no | Contrato roto |

---

### I — Interface Segregation Principle (ISP)

> Una clase no debe depender de métodos que no usa.

#### Violación

```csharp
// ❌ Interfaz gorda: obliga a implementar métodos innecesarios
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct);
    Task<List<Order>> GetAllAsync(CancellationToken ct);
    Task SaveAsync(Order order, CancellationToken ct);
    Task DeleteAsync(Guid id, CancellationToken ct);
    Task<List<Order>> SearchAsync(OrderSearchCriteria criteria, CancellationToken ct);
    Task<OrderStats> GetStatsAsync(CancellationToken ct);
}
```

La vista de reportes usa solo `GetStatsAsync` y `GetAllAsync`. El endpoint de búsqueda solo usa `SearchAsync`. Todos implementan todo.

#### Corrección

```csharp
// ✅ Interfaces segregadas por consumidor (Role Interfaces)
public interface IOrderReader
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct);
}

public interface IOrderLister
{
    Task<List<Order>> GetAllAsync(CancellationToken ct);
}

public interface IOrderWriter
{
    Task SaveAsync(Order order, CancellationToken ct);
    Task DeleteAsync(Guid id, CancellationToken ct);
}

public interface IOrderSearcher
{
    Task<List<Order>> SearchAsync(OrderSearchCriteria criteria, CancellationToken ct);
}

public interface IOrderStatsProvider
{
    Task<OrderStats> GetStatsAsync(CancellationToken ct);
}

// Cada consumidor inyecta solo lo que necesita
public class OrderReportService(IOrderLister lister, IOrderStatsProvider stats) { ... }
public class OrderSearchEndpoint(IOrderSearcher searcher) { ... }
```

#### ISP aplicado a CQRS

Commands y queries ya segregan naturalmente:

```csharp
// ✅ CQRS como ISP natural: un handler por operación
public record GetOrderQuery(Guid Id) : IRequest<OrderDto>;

public class GetOrderHandler(IOrderReader reader)
    : IRequestHandler<GetOrderQuery, OrderDto> { ... }

public record CreateOrderCommand(...) : IRequest<Order>;

public class CreateOrderHandler(IOrderWriter writer)
    : IRequestHandler<CreateOrderCommand, Order> { ... }
```

Cada handler solo depende de lo que necesita.

---

### D — Dependency Inversion Principle (DIP)

> Depender de abstracciones, no de implementaciones concretas.

#### Los dos enunciados

1. Módulos de alto nivel no dependen de módulos de bajo nivel. Ambos dependen de abstracciones.
2. Abstracciones no dependen de detalles. Los detalles dependen de abstracciones.

#### Violación

```csharp
// ❌ OrderService (alto nivel) depende de SqlOrderRepository (bajo nivel)
public class OrderService
{
    private readonly SqlOrderRepository _repository = new("conn-string");

    public async Task<Order?> GetAsync(Guid id)
        => await _repository.FindByIdAsync(id);
}
```

#### Corrección vía DI

```csharp
// ✅ OrderService depende de IOrderRepository (abstracción)
// ✅ SqlOrderRepository depende de IOrderRepository (abstracción)
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct);
}

public class OrderService(IOrderRepository repository)
{
    public async Task<Order?> GetAsync(Guid id, CancellationToken ct)
        => await repository.GetByIdAsync(id, ct);
}

public class SqlOrderRepository(AppDbContext db) : IOrderRepository
{
    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct)
        => await db.Orders.FindAsync([id], ct);
}
```

#### DIP en la práctica .NET

```csharp
// ✅ Clean Architecture: Domain no depende de Infrastructure
// Domain/Orders/IOrderRepository.cs  ← abstracción en capa de dominio
// Infrastructure/Data/SqlOrderRepository.cs ← implementación en infraestructura

// ✅ Aplicación depende de abstracciones de dominio
public class CancelOrderHandler(
    IOrderRepository orders,     // ← abstracción
    IUnitOfWork unitOfWork,      // ← abstracción
    ILogger<CancelOrderHandler> logger) // ← abstracción de Microsoft
{
    public async Task Handle(CancelOrderCommand cmd, CancellationToken ct)
    {
        var order = await orders.GetByIdAsync(cmd.OrderId, ct)
            ?? throw new NotFoundException(nameof(Order), cmd.OrderId);

        order.Cancel();
        await unitOfWork.SaveChangesAsync(ct);
    }
}
```

#### La regla de la interfaz

> La interfaz la define el **consumidor**, no el implementador.

```csharp
// ✅ La interfaz vive en el proyecto del consumidor (Application/Domain)
// ❌ NO en el proyecto de infraestructura
// Correcto:
//   MiApp.Application/IOrderRepository.cs       ← definida por quien la usa
//   MiApp.Infrastructure/SqlOrderRepository.cs   ← implementa la abstracción
```

---

## DRY — Don't Repeat Yourself

> Cada pieza de conocimiento debe tener una representación única y autoritativa.

### DRY bien aplicado

```csharp
// ❌ Lógica de cálculo de impuesto duplicada en 5 lugares
// OrderService.cs
var tax = order.Subtotal * 0.16m;
// InvoiceService.cs
var tax = subtotal * 0.16m;
// ReportService.cs
var tax = order.Subtotal * 0.16m;

// ✅ Única fuente de verdad
public static class TaxCalculator
{
    public const decimal IvaRate = 0.16m;

    public static Money CalculateIva(Money subtotal) =>
        subtotal * IvaRate;
}
```

### DRY mal aplicado (prematuro)

```csharp
// ❌ DRY prematuro: abstraer código que solo COINCIDE, no que comparte RAZÓN DE CAMBIO
public class OrderReportPdfGenerator { ... }
public class InvoicePdfGenerator { ... }

// Forzar DRY crea acoplamiento
public abstract class BasePdfGenerator<TData> // ← acopla cosas que cambian por razones distintas
{
    protected abstract string GenerateHeader(TData data);
    protected abstract string GenerateBody(TData data);
    // Si Invoice cambia su header, Order ahora también hereda el método
}
```

### La regla DRY

> Extraer solo cuando haya **3 o más repeticiones** Y compartan la misma **razón de cambio**. Dos repeticiones idénticas pero con razones de cambio distintas → dejarlas duplicadas temporalmente.

```csharp
// ✅ Duplicación aceptable: mismo código, distinta razón de cambio
// OrderValidator.cs — cambia cuando cambian reglas de órdenes
RuleFor(o => o.CustomerId).NotEmpty().MaximumLength(50);

// CustomerValidator.cs — cambia cuando cambian reglas de clientes
RuleFor(c => c.Id).NotEmpty().MaximumLength(50);

// Forzarlos a compartir una "base" los acoplaría incorrectamente.
```

---

## KISS — Keep It Simple, Stupid

> La solución más simple que funciona es la correcta.

### Ejemplos en .NET

```csharp
// ❌ Over-engineering: patrón Strategy para elegir entre 2 formatos fijos
public interface IDateFormatter { string Format(DateTime date); }
public class IsoDateFormatter : IDateFormatter { ... }
public class UsDateFormatter : IDateFormatter { ... }

// ✅ KISS: un método con parámetro
public static string FormatDate(DateTime date, string format = "yyyy-MM-dd")
    => date.ToString(format);

// ❌ Over-engineering: crear una clase para una validación simple
public class CustomerEmailValidator
{
    private readonly Regex _regex = new(@"^[^@\s]+@[^@\s]+\.[^@\s]+$");

    public ValidationResult Validate(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return ValidationResult.Error("Email required");
        if (!_regex.IsMatch(email))
            return ValidationResult.Error("Invalid format");
        return ValidationResult.Success();
    }
}

// ✅ KISS: DataAnnotation + FluentValidation
public class CreateCustomerRequest
{
    [Required, EmailAddress]
    public string Email { get; init; } = string.Empty;
}
```

### KISS en arquitectura

| Complejidad | Alternativa KISS |
|-------------|-----------------|
| Clean Architecture con 4 proyectos | 2 proyectos (Api + App) hasta que duela |
| CQRS con MediatR | Llamada directa a servicio |
| Microservicios | Modular Monolith |
| Event Sourcing | CRUD con historial de cambios en una tabla de auditoría |
| Kubernetes para un monolito | App Service / VM |

---

## YAGNI — You Ain't Gonna Need It

> No implementar hasta que se necesite.

### Violaciones típicas en .NET

```csharp
// ❌ "Vamos a necesitar multi-tenancy en el futuro"
public interface ITenantProvider { ... }
public class SingleTenantProvider : ITenantProvider { ... }  // Solo hay 1 tenant

// ✅ Eliminar hasta que se necesite. Agregar en el PR que lo requiera.
// Si la feature de multi-tenancy nunca llega: código muerto eliminado.

// ❌ "Quizás cambiemos de SQL Server a PostgreSQL"
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<List<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(T entity);
    // 30 métodos más que solo delegan a DbSet
}

// ✅ EF Core ya abstrae el motor de BD. YAGNI el repo genérico.

// ❌ Configuración para un feature flag que nunca se activará
"Features": {
  "EnableNewCheckout": false,  // ← 2 años en false, nunca se activó
  "EnableDarkMode": false
}

// ✅ Borrar. Cuando se necesite, se agrega. Git tiene la historia.
```

---

## Principios complementarios

### Separation of Concerns (SoC)

```csharp
// ✅ Separación por responsabilidad
// Orders/CreateOrder/           ← carpeta = feature vertical
// ├── CreateOrderEndpoint.cs    ← HTTP concern
// ├── CreateOrderCommand.cs     ← contrato
// ├── CreateOrderHandler.cs     ← lógica de negocio
// └── CreateOrderValidator.cs   ← validación

// ❌ Separación técnica que esparce la feature en 5 proyectos
// Controllers/OrdersController.cs
// Services/OrderService.cs
// Models/OrderDto.cs
// Validators/OrderValidator.cs
// Data/OrderRepository.cs
```

### Composition over Inheritance

```csharp
// ❌ Herencia forzada
public class AuditableEntity
{
    public DateTime CreatedAt { get; set; }
    public string CreatedBy { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public string UpdatedBy { get; set; }
}

public class Order : AuditableEntity { ... }  // Forzado a heredar campos que quizás no aplican

// ✅ Composición (opcional)
public interface IAuditable
{
    DateTime CreatedAt { get; }
    string CreatedBy { get; }
}

public record Order : IAuditable { ... }

// ✅ O mejor: interceptor que agrega auditoría sin tocar la entidad
public class AuditableInterceptor : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken ct = default)
    {
        foreach (var entry in eventData.Context!.ChangeTracker.Entries<IAuditable>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.CreatedAt = DateTime.UtcNow;
                // entry.Entity.CreatedBy = currentUser...
            }
        }
        return new(result);
    }
}
```

### Law of Demeter (LoD) — Principio de mínimo conocimiento

```csharp
// ❌ Tren de dependencias
var street = order.Customer.Address.Street.Name;
// order conoce Customer → Customer conoce Address → Address conoce Street → Street.Name

// ✅ Tell, Don't Ask
var street = order.GetDeliveryStreetName();

// En Order.cs:
public string GetDeliveryStreetName() => Customer.Address.Street.Name;
// La navegación queda encapsulada dentro de Order
```

### Fail Fast

```csharp
// ✅ Validar al inicio, no al final
public async Task ProcessOrderAsync(Order order, CancellationToken ct)
{
    ArgumentNullException.ThrowIfNull(order);
    if (order.Items.Count == 0)
        throw new ArgumentException("Order must have items", nameof(order));
    if (order.CustomerId == Guid.Empty)
        throw new ArgumentException("Order requires a customer", nameof(order));

    // Solo ahora, con estado válido, ejecutar lógica
    await _paymentService.ChargeAsync(order, ct);
}

// ❌ Validar tarde
public async Task ProcessOrderAsync(Order order, CancellationToken ct)
{
    await _paymentService.ChargeAsync(order, ct); // Cargo primero
    if (order.Items.Count == 0) // Valido después
        throw; // Ya cobré, ahora cómo revierto?
}
```

### Convention over Configuration

```csharp
// ✅ EF Core: convención de nombres evita configuración explícita
public class Order
{
    public int Id { get; set; }           // → PK por convención
    public int CustomerId { get; set; }   // → FK por convención
    public Customer Customer { get; set; } // → Navigation property
    public decimal Total { get; set; }    // → decimal(18,2) por convención
}

// No se necesita:
// modelBuilder.Entity<Order>().HasKey(o => o.Id);
// modelBuilder.Entity<Order>().Property(o => o.Total).HasColumnType("decimal(18,2)");
```

---

## Tabla de decisión rápida

| Principio | Aplicar cuando | Ignorar cuando |
|-----------|---------------|----------------|
| SRP | Clase > 200 líneas, métodos no usan mismos campos | DTO anémico, Minimal API endpoint file |
| OCP | Nuevas variantes cada sprint, plugin system | 2 opciones fijas, nunca cambiaron |
| LSP | Jerarquía con polimorfismo real | Herencia por reuso de código (usar composición) |
| ISP | Consumidores usan subconjuntos distintos de la interfaz | Consumidores usan todos los métodos |
| DIP | Capa de dominio/aplicación, integraciones externas | Clases internas de infraestructura |
| DRY | 3+ duplicaciones con misma razón de cambio | 2 coincidencias con distinta razón de cambio |
| KISS | Siempre por defecto | — |
| YAGNI | Feature especulativa, "por si acaso" | Requerimiento confirmado para próximo sprint |

---

## Violaciones frecuentes en código .NET real

### 1. Constructor con lógica pesada

```csharp
// ❌ Constructor llama a la BD
public class OrderService
{
    private readonly List<Product> _products;

    public OrderService(AppDbContext db)
    {
        _products = db.Products.ToList(); // ← WTF
    }
}

// ✅ Solo asignar dependencias
public class OrderService(IProductRepository products)
{
    // Ya está. products se usa en los métodos cuando se necesita.
}
```

### 2. Excepciones como flujo de control

```csharp
// ❌ Usar excepción para "no encontrado" esperado
try
{
    var user = await _userService.GetByIdAsync(id);
}
catch (NotFoundException)
{
    return NotFound();
}

// ✅ Result Pattern o null check
var result = await _userService.GetByIdAsync(id);
if (result is null)
    return NotFound();

// O con Result<T>
var result = await _userService.GetByIdAsync(id);
return result.Match(
    success: user => Ok(user),
    failure: _ => NotFound());
```

### 3. Mutar entidades desde fuera

```csharp
// ❌ Modificar estado de Order desde un servicio externo
order.Status = OrderStatus.Cancelled;
order.CancelledAt = DateTime.UtcNow;

// ✅ Método de dominio que encapsula la lógica
public class Order
{
    public void Cancel(string reason)
    {
        if (Status != OrderStatus.Pending && Status != OrderStatus.Confirmed)
            throw new DomainException($"Cannot cancel order in {Status} state");

        Status = OrderStatus.Cancelled;
        CancelledAt = DateTime.UtcNow;
        CancellationReason = reason;

        AddDomainEvent(new OrderCancelledEvent(Id, reason));
    }
}
```

### 4. `async void` fuera de event handlers

```csharp
// ❌ async void en método de servicio — las excepciones no se capturan
public async void ProcessOrderAsync(Order order)
{
    await _payment.ChargeAsync(order);
}

// ✅ async Task siempre
public async Task ProcessOrderAsync(Order order, CancellationToken ct)
{
    await _payment.ChargeAsync(order, ct);
}
```

### 5. Magic strings para identificadores de política/feature

```csharp
// ❌
pipelineProvider.GetPipeline("payment-pipeline"); // typo silencioso
_httpClient.GetAsync("https://api.stripe.com/v1/charges"); // URL hardcodeada

// ✅ Constantes tipadas
public static class ResiliencePipelines
{
    public const string Payment = "payment-pipeline";
    public const string Email = "email-pipeline";
}

pipelineProvider.GetPipeline(ResiliencePipelines.Payment);

// Para URLs: IOptions<T> con sección de configuración o constantes tipadas
public static class ExternalServices
{
    public const string StripeBaseUrl = "https://api.stripe.com/v1";
}
```
