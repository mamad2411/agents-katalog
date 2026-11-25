---
name: js-testing
description: "Testing de JavaScript vanilla en el navegador y con Node. Cubre testing manual con console.assert, testing automatizado con Vitest + jsdom, testing de componentes vanilla (fetch mock, eventos, DOM assertions), y testing de módulos ES. Actívala al escribir tests para código vanilla JS, configurar un entorno de testing, o agregar pruebas a módulos existentes."
disable-model-invocation: true
---

# JavaScript Testing (Vanilla)

Guía de testing para JavaScript sin framework. Desde asserts manuales hasta Vitest + jsdom.

---

## Testing manual con console.assert

```javascript
// ✅ Rápido para validar durante desarrollo (sin instalar nada)
function sum(a, b) { return a + b; }

console.assert(sum(2, 3) === 5, 'sum(2,3) should be 5');
console.assert(sum(-1, 1) === 0, 'sum(-1,1) should be 0');
console.assert(sum(0, 0) === 0, 'sum(0,0) should be 0');

// Si falla, imprime en consola
```

---

## Vitest + jsdom (recomendado)

```bash
npm init -y
npm install -D vitest jsdom
```

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
```

> **Cuando el layout/CSS real importa:** jsdom no renderiza layout, no aplica CSSOM real, y no soporta `IntersectionObserver`/`ResizeObserver` completos. Para tests donde el posicionamiento, dimensiones, visibilidad o comportamiento CSS son parte de lo que se prueba, usa **Vitest Browser Mode** (`@vitest/browser`), que ejecuta los tests en un navegador real vía Playwright o WebdriverIO en vez de simularlo. Es más fiel que jsdom pero más lento — resérvalo para esos casos, y sigue usando jsdom como entorno por defecto para lógica pura y DOM básico.

```javascript
// js/modules/orders/list.js
export function canCancel(status) {
  return ['pending', 'confirmed'].includes(status);
}

export function formatOrderStatus(status) {
  const labels = {
    pending: 'Pendiente',
    confirmed: 'Confirmada',
    shipped: 'Enviada',
    delivered: 'Entregada',
  };
  return labels[status] || status;
}
```

```javascript
// tests/modules/orders/list.test.js
import { describe, it, expect } from 'vitest';
import { canCancel, formatOrderStatus } from '../../../js/modules/orders/list.js';

describe('canCancel', () => {
  it('returns true for pending orders', () => {
    expect(canCancel('pending')).toBe(true);
  });

  it('returns true for confirmed orders', () => {
    expect(canCancel('confirmed')).toBe(true);
  });

  it('returns false for shipped orders', () => {
    expect(canCancel('shipped')).toBe(false);
  });

  it.each(['pending', 'confirmed'])('allows cancellation for %s', (status) => {
    expect(canCancel(status)).toBe(true);
  });
});

describe('formatOrderStatus', () => {
  it('returns Spanish label for known status', () => {
    expect(formatOrderStatus('shipped')).toBe('Enviada');
  });

  it('returns original status for unknown value', () => {
    expect(formatOrderStatus('unknown')).toBe('unknown');
  });
});
```

---

## Testing de funciones que manipulan el DOM

```javascript
// js/components/modal.js
export function showModal(content) {
  const modal = document.createElement('div');
  modal.className = 'modal';
  modal.innerHTML = `
    <div class="modal-content">
      <span class="close-btn">&times;</span>
      <div class="modal-body">${content}</div>
    </div>
  `;
  modal.querySelector('.close-btn').addEventListener('click', () => hideModal(modal));
  document.body.append(modal);
  modal.style.display = 'block';
}

export function hideModal(modal) {
  modal.style.display = 'none';
  modal.remove();
}
```

```javascript
// tests/components/modal.test.js
import { describe, it, expect, beforeAll } from 'vitest';
import { showModal, hideModal } from '../../js/components/modal.js';

