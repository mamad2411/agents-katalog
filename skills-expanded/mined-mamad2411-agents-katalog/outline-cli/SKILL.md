---
name: outline-cli
description: Search, read, and update company documentation in Outline wiki. Use this skill whenever the user asks to search docs, find documentation, look up a handbook, check the wiki, ask "what do our docs say about X", read a doc page, update/edit a document, find information in Outline, browse collections, or reference any company knowledge base content. Also triggers on mentions of specific doc names (e.g. "Navigos handbook", "onboarding guide", "runbook"), requests to create/delete/template docs, review comments, trace issue links, audit permissions, or sync content. Powered by the local `outline-cli` binary (legacy alias `outline-agent`) with revision-safe mutations, batch operations, and federated sync.
---

# Goal
Execute Outline operations with low-token calls, explicit safety gates, and reproducible machine-readable output.

# Instructions

## Command Surface
- Use `outline-cli` by default.
- Accept `outline-agent` only when the user explicitly asks for that alias.
- Prefer `invoke` + structured JSON args, then `batch` for multi-step operations.

## Session Bootstrap (Always)
1. Verify binary and help surfaces:
   ```bash
   outline-cli --version
   outline-cli tools help --view summary
   ```
2. Refresh source-of-truth contracts:
   ```bash
   outline-cli tools contract all --result-mode inline
   ```
3. Verify profile/auth before any mutation:
   ```bash
   outline-cli profile list --pretty
   outline-cli profile test
   outline-cli invoke auth.info --args '{"view":"summary"}'
   ```

## Capability Map (Use Minimal Tooling)
- Retrieval and navigation:
  - `documents.search`, `documents.list`, `documents.info`, `documents.resolve`, `documents.resolve_urls`, `documents.canonicalize_candidates`
  - `collections.list`, `collections.info`, `collections.tree`
  - `search.expand`, `search.research`
- Safe document mutation:
  - `documents.update`, `documents.safe_update`, `documents.diff`, `documents.apply_patch`, `documents.apply_patch_safe`, `documents.batch_update`
  - `documents.plan_batch_update`, `documents.plan_terminology_refactor`, `documents.apply_batch_plan`
- Lifecycle and collaboration:
  - `revisions.*`, `shares.*`, `templates.*`, `documents.templatize`, `comments.*`, `events.list`
- Knowledge and linkage workflows:
  - `documents.answer`, `documents.answer_batch`
  - `documents.backlinks`, `documents.graph_neighbors`, `documents.graph_report`
  - `documents.issue_refs`, `documents.issue_ref_report`
- Integration/admin wrappers:
  - `federated.sync_manifest`, `federated.sync_probe`, `federated.permission_snapshot`, `capabilities.map`
  - `users.*`, `groups.*`, `collections.*_memberships`, `documents.*_memberships`, `documents.users`
  - `oauth_clients.*`, `oauth_authentications.*`, `oauthClients.delete`, `oauthAuthentications.delete`
  - `webhooks.*`, `file_operations.*`, `documents.import_file`, `documents.create_from_template`, `documents.cleanup_test`
- Escape hatch:
  - `api.call` for endpoints not yet wrapped as dedicated tools.

## Retrieval-First Pattern (Default)
1. Discover candidates with `view:"ids"` or `view:"summary"`.
2. Hydrate only selected IDs (`documents.info` / `collections.info`).
3. Escalate to `view:"full"` only for final documents that require full text.
4. Prefer multi-query/multi-id args (`queries[]`, `ids[]`) over repetitive single calls.

## Mutation Pattern (Safe + Explicit)
1. Read current state first.
2. Use minimal edits (`append`/`prepend`, patch, or targeted update).
3. Use revision guards (`expectedRevision`) for concurrent environments.
4. Set `performAction:true` only on the final confirmed mutation call.
5. Verify via read-back and, for high-impact flows, `events.list`/`revisions.list`.

## Delete Pattern (Mandatory)
1. Arm delete read:
   ```bash
   outline-cli invoke documents.info --args '{"id":"<doc-id>","armDelete":true,"view":"summary"}'
   ```
2. Extract `deleteReadReceipt.token`.
3. Execute delete:
   ```bash
   outline-cli invoke documents.delete --args '{"id":"<doc-id>","readToken":"<token>","performAction":true}'
   ```
