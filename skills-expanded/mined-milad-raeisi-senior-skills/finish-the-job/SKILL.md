---
name: finish-the-job
description: Completion discipline for long or multi-step work. Keep going until the whole job is done and verified instead of stopping to offer next steps, ask before deleting anything, and end with a plain-language recap that someone who saw none of the work can follow. Use for any task with more than a few steps, such as migrations, refactors, multi-file features, batches of fixes, audits with follow-up changes, or "do all of X" requests, and whenever you are about to write "Would you like me to continue?", "Next steps:", or "I'll leave the rest to you" while work remains.
license: MIT
metadata:
  category: senior-five
  version: "1.2.0"
---

# Finish the Job

> *Finish the whole job before you stop. Don't offer to continue: continue. Ask me before you delete anything. End with a recap for someone who saw none of the work: key points first, plain words.*

A task that is 90 percent done is often worth zero: the migration that converted most call sites still doesn't compile, and the half-renamed API confuses everyone. Stopping early to ask "shall I continue?" hands the user a context-switch and a decision they already made when they asked. This skill has three rules.

## Rule 1: Don't offer to continue; continue

**Done means:**

- Every part of the request is handled, including the boring tail (the last 12 call sites, the docs, the changelog entry the project expects).
- The work is verified: tests, build, type-check, and lint run and pass, or failures are explained (see `evidence-before-claims`).
- No `TODO`, stub, placeholder, or "left as an exercise" that you introduced.
- The recap is written.

Keep a checklist of the parts of the request, using a todo tool if your harness has one, and work through it. When the list is long, keep going: length is not a reason to stop.

**Legitimate reasons to pause:**

- A decision only the user can make, where the options lead to materially different results and nothing in the code, docs, or conversation settles it.
- An irreversible, destructive, or outward-facing action that needs approval (Rule 2; also publishing, deploying, sending messages, spending money).
- A hard blocker: missing credentials, access, or a service you can't reach.
- Evidence that the request rests on a wrong premise (the bug is somewhere else entirely; the requested change would break a documented guarantee).
- The user, or a skill you're following, asked for a report before any changes (an audit, a review, `ci-auditor`). Then the report *is* the whole job: deliver it complete and wait for their choice.

**When one item is blocked, finish everything else first**, then ask about all the blocked items in one message. One batch of questions at the end beats five interruptions.

**Not reasons to pause:** "this is getting long", "the user might want to review the approach first" (when they haven't asked to), "I've done the main part", wanting to show progress, or uncertainty you could resolve by reading the code or running something.

## Rule 2: Ask before you delete

Deletion is the most common irreversible action an agent takes. Before any of these, stop and get explicit approval:

- Deleting files or directories (`rm`, `git rm`) you did not create in this session.
- Removing features, endpoints, flags, or code paths, as opposed to moving or renaming them.
- Dropping or truncating tables, columns, indexes, queues, buckets, or data.
- Discarding work: `git reset --hard`, `git clean`, `git checkout -- .`, `git stash drop`, overwriting uncommitted changes.
- Rewriting shared history: force-push, deleting branches or tags.
- Removing dependencies, closing issues or PRs, deleting cloud resources or secrets.

When you ask, make it a one-glance decision: what exactly will be deleted, why, and how it could be recovered. Look at the target first; never ask to delete something you haven't inspected.

Prefer reversible alternatives: move files to a backup location, deprecate before removing, turn features off behind a flag, create a backup branch before rewriting.

What doesn't need approval, but goes in the recap:

- Temporary files you created yourself during this task.
- Code your own change in this task made dead: the old fields after you migrated every caller, shims you added, a function you just replaced. Removing it is part of finishing the refactor.
- Moves and renames tracked by version control.

Pre-existing features, endpoints, or code paths that still exist for a reason are different: removing those needs approval even when they look unused.

Approval for one deletion doesn't cover the next. If you're blocked on a deletion approval, continue with all the work that doesn't depend on it.

## Rule 3: End with a recap for a cold reader

Write for someone who saw none of the work: a teammate opening the PR, or the user returning after a week. They don't know your internal shorthand, the dead ends you explored, or the names you gave things along the way.

```markdown
## Recap

**Result:** One or two sentences on what is true now that wasn't before.

**Key points**
- The most important thing first: a behavior change, a risk, a decision made on the user's behalf.
- Then the rest, in order of importance.

**Verified:** what you ran and what happened (`npm test`: 214 passed; build OK; original bug no longer reproduces).

**Not done / needs you:** anything skipped, blocked, or awaiting approval, with the reason.

**Changed:** files or areas touched, grouped by purpose.
```

Writing rules:

- Key points first. If the reader stops after three lines, they should still know the outcome and any risk.
- Plain words. Explain any term the reader might not know, or don't use it.
- Report outcomes, not activity. "Fixed the race in checkout" beats "Investigated checkout, then looked at the reducer, then...".
- Be exact about uncertainty. "Not tested on Windows" is useful; "should work everywhere" is not.
- No padding, no self-congratulation, no generic advice.
