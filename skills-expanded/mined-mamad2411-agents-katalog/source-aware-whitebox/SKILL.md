---
name: source-aware-whitebox
description: Coordination playbook for source-aware white-box testing with static triage and dynamic validation — trimmed to the tools actually available in this local setup.
---

> **Local adaptation:** the upstream stack here also includes `ast-grep`
> (`sg`), `tree-sitter`, and `gitleaks` — none of those are installed in
> this setup. What's actually available: `semgrep` and `trivy fs` (both
> on-demand containers, see `sandbox/tool-images.md`), `trufflehog`
> (on-demand container, covers the secrets-detection role gitleaks would
> have played), and `ripgrep` (installed in the core sandbox) as a manual
> fallback for structural/pattern search when a dedicated AST tool isn't
> available. References to `create_agent`/child delegation map onto Claude
> Code's `Agent`/`Workflow` tools — see `root-agent/SKILL.md`.
> Adapted from an upstream coordination skill (Apache-2.0) — see
> `LICENSE-NOTICE.md` for the source and what changed.

# Source-Aware White-Box Coordination

Use this coordination playbook when repository source code is available.

## Objective

Increase white-box coverage by combining source-aware triage with dynamic
validation. Source-aware tooling is expected by default when source is
available.

## Recommended Workflow

1. Build a quick source map before deep exploitation. Without a dedicated
   AST tool, use `ripgrep` for structural signal (route definitions, auth
   decorators, dangerous sinks) — e.g. `rg -n "app\.(get|post|put|delete)"`
   for route discovery in a Python/JS web app.
2. Run first-pass static triage (`semgrep`) to rank high-risk paths.
3. Use triage output to prioritize dynamic PoC validation.
4. Keep findings evidence-driven: no report without validation.

## Source-Aware Triage Stack (as available in this setup)

- `semgrep` (on-demand container): fast security-first triage and custom pattern scans
- `trufflehog` (on-demand container): secret detection in the working tree
- `trivy fs` (on-demand container): dependency, misconfiguration, and secret checks
- `ripgrep` (core sandbox): manual structural/pattern search fallback where no AST tool exists

Coverage target per repository:
- one `semgrep` pass
- one `trufflehog` pass
- one `trivy fs` pass
- targeted `ripgrep` passes for anything the above miss (route maps, hardcoded
  config, suspicious string patterns)

## Subagent Delegation Guidance

- Keep subagents specialized by vulnerability/component, per `coordination/root_agent.md`.
- For source-heavy subtasks, give the subagent's `Agent` prompt the specific
  files/directories in scope plus the triage-stack commands above — a fresh
  subagent has no context of its own.
- Use source findings to shape payloads and endpoint selection for dynamic
  testing (ffuf/nmap/nuclei, per their own skill files).

## Validation Guardrails

- Static findings are hypotheses until validated.
- Dynamic exploitation evidence is still required before filing a
  vulnerability finding via `reporting/new_finding.py`.
- Keep scanner output concise, deduplicated, and mapped to concrete code
  locations (file + line range).
