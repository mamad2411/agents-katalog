---
name: cli-forge-pipeline
metadata:
  author: clement
description: >
  Expert CI/CD pipeline optimizer using biomimetic patterns from nature: leafcutter ants
  (task partitioning), slime mold (adaptive path optimization), army ants (self-organizing
  parallelism), honeybees (dynamic resource allocation), and mycelium (fault-tolerant routing).
  Works with any CI system — examples cover both GitLab CI and GitHub Actions.
  Use this skill whenever the user asks to optimize, design, review, speed up, parallelize,
  or fix a CI/CD pipeline. Also triggers on: "slow pipeline", "flaky tests", "runners",
  "artifacts", "CI cache", "parallel build", "GitLab CI", "GitHub Actions", "pipeline design",
  "reduce build time", DAG pipelines, job dependencies, or any request mixing
  infrastructure + automation + deployment. Use it even when the user just pastes a YAML
  pipeline without asking explicitly.
argument-hint: "[pipeline-yaml-file-or-ci-directory]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output (reports, files, documentation), detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

# CI Pipeline Optimizer — Biomimetic

> *"The leafcutter ant colony has no project manager.
> Yet it optimally relocates 15% of all tropical vegetation."*

## The 9 biological models → CI patterns

Read `references/patterns.md` for detailed explanations, biology, and dual GitLab/GitHub examples.

| # | Organism | CI Pattern | Key principle |
|---|----------|------------|---------------|
| 1 | **Leafcutter ants** (Atta) | Stage Specialization + Artifact Cache | Each job = one role. Artifacts = stigmergy |
| 2 | **Slime mold** (Physarum) | Change-Driven Path Selection + Cache Reinforcement | Only rerun what changed. Content-hashed cache |
| 3 | **Army ants** (Eciton) | Fan-out / Fan-in + Ephemeral Runners | Maximum parallelism, disposable runners |
| 4 | **Honeybees** (Apis) | Autoscaling + Priority-based Runner Tagging | Resources proportional to load |
| 5 | **Mycelium** | Multi-Registry Fallback + Distributed Cache | Zero SPOF, waterfall cache |
| 6 | **Mitosis** | Workflow Fission | Pipeline too big → split into independent workflows (S/M/L/XL semantics canonical in `../shared/tiering.md`) |
| 7 | **Immune system** (VDJ) | Combinatorial Fuzzing + Property-Based Testing | Explore the input space, not just the known cases |
| 8 | **Fungal spores** | Full Combinatorial Matrix | OS × arch × version × features, fail-fast: false |
| 9 | **Tardigrade** | Chaos Engineering / Fault Injection | Inject failures to prove survival |

## Workflow for analyzing an existing pipeline

### Step 1 — Map the real DAG
Draw the actual dependencies. Identify sequential jobs that could run in parallel. Compute the critical path.

### Step 2 — Leafcutter audit
Does each job do ONE thing? Are artifacts properly defined (stigmergy)? Are there generalist jobs that should be split?

### Step 3 — Slime mold audit (Physarum)
Are there jobs running without any relevant change? Are cache keys based on content? Are retries selective? Content-hashed keys and reproducibility are shared in `../shared/determinism.md`. CI stages map onto the shared T0-T4 rungs (`../shared/gate-ladder.md`): the **release gate fails at the lowest red rung**.

### Step 4 — Army ants audit
Which slow jobs can be fanned out in parallel? Are runners ephemeral? Are fan-ins happening too early?

### Step 5 — Honeybee audit
Are runners sized for the right profile? Is scale-to-zero enabled? Do critical jobs have dedicated runners?

### Step 6 — Mycelium audit
Are there SPOFs (registry, cache, single runner)? Does the cache have a waterfall fallback? Do multi-project pipelines share expensive artifacts?

### Step 7 — Immune system audit
Is there fuzzing on parsers, serialization, auth? Do tests use property-based testing? Is the crash corpus persisted across runs?

### Step 8 — Spore audit
Does the matrix cover OS × arch × version × features? Are nightly/beta combinations marked `allow_failure`? Are impossible combinations excluded?

### Step 9 — Tardigrade audit
Are there tests under degraded network conditions? Tests under resource pressure? Tests with clock skew? Is graceful degradation verified?

---

## Mandatory rules

### GitHub Action version verification

**Before recommending a version bump for a GitHub Action** (e.g. `@v3` → `@v4`), verify that the target tag actually exists:

1. **Floating major tags** (`@v4`) are a convention, not a requirement. Some maintainers don't create them.
2. **Always verify** via `gh api repos/{owner}/{repo}/git/refs/tags/{tag}` that the exact tag exists.
3. If the floating major tag doesn't exist, **pin to the latest patch version** (e.g. `@v4.1.1`).
4. Never assume a major tag exists just because patch tags do.

> **Reference incident**: bumping `cosign-installer@v3` → `@v4` broke CI because the `v4` tag didn't exist (2026-03-27).

### Gotchas

Read `../gotchas.md` before producing output to avoid known mistakes.

---

## Anti-patterns to identify

