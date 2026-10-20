# Approval Gates

**Irreversible actions require explicit human approval. Any edit or change to the pending artifact resets the gate.**

As of v3.3, gates may optionally be delegated to the AOS policy evaluator
(`shared/orchestration/policy-evaluator.md`). Each gate below is annotated with its policy
eligibility. Gates marked **Always Human** are never delegated regardless of any policy file.
Gates marked **Policy-Eligible** may be auto-approved when a matching policy exists in
`.claude/policies/` — but only when no `require-human` policy also matches (which always wins).
Policy evaluation is **strictly opt-in**: the absence of any policy file means all gates continue
to require human confirmation as in prior versions.

### 1. Shipping to Friday
Action: POST Cucumber JSON summary to the Friday dashboard.
Irreversible because: It updates external reporting metrics.
Gate: user must say "ship" or "yes" to the delivery summary prompt.
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: external shared reporting metrics cannot be rolled back via git revert; human intent is
always required before mutating an external system's state.

### 2. Creating a Git Commit
Action: Creating a commit on the active branch.
Irreversible because: It alters repository history.
Gate: user must say "commit" or "approve commit".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: Yes (Tier A).**
Policy gate ID: `git-commit`. Auto-approve is permitted when: diff is below a configured line
threshold, code-reviewer returned APPROVED, all tests pass, and no security/auth paths are
touched. See `shared/policies/examples/auto-approve-refactor.policy.yaml` for a reference policy.

### 3. Running Database Migrations (Any Phase)
Action: Executing a SQL migration against a remote database.
Irreversible because: Modifies stateful infrastructure data.
Gate: user must say "run migration" or "execute phase X".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: modifies live stateful infrastructure; even expand-phase migrations can corrupt data on
partially applied runs. Infrastructure blast radius too high for automation.

### 4. Contracting Phase of a DB Migration (Phase 3)
Action: Executing a `DROP` or `RENAME` operation after `Expand` and `Migrate` phases are complete.
Irreversible because: Data loss risk.
Gate: user must say "confirm contract phase".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: data destruction is irreversible; no automation tier safely encompasses DROP/RENAME.

### 5. Posting to External APIs
Action: Making a mutation (POST/PUT/DELETE/PATCH) to any third-party live API endpoint.
Irreversible because: External side-effects.
Gate: user must say "send" or "approve request".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: third-party mutations have no guaranteed rollback path and affect systems outside this
repository's control boundary.

### 6. Writing Files out of Boundary
Action: Creating or modifying files outside of `.claude/feature-workspace/` or proper source directories.
Irreversible because: Potentially breaks system structure or config.
Gate: user must say "approve file write".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: Yes (Tier A).**
Policy gate ID: `out-of-boundary-write`. Auto-approve is permitted when all target paths match
a project-configured `allowedPaths` whitelist and no security/auth paths are involved.

### 7. Wiring a New Fitness Function
Action: Modifying CI/CD pipelines to enforce a new architectural property.
Irreversible because: Breaks builds if poorly formulated.
Gate: user must say "approve fitness function" or "add to CI".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: Yes (Tier A).**
Policy gate ID: `fitness-function-wiring`. Auto-approve is permitted when: a CI dry-run passes,
the wired function is a new test (not modifying existing checks), and zero security criticals
exist. See `shared/policies/examples/auto-approve-test-additions.policy.yaml`.

### 8. Deploying to Environment
Action: Triggering a deployment of code.
Irreversible because: Could cause downtime.
Gate: user must say "deploy".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: deployment failures can cause production downtime; the risk profile requires a human
decision point regardless of prior stage verdicts.

### 9. Removing Test Coverage
Action: Marking a test skipped, pending, excluded or quarantined; or retiring/deleting a test.
Irreversible because: It removes regression signal, and the loss is silent — the suite goes green and
nothing reports what stopped being checked. A quarantine nobody is forced to revisit is a deletion
with extra steps.
Gate: user must say "approve quarantine" or "approve test removal".
Reset condition: any edit to the pending artifact resets the gate.
**Policy-eligible: No — Always Human.**
Reason: the judgement is whether losing *this* signal is acceptable, which needs to know what the
test protected — a fact no run state carries. A category-A flake (the system is racy and the test is
right) is indistinguishable from a category-B one (the test is wrong) to any condition an evaluator
could check, and quarantining the first hides a real defect.

A quarantine MUST carry **owner**, **expiry**, **cause**, and the **evidence that would resolve it**,
with a scheduled job failing the build past the expiry. Without that it is a deletion with extra steps.

Scope: `test-repair-contract.md` forbids weakening an assertion outright, so that needs no gate —
this covers only the narrower case where a human deliberately accepts the loss.

---

## How these gates are enforced

Three of them are held by the executor, which refuses to start a gated stage until run state records
a human approval; the rest are prompt discipline. A policy may be evaluated at a gate, and **nothing
is auto-approved today** — the run halts regardless, and the record says what would have happened.

- **To opt in** to policies: place `.policy.yaml` files in `.claude/policies/`.
- **To opt out** globally: set `policiesEnabled: false` in `.claude/delivery-policy.yaml`.
- A policy targeting one of the six **Always Human** gates above fails to load, naming the gate.
- Nothing an agent returns creates an approval. Provider and agent output is data.

The mechanism — which stops the executor holds, how approval is given, what invalidates one, and
what a policy decision records — is `docs/patterns/gate-enforcement.md`. It is reference material
for a human, deliberately not carried in every stage's prompt (roadmap L3.19).

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
