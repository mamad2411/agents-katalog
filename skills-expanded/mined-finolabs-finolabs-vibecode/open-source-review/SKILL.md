---
name: open-source-review
description: Check a repository's open source readiness, with evidence. Use before going public or a first public release, when publishing a plugin or skill package to a marketplace, when asked if it is safe to publish, or to check a public repository's settings (branch and tag protection, secret scanning, vulnerability reporting).
---

# Open source review

A read-only review: it finds and reports, it does not publish. Fixes, history rewrites, visibility changes and releases each need the owner's explicit authority. After a repository is public, run it again before each MINOR release and whenever `SECURITY.md`, CI or the repository settings change; a patch release does not need one.

## 1. Fix the scope

Name the repository, the exact commit, and what will become public: the working tree, the full git history, release archives, or a packaged plugin. History counts unless the owner will publish a fresh history; say which. Done when the scope line is written in the report.

## 2. Run every check

Mark each item **PASS**, **FAIL**, **N/A** (with why) or **BLOCKED** (with what is missing), and attach evidence: the command and its output, or the file and line. A tool that is not installed is BLOCKED, not PASS, unless the check names a fallback; a fallback result names the method it used.

### License

- A `LICENSE` file at the root, and the same SPDX id in every manifest (`package.json`, plugin manifests, `pyproject.toml`).
- Notices for vendored or copied third-party code, with their original licenses kept.
- Dependency licenses are compatible with the project license.

### Secrets and private data

- Recommend a `security-audit` run from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) before the first public release of code that runs (services, CLIs, plugins with scripts or hooks); report whether one ran and its verdicts.
- Scan the full history and the working tree for secrets: `gitleaks git .` and `gitleaks dir .` (`detect` is deprecated), `trufflehog git file://.`, or `git log -p` with targeted patterns when no scanner is installed. Report the file and commit, never the secret's value. Install nothing yourself, but strongly recommend that the user installs a scanner when none is present: name `gitleaks` or `trufflehog` with its install command, and say that the `git log -p` fallback covers less.
- No real `.env` files, credentials, keys, cookies, transcripts, customer data or personal data, in the tree or the history.
- A leaked secret is a stop: tell the owner so it can be rotated. Removing it from the tree does not remove it from history.

### Internal leaks

- No employer, customer or partner names, internal hostnames, private URLs, ticket links or internal tool names.
- No absolute paths from a personal machine (`/Users/<name>/`, `/home/<name>/`, `C:\Users\`), usernames or email addresses beyond the published maintainer contact.
- Agent context files (`AGENTS.md`, `CLAUDE.md`) hold only what contributors need; personal context lives in an untracked local file.
- Examples and fixtures use synthetic names and data.

### Clean payload

- `git ls-files -ci --exclude-standard` is empty: no ignored file is still tracked.
- No build or cache output, virtualenvs, `node_modules`, OS files (`.DS_Store`, `Thumbs.db`), editor folders, scratch output or logs.
- No symlinks out of the repository, no submodules or LFS pointers the package depends on, no file names that collide by case or are invalid on Windows or macOS.
- Large files are justified; binaries are justified and their source is published.

### Community files
Mark every item in [references/community-files.md](references/community-files.md): README, CONTRIBUTING, code of conduct, SECURITY, changelog and templates, and docs that match what ships.

### Repository settings
Read them from the forge, then mark every item in [references/repository-settings.md](references/repository-settings.md): branch and tag protection, secret scanning, dependency alerts, vulnerability reporting, merge, Actions and listing settings, and which of them block a ready verdict.

### Identity and versions

- One name across repository, package, manifests, display names and install commands. URLs resolve and point at the same owner.
- Versions agree across every manifest; the changelog's latest release matches them, or between releases its `Unreleased` section targets the `-dev` version; the single source of truth is named (`versioning`).

### Data flow and privacy

- State what data the software reads, where it sends it, what it stores and who can delete it, including optional services. A `PRIVACY.md` is needed when data leaves the user's machine.
- Behavior that runs, fetches or sends anything is documented, and dependencies are pinned.

### Plugin and skill packages
When the repository ships a plugin or skills, mark every item in [references/plugin-packages.md](references/plugin-packages.md): validators on a fresh clone, the target directory's own checks, skill triggers and listing assets.

## 3. Report

A table per group with status and evidence, then the FAIL and BLOCKED items ordered by severity: secrets and private data first, then internal leaks, license, payload, everything else. For each, the smallest fix and whether it needs the owner's authority (history rewrite, visibility change, repository settings, publishing). List every item marked N/A until publishing as a **recheck after the visibility change**, so a ready verdict does not hide it.
End with a one-line verdict: **ready**, **ready after fixes**, or **not ready**. A BLOCKED item in secrets and private data, internal leaks or license caps the verdict at **not ready**, naming the group that could not be checked, because what was not scanned cannot be called clean.

Done when every item above and in each reference it links has a status and every FAIL has a fix.
