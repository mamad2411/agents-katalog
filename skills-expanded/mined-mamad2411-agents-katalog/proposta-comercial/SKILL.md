---
name: "proposta-comercial"
description: |
  Gera propostas comerciais e orçamentos profissionais para o mercado brasileiro.
  Estrutura o escopo, precifica em R$ com opções de parcelamento, inclui termos
  de pagamento por boleto/PIX/cartão e cláusulas adequadas ao mercado local.
version: 1.0.0
license: MIT
tags:
  - proposta
  - orcamento
  - comercial
  - precificacao
  - b2b
  - contrato
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/proposta-comercial/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/proposta-comercial.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Proposta Comercial

Especialista em criar propostas comerciais persuasivas e profissionais para o mercado B2B brasileiro. Foca em apresentar valor antes de apresentar preço.

## Estrutura Padrão de Proposta

1. **Capa** — Logo, nome do cliente, data, validade da proposta
2. **Diagnóstico do Problema** — Demonstrar que entendeu a dor
3. **Solução Proposta** — O que você vai fazer (escopo claro)
4. **Metodologia** — Como você vai fazer (processo)
5. **Entregáveis** — O que o cliente vai receber (tangível)
6. **Cronograma** — Quando cada entregável estará pronto
7. **Investimento** — Valor, opções de pagamento, validade
8. **Próximos Passos** — CTA claro para aprovação
9. **Sobre a Empresa** — Credenciais, cases relevantes

## Exemplos de Uso

```
Use proposta-comercial para criar uma proposta de desenvolvimento de e-commerce
para uma marca de cosméticos natural em BH. Escopo: loja virtual Nuvemshop + integração
Mercado Pago + setup Google Analytics + treinamento. Investimento: R$ 8.500 à vista
ou 3x R$ 3.000. Prazo: 45 dias. Cliente: empresa com faturamento de R$ 300k/ano.
```

## Regras

1. Valor antes de preço — apresente o ROI esperado antes da seção de investimento
2. Sempre inclua validade da proposta (7-15 dias) para criar senso de urgência real
3. Formas de pagamento BR: PIX (à vista com desconto), boleto 30/60/90, cartão parcelado
4. Inclua cláusula de reajuste por IPCA em contratos anuais
5. Proposta visual (PDF bem diagramado) converte até 3x mais que proposta em texto simples
