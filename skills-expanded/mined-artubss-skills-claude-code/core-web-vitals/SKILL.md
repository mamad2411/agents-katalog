---
name: core-web-vitals
description: Otimize Core Web Vitals (LCP, INP, CLS) para melhor experiência de página e ranking de busca. Use quando solicitado para "melhorar Core Web Vitals", "corrigir LCP", "reduzir CLS", "otimizar INP", "otimização de experiência de página" ou "corrigir deslocamentos de layout".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Otimização de Core Web Vitals

Otimização direcionada para as três métricas de Core Web Vitals que afetam o ranking do Google Search e a experiência do usuário.

## As três métricas

| Métrica | Mede | Bom | Precisa melhorar | Ruim |
|---------|------|-----|------------------|------|
| **LCP** | Carregamento | ≤ 2,5s | 2,5s – 4s | > 4s |
| **INP** | Interatividade | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** | Estabilidade visual | ≤ 0,1 | 0,1 – 0,25 | > 0,25 |

O Google mede no **75º percentil** — 75% das visitas de página devem atender aos limites "Bom".

---

## LCP: Largest Contentful Paint

LCP mede quando o maior elemento de conteúdo visível é renderizado. Geralmente é:
- Imagem ou vídeo em destaque
- Bloco de texto grande
- Imagem de fundo
- Elemento `<svg>`

### Problemas comuns de LCP

**1. Resposta lenta do servidor (TTFB > 800ms)**
```
Solução: CDN, cache, backend otimizado, renderização em edge
```

**2. Recursos que bloqueiam renderização**
```html
<!-- ❌ Bloqueia renderização -->
<link rel="stylesheet" href="/all-styles.css">

<!-- ✅ CSS crítico incorporado, restante adiado -->
<style>/* CSS crítico acima da dobra */</style>
<link rel="preload" href="/styles.css" as="style" 
      onload="this.onload=null;this.rel='stylesheet'">
```

**3. Tempo lento de carregamento de recursos**
```html
<!-- ❌ Sem dicas, descoberto tarde -->
<img src="/hero.jpg" alt="Hero">

<!-- ✅ Pré-carregado com alta prioridade -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">
<img src="/hero.webp" alt="Hero" fetchpriority="high">
```

**4. Atrasos na renderização no cliente**
```javascript
// ❌ Conteúdo carrega após JavaScript
useEffect(() => {
  fetch('/api/hero-text').then(r => r.json()).then(setHeroText);
}, []);

// ✅ Renderização no servidor ou estática
// Use SSR, SSG ou streaming para enviar HTML com conteúdo
export async function getServerSideProps() {
  const heroText = await fetchHeroText();
  return { props: { heroText } };
}
```

### Checklist de otimização de LCP

```markdown
- [ ] TTFB < 800ms (use CDN, cache em edge)
- [ ] Imagem LCP pré-carregada com fetchpriority="high"
- [ ] Imagem LCP otimizada (WebP/AVIF, tamanho correto)
- [ ] CSS crítico incorporado (< 14KB)
- [ ] Nenhum JavaScript que bloqueie renderização em <head>
- [ ] Fontes não bloqueiam renderização de texto (font-display: swap)
- [ ] Elemento LCP no HTML inicial (não renderizado por JS)
```

### Identificação do elemento LCP
```javascript
// Encontre seu elemento LCP
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP element:', lastEntry.element);
  console.log('LCP time:', lastEntry.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

---

## INP: Interaction to Next Paint

INP mede a responsividade em TODAS as interações (cliques, toques, pressionamento de teclas) durante uma visita à página. Ele relata a pior interação (no 98º percentil para páginas de alto tráfego).

### Decomposição de INP

Total INP = **Input Delay** + **Processing Time** + **Presentation Delay**

| Fase | Alvo | Otimização |
|------|------|-----------|
| Input Delay | < 50ms | Reduza bloqueio da thread principal |
| Processing | < 100ms | Otimize manipuladores de eventos |
| Presentation | < 50ms | Minimize trabalho de renderização |

### Problemas comuns de INP

**1. Tarefas longas bloqueando a thread principal**
```javascript
// ❌ Tarefa síncrona longa
function processLargeArray(items) {
  items.forEach(item => expensiveOperation(item));
}

