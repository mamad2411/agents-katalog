---
name: deep-investigation
description: "Hypothesis-driven analysis for all ad-hoc requests — bugs, features, refactoring, and changes. Use as the standard analysis path for every ad-hoc task. Triggers on: ad-hoc analysis, bug analysis, feature analysis, root cause investigation, why doesn't X work, data flow tracing, production issue, unexpected behavior, add feature, refactor, change behavior."
---

# Deep Investigation

> **Load this skill when:**
>
> - Handling ANY ad-hoc request (this is the standard analysis path for all ad-hoc work)
> - Investigating a bug or unexpected behavior
> - Analyzing where and how to add a feature
> - Planning a refactoring or behavioral change
> - Tracing data flows, code patterns, or architectural decisions
> - Diagnosing "it should work but doesn't" problems
> - Analyzing production issues or user-reported bugs
>
> **This skill is loaded for EVERY ad-hoc request.** It replaces the old shallow analysis (grep → probe → dashboard) with a rigorous, hypothesis-driven approach that works for bugs, features, and everything in between.
>
> **Different from `@debugger`:** The `debugger` agent is for production incident triage — pulling ticket context, searching logs, and identifying likely defect areas from external signals. This skill is for hypothesis-driven code and data investigation where you need to prove your analysis with evidence.

---

## Why This Skill Exists

The default analysis pattern is shallow:

```
User requests change → Builder does quick grep → Builder presents
surface-level understanding → implements based on assumptions →
fix is wrong or feature is built in the wrong place
```

This skill enforces a structured, multi-track, hypothesis-driven process that works for ALL ad-hoc requests — bugs, features, refactoring, and changes alike. It separates what's CONFIRMED from what's INFERRED — and refuses to conclude without real evidence.

**For bugs:** This means proving the root cause before fixing.
**For features:** This means understanding existing patterns, tracing related code, and confirming the right approach before building.
**For refactoring:** This means understanding current behavior and dependencies before changing anything.

---

## Investigation Flow

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. OBSERVE       │ ──► │  2. HYPOTHESIZE   │ ──► │  3. DESIGN TESTS  │
│                  │     │                  │     │                  │
│ Gather symptoms, │     │ Form 2-3         │     │ For each: what   │
│ user report,     │     │ candidate root   │     │ confirms it?     │
│ error messages   │     │ causes           │     │ What contradicts? │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                          │
┌──────────────────┐     ┌──────────────────┐             │
│  6. CONCLUDE      │ ◄── │  5. EVALUATE      │ ◄──────────┘
│                  │     │                  │
│ Present root     │     │ Score hypotheses │     ┌──────────────────┐
│ cause with       │     │ against evidence │ ◄── │  4. EXECUTE       │
│ confidence level │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     │ Run parallel     │
                                                  │ investigation    │
                                                  │ tracks           │
                                                  └──────────────────┘
