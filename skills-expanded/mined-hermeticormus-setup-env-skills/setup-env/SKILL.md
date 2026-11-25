---
name: setup-env
description: Set up a project's development environment. Check requirements and versions, install runtime and dependencies from the lockfile, configure env vars and config files, verify with a working first run, and document what was done. Use when setting up a project from a bare clone, onboarding onto an unfamiliar codebase, or reproducing a "works on my machine" environment.
license: MIT
---

# Setup environment

A protocol for setting up a project's development environment from a bare clone to a working first run.

**Tradeoff**: bias toward verifying each step over assuming it worked. For a project set up recently, use judgment.

## 1. Check requirements

Read the project's own docs and version files (`README`, `.tool-versions`, `engines`, `python_requires`, `go.mod`, `Cargo.toml`). Note the required runtime and version, note system dependencies, and compare against what is installed. A version mismatch is the most common setup failure. Report gaps before closing them.

## 2. Install the runtime and package manager

Install the version the project asks for, not the latest. Prefer a version manager (`nvm`, `pyenv`, `rbenv`, `rustup`) over a system-wide install. Use the package manager the lockfile implies.

## 3. Install dependencies

Install from the lockfile (`npm ci`, `poetry install`) so the dependency graph matches the committed one. For Python, create an isolated virtualenv first. If install fails, read the first error, not the last.

## 4. Configure environment and config files

Copy `.env.example` to `.env` and fill every variable. Generate local secrets the project needs. Do not commit secrets or invent placeholder secret values.

## 5. Verify with a working first run

Build, test, then start. Observe behavior rather than trusting an exit code: hit the health endpoint, load a page, run the CLI with `--help`. If a step fails, trace it to the earlier step it came from and fix that step, not the symptom.

## 6. Document what was done

Record the exact steps, the non-obvious gotchas, and the common-command set (build, test, run, lint) so the next person reproduces it without rediscovery.

---

See full content at https://github.com/HermeticOrmus/setup-env-skills.
