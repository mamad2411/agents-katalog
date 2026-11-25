---
name: web-performance-optimization
description: "Otimize website e web application performance incluindo velocidade de carregamento, Core Web Vitals, tamanho de bundle, estratégias de cache e performance em runtime"
---

# Otimização de Performance Web

## Visão Geral

Ajude desenvolvedores a otimizar a performance de websites e web applications para melhorar a experiência do usuário, rankings em SEO e taxas de conversão. Esta skill fornece abordagens sistemáticas para medir, analisar e melhorar a velocidade de carregamento, performance em runtime e métricas de Core Web Vitals.

## Quando Usar Esta Skill

- Use quando website ou app está carregando lentamente
- Use ao otimizar para Core Web Vitals (LCP, FID, CLS)
- Use ao reduzir tamanho de JavaScript bundle
- Use ao melhorar Time to Interactive (TTI)
- Use ao otimizar imagens e assets
- Use ao implementar estratégias de cache
- Use ao debugar gargalos de performance
- Use ao se preparar para auditorias de performance

## Como Funciona

### Passo 1: Medir Performance Atual

Vou ajudar você a estabelecer métricas de baseline:
- Executar auditorias Lighthouse
- Medir Core Web Vitals (LCP, FID, CLS)
- Verificar tamanhos de bundle
- Analisar waterfall de rede
- Identificar gargalos de performance

### Passo 2: Identificar Problemas

Analisar problemas de performance:
- JavaScript bundles grandes
- Imagens não otimizadas
- Recursos que bloqueiam renderização
- Tempos de resposta de servidor lentos
- Headers de cache ausentes
- Layout shifts
- Long tasks bloqueando main thread

### Passo 3: Priorizar Otimizações

Focar em melhorias de alto impacto:
- Otimização do critical rendering path
- Code splitting e lazy loading
- Otimização de imagens
- Estratégias de cache
- Otimização de scripts de terceiros

### Passo 4: Implementar Otimizações

Aplicar melhorias de performance:
- Otimizar assets (imagens, fontes, CSS, JS)
- Implementar code splitting
- Adicionar headers de cache
- Lazy load de recursos não-críticos
- Otimizar critical rendering path

### Passo 5: Verificar Melhorias

Medir impacto das mudanças:
- Re-executar auditorias Lighthouse
- Comparar métricas antes/depois
- Monitorar métricas de usuários reais (RUM)
- Testar em diferentes dispositivos e redes

## Exemplos

### Exemplo 1: Otimizando Core Web Vitals

```markdown
## Resultados da Auditoria de Performance

### Métricas Atuais (Antes da Otimização)
- **LCP (Largest Contentful Paint):** 4.2s ❌ (deve ser < 2.5s)
- **FID (First Input Delay):** 180ms ❌ (deve ser < 100ms)
- **CLS (Cumulative Layout Shift):** 0.25 ❌ (deve ser < 0.1)
- **Lighthouse Score:** 62/100

### Problemas Identificados

1. **Problema LCP:** Hero image (2.5MB) carrega lentamente
2. **Problema FID:** JavaScript bundle grande (850KB) bloqueia main thread
3. **Problema CLS:** Imagens sem dimensões causam layout shifts

### Plano de Otimização

#### Corrigir LCP (Largest Contentful Paint)

**Problema:** Hero image é 2.5MB e carrega lentamente

**Soluções:**
\`\`\`html
<!-- Antes: imagem não otimizada -->
<img src="/hero.jpg" alt="Hero">

<!-- Depois: otimizado com formatos modernos -->
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img 
    src="/hero.jpg" 
    alt="Hero"
    width="1200" 
    height="600"
    loading="eager"
    fetchpriority="high"
  >
</picture>
\`\`\`

**Otimizações adicionais:**
- Comprimir imagem para < 200KB
- Usar CDN para entrega mais rápida
- Preload hero image: `<link rel="preload" as="image" href="/hero.avif">`

#### Corrigir FID (First Input Delay)

**Problema:** JavaScript bundle de 850KB bloqueia main thread

**Soluções:**

1. **Code Splitting:**
\`\`\`javascript
// Antes: tudo em um bundle
import { HeavyComponent } from './HeavyComponent';
import { Analytics } from './analytics';
import { ChatWidget } from './chat';

// Depois: lazy load de código não-crítico
const HeavyComponent = lazy(() => import('./HeavyComponent'));
const ChatWidget = lazy(() => import('./chat'));

// Carrega analytics após página interativa
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    import('./analytics').then(({ Analytics }) => {
      Analytics.init();
    });
  });
}
\`\`\`

2. **Remover Dependências Não Usadas:**
\`\`\`bash
# Analisar bundle
npx webpack-bundle-analyzer

# Remover pacotes não usados
npm uninstall moment  # Usar date-fns em vez disso (menor)
npm install date-fns
\`\`\`

3. **Adiar Scripts Não-Críticos:**
\`\`\`html
<!-- Antes: bloqueia renderização -->
<script src="/analytics.js"></script>

<!-- Depois: adiado -->
<script src="/analytics.js" defer></script>
\`\`\`

#### Corrigir CLS (Cumulative Layout Shift)

**Problema:** Imagens sem dimensões causam layout shifts

**Soluções:**
\`\`\`html
<!-- Antes: sem dimensões -->
<img src="/product.jpg" alt="Product">

<!-- Depois: com dimensões -->
<img 
  src="/product.jpg" 
  alt="Product"
  width="400" 
  height="300"
  style="aspect-ratio: 4/3;"
>
\`\`\`

**Para conteúdo dinâmico:**
\`\`\`css
/* Reservar espaço para conteúdo que carrega depois */
.skeleton-loader {
  min-height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
\`\`\`

### Resultados Após Otimização

- **LCP:** 1.8s ✅ (melhorado em 57%)
- **FID:** 45ms ✅ (melhorado em 75%)
- **CLS:** 0.05 ✅ (melhorado em 80%)
- **Lighthouse Score:** 94/100 ✅
```

