---
name: local-smart
description: Use o executor local inteligente (dots.llm1) para tarefas que exigem reasoning mais forte
---

Use este skill para:
- refactors mais difíceis
- análise de bug
- debugging com mais contexto
- reasoning técnico local
- sugestões de patch mais robustas

Use o script:
!bash .claude/bin/dots-task.sh "<task>"

Depois:
- sintetize a resposta
- compare com a solução atual
- explicite incertezas
- não trate a resposta como decisão final de arquitetura