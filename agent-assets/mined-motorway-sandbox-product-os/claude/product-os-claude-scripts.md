# Scripts

Automation scripts for the PM workspace. Deployed to `~/.local/bin/pm-workspace/` via `deploy.sh` and run by macOS launchd or manually.

## Conventions

- **Naming:** `{frequency}-{purpose}.sh` — e.g. `daily-meeting-prep.sh`, `weekly-analyst-refresh.sh`
- **Prompt files:** Each Claude-invoking script has a companion `{script-name}-prompt.txt` with the prompt template
- **Shared library:** All scripts source `lib.sh` for standard paths, env loading, logging, and helpers. Call `mw_init "script-name"` after sourcing
- **Alert wrapper:** `run-with-alert.sh` wraps launchd jobs — sends Telegram + Slack alerts on failure, Slack on success
- **Environment:** Scripts expect `.env` at the deploy dir (see `.env.example` for required vars)

## Deployment

Scripts are **authored here** but **run from** `~/.local/bin/pm-workspace/`. The deployment flow:

1. Edit scripts in this directory
2. Run `bash scripts/deploy.sh` to copy files to their runtime locations
3. Use `bash scripts/deploy.sh --check` for a dry run

## Key files

- `lib.sh` — shared library (source this, don't run directly)
- `deploy.sh` — deployment tool
- `run-with-alert.sh` — alert wrapper for launchd jobs
- `notify-telegram.sh` — Telegram notification helper
- `setup-notebooks.sh` — one-time Jupyter notebook environment setup
- `examples/` — complete example automation (script + prompt + plist)

See `scripts/README.md` for the full guide.
