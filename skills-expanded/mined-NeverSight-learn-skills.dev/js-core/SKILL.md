---
name: js-core
description: "Guía principal de JavaScript vanilla en el navegador (ES6+). Cubre selectores DOM modernos, fetch API, eventos, ES Modules nativos (type=\"module\"), async/await, FormData, templates, localStorage, MutationObserver, y APIs del navegador. Actívala para cualquier tarea de JavaScript vanilla, especialmente en proyectos ASP.NET MVC + Razor sin bundler ni framework SPA. Las sub-skills del kit profundizan en dominios específicos."
---

# JavaScript Vanilla Core (Navegador)

Guía canónica de JavaScript en el navegador sin frameworks ni bundlers. ES6+ nativo, todos los navegadores modernos lo soportan.

---

## DOM — Selectores y manipulación

```javascript
// ✅ querySelector / querySelectorAll — el estándar 2026 (55.8% del código analizado)
const form = document.querySelector('#order-form');
const rows = document.querySelectorAll('.order-row');
const submitBtn = document.querySelector('button[type="submit"]');

// ✅ Manipulación
const article = document.createElement('article');
article.className = 'order-card';
article.innerHTML = `<h3>Orden #${order.orderNumber}</h3>`;
document.querySelector('#order-list').append(article);

// ✅ Templates (HTML nativo, sin librería)
const template = document.querySelector('#order-card-template');
const clone = template.content.cloneNode(true);
clone.querySelector('.order-number').textContent = order.orderNumber;
document.querySelector('#order-list').append(clone);
```

```html
<template id="order-card-template">
  <article class="order-card">
    <h3 class="order-number"></h3>
    <span class="status"></span>
  </article>
</template>
```

---

## Eventos

```javascript
// ✅ addEventListener (nunca onclick inline)
document.querySelector('#save-btn').addEventListener('click', handleSave);

// ✅ Delegación de eventos (un listener para elementos dinámicos)
document.querySelector('#order-list').addEventListener('click', (e) => {
  const btn = e.target.closest('.cancel-btn');
  if (btn) {
    const orderId = btn.dataset.orderId;
    cancelOrder(orderId);
  }
});

// ✅ Eventos de formulario
form.addEventListener('submit', handleSubmit);
input.addEventListener('input', handleChange);
select.addEventListener('change', handleSelect);

// ✅ Teclado
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    saveForm();
  }
});

// ✅ Custom events (comunicación entre módulos)
const event = new CustomEvent('order:created', {
  detail: { orderId: '123', customerId: 'CUST-001' },
  bubbles: true,
});
document.dispatchEvent(event);

// Escuchar
document.addEventListener('order:created', (e) => {
  refreshOrderList();
  updateStats(e.detail.customerId);
});
```

---

## Fetch API (reemplaza XMLHttpRequest)

```javascript
// ✅ GET
async function getOrders(customerId) {
  const res = await fetch(`/api/orders?customerId=${encodeURIComponent(customerId)}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ✅ POST con JSON
async function createOrder(data) {
  const res = await fetch('/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message);
  }
  return res.json();
}

// ✅ POST con FormData (formularios, archivos)
async function submitForm(formElement) {
  const formData = new FormData(formElement);
  const res = await fetch('/api/orders', {
    method: 'POST',
    body: formData,  // No pongas Content-Type, el navegador lo agrega con boundary
  });
  return res.json();
}

// ✅ AbortController (cancelar peticiones)
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const res = await fetch('/api/orders', { signal: controller.signal });
} catch (err) {
  if (err.name === 'AbortError') console.log('Timeout');
} finally {
  clearTimeout(timeout);
}

// ✅ Subida de archivos con progreso (XMLHttpRequest aún necesario para progress)
function uploadFile(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/upload');

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) resolve(JSON.parse(xhr.response));
      else reject(new Error(`Upload failed: ${xhr.status}`));
    });

    xhr.addEventListener('error', () => reject(new Error('Network error')));

    const formData = new FormData();
    formData.append('file', file);
    xhr.send(formData);
  });
}
```

---

## ES Modules nativos (sin bundler)

```html
<!-- Layout.cshtml -->
<script type="module" src="/js/app.js"></script>
```

```javascript
// js/app.js — punto de entrada
import { initOrderList } from './modules/orders/list.js';
import { initOrderForm } from './modules/orders/form.js';

document.addEventListener('DOMContentLoaded', () => {
  initOrderList();
  initOrderForm();
});
```

```javascript
// js/modules/orders/list.js
import { fetchJson } from '../utils/http.js';

export function initOrderList() {
  const table = document.querySelector('#orders-table');
  if (!table) return;

  // ...
}

// js/modules/utils/http.js
export async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

### Import Maps (para naming clean sin paths relativos)

```html
<script type="importmap">
{
  "imports": {
    "utils/": "/js/utils/",
    "orders/": "/js/modules/orders/"
  }
}
</script>
```

```javascript
import { fetchJson } from 'utils/http.js';  // Sin ../../../utils/http.js
import { initOrderForm } from 'orders/form.js';
```

---

## APIs del navegador útiles

```javascript
// ✅ MutationObserver (reaccionar a cambios en el DOM)
const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    if (mutation.type === 'childList') {
      mutation.addedNodes.forEach(node => {
        if (node.matches?.('.dynamic-row')) {
          attachRowListeners(node);
        }
      });
    }
  }
});
observer.observe(document.querySelector('#dynamic-list'), { childList: true, subtree: true });

