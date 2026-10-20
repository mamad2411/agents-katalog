---
name: js-patterns
description: "Patrones de JavaScript vanilla en el navegador. Cubre IIFE, Revealing Module, ES Modules nativos, namespaces, organización de archivos en wwwroot, incremental modernization (vanilla → módulos → Vite), y patrones de inicialización por página. Actívala al organizar código JavaScript en proyectos ASP.NET MVC sin bundler o al definir la estructura de wwwroot."
disable-model-invocation: true
---

# JavaScript Patterns (Navegador)

Guía de patrones de organización de código JavaScript vanilla. Sin bundler, sin framework.

---

## Evolución de patrones

```
2008: IIFE + globales         ← jQuery plugins, todo en window
2015: Revealing Module        ← Encapsulación sin ES Modules
2020: ES Modules nativos      ← import/export en navegador
2026: ES Modules + Import Map ← El estándar actual
```

---

## IIFE (Immediately Invoked Function Expression)

```javascript
// ✅ Encapsula scope, compatible con todos los navegadores
var Orders = (function() {
  // Variables privadas
  var apiUrl = '/api/orders';
  var cache = {};

  // Función privada
  function buildUrl(params) {
    return apiUrl + '?' + new URLSearchParams(params).toString();
  }

  // API pública
  return {
    getList: async function(filters) {
      var res = await fetch(buildUrl(filters));
      return res.json();
    },
    clearCache: function() {
      cache = {};
    }
  };
})();

// Uso
Orders.getList({ status: 'pending' }).then(renderTable);
```

---

## Revealing Module Pattern

```javascript
// ✅ Más legible: define todo arriba, revela lo público al final
var OrderForm = (function() {
  var form = null;
  var isSubmitting = false;

  function init(selector) {
    form = document.querySelector(selector);
    if (!form) return;
    form.addEventListener('submit', handleSubmit);
  }

  function reset() {
    if (form) form.reset();
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (isSubmitting) return;
    isSubmitting = true;
    // ...
  }

  // Revelar API pública
  return {
    init: init,
    reset: reset,
  };
})();

// Inicializar en la página
OrderForm.init('#order-form');
```

---

## Campos/métodos privados de clase (alternativa moderna a IIFE)

Cuando el código ya usa clases, los campos y métodos privados (`#privado`, ES2022, baseline) dan encapsulación real sin necesidad de IIFE ni de migrar a módulos:

```javascript
class OrderForm {
  #form = null;          // privado: inaccesible fuera de la clase
  #isSubmitting = false;

  init(selector) {
    this.#form = document.querySelector(selector);
    this.#form?.addEventListener('submit', (e) => this.#handleSubmit(e));
  }

  #handleSubmit(e) { /* privado, no expuesto en la API pública */ }
}
```

---

## ES Modules nativos

```javascript
// js/modules/orders/list.js
import { fetchJson } from '../../utils/http.js';
import { showModal } from '../../components/modal.js';
import { formatCurrency } from '../../utils/format.js';

// Variables privadas del módulo (no exportadas)
let currentPage = 1;
let currentFilters = {};

// Export público
export function init(containerId) {
  const container = document.querySelector(containerId);
  if (!container) return;
  loadOrders();
}

export function refresh() {
  currentPage = 1;
  loadOrders();
}

async function loadOrders() {
  const data = await fetchJson('/api/orders?' + new URLSearchParams({
    page: currentPage,
    ...currentFilters,
  }));
  renderOrders(data);
}

function renderOrders(data) {
  // ...
}
```

```javascript
// js/app.js — entry point
import { init as initOrderList } from './modules/orders/list.js';
import { init as initOrderForm } from './modules/orders/form.js';
import { init as initCatalog } from './modules/catalog/search.js';

document.addEventListener('DOMContentLoaded', () => {
  initOrderList('#order-list');
  initOrderForm('#order-form');
  initCatalog('#catalog-search');
});
```

