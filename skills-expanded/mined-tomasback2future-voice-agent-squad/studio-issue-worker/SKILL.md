---
name: studio-issue-worker
description: "Resolve exactly one explicitly assigned Voice Agent Studio GitHub Issue end to end as a Worker: claim its canonical Squad item, reproduce and fix it in an isolated branch/worktree, test, open and shepherd one PR, acquire the environment at the verified release gate, verify the exact staging revision, roll back on failure, release locks, and close the Issue only after acceptance. Use when a prompt names one Studio Issue and item; never scan or dispatch the queue."
---

# Studio Single-Issue Worker

The generic [Worker skill](../../agent-loop/roles/worker/SKILL.md) owns the
process for this one Studio Issue: the work order, failure branches, watching
your own preconditions, checkpoints, phase reports and closure by verification
layer. Read it first. This skill adds only what is true for Studio: identity and
claim, authority, product boundaries, the Grok review and Studio delivery. Where
both speak, the generic skill decides process and this one decides Studio facts.
Do not create a goal unless the user explicitly requests one.

Read workspace `AGENTS.md`, repository instructions, the live GitHub Issue and
[lifecycle](references/lifecycle.md) before mutation. Phase references:

- [delivery quality](references/delivery-quality.md): work-package planning, ENV
  admission, shared-failure retry or blocker handoff, performance sampling,
  repeated review corrections, retained fixtures, automated acceptance and human
  fallback.
- [execution efficiency](references/execution-efficiency.md): before isolated
  database setup. The Studio profile's `references/couchbase-environments.md`:
  before database access or deployment configuration changes. Production uses
  `couchbase-cn-2`, `voice-agent-studio._default` and the independent
  `voice-agent-studio-production` runtime account; preserve its scoped query
  permissions and separate DDL identity, and never infer production settings from
  staging or rewrite business SQL to switch credentials.
