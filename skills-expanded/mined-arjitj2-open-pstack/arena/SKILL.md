---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# Arena

**Dispatch contract.** Read [`provider-dispatch.md`](../poteto-mode/references/provider-dispatch.md) before fan-out. Configured values are provider-qualified descriptors, not host-native model slugs. The parent starts native and external lanes directly; children never route themselves. On Codex, resolve the remaining Claude tool names via [`codex-tools.md`](../poteto-mode/references/codex-tools.md).

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use `arena runners` from the current harness's pstack model sheet when present. Otherwise default to one each on `codex:gpt-5.6-sol@max`, `grok:grok-4.7@xhigh`, `claude:opus@max`. An `auto` or `inherit-parent` entry in this line or the cross-judge line uses the parent model through its native lane. Each seat follows provider-dispatch's saved-chain policy before every attempt. A terminal outcome the sheet's `# fallback` policy authorizes makes a read-only seat eligible for its next saved attempt (`usage-exhausted` only when no policy is saved); a writer advances only when the helper proves the workload never started or a recorded parent inspection clears it, and otherwise stops for inspection. Every other route failure is a dropout, not a substitution; record it and continue with the remaining seats. Spawn more runners when the arena covers multiple design directions. Use the same descriptor N times when the work is generation-bound rather than judgment-sensitive.
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Start all N lanes in one fan-out phase through the provider-dispatch contract. Native lanes are background subagents. External lanes are direct background launcher processes with retained task/session handles, never foreground calls and never subagents supervising subprocesses. Give every lane the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

An external lane counts only when it satisfies [Completion and dropouts](../poteto-mode/references/provider-dispatch.md#completion-and-dropouts), including the assignment and model-argument checks for Codex, Devin, or Cursor `pinned-argv` evidence; a native lane counts when its tool transcript returns the assigned model's result. If the helper stops a candidate or its chain is exhausted, proceed with N-1 and note the exact dropout in the synthesis record. If it returns `inspect`, preserve the writer and inspect it before proceeding. A fallback that ran reports its actual descriptor; never describe it as the primary, and never replace a dropout with another provider silently.

## Phase C: Cross-judge

After every Phase B candidate chain is terminal, choose the judge descriptor from the `arena cross-judge pool` line in the current harness's pstack model sheet. If the sheet or that line is missing, choose from `codex:gpt-5.6-sol@max`, `grok:grok-4.7@xhigh`, `claude:opus@max`. Prefer a provider different from the parent and the likely base candidate. Dispatch one read-only judge through the provider contract. It sees the rubric and completed candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't dispatch it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel. Wait for the cross-judge's verified terminal result or recorded dropout before final selection, then compare its verdict with your scores. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts and fallback attempts with their actual descriptors, and the verification result.
