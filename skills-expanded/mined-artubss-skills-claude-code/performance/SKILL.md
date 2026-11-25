---
name: performance
description: Otimize o desempenho web para carregamento mais rápido e melhor experiência do usuário. Use quando solicitado a "acelerar meu site", "otimizar desempenho", "reduzir tempo de carregamento", "corrigir carregamento lento", "melhorar velocidade da página" ou "auditoria de desempenho".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Otimização de desempenho

Otimização profunda de desempenho baseada em auditorias Lighthouse. Foca em velocidade de carregamento, eficiência em tempo de execução e otimização de recursos.

## Como funciona

1. Identificar gargalos de desempenho em código e assets
2. Priorizar por impacto nas Core Web Vitals
3. Fornecer otimizações específicas com exemplos de código
4. Medir melhoria com métricas antes/depois

## Orçamento de desempenho

| Recurso | Orçamento | Justificativa |
|---------|-----------|---------------|
| Peso total da página | < 1.5 MB | Carregamento em 3G em ~4s |
| JavaScript (comprimido) | < 300 KB | Tempo de parsing + execução |
| CSS (comprimido) | < 100 KB | Render blocking |
| Imagens (above-fold) | < 500 KB | Impacto em LCP |
| Fontes | < 100 KB | Prevenção de FOIT/FOUT |
| Third-party | < 200 KB | Latência não controlada |

## Caminho crítico de renderização

### Resposta do servidor
* **TTFB < 800ms.** O Time to First Byte deve ser rápido. Use CDN, caching e backends eficientes.
* **Ativar compressão.** Gzip ou Brotli para assets de texto. Brotli preferível (15-20% menor).
* **HTTP/2 ou HTTP/3.** Multiplexing reduz overhead de conexão.
* **Edge caching.** Faça cache do HTML na borda do CDN quando possível.

### Carregamento de recursos

**Pré-conectar a origens necessárias:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```

**Pré-carregar recursos críticos:**
```html
<!-- Imagem LCP -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Fonte crítica -->
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
```

**Adiar CSS não crítico:**
```html
<!-- CSS crítico inlineado -->
<style>/* Estilos above-fold */</style>

<!-- CSS não crítico -->
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

### Otimização de JavaScript

**Adiar scripts não essenciais:**
```html
<!-- Parser-blocking (evitar) -->
<script src="/critical.js"></script>

<!-- Deferred (preferível) -->
<script defer src="/app.js"></script>

<!-- Async (para scripts independentes) -->
<script async src="/analytics.js"></script>

<!-- Module (deferred por padrão) -->
<script type="module" src="/app.mjs"></script>
```

**Padrões de code splitting:**
```javascript
// Splitting baseado em rotas
const Dashboard = lazy(() => import('./Dashboard'));

// Splitting baseado em componentes
const HeavyChart = lazy(() => import('./HeavyChart'));

// Splitting baseado em features
if (user.isPremium) {
  const PremiumFeatures = await import('./PremiumFeatures');
}
```

**Melhores práticas de tree shaking:**
```javascript
// ❌ Importa a biblioteca inteira
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Importa apenas o necessário
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Otimização de imagens

### Seleção de formato
| Formato | Caso de uso | Suporte de navegadores |
|---------|-------------|------------------------|
| AVIF | Fotos, melhor compressão | 92%+ |
| WebP | Fotos, fallback bom | 97%+ |
| PNG | Gráficos com transparência | Universal |
| SVG | Ícones, logos, ilustrações | Universal |

### Imagens responsivas
```html
<picture>
  <!-- AVIF para navegadores modernos -->
  <source 
    type="image/avif"
    srcset="hero-400.avif 400w,
            hero-800.avif 800w,
            hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- Fallback WebP -->
  <source 
    type="image/webp"
    srcset="hero-400.webp 400w,
            hero-800.webp 800w,
            hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  
  <!-- Fallback JPEG -->
  <img 
    src="hero-800.jpg"
    srcset="hero-400.jpg 400w,
            hero-800.jpg 800w,
            hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    width="1200" 
    height="600"
    alt="Hero image"
    loading="lazy"
    decoding="async">
