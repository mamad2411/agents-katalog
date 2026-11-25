---
name: frame-claim-ledger
description: "List every factual claim a frame or an architecture rests on — how a flag or API behaves, a cited figure, a user need — and settle the heaviest before the hard-to-reverse decision is recorded: one claim per read-only research agent, run in parallel beside architect, each finding labelled primary, consensus or inference. An unverified or refuted claim cannot be the basis of that decision, so architect returns NEEDS FRAME. Use when a frame is about to go to Architect, when an ADR rests on something nobody has read the source for, or for phrasings like \"what are we assuming here\" or \"has anyone checked that this limit is real\". Not for checking one claim on its own after the fact, writing the ADR (decision-record), or reviewing a diff (code-review)."
allowed-tools: Agent, Read, Grep, Glob
---

# Frame claim ledger

A frame is ledgered when every claim it or the architecture rests on is written down, the two that carry the most weight were settled by someone who read the source, and the hard-to-reverse decision names only settled claims as its basis. Whatever was not settled is listed as not assessed in the decision record rather than left out of it.

The failure is a decision recorded on a premise nobody read: a flag's behaviour remembered from a blog post, a figure with no origin, a user need that is the requester's belief. The decision is the one that is expensive to undo, so a false premise is paid for in full, and the ADR reads as well reasoned because the reasoning is sound and the input is not. The second failure is the opposite: every assumption sent for checking, a week spent confirming claims that could not have changed the decision. This skill lists them all, settles the two that matter and says out loud which it left.

## Scope

Use for: a frame or design note about to go to Architect; an architecture that depends on a limit, a figure or a user need; a decision a person is about to record as an ADR.

Do not use for: verifying one named claim on its own, after the decision, with nothing resting on the rest; writing the record, which is `decision-record`; the stage definitions, which are `family-workflow`; or reviewing a diff, which is `code-review`.

## Workflow

### 1. List every claim the decision rests on

Read the frame and the draft approach for each sentence that would change the decision if it were false. Three kinds recur: behaviour (a flag, an API, a quota), a figure (a statistic, a price, a benchmark) and a need (who wants this, how many). Restate each so it could fail: subject, version or date, scope. Read `references/ledger-format.md` for the table and the restating rules.

### 2. Weigh them and keep two

Rank by how much of the hard-to-reverse decision falls if the claim is false. Settle at most the two heaviest. A third delegation costs a context and a reading, and the third claim rarely moves the decision; an unlisted claim, though, is invisible, which is why the list is complete and the settling is not.

### 3. One claim, one agent, in parallel

Brief one read-only research agent per claim, on a mid tier at medium effort, and run both while architect drafts the approach on the top tier. Read `references/claim-brief.md` for the brief and what must come back. One claim per agent, because a finding averaged over three claims is a finding about none of them. Where `stage-tiering` sets a two-agent limit, these two are the two survey agents; architect is the stage being served, not a survey agent.

The `Agent` grant is unscoped on purpose. The plugin ships no research agent of its own, so the claim agent is whichever read-only one the session has, the built-in `Explore` or a project's own, and naming one here would refuse every other. Absent `Write` and `Edit` are not enough on their own: a shell writes without an editing tool, so when the agent also holds `Bash`, as `Explore` does, the brief says it writes no file and runs nothing that changes the checkout, or you pick one without `Bash`. The same grant starts `architect` beside them.

### 4. Read the labels, not the verdict alone

Each finding returns a verdict (`HOLDS`, `DOES NOT HOLD`, `NARROWER` or `UNVERIFIED`) and evidence labelled primary, consensus or inference. Consensus and inference are unverified for this purpose: several people repeating a claim is not the source.

### 5. Gate the decision on the ledger

- `HOLDS` on primary evidence: the claim may be the basis.
- `NARROWER`: rewrite the premise to the narrower claim and check the decision still follows.
- `DOES NOT HOLD`, `UNVERIFIED`, or held only by consensus: it may not be the basis. If the decision needs it, architect returns `NEEDS FRAME` naming the claim, and the frame is fixed first.

The way out that is not a quiet pass is to choose the reversible alternative, so the claim no longer carries the decision. A claim under a hard-to-reverse decision does not get the Architect gate waived: that waiver is allowed only when the slice carries no such decision.

### 6. Carry the ledger into the record

Hand the settled claims and the not-assessed list to `decision-record`, so the ADR states what it rests on and what it left unchecked.

## Anti-patterns

**The ledger after the ADR.** Listing claims once the decision is written, so the list justifies it instead of testing it.

**The bundle.** Three claims in one delegation, returned as one reassuring paragraph.

**Hunting for agreement.** Briefing an agent to confirm; ask what would make the claim false.

**Settling everything.** No stopping rule, so the frame waits on claims that could not change the decision.

**The silent drop.** Unsettled claims missing from the record, so a reader assumes they were checked.

**"Verified" with no label.** One fetched source and two blog posts reported as one word.

## References

- `references/ledger-format.md`: read at step 1 for the ledger table, the three claim kinds, how to restate a claim so it can fail, and how to weigh.
- `references/claim-brief.md`: read at step 3 for the delegation brief, the return to require, and what each verdict does to the decision.
