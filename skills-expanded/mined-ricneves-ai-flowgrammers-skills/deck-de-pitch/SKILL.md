---
name: "deck-de-pitch"
description: |
  Estrutura e escreve o conteúdo de apresentações de vendas, pitch para investidores
  e apresentações de board com contexto do ecossistema brasileiro. Inclui narrativa,
  dados de mercado BR e estrutura para cada tipo de audiência.
version: 1.0.0
license: MIT
tags:
  - pitch
  - deck
  - investidores
  - apresentacao
  - startup
  - board
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/pitch-deck/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/pitch-deck.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Pitch Deck

Especialista em estruturar o conteúdo de apresentações de alto impacto para o mercado brasileiro. Desde pitch de 3 minutos para investidores anjo até apresentação de 45 minutos para board.

## Estruturas por Tipo

### Pitch para Investidores (10-12 slides)
Problema → Solução → Mercado → Produto → Tração → Modelo de Negócio → Time → Competição → Financeiras → Rodada

### Apresentação de Vendas B2B (15-20 slides)
Diagnóstico do cliente → Contexto de mercado → Problema amplificado → Nossa solução → Como funciona → Cases → ROI esperado → Investimento → Próximos passos

### Pitch de 3 Minutos (Demo Day)
Gancho → Problema (1 slide) → Solução (1 slide) → Tração (1 número) → Time → CTA

## Exemplos de Uso

```
Use pitch-deck para estruturar um pitch de captação de R$ 2M para uma
proptech de gestão de aluguel por temporada. Tração: 450 imóveis ativos,
GMV R$ 1,2M/mês, crescimento 15% ao mês. Rodada: Série Pré-Seed.
Prepare o conteúdo de cada slide com mensagem principal e dados de suporte.
```

## Regras

1. Um slide = uma mensagem — não sobrecarregue visualmente
2. Investidores BR querem ver: TAM em R$, tração real, time com skin in the game
3. Nunca projetar crescimento sem base de cálculo demonstrável
4. Demo day: pratique para 3 minutos — o tempo acaba mais rápido que parece
5. Pitch deck de vendas: comece com o problema do cliente, não com sua empresa
