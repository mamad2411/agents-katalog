---
name: intercom-patterns
description: Intercom integration patterns — webhook event handling, Conversations API, Contacts API, custom inbox channels, operator bot flows, and multi-tenant workspace management.
origin: local
---

# Intercom Integration Patterns

Patterns for integrating with Intercom: webhooks, Conversations API, Contacts API, and custom channels.

## When to Activate

- Building or extending Intercom webhook handlers
- Working with Conversations or Contacts API
- Implementing custom inbox channels (email, WhatsApp, etc.)
- Designing AI/bot reply flows triggered by Intercom events
- Managing multi-workspace Intercom setups
- Debugging Intercom delivery failures or signature mismatches

## Webhook Handling

### Signature Verification

Always verify the `X-Hub-Signature` header before processing any webhook.

```python
import hashlib, hmac
from fastapi import Request, HTTPException

INTERCOM_CLIENT_SECRET = settings.INTERCOM_CLIENT_SECRET

async def verify_intercom_signature(request: Request) -> bytes:
    """Verify Intercom webhook signature. Returns raw body."""
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature", "")

    if not signature.startswith("sha1="):
        raise HTTPException(status_code=401, detail="Missing signature")

    expected = "sha1=" + hmac.new(
        INTERCOM_CLIENT_SECRET.encode(),
        raw_body,
        hashlib.sha1,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")

    return raw_body
```

### Webhook Endpoint Pattern

```python
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/webhooks/intercom")

class IntercomWebhookPayload(BaseModel):
    type: str
    app_id: str
    data: dict[str, Any]
    delivery_attempts: int = 1

@router.post("")
async def handle_intercom_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    raw_body = await verify_intercom_signature(request)
    payload = IntercomWebhookPayload.model_validate_json(raw_body)

    # Respond immediately — Intercom retries if response > 20s
    background_tasks.add_task(dispatch_event, payload)
    return {"status": "accepted"}

async def dispatch_event(payload: IntercomWebhookPayload):
    topic = payload.type  # e.g. "conversation.created"
    handlers = {
        "conversation.created": handle_conversation_created,
        "conversation.reply.created": handle_reply_created,
        "conversation.user.created": handle_user_message,
        "conversation.assigned": handle_assigned,
        "contact.created": handle_contact_created,
    }
    handler = handlers.get(topic)
    if handler:
        await handler(payload.data)
    else:
        logger.info("Unhandled Intercom topic", topic=topic)
```

### Retry / Idempotency

Intercom retries webhooks up to 5 times on non-2xx responses (backoff: 5min, 30min, 1h, 6h, 24h).

```python
from redis.asyncio import Redis

async def handle_conversation_created(data: dict, redis: Redis):
    # Deduplicate using delivery ID
    event_id = data.get("item", {}).get("id")
    key = f"intercom:processed:{event_id}"

    already_processed = await redis.set(key, "1", nx=True, ex=86400)  # 24h TTL
    if not already_processed:
        logger.info("Duplicate Intercom event, skipping", event_id=event_id)
        return

    await process_new_conversation(data["item"])
```

## Conversations API

### Reply to a Conversation

```python
import httpx

INTERCOM_TOKEN = settings.INTERCOM_ACCESS_TOKEN

async def reply_to_conversation(
    conversation_id: str,
    message: str,
    message_type: str = "comment",  # "comment" | "note"
    admin_id: str | None = None,
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.intercom.io/conversations/{conversation_id}/reply",
            headers={
                "Authorization": f"Bearer {INTERCOM_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Intercom-Version": "2.11",
            },
            json={
                "type": "admin",
                "admin_id": admin_id or settings.INTERCOM_BOT_ADMIN_ID,
                "message_type": message_type,
                "body": message,
            },
        )
        response.raise_for_status()
        return response.json()
```

### Assign Conversation

```python
async def assign_conversation(
    conversation_id: str,
    assignee_id: str,
    assignee_type: str = "team",  # "team" | "admin"
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.intercom.io/conversations/{conversation_id}/parts",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            json={
                "type": "admin",
                "admin_id": settings.INTERCOM_BOT_ADMIN_ID,
                "message_type": "assignment",
                "assignee_id": assignee_id,
                "assignee_type": assignee_type,
            },
        )
        response.raise_for_status()
        return response.json()
```

### Fetch Full Conversation

```python
async def get_conversation(conversation_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.intercom.io/conversations/{conversation_id}",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            params={"display_as": "plaintext"},  # Avoid parsing HTML
        )
        response.raise_for_status()
        return response.json()

def extract_messages(conversation: dict) -> list[dict]:
    """Extract conversation history for LLM context."""
    messages = []

    # First message
    source = conversation.get("source", {})
    if source.get("body"):
        messages.append({
            "role": "user",
            "content": source["body"],
            "author": source.get("author", {}).get("type"),
        })

    # Conversation parts (replies)
    for part in conversation.get("conversation_parts", {}).get("conversation_parts", []):
        if part.get("body") and part["part_type"] not in ("close", "open", "assignment"):
            messages.append({
                "role": "assistant" if part["author"]["type"] == "admin" else "user",
                "content": part["body"],
                "author_type": part["author"]["type"],
            })

    return messages
```

