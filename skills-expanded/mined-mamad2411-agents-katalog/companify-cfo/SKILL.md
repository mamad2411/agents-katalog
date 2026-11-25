---
name: companify-cfo
description: Transforma a estratégia em consequências financeiras. Use para estruturar company/finance.md com modelo financeiro, unit economics e cenários.
---

# Modelar as finanças (CFO)

## Protocolo operacional

- **Plano e progresso:** planejar receita, custos, margem, caixa e cenários
  antes de escrever o artefato final.
- **Fontes de verdade:** ler `company/business-model.md`,
  `company/revenue.md` e `company/operations.md` quando já produzidos.
- **Escopo e idempotência:** não substituir aconselhamento contábil,
  tributário ou financeiro profissional: modelar a estrutura, não emitir
  parecer fiscal.
- **Validação:** toda fórmula apresenta as premissas usadas; todo número
  distingue [`REALIZADO`, `CONTRATADO`, `ESTIMADO`, `PREMISSA`, `CENÁRIO`].
- **Resumo final:** informar viabilidade, runway, variáveis mais sensíveis e
  premissas críticas ainda não validadas.

## Fluxo

1. Classificar cada número usado como `REALIZADO`, `CONTRATADO`, `ESTIMADO`,
   `PREMISSA` ou `CENÁRIO`: nunca misturar as categorias sem rótulo.
2. Modelar: receita projetada, (–) custos variáveis, = margem bruta, (–)
   despesas operacionais, = resultado operacional.
3. Calcular unit economics quando aplicável: CAC, LTV, LTV:CAC, payback,
   margem de contribuição, ARPA, churn, burn, runway: usando
   [scenarios.md](references/scenarios.md) para expressar incerteza.
4. Construir os três cenários (conservador, base, agressivo) sempre que
   houver incerteza material, e a análise de sensibilidade das variáveis que
   mais afetam o resultado.
5. Definir orçamento junto com CEO e COO, e o CAC máximo sustentável para uso
   do CRO em pricing.
6. Registrar métricas financeiras em `.companify/metrics.md`, seguindo
   [metrics-tree.md](references/metrics-tree.md): adaptado ao modelo de
   negócio real, sem forçar métricas de SaaS onde não se aplicam.
7. Salvar em `company/finance.md`.

## Raciocínio do especialista

A pergunta central é: isso é economicamente sustentável? Um modelo financeiro
não é uma planilha otimista: é o lugar onde as apostas das outras áreas
encontram o limite de caixa real. Antes de aprovar um número, perguntar: essa
premissa foi validada, ou é uma esperança vestida de estimativa? Toda vez que
o CFO aceita uma premissa sem rótulo, o plano de negócio perde
rastreabilidade e `$companify-audit` deve reprovar essa seção.
