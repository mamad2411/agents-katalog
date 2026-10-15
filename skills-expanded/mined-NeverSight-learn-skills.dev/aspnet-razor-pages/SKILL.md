---
name: aspnet-razor-pages
description: ASP.NET Core Razor Pages. Cubre PageModel, handlers, model binding, validación, TempData, partial views, ViewData, routing por carpetas, filtros para Razor Pages, inyección en pages, y convenciones para aplicaciones basadas en páginas. Actívala al construir aplicaciones Razor Pages, convertir MVC a Razor Pages, o al implementar formularios y contenido web.
disable-model-invocation: true
---

# ASP.NET Core Razor Pages

Guía completa de Razor Pages en .NET 9/10. Ideal para aplicaciones web con formularios, contenido, y SEO.

---

## Setup

```csharp
// Program.cs
builder.Services.AddRazorPages(options =>
{
    // Convenciones globales
    options.Conventions.AuthorizePage("/Admin/Index", "AdminPolicy");
    options.Conventions.AuthorizeFolder("/Admin", "AdminPolicy");
    options.Conventions.AllowAnonymousToPage("/Public/Index");
    options.Conventions.AddPageRoute("/Products/Details", "products/{sku}"); // Ruta amigable
});

var app = builder.Build();

app.MapRazorPages();
```

---

## Estructura de carpetas

```
Pages/
├── _ViewStart.cshtml            # Layout por defecto
├── _ViewImports.cshtml          # Directivas globales
├── _Layout.cshtml               # Layout principal
├── _ValidationScriptsPartial.cshtml
├── Index.cshtml                 # Página principal
├── Index.cshtml.cs              # PageModel
├── Error.cshtml                 # Página de error
├── Orders/
│   ├── Index.cshtml             # Lista
│   ├── Index.cshtml.cs
│   ├── Details.cshtml           # Detalle
│   ├── Details.cshtml.cs
│   ├── Create.cshtml            # Formulario de creación
│   └── Create.cshtml.cs
├── Products/
│   ├── Index.cshtml
│   └── Details.cshtml.cs        # PageModel sin View puede existir
├── Admin/
│   └── Dashboard/
│       └── Index.cshtml
└── Shared/
    ├── _OrderCard.cshtml        # Partial
    ├── _StatusBadge.cshtml
    └── _Pagination.cshtml       # ViewComponent sería mejor
```

---

## PageModel

### Estructura canónica

```csharp
public class CreateModel : PageModel
{
    private readonly IOrderService _orderService;
    private readonly ILogger<CreateModel> _logger;

    public CreateModel(IOrderService orderService, ILogger<CreateModel> logger)
    {
        _orderService = orderService;
        _logger = logger;
    }

    [BindProperty]
    public CreateOrderInput Input { get; set; } = new();

    [TempData]
    public string? SuccessMessage { get; set; }

    public void OnGet()
    {
        // Inicializar dropdowns, cargar datos para selects, etc.
    }

    public async Task<IActionResult> OnPostAsync(CancellationToken ct)
    {
        if (!ModelState.IsValid)
            return Page();

        var order = await _orderService.CreateAsync(Input, ct);
        _logger.LogInformation("Order {OrderId} created", order.Id);

        SuccessMessage = $"Order #{order.Id} created successfully";
        return RedirectToPage("./Index");
    }
}
```

### Handlers nombrados

```csharp
// GET /Orders/Details?id=5
public async Task<IActionResult> OnGetAsync(int id, CancellationToken ct)
{
    Order = await _orderService.GetByIdAsync(id, ct);
    if (Order is null) return NotFound();
    return Page();
}

// POST /Orders/Details/5?handler=Delete
public async Task<IActionResult> OnPostDeleteAsync(int id, CancellationToken ct)
{
    await _orderService.DeleteAsync(id, ct);
    return RedirectToPage("./Index");
}

// GET /Orders/Details/5?handler=Export
public async Task<IActionResult> OnGetExportAsync(int id, CancellationToken ct)
{
    var pdf = await _orderService.ExportPdfAsync(id, ct);
    return File(pdf, "application/pdf", $"order-{id}.pdf");
}

// En la View:
// <form asp-page-handler="Delete" method="post">
//     <button type="submit">Delete</button>
// </form>
// <a asp-page="./Details" asp-route-id="5" asp-page-handler="Export">Export PDF</a>
```

---

## Model Binding

