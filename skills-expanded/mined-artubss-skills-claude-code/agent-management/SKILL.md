---
name: agent-management
description: Criar, gerenciar e orquestrar agentes de IA usando o CLI AI Maestro. Use quando o usuário pedir para "criar agente", "listar agentes", "deletar agente", "hibernar agente", "despertar agente", "instalar plugin", "mostrar agente", "reiniciar agente" ou qualquer tarefa de gerenciamento do ciclo de vida do agente.
---

# Gerenciamento de Agentes AI Maestro

Crie, gerencie e orquestre múltiplos agentes de IA através de um CLI unificado. Gerencia o ciclo de vida completo do agente: criar, hibernar, despertar, renomear, exportar/importar e gerenciamento de plugins. Parte da suite [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Pré-requisitos

Requer [AI Maestro](https://github.com/23blocks-OS/ai-maestro) executando localmente com tmux 3.0+.

```bash
# Instalar o CLI
git clone https://github.com/23blocks-OS/ai-maestro-plugins.git
cd ai-maestro-plugins && ./install-agent-cli.sh
```

## Comandos Principais

### Ciclo de Vida do Agente

| Comando | Descrição |
|---------|-----------|
| `aimaestro-agent.sh list` | Listar todos os agentes com status |
| `aimaestro-agent.sh show <agent>` | Informações detalhadas do agente |
| `aimaestro-agent.sh create <name> --dir <path>` | Criar novo agente |
| `aimaestro-agent.sh update <agent> --task "..."` | Atualizar tarefa/tags |
| `aimaestro-agent.sh delete <agent> --confirm` | Deletar agente |
| `aimaestro-agent.sh rename <old> <new>` | Renomear agente |
| `aimaestro-agent.sh hibernate <agent>` | Salvar estado, liberar recursos |
| `aimaestro-agent.sh wake <agent>` | Retomar agente hibernado |
| `aimaestro-agent.sh restart <agent>` | Hibernar e depois despertar |

### Gerenciamento de Plugins

| Comando | Descrição |
|---------|-----------|
| `aimaestro-agent.sh plugin install <agent> <plugin>` | Instalar plugin |
| `aimaestro-agent.sh plugin uninstall <agent> <plugin>` | Remover plugin |
| `aimaestro-agent.sh plugin list <agent>` | Listar plugins instalados |
| `aimaestro-agent.sh plugin marketplace add <agent> <source>` | Adicionar marketplace |

### Exportar/Importar

| Comando | Descrição |
|---------|-----------|
| `aimaestro-agent.sh export <agent>` | Exportar configuração do agente |
| `aimaestro-agent.sh import <file>` | Importar agente do arquivo |

## Exemplos de Uso

```bash
# Criar um agente backend API
aimaestro-agent.sh create backend-api \
  --dir ~/projects/backend \
  --task "Build REST API with TypeScript" \
  --tags "api,typescript"

# Fim do dia -- economizar recursos
aimaestro-agent.sh hibernate frontend-ui
aimaestro-agent.sh hibernate data-processor

# Retomar na manhã seguinte
aimaestro-agent.sh wake frontend-ui --attach

# Instalar um plugin em um agente
aimaestro-agent.sh plugin install backend-api my-plugin

# Fazer backup antes de mudanças arriscadas
aimaestro-agent.sh export backend-api -o backup.json
```

## Status dos Agentes

| Status | Significado |
|--------|------------|
| `online` | Executando em sessão tmux |
| `offline` | Registrado mas sem sessão ativa |
| `hibernated` | Estado salvo, sessão encerrada |

## Experiência Completa AI Maestro

Esta skill faz parte da plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro), que oferece **6 skills** para orquestração de agentes de IA: mensagens, memória, documentos, grafo, planejamento e gerenciamento de agentes.