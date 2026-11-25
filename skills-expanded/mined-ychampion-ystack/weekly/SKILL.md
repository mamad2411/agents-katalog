---
name: weekly
description: >-
  Weekly founder review. Measures the week from evidence (conversations, pilots, payments, what shipped
  for whom) and from the founder's agent prompt history (building vs tooling vs customer time), applies
  commit / sharpen / kill to each idea, and sets next week's single bottleneck. Use once a week (Monday),
  or when the user asks "how are we doing", "what should I focus on" or for a weekly review.
---

# /weekly: one honest page about the week

## The founder hub

This skill reads and writes a **founder hub**: one folder holding the startup's truth.

- **Location:** the `FOUNDER_HUB` environment variable, default `~/founder`. Below, `<hub>` means that
  folder.
- **Files this skill uses:**

| File | What it holds |
|---|---|
| `<hub>/README.md` | The decision rule and evidence rules. If missing, use the defaults below |
| `<hub>/bottleneck.md` | The current bet, this week's single bottleneck, the goal and its deadline. This skill rewrites it |
| `<hub>/ideas.md` | A table of candidate ideas: one line, who pays, evidence so far, status |
| `<hub>/evidence/` | One or more files per idea: conversation logs, prospects, pipeline, payments, metrics |
| `<hub>/weekly/<YYYY-MM-DD>.md` | The weekly reviews this skill writes |

**If the hub or a file is missing,** say so and offer to create the minimal structure: the folder,
`README.md` with the rules below, an empty `bottleneck.md` (current bet, bottleneck, goal, deadline),
`ideas.md` with a table header (idea, one line, who pays, evidence so far, status), and empty
`evidence/` and `weekly/`. An empty hub still gets a review: it says the week produced no evidence.
Never fail silently.

**Default decision rule:** commit when at least 3 target users show strong pull (a pilot, real data or
access, payment, a letter of intent); sharpen when the pain is real but the framing or buyer is wrong;
kill after about 15 targeted conversations with no strong pull. Compliments and "interesting" don't
count. **Default evidence rule:** only what real people said or did, dated and sourced.

Read `bottleneck.md`, `ideas.md` and every file in `evidence/`.

## 1. Measure the week's attention from prompt history (optional)

```bash
python <this skill's folder>/scripts/attention.py 7
```

It reads Claude Code's `~/.claude/history.jsonl` and Codex's `~/.codex/history.jsonl` if they exist
(pass other history files as extra arguments) and prints a keyword-based split: customer/selling,
fundraising, tooling/meta, fixing, building/other, plus the projects touched (Claude Code only). It's a
heuristic, about 80% accurate; report it as a rough split. If no history is found, or the harness keeps
none, skip this section and say so.

## 2. Write `weekly/<YYYY-MM-DD>.md`

- **Evidence this week:** conversations held; new strong-pull signals (pilot, data access, payment,
  letter of intent); sign-ups and usage; revenue. Numbers and names, from the evidence files only.
- **Shipped:** what shipped, and for which named user. Work that shipped with no user attached is listed
  separately.
- **Attention:** the prompt-history split and the projects touched. Call out tooling/meta above about
  15%, and any new project started.
- **Per idea:** commit / sharpen / keep testing / kill, by the decision rule, with the reason. Update
  `ideas.md`.
- **Next week's single bottleneck:** one sentence, plus 3 concrete actions and what "done" looks like.

## 3. Update `bottleneck.md`

Rewrite it to match: current bet, the new bottleneck, goal, deadline. Keep any scope note the founder
wrote there (for example which projects the hub does not govern). Then show the user the page, briefly.
Be direct and specific. Don't cushion a zero.