## Contacts API

### Find or Create Contact

```python
async def find_or_create_contact(email: str, name: str | None = None) -> dict:
    async with httpx.AsyncClient() as client:
        # Search first
        search_resp = await client.post(
            "https://api.intercom.io/contacts/search",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            json={"query": {"field": "email", "operator": "=", "value": email}},
        )
        results = search_resp.json().get("data", [])
        if results:
            return results[0]

        # Create if not found
        create_resp = await client.post(
            "https://api.intercom.io/contacts",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            json={"role": "user", "email": email, "name": name},
        )
        create_resp.raise_for_status()
        return create_resp.json()
```

### Update Contact Attributes

```python
async def update_contact(contact_id: str, custom_attributes: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://api.intercom.io/contacts/{contact_id}",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            json={"custom_attributes": custom_attributes},
        )
        response.raise_for_status()
        return response.json()
```

## Custom Inbox Channel (Switch API)

Used when you want to receive messages from external channels (WhatsApp, Telegram, custom chat) through Intercom's inbox.

```python
async def create_conversation_from_channel(
    contact_id: str,
    message: str,
    channel_id: str,  # Custom channel ID from Intercom
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.intercom.io/conversations",
            headers={"Authorization": f"Bearer {INTERCOM_TOKEN}", "Intercom-Version": "2.11"},
            json={
                "from": {"type": "contact", "id": contact_id},
                "body": message,
                "channel_initiated_by": "contact",
                "custom_channel_id": channel_id,
            },
        )
        response.raise_for_status()
        return response.json()
```

## AI Bot Reply Pattern

Full flow: webhook → extract context → LLM → reply to Intercom.

```python
async def handle_user_message(data: dict):
    conversation = data["item"]
    conversation_id = conversation["id"]

    # Skip if already handled by a human
    if conversation.get("assignee", {}).get("type") == "admin":
        return

    # Get full conversation for context
    full_conv = await get_conversation(conversation_id)
    messages = extract_messages(full_conv)

    # Generate AI reply
    ai_response = await generate_reply(messages)

    if ai_response.should_escalate:
        # Hand off to human team
        await assign_conversation(conversation_id, settings.SUPPORT_TEAM_ID)
        await reply_to_conversation(
            conversation_id,
            "Transfiriendo a un agente. Un momento.",
            message_type="comment",
        )
    else:
        await reply_to_conversation(conversation_id, ai_response.message)
```

## Multi-Tenant / Multi-Workspace

When managing Intercom for multiple tenants, each with their own workspace:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from cheo.models import TenantIntercomConfig

async def get_tenant_intercom_client(
    tenant_id: str,
    db: AsyncSession,
) -> "IntercomClient":
    config = await db.get(TenantIntercomConfig, tenant_id)
    if not config:
        raise ValueError(f"No Intercom config for tenant {tenant_id}")
    return IntercomClient(
        access_token=config.access_token,
        bot_admin_id=config.bot_admin_id,
    )

# Webhook routing by app_id
async def route_webhook_to_tenant(payload: IntercomWebhookPayload):
    tenant = await get_tenant_by_intercom_app_id(payload.app_id)
    if not tenant:
        logger.warning("Unknown Intercom app_id", app_id=payload.app_id)
        return
    await dispatch_event_for_tenant(payload, tenant)
```

## Rate Limits

| Plan | Requests/minute |
|------|----------------|
| Essential | 350 |
| Advanced+ | 500 |

```python
import asyncio
from tenacity import retry, wait_exponential, retry_if_exception

def is_rate_limited(exc: Exception) -> bool:
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429

@retry(
    retry=retry_if_exception(is_rate_limited),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(5),
)
async def intercom_request(method: str, url: str, **kwargs) -> dict:
    async with httpx.AsyncClient() as client:
        response = await getattr(client, method)(url, **kwargs)
        response.raise_for_status()
        return response.json()
```

## Key Webhook Topics

| Topic | Description |
|-------|-------------|
| `conversation.created` | New conversation started |
| `conversation.user.created` | User sent a new message |
| `conversation.reply.created` | Any reply (user or admin) |
| `conversation.assigned` | Conversation assigned to team/admin |
| `conversation.read` | Conversation marked as read |
| `contact.created` | New contact created |
| `contact.signed_up` | Contact signed up |
| `contact.tag.created` | Tag added to contact |

## Reference Skills

- Async HTTP patterns → skill: `fastapi-patterns`
- LLM reply generation → skill: `llm-engineering`
- Multi-tenant data isolation → skill: `multi-tenant-saas`
