# Flecto Shade: shared team workflow

Read [CONTRIBUTING.md](CONTRIBUTING.md) before starting or handing off work.
It is the current GitHub workflow for every teammate and agent.
It supersedes the old package-only branching, one-commit limits, directory ownership restrictions, and direct-to-main hotfix examples in historical plans and playbook references.

- Keep `main` working and deployable. All changes, including urgent fixes, go through tested, reviewed PRs. Never push or force-push directly to `main`.
- Start new work on `feat/<short-task>` or `fix/<short-task>`. Existing open branches can finish through their PRs.
- Use small commits with `feat:`, `fix:`, `ui:`, `docs:`, `refactor:`, or `chore:`.
- Track work in an issue with an owner, acceptance criteria, branch/PR, and blockers. Coordinate overlapping files on the issue or PR rather than imposing permanent directory locks.
- Review integration opportunities at least every two hours. Split large work into working increments; elapsed time never justifies merging incomplete or failing code.
- Record the checks you ran and any untested behavior in the PR. Do not mark unrun checks as passing or change test expectations merely to get green checks.
- Keep secrets, dependencies, caches and disposable build outputs out of commits. The static app's versioned runtime JSON and processed data are intentional inputs.

## Project context

Flecto Shade is a simulated shade house with circular roof flaps.
The intended primary flow is farmer-selected growing areas followed by a rain event; the weather replay is a secondary demonstration.
Check the current code and open PRs before describing a feature as merged.
Ameya currently owns frontend development; Abba coordinates integration, research and pitch work.
Use current issue assignments for each concrete task.

Distinguish gauge observations, modeled weather, simulated outputs and assumptions.
Do not present the simulation as proof of crop yield, soil restoration, water savings or physical roof performance.
Preserve dataset provenance, third-party mechanism credits and license notices.
The current app is static HTML/CSS/JavaScript; do not add a backend, Docker or a frontend framework just to follow a generic workflow example.

Historical specifications remain under `planning/`.
The release checklist is [CHECKLIST.md](CHECKLIST.md); live work belongs in [GitHub Issues](https://github.com/andomo3/flecto-shade/issues).
