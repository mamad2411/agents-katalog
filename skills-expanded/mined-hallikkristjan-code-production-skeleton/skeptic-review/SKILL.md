---
name: skeptic-review
description: Evidence-based production-readiness audit in 14 sections — every claim needs a file:line, N/A needs a reason, the verdict comes from the table, not the impression. Use only when explicitly asked — /skeptic-review, "production readiness review", "is this ready for production", "audit this checklist", "skeptiku audit", "kas see süsteem on production-valmis". Do NOT auto-trigger on ordinary feature or bugfix work. Pairs with production-skeleton — the skeleton builds the floor, this audit proves it holds.
---

# Skeptic Review — evidence-based production-readiness audit

**Contents:** Overview · Process (6 steps) · Report shape (+ "I can do this now"
rules) · Checklist (14 sections) · Red flags · Typical mistakes

## Overview

A 14-section skeptic's checklist, graded ONLY on evidence found in the code.
Core rule: **a claim without a `file:line` is not a status, it is a guess.**
The default posture is skeptical: a section is ❌ until evidence shows otherwise.

This audit covers breadth: all 14 areas in one pass. For per-path depth in the
security section, hand off to a dedicated security review (in Claude Code: `/cso`).

Reply in the language the user wrote in. Section names and statuses stay as
written here so reports are comparable.

## Process

1. **Map the project** (type, stack, users, data). Decide for every section:
   applies or N/A. **N/A needs a one-sentence reason in the report** (e.g.
   "no payments → PCI DSS scope is zero"). Translate domain items: a
   "dropshipping partner" is every external integration (API, feed, webhook,
   agent).
2. **Collect evidence** with 2–3 parallel read-only sub-agents on a cheap
   model, split for example as security+auth+secrets / automation+monitoring+
   tests / data+backup+privacy. Every fact as `file:line` + one sentence.
   Agents report MISSING findings too.
   Orchestration rule: each evidence agent writes its report to a FILE and the
   synthesizer reads the files — a background agent's return value does not
   always reach the synthesizer's context, and a synthesis that waits for it
   stalls.
