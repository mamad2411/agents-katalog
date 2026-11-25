---
name: polyglot-security-stinger
description: Deep security audit for Node servers, Python, Go, Rust, Rails, PHP, Spring, and .NET, plus secrets, dependencies, SAST, and CI. Read-only, writes Audit My Code findings.
license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, Codex, Cowork. Scripts need Python 3.9 or newer (standard library only). Optional tools via go run, pipx, or uvx in a throwaway copy.
metadata:
  author: Legion Code Inc.
  hive-drone: polyglot-security-wasp-drone
  pair-drone: polyglot-security-wasp-drone
  domain: multi-ecosystem security audit
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# Polyglot Security Stinger

Designed and built by Legion Code Inc.

## Where this skill's files are

Every path below (`guides/`, `references/`, `scripts/`) is relative to the folder that contains this `SKILL.md`. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`. If that text was not replaced with a real path, find the folder yourself (for example with Glob for `**/polyglot-security-stinger/SKILL.md`) and use it as `SKILL_DIR` in every command.

## Purpose

Audit the parts of a codebase that are not React, Next.js, or SvelteKit (those have their own pairs) for security weaknesses, ecosystem by ecosystem, and write the results in the Audit My Code contract shape so the brief can show them. It goes deeper than the core generic pass in `security-stinger`: one guide per ecosystem (Node.js servers, Python, Go, Rust, Ruby on Rails, PHP, Java and Kotlin with Spring Boot, .NET), each backed by a checklist, source and sink tables, ripgrep patterns, and vulnerable versus fixed code pairs, plus cross-cutting guides for secrets, dependency vulnerabilities, static analysis, CI/CD and infrastructure, and AI-generated code. It never changes the audited repository; tools run only in the throwaway copy, and anything that cannot run becomes a recorded coverage cap.

## When to use

- An `/audit-my-code` run at `basic`, `full`, or `mario` tier detects `node-server`, `python`, `go`, `rust`, `ruby`, `php`, `java-kotlin`, `dotnet`, or `other` in `intake.json.stacks`
- "Security audit this Django / FastAPI / Flask / Go / Rails / Laravel / Spring / ASP.NET service"
- "Check this monorepo's backend services, CI workflows, and Dockerfiles for security problems"
- Any time the orchestrator needs to know which ecosystems a repository contains: `scripts/detect_ecosystems.py` returns the `intake.json.stacks` array

## When not to use

- React, Next.js, Svelte, or SvelteKit code: `react-security-stinger`, `nextjs-security-stinger`, `sveltekit-security-stinger`
- Fixing the problems found: this pair reports only; remediation planning belongs to the `mario` tier's remediation Drone, and code changes to the owning engineering Drones
- A Ship Gate pass on a branch before commit: `security-stinger`
- Auditing a live third-party website from the outside: `web-security-posture-stinger`

## Procedure

1. Read `audit-my-code-stinger/references/audit-contract.md` and the arming line. Never write inside the audited repository.
2. Run [guides/00-scoping-and-ecosystem-detection.md](guides/00-scoping-and-ecosystem-detection.md): set up the workspace variables and the `rgs` helper, run `scripts/detect_ecosystems.py` on the copy, build the scope table, and mark paths owned by other Drones.
3. For each stack in scope, run its ecosystem guide: [01 Node.js](guides/01-node-server.md), [02 Python](guides/02-python.md), [03 Go](guides/03-go.md), [04 Rust](guides/04-rust.md), [05 Rails](guides/05-ruby-on-rails.md), [06 PHP](guides/06-php.md), [07 Java and Kotlin](guides/07-java-kotlin-spring.md), [08 .NET](guides/08-dotnet-aspnetcore.md). Stack `other` gets the cross-cutting guides plus a manual read.
4. Run the cross-cutting guides in order: [09 secrets](guides/09-secrets-scanning.md), [10 dependencies](guides/10-dependency-vulnerabilities.md), [11 static analysis](guides/11-static-analysis.md), [12 CI/CD and infrastructure](guides/12-ci-cd-and-infrastructure.md) (when this Drone owns the infra files), [13 AI-generated code patterns](guides/13-ai-generated-code-patterns.md).
5. Run [guides/14-writing-findings.md](guides/14-writing-findings.md): write `02-security/findings-polyglot-security-wasp-drone.jsonl`, `metrics-polyglot-security-wasp-drone.json`, and `notes-polyglot-security-wasp-drone.md`, raw output under `02-security/raw/polyglot/`, and an `## Evidence` section in the notes file.
6. Validate with `scripts/validate_findings.py`, fix every error, then return the verdict, finding counts by severity, and every coverage cap.

## References map

| Path | Load when |
| --- | --- |
| `references/cross-cutting/tool-commands.md` | Always: setup, the `rgs` helper, pinned tool commands, the fallback ladder, what to record when a tool cannot run |
| `references/cross-cutting/manifest-to-stack.md` | Checking or hand-classifying ecosystem detection |
| `references/ecosystems/node-server.md` | Guide 01 |
| `references/ecosystems/python.md` | Guide 02 |
| `references/ecosystems/go.md` | Guide 03 |
| `references/ecosystems/rust.md` | Guide 04 |
| `references/ecosystems/ruby.md` | Guide 05 |
| `references/ecosystems/php.md` | Guide 06 |
| `references/ecosystems/java-kotlin.md` | Guide 07 |
| `references/ecosystems/dotnet.md` | Guide 08 |
| `references/cross-cutting/secrets-patterns.md` | Guide 09, or triaging any secret hit |
| `references/cross-cutting/dependency-triage.md` | Guide 10, or deciding an advisory's severity |
| `references/cross-cutting/static-analysis-rulesets.md` | Guide 11 |
| `references/cross-cutting/ci-cd-infra.md` | Guide 12 |
| `references/cross-cutting/ai-failure-patterns.md` | Guide 13 |
| `references/cross-cutting/contract-output-rules.md` | Guide 14, or any question about severity, confidence, or file shape |
| `references/research/distilled-polyglot-security.md` | Verifying a claim, or checking a known thin spot before asserting a framework default |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |
| `scripts/detect_ecosystems.py` | Guide 00; also reusable by the orchestrator for `intake.json.stacks` |
| `scripts/secrets_fallback.py` | Guide 09 when gitleaks and trufflehog cannot run |
| `scripts/validate_findings.py` | Guide 14, before returning |
| `scripts/test_detect_ecosystems.py` | After changing the detector |

## Related drones and stingers

- [polyglot-security-wasp-drone](../../agents/polyglot-security-wasp-drone.md) - The paired agent in this pack; the orchestrator dispatches it with the list of ecosystems and paths.
- `audit-my-code-stinger` - The orchestrator and the run contract this skill writes against.
- `security-stinger` (core) - The generic security pass that runs beside this one in an audit; also the Ship Gate first pass for development work.
- `react-security-stinger`, `nextjs-security-stinger`, `sveltekit-security-stinger` - The framework pairs that own JavaScript UI framework paths.
- `dependency-audit-stinger` (core) - Deeper dependency-management workflows (Renovate, SBOM, provenance) beyond audit triage.
- `devops-stinger` in `platform-and-release-tools` (confirm installed) - Docker and GitHub Actions implementation guidance when a fix is planned.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [audit-my-code-stinger](../audit-my-code-stinger) - Audit My Code orchestrator and the shared run contract.
  - `security-stinger` (core Wasp Nest skill, when installed) - Generic security pass that runs beside this one; Ship Gate first gate for development work.

<!--
Ship Gate removed: research-only stinger, produces no committable code.
-->