```csharp
public class CreateOrderInput
{
    [Required]
    [Display(Name = "Customer Name")]
    [StringLength(100)]
    [BindProperty(Name = "customer_name")] // Mapeo custom
    public string CustomerName { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required]
    [Range(1, 999)]
    public int Quantity { get; set; }

    [Display(Name = "Express Delivery")]
    public bool IsExpress { get; set; }

    // Binding de propiedades complejas
    public Address ShippingAddress { get; set; } = new();

    // Lista con binding
    public List<OrderItemInput> Items { get; set; } = [];
}

public class OrderItemInput
{
    public string Sku { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}

// Binding de lista en Razor
// <input type="hidden" name="Input.Items[0].Sku" value="SKU1" />
// <input type="hidden" name="Input.Items[0].Quantity" value="2" />
// <input type="hidden" name="Input.Items[0].Price" value="10.00" />
// <input asp-for="Input.Items[i].Sku" />
```

### Binding de query y route

```csharp
// GET /Orders?search=term&page=2
public void OnGet([FromQuery] string? search, [FromQuery] int page = 1)
{
    // ...
}

// GET /Orders/Details/5
public async Task<IActionResult> OnGetAsync(int id) // id viene de la ruta
{
    // ...
}
```

---

## Validación

### Lado servidor

```csharp
public async Task<IActionResult> OnPostAsync(CancellationToken ct)
{
    // Validación de reglas de negocio (adicional a DataAnnotations)
    if (Input.Quantity > 100 && Input.IsExpress)
    {
        ModelState.AddModelError("Input.Quantity",
            "Express delivery not available for orders over 100 items");
    }

    if (!ModelState.IsValid)
        return Page();

    // Procesar...
}
```

### Lado cliente

```razor
@section Scripts {
    @{ await Html.RenderPartialAsync("_ValidationScriptsPartial"); }
}
```

### Validación remota

```csharp
// PageModel
public async Task<JsonResult> OnGetVerifyEmailAsync(string email)
{
    var exists = await _userService.EmailExistsAsync(email);
    return exists ? new JsonResult($"Email {email} is already in use") : new JsonResult(true);
}

// En la View
// <input asp-for="Input.Email" />
// El atributo [Remote] no funciona igual en Razor Pages.
// Usar [PageRemote] o implementar manual con JS.
```

---

## Navegación y routing

### Generar URLs

```razor
@* Misma página *@
<a asp-page="./Index">Back to list</a>

@* Otra página en misma carpeta *@
<a asp-page="./Details" asp-route-id="@order.Id">View</a>

@* Página en otra carpeta *@
<a asp-page="/Admin/Dashboard/Index">Admin</a>

@* Con handler *@
<a asp-page="./Details" asp-route-id="5" asp-page-handler="Export">Export PDF</a>

@* Con área *@
<a asp-area="Admin" asp-page="/Dashboard/Index">Dashboard</a>
```

### Rutas amigables

```csharp
// Program.cs
options.Conventions.AddPageRoute("/Products/Details", "products/{sku}");

// Ahora: /products/SKU123 → Products/Details.cshtml?sku=SKU123

// PageModel
public async Task<IActionResult> OnGetAsync(string sku, CancellationToken ct)
{
    Product = await _productService.GetBySkuAsync(sku, ct);
    if (Product is null) return NotFound();
    return Page();
}
```

---

## TempData y mensajes flash

```csharp
// PageModel con TempData
public class CreateModel : PageModel
{
    [TempData]
    public string? SuccessMessage { get; set; }

    public async Task<IActionResult> OnPostAsync(CancellationToken ct)
    {
        SuccessMessage = "Order created successfully!";
        return RedirectToPage("./Index");
    }
}

// En Index.cshtml
@if (TempData["SuccessMessage"] is string msg)
{
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        @msg
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
}
```

---

## Partial Views

```razor
@* Pasar modelo *@
<partial name="_OrderCard" model="order" />

@* Sin modelo (usa el Model de la página padre) *@
<partial name="_Header" />

@* Con ViewData adicional *@
@{
    var viewData = new ViewDataDictionary(ViewData) { { "ShowFooter", true } };
}
<partial name="_OrderCard" model="order" view-data="viewData" />

@* Async partial (para datos que requieren I/O) *@
@await Html.PartialAsync("_OrderCard", order)
```

### Partial con lógica

```csharp
// Shared/_RecentOrders.cshtml.cs
public class RecentOrdersModel : PageModel
{
    private readonly IOrderService _orderService;
    public List<OrderDto> Orders { get; set; } = [];

    public RecentOrdersModel(IOrderService orderService) => _orderService = orderService;

    public async Task OnGetAsync(CancellationToken ct)
    {
        Orders = await _orderService.GetRecentAsync(5, ct);
    }
}
```

---

## ViewComponents en Razor Pages

