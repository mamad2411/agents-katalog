---
name: pantheon-terminus
description: Pantheon Terminus CLI (v4.x) — install, machine-token auth, the full command directory, scripting, plugins, and CI authentication for GitHub Actions, GitLab, CircleCI, and Bitbucket. Use when running terminus commands, automating Pantheon site workflows, or authenticating Terminus in CI.
license: CC-BY-SA-4.0
metadata:
  source: https://docs.pantheon.io/terminus
  upstream: https://github.com/pantheon-systems/terminus
  category: cli
---

# Pantheon Terminus CLI

Terminus is the command-line interface for advanced interaction with the Pantheon platform. It can do almost everything the Dashboard can, plus scripting and automation: create sites, manage Multidev environments, clone environments, apply upstream updates, deploy code, and run Drush/WP-CLI commands remotely.

This skill captures the Pantheon Terminus Guide **verbatim** (CC BY-SA 4.0, © Pantheon Systems, Inc.) into the reference files below. Prose is faithful to the source; only Docusaurus frontmatter and JSX components were normalized to standard Markdown.

> **Prefer the live binary over memory.** Terminus releases often. For exact flags, run `terminus <command> --help` or `terminus list --raw` locally, and check <https://github.com/pantheon-systems/terminus/releases> for the current version.

## Quick Start

```bash
# macOS (recommended)
brew install pantheon-systems/external/terminus

# Linux / Windows (WSL) / macOS-without-brew — Terminus 4 (PHP 8.2+)
mkdir -p ~/terminus && cd ~/terminus
curl -L https://github.com/pantheon-systems/terminus/releases/latest/download/terminus.phar --output terminus
chmod +x terminus
sudo ln -s ~/terminus/terminus /usr/local/bin/terminus

# Authenticate (machine token from dashboard.pantheon.io → Account → Machine Tokens)
terminus auth:login --email=<email@example.com> --machine-token=<machine_token>

# Subsequent sessions only need the email
terminus auth:login --email=<email@example.com>
```

**Requires:** PHP 8.2+, Composer, Git, OpenSSH 7.8+. Terminus 4.x supports PHP 8.2–8.5. (Terminus 3.x is the last line supporting PHP 7.4–8.3 and is not compatible with PHP 8.4.)

## Command Format

```bash
terminus command:subcommand <site>.<env>      # e.g. terminus env:clear-cache my-site.live
terminus command:subcommand -h                 # help for any command
terminus list --raw                            # all commands, one per line
```

`<site>.<env>` is optional if you run Terminus from inside a checked-out Pantheon site repo on the matching branch — it auto-detects. `<site>` is the machine name (e.g. `my-site`), `<env>` is `dev` / `test` / `live` / a Multidev name.

## Cheatsheet — Most-Used Commands

| Task | Command |
|------|---------|
| Sites you can access | `terminus site:list` |
| Site info / UUID | `terminus site:info <site>` |
| Env status & config | `terminus env:info <site>.<env>` |
| Connection mode | `terminus connection:set <site>.dev git\|sftp` |
| Commit SFTP changes | `terminus env:commit <site>.dev --message="..."` |
| Deploy Dev→Test / Test→Live | `terminus env:deploy <site>.test --sync-content --note="..."` |
| Clear cache | `terminus env:clear-cache <site>.<env>` |
| Clone db+files between envs | `terminus env:clone-content <site>.live dev` |
| List/apply upstream updates | `terminus upstream:updates:list <site>` → `terminus upstream:updates:apply <site>` |
| Backup | `terminus backup:create <site>.live` |
| Restore latest backup | `terminus backup:restore <site>.live` |
| Multidev create / delete | `terminus multidev:create <site>.dev <name>` / `terminus multidev:delete <site>.<name>` |
| Run Drush remotely | `terminus remote:drush <site>.<env> -- <drush_cmd>` |
| Run WP-CLI remotely | `terminus remote:wp <site>.<env> -- <wp_cmd>` |
| Watch workflows | `terminus workflow:watch <site>` |
| Whoami / logout | `terminus auth:whoami` / `terminus auth:logout` |

Non-interactive scripts: add `-y` / `--yes` to skip confirms, or `-n` for non-interactive mode.

## Workflow Snippets

```bash
# Apply core upstream updates (Git mode required on Dev)
terminus env:commit <site>.dev --message="WIP"     # save SFTP work first
terminus connection:set <site>.dev git
terminus upstream:updates:apply <site>

# Deploy a change up the chain
terminus env:deploy <site>.test --sync-content --note="Update core + contrib"
terminus env:clear-cache <site>.test
terminus env:deploy <site>.live --note="Update core + contrib"
terminus env:clear-cache <site>.live
```

## Plugins

```bash
terminus self:plugin:install <vendor/project>   # also accepts a local path
terminus self:plugin:list
terminus self:plugin:update <vendor/project>
terminus self:plugin:uninstall <vendor/project>
terminus self:plugin:create <name> --project-name=<vendor>/<name>
```

## CI Authentication

Cache the session to avoid Auth0 rate limits — log in once, then reuse `$HOME/.terminus/cache/session` across jobs. Provider-specific pipelines (with caching) are in `references/ci-integrations.md`.

## Reference Files

All five files are verbatim extracts from the Pantheon Terminus Guide, reorganized by topic. Each begins with a source/provenance header.

| File | Covers | Source files |
|------|--------|--------------|
| [`references/install.md`](references/install.md) | Install, auth, updates, supported versions, v3/v4 migration notes, changelog | `02`, `10`, `11`, `12`, `13` |
| [`references/commands.md`](references/commands.md) | Full command directory (158 commands from `terminus list`), config file, plugin install, plugin directory | `04`, `09`, `06`, `08` |
| [`references/examples.md`](references/examples.md) | Apply updates, deploy, reset Dev to Live, switch upstreams, author/test plugins | `03`, `07` |
| [`references/scripting.md`](references/scripting.md) | Auth for CI, bash variables, example scripts (backup all sites, PHP-version CSV) | `05` |
| [`references/ci-integrations.md`](references/ci-integrations.md) | GitHub Actions, GitLab, CircleCI, Bitbucket pipelines with session caching | `05`, `ci/*` |

## Version & Compatibility

- **Current line:** Terminus 4.x (PHP 8.2–8.5). Installed locally at the time of scraping: **4.3.1**; latest release per GitHub API: **4.3.2**.
- **Terminus 3.x:** PHP 7.4–8.3 only, not compatible with PHP 8.4. Reaching/has reached EOL — see the support matrix in `references/install.md`.
- Each major/minor is supported for one year after the next release; then EOL. See <https://docs.pantheon.io/terminus/supported-terminus>.

## See Also

- Live docs: <https://docs.pantheon.io/terminus>
- Terminus source & issues: <https://github.com/pantheon-systems/terminus>
- Plugin project: <https://github.com/terminus-plugin-project>
- Drush on Pantheon: <https://docs.pantheon.io/guides/drush>
- WP-CLI on Pantheon: <https://docs.pantheon.io/guides/wp-cli>
- Quicksilver: <https://docs.pantheon.io/guides/quicksilver>

## Keywords

Pantheon, Terminus, terminus, CLI, Pantheon CLI, machine token, auth:login, site:list, env:deploy, upstream:updates, multidev, remote:drush, remote:wp, backup, deploy, Pantheon CI, Pantheon GitHub Actions, Pantheon GitLab, Pantheon CircleCI, Pantheon Bitbucket, WebOps, Drupal, WordPress
