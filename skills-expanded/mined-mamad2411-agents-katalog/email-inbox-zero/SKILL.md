---
name: email-inbox-zero
description: >
  Use when Cooper wants inbox zero across email accounts.
version: 1.0.0
metadata:
  hermes:
    tags: [email, inbox-zero, gmail, gog, feed, triage, pay-decision]
    category: ops
    related_skills: [gog, financial-operations, operator-status, communications]
---

# Email Inbox Zero (Cooper)

Class skill for multi-account inbox cleanup. Deep Gmail CLI details live in **`gog`**; money secrets in **`financial-operations`**; dashboard plumbing in **`operator-status`** (user-owned — adopt if you need to edit it).

## Accounts & order

1. `cooper@darkmatter.io` (work) and `me@cm.xyz` (personal) via `gog`
2. **Outlook last** — Kernel browser + profile `cooper-outlook-email`; do not triage until both Gmails are done unless Cooper says otherwise

## Auth every shell

```bash
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD=<REDACTED>
gog -a <email> --gmail-no-send …
# If Gmail fails with oauth2 unauthorized_client: re-store OAuth client JSON
# (gog skill → Auth & keyring) then auth doctor --check per account
```

## Multi-pass bulk (no-input)

EXECUTE-SAFE only: label + archive + mark-read. Never send/delete/click links/pay/security.

1. List pages (`--max 10–25`), classify, batch-label, re-list (archived bulk advances older mail)
2. **Mute+archive:** marketing, USPS/CT tracking, promos, obvious pitches
3. **Done+archive:** expected receipts/statements/cancel confirms
4. **Needs-Action:** money failures, KYC, domains, human threads, security
5. Gmail `rateLimitExceeded` → sleep ~60–90s, smaller pages, serial calls
6. Subagents OK for per-account bulk; **600s timeouts are normal** — parent continues paced drain

Heuristics: `gog` → `references/interactive-triage-pass.md`

## User-confirmed buckets

When Cooper says a class is **legit / no issue** (e.g. Mercury transfers intentional, Cloudflare NS moves OK, security reviewed):

- Batch `Triage/Done` + remove `INBOX,UNREAD,Triage/Needs-Action` (+ personal `Action Required`/`Security Alert` only if that account has them)
- Verify with thread-level label read-back, not only sender search
- Do not re-surface

## Presentation

- ≤**5** action items per chat update
- Dated “need response by” table for deadlines
- **Pure pay / approve decisions → feed HITL**, not chat walls
- Agent-first: investigate before asking Cooper; never “what did the console show?”

## Pay / Don't-pay → feed HITL

Do **not** rebuild kanban for the UI. Prefer:

```bash
cd ~/git/darkmatter/feed
bun scripts/hitl.ts ask \
  --title "Pay <vendor> \$N?" \
  --body "Investigated: … official portal status …" \
  --option "*pay:✅ Pay" --option "skip:❌ Don't pay" \
  --category pay --priority 80
```

Cooper answers on https://feed.cm.xyz → **Needs your decision**.
Execute Pay under `financial-operations` (Studio CUA, charge gate, SA op).
Progress: `feed-decisions` / `poll-responses.ts`.

Optional long-running kanban card is fine for ops tracking — not required for HITL.

UI contracts: skill **`feed-decisions`** (Tabs single-select; no clipboard; no container `preventDefault`).

## Secrets during payment repair

- Only `~/.local/bin/op` + SA + `--vault cm|cooper|dev`
- Catalog: `~/.hermes/op-sa-catalog.json`
- Missing item: ask Cooper **as-needed** to move that title into vault **`cm`**
- Never biometric / personal agenix token

## Definition of Done (inbox pass)

```gherkin
Scenario: Safe Gmail pass complete
  Given both Gmail accounts authenticate
  When bulk mute/Done is exhausted for no-input mail
  Then remaining inbox is mostly Needs-Action / human / money / security
  And pay/approve gates are staged as feed HITL (hitl.ts ask), not chat walls
  And chat shows ≤5 critical non-checkbox items plus any dated deadline table
  And no send/delete/link-click/security change occurred without a gate
```
