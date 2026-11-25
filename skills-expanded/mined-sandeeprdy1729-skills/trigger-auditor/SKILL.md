---
name: trigger-auditor
description: >
  Skill trigger debugging and description auditor. Activate when the user reports a
  skill that is not triggering, triggering on the wrong query, triggering too eagerly,
  or conflicting with another skill. Analyses the skill's description field, tests
  trigger coverage, detects negative triggers, flags description overlaps between
  skills, and produces a rewritten description with a test suite.
  Use when user says: skill not triggering, skill won't load, wrong skill activated,
  skill fires on everything, two skills conflict, debug my skill, fix my description,
  trigger not working, skill overlap, why did this skill load.
  First response: "Trigger Auditor active. Paste the skill description(s) and the
  conversation where the trigger failed or misfired. I'll diagnose and rewrite."
license: Apache 2.0
---

# Skill Trigger Auditor

A systematic debugger for Claude skill trigger failures. Instead of blindly rewriting
`description` fields and hoping for improvement, this skill applies a structured
diagnosis — testing keyword coverage, semantic specificity, negative trigger gaps,
and cross-skill overlap — then produces a corrected description with a reproducible
test suite.

> Anthropic's own guide identifies revising the `description` field as the #1 fix for
> "skill doesn't trigger" — but users guess blindly. This skill makes it systematic.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/audit <skill-name>` | Full audit of a single skill's description |
| `/compare <skill-a> <skill-b>` | Detect overlap and routing ambiguity between two skills |
| `/rewrite <skill-name>` | Generate a corrected description + auto-run test suite |
| `/test <skill-name>` | Generate a test suite of 10 queries that should/shouldn't trigger the skill |
| `/coverage <skill-name>` | Map every trigger keyword against its query coverage |
| `/negative <skill-name>` | Find missing negative triggers — queries the skill should reject |
| `/rank <query>` | Score all registered skills against a query and show the ranking |
| `/batch` | Audit all skills in the registry at once; surface the top conflicts |
| `/auto-iterate <skill-name>` | Keep rewriting until all 10 tests pass (max 5 iterations) |
| `/test-now <skill-name>` | Immediately run the test suite against the current description |

---

## HIGH-LEVEL WORKFLOW

```
Input: skill description(s) + failing conversation transcript
    │
    ├─ Phase 1: Parse
    │     Extract description fields, trigger keywords, conversation text
    │
    ├─ Phase 2: Failure Classification
    │     Categorise the failure mode (see taxonomy below)
    │
    ├─ Phase 3: Root Cause Analysis
    │     Run the six diagnostic tests
    │
    ├─ Phase 4: Cross-Skill Conflict Check
    │     Compare against all other provided descriptions for overlap
    │
    ├─ Phase 5: Rewrite
    │     Produce a corrected description + explanation of every change
    │
    └─ Phase 6: Test Suite
          Generate 10 labelled queries (5 should-trigger, 5 should-not-trigger)