### Exemplo 2: Reduzindo Tamanho do JavaScript Bundle

```markdown
## Otimização de Tamanho de Bundle

### Estado Atual
- **Total Bundle:** 850KB (gzipped: 280KB)
- **Main Bundle:** 650KB
- **Vendor Bundle:** 200KB
- **Tempo de Carregamento (3G):** 8.2s

### Análise

\`\`\`bash
# Analisar composição do bundle
npx webpack-bundle-analyzer dist/stats.json
\`\`\`

**Descobertas:**
1. Moment.js: 67KB (pode substituir por date-fns: 12KB)
2. Lodash: 72KB (usando biblioteca inteira, precisa apenas de 5 funções)
3. Código não usado: ~150KB de dead code
4. Sem code splitting: tudo em um único bundle

### Passos de Otimização

#### 1. Substituir Dependências Pesadas

\`\`\`bash
# Remover moment.js (67KB) → Usar date-fns (12KB)
npm uninstall moment
npm install date-fns

# Antes
import moment from 'moment';
const formatted = moment(date).format('YYYY-MM-DD');

# Depois
import { format } from 'date-fns';
const formatted = format(date, 'yyyy-MM-dd');
\`\`\`

**Economia:** 55KB

#### 2. Usar Lodash Seletivamente

\`\`\`javascript
// Antes: importar biblioteca inteira (72KB)
import _ from 'lodash';
const unique = _.uniq(array);

// Depois: importar apenas o que precisa (5KB)
import uniq from 'lodash/uniq';
const unique = uniq(array);

// Ou usar métodos nativos
const unique = [...new Set(array)];
\`\`\`

**Economia:** 67KB

#### 3. Implementar Code Splitting

\`\`\`javascript
// Exemplo Next.js
import dynamic from 'next/dynamic';

// Lazy load de componentes pesados
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <div>Carregando gráfico...</div>,
  ssr: false
});

const AdminPanel = dynamic(() => import('./AdminPanel'), {
  loading: () => <div>Carregando...</div>
});

// Code splitting baseado em rota (automático no Next.js)
// pages/admin.js - Carregado apenas ao visitar /admin
// pages/dashboard.js - Carregado apenas ao visitar /dashboard
\`\`\`

#### 4. Remover Dead Code

\`\`\`javascript
// Habilitar tree shaking em webpack.config.js
module.exports = {
  mode: 'production',
  optimization: {
    usedExports: true,
    sideEffects: false
  }
};

// Em package.json
{
  "sideEffects": false
}
\`\`\`

#### 5. Otimizar Scripts de Terceiros

\`\`\`html
<!-- Antes: carrega imediatamente -->
<script src="https://analytics.com/script.js"></script>

<!-- Depois: carrega após página interativa -->
<script>
  window.addEventListener('load', () => {
    const script = document.createElement('script');
    script.src = 'https://analytics.com/script.js';
    script.async = true;
    document.body.appendChild(script);
  });
</script>
\`\`\`

### Resultados

- **Total Bundle:** 380KB ✅ (reduzido em 55%)
- **Main Bundle:** 180KB ✅
- **Vendor Bundle:** 80KB ✅
- **Tempo de Carregamento (3G):** 3.1s ✅ (melhorado em 62%)
```

