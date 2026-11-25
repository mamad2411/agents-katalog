---
name: html-first
description: Produz artefatos HTML auto-contidos (single-file) quando a tarefa se beneficia estruturalmente de layout espacial, cor, diagramas reais, interatividade ou edição round-trip — em vez de Markdown linear. Use SEMPRE que o usuário pedir planos de implementação, comparações lado-a-lado, code reviews/PRs, explainers conceituais, status reports, post-mortems, slide decks, diagramas de arquitetura/sequência/deploy, design systems, mockups de UI, prototipação de animações ou "micro-editores descartáveis" — mesmo que ele não mencione HTML explicitamente. Use também quando o output for longo (>100 linhas de conteúdo), precisar ser compartilhado fora do chat, ou exigir SVG/charts/diagramas que Markdown só conseguiria simular com ASCII. NÃO use para respostas curtas conversacionais, snippets de código, comandos de terminal, ou conteúdo que cabe naturalmente em 1-2 parágrafos.
---

# html-first

Skill para produzir artefatos HTML auto-contidos (single-file `.html`) que **comunicam melhor que Markdown** quando a tarefa carrega informação espacial, visual ou interativa. Operacionaliza a tese "HTML é o novo Markdown" de Thariq Shihipar (Claude Code team, Anthropic, maio/2026) **sem cair na armadilha da skill mecânica** que converte tudo em HTML.

## Princípio

Markdown é correto para: respostas conversacionais, snippets de código, listas curtas, comandos, terminal-style. **Não desfaça isso.**

HTML é correto quando a resposta carrega pelo menos um destes:

- **Espacialidade** — comparações lado-a-lado, módulos como caixas, diff em duas colunas, timelines
- **Cor com significado** — severidade, status, diff add/del, categoria
- **Diagrama de verdade** — SVG, não ASCII; arrow-key entre nodes, hover annotations
- **Interatividade** — sliders, toggles, drag-and-drop, copy buttons, live preview
- **Round-trip** — humano edita na UI → exporta JSON/Markdown → cola de volta no agente
- **Comprimento** — qualquer plano/report/explainer que vai passar de ~100 linhas e provavelmente não será lido se for Markdown

A heurística operacional: **"este artefato seria lido com mais atenção, ou compartilhado com alguém, se fosse uma página em vez de um arquivo `.md`?"** Se sim, HTML.

## Reconhecimento — quando disparar

Use HTML por padrão quando o usuário pedir qualquer um dos seguintes (mesmo sem mencionar HTML):

| Sinal no pedido | Categoria | Reference a carregar |
|---|---|---|
| "compare X abordagens", "três opções", "lado a lado", "trade-offs" | Exploration | `references/01-exploration-planning.md` |
| "plano de implementação", "como vou implementar", "spec", "design doc" | Planning | `references/01-exploration-planning.md` |
| "revise esse PR", "explica essa mudança", "code review" | Code Review | `references/02-code-review.md` |
| "entenda esse módulo", "mapa do código", "como funciona X no codebase" | Code Understanding | `references/02-code-review.md` |
| "design system", "componentes", "mockup", "variantes", "protótipo" | Design | `references/03-design-prototype.md` |
| "animação", "transição", "feel da interação" | Prototyping | `references/03-design-prototype.md` |
| "diagrama", "fluxograma", "arquitetura", "sequência", "deploy pipeline" | Diagrams | `references/04-diagrams-svg.md` |
| "explica conceito X", "tutorial", "como funciona Y" | Research/Learning | `references/05-reports-research.md` |
| "status report", "weekly", "post-mortem", "incident report" | Reports | `references/05-reports-research.md` |
| "deck", "slides", "apresentação" | Decks | `references/06-decks.md` |
| "editor pra X", "triagem", "drag and drop", "ajuste tunável" | Custom Editor | `references/07-custom-editors.md` |
| Pedidos de GenAI: agent flow, RAG, prompt comparison | Especial GenAI | `references/04-diagrams-svg.md` + `references/07-custom-editors.md` |
| Pedidos de Cloud/K8s: arquitetura, topologia, blast radius | Especial Infra | `references/04-diagrams-svg.md` |

