---
name: scratch-artifact-naming
description: >-
  Base primitive — resolve a session-scoped scratch artifact STEM path under
  `<repo>/scratch/<session-id>/`, either the timestamp variant
  `<purpose>_<YYYY-MM-DD_HH-MM-SS>` or the git-ref variant
  `<purpose>_<ref-slug>_<full-sha>`. Auto-discovers the opencode session ID,
  creates the session directory idempotently, and emits the absolute stem so
  callers simply append the extension.
category: General-Domain
---

# Scratch Artifact Naming (v1)

> **Skill ID:** `scratch-artifact-naming`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

This is the **base** skill for the session-scoped scratch artifact scheme.
Every artifact a workflow captures under `<repo>/scratch/` must live in a
session-named subfolder and carry one of two machine-parsable names: a
timestamp variant for command output (`<purpose>_<YYYY-MM-DD_HH-MM-SS>`) or a
git-ref variant for content captured at a specific commit
(`<purpose>_<ref-slug>_<full-40-hex-sha>`).

The skill resolves the session-scoped path deterministically — auto-discovering
the current opencode session ID (via `opencode-current-session-id`), creating
the `<repo>/scratch/<session-id>/` folder idempotently, and emitting the
absolute **stem** path on stdout so callers only append the file extension.

## Scope & Intent

*In scope:*

- Compute the session-scoped scratch path `<repo>/scratch/<session-id>/` for any artifact.
- Emit the absolute **STEM** path (no extension) — callers append `.out` / `.err` / `.json` / etc.
- Support the two naming variants:
    - **Timestamp variant** (command output / probe / log): `<purpose>_<YYYY-MM-DD_HH-MM-SS>`
    - **Git-ref variant** (content captured at a commit): `<purpose>_<ref-slug>_<full-40-hex-sha>`
- Auto-discover the current opencode session ID (via `opencode-current-session-id`)
  when `--session-id` is omitted; strip any `ses_` prefix from the folder name.
- Create `<repo>/scratch/<session-id>/` idempotently (`--no-mkdir` to override).

*Out of scope:*

- Writing the actual file content (that belongs to the caller / composer script).
- The `.out`/`.err` pairing doctrine is owned by
  [`repo-scratch-output-capture`](../../../repo-scratch-output-capture/SKILL.md).
- Capturing a file at a git ref (composer: `git-ref-artifact-extract`).

## Environment & Dependencies

| Requirement | Version | Notes |
| ------------- | --------- | ------- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| `opencode-current-session-id` skill | present | Composed only for auto-discovery (graceful fallback) |
| Git repo | — | `--repo` must resolve to an existing directory |

## CLI Contract

```text
python3 scripts/resolve-scratch-path.py --repo <path> --purpose <slug>
    [--session-id <id>] [--ref-name <slug>] [--ref-sha <full-sha>]
    [--timestamp <ts>] [--no-mkdir]
```

| Argument | Required | Description |
| ---------- | ---------- | ------------- |
| `--repo <path>` | No | Repo root (default: CWD) |
| `--purpose <slug>` | Yes | Lowercase-kebab purpose slug |
| `--session-id <id>` | No | Full opencode session ID (`ses_` prefix optional); auto-discovered when omitted |
| `--ref-name <slug>` | No | Lower-kebab ref slug (with `--ref-sha` selects ref variant) |
| `--ref-sha <sha>` | No | Full 40-hex commit SHA (with `--ref-name` selects ref variant) |
| `--timestamp <ts>` | No | `YYYY-MM-DD_HH-MM-SS` override (tests) |
| `--no-mkdir` | No | Print without creating the session directory |

**Output:** absolute STEM path on stdout (no extension; caller appends `.ext`).

*Exit codes:*

- `0` — success
- `1` — invalid `--purpose` / unpaired or malformed ref args / repo missing / session discovery failure / mkdir failure
- `2` — argparse usage error

## Protocol

1. Confirm the artifact is intended for session-scoped scratch under the target repo.
2. Run `python3 .agents/skills/general/file/scratch-artifact-naming/scripts/resolve-scratch-path.py --repo <repo>
   --purpose <purpose-slug> [--ref-name <slug> --ref-sha <sha>]`.
3. Append the appropriate extension to the printed stem and capture output there.

## Edge Cases

- **Timestamp collisions**: two captures within the same second collide on stem —
  pass `--timestamp` explicitly or rely on the ref variant (full SHA is unique).
- **Unnamed session at repo root**: a repo outside `.opencode/logs` discovery
  scope has no session — pass `--session-id` explicitly.
- **No `.git` in repo**: does not require git; only checks the directory exists.
- **`ses_` prefix handling**: both `--session-id ses_02c6…` and
  `--session-id 02c6…` resolve to folder `scratch/02c6…/`.
- **Concurrent sessions in the same repo**: the composed auto-discovery is
  pending-marker-first (the in-flight session wins) with newest-mtime fallback,
  and can still resolve to a sibling session when multiple sessions are truly
  active. NEVER pin `--session-id` from a remembered or deduced value — IDs
  change on fork; omit the flag (auto-discovery) or pass only an ID resolved in
  the current run or supplied by the user.

## Prohibited Actions

- Do NOT re-derive the naming formula in caller scripts — always pipe through
  this script (SSOT for the scheme).
- Do NOT hardcode session-scope folders like `scratch/<purpose>.out` at the
  scratch root (flattens and collides across sessions).
- Do NOT write timestamps into the ref variant NOR commit SHAs into the
  timestamp variant — each variant is defined by its inclusion/exclusion.
- Do NOT pass `--session-id` values deduced from artifact filenames, scratch
  folders, or prior conversation context — session IDs change on fork. Omit the
  flag (auto-discovery) or use an ID resolved in the current run.

## Script Reference

`resolve-scratch-path.py`:

1. Validates `--purpose` (lowercase-kebab) and ref pairing/shape.
2. Resolves `--repo` to absolute; fails on nonexistent dir.
3. Resolves session ID: strips `ses_` from `--session-id`, else composes
   `opencode-current-session-id` (REPO_ROOT-relative discovery).
4. Creates `<repo>/scratch/<session-id>/` (mkdir parents, idempotent).
5. Prints `session_dir / "purpose_<ts>"` or
   `session_dir / "purpose_<ref-name>_<ref-sha>"`.

## Composition by Higher-Level Skills

- [`git-ref-artifact-extract`](../../../git-ref-artifact-extract/SKILL.md) —
  composer; captures a file at any git ref into session-scoped scratch by calling
  this script with `--ref-name --ref-sha`.
- [`repo-scratch-output-capture`](../../../repo-scratch-output-capture/SKILL.md) —
  enriched sibling; delegates its naming to this script.

## Related Skills

- [`opencode-current-session-id`](../../../opencode/opencode-current-session-id/SKILL.md) — the
  discovery script this skill composes for auto session-ID.
- [`git-commit-metadata-extraction`](../../../git-commit-metadata-extraction/SKILL.md) —
  provides the git-ref plumbing a composer may need before calling this skill.
- [`opencode-session-path-attribution`](../../../opencode/opencode-session-path-attribution/SKILL.md)
  — related — evidence cards (attribution results) land in session-scoped scratch.
