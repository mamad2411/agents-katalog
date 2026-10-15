---
name: js-jquery
description: "jQuery 4.0 en proyectos legacy ASP.NET MVC. Cubre selectores, AJAX, plugins, Migrate plugin para modernización incremental, cuándo usar jQuery vs vanilla JS, y estrategias de migración a ES Modules. Actívala cuando el proyecto use jQuery (especialmente apps enterprise con 50k+ líneas de Razor + jQuery), al mantener código legacy, o al planear migración a vanilla JS."
---

# JavaScript + jQuery 4.0

Guía de jQuery 4.0 (Ene 2026) para proyectos legacy ASP.NET MVC. jQuery sigue mantenido por OpenJS Foundation.

---

## ¿jQuery o vanilla JS?

| Escenario | Usar |
|-----------|------|
| Proyecto nuevo greenfield (2026) | ✅ Vanilla JS |
| App legacy con 50k+ líneas jQuery + Razor | ✅ jQuery 4.0 (migrar la versión, no reescribir todo) |
| Widget simple en una página Razor | ✅ Vanilla JS |
| Plugin jQuery específico sin equivalente vanilla | ✅ jQuery |
| Selectores complejos, animaciones encadenadas | ✅ jQuery (más conciso) |

---

## Setup en ASP.NET MVC

### Opción 1: Bundle (tradicional)

```csharp
// BundleConfig.cs
bundles.Add(new ScriptBundle("~/bundles/jquery").Include(
    "~/lib/jquery/jquery-4.0.0.min.js"));

bundles.Add(new ScriptBundle("~/bundles/app").Include(
    "~/js/app.js"));
```

```html
<!-- _Layout.cshtml -->
@Scripts.Render("~/bundles/jquery")
@Scripts.Render("~/bundles/app")
```

### Opción 2: Import Map (moderno)

```html
<script type="importmap">
{
  "imports": {
    "jquery": "/lib/jquery/jquery-4.0.0.min.js"
  }
}
</script>
```

---

## Selectores y DOM

```javascript
// ✅ Selectores jQuery (concisos para operaciones batch)
$('.order-row').addClass('highlight');
$('#order-list').find('.cancel-btn').prop('disabled', true);

// ✅ Equivalentes vanilla (modernos, sin dependencia)
document.querySelectorAll('.order-row').forEach(el => el.classList.add('highlight'));
document.querySelectorAll('#order-list .cancel-btn').forEach(btn => btn.disabled = true);

// ✅ Encadenamiento jQuery (legible para flujos largos)
$('#order-table')
  .find('tr.selected')
  .addClass('processing')
  .slideUp(300, function() {
    $(this).remove();
  });
```

---

## AJAX con jQuery

```javascript
// ✅ $.ajax tradicional (proyectos legacy)
$.ajax({
  url: '/api/orders',
  method: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({ customerId: 'CUST-001', amount: 150 }),
  success: function(order) {
    showSuccess('Orden creada');
  },
  error: function(xhr) {
    showError(xhr.responseJSON?.message || 'Error');
  }
});

// ✅ $.post / $.get (atajos)
$.get('/api/orders', { customerId: 'CUST-001' }, function(orders) {
  renderOrderList(orders);
});

$.post('/api/orders', { customerId: 'CUST-001', amount: 150 }, function(order) {
  showSuccess('Orden #' + order.orderNumber);
}, 'json');

// ✅ Anti-forgery token en AJAX (ASP.NET MVC)
$.ajaxSetup({
  beforeSend: function(xhr) {
    xhr.setRequestHeader('RequestVerificationToken',
      $('input[name="__RequestVerificationToken"]').val());
  }
});
```

---

## Plugins jQuery comunes en enterprise