## Carve-outs — quando NÃO disparar

Mantenha Markdown ou prosa simples quando:

- A resposta cabe em ≤2 parágrafos curtos
- O usuário está em uma conversa rápida ("qual o comando pra...", "o que significa Y")
- O output é primariamente código (entregue o código com formatação Markdown normal)
- O usuário pediu explicitamente Markdown, texto, ou um formato específico
- O artefato vai para terminal/CLI (ex: agent rule files, configs)
- O usuário está iterando rapidamente — fluxo de chat funciona melhor

**Quando em dúvida**, ofereça: "Posso entregar isso em prosa, ou montar um HTML auto-contido que você pode abrir/compartilhar — qual prefere?"

## Regras universais para todo artefato HTML

Toda página gerada por esta skill respeita estas regras, **independente da categoria**:

### 1. Single-file, auto-contido

- Todo CSS inline em `<style>`, todo JS inline em `<script>` no fim do `<body>`
- Sem dependências externas obrigatórias (CDN). Se for inevitável, prefira CDN com SRI ou inline o subset usado
- Imagens via SVG inline ou data-URI. Sem dependência de arquivos locais que quebram o "abrir no browser"
- O arquivo precisa rodar com `open arquivo.html` sem servidor

### 2. Mobile-responsive por default

- `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Layout em CSS Grid/Flexbox com `minmax()` e breakpoints simples
- Texto fluido com `clamp()` quando fizer sentido
- Touch targets ≥44px em elementos interativos

### 3. Acessibilidade não-negociável

- HTML semântico (`<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`)
- Contraste mínimo WCAG AA (4.5:1 para texto normal)
- `aria-label` em controles sem texto visível
- Foco visível em interativos
- `prefers-reduced-motion` respeitado em animações

### 4. Sem "default AI aesthetic"

Anti-padrões a evitar ativamente (eles imediatamente sinalizam "isso saiu de um LLM sem cuidado"):

- ❌ Gradientes purple → blue de fundo
- ❌ Quatro tons de indigo (#6366f1 e variantes)
- ❌ Glassmorphism gratuito (`backdrop-filter: blur`)
- ❌ Headers com emoji decorativo (`✨ Visão Geral`)
- ❌ Cards com `border-radius: 1rem` + sombra suave + tudo igual
- ❌ Tailwind-feel sem motivo (cada elemento com 12 classes utility)
- ❌ Dark mode "ficou bonito" com `#1a1a2e` de fundo e neon

Em vez disso, parta do baseline tipográfico em `references/08-design-tokens.md` e **só desvie quando o conteúdo exigir**.

### 5. Respeite o design system do projeto, se existir

Antes de partir do zero, verifique se o projeto tem um `design_system.html`, `tokens.css`, `theme.json`, ou similar. Se sim, **use-os**. Se não, ofereça extrair um do codebase (ver `references/09-design-system-extraction.md`) na primeira vez que o usuário pedir múltiplos artefatos relacionados.

### 6. Round-trip first em editores

Qualquer artefato com componente editável (forms, drags, toggles, sliders) **obrigatoriamente** termina com botão de export — "Copy as JSON", "Copy as Markdown", "Download diff". O loop é: agente gera UI → humano edita → exporta → cola no próximo prompt. Sem export, a UI é beco sem saída.

### 7. Saída para o sistema de arquivos

- Salve em `outputs/<slug>.html` (ou onde o ambiente determinar — em Claude Code: workspace; em claude.ai: `/mnt/user-data/outputs/`)
- `slug` deve ser descritivo (`implementation-plan-auth-refactor.html`, não `output.html`)
- Após salvar, presente o arquivo ao usuário com instrução de "abrir no browser" — não cole o HTML inline na conversa

## Workflow recomendado