describe('showModal', () => {
  it('creates modal element with content', () => {
    showModal('<p>Test content</p>');

    const modal = document.querySelector('.modal');
    expect(modal).not.toBeNull();
    expect(modal.querySelector('.modal-body').textContent).toBe('Test content');
    expect(modal.style.display).toBe('block');
  });

  it('hides modal when close button clicked', () => {
    showModal('<p>Test</p>');
    const modal = document.querySelector('.modal');
    const closeBtn = modal.querySelector('.close-btn');

    closeBtn.click();

    expect(document.querySelector('.modal')).toBeNull();
  });
});
```

---

## Testing de fetch sin llamar al servidor real

```javascript
// js/utils/http.js
export async function fetchOrders(customerId) {
  const res = await fetch(`/api/orders?customerId=${encodeURIComponent(customerId)}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

```javascript
// tests/utils/http.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchOrders } from '../../js/utils/http.js';

// Mock global fetch
global.fetch = vi.fn();

beforeEach(() => {
  vi.clearAllMocks();
});

describe('fetchOrders', () => {
  it('returns parsed JSON on success', async () => {
    const mockOrders = [{ id: '1', status: 'pending' }];
    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockOrders),
    });

    const result = await fetchOrders('CUST-001');

    expect(result).toEqual(mockOrders);
    expect(fetch).toHaveBeenCalledWith('/api/orders?customerId=CUST-001');
  });

  it('throws error on HTTP failure', async () => {
    fetch.mockResolvedValue({
      ok: false,
      status: 500,
    });

    await expect(fetchOrders('CUST-001')).rejects.toThrow('HTTP 500');
  });

  it('encodes special characters in customerId', async () => {
    fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve([]) });

    await fetchOrders('CUST & Co');

    expect(fetch).toHaveBeenCalledWith('/api/orders?customerId=CUST%20%26%20Co');
  });
});
```

---

## Testing de eventos

```javascript
// js/modules/orders/form.js
export function initForm(formSelector) {
  const form = document.querySelector(formSelector);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Guardando...';

    // ...
  });
}
```

```javascript
// tests/modules/orders/form.test.js
import { describe, it, expect, vi } from 'vitest';
import { initForm } from '../../../js/modules/orders/form.js';

describe('initForm', () => {
  it('disables submit button on submit', () => {
    document.body.innerHTML = `
      <form id="test-form">
        <button type="submit">Guardar</button>
      </form>
    `;

    initForm('#test-form');
    const form = document.querySelector('#test-form');
    const btn = form.querySelector('button');

    form.dispatchEvent(new Event('submit', { cancelable: true }));

    expect(btn.disabled).toBe(true);
    expect(btn.textContent).toBe('Guardando...');
  });

  it('does nothing if form not found', () => {
    initForm('#non-existent');
    // No debería lanzar error
  });
});
```

---

## Testing con Node (sin navegador)

```bash
# Para módulos que no tocan el DOM
node --test tests/utils/format.test.js
```

```javascript
// tests/utils/format.test.js
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { formatCurrency } from '../../../js/utils/format.js';

describe('formatCurrency', () => {
  it('formats MXN with 2 decimals', () => {
    assert.strictEqual(formatCurrency(150.5, 'MXN'), '$150.50 MXN');
  });

  it('formats USD with symbol', () => {
    assert.strictEqual(formatCurrency(99.99, 'USD'), '$99.99 USD');
  });

  it('returns empty for zero', () => {
    assert.strictEqual(formatCurrency(0, 'MXN'), '$0.00 MXN');
  });
});
```

---

## Checklist testing

- [ ] Tests unitarios para funciones puras (cálculos, formateo, validación)
- [ ] Mock de `fetch` para no depender del servidor real
- [ ] Tests de componentes DOM con jsdom (crear, modificar, eventos)
- [ ] Tests de integración: flujo completo submit de formulario
- [ ] CI ejecuta `npx vitest run` (sin watch)
- [ ] Nombres de test: `método_escenario_resultadoEsperado`
- [ ] Sin tests acoplados al orden de ejecución