</picture>
```

### Prioridade de imagem LCP
```html
<!-- Imagem LCP above-fold: carregamento eager, alta prioridade -->
<img 
  src="hero.webp" 
  fetchpriority="high"
  loading="eager"
  decoding="sync"
  alt="Hero">

<!-- Imagens below-fold: lazy loading -->
<img 
  src="product.webp" 
  loading="lazy"
  decoding="async"
  alt="Product">
```

## Otimização de fontes

### Estratégia de carregamento
```css
/* Stack de fontes do sistema como fallback */
body {
  font-family: 'Custom Font', -apple-system, BlinkMacSystemFont, 
               'Segoe UI', Roboto, sans-serif;
}

/* Impedir texto invisível */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* ou optional para não críticas */
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF; /* Subset para Latin */
}
```

### Pré-carregamento de fontes críticas
```html
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

### Variable fonts
```css
/* Um arquivo em vez de múltiplos pesos */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

## Estratégia de caching

### Headers Cache-Control
```
# HTML (cache curto ou nenhum)
Cache-Control: no-cache, must-revalidate

# Assets estáticos com hash (imutável)
Cache-Control: public, max-age=31536000, immutable

# Assets estáticos sem hash
Cache-Control: public, max-age=86400, stale-while-revalidate=604800

# Respostas de API
Cache-Control: private, max-age=0, must-revalidate
```

### Caching com service worker
```javascript
// Cache-first para assets estáticos
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          const clone = response.clone();
          caches.open('static-v1').then((cache) => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});
```

## Desempenho em tempo de execução

### Evitar layout thrashing
```javascript
// ❌ Força múltiplos reflows
elements.forEach(el => {
  const height = el.offsetHeight; // Leitura
  el.style.height = height + 10 + 'px'; // Escrita
});

// ✅ Agrupar leituras, depois agrupar escritas
const heights = elements.map(el => el.offsetHeight); // Todas as leituras
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // Todas as escritas
});
```

### Debounce de operações caras
```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

// Debounce de handlers de scroll/resize
window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Usar requestAnimationFrame
```javascript
// ❌ Pode causar jank
setInterval(animate, 16);

// ✅ Sincronizado com refresh da tela
function animate() {
  // Lógica de animação
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Virtualizar listas longas
```javascript
// Para listas > 100 itens, renderizar apenas itens visíveis
// Use bibliotecas como react-window, vue-virtual-scroller, ou CSS nativo:
.virtual-list {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px; /* Altura estimada do item */
}
```

## Scripts third-party

### Estratégias de carregamento
```javascript
// ❌ Bloqueia a thread principal
<script src="https://analytics.example.com/script.js"></script>

// ✅ Carregamento async
<script async src="https://analytics.example.com/script.js"></script>

// ✅ Atrasar até interação
<script>
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      const script = document.createElement('script');
      script.src = 'https://widget.example.com/embed.js';
      document.body.appendChild(script);
      observer.disconnect();
    }
  });
  observer.observe(document.querySelector('#widget-container'));
});
</script>
```

### Padrão Facade
```html
<!-- Mostrar placeholder estático até interação -->
<div class="youtube-facade" 
     data-video-id="abc123" 
     onclick="loadYouTube(this)">
  <img src="/thumbnails/abc123.jpg" alt="Video title">
  <button aria-label="Play video">▶</button>
</div>
```

## Medição

### Métricas chave
| Métrica | Alvo | Ferramenta |
|---------|------|-----------|
| LCP | < 2.5s | Lighthouse, CrUX |
| FCP | < 1.8s | Lighthouse |
| Speed Index | < 3.4s | Lighthouse |
| TBT | < 200ms | Lighthouse |
| TTI | < 3.8s | Lighthouse |

### Comandos de teste
```bash
# Lighthouse CLI
npx lighthouse https://example.com --output html --output-path report.html

# Biblioteca Web Vitals
import {onLCP, onINP, onCLS} from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

## Referências

Para otimizações específicas de Core Web Vitals, veja [Core Web Vitals](../core-web-vitals/SKILL.md).