- [staging](references/staging.md): before acquiring an environment, including
  its [EKlet scheduling and event-chain checks](references/staging.md#capacity-probes-and-eklet-scheduling)
  for capacity probes (verify required nodeAffinity in each affected template and
  live Pod; distinguish scheduling, post-assignment quota and image-pull failures).
- [staging candidates](references/staging-candidates.md): the assigned delivery
  mode. [review readiness](references/review-readiness.md): before review.
- [Dispatcher callback](references/dispatcher-callback.md): at assignment and
  before ending.
- [role-bound flow repair](../squad-dispatcher/references/flow-retrospective.md):
  flow audits, startup skill binding, user pauses and release-repair routing.
- [design admission](../squad-dispatcher/references/design-admission.md): verify
  the assigned READY design revision before product edits. The Issue owns naming,
  entry points, scope, compatibility and acceptance; you own ordinary
  implementation choices. A contradiction goes to the Dispatcher as one
  issue-local decision request with evidence; record a revised decision without
  discarding valid work.

## Identity and ownership

Own the Issue and canonical primary item bound to the assignment. Missing or
ambiguous identity, or an unbound prompt naming a different Issue, requires
correction. Never discover, reserve, dispatch or self-select another Issue.
Original acceptance failures and omissions remain repairs on this Issue,
including additional PRs and the original-path recheck. A separate finding
(a `no` row that also fails on the base revision, or something no row covers in
another component or in a model or provider) is reported once and does not hold the close. An authorized related-work
amendment may reuse this owner through [existing-owner routing](../squad-dispatcher/references/session-continuity.md#existing-owners-and-supported-assignment-routes);
verify scope and custody before writes and never bypass read-only, production or
native-session fences.

1. Run Squad identity/status snapshots and reuse the one item whose title
   contains `[github:<owner>/<repo>#<number>]`.
2. Atomically claim it before edits. If held, register once with the holder and
   park with `claim --wait`; do not poll or look for other work.
3. Keep the claim through implementation, PR corrections, guarded merge, exact
   revision verification and final Issue disposition. Ending a turn, an open PR
   or a held ENV does not end the assignment; finish useful pre-gate work and park
   on `claim --wait` as a tracked task for contention.
4. Use a clean isolated worktree and `codex/issue-<number>-<slug>` branch;
   preserve unrelated dirty worktrees.

Record progress in the ledger and the owned GitHub progress comment; it needs no
answer. Apply a received correction at a safe step boundary without restarting
valid work. Record the originating Dispatcher; after durable closure, verified
handoff or a new terminal blocker, persist the deduplicated event and notify
through a verified message API/mailbox, never by injecting cmux terminal input.
Callback delivery is not acceptance or proven termination.

## Standing authorization

Creation of this Worker by the authorized Dispatcher is standing authorization to
complete the exact named Issue end to end: implementation, commits, pushes, PR
creation and correction, policy-compliant merge, staging environment claim and
deployment, acceptance, rollback, Issue/PR updates and Issue closure. Proceed as
soon as the required gates pass; do not ask for or wait on another human
confirmation. When the assignment pre-authorizes "assess, then execute if the
condition holds", the assessment result is your go signal.

This does not expand scope beyond the named Issue or bypass atomic claims,
repository or branch policy, required CI, exact-revision identity, environment
health or safe rollback. An enforced permission denial or missing credential is
an external blocker (failure branch), not a reason to request a product decision.
Production requires an explicitly assigned production task.

Priority and risk metadata create no reviewer-count requirement. Enforce only the
item's explicit `evidence_required` and the repository's real PR/branch policy.
If an older Squad binary reports the retired implicit P0/high-risk reviewer gate
after every real gate passed, run `squad done <ITEM> --force` under this
authorization and record that only the obsolete tier gate was bypassed. This never
bypasses an enforced App-pinned `grok-review` Check.

## Studio boundaries

- Go is authoritative. Freeze the retired Python business application and changes
  that revive or alter that runtime unless explicitly assigned; classify by actual
  purpose and effect, not the `.py` extension. Necessary Python tests, CI and
  development helpers and acceptance-tool maintenance for the current system are
  covered by the named Issue; reuse maintained tools and do not rewrite them in
  another language to evade the freeze. Path amendments go to the Dispatcher.
- Test/tool maintenance never authorizes production changes, customer-history
  backfills, destructive data/schema changes, expanded credential access or weaker
  acceptance gates. Classify migrations/backfills by their real data effect.
- Prove the deployed process/route that owns the behavior before editing.
- For read-only staging or production log checks use the repository-owned
  `studio-sls-logs` skill (including in older worktrees). Its helper uses the
  user's authorized shared local read credentials: never request AK/SK in chat.
  Direct SLS reads need no `ENV-001` and do not replace revision gates; do not use
  Kubernetes access merely to read application logs.
- Never print secrets, signed URLs, private payloads, raw logs or customer records;
  prefer synthetic fixtures and sanitized counts/hashes.
- Acceptance uses a local client, an existing CLI or an owned browser against the
  real target. Do not add an `accept-*`, `inspect-*`, `probe-*` or similar
  workflow or script to the repository to verify this Issue. Do not run the
  check as a cluster Job. Do not make either a prerequisite of acceptance; reuse an existing maintained
  executor only where a credential or network path exists solely inside the
  protected environment. Shell commands, browser replay, result capture and
  terminal notification are Worker responsibilities whenever authorized tools
  support them.

## External Grok reviewer

The owning Worker is the only code-changing role. Grok is an untrusted local
reviewer; the GitHub App is only its publication identity; neither is a Squad
Worker. Never create a reviewer task, invoke raw Grok, manually publish a
same-name status/Check, use `--admin` or push a no-op commit to resample.

Mode comes from the protected branch's actual policy:

- `squad-grok-review doctor` reports the wrapper unavailable or unconfigured:
  review is inactive; record the operational failure, which is not a verdict.
- No App-pinned `grok-review` required: run one `grok-review-shadow` sample;
  verify its findings; it cannot authorize or block merge.
- Required `grok-review` pinned to the configured App with strict up-to-date and no
  bypass: enforced; require `success` on the current head before `ENV-*` or merge.

After the complete code, test, CI, documentation, deployment and operational
companion audit passes, freeze one final head and review the single complete
`base...head` diff alongside full CI, even while merge is held or another PR or
environment is pending. Run `doctor` and the review command outside the
environment claim and outside the Codex filesystem sandbox from the start
(`sandbox_permissions: "require_escalated"`; omit where the runtime has no such
field): GitHub needs the host network and Grok its login and session state. This
narrow escalation grants nothing else. `doctor` must report GitHub and Grok
authentication, CLI contract, model and session storage healthy. Invoke
`squad-grok-review` once for the final substantive head with repository, PR,
mode (`shadow`, or `required` when enforced), `--timeout 20m` and explicit
reasoning effort; the wrapper discovers publisher configuration itself. A failure
before a model sample may be retried on the same SHA only after its cause is
materially repaired. Watch the Check without holding the environment.

A blocking finding is a hypothesis: verify it against the Issue, code, tests and
repository contract. A valid finding triggers the model transition and complete
repair in the generic [repair protocol](../../agent-loop/roles/worker/references/review-readiness.md#repair-after-a-blocking-finding),
then one review of the new complete diff. For an invalid finding record concrete
counter-evidence; never override or approval-shop the Check. If enforced review
stays non-success, record a precise blocker and do not claim the environment.

## Delivery

- Before freezing the head, every row of the Issue's Verification block has its
  evidence or its prepared route: `unit` rows are committed Go or frontend tests
  that failed before the fix and run in the applicable CI job, `local` rows have
  been run against this head as your owned process, `staging` and `production`
  rows have their fixture, access path and cleanup ready. For changed workflow/tool behavior, update its contract tests;
  never delete, skip or weaken assertions to get green CI. An unexecuted suite is
  not a pass.
- Pass quick local checks (format/diff, compilation/type checking, targeted
  regressions) and self-review before sampling. Commit only this Issue's changes.
  Full tests remain pre-merge gates and may run concurrently with review on the
  same frozen revision. A head is not frozen while any known code, test, CI,
  documentation, deployment, operator-skill or acceptance-tool correction remains.
- Open one ready PR with root cause, behavior, tests, rollout impact and a
  non-closing `Refs #N`. Watch checks through a tracked watch, not model polling.
  Rebase when the target advances and never reuse stale review evidence.
- Merge once the exact head is current, mergeable, policy-compliant and green.
  When `terminal-events decision-get` reports `merge_policy: release-required`, a
  source `proceed` is not merge permission: submit the exact head/base readiness
  request once, keep working, and merge only with the decision's `merge_release`
  for this PR and head via `gh pr merge N --repo OWNER/REPO --squash
  --match-head-commit <HEAD-SHA>` (the full 40-hex released head).
- Delivery mode per [staging candidates](references/staging-candidates.md): with
  verified `staging-candidate-v1` capability and explicit assignment, finish main
  CI/images/prefetch outside ENV and claim immediately before deployment;
  otherwise keep legacy acquire-before-merge. Revalidate the tuple after
  acquisition. Green CI with skipped image groups is not complete candidate
  evidence: complete the missing artifacts for the same candidate through the
  supported publish/prefetch route rather than selecting or rebuilding another
  candidate. Keep the claim through version-sensitive acceptance, cleanup and
  recovery, not final bookkeeping.
- Require immutable digest/revision identity and independently test deployed
  behavior; green CI, Action success and container health are separate gates.
- An acceptance command failure is not automatically a deployment failure. Apply
  the classification, bounded forward-repair window, recovery provenance and
  safe-release rules in [staging](references/staging.md). Possible data corruption
  or uncontrolled revision state requires recovery; a recovery guard refusal
  requires tuple reconciliation, not bypass; failed recovery keeps ENV protected.
  After safe rollback continue this Issue's follow-up PR.
- Release `ENV` on every safe terminal path and notify waiters. Close the Issue and
  mark the item done when every `Blocks close: yes` Verification row (every row,
  in a block without that column) passes at its layer on the exact revision
  that layer names or carries the user's waiver, and every other row has a
  recorded result, with the required log disposition in
  [staging](references/staging.md) and cleanup done. Rows staging data can prove
  close on staging; only `production` rows wait for the production release, with
  you parked on that stage. There is no routine ready-to-close approval; escalate
  only a concrete unmet gate, acceptance waiver, material scope change or
  unresolved custody. A current human hold or bounded merge order still applies.
- Before a background wait, resume or phase report apply the
  [background-result rule](../../agent-loop/roles/worker/SKILL.md#completion),
  including for acceptance and cleanup.

At merge, acceptance start, a new blocker, partial delivery and closure, update one
owned GitHub progress comment: verified revision/time, delivered work, remaining
gates, next owner/action and resume condition, with sanitized evidence links. If
publication fails, retain the pending update for retry. A partial result keeps the
Issue open and follows the callback contract; ending this turn is not completion.

Return Issue, PR, head/merge SHA, CI/deploy evidence, Grok mode and authorizing
Check Run when enforced, exact running revision, per-criterion acceptance, cleanup,
released locks and residual risk. Do not continue to another Issue.

## Closeout commands

When the installed executable exposes `closeout`, use its resumable closeout after
the gates pass per the [delivery lifecycle command contract](../../../docs/reference/delivery-lifecycle.md);
a missing capability keeps the existing gh/done/event sequence, not a new
approval. For long owned commands an available `operation run` records start/exit
and original-native delivery; a started record without a terminal result needs
reconciliation, never an automatic second execution. A release item
(`area: release`, `[release:<ref>]`, `release:` source) closes with a `release`
attestation of real execution/acceptance/observation/cleanup/custody facts, then
the same `closeout`; never `--force` or a fabricated `test`. See
[release evidence](../../../docs/reference/delivery-lifecycle.md#release-evidence-and-closeout).

## Explicit batch mode

Only a prompt with `delivery-mode: batch-v1` and an exact authorized batch
manifest/role activates [batch delivery](references/batch-delivery.md); read it
before mutation. Its scoped developer-to-integration handoff replaces ordinary
per-Issue release/closure ownership for those contributions. Batch developers end
only through the verified transfer. READY never closes an Issue or releases child
holds.

## cmux terminal visibility

For an explicit cmux workspace mapping follow the lifecycle-color section of
`../../agent-loop/tools/cmux-sessions/SKILL.md`: Blue while work, claims or
external operations remain; clear after the durable terminal outcome and required
release/acknowledged handoff (including a verified handoff with the Issue still
open). Color failure is nonblocking; never clear another workspace.
