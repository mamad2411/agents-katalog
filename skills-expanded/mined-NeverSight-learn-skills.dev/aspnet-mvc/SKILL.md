---
name: aspnet-mvc
description: ASP.NET Core MVC y Razor Views. Cubre Controllers, Actions, Views, Razor syntax, Tag Helpers, View Components, Layouts, Partial Views, Areas, ViewData/ViewBag/TempData, routing MVC, validación con DataAnnotations, model binding, y convenciones para aplicaciones MVC. Actívala al construir aplicaciones MVC, migrar desde ASP.NET clásico, o trabajar con Views y controllers.
disable-model-invocation: true
---

# ASP.NET Core MVC

Guía completa de MVC (Model-View-Controller) en ASP.NET Core. Para APIs REST con Controllers, ver `aspnet-web-api`. Para Razor Pages, ver `aspnet-razor-pages`.

---

## Setup

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// MVC con Views
builder.Services.AddControllersWithViews();

// Solo Controllers (API)
builder.Services.AddControllers();

// MVC + Razor Pages (híbrido)
builder.Services.AddControllersWithViews()
                .AddRazorPagesOptions(options => { /* ... */ });

var app = builder.Build();

// Routing MVC por convención
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// Routing por área
app.MapAreaControllerRoute(
    name: "admin",
    areaName: "Admin",
    pattern: "Admin/{controller=Dashboard}/{action=Index}/{id?}");

app.Run();
```

---

## Controllers

### Estructura canónica

```csharp
public class OrdersController : Controller
{
    private readonly IOrderService _orderService;
    private readonly ILogger<OrdersController> _logger;

    public OrdersController(IOrderService orderService, ILogger<OrdersController> logger)
    {
        _orderService = orderService;
        _logger = logger;
    }

    // GET: /Orders
    public async Task<IActionResult> Index(CancellationToken ct)
    {
        var orders = await _orderService.GetAllAsync(ct);
        return View(orders);
    }

    // GET: /Orders/Details/5
    public async Task<IActionResult> Details(int id, CancellationToken ct)
    {
        var order = await _orderService.GetByIdAsync(id, ct);
        if (order is null)
            return NotFound();

        return View(order);
    }

    // GET: /Orders/Create
    public IActionResult Create() => View();

    // POST: /Orders/Create
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CreateOrderViewModel model, CancellationToken ct)
    {
        if (!ModelState.IsValid)
            return View(model);

        var order = await _orderService.CreateAsync(model, ct);
        _logger.LogInformation("Order {OrderId} created", order.Id);

        TempData["SuccessMessage"] = "Order created successfully";
        return RedirectToAction(nameof(Index));
    }

    // POST: /Orders/Delete/5
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        await _orderService.DeleteAsync(id, ct);
        return RedirectToAction(nameof(Index));
    }
}
```

### Atributos útiles

```csharp
[Authorize]                         // Requiere autenticación
[Authorize(Roles = "Admin")]        // Requiere rol
[AllowAnonymous]                    // Excepción a authorize del controller
[Route("custom/path")]              // Ruta custom
[ApiController]                     // APIs REST
[NonController]                     // Excluye de detección automática
[AutoValidateAntiforgeryToken]      // Valida anti-forgery en todos los POST
[RequireHttps]                      // Fuerza HTTPS
[ResponseCache(Duration = 300)]     // Cache de respuesta
[ServiceFilter(typeof(LogActionFilter))] // Aplica filter desde DI
[TypeFilter(typeof(AuditFilter))]   // Aplica filter con DI en sus dependencias
```

### Inyección en Actions

```csharp
// Además del constructor, se puede inyectar por acción
public async Task<IActionResult> Details(
    int id,
    [FromServices] IUserContext userContext, // Solo esta acción
    CancellationToken ct)
{
    // ...
}
```

---

## Views

### Estructura de carpetas

```
Views/
├── _ViewStart.cshtml          # Layout por defecto
├── _ViewImports.cshtml        # @using, @addTagHelper, etc.
├── Shared/
│   ├── _Layout.cshtml         # Layout principal
│   ├── _ValidationScriptsPartial.cshtml
│   ├── _LoginPartial.cshtml
│   ├── _CookieConsentPartial.cshtml
│   ├── Error.cshtml           # Página de error
│   └── NotFound.cshtml
├── Orders/
│   ├── Index.cshtml
│   ├── Details.cshtml
│   ├── Create.cshtml
│   └── Edit.cshtml
└── Home/
    └── Index.cshtml
