---
name: astro-site-governance
description: Bootstrap or replicate battle-tested GitHub governance (Security/Quality/Workflow core Rulesets always applied, plus an opt-in Review ruleset for Copilot code review + required conversation resolution — ADR-0021 in tarotene/dotfiles, Biome/Vitest CI, cog.toml, Renovate, release-please, git hooks, Justfile) into any Astro site repository. Use when asked to "撒く", "bootstrap governance", "apply rulesets", "apply GitHub settings", "set up release-please", "seed CI to a new Astro repo", "rulesets / release / renovate をまとめて適用", or "Astro サイトに governance を播く". This is the Astro/site counterpart of `rust-repo-governance`; use `typst-repo-governance` instead for Typst/document repositories.
---

## What this Skill does

1. Copies parameterised templates (CI workflows including a per-file
   language-mixing check — `lang-mix.yml` —, an ADR-number check —
   `adr-number.yml`, ADR-380 in tarotene/dotfiles —, git hooks, Biome/Vitest/cog/Renovate/
   release-please configs, CODEOWNERS, AGENTS.md/CLAUDE.md routing skeleton
   — ADR-0016 in tarotene/dotfiles) into the target repository, substituting
   `__PLACEHOLDER__` values for your repo's specifics.
   No API-docs job is seeded: `github-audit`'s `docs` domain (ADR-640 in
   tarotene/dotfiles) is `not-applicable` for an Astro site — the site/document is
   itself the build artifact. If the repo is also a TypeScript library (its
   `package.json` declares `exports`/`main`/`types`), the audit will ask for
   `tarotene/dotfiles/.github/actions/docs-typescript@main` in `ci.yml`.