### Exemplo 3: Estratégia de Otimização de Imagens

```markdown
## Otimização de Imagens

### Problemas Atuais
- 15 imagens totalizando 12MB
- Sem formatos modernos (WebP, AVIF)
- Sem imagens responsivas
- Sem lazy loading

### Estratégia de Otimização

#### 1. Converter para Formatos Modernos

\`\`\`bash
# Instalar ferramentas de otimização de imagens
npm install sharp

# Script de conversão (optimize-images.js)
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

async function optimizeImage(inputPath, outputDir) {
  const filename = path.basename(inputPath, path.extname(inputPath));
  
  // Gerar WebP
  await sharp(inputPath)
    .webp({ quality: 80 })
    .toFile(path.join(outputDir, \`\${filename}.webp\`));
  
  // Gerar AVIF (melhor compressão)
  await sharp(inputPath)
    .avif({ quality: 70 })
    .toFile(path.join(outputDir, \`\${filename}.avif\`));
  
  // Gerar JPEG otimizado como fallback
  await sharp(inputPath)
    .jpeg({ quality: 80, progressive: true })
    .toFile(path.join(outputDir, \`\${filename}.jpg\`));
}

// Processar todas as imagens
const images = fs.readdirSync('./images');
images.forEach(img => {
  optimizeImage(\`./images/\${img}\`, './images/optimized');
});
\`\`\`

#### 2. Implementar Imagens Responsivas

\`\`\`html
<!-- Imagens responsivas com formatos modernos -->
<picture>
  <!-- AVIF para navegadores que suportam (melhor compressão) -->
  <source 
    srcset="
      /images/hero-400.avif 400w,
      /images/hero-800.avif 800w,
      /images/hero-1200.avif 1200w
    "
    type="image/avif"
    sizes="(max-width: 768px) 100vw, 50vw"
  >
  
  <!-- WebP para navegadores que suportam -->
  <source 
    srcset="
      /images/hero-400.webp 400w,
      /images/hero-800.webp 800w,
      /images/hero-1200.webp 1200w
    "
    type="image/webp"
    sizes="(max-width: 768px) 100vw, 50vw"
  >
  
  <!-- JPEG como fallback -->
  <img 
    src="/images/hero-800.jpg"
    srcset="
      /images/hero-400.jpg 400w,
      /images/hero-800.jpg 800w,
      /images/hero-1200.jpg 1200w
    "
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="Imagem hero"
    width="1200"
    height="600"
    loading="lazy"
  >
</picture>
\`\`\`

#### 3. Lazy Loading

\`\`\`html
<!-- Native lazy loading -->
<img 
  src="/image.jpg" 
  alt="Descrição"
  loading="lazy"
  width="800"
  height="600"
>

<!-- Eager loading para imagens acima da dobra -->
<img 
  src="/hero.jpg" 
  alt="Hero"
  loading="eager"
  fetchpriority="high"
>
\`\`\`

#### 4. Componente Image do Next.js

\`\`\`javascript
import Image from 'next/image';

// Otimização automática
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // Para imagens acima da dobra
  quality={80}
/>

// Lazy loaded
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
  loading="lazy"
/>
\`\`\`

### Resultados

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Tamanho Total de Imagens | 12MB | 1.8MB | 85% redução |
| LCP | 4.5s | 1.6s | 64% mais rápido |
| Carregamento de Página (3G) | 18s | 4.2s | 77% mais rápido |
```

## Melhores Práticas

### ✅ Faça Isto

- **Medir Primeiro** - Sempre estabeleça métricas de baseline antes de otimizar
- **Usar Lighthouse** - Execute auditorias regularmente para acompanhar progresso
- **Otimizar Imagens** - Use formatos modernos (WebP, AVIF) e imagens responsivas
- **Code Split** - Divida bundles grandes em chunks menores
- **Lazy Load** - Adie o carregamento de recursos não-críticos
- **Cache Agressivamente** - Defina headers de cache apropriados para assets estáticos
- **Minimizar Trabalho da Main Thread** - Mantenha execução de JavaScript em chunks < 50ms
- **Preload de Recursos Críticos** - Use `<link rel="preload">` para assets críticos
- **Usar CDN** - Sirva assets estáticos de CDN para entrega mais rápida
- **Monitorar Usuários Reais** - Rastreie Core Web Vitals de usuários reais

### ❌ Não Faça Isto

