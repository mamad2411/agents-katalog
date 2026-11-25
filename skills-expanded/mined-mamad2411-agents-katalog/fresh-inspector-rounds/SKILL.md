---
name: fresh-inspector-rounds
description: "Run Inspect as rounds with an independence contract: each round a new inspector context, never resumed; only the blocking findings travel back to the builder, never the whole report; and the same finding returning a second time halts the loop and reopens Architect with that finding as a constraint, because a symptom was fixed. Includes the author guard, which lists checks for the owner to run rather than executing them on a change the owner did not write. Use when an inspect-fix-inspect cycle is running, when an inspector keeps being resumed, or for phrasings like \"the same bug keeps coming back after each fix\" or \"how many review rounds before we stop\". Not for reviewing one diff (code-review), the stage definitions (family-workflow) or QA's go/no-go (qa-workflow)."
allowed-tools: Agent(inspector), Read, Write, Edit, Grep, Glob, Bash(git:*)
---

# Fresh inspector rounds

Inspect is run as rounds when every round used a new inspector context, only blocking findings went back to the builder, and the loop ended either on a `PASS` that the Inspect owner accepted or on a recurrence that reopened Architect. The tier is fixed by the work: the inspector on the top tier, because it is the independent check, and the fixer on a mid tier, because it applies a bounded fix.

The failure of a review loop is that it stops being independent. A resumed inspector grades its own earlier verdict as much as the new diff, so each round gets gentler. A whole report sent back becomes the builder's to-do list: nits get fixed, the diff widens, and every extra change is new surface for the next round. And a loop that never stops on repetition fixes the same symptom three times, because the defect is in the approach and no amount of patching reaches it.

## Scope

Use for: an inspect, fix, inspect cycle on a slice; deciding what goes back to the builder; deciding when to stop and reopen the design; a change the owner did not write that the inspector must not execute.

Do not use for: reviewing one diff with findings by severity, which is `code-review`; the stage definitions, which are `family-workflow`; QA's strategy and its go/no-go, which is `qa-workflow`; a defect class that keeps recurring across separate slices, which is `yield-to-lesson`; or writing the tests, which is `test-design`.

## Workflow

### 1. Settle whose change it is

Run the checks only on a change the owner wrote. A test, a build target, a hook or a config entry the change touches is code the change controls, and running it runs that code with your credentials and network. For a contributor's change, a fork's, or one whose author you cannot confirm: run nothing it controls, read it through git refs, list the checks it would need as not assessed, and name them for the owner to run in a disposable sandbox with no credentials and no network. Open the session from the base branch, not the contributor's checkout, which loads its own agents, settings and hooks.

### 2. Start a new inspector for the round

Brief it with the frame's success criteria, the diff or changed paths, the commands, and the Author line. Do not give it an earlier round's report or findings: the coordinator keeps that record, and the inspector reads the change cold. Read `references/round-protocol.md` for the brief and the finding ledger.

### 3. Read the report per criterion

The inspector reports each success criterion as `HOLDS`, `FAILS` or `NOT ASSESSED`, with its evidence locator and the check it ran, and returns `PASS`, `FIX` or `STOP`. A criterion without evidence is not assessed, not held. A `FAILS` line also carries the consequence and the smallest fix. Severity-ranked findings on the diff itself are `code-review`'s work; the inspector lists those as observations, unranked, and they are not rebuilt here.

### 4. Send back the failures only

Each `FAILS` line is a blocking finding. It goes to the builder as problem, evidence locator and the fix the inspector gave for it. For a slice the owner wrote, the builder is the writing agent that built it; when none is running, the main conversation is the builder and applies the fix itself, which is why this skill can edit the tree. For a contributor's change, the fix packet goes back to that contributor to apply on their own branch, and the next round inspects what they push. When the author is unknown, there is no one to send it to: stop the loop, hand the packet to whoever asked for the review, and name the missing author as the blocker. In neither case does the main conversation apply the fix to the trusted checkout. The builder is never the inspector's context. A `NOT ASSESSED` criterion is a gap for the Inspect owner to close, not a task for the builder, and observations stay in the report and travel to Yield. The builder never receives the report itself.

### 5. Re-inspect with a fresh inspector

Return to step 2. Never resume the inspector that judged the earlier round; a new context is the contract. There is no fixed round count, because the stop is recurrence, not a number.

### 6. Halt on a repeated finding

Match each blocking finding to the ledger by criterion and locator. The same finding returning a second time halts the loop: a symptom was fixed. Reopen Architect with that finding as a constraint, so the approach changes rather than the patch. Read `references/recurrence.md` for what counts as the same finding and what Architect receives.

### 7. Hand the go/no-go to its owner

On a final `PASS`, give the Inspect owner the report and its not-assessed list. The go/no-go is theirs, with evidence; the loop supplies it and does not decide it.

## Anti-patterns

**The resumed inspector.** Continuing the same context to re-check a fix, so it defends its first verdict.

**The whole report back.** The builder fixes the nits too and the diff grows each round.

**The third patch.** Fixing the same finding again instead of reopening Architect.

**Self-inspection.** The builder, or a context that inherited the build, acting as the inspector.

**Running the contributor's checks.** Executing a change's own tests on your machine to see if it passes.

## References

- `references/round-protocol.md`: read at step 2 for the inspector brief, the fix packet, the finding ledger and the stop conditions per round.
- `references/recurrence.md`: read at step 6 for what counts as the same finding, and what to hand Architect when the loop halts.