3. **Verify by running**, not by reading the README: tests, type-check,
   `npm audit` (or the ecosystem's equivalent), and the production-skeleton
   probe:
   `node <skeleton-skill>/scripts/probe.mjs . --json`
   (`<skeleton-skill>` is the production-skeleton skill directory; add
   `--url <deployment>` when a deployment is reachable). Its rows are
   `file:line` evidence for sections 1, 2, 3, 5, 6, 9, 10, 11, 12 and 13 — cite them. Read
   ops documents (runbook, backup doc), but check every claim in them against
   code or a workflow.
4. **Grade item by item:** every checklist item gets ✅ / ⚠️ / ❌ / ❓ / N/A plus
   an evidence reference. An item without evidence cannot be ✅. ❓ means not
   verified: the evidence lives where you cannot look (a vendor dashboard, MFA
   settings, a live deploy you cannot reach) or a check could not run. Say what
   you searched and where; ❓ is not ❌ (absence was not shown) and never ✅.
   A probe PASS is evidence that a pattern exists, not that the section is ✅ —
   follow it to where it is wired in or runs.
5. **Report shape** — see below, exactly in that order.
6. **Offer to save** the report as `docs/ops/skeptic-review-YYYY-MM-DD.md`
   (today's date). Ask; the audit itself is read-only.

## Report shape (exactly this order)

- **Top-3 risks** — concrete, with evidence, impact described in the user's
  language, not in audit jargon.
- **Section table** — all 14 sections, N/A included (status + 1–2 sentences
  with evidence).
- **Skeleton scorecard** — the probe's score line and its failing rows, verbatim.
- **Quick wins** — fixes under about an hour, as a separate list.
- **Not traced** — 2–4 lines: the route families, tools or jobs you did not
  open, and the checks you made by search only. End with one line: a per-path
  security review (in Claude Code: `/cso`) is the next pass for these.
- **Verdict.** "Ready" is allowed only when no applicable section is ❌ or ❓
  AND no required skeleton gate is FAIL, STALE or UNKNOWN. Otherwise the verdict
  names the blocking sections and gates; for ❓ and UNKNOWN it names what a
  human has to confirm.
- **I can do this now:** — 1–3 numbered lines (rules below). Last block.

### "I can do this now" rules (last block of the report)

- 1–3 lines, only actions the agent can take ITSELF in this environment
  (write a test, add an alert, patch a dependency, write a runbook, fix a
  config) — not "talk to the host" or "decide the RPO".
- Pick from the top-3 risks and quick wins the ones that are DOABLE — the
  block is not a repeat of quick wins, it is their executable subset in the
  form verb + object + time estimate.
- **Ordered by risk, not by ease** — the first line addresses the worst finding
  the agent can touch. A ❌ finding goes before a convenience fix.
- **Do not run them** — the audit is read-only; wait for a number or "do 1 and 3".
- If every applicable finding needs a human decision (price, legal, access):
  "I can do this now: nothing — the next step is your decision on X." Padding
  the list with trivial edits is a mistake.

## Checklist (14 sections)

1. **Architecture** — stack? where does it run? where is the database?
   backups? disaster recovery? RPO and RTO AS NUMBERS (backup frequency →
   RPO; a tested restore procedure → RTO)?
2. **Identity and access** — admin MFA? API-key management? where are secrets
   (env / Vault / Secrets Manager; any leaks in the repo)? least privilege
   (RLS, roles, scopes)? Then trace the seams:
   - **Every path:** for each documented rule on data (a `draft` status
     "hidden from users", a revoked token, a role, a time window, an OAuth
     scope), list every read and write path that touches that data — routes,
     MCP/API tools, service worker, exports — and cite where each enforces the
     rule. One path without it is ❌.
   - **Side paths:** where a guard exists (`requireAdmin`, a version check, a
     scope check), list the other handlers for the same resource and check
     each calls it. A handler that re-implements half the guard counts as missing.
   - **Fail-open:** for each guard, ask what happens when its input is absent
     or stale — no token, no role claim, an expired session, a revoked key.
     ✅ needs the request to stop (401/403, cite the line); a guard that only
     acts when the input is present and otherwise falls through is ❌.
   - **Labels vs behaviour:** a tool or scope named read-only must not write;
     a write-only grant must not return personal data.
   - **Secrets per environment:** for each production secret, list which
     environments receive it — hosting Preview/Development builds, CI jobs on
     pull requests or manually dispatched branches, and any doc that says to
     add it to "all environments". Code that nobody reviewed yet running with
     a production key is ❌.
   - **Hard-coded accounts:** search seeds, migrations, fixtures and code for
     a fixed user or password (`admin/admin`, a default password in a
     migration, `if (email === "owner@…")` as an admin check, a shared
     `ADMIN_PASSWORD`). Follow each hit: if it can reach production (a
     migration that runs there, a seed the deploy runs, a code branch with no
     environment guard) it is ❌; a fixture that only local setup loads is ✅
     with the line that keeps it local.
   - **Hand-rolled auth:** who verifies identity — an established provider
     (TARA, an OIDC/OAuth2 provider, the platform's auth) or the app's own
     code? Own code needs a password hash built for passwords (bcrypt,
     scrypt, argon2 — a plain or salted SHA/MD5 is ❌), session or reset
     tokens from a cryptographic random source (`Math.random`, timestamps or
     user ids are ❌), and JWT checks done by a library that pins the
     algorithm and checks expiry. A hand-written login flow where a provider
     was available is ⚠️ even when it passes these.
3. **External integrations** — how is each authenticated? what happens when a
   partner is down? retry/backoff? idempotency (can the same operation run
   twice)?
   **If the server fetches a URL that comes from data** (a link checker, a
   webhook target, an image proxy, a preview/unfurl, a URL stored by a user or
   an agent): ✅ needs a check that blocks private, loopback and link-local
   addresses after DNS resolution, with redirects re-checked, or a host
   allowlist. A scheme check alone is ❌.
4. **Payments** — are card details touched? PCI DSS scope? webhook
   validation? double-charge prevention? (No payments → N/A with a reason.)
5. **Security** — SQLi? XSS? CSRF? CSP headers? rate limiting? login
   brute-force protection? CONTINUOUS dependency CVE scanning (Dependabot /
   Renovate / audit in CI — a one-off `npm audit` does not count as ✅)?
   **Hand-rolled primitives:** list code that reimplements what the standard
   library or a maintained package already does — date and time-zone math,
   money as floating point, CSV or HTML parsing, HTML sanitizing, encryption
   or signing, URL or e-mail validation used as a security check. Each needs
   a reason in the code or docs; a hand-written sanitizer or crypto routine is
   ❌, other primitives are ⚠️ with the input that would break them (a DST
   switch, a time zone other than the server's, 0.1 + 0.2, a quoted comma).
6. **Data protection** — where does personal data live (per table)? privacy
   mapping documented (GDPR or the local equivalent)? log/audit retention defined AND enforced? right to be
   forgotten mechanism (soft-archive is not deletion; mind the backup copies)?
   **If the app exports CSV or spreadsheets** with text people typed: a cell
   that starts with `=`, `+`, `-`, `@`, tab or carriage return runs as a
   formula when opened. ✅ needs neutralization in the export function (cite
   it); quoting the cell is not enough.
7. **AI usage** — which AI does what (inventory)? can AI change data without
   human confirmation? hallucination guards (schema validation,
   human-in-the-loop)? prompt-injection surface (which external data reaches
   a prompt)?
   **If the app has a tool-calling agent** (MCP server, function calling, an
   agent loop that reads or writes data):
   - **Whose key:** cite the credential each tool uses. The owner's service
     key or the user's full session is ❌; a key scoped to the task and the
     caller's permissions is ✅. A read-only tool on a write-capable key is ❌.
   - **Memory:** list every write to agent memory, a vector store or a
     "notes" table whose content came from outside text (a web page, an
     e-mail, a document, another tool's output). ✅ needs validation or a
     human step before the write; untrusted text that persists and is read
     back into a later prompt is ❌.
   - **Ceiling:** per-user or per-session caps on model calls, tool calls and
     spend, cited. None is ❌ (one runaway loop is the whole month's budget).
8. **Automation** — handling of bad input (sanity checks, limits such as
   max-delete)? protection against absurd values? change log? rollback path?
   **Read-then-write:** every counter, limit, "already sent" flag or
   move/assign operation that is read in one query and written in another
   can race. List them with `file:line`; ✅ needs a single conditional
   `UPDATE … WHERE`, a unique constraint, a lock or an RPC.
9. **Monitoring** — HOW do you learn that the nightly job failed (a silent
   `console.error` is not an alert)? alerting? dashboard / health? are logs
   in one place?
10. **Testing** — how many tests (count them, do not trust the README)?
    integration tests? CI/CD? smoke test before/after a production deploy?
11. **Scalability** — 10× load? a slow external API (timeouts)? loss of a
    single worker/instance (in-memory state)? Judge in THE PROJECT'S context,
    not abstractly.
12. **Business continuity** — AI service down? external API changes? partner
    quits? bus factor (who besides the owner can get in / knows the system)?
13. **Operations** — the processes that keep the system running after the code
    is written. A process counts only with a trace that it is followed; a
    document nobody has used is ⚠️, and settings you cannot see (branch
    protection, on-call rota, vendor support plan) are ❓.
    - **Incidents:** who gets the alert, and what do they do in the first 15
      minutes (an incident runbook, cited)? where are past incidents written
      down (a post-mortem, an issue label)? An alert with no named receiver is ❌.
    - **Support:** where does a user report a problem (a channel named in the
      app or docs) and who reads it? a stated response time? No channel is ❌.
    - **Change:** how does a change reach production — reviewed, tested in CI,
      deployed by a recorded pipeline, with a change log or release notes? A
      manual deploy from a laptop with no record is ❌.
    - **Lifecycle:** runtime, framework and database versions against their
      end-of-life dates (cite the version line); domain and certificate renewal
      (who, automatic?). A version past EOL is ❌.
    - **Redundancy and failover:** what is single — one region, one instance,
      one database, one person with the keys? what happens when it fails, and
      does that match the RTO in section 1? "The host handles it" needs the
      plan or setting that says so.
    - **Secret rotation:** a written way to rotate each production secret, and
      the date it last happened. A key that cannot be rotated without downtime
      is ⚠️.
    For a one-person project the short version is enough, but it has to exist:
    who answers when the owner is away, and where that is written.
14. **Top-3 risks** — the opening question of the checklist; answer it at the
    top of the report, with evidence.

## Red flags — these thoughts mean you are slipping

| Thought | Reality |
|---|---|
| "The README/doc says it exists" | Doc ≠ evidence. Find the code or workflow that does it. |
| "The project is small, this section does not matter" | The section still goes in the report — graded, or N/A with a reason. |
| "Monitoring exists (Sentry is installed)" | The question is whether THIS specific silent failure reaches an alert. Follow the path to the end. |
| "There is a backup → architecture ✅" | Without RPO/RTO numbers a backup is half an answer. A weekly backup is a 7-day RPO — say it. |
| "Overall it feels mature, verdict: ready" | The verdict comes from the section table and the skeleton scorecard, not from the impression. Count the ❌. |
| "The privacy / AI / continuity sections do not seem relevant" | The three most often skipped. If truly N/A, write why. |
| "Two slop patterns already — the rest will be the same, stop here" | Patterns are findings, not a verdict. Hard-coded accounts, hand-rolled auth and hand-rolled primitives go into Top-3 risks, and the audit still runs all 14 sections: the fix list needs every hole, not the first one. |
| "It is a solo project, processes do not apply" | Operations is never N/A for a deployed app. Grade the short version: who answers when the owner is away, where that is written. |

## Typical mistakes

- **A section left uncovered by default** — in baseline runs, privacy,
  AI governance, RPO/RTO and business continuity were consistently skipped.
  The mandatory section table exists against exactly that.
- **An optimistic summary** — found ⚠️s get softened under "but generally
  fine". The top-3 risks must be the first thing the reader sees.
- **The last block filled with other people's work** — "I can do this now"
  lines that need the user's decision or an outside party do not belong
  there; they stay in risks / quick wins.
- **Evidence = "the code looks OK"** — evidence is a `file:line` the reader
  can open.
- **"Ready" over a failing skeleton gate** — a working app with no CI, no
  backup drill or no error tracking is not ready, however clean the code.
