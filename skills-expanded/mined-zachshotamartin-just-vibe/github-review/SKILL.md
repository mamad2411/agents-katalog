---
name: github-review
description: "Review a PR using its discussion, changes, and checks. Use to review a specific remote PR revision; review handles supplied/local diffs."
---

# github-review

Review a PR using its discussion, changes, and checks.

## Choose this workflow

Use to review a specific remote PR revision; review handles supplied/local diffs.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [GitHub methods](../../references/packs/github.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; PR URL/number, revision, and review focus. Posting a requested review uses apply mode.

**Pack prerequisites:** Exact owner/repository and relevant issue/PR/ref; authenticated read access through an available connector or CLI for remote evidence. External writes require the requested operation, appropriate account permissions, and rechecking target state. Local preparation remains useful without write access.

- **Infer from evidence:** Resolve owner/repository and PR/issue/ref from links, remotes and supplied artifacts; inspect available account and head identity.
- **Reasonable default:** Prepare local text or analyze supplied evidence if remote access is absent; label its freshness.
- **Ask only when needed:** Ask only when repository/account/target ambiguity blocks the requested remote action; missing write access does not block local drafting.

Declared evidence requirements: `github.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Code review informed by discussion and checks; no automatic review submission.

Inspect/plan: review without posting; save requested artifacts only. Apply: post only the requested review or comments to the resolved PR after revalidating its head revision. Approving, merging, resolving threads and pushing need their own exact request.

## Execute

1. Record the head and base SHA and fetch that diff; read changed and surrounding source and relevant discussion.
2. Map each finding to a current diff location and verify it against the current head, distinguishing blockers from optional observations.
3. Revalidate the head before any requested posting.
4. All changes are owned by the user. Add no agent/model self-attribution, AI-generated signature, badge, or agent Co-authored-by trailer to commits, PRs, comments, release notes or messages. Use the existing user Git identity; preserve legitimate human attribution and required third-party notices.

## Technical method

- **Inspect:** Obtain the exact PR head diff, full changed files, callers, checks and relevant prior discussion.
- **Method:** Apply the review selection guide to changed boundaries; require a concrete trigger, reachable bad outcome and verified absence of an upstream guard.
- **Avoid misdiagnosis:** Fixed line numbers or findings from an older head can become wrong after force-push; unchanged critical risks need explicit attribution.
- **Check the result:** Reconfirm head and diff location before any authorized posting; report severity from impact and confidence separately.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [GitHub worked example](../../references/examples/github.md).
- Reviewing code or security boundaries: select and read the matching technical branches before concluding: [Review selection and evidence](../../references/security/review.md).
- Language/runtime semantics, concurrency or resource ownership can change the result: [Language and runtime review methods](../../references/scenarios/language-review.md).

## Decision branches

- **When the PR head changes during inspection:** Refresh affected findings and checks rather than attaching stale comments.

## Deliver and verify

- Prioritized findings with trigger, evidence and current diff locations, the reviewed SHA and review limitations.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A finding fixed in the latest revision is not repeated; review comments use locations that exist in the reviewed diff.
- Review newly prepared commit/PR/message text, including template or hook additions, for agent self-attribution before submission; verify the resulting artifact when available. Do not silently rewrite existing history or remove human credits.

## Stop and recover

- Sending a review requires explicit instruction. Recheck head before posting so findings are not silently attached to stale code.

## Example requests

- **Normal (inspect):** Review the current head of the specified PR without posting a review.
- **Edge (inspect):** Review a PR that was force-pushed after an earlier comment.
- **Blocked (inspect):** Review exported PR artifacts without posting or live metadata access.