---

## Inicialización por página

```javascript
// js/app.js — patrón de inicialización selectiva
import { init as initOrderList } from './modules/orders/list.js';
import { init as initOrderForm } from './modules/orders/form.js';
import { init as initDashboard } from './modules/dashboard/charts.js';

// Mapa de selectores → inicializadores
const pages = {
  '#order-list': initOrderList,
  '#order-form': initOrderForm,
  '#dashboard-charts': initDashboard,
};

document.addEventListener('DOMContentLoaded', () => {
  for (const [selector, initFn] of Object.entries(pages)) {
    if (document.querySelector(selector)) {
      initFn(selector);
    }
  }
});
// Solo se ejecuta el código de la página actual, no todo.
```

---

## Namespaces globales (transición)

```javascript
// js/app.js
// Namespace global para evitar colisiones
window.App = window.App || {};

window.App.Orders = {
  List: OrderListModule,
  Form: OrderFormModule,
};

window.App.Utils = {
  Http: HttpUtils,
  Format: FormatUtils,
};

// Las páginas Razor pueden llamar:
// App.Orders.List.init('#order-list');
```

---

## Incremental modernization

### Fase 1: Todo en bundles

```
wwwroot/js/
├── app.js              (todo mezclado, globales)
├── orders.js
├── catalog.js
└── utils.js
```

### Fase 2: Módulos IIFE con namespaces

```
wwwroot/js/
├── app.js
├── modules/
│   ├── orders.js       (var Orders = (function() { ... })())
│   └── catalog.js
└── utils/
    └── http.js
```

### Fase 3: ES Modules con type="module"

```
wwwroot/js/
├── app.js              (entry point, type="module")
├── modules/
│   ├── orders/
│   │   ├── list.js     (export function init)
│   │   └── form.js
│   └── catalog/
├── utils/
│   ├── http.js
│   └── format.js
└── components/
    └── modal.js
```

### Fase 4: Vite + npm (si el proyecto crece)

```bash
npm create vite@latest miapp-web -- --template vanilla
# Mover wwwroot/js/ → src/
# Agregar vite.config.js con proxy al backend ASP.NET
```

---

## Comunicación entre módulos

```javascript
// ✅ Custom events (desacoplado)
// Módulo 1: orders/form.js
const event = new CustomEvent('order:created', {
  detail: { orderId: '123', customerId: 'CUST-001' },
  bubbles: true,
});
document.dispatchEvent(event);

// Módulo 2: dashboard/stats.js (reacciona sin conocer al módulo 1)
document.addEventListener('order:created', (e) => {
  updateCustomerStats(e.detail.customerId);
});

// ✅ Event bus simple (alternativa a CustomEvents)
window.App = window.App || {};
window.App.EventBus = {
  _listeners: {},
  on(event, fn) {
    (this._listeners[event] = this._listeners[event] || []).push(fn);
  },
  emit(event, data) {
    (this._listeners[event] || []).forEach(fn => fn(data));
  },
};

App.EventBus.on('order:created', ({ orderId }) => {
  refreshOrderList();
});
App.EventBus.emit('order:created', { orderId: '123' });
```

---

## Checklist patterns

- [ ] ES Modules (`type="module"`) para código nuevo
- [ ] IIFE/Revealing Module para código legacy que no puede migrarse aún
- [ ] Campos/métodos privados de clase (`#privado`) si el código ya usa clases
- [ ] Un entry point (`app.js`) que inicializa solo lo necesario para la página actual
- [ ] Custom events para comunicación entre módulos (sin acoplarlos)
- [ ] `wwwroot/js/` organizado por módulo, no por tipo de archivo
- [ ] Plan de modernización incremental definido (fases, prioridades)
- [ ] Sin variables globales (usar módulos o namespaces)
- [ ] Dynamic `import()` para código que no se necesita al cargar la página