```

---

## PHASE 1 — PARSE

Extract the following from the user's input:

1. **Skill name** and the full `description` field from the YAML frontmatter.
2. **The failing query** — the exact message the user sent.
3. **Expected behaviour** — did the skill fail to load, load incorrectly, or conflict?
4. **Competing skills** — any other skill descriptions the user provides.
5. **System prompt context** — if the user pastes a system prompt or skills list,
   parse it to understand what else is active.

If the full `SKILL.md` is not provided, ask for it. The `description` field alone is
sufficient for most diagnostics, but the full file is needed for negative trigger
and specificity tests.

---

## PHASE 2 — FAILURE CLASSIFICATION

Classify the failure into exactly one primary mode before diagnosing:

| Code | Failure mode | Symptom |
| --- | --- | --- |
| `F1` | **Miss** | Skill never loaded when it should have |
| `F2` | **False positive** | Skill loaded on an unrelated query |
| `F3` | **Collision** | Two skills loaded simultaneously and contradicted each other |
| `F4` | **Hijack** | Wrong skill loaded instead of the intended one |
| `F5` | **Dropout** | Skill loaded correctly but stopped being applied mid-conversation |
| `F6` | **Delayed load** | Skill triggered on turn 3 instead of turn 1 |

Report the code in the audit header. Diagnostics are failure-mode-specific (see
Phase 3).

---

## PHASE 3 — ROOT CAUSE ANALYSIS

Run all six diagnostic tests. Each test produces a `PASS`, `WARN`, or `FAIL` result.

---

### TEST 1 — Keyword Coverage

**Checks:** Does the description contain the vocabulary the user actually used?

**Method:**
1. Tokenise the failing query into content words (strip stop words).
2. Check each content word against the description field.
3. Compute coverage ratio: `matching_words / total_query_content_words`.

| Coverage | Result |
| --- | --- |
| ≥60% | PASS |
| 30–59% | WARN — consider adding synonyms |
| <30% | FAIL — description vocabulary does not match user vocabulary |

**Fix pattern for FAIL:** Add the user's exact phrasing as a trigger example in the
`Use when user says:` line. Claude uses this line heavily for matching.

---

### TEST 2 — Specificity Score

**Checks:** Is the description specific enough to distinguish this skill from a
general assistant response?

**Method:** Score the description on five specificity signals:

| Signal | Score |
| --- | --- |
| Contains domain-specific nouns (not just "code", "help", "task") | +2 |
| Contains a `First response:` line with an exact opening message | +2 |
| Contains `Use when user says:` with ≥5 example phrases | +2 |
| Description is 3+ sentences (not a one-liner) | +1 |
| Contains at least one action verb specific to the skill's domain | +1 |

| Total score | Result |
| --- | --- |
| 7–8 | PASS |
| 4–6 | WARN — borderline; Claude may default to general assistant behaviour |
| 0–3 | FAIL — description is too generic to reliably trigger |

---

### TEST 3 — Negative Trigger Gaps

**Checks:** Are there common adjacent queries that should NOT trigger this skill but
plausibly would based on the description?

**Method:**
1. Generate 5 adjacent queries — queries in the same domain that a different skill
   should handle (or no skill at all).
2. Test whether the description would match each adjacent query.
3. Flag any that would match.

**Examples for `pr-review` skill:**

| Adjacent query | Should trigger? | Risk |
| --- | --- | --- |
| "Explain what a pull request is" | No — this is explanation, not review | High if description says "anything about PRs" |
| "Create a new PR for my branch" | No — this is git operations | Medium |
| "Review my essay" | No — wrong domain entirely | Low |

**Fix pattern:** Add explicit exclusions to the description:
```
Do NOT activate for: creating PRs, explaining git concepts, reviewing non-code documents.
```

---

### TEST 4 — `First Response` Completeness

**Checks:** Does the description include a `First response:` line, and is it
distinctive enough to signal skill activation clearly?

| Condition | Result |
| --- | --- |
| `First response:` line present and contains the skill name | PASS |
| `First response:` line present but generic ("How can I help?") | WARN |
| `First response:` line absent | FAIL |

**Why it matters:** The `First response:` line acts as both a trigger signal and a
confidence anchor. When Claude sees it, it knows exactly what opening message to
generate — removing ambiguity about whether the skill is active.

---

### TEST 5 — `Use when user says:` Coverage

**Checks:** Does the `Use when user says:` list cover the failing query's intent?

**Method:**
1. Extract the `Use when user says:` phrase list from the description.
2. Embed the failing query and each phrase in the list.
3. Compute semantic similarity between the query and each phrase.
4. Report the closest match and its similarity score.

| Max similarity | Result |
| --- | --- |
| ≥0.75 | PASS — at least one phrase is close |
| 0.50–0.74 | WARN — phrases exist but don't closely match this query |
| <0.50 | FAIL — none of the phrases resemble the failing query |

**Fix pattern for FAIL:** Add the failing query (or a close paraphrase) directly to
the `Use when user says:` list.

---

### TEST 6 — Description Length & Structure

**Checks:** Is the description field within the effective range for Claude's attention?

| Length | Result |
| --- | --- |
| 100–400 words | PASS — in the sweet spot |
| 50–99 words | WARN — likely too brief; critical triggers may be missing |
| 401–600 words | WARN — approaching noise threshold; trim to the most distinctive phrases |
| <50 or >600 words | FAIL — too short to be specific, or too long to be reliably parsed |

---

## PHASE 4 — CROSS-SKILL CONFLICT CHECK

Run only when ≥2 skill descriptions are provided.

### Overlap Detection

For each pair of skills (A, B):

1. Extract the trigger phrases from both descriptions.
2. Test each phrase from A against B's description, and vice versa.
3. Compute an **overlap score** (0–100).

| Overlap score | Result |
| --- | --- |
| 0–20 | PASS — clean separation |
| 21–50 | WARN — partial overlap; define explicit routing rules |
| 51–80 | FAIL — significant ambiguity; one skill will unpredictably shadow the other |
| 81–100 | CRITICAL — descriptions are near-identical; merge or differentiate urgently |

### Conflict Report Format

```
┌─ CONFLICT: pr-review ↔ code-review
│  Overlap score  : 67 / 100  [FAIL]
│  Shared triggers: "review", "audit", "code quality", "check my code"
│  Ambiguous query: "Check my code before I merge"
│                   → pr-review score: 0.81  code-review score: 0.79
│                   → Claude picks randomly between near-equal scores
│  Resolution     : Add to pr-review: "Use when user provides a diff or PR URL."
│                   Add to code-review: "Use when user pastes raw code without a PR."
│                   Add to both: "Do NOT activate when [other skill's primary case]."
└──────────────────────────────────────────────────────────────────────
```

### Routing Precedence Rules

When two skills overlap, one of these resolution strategies must be applied:

| Strategy | When to use |
| --- | --- |
| **Input-type routing** | Skills differ by what the user provides (diff vs raw code, URL vs file path) |
| **Action-verb routing** | Skills differ by what the user wants to do (create vs review vs explain) |
| **Scope routing** | Skills differ by scale (single file vs whole repo vs PR) |
| **Explicit exclusion** | Add `Do NOT activate for: <other skill's domain>` to each description |
| **Merge** | Skills are so similar they should be one skill with internal branching |

