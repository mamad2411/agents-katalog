---
name: itsol-current-tech-context
description: "Verify repo-pinned and current framework, SDK, package, runtime, and API behavior."
---

# ITSOL Current Tech Context

Use current technology facts instead of stale model memory. Before making planning or review claims about a framework, SDK, runtime, library, package, edition, API, generator, or tool, verify what the repo uses and what the current official documentation says.

## Process

1. Detect the technology context from the repo first: manifests, lockfiles, toolchain files, SDK pins, Dockerfiles, CI, generated clients, API schemas, build scripts, package managers, and framework config.
2. Determine whether the user or repo pins a version, edition, SDK, runtime, package manager, or compatibility target. Honor explicit pins and document the constraint.
3. When internet access is available, check current official documentation, release notes, package registries, or language/runtime docs for the detected versions and for the latest stable version when planning a new project.
4. Prefer official sources and primary package registries: framework docs, language docs, SDK docs, npm, crates.io, NuGet, Docker Hub or vendor docs, GitHub releases, and official migration guides.
5. For an existing repo, plan and review against the version the repo actually uses. Recommend upgrades only when they are in scope, low risk, or necessary for security/support; otherwise record them as follow-up risk.
6. For a new project, default to the latest stable ecosystem choices unless the user requests older versions, compatibility targets, or long-term support constraints.
7. For Rust, prefer the latest stable Rust toolchain and newest stable edition supported by the current toolchain unless the repo pins otherwise.
8. For .NET, prefer the latest stable SDK/LTS choice appropriate to the project constraints; if the user asks for production longevity, explicitly compare current STS/LTS tradeoffs.
9. For Bun/npm/Node projects, use the package manager detected in the repo. For new projects, choose current stable packages and record major-version assumptions.
10. Include the result in plans and reviews as `Current Tech Context`: versions found, sources checked, version/upgrade decisions, compatibility risks, and any places where internet access was unavailable.

## Focused References

- [01-output-and-existing-repo.md](./references/01-output-and-existing-repo.md) - Output And Existing Repository
- [02-new-projects-and-sources.md](./references/02-new-projects-and-sources.md) - New Projects And Sources
- [03-planning-and-review-rules.md](./references/03-planning-and-review-rules.md) - Planning And Review Rules
