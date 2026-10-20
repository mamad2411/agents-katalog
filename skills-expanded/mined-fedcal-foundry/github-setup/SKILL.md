---
name: github-setup
description: Bootstrap repository governance with the gh CLI — label taxonomy, milestones, a Projects v2 board, branch protection or rulesets, issue and PR templates, and required checks. Idempotent, safe to re-run. Use when starting a repository or bringing an existing one under governance. Not for CI pipeline design, deployment, or secret management.
argument-hint: "[--labels] [--milestones] [--project] [--protection] [--templates] [--all] [--dry-run]"
user-invocable: true
agent: foundry-pmo:github-operator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "plan.v1 -> GitHub repository configuration + handoff.v1"
license: Apache-2.0
---

# GitHub setup

Bring a repository under governance with exact, idempotent `gh` commands. Re-running a completed
setup must produce **zero changes**. If it does not, that is a defect in this skill, not a quirk.

Default posture is `--dry-run`: print the commands, apply after approval. Section flags run
subsets; `--all` runs everything in order.

## Step 0 — Preflight, always

```bash
gh --version                || echo "gh NOT INSTALLED"
gh auth status              || echo "gh NOT AUTHENTICATED"
gh repo view --json nameWithOwner,defaultBranchRef,visibility,isArchived,isFork
gh api repos/{owner}/{repo} --jq '.permissions'
gh auth status 2>&1 | grep -i 'token scopes'
git remote -v
```

Record and report: repo, default branch, visibility, archived/fork status, permissions
(`admin`/`maintain`/`push`), and token scopes.

| Section | Needs |
|---|---|
| Labels, milestones, issues | `repo` scope (`public_repo` on public repos) |
| Projects v2 | `project` scope → `gh auth refresh -s project` |
| Rulesets / branch protection | repository `admin` permission |
| Workflow files | `workflow` scope |

Degradation ladder — announce the rung, then continue:

1. **`gh` absent** — write the file-based assets (`.github/**`, `.github/labels.json`,
   `.github/rulesets/*.json`), emit every API command as a copy-pasteable block, set
   `handoff.v1.status: blocked`. Never claim repository state you could not read.
2. **Unauthenticated** — print `gh auth login --scopes repo,project,workflow`; stop mutating.
3. **Missing scope** — do what the scope allows; list skipped actions with the exact
   `gh auth refresh -s <scope>`.
4. **Insufficient permission** — emit the settings as files plus the `gh api` command an admin
   can run; mark `partial`.

Archived repository, fork without upstream write, or no remote: report and stop. These change
what is possible and must not be worked around.

## Step 1 — Labels

Desired state lives in `.github/labels.json` so it is reviewable and diffable. Start from
`templates/labels.json` and adjust the `area:` namespace to the project.

```bash
gh label list --limit 200 --json name,color,description > .foundry/scratch/labels-current.json

# create-or-update (idempotent: --force updates an existing label)
gh label create "type:feat" --color "1D76DB" --description "New capability" --force

# report the diff before touching anything
jq -r '.[].name' .foundry/scratch/labels-current.json | sort > /tmp/have.txt
jq -r '.[].name' .github/labels.json | sort > /tmp/want.txt
comm -13 /tmp/have.txt /tmp/want.txt   # to create
comm -23 /tmp/have.txt /tmp/want.txt   # extra — propose removal, never automatic
```

Namespaces: `type:`, `sev:`, `prio:`, `size:`, `status:`, `needs:`, `area:`, `stale:`, plus flat
flags (`risk`, `security`, `breaking`, `blocked`, `good-first-issue`). Keep the total under ~40 —
a taxonomy nobody can hold in their head is applied inconsistently, and inconsistent labels make
every query silently under-report.

**Deletion is never automatic.** Labels carry history; removing one strips it from every closed
issue. Propose, show `gh label delete "<name>" --yes`, wait.

## Step 2 — Milestones

No `gh milestone` subcommand exists; use the API. Milestones come from `plan.v1` waves.