```

### _ViewStart.cshtml

```razor
@{
    Layout = "_Layout";
}
```

### _ViewImports.cshtml

```razor
@using MiApp.Web
@using MiApp.Web.Models
@using MiApp.Application.Orders
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
@addTagHelper *, MiApp.Web
```

### _Layout.cshtml canónico

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - MiApp</title>
    <link rel="stylesheet" href="~/lib/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
</head>
<body>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" asp-area="" asp-controller="Home" asp-action="Index">MiApp</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" asp-controller="Orders" asp-action="Index">Orders</a>
                    </li>
                </ul>
                <partial name="_LoginPartial" />
            </div>
        </nav>
    </header>

    <main role="main" class="container mt-4">
        @RenderBody()
    </main>

    <footer class="border-top mt-5 pt-3 text-muted text-center">
        &copy; @DateTime.Now.Year - MiApp
    </footer>

    <script src="~/lib/jquery/jquery.min.js"></script>
    <script src="~/lib/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="~/js/site.js" asp-append-version="true"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

---

## Razor Syntax (lo esencial)

```razor
@* Directivas *@
@model OrdersViewModel           @* Modelo tipado de la View *@
@inject IUserContext UserContext  @* Inyección de dependencias *@
@using MiApp.Models               @* Namespace *@
@addTagHelper *, MiApp.Web        @* Tag Helpers *@

@* C# embebido *@
@DateTime.Now.Year                @* Expresión inline *@
@{
    var title = "Orders";         @* Bloque de código *@
    Layout = "_Layout";
}

@* Control flow *@
@if (Model.Orders.Any())
{
    foreach (var order in Model.Orders)
    {
        <partial name="_OrderCard" model="order" />
    }
}
else
{
    <div class="alert alert-info">No orders found</div>
}

@* Switch expression *@
<p class="badge @(order.Status switch
{
    OrderStatus.Pending => "bg-warning",
    OrderStatus.Confirmed => "bg-success",
    OrderStatus.Cancelled => "bg-danger",
    _ => "bg-secondary"
})">
    @order.Status
</p>
```

---

## Tag Helpers (versión Razor de HTML Helpers)

### Tag Helpers integrados

```html
@* Formulario *@
<form asp-controller="Orders" asp-action="Create" method="post">
    <div asp-validation-summary="ModelOnly" class="text-danger"></div>

    <div class="mb-3">
        <label asp-for="CustomerName" class="form-label"></label>
        <input asp-for="CustomerName" class="form-control" />
        <span asp-validation-for="CustomerName" class="text-danger"></span>
    </div>

    <button type="submit" class="btn btn-primary">Create</button>
</form>

@* Links *@
<a asp-controller="Orders" asp-action="Details" asp-route-id="@order.Id">
    View Details
</a>

@* Scripts y CSS con cache busting *@
<link rel="stylesheet" href="~/css/site.css" asp-append-version="true" />
<script src="~/js/site.js" asp-append-version="true"></script>

@* Environment tag *@
<environment include="Development">
    <link rel="stylesheet" href="~/css/debug.css" />
</environment>
<environment exclude="Development">
    <link rel="stylesheet" href="~/css/site.min.css" asp-append-version="true" />
</environment>

@* Cache tag *@
<cache expires-after="@TimeSpan.FromMinutes(5)">
    @await Component.InvokeAsync("RecentOrders")
</cache>
```

### Custom Tag Helper

```csharp
[HtmlTargetElement("email-link")]
public class EmailLinkTagHelper : TagHelper
{
    public string Email { get; set; } = string.Empty;
    public string? Subject { get; set; }

    public override void Process(TagHelperContext context, TagHelperOutput output)
    {
        output.TagName = "a";
        output.Attributes.SetAttribute("href", $"mailto:{Email}?subject={Subject}");
        output.Content.SetContent(Email);
    }
}

// Uso en Razor
// <email-link email="support@miapp.com" subject="Help"></email-link>
```

---

## View Components

```csharp
// Componente
public class OrderSummaryViewComponent : ViewComponent
{
    private readonly IOrderService _orderService;

    public OrderSummaryViewComponent(IOrderService orderService)
        => _orderService = orderService;

    public async Task<IViewComponentResult> InvokeAsync(string customerId)
    {
        var summary = await _orderService.GetSummaryAsync(customerId);
        return View(summary);
    }
}

// Vista: Views/Shared/Components/OrderSummary/Default.cshtml
@model OrderSummary
<div class="card">
    <h5>Orders: @Model.TotalOrders</h5>
    <p>Pending: @Model.PendingCount</p>
    <p>Total Amount: @Model.TotalAmount.ToString("C")</p>
</div>

// Invocar desde cualquier View
@await Component.InvokeAsync("OrderSummary", new { customerId = "CUST-1" })

// O como Tag Helper
<vc:order-summary customer-id="CUST-1"></vc:order-summary>
```

---

## ViewData, ViewBag, TempData

```csharp
// ViewData: diccionario tipado débil. Vive un request.
ViewData["Title"] = "Orders";
// En View: @ViewData["Title"]

