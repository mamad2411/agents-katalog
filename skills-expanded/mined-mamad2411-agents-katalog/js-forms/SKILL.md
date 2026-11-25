---
name: js-forms
description: "Formularios en JavaScript vanilla. Cubre FormData + fetch(), validación HTML5 (required, pattern, setCustomValidity), Constraint Validation API, validación custom, feedback visual de errores, file upload, y formularios dinámicos (agregar/quitar filas). Actívala al implementar formularios en proyectos ASP.NET MVC sin React Hook Form, o al reemplazar jQuery Validation por vanilla JS."
---

# JavaScript Forms & Validation

Guía de formularios con JavaScript vanilla. Sin frameworks. HTML5 + Constraint Validation API.

---

## FormData + fetch (el estándar 2026)

```javascript
// ✅ Submit con FormData (campos + archivos automáticamente)
document.querySelector('#order-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const submitBtn = form.querySelector('button[type="submit"]');

  submitBtn.disabled = true;
  submitBtn.textContent = 'Guardando...';

  try {
    const res = await fetch(form.action, {
      method: form.method,
      body: formData,  // Content-Type automático con boundary
    });

    if (!res.ok) {
      const error = await res.json();
      showServerErrors(error.errors);
      return;
    }

    const order = await res.json();
    window.location.href = `/Orders/Details/${order.id}`;
  } catch (err) {
    showError('Error de conexión. Intente de nuevo.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Guardar';
  }
});
```

---

## Validación HTML5 (sin JS)

```html
<form id="order-form">
  <input type="text"
         name="customerId"
         required
         minlength="3"
         maxlength="50"
         placeholder="CUST-001">

  <input type="number"
         name="amount"
         required
         min="0.01"
         max="9999999"
         step="0.01">

  <input type="email"
         name="email"
         placeholder="cliente@correo.com">

  <input type="url"
         name="website"
         placeholder="https://...">

  <input type="text"
         name="sku"
         pattern="[A-Z]{3}-\\d{4}"
         title="Formato: XXX-0000">

  <select name="currency" required>
    <option value="">Seleccione...</option>
    <option value="MXN">MXN</option>
    <option value="USD">USD</option>
  </select>

  <button type="submit">Crear</button>
</form>
```

---

## Constraint Validation API

```javascript
// ✅ Validación custom + mensajes personalizados
const form = document.querySelector('#order-form');
const customerInput = form.querySelector('[name="customerId"]');
const amountInput = form.querySelector('[name="amount"]');

customerInput.addEventListener('input', () => {
  customerInput.setCustomValidity('');  // Limpiar error previo

  if (customerInput.value.length < 3) {
    customerInput.setCustomValidity('El ID debe tener al menos 3 caracteres');
  }
  if (!/^[A-Za-z0-9\-_]+$/.test(customerInput.value)) {
    customerInput.setCustomValidity('Solo letras, números y guiones');
  }

  customerInput.reportValidity();  // Mostrar mensaje inmediatamente
});

amountInput.addEventListener('input', () => {
  amountInput.setCustomValidity('');
  const val = parseFloat(amountInput.value);
  if (val <= 0) amountInput.setCustomValidity('El monto debe ser positivo');
  if (val > 9999999) amountInput.setCustomValidity('Monto máximo: $9,999,999');
  amountInput.reportValidity();
});

// ✅ Validación al submit con resumen de errores
form.addEventListener('submit', (e) => {
  if (!form.checkValidity()) {
    e.preventDefault();
    showFieldErrors(form);
  }
});

function showFieldErrors(form) {
  const errors = [];
  form.querySelectorAll(':invalid').forEach(field => {
    const label = form.querySelector(`label[for="${field.id}"]`)?.textContent || field.name;
    errors.push(`${label}: ${field.validationMessage}`);
    field.classList.add('is-invalid');
  });
  document.querySelector('#error-summary').innerHTML = errors
    .map(e => `<li>${e}</li>`).join('');
}
```

### CSS para feedback visual

```css
input:invalid,
select:invalid {
  border-color: #dc3545;
}

input.is-invalid,
select.is-invalid {
  border-color: #dc3545;
  background-image: url("data:image/svg+xml,..."); /* Icono de error */
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
```

---

## Validación cross-field

