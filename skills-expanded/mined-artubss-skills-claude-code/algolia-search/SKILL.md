---
name: algolia-search
description: "Padrões especializados para implementação de busca Algolia, estratégias de indexação, React InstantSearch e ajuste de relevância. Use quando: adicionar busca, algolia, instantsearch, search api, funcionalidade de busca."
source: vibeship-spawner-skills (Apache 2.0)
---

# Integração Algolia Search

## Padrões

### React InstantSearch com Hooks

Setup moderno de React InstantSearch usando hooks para busca com autocompletar.

Usa pacote react-instantsearch-hooks-web com cliente algoliasearch.
Widgets são componentes que podem ser customizados com classnames.

Hooks principais:
- useSearchBox: Tratamento de entrada de busca
- useHits: Acesso aos resultados de busca
- useRefinementList: Filtragem por faceta
- usePagination: Paginação de resultados
- useInstantSearch: Acesso ao estado completo


### Next.js Server-Side Rendering

Integração SSR para Next.js com pacote react-instantsearch-nextjs.

Use <InstantSearchNext> em vez de <InstantSearch> para SSR.
Suporta Pages Router e App Router (experimental).

Considerações principais:
- Defina dynamic = 'force-dynamic' para resultados frescos
- Gerencie sincronização de URL com prop routing
- Use getServerState para estado inicial


### Sincronização de Dados e Indexação

Estratégias de indexação para manter Algolia sincronizado com seus dados.

Três abordagens principais:
1. Reindexação Completa - Substitui índice inteiro (caro)
2. Atualizações de Registro Completo - Substitui registros individuais
3. Atualizações Parciais - Atualiza apenas atributos específicos

Melhores práticas:
- Agrupe registros em lotes (ideal: 10MB, 1K-10K registros por lote)
- Use atualizações incrementais quando possível
- partialUpdateObjects para mudanças apenas de atributos
- Evite deleteBy (computacionalmente cara)


## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | crítica | Veja docs |
| Problema | alta | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |