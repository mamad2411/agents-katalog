---
name: sonarqube-scan
description: Run static code analysis on the Semantic Markdown repository with a local SonarQube server in Docker Compose, and gate releases on its results — bugs, vulnerabilities, security hotspots, code smells, duplication, maintainability and coverage. Use this skill before every release (on the release branch, before tagging and before marking the tracking PR ready), before opening a feature PR, and whenever the user asks for a code-quality, static-analysis, SonarQube/Sonar, lint, "code smells", security-scan or maintainability check, or asks whether the code is clean enough to ship. Use together with the smd-release skill, which calls for this gate in its release steps.
---

# SonarQube gate

GitHub CI runs typecheck, tests and the compatibility check, but **no static analysis**. This skill fills that gap locally: a SonarQube Community server runs in Docker Compose on the maintainer's machine, analyses the current checkout, and blocks the release if it finds new problems. Nothing leaves the machine, and no CI secrets are needed.

| File | Purpose |
|---|---|
| `docker-compose.yml` | SonarQube Community + Postgres (UI on `127.0.0.1:9000`), and a `scan` profile with `sonar-scanner-cli` |
| `scripts/sonar-scan.mjs` | Starts the server, bootstraps credentials, runs coverage + scanner, applies the gate, writes the report |
| `baseline.json` | Existing findings a maintainer accepted as known debt. Reported, but not blocking |
| `/sonar-project.properties` (repo root) | What is analysed: hand-written sources only, never `dist/`, bundled `smd.cjs` or `media/vendor/` |

## When to run it

| Moment | Command | Must pass? |
|---|---|---|
| Before opening a feature PR into `release/vX.Y.Z` | `sonar-scan.mjs --changed origin/release/vX.Y.Z` | Yes: nothing new on the lines the branch changed |
| On the release branch, before `release-check.mjs` and before tagging (smd-release §4–5) | `sonar-scan.mjs` | **Yes, mandatory** |
| Quick look while developing | `sonar-scan.mjs --no-coverage` | No |
| Hardening pass | `sonar-scan.mjs --strict` | Optional |

Run everything from the repository root (or a worktree root):

```bash
node .claude/skills/sonarqube-scan/scripts/sonar-scan.mjs
```

Prerequisites: Docker running, `npm ci` done in `extension/`. The first run pulls ~1 GB of images and takes a few minutes. Later runs reuse the running server and take about a minute.

## What the script does

1. `docker compose up -d` for the server and waits until `/api/system/status` is `UP`.
2. **First run only:** it replaces the default `admin/admin` password with a random one and creates an analysis token. Both are stored in `~/.smd-sonar/state.json`, outside the repository, so every worktree shares one server. To sign in to the UI, read the password from that file. Never commit it, paste it into chat, or put it in a PR.
3. It runs the unit tests with Node's built-in coverage, which writes `extension/coverage/lcov.info`. **If the tests fail, the scan stops.**
4. It runs `sonar-scanner` in a container against the checkout, with `sonar.projectVersion` set to the version in `extension/package.json`.
5. It waits for the server to process the analysis, then applies the gate and writes `.scannerwork/sonar-report.md`.

Exit codes: `0` pass, `1` blocked, `2` infrastructure or usage error (Docker down, failing tests, server didn't start).

## The gate

A finding **blocks** unless it is listed in `baseline.json`:

- an open issue of severity **Blocker** or **High** (Critical in standard mode), for bugs, vulnerabilities and code smells alike
- any open **security** issue, whatever its severity
- any **security hotspot** still "to review"
- with `--strict`, **Medium** (Major) issues too
- with `--changed <base>`, every open issue of **any** severity and every **duplicated block** on a line the checkout adds or edits since it left `<base>` (the branch or tag the work started from)

Lower-severity code smells, duplication and coverage elsewhere are reported as **non-blocking**. Still mention them in the release summary.

### Changed code (`--changed <base>`)

This is the gate for a feature branch: the change must not add a bug, a code smell or a copy of existing code, while the debt that was already in the repository stays out of the way.

- Changed lines come from `git diff` between the working tree and the merge base with `<base>`, so uncommitted work counts. Untracked files count as changed in full.
- An issue belongs to the change when its own location, or one of its secondary locations in the same file, is on a changed line. So a new branch that pushes a function over the cognitive complexity limit blocks, though the issue is reported on the function's first line.
- An issue that was already on a line the branch edits blocks too. Fix it when the fix is small and safe. Otherwise report it.
- It can't be combined with `--update-baseline`: findings on changed code are fixed, not accepted.

SonarQube's own quality gate (Sonar way) is shown as **informational**. Its "new code" is measured against whatever this local server analysed earlier, so it differs between machines. The committed baseline is what makes the gate repeatable. If the Sonar way gate fails, look at the conditions it lists (for example coverage on new code) and mention them in the summary.

## Handling findings

Work through the report's **Blocking** section. For each finding, in order of preference:

1. **Fix it.** This is the default. Re-run the scan to confirm it's gone.
2. **False positive or accepted risk in code we own:** suppress it at the line with a reason, so the decision is committed and reviewed:

   ```ts
   const re = new RegExp(pattern); // NOSONAR(typescript:S5852): pattern comes from the .smd spec, input length is bounded
   ```

   Don't use a bare `// NOSONAR` without a rule and reason.
3. **Security hotspot that is safe:** add a `NOSONAR` comment with a reason as above. Or mark it **Safe** in the UI (<http://localhost:9000/security_hotspots?id=styled-markdown>) if the reason doesn't belong in code. UI reviews only live in the local server's volume, so prefer the comment.
4. **Existing debt that can't be fixed in this release:** add it to the baseline, but only with the maintainer's explicit approval in chat. Then run:

   ```bash
   node .claude/skills/sonarqube-scan/scripts/sonar-scan.mjs --update-baseline
   ```

   This rewrites `baseline.json` from **every** current blocking finding. Review the diff so nothing new slips in, and commit it in its own `chore(quality): …` commit.

Never grow the baseline to make a release pass without asking. When a baselined finding is fixed, the report notes stale entries. Prune them with `--update-baseline` on a run that has **no blocking findings**, so the diff only removes lines.

## Reporting (release summary)

Add a **Static analysis** block to the smd-release §5 summary:

- **Result:** PASS/BLOCKED, quality gate status, and whether `--strict` was used
- lines of code, coverage, duplication, bugs / vulnerabilities / code smells / hotspots
- new findings fixed in this release, and any `NOSONAR` suppressions or baseline changes added, each with a one-line reason
- the non-blocking findings worth a follow-up (top rules)

## Maintenance

| Task | Command |
|---|---|
| Stop the server after the scan | add `--down` (data is kept) |
| Wipe the server, its data and the stored credentials | `sonar-scan.mjs --reset` |
| Different port | `--port 9100` or `SONAR_PORT=9100` |
| Pin or upgrade images | `SONARQUBE_IMAGE=sonarqube:<tag>` / `SONAR_SCANNER_IMAGE=…`; on upgrade the script runs the DB migration automatically |
| Admin password lost | `SONAR_ADMIN_PASSWORD=<pw> sonar-scan.mjs`, or `--reset` |
| Server won't start | `docker compose -f .claude/skills/sonarqube-scan/docker-compose.yml logs sonarqube`. It needs about 4 GB of RAM for Docker |

When new hand-written code folders are added (for example a new skill's `scripts/`), add them to `sonar.sources` in `sonar-project.properties`. Never add generated output.
