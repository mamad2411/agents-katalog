---
name: sprint-day
risk_tier: side-effectful-bounded
description: >
  Plan the owner's day as ultradian sprint blocks on their measured curve, then check at each block boundary whether the work happened by looking at what it produced. Three modes: `plan` writes the day ledger and registers its own boundary check-ins, `check` resolves one block against declared evidence, `close` reports the day and appends the rollup. Use when the user asks for their sprint day, their block plan, an accountability check, or invokes /sprint-day. Also the skill the scheduled sprint tasks invoke.
---

# Sprint day

An accountability agent that does not ask whether you did the work. It looks at what the work produced, and only asks about what the artifacts could not answer.

That distinction is the whole reason this exists. Every focus product on the market records a self-report: at the end of the day you say whether you did it, and the coach then reasons off your say-so. A complete record of a claim is not evidence of work. It is the same failure this shop published a paper about, wearing a habit tracker's clothes.

Read these before you start, and follow them rather than the summaries here:

- `${CLAUDE_PLUGIN_ROOT}/skills/sprint-day/references/ultradian-ledger.md`: the `ultradian` config block, the ledger schema, and the three block statuses
- `${CLAUDE_PLUGIN_ROOT}/references/briefing-config.md`: every other person-specific value
- `${CLAUDE_PLUGIN_ROOT}/references/source-discipline.md`: the three source states, which apply here unchanged

## Unattended by default

Every mode is built to run with nobody watching. Do not ask clarifying questions in a scheduled run. Resolve from the config, make the honest choice where the config is silent, and put anything unresolved in the day's caveats. `check` is the one mode that may address the owner, and it does that by leaving a question in its report, not by blocking on an answer.

## The one rule

**A block reaches `verified` only from an artifact whose own timestamp falls inside the block window.** Not from the owner saying so, not from a ticket being in the right column, not from a plausible inference. The owner answering produces `self-reported`. Nothing found and nobody answering produces `unknown`. There is no config option that softens this, and a run that cannot tell the three apart reports `unknown` rather than guessing upward.

---

## Mode: plan

Runs once in the morning. Normally invoked at the end of the 07:00 commitment-calendar task, which has already resolved today's commitments; use those rather than sweeping again. When invoked standalone, pull today's calendar only.

1. **Anchor the date.** Run `date`. Resolve today in `owner.timezone`, never from the sandbox's UTC date and never from a filename.
2. **Load the curve** from `ultradian` in the config, then run `check_curve()` from the block planner before anything else. It raises when `curveSource` is empty and when the bands are still the documented fixture. Both are hard stops, and neither is overridable. A curve nobody can attribute is not a measurement, and a config that was never filled in looks exactly like one that was. An hour the survey did not measure is `unmeasured`, which ranks above a measured dip and below a measured peak. Never relabel it `low` to make the curve look complete.
3. **Collect today's commitments.** Each needs an id, a title, a weight of `deep` or `shallow`, a source, and an `evidence.expect` list naming the surface and query that would prove it. A commitment with no expectable evidence is still planned, and its `expect` is an empty list, which is what forces it to end the day `self-reported` at best. That is honest and it is the point.
4. **Collect busy time** from today's calendar events. A block may not sit inside a meeting.
5. **Place the blocks** with `${CLAUDE_PLUGIN_ROOT}/skills/sprint-day/scripts/plan_blocks.py`, feeding it `{ultradian, commitments, busy}` on stdin. Do not do this arithmetic yourself. The script reserves the frog window first and reports anything it could not place.
6. **Write the ledger** to `sprint-ledger/YYYY-MM-DD.json` under the config directory in the vault. In a scheduled run the vault is not mounted, so write through the Drive API. Refuse to overwrite a ledger for today that already carries a `checkedAt` on any block; report the collision instead.
7. **Register the check-ins.** One `mcp__claude-code-remote__create_trigger` per block that has a commitment, `run_once_at` its end time, plus one close task at the end of the frog window. Prompt bodies are in `${CLAUDE_PLUGIN_ROOT}/skills/sprint-day/references/sprint-trigger-prompts.md`, used verbatim. Write each returned `trigger_id` into its block. On a re-plan, delete the ids the ledger already holds before registering new ones, and verify each with `list_triggers` first rather than trusting the stored id.
8. **Run `curve_conflicts()`** and carry every sentence it returns into the ledger's caveats and into the report. A meal window sitting on the frog window is the headline, not a footnote. Never resolve a conflict by moving the block quietly: state it and let the owner choose.
9. **Report** in one line: block count, how many carry a commitment, how many check-ins registered, and anything unplaced. Lead with a conflict if there is one.

## Mode: check

Fires at one block boundary. It knows nothing except what it can read.

1. **Anchor the date**, open today's ledger, and stop if it is missing or unparseable. Do not reconstruct the day.
2. **Resolve the block by its start time**, not by position in the array. A ledger rewritten mid-day renumbers.
3. **Query only that block's `evidence.expect`.** Nothing wider. A wide sweep here finds artifacts from other blocks and credits them to this one, which is precisely the link defect this agent exists to catch.
4. **Judge.** An artifact whose timestamp falls inside `[start, end]` sets `verified`, and the artifact's identifier, surface and timestamp are written into `verifiedBy`. A boolean is not enough: a proof nobody can re-check is not a proof. Outside the window is not a match, and it goes in the note.
5. **Write back** status, `checkedAt`, `verifiedBy`, and any note. Record each evidence surface's state in the ledger's source map, three-state.
6. **Report** one line. When the status is not `verified`, end with the single question the artifacts could not answer. The owner's later answer, if it comes, sets `self-reported`.

## Mode: close

Fires at the end of the frog window.

1. Open the ledger. Count blocks planned, `verified`, `self-reported`, `unknown`, `open`.
2. Email one summary to `owner.email`, email-safe per the house rules, naming the artifact behind each verified block and the question left open on every other. Never split it across messages.
3. Name every evidence source that was `unavailable` or `not checked`. An unread surface is never reported as a quiet one.
4. Append one row to `sprint-ledger/_rollup.json` carrying the date, the four counts, and the ledger filename the row came from. A rollup row whose ledger is gone is unfalsifiable, so the filename travels with it.
5. Report one line, and say plainly whether the email sent.

---

## What earns `verified`

The bar is deliberately narrow, because the number this agent produces is only worth having if it is hard to inflate:

- a commit, PR review, or release on a declared repo, authored by the owner, timestamped inside the window
- a file created or modified at a declared vault path inside the window
- a message sent from the owner's account inside the window
- a URL that did not resolve before the block and resolves after it

Anything else is evidence of activity, not of this block's commitment, and it belongs in the note.

## Boundaries

- Writes exactly two kinds of path: `sprint-ledger/YYYY-MM-DD.json` and `sprint-ledger/_rollup.json`, under the configured vault directory. Nothing else, ever.
- **Read-only on every work surface**, like the rest of this plugin. It never closes a ticket, replies to a thread, merges anything, or marks work done on the owner's behalf.
- Creates scheduled tasks only of the bounded kind: one-shot, firing today, invoking `/sprint-day check` or `/sprint-day close` and nothing else. It never creates a recurring task; that stays with `/briefings-setup`, where a human sees it first.
- Deletes only scheduled tasks whose ids this skill wrote into today's ledger.
- Sends exactly one email per day, from `close`, to `owner.email`. Never to anyone else.
- Never upgrades a status. `unknown` does not become `self-reported` without an answer, and `self-reported` does not become `verified` without an artifact.
