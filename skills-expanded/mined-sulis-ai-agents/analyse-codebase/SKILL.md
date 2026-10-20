---
name: analyse-codebase
description: "Scans an existing codebase and reports its structure, complexity, and risks."
user_invocable: true
---

# Code Intelligence Probe

When invoked, run deterministic structural analysis of the project and
produce:

- `.architecture/{project}/probe-raw/{workspace}/1_*.json` — 15 phase
  outputs per workspace, deterministic
- `.architecture/{project}/probe-raw/synthesis.json` — LLM-authored
  synthesis sections (Summary, Pattern Recognition, Wrapper-Rot Triage,
  Recommendations)
- `.architecture/{project}/CODE_INTELLIGENCE.md` — Markdown summary
- `.architecture/{project}/CODE_INTELLIGENCE.html` — human-navigable HTML
  with sidebar TOC, sortable tables, collapsible sections; self-contained
  (works offline)

**Hard tool requirement.** `/sulis:analyse-codebase` does not run without its toolchain.
If a required tool is missing, run `scripts/install-probe-tools.sh` (macOS
via brew + pipx; Linux via apt + cargo/npm/pip). There is no LLM-only
fallback — at codebase scale, LLM-as-AST-walker has unacceptable
hallucination risk.

---

## Inputs You Read

