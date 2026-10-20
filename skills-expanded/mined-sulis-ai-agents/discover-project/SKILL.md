---
name: discover-project
description: Set up Sulis for a project by minting its Project entity. Run this once when adopting Sulis in a new repo.
canonical_source: plugins/sulis/instances/discover-project/workflow.jsonld
canonical_workflow_ulid: dna:workflow:01KT1WDSCVRWFW00000000000A
---

# /sulis:discover-project

> Minting a Project entity for the repo you're in. One command, one
> outcome: `.sulis/projects/<slug>.jsonld`.

This skill is the imperative side of Path A for the discover-project
Workflow. Every annotation `<!-- canonical:step:<name> -->` below
binds a paragraph to the canonical Step defined in
`plugins/sulis/instances/discover-project/steps.jsonld`. The drift
detector enforces this binding at PR time — if the canonical and the
imperative diverge, CI fails. That is the load-bearing contract for
ADR-001.

The skill orchestrates the 5 phases (Detect → Infer → Ask → Mint →
Verify) by calling into the Python helpers authored by WP-002
through WP-007. Every founder-facing prompt is plain English;
structured trace lines go to stderr; the JSON envelope on stdout
matches the marketplace's existing `{ok, data}` shape.

## Flags

- `--update` — re-discovery mode. The skill reads the existing
  `.sulis/projects/<slug>.jsonld`, runs Detect + Infer fresh, and
  produces a per-field diff for the founder to confirm one field at
  a time (per ADR-005). Without `--update`, an existing entity
  triggers the entity-already-exists failure mode.
- `--path <sub-path>` — monorepo mode. Scopes the Detect phase to a
  sub-path of the repo and derives the project slug from that
  basename via `slug_from_monorepo_path`. Without `--path`, a
  monorepo with a sibling Project already minted raises the
  monorepo-sibling-collision failure mode.
- `--source-repo <org/name>` — override for repos with no git remote
  (MUC-006). The Detect phase normally derives this from the git
  remote URL; the flag lets a founder run the skill against a clone
  that hasn't been pushed yet.

## Pre-flight: stale .tmp sweep

<!-- canonical:step:write-project-entity -->
Before any phase runs, the skill invokes `stale_tmp_sweep` against
`.sulis/projects/` to remove any leftover `*.tmp` files from a
prior session that was cancelled mid-write. This is the protection
against the SIGINT-mid-write race in MUC-002 (see TDD §Armor
§Atomic write semantics) — without the sweep, a stale `.tmp` from a
cancelled run could collide with this run's atomic write.

The sweep is silent on success. If it cannot remove a stale file
(permissions, disk error), the skill surfaces the OSError verbatim
to the operator and terminates — no Phase advances on a degraded
pre-flight.

## Phase 1 — Detect

The Detect phase reads the consuming repo's filesystem and gathers
the structured facts the Infer phase needs as context. Every read
is deterministic; no LLM involvement.

<!-- canonical:step:read-repo-root -->
Read the consuming repo's `.git/` state via
`LocalFilesystemInspector.read_root`. Three outcomes:

- A `.git/` directory with a configured remote → pass the
  `{is_git, has_remote, remote_url, primary_branch, repo_root}`
  payload to the rest of Detect.
- <!-- canonical:failuremode:non-git-directory --> No `.git/` directory at all → raise the non-git-directory
  failure mode (MUC-001) and terminate. Founder-facing message
  comes from FailureMode `01KT1WFM01N0NG1TD1R000000A`.
- <!-- canonical:failuremode:git-no-remote --> `.git/` exists but has no remote → raise the git-no-remote
  failure mode (MUC-006) unless `--source-repo` was provided. If
  the override is present, accept it as the canonical remote
  identity for the rest of the run.

<!-- canonical:step:read-package-manifests -->
Enumerate `package.json`, `pyproject.toml` (and, when present,
Cargo.toml and Gemfile) under the repo root — or under the
`--path` scope if that flag was set. Missing manifests are not an
error; a consumer might be a pure shell-script repo or a Terraform
module. The phase produces a union of whatever was found, keyed by
manifest filename.

