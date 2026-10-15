---
name: dotnet-clean-code
description: Código limpio aplicado a C# y .NET. Cubre naming, tamaño de métodos y clases, estructura de archivos, comentarios efectivos, manejo de excepciones, null-handling idiomático, reglas de refactoring y code smells específicos de .NET. Actívala al revisar PRs, refactorizar código legacy, establecer estándares de equipo o mejorar mantenibilidad.
disable-model-invocation: true
---

# Código Limpio en .NET

Guía de código limpio idiomático en C#. Basada en Clean Code (Robert C. Martin) pero adaptada al ecosistema .NET moderno (9/10).

---

## Naming

### Regla de oro

> El nombre debe revelar la intención. No debería necesitar un comentario para entenderse.

### Variables

```csharp
// ❌ Nombres que no revelan intención
var d = DateTime.Now;           // ¿d de qué?
var list = new List<Order>();   // ¿lista de qué?
var flag = true;                // ¿qué flag?
var temp = Calculate();         // ¿temporal para qué?

// ✅ Nombres que responden "¿qué es esto?"
var today = DateTime.Now;
var pendingOrders = new List<Order>();
var isPaymentAuthorized = true;
var orderTotal = CalculateTotal(order);
```

### Booleanos

```csharp
// Prefijo is/has/can/should
bool isActive = true;
bool hasItems = order.Items.Count > 0;
bool canCancel = order.Status == OrderStatus.Pending;
bool shouldNotify = order.Total > 1000;

// ❌ Nombres que no sugieren booleano
bool active;      // ¿objeto? ¿estado?
bool notify;      // ¿verbo? ¿acción?
bool empty;       // ¿adjetivo suelto?
```

### Métodos

```csharp
// ✅ Verbo + sustantivo (o solo verbo si el contexto es obvio)
public async Task<OrderDto> GetOrderByIdAsync(Guid id, CancellationToken ct);
public async Task CancelOrderAsync(Guid id, string reason, CancellationToken ct);
public Money CalculateTax(Order order);
public bool CanBeCancelled();

// ✅ Método booleano empieza con Is/Has/Can
public bool IsOverdue(DateTime dueDate) => dueDate < DateTime.UtcNow;
public bool HasPendingItems() => Items.Any(i => i.Status == ItemStatus.Pending);

// ❌ Nombres genéricos
public void Process();       // ¿Procesar qué?
public Task Handle();        // ¿Manejar qué?
public object GetData();     // ¿Qué datos?
```

### Clases

```csharp
// ✅ Sustantivo o frase nominal. No verbo.
public class OrderService { }
public class InvoicePdfGenerator { }
public class EmailNotificationHandler { }

// ❌ Nombres de clase con verbo, vagos, o sufijos genéricos
public class ProcessOrder { }     // ¿Clase o método?
public class Manager { }           // ¿Manager de qué?
public class OrderHelper { }       // Helper = "no sé dónde poner esto"
public class CommonUtils { }       // Basurero
```

---

## Tamaño

### Métodos

```csharp
// ❌ Método largo: mezcla validación, lógica de negocio, y efectos secundarios
public async Task<OrderResult> PlaceOrderAsync(PlaceOrderRequest request)
{
    // 20 líneas de validación
    if (string.IsNullOrEmpty(request.CustomerId)) throw new...
    if (request.Items is null || request.Items.Count == 0) throw new...
    foreach (var item in request.Items)
    {
        if (item.Quantity <= 0) throw new...
        if (string.IsNullOrEmpty(item.Sku)) throw new...
    }

    // 30 líneas de carga de datos
    var customer = await...
    var products = await...
    var inventory = await...

    // 40 líneas de lógica de negocio
    foreach (var item in request.Items)
    {
        var product = products.First(p => p.Sku == item.Sku);
        if (product.Price != item.ExpectedPrice)...
        // ...
    }

    // 20 líneas de guardado y notificación
    await _db.Orders.AddAsync(order);
    await _db.SaveChangesAsync();
    await _emailSender.SendAsync(...);
    await _eventBus.PublishAsync(new OrderPlacedEvent(order.Id));
}
// Total: ~110 líneas. Imposible de testear unitariamente y entender de un vistazo.
```

**Regla**: Si un método no cabe en una pantalla (~30 líneas), extraer.

