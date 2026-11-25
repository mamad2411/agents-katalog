---
name: wrap-session
description: "Session bookmark. Triggers when user says 'wrap up', 'done for today', /wrap-session, or when closing a work session on a CONTEXT.md-bearing project. Rewrites .attacca/focus.md, appends new decisions to CONTEXT.md, and surfaces repeated corrections as proposed amendments to AGENTS.md."
---

<!-- Design razor: VERIFICATION only. Checking current state and updating existing artifacts. Not a process or discovery. Delete when: CONTEXT.md is current and git history is clean. -->

# Wrap Session Skill

Close a session so the next one can start *attacca* — without pause. Two artifacts, two different jobs: rewrite the performance, and amend the score only where the session earned it.

## When to Use

Run this skill when:
- User says "wrap up" or "done for today"
- User runs `/wrap-session`
- End of a work session on a project with CONTEXT.md
- Handing off to a teammate or a cloud agent

---

## Inputs

| Layer | File | Scope | Why |
|---|---|---|---|
| Reference (stable) | `CONTEXT.md` | "Key Decisions" only | To append to, and to avoid re-recording a decision already there |
| Working (per-run) | `.attacca/focus.md` | Full file | The file being replaced |
| Working (per-run) | `git status`, `git log` since session start | Full | What actually happened |
| Working (per-run) | This session's conversation | Corrections you received | Step 4 — a note given twice is a score-level gap |
| Reference (stable) | `AGENTS.md` | Full — only if step 4 found something | Where a repeated correction is proposed as a convention |

Do not read the Project or Stack sections of `CONTEXT.md`. They are not yours to change, and loading them invites rewording them.

---

## Steps

### 1. Locate the files

`CONTEXT.md` at repo root, `.attacca/focus.md` beside it.

- **Neither exists** — this skill doesn't apply. Suggest `/interrogate` if starting a new project.
- **`CONTEXT.md` exists, `focus.md` doesn't** — a pre-4.3 project. Create `.attacca/focus.md`, move the `Current Focus` / `Next Steps` / `Blockers` sections into it, and delete those sections from `CONTEXT.md`. Tell the user you did this and why. Then check `.gitignore`: if it ignores `.attacca/` wholesale, narrow it to `.attacca/audits/` and `.attacca/sbom/` so `focus.md` is committed.

### 2. Rewrite `.attacca/focus.md`

This file is disposable. Replace it outright — don't merge, don't preserve history.

**Current Focus**: what was actually worked on today. 3–5 bullets max. Drop what shipped.
**Next Steps**: prune completed steps; add what this session revealed. 3–5 items, actionable.
**Blockers**: add new ones, remove resolved ones. "None" if clear.
**Last updated**: today's date.

Target ~30 lines. If it's longer, you're journaling.

### 3. Append new decisions to `CONTEXT.md`

Only if a real decision was made this session — a choice with a rejected alternative, not a task that got done.

- Append one bullet per decision: what was chosen, what was rejected, why.
- **Append only.** Never edit, reword, reorder, or delete an existing bullet. A decision that got reversed gets a *new* bullet saying so and naming the one it supersedes.
- If nothing was decided, don't touch `CONTEXT.md` at all. Most sessions don't.
- Update `Last updated` only if you appended.

Test for whether something belongs here: *would a teammate cloning this repo in six months need to know this to avoid re-making the same mistake?* If no, it goes in `focus.md` or nowhere.

### 4. Amend the score

*When performances keep going wrong the same way, fix the score.*

Look back over the session for **corrections you received more than once** — the same note, twice or more. Not preferences stated once, and not you catching your own mistake: things the user had to tell you again.

Each one is evidence of a gap in the score, and the fix belongs in a different place depending on what kind of gap it is:

| The repeated correction was about | Amend |
|---|---|
| How this project does things (style, conventions, workflow) | `AGENTS.md` |
| What this project is or has already settled | `CONTEXT.md` → Key Decisions |
| A constraint that should block, not remind | Propose a hook or a `/quality-gate` check |

Surface them, don't apply them silently:

> "You corrected me twice this session on X. That reads as a gap in AGENTS.md rather than a one-off — want me to add: *[proposed line]*?"

Two rules on this:

- **Two is the threshold, and one is not.** A single correction is a preference; asking to codify every one turns the score into a transcript.
- **The third correction is the expensive one.** If you're proposing an amendment for something you were told three times, say so — it means the last two sessions paid for a fix nobody made.

If nothing recurred, skip this step silently. Most sessions have nothing here, and inventing a gap to look thorough is worse than saying nothing.

### 5. Check for uncommitted work

Run `git status`. If uncommitted changes exist:
- Offer to create a BDR commit (reference `/bdr-commit`)
- If user declines, remind them uncommitted work will be lost on repo switch
- Do NOT force a commit

### 6. Verify budgets

- `.attacca/focus.md` under ~30 lines — prune Next Steps.
- `CONTEXT.md` under ~100 lines. If it's over, the fix is **never** deleting decision bullets. Move detailed spec prose to `docs/spec.md` and link it, or tighten the Project/Stack sections.

---

## What NOT to Do

- **Don't rewrite `CONTEXT.md`.** You append to one section of it, and propose amendments to another. A performance never edits the score.
- **Don't duplicate git history**: don't list every file changed. Git log already has that.
- **Don't create a journal**: `focus.md` is a bookmark, not a daily log.
- **Don't promote tasks to decisions.** "Implemented OAuth" is not a decision. "Chose Google-only OAuth, rejected GitHub for v1 because the reviewer flow needs org membership we can't read" is.

---

## Example

**`.attacca/focus.md` before:**
```markdown
## Current Focus
- Build authentication flow
- Set up database
- Design dashboard

## Next Steps
1. Implement OAuth with Google
2. Create users table
3. Build dashboard UI
4. Add payment processing
5. Set up monitoring
```

**`.attacca/focus.md` after:**
```markdown
## Current Focus
- Dashboard scaffolding (needs invoice filtering logic)

## Next Steps
1. Add invoice filtering to dashboard
2. Implement Stripe webhook handler
3. Write tests for payment flow

## Blockers
- Waiting on Stripe API key from client (blocking webhook testing)

Last updated: 2026-08-14
```

**Appended to `CONTEXT.md` → Key Decisions:**
```markdown
- OAuth via Google only for v1. Rejected GitHub — the reviewer flow needs org
  membership, which their scope doesn't grant. Revisit if enterprise asks.
```

Note what did *not* get appended: "completed database schema," "started dashboard." Those are work, not decisions, and git log already has them.

---

## Outcome

Next session (or teammate, or cloud agent) opens two files and immediately knows:
- From `CONTEXT.md`: what this project is and every decision that constrains it
- From `.attacca/focus.md`: where the work stopped and what's blocking

The decision trail is one session older and no shorter. The task list is current. Neither had to fight the other for space.

And if the session produced a repeated correction, the score is one line better — so the next performance doesn't need the same note. That's the difference between a project that stays as good as its last fix and one that compounds.
