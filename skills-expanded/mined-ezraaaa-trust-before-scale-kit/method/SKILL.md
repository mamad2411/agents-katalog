---
name: method
description: "How to work in a trust-before-scale project: session-start checks, turning repeat failures into checks, and when to add agents. Use at session start where .agents/trust-before-scale.json (or legacy .claude/trust-before-scale.json) exists, or before adding agents."
---

# Trust before scale: how to work

The limit on agent output is how much can be trusted without a full read, not how many agents run.

**Every session start**
- `node scripts/tbs/learn.mjs --due`: read repeated mistakes and checks that did not hold. Use the `learn` skill to draft prevention before scaling.
- `node scripts/tbs/self-merge.mjs --owed`: read each owed self-merged PR, then label it `reviewed-after-merge`
  or revert it. Review the listed hook skips, then run `node scripts/tbs/self-merge.mjs --ack-skips`.
  The list includes skips after the last acknowledgement and since the oldest owed PR (if any).
  Do this before new work.
- `node scripts/tbs/skill-eval.mjs --check`: if a review skill changed, run its eval before relying on it.

**When something goes wrong twice** (a review finding, a process slip, a bad merge), use the strongest layer
that can prevent it: architecture that removes the possibility, then types, a lint whose error tells you the
fix, a test, and a hook or gate. Put docs last for remaining judgment calls. Prove each check red on a real
past mistake before trusting it, then reduce the prose rule to the check's name. Keep the rule-to-enforcer
table at `docs/trust-before-scale/enforcers.md` current. Exceptions need a reason, an expiry date and a
human's approval.

**Evidence that proves itself.** Every gate and review log starts with `HEAD=<sha>` and ends with the exit marker:
`{ echo "HEAD=$(git rev-parse HEAD)"; <gate>; } > gate.log 2>&1; echo "EXIT=$?" >> gate.log`.
Merge with `grep -qx 'EXIT=0' gate.log && gh pr merge <N> --merge --match-head-commit <sha>`. The plugin's hook
blocks anything looser. To stand down explicitly, prefix the command with
`HOOK_SKIP=1 HOOK_SKIP_REASON="<text>"`; a bare skip is held. Accepted skips append UTC time, reason and
the first 120 command characters to the git directory's `tbs-skips.log` for the next session to review.

**Walks and emulators** run on free ports: `node scripts/tbs/free-ports.mjs -- <command>`. Never take another
session's default ports, and never ask for them when free ports will do.

**Briefs** use `docs/trust-before-scale/brief-template.md`. Before sending, check every step, red proof and imported
pattern against the allowed-files list. A contradiction there stops the implementer, which is right but costs a run.

**Before asking the owner**, check whether a run or the code can answer the question. If so, find out.
Batch what remains at check-ins, each with the recommended pick, the evidence, the risk, and what happens
if no answer comes. At adoption level 4, if the owner is not around, park what needs them and keep working
on what does not; never stop for one open question. Silence or elapsed time is never an answer.

**Scale:** run `node scripts/tbs/lanes.mjs` before adding a lane. Never exceed what it allows.

**Every session end:** run `node scripts/tbs/learn.mjs sync` so local journal lessons enter the normal commit.
Review the added entries; leave them with the session changes for the authorized commit workflow.
