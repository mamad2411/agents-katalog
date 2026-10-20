---
name: "impostos-br"
description: |
  Orienta sobre o sistema tributário brasileiro para empresas e empreendedores:
  MEI, Simples Nacional (todos os anexos), Lucro Presumido e Lucro Real. Calcula
  carga tributária estimada e apoia decisões de enquadramento tributário.
version: 1.0.0
license: MIT
tags:
  - impostos
  - simples-nacional
  - lucro-presumido
  - lucro-real
  - mei
  - tributario
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read financeiro-compliance/impostos-br/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/impostos-br.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Impostos BR

Orientação sobre o sistema tributário brasileiro para empresas de todos os portes. Foco em decisões práticas de enquadramento e planejamento tributário.

## Regimes Tributários

| Regime | Limite de Faturamento | IRPJ + CSLL | Indicado |
|--------|-----------------------|-------------|----------|
| MEI | R$ 81.000/ano | Fixo mensal | Autônomo solo |
| Simples Anexo I | R$ 4,8M/ano | 4-11,5% | Comércio |
| Simples Anexo III | R$ 4,8M/ano | 6-17,5% | Serviços (fator-r alto) |
| Simples Anexo V | R$ 4,8M/ano | 15,5-30,5% | Serviços (fator-r baixo) |
| Lucro Presumido | R$ 78M/ano | ~11-13% receita | Serviços com margem |
| Lucro Real | Sem limite | 15-25% lucro | Alta margem ou prejuízo |

## Exemplos de Uso

```
Use impostos-br para comparar a carga tributária de uma empresa de desenvolvimento
de software com faturamento de R$ 2,4M/ano e folha de pagamento de R$ 480k/mês.
Sócios retiram pró-labore de R$ 8k cada (2 sócios). Compare: Simples Anexo V vs.
Lucro Presumido. Inclua: PIS/COFINS, ISS, IRPJ, CSLL, INSS patronal e carga total.
```

## Regras

1. AVISO: esta análise é educacional — consulte seu contador para decisões tributárias reais
2. Fator-R no Simples Nacional: folha/faturamento determina o anexo (III vs. V)
3. Planejamento tributário LEGAL é obrigação de todo CFO — elisão (não evasão)
4. DAS do MEI vence dia 20 de cada mês — inadimplência gera multa e juros
5. Distribuição de lucros no Simples e LP é isenta de IR para os sócios (uma das maiores vantagens BR)