<!-- canonical:step:read-ci-workflows -->
Enumerate `.github/workflows/*.yml` and `.gitlab-ci.yml` under the
repo root (or `--path` scope). For each workflow found, capture
its path, declared name, and trigger list. An empty list is a
legitimate state — many consumers have no CI configured yet.

<!-- canonical:step:read-repo-contract -->
Read `.sulis/repo-contract.yml` if present; skip silently if
absent. Also read README.md and CONTRIBUTING.md as plain-text
context for the Infer phase's prompt. Missing files are
non-errors.

Structured log line at phase exit:

    [discover-project] Detect phase: collected N manifests, M CI workflows, contract={present|absent}

## Phase 2 — Infer

The Infer phase is the only probabilistic Step in the Workflow.
It calls an LLM with the Detect findings as context and asks for
proposed values for every configuration field the entity needs.
Token budget is capped at 10,000 per NFR-002 (the budget number
lives in the inferrer module — operator-facing prose does not
quote it).

<!-- canonical:step:propose-configuration-values -->
Call `LLMConfigurationInferrer.infer(detected, token_budget=...)`.
<!-- canonical:failuremode:token-budget-exceeded --> On `TokenBudgetExceeded`, swap in `NullConfigurationInferrer` for
the remainder of the run; the Ask phase will then prompt the
founder for every field directly. On any LLM-unreachable error
(timeout, transport, auth), apply the same fallback (NFR-006).
The swap is silent from the operator's perspective — they see
more prompts in Ask, not a stack trace.

Structured log line at phase exit:

    [discover-project] Infer phase: proposed N values; mode={llm|null-fallback}

## Phase 3 — Ask

The Ask phase is where the founder confirms or overrides every
proposed value, and supplies the fields the Infer phase couldn't
or shouldn't have populated (Project name, brand-scope,
description — the authoritative-to-the-founder fields).

<!-- canonical:step:confirm-or-override-inferences -->
<!-- canonical:failuremode:inferred-value-rejected -->
For each inferred value, follow the prompt template at
`_prompts/confirm-or-override.md`. The skill reads the template
verbatim and substitutes the field name + proposed value; the
operator either presses Enter to accept or types a new value to
override. Record the founder's choice for the Mint phase. A
rejected proposal is itself a recorded outcome — the
inferred-value-rejected failure mode is the bookkeeping label
for "founder said no to the LLM's guess" (per MUC-004); the
override value the founder typed becomes the canonical value.

<!-- canonical:step:gather-ambiguous-fields -->
For fields the Infer phase did not populate (or that the founder
must speak to directly), follow the template at
`_prompts/gather-ambiguous-fields.md`. If `--update` was passed
on the command line, instead follow `_prompts/per-field-diff.md`
and present the diff between the existing entity and the freshly-
inferred values one field at a time.

<!-- canonical:failuremode:mid-flow-cancellation -->
Cancellation safety: at any prompt, Ctrl-C is a legitimate exit.
The mid-flow-cancellation failure mode (MUC-002) covers every
phase where the founder might Ctrl-C; here in Ask, the response
is a clean abandon — no partial entity exists yet, so there is
nothing for the pre-flight sweep to clean up on the next run.

Structured log line at phase exit:

    [discover-project] Ask phase: confirmed K fields; gathered J ambiguous

## Phase 4 — Mint

Mint composes the Project entity from confirmed values + gathered
ambiguous fields + computed identifiers, then writes it atomically
to disk.

<!-- canonical:step:write-project-entity -->
Compose the entity. Specifically:

- `belongs_to_tenant` is computed as
  `Sha256CrockfordTenantDeriver().derive_consumer_tenant(<org>/<name>)`.
  The `<org>/<name>` pair comes from the git remote (or
  `--source-repo`).
