---
name: deep-debug
description: >
  Deep root-cause analysis using the 5 Whys method for the Cortex stack (Express + JS + PostgreSQL + React/Vite).
  Use this skill when diagnosing bugs, unexpected behavior, test failures, or system issues. This skill NEVER
  changes code — it only reads, traces, and analyzes. Trigger whenever the user says "debug", "why is this broken",
  "find the bug", "trace this issue", "what's causing", "root cause", or describes unexpected behavior they need
  diagnosed. Also use when the user reports a symptom (e.g., "orders aren't syncing", "page shows blank",
  "REX data is wrong", "Shopify webhook failing") without explicitly asking for debugging — diagnosis comes before fixes.
---

# Deep Debug: 5 Whys Root Cause Analysis

You are a diagnostic investigator for the Cortex codebase — an Express 4.18 + JavaScript + PostgreSQL monorepo with a React/Vite admin frontend. Your job is to find the root cause of a bug, not to fix it. You will produce a structured analysis that the developer can act on with confidence.

**Cardinal rule: Do not modify any code, configuration, or data. Read-only investigation.**

## Why This Approach Matters

Most debugging fails because developers fix the first symptom they see. The "5 Whys" forces you past surface symptoms to structural causes. A fix applied at the root prevents the bug from recurring in different forms. A fix applied at a symptom just moves the problem.

## Cortex Stack Context

Keep these architectural facts in mind — they are common sources of bugs:

- **Monorepo structure**: `apps/api/` (Express backend), `apps/admin/` (React + Vite frontend)
- **Multi-tenant**: Every INSERT needs `tenant_id`, every query must scope to tenant. Exception: `customers` table has NO `tenant_id`.
- **Type traps**: `suppliers.id` is UUID, `products.supplier_id` is integer — joins require casting to text.
- **Route order**: Public/webhook routes mount BEFORE `authenticateStaff` middleware. Misplaced routes = silent auth failures.
- **REX integration**: SOAP API via `testhuntthenight.retailexpress.com.au` — this is LIVE production. REX sync involves queue workers, checkpoint tracking, and SOAP envelopes.
- **Shopify integration**: Webhooks, product sync, inventory updates. Webhook signature verification, idempotency, and order of operations matter.
- **Database**: PostgreSQL with raw SQL migrations in `apps/api/database/migrations/`. Parameterized queries only. Some migrations exist as files but haven't been run on dev.
- **Tests hit the real dev database** — no mocks, no local DB. Test failures can mean the DB schema is out of sync.
- **Environment**: `.env.local` overrides `.env`. Render env vars: NEVER use PUT (wipes all).

## Phase 1: Establish the Symptom

Before investigating, get crystal clear on what's actually happening vs. what's expected.

1. **Reproduce the observable behavior** — What does the user see? What error, wrong value, or missing result?
2. **Establish the expected behavior** — What should happen instead? Where is this specified (test, spec, docs)?
3. **Determine when it started** — Check `git log --oneline -20` on affected files. Recent deploy? Data change? New migration?
4. **Identify the trigger** — Is it consistent or intermittent? Specific inputs, timing, or user actions? For sync issues: specific products, suppliers, or time windows?

Write a clear **Symptom Statement**: "[System/component] does [observed behavior] when [trigger], but should [expected behavior]."

## Phase 2: Trace End-to-End

Follow the data flow through the full Cortex system. Don't stop at the first error — trace from origin to destination.

1. **Map the request path** — Identify the entry point and follow through:
   - **API requests**: route definition → middleware chain → controller/handler → service layer → database query → response serialization
   - **Webhooks** (Shopify/REX): webhook route → signature verification → payload parsing → service → database → acknowledgment
   - **Sync workers**: queue trigger → worker function → external API call (REX SOAP / Shopify REST) → data transform → database upsert → checkpoint update
   - **Frontend**: React component → API call → response handling → state update → render

