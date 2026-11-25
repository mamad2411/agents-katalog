---
name: graph-orchestrator
description: Use when a request has many similar subtasks (auditing every file in a repo, researching a list of companies, migrating a set of endpoints, reviewing a batch of documents), when a plan is about to be written as "first X, then Y, then Z" across more than about four steps, or when work spans 10+ files or sources. Also use when a previous attempt at a large task ran out of context, lost detail partway through, or produced a summary that thinned out toward the end, or when a plan ends in an irreversible action (mass send, deploy, delete) that needs gating.
---

# Graph Orchestrator

Most multi-step plans are written as chains because that's how people narrate work, not because the steps actually depend on each other. A chain of ten steps where only three real dependencies exist wastes time, and worse, it burns context linearly, so quality degrades toward the end. This skill turns a request into a dependency graph first, then executes it in phases.

The graph is a *planning* artifact, but it also decides who executes each node: work you do inline, and work you dispatch to parallel subagents when the environment provides them. What the graph buys you is knowing which work can fan out, which must wait, where results need to be consolidated before they overflow, and which single node needs a human's sign-off.

## The core move: the dependency audit

This is the part that matters most. Everything else follows from it.

For every pair of steps you were about to sequence, ask one question:

> **Does step B literally read the output of step A?**

If B only needs the *same inputs* A had, they are independent. If B needs A's *result*, there's a real edge.

People systematically over-connect. "Analyze the auth module and then analyze the payments module" has no edge. The word "then" is narration. "Analyze the auth module and then write a report on it" has a real edge.

Work through the list explicitly rather than eyeballing it:

```
Step: Summarize each of 40 support tickets
  Reads prior output? No, each ticket is independent input
  → parallel

Step: Cluster the summaries into themes
  Reads prior output? Yes, needs all 40 summaries
  → depends on the summarize group

Step: Draft recommendations
  Reads prior output? Yes, needs the clusters
  → depends on clustering
```

### Hidden edges

Data flow isn't the only thing that creates an edge. Check for these too, because they're the ones that cause real failures:

- **Shared writes.** Two nodes editing the same file must be ordered, even though neither reads the other.
- **Rate limits and quotas.** Twenty concurrent calls to an API that allows five will fail. The constraint is real even though the tasks are logically independent, so cap the batch size instead.
- **Schema or interface changes.** Anything that renames a symbol, changes a signature, or alters a data format must complete before work that consumes it.
- **Cost or destructiveness.** Anything irreversible (writes to production, sends, deletes) sits behind a verification node *and* a human approval gate, see "Irreversible actions" below. This edge exists regardless of the dependency structure.

If you find no hidden edges, say so explicitly. Silence here usually means the check wasn't done.

## Fan-in is where quality is actually lost

A single synthesis step reading 100 outputs produces a worse result than a layered one, and the degradation is quiet. The output looks fine, it's just thin on everything after the first twenty items.

Consolidate in layers of **20 to 30 items**:

```
100 file analyses
  → 4 batch summaries (25 each)
    → 1 final synthesis
```

Two rules make this work:

1. **Count before you consolidate.** At every fan-in, check received against expected. If 38 of 40 came back, name the two that are missing rather than synthesizing over the gap. A synthesis that silently drops items is worse than one that reports a hole.
2. **Preserve specifics upward.** Each batch summary should carry concrete findings (file paths, quantities, names), not just impressions. Impressions don't compose. If a batch summary says "several files had issues," the final synthesis has nothing to work with.

## Output format

Produce a phase plan before doing any work. Keep it short enough to read at a glance:

```markdown
## Goal
[One sentence.]

## Dependency audit
[Each step, whether it reads prior output, and the verdict. Note hidden edges or state that none were found.]

## Phases
**Phase 1 - parallel (N items, batches of M)**
- [what runs, and why these are independent]

**Phase 2 - depends on Phase 1**
- [what runs, and which output it consumes]

## Consolidation
[Layer structure and the completeness check.]

## Verification
[What gets checked before this is called done. Omit only for low-stakes work.]

## Approval gate
[Required if any node is irreversible or outward-facing: the exact action, scope, and cost the human will be shown. Write "none, nothing irreversible" otherwise.]

## Risks
[What could make this plan wrong.]
```

Then say what you're about to run and start Phase 1.

For a plan that will be handed to a scheduler or another agent, a machine-readable version is in `references/plan-schema.md`. Don't emit it by default, it's noise for a human reader.

## Executing the phases