```bash
gh api repos/{owner}/{repo}/milestones --paginate \
  --jq '.[] | {number,title,state,due_on}' > .foundry/scratch/milestones.json

# create; 422 means the title exists → switch to PATCH by number
gh api repos/{owner}/{repo}/milestones -X POST \
  -f title='M2 — Merchants can take card payments' \
  -f description='Exit: checkout success rate >= 97% over 7d; e2e @payments green; zero open sev:1' \
  -f due_on='2026-11-30T23:59:59Z'

gh api repos/{owner}/{repo}/milestones/<number> -X PATCH -f description='...' -f due_on='...'
```

Rules:
- The milestone **description is the wave gate**. Paste the exit criteria there, so the
  definition of done sits where the work is.
- Due dates use the **p80** date from `estimate.v1`, and the description says so explicitly.
  A milestone due date presented as a point commitment misrepresents the plan.

## Step 3 — Templates

Issue **forms** (`.yml`) beat markdown templates: GitHub enforces required fields, so
`groom-backlog` receives structured input instead of prose.

| File | Source |
|---|---|
| `.github/ISSUE_TEMPLATE/bug.yml` | `templates/issue-bug.yml` |
| `.github/ISSUE_TEMPLATE/feature.yml` | `templates/issue-feature.yml` |
| `.github/ISSUE_TEMPLATE/config.yml` | `templates/issue-config.yml` — `blank_issues_enabled: false` |
| `.github/PULL_REQUEST_TEMPLATE.md` | `templates/pull-request.md` |

Idempotency: write only if absent or if the content differs; report `created` / `updated` /
`unchanged`. Never clobber a template the project already customised without showing the diff.

Verify the forms parse — GitHub silently ignores a malformed template, which looks identical to
it not being there:

```bash
gh api repos/{owner}/{repo}/contents/.github/ISSUE_TEMPLATE --jq '.[].name'
# then open the "New issue" chooser once and confirm the forms appear
```

## Step 4 — Projects v2 board

Requires the `project` scope. Field ids are opaque and repository-specific — always resolve them
at runtime; a hardcoded id produces a script that works exactly once.

```bash
gh project list --owner <owner> --format json
gh project create --owner <owner> --title "Delivery"
gh project field-list <number> --owner <owner> --format json
gh project item-list <number> --owner <owner> --format json --limit 500

gh project item-add <number> --owner <owner> \
  --url https://github.com/<owner>/<repo>/issues/318

gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --single-select-option-id <option-id>
```

Minimum field set: **Status** (Triage, Ready, In progress, In review, Done), **Size** (XS–XL),
**Iteration**, **Blocked**. Views to create: a board grouped by Status with WIP counts visible,
a table filtered `is:open no:assignee label:status:ready` (the pull queue), and a table filtered
`is:open label:blocked` sorted by age (the escalation queue).

Board automation is configured in the Project's own **Workflows** UI (item added → Triage; PR
merged → Done). Those are not scriptable via `gh` today: emit them as documented manual steps in
`docs/runbooks/github-governance.md` rather than pretending they were applied.

## Step 5 — Branch protection or rulesets

Rulesets are the current mechanism, compose by pattern and support bypass actors; classic branch
protection remains available via `.../branches/{branch}/protection`. Full documents and the
classic equivalent: `references/rulesets.md`.

```bash
gh api repos/{owner}/{repo}/rulesets --paginate --jq '.[] | {id,name,enforcement}'

# PUT the whole desired document — declarative, therefore idempotent
gh api repos/{owner}/{repo}/rulesets -X POST --input .github/rulesets/main.json
gh api repos/{owner}/{repo}/rulesets/<id> -X PUT --input .github/rulesets/main.json
```

Baseline on the default branch: block deletion, block non-fast-forward, require a pull request
(1 approval, dismiss stale reviews, require last-push approval, require conversation resolution),
and require named status checks.

Three rules that matter more than the JSON:

1. **Required checks must already exist.** A required check name no workflow produces blocks
   every PR forever. Verify:
   ```bash
   gh api repos/{owner}/{repo}/commits/$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)/check-runs \
     --jq '.check_runs[].name' | sort -u
   ```
