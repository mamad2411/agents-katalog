---
name: pickup
description: Pick up an issue that's ready for an agent and work it end-to-end. Reads the project issue tracker for issues carrying the AFK-ready triage label (default `ready-for-agent`), picks one, checks it's actually ready, then implements it via /tdd or /diagnose and opens a PR. Use when the user wants to grab an issue, work the next ready-for-agent ticket, start AFK work, or run /pickup. This is the "Work" entry point for the to-prd → to-issues → triage → pickup pipeline; it pairs with mattpocock/skills.
---

# Pickup

Grab a ready-for-agent issue and take it from the issue tracker to a pull request. This is the **Work** step of the pipeline: `to-prd` → `to-issues` → `triage` → **`pickup`** → ship.

`pickup` does **not** create or specify issues — `to-issues`/`to-prd` do that, and `triage` makes them ready. `pickup` does **not** invent its own implementation loop — it delegates to `/tdd` (enhancements) or `/diagnose` (bugs). Its job is selection, a readiness gate, and orchestration.

The issue tracker and triage label vocabulary should have been provided to you (in `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`, summarised under `## Agent skills` in CLAUDE.md/AGENTS.md). If they have not, run `/setup-matt-pocock-skills` first. Use the configured tracker and the configured label for the canonical `ready-for-agent` role — never assume GitHub or the literal string `ready-for-agent` without checking the config.

## Process

### 1. Resolve config

Read the project's issue-tracker conventions and triage-label mapping. Note the actual label string mapped to the `ready-for-agent` role — call it the **ready label** below.

### 2. Select an issue

Interpret the invocation argument:

- **An issue number / URL / path** → use that issue directly. Skip listing.
- **`next` or `auto`** → grab the best candidate without asking (AFK mode). "Best" = oldest open issue with the ready label and no unmet `Blocked by` dependency. If the best candidate is blocked, fall through to the next; if all are blocked, say so and stop.
- **No argument** → list open issues carrying the ready label (oldest first) with a one-line summary each, give a recommendation with reasoning, and let the user pick. If none carry the ready label, say so and suggest `/triage` to promote one.

Before committing to a blocked-looking issue, check its `Blocked by` section: confirm the referenced blockers are actually closed/merged. Don't start work whose prerequisites are unmet — surface the blocker and pick something else (or stop, in `auto` mode).

### 3. Readiness gate

Read the full issue: body, comments, labels, and any **Agent Brief** comment. The agent brief (not the original body) is the contract — see how `triage` writes them.

An issue is ready to work only if you can answer all of:

- Is there a concrete, testable set of acceptance criteria?
- Is the desired behaviour unambiguous (no open architectural/design decision, no "TBD")?
- Are scope boundaries clear enough that you won't gold-plate?
- Is it genuinely AFK — no human-only step (external access, a judgment call, manual device testing)?

If **any** answer is no, do **not** start coding. Stop and hand off to triage: tell the user exactly what's missing and recommend running `/triage <issue>` (or moving it to `ready-for-human` if it needs a person). Don't silently downgrade the issue's labels yourself — surface it and let the maintainer decide.

If the issue is ready, briefly confirm the plan (one or two lines: what you'll build, the category, the acceptance criteria you'll satisfy) before writing code.

### 4. Work it

Explore the codebase using the project's domain glossary, respecting ADRs in the area you're touching. Then delegate the implementation:

- **enhancement** → `/tdd`, one vertical slice at a time against the acceptance criteria
- **bug** → `/diagnose` to reproduce and fix, then a regression test

The issue's category role (`bug` / `enhancement`) tells you which. If unlabeled but ready, infer from the brief. Stay inside the issue's scope boundaries — anything you discover that's out of scope becomes a note for a follow-up issue, not extra work now.

### 5. Ship

When the acceptance criteria are met and tests pass:

- Verify before claiming done — run the tests/build and confirm the acceptance criteria, don't assert success on faith.
- Open a pull request that references the issue (e.g. `Closes #<n>`) and summarises what was built against the acceptance criteria. Follow the project's ship/PR conventions if it has them.
- In `auto` mode, do the work unattended but **confirm with the user before opening the PR** unless they've explicitly authorised fully unattended shipping.
- Post a short comment on the issue noting the PR. If the tracker is local markdown, append the PR/branch reference under the issue file's `## Comments` heading instead.

Do not close the issue yourself — let the merged PR (or the maintainer) do that.

## Notes

- One issue per `pickup` run. To work several, run it again — keeps each PR small and reviewable, matching the thin-vertical-slice philosophy of `to-issues`.
- If mid-work you discover the issue was not actually ready (a hidden decision surfaces), stop and kick back to triage rather than making the call yourself.