```csharp
// ✅ Método corto que orquesta, no implementa
public async Task<OrderResult> PlaceOrderAsync(PlaceOrderRequest request, CancellationToken ct)
{
    Validate(request);
    var context = await LoadContextAsync(request, ct);
    var order = CreateOrder(request, context);
    await PersistAndNotifyAsync(order, ct);
    return OrderResult.From(order);
}

private static void Validate(PlaceOrderRequest request) { /* solo validación */ }
private async Task<OrderContext> LoadContextAsync(PlaceOrderRequest request, CancellationToken ct) { ... }
private static Order CreateOrder(PlaceOrderRequest request, OrderContext context) { ... }
private async Task PersistAndNotifyAsync(Order order, CancellationToken ct) { ... }
```

### Clases

| Tamaño | Acción |
|--------|--------|
| < 100 líneas | ✅ Ideal |
| 100–200 líneas | ⬜ Aceptable si es cohesiva |
| 200–400 líneas | ⚠️ Sospechoso. Verificar SRP. |
| > 400 líneas | ❌ Refactorizar. Seguramente son 2+ clases. |

### Archivos

Un tipo público por archivo. Excepción: records/DTOs pequeños y relacionados pueden coexistir.

```csharp
// ✅ Ok: tipos íntimamente relacionados
// Orders/CreateOrder.cs
public record CreateOrderRequest(string CustomerId, List<OrderItemDto> Items);
public record OrderItemDto(string Sku, int Quantity, decimal ExpectedPrice);
public record CreateOrderResponse(Guid OrderId, string Status);

// ❌ No ok: tipos no relacionados en un solo archivo
// Models.cs
public class Order { ... }
public class Customer { ... }
public class Invoice { ... }
```

---

## Estructura de una clase

Orden canónico:

```csharp
public class OrderService
{
    // 1. Campos privados (readonly primero)
    private readonly IOrderRepository _orderRepository;
    private readonly ILogger<OrderService> _logger;

    // 2. Constructor (uno solo, o sobrecargas llamando a this(...))
    public OrderService(IOrderRepository orderRepository, ILogger<OrderService> logger)
    {
        _orderRepository = orderRepository;
        _logger = logger;
    }

    // 3. Propiedades públicas (si las hay)
    public int OperationsPerformed { get; private set; }

    // 4. Métodos públicos
    public async Task<OrderDto> GetByIdAsync(Guid id, CancellationToken ct) { ... }
    public async Task CancelAsync(Guid id, CancellationToken ct) { ... }

    // 5. Métodos privados (llamados por los públicos, en orden de aparición)
    private async Task<Order> LoadOrderAsync(Guid id, CancellationToken ct) { ... }
    private static void ValidateCancellation(Order order) { ... }
}
```

---

## Comentarios

### La regla: el código se documenta solo. El comentario explica el POR QUÉ, no el QUÉ.

```csharp
// ❌ Comentario redundante — repite el código
// Get order by id
public async Task<Order> GetOrderByIdAsync(Guid id)
{
    // Find the order in database
    var order = await _db.Orders.FindAsync(id);
    // Return the order
    return order;
}

// ✅ Comentario que explica la decisión (el "por qué")
public async Task ChargeAsync(Order order, CancellationToken ct)
{
    // ponytail: global lock on payment gateway. Per-account locking if throughput > 10 req/s.
    await _semaphore.WaitAsync(ct);
    try
    {
        await _gateway.ChargeAsync(order.Total, order.PaymentMethodId, ct);
    }
    finally { _semaphore.Release(); }
}

// ✅ Comentario que advierte
// WARNING: This query is not covered by an index. Do not call with high frequency.
// Use GetRecentOrdersAsync for the dashboard.
public async Task<List<Order>> GetAllOrdersAsync(CancellationToken ct) { ... }

// ✅ Comentario que referencia una decisión externa
// See: https://github.com/org/repo/issues/1234 — timeout chosen to match
// downstream Stripe timeout of 10s.
private static readonly TimeSpan PaymentTimeout = TimeSpan.FromSeconds(10);
```

### Tipos de comentarios a eliminar

| Tipo | Ejemplo | Por qué |
|------|---------|---------|
| Redundante | `// Increment counter` → `counter++` | El código ya lo dice |
| Código comentado | `// var old = OldMethod();` | Git tiene la historia |
| Diario | `// 2024-03-15: Miguel changed this` | Git blame |
| Divider | `// ═══════ ORDERS ═══════` | Las clases y métodos ya dividen |
| TODO sin dueño | `// TODO: fix this` | Sin issue asociado, no se hará nunca |

### TODO efectivo

```csharp
// ✅ TODO con issue y dueño
// TODO(SPK-456, @miguel): Replace with HybridCache when migrating to .NET 9+
var cached = await _memoryCache.GetOrCreateAsync(...);
```

