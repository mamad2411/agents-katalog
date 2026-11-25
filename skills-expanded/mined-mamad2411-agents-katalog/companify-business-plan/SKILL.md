---
name: companify-business-plan
description: Consolida o plano de negócio como narrativa coerente. Use depois do Executive Alignment Gate para produzir company/business-plan.md e company/roadmap.md.
---

# Consolidar o plano de negócio

## Protocolo operacional

- **Plano e progresso:** planejar a narrativa pelas 32 seções do
  [outline](references/business-plan-outline.md) antes de escrever, citando
  a fonte de cada seção em `company/`.
- **Fontes de verdade:** ler todos os artefatos de `company/`,
  `.companify/assumptions.md`, `.companify/escolhas.md` e
  `.companify/metrics.md`.
- **Escopo e idempotência:** não concatenar os documentos, e sim construir
  uma narrativa única. Preservar versões anteriores do plano; cada revisão soma
  uma entrada de versão, não substitui a história.
- **Validação:** nenhuma hipótese crítica aparece como fato; toda projeção
  cita premissa; toda ameaça crítica tem mitigação.
- **Resumo final:** informar a versão gerada, o que mudou desde a última
  versão e as pendências que seguem abertas.

## Fluxo

1. Confirmar que o Executive Alignment Gate está completo (ver
   [gates.md](../companify-builder/references/gates.md) em
   `companify-builder`); um plano consolidado sobre análises incompletas é
   prematuro.
2. Escrever `company/business-plan.md` seguindo as 32 seções do
   [outline](references/business-plan-outline.md), sempre citando o artefato
   de origem de cada seção: a consolidação narra, não inventa.
3. Consolidar `company/roadmap.md` a partir dos roadmaps setoriais já
   registrados por CPO, CTO, CMO, CRO, COO, CHRO e CFO, organizados pelos
   horizontes definidos no outline.
4. Escrever o plano de 90 dias (objetivo → iniciativa → experimento →
   métrica → responsável → prazo, separado em dias 1–30, 31–60, 61–90),
   priorizando com `$companify-ceo` e `$companify-board` para evitar dezenas
   de iniciativas simultâneas.
5. Listar premissas críticas, experimentos recomendados e escolhas
   pendentes, puxando diretamente de `.companify/assumptions.md` e
   `.companify/escolhas.md`.
6. Atualizar `company/README.md` com o status de cada artefato.
7. Registrar versão, data, mudanças relevantes, novas comprovações, premissas
   invalidadas e escolhas alteradas no topo de `company/business-plan.md`.

## Raciocínio do especialista

O plano de negócio não é um PDF estático: é uma fotografia datada de um
raciocínio vivo. A consolidação testa se produto, mercado, marketing,
tecnologia, finanças e operação contam a mesma história; quando não contam,
o trabalho aqui é expor a divergência para `$companify-board`, não escondê-la
suavizando a linguagem. Evitar dezenas de iniciativas simultâneas no plano de
90 dias: um plano que tenta tudo não prioriza nada.
