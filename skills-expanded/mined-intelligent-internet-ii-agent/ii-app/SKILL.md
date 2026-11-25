---
name: ii-app
description: Use this skill when you need to initialize or restart local web and mobile app projects through the bundled Rust `ii-app` CLI instead of calling MCP tools.
---

# ii-app Skill

Use this skill for local app lifecycle actions that should go through the bundled Rust CLI:

- `ii-app web init <template_id>` to scaffold a bundled web template and write a web cache
- `ii-app web restart` to restart the cached tmux-backed web servers
- `ii-app web view-log` to inspect web server output
- `ii-app web screenshot` to open the cached preview URL in `agent-browser`, save a screenshot, and print the file path
- `ii-app web status` to save server log output and a screenshot snapshot to disk, then print the status file path
- `ii-app web checkpoint` to run `bun run build:local`, clean transient build artifacts, and create a git checkpoint commit
- `ii-app web list-templates` to inspect bundled web template IDs
- `ii-app mobile init <project_name>` to scaffold an Expo app and write a mobile cache
- `ii-app mobile restart` to restart the Expo dev server and refresh tunnel/LAN URLs
- `ii-app mobile view-log` to inspect Expo output
- `ii-app stripe register-webhook` to create a Stripe webhook endpoint and write `STRIPE_WEBHOOK_SECRET` into the project `.env`

## Workflow

Resolve the skill root as the directory containing this `SKILL.md`.

1. If `bin/ii-app` is missing or stale, build it with `scripts/build.sh`.
2. Run the binary from the skill root or by absolute path.
3. Prefer `--json` when another agent step needs structured output.
4. Use workspace-local caches unless the user asks for a custom `--cache-path`.

Default cache locations:

```text
<workspace>/.ii-app/web.json
<workspace>/.ii-app/mobile.json
```

## Commands

```bash
"<skill-root>/bin/ii-app" web list-templates
"<skill-root>/bin/ii-app" web init <template_id> --project-name <name> --workspace <dir>
"<skill-root>/bin/ii-app" web restart --workspace <dir>
"<skill-root>/bin/ii-app" web view-log --workspace <dir>
"<skill-root>/bin/ii-app" web screenshot --workspace <dir>
"<skill-root>/bin/ii-app" web status --workspace <dir>
"<skill-root>/bin/ii-app" web checkpoint --workspace <dir> --project-directory <dir>
"<skill-root>/bin/ii-app" mobile init <project_name> --workspace <dir>
"<skill-root>/bin/ii-app" mobile restart --workspace <dir>
"<skill-root>/bin/ii-app" mobile view-log --workspace <dir>
"<skill-root>/bin/ii-app" stripe register-webhook --stripe-secret-key <sk_...> --endpoint-url <https-url> --project-directory <dir>
```

Useful flags:

- `web init --database-url <url>` writes a project `.env`
- `web init --host-url <suffix>` emits preview URLs like `https://3000-<suffix>`
- `web screenshot --annotate` saves an annotated screenshot with numbered labels from `agent-browser`
- `web screenshot --screenshot-dir <dir>` overrides the default screenshot output directory
- `web screenshot --screenshot-format png|jpeg` and `--screenshot-quality <0-100>` map to `agent-browser screenshot`
- `web status --output-dir <dir>` writes a `.log`, optional screenshot, and `.json` summary, then prints the summary path
- `web init --skip-install` and `mobile init --skip-install` avoid dependency installation
- `web init --skip-start` and `mobile init --skip-start` avoid starting tmux or Expo after setup
- `mobile init --template tabs|blank|blank-typescript` chooses the Expo starter
- `mobile init --example with-reanimated` creates from an official Expo example instead of a template
- `mobile init --no-tailwind` skips NativeWind-related install steps
- `stripe register-webhook --event evt1,evt2` overrides the default Stripe event set
- `stripe register-webhook` writes only `STRIPE_WEBHOOK_SECRET` to `.env`; it does not print the secret in plain-text output
- `view-log --session <name>` targets a specific tmux session
- `--json` is supported by every command

## References

- For web template IDs and mobile starter options, read `references/template-ids.md`.
- For cache shapes and CLI output expectations, read `references/cli-contract.md`.
