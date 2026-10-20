# Attention Digest Workflow

This directory contains the attention digest workflow definition and its
semantic detector, renderer, route, and CLI coverage.

- Inspect monitored completions for changed attention, never use run-count cadence.
- Push only new or changed label/detail pairs. Ordering alone is not a change;
  removals advance the snapshot silently so a cleared condition can alert again.
- Keep completion triggers filtered to exclude the digest's own completion.

## On-Demand Seam

`renderOnDemandAttention({ scopeRoot, runsDir, authority })` in `step.ts` runs the same
detector + renderer the automated path uses and returns the full current
`{ items: AttentionItem[]; text: string }`, regardless of prior alerts. Operator-facing pull
surfaces such as Telegram, Slack, CLI, daemon HTTP, embedded web, macOS, and
mobile should consume this seam directly and pass canonical workflow-run
authority rather than deriving it from the run-artifact directory.
Issue inspection uses the explicit authority state directory or the daemon's
read-only scope-state provider. CLI inspection uses `client.autonomy` so live
reads resolve authority on the daemon. `--state-dir` selects explicit offline inspection.

Provider arm: unlike the recall, answer, and voice surfaces, attention has no
semantic provider seam — the body is deterministic over local task state and
run history. It does require the daemon's canonical workflow authority. The
route returns success (200) when it can render and reports read failures. New attention client
surfaces should strict-decode `{ data: { items }, text }` and surface transport
errors as plain failure banners.

Snapshot invariant: revisioned scope state and a scope-local logical resource
keep observations serialized through transaction completion. Changed snapshots
and alert events publish together only on run success. Unchanged observations
do not write state; on-demand reads neither consume alerts nor advance state.

Bus invariant: the on-demand path must not emit `workflow.attention.digest`.
Other notification channels (Slack, email, webhook) must not see an operator's
`/attention` as a duplicate automated digest; the requesting Telegram
chat receives the rendered text in-band.

No-items reply: when `detectAttentionItems` returns nothing, the on-demand
body is `NO_ATTENTION_ITEMS_TEXT` (a short fixed reply) rather than the
digest header with an empty bullet list, so an operator can
distinguish "nothing wrong" from "command failed".

Quiet-hours invariant: quiet hours do not gate the on-demand path. The
operator initiated the request, so the runtime quiet-hours rule that buffers
automated pushes does not apply.