| Anti-pattern | Broken biology | GitLab fix | GitHub Actions fix |
|---|---|---|---|
| Sequential jobs with no real dependency | Generalist ant | Direct `needs:` DAG | `needs:` between jobs |
| Cache key = branch or date | Slime mold with no memory | `key: files: [Cargo.lock]` | `key: rust-${{ hashFiles('Cargo.lock') }}` |
| Retry on everything | Slime mold retracing wrong paths | `when: [runner_system_failure]` | `nick-fields/retry` with `retry_on: error` |
| Full rebuild on minor change | Slime mold with no pruning | `rules: changes:` | `on.push.paths` or `dorny/paths-filter` |
| Single runner for everything | No caste division | `tags:` + autoscaler | Runner labels + larger runners |
| Registry without fallback | Mycelium without redundancy | `cmd1 \|\| cmd2 \|\| cmd3` | same |
| Huge artifacts passed everywhere | Forager carrying everything to everyone | Scoped artifacts, selective `needs:` | Named artifacts + selective `download-artifact` |
| Non-sharded tests | Army ants with no flanks | `parallel: N` + sharding | `strategy.matrix` + sharding |
| Tests only on hand-written cases | Immune system with no VDJ | `cargo fuzz` + `proptest` | same |
| Single OS/version combination | Single spore, no dispersal | `parallel: matrix:` | Combinatorial `strategy.matrix` |
| No tests under degraded conditions | Sedentary tardigrade | Toxiproxy + stress-ng + faketime | same |

---

## Success metrics

- **Critical path**: < 50% of the theoretical sequential total time
- **Cache hit rate**: > 80% on dependencies
- **Runner utilization**: > 70%
- **Flaky test rate**: < 1%
- **SPOF count**: 0

---

## Pipeline Scoring (15 dimensions)

Read `references/scoring.md` for detailed scoring criteria and scorecard template.

| # | Dimension | 0 | 4 |
|---|-----------|---|---|
| D1 | **DAG** | All sequential | DAG + dynamic pruning |
| D2 | **Cache** | None | Cross-pipeline + GC |
| D3 | **Parallelism** | 1 runner | Auto-scale + spot |
| D4 | **Resilience** | No retry | Multi-provider + self-healing |
| D5 | **Feedback** | > 15 min | < 2 min (smoke) |
| D6 | **Pruning** | Rebuild everything | Predictive skip |
| D7 | **Artifacts** | Everything shared | Content-addressed |
| D8 | **Security** | No scan | SBOM + signing |
| D9 | **Observability** | Raw logs | Anomaly detection |
| D10 | **Mitosis** | 1 mega-pipeline | Event-driven mesh |
| D11 | **Cost** | No measurement | FinOps optimized |
| D12 | **DX** | Manual config | GitOps + preview envs |
| D13 | **Fuzzing** | None | Persistent corpus + regression |
| D14 | **Matrix** | 1 env | Full combinatorial + nightly |
| D15 | **Chaos** | None | Chaos Monkey in prod + observability |

**Target score:** > 45/60 (75%) for a production project.

---

## Pipeline Pre-Mortem

Before merging a pipeline change, imagine the failures:

1. Poisoned cache (malicious artifact)
2. Compromised runner (secret leak)
3. Registry down (no fallback)
4. Flaky job retry-masked for 3 months
5. Cache miss → 45-minute pipeline
6. Cross-workflow dependency silently broken
7. DAG dependency diamond (C fails silently)

For each scenario: what mitigation ALREADY exists? If none → accepted risk, document it.

---

## Pipeline Mutation Testing

The mutation set + scorecard threshold is this skill's post-verification gate; the 3-phase definition-of-done structure (pre → during → post) is canonical in `../shared/done-gate.md`.

| Mutation | Expected | If it passes = bug |
|----------|----------|-------------------|
| Remove a `needs:` | Job runs too early | DAG misconfigured |
| Cache key `always-hit` | Poisoned cache detected | No validation |
| Remove `paths:` filter | Everything rebuilds (slow) | OK (conservative) |
| `continue-on-error: true` everywhere | Release despite failure | Missing gate |
| Remove security scan | Release without scan | No security gate |
| Double `timeout-minutes` | Slow job not detected | No duration alert |

If > 2 mutations pass silently, the pipeline has holes.

---

## Reference templates

- `references/patterns.md` — The 9 biological models in detail with GitLab + GitHub Actions examples
- `references/scoring.md` — Detailed 15-dimension scoring + scorecard
- `references/gitlab-ci-biomimic.yml` — Complete GitLab pipeline
- `references/github-actions-biomimic.yml` — Complete GitHub Actions pipeline
- `references/runner-autoscaler.toml` — GitLab Runner autoscaler config (honeybees)
- `references/cache-strategy.md` — Advanced cache strategies (slime mold + mycelium)

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Shell scripts used as pipeline entrypoints | `/cli-audit-shell` | Audit the scripts |
| Tests referenced in CI but not audited | `/cli-audit-test` | Test strategy audit |
| Pipeline builds containers | `/cli-forge-infra` | Container/image audit |
| Pipeline has > 10 jobs with complex dependencies | `/cli-audit-tangle` | CI dependency topology |
| Pipeline lacks a perf budget gate, or A/B benches are not reproducible | `/cli-forge-perf` | Native bench protocol (Criterion/benchstat/hyperfine) + content-hashed cache → reproducible perf gate |
| Jobs rebuild far more than the change (image layers or caches invalidated on every run) | `/cli-audit-hanoi` | Ordering/layering audit of build steps and image stacks |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-test` | D13 covers drift detection within tests. cli-forge-pipeline covers the **CI that executes** those tests |
| `cli-audit-code` | Audits code quality. cli-forge-pipeline audits **pipeline quality** |
| `cli-forge-perf` | Pipeline is the natural home of the perf gate: content-hashed cache (`../shared/determinism.md`) makes baselines reproducible; A/B bench jobs run on every PR; lowest red rung of `../shared/gate-ladder.md` includes T4 perf stress |
| `cli-cycle` | Calls cli-forge-pipeline as part of the full review |
