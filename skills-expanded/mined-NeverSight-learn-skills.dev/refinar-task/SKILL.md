---
name: refinar-task
description: Refina tasks do backlog.md seguindo o padrão (descrição detalhada, passos numerados, pseudocódigo)
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: backlog-management
---

## Quando usar
Quando o usuário pedir para refinar uma task do backlog.

## Como funciona
1. Pergunte o ID da task (ex: TASK-3) e contexto adicional se necessário
2. Use `backlog_task_view` para buscar a task atual
3. Explore o código relevante para entender o contexto
4. Proponha refinamento no mesmo formato da TASK-2:
   - Descrição clara do que a task faz
   - Passos numerados para executar
   - Pseudocódigo de implementação
5. Apresente para o usuário validar
6. Se aprovado, atualize a task com `backlog_task_edit`
7. Mude o status para "Refined"

## Formato da task refinada
Deve seguir o padrão:
- Descrição com explicação + Passos + Pseudocódigo
- Sem Definition of Done separados (tudo na descrição)
- Status final: "Refined"

## Template de Descrição

```
## Descrição

[Resumo do objetivo da task]

### Passos para executar:
1. [Passo 1 - ação concreta]
2. [Passo 2 - ação concreta]
3. [Passo n - ação concreta]

### Implementação

```lang
// Pseudocódigo a ser definido durante refinamento
```
```
