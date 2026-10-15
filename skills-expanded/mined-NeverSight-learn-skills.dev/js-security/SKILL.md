---
name: js-security
description: "Seguridad en JavaScript vanilla en el navegador. Cubre XSS prevention (sanitización, textContent sobre innerHTML, DOMPurify), CSRF via anti-forgery tokens, Content Security Policy, sanitización de input, secure storage (sessionStorage vs cookies), y mejores prácticas de seguridad en el frontend. Actívala al asegurar formularios, prevenir XSS, o implementar CSP en proyectos ASP.NET MVC + vanilla JS."
---

# JavaScript Security (Navegador)

Guía de seguridad en el frontend vanilla JS. Defensa en profundidad desde el cliente.

---

## XSS Prevention

```javascript
// ❌ NUNCA insertar input de usuario con innerHTML
const userInput = '<img src=x onerror="alert(1)">';
document.querySelector('#output').innerHTML = userInput;  // Ejecuta el script

// ✅ textContent — escapa automáticamente
document.querySelector('#output').textContent = userInput;  // Muestra el texto literal

// ✅ innerHTML con sanitización (DOMPurify)
import DOMPurify from 'dompurify';  // o cargar vía CDN
const clean = DOMPurify.sanitize(userInput);
document.querySelector('#output').innerHTML = clean;

// ✅ Crear elementos manualmente (más seguro que innerHTML)
const div = document.createElement('div');
div.textContent = userInput;
document.querySelector('#output').append(div);

// ❌ Nunca pasar input de usuario a eval(), setTimeout(string), new Function()
eval(userInput);                    // ❌
setTimeout("doSomething()", 1000);  // ❌ (string, no function)
new Function('return ' + userInput)(); // ❌

// ✅ Siempre usar funciones, no strings
setTimeout(() => doSomething(), 1000);  // ✅
```

---

## Sanitización de URLs y atributos

```javascript
// ❌ URL del usuario en href sin validar
link.href = userInput;  // Podría ser: javascript:alert(1)

// ✅ Validar protocolo
function safeUrl(input) {
  const url = new URL(input, location.origin);
  if (!['http:', 'https:'].includes(url.protocol)) {
    throw new Error('Invalid protocol');
  }
  return url.href;
}
link.href = safeUrl(userInput);

// ✅ Atributos peligrosos: src, href, action, formaction
// Siempre validar que la URL sea http/https y del dominio esperado
```

---

## CSRF con ASP.NET MVC

```html
<!-- El helper genera un input hidden con el token -->
@Html.AntiForgeryToken()
<!-- <input name="__RequestVerificationToken" type="hidden" value="CfDJ8..."> -->
```

```javascript
// ✅ Incluir token en todo POST
async function safePost(url, data) {
  const token = document.querySelector(
    'input[name="__RequestVerificationToken"]'
  )?.value;

  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['RequestVerificationToken'] = token;
  }

  const res = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(data),
  });

  if (res.status === 400) {
    const body = await res.text();
    if (body.includes('anti-forgery')) {
      throw new Error('CSRF token inválido. Recarga la página.');
    }
  }

  return res;
}

// ✅ También funciona con FormData (el token va en el formulario)
const formData = new FormData(form);
// input[name="__RequestVerificationToken"] se incluye automáticamente
```

---

## Content Security Policy (CSP)

```html
<!-- _Layout.cshtml — configurar en el servidor, no en meta tags -->
<!-- Pero puedes empezar con meta para testing -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'nonce-@Model.CspNonce';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data:;
               connect-src 'self' https://api.miapp.com;">
```

```html
<!-- Scripts con nonce (generado por el servidor) -->
<script nonce="@Model.CspNonce">
  // Este script se ejecuta
</script>

<!-- ❌ Scripts sin nonce bloqueados por CSP -->
<script>alert('bloqueado')</script>

<!-- ❌ inline event handlers bloqueados -->
<button onclick="doSomething()">Click</button>

<!-- ✅ addEventListener en archivo externo con nonce -->
```

---

## Secure Storage

```javascript
// ❌ NUNCA guardar tokens en localStorage (vulnerable a XSS)
localStorage.setItem('authToken', token);

// ✅ HttpOnly cookies (el servidor las configura, JS no puede leerlas)
// En el controller: Response.Cookies.Append("token", value, new CookieOptions { HttpOnly = true });

// ✅ sessionStorage para datos de sesión no sensibles
sessionStorage.setItem('currentFilter', JSON.stringify({ status: 'pending' }));

// ✅ localStorage para preferencias de UI (tema, idioma, columnas visibles)
localStorage.setItem('theme', 'dark');
localStorage.setItem('tableColumns', JSON.stringify(['orderNumber', 'status', 'total']));
```

---

## Validación de input del usuario

```javascript
// ✅ Sanitizar antes de enviar al servidor (defensa en profundidad)
function sanitizeInput(value) {
  if (typeof value !== 'string') return value;
  return value
    .trim()
    .replace(/[<>]/g, '');  // Eliminar < y >
}

// ✅ Validar tipos antes de enviar
function validateOrderInput(data) {
  if (typeof data.customerId !== 'string' || data.customerId.length === 0) {
    throw new Error('Customer ID inválido');
  }
  if (typeof data.amount !== 'number' || data.amount <= 0) {
    throw new Error('Amount inválido');
  }
  return {
    customerId: sanitizeInput(data.customerId),
    amount: data.amount,
  };
}

// ✅ Codificar parámetros en URLs
const encoded = encodeURIComponent(userInput);
fetch(`/api/orders?q=${encoded}`);

// ❌ Nunca concatenar input crudo en URLs
fetch(`/api/orders?q=${userInput}`);  // Vulnerable a inyección
```

---

## Dependencias de terceros

```html
<!-- ✅ Subresource Integrity (SRI) para CDNs -->
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.0/dist/purify.min.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>

<!-- ❌ CDN sin SRI — si el CDN es comprometido, el atacante inyecta código -->
```

---

## Checklist seguridad

- [ ] `textContent` sobre `innerHTML` para input de usuario (o DOMPurify)
- [ ] Anti-forgery token en todos los POST
- [ ] CSP configurado (al menos `script-src 'self'`)
- [ ] No `eval()`, `new Function()`, `setTimeout(string)`
- [ ] No tokens en `localStorage` (usar HttpOnly cookies)
- [ ] URLs validadas antes de poner en `href`, `src`, `action`
- [ ] `encodeURIComponent()` para parámetros en URLs
- [ ] SRI para dependencias de CDN
- [ ] Validación client-side + server-side (defensa en profundidad)
- [ ] `autocomplete="off"` en campos sensibles (o `new-password` en passwords)