| Source | Why |
|---|---|
| Project source tree | Primary input — runners walk it, respecting .gitignore + the centralised exclusion list |
| `.context/{project}/INDEX.md` (if present) | Adjusts which conventions to look for; flag if absent on non-trivial repos |
| `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `pom.xml` / `build.gradle*` | Language + framework inference |

If `.context/{project}/INDEX.md` does not exist on a non-trivial codebase,
recommend `/sulis:discover-context` first (same auto-suggest gate as the
other SEA skills).

---

## Workflow

### Phase 0 — Tool Detection

Run `bash scripts/install-probe-tools.sh --check`. The script verifies
ast-grep, lizard, scc, git are present and that lizard is the McCabe
analyser (not the compression utility — v0.7.1 regression check).

If any required tool is missing, present the missing-tool list and run the
installer with the user's confirmation. There is no LLM-only fallback.

### Phase 1 — Deterministic Extraction (Python orchestrator)

Invoke the orchestrator:

```bash
python scripts/probe.py --root . --project {project-slug}
```

Common flags:
- `--workspace {name}` — restrict to one workspace in a monorepo
- `--run-tests` — opt-in test execution (Phase 1.9)
- `--git-lookback-days N` — git churn window (default 365)
- `--skip-tests` / `--skip-lints` / `--skip-history` / `--skip-duplication`
  / `--skip-deadcode` / `--skip-architecture` — opt out of specific phases
- `--skip-deployment` — skip Phase 1.16 (Deployment Topology, repo-wide)
- `--skip-credentials` — skip Phase 1.17 (Credential Scanning, repo-wide)
- `--exclude-dir DIR` — exclude a top-level dir from enumeration (repeatable)
- `--secrets-baseline PATH` — override `.secrets.baseline` location
- `--continue-on-error` — don't fail-fast on individual runner errors
- `--json-only` — skip Markdown + HTML rendering
- `--md-only` — render Markdown but skip HTML

The orchestrator runs 15 per-workspace phases + 2 repo-wide phases:

| Phase | Scope | Tool | Output |
|---|---|---|---|
| 1.1 | per-workspace | scc | stack inventory, LOC, complexity totals |
| 1.2 | per-workspace | ast-grep | capabilities (classes / functions / interfaces / types) |
| 1.3 | per-workspace | ast-grep | extension points (abstract classes, interfaces, registries) |
| 1.4 | per-workspace | ast-grep + grep | reusable abstractions (consumer counts) |
| 1.5 | per-workspace | ast-grep + Tarjan | coupling (fan-in/out, cycles) |
| 1.6 | per-workspace | lizard | complexity hotspots (CCN > threshold) |
| 1.7 | per-workspace | ast-grep | wrapper-rot candidates |
| 1.8 | per-workspace | filesystem | conventions (naming, layout, error handling) |
| 1.9 | per-workspace | pytest / vitest / jest / go test / cargo test | test discovery + optional execution |
| 1.10 | per-workspace | eslint / ruff / mypy / clippy / golangci-lint | lint dry-run signal |
| 1.11 | per-workspace | git | history: churn, age, authors, co-change |
| 1.12 | per-workspace | jscpd | code duplication (optional) |
| 1.13 | per-workspace | ts-prune / vulture / deadcode | dead code (optional) |
| 1.14 | per-workspace | dependency-cruiser / import-linter | architecture rule violations (optional) |
| 1.15 | per-workspace | (parses Phase 1.9) | coverage signal |
| **1.16** | **repo-wide** | **filesystem + YAML** | **Deployment topology — Dockerfiles, K8s, Helm, Terraform, GH Actions, Sulis manifests** |
| **1.17** | **repo-wide** | **detect-secrets** | **Credential scanning — hardcoded secrets (hash-only, baseline-aware)** |

Per-workspace phases write to `.architecture/{project}/probe-raw/{workspace}/1_N_xxx.json`.
Repo-wide phases (1.16, 1.17) write to `.architecture/{project}/probe-raw/1_16_deployment.json`
and `.architecture/{project}/probe-raw/1_17_credentials.json` — once per run, not per-workspace.

**Graceful degradation:** if an optional tool is missing, that phase is
skipped with a warning recorded in the workspace manifest. The probe never
installs project dependencies — that would be destructive.

### Phase 2 — LLM Synthesis

After Phase 1 completes, write a draft synthesis template:

```bash
python scripts/probe.py --draft-synthesis
```

This produces `probe-raw/synthesis.json` with empty fields and per-section
hints. Read the JSON files in `probe-raw/` and fill the four synthesis
sections:

- **`summary`** — ~5-sentence overview of the codebase: what it is, what
  patterns it follows, what's healthy, what's smelly. Source the facts
  from `1_1_stack.json`, `1_2_capabilities.json`, and the various
  cross-references.
- **`pattern_recognition`** — list of system-level patterns identified
  (Ports & Adapters, MVC, CQRS, event-sourced, layered, etc.). Each
  entry: `{pattern, confidence, evidence}`.
- **`wrapper_rot_triage`** — for each candidate in `1_7_wrappers.json`,
  classify as one of: `wrapper-rot`, `legitimate-adapter`,
  `in-progress-strangle`, `branch-by-abstraction`. Cite evidence.
- **`recommendations`** — prioritised list citing evidence from multiple
  JSON files (e.g. `1.6 ∩ 1.11 ∩ 1.15` → "Decompose; high CCN, high churn,
  low coverage; **MUST add characterisation tests first**"). Each entry:
  `{priority, primitive, target, evidence_phases, rationale, confidence}`.

The synthesis is structured JSON — NOT Markdown. The renderer formats it
into both Markdown and HTML automatically.

### Phase 3 — Render

```bash
python scripts/probe.py --render
```

Produces both `CODE_INTELLIGENCE.md` and `CODE_INTELLIGENCE.html` from
the phase JSONs + `synthesis.json`. The HTML is self-contained (inline
CSS + JS) and navigable in any browser.

### Phase 4 — Report

Tell the user where the HTML is and to open it for review:

> "Probe complete. Open `.architecture/{project}/CODE_INTELLIGENCE.html` in
> a browser for the navigable report. The Markdown summary is also at
> `CODE_INTELLIGENCE.md`. Raw JSON is in `probe-raw/`.
>
> Top findings:
> - **{N}** modules, **{M}** capabilities catalogued
> - **{K}** complexity hotspots (CCN > 15)
> - **{R}** wrapper-rot candidates (internal — needs review)
> - **{S}** recommendations prioritised
>
> Refresh: re-run `/sulis:analyse-codebase` when source files change (the orchestrator
> compares mtimes)."

---

## Refresh Policy

CODE_INTELLIGENCE is regenerated when:

- Source-file mtimes are newer than the system manifest's `finished_at`
  timestamp
- Downstream skills (blueprint, decompose, harden, verify) refuse to use
  intelligence older than 30 days
- The user invokes `/sulis:analyse-codebase` explicitly

Refresh is a full re-run, not incremental — Phase 1 is fast enough on most
projects (sub-minute) that incremental refresh isn't worth the complexity.

---

## How Other Skills Use the Output

**`/sulis:draft-architecture`** — reads `1_2_capabilities.json` (Reuse decisions),
`1_3_extensions.json` (Extend / Create-adapter decisions), and the
Recommendations from `synthesis.json` before designing.

**`/sulis:plan-work`** — reads everything to assign primitives to WPs and
cite specific code regions. Wrapper-rot candidates from `1_7_wrappers.json`
flow into the wrap audit.

**`/sulis:harden-codebase`** — reads `1_5_coupling.json` (impact radius) and
`1_11_history.json` (high-churn = high-risk delta).

**`/sulis:codebase-audit`** — uses `1_2_capabilities.json` as the structural
baseline against which to find pillar gaps.

**`/sulis:verify-architecture`** — reads `1_7_wrappers.json` for the P6 wrapper-rot check
and `1_15_coverage.json` for the characterisation-tests-before-Refactor
gate.

---

## Output Layout

```
.architecture/{project}/
├── CODE_INTELLIGENCE.md       # Markdown summary (machine + git diff)
├── CODE_INTELLIGENCE.html     # Self-contained navigable HTML (human review)
└── probe-raw/
    ├── 00_system_manifest.json
    ├── synthesis.json
    ├── 1_16_deployment.json      # repo-wide: Deployment Topology
    ├── 1_17_credentials.json     # repo-wide: Credential Scanning
    └── {workspace}/
        ├── 00_manifest.json
        ├── 1_1_stack.json
        ├── 1_2_capabilities.json
        ├── 1_3_extensions.json
        ├── 1_4_reuse.json
        ├── 1_5_coupling.json
        ├── 1_6_complexity.json
        ├── 1_7_wrappers.json
        ├── 1_8_conventions.json
        ├── 1_9_tests.json
        ├── 1_10_lints.json
        ├── 1_11_history.json
        ├── 1_12_duplication.json
        ├── 1_13_deadcode.json
        ├── 1_14_architecture.json
        └── 1_15_coverage.json
