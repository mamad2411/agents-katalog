---
name: recording-studio-data-shape
description: Choose recordings, recordables, events, logs, or a separate table. Use when modelling new data, deciding whether something belongs in the tree, or when tempted to add a recordable for facts, exhaust, derived data, or polymorphism.
---

# Data shape

Recording Studio is the **shared object layer**. Separate tables are the **fact, infrastructure, and scale layer**. Do not make everything a Recording merely because you can.

First decide whether this is a Recording at all. Then decide what belongs on the Recording vs the Recordable. Writes: `recording-studio-saving`. New types: `recording-studio-new-recordable`.

## Layers

| It is… | Use | Example |
|---|---|---|
| A durable product-managed object in the tree | **Recording + recordable** | Workspace, folder, page, webhook *endpoint* |
| Immutable type-specific state for that object | **Recordable** (snapshot) | Page title and body; endpoint URL |
| History of that object’s lifecycle or a capability action | **Event** (`log_event!`) | Page revised, folder moved, kit published |
| Caused activity they do not own as content | **Log** or a normal table | Webhook *delivery* attempts, page views, usage |

**Event** and **Log** are not the same. Events answer “what happened to this object?” Logs answer “what operational exhaust do we still need to query?”

Webhook **endpoints** (the configuration people create) are recordings. Webhook **deliveries** (each attempt, payload, status) are logs.

## Decision flow

1. Is this a durable, product-managed object with shared ecosystem value? If no → Log or a separate table.
2. If yes → Recording + Recordable.
3. Shared identity, hierarchy, mixins → Recording.
4. Type-specific snapshot and behaviour → Recordable (`revise`, never mutate in place).
5. Lifecycle history of that object → Event (`log_event!`).
6. Needs to reference a Recording but is not tree content → foreign key, not a child Recording.

## When to use a Recording

Use a Recording when the thing behaves like a durable, product-managed object in the ecosystem.

A Recording is a good fit when:

- People (or the product) create or manage it as a first-class thing
- You need change history, or who changed what and when
- Reverting or restoring a previous version would make sense
- It has a durable identity even as its attributes change
- It should participate in shared capabilities
- Other gems should operate on it without knowing the Recordable type
- It belongs as a first-class node in the Recording hierarchy

Typical shared capabilities: move, duplicate, attachments, comments, trash, publish, order, access. Later mixins (workflows, AI actions) follow the same rule — enable them on types that are already Recordings, do not invent a Recording just to hang a mixin on it.

User editability is a strong signal, not a hard gate. A workspace created at signup still belongs in the tree.

> If something behaves like a product-managed object in the ecosystem, prefer a Recording.

## Recording vs Recordable

The Recording is thin and universal. The Recordable holds domain-specific data and behaviour.

- Shared concepts belong on Recording (identity, parent, mixins, generic traversal).
- Type-specific concepts belong on the Recordable.
- Do not duplicate authoritative state between the two tables.
- Recordables are **immutable snapshots**. Change state with `revise`; append history with `log_event!`.

> Keep Recording thin and universal; keep domain-specific behaviour in the Recordable.

## Hierarchy

Use a Recording when the thing needs to be a **first-class part of the parent/child tree**.

Useful when:

- Parent or children have meaningful domain significance
- Location in the tree says what the entity is
- Generic traversal should discover it
- Move and duplicate should apply
- Permissions or other behaviour may inherit through the hierarchy

```text
Project
└── Media Kit
    ├── Image
    └── Document
```

These belong in the Recording hierarchy.

### Belongs-to is not a child

> “Belongs to a Recording” is not the same as “is a child Recording.”

A separate table can hold `recording_id` (or similar) when it needs to reference a Recording without joining the tree.

Examples: log entry, lifecycle Event, page view, webhook attempt, usage measurement.

> If the parent/child relationship describes what the thing **is**, favour a Recording.

> If it merely describes what the thing **relates to**, use a normal foreign key.

## When to use a separate table or log

Use a normal table (or the gem’s **log** API) when the data is a fact, operational record, measurement, or infrastructure concern — not a product-managed object.

Good fits: logs, analytics, page views, usage, webhook deliveries, job executions, telemetry, search indexes, cached or derived data.

Especially when:

- The data is immutable and written once
- The row itself *is* the history
- Reverting an old version would not make sense
- It does not need Recording capabilities
- It is system-generated rather than product-managed
- Volume or churn would make the `recordings` table a dumping ground

> Immutable, system-generated, or high-volume data usually belongs outside Recording.

Owned content: `recording-studio-saving`. Exhaust: the gem’s log API — not `root.record(Delivery)`. Product words: `recording-studio-text`. Admin screens that inspect deliveries should read **logs**, not invent a recordable type per attempt (`recording-studio-admin`).

## Objects versus facts

Recordings model **things**. Events and logs model **things that happened**.

Objects (usually Recordings): Project, Media Kit, Image, Document.

Facts (usually tables / logs): a user viewed this page; a webhook was delivered; an action failed; a token was consumed.

A Recording can be the current editable object while separate events or logs record what happened to it:

```text
Recording — current editable Media Kit

Events
└── Media Kit published   (lifecycle of that recording)

Logs / tables
├── Media Kit viewed
└── webhook delivery for that kit
```

Do not force operational history into the hierarchy just because it relates to a Recording.

## High-volume, high-churn, and derived data

Avoid Recordings for counters, heartbeats, job progress, token usage, analytics, telemetry, and page views. They create unnecessary recording rows, versions, and history. Optimise those tables for their own query and aggregation patterns.

Do not normally make derived or rebuildable data a Recording: search indexes, cached summaries, aggregated statistics, materialised projections, calculated values.

If the system can regenerate it and people do not manage it directly, keep it outside the Recording layer.

> The central Recording table should not become the dumping ground for every piece of system data.

## Do not use Recording just for polymorphism

Do not create a Recording merely because several entity types need a shared reference. A normal polymorphic association or foreign key may be enough.

Recording should buy identity, history, hierarchy, shared capabilities, or generic ecosystem behaviour.

> Recording should buy us meaningful shared behaviour, not merely another level of indirection.

## Useful questions

1. Is this a product-managed object or a fact that happened?
2. Can people edit it, or does the product manage it as a durable thing?
3. Does change history matter? Would reverting ever make sense?
4. Does it have a durable identity?
5. Should other Recording Studio gems operate on it generically?
6. Does it need shared capabilities?
7. Is it genuinely part of the Recording hierarchy?
8. Does its parent tell us what the thing **is**, or merely what it relates to?
9. Could there eventually be millions of these rows?
10. Is it high-churn, machine-generated, derived, or rebuildable?
11. Would making it a Recording provide meaningful shared behaviour?

If most answers point at exhaust, volume, or “just a reference,” it is not a Recording.

## Do not

- Add a recordable type because “we need to store these rows.”
- Put billing invoices, deliveries, or request dumps in the tree to reuse Accessible by accident. Access stays on the **endpoint** or root; the log rows hang off that.
- Duplicate the same fact as an Event *and* a Log unless they answer different questions (lifecycle vs exhaust).
- Use `record` / `revise` for logs or plain tables.

## Related

`recording-studio-saving`, `recording-studio-new-recordable`, `recording-studio-capabilities`, `recording-studio-admin`, `recording-studio-big-picture`.
