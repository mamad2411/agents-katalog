---
name: bot-scaffold
description: MUST USE when building Telegram/Discord bots — handlers, FSM, rate limits, idempotency, deploy. Triggers on new bot, webhook vs polling, spam/abuse, or state machine bugs.
---

# Bot Scaffold

Chat bots are **long-running event systems**. Scaffold with explicit handler map, FSM storage, rate limits, and structured logging — same reliability skeleton as `workflow-design`.

## When This Skill Applies

- New Telegram/Discord/Slack bot
- Adding commands to existing bot
- Webhook production setup
- Abuse: spam commands, wallet drain via API calls
- Multi-step flows (onboarding, checkout in chat)

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **B0** | Bot token in client; no auth on webhook; arbitrary shell from command | Block deploy |
| **B1** | No rate limit; FSM in memory only on multi-instance | Fix pre-scale |
| **B2** | Missing error UX; no idempotency on payments | Sprint |
| **B3** | Help text | Optional |

Cross-ref: `api-integration` for external APIs; `secrets-audit` for tokens; `waf-review` not applicable but rate limit at bot framework.

## Phase 0 — Platform Choice

| Mode | When |
|------|------|
| Webhook | Prod, HTTPS, low latency |
| Long polling | Dev, behind NAT |

Telegram: setWebhook with secret token header. Discord: interactions + verify signature.

## Phase 1 — Project Structure

```text
bot/
  main.py              # bootstrap
  config.py            # env validation
  handlers/
    start.py
    orders.py
  middlewares/
    rate_limit.py
    logging.py
  fsm/                 # states
  services/            # business logic — not in handlers
  tests/
```

Handlers thin — call services; services testable without Telegram mock hell.

## Phase 2 — Handler Map

Document every update type:

| Command/Callback | Auth | Rate | FSM | Side effects |
|------------------|------|------|-----|--------------|

Deny unknown callbacks — don't no-op silently.

## Phase 3 — FSM & Storage (2025–2026)

- Redis or DB for FSM — not process memory if >1 replica
- TTL on stale states
- Clear state on `/cancel`
- Version FSM schema — migrate old users

```python
# Idempotent callback handling pattern
if await processed.update_id_seen(callback.id):
    return
```

## Phase 4 — Rate Limits & Abuse

- Per-user command bucket (e.g. 30/min)
- Global flood control on expensive API calls
- Admin commands behind allowlist user IDs
- Log suspicious patterns

Cross-ref: `auth-review` if bot gates access to user data.

## Phase 5 — Deploy & Ops

```bash
# Telegram webhook check
curl "https://api.telegram.org/bot$TOKEN/getWebhookInfo"

# Health endpoint for load balancer
curl -s localhost:8080/health
```

- Graceful shutdown: stop polling, drain updates
- Structured logs with `update_id`, `user_id` (hash if GDPR)
- Metrics: commands/min, errors, latency

## Output Template

```markdown
## Bot Scaffold: [platform/name]

**Verdict:** ✅ / 🔶 / ❌

### Architecture
- Mode: webhook/polling
- FSM store:

### Handler map
| ... |

### Security
- Token storage:
- Admin allowlist:

### Gaps
| ID | Sev | Fix |

### Deploy checklist
- [ ] webhook secret
- [ ] Redis FSM
- [ ] rate limits
```

## Anti-Patterns

- **All logic in one handler file**
- **Sync blocking HTTP** in async bot — stalls event loop
- **Edit message on every keystroke** — API limit ban
- **No webhook secret** — forged updates
- **Global mutable dict** for state

## Cross-References

| Skill | Use when |
|-------|----------|
| `workflow-design` | Complex multi-system flows |
| `agent-design` | LLM in bot loop |
| `redis` template | FSM storage |

## Cursor Kit Templates

- `telegram-bot`, `discord-bot`

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