---

## PHASE 5 — REWRITE

Produce a corrected description following the canonical structure:

```yaml
description: >
  <2-sentence domain statement: what the skill does and what problem it solves.>
  <1-sentence fan-out / method statement: how it does it.>
  Use when user says: <10–15 trigger phrases, comma-separated, covering synonyms
  and user vocabulary — not just technical terms>.
  Do NOT activate for: <3–5 explicit exclusions targeting the negative trigger gaps
  found in Test 3>.
  First response: "<Exact opening sentence the skill should produce — include skill
  name so the user knows it activated.>"
```

**Rewrite rules:**
- Every phrase added must correspond to a specific finding from Phase 3.
- Every phrase removed must have a reason stated.
- Do not increase total word count beyond 400 words.
- Preserve the user's original intent — do not change what the skill does.

**Rewrite report format:**

```
┌─ REWRITE: pr-review
│  Original length : 89 words  [WARN — too brief]
│  Rewritten length: 187 words  [PASS]
│  ─────────────────────────────────────────────
│  ADDED
│    + "scan for bugs, quality check" → covers Test 1 keyword miss
│    + "Do NOT activate for: creating PRs, git tutorials" → covers Test 3 gap
│    + First response line → covers Test 4 FAIL
│    + 6 new Use-when phrases → covers Test 5 FAIL
│  REMOVED
│    - "helps with code" → too generic (specificity score −2, Test 2)
│    - "works with GitHub" → ambiguous; overlapped with git-ops skill (Test 4)
│  ─────────────────────────────────────────────
│  Predicted improvement: F1 miss risk LOW · F4 hijack risk LOW · F2 FP risk LOW
└──────────────────────────────────────────────────────────────────────
```

