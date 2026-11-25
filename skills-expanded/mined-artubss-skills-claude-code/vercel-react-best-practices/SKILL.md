---
name: vercel-react-best-practices
description: Diretrizes de otimização de desempenho para React e Next.js da Vercel Engineering. Esta skill deve ser utilizada ao escrever, revisar ou refatorar código React/Next.js para garantir padrões de desempenho ideal. Dispara em tarefas envolvendo componentes React, páginas Next.js, busca de dados, otimização de bundle ou melhorias de desempenho.
---

# Vercel React Best Practices

Guia abrangente de otimização de desempenho para aplicações React e Next.js, mantido pela Vercel. Contém 45 regras distribuídas em 8 categorias, priorizadas por impacto para orientar refatoração automatizada e geração de código.

## Quando Aplicar

Consulte estas diretrizes quando:
- Escrever novos componentes React ou páginas Next.js
- Implementar busca de dados (lado do cliente ou servidor)
- Revisar código quanto a problemas de desempenho
- Refatorar código React/Next.js existente
- Otimizar tamanho de bundle ou tempos de carregamento

## Categorias de Regras por Prioridade

| Prioridade | Categoria | Impacto | Prefixo |
|----------|----------|--------|--------|
| 1 | Eliminando Waterfalls | CRÍTICO | `async-` |
| 2 | Otimização de Bundle | CRÍTICO | `bundle-` |
| 3 | Desempenho do Lado do Servidor | ALTO | `server-` |
| 4 | Busca de Dados do Lado do Cliente | MÉDIO-ALTO | `client-` |
| 5 | Otimização de Re-render | MÉDIO | `rerender-` |
| 6 | Desempenho de Renderização | MÉDIO | `rendering-` |
| 7 | Desempenho de JavaScript | BAIXO-MÉDIO | `js-` |
| 8 | Padrões Avançados | BAIXO | `advanced-` |

## Referência Rápida

### 1. Eliminando Waterfalls (CRÍTICO)

- `async-defer-await` - Mova await para ramificações onde realmente é usado
- `async-parallel` - Use Promise.all() para operações independentes
- `async-dependencies` - Use better-all para dependências parciais
- `async-api-routes` - Inicie promises cedo, await tarde em rotas de API
- `async-suspense-boundaries` - Use Suspense para fazer stream de conteúdo

### 2. Otimização de Bundle (CRÍTICO)

- `bundle-barrel-imports` - Importe diretamente, evite barrel files
- `bundle-dynamic-imports` - Use next/dynamic para componentes pesados
- `bundle-defer-third-party` - Carregue analytics/logging após hidratação
- `bundle-conditional` - Carregue módulos apenas quando o recurso é ativado
- `bundle-preload` - Pré-carregue ao passar mouse/foco para velocidade percebida

### 3. Desempenho do Lado do Servidor (ALTO)

- `server-cache-react` - Use React.cache() para deduplicação por requisição
- `server-cache-lru` - Use cache LRU para cache entre requisições
- `server-serialization` - Minimize dados passados para componentes cliente
- `server-parallel-fetching` - Reestruture componentes para paralelizar buscas
- `server-after-nonblocking` - Use after() para operações não-bloqueantes

### 4. Busca de Dados do Lado do Cliente (MÉDIO-ALTO)

- `client-swr-dedup` - Use SWR para deduplicação automática de requisições
- `client-event-listeners` - Deduplicar event listeners globais

### 5. Otimização de Re-render (MÉDIO)

- `rerender-defer-reads` - Não se inscreva em estado usado apenas em callbacks
- `rerender-memo` - Extraia trabalho caro em componentes memoizados
- `rerender-dependencies` - Use dependências primitivas em effects
- `rerender-derived-state` - Inscreva-se em booleanos derivados, não valores brutos
- `rerender-functional-setstate` - Use setState funcional para callbacks estáveis
- `rerender-lazy-state-init` - Passe função para useState em valores caros
- `rerender-transitions` - Use startTransition para atualizações não-urgentes

### 6. Desempenho de Renderização (MÉDIO)

- `rendering-animate-svg-wrapper` - Anime div wrapper, não elemento SVG
- `rendering-content-visibility` - Use content-visibility para listas longas
- `rendering-hoist-jsx` - Extraia JSX estático fora de componentes
- `rendering-svg-precision` - Reduza precisão de coordenadas SVG
- `rendering-hydration-no-flicker` - Use script inline para dados apenas do cliente
- `rendering-activity` - Use componente Activity para mostrar/ocultar
- `rendering-conditional-render` - Use ternário, não && para condicionais

### 7. Desempenho de JavaScript (BAIXO-MÉDIO)

- `js-batch-dom-css` - Agrupe mudanças CSS via classes ou cssText
- `js-index-maps` - Construa Map para buscas repetidas
- `js-cache-property-access` - Cache propriedades de objeto em loops
- `js-cache-function-results` - Cache resultados de função em Map em nível de módulo
- `js-cache-storage` - Cache leituras de localStorage/sessionStorage
- `js-combine-iterations` - Combine múltiplos filter/map em um loop
- `js-length-check-first` - Verifique comprimento do array antes de comparação cara
- `js-early-exit` - Retorne cedo de funções
- `js-hoist-regexp` - Extraia criação de RegExp fora de loops
- `js-min-max-loop` - Use loop para min/max em vez de sort
- `js-set-map-lookups` - Use Set/Map para buscas O(1)
- `js-tosorted-immutable` - Use toSorted() para imutabilidade

### 8. Padrões Avançados (BAIXO)

- `advanced-event-handler-refs` - Armazene event handlers em refs
- `advanced-use-latest` - useLatest para refs de callback estáveis

## Como Usar

Leia arquivos de regra individuais para explicações detalhadas e exemplos de código:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Cada arquivo de regra contém:
- Breve explicação de por que importa
- Exemplo de código incorreto com explicação
- Exemplo de código correto com explicação
- Contexto adicional e referências

## Documento Compilado Completo

Para o guia completo com todas as regras expandidas: `AGENTS.md`