```

---

## Gotchas

- **Python 3.11+** required for the orchestrator (stdlib `tomllib`).
- **Lizard must be the McCabe analyser**, not the compression utility from
  `brew install lizard`. The installer enforces this via pipx; the
  detection step greps `lizard --help` for "Cyclomatic Complexity Analyzer".
- **`.claude/` and other dotfile-prefixed dirs are scanned**. The orchestrator
  passes `--no-ignore hidden --no-ignore dot` to ast-grep so user code in
  those locations isn't silently missed. `.gitignore` is still respected
  (so `.venv/` and `node_modules/` are excluded).
- **Monorepo support:** the orchestrator detects pnpm-workspace, lerna,
  nx, turborepo, cargo, maven, gradle, bazel, rush, and go-workspaces. Each
  workspace gets its own per-workspace JSONs.
- **Polyglot enumeration (v0.9.0):** even when a monorepo manifest is
  present, the orchestrator additively discovers (Stage 2) top-level
  auxiliary packages with their own manifest (`pyproject.toml`, `Cargo.toml`,
  `go.mod`, etc.) at depth 1 or 2; (Stage 3) code-bearing dirs with ≥ 10
  source files in known extensions OR any `.tf`/`.tfvars`; and (Stage 4)
  deployment-only dirs containing `Dockerfile`, compose YAML, or
  k8s/Sulis YAML. Each stage skips paths already claimed by an earlier
  stage. `.github`, `docs`, `.vscode`, etc. are never enumerated.

---

## Polyglot Workspace Enumeration

The default assumption is that the repo is a polyglot monorepo. The 4-stage
pipeline runs additively:

| Stage | Adds | Style tag |
|---|---|---|
| 1 | Existing monorepo manifest (pnpm/lerna/nx/turborepo/cargo/maven/gradle/bazel/rush/go-workspaces) | matches the manifest |
| 2 | Top-level (depth 1-2) dirs with a project manifest (`pyproject.toml`, `Cargo.toml`, `go.mod`, `setup.py`, `Gemfile`, `composer.json`) | `auxiliary-package` |
| 3 | Top-level dirs with ≥ 10 source files in known extensions, OR any `.tf`/`.tfvars` | `code-bearing-dir` |
| 4 | Top-level dirs with `Dockerfile`, `docker-compose.yml`, or a k8s/Sulis YAML manifest | `deployment-dir` |

A dir is skipped by stages 2-4 if it (or any of its children/parents) is already
claimed by an earlier stage. Hard skip list: `.github`, `.vscode`, `.idea`,
`.devcontainer`, `.husky`, `.claude`, `.git`, `.circleci`, `.gitlab`, `docs`,
`doc`, plus the standard build-output exclusions (`node_modules`, `.venv`, etc.).

If workspace count exceeds 25, a warning is logged to stderr — narrow with
`--workspace` or `--exclude-dir`.

---

## Credential Scanning Privacy Contract

Phase 1.17 invokes [detect-secrets](https://github.com/Yelp/detect-secrets)
to find hardcoded credentials. Three invariants apply:

1. **Hashes only.** The runner stores the SHA-1 hash that detect-secrets
   produces — never the plaintext value. No `secret`, `value`, `plaintext`,
   `raw_secret`, or `password` field exists in `CredentialFinding`. A unit
   test (`test_credential_finding_never_contains_value`) asserts this.

2. **Baseline-aware.** If a `.secrets.baseline` file exists at the repo
   root (or at the path supplied via `--secrets-baseline`), the runner
   loads it and marks each finding's `is_known` flag accordingly:
   `is_known=True` for hashes acknowledged in the baseline, `False` for
   new findings. The probe does **not** pass `--baseline` to detect-secrets
   directly (that would filter known findings from the output); it tags
   them itself so both categories appear in the payload.

3. **Graceful degradation.** If detect-secrets is not on `PATH`, Phase
   1.17 emits a payload with `skipped=True` and `skip_reason` populated;
   the probe never fails for a missing optional tool.

Sulis manifests and CI workflows are scanned separately by Phase 1.16 for
**secret references** (e.g. `${{ secrets.NAME }}`) — these are NAMES only,
never values. Together, Phases 1.16 and 1.17 answer "what credentials does
this codebase depend on AND where might it have leaked them."

---

## See Also

- `references/code-intelligence-template.md` — the CODE_INTELLIGENCE schema
- `references/change-primitives.md` — what the intelligence informs
- `references/right-sizing.md` — how tier interacts with intelligence depth
- `scripts/install-probe-tools.sh` — installer for required + optional tools
- `scripts/probe.py` — orchestrator entry point
- `scripts/probe/` — runner package
- `tests/` — unit + integration test suites
