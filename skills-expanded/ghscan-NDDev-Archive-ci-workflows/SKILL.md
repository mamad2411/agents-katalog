---
name: nddev-repo-flow
description: Operating this repository end to end — the catalog-as-source-of-truth model, the golden path for any change, the tiered validation gate, and the release procedure. Invoke when working on ci-workflows itself, rather than on CI doctrine in general.
license: AGPL-3.0-or-later
compatibility: Codex and Agent Skills compatible; OpenCode discovers .agents/skills. Generate .claude/skills mirrors for Claude Code.
metadata:
  version: 2.0.0
  owner: NDDev
  status: proposed
  reviewed_at: '2026-08-12'
---

# Operating ci-workflows

This replaces the former `nddev-repo-orientation`, `nddev-change-flow` and
`nddev-release-flow`. Three skills describing one workflow meant three places to
keep in step, and they drifted from each other and from `AGENTS.md`.

`AGENTS.md` is the brief — file map, change-impact map, and the table of
contracts with the validator that owns each. Read it first; this skill is the
procedure, not a second copy of the facts.

## The model in one paragraph

`catalog/*.yml` is authoritative. `docs/generated/*` is rendered from it and a
drift check rejects hand edits. Prose may reference the catalog, never restate
it; where prose and a generated artifact disagree, the generated artifact is
right, because it is validated and the prose is not. Every volatile external
fact carries `verified_at` / `expires_after` and expires closed. `docs/adr/`
records *why* each contract exists — read the ADR before changing the contract
it explains, so a reversal is deliberate.

## Golden path for a change

1. Edit the workflow or script.
2. Update `catalog/capabilities.yml`, and `catalog/tools.yml` if you added or
   bumped an action. `used_by` and tool registration are both derived from the
   tree by `check_tool_registry.py`, so an omission fails rather than rots.
3. Run `generate_docs.py` through the repository's isolated Python launcher.
4. Add a caller example under `examples/`. `check_examples.py` fails a reusable
   with no example — it is the only executable statement of a caller contract.
5. Sync prose: `README.md`, the tier docs, the matching example.
6. Run `sync_skills.py` through the isolated launcher if you touched a skill.
7. `CHANGELOG.md` under `[Unreleased]`.
8. Validate, then PR.

## Validate

```bash
python3.13 -I -B -m venv --copies .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-ci.txt
.venv/bin/python -I -B scripts/check_python_syntax.py
.venv/bin/python -I -B scripts/check_python_execution_contract.py --launch validate_all.py -- --tier core
.venv/bin/python -I -B scripts/check_python_execution_contract.py --launch validate_all.py --
actionlint
GH_TOKEN=$(gh auth token) uvx zizmor@1.26.1 --persona pedantic --min-severity low .github/workflows
```

Three tiers, and the split is load-bearing. **core** holds only properties of
the tree, so it can fail only because of your change. **touched** is scoped: a
product fact is checked for expiry only when the changed capability declares it.
**scheduled** is advisory and runs in `maintenance.yml`. Do not move a
calendar-driven check back into core — that coupling is what let an external
vendor's tariff block an unrelated bugfix.

Never use `pip` or `pipx`, and never a mutable version (`@latest`). Run zizmor
at the version `zizmor-sarif.yml` pins, not whatever is on `PATH`; a different
version reports different findings than the gate.

**Give zizmor a token.** Its online audits — `ref-version-mismatch`,
`impostor-commit` — need the API. Without one it skips them silently and prints
"No findings" while CI fails, because CI has `GH_TOKEN`. Three pin comments
naming the wrong release reached the default branch that way, and only a real
fixture run caught them.

## When a check fails

Most validators execute real fixtures — temporary Git repositories, extracted
embedded programs, adversarial input matrices — so the message names the exact
broken contract. Open the named script and read its docstring: it says what the
contract defends against and usually names the incident that produced it. That
is faster than reasoning from the YAML.

## The static-only dance

Editing a workflow the ledger marks `runtime-proven` invalidates its
`proven_digest`, and the gate fails. There is no way to keep the label without
new evidence, which is the point.

There is now a way to supply it. Push a `fixtures/**` branch. The estate is
three workflows: `runtime-fixtures.yml` for the tree-level lanes,
`runtime-fixtures-languages.yml` for the language and tooling lanes — split
because one file grew until it stopped starting at all — . The negative
gates live in `ci.yml` instead, inside `ci-gate`'s `needs`, so a gate that stops
refusing bad input blocks the merge that broke it. Both estate files call the
reusables the way a consumer would, and each prints the run
URL and every workflow's new sha256 ready to paste into the ledger. Only a `success` row is evidence — a failed or skipped row
proves nothing and says so. Re-proving a change that touched every workflow is
one push.

