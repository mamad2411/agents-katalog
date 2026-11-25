---
name: best-practices
description: Aplique práticas modernas de desenvolvimento web para segurança, compatibilidade e qualidade de código. Use quando solicitado "aplicar best practices", "auditoria de segurança", "modernizar código", "análise de qualidade de código" ou "verificar vulnerabilidades".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Best practices

Padrões de desenvolvimento web moderno baseados em auditorias Lighthouse best practices. Aborda segurança, compatibilidade entre navegadores e padrões de qualidade de código.

## Segurança

### HTTPS em todos os lugares

**Enforce HTTPS:**
```html
<!-- ❌ Conteúdo misto -->
<img src="http://example.com/image.jpg">
<script src="http://cdn.example.com/script.js"></script>

<!-- ✅ HTTPS apenas -->
<img src="https://example.com/image.jpg">
<script src="https://cdn.example.com/script.js"></script>

<!-- ✅ Protocol-relative (usará o protocolo da página) -->
<img src="//example.com/image.jpg">
```

**Header HSTS:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### Content Security Policy (CSP)

```html
<!-- CSP básico via meta tag -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' https://trusted-cdn.com; 
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;
               connect-src 'self' https://api.example.com;">

<!-- Melhor: HTTP header -->
```

**Header CSP (recomendado):**
```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-abc123' https://trusted.com;
  style-src 'self' 'nonce-abc123';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'self';
  base-uri 'self';
  form-action 'self';
```

**Usando nonces para scripts inline:**
```html
<script nonce="abc123">
  // Este script inline é permitido
</script>
```

### Headers de segurança

```
# Prevenir clickjacking
X-Frame-Options: DENY

# Prevenir sniffing de tipo MIME
X-Content-Type-Options: nosniff

# Habilitar filtro XSS (navegadores legados)
X-XSS-Protection: 1; mode=block

# Controlar informações de referência
Referrer-Policy: strict-origin-when-cross-origin

# Permissions policy (anteriormente Feature-Policy)
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### Sem bibliotecas vulneráveis

```bash
# Verificar vulnerabilidades
npm audit
yarn audit

# Auto-fix quando possível
npm audit fix

# Verificar pacote específico
npm ls lodash
```

**Mantenha dependências atualizadas:**
```json
// package.json
{
  "scripts": {
    "audit": "npm audit --audit-level=moderate",
    "update": "npm update && npm audit fix"
  }
}
```

**Padrões vulneráveis conhecidos a evitar:**
```javascript
// ❌ Padrões vulneráveis a prototype pollution
Object.assign(target, userInput);
_.merge(target, userInput);

// ✅ Alternativas mais seguras
const safeData = JSON.parse(JSON.stringify(userInput));
```

### Sanitização de entrada

```javascript
// ❌ Vulnerável a XSS
element.innerHTML = userInput;
document.write(userInput);

// ✅ Conteúdo de texto seguro
element.textContent = userInput;

// ✅ Se HTML for necessário, sanitize
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Cookies seguros

```javascript
// ❌ Cookie inseguro
document.cookie = "session=abc123";

// ✅ Cookie seguro (lado do servidor)
Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Strict; Path=/
```

---

## Compatibilidade entre navegadores

### Declaração doctype

```html
<!-- ❌ Doctype ausente ou inválido -->
<HTML>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">

<!-- ✅ Doctype HTML5 -->
<!DOCTYPE html>
<html lang="pt-BR">
```

### Codificação de caracteres

```html
<!-- ❌ Charset ausente ou tardiamente declarado -->
<html>
<head>
  <title>Página</title>
  <meta charset="UTF-8">
</head>

<!-- ✅ Charset como primeiro elemento na head -->
<html>
<head>
  <meta charset="UTF-8">
  <title>Página</title>
</head>
```

### Meta tag viewport

```html
<!-- ❌ Viewport ausente -->
<head>
  <title>Página</title>
</head>

<!-- ✅ Viewport responsivo -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Página</title>
</head>
```