---

## Métodos: reglas de oro

### 1. Un nivel de abstracción por método

```csharp
// ❌ Mezcla alto nivel (orquestación) con bajo nivel (concatenar strings)
public async Task SendOrderConfirmationAsync(Order order)
{
    var email = await _templateService.LoadTemplateAsync("order-confirmation", ct);
    var body = email.Replace("{{OrderId}}", order.Id.ToString())
                    .Replace("{{Total}}", order.Total.ToString("C"))
                    .Replace("{{Date}}", order.CreatedAt.ToString("d"));
    await _emailSender.SendAsync(order.CustomerEmail, "Order Confirmed", body, ct);
}

// ✅ Cada método en su nivel de abstracción
public async Task SendOrderConfirmationAsync(Order order, CancellationToken ct)
{
    var body = await BuildEmailBodyAsync(order, ct);
    await _emailSender.SendAsync(order.CustomerEmail, "Order Confirmed", body, ct);
}

private async Task<string> BuildEmailBodyAsync(Order order, CancellationToken ct)
{
    var template = await _templateService.LoadTemplateAsync("order-confirmation", ct);
    return template.Replace("{{OrderId}}", order.Id.ToString())
                   .Replace("{{Total}}", order.Total.ToString("C"))
                   .Replace("{{Date}}", order.CreatedAt.ToString("d"));
}
```

### 2. Pocos argumentos

| Argumentos | Acción |
|------------|--------|
| 0 | ✅ Ideal |
| 1 | ✅ Bueno |
| 2 | ⬜ Aceptable |
| 3 | ⚠️ Revisar — ¿deberían ser un objeto? |
| 4+ | ❌ Refactorizar a un DTO/request |

```csharp
// ❌ Demasiados argumentos
public async Task CreateOrderAsync(
    string customerId,
    string shippingAddress,
    string billingAddress,
    string paymentMethodId,
    List<OrderItem> items,
    string? couponCode,
    bool giftWrap,
    string? giftMessage)
{ }

// ✅ Agrupados en DTO
public record CreateOrderCommand(
    string CustomerId,
    string ShippingAddress,
    string BillingAddress,
    string PaymentMethodId,
    List<OrderItem> Items,
    string? CouponCode = null,
    bool GiftWrap = false,
    string? GiftMessage = null);

public async Task<Order> CreateOrderAsync(CreateOrderCommand command, CancellationToken ct) { }
```

### 3. Sin efectos secundarios ocultos

```csharp
// ❌ Getter que modifica estado
public decimal Total
{
    get
    {
        _accessCount++; // Efecto secundario inesperado
        return _items.Sum(i => i.Price * i.Quantity);
    }
}

// ✅ El nombre revela el efecto secundario
public int IncrementAndGetAccessCount() => ++_accessCount;
public decimal CalculateTotal() => _items.Sum(i => i.Price * i.Quantity);
```

### 4. Command-Query Separation (CQS)

```csharp
// ✅ Command: modifica estado, no retorna datos (o retorna void/result)
public async Task CancelOrderAsync(Guid id, CancellationToken ct);

// ✅ Query: retorna datos, no modifica estado
public async Task<OrderDto?> GetOrderAsync(Guid id, CancellationToken ct);

// ❌ Método que hace ambas cosas: modifica Y retorna
public async Task<Order> ProcessAndSaveAsync(Order order)
{
    order.Status = OrderStatus.Processed; // modifica
    _db.Orders.Add(order);
    await _db.SaveChangesAsync();
    return order; // retorna — ¿el caller sabe que ya se guardó?
}
```

---

## Excepciones: uso limpio

### Prefiere excepciones custom de dominio

```csharp
// ✅ Jerarquía clara
public abstract class DomainException(string message) : Exception(message);

public class OrderNotFoundException(Guid orderId)
    : DomainException($"Order {orderId} not found");

public class InsufficientStockException(string sku, int requested, int available)
    : DomainException($"Insufficient stock for {sku}: requested {requested}, available {available}");

public class PaymentFailedException(Guid orderId, string reason)
    : DomainException($"Payment failed for order {orderId}: {reason}");
```

### No atrapar para relanzar sin contexto

```csharp
// ❌ Swallow silencioso
try { await _payment.ChargeAsync(order, ct); }
catch (Exception) { } // El pago falló y nadie sabe

// ❌ Relanzar sin contexto
try { await _payment.ChargeAsync(order, ct); }
catch (Exception ex) { throw; } // ¿Para qué? No agrega nada

// ✅ Atrapar para enriquecer o manejar
try { await _payment.ChargeAsync(order, ct); }
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Payment gateway unreachable for order {OrderId}", order.Id);
    throw new PaymentFailedException(order.Id, "Gateway unreachable", ex);
}
```

