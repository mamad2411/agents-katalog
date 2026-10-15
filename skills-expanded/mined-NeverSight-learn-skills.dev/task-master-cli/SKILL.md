---
name: task-master-cli
description: Use the `task-master` CLI to manage tasks in software projects — creating, listing, updating, expanding, and tracking tasks and subtasks from the command line. Trigger this skill whenever the user wants to manage tasks via `task-master`, asks how to create/update/list/expand/prioritize tasks or subtasks, track progress, manage dependencies, analyze complexity, initialize a new project with Task Master, or run the TDD autopilot workflow (RED → GREEN → COMMIT cycle). Also trigger when the user mentions task-master, TaskMaster, TM, parse-prd, tm autopilot, or wants to automate AI-driven task management.
---

# Task Master CLI (`task-master`) Skill

`task-master` is a CLI for AI-driven development task management. Run `task-master init` once per project before using any other command.

## Command Reference

For detailed command reference, read the relevant file based on the user's task:

| Domain | File | When to read |
|--------|------|--------------|
| Tasks | `references/tasks.md` | Listar, criar, atualizar, mostrar, gerar e definir status de tasks |
| Subtasks | `references/subtasks.md` | Expandir, atualizar, limpar subtasks |
| Dependencies | `references/dependencies.md` | Adicionar, remover, validar e corrigir dependências |
| Complexity | `references/complexity.md` | Analisar e exibir relatório de complexidade |
| Setup | `references/setup.md` | Inicializar projeto e parsear PRD |
| Autopilot | `references/autopilot.md` | Workflow TDD autônomo para agentes AI (RED → GREEN → COMMIT) |

## Common Workflows

### Iniciar um projeto
```bash
task-master init
task-master models --setup       # configurar modelos de LLM
task-master parse-prd prd.txt    # gerar tasks a partir de um PRD
```

### Fluxo de desenvolvimento diário
```bash
task-master next                 # próxima task recomendada
task-master show <id>            # ver detalhes da task
task-master set-status --id=<id> --status=in-progress
# ... implementar ...
task-master set-status --id=<id> --status=done
```

### Expandir task em subtasks
```bash
task-master expand --id=<id> --num=5
task-master expand --id=<id> --prompt="contexto adicional"
task-master expand --all --force   # regenerar subtasks de todas as tasks
```

### Gerenciar dependências
```bash
task-master add-dependency --id=<id> --depends-on=<id>
task-master validate-dependencies
task-master fix-dependencies
```

### Analisar complexidade
```bash
task-master analyze-complexity
task-master complexity-report
```

## Status disponíveis

| Status | Descrição |
|--------|-----------|
| `pending` | Aguardando início |
| `in-progress` | Em desenvolvimento |
| `review` | Aguardando revisão/PR |
| `done` | Concluída |
| `deferred` | Postergada |
| `cancelled` | Cancelada |

## Tips

- `task-master <comando> --help` exibe referência completa de flags para qualquer comando.
- Subtasks usam o formato `<parentId>.<subtaskId>` (ex.: `1.2` = subtask 2 da task 1).
- Ao marcar uma task como `done`, todas as subtasks são automaticamente marcadas como `done`.
- Flags `--research` usam Perplexity AI para geração com embasamento externo.
- Use `task-master list -w` (watch) para atualização automática em tempo real.