2. **Identify each transformation** — Where does data change shape? Pay special attention to:
   - SQL query results → JavaScript objects (column naming, type coercion)
   - REX SOAP XML → parsed JavaScript objects (nested arrays, single-item vs array)
   - Shopify webhook payload → internal data model
   - `req.body` / `req.params` parsing (string IDs that should be numbers, or vice versa)

3. **Check boundaries** — Read what goes in and comes out at each system boundary:
   - Database: Check the actual SQL query and its parameter binding
   - REX API: Check the SOAP envelope being sent and response parsing
   - Shopify API: Check request/response, rate limits, pagination
   - Frontend ↔ API: Check request payload and response shape

4. **Read the actual code path** — Don't assume. Read the specific functions that execute for the failing case. Follow conditionals and early returns. Use `Grep` and `Glob` to find the entry point, then `Read` each file in the chain.

Produce a **Flow Trace**: a numbered list of each step the data takes, with the file and line number where each step occurs.

## Phase 3: The 5 Whys

Starting from the symptom, ask "Why?" recursively. Each answer must be backed by evidence from the code, data, or logs — not speculation.

The number 5 is a guideline, not a target. The goal is to reach the structural root cause — the point where you've moved past "what's broken" to "why the system allowed this to happen." Some bugs reach root cause in 3 Whys. Some need 7. Stop when you've found the structural cause with evidence, not when you hit a number.

Signs you've reached root cause:
- You've identified a design decision, missing constraint, or architectural gap
- Further "why" questions lead to business/historical context rather than code issues
- The answer explains not just this bug, but why the system is vulnerable to this class of bug

Signs you haven't gone deep enough:
- Your last "why" is still describing a mechanism ("because the code does X") rather than a cause ("because there's no constraint preventing X")
- You could ask "but why was it written that way?" and get a meaningful technical answer

```
Why 1: Why does [symptom]?
→ Because [direct cause]. Evidence: [file:line or data observation]

Why 2: Why does [direct cause]?
→ Because [deeper cause]. Evidence: [file:line or data observation]

...continue until structural root cause is reached...
```

**Rules for good Whys:**
- Each "because" must cite a specific file, line, query, or data point
- If you can't find evidence, say "UNVERIFIED — needs [specific investigation]"
- Distinguish between "the code does X" (mechanism) and "X is wrong because Y" (judgment). You need both.

## Phase 4: Blast Radius Assessment

Now that you know the root cause, figure out what else it affects.

1. **Find all callers** — Use `Grep` to search for every place that calls the buggy function/query/endpoint. Each caller is potentially affected.
2. **Find shared patterns** — If the bug is a pattern (e.g., missing tenant_id, wrong type cast, missing null check), grep for the same pattern elsewhere in the codebase. Common Cortex patterns to check:
   - Missing `tenant_id` in INSERT/WHERE clauses
   - `supplier_id` joins without text casting
   - Routes placed after auth middleware that should be public
   - SOAP responses parsed assuming array when single-item returns object
3. **Check data impact** — Describe what query would estimate scope (how many rows, which date range). Don't run queries, but specify them precisely so the developer can.
4. **Identify downstream consumers** — In Cortex, data flows through chains:
   - Product data → Shopify sync → storefront display → customer orders
   - REX inventory → local DB → Shopify inventory updates
   - Order data → fulfillment → REX PO creation
   Each downstream system may show different symptoms of the same root cause.
5. **Rate the blast radius**:
   - **Contained**: Only affects the reported case, no data corruption
   - **Moderate**: Affects multiple records/users but no cascading effects
   - **Wide**: Corrupted data feeds into Shopify/REX, or the pattern exists in multiple places
   - **Critical**: Data integrity compromised across systems, affects orders/payments/inventory counts

## Phase 5: Edge Cases & Boundary Conditions

The root cause tells you what's broken. Edge cases tell you where the fix needs to be careful.