2. **Start at `enforcement: evaluate`** on a repository with open PRs, review what would have
   been blocked, then move to `active`. Going straight to `active` strands in-flight PRs.
3. **Bypass actors are an audit finding, not a convenience.** If one is genuinely needed, record
   who and why as a `fact.v1` of type `decision`.

On a private repository without the required plan tier some ruleset features return 403/422.
Detect it, report it, fall back to classic protection — do not retry blindly.

## Step 6 — Required checks and minimal automation

Prefer built-in GitHub features over bespoke workflows; every workflow is code you maintain.

| Need | Mechanism |
|---|---|
| Move a card on PR open/merge | Projects v2 built-in workflows |
| Close an issue on merge | `Closes #N` in the PR body |
| Label by path | `actions/labeler` + `.github/labeler.yml` |
| Stale handling | `actions/stale` matching the `groom-backlog` ageing policy, `days-before-close: -1` initially so nothing closes automatically |
| Release notes | `.github/release.yml` with categories keyed to `type:` labels |
| Dependency updates | `.github/dependabot.yml` |

Any workflow written here **must** pin actions to a commit SHA (not a tag) and declare an
explicit least-privilege `permissions:` block. Default write-all permissions plus a floating tag
is a supply-chain risk; if you find one, report it as a finding.

## Step 7 — Verify and emit

Re-run the read commands from every step and compare against the desired state. Then run the
whole skill a second time: the diff must be empty.

```
Labels        : 31 desired | 24 created | 7 unchanged | 3 extra (removal proposed, not applied)
Milestones    :  4 desired |  2 created | 2 updated
Templates     :  4 files   |  3 created | 1 unchanged
Project       : "Delivery" #7 | fields Status,Size,Iteration,Blocked | 2 views | automation: MANUAL STEPS in docs/runbooks/github-governance.md
Rulesets      : main.json applied as evaluate (12 open PRs) — promote to active after review
Required chks : build, test, lint — all three confirmed present on the default branch
Second run    : 0 changes  ✅ idempotent
```

Write `handoff.v1` to `.foundry/blackboard/<wave>/github-operator.json` via
`mcp__plugin_foundry-core_foundry__blackboard_write`, listing created files in `artifacts[]` and every skipped
action in `blockedBy[]` with the exact command to complete it.

## Exit criteria

- [ ] Preflight recorded: `gh` version, auth, scopes, repository permissions, default branch.
- [ ] Every mutation preceded by a read and followed by a verifying read-back.
- [ ] Second full run produces zero changes — demonstrated, not asserted.
- [ ] No label deleted without explicit confirmation.
- [ ] Every required status-check name confirmed to be produced by an existing workflow.
- [ ] Rulesets applied at `evaluate` first when open PRs exist, unless the user chose otherwise.
- [ ] Any workflow written pins actions by SHA and declares least-privilege `permissions:`.
- [ ] Non-scriptable steps (Projects automation) documented as manual steps, not reported as done.
- [ ] `handoff.v1` validates and lists every skipped action with its reason and command.

## What this skill deliberately does not cover

- **CI pipeline design, build and deployment.** `foundry-ops`. This skill only *requires* checks
  the pipeline already produces.
- **Secret management.** It never creates, prints or rotates a secret; `gh secret set` is out of
  scope.
- **Git history operations.** No force-push, no rebase of shared branches, no tag moving.
- **Organisation-level policy.** Org rulesets, SSO, SCIM, billing — administrator territory; it
  reports what it cannot change.
- **Deciding scope, priority or dates.** It materialises `plan.v1`; it does not author it.
- **Release publication.** See `github-operator`; releases are created as drafts and published
  by a human.
- **Non-GitHub trackers.** Concepts port, commands do not.

## References

| File | Load when |
|---|---|
| `references/rulesets.md` | writing the ruleset document or the classic-protection equivalent |
| `references/gh-recipes.md` | any `gh` command that is not in this file, plus failure-mode handling |
| `templates/labels.json` | the label taxonomy as data |
| `templates/issue-bug.yml`, `templates/issue-feature.yml`, `templates/issue-config.yml` | issue forms |
| `templates/pull-request.md` | PR template with the DoD checklist |
