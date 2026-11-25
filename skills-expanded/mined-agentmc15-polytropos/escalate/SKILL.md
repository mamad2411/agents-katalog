---
name: escalate
description: Run one task on the cheapest sufficient model behind a machine-checkable success check, and automatically escalate to a Fable 5.1 subagent (carrying the failure evidence) only if the check fails. Use when the user wants "try it cheap first, fall back to Fable if it doesn't work", an auto-escalating / verify-gated dispatch, or "have Opus attempt it and call Fable if needed".
---

# Verify-gated escalation

You run ONE task through a cost-ascending ladder of models, promoting to the next tier **only when a check fails** — so Fable 5.1 is spent on genuine difficulty, never on routine work. You are the orchestrator; you stay on the session model and dispatch attempts as subagents so you can grade them with fresh eyes.

**The constraint that shapes everything:** nothing can switch the *main session's* model — only the user, via `/model`. "Opus checks, then calls Fable automatically" is therefore always: the orchestrator dispatches a subagent with the Agent tool's `model` parameter (`sonnet`/`opus`/`fable`), runs the verify command itself, and promotes on failure. There is no smaller/cheaper Fable model — the cheaper *way to run Fable* is lower effort and narrower scope (see Step 4).

## Step 0 — Establish the trigger (the verify command)

Automatic escalation needs a failing check to fire on. Before dispatching anything, pin a **machine-checkable success condition** for the task: a test command, a build, a lint, a `curl` + grep, a script that exits non-zero on failure. State it explicitly.

- If the task already implies one (a failing test, "make X pass"), use it.
- If it doesn't, derive the cheapest sufficient check and say what you chose.
- If the task genuinely has no checkable outcome (open-ended writing, judgment calls), say so plainly: automatic escalation can't trigger reliably here. Offer the fallback — attempt on the cheaper model, and escalate on the subagent *reporting blocked* or on your own adversarial read, not on a green check. Don't pretend a vibe is a verify.

## Step 1 — Pick the first (cheapest sufficient) tier

Default to the **cheapest model you'd actually trust for this task**, not the session model by reflex. Use `/route`'s framing if unsure; typically the sonnet tier (Sonnet 5.5 today) for routine coding/edits, Opus 5.5 for multi-file or harder reasoning. This is the tier you're betting can do it without Fable. Read prices only if the user asks for a cost figure — resolve `data/pricing.json` via `${CLAUDE_PLUGIN_ROOT}/data/pricing.json`, falling back to `../../data/pricing.json` relative to this SKILL.md — and never quote rates from memory.

## Step 2 — First attempt

Dispatch a subagent at the Step 1 model with a **self-contained brief**: the task, the relevant context (the subagent sees none of this conversation), and the verify command with an instruction to run it and report its output. Keep the brief tight; don't pre-solve it.

## Step 3 — Verify independently, then decide

Run the verify command **yourself**, from the right working directory. The subagent's claim of success is not evidence.

- **Passes** → done. Relay the result and note it never needed Fable.
- **Fails** → retry once on the *same* model, handing the subagent the exact failure output — cheap attempts often just need to see the error. Re-verify.
- **Fails again** → escalate (Step 4).

## Step 4 — Escalate to Fable 5.1, cheaply

Dispatch a subagent with `model: fable` carrying **only** what it needs: the task, the verify command, and the evidence from both failed attempts (what was tried, what the check reported). Ask it to either make the check pass or explain precisely why the task isn't doable as specified.

Two cost levers, in order of what you can actually control at dispatch:
- **Scope (primary, always available): hand it the diagnosis, not a blank re-attempt.** The failure evidence is what makes the Fable hop short — this is the lever you fully control from the orchestrator, so lean on it.
- **Effort (only where the invocation exposes it): prefer `medium`.** Fable at `medium` often beats older models at `max`, the real "cheaper Fable" — but the Agent tool takes only a `model` parameter, not an effort level, so a plain subagent dispatch runs at the default. Apply this lever only in a context that supports per-agent effort (e.g. a workflow step, or the user running `/model fable` at a chosen effort); otherwise rely on scope. If a `medium` hop is available and still fails the check, step up to `high`/`xhigh`.

Re-verify Fable's output yourself. If it passes, relay it. If even Fable fails, stop and report honestly — what each tier tried, the final check output, and your read on whether the task is mis-specified. Do not keep burning Fable effort past `xhigh`.


## Cost posture

In **subscription** mode the marginal dollar cost of the Fable hop is zero; the cost is rate-limit burn, so the effort/scope levers still matter. In **api** mode the whole point is that Fable runs only on the fraction of tasks the cheaper tier failed — report roughly what fraction escalated so the user can see the ladder paying off. This is the per-task sibling of `/polytropos:execute`'s blocked-task escalation valve; for multi-task work, prefer a kit (`/polytropos:architect`) over calling this in a loop.

## Optional context travel

When an explicit repository/kit/assignment and authorized startup config are supplied, use the native `context-travel` skill and read `${CLAUDE_PLUGIN_ROOT}/docs/CONTEXT-TRAVEL-SURFACES.md` (or resolve relative to the skill file) on demand for a bounded recovery brief. Treat missing, stale, partial, or refused context as advisory; retain this workflow's authoritative sources, policy, pricing, permission, and mandatory verification rules. If no authorized context transport is available, continue this workflow and report context unavailable.
