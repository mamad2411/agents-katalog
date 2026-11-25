---
name: project-showcase
description: "Automate the creation of high-quality project showcases: UI captures, security scans, repo health audits, README injection, GitHub releases, and social media launches."
---

# Project Showcase Skill

Automates the "last mile" of development — capturing visuals, auditing health, injecting professional READMEs, and shipping.

## Commands

| Command | Script | Description |
|---|---|---|
| `/showcase` | (all) | Full pipeline: scan → capture → audit → readme → release → metadata |
| `/capture` | `scripts/capture.py` | UI screenshots via Playwright (web apps) |
| `/record` | VHS + `.tape` | Terminal demo GIF (CLI tools, skills) |
| `/scan` | `scripts/scan.py` | Security scan for secrets |
| `/audit` | `scripts/audit.py` | Repo health score (0-100) + healing plan |
| `/readme` | `scripts/inject_readme.py` | Surgical README gallery injection |
| `/release` | `scripts/release.py` | GitHub release with auto-changelog |
| `/metadata` | `scripts/manage_metadata.py` | GitHub topics + description |
| `/setup` | `scripts/setup.sh` | Install dependencies |
| `/socials` | `linkedin-magic/` | LinkedIn post generation + asset bundling |

## Workflows

### 1. Security First (`/scan`)
```bash
python3 scripts/scan.py --dir /path/to/project
```
If secrets found → warn user, propose `.gitignore` fixes, halt capture.

### 2. Capture (`/capture`)

**For web apps** — Playwright screenshots:
```bash
python3 scripts/capture.py --url http://localhost:3000 --responsive --record-video
```
- Waits for `networkidle` + framework hydration
- Supports masking (`--mask ".api-key"`), dark mode, A/B mode
- Outputs to `showcase/` directory

**For CLI tools / skills** — VHS terminal recording:
```bash
vhs scripts/showcase_demo.tape
```
- Records real terminal output as GIF
- Edit `.tape` file to customize the demo
- Outputs to `showcase/demo.gif`

**For non-web, non-CLI projects** — terminal screenshots:
- Run key commands (audit, scan, etc.)
- Capture output as PNG via Playwright HTML rendering
- Never generate fake architecture diagrams

### 3. Audit (`/audit`)
```bash
python3 scripts/audit.py --dir /path/to/project --heal
```
Scores 5 categories (Documentation, Security, Automation, Showcase, Distribution) on 0-100 scale. `--heal` shows prioritized fix plan.

### 4. README Injection (`/readme`)
```bash
python3 scripts/inject_readme.py --readme README.md --gallery "## 🎬 Showcase Gallery\n![Demo](showcase/demo.gif)"
```
- Replaces existing gallery or inserts before first `##` section
- Never duplicates, always backs up first
- Moves health tables to `REPO_HEALTH.md` (not main README)

### 5. Release (`/release`)
```bash
python3 scripts/release.py --version v1.0.0
```
Auto-generates changelog from conventional commits. Supports `--prerelease` and `--dry-run`.

### 6. Metadata (`/metadata`)
```bash
python3 scripts/manage_metadata.py --apply
```
Auto-detects topics from file patterns, extracts description from README, applies via `gh repo edit`.

## Best Practices

- **Real captures only**: Never generate fake SVGs or architecture diagrams. If there's no web UI, use VHS terminal recordings or terminal screenshots of actual tool output.
- **Vibe-first README**: No diagnostic tables in main README. Health data goes in `REPO_HEALTH.md`.
- **Badge discipline**: "Tested on Gemini CLI" only for agentic projects. "Live App" only if deployed.
- **Wait for hydration**: Always use `networkidle` + selector waits before capturing.
- **Mask by default**: Use `--mask` for any UI showing emails, keys, or personal data.
- **Idempotent**: All scripts are safe to re-run. Injection won't duplicate. Audit won't break.

## Sub-Skills

- **LinkedIn Magic** (`linkedin-magic/SKILL.md`): Post templates, asset bundling, hashtag strategy.

## Docs

Full documentation: https://project-showcase-skill.readthedocs.io/

---
*Built for Vibe Coders everywhere.*