### Detecção de recursos

```javascript
// ❌ Detecção de navegador (frágil)
if (navigator.userAgent.includes('Chrome')) {
  // Código específico do Chrome
}

// ✅ Detecção de recurso
if ('IntersectionObserver' in window) {
  // Usar IntersectionObserver
} else {
  // Fallback
}

// ✅ Usando @supports em CSS
@supports (display: grid) {
  .container {
    display: grid;
  }
}

@supports not (display: grid) {
  .container {
    display: flex;
  }
}
```

### Polyfills (quando necessário)

```html
<!-- Carregar polyfills condicionalmente -->
<script>
  if (!('fetch' in window)) {
    document.write('<script src="/polyfills/fetch.js"><\/script>');
  }
</script>

<!-- Ou usar polyfill.io -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=fetch,IntersectionObserver"></script>
```

---

## APIs deprecadas

### Evite estas

```javascript
// ❌ document.write (bloqueia análise)
document.write('<script src="..."></script>');

// ✅ Carregamento dinâmico de script
const script = document.createElement('script');
script.src = '...';
document.head.appendChild(script);

// ❌ XHR síncrono (bloqueia thread principal)
const xhr = new XMLHttpRequest();
xhr.open('GET', url, false); // false = síncrono

// ✅ Fetch assíncrono
const response = await fetch(url);

// ❌ Application Cache (deprecado)
<html manifest="cache.manifest">

// ✅ Service Workers
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

### Event listener passive

```javascript
// ❌ Touch/wheel não-passive (pode bloquear scroll)
element.addEventListener('touchstart', handler);
element.addEventListener('wheel', handler);

// ✅ Listeners passive (permite scroll suave)
element.addEventListener('touchstart', handler, { passive: true });
element.addEventListener('wheel', handler, { passive: true });

// ✅ Se precisar de preventDefault, seja explícito
element.addEventListener('touchstart', handler, { passive: false });
```

---

## Console & erros

### Sem erros de console

```javascript
// ❌ Erros em produção
console.log('Informação de debug'); // Remova em produção
throw new Error('Não capturado'); // Capture todos os erros

// ✅ Tratamento de erro apropriado
try {
  operacaoArriscada();
} catch (error) {
  // Registre no serviço de rastreamento de erro
  rastreadorErro.captureException(error);
  // Mostre mensagem amigável ao usuário
  mostrarMensagemErro('Algo deu errado. Por favor, tente novamente.');
}
```

### Error boundaries (React)

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, info) {
    rastreadorErro.captureException(error, { extra: info });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}

// Uso
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### Global error handler

```javascript
// Capturar erros não capturados
window.addEventListener('error', (event) => {
  rastreadorErro.captureException(event.error);
});

// Capturar rejeições de promise não capturadas
window.addEventListener('unhandledrejection', (event) => {
  rastreadorErro.captureException(event.reason);
});
```

---

## Source maps

### Configuração de produção

```javascript
// ❌ Source maps expostos em produção
// webpack.config.js
module.exports = {
  devtool: 'source-map', // Expõe código-fonte
};

// ✅ Source maps ocultos (enviados para rastreador de erro)
module.exports = {
  devtool: 'hidden-source-map',
};

// ✅ Ou sem source maps em produção
module.exports = {
  devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
};
```

---

## Práticas de performance

### Evite padrões bloqueadores

```javascript
// ❌ Script bloqueador
<script src="heavy-library.js"></script>

// ✅ Script deferido
<script defer src="heavy-library.js"></script>

// ❌ Importação CSS bloqueadora
@import url('other-styles.css');

// ✅ Link tags (carregamento paralelo)
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="other-styles.css">
```

### Manipuladores de evento eficientes

```javascript
// ❌ Manipulador em cada elemento
items.forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ Delegação de evento
container.addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleClick(e);
  }
});
```

### Gerenciamento de memória

```javascript
// ❌ Vazamento de memória (nunca removido)
const handler = () => { /* ... */ };
window.addEventListener('resize', handler);