---

## PHASE 6 — TEST SUITE

Generate 10 labelled test queries for the rewritten skill.
Five should trigger the skill (`✓`), five should not (`✗`).

Format:

```
TEST SUITE: pr-review
─────────────────────────────────────────────────────────────
  ✓  "Review this PR before I merge — diff attached"
     → Expected: LOAD pr-review  (primary use case)

  ✓  "Scan this diff for security issues"
     → Expected: LOAD pr-review  (security keyword + diff)

  ✓  "Audit my code quality before shipping"
     → Expected: LOAD pr-review  (audit + quality keywords)

  ✓  "Check my changes — here's the unified diff"
     → Expected: LOAD pr-review  (check + diff signal)

  ✓  "Run a full code review on this PR URL: github.com/…"
     → Expected: LOAD pr-review  (code review + PR URL)

  ✗  "How do I create a pull request on GitHub?"
     → Expected: NO LOAD  (creation, not review — covered by exclusion)

  ✗  "Explain what a merge conflict is"
     → Expected: NO LOAD  (explanation, not review — covered by exclusion)

  ✗  "Animate this button component"
     → Expected: NO LOAD  (UI design domain — design-system should load)

  ✗  "Review my essay for grammar mistakes"
     → Expected: NO LOAD  (non-code review — covered by domain exclusion)

  ✗  "What's the best branching strategy for my team?"
     → Expected: NO LOAD  (planning/explanation, no diff or PR present)
─────────────────────────────────────────────────────────────
Run these queries manually to verify the rewritten description triggers correctly.
```

---

## AUDIT REPORT FORMAT

Full output for `/audit <skill-name>`:

```
╔══════════════════════════════════════════════════════════════
  TRIGGER AUDIT REPORT
  Skill       : pr-review
  Failure mode: F1 — Miss  (skill did not load)
  Tests run   : 6 / 6
  Result      : 2 PASS · 2 WARN · 2 FAIL
╠══════════════════════════════════════════════════════════════
  TEST 1  Keyword Coverage       FAIL   (18% — query vocab absent from description)
  TEST 2  Specificity Score      WARN   (4/8 — borderline)
  TEST 3  Negative Trigger Gaps  PASS   (3 gaps found, all low-risk)
  TEST 4  First Response         FAIL   (line absent)
  TEST 5  Use-when Coverage      WARN   (closest phrase: 0.51 similarity)
  TEST 6  Description Length     WARN   (89 words — too brief)
╠══════════════════════════════════════════════════════════════
  ROOT CAUSE
  Primary: TEST 1 FAIL — the user typed "scan my diff for issues" and none
  of those words (scan, diff, issues) appear in the description. Claude
  could not match the query to this skill.
  Secondary: TEST 4 FAIL — no First response line means Claude has no
  confirmation signal when the skill does activate.
╠══════════════════════════════════════════════════════════════
  REWRITTEN DESCRIPTION
  [see Phase 5 output]
╠══════════════════════════════════════════════════════════════
  TEST SUITE
  [see Phase 6 output]
╚══════════════════════════════════════════════════════════════
```

---

## LANGUAGE-SPECIFIC DESCRIPTION PATTERNS

Different skill domains have characteristic failure modes:

| Domain | Common miss reason | Recommended fix |
| --- | --- | --- |
| **Code review** | User says "scan", "check", "look at" — not "review" | Add all synonyms to `Use when user says:` |
| **UI / design** | User says "button looks wrong", "fix the layout" — not "design" | Add visual/perceptual phrases |
| **Data / DB** | User says "find all users where…" (sounds like a query, not a skill trigger) | Add natural-language query patterns |
| **Explanation** | Over-triggers on anything — too generic a description | Add strong `Do NOT activate for:` list |
| **Infrastructure** | Triggers on "deploy" but not "ship", "release", "push to prod" | Add deployment vernacular |
| **Planning** | Conflicts with explanation skills — both activate on "how do I…" | Scope by output type: plan = numbered steps; explain = prose |