// ViewBag: dynamic wrapper de ViewData. Mismo ciclo de vida.
ViewBag.SuccessMessage = "Order created";

// TempData: sobrevive un redirect (usado para mensajes post-redirect-get)
TempData["SuccessMessage"] = "Order created";
// En View: @TempData["SuccessMessage"]

// ✅ Patrón PRG (Post-Redirect-Get) con TempData
[HttpPost]
public async Task<IActionResult> Create(CreateOrderViewModel model, CancellationToken ct)
{
    if (!ModelState.IsValid) return View(model);

    await _orderService.CreateAsync(model, ct);
    TempData["SuccessMessage"] = "Order created successfully";
    return RedirectToAction(nameof(Index));
}

// En Index.cshtml:
@if (TempData["SuccessMessage"] is string msg)
{
    <div class="alert alert-success">@msg</div>
}
```

---

## Áreas

```
Areas/
├── Admin/
│   ├── Controllers/
│   │   ├── DashboardController.cs
│   │   └── OrdersController.cs
│   ├── Views/
│   │   ├── _ViewImports.cshtml
│   │   ├── _ViewStart.cshtml
│   │   ├── Dashboard/
│   │   │   └── Index.cshtml
│   │   └── Orders/
│   │       └── Index.cshtml
│   └── Models/
├── Api/
│   └── Controllers/
│       └── ExternalController.cs
└── Store/
    ├── Controllers/
    └── Views/
```

```csharp
// Program.cs
app.MapAreaControllerRoute(
    name: "admin",
    areaName: "Admin",
    pattern: "Admin/{controller=Dashboard}/{action=Index}/{id?}");

// Controller
[Area("Admin")]
[Authorize(Roles = "Admin")]
public class DashboardController : Controller { ... }

// Link entre áreas y no-áreas
<a asp-area="Admin" asp-controller="Dashboard" asp-action="Index">Admin</a>
<a asp-area="" asp-controller="Home" asp-action="Index">Home</a> @* sin área *@
```

---

## Validación del lado servidor

```csharp
public class CreateOrderViewModel
{
    [Required(ErrorMessage = "Customer name is required")]
    [Display(Name = "Customer Name")]
    [StringLength(100, MinimumLength = 2)]
    public string CustomerName { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    [Display(Name = "Email")]
    public string CustomerEmail { get; set; } = string.Empty;

    [Required]
    [Range(1, 999)]
    public int Quantity { get; set; }

    [Required]
    [CreditCard]
    public string CreditCardNumber { get; set; } = string.Empty;

    // Validación custom a nivel modelo
    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (Quantity > 100 && CustomerEmail.EndsWith("@gmail.com"))
            yield return new ValidationResult(
                "Gmail users cannot order more than 100 items",
                [nameof(Quantity)]);
    }
}
```

### Validación remota

```csharp
[Remote(action: "VerifyEmail", controller: "Validation")]
public string Email { get; set; }

// ValidationController.cs
[AcceptVerbs("GET", "POST")]
public async Task<IActionResult> VerifyEmail(string email)
{
    var exists = await _userService.EmailExistsAsync(email);
    return exists ? Json($"Email {email} is already in use") : Json(true);
}
```

---

## Cuándo usar MVC sobre Razor Pages

| Criterio | MVC | Razor Pages |
|----------|-----|-------------|
| Acciones múltiples por página | ✅ Natural | ⬜ Posible pero no idiomático |
| URLs jerárquicas | ✅ `/{controller}/{action}/{id}` | ⬜ `/{Page}` planas por defecto |
| Equipo migrando de ASP.NET clásico | ✅ Familiar | ⬜ Nuevo paradigma |
| Feature pequeña autocontenida | ⬜ Muchos archivos | ✅ Page + PageModel juntos |
| SEO / contenido estático | ⬜ Overhead | ✅ Más simple |

**Regla pragmática**: MVC para aplicaciones grandes con muchas acciones. Razor Pages para contenido y formularios simples.

---

## Migración desde ASP.NET clásico

```csharp
// ASP.NET clásico → ASP.NET Core
// Request["key"]       → Request.Query["key"] o Request.Form["key"]
// HttpContext.Current   → IHttpContextAccessor
// Server.MapPath()     → IWebHostEnvironment.ContentRootPath
// ConfigurationManager  → IConfiguration / IOptions<T>
// HtmlHelper           → Tag Helpers
// Web.config           → appsettings.json
// Global.asax          → Program.cs + Middleware
// App_Start            → Program.cs
// Bundling             → BuildBundlerMinifier o Webpack/Gulp/Vite
```
