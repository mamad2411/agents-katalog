---
name: companify-builder
description: Coordena a construção ou revisão completa do plano de negócio. Use quando o trabalho abranger mercado, modelo de negócio, conselho executivo e consolidação.
---

# Construir o plano de negócio completo

## Protocolo operacional

- **Plano e progresso:** criar um plano com os marcos da esteira e os quatro
  gates, atualizando o estado após cada aceite.
- **Fontes de verdade:** ler `.companify/config.yaml`,
  `.companify/company-context.md`, os artefatos existentes em `company/`,
  `.brandfy/config.yaml` e `brand/strategy.md` quando existentes, e
  [gates.md](references/gates.md).
- **Escopo e idempotência:** retomar o estado registrado, preservar
  artefatos aprovados. Uma empresa existente pode pular etapas já
  suficientemente documentadas: a comprovação do que já existe justifica o
  salto.
- **Validação:** não avançar de um gate ao seguinte com item pendente sem
  justificativa registrada.
- **Resumo final:** registrar artefatos produzidos, gates concluídos,
  escolhas tomadas, comprovações usadas e pendências.

## Esteira

1. Usar `$companify-setup`.
2. Carregar o contexto Brandfy quando existente (`.brandfy/config.yaml`,
   `brand/strategy.md`, `brand/voice.md`, `brand/manual.md`).
3. Detectar o estágio da empresa e os documentos já existentes em `company/`.
4. Conduzir `$companify-interview` quando o Company Context tiver lacuna
   relevante.
5. Confirmar o **Context Gate**.
6. Usar `$companify-market` e `$companify-business-model` em paralelo.
7. Confirmar o **Viability Gate**.
8. Acionar os nove especialistas sobre o mesmo Company Context:
   `$companify-ceo`, `$companify-cpo`, `$companify-cto`, `$companify-cmo`,
   `$companify-cro`, `$companify-cfo`, `$companify-coo`, `$companify-chro` e
   `$companify-ameacas`. Eles não dependem sequencialmente uns dos outros, mas
   cada um lê os artefatos que os demais já publicaram em `company/`.
9. Usar `$companify-board` para confrontar as análises, resolver conflitos e
   registrar escolhas.
10. Confirmar o **Executive Alignment Gate**.
11. Usar `$companify-business-plan` para consolidar `company/business-plan.md`
    e `company/roadmap.md`.
12. Usar `$companify-audit`.
13. Confirmar o **Business Plan Gate** e apresentar os próximos passos.

Ver [gates.md](references/gates.md) para o checklist completo de cada gate e
o diagrama da esteira.

## Raciocínio do especialista

O builder não substitui o raciocínio de cada especialista: orquestra a
sequência, garante que nenhuma etapa avance sobre lacuna não reconhecida e
mantém os quatro gates como pontos de honestidade, não como burocracia. Uma
empresa existente com documentação forte deve avançar rápido; uma ideia em
estágio inicial deve gastar mais tempo no Context Gate do que na
consolidação final. O sinal de builder mal executado é um plano de negócio
elegante que nenhuma das nove lideranças reconheceria como fiel à própria
análise.