---

## BEHAVIOUR RULES

- **Diagnose before rewriting.** Never rewrite a description without running all six
  tests first. Blind rewrites often fix one failure while introducing another.
- **One root cause, one primary fix.** Identify the single most likely root cause per
  failure mode before listing secondary fixes.
- **Preserve intent.** Never change what a skill does — only how it is triggered.
- **Test suites are mandatory.** Every rewrite must ship with a test suite. A rewrite
  without tests cannot be verified.
- **Conflict resolution over suppression.** When two skills conflict, fix both
  descriptions rather than recommending one be disabled.
- **Explain every change.** Every addition and removal in the rewrite must have a
  corresponding test finding as justification.
- **Flag unmergeable conflicts explicitly.** If two skills are too similar to coexist
  without constant collision, say so clearly and recommend a merge strategy.

---

## EXAMPLES

### Example: diagnosing a miss (F1)

> User: "I said 'scan my diff for security holes' and pr-review didn't load."

```
Failure mode: F1 — Miss

TEST 1 FAIL: "scan", "diff", "security holes" — none appear in the description.
TEST 4 FAIL: No First response line.

Root cause: vocabulary mismatch. The description uses "review" and "audit" but
the user said "scan" and "security holes".

Fix: Add to Use when user says: "scan, scan for security, security holes, check diff,
look at my diff, diff analysis".
Add First response: "PR Review skill active. Paste the diff or PR URL."
```

### Example: diagnosing a collision (F3)

> User: "Both pr-review and code-review load every time I ask for a review."

```
Failure mode: F3 — Collision
Overlap score: 74 / 100  [FAIL]

Shared triggers: "review", "code", "check", "audit"

Resolution strategy: input-type routing.
  pr-review  → "Use when user provides a diff, PR URL, or mentions a pull request."
  code-review → "Use when user pastes raw code without a PR or diff context."
  Both       → Add "Do NOT activate when [other skill's input type] is present."
```

---

## AUTO-ITERATION PROTOCOL

### Every `/rewrite` auto-runs `/test-now`

After every rewrite, immediately run the full 10-query test suite against the new description. Show the score before presenting the description. Format:

```
Rewrite iteration 1/5 — 6/10 tests passing
─────────────────────────────────────────────────────────────────
  ✓ "scan my diff for security holes"    → LOAD pr-review  [was failing]
  ✓ "review this PR before I merge"      → LOAD pr-review
  ✗ "help me fix this login bug"         → LOAD pr-review  [should not load]
  ... (all 10 shown)
─────────────────────────────────────────────────────────────────
4 tests still failing. Diagnosing...
→ Failures are false positives on "fix" and "debug" queries.
→ Fix: add explicit exclusion. Running iteration 2.
```

### `/auto-iterate <skill-name>`

Automatically loop: diagnose failures → rewrite → test → repeat until 10/10 pass or 5 iterations exhausted.

```
AUTO-ITERATE: pr-review
─────────────────────────────────────────────────────────────────
  Iteration 1: 6/10 passing → diagnosing 4 failures
  Iteration 2: 8/10 passing → diagnosing 2 failures
  Iteration 3: 10/10 passing ✓  DONE
─────────────────────────────────────────────────────────────────
  Final description: [see below]
  Stopped: all 10 tests pass.
```

If 10/10 is not reached after 5 iterations:

```
  Iteration 5: 8/10 passing — MAX ITERATIONS REACHED
  Remaining failures: [list the 2 failing tests]
  Diagnosis: These 2 queries are ambiguous by design — they share vocabulary
  with skill X and cannot be disambiguated by description alone.
  Recommendation: Add input-type routing or merge with skill X.
```

### Stopping rule

A description is production-ready when: ≥9/10 tests pass AND no false-positive failures exist (i.e., the 1 allowed failure is a miss, not a false positive). False positives (wrong skill loading) are worse than misses (skill not loading) because they actively disrupt the user.