If a workflow has no fixture, drop its record to `static-only` naming a validator
that actually exists. Never leave a stale run as proof.

Say *why* a record is unproven rather than reaching for the template. "No
observed consumer run" was true of everything before the estate existed and
is now nearly always the wrong sentence: the useful record names the obstacle
— an SDK nobody installed, a gate needing `contents: write` the estate refuses
to grant, a scanner that only evaluates a default branch. The status column
says *that* something is unproven; only the evidence column can say whether
that is a gap to close or a property of the thing.

`release`, `security-blocking` and `required-gate` may not rest at `unverified`:
prove, stand in with a validator, or take a dated waiver with an owner. Stagger
new expiries — a renewal wave landing on one date recreates the cliff the rule
exists to prevent. The blocking families are pinned in `PINNED_CRITICALITY`, so
relabelling to escape the obligation is itself a gate failure.

## Contracts worth knowing before you edit

- **Paired variants stay byte-parallel.** `release-supply-chain.yml` ↔ `-free`
  differ only in the attest steps, permissions and `slsa_build_level`;
  `benchmark.yml` ↔ `-compare` only in `auto-push` and permissions.
- **Fail-closed routing.** `monorepo-changed-paths.yml` takes strict JSON
  filters; wildcards, unresolvable bases and malformed groups fail the run, and
  an uncertain push base goes conservative all-true, never silent all-false.
- **Tier separation is structural**, never a boolean around a privileged action.
  Harden-Runner has `pre`/`post` hooks GitHub can run even when a step `if` is
  false, so it lives only in the explicit allowlist, unconditional and first.
- **Caller commands run `bash -euo pipefail -c`.** A plain `bash -c "$CMD"` lets
  `a; b` report success after `a` failed.
- **`gate.yml` is a report, not a merge gate.** A reusable cannot read its
  caller's `needs`, so `needs_json` is caller-authored. A required check must be
  caller-native — see `examples/quality/caller-native-gate.yml`.

## Releasing

Requires an authorized maintainer. The graph is
`resolve → promotion → authorize → publish`: every write scope sits on
`publish`, which cannot start until the promotion gate verifies the tag's
control-plane record **and** a reviewer approves the protected `release`
environment. `check_release_graph.py` enforces that shape.

1. **Version prep, as a normal PR.** `VERSION` becomes `X.Y.Z` on one
   LF-terminated line. `CHANGELOG.md` gets exactly one `## [X.Y.Z]` heading,
   with `[Unreleased]` emptied above it. Run the full sweep, not just core — a
   release must not ship carrying an expired fact.
2. **Build the promotion record** in the control plane —
   `scripts/promotion_record.py create --module ci-workflows` in
   `nddev-harnesses`. It enforces the same schema the gate does; do not
   hand-write one. **Its `--evidence-manifest` input has no producer yet**, so
   this step currently cannot be completed: the manifest needs nine lane records
   — two of them macOS architectures — each with a real run identity and log
   digest inside a 168-hour window, and nothing in the estate emits one. That is
   why no release has run since the gate landed on 2026-08-05. See issue #157
   before starting a release; if it is still open, stop after step 1.
3. **Cut the signed tag** with that record as the annotation:
   `git tag -s X.Y.Z -F promotion.json`, then push the tag. Numeric SemVer only,
   no `v`. The annotation must be canonical compact JSON plus one LF, and the
   record expires within 168 hours of generation.
4. **Approve** the `release` environment when the promotion gate has passed.
5. **Verify** the release publishes exactly five checksummed assets in one
   create call, and that the attestations verify with
   `scripts/verify_attestations.sh`. Releases are immutable: never
   `gh release upload --clobber`, never republish.
6. **Re-promote** the runtime-coverage record for `release-supply-chain.yml`
   afterwards — that run is real evidence, so record its URL and digest.

If the promotion gate fails, the tag is not authorized. Fix the cause; do not
route around the gate.

## Git etiquette

Conventional Commits under 100 chars, `git commit -s -S`, no `Co-Authored-By`.
`main` is PR-only and takes **merge commits** — squash and rebase are disabled
live, and `.gds/compiled-policy.json` now agrees, via a repository-tier override
in the control plane. Never hand-edit that file; it regenerates. Fill the PR
template: workflow changes owe a permissions diff and a threat-model note.
