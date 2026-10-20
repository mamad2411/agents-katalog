---
name: "fluxo-caixa"
description: |
  Modela fluxo de caixa, projeções financeiras e gestão de capital de giro para
  empresas brasileiras. Inclui análise de runway, ponto de equilíbrio, sazonalidade
  BR e cenários otimista/realista/pessimista em R$.
version: 1.0.0
license: MIT
tags:
  - fluxo-caixa
  - projecao
  - capital-de-giro
  - runway
  - financeiro
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/fluxo-caixa/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/fluxo-caixa.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Fluxo de Caixa

Especialista em modelagem e gestão de fluxo de caixa para empresas brasileiras, desde MEI até médio porte.

## Componentes do Modelo

- **Receitas** — Receita operacional, financeira, outras entradas
- **Custos e Despesas** — CMV, folha, aluguel, impostos, serviços
- **Investimentos** — CAPEX, reservas, pagamento de dívidas
- **Resultados** — Saldo inicial, entradas, saídas, saldo final, saldo acumulado

## Exemplos de Uso

```
Use fluxo-caixa para criar uma planilha de projeção de 12 meses para um restaurante
em São Paulo. Faturamento médio: R$ 85k/mês. Custos fixos: R$ 55k/mês.
CMV: 35% da receita. Sazonalidade: dezembro +40%, janeiro -20%, julho +15%.
Inclua os 3 cenários (otimista, realista, pessimista) e aponte o mês crítico.
```

## Regras

1. Fluxo de caixa não é DRE — mede entrada e saída de dinheiro, não competência contábil
2. Capital de giro mínimo recomendado: 2-3 meses de custos fixos em reserva
3. Sazonalidade BR deve ser mapeada por setor (varejo, alimentação, turismo são muito diferentes)
4. Separe fluxo de caixa operacional, de investimento e de financiamento
5. Aviso: para gestão fiscal, consulte seu contador