### Using para disposables — sintaxis limpia

```csharp
// ✅ using declaration (C# 8+) — limpio y conciso
using var scope = _logger.BeginScope(new { OrderId = id });
using var transaction = await _db.Database.BeginTransactionAsync(ct);

await ProcessOrderAsync(order, ct);
await transaction.CommitAsync(ct);
// scope y transaction se disponen al salir del método

// ✅ using block — cuando necesitas disponer antes
Order order;
using (var context = new AppDbContext())
{
    order = await context.Orders.FindAsync(id);
}
// context ya está dispuesto. order se usa fuera.
```

---

## Null handling idiomático

```csharp
// ✅ Null-coalescing para defaults
var discount = order.Discount ?? Money.Zero;
var name = customer.Name ?? "Anonymous";

// ✅ Null-conditional para navegación segura
var city = customer?.Address?.City;
var count = orders?.Count ?? 0;

// ✅ Throw helper en .NET 6+
ArgumentNullException.ThrowIfNull(request);
ArgumentNullException.ThrowIfNull(request.Items);

// ✅ required + init para null-safety en compile-time
public class CreateOrderRequest
{
    public required string CustomerId { get; init; }
    public required List<OrderItemDto> Items { get; init; }
    public string? CouponCode { get; init; } // null es válido aquí
}
```

---

## Conditionals

### Early return sobre anidamiento

```csharp
// ❌ Pirámide del horror
public async Task<IActionResult> GetOrderAsync(Guid id)
{
    var order = await _repository.GetByIdAsync(id);
    if (order is not null)
    {
        if (order.Status != OrderStatus.Deleted)
        {
            if (_authorization.CanView(User, order))
            {
                return Ok(OrderDto.From(order));
            }
            else
            {
                return Forbid();
            }
        }
        else
        {
            return NotFound();
        }
    }
    else
    {
        return NotFound();
    }
}

// ✅ Early returns — flujo principal sin indentación
public async Task<IActionResult> GetOrderAsync(Guid id)
{
    var order = await _repository.GetByIdAsync(id);
    if (order is null) return NotFound();
    if (order.Status == OrderStatus.Deleted) return NotFound();
    if (!_authorization.CanView(User, order)) return Forbid();

    return Ok(OrderDto.From(order));
}
```

### Switch expression sobre if-else en cadena

```csharp
// ✅ Switch expression para mapeos
string GetStatusLabel(OrderStatus status) => status switch
{
    OrderStatus.Pending => "Pending Review",
    OrderStatus.Confirmed => "Confirmed",
    OrderStatus.Shipped => "Shipped",
    OrderStatus.Delivered => "Delivered",
    OrderStatus.Cancelled => "Cancelled",
    _ => "Unknown"
};

// ✅ Pattern matching con propiedades
string DescribeOrder(Order order) => order switch
{
    { Status: OrderStatus.Pending, Items.Count: > 10 } => "Large pending order",
    { Status: OrderStatus.Pending } => "Pending order",
    { Total: > 1000 } => "High-value order",
    _ => "Standard order"
};
```

---

## Refactoring: code smells .NET

### 1. Método largo → Extract Method

```csharp
// ❌ Todo en uno
public async Task ProcessAsync(Order order, CancellationToken ct)
{
    // validar
    if (order.Items.Count == 0) throw new...
    // calcular
    order.Total = order.Items.Sum(...)
    // guardar
    await _db.SaveChangesAsync(ct);
    // notificar
    await _email.SendAsync(...)
}

// ✅ Extraer a métodos privados nombrados → luego a clases si crecen
public async Task ProcessAsync(Order order, CancellationToken ct)
{
    ValidateOrder(order);
    CalculateTotals(order);
    await SaveAsync(order, ct);
    await NotifyAsync(order, ct);
}
```

### 2. Feature Envy → Move Method

```csharp
// ❌ OrderService obsesionado con los datos de Order
public class OrderService
{
    public decimal CalculateTotal(Order order)
    {
        return order.Items.Sum(i => i.Price * i.Quantity)
               - order.Discounts.Sum(d => d.Amount)
               + order.Taxes.Sum(t => t.Amount);
    }
}

// ✅ El cálculo pertenece a Order
public class Order
{
    public Money CalculateTotal() =>
        Items.Sum(i => i.LineTotal) - Discounts.Sum(d => d.Amount) + Taxes.Sum(t => t.Amount);
}
```

