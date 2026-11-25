---
name: task-execution-engine
description: Execute tarefas de implementação de documentos de design usando checkboxes markdown. Use quando (1) implementar features da saída do feature-design-assistant, (2) retomar trabalho interrompido, (3) executar tarefas em lote. Dispara em 'start implementation', 'run tasks', 'resume'.
---

# Pipeline de Features

Execute tarefas de implementação diretamente de documentos de design. Tarefas são gerenciadas como checkboxes markdown - nenhum arquivo de sessão separado necessário.

## Referência Rápida

```bash
# Obter próxima tarefa
python3 scripts/task_manager.py next --file <design.md>

# Marcar tarefa como concluída
python3 scripts/task_manager.py done --file <design.md> --task "Task Title"

# Marcar tarefa como falha
python3 scripts/task_manager.py fail --file <design.md> --task "Task Title" --reason "..."

# Mostrar status
python3 scripts/task_manager.py status --file <design.md>
```

## Formato de Tarefa

Tarefas são escritas como checkboxes markdown no documento de design:

```markdown
## Implementation Tasks

- [ ] **Create User model** `priority:1` `phase:model`
  - files: src/models/user.py, tests/models/test_user.py
  - [ ] User model has email and password_hash fields
  - [ ] Email validation implemented
  - [ ] Password hashing uses bcrypt

- [ ] **Implement JWT utils** `priority:2` `phase:model`
  - files: src/utils/jwt.py
  - [ ] generate_token() creates valid JWT
  - [ ] verify_token() validates JWT

- [ ] **Create auth API** `priority:3` `phase:api` `deps:Create User model,Implement JWT utils`
  - files: src/api/auth.py
  - [ ] POST /register endpoint
  - [ ] POST /login endpoint
```

Veja [references/task-format.md](references/task-format.md) para a especificação completa do formato.

## Loop de Execução

```
LOOP enquanto houver tarefas:
  1. OBTER próxima tarefa (task_manager.py next)
  2. LER detalhes da tarefa (arquivos, critérios)
  3. IMPLEMENTAR a tarefa
  4. VERIFICAR critérios de aceição
  5. ATUALIZAR status (task_manager.py done/fail)
  6. CONTINUAR
```

### Regras do Modo Autônomo

- **NUNCA parar** para fazer perguntas
- **NUNCA pedir** esclarecimentos
- Tomar decisões autônomas com base em padrões do codebase
- Se bloqueado, marcar como falha e continuar

## Atualizações de Status

Tarefa concluída:
```markdown
- [x] **Create User model** `priority:1` `phase:model` ✅
  - files: src/models/user.py
  - [x] User model has email field
  - [x] Password hashing implemented
```

Tarefa falha:
```markdown
- [x] **Create User model** `priority:1` `phase:model` ❌
  - files: src/models/user.py
  - [ ] User model has email field
  - reason: Missing database configuration
```

## Retomar / Recuperação

Para retomar trabalho interrompido, simplesmente execute novamente com o mesmo arquivo de design:

```
/feature-pipeline docs/designs/xxx.md
```

O gerenciador de tarefas encontrará a primeira tarefa incompleta e continuará a partir daí.

## Integração

Esta skill é normalmente disparada após o `/feature-analyzer` ser concluído:

```
User: /feature-analyzer implement user auth

Claude: [designs feature, generates task list]
        Design saved to docs/designs/2026-01-02-user-auth.md
        Ready to start implementation?

User: Yes / 开始实现

Claude: [executes tasks via task-execution-engine]
```