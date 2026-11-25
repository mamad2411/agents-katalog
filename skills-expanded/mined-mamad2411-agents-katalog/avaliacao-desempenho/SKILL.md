---
name: "avaliacao-desempenho"
description: |
  Cria templates de avaliação de desempenho 360°, PDI (Plano de Desenvolvimento
  Individual), calibração de notas e critérios de promoção para empresas brasileiras.
  Adapta ao contexto cultural BR com feedback construtivo e estruturado.
version: 1.0.0
license: MIT
tags:
  - avaliacao-desempenho
  - 360
  - pdi
  - feedback
  - promocao
  - calibracao
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/avaliacao-desempenho/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/avaliacao-desempenho.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Avaliação de Desempenho

Especialista em sistemas de avaliação de performance para empresas brasileiras. Cria processos justos, transparentes e que desenvolvem as pessoas.

## Tipos de Avaliação

- **Autoavaliação** — O colaborador avalia sua própria performance
- **Avaliação do Gestor** — O líder direto avalia entregas e comportamentos
- **Avaliação 360°** — Pares, liderados e stakeholders também avaliam
- **Calibração** — Reunião dos gestores para alinhar notas e evitar vieses
- **PDI** — Plano de desenvolvimento individual pós-avaliação

## Competências Comumente Avaliadas

- Qualidade das entregas (vs. metas/OKRs)
- Comunicação e colaboração
- Autonomia e iniciativa
- Aprendizado e adaptabilidade
- Liderança (para posições de gestão)
- Aderência aos valores da empresa

## Exemplos de Uso

```
Use avaliacao-desempenho para criar o formulário de avaliação semestral 360°
para uma empresa de tecnologia de 35 pessoas. Crie: formulário de autoavaliação
(10 perguntas), formulário para pares (6 perguntas) e guia do gestor para
calibração. Escala: 1-5 com descritor por nota. Inclua seção de PDI obrigatória.
```

## Regras

1. Avaliação de desempenho não deve ser surpresa — feedback contínuo em 1:1s previne isso
2. Calibração é obrigatória para evitar gestores muito generosos ou muito rigorosos
3. PDI sem recursos e tempo alocado para o desenvolvimento é promessa vazia
4. Vincular avaliação a PLR ou promoção requer critérios cristalinos ANTES do ciclo
5. No Brasil, avaliação negativa sem histórico documentado pode gerar questionamentos em demissão por justa causa
