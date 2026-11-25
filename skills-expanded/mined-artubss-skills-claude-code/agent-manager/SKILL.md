---
name: agent-manager-skill
description: Gerencie múltiplos agentes CLI locais via sessões tmux (iniciar/parar/monitorar/atribuir) com agendamento compatível com cron.
---

# Agent Manager Skill

## Quando usar

Use essa skill quando você precisar:

- executar múltiplos agentes CLI locais em paralelo (sessões tmux separadas)
- iniciar/parar agentes e acompanhar seus logs
- atribuir tarefas aos agentes e monitorar a saída
- agendar trabalho recorrente de agentes (cron)

## Pré-requisitos

Instale `agent-manager-skill` em seu workspace:

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## Comandos comuns

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start EMP_0001
python3 agent-manager/scripts/main.py monitor EMP_0001 --follow
python3 agent-manager/scripts/main.py assign EMP_0002 <<'EOF'
Follow teams/fractalmind-ai-maintenance.md Workflow
EOF
```

## Observações

- Requer `tmux` e `python3`.
- Agentes são configurados em um diretório `agents/` (consulte o repositório para exemplos).