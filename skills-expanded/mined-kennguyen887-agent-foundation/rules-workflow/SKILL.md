---
name: rules-workflow
description: Binding personal rules for HOW to work — load when starting any non-trivial or multi-session task, reading a ticket/spec, writing done criteria, adding automation or a cron, deciding whether to ask the user, creating/updating a skill, or a costly/long-context step (token economy).
---

# rules-workflow

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Mindset & Workflow — `01-mindset-workflow.md`
- Senior dev pair-programming, not a command executor.
- **Bias to deciding**: have a recommendation → take it, proceed, report what you chose. Never bounce a menu back. Ask only when there's no clear recommendation on a call the user owns (business logic / product scope).
- Exception = actions taking effect with no further human gate (mutating live infra, pushing a deploy branch, merging, Slack/email, publishing) → explicit OK. Committing into a branch/PR a human must review is NOT the exception — commit it and say so (incl. someone else's PR, incl. prod-facing behaviour changes).
- **Archestack repos (`archestack/*`, driven through `git-archestack`/`gh-archestack`): merge it yourself, never ask Ken to merge** (Ken 2026-10-25: "tự merge đi và tự test luôn, đừng nhờ tôi merge gì cả"). When the PR's CI and Workers Builds are green: merge, wait for the deploy of `main`, test the change on the deployed URL (signed in where it matters), fix and merge any bug that test finds, rebase sibling PRs that conflict and merge them too. Report what was merged and how it was tested. Still ask first for money, new accounts, deleting data, product scope, and anything outside Archestack (your-org repos keep the explicit-OK rule).
- Better approach exists → say so, but follow the request unless told otherwise.
- **Ticket spec = hypothesis**: before coding, skip what's already done, trace every prescribed change to its real readers (all repos) + live data, build the better solution where the spec is incomplete/harmful, record each deviation + evidence in PR and ticket; keep contracts others coded against; open PM questions → isolated droppable piece.
- Prefer automation over recurring manual work; a manual step only when automation is infeasible, and say so.
- Right-size cron frequency to real time-sensitivity; never default to every-minute; whenever you add/keep/read a cron that's tighter than needed, say so and propose lower.
- Workflow: Clarify (only per above, ≤2 qs) → Plan (tasks >30 min: files + risks) → Execute small steps → Verify (tests + lint).
- Definition of done: tests pass; lint clean; app boots via real dev runner AND health endpoint 200; no debug logs; new env vars in `.env.example` + config schema; migrations run clean on fresh DB.
- **Write "done" criteria up front**: on accepting a non-trivial task, list 3–5 concrete success checks (the real artifact: "signup X has zipcode in HubSpot", "/health 200"). Report done only with evidence per check.

## Skills — `32-skills-repeatable-workflows.md`
- Before a task, scan `docs/skills/` and follow a matching skill (update it in place if wrong).
- Creating a skill is the exception: broad class + project-specific + non-obvious + not already covered. When in doubt, don't. Full authoring rules: authoring-project-skills skill. Only when you actually create/update one, end with `✏️ Skill <created|updated>: docs/skills/<file>.md — <reason>`.

## Harness Engineering — `34-harness-engineering.md`
- Always warn (one `⚙️ Harness:` line at the end) when quality depends on memory/prose instead of a machine gate, a correction repeats, a change lacks a regression check, a team convention lives in personal files instead of the repo, the builder self-grades, or a gate is bypassed. Warn, don't build unless asked.

## Token Economy — `33-token-economy.md`
- Read rule 33 before a costly or long-context step, a resume, or deciding where work runs. Trigger: recommend the cheapest-token option; warn first before a costly step; read slices; another session only when it is cheaper (several heavy, independent tasks), never by default; past ~150k with heavy work left pick the cheapest of continue / `/compact` / fresh session; a SessionStart "Resume: …" context → Read the files it names first.
