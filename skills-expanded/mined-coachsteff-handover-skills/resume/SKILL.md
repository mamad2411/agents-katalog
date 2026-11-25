---
name: "Resume"
description: "Start a fresh coding session from a HANDOVER. Read the brief, verify it against the live files and git, reconcile any drift, then restate the active plan before making changes."
alwaysAllow: ["Bash", "Read"]
---

# Resume — Reconstruct State Before Acting

You are starting cold. A previous session left a HANDOVER. Your job is to ground yourself in the
ACTUAL current state before you answer or edit anything. Do not trust the brief blindly — verify it.

> This skill intentionally does not pre-approve `Write` or `Edit`. Resume is read-and-verify first;
> editing begins only after you have restated the plan (and, in Ask-to-Edit / Explore mode, the user
> has confirmed it).

## Startup protocol (do these in order, before any new work)

1. **Locate the project root.** If ambiguous, ask which project to resume.
2. **Read, in this order:** HANDOVER.md → PROGRESS.md → the spec / README → the key source files
   the handover names. Then follow the handover's own `<startup_protocol>` if it adds steps.
3. **Verify against reality.** Run the checks named in `<verification>` and `<artifacts>`:
   - `git status` and `git log --oneline -5` — does the last commit match the handover?
   - Run `init.sh` (or the documented start command) and exercise the app / run the tests.
   - Confirm each claim in `<current_state>` is still true.
4. **Honour `<source_of_truth_rank>`.** Where the handover disagrees with the code, the code wins.
5. **Treat `<unknowns_and_do_not_assume>` as blockers.** Resolve each by inspection before relying
   on it. Never act on an unknown as if it were settled.

## Reconcile drift

If what you observe differs from the handover (newer commits, a fix already applied, something
broken that now works or vice versa), say so explicitly in a short "Drift" note:

> Drift: handover says delete crashes, but the empty list is already guarded — likely fixed after
> the handover was written. Adjusting next_steps.

## Restate, then act

Before editing, post a short restatement the user can confirm:

- **Mission / phase** (one line).
- **Verified current state** (what you actually saw, not what the brief claimed).
- **Drift**, if any.
- **Plan** — the `<next_steps>`, adjusted for drift, as an ordered list.

In Explore or Ask-to-Edit mode, wait for the user to confirm or for a plan acceptance before
changing files. In Execute mode, proceed once the restatement is posted.

## Respect closed doors

Anything in `<decisions>` is settled. Do not reopen it unless the user explicitly asks.

## Do not

- Do not start editing before completing the startup protocol and restating the plan.
- Do not quote the handover as fact when the code says otherwise.
- Do not skip the verification run because the brief "looks complete".