2. Applies repository merge settings (squash-only, delete-on-merge, wiki/projects disabled — same
   baseline `github-audit`'s `settings` domain judges, ADR-0015 in tarotene/dotfiles) via `gh api`.
3. Creates the core GitHub Rulesets (Security / Quality / Workflow) that enforce
   branch protection and required status checks. A fourth, Review, is
   **opt-in** (`--with-review`) — Copilot code review auto-request + required
   conversation resolution before merge. It is left out by default because
   forcing that review round trip on every commit of an early-stage or
   pre-release repository was judged excessive and noisy (ADR-0021 in
   tarotene/dotfiles). Opt in once the repository is past that phase, or
   strip it back out of an already-governed repository — remove
   `.github/rulesets/review.json` from the declaration, then
   `apply-rulesets.sh OWNER/REPO --delete-ruleset Review` (see "Removing the
   review layer" below).
4. Guides you through the manual steps that require browser flows (GitHub Pages
   setup, optional GitHub App for release-please).

For an explanation of why each layer was chosen and how to migrate from an
existing setup, see `reference/migration-guide.md` in this Skill directory.

---

## Step 0: Gather parameters

Before running anything, confirm the following values with the user:

| Parameter | Flag | Example |
|-----------|------|---------|
| GitHub owner | `--owner` | `tarotene` |
| Repository name | `--repo` | `my-astro-site` |
| npm package name | `--package-name` | `my-astro-site` |
| Current version | `--package-version` | `0.1.0` (from package.json) |
| Default branch | `--default-branch` | `main` (default) |
| Node.js version | `--node-version` | `22` (default) |
| Astro base path | `--site-base` | `/my-astro-site` (docs only, optional) |
| Pages URL | `--pages-url` | `https://owner.github.io/my-astro-site/` (docs only, optional) |
| Target repo path | `--dest` | `/home/user/src/my-astro-site` |
| Review layer? | `--with-review` | pass flag to also apply the Review ruleset (Copilot code review + required conversation resolution — ADR-0021). Ask whether the repository is past its early-development phase before defaulting this on. |

Also check prerequisites:

```
gh auth status
command -v jq git npm
mise install  # (or ensure cog is on PATH)
```

---

## Step 1: Dry-run preview

Run seed.sh with `--dry-run` so the user can review what will change before
any files are written or API calls are made:

```bash
~/.claude/skills/astro-site-governance/scripts/seed.sh \
  --owner OWNER --repo REPO \
  --package-name NAME --dest /path/to/repo \
  --dry-run
```

Show the output to the user. Confirm they are happy to proceed.

---

## Step 2: Apply

Run without `--dry-run`:

```bash
~/.claude/skills/astro-site-governance/scripts/seed.sh \
  --owner OWNER --repo REPO \
  --package-name NAME --dest /path/to/repo
```

Individual sub-scripts can be run independently (useful for re-runs):

```bash
# Copy files only (no GitHub API calls):
~/.claude/skills/astro-site-governance/scripts/copy-files.sh \
  --owner OWNER --repo REPO --package-name NAME \
  --dest /path/to/repo

# Create Rulesets only (files already copied — the generic apply script,
# not part of this skill, reads OWNER/REPO's own .github/rulesets/*.json;
# ADR-503):
apply-rulesets.sh OWNER/REPO --unverified-contexts

# Apply repo settings only:
~/.claude/skills/astro-site-governance/scripts/apply-repo-settings.sh \
  --owner OWNER --repo REPO

# Wire git hooks only:
~/.claude/skills/astro-site-governance/scripts/setup-hooks.sh \
  --dest /path/to/repo
```

---

## Step 3: Manual ADJUST checklist

After `seed.sh` completes, open each copied file and address every `# ADJUST:`
comment. The most important locations:

| File | What to update |
|------|----------------|
| `package.json` | Merge scripts/devDependencies snippet (shown by copy-files.sh); run `npm install` |
| `mise.toml` | Add `cocogitto = "latest"` to `[tools]`; run `mise install` |
| `.github/workflows/ci.yml` | If project has NO MDX content-lint scripts, remove the `content-lint` job AND its entry in `ci-passed`'s `needs:` (they are a pair) |
| `release-please-config.json` | Verify `package-name` is correct |
| `.release-please-manifest.json` | Verify version matches current `package.json` |
| `renovate.json` | Adjust `packageRules` grouping for your actual dependencies |
| `biome.json` | Check `files.includes` globs match your TS/CSS paths; **never add `.mdx` or `.astro`** |
| `.github/workflows/pr-title.yml` | Nothing to adjust — calls tarotene/dotfiles' composite action (ADR-0031/ADR-591); the reported check context is simply this job's own `name: PR title`, no manual confirmation needed |
| `.github/workflows/close-linked-issues.yml` | Nothing to adjust — closes the issues a merged PR names with `Closes #N` even when the PR was stacked on a non-default base (GitHub only acts on the keyword for PRs targeting the default branch, tarotene/dotfiles#609); needs no secrets, only `issues: write` |
| `.github/zizmor.yml` | Nothing to adjust — `"tarotene/*": ref-pin` covers the composite action's symbolic-ref `uses:` (#491); zizmor's own blanket default (hash-pin) still applies to every other `uses:` |

**Key invariant:** The `name:` field of each workflow job in `ci.yml`
**must exactly match** the entries in `ci-passed`'s `needs:` (job *id*, not
`name:`) — the Ruleset only ever requires `CI passed`/`PR title`
(ADR-591), so the four individual job `name:` values (`Format & Lint
(Biome)`, `Content lint`, `Unit tests`, `Build`) are display labels and no
longer need to match anything in `.github/rulesets/quality.json`.
`workflow-naming-check` (tarotene/dotfiles, a required check on every PR)
verifies this `needs:` coverage automatically.

**`pr-title.yml`** has no `workflow_call` concatenation to worry about
(ADR-591 replaced the old reusable-workflow form with a composite action,
docs/adr/591-ci-workflow-naming.md D3 in tarotene/dotfiles) — the reported
check context is simply this job's own `name: PR title`, pinned by the
`repo-governance-common/templates/.github/workflows/pr-title.yml` template
(this skill's copy is a symlink to it).
If you remove `"content-lint"` (no MDX scripts), remove it from `ci.yml`
(the job) and from `ci-passed`'s `needs:` in the same file.

---

## Step 4: Manual steps (browser flows)

Follow `./reference/manual-steps.md` for:

1. **Enable GitHub Pages** — Settings → Pages → Source: GitHub Actions.
2. **Verify Rulesets** — `gh api` commands to confirm contexts match.
3. **First PR walkthrough** — all 4 CI jobs should turn green.
4. **(Optional) GitHub App** — for release PRs that trigger full CI.

---

## Step 5: Verification

### Local sanity
```bash
# Validate Ruleset JSONs
jq -e . ~/.claude/skills/astro-site-governance/templates/.github/rulesets/*.json

# Check hooks are wired
git -C /path/to/repo config --local core.hooksPath
# → should print: .githooks

# Try a Conventional Commit (should pass)
echo "feat: test" | cog verify -

# Run full local quality gate
npm run ci:biome
npm run check
npm test
npm run build
```

### After pushing the first PR

```bash
# Rulesets should appear:
gh api repos/OWNER/REPO/rulesets --jq '.[].name'
# → Security, Quality, Workflow (+ Review if seeded with --with-review)

# Required checks contexts in Quality Ruleset:
gh api repos/OWNER/REPO/rulesets \
  --jq '.[] | select(.name=="Quality") | .rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
# → CI passed / PR title

# Repo merge settings:
gh api repos/OWNER/REPO \
  --jq '{allow_squash_merge, allow_merge_commit, allow_rebase_merge, delete_branch_on_merge}'
# → true / false / false / true
```

### Removing the review layer (ADR-0021)

Remove `.github/rulesets/review.json` from the repository first (the
declaration is the source of truth — ADR-503),
commit that, then run `apply-rulesets.sh OWNER/REPO --delete-ruleset Review
[--dry-run]` — it refuses to run while `review.json` is still declared, so
the order above is enforced, not just recommended. It only handles the
standalone `Review` ruleset shape (this skill's own `review.json` layout);
`copilot_code_review` or `required_review_thread_resolution: true` bundled
into some *other* active branch ruleset needs manual removal via
`gh api repos/OWNER/REPO/rulesets/<id>` + a hand-built `PUT`
(`crates/rulesets-write-guard` denies this from a Claude session — pass
`RULESETS_WRITE_GUARD_BYPASS=1` if you're deliberately doing this by hand).

---

## Template structure reference

```
~/.claude/skills/astro-site-governance/
├── SKILL.md                              ← this file (orchestration instructions)
├── templates/
│   ├── biome.json                        Biome formatter + linter config
│   ├── cog.toml                          cocogitto Conventional Commits config
│   ├── renovate.json                     Renovate dependency update config
│   ├── release-please-config.json        release-please config (node type)
│   ├── .release-please-manifest.json     initial version manifest
│   ├── vitest.config.ts                  Vitest test runner config
│   ├── mise.toml-snippet                 node + cocogitto merge snippet
│   ├── package.scripts.jsonc-snippet     scripts/devDeps/private/engines merge snippet
│   ├── .github/
│   │   ├── CODEOWNERS                    * @__OWNER__
│   │   └── workflows/
│   │       ├── ci.yml                    required: CI passed (aggregate of biome/
│   │       │                             content-lint/unit-tests/build via
│   │       │                             needs:, ADR-591 in tarotene/dotfiles)
│   │       ├── release-please.yml        automated CHANGELOG + Release
│   │       └── pr-title.yml              required: PR title (calls tarotene/dotfiles'
│   │                                     composite action, ADR-0031/ADR-591)
│   └── .githooks/
│       ├── commit-msg                    cog verify (Conventional Commits)
│       ├── pre-commit                    biome check --staged (fast)
│       └── pre-push                      npm run check + npm test
│   ├── .github/rulesets/                   (declaration copied into the target repo —
│   │   │                                    ADR-503)
│   │   ├── security.json    shared with repo-governance-common: deletion + non_fast_forward
│   │   ├── quality.json     astro-specific (bypass_actors only): signatures +
│   │   │                    linear history + the fixed pair CI passed/PR title (ADR-591)
│   │   ├── workflow.json    shared with repo-governance-common: squash-only (core)
│   │   └── review.json      shared with repo-governance-common: Copilot code review +
│   │                        required thread resolution (opt-in, --with-review only)
├── scripts/
│   ├── seed.sh                           main orchestrator — copy-files.sh, setup-hooks.sh,
│   │                                      apply-repo-settings.sh, then the generic
│   │                                      apply-rulesets.sh (not part of this skill;
│   │                                      home-manager deploys it to ~/.local/bin)
│   ├── copy-files.sh                     template + .github/rulesets/*.json copy, placeholder
│   │                                      substitution, verify_declaration safety check
│   ├── apply-repo-settings.sh            gh api PATCH repo merge settings
│   └── setup-hooks.sh                    git config core.hooksPath
└── reference/
    ├── releasing.md                      release-please runbook
    ├── manual-steps.md                   browser-flow checklist
    └── migration-guide.md                ★ how to migrate from minimal/ESLint/Prettier
```

## Placeholder reference

| Placeholder | Meaning | Example |
|---|---|---|
| `__OWNER__` | GitHub owner login | `tarotene` |
| `__REPO__` | Repository name | `my-astro-site` |
| `__DEFAULT_BRANCH__` | Default branch | `main` |
| `__NODE_VERSION__` | Node.js version | `22` |
| `__PACKAGE_NAME__` | npm package name | `my-astro-site` |
| `__PACKAGE_VERSION__` | Current version | `0.1.0` |
| `__SITE_BASE__` | Astro base path (docs only) | `/my-astro-site` |
| `__PAGES_URL__` | Deployed Pages URL (docs only) | `https://tarotene.github.io/my-astro-site/` |
