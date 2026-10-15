---
name: companify-business-model
description: Define a lógica econômica do negócio. Use para estruturar company/business-model.md com criação, entrega e captura de valor.
---

# Estruturar o modelo de negócio

## Protocolo operacional

- **Plano e progresso:** planejar cliente, proposta de valor, canais,
  receita, custos e vantagem competitiva antes de escrever o artefato final.
- **Fontes de verdade:** ler `.companify/company-context.md`,
  `company/market.md` e `brand/strategy.md` quando existente.
- **Escopo e idempotência:** preservar escolhas de modelo já aprovadas;
  mudança de modelo vira `ESC-NNN` em `.companify/escolhas.md`, não
  reescrita silenciosa.
- **Validação:** cada elemento do modelo responde a uma das quatro perguntas
  centrais (como criamos, entregamos, capturamos valor, por que pode
  funcionar).
- **Resumo final:** informar o modelo escolhido, as alternativas descartadas
  e o que precisa ser verdadeiro para funcionar.

## Fluxo

Use o [canvas do modelo de negócio](references/business-model-canvas.md) para
preencher os blocos antes de escrever o artefato final.

1. Analisar cliente, problema e proposta de valor a partir do Company
   Context e de `company/market.md`.
2. Definir canais, relacionamento, fontes de receita, recursos-chave,
   atividades-chave, parceiros-chave e estrutura de custos.
3. Escolher o arquétipo de modelo mais próximo (SaaS, marketplace,
   assinatura, licenciamento, serviços, consumo, comissão, freemium, usage
   based, ou híbrido) e adaptar: não forçar um arquétipo que não corresponde
   à forma real de cobrança e entrega.
4. Explicitar a vantagem competitiva e a escalabilidade do modelo escolhido.
5. Responder por escrito: como criamos valor? Como entregamos valor? Como
   capturamos valor? Por que este modelo pode funcionar? O que precisa ser
   verdadeiro para funcionar?
6. Salvar em `company/business-model.md`.

## Raciocínio do especialista

Usar Business Model Canvas, Lean Canvas ou Value Proposition Canvas como
ferramenta de raciocínio, não como formulário a preencher mecanicamente. Um
modelo de negócio é uma cadeia de apostas causais: se o canal X funciona,
então o CAC Y é sustentável, então a margem Z permite reinvestir em
aquisição. Testar a cadeia inteira, não cada bloco isoladamente: um modelo
com blocos individualmente plausíveis pode ser inviável quando encadeado.
