---
name: supabase-postgres
description: MUST USE for Supabase Postgres — RLS policies, auth.uid() patterns, indexes, edge functions, realtime, storage rules. Triggers on Supabase project, client bypassing RLS, or migration to hosted Postgres+Auth.
---

# Supabase Postgres

Supabase is **Postgres + Auth + RLS as the security boundary**. Treat the anon/service keys correctly: browser uses anon + RLS; server uses service role only behind your API — never expose service key to clients.

## When This Skill Applies

- New Supabase project or table exposed via PostgREST
- Policies missing or `USING (true)` on sensitive tables
- Edge Function calling DB or third parties
- Realtime channel authorization
- Performance on RLS-heavy queries

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **SB0** | Service role in frontend; RLS disabled on PII; storage bucket public read private write confusion | Block ship |
| **SB1** | Missing indexes on RLS columns; policy per row subquery scan | Fix pre-scale |
| **SB2** | Edge function no JWT verify | Sprint |
| **SB3** | Naming | Optional |

Cross-ref: `auth-review` for app JWT; `schema-design` for tenant keys; `sql-write` for plan tuning.

## Phase 0 — Key & Role Map

| Key | Where | Powers |
|-----|-------|--------|
| anon | Browser/mobile | RLS-enforced |
| service_role | Server only | Bypass RLS |

```bash
# Local dev
supabase status
supabase db diff --linked 2>/dev/null | head
```

## Phase 1 — RLS Design

Enable RLS on every public schema table with user data:

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY orders_select_own ON orders
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY orders_insert_own ON orders
  FOR INSERT TO authenticated
  WITH CHECK (user_id = auth.uid());
```

Checklist:

- [ ] Separate policies per command (SELECT/INSERT/UPDATE/DELETE)
- [ ] `authenticated` vs `anon` explicit
- [ ] Multi-tenant: `tenant_id` from JWT claim `auth.jwt() ->> 'tenant_id'`
- [ ] No policy recursion traps — use security definer functions sparingly, document

Test as user A cannot read B:

```sql
SET request.jwt.claim.sub = 'user-a-uuid';
SELECT * FROM orders; -- expect only A rows
```

## Phase 2 — Indexes for RLS

Index columns in `USING` / `WITH CHECK`:

```sql
CREATE INDEX orders_user_id_idx ON orders (user_id);
```

Run EXPLAIN with RLS on (`sql-write`).

## Phase 3 — Edge Functions (2025–2026)

- [ ] Verify JWT unless public webhook with separate HMAC
- [ ] Use `Deno.env` secrets — not committed
- [ ] Prefer database functions for simple logic — edge for external IO
- [ ] Idempotency keys for payment webhooks
- [ ] OTel or structured logs — no service key in log

```typescript
// Pattern: createClient with user JWT from Authorization header
import { createClient } from "@supabase/supabase-js";
```

Cross-ref: `llm-integration` if edge calls LLM.

## Phase 4 — Realtime & Storage

- Realtime: channel auth matches RLS — private channels per user/tenant
- Storage: bucket policies mirror table RLS; no public bucket for user uploads with predictable paths

## Phase 5 — Migrations & Branching

- SQL migrations in repo; review like prod DDL (`schema-design`)
- Preview branches for PR environments
- Seed data without prod PII

## Output Template

```markdown
## Supabase Review: [project]

**Verdict:** ✅ / 🔶 / ❌

### RLS coverage
| Table | RLS on | Policies | Tested |

### Key exposure
- Frontend keys:
- Service role location:

### Findings
| ID | Sev | Issue | Fix SQL/policy |

### Performance
- Plans reviewed:

### Follow-ups
- [ ] `auth-review` custom JWT claims
```

## Anti-Patterns

- **RLS on but service role everywhere** — RLS theater
- **`USING (true)`** for "quick demo"
- **Client-side only filters**
- **auth.uid() in public insert** without WITH CHECK
- **Edge function as monolith** — cold start + secret sprawl

## Cross-References

| Skill | Use when |
|-------|----------|
| `neon-postgres` | comparing serverless Postgres |
| `secure-coding` | SSRF from edge |
| `secrets-audit` | leaked service key |

## Cursor Kit Templates

- `postgresql`, `auth` — JWT claim patterns

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