Para tarefas não-triviais (planos, reviews, explainers grandes), prefira **uma teia de arquivos** a um arquivo monolítico:

```
trabalho-X/
├── 01-explorations.html       (3-6 abordagens lado-a-lado)
├── 02-mockups.html            (UI variations da abordagem escolhida)
├── 03-implementation-plan.html (timeline + diagrams + risk table)
└── 04-design-system.html      (tokens/components reutilizáveis)
```

Cada arquivo é digerível sozinho. Em sessões futuras, passe-os como contexto pro agente — ele lê mais informação útil de um HTML rico do que de qualquer Markdown de tamanho equivalente.

## Templates disponíveis

Em `templates/` há esqueletos prontos. Use como ponto de partida, **adapte ao conteúdo** — não force o conteúdo no template:

- `_base.html` — esqueleto mínimo com tokens, reset, responsivo, dark mode opcional
- `comparison-grid.html` — 2-6 opções lado-a-lado, com trade-offs
- `implementation-plan.html` — timeline + mockups + code excerpts + risk table
- `pr-review.html` — diff anotado + margin notes + severity tags
- `status-report.html` — what shipped / what slipped / metrics chart
- `concept-explainer.html` — TL;DR + collapsibles + glossary hover
- `slide-deck.html` — `<section>` + arrow-key navigation + speaker notes (escondidos)
- `custom-editor.html` — esqueleto com toggle/drag/form + botão "copy as JSON/Markdown"

Carregue só o(s) template(s) e reference(s) relevante(s) — não leia tudo de uma vez.

## Pattern de prompt → output

Quando o usuário pede algo que dispara esta skill, **antes de gerar o HTML**:

1. **Confirme a categoria** mentalmente (Exploration? Code Review? Report?)
2. **Leia a reference da categoria** (uma só, ou duas se for híbrido)
3. **Leia o template correspondente** (se houver)
4. **Decida o slug do arquivo**
5. **Gere o HTML** seguindo regras universais + reference da categoria
6. **Salve em outputs/** e **apresente** com o caminho

Não gere o HTML "pra prévia" no chat antes de salvar — vai duplicar tokens e poluir o contexto. Direto para o arquivo.

## Sinais que indicam acerto

Bons artefatos desta skill:

- Cabem em **um arquivo `.html`** que abre direto no browser
- São **navegáveis em 30 segundos** (anchors, tabs, ou TOC fixo)
- Funcionam **mobile e desktop** sem ajuste manual
- Têm **um propósito claro** por página — não tentam ser app, blog e dashboard ao mesmo tempo
- Em editores: **exportam de volta** pro fluxo do agente
- Não parecem **default AI aesthetic** (ver lista de anti-padrões)
- Um colega olhando por 5 segundos entende **o que é** e **onde clicar**

## Quando o usuário pedir explicitamente Markdown

Respeite. Não argumente. Markdown ainda é a melhor escolha em vários casos — esta skill é sobre reconhecer os casos em que **não é**.

## Sobre o aviso original do autor da tese

Thariq escreveu, no post original:

> *"I'm a little bit afraid that people will read this article and turn it into a /html skill or something. While there might be some value in that, I want to emphasize that you don't need to do much to get Claude to do this."*

Esta skill **não** é um "/html sempre". É um curador que reconhece *quando* HTML compete em vantagem clara, aplica padrões testados por categoria, e ativamente se segura de cair em estética padronizada de LLM. Se o output desta skill começar a parecer genérico, o problema está nesta skill — abra e ajuste os templates e tokens.

---

**Próximos passos para Claude usando esta skill:**

1. Detecte a categoria a partir do pedido do usuário (use a tabela de reconhecimento)
2. Verifique carve-outs — talvez Markdown seja melhor
3. Carregue `references/0X-categoria.md` correspondente
4. Carregue `templates/categoria.html` se houver
5. Gere o artefato seguindo regras universais + padrões da categoria
6. Salve em `outputs/<slug>.html` e apresente