// ✅ Divida em chunks com yielding
async function processLargeArray(items) {
  const CHUNK_SIZE = 100;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => expensiveOperation(item));
    
    // Ceda à thread principal
    await new Promise(r => setTimeout(r, 0));
    // Ou use scheduler.yield() quando disponível
  }
}
```

**2. Manipuladores de eventos pesados**
```javascript
// ❌ Todo trabalho no manipulador
button.addEventListener('click', () => {
  // Computação pesada
  const result = calculateComplexThing();
  // Atualizações de DOM
  updateUI(result);
  // Analytics
  trackEvent('click');
});

// ✅ Priorize feedback visual imediato
button.addEventListener('click', () => {
  // Feedback visual imediato
  button.classList.add('loading');
  
  // Adie trabalho não-crítico
  requestAnimationFrame(() => {
    const result = calculateComplexThing();
    updateUI(result);
  });
  
  // Use requestIdleCallback para analytics
  requestIdleCallback(() => trackEvent('click'));
});
```

**3. Scripts de terceiros**
```javascript
// ❌ Carregado com entusiasmo, bloqueia interações
<script src="https://heavy-widget.com/widget.js"></script>

// ✅ Carregado com preguiça na interação ou visibilidade
const loadWidget = () => {
  import('https://heavy-widget.com/widget.js')
    .then(widget => widget.init());
};
button.addEventListener('click', loadWidget, { once: true });
```

**4. Re-renderizações excessivas (React/Vue)**
```javascript
// ❌ Re-renderiza toda a árvore
function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <ExpensiveComponent /> {/* Re-renderiza a cada mudança de count */}
    </div>
  );
}

// ✅ Componentes caros memoizados
const MemoizedExpensive = React.memo(ExpensiveComponent);

function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <MemoizedExpensive />
    </div>
  );
}
```

### Checklist de otimização de INP

```markdown
- [ ] Nenhuma tarefa > 50ms na thread principal
- [ ] Manipuladores de eventos concluem rapidamente (< 100ms)
- [ ] Feedback visual fornecido imediatamente
- [ ] Trabalho pesado adiado com requestIdleCallback
- [ ] Scripts de terceiros não bloqueiam interações
- [ ] Manipuladores de entrada com debounce quando apropriado
- [ ] Web Workers para operações intensivas de CPU
```

### Depuração de INP
```javascript
// Identifique interações lentas
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 200) {
      console.warn('Slow interaction:', {
        type: entry.name,
        duration: entry.duration,
        processingStart: entry.processingStart,
        processingEnd: entry.processingEnd,
        target: entry.target
      });
    }
  }
}).observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

---

## CLS: Cumulative Layout Shift

CLS mede deslocamentos de layout inesperados. Um deslocamento ocorre quando um elemento visível muda de posição entre quadros sem interação do usuário.

**Fórmula de CLS:** `impacto de fração × fração de distância`

### Causas comuns de CLS

**1. Imagens sem dimensões**
```html
<!-- ❌ Causa deslocamento de layout quando carregada -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Espaço reservado -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ Ou use aspect-ratio -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 4/3; width: 100%;">
```

**2. Anúncios, embeds e iframes**
```html
<!-- ❌ Tamanho desconhecido até carregar -->
<iframe src="https://ad-network.com/ad"></iframe>

<!-- ✅ Reserve espaço com min-height -->
<div style="min-height: 250px;">
  <iframe src="https://ad-network.com/ad" height="250"></iframe>
</div>

<!-- ✅ Ou use container com aspect-ratio -->
<div style="aspect-ratio: 16/9;">
  <iframe src="https://youtube.com/embed/..." 
          style="width: 100%; height: 100%;"></iframe>
</div>
```

