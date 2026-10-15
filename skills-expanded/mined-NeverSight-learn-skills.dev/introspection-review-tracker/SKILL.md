---
name: introspection-review-tracker
description: >
  Reference documentation for the automated ReviewOutcomeTracker hook that persists
  adversarial code review findings as self_assessment memories. The hook fires
  automatically after every review — no manual steps required. This skill documents
  the mapping from severity tiers to error categories and the content format.
  Triggers on: "review outcome", "track findings", "record review",
  "self_assessment".
license: MIT
---

# Introspection Review Tracker — Reference Documentation

This skill is **reference documentation** for the automated review outcome persistence hook. The `llmem track-review` CLI command fires automatically after every adversarial code review, creating `self_assessment` memories without requiring manual agent intervention. This skill documents how the hook works, the severity-to-category mapping, and the content format.

## How Persistence Works

Persistence happens **mechanically** via `llmem track-review` (CLI). The agent must run this command after every adversarial code review — it is not optional.

### CLI: `llmem track-review`

The primary mechanism. Run after every review:

```bash
# For a review with findings (batch mode):
llmem track-review --finding-file /tmp/review-findings.json --context "handler.py"

# For a single finding:
llmem track-review --category NULL_SAFETY --what-happened "missing null check" --context "handler.py:42" --severity Required --caught-by self-review

# For a clean review (no findings):
llmem track-review --context "handler.py"

# See categories for a severity tier:
llmem suggest-categories Required
```

The `--finding-file` expects a JSON array of finding objects, each with `category`, `what_happened`, and optional `severity` keys.

### Python API

The Python API for programmatic review outcome tracking is planned but not yet implemented. Use the `llmem track-review` CLI command as the primary interface. Once available, the API will follow this pattern:

```python
from llmem.store import MemoryStore

store = MemoryStore(db_path=db_path)

# Programmatic tracking will mirror the CLI:
# - Single finding → one self_assessment memory
# - Batch findings → one memory per finding
# - Clean review → REVIEW_PASSED memory
# - Category suggestions → via llmem/taxonomy.py constants
```

## Verification

After an adversarial code review completes, verify that the post-review command was run:

1. Check that at least one `self_assessment` memory was created:
   ```bash
   llmem search "review_tracker" --type self_assessment
   ```

2. For each finding, confirm the category matches the severity tier mapping below.

3. For clean reviews, confirm one `REVIEW_PASSED` memory with outcomes "all clear".

## When This Skill Is Used

- **After every adversarial code review completion** — the hook must be run mechanically.
- **To verify** that the hook ran correctly (see Verification above).
- **As reference** for understanding the severity-to-category mapping and content format.

## Severity-to-Category Mapping

The `REVIEW_SEVERITY_TAXONOMY` constant in `llmem/taxonomy.py` maps each severity tier to applicable error taxonomy categories. The `llmem suggest-categories` CLI command uses this mapping directly.

| Severity Tier | Applicable Categories | Guidance |
|---|---|---|
| Blocking | AUTH_BYPASS, RACE_CONDITION, DATA_INTEGRITY | Security holes, data corruption risks, logic errors |
| Required | NULL_SAFETY, ERROR_HANDLING, MISSING_VERIFICATION, EDGE_CASE | Quality gaps — slop, missing safety checks, unhandled cases |
| Strong Suggestions | PERFORMANCE, DESIGN | Suboptimal approaches, missing tests, unclear intent |
| Noted | OFF_BY_ONE | Minor style issues, small boundary errors |
| Passed | REVIEW_PASSED | Clean review with no findings — positive outcome |

These mappings are advisory — the agent should pick the most meaningful category for the actual finding, not follow them mechanically. A Required-tier finding about performance might still map to PERFORMANCE rather than NULL_SAFETY. Note that the reviewer's tier name is "Strong Suggestions" (not just "Suggestions"); the taxonomy key matches this exactly.

## Content Format

Memories created by `llmem track-review` use the `SELF_ASSESSMENT_FIELDS` format from `llmem/taxonomy.py:29-39`, ensuring format parity with the `llmem introspect` manual mode:

```
Category: <ERROR_TAXONOMY category>
Context: <file:line or task identifier>
What_happened: <behavioral description>
Outcomes: <results or "all clear" for clean reviews>
What_caught_it: <how discovered, e.g. "self-review">
Estimates_vs_actual: <optional>
Recurring: <"yes" or "no">
Proposed_update: <optional>
Iteration_count: <optional integer>
```

## Key References

- **CLI command**: `llmem track-review` — the mechanical post-review hook
- **CLI command**: `llmem suggest-categories` — list categories for a severity tier
- **Error taxonomy categories**: `llmem/taxonomy.py:3-15` → `ERROR_TAXONOMY`
- **Severity mapping**: `llmem/taxonomy.py:21-27` → `REVIEW_SEVERITY_TAXONOMY`
- **Self-assessment fields**: `llmem/taxonomy.py:29-39` → `SELF_ASSESSMENT_FIELDS`
- **Reviewer severity tiers**: Defined by the adversarial review skill (e.g., Blocking, Required, Strong Suggestions, Noted, Passed) — see your review skill's Severity Tiers section
- **llmem introspect command**: `skills/llmem/SKILL.md` (manual and automatic modes)