```

---

## Step 1: Observe

Gather all available information before forming hypotheses:

- **User report** — What did they describe? What did they expect? What happened instead?
- **Error messages** — Exact text, not paraphrased
- **Reproduction steps** — Can it be reproduced? Under what conditions?
- **Scope** — Does it affect all users, some users, one user? All data, some data?
- **Timing** — When did it start? Did anything change recently?

Write down the symptoms as a factual list. No interpretation yet.

```
SYMPTOMS:
1. User reports: "New comments don't show up on the dashboard"
2. Comments ARE saved successfully (user confirmed they appear on the detail page)
3. Dashboard shows stale data — last updated timestamp is 3 hours old
4. Affects all users (confirmed by checking with second account)
5. Started after last deploy (Thursday 2pm)
```

---

## Step 2: Hypothesize

Form **2-3 candidate hypotheses or approaches**. Each must be specific and testable — not vague.

**For bugs** — hypothesize the root cause:

| Quality | Example |
|---------|---------|
| Too vague | "Something is wrong with the data flow" |
| Too specific | "Line 47 of comments.ts has a typo" |
| Right level | "The dashboard query filters by `updated_at` but comments don't update the parent record's `updated_at`" |

**For features** — hypothesize the best implementation approach:

| Quality | Example |
|---------|---------|
| Too vague | "Add it somewhere in the settings" |
| Too specific | "Add a toggle at line 47 of Settings.tsx" |
| Right level | "Dark mode toggle belongs in the theme context, following the existing pattern used by font-size preferences" |

**For refactoring** — hypothesize the best strategy:

| Quality | Example |
|---------|---------|
| Too vague | "Clean up the code" |
| Right level | "Extract the shared validation logic from 3 form components into a useFormValidation hook, following the existing useFormState pattern" |

**Rules:**
- Minimum 2 hypotheses/approaches, maximum 4
- Each must be specific enough to investigate and confirm/contradict with evidence
- At least one hypothesis should challenge the obvious assumption
- If you can only think of one, you haven't investigated enough — look at the problem from the data side, the code side, and the architecture side

---

## Step 3: Design Tests

For each hypothesis/approach, fill out this template:

**For bugs (root cause investigation):**

```
HYPOTHESIS: [one sentence — what's wrong and why]
IF TRUE:    [what specific evidence would we expect to find?]
IF FALSE:   [what specific evidence would contradict this?]
TEST:       [concrete action — query, log check, code trace, API call]
```

**For features and refactoring (approach investigation):**

```
APPROACH:        [one sentence — where and how to implement]
ADVANTAGES:      [why this approach is good — existing patterns, simplicity, consistency]
RISKS:           [what could go wrong — breaking changes, inconsistency, performance]
INVESTIGATION:   [concrete action — trace existing patterns, check consumers, verify assumptions]
```

**Bug example:**

```
HYPOTHESIS: Dashboard query uses a materialized view that isn't refreshed on comment creation
IF TRUE:    The materialized view's last refresh timestamp is older than recent comments
IF FALSE:   The materialized view was refreshed after the most recent comment
TEST:       Query the materialized view metadata for last refresh time; compare with latest comment created_at
```

**Feature example:**

```
APPROACH: Add dark mode toggle to the existing ThemeContext, following the font-size preference pattern
ADVANTAGES: Consistent with existing pattern; ThemeContext already propagates to all components; CSS variables are already in place
RISKS: ThemeContext may not persist to localStorage — font-size doesn't persist either; some components may use hardcoded colors
INVESTIGATION: Trace ThemeContext consumers; check if CSS variables cover all color tokens; check localStorage persistence in existing preferences
```

**Quality check:** If your IF TRUE/IF FALSE (bugs) or ADVANTAGES/RISKS (features) sections are vague ("we'd see an error" / "it might break"), the test isn't specific enough. What error? Where? What breaks and why?

---

## Step 4: Execute — Parallel Investigation Tracks

Launch **at minimum 2-3 of these tracks in parallel**. Never send a single @explore agent and call it done.

### Track 1: Code Trace

**Agent:** @explore

**Objective:** Trace the relevant code paths end-to-end.

**For bugs:** Trace both the write/producer side AND the read/consumer side of the data flow.
**For features:** Trace existing patterns that the new feature should follow, and identify integration points.
**For refactoring:** Trace all consumers of the code being refactored to understand blast radius.

**Delegation template (bugs):**

```
Trace the complete data flow for [feature]:

WRITE SIDE:
- Where does data enter the system? (UI form, API endpoint, webhook, etc.)
- What transformations happen? (validation, mapping, enrichment)
- Where is it stored? (which table, which columns, what format)
- Are there any side effects? (cache invalidation, event emission, notifications)

READ SIDE:
- Where does the UI read this data from? (API endpoint, direct query, cache)
- What query/filter is used? (exact SQL or ORM call)
- Are there any transformations between storage and display? (aggregation, joins, formatting)
- Are there intermediate layers? (materialized views, caches, CDN, edge functions)
- Are there decoding/mapping structs that could drop fields? (Codable, DTOs, GraphQL selections)

CRITICAL: Trace BOTH sides. Finding how data is written tells us nothing about how it's read.
Report each finding with its source (file:line) and include the actual code snippet.
If a struct decodes data, list ALL its fields — omitted fields are a common root cause.
```

**Delegation template (features):**

```
Analyze existing patterns for [feature area]:

EXISTING PATTERNS:
- How do similar features work in this codebase? (find 2-3 analogous features)
- What patterns do they follow? (component structure, state management, data flow)
- What shared infrastructure exists? (contexts, hooks, utilities, design system components)

INTEGRATION POINTS:
- Where would this feature connect to the existing code? (routes, navigation, layouts)
- What data does it need? (API endpoints, database tables, state stores)
- What components can be reused? (design system, shared components)

CONSTRAINTS:
- Are there architectural boundaries to respect? (module boundaries, layer restrictions)
- Are there conventions that apply? (naming, file structure, test patterns)

Report each finding with its source (file:line) and include the actual code snippet.
```

> **Never accept "the code looks correct" as a finding.** The question is not whether the code looks correct — it's whether it actually produces the expected behavior. Code that "looks correct" but doesn't work is the entire reason we're investigating.

### Track 2: Data & Pattern Verification

**Agent:** @explore

**Objective (bugs):** Query ACTUAL data state using available tools.
**Objective (features):** Verify assumptions about existing patterns, data structures, and infrastructure.

**Tool discovery is mandatory.** Before designing queries, @explore MUST check `project.json` to determine what's available:

| Check in `project.json` | What it means | Tool to use |
|--------------------------|---------------|-------------|
| `integrations` contains `supabase` | Supabase project exists | `supabase` CLI (check linked project with `supabase projects list`), or direct REST API via `curl` with service_role key from `supabase projects api-keys --project-ref <ref>` |
| `database.client` is `supabase` | Same as above | Same as above |
| `stack.frameworks` contains `prisma` | PostgreSQL likely | `psql` or Prisma Studio |
| `apps[].type` is `desktop` or `mobile` | May have local SQLite | `sqlite3` on local DB files |
| `integrations` contains `redis` | Cache layer exists | `redis-cli` |
| Project has REST API endpoints | API is queryable | `curl` against running server |

**Also check the environment:**
- `which supabase psql sqlite3 redis-cli` — what CLIs are actually installed?
- `supabase projects list` — is the project linked? What's the project ref?
- `ls <project>/supabase/migrations/` — what tables exist? What columns were added recently?

**Delegation template (bugs):**

```
Verify the actual data state for [feature].

STEP 1 — Tool discovery:
- Read project.json → integrations, database, stack sections
- Run `which supabase psql sqlite3 redis-cli` to check available CLIs
- If Supabase: run `supabase projects api-keys --project-ref <ref>` to get credentials
- Check migrations directory for relevant table schemas

STEP 2 — Query real data:
For every claim about what data "should" exist, run a real query.

Specific queries to run:
1. [Query to verify data exists where we expect it]
2. [Query to check timestamps/freshness]
3. [Query to compare write-side data with read-side data]
4. [Query to check for edge cases — nulls, empty strings, wrong types]

STEP 3 — Report with evidence:
For EVERY finding, include:
- The exact command you ran
- The exact output you got
- Your interpretation of the result

Do NOT report "data should be in table X" without querying table X.
Do NOT report "the column exists" without checking if it has non-null data.
```

**Delegation template (features):**

```
Verify assumptions about [feature area].

STEP 1 — Tool discovery:
- Read project.json → integrations, database, stack sections
- Check available CLIs and infrastructure

STEP 2 — Verify each assumption:
For every claim about "how the codebase works" or "what patterns exist," find concrete evidence.

Specific checks:
1. [Verify the assumed pattern actually exists — find real examples]
2. [Verify the data structures/APIs we plan to use exist and work as expected]
3. [Verify there are no conflicting patterns or conventions]
4. [Check if similar features have tests — what patterns do they follow?]

STEP 3 — Report with evidence:
For EVERY finding, include:
- The file:line where you found the evidence
- The actual code snippet
- Your interpretation

Do NOT report "the codebase uses pattern X" without citing specific files.
Do NOT report "this API exists" without showing its signature and usage.
```

> **Every claim about data state MUST be backed by a query.** "The data should be in the comments table" is INFERRED. "I ran `SELECT count(*) FROM comments WHERE created_at > '2026-03-01'` and got 47 rows" is CONFIRMED.

### Track 3: Runtime / Current State Evidence

**Agent:** @explore

**Objective (bugs):** Check what actually happened at runtime — logs, console output, network requests, error tracking.
**Objective (features):** Observe the current state of the affected area — what exists now, what the user sees, what the current behavior is.

**What to check depends on the project:**

| Evidence Source | How to Access | What to Look For |
|-----------------|---------------|------------------|
| Server logs | Log files, `docker logs`, cloud logging | Errors, warnings, unexpected paths taken |
| Browser console | Playwright, DevTools screenshot | JS errors, failed network requests |
| Network requests | Playwright network interception, proxy logs | Response status codes, response bodies, timing |
| Error tracking | Sentry, Bugsnag, etc. via API or dashboard | Unhandled exceptions, frequency, stack traces |
| Database logs | `pg_stat_activity`, slow query log | Failed queries, lock contention, deadlocks |

**Delegation template (bugs):**

```
Gather runtime evidence for [feature]:

1. Check server logs for errors or warnings related to [area] in the last [timeframe]
2. If Playwright is available: navigate to [page], open DevTools, reproduce [action], capture console output and network requests
3. Check for any error tracking entries (Sentry, etc.) related to [area]
4. Check application-level logs (log files, structured logging output)

For EVERY check, report:
- The exact command you ran (grep, tail, curl, Playwright script, etc.)
- The exact output — copy/paste the relevant lines, don't summarize
- If a check returned nothing: say "Ran [command], got 0 results" — absence of evidence is still evidence

Do NOT say "the logs show normal behavior" without including the log lines.
Report what ACTUALLY happened at runtime — not what the code says should happen.
```

**Delegation template (features):**

```
Observe the current state of [affected area]:

1. What does the user currently see in this area? (describe the current UI/behavior)
2. What existing functionality is adjacent to where the new feature will go?
3. Are there any existing UI elements, routes, or state that the feature will interact with?
4. Check for any existing configuration, feature flags, or settings related to [area]

For EVERY observation, report:
- What you found and where (file:line or runtime observation)
- Whether this is from code analysis (INFERRED) or actual runtime/data check (CONFIRMED)
```

### Track 4: Comparative Analysis (Optional but Valuable)

**Agent:** @explore

**Objective:** Find a similar feature that DOES work and identify what's different.

**When to use:**
- The broken feature follows "the same pattern" as something that works
- The feature worked before and stopped working
- Multiple similar features exist but only one is broken

**Delegation template:**

```
Compare [broken feature] with [working feature]:

1. Both use the same pattern/architecture — what's different in implementation?
2. Compare the data flow: where does the working version do something the broken one doesn't?
3. Check for recent changes to the broken feature that diverged from the pattern
4. Look at the database schema — are there differences in indexes, constraints, triggers?

Focus on DIFFERENCES. Similarities confirm the pattern; differences point to the bug.
```

---

## Step 5: Evaluate

When investigation tracks return, score each hypothesis against the evidence.

### Evidence Classification

**Every finding MUST be tagged with one of these classifications:**

| Tag | Meaning | Reliability |
|-----|---------|-------------|
| **CONFIRMED** | Verified by querying real data, running real commands, or observing real behavior | High — this is fact |
| **INFERRED** | Logically follows from code reading, but not independently verified | Medium — could be wrong |
| **ASSUMED** | Gap-filling, no evidence either way | Low — probably wrong |

**Rules for classification:**

- "I read the code and it does X" → **INFERRED** (code could be dead, overridden, or conditional)
- "I ran this query and got this result" → **CONFIRMED** (with the query and result as evidence)
- "I checked the logs and saw this error" → **CONFIRMED** (with the log entry as evidence)
- "This probably happens because..." → **ASSUMED** (no evidence cited)
- "The cache TTL is set to 1 hour in config" → **INFERRED** (config could be overridden at runtime)
- "I called the API and the response had Cache-Control: max-age=3600" → **CONFIRMED**

### Hypothesis/Approach Scoring

For each hypothesis or approach, list the evidence and classify it:

**Bug example:**

```
HYPOTHESIS 1: Dashboard uses materialized view that isn't refreshed

  Evidence FOR:
  [CONFIRMED] Queried pg_matviews — last_refresh is 2026-03-15 08:00, latest comment is 2026-03-15 14:30
  [CONFIRMED] Dashboard API returns data matching the stale materialized view, not the live table
  [INFERRED]  Comment creation code does not call REFRESH MATERIALIZED VIEW

  Evidence AGAINST:
  (none found)

  Verdict: LIKELY ROOT CAUSE — 2 CONFIRMED findings support, 0 contradict
  Confidence: HIGH

HYPOTHESIS 2: API response caching with long TTL

  Evidence FOR:
  [INFERRED]  API middleware includes caching layer

  Evidence AGAINST:
  [CONFIRMED] curl -I shows Cache-Control: no-cache on dashboard endpoint
  [CONFIRMED] Two sequential API calls return identical data (but this is because
              the materialized view hasn't changed, not because of HTTP caching)

  Verdict: CONTRADICTED — confirmed evidence shows no HTTP caching
  Confidence: N/A (eliminated)
```

### Decision Rules

| Scenario | Action |
|----------|--------|
| One hypothesis has CONFIRMED evidence, others contradicted | Present as root cause with HIGH confidence |
| Multiple hypotheses have CONFIRMED evidence | Investigate interaction — may be multiple contributing factors |
| Only INFERRED evidence for all hypotheses | **STOP — run additional verification.** Cannot conclude without CONFIRMED evidence |
| All hypotheses contradicted | Form new hypotheses based on what you learned — see "Escalation" below |
| Evidence is contradictory | Contradictions are gold — investigate the contradiction itself, it often IS the bug |

### Escalation: When All Hypotheses Fail

If all hypotheses are contradicted or evidence is inconclusive, widen the investigation:

1. **Check recent changes.** Run `git log --oneline --since="2 weeks ago" -- <relevant paths>` to see what changed recently in the affected area. A hypothesis of "something changed recently that broke this" is always worth testing.

2. **Check adjacent systems.** The bug may not be in the component you investigated — it may be in something that feeds into it (an upstream service, a database trigger, a middleware, a build step).

3. **Check infrastructure.** Environment variables, deployment config, DNS, SSL, permissions — the "it works on my machine" class of bugs.

4. **Reproduce and observe.** If the project supports it, use Playwright or manual reproduction to observe the actual behavior step-by-step. Sometimes watching the bug happen reveals the cause.

5. **Ask the user.** If you've exhausted technical investigation, present what you've eliminated and ask the user for additional context. "I've ruled out X, Y, and Z. Can you tell me more about when this started or what changed?"

Form new hypotheses from whatever the escalation reveals, then go back to Step 3 (Design Tests).

---

## Step 6: Conclude

Present the finding (root cause for bugs, recommended approach for features) with supporting evidence and confidence level.

### Investigation Dashboard

**For bugs:**

```
═══════════════════════════════════════════════════════════════════════
                        INVESTIGATION COMPLETE
═══════════════════════════════════════════════════════════════════════

ISSUE: New comments don't appear on dashboard

ROOT CAUSE                                        Confidence: HIGH
───────────────────────────────────────────────────────────────────────
Dashboard reads from materialized view `dashboard_summary` which is
only refreshed by a cron job every 6 hours. Comment creation does not
trigger a view refresh.

EVIDENCE
───────────────────────────────────────────────────────────────────────
  [CONFIRMED] Materialized view last refreshed at 08:00; latest comment
              at 14:30 (query: SELECT * FROM pg_matviews WHERE ...)
  [CONFIRMED] Dashboard API returns stale data matching view contents
              (curl output attached)
  [INFERRED]  Comment creation handler does not call REFRESH MATERIALIZED
              VIEW (code trace: src/api/comments.ts:47)

ELIMINATED HYPOTHESES
───────────────────────────────────────────────────────────────────────
  HTTP caching — CONTRADICTED by confirmed Cache-Control: no-cache header
  Wrong table — CONTRADICTED by confirmed schema trace showing same table

RECOMMENDED FIX
───────────────────────────────────────────────────────────────────────
  Option A: Add REFRESH MATERIALIZED VIEW CONCURRENTLY after comment
            insert (immediate consistency, small write latency cost)
  Option B: Switch dashboard query from materialized view to live table
            with proper indexes (always fresh, slightly slower reads)
  Option C: Reduce cron refresh interval to 5 minutes (compromise —
            still slightly stale but much better)

VERIFICATION
───────────────────────────────────────────────────────────────────────
  After fix: Create comment → check dashboard within 10 seconds →
  new comment should appear

═══════════════════════════════════════════════════════════════════════

[G] Go ahead — implement the recommended fix
[V] Run additional verification on a specific finding
[?] Ask questions about the evidence or findings

> _
═══════════════════════════════════════════════════════════════════════
```

**For features:**

```
═══════════════════════════════════════════════════════════════════════
                        INVESTIGATION COMPLETE
═══════════════════════════════════════════════════════════════════════

REQUEST: Add dark mode toggle to settings

RECOMMENDED APPROACH                              Confidence: HIGH
───────────────────────────────────────────────────────────────────────
Add toggle to ThemeContext following the existing font-size preference
pattern. CSS variables already cover all color tokens. Toggle persists
to localStorage via the existing usePersistedState hook.

EVIDENCE
───────────────────────────────────────────────────────────────────────
  [CONFIRMED] ThemeContext exists at src/contexts/ThemeContext.tsx:1
              with provider wrapping entire app (src/App.tsx:12)
  [CONFIRMED] Font-size preference uses usePersistedState hook
              (src/hooks/usePersistedState.ts:1) — same pattern works
  [CONFIRMED] CSS variables for colors defined in src/styles/tokens.css
              with dark-mode variants already present (lines 45-120)
  [INFERRED]  3 components use hardcoded colors instead of CSS variables:
              Header.tsx:23, Sidebar.tsx:45, Footer.tsx:12

ELIMINATED APPROACHES
───────────────────────────────────────────────────────────────────────
  Tailwind dark: class — CONTRADICTED by project not using Tailwind
  CSS media query only — CONTRADICTED by need for user toggle (not just
    system preference)

IMPLEMENTATION PLAN
───────────────────────────────────────────────────────────────────────
  1. Add isDarkMode state + toggle to ThemeContext
  2. Persist via usePersistedState (existing pattern)
  3. Apply data-theme attribute to document root
  4. Fix 3 hardcoded color components (Header, Sidebar, Footer)
  5. Add toggle UI to Settings page

VERIFICATION
───────────────────────────────────────────────────────────────────────
  After implementation: Toggle dark mode → all pages render correctly
  in both modes → preference persists across page reload

═══════════════════════════════════════════════════════════════════════

[G] Go ahead — implement the plan
[V] Run additional verification on a specific finding
[?] Ask questions about the evidence or findings

> _
═══════════════════════════════════════════════════════════════════════
```

---

## Rules

> These rules are non-negotiable. They exist because past work failed by violating them.

### 1. Never conclude with only INFERRED evidence

At least one piece of CONFIRMED evidence is required to present a conclusion — whether it's a root cause (bugs) or a recommended approach (features). If all you have is code analysis, run queries, check actual files, or verify patterns exist to confirm.

**Wrong:** "The code reads from table X so the data must be there"
**Right:** "I queried table X and found 0 rows matching the filter" (CONFIRMED)

**Wrong:** "The codebase probably uses context for state management"
**Right:** "I found ThemeContext at src/contexts/ThemeContext.tsx with 12 consumers" (CONFIRMED)

### 2. Always trace BOTH sides of a data flow

If the issue is "data doesn't appear," investigate BOTH where data is written AND where data is read. If the request is a feature, investigate BOTH where similar features live AND how they integrate with the rest of the system. The insight is almost always in the gap between them.

**Wrong:** "I traced the comment creation code and it correctly inserts into the table"
**Right:** "Comment inserts into `comments` table (confirmed via query), but dashboard reads from `dashboard_summary` materialized view (confirmed via code trace + query comparison)"

### 3. Verify data claims with real queries

If the project has database access (Supabase CLI, psql, API), every claim about data state MUST include the query and its result. No exceptions.

### 4. Verify runtime claims against logs

If the project has logs (server logs, browser console, error tracking), runtime behavior claims SHOULD be verified against actual log output.

### 5. Contradictions are the most valuable findings

When code analysis says X but data shows Y, that contradiction usually points directly at the bug. Never dismiss or smooth over contradictions — investigate them.

### 6. Explicitly report contradicted hypotheses

When evidence contradicts a hypothesis, say so clearly. Don't silently drop hypotheses — the user needs to see what was eliminated and why.

### 7. Never send a single investigation track

Minimum 2 parallel tracks. A single @explore returning a single narrative is how investigations fail. Multiple angles catch what a single angle misses.

---

## Integration with Ad-Hoc Workflow

### When This Skill Is Loaded

This skill is loaded by the `adhoc-workflow` skill for **every ad-hoc request**. It is the standard analysis path — not a special case for bugs only.

| Request Pattern | Load This Skill? |
|-----------------|------------------|
| "Why doesn't X work?" | Yes |
| "X is broken / not showing / returns wrong data" | Yes |
| "Users are reporting [unexpected behavior]" | Yes |
| "Add feature X" | Yes |
| "Refactor Y" | Yes |
| "Change the behavior of Z" | Yes |
| "Fix the typo in X" | Yes (lightweight — 2 tracks, quick conclude) |
| "X throws error Y" with obvious cause | Yes (lightweight — may conclude quickly) |

### Sequencing with Ad-Hoc Workflow

This skill runs **during Phase 0 of adhoc-workflow** — replacing the old shallow analysis with rigorous, hypothesis-driven investigation for all requests:

```
adhoc-workflow Phase 0
    │
    └── Deep investigation (ALL ad-hoc requests) ◄── THIS SKILL
            │
            ├── Observe (gather context)
            ├── Hypothesize (2-3 approaches)
            ├── Parallel investigation tracks
            ├── Evaluate evidence
            ├── Implementation decisions (Step 0.1c from adhoc-workflow)
            └── Present investigation dashboard
                    │
                    └── [G] Go ahead → adhoc-workflow Phase 1 (implement)
```

After the user chooses `[G] Go ahead`, control returns to adhoc-workflow Phase 1 for implementation. The investigation findings (root cause/recommended approach, evidence, implementation plan) are passed as context for the implementation delegation.

### Analysis Dashboard Integration

The investigation dashboard (Step 6) IS the analysis dashboard for all ad-hoc requests. It shows:

- Hypotheses/approaches with evidence classification (CONFIRMED / INFERRED / ASSUMED)
- Eliminated hypotheses/approaches with contradiction evidence
- Confidence level (HIGH / MEDIUM / LOW)
- Recommended fix (bugs) or implementation plan (features)

The **[G] gate** clearly shows the user which claims are CONFIRMED vs INFERRED, so they can make an informed decision about proceeding.

### Low Confidence Handling

If confidence is LOW (mostly INFERRED/ASSUMED evidence):

1. **Do NOT present to the user yet**
2. Run additional verification tracks targeting the gaps
3. If still LOW after additional verification, present with explicit warnings:

```
═══════════════════════════════════════════════════════════════════════

WARNING — CONFIDENCE: LOW
Most findings are INFERRED, not confirmed with real evidence.

The following claims need verification before implementing a fix:
  [INFERRED] Cache TTL is set to 1 hour (not verified at runtime)
  [ASSUMED]  The issue started after Thursday's deploy (timing correlation only)

Recommended: Run [specific verification steps] before proceeding.

[G] Go ahead anyway (risk: may fix wrong thing)
[V] Run additional verification
[?] Ask me questions about the findings

> _
═══════════════════════════════════════════════════════════════════════
```

---

## Anti-Patterns This Skill Prevents

| Anti-Pattern | What Goes Wrong | What This Skill Does Instead |
|--------------|----------------|------------------------------|
| Single explore agent, single narrative | Misses alternative explanations; confirmation bias | Minimum 2-3 parallel tracks with competing hypotheses |
| "Code shows X should work" | Code can be dead, overridden, conditional, or simply wrong | Requires CONFIRMED evidence from queries or runtime |
| Investigating only the suspected component | Bug is often in the gap between components; feature often needs to integrate with multiple systems | Traces BOTH sides of every data flow; maps full integration surface for features |
| Accepting plausible narratives | Plausible ≠ true; sounds right ≠ is right | Evidence classification forces explicit proof |
| Presenting INFERRED as CONFIRMED | User thinks analysis is proven when it's actually a guess | Every finding tagged with evidence classification |
| Missing the real issue | Single angle → single narrative → wrong fix or wrong approach | Multiple tracks + hypothesis testing → correct conclusion |
| Silently dropping contradicted hypotheses | User doesn't know what was eliminated or why | Explicit ELIMINATED section with contradiction evidence |
| Shallow feature analysis | "Just add it here" without understanding existing patterns | Parallel pattern discovery + data verification → informed approach |

---

## Example: Minimal Investigation (Bug)

Even for quick investigations, the structure applies. Here's a minimal version:

```
SYMPTOMS: Button click doesn't trigger save

HYPOTHESIS 1: onClick handler not attached to button element
IF TRUE:    Button element in DOM has no click event listener
IF FALSE:   Click event listener is present and fires
TEST:       Playwright — click button, check if handler console.log fires

HYPOTHESIS 2: Save API call fails silently
IF TRUE:    Network tab shows failed request or no request on click
IF FALSE:   Network request succeeds with 200
TEST:       Playwright — click button, capture network requests

TRACKS:
  Track 1 (Code): @explore — trace onClick from JSX to API call
  Track 2 (Runtime): @explore — Playwright click + network capture

[Results come back, evaluate, conclude]
```

## Example: Minimal Investigation (Feature)

```
REQUEST: Add a "copy to clipboard" button to code blocks

APPROACH 1: Use existing IconButton component + navigator.clipboard API
ADVANTAGES: Consistent with existing icon buttons; clipboard API is standard
RISKS: navigator.clipboard may need HTTPS; existing CodeBlock may not have a wrapper element
INVESTIGATION: Check if IconButton exists; check CodeBlock component structure; check if other copy features exist

APPROACH 2: Use a third-party copy library (react-copy-to-clipboard)
ADVANTAGES: Handles edge cases (fallback for older browsers)
RISKS: New dependency; may not match existing component patterns
INVESTIGATION: Check package.json for existing copy utilities; check bundle size policy

TRACKS:
  Track 1 (Code): @explore — trace CodeBlock component structure, find IconButton pattern
  Track 2 (Pattern): @explore — find other "action buttons on content" patterns in the codebase

[Results come back, evaluate, conclude]
```

The overhead is minimal. The value — not building the wrong thing — is significant.
