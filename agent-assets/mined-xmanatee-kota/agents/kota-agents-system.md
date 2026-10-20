# System Module

This directory contains the system capability pack — a repo module that owns host OS interaction tools.

- This is the canonical home for clipboard, image-viewing, environment-discovery, and SQLite tools. Do not add these to `src/core/tools/`.
- Tools, helpers, and tests are co-located here, following the pattern established by `web-access/` and `filesystem/`.
- Read-only tools (`clipboard` read, `view_image`, `env_info`) are classified as safe in guardrails.
- Write tools (`clipboard` write) and mutating tools (`sqlite` query) are classified as safe/moderate respectively.
- Image-observation tools use `detail: "resized" | "original"` for fidelity.
  `resized` stays the default; `original` must return original bytes or fail
  when the declared safety limit is exceeded. Output should report original
  and returned dimensions, returned bytes, original bytes, and whether pixels
  were resized.

## Boundaries

- Does not own shell execution, code REPL, or file I/O — those belong in `execution/` and `filesystem/`.
- Does not own web/HTTP access — that belongs in `web-access/`.
- Does not own git operations — that belongs in `git/`.