- **Não Otimize Cegamente** - Meça primeiro, depois otimize
- **Não Ignore Mobile** - Teste em dispositivos móveis reais e redes lentas
- **Não Bloqueie Renderização** - Evite CSS e JavaScript que bloqueiam renderização
- **Não Carregue Tudo de Uma Vez** - Lazy load de recursos não-críticos
- **Não Esqueça Dimensões** - Sempre especifique width/height em imagens
- **Não Use Scripts Síncronos** - Use atributos async ou defer
- **Não Ignore Scripts de Terceiros** - Eles frequentemente causam problemas de performance
- **Não Pule Compressão** - Sempre comprima e minifique assets

## Armadilhas Comuns

### Problema: Otimizado para Desktop mas Lento em Mobile
**Sintomas:** Bom score Lighthouse no desktop, ruim no mobile
**Solução:**
- Teste em dispositivos móveis reais
- Use throttling de mobile em Chrome DevTools
- Otimize para redes 3G/4G
- Reduza tempo de execução de JavaScript
```bash
# Testar com throttling
lighthouse https://yoursite.com --throttling.cpuSlowdownMultiplier=4
```

### Problema: JavaScript Bundle Grande
**Sintomas:** Time to Interactive (TTI) longo, FID alto
**Solução:**
- Analise bundle com webpack-bundle-analyzer
- Remova dependências não usadas
- Implemente code splitting
- Lazy load de código não-crítico
```bash
# Analisar bundle
npx webpack-bundle-analyzer dist/stats.json
```

### Problema: Imagens Causando Layout Shifts
**Sintomas:** CLS score alto, conteúdo pulando
**Solução:**
- Sempre especifique width e height
- Use propriedade CSS aspect-ratio
- Reserve espaço com skeleton loaders
```css
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}
```

### Problema: Tempo de Resposta de Servidor Lento
**Sintomas:** TTFB alto (Time to First Byte)
**Solução:**
- Implemente cache no servidor
- Use CDN para assets estáticos
- Otimize queries de banco de dados
- Considere static site generation (SSG)
```javascript
// Next.js: static generation
export async function getStaticProps() {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 60 // Regenerar a cada 60 segundos
  };
}
```

## Checklist de Performance

### Imagens
- [ ] Converter para formatos modernos (WebP, AVIF)
- [ ] Implementar imagens responsivas
- [ ] Adicionar lazy loading
- [ ] Especificar dimensões (width/height)
- [ ] Comprimir imagens (< 200KB cada)
- [ ] Usar CDN para entrega

### JavaScript
- [ ] Tamanho de bundle < 200KB (gzipped)
- [ ] Implementar code splitting
- [ ] Lazy load de código não-crítico
- [ ] Remover dependências não usadas
- [ ] Minificar e comprimir
- [ ] Usar async/defer para scripts

### CSS
- [ ] Inlinar CSS crítico
- [ ] Adiar CSS não-crítico
- [ ] Remover CSS não usado
- [ ] Minificar arquivos CSS
- [ ] Usar CSS containment

### Cache
- [ ] Definir headers de cache para assets estáticos
- [ ] Implementar service worker
- [ ] Usar cache de CDN
- [ ] Cachear respostas de API
- [ ] Versionar assets estáticos

### Core Web Vitals
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] TTFB < 600ms
- [ ] TTI < 3.8s

## Ferramentas de Performance

### Ferramentas de Medição
- **Lighthouse** - Auditoria abrangente de performance
- **WebPageTest** - Análise detalhada de waterfall
- **Chrome DevTools** - Profiling de performance
- **PageSpeed Insights** - Métricas de usuários reais
- **Web Vitals Extension** - Monitorar Core Web Vitals

### Ferramentas de Análise
- **webpack-bundle-analyzer** - Visualizar composição de bundle
- **source-map-explorer** - Analisar tamanho de bundle
- **Bundlephobia** - Verificar tamanho de pacotes antes de instalar
- **ImageOptim** - Ferramenta de compressão de imagens

### Ferramentas de Monitoramento
- **Google Analytics** - Rastrear Core Web Vitals
- **Sentry** - Monitoramento de performance
- **New Relic** - Monitoramento de performance de aplicação
- **Datadog** - Real user monitoring

## Skills Relacionadas

- `@react-best-practices` - Padrões de performance React
- `@frontend-dev-guidelines` - Padrões de desenvolvimento frontend
- `@systematic-debugging` - Debugar problemas de performance
- `@senior-architect` - Arquitetura para performance

## Recursos Adicionais

- [Web.dev Performance](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Documentação Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Guia de Performance MDN](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [Performance Next.js](https://nextjs.org/docs/advanced-features/measuring-performance)
- [Guia de Otimização de Imagens](https://web.dev/fast/#optimize-your-images)

---

**Dica Profissional:** Foque primeiro em Core Web Vitals (LCP, FID, CLS) - eles têm o maior impacto na experiência do usuário e rankings de SEO!