4. If token is stale/mismatched/expired, re-run step 1 immediately and retry once.

## Output and Token Controls
- Formats:
  - `--output json` (default)
  - `--output ndjson` for stream-friendly automation
- Result modes:
  - `--result-mode auto` (default offload when payload is large)
  - `--result-mode inline`
  - `--result-mode file`
- Use `--args-file` / `--ops-file` for large payloads.
- If output is offloaded, inspect only required fields:
  ```bash
  outline-cli tmp cat /absolute/path/from/result.json
  ```
- Periodic cleanup:
  ```bash
  outline-cli tmp gc --older-than-hours 24
  ```

## Built-in Agent Guidance
- Beginner onboarding playbook:
  ```bash
  outline-cli tools help quick-start-agent --view full
  ```
- Scenario playbooks (14 workflows):
  ```bash
  outline-cli tools help ai-skills --view full
  ```

# Source References (MANDATORY)

Every response that presents information retrieved from Outline **MUST** include source references linking back to the original documents.

## How to Build Source Links
- The base URL comes from `team.url` in the `profile test` or `auth.info` response (e.g. `https://handbook.navigosgroup.site`).
- `view:"full"` returns a `url` field (e.g. `/doc/some-title-s51py6qL8O`) — construct: `{baseUrl}{url}`.
- `view:"summary"` returns only `urlId` (e.g. `s51py6qL8O`) — construct: `{baseUrl}/doc/{urlId}`.
- When using `search.research` or `documents.search`, extract `urlId` from each result in the merged/expanded arrays.

## How to Present Source Links
Append a **Sources** section at the end of the response:

```
**Sources:**
- [Document Title](https://handbook.navigosgroup.site/doc/urlId)
- [Another Document](https://handbook.navigosgroup.site/doc/urlId2)
```

Rules:
- Include ALL documents that contributed information to the response.
- Use the document `title` as link text, not raw IDs.
- When multiple sections from the same document are cited, list it once.
- When answering from a single document, still include the source link.
- Extract `title` + `urlId` during retrieval — do not make extra API calls just for references.

# Constraints
- Never run mutating operations without explicit `performAction:true`.
- Never delete without a fresh read token from `documents.info armDelete:true`.
- Never default to `view:"full"` for discovery.
- Never assume profile context; verify `profile list/test` + `auth.info`.
- Never hardcode old contracts; refresh with `tools contract all` before long automation runs.
- Never present Outline data to the user without source reference links.

# Examples

## Example 1: Research retrieval in one call
```bash
outline-cli invoke search.research --args '{
  "question": "How do we run incident communication and escalation?",
  "queries": ["incident comms", "escalation matrix"],
  "precisionMode": "precision",
  "limitPerQuery": 8,
  "perQueryView": "ids",
  "perQueryHitLimit": 4,
  "expandLimit": 4,
  "view": "summary"
}'
```

## Example 2: Template placeholder extraction + strict instantiation
```bash
outline-cli invoke templates.extract_placeholders --args '{"id":"template-id"}'

outline-cli invoke documents.create_from_template --args '{
  "templateId": "template-id",
  "title": "Service A - Incident Postmortem",
  "placeholderValues": {"service_name":"Service A","owner":"SRE Team"},
  "strictPlaceholders": true,
  "publish": true,
  "performAction": true,
  "view": "summary"
}'
```

## Example 3: Safe patch update with revision guard
```bash
outline-cli invoke documents.info --args '{"id":"doc-a","view":"summary"}'

outline-cli invoke documents.apply_patch_safe --args '{
  "id": "doc-a",
  "expectedRevision": 12,
  "mode": "unified",
  "patch": "@@ -1,1 +1,1 @@\n-Old\n+New",
  "performAction": true,
  "view": "summary"
}'
```

## Example 4: Federated sync + ACL snapshot
```bash
outline-cli invoke federated.sync_manifest --args '{
  "collectionId": "collection-id",
  "since": "2026-03-01T00:00:00.000Z",
  "limit": 100,
  "offset": 0
}'

outline-cli invoke federated.permission_snapshot --args '{
  "ids": ["doc-1", "doc-2"],
  "includeDocumentMemberships": true,
  "includeCollectionMemberships": true
}'
```

# Read Next
Load command recipes only when needed:
- `references/tool-playbook.md`