```csharp
// Componente reutilizable con lógica propia
public class OrderStatsViewComponent : ViewComponent
{
    private readonly IOrderService _orderService;

    public OrderStatsViewComponent(IOrderService orderService) => _orderService = orderService;

    public async Task<IViewComponentResult> InvokeAsync()
    {
        var stats = await _orderService.GetStatsAsync();
        return View(stats);
    }
}

// Views/Shared/Components/OrderStats/Default.cshtml
@model OrderStats
<div class="row">
    <div class="col">Total: @Model.TotalOrders</div>
    <div class="col">Pending: @Model.Pending</div>
    <div class="col">Revenue: @Model.Revenue.ToString("C")</div>
</div>

// Invocar en cualquier página
@await Component.InvokeAsync("OrderStats")
```

---

## Filtros para Razor Pages

```csharp
// Filtro custom
public class LogPageAccessFilter : IAsyncPageFilter
{
    private readonly ILogger<LogPageAccessFilter> _logger;

    public LogPageAccessFilter(ILogger<LogPageAccessFilter> logger) => _logger = logger;

    public async Task OnPageHandlerExecutionAsync(
        PageHandlerExecutingContext context,
        PageHandlerExecutionDelegate next)
    {
        _logger.LogInformation("Accessing {Page} by {User}",
            context.ActionDescriptor.RelativePath,
            context.HttpContext.User.Identity?.Name ?? "Anonymous");

        await next();
    }

    public Task OnPageHandlerSelectionAsync(PageHandlerSelectedContext context)
        => Task.CompletedTask;
}

// Aplicar filtro
[ServiceFilter(typeof(LogPageAccessFilter))]
public class CreateModel : PageModel { ... }
```

---

## Anti-forgery (CSRF)

```csharp
// Razor Pages incluye anti-forgery por defecto en todos los POST.
// No necesitas [ValidateAntiForgeryToken] explícito.

// Para AJAX POST:
// Incluir el token en el header:
// <form method="post">
//     @Html.AntiForgeryToken()
//     ...
// </form>

// Configurar
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "RequestVerificationToken";
    options.Cookie.Name = "XSRF-TOKEN";
    options.Cookie.HttpOnly = false; // Para que JS pueda leer la cookie
});
```

---

## Inyección directa en la View

```razor
@* Directiva al inicio de la View *@
@inject IUserContext UserContext
@inject Microsoft.Extensions.Configuration.IConfiguration Config

<p>Welcome, @UserContext.CurrentUserName</p>
<p>Environment: @Config["ASPNETCORE_ENVIRONMENT"]</p>
```

---

## Manejo de errores

```csharp
// Pages/Error.cshtml.cs
[ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
[IgnoreAntiforgeryToken]
public class ErrorModel : PageModel
{
    public string? RequestId { get; set; }
    public bool ShowRequestId => !string.IsNullOrEmpty(RequestId);
    public int? StatusCode { get; set; }

    public void OnGet(int? statusCode = null)
    {
        RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier;
        StatusCode = statusCode;
    }
}

// Pages/Error.cshtml
@page "{statusCode?}"
@model ErrorModel
@{
    ViewData["Title"] = Model.StatusCode switch
    {
        404 => "Page Not Found",
        500 => "Server Error",
        _ => "Error"
    };
}

<h1>@Model.StatusCode</h1>
<p>@ViewData["Title"]</p>
@if (Model.ShowRequestId)
{
    <p>Request ID: @Model.RequestId</p>
}
```

---

## Cuándo elegir Razor Pages

| Escenario | Razor Pages | MVC |
|-----------|-------------|-----|
| Formulario simple | ✅ Natural | ⬜ Overhead |
| CRUD de una entidad | ✅ Page por operación | ⬜ Controller + varias Views |
| Dashboard con widgets | ✅ Varios ViewComponents | ⬜ Un Controller |
| Múltiples acciones en misma URL | ⬜ Posible pero no idiomático | ✅ Natural |
| API sin vistas | ❌ No usar | ✅ Controllers / Minimal API |
| Contenido SEO | ✅ Simple | ⬜ Más archivos |

**Regla**: Para apps web con formularios y contenido → Razor Pages. Para APIs → Minimal API. Para apps con muchas acciones en una ruta → MVC.

---

## Checklist Razor Pages

- [ ] `AddRazorPages()` con convenciones globales de auth
- [ ] Layout consistente con `_ViewStart.cshtml`
- [ ] `_ViewImports.cshtml` con Tag Helpers y namespaces
- [ ] Anti-forgery configurado (viene por defecto en POST)
- [ ] `[BindProperty]` solo en propiedades que reciben input del usuario
- [ ] Validación servidor con `ModelState.IsValid` + reglas de negocio
- [ ] Validación cliente con `_ValidationScriptsPartial`
- [ ] TempData para mensajes post-redirect-get
- [ ] ViewComponents para widgets reutilizables
- [ ] Página de error con `{statusCode?}` parameter
- [ ] Inyección limitada en Views (solo para datos de presentación)
- [ ] No lógica de negocio en PageModel — delegar a servicios
