---
name: ci-pipelines
last_reviewed: 2026-09-06
group: Ship and run
description: >-
  Build CI/CD with build, test, security scan and deploy stages across common providers. Use when
  setting up GitHub Actions, GitLab CI, or build pipelines.
---

# CI Pipelines

You're writing configuration that runs unattended on every push or PR — a broken pipeline either blocks every contributor or, worse, silently stops catching real problems. Correctness and clarity both matter more here than in most code, since the person debugging a failing run at 11pm needs to understand what happened from the config alone.

## Workflow

1. **Identify the platform.** Look for existing signals first — a `.github/workflows/` folder, `.gitlab-ci.yml`, or `.circleci/config.yml` already in the repo tells you the platform without asking. If nothing exists yet, ask which CI platform they're using (or default to GitHub Actions if the repo is already on GitHub, since that's the path of least setup friction).
2. **Identify the stack.** Check for `package.json`, `requirements.txt`/`pyproject.toml`, `go.mod`, `Cargo.toml`, etc. to infer the language/package manager rather than asking the user to specify what's discoverable from the repo.
3. **Build stages in this order, only including what's relevant:**
   - **Checkout** — always first.
   - **Setup** — install the right language runtime version, matching what's pinned in the repo (e.g. `.nvmrc`, `engines` field, `python_requires`) rather than defaulting to "latest."
   - **Cache** — cache dependency installs (node_modules, pip cache, cargo registry) keyed on the lockfile hash, since this is the single biggest speed win for most pipelines and is easy to skip by accident.
   - **Install** — use the lockfile-respecting install command (`npm ci` not `npm install`, `pip install -r requirements.txt` with a pinned file) so CI matches what's actually committed, not whatever the latest compatible versions happen to be that day.
   - **Lint** — if a linter config exists in the repo (`.eslintrc`, `ruff.toml`, etc.).
   - **Test** — run the test suite; fail the pipeline on non-zero exit.
   - **Build** — compile/bundle step if the project has one.
   - **Deploy** — only on the appropriate trigger (e.g. push to `main`, or a tagged release) — never deploy on every PR from a fork, since that's both wasteful and a security risk if secrets are involved.
4. **Gate secrets properly.** Any deploy or notification step needing credentials should read them from the platform's secret store (`${{ secrets.X }}` for GitHub Actions), never hardcoded, and should not run on pull_request events from forks, which don't have access to repo secrets by design — explain this if the user is confused about why a fork's PR pipeline can't deploy.
5. **Add a status badge snippet** for the README if the user is setting this up for the first time — a small thing, but it's usually wanted and easy to forget.

## Debugging an existing pipeline

If the user pastes a failing run's log or error, read it for the actual failure point first — CI failures are often a symptom one or two steps upstream of where the error message appears (e.g. a cache-key collision masking a stale dependency, not the test itself being wrong). Don't just patch the visible error; check whether an earlier step's assumption broke.

## Anti-Patterns & Constraints

- Don't invent secret names or environment variables the user hasn't mentioned — ask what they're actually called in their existing secret store rather than guessing plausible-sounding ones.
- Don't add deploy steps unless explicitly asked — a CI setup for testing shouldn't quietly ship a deploy stage the user didn't request.
- Don't over-engineer a pipeline for a repo that clearly doesn't need matrix builds or multi-environment deploys yet — match the pipeline's complexity to the project's actual size.

## Output format

Provide the complete config file, ready to drop in at its correct path (e.g. `.github/workflows/ci.yml`), with a comment above any non-obvious step explaining why it's there. Follow it with a short explanation of what triggers the pipeline and what each stage does — not a line-by-line narration, just enough for someone unfamiliar with the file to orient themselves.

See `references/github-actions.md`, `references/gitlab-ci.md` for platform-specific syntax quirks and caching patterns.

## Verification & Quality Checklist

- [ ] Code compiles and all automated tests and typechecks pass without new warnings.
- [ ] Edge cases, boundary conditions, and error states handled explicitly rather than assumed.
- [ ] No hardcoded secrets, credentials, or insecure defaults introduced.
- [ ] Changes are covered by a test that fails without them.
