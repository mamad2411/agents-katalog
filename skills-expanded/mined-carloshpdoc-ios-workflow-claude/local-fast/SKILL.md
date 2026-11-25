---
name: local-fast
description: Use o executor local rápido (Qwen3.5 35B A3B) para tarefas de baixo risco e baixo custo
---

Use este skill para:
- gerar testes
- revisar diff
- resumir logs
- explicar código
- propor refactor simples
- sugerir melhorias locais

Use o script:
!bash .claude/bin/qwen-task.sh "<task>"

Depois:
- sintetize a resposta
- destaque riscos
- não aplique mudanças críticas sem validação