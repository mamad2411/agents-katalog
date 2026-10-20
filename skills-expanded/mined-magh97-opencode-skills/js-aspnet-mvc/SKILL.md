---
name: js-aspnet-mvc
description: "Integración de JavaScript con ASP.NET MVC y Razor. Cubre bundles, sections, anti-forgery tokens en AJAX, ViewBag/ViewData a JS, partial views con AJAX, Import Maps en Razor, y convenciones de wwwroot. Actívala en proyectos ASP.NET MVC + vanilla JS o jQuery, al implementar AJAX con Razor, o al migrar scripts a módulos ES."
disable-model-invocation: true
---

# JavaScript + ASP.NET MVC Integration

Guía de integración entre JavaScript y ASP.NET MVC. Razor views, bundles, anti-forgery, partial views.

---

## Pasar datos del servidor al cliente

```csharp
// ❌ Inyectar JSON manualmente en <script>
// ❌ <script>var orders = @Html.Raw(Json.Encode(Model.Orders));</script>

// ✅ data-attributes en HTML (preferido)
<div id="order-list"
     data-customer-id="@Model.CustomerId"
     data-base-url="@Url.Action("Index", "Orders")">
</div>
```

```javascript
const list = document.querySelector('#order-list');
const customerId = list.dataset.customerId;
const baseUrl = list.dataset.baseUrl;
```

```csharp
// ✅ Serializar a JSON en un elemento oculto (para datos complejos)
<div id="order-data" type="application/json" style="display:none">
  @Json.Serialize(Model.Orders)
</div>
```

```javascript
const orders = JSON.parse(document.querySelector('#order-data').textContent);
```

---

## URLs de ASP.NET MVC en JavaScript

```csharp
// ❌ URLs hardcodeadas
// ❌ fetch('/Orders/Details/123')

// ✅ @Url.Action() en data-attributes
<a href="#" class="detail-link"
   data-url="@Url.Action("Details", "Orders", new { id = item.Id })">
   Ver detalle
</a>
```

```javascript
document.querySelectorAll('.detail-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const url = link.dataset.url;  // /Orders/Details/123
    fetch(url).then(r => r.text()).then(html => {
      document.querySelector('#detail-panel').innerHTML = html;
    });
  });
});
```

---

## Anti-forgery tokens (CSRF)

```html
<!-- _Layout.cshtml — el formulario global genera el token -->
@Html.AntiForgeryToken()
```

```javascript
// ✅ Incluir token en fetch POST
async function postJson(url, data) {
  const token = document.querySelector('input[name="__RequestVerificationToken"]')?.value;
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['RequestVerificationToken'] = token;

  const res = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ✅ jQuery: configurar globalmente
$.ajaxSetup({
  beforeSend: function(xhr) {
    const token = $('input[name="__RequestVerificationToken"]').val();
    if (token) xhr.setRequestHeader('RequestVerificationToken', token);
  }
});

// ✅ FormData (el token se incluye automáticamente si está en el <form>)
const formData = new FormData(document.querySelector('#order-form'));
// El input[name="__RequestVerificationToken"] va incluido en FormData
await fetch('/Orders/Create', { method: 'POST', body: formData });
```

---

## Bundles y sections en Razor

```html
<!-- _Layout.cshtml -->
@Scripts.Render("~/bundles/jquery")
@Scripts.Render("~/bundles/bootstrap")
@RenderSection("scripts", required: false)
```

```html
<!-- Views/Orders/Index.cshtml -->
@section scripts {
  @Scripts.Render("~/bundles/orders")
  <script>
    // Script inline específico de esta página
    OrderList.init('@Model.CustomerId');
  </script>
}
```

### Migrar de bundles a ES Modules

```html
<!-- _Layout.cshtml — reemplazar @Scripts.Render con type="module" -->
<script type="module" src="/js/app.js"></script>

<!-- Páginas específicas cargan sus módulos bajo demanda -->
<script type="module">
  import { initOrderList } from '/js/modules/orders/list.js';
  initOrderList('@Model.CustomerId');
</script>
```

---

## Partial views cargadas con AJAX

```csharp
// OrdersController.cs
public async Task<IActionResult> Details(string id)
{
    var order = await _orderService.GetByIdAsync(id);
    if (order == null) return NotFound();
    return PartialView("_OrderDetail", order);  // Retorna solo el HTML de la partial
}
```

```javascript
// Cargar partial view y mostrarla en un modal
async function loadOrderDetail(orderId) {
  const url = `/Orders/Details/${orderId}`;
  const res = await fetch(url, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }  // Para que el controller detecte AJAX
  });
  if (!res.ok) {
    showError('Orden no encontrada');
    return;
  }
  const html = await res.text();
  document.querySelector('#modal-body').innerHTML = html;
  showModal();
}
```

---

## Import Maps en Razor

```html
<!-- _Layout.cshtml -->
<script type="importmap">
{
  "imports": {
    "utils/": "/js/utils/",
    "orders/": "/js/modules/orders/",
    "catalog/": "/js/modules/catalog/"
  }
}
</script>
<script type="module" src="/js/app.js"></script>
```

```javascript
// js/modules/orders/list.js
import { fetchJson } from 'utils/http.js';  // Resuelto por Import Map
import { showModal } from 'utils/dom.js';
```

---

## Convenciones wwwroot

```
wwwroot/
├── js/
│   ├── app.js                  # Entry point
│   ├── modules/                # Módulos de negocio
│   │   ├── orders/
│   │   │   ├── list.js
│   │   │   └── form.js
│   │   └── catalog/
│   ├── utils/                  # Helpers reutilizables
│   │   ├── http.js
│   │   ├── dom.js
│   │   └── validation.js
│   └── components/             # Componentes UI reusables
│       ├── modal.js
│       └── toast.js
├── css/
│   └── site.css
├── lib/                        # Librerías de terceros (no npm)
│   ├── jquery/
│   └── datatables/
└── images/
```

---

## Checklist ASP.NET MVC + JS

- [ ] Anti-forgery token incluido en todos los POST vía AJAX
- [ ] URLs generadas con `@Url.Action()`, no hardcodeadas
- [ ] Datos del servidor pasados vía `data-attributes`, no `<script>` inline
- [ ] Bundles cargados en orden correcto (jQuery antes de plugins)
- [ ] Scripts específicos de página en `@section scripts`
- [ ] Partial views cargadas con `X-Requested-With: XMLHttpRequest`
- [ ] `wwwroot/` organizado por módulo, no por tipo de archivo
- [ ] Import Maps evaluados como reemplazo de bundles para módulos ES
