---
name: setup-office-kit
description: Install or update an isolated OfficeKit workspace inside the current repository. Use before creating OfficeKit documents, slides, videos, brands, or narration when a .office-kit workspace is absent or needs an upgrade.
compatibility: Requires Python 3.10+, Node.js 22+, npm, and uv. ffmpeg is required for final video encoding. Initial dependency setup needs network access.
metadata:
  author: OfficeKit
  version: "0.2.0"
---

# Set up OfficeKit

Create an isolated `.office-kit/` workspace in the current repository
(a dot-directory, so it stays out of the host project's own tree and
tooling). A workspace an earlier version installed as `office-kit` (no
leading dot) is still recognised and updated in place; rename it to
`.office-kit/` to adopt the new default. Do not
copy this plugin by hand and do not merge OfficeKit's package files into the
host repository root.

Resolve `scripts/bootstrap.py` relative to this `SKILL.md`, then invoke that
resolved script while the shell's working directory is the host repository
root:

```bash
uv run python <setup-office-kit-skill-root>/scripts/bootstrap.py
```

The placeholder above is explanatory; replace it with the actual skill path.
The destination remains the current working directory's `.office-kit/`.

The bootstrapper:

- copies only the allowlisted OfficeKit-authored workspace payload;
- creates `.office-kit/projects/` for deliverables;
- installs Python dependencies with `uv sync`;
- initializes npm at the workspace root, preserving one shared
  `.office-kit/node_modules/`;
- records managed file hashes in `.office-kit/.officekit-managed.json`;
- refuses to overwrite an unrelated directory or a user-modified managed file.

Use `--no-install` only for offline setup or tests. Use `--target PATH` when
the user explicitly wants a different workspace directory. `--force` may
replace only OfficeKit-managed payload files; it never deletes projects,
additional brands, or unrelated files.

After setup, run all OfficeKit commands from the generated workspace:

```bash
cd .office-kit
uv run python scripts/document/doc.py --help
uv run python scripts/presentation/deck.py --help
uv run python scripts/video/video.py --help
```

Report the workspace path and any missing runtime prerequisite. Never claim
setup succeeded when dependency installation failed.
