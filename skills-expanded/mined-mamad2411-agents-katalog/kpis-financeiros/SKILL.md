---
name: "kpis-financeiros"
description: |
  Calcula e analisa KPIs financeiros para empresas brasileiras: LTV, CAC, MRR,
  ARR, churn, payback, margem, ROI e NRR. Compara com benchmarks do mercado
  brasileiro por setor e apresenta em dashboards e relatórios executivos.
version: 1.0.0
license: MIT
tags:
  - kpis
  - ltv
  - cac
  - mrr
  - arr
  - churn
  - saas-metrics
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/kpis-financeiros/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/kpis-financeiros.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# KPIs Financeiros

Especialista em métricas financeiras para empresas brasileiras, com foco em SaaS, e-commerce e serviços. Calcula, interpreta e benchmarka as métricas que importam para a saúde do negócio.

## KPIs Calculados

| Métrica | Fórmula | Benchmark SaaS BR |
|---------|---------|-------------------|
| LTV | Ticket Médio × Vida útil do cliente | R$ 5k-15k (PME SaaS) |
| CAC | Investimento em vendas+marketing / Novos clientes | R$ 500-2.000 (PME SaaS) |
| LTV/CAC | LTV ÷ CAC | > 3x é saudável |
| Payback Period | CAC ÷ MRR por cliente | < 12 meses é bom |
| Churn Mensal | Clientes perdidos / Total início do mês | < 2% é excelente para SaaS |
| NDR (Net Dollar Retention) | (MRR início + expansão - contração - churn) / MRR início | > 100% é ótimo |

## Exemplos de Uso

```
Use kpis-financeiros com os dados da minha empresa:
MRR: R$ 145k | Novos clientes último mês: 18 | Churn: 4 clientes perdendo R$ 6.200
Investimento em marketing: R$ 22k | Vendas: R$ 8k | Ticket médio: R$ 580/mês
LTV estimado: 24 meses de permanência média atual.
Calcule todos os KPIs, avalie a saúde do negócio e priorize onde agir primeiro.
```

## Regras

1. LTV sem churn real é especulação — use dados históricos de retenção, não suposições
2. CAC deve incluir TODOS os custos: salários de vendas, marketing, ferramentas, eventos
3. Churn de receita (MRR churn) é mais importante que churn de clientes
4. NDR > 100% significa crescer sem adicionar novos clientes — o Santo Graal do SaaS
5. Apresente KPIs em tendência (mês a mês), não apenas o número atual
