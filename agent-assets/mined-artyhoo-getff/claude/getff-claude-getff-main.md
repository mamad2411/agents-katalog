# Claude / Agent Guidance

This file is auto-loaded by Claude Code when sessions run inside this repo.

> **Authoritative for:** AI-tooling conventions, capability-commit gates, build-vs-reuse discipline, Artifact Ownership Contract.
> **NOT authoritative for:** project goal, methodology, design invariants — see [README.md#why-this-exists](README.md#why-this-exists).

## Goal + Step 0 (methodology ≠ goal)

[Step-0](.claude/session-bootstrap.md) + [goal](README.md#why-this-exists). If a doc contradicts README, it has drifted — surface as a [research-patch](docs/meta-factory/research-patches/).

## Build-vs-reuse invariant (Phase 8.8)

Before introducing any **capability commit** (definition below), **MUST**:

1. Consult [docs/meta-factory/prior-art-evaluations.md](docs/meta-factory/prior-art-evaluations.md) (SSOT) for matches on the capability area.
2. Run context7 query (≥3 phrasings) on the capability area; cite candidates surfaced.
3. Document the evidence via a `Prior-art:` commit trailer (syntax below).

If no SSOT entry matches and context7 surfaces no production-grade analog, add a new SSOT entry — with `Verdict`, `Rationale`, `Trigger to revisit` — in the same commit as the capability artifact (per [prior-art-evaluations.md §3](docs/meta-factory/prior-art-evaluations.md)).

The phase entry consult gate is the same enforcement at planning time — see [EXECUTION-PLAN.md §5.5 Step 1.5](docs/meta-factory/EXECUTION-PLAN.md).

For the **consumer-side authority model** governing how shipped artefacts may be customised after install (three-layer model + `<file>.override.md` escape hatch), see [INSTALL-FOR-AI.md `Three-layer authority for shipped artefacts`](INSTALL-FOR-AI.md#three-layer-authority-for-shipped-artefacts). This is the consumer-facing companion to the build-vs-reuse discipline above.

> **Satellite doctrine** (own-stack-first · operator-vs-shipped axes · cost = capability-commit · use-before-build) lives at its authoritative home [`.claude/rules/build-first-reuse-default.md §1.1`](.claude/rules/build-first-reuse-default.md) — that rule owns «relationship to upstream tools + default verdict for capability proposals». CLAUDE.md owns only the **per-commit** build-vs-reuse gate (above + below); the macro companion-relationship doctrine is BFR's scope (relocated 2026-06-01 — the §32 placement was a doc-authority slip per [doc-authority-hierarchy.md §4](.claude/rules/doc-authority-hierarchy.md) `#contradicting-authority-claims`).

## What is a capability commit?

A commit that does **any** of the following (mirrors `packages/core/hooks/checks/prior-art.ts` detection — the prose definition and the hook stay in sync):

- Adds a new **explicit dependency** in `package.json` (transitive deps don't count; detected as a dependency key present on an added `+` line with no matching removed `-` line for the same key, across common semver-prefix forms `^ ~ >= <= = *`, in the package.json diff). Keys inside `overrides` / `resolutions` / `pnpm` blocks do NOT count — they force versions of packages already in the tree, adding no capability (PR #980 incident); a block that opens **and closes on one line** (`"overrides": { "lodash": "4.17.21" },` — what prettier emits when the object fits `printWidth`) exempts only itself, so dependencies added after it in the same hunk are still detected (2026-09-05 fix).
- Adds a new file **≥50 LOC** under a new subdirectory of `packages/core/<new-dir>/`.
- Adds a new file **≥80 LOC** anywhere under `packages/`.

Three carve-outs on the LOC triggers (hook parity 2026-08-07, mirroring the PR #980 overrides carve-out pattern): **documentation files** (`*.md`/`*.markdown`) never count — the «doc edits are NOT capability commits» exemption below always covered them, but a shipped ≥80-LOC doc template tripped the detector (PR #1272 incident); and a new file **byte-identical to a blob already tracked in the pre-image tree** — the commit's parent, or the merge-base for the PR-body arm — never counts, because a relocation/vendor copy adds no capability by construction (PR #1271 incident: vendored runtime-bridge subset). The pre-image tree is the whole of that carve-out: a new file and a byte-identical copy **both created in the same commit** (a new hook plus the plugin twin the pre-commit twin-sync generates) are a new capability, not a relocation, and are still detected (2026-09-05 fix).

The third carve-out is **test material** — a `*.test.*` / `*.spec.*` file, or any file under a `test(s)/`, `__tests__/` or `*fixtures/` directory — which never counts, because the closing sentence below has always exempted «test additions for existing capabilities» while the detector counted them anyway (2026-09-06 fix: over the last 250 first-parent commits on staging the ≥80-LOC arm fired on 27 commits, 18 of them test-only, and the trailers it forced cited SSOT rows the commit never touched). The carve-out cannot hide a capability: a commit that adds test material **alongside** a qualifying production file still trips on that production file. Its one exception is a file directly in `packages/core/principles/` — a principle IS the enforcement capability, not a test for one, so those keep demanding a consult (subdirectories such as `packages/core/principles/fixtures/` are ordinary test material and stay exempt).

Refactors, doc edits, test additions for existing capabilities, bug fixes, snapshot regenerations, recipe data edits — **NOT** capability commits.

## `Prior-art:` trailer syntax

In the commit message body, after the blank line that follows the subject:

```text
Prior-art: <narrative naming a resolvable referent — prior-art-evaluations.md#<ID>, an artefact path, or an issue/PR reference — or the escape hatch>
```

A positive trailer must name something a reader can open. Three accepted referent forms (enforced by `packages/core/hooks/checks/prior-art.ts`; measured 2026-09-06 against the post-cutoff first-parent history — 2 of 145 capability commits with a positive trailer fail this grammar, both from before 2026-07-19):

1. an **SSOT row** — `prior-art-evaluations.md#<ID>` (the primary form; the cited row must exist);
2. an **artefact path** — `setup.d/lib.sh:359`, `research-patches/2026-05-23-guard-liveness-gate.md §2`;
3. an **issue / PR reference** — `#1271`, `PR #1094`.

A referent-free assertion (`Prior-art: consulted — no entry applies`) is rejected: it is the `#hope-as-gate` shape of [attention-is-not-a-mechanism.md §2](.claude/rules/attention-is-not-a-mechanism.md).

**Examples:**

- Positive: `Prior-art: prior-art-evaluations.md#1 (Autogrep, verdict DEFER — different domain, no overlap with this commit's capability).`
- Multiple refs: stack two `Prior-art:` lines, one per entry. Each line is independently parsed.
- Escape hatch (non-capability commits caught by the hook in mixed PRs): `Prior-art: skipped — refactor only, no new capability` — rationale **must** be ≥20 chars and specify *why* (e.g. «refactor only, no new capability», «snapshot regen after recipe edit», NOT «TODO» / «later» / placeholder).

## Recursive self-application

This convention is enforced via three layers, each validating a different artifact:

| Layer | Surface | Artifact | Added |
|---|---|---|---|
| 1 — meta-test | Phase 2 principle 08 | research files cite SSOT by ID; broken refs caught | T3 |
| 2 — process gate | EXECUTION-PLAN §5.5 Step 1.5 | phase research consult before drafting | T6 |
| 3 — developer-time | `.husky/pre-push` + commit trailer | capability commits carry `Prior-art:` line | T7 + T8 |

The convention applies to its own implementation: Phase 8.8 commits T2-T11 carry `Prior-art:` trailers, and principle 08 validates the SSOT it builds on.

## Artifact Ownership Contract

Each artifact has one owner. Cross-owner edits require explicit handoff (separate atomic commit + rationale, not side-effect of operational work). Reviewer agents are read-only for any artifact they don't own.

| Artifact | Owner | Read-only for | Why |
|---|---|---|---|
| [README.md](README.md) (`§Why this exists`) | maintainers (deliberate edit) | all reviewer / implementation / planning sessions | goal-redefinition is structural change |
| [docs/meta-factory/EXECUTION-PLAN.md](docs/meta-factory/EXECUTION-PLAN.md) | maintainers + planning sessions | reviewer agents, implementation agents | operational; does not own goal |
| [docs/meta-factory/PROPOSAL.md](docs/meta-factory/PROPOSAL.md) | frozen — historical artifact | all sessions | design-history record; do not retroactively rewrite |
| [docs/meta-factory/prior-art-evaluations.md](docs/meta-factory/prior-art-evaluations.md) | phase research sessions, capability-commit authors | reviewer agents | append-only register per [§3](docs/meta-factory/prior-art-evaluations.md) |
| [docs/meta-factory/retros/](docs/meta-factory/retros/) `*` | phase orchestrator at retro time | all subsequent sessions | closed historical artifact post-merge |
| [docs/meta-factory/research-patches/](docs/meta-factory/research-patches/) `*` | session that discovered the gap | all subsequent sessions | one patch per gap, append-only |
| [.husky/pre-push](.husky/pre-push), [.claude/rules/](.claude/rules/) `*` | maintainers | all session agents | enforcement layer |
| [.claude/session-bootstrap.md](.claude/session-bootstrap.md) | maintainers (deliberate edit) | reviewer agents | operational restatement; modify only when invariants/reading-order change |
| `agents/living-docs-auditor.md`, `agents/review-sidecar.md`, `agents/rule-test-author.md` (rule-tests write-half protocol, added 2026-07-22) (consumer-facing agents); `packages/core/templates/shared/skill-context/*/SKILL.md` (shipped AIF skill-context overrides) | framework maintainers | all sessions | design-by-spec ref consumer-project paths absent in source repo (per D-AuditC-6, 2026-05-16; renamed from `docs-auditor` + `best-practices-sidecar` removed per C-1 resolution 2026-05-20; skill-context overrides added per C-1 follow-up + SSOT #50, 2026-05-20) |
| [packages/core/principles/](packages/core/principles/) `*` | meta-tests CI | implementation agents | enforcement code |

The contract addresses the exact mechanism of the 2026-05-09 incident: reviewer agents pattern-matching on language in [docs/meta-factory/EXECUTION-PLAN.md](docs/meta-factory/EXECUTION-PLAN.md) §1 («north star»), then reinforcing the wrong goal across reviewer cycles. Read-only constraint on goal-bearing artifacts (README) prevents reviewer agents from silently re-establishing a different goal.

## PR strategy

When working on an agreed scope (a defined umbrella, batch, or single-concern PR), stay strictly within that scope.

**Rule:** if you notice a separate systemic issue mid-PR (e.g. «PR template missing §1.7 stubs causes recurring CI fails»), do NOT autonomously open an additional PR. Surface it as an observation in the final summary («I noticed X, want me to fix as a separate task?»), do NOT spawn a PR/branch/commit autonomously.

**Why:** Incident 2026-05-11, PR #33. While completing PR #32 (Wave 5 readiness SSOT remap), the orchestrator noticed a real recurring CI-fail trigger in the PR template and opened PR #33 autonomously. Maintainer pushback: drive-by scope expansion adds PR review overhead, introduces shared-state operations without explicit invitation, and violates atomic-umbrella discipline. Atomic-umbrella discipline is parallel to atomic-commit discipline: one concern per PR, even if «we're already here».

**How to apply:**

- Within the originally agreed umbrella scope → atomic commits OK, multiple files OK, multiple concerns within the umbrella OK.
- Outside the umbrella → surface as observation, await explicit invitation.
- The `work-without-stopping` user override applies to **clarification within the agreed scope**, not to expanding scope with new shared-state operations.
- Exception: if maintainer explicitly invited the systemic fix in this session, proceed — but that's an explicit invitation, not autopilot.

## Task-tier routing (which model plans, and whether to use the pipeline at all)

The Tier 0/1/2 criteria + the bridge-profile mechanic + the marker value rule + the
explicit capability-absence degradation matrix live in the shipped tier-home doc — the
**single source of truth**, installed at `.ai-factory/tier-home.md` for `env`+ consumers
and referenced here for the operator repo:

[`packages/core/templates/shared/tier-home.md`](packages/core/templates/shared/tier-home.md)

That doc owns the *criteria*; night-mode + the aif runtime profile config own *which model
fills which tier*. The acceptance-contour D1 exception (Tier-2 + /arch-reviewed
plan-complete kickoff → bridge-profile marker) still applies — see the doc's §2 lift.

## Skill routing bindings (three-stack harmonization)

Ratified 2026-08-18 (harmonization round 3 — [operator-axis spec §5.1](docs/superpowers/specs/2026-08-18-skill-stack-harmonization-design.md)): satellite-skill routing collisions die in THIS injected layer, not by cache pruning.

- **TDD loop:** `superpowers:test-driven-development` owns the loop. On «TDD» / «test-first» work, invoke it by explicit name; never route to `mattpocock-skills:tdd`.
- **Merge conflicts:** follow [.claude/rules/git-conflict-merge-forward.md](.claude/rules/git-conflict-merge-forward.md); never `mattpocock-skills:resolving-merge-conflicts` — its rebase-continuation advice dead-ends (force-push is classifier-blocked for agents machine-wide).

Full ownership map: [harmonization spec §3](docs/superpowers/specs/2026-08-18-skill-stack-harmonization-design.md). A live misroute despite these bindings = D-H7 incident (SSOT #253) → D-H8 escalation ladder (frontmatter neutering → prune → vendor).

## Umbrella closure convention

> **See:** [docs/meta-factory/operational-conventions.md#1-umbrella-closure-convention](docs/meta-factory/operational-conventions.md#1-umbrella-closure-convention) — when the last stage of a multi-stage umbrella merges, the merging session writes `done.md` (the load-bearing `priority-score.sh` Layer C3 fallback).

## Operational conventions (non-obvious harness gates + orchestration obligations)

### Harness gates

- **Agent PR merge policy — merging allowed by default:** agents merge their own `base=staging` PRs (`gh pr merge --squash`) once CI is green; handing a merge-ready PR to the operator is the anti-pattern (operator directive 2026-09-10). Nothing mechanically gates `gh pr merge` — git-safety.sh v3 covers destructive git + §1.7 PR-body validation only; this bullet's earlier «staging-allowed / main-blocked gate» wording described a mechanism that no longer exists. `base=main` (promotes) stays maintainer-owned per the promote hard rules below — its protection is the deep-review floor plus the `git push * main*` deny, not a merge hook.
- **CONFLICTING PR → merge-forward, never rebase:** force-push is permission-classifier-blocked for agents in every form (`--force`, `--force-with-lease`, rewritten history to a new branch — verified 2026-07-21), so `git rebase` on a published PR branch is a dead end. Instead merge the base INTO the PR branch, regenerate conflicted generated artefacts (`SNAPSHOT_MODE=capture bash tests/install-sh/snapshot.sh`; `plugin/hooks` twins regenerate via pre-commit), verify, then plain fast-forward push. Full recipe + triage: [.claude/rules/git-conflict-merge-forward.md](.claude/rules/git-conflict-merge-forward.md). (Incident 2026-07-21, PR #1058.)
- **Promote staging→main mechanics (three hard rules):** see [docs/meta-factory/operational-conventions.md#promote-stagingmain-mechanics-three-hard-rules](docs/meta-factory/operational-conventions.md#promote-stagingmain-mechanics-three-hard-rules) — fires when promoting staging→main (the `head=staging`-only §7 exemption + the merge-commit-never-squash rule + the maintainer deep review `/code-review ultra <PR#>` before merge).
- **Never move a branch ref with `git update-ref`:** see [docs/meta-factory/operational-conventions.md#never-move-a-branch-ref-with-git-update-ref--check-every-worktree-first](docs/meta-factory/operational-conventions.md#never-move-a-branch-ref-with-git-update-ref--check-every-worktree-first) — fires before any `git update-ref` / branch-ref move (worktree-desync hazard — check EVERY worktree first).
- **600-line markdown gate:** pre-commit hook blocks commits that push any markdown file past 600 lines. Check `wc -l <file>` before adding content to near-600 files (e.g. `docs/meta-factory/open-questions.md`). To free lines: migrate resolved `§13.x` entries to `docs/meta-factory/closed-questions.md` (append-only archive — TOC row + full entry under `## Archived entries`).
- **Homebrew PATH in hooks:** CC-launched hooks run with a stripped PATH (Homebrew absent). Hooks calling `gh`, `jq`, or other Homebrew tools must export `PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"` after `set -euo pipefail`. Symptom: hook returns empty output from `gh pr view` despite correct auth. (Codified from memory `feedback_harness_merge_block_and_500line_gate`.)

### Meta-orchestrator self-review obligation

> **See:** [docs/meta-factory/operational-conventions.md#3-meta-orchestrator-self-review-obligation](docs/meta-factory/operational-conventions.md#3-meta-orchestrator-self-review-obligation) — before any `/meta-orchestrator` session hands off a meta-kickoff to an orchestrator, spawn a Phase -1 cold-review on the generated `<umbrella>-meta-launch/kickoff.md` against the umbrella's `kickoff.md`.

### Phase -1 principle-test allowlist probe

Moved 2026-07-21 to its declared codification target: `.claude/skills/orchestrator/SKILL.md` Phase -1 → «Principle-test allowlist probe». This stub stays because in-flight kickoffs cite «CLAUDE.md §Operational conventions» for the probe; new kickoffs should cite the skill directly.

### Pre-dispatch in-flight probe

Before dispatching any stage/sub-wave Worker, probe for in-flight parallel work — ALL of: (a) `gh pr list --head <branch> --state all` (PR-stage); (b) `git log origin/staging..<branch>` ahead-commits on any existing worktree/branch (commit-stage — the window the PR-probe misses); (c) scan for parallel CC sessions working the same umbrella (e.g. other worktrees named for the same stage); (d) **container branches + un-harvested finished tasks** — `docker exec <container> git -C <repo> branch -a`, and any aif task at `done`/`verified` whose branch carries no PR. Items (a)-(c) are ALL origin/host-scoped, so a branch that exists only inside the aif container is invisible to every one of them; (e) RE-probe immediately after any Phase -1 review completes, before the actual dispatch — all historical collisions materialized inside the Phase -1 window. On any hit: STOP and surface, never double-dispatch. Root cause: one stage = one executor session (single-owner-per-stage).

**Run it, do not re-derive it:** `SLUG=<umbrella> bash .claude/skills/dispatcher/helpers/probe-inflight.sh` executes all of the above and emits one `VERDICT:` line; a probe that could not be *asked* yields `PROBE-INCOMPLETE`, never a clean answer ([.claude/skills/dispatcher/SKILL.md](.claude/skills/dispatcher/SKILL.md) §2.0). (Codified from memory `feedback_probe_inflight_automation_before_dispatch`; 3/3 incident threshold reached 2026-06-10, all during the one-click-installer umbrella. Item (d) added 2026-08-09 after `feature/beta-delivery-ux-995e9c` — a duplicate dispatch fired by an origin-only probe an hour after the real run had finished in the container.)

## See also

- [CONTRIBUTING.md](CONTRIBUTING.md) — full contributor-facing details (hook setup, bypass policy).
- [docs/meta-factory/prior-art-evaluations.md](docs/meta-factory/prior-art-evaluations.md) — the SSOT.
- [.github/pull_request_template.md](.github/pull_request_template.md) — PR checklist.
- [packages/core/principles/08-prior-art-cited.test.ts](packages/core/principles/08-prior-art-cited.test.ts) — meta-test enforcing citations.
- [agents/compliance-verifier.md](agents/compliance-verifier.md) — AI-agnostic sub-agent for §1.7 substance review; read in your active session before merging a discipline-bearing PR (Wave 8.1b, $0 LLM-in-CI).
- **Parallel-session dispatch:** spawn isolated worktrees with `claude -w <name>`, or portably via `bash scripts/create-worktree.sh <name>` (≤2-step pipeline, empirically accepted in [docs/meta-factory/research-patches/2026-05-29-dispatch-worktree-iphase-acceptance.md](docs/meta-factory/research-patches/2026-05-29-dispatch-worktree-iphase-acceptance.md)).
- **Worktree `node_modules` provisioning:** [`scripts/worktree-node-modules.sh`](scripts/worktree-node-modules.sh) is the single source of truth; [`scripts/create-worktree.sh`](scripts/create-worktree.sh) and [`.claude/hooks/worktree-setup.sh`](.claude/hooks/worktree-setup.sh) both call it. **Do not assume the CC hook runs** — `WorktreeCreate` is NOT registered in [`.claude/settings.json`](.claude/settings.json) (verify: `jq '.hooks.WorktreeCreate' .claude/settings.json`), and `.claude/settings.json` lists `Edit(.claude/settings.json)` + `Write(.claude/settings.json)` on its own `permissions.deny`, so no agent can register the hook — it fires only for maintainers who did so by hand. That deny rule is the narrower layer: staging the file at all is refused more broadly by the auto-mode classifier's `[Self-Modification]` guard, which also blocks `cp` onto it, `git checkout -b` / `git switch -c` in a worktree, and `git commit` of it — four denials measured 2026-09-14 while landing exactly such a change. So «agent-uncommittable» holds in effect at every channel; an agent that has prepared a settings change should hand the operator the command rather than look for a path around the guard (`git push` of an already-made commit is NOT blocked). Worktrees born any other way (desktop app, agent container, bare `git worktree add`) are provisioned by the `worktree-provisioning` pre-push section, which self-heals before the test sections run. To sweep every worktree at once: `bash scripts/worktree-doctor.sh [--fix]`. (Incident 2026-07-23: the hook had never been registered since it shipped in PR #279, this bullet claimed otherwise, and 63 of 125 worktrees were unprovisioned.)
