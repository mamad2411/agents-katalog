---
name: from-roadmap
description: Pull the next actionable insight from the vault work queue (active/triage, unblocked, best impact-vs-effort) and propose its execution. Use when the user says "/from-roadmap", "what should I work on", "next item".
---

# from-roadmap — what to do next

Answers "what now?" from the vault itself: frontmatter is the queue.

## Task

1. **Scan `<vault>/insights/`** (cheap: frontmatter only) for candidates:
   `status` in {active, triage} — terminal statuses are out.
2. **Filter to unblocked**: every slug in `depends_on` must already be
   implemented/closed; otherwise the item is blocked (report it as such).
3. **Rank** by impact (high first), then effort (low first), then risk (low
   first). `next_step` non-empty is a strong signal of readiness.
4. **Propose the top item**: one-paragraph summary (problem, recommendation,
   scores, next_step) + up to 2 runners-up as one-liners.
5. On the user's "go": hand off to `execute-insight` (insights) or `implement`
   (if it was promoted to a spec). Don't start work without the go.

## Rules

- Read frontmatter, not bodies, until one item is chosen (context budget).
- Empty queue → say so and suggest `discovery` or `discover-standards` to
  generate candidates.
- Never invent priorities; the frontmatter scores are the truth.
