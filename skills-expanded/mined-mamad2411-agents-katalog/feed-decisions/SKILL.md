---
name: feed-decisions
description: >-
  Use when staging or polling feed.cm.xyz HITL decisions (any agent→Cooper
  request) or agent work progress after Cooper answers. Prefer over chat walls
  and clipboard paste.
version: 2.0.0
metadata:
  hermes:
    tags: [feed, d1, hitl, pay-decision, dashboard, hermes-queue]
    category: ops
    related_skills: [email-inbox-zero, financial-operations, operator-status, decision-queues]
---

# Feed HITL (agent ↔ Cooper)

Cooper’s preference: **decisions live on https://feed.cm.xyz**, not chat walls,
and **never via clipboard “Copy for Hermes.”** This is a **HITL interface**, not
a kanban rebuild UI.

## Two D1 queues

| Direction | Table / API | When |
|---|---|---|
| **Agent → Cooper** | `hitl_requests` · `/api/hitl` | Any ask: pay, approve, pick, confirm, freeform |
| **Work progress** | `feed_responses` · `/api/responses` | After Cooper answers (or agent work with progress bar) |

Repo: `~/git/darkmatter/feed` · Worker `cooper-feed` · Access team `drkmttr.cloudflareaccess.com`.

## Agent → Cooper (primary)

```bash
cd ~/git/darkmatter/feed
# himitsu: feed/ingest-token, cf-access-client-id, cf-access-client-secret

bun scripts/hitl.ts ask \
  --title "Pay Kernel \$30?" \
  --body "Investigated (readonly): card declined; repair ready at billing portal." \
  --option "*pay:✅ Pay" \
  --option "skip:❌ Don't pay" \
  --category pay --priority 80 --source hermes

bun scripts/hitl.ts list --status open
bun scripts/hitl.ts wait 12          # poll until answered
bun scripts/hitl.ts get 12
```

Cooper: hard-refresh feed → **Needs your decision** → pick tab → **Submit answer**.

### Agent-first body rules

- Investigate **before** opening HITL (gog, official URLs, SA op, Studio CUA).
- Never ask Cooper “what did the console show?” — you log in and look.
- HITL body = findings + proposed options only.
- True gates only: charge click, external send, security/MFA, missing SA vault item (ask move **that title** into vault `cm` as-needed).

## Work progress (after answer / execution)

```bash
bun scripts/poll-responses.ts --status open --claim
bun scripts/poll-responses.ts --progress 12 --message "Opened billing portal" --pct 40
bun scripts/poll-responses.ts --done 12 --summary "Receipt …"
# or --fail 12 --error "…"
```

UI: **Agent activity** auto-polls Queued → Claimed → Running → Done/Failed.

## UI contracts (do not regress)

- Choices = **Tabs** single-select (one panel: label + optional note + submit). Not stacked radio+input rows.
- Container handlers: **`stopPropagation` only** — never `preventDefault` (kills clicks).
- **Send to Hermes** / **Submit answer** write D1. Clipboard paths retired.
- Prod components: `src/components/hitl-panel.tsx`, `agent-activity.tsx`, `dashboard.tsx`, `worker.ts`.
- Migrations: `0002_feed_responses`, `0003_response_progress`, `0004_hitl_requests`.

## Deploy

```bash
cd ~/git/darkmatter/feed && bun run build
# CLOUDFLARE_ACCOUNT_ID + API token + FEED_INGEST_TOKEN via himitsu
STAGE=prod bun alchemy deploy ./alchemy.run.ts --stage prod --profile default --yes
```

## Pay decisions during email triage

Stage HITL with `hitl.ts ask` (category `pay`). Optional blocked kanban for long-running repair tracking — **not required for the feed UI**. Execute Pay under `financial-operations` (Studio CUA, charge gate, SA op).

## Related

- `email-inbox-zero` — when triage surfaces pay/approve needs
- `financial-operations` — execute Pay (SA 1P, charge gate)
- `operator-status` — feed deploy/Access/weekly review
- `decision-queues` — generic form-queue pattern; **prefer feed HITL for Cooper**

## References

- `references/hitl-api.md` — endpoints + CLI
- `references/agent-progress.md` — progress lifecycle
- `references/ui-contracts.md` — tabs / no-clipboard / click pitfalls
- `references/agent-first.md` — investigate before HITL