// ✅ IntersectionObserver (lazy loading, infinite scroll)
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;  // Cargar imagen real
      io.unobserve(img);
    }
  });
}, { rootMargin: '100px' });  // Cargar 100px antes de que sea visible
document.querySelectorAll('img[data-src]').forEach(img => io.observe(img));

// ✅ ResizeObserver
const resizeObserver = new ResizeObserver((entries) => {
  for (const entry of entries) {
    console.log('Element resized:', entry.contentRect.width, entry.contentRect.height);
  }
});
resizeObserver.observe(document.querySelector('#chart-container'));

// ✅ localStorage (datos simples)
localStorage.setItem('filters', JSON.stringify({ status: 'pending', page: 2 }));
const filters = JSON.parse(localStorage.getItem('filters') || '{}');

// ✅ sessionStorage (datos de sesión)
sessionStorage.setItem('currentOrder', JSON.stringify(order));

// ✅ History API (SPA-like navigation sin framework)
history.pushState({ page: 'orders' }, '', '/orders');
window.addEventListener('popstate', (e) => {
  if (e.state?.page === 'orders') loadOrdersPage();
});
```

---

## Convenciones de código

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Archivos | `kebab-case.js` | `order-list.js`, `http-utils.js` |
| Funciones | `camelCase` | `getOrders()`, `handleSubmit()` |
| Variables | `camelCase` | `orderId`, `customerName` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_FILE_SIZE`, `API_BASE_URL` |
| Clases (raras) | `PascalCase` | `OrderService`, `EventBus` |
| IDs en HTML | `kebab-case` | `order-form`, `cancel-btn` |
| Data attributes | `data-kebab-case` | `data-order-id`, `data-customer-name` |

### Estructura de proyecto (wwwroot)

```
wwwroot/
├── js/
│   ├── app.js                  # Entry point (type="module")
│   ├── modules/
│   │   ├── orders/
│   │   │   ├── list.js         # Tabla de órdenes
│   │   │   ├── form.js         # Formulario crear/editar
│   │   │   └── detail.js       # Modal detalle
│   │   └── catalog/
│   │       └── search.js
│   ├── utils/
│   │   ├── http.js             # fetch wrapper
│   │   ├── dom.js              # Helpers DOM
│   │   └── validation.js       # Validación de formularios
│   └── components/
│       ├── modal.js
│       ├── toast.js
│       └── dropdown.js
├── css/
│   └── site.css
└── lib/
    └── jquery/                 # Si se usa jQuery (ver js-jquery)
```

---

## Reglas de oro

1. **`querySelector` sobre `getElementById`.** Es el estándar 2026.
2. **`fetch()` sobre `XMLHttpRequest`.** Excepto para progress de upload.
3. **ES Modules (`type="module"`) sobre `<script>` sueltos.** Scope limpio, sin globales.
4. **`addEventListener` sobre `onclick` inline.** Separación de responsabilidades.
5. **Delegación de eventos sobre listeners por elemento.** Un listener en el padre para N hijos dinámicos.
6. **`FormData` para formularios.** Serializa campos y archivos automáticamente.
7. **`AbortController` para cancelar fetch.** Evita race conditions en sugerencias/búsquedas.
8. **Nada de `eval()`, `with`, o `==` sin triple igual.**
9. **Data attributes (`dataset`) sobre clases CSS para datos.** `btn.dataset.orderId`, no `btn.className.includes`.
10. **`MutationObserver`/`IntersectionObserver` sobre polling.** APIs nativas, eficientes.

---

## Sub-skills del kit

| Skill | Cuándo cargarla |
|-------|-----------------|
| `js-jquery` | jQuery 4.0 en proyectos legacy ASP.NET MVC, migración incremental |
| `js-aspnet-mvc` | Integración con Razor, anti-forgery, bundles, ViewBag a JS |
| `js-forms` | Formularios, validación HTML5 + Constraint Validation API, file upload |
| `js-security` | XSS, CSRF, CSP, sanitización, secure storage |
| `js-performance` | DOM batching, debounce/throttle, IntersectionObserver, bundle optimization |
| `js-patterns` | IIFE, Revealing Module, ES Modules, organización de código |
| `js-testing` | Testing vanilla JS en el navegador y con Node |
