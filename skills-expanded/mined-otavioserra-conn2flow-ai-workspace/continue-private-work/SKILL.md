---
description: Retoma uma demanda em andamento em projeto privado Conn2Flow. Use quando houver delta operacional novo, arquivos alterados manualmente, ou mudança de escopo no meio da execução.
disable-model-invocation: true
argument-hint: [o-que-mudou-desde-a-última-rodada]
---

# Continuidade de projeto privado

Trate `$ARGUMENTS` como o delta operacional desde a última rodada.

## Antes de continuar

1. Releia primeiro os arquivos, folders ou artefatos explicitamente citados no delta.
2. Se a tarefa continuar ancorada em um escopo local SDD dentro de `project/`, releia `00-START-HERE.md`, `01-WORKFLOW.md`, a spec principal, `implementation/BATCH-INDEX.md` e `validation/VALIDATION-CHECKLIST.md` antes de editar.
3. Se o delta mexer no split entre privado e core, recarregue `private-project-context`.
4. Se o delta tocar módulo do gestor, recarregue `gestor-module-integration`.

## Regra de execução

- Não recomeçar exploração ampla sem necessidade.
- Continuar a partir do menor conjunto de arquivos que realmente mudou.
- Validar cedo de novo se o delta afetar a implementação ou a premissa de validação.

## Delta atual

$ARGUMENTS