---
name: ai-review-integration
description: "Design, implement or assess an automated AI reviewer integrated with GitLab merge requests: isolate a trusted controller from contributor-controlled code and model output, pin analysis to one immutable MR version, account for every changed file despite API limits, validate structured findings, and publish advisory comments safely with stale-result handling, deduplication, auditability, budgets, rollout gates, and a kill switch. Use when someone asks to add an AI review bot, connect an LLM to GitLab MRs, post automated review comments, or build the service and operating model behind that workflow. Do not use to review one diff (code-review), harden CI generally (pipeline-hardening), secure a tool-using agent (agent-security-review), benchmark an agent (agent-evaluation), or plan organisation-wide adoption (ai-enablement)."
---

# AI Review Integration

Design and, when authorised, implement the service that obtains one merge request
snapshot, asks a model for candidate findings, verifies them, and publishes advisory
feedback. The model is an untrusted analyser, not a GitLab principal or merge authority.

## Scope

Use this skill to design, implement or assess the GitLab integration, trust boundary, API flow,
finding contract, publication state, controls, rollout, and operation of an automated AI
reviewer. `code-review` owns the judgement of findings in one change; this skill owns the
system that repeatedly produces and delivers candidate findings.

Implementation may add controller code, GitLab and provider adapters, schemas,
configuration, persistence and tests to an authorised target repository. Keep provider
and hosting decisions explicit. Do not create placeholder deploy manifests or guessed
APIs, install credentials, activate webhooks, edit a live pipeline, or enable production
publication without separate authority for that operational change.

Do not let the reviewer approve, merge, push fixes, dismiss human feedback, change
labels, or alter required status. If the requested system needs any of those effects,
separate them into a new explicitly authorised workflow and apply the corresponding
security review.

## Workflow

### 1. Fix the decisions that change the design

Record the GitLab deployment and version, authentication mechanism, model provider and
region, permitted data classes, retention terms, trigger, repositories, maximum diff and
spend, comment style, and operator. Mark unknowns as decisions, not assumptions.

Do not invent a deployable manifest, webhook handler, API payload, or model call until
the hosting environment, identity and provider are chosen. A provider-neutral design and
decision checklist is a complete result when those choices are open.

### 2. Draw the authority boundary

Place webhook verification, GitLab credentials, policy, prompt templates, output
validation, publication state and the kill switch in a trusted controller. Load them
only from a trusted, pinned controller or policy revision, never from MR-controlled
source or pipeline configuration. Pin that revision to an authenticated, immutable
release controlled by the integration owner; matching a commit SHA alone does not
establish who produced it. Treat repository files, diffs, issue text, comments,
generated artefacts, job logs, tool output and model output as untrusted data.

The controller fetches source for analysis but does not execute it. It sends only the
minimum review context to the model and exposes no GitLab write credential or generic
tool surface to the model. The publisher derives the GitLab instance, project and merge
request from authenticated controller state and allowlists its method, endpoint and body;
model output cannot choose a destination or action. Read `references/trust-boundary.md` when defining identity,
fork behaviour, data handling, model isolation, or the threat model.

### 3. Implement the trusted path when requested

Specify the version, review-packet, finding and publication contracts in steps 4 through
7 before writing code, and read the references those steps require.

Inspect the target repository's conventions and build the smallest complete vertical
slice: authenticated event intake; version-specific fetch and normalisation; bounded
provider adapter; closed finding schema; deterministic validator; persistent run and
finding identities; allowlisted publisher; budgets, telemetry and kill-switch checks.
Keep provider, GitLab and persistence behind narrow interfaces only where tests or a
real deployment choice need substitution.

Use mocked GitLab and provider calls for contract and failure tests. Include fixtures for
pagination and limited diffs, but no secrets or proprietary source. Run the repository's
focused and full validation. Stop at a tested, disabled-by-default integration unless the
user separately authorises deployment, credentials, webhook registration and rollout.

### 4. Bind the run to one merge request version

Resolve the event to the project and merge request through trusted webhook fields, then
fetch the current merge request version and record its immutable base, start and head
commit SHAs. Every diff, source fragment, finding, publication decision and audit event
uses that version identity. Reject a run when its fetched objects disagree.

