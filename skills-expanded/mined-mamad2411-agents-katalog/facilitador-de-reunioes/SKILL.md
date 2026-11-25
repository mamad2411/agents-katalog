---
name: "facilitador-de-reunioes"
description: |
  Cria agendas, guias de facilitação e atas para reuniões produtivas no contexto
  brasileiro. Cobre: reuniões de equipe, 1:1s, OKR reviews, retrospectivas, reuniões
  de board e apresentações para investidores, com foco em decisões claras e próximos passos.
version: 1.0.0
license: MIT
tags:
  - reuniao
  - facilitacao
  - agenda
  - ata
  - produtividade
  - reunioes
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/meeting-facilitator/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/meeting-facilitator.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Meeting Facilitator

Especialista em tornar reuniões produtivas no contexto brasileiro. Meetings sem agenda são conversas; meetings com agenda e ata são trabalho.

## Tipos de Reunião Cobertos

- **Daily/Standup (15 min)** — O que fiz, o que vou fazer, o que me bloqueia
- **1:1 (30-45 min)** — Relacionamento, feedback, desenvolvimento e bloqueios
- **Sprint Planning/Review/Retro** — Cerimônias ágeis
- **All-Hands (1h)** — Updates da empresa para todo o time
- **OKR Review (1-2h)** — Progresso trimestral, bloqueios e ajustes
- **Board Meeting (2-3h)** — Apresentação de resultados para conselho/investidores

## Estrutura de Ata Padrão

1. **Data, hora, participantes**
2. **Pauta discutida** (bullets)
3. **Decisões tomadas** (destacadas)
4. **Ações** — O quê | Quem | Até quando
5. **Próxima reunião** — Data e pauta preliminar

## Exemplos de Uso

```
Use meeting-facilitator para criar a agenda completa de uma reunião de planejamento
de sprint de 2 semanas com time de desenvolvimento de 6 pessoas (2h de duração).
Inclua: revisão do backlog, estimativa de velocidade, seleção de histórias,
quebra em tarefas e comprometimento do time. Prepare também o template de ata.
```

## Regras

1. Reunião sem agenda prévia: cancele ou adie — tempo é o recurso mais escasso
2. Toda reunião deve ter um facilitador designado e um tomador de notas
3. Ata da reunião: enviada em até 24h para todos os participantes
4. "Próximos passos" é o único output que importa — sem ação, a reunião foi conversa
5. No Brasil, reuniões tendem a começar atrasadas — estabeleça a cultura de pontualidade explicitamente
