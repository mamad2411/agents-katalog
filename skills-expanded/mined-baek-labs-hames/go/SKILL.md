---
name: go
description: Approve and execute the exact Hames contract just presented in the same session, or resume a selected active contract, when the user invokes /go.
---

# Go

Use the user's language. Hames contains its adapted DryForge execution workflow. Git, a clean working tree, branches and worktrees are not prerequisites. Never initialize, commit, switch branches, or push unless the user explicitly requests that operation. Do not install another plugin or create a separate `.dryforge/` state.

Load common rules and the selected workspace with `runtime/context.js`, then relevant shared root `docs/` and the active contract. Never read all docs by default or create a full empty document set.

Activate only the contract the user selected, execute within its bounds, and collect the required evidence.

When `/go` uniquely follows a contract presented in the same session, treat that invocation as approval and activation of its exact revision and display. Pass `--approve-presented`; do not ask for another approval or require the task ID. This shortcut never applies merely because a contract is newest or is the only stored candidate.

For a named contract already reviewed by the user, activate without repeating approval. If review cannot be established, show it once and wait, then pass `--approve-selected` with the user's confirmation. With zero or multiple plausible candidates, show choices. A single contract from another session still requires one selection confirmation.

Before activation, verify project root, `READY` state, current-user approval, revision, specification hash, and session availability. Never clear or replace a mismatched pointer automatically.

For the same session's `ACTIVE` contract, validate its pointer and resume from recorded progress without another confirmation. Transfer to another session only after one explicit handoff confirmation and evidence that the prior session ended or safely yielded.

Follow the numbered work plan. Record each step as pending, in progress, completed, failed, or blocked. Record a failed step's failure point and error note; after three failures at the same point the runtime blocks further progress. Start a step only after its dependencies complete. Parallelize only declared independent work that does not share files or external state and materially saves time.

Immediately before every critical action, show its target, action, and expected impact and obtain a separate explicit confirmation. `/go` approval does not replace this confirmation.

Stop if scope must change, a required result cannot be observed, or the contract changes. Record only safe evidence metadata; never store tokens, credentials, raw messages, personal data, or full tool output.

Apply verification in proportion to risk. Establish a failing check before behavior changes. Stop and report after three failures at the same point.

When independent review is required, give a separate reviewer the specification plus actual diff or artifact and evidence. Record one review checklist with `record-review`, fix blocking findings, and recheck them. Do not enter `REVIEW` until required work steps and review pass.

After a supported file write, the index hook updates the affected managed blocks. Verify its result; a failed index update means follow-up is needed and never authorizes deleting the original file. Use `/index` to detect changes made through shell or external apps. Keep index repair separate from its read-only audit.

Write durable knowledge only to approved shared root `docs/` destinations and record each as applied or deferred with `record-knowledge`. For useful discoveries outside them, show the exact proposed change and obtain separate approval before recording it. This does not authorize editing host memory.

Move to `REVIEW` only when every required evidence item passes. Present requirement-to-artifact results and limitations, wait for current-user acceptance, then transition through `ACCEPTED` and archive the same package internally.

Use the bundled `runtime/contract.js` `candidate`, `activate`, `resume`, `step`, `record-review`, `record-knowledge`, `confirm-critical`, `review`, and `accept` commands. Evidence is accepted only from the bundled post-tool hook's observed response. Never pass presentation approval, selection approval, handoff, critical confirmation, or acceptance flags before the corresponding user message.

After creating a remote resource, compare its returned identifier, parent, name, and type with the contract. Stop on mismatch or duplicate creation; attach the generated identifier to evidence and results without changing the specification.
