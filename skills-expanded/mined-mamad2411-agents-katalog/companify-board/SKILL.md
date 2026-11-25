---
name: companify-board
description: Confronta as análises executivas, resolve conflitos e prioriza. Use antes da consolidação, ou para debater isoladamente uma escolha complexa.
---

# Reunir o conselho executivo (Board)

## Protocolo operacional

- **Plano e progresso:** planejar quais artefatos de `company/` entram na
  análise e quais conflitos já são conhecidos antes de escrever o resultado.
- **Fontes de verdade:** ler todos os artefatos disponíveis em `company/`,
  `.companify/assumptions.md`, `.companify/escolhas.md` e a
  [matriz de colaboração executiva](references/collaboration-matrix.md).
- **Escopo e idempotência:** não escolher sozinho o que a
  [matriz](references/collaboration-matrix.md) atribui a uma liderança
  específica; o Board resolve conflito entre áreas, não substitui a área.
- **Validação:** toda escolha registrada segue o formato
  [`ESC-NNN`](references/decision-record.md), com alternativas, comprovações e
  condição de revisão explícitas.
- **Resumo final:** informar a escolha tomada (ou provisória), a comprovação
  ainda necessária e a data de revisão.

## Fluxo

1. Reunir os artefatos relevantes de `company/` para a escolha em análise.
2. Procurar especificamente: conflitos entre áreas, premissas incompatíveis,
   dependências não declaradas, escolhas sem comprovação, otimização local,
   ameaças ignoradas, metas incompatíveis e inconsistências entre documentos.
3. Apresentar a leitura de cada área envolvida separadamente (CMO, CRO, CFO,
   CPO etc.), sem diálogo teatral: ver
   [decision-record.md](references/decision-record.md) para o formato
   analítico esperado e o exemplo a evitar.
4. Nomear o conflito central em uma frase.
5. Listar alternativas reais, não apenas "fazer" ou "não fazer".
6. Recomendar uma alternativa, a comprovação ainda necessária para
   confirmá-la e a condição de revisão.
7. Registrar em `.companify/escolhas.md` como `ESC-NNN`, com status
   `provisória` ou `aprovada`.

## Raciocínio do especialista

A pergunta central é: essas respostas continuam coerentes quando analisadas
juntas? Cada C-level otimiza uma função diferente por desenho: o valor do
Board está em não deixar nenhuma dessas funções silenciada. Uma recomendação
que elimina toda tensão sem comprovação nova é suspeita: normalmente
significa que uma área foi ignorada, não conciliada. Preferir escolha
provisória com regra de revisão explícita a escolha definitiva sem
comprovação suficiente.
