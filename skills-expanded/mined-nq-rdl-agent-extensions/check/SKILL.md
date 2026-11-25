---
license: CC-BY-4.0
description: >-
  Fast link checker for documentation, READMEs, skills, and any text/markdown files.
  Use when the user asks to "check links", "find broken links", "lint URLs",
  "validate links", "check for dead links", or mentions link rot, broken URLs,
  or URL validation. Also trigger when reviewing documentation quality, auditing
  skills or READMEs for broken references, or before publishing/releasing docs.
  Use this skill even if the user just says "are there any broken links?" or
  "check the docs" in the context of link health.
compatibility: >-
  Requires lychee >=0.24.0 on PATH (string fragment modes and --cache=false)
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Lychee — Fast Link Checker

## Overview

[Lychee](https://github.com/lycheeverse/lychee) is a fast, async link checker
written in Rust. This skill wraps it with documentation-friendly defaults so
agents can quickly find broken URLs in markdown, HTML, YAML, and other text files.

## Dependencies

Lychee is a standalone binary. Install via any of these methods:

```bash
# pixi (recommended)
pixi global install lychee

# cargo (if Rust toolchain installed)
cargo install lychee

# brew (macOS)
brew install lychee

# conda-forge
conda install -c conda-forge lychee
```

The wrapper script checks for `lychee` on PATH and exits with install instructions if missing.

Tested with **lychee 0.24.2 on 2026-09-16**; this is separate from the minimum
version above. Verify changed options against `lychee --help` and the
[canonical configuration](https://lychee.cli.rs/guides/config/); if the installed
version rejects an option, report the mismatch before claiming a completed scan.
When offline, use local help and report external links as unverified.

## Commands

### Check links in specific files or directories

```bash
# Resolve scripts/ relative to this installed skill directory, not the project cwd.
bash scripts/check-links.sh /path/to/README.md
bash scripts/check-links.sh '/path/to/docs/**/*.md'
bash scripts/check-links.sh /path/to/project/
```

### JSON output (for programmatic analysis)

```bash
bash scripts/check-links.sh --format json '/path/to/docs/**/*.md'
```

### Pass additional lychee flags

The wrapper forwards all arguments to lychee, so any lychee flag works:

```bash
# Offline mode — only check local file references, no network requests
bash scripts/check-links.sh --offline /path/to/docs/

# Check a remote page (reserved example.com URLs are excluded by default)
bash scripts/check-links.sh 'https://lychee.cli.rs/'

# Exclude a pattern
bash scripts/check-links.sh --exclude 'github\.com/.*?/issues' /path/to/docs/

# Verbose output for debugging
bash scripts/check-links.sh -v /path/to/docs/

# Use project-specific config instead of bundled defaults
bash scripts/check-links.sh --config /path/to/project/lychee.toml /path/to/docs/

# Detailed output format (shows each link's status)
bash scripts/check-links.sh --format detailed /path/to/docs/

# Markdown report saved to file
bash scripts/check-links.sh --format markdown -o report.md /path/to/docs/
```

## Bundled Defaults

The skill ships a `lychee.toml` with opinionated defaults for documentation repos:

- **Caching** enabled (`.lycheecache` in the working directory), bounded to one hour
- **Fragment checking** on — verifies `#section-name` anchors resolve
- **Concurrency** capped at 32 — avoids triggering rate limits
- **Common exclusions** — RFC 2606 reserved names and subdomains, localhost, mailto
- **Private IPs excluded** — skips 10.x, 192.168.x, link-local ranges

Pass `--config "/path with spaces/lychee.toml"` to replace the bundled defaults.
The wrapper also recognizes `--config=path`, `-c path`, and `-cpath`; it forwards
arguments unchanged and adds `--no-progress`. A project-root config is selected
only when explicitly passed. Repository-specific exceptions and per-host headers
belong in that config, not the shipped defaults.

Use `--cache=false` for audits and verification, even if a cache already exists.
A cached success does not establish current health. This catalog's CI and local
hooks explicitly select root `lychee.toml` and disable caching; consumers need
neither that file nor its exclusions.

## Typical Agent Workflows

### Pre-release doc audit

```bash
bash scripts/check-links.sh --cache=false --format json '/path/to/project/**/*.md' > /tmp/link-report.json
```

Read the JSON output and exit status to summarize failed URLs and their source
files. Keep authentication/rate-limit/timeout failures distinct from confirmed
missing pages; report incomplete scans honestly. Use `--format markdown -o
report.md` for a shareable report. Lychee's plain-text RST extraction does not
validate every relative RST reference; an offline pass is not proof they resolve.

### Skill quality check

```bash
bash scripts/check-links.sh '/path/to/skills/*/SKILL.md' '/path/to/skills/*/references/*.md'
```

### CI-style check (exit code reflects broken links)

Lychee exits non-zero when broken links are found, so the Bash tool will report
failure automatically. Use this to gate PRs or releases.

## Output Formats

| Format       | Flag               | Best for                        |
|-------------|--------------------|---------------------------------|
| `compact`   | (default)          | Quick terminal summary          |
| `detailed`  | `--format detailed`| Per-link status breakdown       |
| `json`      | `--format json`    | Programmatic analysis by agents |
| `markdown`  | `--format markdown`| Reports saved to files          |

## Exit Codes

- `0` — all links OK
- `1` — general error
- `2` — broken links found

A non-zero exit code is the expected signal for "there are problems to fix."

## Troubleshooting

**Rate limiting (429 errors):** Lower concurrency with `--max-concurrency 8`
or add the affected domain to the exclude list.

**Timeouts on slow sites:** Increase with `--timeout 60`.

**False positives behind auth:** Exclude the domain pattern with `--exclude 'private\.example\.com'`.

**GitHub API rate limits:** Lychee reads an available `GITHUB_TOKEN` from the
environment for GitHub API requests. Use only a token authorized for the task;
do not print it or write it into config/reports. Without one, report rate-limit or
access failures rather than assuming a private URL is broken.
