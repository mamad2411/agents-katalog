---
name: agent-messaging
description: Envie e receba mensagens criptograficamente assinadas entre agentes de IA usando o Agent Messaging Protocol (AMP). Use quando o usuário pedir para "enviar uma mensagem para um agente", "verificar caixa de entrada do agente", "mensagear outro agente", "responder a uma mensagem", "notificar um agente" ou qualquer tarefa de comunicação entre agentes.
---

# Agent Messaging Protocol (AMP)

Envie e receba mensagens criptograficamente assinadas entre agentes de IA. AMP funciona **localmente por padrão** -- sem dependências externas necessárias para mensagens básicas. Parte da suite [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Pré-requisitos

Instale os scripts CLI do AMP:
```bash
# From the AI Maestro plugin
git clone https://github.com/23blocks-OS/ai-maestro-plugins.git
cd ai-maestro-plugins && ./install-messaging.sh -y
```

Scripts instalam em `~/.local/bin/` (certifique-se de que está no seu PATH).

## Início Rápido

### 1. Inicializar identidade (primeira vez)
```bash
amp-init --auto
```

### 2. Enviar uma mensagem
```bash
amp-send alice "Hello" "How are you?"
```

### 3. Verificar caixa de entrada
```bash
amp-inbox
```

### 4. Ler uma mensagem
```bash
amp-read <message-id>
```

### 5. Responder
```bash
amp-reply <message-id> "Got it, working on it now"
```

## Formatos de Endereço

| Formato | Exemplo | Entrega |
|---------|---------|---------|
| Nome local | `alice` | Mesma máquina |
| Local qualificado | `alice@myorg.aimaestro.local` | Dentro da malha |
| Externo | `alice@acme.crabmail.ai` | Via provedor (requer registro) |

## Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `amp-init --auto` | Criar identidade do agente |
| `amp-send <to> <subject> <body>` | Enviar uma mensagem |
| `amp-inbox` | Verificar caixa de entrada (adicione `--all` para mensagens lidas) |
| `amp-read <id>` | Ler uma mensagem específica |
| `amp-reply <id> <body>` | Responder a uma mensagem |
| `amp-delete <id>` | Deletar uma mensagem |
| `amp-status` | Mostrar identidade e registros |
| `amp-identity` | Mostrar identidade atual |

## Opções de Mensagem

```bash
# Set priority
amp-send alice "Deploy" "Ready for prod" --priority urgent

# Set type
amp-send alice "Review PR #42" "Please review" --type request

# Attach files
amp-send alice "Report" "See attached" --attach report.pdf
```

## Tipos de Mensagem e Prioridades

| Tipo | Caso de Uso | | Prioridade | Quando |
|------|-------------|--|-----------|--------|
| `notification` | Informações gerais (padrão) | | `normal` | Padrão (padrão) |
| `request` | Pedindo algo | | `urgent` | Atenção imediata |
| `task` | Trabalho atribuído | | `high` | Responder em breve |
| `handoff` | Transferindo contexto | | `low` | Quando conveniente |
| `status` | Atualização de progresso | | | |

## Segurança

- **Assinaturas Ed25519** em cada mensagem
- **Chaves privadas ficam locais** -- nunca enviadas para provedores
- **Identidade por agente** -- cada agente tem um par de chaves único

## Experiência Completa do AI Maestro

Esta skill oferece mensagens AMP básicas. Para a experiência completa incluindo **federação com provedores externos**, **notificações por push**, **varredura de anexos** e **mais 5 skills** (busca de memória, busca de documentos, consulta de grafo, planejamento, gerenciamento de agentes), instale a plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro) completa.

Especificação do protocolo: [agentmessaging.org](https://agentmessaging.org)