// ✅ Limpeza quando concluído
const handler = () => { /* ... */ };
window.addEventListener('resize', handler);

// Depois, quando componente desmonta:
window.removeEventListener('resize', handler);

// ✅ Usando AbortController
const controller = new AbortController();
window.addEventListener('resize', handler, { signal: controller.signal });

// Limpeza:
controller.abort();
```

---

## Qualidade de código

### HTML válido

```html
<!-- ❌ HTML inválido -->
<div id="header">
<div id="header"> <!-- ID duplicado -->

<ul>
  <div>Item</div> <!-- Filho inválido -->
</ul>

<a href="/"><button>Click</button></a> <!-- Aninhamento inválido -->

<!-- ✅ HTML válido -->
<header id="site-header">
</header>

<ul>
  <li>Item</li>
</ul>

<a href="/" class="button">Click</a>
```

### HTML semântico

```html
<!-- ❌ Não-semântico -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
<div class="main">
  <div class="article">
    <div class="title">Headline</div>
  </div>
</div>

<!-- ✅ HTML5 semântico -->
<header>
  <nav>
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Headline</h1>
  </article>
</main>
```

### Proporção de aspecto de imagens

```html
<!-- ❌ Imagens distorcidas -->
<img src="photo.jpg" width="300" height="100">
<!-- Se a proporção real é 4:3, isto comprime a imagem -->

<!-- ✅ Preservar proporção de aspecto -->
<img src="photo.jpg" width="300" height="225">
<!-- Dimensões reais 4:3 -->

<!-- ✅ CSS object-fit para flexibilidade -->
<img src="photo.jpg" style="width: 300px; height: 200px; object-fit: cover;">
```

---

## Permissões & privacidade

### Solicite permissões apropriadamente

```javascript
// ❌ Solicitar no carregamento da página (UX ruim, geralmente negado)
navigator.geolocation.getCurrentPosition(success, error);

// ✅ Solicitar em contexto, após ação do usuário
findNearbyButton.addEventListener('click', async () => {
  // Explique por que você precisa
  if (await showPermissionExplanation()) {
    navigator.geolocation.getCurrentPosition(success, error);
  }
});
```

### Permissions policy

```html
<!-- Restrinja recursos poderosos -->
<meta http-equiv="Permissions-Policy" 
      content="geolocation=(), camera=(), microphone=()">

<!-- Ou permita para origens específicas -->
<meta http-equiv="Permissions-Policy" 
      content="geolocation=(self 'https://maps.example.com')">
```

---

## Checklist de auditoria

### Segurança (crítico)
- [ ] HTTPS ativado, sem conteúdo misto
- [ ] Sem dependências vulneráveis (`npm audit`)
- [ ] Headers CSP configurados
- [ ] Headers de segurança presentes
- [ ] Source maps não expostos

### Compatibilidade
- [ ] Doctype HTML5 válido
- [ ] Charset declarado primeiro na head
- [ ] Meta tag viewport presente
- [ ] Nenhuma API deprecada usada
- [ ] Event listeners passive para scroll/touch

### Qualidade de código
- [ ] Sem erros de console
- [ ] HTML válido (sem IDs duplicados)
- [ ] Elementos HTML semânticos usados
- [ ] Tratamento de erro apropriado
- [ ] Limpeza de memória em componentes

### UX
- [ ] Sem interstíciais intrusivos
- [ ] Solicitações de permissão em contexto
- [ ] Mensagens de erro claras
- [ ] Proporções de aspecto apropriadas para imagens

## Ferramentas

| Ferramenta | Propósito |
|------|---------|
| `npm audit` | Vulnerabilidades de dependência |
| [SecurityHeaders.com](https://securityheaders.com) | Análise de headers |
| [W3C Validator](https://validator.w3.org) | Validação HTML |
| Lighthouse | Auditoria de best practices |
| [Observatory](https://observatory.mozilla.org) | Varredura de segurança |

## Referências

- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Quality Audit](../web-quality-audit/SKILL.md)