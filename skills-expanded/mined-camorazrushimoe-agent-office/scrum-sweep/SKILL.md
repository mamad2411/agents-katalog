---
name: scrum-sweep
description: "Scrum Master's GitHub sweep — collect repo activity + open issues/PRs (last N days), triage issues into buckets (bug/feature/tech-debt/performance/...), propose GitHub labels, and update the portfolio memory. Use when asked for a project-status sweep/обзор/пробег: 'сделай пробег', 'sweep', 'статус проектов', 'что происходит на фабрике', 'какие проекты активны', 'разбери issues'."
version: 1.0.0
author: local
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [agent-office, scrum-master, github, sweep, triage, portfolio, issues]
prerequisites:
  commands: [python3]
---

# Scrum Sweep

The Scrum Master's morning routine: sweep GitHub for what's moving, triage the
inbox, and keep the **portfolio** (memory of active projects) in order.

## When to use

- Every morning (or whenever the human asks "сделай пробег", "sweep", "статус
  проектов", "что происходит").
- When the human wants to know which projects are active and what's in flight.

## How to sweep

1. Run the collector:

   ```bash
   python3 /opt/data/skills/agent-office/scrum-sweep/sweep.py --days 7
   ```

   (or `--json` for structured data). **Do not** prefix it with
   `GITHUB_TOKEN=$GITHUB_TOKEN`: Hermes deliberately strips `GITHUB_TOKEN` /
   `GH_TOKEN` from tool subprocess environments, so that variable is always
   empty for you. The script resolves the token itself from the factory's
   single source of truth (`$TOKENS_FILE`, mounted read-only). If it exits with
   "No GitHub token", the tokens file or `/opt/office-lib` is not mounted —
   report that instead of falling back to the unauthenticated API (60 req/h,
   public repos only), which silently gives an incomplete picture.

   It lists the org's repos grouped by activity — active (pushed in the
   window), quiet (open issues but no push), silent — with each repo's open
   issues and their labels.

2. **Read the portfolio** (memory): `/opt/data/portfolio.yaml`. It records which
   projects you already track, their stage, and their tags.

## Analysis (the value-add)

From the sweep output, produce a short summary answering:

- **Which projects are active** — repos pushed/worked in the last 7 days.
- **What's in flight** — open PRs and the issues being worked.
- **What's stale** — repos with open issues but no recent activity.

## Triage / classification

For repos with a pile of untriaged issues, classify each issue into buckets and
**propose** GitHub labels (do NOT apply them yourself without the human's OK):

| Label | Meaning |
|-------|---------|
| `bug` | something is broken / wrong behaviour |
| `feature` | new functionality / enhancement |
| `tech-debt` | refactor, cleanup, "make it maintainable" |
| `performance` | speed / resource / latency problems |
| `docs` | documentation |
| `question` | needs clarification before any work |

Group and report by bucket, e.g. *"spaced-bro: 6 bugs, 2 performance, 4
tech-debt — suggest labelling and batching the bugs for a fix sprint."*

## Portfolio update

After the sweep, update `/opt/data/portfolio.yaml`:

- Add repos that became active; mark repos that went quiet as `stage: parked`
  (or keep them, with `last_activity` updated).
- Set/refresh `stage` per project: `research | spec | implementation | review |
  done | parked`.
- Keep `tags` reflecting the buckets you triaged.

The portfolio is the durable memory — do not rely on the conversation context
to remember which projects matter.

## Output / summary format

Deliver a compact Telegram-friendly summary to the human (via the external
Hermes agent or directly):

```
🧹 Утренний пробег — <дата>
🟢 Активные: spaced-bro (3 issues · 2 PR), club27 (…)
🟡 Заглохшие: board (12 issues)
Триаж: spaced-bro → 6 bug / 2 perf / 4 tech-debt. Предлагаю завести лейблы
и отправить 6 bug пачкой в dev-crew.
```

## Rules

- Labels are **proposed first, applied after the human approves**.
- The portfolio is updated every sweep — it's the source of "what's active".
- Consult other agents (architect, staff-engineer) if an issue's nature is
  unclear, but you can decide on your own.
- Never push to `main` / merge PRs while sweeping — this skill is read + triage
  only. Code changes go through the normal PR flow (`docs/github-workflow.md`).
