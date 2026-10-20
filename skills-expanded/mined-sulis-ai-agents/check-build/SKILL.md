---
name: check-build
description: "Checks whether your project builds and flags anything broken."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
  custom_dimensions:
    - name: "Primitive Coverage Completeness"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md INF-01 + INF-02"
      scorer: generating_agent
      evidence_required: "INF-01 (container security) + INF-02 (deploy-config secrets) + manifest hygiene all have status"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 1 (Exists) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/tools
    notes: shared tool-integration foundation
  - relationship: depends_on
    skill: _lib/tools/hadolint
    notes: NEW — to be created — covers INF-01 Dockerfile lint
  - relationship: depends_on
    skill: _lib/tools/trivy
    notes: NEW — to be created — covers INF-01 base-image CVE scan
  - relationship: depends_on
    skill: _lib/tools/gitleaks
    notes: NEW — to be created — covers INF-02 secrets in deploy configs (yaml/k8s/CI)
---

# Check Build

The most basic check: does the project build at all? Two parts:

1. **Build run** — detect the build system (Python, Node, Go, Rust,
   Docker, Make), run the build command (when `--run` passed), report
   success or failure.
2. **Manifest hygiene** — verify the project's manifest files
   (`plugin.json`, `marketplace.json`, `package.json`, `pyproject.toml`)
   are not just JSON-parseable but semantically correct (required fields
   present, version strings valid, no description bloat).

Both checks are read-only. The skill identifies what's broken; fixing is
a separate engineering action.

## Auto-detection

Same scope auto-detection as sibling tier-skills (PR vs codebase from
local git state; `--scope`, `--base-branch`, `--pr-number` overrides).
Build-system detection is per-project; multi-language monorepos detect
all systems and run each.

## Two modes

- **Founder mode (default).** Verdict in plain English: "builds — all
  good" or "the build broke — pip can't find package X." Operator IDs
  (specific pip resolver errors, npm tarball hashes) parenthetical.
- **Operator mode (`--raw`).** JSON envelope with detected systems,
  per-system command + exit code + parsed errors, manifest hygiene
  findings.

## Three invocation modes (same as check-tests)

1. **Cached** — read prior build state if recent (within `--cache-max-age`)
2. **Fresh (`--run`)** — actually invoke build commands
3. **Detection-only** — report what systems were detected without running

Build runs have side effects (some Make targets publish; some npm scripts
deploy). v1 blocklists known-dangerous targets (`publish`, `deploy`,
`release`); `--allow-side-effects` opt-in to skip the blocklist.

## When invoked

1. **Detect build systems.** Walk the repo for known signals
   (pyproject.toml, package.json, go.mod, Cargo.toml, Dockerfile,
   Makefile). Report each detected system with confidence.
2. **Run manifest hygiene** (always; cheap). Check all `*.json` /
   `*.toml` manifests for: parseable, required fields present, version
   string valid (semver), description ≤ 500 chars (per HD-004 anti-bloat).
3. **Run build** (if `--run` passed). Execute per-system command;
   capture stdout/stderr; parse known error patterns.
4. **Compare to baseline** (if exists at `.checkup/{project}/baseline.json`
   under `tier_1_*` keys). Report newly-broken systems as regressions.
5. **Present verdict.** Founder-mode template:

   ```
   🏗 Build check — {scope description}

   Verdict: {builds — all good / something broke / manifests need attention}

   Build systems detected: Python (pip), Node (npm)

   ✓ Python build: succeeded
   ❌ Node build: failed
     • npm install failed: package "@org/private-pkg" not found in registry
     • To investigate: check the npm registry config or auth.

   Manifest hygiene: ✓ all parse; ⚠ 1 with bloated description
     • plugins/old-plugin/.claude-plugin/plugin.json — description is 8,247 chars
       (recommended max 500; consider moving cumulative history to CHANGELOG.md)
   ```

## Gotchas

- **Multi-language monorepo detection.** Repos with Python + Node + Go
  simultaneously can have build systems that overlap or conflict.
  Detection finds ALL; report names each before running.
  *Source: HD-008 source-discovery brittleness pattern.*

- **Builds with side effects.** Some Make targets / npm scripts
  publish artifacts or deploy. Auto-running with `--run` could trigger
  unintended actions. v1 blocklist covers common cases (`publish`,
  `deploy`, `release`); per-project blocklist via
  `.checkup/{project}/dangerous-targets.txt`.
  *Source: founder-facing-conventions Rule 3 (prompt-before-destroy).*

- **First-run has no baseline.** Same as check-tests — first invocation
  captures baseline; explicitly says so; never silently passes.

- **Manifest hygiene false-positives.** Some manifests have intentional
  patterns that look like bloat (legacy cumulative descriptions
  pre-HD-004 cleanup). Hygiene rules know about the marketplace's
  conventions and the HD-004 migration.
  *Source: HD-004 lived experience.*

- **Founder might expect this to FIX broken builds.** Universal
  read-only audit ambiguity. This skill never modifies code; fixing a
  broken build is a separate engineering action.
  *Source: check-readability + check-tests + code-health prior art.*

## Vocabulary

- **build-success** — the build command exits 0 AND produces the
  expected artifact (wheel, dist/, binary, image). Distinct from
  "runs without error" — produces output.
- **manifest-hygiene** — semantic correctness of JSON manifests
  beyond parseability. Required fields, valid version strings, no
  description bloat.
- **build-system** — the toolchain that builds the project.
  Identified by config files: pyproject.toml → pip; package.json → npm;
  go.mod → go; Cargo.toml → cargo; Dockerfile → docker; Makefile → make.
- **build-artefact** — what the build produces. Wheel for pip; dist/
  for npm; binary for go/cargo; image for docker.
- **buildable** — the binary property: does the project build at all?
  Distinct from "builds correctly" (tier 3, where you verify tests pass
  on the build artefact).

## When to invoke this skill

- Founder asks "does it build?", "is the project even working?",
  "did I break the build?", "are my package files OK?"
- Before opening a PR — verify build still works
- After dependency changes — catch resolution failures early
- Code-health invokes this at tier 1 (foundational; checked first)

## When NOT to invoke this skill

- Founder asks "do my tests pass?" — that's `/sulis:check-tests` (tier 3)
- Founder asks "is my code readable?" — that's `/sulis:check-readability`
  (tier 5)
- Founder wants the FIX for a broken build — this skill reports; fixing
  is separate work
- Operator wants raw build output — run pip/npm/go/etc. directly, or
  use `--raw` for the JSON envelope
