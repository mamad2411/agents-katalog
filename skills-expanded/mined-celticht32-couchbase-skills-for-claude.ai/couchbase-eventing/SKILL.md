---
name: couchbase-eventing
description: "Design, deploy, and troubleshoot Couchbase Eventing functions. Use whenever the user asks about Eventing, eventing functions, JavaScript functions on document mutations, source bucket, metadata bucket, source keyspace, metadata keyspace, OnUpdate, OnDelete, cron triggers, curl() in eventing, N1QL in eventing, eventing deployment state (deployed / undeployed / paused), eventing worker count, DCP feed, Eventing service, admin_eventing_* tools, or 'how do I run code when a document changes.' Distinct from couchbase-mcp (calling the tools) and couchbase-app-integration (SDK-based change notification via DCP/Kafka). Use proactively when the user has a change-driven processing need: cache warming, audit logging, cross-collection sync, event publishing, or derived document generation."
license: MIT
---

# Couchbase Eventing

A skill for *designing and operating* Couchbase Eventing functions — JavaScript that runs in response to document mutations in a source collection.

Distinct from:
- `couchbase-mcp` — calling `admin_eventing_*` tools to deploy and manage functions
- `couchbase-app-integration` — SDK-based DCP consumer code for change processing outside the cluster
- `couchbase-data-modeling` — document shape decisions

If the conversation is "I want to run code when a document changes," this is the right skill.

## When this skill applies

- "How do Eventing functions work?"
- "How do I deploy an Eventing function?"
- "How do I write an OnUpdate handler?"
- "How do I call an external API from Eventing?"
- "Can I run SQL++ from inside an Eventing function?"
- "How do I sync data between two collections automatically?"
- "Eventing function is deployed but nothing happens"
- "How do I debug an Eventing function?"
- "What's the metadata bucket / keyspace for?"
- "How do I handle errors in Eventing functions?"

## Pick the right reference

| Question | Read |
|---|---|
| "How do I write the JavaScript? OnUpdate, OnDelete, cron, curl, N1QL?" | `references/function-authoring.md` |
| "How do I configure and deploy a function — source, metadata, workers, bindings?" | `references/deployment.md` |
| "Function isn't triggering / processing slowly / throwing errors — what's wrong?" | `references/troubleshooting.md` |

## Three core principles

**Principle 1 — Eventing is exactly-once delivery from the DCP feed, not exactly-once execution.**
The Eventing service reads from Couchbase's internal DCP (Database Change Protocol) feed. Each mutation triggers `OnUpdate` or `OnDelete` once *in the steady state*. But during node failures, rebalances, or function redeploys, a mutation can be delivered more than once. Write your handlers to be idempotent — running the same function against the same document twice should produce the same result.

**Principle 2 — The metadata keyspace is reserved; never store application data there.**
The Eventing service uses the metadata keyspace internally to track which mutations have been processed (checkpointing), manage timers, and store function state. Writing application documents into it causes unpredictable behaviour. Create a dedicated bucket/scope/collection for metadata, separate from your application data.

**Principle 3 — Eventing is not a general compute layer.**
Eventing handlers run synchronously per-mutation on the Eventing service nodes. Heavy computation, large curl() loops, or long-running N1QL queries inside handlers will queue mutations and cause the DCP feed to lag. For complex processing, emit a lightweight "work order" document to a queue collection and process it separately.

## Quick tool map

| Task | Tool |
|---|---|
| List all functions | `admin_eventing_list_functions` |
| Get one function's definition | `admin_eventing_get_function` |
| Create or update a function | `admin_eventing_upsert_function` |
| Delete a function | `admin_eventing_delete_function` |
| Deploy a function | `admin_eventing_deploy_function` |
| Undeploy a function | `admin_eventing_undeploy_function` |
| Pause a function (keeps state) | `admin_eventing_pause_function` |
| Resume a paused function | `admin_eventing_resume_function` |
| Get function stats (processing rate, backlogs) | `admin_eventing_get_function_stats` |

## Deployment state machine

```
Undeployed ──deploy──► Deployed ──undeploy──► Undeployed
                           │
                         pause
                           │
                           ▼
                        Paused ──resume──► Deployed
```

- **Undeployed:** function definition exists but no processing occurs. DCP checkpoint is not held.
- **Deployed:** function is actively processing mutations. DCP checkpoint is maintained.
- **Paused:** processing stops but the DCP checkpoint position is held. Resume continues from where processing stopped. Use pause instead of undeploy when you want to make function code changes without reprocessing all historical mutations.

Redeploying an undeployed function by default processes all existing documents in the source collection (a "from beginning" deployment). Use `deployment_config.from_now: true` to process only new mutations from the deployment point.

## Related skills

- `couchbase-mcp` — the `admin_eventing_*` tools that deploy and manage functions
- `couchbase-app-integration` — alternative: SDK-based DCP consumers for change processing in application code
- `couchbase-data-modeling` — source and destination document shapes
