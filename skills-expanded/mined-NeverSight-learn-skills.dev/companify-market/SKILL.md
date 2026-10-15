---
name: companify-market
description: Analisa mercado, segmentos, ICP e concorrência. Use para estruturar company/market.md antes da consolidação executiva.
---

# Analisar mercado e concorrência

## Protocolo operacional

- **Plano e progresso:** planejar categoria, segmentos, concorrência e
  dimensionamento antes de escrever o artefato final.
- **Fontes de verdade:** ler `.companify/company-context.md`,
  `.companify/interview.md`, comprovações em `.companify/comprovacoes.md` e
  `brand/strategy.md` quando existente.
- **Escopo e idempotência:** preservar hipóteses já validadas; uma nova
  pesquisa complementa, não apaga, achados anteriores sem justificativa.
- **Validação:** toda alegação sobre tamanho de mercado, concorrente ou
  tendência cita a fonte ou é marcada como hipótese.
- **Resumo final:** informar o que foi confirmado, o que segue como
  hipótese e quais comprovações ainda faltam.

## Fluxo

Use o [worksheet de mercado](references/market-worksheet.md) para conduzir a
análise campo a campo antes de escrever o artefato final.

1. Definir categoria e o mercado relevante a partir do problema descrito no
   Company Context.
2. Mapear segmentos e estruturar o ICP; diferenciar usuário, comprador e
   decisor quando forem pessoas ou papéis diferentes.
3. Mapear personas econômicas quando necessário (ex.: comprador B2B com
   orçamento próprio vs. usuário final sem poder de compra).
4. Levantar alternativas atuais do cliente (incluindo "não fazer nada" e
   soluções manuais), concorrentes diretos, substitutos e barreiras de
   entrada. Não inventar concorrente sem fonte verificável.
5. Analisar forças competitivas e tendências relevantes ao estágio da
   empresa.
6. Estruturar TAM/SAM/SOM apenas quando houver dado confiável; quando não
   houver, registrar a premissa de cálculo explicitamente (fonte, ano,
   método) em vez de apresentar um número sem lastro.
7. Salvar em `company/market.md` com a estrutura: mercado, categoria,
   problema, segmentos, ICP, jobs/necessidades, alternativas, concorrentes,
   substitutos, TAM, SAM, SOM, tendências, barreiras, oportunidades,
   ameaças, hipóteses e comprovações necessárias.

## Raciocínio do especialista

Um mercado não é definido pelo produto, é definido pelo problema e por quem o
sente com intensidade suficiente para pagar por uma solução. Testar cada
segmento com uma pergunta: esse grupo já gasta dinheiro, tempo ou esforço
tentando resolver isso hoje? Se não, o segmento é hipótese, não mercado
validado. TAM/SAM/SOM sem premissa explícita é decoração: declarar sempre a
fonte e o método usados para chegar ao número.
