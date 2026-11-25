---
name: js-performance
description: "Rendimiento en JavaScript vanilla en el navegador. Cubre DOM batching (lecturas separadas de escrituras), debounce/throttle, IntersectionObserver para lazy loading, requestAnimationFrame, event delegation, memory leaks (listeners huérfanos), y bundle optimization (minificación, tree shaking con ES Modules). Actívala al optimizar páginas lentas, reducir re-renders, o mejorar Core Web Vitals."
---

# JavaScript Performance (Navegador)

Guía de rendimiento en el frontend vanilla JS. Optimizar Core Web Vitals sin framework.

---

## DOM Batching — lecturas y escrituras separadas

```javascript
// ❌ Layout thrashing: lectura → escritura → lectura → escritura
elements.forEach(el => {
  const height = el.offsetHeight;  // Lectura (fuerza reflow)
  el.style.height = height + 10 + 'px';  // Escritura (invalida layout)
  const width = el.offsetWidth;  // Lectura (fuerza reflow de nuevo)
  el.style.width = width + 10 + 'px';  // Escritura
});

// ✅ Batch: todas las lecturas primero, luego todas las escrituras
const heights = elements.map(el => el.offsetHeight);  // Solo lecturas
const widths = elements.map(el => el.offsetWidth);

elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';  // Solo escrituras
  el.style.width = widths[i] + 10 + 'px';
});

// ✅ requestAnimationFrame para escrituras (se alinea con el repaint)
requestAnimationFrame(() => {
  elements.forEach((el, i) => {
    el.style.transform = `translateY(${i * 50}px)`;
  });
});
```

---

## Debounce y Throttle

```javascript
// ✅ Debounce: esperar a que el usuario termine de escribir (búsquedas)
function debounce(fn, delay = 300) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

searchInput.addEventListener('input', debounce(async (e) => {
  const results = await fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`);
  renderResults(results);
}, 300));

// ✅ Throttle: ejecutar máximo 1 vez cada X ms (scroll, resize)
function throttle(fn, limit = 100) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

window.addEventListener('scroll', throttle(() => {
  updateScrollIndicator(window.scrollY);
}, 100));
```

---

## IntersectionObserver — Lazy Loading

```javascript
// ✅ Lazy load de imágenes
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;           // Cargar imagen real
      img.srcset = img.dataset.srcset;     // Responsive images
      img.classList.remove('lazy');
      imageObserver.unobserve(img);
    }
  });
}, {
  rootMargin: '200px',  // Cargar 200px antes de que sea visible
});

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});
```

```html
<img data-src="/images/product-large.jpg"
     data-srcset="/images/product-small.jpg 400w, /images/product-large.jpg 800w"
     src="data:image/svg+xml,..."  <!-- placeholder inline -->
     class="lazy"
     alt="Producto">
```

```javascript
// ✅ Infinite scroll
const sentinel = document.querySelector('#scroll-sentinel');
const scrollObserver = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting && !isLoading) {
    isLoading = true;
    page++;
    const items = await fetchPage(page);
    appendItems(items);
    isLoading = false;
  }
});
scrollObserver.observe(sentinel);
```

---

## Event delegation

```javascript
// ❌ Listener por cada fila (1000 listeners = 1000 en memoria)
document.querySelectorAll('.order-row').forEach(row => {
  row.addEventListener('click', handleRowClick);
});

// ✅ Un listener en el padre para N hijos (1 listener)
document.querySelector('#order-list').addEventListener('click', (e) => {
  const row = e.target.closest('.order-row');
  if (!row) return;

  if (e.target.closest('.cancel-btn')) {
    cancelOrder(row.dataset.orderId);
  } else {
    showOrderDetail(row.dataset.orderId);
  }
});
```

---

## Memory leaks — prevención

```javascript
// ❌ Listeners en elementos que se eliminan del DOM
function createModal() {
  const modal = document.createElement('div');
  document.body.append(modal);

  document.addEventListener('keydown', handleEscape);  // ❌ Nunca se remueve

  modal.remove();  // El listener sigue en memoria
}

// ✅ Remover listeners cuando el elemento sale del DOM
function createModal() {
  const modal = document.createElement('div');
  document.body.append(modal);

  function handleEscape(e) {
    if (e.key === 'Escape') {
      closeModal(modal);
      document.removeEventListener('keydown', handleEscape);  // ✅ Limpiar
    }
  }

  document.addEventListener('keydown', handleEscape);
}

// ✅ AbortController para fetch (evita race conditions)
let controller;

async function search(query) {
  controller?.abort();  // Cancelar búsqueda anterior
  controller = new AbortController();

  try {
    const res = await fetch(`/api/search?q=${query}`, {
      signal: controller.signal,
    });
    return res.json();
  } catch (err) {
    if (err.name === 'AbortError') return;  // Cancelado, ignorar
    throw err;
  }
}

// ✅ WeakMap para datos asociados a elementos DOM (se limpian solos)
const elementData = new WeakMap();
elementData.set(rowElement, { orderId: '123' });
// Cuando rowElement se elimina del DOM y no hay referencias → GC lo limpia
```

---

## requestAnimationFrame para animaciones

```javascript
// ❌ setInterval para animaciones (no sincronizado con el monitor)
setInterval(() => {
  element.style.left = (parseInt(element.style.left) || 0) + 1 + 'px';
}, 16);  // ~60fps pero no sincronizado

// ✅ requestAnimationFrame (sincronizado con el refresh del monitor)
function animate(element, startTime) {
  const elapsed = Date.now() - startTime;
  element.style.transform = `translateX(${Math.min(elapsed / 10, 200)}px)`;

  if (elapsed < 2000) {
    requestAnimationFrame(() => animate(element, startTime));
  }
}

requestAnimationFrame(() => animate(element, Date.now()));
```

---

## Bundle optimization sin bundler

```javascript
// ✅ ES Modules: el navegador solo carga lo que se importa
// app.js
import { initOrderList } from './modules/orders/list.js';  // Solo carga este archivo

// ✅ Dynamic import: cargar bajo demanda
document.querySelector('#reports-tab').addEventListener('click', async () => {
  const { initReports } = await import('./modules/reports/dashboard.js');
  initReports();
});

// ✅ Scripts con defer (no bloquean el parser HTML)
<script src="/js/app.js" defer></script>

// ❌ Scripts sin defer ni async (bloquean el render)
<script src="/js/app.js"></script>
```

---

## Checklist performance

- [ ] DOM batching: lecturas agrupadas antes de escrituras
- [ ] Debounce en inputs de búsqueda (300ms)
- [ ] Throttle en scroll/resize (100ms)
- [ ] IntersectionObserver para imágenes y infinite scroll
- [ ] Event delegation (1 listener para N elementos)
- [ ] Listeners removidos al eliminar elementos del DOM
- [ ] AbortController para cancelar fetch obsoletos
- [ ] `requestAnimationFrame` para animaciones (no setInterval)
- [ ] Dynamic `import()` para código que no se usa inmediatamente
- [ ] `<script defer>` para no bloquear el render inicial
