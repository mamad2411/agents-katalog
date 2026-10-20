---
name: github-address-review
description: "Implement actionable review changes and explain resolutions. Use to implement accepted review feedback; github-review produces findings."
---

# github-address-review

Implement actionable review changes and explain resolutions.

## Choose this workflow

Use to implement accepted review feedback; github-review produces findings.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [GitHub methods](../../references/packs/github.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; PR and review threads plus accepted product constraints.

**Pack prerequisites:** Exact owner/repository and relevant issue/PR/ref; authenticated read access through an available connector or CLI for remote evidence. External writes require the requested operation, appropriate account permissions, and rechecking target state. Local preparation remains useful without write access.

- **Infer from evidence:** Resolve owner/repository and PR/issue/ref from links, remotes and supplied artifacts; inspect available account and head identity.
- **Reasonable default:** Prepare local text or analyze supplied evidence if remote access is absent; label its freshness.
- **Ask only when needed:** Ask only when repository/account/target ambiguity blocks the requested remote action; missing write access does not block local drafting.

Declared evidence requirements: `project.read`, `git.repo`, `github.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Implement actionable feedback locally; pushing, replying, and resolving threads follow explicit requested scope.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Map each comment to current code and accepted contracts, verify its premise and identify conflicting suggestions.
2. Implement coherent changes for the accepted comments and run the relevant checks.
3. Keep a per-comment disposition tied to the final diff.
4. All changes are owned by the user. Add no agent/model self-attribution, AI-generated signature, badge, or agent Co-authored-by trailer to commits, PRs, comments, release notes or messages. Use the existing user Git identity; preserve legitimate human attribution and required third-party notices.

## Technical method

- **Inspect:** Map each comment to its current code and the accepted requirement, including already changed or conflicting requests.
- **Method:** Fix the demonstrated issue, preserve scope and track which comments are addressed by evidence versus need clarification.
- **Avoid misdiagnosis:** A reviewer suggestion can be stale or introduce a regression; resolving a thread is a distinct remote action.
- **Check the result:** Verify each accepted fix against the original trigger and re-read current review state before requested replies or resolution.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [GitHub worked example](../../references/examples/github.md).


## Decision branches

- **When a suggested change contradicts verified behavior or another accepted request:** Explain the conflict and seek that decision without applying incompatible edits.

## Deliver and verify

- Patch with a comment-to-change mapping, verification evidence, and disputed, blocked or remote threads still requiring action.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A valid review bug is fixed; a suggestion contradicting the accepted API contract is explained rather than blindly applied.
- Review newly prepared commit/PR/message text, including template or hook additions, for agent self-attribution before submission; verify the resulting artifact when available. Do not silently rewrite existing history or remove human credits.

## Stop and recover

- Do not claim remote threads resolved from a local fix. Ambiguous policy changes need clarification before dependent edits.

## Example requests

- **Normal (apply):** Implement the actionable feedback on the specified PR; keep API compatibility.
- **Edge (apply):** Address feedback when one comment is already fixed and another conflicts with the API.
- **Blocked (inspect):** Inspect review feedback without the referenced revision; do not claim threads resolved.