- `release_workflow_ref` is set to the canonical marketplace
  release-train Workflow ULID
  (`dna:workflow:01KT0RTRA1NWFW00000000000A`). This is the one
  cross-tenant reference in the Project entity (per ADR-002) — the
  drift detector accepts it when invoked with
  `--cross-tenant-refs-allowed-for release_workflow_ref`.
- The slug is derived via `slug_from_project_name` from the
  founder-confirmed Project name, OR via `slug_from_monorepo_path`
  when `--path` was passed.

Collision detection runs before any write touches disk:

- <!-- canonical:failuremode:entity-already-exists --> If `.sulis/projects/<slug>.jsonld` exists AND `--update` is
  absent → raise the entity-already-exists failure mode (MUC-003).
- <!-- canonical:failuremode:monorepo-sibling-collision --> If a sibling Project exists in `.sulis/projects/` AND `--path`
  was not passed → raise the monorepo-sibling-collision failure
  mode (MUC-007). The Project is collapsing what should be two.

Then install the SIGINT handler via `install_sigint_handler` and
invoke `write_project_entity` for the atomic write — temp file +
fsync + rename. Mid-flow Ctrl-C between these two calls is the
window the pre-flight sweep at the top of this skill cleans up
on the next run (MUC-002).

Structured log line at phase exit:

    [discover-project] Mint phase: writing to .sulis/projects/<slug>.jsonld (atomic)

## Phase 5 — Verify

Verify is the load-bearing structural acceptance — it runs the
drift detector against the just-written entity and rolls back if
anything fails to resolve.

<!-- canonical:step:run-drift-detector-on-mint -->
<!-- canonical:failuremode:unknown-workflow-ulid -->
Call `verify_and_roll_back_on_failure(entity_path)`. The verifier
invokes `check-canonical-drift.py` scoped to the new entity. On
`DriftVerifyFailed`, the failure surface is MUC-005: the verifier
removes the just-written entity (the rollback) and re-raises with
the drift detector's stderr captured verbatim. The skill surfaces
that stderr to the operator unmodified — the diff between
canonical expectation and the actual write is the diagnostic. The
unknown-workflow-ulid failure mode is the specific drift surface
this Step handles — a `release_workflow_ref` that doesn't resolve
in the marketplace's Workflow catalogue.

Structured log line at phase exit:

    [discover-project] Verify phase: drift detector PASS

## Output envelope

On success, the skill emits exactly one line on stdout (suitable
for `jq` or another marketplace skill to consume):

    {"ok": true, "data": {"entity_path": "<path>", "tenant_ulid": "<ulid>", "tokens_consumed": <int>}}

On failure (any phase raises a FailureMode), the skill emits:

    {"ok": false, "error": {"failuremode_id": "<ulid>", "user_message": "<verbatim from FailureMode>"}}

The `user_message` is the founder-facing prose carried by the
FailureMode entity in `failuremodes.jsonld` — the skill never
synthesises an error message inline. Every error the operator
sees is a deliberate, reviewed phrase.

## Tests this skill passes

The conformance evidence for this skill lives in two places:

- `plugins/sulis/scripts/tests/unit/test_discover_project_skill_conformance.py`
  — 11 structural assertions (frontmatter shape, annotation set
  matches canonical Step set, every phase helper referenced, all
  three flags described, per-phase structured log lines, JSON
  envelope shapes, pre-flight sweep ordering, prompt fragments
  referenced, phase sections in canonical order).
- `plugins/sulis/scripts/tests/unit/test_check_canonical_drift_discover.py::test_drift_detector_passes_against_skill_md`
  — the n=2 dogfood acceptance. Invokes `check-canonical-drift.py`
  with `--instance-dir plugins/sulis/instances/discover-project`
  and `--yaml-path` pointing at this file. Exit 0 is the
  load-bearing assertion for ADR-001.
- `plugins/sulis/scripts/tests/integration/test_discover_e2e.py`
  — authored in WP-010. Covers UC-001..UC-006 end-to-end against
  the four fixture repos.
