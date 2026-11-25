---
name: slack-bot-builder
description: "Crie aplicativos Slack usando o framework Bolt em Python, JavaScript e Java. Abrange Block Kit para UIs ricas, componentes interativos, slash commands, tratamento de eventos, fluxos de instalação OAuth e integração com Workflow Builder. Foco em melhores práticas para aplicativos Slack prontos para produção. Use quando: slack bot, slack app, bolt framework, block kit, slash command."
source: vibeship-spawner-skills (Apache 2.0)
---

# Slack Bot Builder

## Padrões

### Padrão de Fundação da App Bolt

O framework Bolt é a abordagem recomendada pelo Slack para criar aplicativos.
Ele cuida da autenticação, roteamento de eventos, verificação de solicitações e
processamento de requisições HTTP para que você possa focar na lógica da aplicação.

Principais benefícios:
- Tratamento de eventos em poucas linhas de código
- Verificações de segurança e validação de payload incorporadas
- Padrões organizados e consistentes
- Funciona para experimentos e produção

Disponível em: Python, JavaScript (Node.js), Java


**Quando usar**: ['Começar qualquer novo aplicativo Slack', 'Migrar de APIs Slack legadas', 'Construir integrações Slack prontas para produção']

```python
# Python Bolt App
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

# Initialize with tokens from environment
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Handle messages containing "hello"
@app.message("hello")
def handle_hello(message, say):
    """Respond to messages containing 'hello'."""
    user = message["user"]
    say(f"Hey there <@{user}>!")

# Handle slash command
@app.command("/ticket")
def handle_ticket_command(ack, body, client):
    """Handle /ticket slash command."""
    # Acknowledge immediately (within 3 seconds)
    ack()

    # Open a modal for ticket creation
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "ticket_modal",
            "title": {"type": "plain_text", "text": "Create Ticket"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_input"
                    },
                    "label": {"type": "plain_text", "text": "Title"}
                },
                {
                    "type": "input",
                    "block_id": "desc_block",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "desc_input"
                    },
                    "label": {"type": "plain_text", "text": "Description"}
                },
                {
                    "type": "input",
                    "block_id": "priority_block",
                    "element": {
                        "type": "static_select",
                        "action_id": "priority_select",
   
```

### Padrão Block Kit UI

Block Kit é o framework UI do Slack para criar mensagens ricas e interativas.
Componha mensagens usando blocos (sections, actions, inputs) e elementos
(buttons, menus, text inputs).

Limites:
- Até 50 blocos por mensagem
- Até 100 blocos em modals/Home tabs
- Texto em blocos limitado a 3000 caracteres

Use o Block Kit Builder para prototipar: https://app.slack.com/block-kit-builder


**Quando usar**: ['Construir layouts de mensagens ricas', 'Adicionar componentes interativos às mensagens', 'Criar formulários em modals', 'Construir experiências na Home tab']

```python
from slack_bolt import App
import os

app = App(token=os.environ["SLACK_BOT_TOKEN"])

def build_notification_blocks(incident: dict) -> list:
    """Build Block Kit blocks for incident notification."""
    severity_emoji = {
        "critical": ":red_circle:",
        "high": ":large_orange_circle:",
        "medium": ":large_yellow_circle:",
        "low": ":white_circle:"
    }

    return [
        # Header
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{severity_emoji.get(incident['severity'], '')} Incident Alert"
            }
        },
        # Details section
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Incident:*\n{incident['title']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:*\n{incident['severity'].upper()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Service:*\n{incident['service']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Reported:*\n<!date^{incident['timestamp']}^{date_short} {time}|{incident['timestamp']}>"
                }
            ]
        },
        # Description
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Description:*\n{incident['description'][:2000]}"
            }
        },
        # Divider
        {"type": "divider"},
        # Action buttons
        {
            "type": "actions",
            "block_id": f"incident_actions_{incident['id']}",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Acknowledge"},
                    "style": "primary",
                    "action_id": "acknowle
```

### Padrão de Instalação OAuth

Permita que os usuários instalem seu aplicativo em seus workspaces via OAuth 2.0.
Bolt cuida da maioria do fluxo OAuth, mas você precisa configurá-lo
e armazenar os tokens com segurança.

Conceitos-chave de OAuth:
- Scopes definem permissões (solicite o mínimo necessário)
- Tokens são específicos do workspace
- Dados de instalação devem ser armazenados permanentemente
- Usuários podem adicionar scopes posteriormente (aditivo)

70% dos usuários abandonam a instalação quando confrontados com solicitações
de permissão excessivas - solicite apenas o que você precisa!


**Quando usar**: ['Distribuir aplicativo para múltiplos workspaces', 'Construir aplicativos Slack públicos', 'Integrações de nível empresarial']

```python
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
import os

# For production, use database-backed stores
# For example: PostgreSQL, MongoDB, Redis

class DatabaseInstallationStore:
    """Store installation data in your database."""

    async def save(self, installation):
        """Save installation when user completes OAuth."""
        await db.installations.upsert({
            "team_id": installation.team_id,
            "enterprise_id": installation.enterprise_id,
            "bot_token": encrypt(installation.bot_token),
            "bot_user_id": installation.bot_user_id,
            "bot_scopes": installation.bot_scopes,
            "user_id": installation.user_id,
            "installed_at": installation.installed_at
        })

    async def find_installation(self, *, enterprise_id, team_id, user_id=None, is_enterprise_install=False):
        """Find installation for a workspace."""
        record = await db.installations.find_one({
            "team_id": team_id,
            "enterprise_id": enterprise_id
        })

        if record:
            return Installation(
                bot_token=decrypt(record["bot_token"]),
                # ... other fields
            )
        return None

# Initialize OAuth-enabled app
app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    oauth_settings=OAuthSettings(
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        scopes=[
            "channels:history",
            "channels:read",
            "chat:write",
            "commands",
            "users:read"
        ],
        user_scopes=[],  # User token scopes if needed
        installation_store=DatabaseInstallationStore(),
        state_store=FileOAuthStateStore(expiration_seconds=600)
    )
)

# OAuth routes are handled a
```

## ⚠️ Armadilhas Perigosas

| Problema | Severidade | Solução |
|----------|-----------|--------|
| Problema | crítica | ## Reconheça imediatamente, processe depois |
| Problema | crítica | ## Validação adequada de estado |
| Problema | crítica | ## Nunca codifique nem registre em log tokens |
| Problema | alta | ## Solicite os scopes mínimos necessários |
| Problema | média | ## Conheça e respeite os limites |
| Problema | alta | ## Socket Mode: Apenas para desenvolvimento |
| Problema | crítica | ## Bolt cuida disso automaticamente |