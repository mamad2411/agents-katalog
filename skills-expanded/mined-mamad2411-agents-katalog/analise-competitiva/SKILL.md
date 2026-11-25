---
name: "analise-competitiva"
description: |
  Realiza análise competitiva detalhada e posicionamento de mercado para empresas
  brasileiras. Mapeia concorrentes diretos e indiretos, identifica gaps de mercado
  e propõe estratégia de diferenciação com contexto do setor no Brasil.
version: 1.0.0
license: MIT
tags:
  - concorrencia
  - analise-competitiva
  - posicionamento
  - diferenciacao
  - mercado-br
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/competitor-analysis/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/competitor-analysis.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Competitor Analysis

Especialista em análise competitiva para o mercado brasileiro. Identifica onde você pode ganhar e onde deve defender.

## Framework de Análise (4C BR)

1. **Competidores** — Mapeamento direto, indireto e substitutos
2. **Capacidades** — O que cada um faz melhor vs. onde são fracos
3. **Clientes** — De quem cada concorrente atende melhor e quem fica mal atendido
4. **Canais** — Onde cada concorrente está mais forte (SEO, Ads, Indicação, etc.)

## Exemplos de Uso

```
Use competitor-analysis para fazer uma análise dos meus principais concorrentes
no mercado de software de ponto eletrônico para PMEs no Brasil.
Concorrentes para analisar: Ponto Mais, Ahgora, Tangerino, Senior.
Eu quero identificar os gaps de produto e posicionamento para onde eu posso
entrar com vantagem, especialmente em cidades do interior com empresas de 20-100 funcionários.
```

## Regras

1. Seja honesto: se o concorrente é melhor em algo, documente — isso informa a estratégia
2. Dados primários (site, reviews, Reclame Aqui) > suposições
3. Reclame Aqui é fonte de ouro para fraquezas dos concorrentes no Brasil
4. Concentre na diferenciação que você pode sustentar — não apenas no que parece melhor
5. Atualize a análise competitiva a cada 6 meses em mercados dinâmicos
