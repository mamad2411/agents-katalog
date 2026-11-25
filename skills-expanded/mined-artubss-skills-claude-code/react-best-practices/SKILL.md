---
name: react-best-practices
description: Guia abrangente de otimização de desempenho React e Next.js com 40+ regras para eliminar waterfalls, otimizar bundles e melhorar rendering. Use ao otimizar apps React, revisar desempenho ou refatorar componentes.
version: 1.0.0
author: Vercel Engineering
license: MIT
tags: [React, Next.js, Performance, Optimization, Best Practices, Bundle Size, Rendering, Server Components]
dependencies: []
---

# React Best Practices - Performance Optimization

Guia abrangente de otimização de desempenho para aplicações React e Next.js com 40+ regras organizadas por nível de impacto. Desenvolvido para ajudar desenvolvedores a eliminar gargalos de desempenho e seguir as melhores práticas.

## Quando usar esta skill

**Use React Best Practices quando:**
- Otimizar desempenho de aplicações React ou Next.js
- Revisar código para melhorias de desempenho
- Refatorar componentes existentes para melhor desempenho
- Implementar novos recursos com desempenho em mente
- Debugar problemas de rendering lento ou carregamento lento
- Reduzir tamanho de bundle
- Eliminar request waterfalls

**Áreas principais cobertas:**
- **Eliminando Waterfalls** (CRÍTICO): Prevenir operações assíncronas sequenciais
- **Otimização de Bundle Size** (CRÍTICO): Reduzir payload inicial de JavaScript
- **Desempenho Server-Side** (ALTO): Otimizar RSC e data fetching
- **Client-Side Data Fetching** (MÉDIO-ALTO): Implementar cache eficiente
- **Otimização de Re-render** (MÉDIO): Minimizar re-renders desnecessários
- **Desempenho de Rendering** (MÉDIO): Otimizar rendering do navegador
- **Desempenho de JavaScript** (BAIXO-MÉDIO): Micro-otimizações para hot paths
- **Padrões Avançados** (BAIXO): Técnicas especializadas para casos extremos

## Referência rápida

### Prioridades críticas

1. **Defer await até quando necessário** - Mover awaits para branches onde são usados
2. **Usar Promise.all()** - Paralelizar operações assíncronas independentes
3. **Evitar barrel imports** - Importar diretamente de arquivos fonte
4. **Dynamic imports** - Lazy-load de componentes pesados
5. **Strategic Suspense** - Fazer streaming de conteúdo enquanto mostra layout

### Padrões comuns

**Parallel data fetching:**
```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

**Direct imports:**
```tsx
// ❌ Carrega toda a biblioteca
import { Check } from 'lucide-react'

