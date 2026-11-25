---
name: skill2-package
description: "Use when making a skill repository installable or public: manifests, README, artifacts, releases, publishing, or package checks."
---

# Package and Publish Skill Repositories

Make a Skill repository installable. Add public presentation or remote release work only when requested.

## Select a Profile

- **Native (default):** use the target harness's Git, plugin, marketplace, or package-manager install path. Do not require an archive, checksum, or custom installer.
- **Artifact:** use only when the user requests a distributable archive or the destination requires one. Add versioned artifact, checksum, and artifact install smoke.
- **Release:** use only when the user requests public documentation, push, tag, release, registry, or marketplace work. Read [references/publish.md](references/publish.md).

Use the smallest profile that satisfies the request. Profiles compose; Release does not imply Artifact.

## README Language

`README.md` is always canonical English. When the user's query is primarily non-English, add `README.<language-code>.md`; Chinese uses `README.zh.md`. Explicit language requests override query detection. Preserve existing translations unless removal is requested.

## Candidate

Keep shared behavior in `skills/<name>/SKILL.md`. Add harness metadata only when a target format requires it. Include only resources used by installed skills.

When a Skill ships deterministic tooling, the installed candidate must include that Skill's `scripts/` entrypoint and generated `_runtime/` (or equivalent self-contained resources). Detached install paths must not require repository `src/`, `.venv`, or a global `skill2` CLI.

## Native Gates

- Every Skill passes format and repository lint.
- References, scripts, and assets resolve.
- Scripts are auditable and executable when required.
- Skill-owned runtimes stay in sync with canonical source when the repo generates them.
- Candidate contains no secrets, accidental local paths, or unrelated large files.
- Documented native install path succeeds in a clean temporary home when feasible.
- An installer, when shipped, is explicit, repeatable, conflict-aware, and safe to preview.

## Artifact Gates

- Artifact contains only the intended install candidate.
- Version and checksum identify the exact artifact.
- Clean artifact installation succeeds without repository-only dependencies.

## Output

Return selected profiles, candidate or public destination, relevant verification, remote writes performed, and unresolved blockers.

```bash
uv run --script <skill-dir>/scripts/run -- scaffold skill-repo <name>
uv run --script <skill-dir>/scripts/run -- lint skills
uv run --script <skill-dir>/scripts/run -- package-check . --json
```
