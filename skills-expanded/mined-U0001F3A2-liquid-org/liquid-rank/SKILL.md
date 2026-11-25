---
name: liquid-rank
description: >-
  Rank the available skills by RELEVANCE to the current task, on demand, using
  liquid-org's read-only hermes skill ranker. This is an EXPLICIT, OPT-IN
  selector you invoke WHEN you want help choosing the most relevant skill for
  what you're doing — it is NOT default, automatic skill selection, and it does
  NOT decide for you. Relevance here means SIGNATURE + CONTENT similarity
  (task-signature match plus lexical overlap with each SKILL.md): it is a
  retrieval/relevance ranking, NOT a measure of "learned skill quality",
  success, or reward. Trigger when you (or the user) say "which skill fits this",
  "rank the skills for this task", "what's the most relevant skill", "use
  liquid-rank", or you want a relevance-ordered shortlist before picking a skill
  to run. Do NOT treat its output as an instruction to auto-load the top skill —
  it is a suggestion you read and decide on.
---

# Rank skills by relevance for the current task (opt-in)

You have many skills available. When you want a relevance-ordered view of which
of them best fit the task at hand, run liquid-org's read-only ranker and read
its report. This is a **selector you choose to invoke**, not an automatic
default — nothing here changes which skill loads. You stay in control: the
ranker only surfaces a relevance ordering for you to consider.

## What this ranks (and what it does NOT)

- It ranks by **RELEVANCE only**: signature similarity (the task's inferred
  signature vs each skill's) plus content similarity (lexical overlap between
  the task text and each SKILL.md). Higher = more topically relevant.
- It is **NOT** a measure of learned skill quality, success rate, or reward.
  Do not read the ranking as "this skill is better"; read it as "this skill is
  more about this task".
- It is **read-only and preview-only**: it never prunes, archives, deletes,
  moves, or rewrites any skill. It only reads `SKILL.md` files and prints a
  ranked report.

## How to use it — EXECUTE the CLI (don't read it)

Run the ranker as a command, passing the current task as a single argument, and
read the printed ranked report. Do not paraphrase its internals — just run it:

```bash
python -m liquid_org.integrations.hermes_skill_ranker "<the task you are working on>"
```

(Requires the `liquid-org` package installed. Inside the liquid-org dev repo,
prefix with `uv run` so `uv` resolves the repo env: `uv run python -m ...`.)

It scans the configured hermes skills directory (default `~/.hermes/skills`),
ranks every `SKILL.md` by relevance to `<the task>`, and prints a table: per
skill a `sig` (signature-match) score, a `cont` (content-similarity) score, and
a combined relevance score, ordered most-relevant first.

- To limit the output to the top few: add `--top 5`.
- To point at a non-default skills directory: add `--skills-dir <path>`.

## What to do with the output

Read the top entries as a **relevance shortlist** and decide for yourself which
skill (if any) to use. Treat the order as a suggestion, not a command — there is
no "auto-pick the #1 skill" step, and the score is relevance, not quality. If
nothing ranks as clearly relevant, that itself is useful: it means no installed
skill is a strong fit for this task.
