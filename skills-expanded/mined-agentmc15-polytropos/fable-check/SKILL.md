---
name: fable-check
description: Decide whether a task is worth running on Fable 5.1 (vs Opus 5.5 / Sonnet 5.5) and how to run it optimally — effort level and task spec. Use when the user asks "should this run on Fable", "is Fable worth it", or how to get the most out of Fable.
---

# Fable 5.1 usage check

Read the plugin's `data/pricing.json` for current prices — resolve in order: `${CLAUDE_PLUGIN_ROOT}/data/pricing.json`; if that variable is unset, `../../data/pricing.json` relative to this SKILL.md; if neither exists, `references/pricing.json` beside this SKILL.md (a vendored snapshot — check its `cached_date` and flag prices as possibly stale if it is more than 60 days old). Derive the Fable-vs-Opus and Fable-vs-Sonnet cost ratios from those rates — never quote ratios from memory. Answer two questions about the task at hand: **is Fable worth it here**, and **if yes, how should it be run**.

## Is Fable worth it?

Fable 5.1's gains are on work *above* what the other current models can do. Route to Fable when the task is:

- **Long-horizon autonomous work** — overnight runs, large multi-file migrations, complex refactors expected to complete without human correction
- **Problems Opus 5.5 at higher effort already failed on** — a concrete failure is the strongest signal
- **Deep research / hardest reasoning** — multi-source synthesis, ambiguous problems needing judgment
- **Heavy parallel sub-agent orchestration** — Fable reliably sustains long-running sub-agent coordination

Do NOT route to Fable for: routine coding, tasks with well-known solutions, or anything Sonnet 5.5 or Opus 5.5 can handle at the needed effort.

## Caveats to surface every time Fable is recommended

- **Thinking is always on** — Fable 5.1 uses adaptive thinking; do not plan a no-thinking mode.

## How to run it optimally

1. **Full spec up front.** One well-specified first turn (goal, constraints, what "done" looks like) beats drip-fed instructions — Fable's long-horizon coherence comes from planning against a clear goal.
2. **Use the documented default as a baseline.** Fable 5.1 defaults to `high`; raise effort only when task evidence warrants it.
3. **De-prescribe migrated prompts.** Step-by-step scaffolding written for older models reduces Fable output quality — state the goal and constraints, not the steps.
4. **Let it delegate.** Encourage parallel sub-agents for independent workstreams; give it a memory surface (even a plain `.md` notes file) for multi-session work.
5. **Ground progress claims** on long runs: require it to verify claims against tool results before reporting.

## Standing recommendation for this setup

The user's working posture: **Opus 5.5 as daily driver; Fable 5.1 escalated per-portion, then back down.**

- **The default escalation path is `/polytropos:architect`**, not a session switch: Fable does the planning/meta-work once and emits an execution kit (task briefs, model-pinned subagents, guardrails, verification loops); `/polytropos:execute` then runs it on Opus/Sonnet at near-Fable quality. Blocked tasks escalate back to Fable one at a time. Use `/model fable` for a whole session only when the *entire* session is Fable-class work.
- Global default in `~/.claude/settings.json` should be `opus`; set effort per task, not globally.
