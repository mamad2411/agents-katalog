---
name: xutao-codex-image-archive
description: Install, verify, backfill, uninstall, troubleshoot, or migrate a global Codex chat image archive that preserves pasted clipboard images and image attachments from Codex session logs across projects and conversations. Use when a user wants Codex screenshots or clipboard images saved for history review, wants to install this archive on another computer, wants to inspect archive status, or wants to repair the notify hook.
---

# xutao Codex Image Archive

Use this skill when the user wants Codex chat images, clipboard screenshots, or image attachments preserved across projects and sessions.

## Workflow

1. Inspect whether the archive is already installed:
   - Check `$CODEX_HOME/bin/codex-image-archive`, defaulting to `~/.codex/bin/codex-image-archive`.
   - Check `$CODEX_HOME/config.toml` for `codex-notify-wrapper`.
2. Install or update with `scripts/install.sh`.
3. Run `codex-image-archive report` before backfilling when the user wants a dry-run.
4. Run `codex-image-archive backfill` when the user wants old recoverable images saved.
5. Run `codex-image-archive recent` to verify the notify-time workflow.
6. Run `codex-image-archive repair` when old sessions have missing `/var/folders/...` image paths.

## Commands

From this skill directory:

```bash
scripts/install.sh
scripts/install.sh --backfill
scripts/install.sh --force-original
scripts/uninstall.sh
~/.codex/bin/codex-image-archive repair
```

After installation:

```bash
~/.codex/bin/codex-image-archive report
~/.codex/bin/codex-image-archive recent
~/.codex/bin/codex-image-archive backfill
~/.codex/bin/codex-image-archive repair
```

## Behavior

- Archive root defaults to `~/.codex/chat-image-archive/`.
- Set `CODEX_IMAGE_ARCHIVE_ROOT` to override the archive location.
- The installer saves the existing Codex `notify` command in `original-notify.json`.
- Re-running install does not overwrite `original-notify.json` unless `--force-original` is passed.
- The wrapper calls the original notify command first, then runs `codex-image-archive recent`.
- The archiver deduplicates by SHA-256 and writes `manifest.jsonl` plus `state.json`.

## Safety

- Do not commit user archives, manifests, logs, state files, or images.
- Always preserve unrelated `config.toml` settings.
- If `config.toml` cannot be parsed, stop and report the error instead of overwriting it.
- Uninstall should restore the saved original notify command; it should not delete archived images.