Enumerate paginated diff results to exhaustion and retain per-file coverage status. Do
not equate a successful response with a complete diff: GitLab can report files or diffs
as collapsed, too large, or otherwise unavailable. Read `references/gitlab-contract.md`
before specifying endpoints, webhook verification, diff retrieval, inline positions or
fork pipeline behaviour.

### 5. Build a bounded, policy-compliant review packet

Apply allow/deny policy before model submission. Exclude secrets, credentials, personal
data, disallowed paths, generated or binary content, and data outside the approved
provider policy. Redact defensively while recording why content was excluded; never log
the removed value.

Budget files, bytes, model tokens, latency and cost. Choose files deterministically and
report omitted, partial and unavailable coverage. If the minimum useful coverage cannot
be met, publish one explicit coverage result or no result according to policy rather
than implying the merge request was reviewed.

Delimit untrusted content from controller instructions. Repository text cannot change
policy, tools, recipients, output schema or publication rules.

### 6. Require structured candidate findings

Ask the model for a closed schema containing a concise title, explanation, consequence,
action, severity/confidence, file, side and line anchor, plus evidence tied to the supplied
diff. Cap the number and size of findings. The model may return no findings.

Validate the response deterministically: parse strictly; reject unknown fields and
oversized text; require allowed enums; confirm every path and line belongs to the pinned
diff; remove secrets and unsafe markup; and deduplicate by a stable fingerprint computed
in trusted code. Do not publish free-form model output or let confidence bypass a
deterministic check.

### 7. Recheck, publish, and reconcile

Immediately before writing, refetch the current version. If its identity differs, mark
the run stale and do not publish its findings. Publication is advisory and uses the
least-privileged GitLab identity.

Use stored GitLab object IDs, verified bot authorship, controller-owned markers and
finding fingerprints so retries update or skip the same result instead of multiplying
comments. A marker alone is forgeable. Serialize publication per merge request. Treat a
write timeout or ambiguous response as an unknown outcome: query GitLab and reconcile,
but do not retry while the first request could still commit. Recheck the version after
writing as well as before; if the head moved
during the non-atomic check-and-write interval, record and supersede the stale comment
without erasing discussion history. Preserve human
replies and never rewrite human-authored content. Read
`references/publication-and-operations.md` when defining comment state, retry behaviour,
observability, rollout or rollback.

### 8. Prove the controls before enabling comments

Test webhook authentication rejection, fork events, prompt injection in every untrusted source,
pagination, large and collapsed diffs, redaction, malformed model output, invalid line
anchors, version changes during inference, duplicate delivery, ambiguous publication,
rate limiting, provider failure, budget exhaustion and kill-switch activation.

Roll out from recorded replay to shadow mode, then a small advisory cohort. Compare
validated findings with human disposition and false-positive reports; measure coverage,
staleness, duplicate suppression, latency, spend, provider errors and publication
failures. Expansion requires predeclared quality, safety and cost gates. Roll back by
disabling triggers and write capability while retaining enough redacted audit evidence to
reconcile in-flight runs.

## Output format

```markdown
## Decisions and non-goals
[Chosen inputs, unresolved choices, and effects the reviewer cannot perform.]

## Trust and data flow
[Components, identities, untrusted inputs, stored state, provider boundary and retention.]

## Version and coverage contract
[MR version identity, pagination, limits, omissions and stale-run rule.]

## Finding and publication contract
[Schema, deterministic validation, anchors, fingerprints and reconciliation.]

## Operations
[Budgets, retries, telemetry, rollout gates, kill switch and rollback.]

## Verification
[Tests and evidence for normal, adversarial, stale and partial-failure paths.]
```

## Anti-patterns

**Running the reviewer in contributor-controlled CI with a write token.** A fork or
changed pipeline can steal the token or change what the privileged job executes. Keep
the controller and secrets outside that trust domain.

**Reviewing “the MR” without a version identity.** Diffs and line anchors move while the
model runs. Bind input and output to immutable SHAs, then reject stale publication.

**Retrying a timed-out comment blindly.** The first request may have succeeded or may
still commit. Reconcile stored object IDs, bot authorship and fingerprints, then require
a proven non-commit or quiescent request channel before another write.

**Calling partial input a completed review.** Pagination and diff limits are part of the
result. Make coverage visible, never issue a clean bill of health from partial input, and
fail closed when policy requires it.