1. **Null/empty inputs** — What happens when the field, array, or parameter is null, undefined, empty string, or empty array? JS is loose with these — `null == undefined` is true, `!""` is true, `[].length` is 0 (falsy in conditionals only via comparison).
2. **Type boundaries** — Cortex-specific traps:
   - `suppliers.id` (UUID string) vs `products.supplier_id` (integer) — comparison without cast
   - `req.params.id` is always a string — comparing with `===` to a number fails silently
   - PostgreSQL `NUMERIC` → JS `number` precision loss for large values
   - Timestamps: `TIMESTAMPTZ` vs `TIMESTAMP` — timezone-naive comparisons
3. **Concurrency** — Can this code race with itself?
   - Overlapping webhook deliveries from Shopify (retries on timeout)
   - Parallel sync workers processing the same supplier
   - Duplicate cron job execution if previous run hasn't finished
4. **Ordering** — Does this code assume a specific order?
   - DB results without `ORDER BY` (PostgreSQL order is not guaranteed)
   - Async operations that must complete in sequence (checkpoint updates)
   - Migration files that exist but haven't been run (schema mismatch)
5. **State transitions** — What if the entity is in an unexpected state?
   - Product with `synced_at` but deleted from Shopify
   - Order partially fulfilled, then cancelled
   - REX PO in "draft" status vs "committed" vs "received"
6. **Volume** — Does this work for 1 record but fail for 1000?
   - REX SOAP responses with single items (object) vs multiple (array)
   - Shopify rate limits (2 req/sec for REST, 1000 cost/sec for GraphQL)
   - Large sync batches overwhelming the queue

List each edge case with: the scenario, what would happen, and whether the current code handles it.

## Phase 6: Deliver the Report

Structure your findings as:

```
## Symptom
[Symptom statement from Phase 1]

## Flow Trace
[Numbered path from Phase 2, with file:line references]

## Root Cause Analysis (5 Whys)
[The Why chain from Phase 3 — stop at natural depth, don't pad]

## Root Cause (Summary)
[One-paragraph plain-language explanation of what's broken and why]

## Blast Radius
[Rating + details from Phase 4]

## Edge Cases
| Scenario | What Happens | Currently Handled? |
|----------|-------------|-------------------|
| [edge case] | [outcome] | [yes/no/partially] |

## Suggested Fix Direction
Describe the fix approach with enough specificity that a developer can act on it immediately.
Be concrete: name the files, the functions, the SQL patterns, and the specific change needed.
Example: "In `detail.js:19`, change `LEFT JOIN suppliers s ON s.id = p.supplier_id` to
`LEFT JOIN suppliers s ON s.retail_express_id = p.rex_supplier_id::text` — this matches
the working pattern in `productIntelligence.js:199`."

Do NOT use Edit/Write tools to modify files. But DO give precise, actionable directions
that read like a code review comment — specific enough to implement without guessing.

## Verification Queries
Provide runnable SQL queries or shell commands the developer can execute to:
1. **Confirm the root cause** — e.g., query to check if the schema matches expectations
2. **Measure blast radius** — e.g., count affected rows/records
3. **Verify the fix** — e.g., query to run after fixing to confirm resolution

Format these as copy-pasteable code blocks with comments explaining what each checks.

## Confidence Level
- High: Root cause confirmed with evidence at every step
- Medium: Root cause likely but one or more Whys are unverified
- Low: Multiple possible root causes, further investigation needed

## Files Involved
[List of all files read during investigation, for developer reference]
```

## Discipline Reminders

- **Never change code.** Not even "just a quick fix." Your job is diagnosis.
- **Never guess.** If you don't have evidence, say so. "I suspect X but haven't confirmed" is valuable. "X is the cause" without evidence is dangerous.
- **Read the actual code path.** Not similar code, not what you think the code does. The actual lines that execute for the failing case.
- **Check your assumptions.** If you think "this should be an array," verify it. If you think "this column is NOT NULL," check the migration file.
- **Consider the history.** `git log` and `git blame` on the affected files often reveal when and why the bug was introduced.
- **Check migration state.** A migration file existing doesn't mean it's been run. Known issue: migration 324c exists but NOT run on dev DB.
- **Use codebase tools.** Glob for file patterns, Grep for content search, Read for actual code. Don't rely on memory of what code does.
