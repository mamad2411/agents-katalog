---
name: konecty-meta-namespace
description: "Manage Konecty Namespace global configuration: email servers, RabbitMQ queue config, storage, webhooks, plan settings, portal config. Use when the user wants to configure SMTP servers, add RabbitMQ queues, set up storage, configure global webhooks (onCreate/onUpdate/onDelete), manage Konsistent settings, or view global tenant configuration. Requires admin credentials."
---

# Konecty Meta Namespace

Manage the global Namespace singleton configuration.

## Prerequisites

Requires **admin** credentials from **konecty-session**. User must have `admin: true`.

## Workflow

### 1. Show the full Namespace

```bash
python3 scripts/meta_namespace.py show
```

### 2. List email servers

```bash
python3 scripts/meta_namespace.py email-servers
```

### 3. Set or update an email server

```bash
python3 scripts/meta_namespace.py set-email-server smtp_foxter --host email-smtp.us-east-1.amazonaws.com --port 2587 --user AKIA... --pass secret
```

### 4. Show queue configuration

```bash
python3 scripts/meta_namespace.py queue-config
```

### 5. Add a queue to a resource

```bash
python3 scripts/meta_namespace.py add-queue rabbitmq_default my-new-queue
```

### 6. Set a global webhook

```bash
python3 scripts/meta_namespace.py set-webhook onCreate "https://api.example.com/sync/\${documentId}/\${dataId}"
```

### 7. Upsert full Namespace

```bash
python3 scripts/meta_namespace.py upsert --file namespace.json
```

## Key concepts

- Singleton: `_id: "Namespace"`, `type: "namespace"`
- See [references/namespace-schema.md](references/namespace-schema.md) for full schema documentation
- `emailServers` keys are referenced by hooks: `emails.push({ server: "smtp_foxter" })`
- `QueueConfig.resources` are referenced by `document.events`: `event.resource: "rabbitmq_default"`
- `QueueConfig.konsistent: [resourceName, queueName]` for external Konsistent
- `plan.useExternalKonsistent` must be `true` for queue-based Konsistent
- `onCreate/onUpdate/onDelete` are global webhooks for ALL documents

## Script reference

See [scripts/meta_namespace.py](scripts/meta_namespace.py). Stdlib only.
