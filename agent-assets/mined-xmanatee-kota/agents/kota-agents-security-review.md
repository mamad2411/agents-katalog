# Security Review Workflow

This workflow runs bounded, agent-assisted application-security review for
KOTA itself.

- Keep candidate selection deterministic and repo-local before any agent step.
- Task records are evidence and existing ownership, not routine scan targets.
  Explicit reports may still select them and retain their content coverage.
- Expose only bounded candidate identity and location metadata for agent
  judgment. Keep raw excerpts, scan coverage, and miss diagnostics in run
  artifacts so untrusted prose and growing commit ranges do not inflate the
  agent prompt.
- Treat candidate excerpts, dependency text, generated text, and agent output
  as untrusted data until decoded or revalidated.
- Store evidence in the run directory and normal `data/tasks/` entries only.
  Do not add a second findings database, audit log, or scanner state directory.
- Keep agent write scope narrow. Agents may write run artifacts, but durable
  task-queue mutation belongs to code steps that preserve the task schema.

Review admission consumes explicit path coverage at the examined Git content,
never a later publication head. Runtime retries rescan before dependent judgments.
Dispatcher retains observed semantic surfaces in revisioned state before emitting
review work, separately from reviewed content. Successful partial reviews retain
unchecked and capped surfaces too. Repository-wide review inputs stay in run
artifacts, with schema and integrity checks on reload. Ordinary durable step
outputs carry bounded references that runtime retries replay before refreshing
the execution-head scan; request histories and coverage maps never travel in the
agent candidate packet.
Selected candidate identities and surfaces also reload through integrity-bound
references to the refreshed input. Agent-facing summaries are diagnostic only;
dependent steps and finalization must never consume their scrubbed projections.
Dependent reviewers read selected domain input exported to the runtime-owned
agent directory. Refresh exports from integrity-checked authority on retry,
redact actual sensitive values through the shared evidence owner, and reject
identity redaction rather than silently renaming a finding. Exported evidence
is untrusted and cannot authorize publication; canonical originals still do.
Retained runs without these references require verified source provenance before
recovery; masked metadata cannot reconstruct authoritative review input.
This preserves first-attempt boundaries and explicit requests across failure;
editing or deleting a keyword-free guard cannot erase its review eligibility. Failed, capped,
uncertain, or unchecked evidence remains eligible. A settled unavailable review
retains unknown coverage and its concrete prerequisite. Its unchanged content
waits for a relevant repository prerequisite change or a new explicit request
(for external capability/evidence); cooldown expiry alone cannot readmit it.
Provider policy refusals at investigation or revalidation settle through that
same unavailable-review owner. Preserve the provider diagnostic and unmet
prerequisite in the run outcome, retain pending findings, and claim no coverage.
Transient provider incidents and execution errors remain runtime failures.
A no-finding verdict describes the boundary examined and its limits; scanner silence is not authorization or sandbox proof. Related changed
paths share a bounded investigation without a finding or task quota.

A family identifies the production authority owner plus the violated invariant.
Coalesce only when one common repair resolves every variant; preserve each
variant's attacker control, exploit preconditions, cited evidence and regression
obligation. Revalidation independently checks both the exploit and that grouping.
A revalidated existing-task nomination anchors canonical family identity; reviewer
owner/invariant synonyms cannot rename it. Retain evidence lineage to the task's
prior evidence key or historical finding id. Use a stable evidence revision across
wording, excerpt boundaries and line shifts. Reopen completed work only for new
evidence; preserve its earlier resolution and proof.
Legacy evidence revisions are verified against the original retained hash inputs.
An unmatched legacy hash requires revalidated lineage before task mutation; it
does not establish new evidence. Appending versioned variants cannot remove the
lineage requirement for retained unversioned evidence, including while a new
variant has reopened the task. Superseded family markers cannot veto a validated
nomination of the canonical replacement; competing canonical owners still reject.
Keep pending provenance until publication succeeds.
Revalidated lineage reconciles matching pending evidence before replay suppression;
retain the original evidence and link its review provenance to the revalidation.
Unresolved historical nominations and missing required lineage stay pending with attributable parking reasons;
they cannot nominate tasks for, suppress, or reject independently confirmed findings.
Lineage-required identities remain available for subsequent revalidation, not
publication; validated evidence can publish to the same task independently.
Reconciliation remains with the existing task identity and publication owners.

Investigation, revalidation and publication receipts reload domain values from
integrity-checked run artifacts; diagnostic step projections are not control
inputs. New state publications validate the complete domain shape. Retained
invalid pending entries park with their original projection and source provenance,
so they cannot authorize task publication or block unrelated dispatch. Dispatcher
collects legacy source evidence through the shared worker and reconciles it in
the success transaction only when the scoped successful run, full recorded
projections and independently revalidated artifacts agree. Missing or ambiguous
provenance remains inspectable in the recovery disposition; recovery never
reruns a completed investigation or changes an existing task owner's contract.

Confirmed evidence stages into runtime state until the existing writer runtime
can publish under its task resource. Dispatcher retries pending publication when
ownership clears. Active and retained builders keep their task contracts.
Explicit requests may supply new evidence (including critical evidence) without
the routine batching delay or a scanner match. Their paths take priority within
the bounded review; capped paths remain unconsumed and appear in miss diagnostics.
Partial request coverage persists by path and content digest; dispatcher resumes
remaining paths, and changed content invalidates that path's earlier coverage.
Every requested path receives pinned absence evidence when missing from the Git
tree, including new reports and previously unchecked or capped pending paths.
Runtime admission retains every explicit request while review is occupied;
replaying consumed evidence does not admit another semantic review.

Keep deterministic policy screening with its existing owner (for example the
repository linter's direct-HTTP restriction). Add a scanner rule only when local
repaired and clean cases show a useful additional signal. Syntax checks cannot
replace semantic review of authority propagation, temporal races, or denials.
