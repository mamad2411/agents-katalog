---
name: follow-tool-semgrep-config-rules
description: Configure Semgrep rules — custom YAML rules, registry rulesets, and CI gating
argument-hint: "[ruleset-or-path]"
related:
  - follow-tool-semgrep
  - use-astgrep
  - update-config
  - run-scan
  - setup-cicd
---

## Goal

Configure Semgrep rules as versioned config in the repo — custom YAML rules, registry rulesets selection, and CI gating

## Scope

- Rule config for a Semgrep that is already installed (scan-only usage → parent skill)
- Covers: `.semgrep/` custom rules, rule YAML anatomy, `p/*` registry rulesets, `--test`, CI gating
- Does not cover: fixing findings (`/deep-review-codebase` or `/fix`)

## Execute

### 1. Choose Rule Sources

> Goal: Decide custom vs registry per the coverage you need

1. Registry rulesets — `p/default`, `p/security-audit`, `p/owasp-top-ten`, `p/<language>`, `p/<framework>` — start narrower first, `p/default` can be noisy
2. Custom rules — project-specific patterns, internal API misuse, banned functions — keep in `.semgrep/` or `semgrep.yml`
3. Simple structural patterns → consider `use-astgrep` first (faster, no install); semgrep when you need taint/dataflow

### 2. Write Custom Rules

> Goal: Correct, testable custom rules

1. Create `.semgrep/<domain>.yml` — a top-level `rules:` list
2. Each rule must have: `id` (namespaced, e.g. `project.no-fetch-in-loop`), `patterns`/`pattern`/`pattern-either`, `message`, `severity` (`ERROR`/`WARNING`/`INFO`), `languages`
3. Use `pattern-inside`, `pattern-not`, `metavars` (`$X`), `pattern-regex` as needed — see the official docs for advanced operators (`pattern-sources`/`pattern-sinks` for taint)
4. Add `metadata` such as `category`, `cwe`, `references` for triage
5. Write a paired test file (e.g. `.semgrep/<domain>.ts` with `// ruleid:`/`// ok:` annotations) then run `semgrep scan --test .semgrep/`

### 3. Wire Local And CI Config

> Goal: The ruleset is selected consistently across local and CI

1. Combine configs: `semgrep scan --config=.semgrep/ --config=p/security-audit` — custom + registry can be mixed
2. Use `.semgrepignore` to skip tests/generated/vendored paths (syntax similar to `.gitignore`)
3. Choose a baseline strategy for legacy — `--baseline <ref>` shows only new findings

### 4. CI Gating

> Goal: Make semgrep a controllable quality gate

1. A CI step running `semgrep scan --config=<...>` — use `--error` to exit non-zero when findings exist (gate)
2. Output `--sarif` for GitHub code scanning or `--json` for processing
3. If using the Semgrep AppSec Platform → `semgrep login` + `semgrep ci` instead of `scan`
4. Pin the ruleset in CI — ruleset change = findings change; don't let the gate break from upstream
5. Triage loop: `// nosemgrep` with a reason for intentional patterns — never suppress without a comment

### 5. Verify

> Goal: Rules fire correctly and the gate behaves

1. Run `semgrep scan --config=.semgrep/ <path>` — custom rules fire on a known-bad sample
2. Run `semgrep scan --test .semgrep/` — rule tests pass
3. Run the CI command locally — the exit code matches what the gate expects
4. If verification fails → run `/resolve-errors` max 3 rounds, then report

## Rules

- Custom rules must live in the repo with tests — never a rule that has never passed `semgrep scan --test`
- Every rule has a namespaced `id`, an actionable `message`, and an appropriate `severity`
- Pin ruleset versions in CI — don't track latest uncontrolled
- `// nosemgrep` must always have a reason comment
- Start the ruleset narrow — increase coverage gradually so signal doesn't drown in noise
- If unsure about rule syntax → see the official docs (Semgrep rule schema)

## Expected Outcome

- `.semgrep/` holds custom rules with rule tests that pass
- Registry rulesets selected per goal, with a baseline strategy
- A CI gate with `--error`/SARIF behaving correctly and findings triaged