```javascript
// ✅ DataTables (tablas con sorting, filtros, paginación — muy usado en MVC)
$('#orders-table').DataTable({
  ajax: '/api/orders',
  columns: [
    { data: 'orderNumber' },
    { data: 'customerId' },
    { data: 'status' },
    { data: 'totalAmount', render: $.fn.dataTable.render.number(',', '.', 2, '$') },
  ],
  serverSide: true,
  processing: true,
});

// ✅ Select2 (dropdowns con búsqueda)
$('.customer-select').select2({
  ajax: {
    url: '/api/customers/lookup',
    dataType: 'json',
    delay: 250,
  },
});

// ✅ jQuery Validation (validación de formularios)
$('#order-form').validate({
  rules: {
    customerId: { required: true, minlength: 1 },
    amount: { required: true, number: true, min: 0.01 },
  },
  messages: {
    customerId: 'El cliente es requerido',
    amount: { required: 'El monto es requerido', min: 'Debe ser positivo' },
  },
});
```

---

## Migrar de jQuery a vanilla JS

### Estrategia incremental

```
Fase 1: Actualizar jQuery 1.x/2.x/3.x → jQuery 4.0 + Migrate plugin
  ↓ (sin cambios de código, solo actualizar versión)
Fase 2: Identificar usos simples de jQuery y reemplazar por vanilla
  ↓ $(selector) → querySelector, $.ajax → fetch, $.each → forEach
Fase 3: Migrar plugins jQuery a alternativas vanilla o mantener
  ↓ DataTables → gridjs, Select2 → Tom Select, Datepicker → input[type="date"]
Fase 4: Adoptar ES Modules
  ↓ <script src="..."> → <script type="module" src="...">
```

### Tabla de migración jQuery → vanilla

| jQuery | Vanilla JS |
|--------|-----------|
| `$('.foo')` | `document.querySelectorAll('.foo')` |
| `$('.foo').hide()` | `el.style.display = 'none'` |
| `$('.foo').addClass('bar')` | `el.classList.add('bar')` |
| `$.ajax({ url, method, data })` | `fetch(url, { method, body })` |
| `$.getJSON(url, callback)` | `fetch(url).then(r => r.json()).then(callback)` |
| `$(document).ready(fn)` | `document.addEventListener('DOMContentLoaded', fn)`  o `<script defer>` |
| `$.each(arr, fn)` | `arr.forEach(fn)` |
| `$.extend({}, a, b)` | `{ ...a, ...b }` |
| `$el.on('click', fn)` | `el.addEventListener('click', fn)` |
| `$el.attr('data-id')` | `el.dataset.id` |

---

## jQuery Migrate plugin

```html
<!-- Cargar después de jQuery, antes de tu código -->
<script src="/lib/jquery/jquery-migrate-4.0.0.min.js"></script>
```

El plugin advierte en consola sobre APIs deprecadas. Usarlo en desarrollo para encontrar qué APIs de jQuery 1.x/2.x/3.x ya no existen en 4.0.

---

## Buenas prácticas jQuery

```javascript
// ✅ Cachear selectores (evitar re-query)
const $table = $('#orders-table');
$table.find('tr').addClass('highlight');
// ❌ $('#orders-table').find('tr').addClass('highlight');
// ❌ $('#orders-table tr').addClass('highlight');

// ✅ Delegación con .on() (elementos dinámicos)
$('#order-list').on('click', '.cancel-btn', function() {
  const orderId = $(this).data('order-id');
  cancelOrder(orderId);
});

// ✅ Promises con $.ajax (jQuery 3+)
$.ajax({ url: '/api/orders' })
  .done(renderOrders)
  .fail(showError)
  .always(hideSpinner);

// ✅ No mezclar jQuery con vanilla sin criterio
// Si un módulo ya usa vanilla, mantenlo vanilla. Si usa jQuery, mantenlo jQuery.
// No hagas $(vanillaElement) para usar un solo método jQuery.
```

---

## Checklist jQuery legacy

- [ ] jQuery 4.0 + Migrate plugin cargados (si el proyecto estaba en 1.x/2.x/3.x)
- [ ] `$.ajaxSetup` con anti-forgery token configurado
- [ ] Plugins actualizados (DataTables, Select2, jQuery Validation)
- [ ] Selectores cacheados en variables (evitar re-query del DOM)
- [ ] Delegación de eventos con `.on()` para contenido dinámico
- [ ] Plan de migración a vanilla definido (fases, prioridad)
- [ ] Sin mezclar `$` con `querySelector` en el mismo módulo sin criterio
