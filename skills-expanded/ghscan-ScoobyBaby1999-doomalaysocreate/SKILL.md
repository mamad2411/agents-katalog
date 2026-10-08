---
name: workspace-artifacts
description: How to produce downloadable artifacts in doomalaysocreate's agent workspace — pack files/repos into zips, organize outputs, and tell the user what to download. Use whenever the user asks you to create, build, export, package, or hand back files.
---

# Producing artifacts the user can download

You are running inside the user's own private doomalaysocreate Space. Your current working
directory is a per-session **workspace** that the app exposes to the user: any
regular file you write there appears in the "artifacts" strip below the chat,
with a download button. Dotfiles and `.claude/` are hidden from that list.

## Conventions

- **Write outputs to the workspace root** (your cwd), not to `/tmp` or `$HOME` —
  only the workspace is surfaced for download.
- **Prefer a single bundle** when handing back many files. Pack them into one zip
  so the user taps one button:
  ```bash
  zip -r project.zip project/ -x '*/node_modules/*' '*/.git/*'
  ```
- **Unpacking** an archive the user references: `unzip -o archive.zip -d unpacked/`.
- **Repos**: `git clone <url> repo && ...`. To hand a repo back as a reviewable
  bundle, zip it excluding `.git` and dependency dirs.
- The disk is **ephemeral** — it is wiped when the Space restarts. After you
  finish, end your message by telling the user which artifact(s) to download and
  that they are temporary.

## After creating files

List what you produced and name the download(s) explicitly, e.g.:

> Done. Download **report.zip** from the artifacts strip — it contains the
> generated report and charts. The workspace is temporary, so grab it now.
