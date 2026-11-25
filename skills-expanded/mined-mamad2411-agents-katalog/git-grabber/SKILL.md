---
name: git-grabber
description: Copy a specific public GitHub folder or file into the current working directory from a shared GitHub tree/blob URL. Use when a user shares a GitHub folder or file link and asks to clone, grab, download, or copy only that subpath instead of the whole repo.
---

# GitHub Path Cloner

Copy a specific public GitHub folder or file into the current working directory without cloning the entire repository.

## Source URL

$ARGUMENTS

## When to Use

Invoke this skill when the user:
- Shares a `github.com/.../tree/...` or `github.com/.../blob/...` URL
- Asks to clone, grab, copy over, or download just that folder or file
- Wants a GitHub subpath locally instead of the full repo

## Approach

Use the bundled script `scripts/github_path_cloner.py`.

The script follows the same general approach as DownGit:
- Parse the GitHub URL into owner, repo, ref, and subpath
- Resolve ambiguous refs safely
- Traverse directories with the GitHub contents API
- Download file bytes directly
- Write the requested folder or file into the destination directory

## Workflow

1. Use the URL provided in the $ARGUMENTS as the source.
2. Default the destination to the current working directory unless the user asked for a different target.
3. Do not overwrite an existing top-level target silently. If there is a collision, either confirm with the user or use `--overwrite` if they already asked for replacement.
4. Run the bundled script with an absolute destination path.
5. Inspect the copied result and report what was written.

## Commands

Copy a folder and preserve its root directory name:

```bash
python3 scripts/github_path_cloner.py \
  "$ARGUMENTS" \
  --dest "$PWD"
```

Copy only the folder contents into the destination directory:

```bash
python3 scripts/github_path_cloner.py \
  "$ARGUMENTS" \
  --dest "$PWD" \
  --strip-root
```

Copy a single file:

```bash
python3 scripts/github_path_cloner.py \
  "$ARGUMENTS" \
  --dest "$PWD"
```

Replace an existing copied target when the user explicitly wants that:

```bash
python3 scripts/github_path_cloner.py \
  "$ARGUMENTS" \
  --dest "$PWD" \
  --overwrite
```

## Notes

- Public GitHub repositories only
- `GITHUB_TOKEN` is optional but helps avoid GitHub API rate limits
- Directory copies preserve the shared folder name by default
- `--strip-root` copies the selected directory contents directly into the destination directory
