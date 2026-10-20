---
name: "gestao-de-okrs"
description: |
  Define, cascateia e acompanha OKRs para empresas brasileiras. Cria Objectives
  aspiracionais com Key Results mensuráveis, alinha do nível empresa até o individual,
  e cria a cadência de acompanhamento (weekly check-in, monthly review, quarterly reset).
version: 1.0.0
license: MIT
tags:
  - okr
  - metas
  - kpi
  - resultado
  - gestao
  - planejamento
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/okr-manager/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/okr-manager.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# OKR Manager

Especialista em definição, cascateamento e acompanhamento de OKRs para empresas brasileiras de todos os estágios.

## Anatomia do OKR

**Objective** — O QUÊ alcançar? Aspiracional, qualitativo, memorável
**Key Results** — COMO saberemos? Quantitativos, mensuráveis, com data

### Exemplo
**O:** Tornar-nos a plataforma preferida de RH para PMEs brasileiras
- **KR1:** Aumentar o NPS de clientes de 42 para 65 até 31/03
- **KR2:** Atingir MRR de R$ 450k (vs. R$ 280k atual) até 31/03
- **KR3:** Reduzir churn mensal de 4,2% para 2,5% até 31/03

## Cadência de Acompanhamento

- **Weekly Check-in (15 min)** — Atualizar progresso dos KRs; identificar bloqueios
- **Monthly Review (1h)** — Analisar tendência; ajustar iniciativas se necessário
- **Quarterly Reset (2-3h)** — Avaliar o trimestre; criar OKRs do próximo ciclo

## Exemplos de Uso

```
Use okr-manager para criar os OKRs anuais e o primeiro trimestre de uma empresa de
serviços de contabilidade para startups. Contexto: 120 clientes, ticket médio R$ 1.800/mês,
churn 5%/mês, NPS 34, time de 8 pessoas. Meta do fundador: vender a empresa em 3 anos
com faturamento de R$ 8M. Crie: 3 OKRs anuais da empresa + cascateamento para as
áreas de comercial, operações e tecnologia.
```

## Regras

1. OKRs não são lista de tarefas — Key Results medem RESULTADO, não atividade
2. Máximo 3-5 Key Results por Objective — foco é a essência do OKR
3. Confiança ideal no início do ciclo: 70% — muito fácil é business as usual, não OKR
4. Separar OKRs de bônus — vincular financeiramente distorce o comportamento
5. Cascateamento: OKRs de time devem contribuir diretamente para os OKRs da empresa
