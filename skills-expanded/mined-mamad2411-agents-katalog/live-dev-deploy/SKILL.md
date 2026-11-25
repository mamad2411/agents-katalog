---
name: live-dev-deploy
description: Guides through the verification, commit, testing, auto-healing, preview polling, and Git Flow deployment lifecycle. Runs Playwright local verification loops, checks Vercel Preview URLs, and handles staging-to-production releases.
---

# live-dev-deploy

This skill guides local verification, test-driven auto-healing, preview URL delivery, and Git Flow release deployment.

`bash` blocks are POSIX (Git Bash on Windows). Any logic beyond one command/pipe lives in `resources/*.js`, never in shell control flow. If your Bash tool is cmd.exe or PowerShell, translate each snippet before running it.

## 1. Git Flow & Release Lifecycle

| Transition | Trigger | Gate |
| --- | --- | --- |
| `develop` → `feature/*` | new request | — |
| `feature/*` → `develop` | QA loop + secret scan PASS locally | `gh pr checks <PR#> --watch` green. Local ≠ CI: CI also runs `lint` + `build`. |
| `develop` → `main` | user approves the release prompt below | same CI wait → merge → tag → bump |
| `main` → `develop` | immediately after the release PR merges | back-merge, no PR needed. The bump commit exists only on `main`; skip this to prevent branch version collision. |

Release prompt, verbatim: `"Would you like to release this to the production environment?"`

- **Version Bump:** The release PR carries both the tag `v<major>.<minor>.<patch>` and the matching `package.json:version` (read it, default `0.0.0`, bump patch unless told otherwise).
- **Merge Restrictions:** Never merge on red or pending CI. Red after green local → back into the QA healing loop → push → wait.
- **Merge Conflicts:** Show conflicts to the user. Do not self-resolve handwritten source conflicts.
- **Staging vs. Production Deploy:** Deploy via Vercel GitHub integration. Production deployments must not have Vercel Deployment Protection (password protection or Vercel Authentication) by default, ensuring public access.
- **Public Access Validation:** If a production deployment is not publicly accessible (redirects to login/fails ping), ask: "The production deployment is not publicly accessible. Would you like to enable public access?" and guide them to Vercel Project Dashboard (Settings -> Deployment Protection) to disable it.
- **Rollback:** In case of broken production, `git revert` the merge commit on `main` → push.

## 2. Local Verification & Auto-Healing

Setup, port discovery, and test templates: `references/playwright-qa-rules.md`. One port for dev server + `baseURL` + any test URL.

Gates, all green before any commit or push — never commit or push past a red one: the Playwright suite, `lint`, `build`, and `gitleaks protect --staged` (staged diff, not `detect`) before every commit.

- **On failure:** Parse errors/traces → fix implementation code only → rerun under the healing loop of `references/playwright-qa-rules.md` (limit 3 attempts, then halt and report).
- **Secret Scan Gate:** Any secret match blocks the commit → move to vault, reference via `process.env`.
- **Firestore Local Verification:** If features touch Firestore, run the QA loop against the Local Emulator Suite (`references/react-firestore-rules.md`), never the real project.
- **Hooks:** Install a committed, auto-installing hook manager (Husky/Lefthook) running lint + secret scan pre-commit.

## 3. Preview-First Delivery

Never hand the user a `localhost` link for verification. Run:

```bash
node resources/resolve-preview-url.js   # exit 0 -> prints PREVIEW_URL=<url>
```

- Polling uses `resolve-preview-url.js` to query GitHub Deployments API.
- If it takes too long, escalate:
  - 60s: extend attempts, tell user a build is in progress.
  - ~5 min: use non-interactive JSON `vercel list` filtered to the pushed commit.
  - After that: report dashboard URL or `vercel inspect`.

```text
⚡️ Features deployed successfully! Preview URL: https://project-git-develop-user.vercel.app
```

## 4. Guardrails

Bad pattern requested (prop drilling over Context, bypassing GitHub automation, reusing preview database for production, …) → halt and emit:

| | Requested | Proposed alternative |
| --- | --- | --- |
| Security risk | | |
| Maintenance cost | | |

Resume only on the verbatim string `"I understand the risk and insist on this."`

## 5. Output Format

### Verification Log
- Vercel Deployment Link: [preview or production URL]
- Git Branch: [feature branch / develop / main]
- PLAYWRIGHT Test Status: [PASS / FAIL]

### Checklist
| ID | Item | Result | Evidence |
| -- | --- | --- | --- |
| F1 | Local QA Test | PASS / FAIL / N/A | [test log snippet] |
| F2 | Preview URL | PASS / FAIL / N/A | [live vercel preview URL] |
| F3 | Secret Scan | PASS / FAIL / N/A | [scan result summary] |

### Code Changes
- `[file path]`: [description of change]

### Smoke Test Output
```text
[Playwright execution output]
```

### Remaining Risks
- [untested features, credentials isolation, or "None"]

### Recurrence Protection
- [Rule / Hook / Test / Skill / "Not Needed" + reason; plus the repo URL, Vercel project, and Firebase project id]
