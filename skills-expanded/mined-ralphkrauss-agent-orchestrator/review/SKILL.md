---
name: review
description: Session-scoped review of uncommitted changes against .agents/rules/ and the static checklist. Only reviews what was changed in THIS session (working tree diff), not the full branch. Use when user says "review", "check my changes", "review this", or wants a quick quality check before committing.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Review (Session-Scoped)

Lightweight review of uncommitted working tree changes only. Unlike `/review-pr` (which reviews the full branch vs main), this reviews only what's been modified in the current session — staged + unstaged changes.

## Instructions

### Step 1: Get Session Diff

```bash
git diff          # unstaged changes
git diff --cached # staged changes
git diff HEAD     # both combined
```

Use `git diff HEAD` as the scope. If the diff is empty, report "No uncommitted changes to review" and stop.

List changed files:
```bash
git diff HEAD --name-only
```

### Step 1b: Load Context

1. Get the current branch: `git branch --show-current`
2. Check if a context file exists at `contexts/{branch-name}/context.md`
   - If it exists, read it. This contains pre-curated research: critical path, must-read file manifest, external provider knowledge, internal architecture patterns, and test patterns.
   - Use this context to understand the intent behind the changes — it informs which documentation to cross-reference and which invariants are most critical to verify.
3. Check if a plan exists at `plans/{branch-name}/plan.md`
   - If it exists, read it and any sub-plans. The plan's Decisions, Scope, and Risks sections inform what the code should do — verify the diff matches intent, not just patterns.

### Step 2: Classify and Load Rules

1. Classify changed files into categories (Safety-critical, Domain, Integration, UI, Infrastructure, Tests, Config) — same categories as `/review-pr`
2. Enable **strict mode** if any safety-critical files are in the diff (money handling, irreversible mutations, regulated flows, etc.)
3. Load rules from `.agents/rules/` that match the changed file paths
4. Log: "Reviewing N files against .agents/rules/"

### Step 3: Check Against Rules + Checklist

For each relevant rule in `.agents/rules/`:
- Check if the diff exhibits any anti-pattern described in the rules
- If violation found: report with rule file, section, file, line, and the rule

If the project maintains a review checklist (e.g., `docs/reviewing/checklist.md`):
- Run only the dimensions relevant to the changed file categories
- Skip dimensions where no files match

**Severity rules:**
- Strict mode: any safety-critical invariant violation = Critical
- Test code exempt from strict mode

### Step 3b: Critical Documentation Validation

For each file in the diff that touches crucial logic (money/safety-critical flows, third-party integrations, domain state transitions, irreversible mutations):

1. **Identify the relevant documentation** — find the docs that describe how this code should behave (`docs/`, architecture notes, third-party spec files, `AGENTS.md` sections)
2. **Read the documentation** — do not rely on memory or pattern-matching. Actually read the doc.
3. **Verify correctness against the doc** — trace the code path and confirm it implements what the documentation specifies. Check:
   - Are the method calls correct? (correct method on the correct service, correct event type)
   - Are the parameters in the right order with the right types?
   - Does the flow match the documented sequence?
   - Are edge cases from the documentation handled?
4. **Report discrepancies** as Critical findings with evidence from both the code and the doc

This step is what separates a mechanical pattern check from a real review. Pattern compliance does not prove correctness — a handler can follow every naming convention and still call the wrong service method.

### Step 4: Save Artifact

```bash
BRANCH=$(git branch --show-current)
mkdir -p plans/$BRANCH/reviews
ARTIFACT=plans/$BRANCH/reviews/review-$(date +%Y-%m-%d).md
```

If file exists for today, append counter: `review-2026-04-01-2.md`

Write the review output to `$ARTIFACT` before presenting. This creates a durable record alongside Codex review artifacts.

### Step 5: Present Findings

```
## Session Review: N files, M lessons loaded

### Findings

| # | Severity | Rule | File | Issue |
|---|----------|------|------|-------|
| 1 | critical | rules/safety.md § Idempotency | src/service/handler.ext:42 | Idempotency check after mutation |

### 1. RULE-001: Idempotency check after mutation (critical)
**File:** `src/service/handler.ext:42`
**Issue:** {description}
**Fix:** {recommendation}

---

No findings? → "Session changes look clean. Ready to commit."
```

For each Critical/Important finding, ask: **fix / defer / dismiss**

### Step 6: Knowledge Capture — Rule Check

Check if any findings represent patterns not covered by existing `.agents/rules/` files. If a finding is reusable (not a one-off typo or naming nit), suggest `/create-rule`. Provide:
- The pattern (rule text)
- The anti-pattern (the bad code that was caught, with example)
- The evidence (source: the session review finding that surfaced it)
- Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

## Critical Rules

- **Session-scoped ONLY** — review `git diff HEAD`, not `git diff main...HEAD`. This is about what you just changed, not the full branch.
- **No auto-fixes** — present findings only. The user decides.
- **No build/test runs** — this is a quick check, not a full self-review. Suggest running tests if logic was changed.
- **Evidence-based** — every finding cites file:line and the rule file/section.
- **Fast** — this should complete in under 30 seconds for typical changes.
