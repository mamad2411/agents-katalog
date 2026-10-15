---
name: stackbone-debug
description: >-
  Use this skill when triaging an error, failure or unexpected behavior in a Stackbone workspace —
  a deep agent or a durable workflow running locally under `stackbone dev`, or an install
  deployed to a cloud / self-host.
  Covers SDK errors ({ data, error } envelope codes from the catalog returned by the ambient `stackbone`
  client), HTTP 4xx/5xx from the control plane, durable run failures and timeouts, `workflow_input_invalid`
  (a workflow start whose input failed its declared schema), HITL stuck at either level (a workflow parked on a
  `requestApproval()` gate, or an agent turn `interrupted` on a tool gated with `interruptOn`), durable-session
  issues (memory not surviving because `x-stackbone-session` wasn't sent, or the checkpointer package is missing),
  database slow queries / missing indexes / pgvector mismatches, secrets decryption errors, connector
  action failures via `stackbone.connection(id)` (ambiguous / unauthorized connections), publish/build failures
  (SDK inlined, native dep), tier quota exceeded responses, and OpenRouter rate-limit / billing-paused
  situations. Trigger on requests like: my agent isn't working, why is this 500, this run hung, the HITL inbox is
  empty but the run is paused, the agent forgot the conversation, the workflow rejected my input, publish failed,
  why am I getting 402, why is my connector call ambiguous, the model call returns no response. The skill guides
  diagnostic command execution; it does not propose fixes — once you've located the cause, switch back to the
  stackbone or stackbone-cli skill to implement the fix.
license: MIT
metadata:
  author: stackbone
  version: '1.2.0'
  organization: Stackbone
  date: July 2026
---

# Stackbone debug & diagnostics

This skill helps an AI coding agent **locate** the source of a failure in a Stackbone workspace — a deep agent or a durable workflow — it does not propose fixes. Once the cause is identified, switch back to the **stackbone** skill (for SDK / agent / workflow code changes) or the **stackbone-cli** skill (for CLI / db / publish actions) to implement the fix.

A workspace is a multi-piece project: a `deep-agents/` folder (one agent per subfolder, each a `deep-agents/<name>/index.ts` default-exporting `defineDeepAgent(...)`) and a `workflows/` folder (one durable workflow per `workflows/<name>.workflow.ts`, its name the file basename without `.workflow.ts`, exporting `<camelCase(name)>Workflow`). The registry is **discovered by convention** from those files; a `stackbone.config.ts` can only override the workflow list. Agents run **in-process** and are served over the standard OpenAI/Anthropic chat endpoints (the `model` field selects the agent); workflows are durable functions (`'use workflow'` / `'use step'`) triggered through the runtime's HTTP contract or the CLI. Every invocation — an agent turn or a workflow run — produces a **durable run** with a log you inspect after the fact.

> Deep agents, durable workflows and the workspace runtime are exercised by `stackbone dev` today. On a deployed cloud install the workflows / runs / HITL endpoints may still 404 until the prod port lands — a 404 there is expected, not a bug.

## How to use this skill

1. Capture the symptom verbatim from the user (error message, HTTP status, stuck run, unexpected output).
2. Match the symptom to a row in the tables below.
3. Run the diagnostic command **as-is** (these are read-only, safe).
4. Report what you found in plain narrative — exact command output, not paraphrase.
5. Hand off to `stackbone` or `stackbone-cli` for the fix.

> **Read-only by design.** No command in this skill mutates state. If a diagnostic requires a mutation (e.g. retrying a failed run), it's flagged with **⚠️ destructive** and the agent must surface the proposal to the user before executing.

---

## SDK errors — `{ data, error }` envelope

Most surface reads on the ambient `stackbone` client return a `{ data, error }` envelope. The `error` is `null` on success; otherwise it carries `{ code, message, cause?, meta? }`. `code` is a literal from the catalog (`<prefix>_<reason>`, e.g. `ai_rate_limited`, plus a handful of standalone setup-bug codes); `meta` is the structured escape hatch (paths, retry hints, AWS metadata, constraint names); `cause` carries the upstream error object. There is no `details`, `retryable`, or `nextActions` field on an `SdkError` — read `meta`/`cause` instead.

> Three surfaces do NOT use the envelope. `stackbone.database` is native Drizzle — `await` returns rows and **throws** on error (catch it, there's no `.error`). `callDeepAgent(name, input)` (from `@stackbone/sdk/workflow`) returns `{ text }` and **throws** on failure — the throw fails the enclosing `'use step'`, so the error shows in the run's log frames. And `stackbone.connection(id)` (the Stackbone Connect broker) returns the operation output directly and **throws** a `ConnectorCallError` on failure — match `err.code`, never `instanceof` (see the connectors note in the Secrets / config section).

| `error.code`                      | Where it comes from                                                                     | First diagnostic                                                                                                                                                                                             |
| --------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `capability_unavailable`          | A module (e.g. `stackbone.rag`) isn't granted by the negotiated protocol contract       | Gating is in the contract handshake, not a config field — if it persists it's a control-plane/install issue, not a workspace edit                                                                            |
| `rag_invalid_request`             | Input to `stackbone.rag.*` failed validation (missing `id`/`text`, bad shape)           | `error.message` names the missing/invalid field; check the call args                                                                                                                                         |
| `rag_schema_missing`              | The workspace's RAG tables aren't present on this install                               | The RAG schema is platform-provisioned per install — a missing one is a setup/provisioning issue, not a creator action                                                                                       |
| `rag_dim_mismatch`                | Stored embedding dimension differs from the query model's dimension                     | `error.meta` has the expected vs actual dims; the embedding model changed after ingest                                                                                                                       |
| `rag_embedding_failed`            | The embedder call failed (OpenRouter error, bad model)                                  | Inspect `error.cause`; confirm the embedding model the workspace configured                                                                                                                                  |
| `rag_embedding_model_unsupported` | The configured embedding model isn't supported by the pipeline                          | `error.message` names the model; pick a supported one                                                                                                                                                        |
| `rag_ingest_cancelled`            | An in-flight ingest job was cancelled                                                   | Expected when a newer ingest superseded it; re-run if unintended                                                                                                                                             |
| `ai_rate_limited`                 | OpenRouter throttling (HTTP 429)                                                        | `error.meta` carries the upstream headers — back off and retry                                                                                                                                               |
| `ai_credits_exhausted`            | The org's OpenRouter credit bundle is out of credits (HTTP 402)                         | Org credit bundle is spent — surface and stop, do not retry                                                                                                                                                  |
| `ai_moderation_blocked`           | OpenRouter blocked the request on moderation (HTTP 451)                                 | Inspect the prompt; this is a content decision, not retryable                                                                                                                                                |
| `ai_provider_error`               | Upstream model/provider failure (5xx from OpenRouter)                                   | `error.cause` has the raw provider error — transient, retry once                                                                                                                                             |
| `ai_no_image_generated`           | An image generation call returned no image                                              | Inspect the prompt/model; not retryable as-is                                                                                                                                                                |
| `openrouter_key_missing`          | `OPENROUTER_API_KEY` not injected into the runtime                                      | Setup bug — the per-install sub-key wasn't provisioned; `stackbone openrouter get --agent <id> --json` shows whether the install's key is `configured` and its `mode`/`status` (the value is never revealed) |
| `s3_invalid_key`                  | The object key is malformed or empty                                                    | Check the `key` you passed to `stackbone.storage.*`                                                                                                                                                          |
| `s3_error`                        | Generic R2/MinIO failure (most S3 errors collapse here)                                 | `error.meta` carries the AWS metadata; `error.cause` the raw SDK error                                                                                                                                       |
| `s3_credentials_missing`          | R2/MinIO credentials not injected                                                       | Setup bug — check the install's storage env                                                                                                                                                                  |
| `s3_bucket_missing`               | The bucket env var isn't set                                                            | Setup bug — check the install's storage env                                                                                                                                                                  |
| `secrets_not_found`               | `stackbone.secrets.get('FOO')` for a name that isn't set                                | Confirm with `stackbone secrets list --agent <id> --json` (names + masked previews) or Studio's Secrets tab                                                                                                  |
| `secrets_not_configured`          | `STACKBONE_SECRET_KEY` (the per-agent decrypt key) is missing                           | Setup bug — the install never received its secret key                                                                                                                                                        |
| `secrets_decrypt_failed`          | The stored envelope can't be decrypted with the agent's key                             | Key/envelope mismatch — `error.cause` has the crypto error                                                                                                                                                   |
| `database_not_configured`         | `DATABASE_URL` missing — the database pool can't be built                               | Setup bug — applies to `stackbone.database` and its consumers (RAG, secrets, config, prompts)                                                                                                                |
| `approval_persist_failed`         | The `stackbone_platform.approvals` row write failed (the run never showed in the inbox) | A missing/unmigrated `approvals` table or a DB error — `error.cause` has the Postgres error                                                                                                                  |
| `approval_cancel_failed`          | A cancel landed on an approval that is no longer `pending`                              | `stackbone hitl get <hitlId> --agent <id> --json` shows the current `status`                                                                                                                                 |
| `approval_not_found`              | A get/cancel for an approval id that doesn't exist                                      | The id never persisted — check the approval id from the run's inbox entry                                                                                                                                    |
| `approval_invalid_signature`      | An HMAC approval callback whose signature doesn't match                                 | The callback wasn't signed by the control plane (or the signing key drifted)                                                                                                                                 |
| `prompts_not_configured`          | The prompts schema isn't present on this install                                        | Run the migrations (`stackbone db migrate up --agent <id>`); `error.message` carries the hint                                                                                                                |
| `prompts_not_found`               | `stackbone.prompts.get(key)` for an absent / soft-deleted key                           | List what exists in Studio's Prompts tab                                                                                                                                                                     |
| `prompts_missing_var`             | A `{{var}}` in the template had no value at compile time                                | `error.message` names the variable; pass it in the compile call                                                                                                                                              |

> The full catalog of `<prefix>_<reason>` codes is the public error surface; pattern-match on `result.error.code` to branch. New codes arrive behind a minor — if you see a code not in this table, read `error.message` and treat it by its prefix family.

---

## HTTP errors from the control plane

When you call the platform API directly (the control plane at `STACKBONE_API_URL`), or when `stackbone <command>` reports a backend error:

| Status | Meaning                                                                                              | Diagnostic                                                                                                                                                                                                  |
| ------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | Workflow input failed its declared schema (`workflow_input_invalid`)                                 | A `POST /api/workflows/:name/start` (or `/chat`) body that violates the workflow's input schema is rejected with an `issues[]` array and **no run is started** — fix the input shape (see the runs section) |
| 401    | Not authenticated                                                                                    | `stackbone login` (interactive); in CI the session file `~/.stackbone/credentials.json` must be pre-seeded — there is no token env var                                                                      |
| 402    | Tier quota exceeded — org credit bundle spent                                                        | Read the 402 body's `reason` + message (not an `SdkError`); org owner must upgrade                                                                                                                          |
| 403    | RBAC capability mismatch (e.g. an `approver`-only role doing an `owner`-only action)                 | Body's `capability` field tells you which one is needed                                                                                                                                                     |
| 404    | Resource not found OR cross-org leak prevention (also `workflow_not_found` for an unknown name)      | If targeting `--agent <id>` from another org, that's expected — Studio uses the same 404 to avoid leaking existence                                                                                         |
| 409    | State conflict (publishing a version that already exists, linking a directory that's already linked) | Read the body's `conflict` field                                                                                                                                                                            |
| 422    | Validation failed                                                                                    | Body's `errors[]` array lists path + reason                                                                                                                                                                 |
| 5xx    | Backend issue                                                                                        | `stackbone logs tail --level error --agent <id> --json` (or Studio's Logs tab), then retry once with exponential backoff                                                                                    |

---

## Durable runs failing or timing out

Every invocation — an agent turn or a workflow run — produces a **durable run**. A run records a `status` (`running` / `done` / `failed` / `interrupted`), a `trigger`, timing, and a step log. Each `'use step'` inside a workflow is a persisted, replay-safe step: it runs once, is recorded, and is retried on failure — so a failed run can be inspected step-by-step and retried from its input.

Locate the failing run from the shell (the local-dev install by default, or a cloud install via `--agent <id>` — `stackbone agents list` gives the ids). See the **stackbone-cli** skill for full flags.

```sh
stackbone runs list --status failed --agent <id> --json   # find the run id
stackbone runs get <runId> --agent <id> --json            # header: status, trigger, timing
stackbone logs tail --run <runId> --agent <id> --json     # the run's log frames (the step waterfall lands here)
```

> There is **no** `stackbone runs steps` verb. Inspect a run's progression through its log frames: `stackbone logs tail --run <runId>` carries the per-step records (each `'use step'` boundary, its inputs, retries and the error that failed it). Without `--follow` the tail prints the buffered frames (up to `--limit`, default 100) and exits; add `--follow` to keep watching a still-running run.

Studio's Runs tab (production, or the dev Studio served alongside `stackbone dev`) shows the same timeline visually. Common causes:

| Symptom                                   | Likely cause                                                                                             | Diagnostic                                                                                                                  |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Workflow start rejected, no run created   | The `start`/`chat` body didn't match the workflow's `inputSchema` → HTTP 400 `workflow_input_invalid`    | The 400 body's `issues[]` lists each offending `{ path, message }`; cross-check against `stackbone workflows schema <name>` |
| A step retries forever then fails the run | A `'use step'` that isn't idempotent or keeps hitting a transient error                                  | `stackbone logs tail --run <runId>` shows the retry attempts and the recurring `error.cause`; make the step idempotent      |
| Run stuck `running` with no progress      | The workflow is parked on a durable gate (a `requestApproval()` hook) waiting for a human or its timeout | See the HITL section — the run resumes when the hook is resumed or the `timeout` fallback fires                             |
| Run fails immediately on input validation | Schema mismatch between the request body and the workflow/agent's declared input schema                  | The run's first frames carry the Zod-style validation errors with the offending path                                        |
| Run succeeds but no output                | A step or the workflow body returned `undefined` instead of an object matching `outputSchema`            | Confirm the body ends with `return { ... }`; add a log line before the return to dump the keys                              |

---

## HITL runs stuck

HITL pauses exist at **two levels**, resolved through the same approvals inbox.

### Tool-level — an agent turn `interrupted` on a gated tool

A deep agent with `interruptOn: { <tool>: true }` pauses **before** the gated tool runs: the chat turn ends as a well-formed standard response (Anthropic `stop_reason: 'tool_use'` / OpenAI `finish_reason: 'tool_calls'`), the run flips to `interrupted`, and an approvals row appears (topic `tool-approval for <tool> on <agent>`). Deciding it (`stackbone hitl approve|reject <id> --yes`) resumes the turn **server-side** on the same session — the client never re-POSTs.

| Symptom                                              | Diagnostic                                                                                                                                                                 |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A stateless chat errors when the gated tool fires    | Pauses need a durable session — the error hints at it: the client must send the `x-stackbone-session` header (only the new message per turn).                              |
| New messages into the paused session are rejected    | Expected (`approval_pending`) — decide the pending approval first; `stackbone hitl list --status pending --json` shows it.                                                 |
| Durable sessions silently off / memory not surviving | The workspace lacks `@langchain/langgraph-checkpoint-postgres` (the boot log warns once with the `pnpm add` hint), or the client never sent `x-stackbone-session`.         |
| Run stuck `interrupted` after deciding               | The resume happens server-side on the same run row (`interrupted → running → done`) — check `stackbone runs get <runId> --json`; the resumed reply lands on that same run. |

### Workflow-level — `requestApproval()`

Human-in-the-loop in a workflow is the `requestApproval()` gate from `@stackbone/sdk/workflow`. It writes an `approvals` row (so the run shows in the inbox), then PAUSES the run durably on a Workflow SDK hook, racing the human decision against the `timeout` (applying the `fallback` — `'approve'` / `'reject'` — if nobody decides). The caller gates the side-effect on `decision.status === 'approved'`. The raw `defineHook` + `sleep` (also re-exported from `@stackbone/sdk/workflow`) are the escape hatch for custom gates.

```ts
import { requestApproval } from '@stackbone/sdk/workflow';

const decision = await requestApproval({
  token: `refund-${orderId}`, // the resume key
  topic: 'refund',
  payload: { orderId, amount },
  timeout: '24h',
  fallback: 'reject',
});
if (decision.status !== 'approved') return { refunded: false };
```

When the org member says "the run is paused but nothing is in the inbox":

1. The approvals row likely **failed to write** and the run never registered. Look for `approval_persist_failed` in the run's frames (`stackbone logs tail --run <runId> --agent <id> --json`) — usually a missing/unmigrated `approvals` table or a DB error (`error.cause` has the Postgres error). `requestApproval()` writes the row in its own `'use step'`, so a failed write surfaces as a failed step, not a silent swallow.
2. Or the row was created but the run **was never resumed**. The pause is a hook keyed by the `token`; the human decides in Studio (or via the CLI), and the host resumes the parked run by that token through `POST /api/workflows/hooks/:token/resume`. List the inbox from the shell with `stackbone hitl list --agent <id> --json` and inspect one with `stackbone hitl get <hitlId> --agent <id> --json` to see its current `status` and audit trail of decisions. Decide it from the shell with `stackbone hitl approve <hitlId> --agent <id> --yes` / `stackbone hitl reject <hitlId> --agent <id> --yes` (both `⚠️ destructive`, require `--yes`, accept an optional `--reason`). Studio's HITL tab shows the same.
3. Or the **approver role isn't assigned** to any org member, so no one can decide. `stackbone metadata --json` shows the org's roles.
4. Or the pause already **timed out**: when the `timeout` elapses before a human decides, the `fallback` is applied and the run continues with `decision.timedOut === true`. A run that "resumed on its own and rejected" is the fallback firing — check the `timeout`/`fallback` on the `requestApproval()` call.

> The CLI verb group is `hitl`; the SDK surface that writes the row is `stackbone.approval` (driven for you by `requestApproval()`). You rarely call `stackbone.approval` directly — author the gate with `requestApproval()` and let it manage the row + hook.

---

## Workflows — input schema, triggering, discovery

A workflow declares optional sibling `inputSchema` / `outputSchema` Zod exports. The runtime validates the start/chat body against `inputSchema` at the frontier, **before** the run starts — a mismatch is the 400 `workflow_input_invalid` above (with `issues[]`), and no run is created.

| Symptom                                          | Diagnostic                                                                                                                                                                                                                           |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `stackbone workflows list` shows nothing         | The workspace exposes no workflows, or `stackbone dev` isn't serving them — confirm there are `workflows/<name>.workflow.ts` files (discovered by convention; a `stackbone.config.ts` override, if present, wins) and that dev is up |
| Start/chat returns 400 `workflow_input_invalid`  | The body violated the declared schema — `stackbone workflows schema <name> --agent <id> --json` prints the input JSON Schema to fix the body against                                                                                 |
| Start/chat returns 404 `workflow_not_found`      | The `:name` in the path isn't a known workflow — `stackbone workflows list --agent <id> --json` shows the exposed names                                                                                                              |
| A workflow `◇` (no schema marker) takes raw JSON | It declares no `inputSchema`, so input passes through unvalidated and a bad shape fails later inside the run, not at the frontier                                                                                                    |

---

## Database — slow queries, missing indexes, pgvector

The CLI has a read-only SQL explorer against the targeted install: `stackbone db query "<single SELECT>" --agent <id> --json`, `stackbone db schemas` and `stackbone db table <schema> <table>` (see the **stackbone-cli** skill). It is **read-only** — `EXPLAIN ANALYZE` and any write still need standard Postgres tooling (`psql` or any client) pointed at `DATABASE_URL`:

- **Slow `SELECT`** — `EXPLAIN (ANALYZE, BUFFERS) <query>` via `psql` (the CLI `db query` only runs plain reads); look for sequential scans on large tables.
- **`pgvector` distance returns wrong order** — confirm the index uses the **same distance operator** as your query (`<->` cosine, `<#>` inner product, `<=>` L2). A query with `<->` against an index built for `<#>` does a sequential scan and returns wrong results.
- **`tsvector` queries return nothing** — confirm the column was populated (`UPDATE … SET search_tsv = to_tsvector(…)` on existing rows; the trigger only fires on writes after creation).
- **Migration applied but the table isn't there** — `stackbone db migrate status` shows the journal. Inspect with `stackbone db schemas --agent <id> --json` (does the table exist?) or read the journal directly via `psql`.

> `stackbone.database` is native Drizzle — it **throws** on a query error (no `{ data, error }` envelope), so wrap DB code in `try/catch` and inspect the thrown Postgres error.

---

## Storage — missing files, signed URLs failing

| Symptom                                                  | Diagnostic                                                                                                                                                           |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 404 on a key you just uploaded                           | The upload returned `error` and you didn't check; or you saved `key` before the `await` resolved                                                                     |
| Signed URL returns 403 after 5 min                       | The URL TTL elapsed — `signedUrl(key, { expiresIn: 3600 })`                                                                                                          |
| Object exists in storage console but not in the SDK list | Someone uploaded directly to the bucket, bypassing the SDK — `stackbone.storage.list()` (or `stackbone storage list --bucket <b> --agent <id> --json`) won't show it |
| Local dev: uploads silently disappear                    | The local MinIO container isn't running — bring the local dev stack (Postgres + Redis + MinIO) back up                                                               |

---

## Scheduled workflows not firing

A recurring trigger is a **dynamic schedule** registered with `stackbone.workflows.schedule(name, input, cron)` on the ambient client (or a declarative `export const schedules` next to the workflow). Each tick starts the named workflow as its **own run**, so you diagnose a missing tick like any run.

| Symptom                     | Diagnostic                                                                                                                                                                                                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A schedule never fires      | `stackbone workflows list --agent <id> --json` confirms the workflow exists; check the cron cadence and that `stackbone dev` / the install is up. Re-call `stackbone.workflows.schedule` with the same `name` to replace a bad cadence (it's idempotent by `name`). |
| It fired but the run failed | Find it with `stackbone runs list --status failed --agent <id> --json`, then `stackbone logs tail --run <runId> --agent <id> --json` (see the durable-runs section).                                                                                                |
| It fires twice              | Two schedules target the same workflow — `stackbone.workflows.listSchedules()` shows what's registered; `stackbone.workflows.unschedule(name)` the duplicate.                                                                                                       |

---

## Publish / build — `stackbone publish` failed

`stackbone publish` packages the whole workspace (every agent's compiled output + the workflows) into a verifiable bundle. The build runs on your host; the most common failures are build-time guardrails that abort BEFORE producing a bundle, so a broken agent never ships and crash-loops in production.

| Stage        | Failure                                      | Diagnostic                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Native deps  | A native (non-portable) dependency           | The scan names the offending package; remove it or replace it with a portable one                                                                                                                                                                                                                                                                                                                                                               |
| Bundle (SDK) | `@stackbone/sdk` was inlined, not external   | The build aborts: an inlined SDK creates a second invocation context, so per-run logs arrive with no run id. The esbuild step keeps `@stackbone/sdk` + `deepagents` + `@langchain/*` external and verifies the SDK stayed external per agent — an abort here usually means a stray per-agent `node_modules` or a dep pinned somewhere other than the workspace root `package.json`. Delete the nested `node_modules` / move the pin to the root |
| Manifest     | `stackbone.config.ts` / `agent.yaml` invalid | The error carries the field path; fix the offending field                                                                                                                                                                                                                                                                                                                                                                                       |

The upload to the registry + build-pointer registration is the provisioning step's job under BYOC (the CLI has no registry credentials), so `publish` writes the verifiable artifact + its digest locally and prints them. A failure there is a control-plane/provisioning concern, not a CLI one.

---

## Secrets / config

| Symptom                                                                       | Diagnostic                                                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stackbone.secrets.get('FOO')` returns `error.code: 'secrets_not_found'`      | The secret isn't set — confirm with `stackbone secrets list --agent <id> --json` (names + masked previews; the value is never revealed by the CLI), or Studio's Secrets tab                                                                                                         |
| `stackbone.secrets.get('FOO')` returns `error.code: 'secrets_decrypt_failed'` | The per-agent decrypt key (`STACKBONE_SECRET_KEY`) doesn't match the stored envelope — `error.cause` has the crypto error                                                                                                                                                           |
| `stackbone.config.get<T>(key)` returns the wrong shape                        | The org member edited the config to something that doesn't match the schema you validate it against — inspect the active document with `stackbone config get --agent <id> --json` (and its history with `stackbone config versions`), then surface the error so they can correct it |

> Connectors are a live surface, but `stackbone.connection(id)` (the Stackbone Connect broker) **throws** a `ConnectorCallError` on failure — it does **not** return a `{ data, error }` envelope. Match `err.code` (never `instanceof`) against the broker taxonomy: `invalid_args` (args failed the operation schema, or a bad operation id), `credential_error` (token revoked/expired, or a non-2xx from the broker), `timeout`, `ambiguous` (several connections of that connector matched and none was selected), `unauthorized` (caller identity rejected), and `unavailable` / `execute_failed` (broker or provider unreachable). For `ambiguous`, resolve the id or unique name with `stackbone connectors --json` (see the **stackbone-cli** skill) and pass it: `stackbone.connection('<id or unique name>')`. The legacy `connections_*` envelope codes belong to the deprecated `client.legacyConnections` proxy (not shipped as a live surface), **not** to `stackbone.connection(id)`. See the **stackbone** skill's connections doc for the full table.

---

## Tier / billing — 402 responses

These are **control-plane HTTP 402 bodies**, not `SdkError`s. They surface when you call the platform API directly (or when a `stackbone <command>` hits a tier cap) — they are **not** in the `SdkErrorCode` catalog and you **cannot** pattern-match them with `result.error.code` from a `stackbone.*` call. The strings below are fields on the API's HTTP response body, not SDK error codes.

| HTTP 402 body reason              | Meaning                                    | Action                                                            |
| --------------------------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| `tier_quota_exceeded`             | Period credit bundle spent                 | Owner upgrades the org's tier (`stackbone docs tiers` for limits) |
| `installed_agents_cap_reached`    | Org at `installed agents` cap for its tier | Owner uninstalls an agent or upgrades                             |
| `members_cap_reached`             | Org at members cap (`free` = 1)            | Owner upgrades to `starter` or higher                             |
| `published_templates_cap_reached` | Creator at `published` cap                 | Owner upgrades                                                    |

These are **not retryable** — surface the body's message (and any hints it carries) to the user verbatim. The closest SDK-side signal is `ai_credits_exhausted` (an actual catalog code) when a model call hits a spent credit bundle.

---

## What this skill does NOT cover

- **Performance tuning** of the runtime (cold start, machine sizing, scale-to-zero pauses). That's a feature with its own metrics surface.
- **Cost analysis** beyond the 402 codes above. The Studio Costs panel covers per-agent breakdown.
- **Custom OTel queries** against external tracing backends. For now Studio's Logs tab is the supported path.
