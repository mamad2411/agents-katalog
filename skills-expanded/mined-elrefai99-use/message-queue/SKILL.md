---
name: message-queue
metadata:
  author: Mohamed
description: >
  Scaffold, architect, and implement production-grade message queue systems using BullMQ (Redis-backed),
  AWS SQS, or Agenda (MongoDB/PostgreSQL) in a Node.js + TypeScript + Express backend.
  Use this skill whenever the user mentions queues, workers, jobs, background tasks, scheduled tasks,
  cron jobs, producers, consumers, SQS, BullMQ, Agenda, or wants to process tasks asynchronously.
  Also trigger when the user asks to "add a worker", "process jobs in the background",
  "retry failed tasks", "schedule a recurring job", or "offload heavy work from the request cycle".
  Use even for vague requests like "I need to send emails in the background" or "run this job every night".
---

# Message Queue Skill

Covers three systems: **BullMQ**, **AWS SQS**, and **Agenda**.

Each has a dedicated reference file. Load only the one relevant to the user's system.

| System   | When to use                                          | Reference file          |
|----------|------------------------------------------------------|-------------------------|
| BullMQ   | Redis-backed, real-time, priority queues, repeatable | `references/bullmq.md`  |
| SQS      | AWS-native, distributed, decoupled microservices     | `references/sqs.md`     |
| Agenda   | MongoDB/PostgreSQL, cron, human-readable scheduling  | `references/agenda.md`  |

---

## How to Respond

### Planning / Architecture mode (default)

1. Show a **Mermaid sequence diagram** of the queue flow first.
2. Show the **folder structure** (tree with one-line annotations).
3. Explain tradeoffs if multiple approaches apply.
4. Do NOT generate file contents unless asked.

### Code mode (triggered by: write code / implement / show code / fix code)

1. Load the relevant reference file.
2. Follow the file structure from that reference.
3. Produce typed, production-ready TypeScript — no `any`, no `console.log`, no stack traces in responses.
4. Follow conventions from `express-module-architecture` if integrating into an Express module.

---

## Folder Structure

### Standalone (not tied to an Express module)

```
src/
└── queues/
    ├── @types/
    │   └── index.d.ts              → Shared job payload types, queue names enum
    ├── {queue-name}/
    │   ├── producer.ts             → Enqueues jobs
    │   ├── worker.ts               → Processes jobs, retry logic
    │   ├── handlers/
    │   │   └── {job-type}.handler.ts → One file per job type
    │   └── index.ts                → Barrel export
    ├── scheduler.ts                → Repeatable/cron job registration (BullMQ / Agenda)
    └── index.ts                    → Initializes all queues/workers on app boot
```

### Integrated with Express module (express-module-architecture)

Queue lives inside the module that owns the domain:

```
src/
└── modules/
    └── {name}/
        ├── queue/
        │   ├── {name}.producer.ts  → Enqueues domain jobs
        │   ├── {name}.worker.ts    → Consumes + processes jobs
        │   └── handlers/
        │       └── {job}.handler.ts
        ├── service/
        │   └── {name}.service.ts   → Calls producer, orchestrates logic
        └── index.ts                → Barrel: exports router, service, producer
```

---

## Naming Rules

- Queue names: `SCREAMING_SNAKE_CASE` enum → `QueueName.EMAIL_NOTIFICATION`
- Job types: string literal union → `type EmailJobType = 'welcome' | 'reset-password'`
- Handlers: `{job-type}.handler.ts` → `welcome.handler.ts`
- Workers: `{name}.worker.ts` → `email.worker.ts`
- Producers: `{name}.producer.ts` → `email.producer.ts`

---

## Cross-cutting Concerns (all systems)

### Retry strategy defaults
- Max attempts: 3
- Backoff: exponential (`delay * 2^attempt`)
- Dead letter: separate queue/collection after max attempts exceeded

### Monitoring hooks
- Emit structured logs (Winston/Pino) on `completed`, `failed`, `stalled`
- Never log job payload in prod (PII risk)
- Track queue depth as a metric (CloudWatch / custom endpoint)

### Concurrency defaults
| System  | Default concurrency | Notes                          |
|---------|---------------------|--------------------------------|
| BullMQ  | `concurrency: 5`    | Per worker instance            |
| SQS     | `batchSize: 10`     | Adjust to Lambda/EC2 capacity  |
| Agenda  | `maxConcurrency: 5` | Global + per-job override      |

---

## Reference Files

Load the relevant one before generating any code or detailed architecture:

- BullMQ → `references/bullmq.md`
- SQS → `references/sqs.md`
- Agenda → `references/agenda.md`
