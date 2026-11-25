---
name: dev-environment-manager
description: "Reproducible, containerized dev environments — devcontainers, dotfiles, tooling, and configuration as code. Use when setting up or standardizing a dev environment."
version: 1.0.0
platforms: [linux, macos]
---

# Dev Environment Manager

## What It Does
Manages reproducible development environments as code. Creates and maintains devcontainer configurations, dotfiles, tool version management, and environment provisioning scripts. Ensures every developer on a team has an identical, working environment — eliminating "works on my machine" and reducing setup time from hours to minutes.

## Iron Laws (NEVER violate)
1. **Environment as code** — Dev environment configuration lives in version control alongside application code. No manual setup steps.
2. **Deterministic builds** — Same configuration always produces the same environment. Pinned versions, locked dependencies, checksum verification.
3. **Isolation by default** — Every project gets its own isolated environment. No global dependency conflicts.
4. **Fast start** — New team member must go from zero to running tests in under 15 minutes. Longer = broken onboarding.

## Red Flags (STOP immediately)
- **Drifting environments** — Two developers on same project have different tool versions → environment config not enforced
- **"Works on my machine"** — Bug that reproduces on one machine but not another → environment inconsistency
- **Secret in config** — API keys, tokens, or credentials in devcontainer or dotfiles config → security breach
- **Platform lock-in** — Environment only works on macOS → exclude Linux/Windows developers

## Common Rationalizations (self-deception)
- "Everyone installs tools differently, it's fine" → Tool version differences are a leading cause of "mystery bugs."
- "Devcontainers add overhead" → The overhead of debugging environment issues is 10x the overhead of containers.
- "We'll standardize environments later" → Environment drift compounds. The longer you wait, the harder the fix.

## When To Use
- Setting up a new project with multiple developers
- Standardizing tool versions across a team (Node, Python, Go, Rust, etc.)
- Migrating from manual setup to devcontainers
- Creating dotfiles management for personal development setup
- Troubleshooting "works on my machine" issues

## Human Partner Signals (escalate to human)
- **Hardware constraints** — Environment requires resources (RAM, disk) some developers don't have → lightweight alternative needed
- **License restriction** — Required tool requires paid license → procurement decision
- **Security policy conflict** — Devcontainer configuration conflicts with corporate security policy → negotiation needed
- **Legacy system** — Project can't be containerized due to legacy dependencies → alternative approach needed

## Pipeline
1. Audit: inventory current tools, versions, and manual setup steps across the team
2. Design: choose environment strategy — devcontainers, nix, docker-compose, or hybrid
3. Implement: create devcontainer.json / Dockerfile / nix flake with pinned versions
4. Configure: set up dotfiles — shell config, editor settings, git aliases, linting/formatting
5. Automate: create bootstrap script — one command to install, configure, and verify
6. Test: verify environment works on all supported platforms (macOS, Linux, Windows/WSL)
7. Document: add setup instructions (one-liner), troubleshooting guide, and update process

## Verification Checklist
- [ ] Single bootstrap command works on all supported platforms
- [ ] All tool versions pinned (no floating "latest" tags)
- [ ] Fresh environment passes full test suite without manual intervention
- [ ] Devcontainer starts and is usable within 2 minutes
- [ ] No secrets or credentials in version-controlled config files
- [ ] Environment update process documented and tested
- [ ] Cross-platform testing completed (macOS + Linux minimum)

## Related Skills
- `onboarding-automator` — Dev environment is the first step of onboarding
- `docker-k8s-pro` — Container expertise for devcontainer design
- `documentation-generator` — Environment setup docs generated and kept current
- `supply-chain-verifier` — Verify tool and dependency provenance
