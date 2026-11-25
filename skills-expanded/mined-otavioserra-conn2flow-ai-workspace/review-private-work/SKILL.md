---
description: Faz review findings-first em projeto privado Conn2Flow. Use quando a implementação já existe e o foco agora é encontrar bugs, regressões, drift de escopo e validação ausente.
disable-model-invocation: true
allowed-tools: Read Grep Glob Bash(git diff *) Bash(git status *)
argument-hint: [foco-opcional]
---

# Review de projeto privado

Revise o diff atual em modo findings-first.

## Foco padrão

1. bugs funcionais
2. regressão
3. escopo errado entre privado e core
4. drift contra batches, specs locais ou validação
5. ausência de testes ou validação relevante

## Formato esperado

1. Liste findings primeiro, do mais severo para o menos severo.
2. Diga quando não houver findings.
3. Deixe resumo ou change log em segundo plano.

## Foco adicional desta rodada

$ARGUMENTS