```javascript
// ✅ Validar que dos campos coincidan (ej: password + confirmación)
const password = form.querySelector('[name="password"]');
const confirm = form.querySelector('[name="confirmPassword"]');

function validatePasswordMatch() {
  confirm.setCustomValidity('');
  if (password.value !== confirm.value) {
    confirm.setCustomValidity('Las contraseñas no coinciden');
  }
}

password.addEventListener('input', validatePasswordMatch);
confirm.addEventListener('input', validatePasswordMatch);

// ✅ Validar fecha inicio < fecha fin
const startDate = form.querySelector('[name="startDate"]');
const endDate = form.querySelector('[name="endDate"]');

function validateDateRange() {
  endDate.setCustomValidity('');
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    endDate.setCustomValidity('La fecha fin debe ser posterior a la fecha inicio');
  }
}

startDate.addEventListener('change', validateDateRange);
endDate.addEventListener('change', validateDateRange);
```

---

## File upload con feedback

```html
<input type="file"
       name="attachment"
       accept=".pdf,.jpg,.png"
       data-max-size="10485760">
<!-- 10 MB -->
<div class="file-info"></div>
<progress value="0" max="100" class="upload-progress" style="display:none"></progress>
```

```javascript
const fileInput = document.querySelector('[name="attachment"]');
const fileInfo = document.querySelector('.file-info');
const progressBar = document.querySelector('.upload-progress');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;

  // Validar tipo
  const allowed = ['application/pdf', 'image/jpeg', 'image/png'];
  if (!allowed.includes(file.type)) {
    fileInput.setCustomValidity('Solo PDF, JPG o PNG');
    fileInput.reportValidity();
    fileInput.value = '';
    return;
  }

  // Validar tamaño
  const maxSize = parseInt(fileInput.dataset.maxSize);
  if (file.size > maxSize) {
    const maxMB = (maxSize / 1024 / 1024).toFixed(1);
    fileInput.setCustomValidity(`Máximo ${maxMB} MB`);
    fileInput.reportValidity();
    fileInput.value = '';
    return;
  }

  // Mostrar preview
  fileInfo.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
});

// Upload con progreso
async function uploadWithProgress(file) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/upload');

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percent = Math.round((e.loaded / e.total) * 100);
        progressBar.style.display = 'block';
        progressBar.value = percent;
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`));
      }
    });

    xhr.addEventListener('error', () => reject(new Error('Network error')));

    const formData = new FormData();
    formData.append('file', file);
    xhr.send(formData);
  });
}
```

---

## Formularios dinámicos (agregar/quitar filas)

```html
<template id="item-row-template">
  <tr class="item-row">
    <td><input type="text" name="items[].sku" required></td>
    <td><input type="number" name="items[].quantity" min="1" value="1" required></td>
    <td><input type="number" name="items[].unitPrice" min="0.01" step="0.01" required></td>
    <td><button type="button" class="remove-row-btn">✕</button></td>
  </tr>
</template>

<table id="items-table">
  <thead><tr><th>SKU</th><th>Cantidad</th><th>Precio</th><th></th></tr></thead>
  <tbody></tbody>
</table>
<button type="button" id="add-row-btn">+ Agregar item</button>
```

```javascript
const tbody = document.querySelector('#items-table tbody');
const template = document.querySelector('#item-row-template');

document.querySelector('#add-row-btn').addEventListener('click', () => {
  const clone = template.content.cloneNode(true);
  // Botón de eliminar
  clone.querySelector('.remove-row-btn').addEventListener('click', function() {
    this.closest('tr').remove();
  });
  tbody.appendChild(clone);
});

// El form submit envía items[] como array automáticamente con FormData
```

---

## Checklist forms

- [ ] `FormData` + `fetch()` para submit (no `XMLHttpRequest` salvo para progress)
- [ ] Validación HTML5 base: `required`, `min`/`max`, `pattern`, `minlength`/`maxlength`
- [ ] `setCustomValidity()` para reglas de negocio
- [ ] `reportValidity()` para mostrar errores inmediatamente
- [ ] `.is-invalid` CSS class + `.error-message` para feedback visual
- [ ] Anti-forgery token incluido vía `FormData` o header
- [ ] File upload con validación de tipo + tamaño + progress
- [ ] Botón submit deshabilitado durante envío (`disabled` + texto "Guardando...")
- [ ] Formularios dinámicos con `<template>` + `cloneNode`