**3. Conteúdo injetado dinamicamente**
```javascript
// ❌ Insere conteúdo acima do viewport
notifications.prepend(newNotification);

// ✅ Insira abaixo do viewport ou use transform
const insertBelow = viewport.bottom < newNotification.top;
if (insertBelow) {
  notifications.prepend(newNotification);
} else {
  // Anime sem deslocar
  newNotification.style.transform = 'translateY(-100%)';
  notifications.prepend(newNotification);
  requestAnimationFrame(() => {
    newNotification.style.transform = '';
  });
}
```

**4. Fontes web causando FOUT**
```css
/* ❌ Troca de fonte desloca texto */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
}

/* ✅ Fonte opcional (sem deslocamento se lenta) */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: optional;
}

/* ✅ Ou combine métricas de fallback */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%; /* Combine tamanho de fallback */
  ascent-override: 95%;
  descent-override: 20%;
}
```

**5. Animações disparando layout**
```css
/* ❌ Anima propriedades de layout */
.animate {
  transition: height 0.3s, width 0.3s;
}

/* ✅ Use transform em vez disso */
.animate {
  transition: transform 0.3s;
}
.animate.expanded {
  transform: scale(1.2);
}
```

### Checklist de otimização de CLS

```markdown
- [ ] Todas as imagens têm width/height ou aspect-ratio
- [ ] Todos os vídeos/embeds têm espaço reservado
- [ ] Anúncios têm containers com min-height
- [ ] Fontes usam font-display: optional ou métricas combinadas
- [ ] Conteúdo dinâmico inserido abaixo do viewport
- [ ] Animações usam apenas transform/opacity
- [ ] Nenhum conteúdo injetado acima do conteúdo existente
```

### Depuração de CLS
```javascript
// Rastreie deslocamentos de layout
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log('Layout shift:', entry.value);
      entry.sources?.forEach(source => {
        console.log('  Shifted element:', source.node);
        console.log('  Previous rect:', source.previousRect);
        console.log('  Current rect:', source.currentRect);
      });
    }
  }
}).observe({ type: 'layout-shift', buffered: true });
```

---

## Ferramentas de medição

### Testes em laboratório
- **Chrome DevTools** → Painel Performance, Lighthouse
- **WebPageTest** → Detalhado waterfall, filmstrip
- **Lighthouse CLI** → `npx lighthouse <url>`

### Dados de campo (usuários reais)
- **Chrome User Experience Report (CrUX)** → BigQuery ou API
- **Search Console** → Relatório de Core Web Vitals
- **web-vitals library** → Envie para sua analytics

```javascript
import {onLCP, onINP, onCLS} from 'web-vitals';

function sendToAnalytics({name, value, rating}) {
  gtag('event', name, {
    event_category: 'Web Vitals',
    value: Math.round(name === 'CLS' ? value * 1000 : value),
    event_label: rating
  });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

---

## Correções rápidas por framework

### Next.js
```jsx
// LCP: Use next/image com priority
import Image from 'next/image';
<Image src="/hero.jpg" priority fill alt="Hero" />

// INP: Use importação dinâmica
const HeavyComponent = dynamic(() => import('./Heavy'), { ssr: false });

// CLS: Componente Image cuida automaticamente das dimensões
```

### React
```jsx
// LCP: Pré-carregue na head
<link rel="preload" href="/hero.jpg" as="image" fetchpriority="high" />

// INP: Memoize e useTransition
const [isPending, startTransition] = useTransition();
startTransition(() => setExpensiveState(newValue));

// CLS: Sempre especifique dimensões em tags img
```

### Vue/Nuxt
```vue
<!-- LCP: Use nuxt/image com preload -->
<NuxtImg src="/hero.jpg" preload loading="eager" />

<!-- INP: Use componentes assíncronos -->
<component :is="() => import('./Heavy.vue')" />

<!-- CLS: Use CSS aspect-ratio -->
<img :style="{ aspectRatio: '16/9' }" />
```

## Referências

- [web.dev LCP](https://web.dev/articles/lcp)
- [web.dev INP](https://web.dev/articles/inp)
- [web.dev CLS](https://web.dev/articles/cls)
- [Performance skill](../performance/SKILL.md)