// ✅ Carrega apenas o necessário
import Check from 'lucide-react/dist/esm/icons/check'
```

**Dynamic components:**
```tsx
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('./monaco-editor'),
  { ssr: false }
)
```

## Usando as diretrizes

As diretrizes completas de desempenho estão disponíveis na pasta references:

- **react-performance-guidelines.md**: Guia completo com todos os 40+ regras, exemplos de código e análise de impacto

Cada regra inclui:
- Comparações de código incorreto/correto
- Métricas de impacto específicas
- Quando aplicar a otimização
- Exemplos do mundo real

## Visão geral das categorias

### 1. Eliminando Waterfalls (CRÍTICO)
Waterfalls são o problema #1 de desempenho. Cada await sequencial adiciona latência de rede completa.
- Defer await até quando necessário
- Paralelização baseada em dependências
- Prevenir cadeias de waterfall em API routes
- Promise.all() para operações independentes
- Suspense boundaries estratégicos

### 2. Otimização de Bundle Size (CRÍTICO)
Reduzir tamanho de bundle inicial melhora Time to Interactive e Largest Contentful Paint.
- Evitar barrel file imports
- Carregamento de módulo condicional
- Defer de bibliotecas third-party não críticas
- Dynamic imports para componentes pesados
- Preload baseado na intenção do usuário

### 3. Desempenho Server-Side (ALTO)
Otimizar server-side rendering e data fetching.
- Cross-request LRU caching
- Minimizar serialização em RSC boundaries
- Parallel data fetching com composição de componentes
- Per-request deduplication com React.cache()

### 4. Client-Side Data Fetching (MÉDIO-ALTO)
Deduplicação automática e padrões eficientes de data fetching.
- Deduplicate global event listeners
- Usar SWR para deduplicação automática

### 5. Otimização de Re-render (MÉDIO)
Reduzir re-renders desnecessários para minimizar computação desperdiçada.
- Defer state reads para o ponto de uso
- Extrair para componentes memoizados
- Narrowing effect dependencies
- Subscribe to derived state
- Usar lazy state initialization
- Usar transitions para atualizações não urgentes

### 6. Desempenho de Rendering (MÉDIO)
Otimizar o processo de rendering do navegador.
- Animar SVG wrapper em vez de SVG element
- CSS content-visibility para listas longas
- Hoist static JSX elements
- Otimizar precisão de SVG
- Prevenir hydration mismatch sem flickering
- Usar Activity component para show/hide
- Usar explicit conditional rendering

### 7. Desempenho de JavaScript (BAIXO-MÉDIO)
Micro-otimizações para hot paths.
- Batch DOM CSS changes
- Construir mapas de índice para lookups repetidos
- Cache property access em loops
- Cache chamadas de função repetidas
- Cache storage API calls
- Combinar múltiplas iterações de array
- Early length check para comparações de array
- Early return de funções
- Hoist RegExp creation
- Usar loop para min/max em vez de sort
- Usar Set/Map para O(1) lookups
- Usar toSorted() em vez de sort()

### 8. Padrões Avançados (BAIXO)
Técnicas especializadas para casos extremos.
- Store event handlers em refs
- useLatest para stable callback refs

## Abordagem de implementação

Ao otimizar uma aplicação React:

1. **Profile primeiro**: Use React DevTools Profiler e ferramentas de performance do navegador para identificar gargalos
2. **Focar em critical paths**: Comece eliminando waterfalls e reduzindo bundle size
3. **Medir impacto**: Verificar melhorias com métricas (LCP, TTI, FID)
4. **Aplicar incrementalmente**: Não over-otimizar prematuramente
5. **Testar completamente**: Garantir que otimizações não quebrem funcionalidade

## Métricas principais para rastrear

- **Time to Interactive (TTI)**: Quando página fica totalmente interativa
- **Largest Contentful Paint (LCP)**: Quando conteúdo principal é visível
- **First Input Delay (FID)**: Responsividade para interações do usuário
- **Cumulative Layout Shift (CLS)**: Estabilidade visual
- **Bundle size**: Payload inicial de JavaScript
- **Server response time**: TTFB para conteúdo server-rendered

## Armadilhas comuns para evitar

❌ **Não faça:**
- Usar barrel imports de bibliotecas grandes
- Bloquear operações paralelas com awaits sequenciais
- Re-renderizar árvores inteiras quando apenas parte precisa atualizar
- Carregar analytics/tracking no critical path
- Mutar arrays com .sort() em vez de .toSorted()
- Criar RegExp ou objetos pesados dentro de render

✅ **Faça:**
- Importar diretamente de arquivos fonte
- Usar Promise.all() para operações independentes
- Memoizar componentes caros
- Lazy-load código não crítico
- Usar métodos imutáveis de array
- Hoist objetos estáticos fora de componentes

## Recursos

- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
- [SWR Documentation](https://swr.vercel.app)
- [Vercel Bundle Optimization](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
- [Vercel Dashboard Performance](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
- [better-all Library](https://github.com/shuding/better-all)
- [node-lru-cache](https://github.com/isaacs/node-lru-cache)

## Histórico de versão

**v0.1.0** (Janeiro 2026)
- Lançamento inicial do Vercel Engineering
- 40+ regras de desempenho em 8 categorias
- Exemplos de código abrangentes e análise de impacto