A phase of independent items can execute two ways. Pick per phase, not per plan.

**Subagent fan-out.** When the environment has a subagent tool (Claude Code's Agent tool, or equivalent), dispatch a fan-out phase as parallel subagents in a single turn. Each subagent gets a self-contained prompt: the shared context it needs pasted in, its slice of the items, and the exact output shape to return. This is real concurrency, and just as importantly each item gets a fresh context, so item 47 isn't degraded by 46 items of accumulated state. Dispatch when the per-item work is substantial (reading and analyzing a file, researching a company), the prompt can carry everything the item needs, and the output compresses to a fixed shape. Cap the width at whatever hidden edge binds (rate limits, spawn cost). Batches of items per subagent beat one subagent per item when items are small.

**Inline batching.** When no subagent tool exists, or the items are too small or too entangled with evolving shared context to be worth a dispatch, issue independent tool calls together in a single turn and process the phase yourself. The win is smaller but real: you're not carrying irrelevant intermediate state between independent items.

Some nodes stay inline regardless: the dependency audit and rubric-setting (everything downstream depends on getting these right), the final synthesis and prioritization (judgment the orchestrator must own), and any irreversible action (never delegate a send, deploy, or delete to a subagent).

### Model tiering

When subagents can be assigned a model tier, match the tier to the node, not the plan:

- **Fast/cheap tier** for classification, extraction, and mechanical checks (does every expected item appear in the synthesis?). Misrouting here is recoverable.
- **Standard tier** for the per-item analysis and building. This is most of the work.
- **Strongest tier** for the final verification of high-stakes output, in a fresh context that did not produce the work. The expensive failure mode is a false "looks good," so this is the one place to pay up.

Don't hardcode model IDs in plans. Name the tier and let the environment resolve it.

A few things worth holding to during execution:

- **Same shape for every item in a group.** If forty files are being analyzed, each analysis should return the same fields. Ragged outputs make the fan-in step do reconciliation work it shouldn't have to.
- **Report failures as data.** If one item fails, record it and continue the batch. Halting a 40-item phase because item 12 errored throws away 39 completed results. Halt only when the failure invalidates the rest.
- **Re-read the plan at each phase boundary.** By phase 3 the original plan has scrolled well out of working attention. A one-line restatement of what the phase depends on is enough to catch drift.
- **Stop and re-plan when the graph is wrong.** Discovering mid-execution that two "independent" items actually conflict is normal. Revise the plan and say what changed. Don't quietly work around it.

## Scope

This is for work with genuine structure to exploit: many similar subtasks, or a real mix of independent and dependent steps. A five-step linear task where each step truly feeds the next gains nothing from a graph. The plan is just the chain, so say that and get on with it rather than dressing a chain up as a DAG.

Rough threshold: fewer than about six subtasks with no meaningful fan-out, skip the formal plan and do the dependency audit in your head.

## Verification

For anything high-stakes (code that will merge, analysis that will inform a decision, output the user can't easily check) add an explicit verification node after consolidation. It should re-derive at least one claim from source rather than re-reading the synthesis, since a critique pass over a summary mostly just agrees with the summary. Where subagents exist, run verification as a fresh-context subagent given only the claims and the sources, not your synthesis, so it can't ratify what it's checking.

**When verification fails, that's data, not a dead end.** Feed the specific failures back and redo only the affected nodes, not the whole graph, then re-verify the changed portion plus a fresh sample. Cap this at about three attempts. If the same class of failure comes back twice, the problem is upstream: the rubric or the plan is wrong, so stop and re-plan rather than loop. If it still can't pass, deliver the failure report to the user instead of shipping output you know is flawed.

## Irreversible actions

Verification is a quality check, not an authorization. Anything irreversible or outward-facing (sending to people, deploying, deleting, writing to production) gets its own human approval node after verification passes, and the graph hard-stops there.

The approval request must be concrete enough to decide on in seconds: the exact action, its scope, and its cost. "Send this email to the engineering list (500 recipients, one list alias), subject and body below", not "ready to proceed?" If the human says no, their reason goes into state and the affected nodes redo, same as a failed verification. And the irreversible action itself always executes inline, never in a subagent.

## Further reading

- `references/best-practices.md` has worked patterns, common failure modes, and a longer example. Read it when a plan is unusually large (50+ nodes) or when a previous run degraded and you're diagnosing why.
- `references/plan-schema.md` has the machine-readable plan format. Read it only when the plan is being handed to an external runner.