### 3. Primitive Obsession → Value Objects

```csharp
// ❌ Primitivos para conceptos de dominio
public class Order
{
    public string CustomerEmail { get; set; }        // string cualquiera
    public string Currency { get; set; }             // "USD", "MXN", "eur"?
    public decimal Total { get; set; }               // ¿IVA incluido?
}

// ✅ Value objects
public record Email
{
    public string Value { get; }
    public Email(string value)
    {
        if (string.IsNullOrWhiteSpace(value) || !value.Contains('@'))
            throw new ArgumentException("Invalid email", nameof(value));
        Value = value.Trim().ToLowerInvariant();
    }
}

public record Money(decimal Amount, string Currency)
{
    public static Money Zero(string currency = "MXN") => new(0, currency);
    public static Money operator +(Money a, Money b) =>
        a.Currency == b.Currency ? new(a.Amount + b.Amount, a.Currency)
        : throw new InvalidOperationException("Currency mismatch");
}

public class Order
{
    public Email CustomerEmail { get; set; }
    public Money Total { get; set; }
}
```

### 4. Shotgun Surgery → Consolidar responsabilidad

Si un cambio de negocio te obliga a modificar 6 archivos, la responsabilidad está dispersa.

```csharp
// ❌ Agregar un campo "TaxId" al cliente requiere tocar:
// - Customer.cs (entidad)
// - CustomerDto.cs
// - CreateCustomerRequest.cs
// - UpdateCustomerRequest.cs
// - CustomerConfiguration.cs (EF)
// - CustomerValidator.cs
// - CustomerMappingProfile.cs
// --- 7 archivos para 1 campo ---

// ✅ Solución: definir el concepto una vez
// Domain/Customers/Customer.cs → el resto se deriva o se genera
// Si usas source generators: el DTO, el validator parcial, y el mapping
// se actualizan automáticamente.
```

### 5. Dead Code → Delete

```csharp
// ❌ Código comentado "por si acaso"
// private void OldPaymentMethod() { ... }

// ❌ Método sin referencias
public void LegacyExport() { ... } // Ningún caller, 3 años así

// ❌ Enum values no usados
public enum OrderStatus
{
    Draft,         // ✅ usado
    Pending,       // ✅ usado
    Confirmed,     // ✅ usado
    Archived,      // ❌ nunca se usó. Borrar.
    Legacy_Migrated // ❌ código de migración de hace 2 años
}
```

---

## Vertical Slices: agrupar por feature, no por tipo

```csharp
// ❌ Agrupación técnica tradicional (horizontal)
Controllers/
├── OrdersController.cs
├── CustomersController.cs
Services/
├── OrderService.cs
├── CustomerService.cs
Models/
├── Order.cs
├── Customer.cs

// ✅ Agrupación por feature (vertical)
Orders/
├── CreateOrder/
│   ├── CreateOrderEndpoint.cs    // HTTP
│   ├── CreateOrderCommand.cs     // DTO
│   ├── CreateOrderHandler.cs     // lógica
│   └── CreateOrderValidator.cs   // reglas
├── CancelOrder/
│   └── CancelOrderEndpoint.cs    // todo en uno si es simple
└── GetOrder/
    └── GetOrderEndpoint.cs
Customers/
├── Register/
│   ├── RegisterCustomerEndpoint.cs
│   └── RegisterCustomerHandler.cs
└── GetProfile/
    └── GetProfileEndpoint.cs
```

Ventaja: para trabajar en la feature "Cancelar Orden", tocás una carpeta, no 4.

---

## Checklist de Clean Code para PR review

- [ ] El nombre de cada clase, método y variable revela su intención
- [ ] Ningún método tiene más de ~30 líneas
- [ ] Ninguna clase tiene más de ~300 líneas
- [ ] Los métodos tienen 0-2 argumentos; 3+ están agrupados en un DTO
- [ ] No hay `NotImplementedException` salvo en stubs explícitamente temporales
- [ ] No hay `async void` fuera de event handlers
- [ ] Los comentarios explican POR QUÉ, no QUÉ
- [ ] No hay código comentado
- [ ] Los condicionales usan early return en vez de anidamiento profundo
- [ ] Las excepciones son custom y específicas del dominio
- [ ] No hay magic strings/numbers sin nombre
- [ ] Los `using` están en formato declaration (`using var x = ...`)
- [ ] Archivos agrupados por feature, no por tipo técnico
- [ ] Si un cambio de negocio toca más de 4 archivos, considerar consolidar
