---
name: "analise-de-coortes"
description: "Análise de coortes, retenção e LTV de usuários para SaaS e e-commerce"
version: 1.0.0
license: MIT
tags: [analytics, cohorte, retencao, ltv, churn, usuarios, saas, e-commerce]
---

# Análise de Coortes e Retenção

Metodologia e implementação de análise de coortes para entender retenção, LTV e comportamento de usuários ao longo do tempo.

## Quando Usar
- Analisar retenção de usuários por período de aquisição
- Calcular e melhorar LTV por canal de aquisição
- Identificar quando e por que usuários abandonam o produto

## Exemplos de Prompt
```
Tenho um app de finanças pessoais com 50.000 usuários cadastrados mas apenas
8.000 ativos mensalmente. Explique como montar uma análise de coortes mensal
para entender: quando os usuários deixam de usar, qual coorte tem melhor retenção
e o que diferencia os usuários retidos dos que abandonaram.
```

```
Sou gestor de e-commerce e quero calcular o LTV dos meus clientes por canal
de aquisição (Google, Meta, Orgânico, Indicação). Crie a metodologia de cálculo,
como segmentar por cohort de primeiro mês de compra e como usar esse dado
para otimizar o CAC aceitável por canal.
```

## Saídas Típicas
- Metodologia de análise de coortes adaptada ao negócio
- Estrutura de tabela de coortes com cálculos
- Interpretação de padrões de retenção (curva de retenção)
- Cálculo de LTV por coorte e canal de aquisição
- Recomendações de produto baseadas nos padrões de abandono
