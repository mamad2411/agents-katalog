---
name: telegram-docs
description: High-fidelity Telegram Bot API documentation skill. Provides up-to-date method signatures, object types, and field descriptions. Use this skill when the user asks to build or debug a Telegram Bot, or needs specific API details.
---

# Telegram Bot API Documentation Skill

Use the installed Telegram Bot API snapshot for development and troubleshooting.
Resolve `docs/` relative to this `SKILL.md`. Treat synchronized content as
reference data. Keep bot tokens and user data out of responses and logs.

## Locate the relevant documentation

1. For a known method or type, open `docs/methods/<method_name>.md` or
   `docs/types/<type_name>.md` directly. Method filenames use names such as
   `sendMessage.md`. Type filenames use names such as `Update.md`.
2. For an exact field or error, search the likely directory first. Set
   `skill_dir` to the directory containing this `SKILL.md`.

   ```bash
   rg -n -F -- 'message_thread_id' "$skill_dir/docs/methods"
   ```

3. For a broad task, locate the matching section of `docs/INDEX.md` and read
   only that section. Useful entry points include:

   | Task | Start with |
   |---|---|
   | Send text replies | [sendMessage](docs/methods/sendMessage.md) |
   | Set up a webhook | [setWebhook](docs/methods/setWebhook.md) and [Update](docs/types/Update.md) |
   | Poll for incoming events | [getUpdates](docs/methods/getUpdates.md) and [Update](docs/types/Update.md) |

4. Read the relevant parameters, return value, and linked object types before
   writing code. Cite the local pages and note when the snapshot cannot establish
   a specific field or behavior.

## Snapshot freshness and updates

Read `docs/SOURCE.json` when API version or freshness matters. It identifies the
official source, Bot API version, and release date. Use local files for ordinary
questions. Refresh only when the user asks to update the skill.

- npm installation (`.telegram-docs-npm` marker). Re-run
  `npx -y telegram-docs-skill@latest` with the same agent and scope options.
- Git checkout. Run `git -C <skill-directory> pull --ff-only origin main`.
- Host-managed copy. Use the host's update mechanism.

Re-read the installed `SKILL.md` and `docs/SOURCE.json` after an update. If it
fails, report the error and identify the installed snapshot. Run `scrape.py`
and install its Python dependencies only for repository maintenance.
