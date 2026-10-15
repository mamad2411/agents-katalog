---
name: companify-audit
description: Audita a consistência e a prontidão do plano de negócio. Use para revisar company/ antes de considerar o pacote pronto para uso.
---

# Auditar o plano de negócio

## Protocolo operacional

- **Plano e progresso:** planejar a varredura pelas dimensões da
  [rubrica](references/audit-rubric.md) antes de escrever o relatório.
- **Fontes de verdade:** ler todos os artefatos de `company/`,
  `.companify/assumptions.md`, `.companify/escolhas.md`,
  `.companify/metrics.md` e `brand/strategy.md` quando existente.
- **Escopo e idempotência:** auditar sem corrigir silenciosamente artefatos
  aprovados: reportar o achado e deixar a correção para a skill
  responsável.
- **Validação:** todo achado é classificado por impacto, probabilidade e
  reversibilidade, e por severidade (impedimento, correção necessária,
  melhoria recomendada, observação).
- **Resumo final:** apresentar o veredito e a lista de achados por
  severidade.

## Fluxo

1. Ler a [rubrica de auditoria](references/audit-rubric.md) e aplicar cada
   dimensão: consistência, comprovação, hipóteses apresentadas como fato,
   finanças, produto, tecnologia, marketing, receita, operação, pessoas,
   marca e ameaças.
2. Cruzar `company/product.md`, `company/market.md`, `company/marketing.md`,
   `company/technology.md`, `company/finance.md` e `company/operations.md`
   em busca de contradição: o mesmo ICP, o mesmo estágio, o mesmo modelo de
   negócio, em todos os documentos.
3. Verificar se toda projeção em `company/finance.md` cita premissa ou
   cenário.
4. Verificar se toda escolha relevante tem entrada em
   `.companify/escolhas.md` com rastreabilidade.
5. Verificar se as ameaças críticas de `company/ameacas.md` têm mitigação.
6. Verificar se `company/business-plan.md` contradiz alguma escolha
   aprovada pelo Brandfy sem registro de tensão.
7. Salvar em `.companify/reviews/YYYY-MM-DD-audit.md` com veredito `PASSED`,
   `PASSED WITH PENDING ITEMS` ou `FAILED`.

## Raciocínio do especialista

Auditar por cadeia de comprovação: Company Context, artefato especializado,
consolidação no plano e uso real precisam concordar. Não reduzir a auditoria
à presença de arquivos: um `company/finance.md` que existe mas projeta
números sem premissa reprova a mesma seção quanto a ausência do arquivo.
Diferenciar impedimento de publicação de melhoria recomendada; nem todo
achado impede o uso do plano.
