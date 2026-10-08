---
name: gh-cli-projects-tasks-conventions
description: "How The Lossless Group uses the `gh` CLI for GitHub issues and Projects v2 tasks across the pseudomonorepo tree. Use whenever creating, editing, or listing GitHub Project tasks via `gh project item-create`, `gh project item-add`, or `gh project item-edit`; whenever creating repo issues via `gh issue create`; whenever the user mentions \"gh project\", \"create a task\", \"create an issue\", \"add to the project\", \"draft a project item\", \"ProjectV2\", labels, milestones, issue types, or asks to script task/issue creation; whenever an agent is about to author a task body that references one or more `context-v/` files. Encodes the **task-body-is-a-github-link** convention — every task whose work-context lives in a `context-v/` file gets a body whose primary content is a clickable GitHub URL to that file in its own repo (NOT a deep path inside the parent monorepo, because each pseudomonorepo level is its own git repo and the URL must respect that) — and the **prefill-the-sidebar** convention: query the repo/org's actual labels, milestones, assignees, and issue types, infer the best fit, ask the user only when nothing fits logically. Composes with the `pseudomonorepos` skill to identify which repo a local context-v path belongs to and which branch tier (`development` / `main` / `master`) the link should target."
---

# gh CLI · Projects & Tasks Conventions

> **Premature on purpose — 2026-06-05.** We don't yet have many preferences. The ones that exist are codified here so they don't drift in the meantime — **listed in order of priority to adhere to, not in the order they were added**: (1) compose with [[pseudomonorepos]] to figure out which repo a local path actually lives in; (2) every task body that points at a `context-v/` file points at it via a clickable GitHub URL; (3) pin the branch explicitly when worktrees are in play, because `HEAD` answers per-worktree; (4) prefill the issue sidebar — assignee, label, type, milestone — by querying the available options and inferring best fit, asking the user only when nothing fits (Convention 6). As more conventions emerge (status field discipline, priority discipline, custom-field schemas, project-per-app vs project-per-engagement), they get added here.

## When to use this skill

- Creating, editing, or listing GitHub Project tasks via `gh project` — particularly `item-create`, `item-add`, `item-edit`.
- Creating repo issues via `gh issue create` whose sidebar (assignee, labels, type, milestone) should arrive prefilled (Convention 6).
- The user says "create a task," "add to the project," "draft a project item," "set up a project," "gh project," or any variant.
- An agent is about to author a task body that references one or more `context-v/` files anywhere in the pseudomonorepo tree.
- Scripting bulk task creation from a spec, exploration, or plan that has sections / decisions / placeholders worth tracking.
- Any of the above **while git worktrees are in play** — multiple checkouts of the same repo at different branch tiers change what `HEAD` resolves to, and therefore which branch ends up in the link (Convention 3b).

## Compose with `pseudomonorepos`

This skill assumes [[pseudomonorepos]] is in context. The tree-walking discipline there is what makes the link-building behavior below correct: a `context-v/` file at `/Users/mpstaton/code/lossless-monorepo/ai-labs/context-v/explorations/X.md` does **not** live in the `lossless-monorepo` repo on GitHub — it lives in the `ai-labs` repo, which is submoduled. The link convention below depends on resolving the right repo before building the URL.

If you don't load `pseudomonorepos` first, you will produce links that look right (`github.com/lossless-group/lossless-monorepo/blob/development/ai-labs/context-v/...`) but 404, because that path doesn't exist in the parent repo — only the submodule pointer does.

## The behavioral core (this is the actual skill)

### Convention 1 — Task bodies that reference `context-v/` files use GitHub URLs

When a task's work-context is "go read these context-v files and act on them," the **body of the task is, primarily, the GitHub link(s) to those files**. Not a copy-pasted summary. Not a path the collaborator has to translate manually. A clickable URL that lands them in the right file in the right repo on the right branch.

**Why:** project items are read by collaborators who may not have the full tree cloned. They click. The click has to work. A correct link is the difference between "I'll get to it" and "where is this." A wrong link silently rots the trust the project list is supposed to build.

**Body shape, default:**

```markdown
Context:
- [<file title or relative path>](<github URL to file in its own repo on its own branch>)
- [<another file>](<URL>)

<optional one-line ask if the title doesn't make the ask obvious>
```

That's it for the default. The link is the whole point. Add prose only when the file title doesn't convey what the work is.

### Convention 2 — Building the URL correctly

Given a local path `/Users/mpstaton/code/lossless-monorepo/<some-sub-path>/context-v/<rest>/<file>.md`, the URL is **not** built by string-substitution on the parent path. It is built by asking the **repo that actually owns the file** for its remote and branch.

Recipe:

```bash
# Given LOCAL_PATH = an absolute path to a context-v file
DIR=$(dirname "$LOCAL_PATH")
cd "$DIR"

# 1. Find the git root of the repo that owns this file (NOT the parent monorepo)
REPO_ROOT=$(git rev-parse --show-toplevel)

# 2. Get its origin remote (the GitHub URL of the repo this file is in)
REMOTE=$(git remote get-url origin)
# Normalize: git@github.com:owner/repo.git or https://github.com/owner/repo.git → owner/repo
OWNER_REPO=$(echo "$REMOTE" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')

# 3. Get the current branch on that repo (NOT the parent's branch — they may differ)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 4. Compute the file's path relative to the repo root
REL_PATH=$(realpath --relative-to="$REPO_ROOT" "$LOCAL_PATH")

# 5. Assemble
URL="https://github.com/${OWNER_REPO}/blob/${BRANCH}/${REL_PATH}"
echo "$URL"
```

The `cd "$DIR"` and `git rev-parse --show-toplevel` together do the work of "which repo am I actually in" — submodules report their own root, not the parent's. That's the entire point.

**On macOS, `realpath --relative-to` requires coreutils** (`brew install coreutils` then `grealpath`, or use Python: `python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$LOCAL_PATH" "$REPO_ROOT"`).

### Convention 3 — Branch tier (per [[pseudomonorepos]])

The branch the URL targets must match the **branch tier** of the work the task represents:

- Active work in motion → `development` (default).
- Cohesive shipped chunk → `main`.
- Settled stable surface → `master`.

The recipe above uses `git rev-parse --abbrev-ref HEAD` because the file's own repo is presumably checked out at the tier the work is happening on. If you're scripting from a stale checkout, override `BRANCH` explicitly.

**Do not** default to `main` blindly because it's GitHub's default. The pseudomonorepo tree's default tier for in-motion work is `development`. A link to `main` for a draft spec produces a 404 (the spec is on `development`, hasn't been promoted yet).

### Convention 3b — Git worktrees make `HEAD` ambiguous; pin the branch (2026-08-14)

Convention 2's recipe resolves two things from the shell's current location:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
```

**Both are per-worktree, not per-repository.** A linked worktree has its own
`HEAD`, its own index, and its own checked-out branch, while sharing one object
database and one set of refs with the main worktree. So `--show-toplevel` returns
*that worktree's* root and `--abbrev-ref HEAD` returns *that worktree's* branch.

That's correct behavior, and it's exactly what makes the recipe safe to run from
inside a submodule. But it introduces a failure mode Convention 3 doesn't cover
on its own:

> If the tree has more than one worktree checked out at different tiers — say a
> `development` worktree and a `main` worktree — then running the recipe from the
> wrong directory silently produces a link to the wrong tier.

This is nastier than the plain wrong-branch mistake, because the two directories
are indistinguishable at a glance. Neither is "the" repo. Both have a valid
`.git`. The URL that comes out is well-formed and 404s only for the reader.

**The rules:**

1. **When generating a link for one file**, `cd` to that file's own directory
   first — as Convention 2 already instructs — and let `--show-toplevel` resolve
   it. Never assume the shell's current worktree is the one you mean.
2. **When scripting in bulk, pin the branch explicitly** rather than inheriting
   whatever the ambient worktree happens to be on:

   ```bash
   BRANCH=development     # deliberate, not inherited
   URL="https://github.com/${OWNER_REPO}/blob/${BRANCH}/${REL_PATH}"
   ```
3. **When auditing what's checked out where**, use the porcelain form. Human
   output marks worktree branches with `+` instead of `*`, which quietly breaks
   scripts that grep for `*` to find the current branch:

   ```bash
   git worktree list --porcelain
   ```

**One-worktree-per-issue composes well** with the rest of this skill — the branch,
the directory, and the task can all carry the issue number, and `gh` works
normally inside a worktree because it reads the shared remote config:

```bash
git worktree add -b issue/42-portfolio-monitoring ../repo--42 development
cd ../repo--42
gh pr create --fill
```

Two setup steps that bite in this tree specifically: `git worktree add` does
**not** populate submodules (`git submodule update --init --recursive` is
required), and gitignored files do not come along — which in `self-host-stack`
means the entire `client-stacks/` directory, and everywhere means `.env`.

Full treatment: [[Git Worktrees]] in `content-md/lossless/`.

### Convention 4 — One link per relevant file, not summary-replaces-link

If a task pulls from three files, the body lists three links. Do **not** synthesize one prose paragraph that "summarizes" all three; that creates a second source of truth that immediately drifts from the files themselves. The whole point of the link is that the file is the source. The body is a pointer set, not a recap.

### Convention 5 — When the work is itself authoring a new context-v file

If the task is "write a new `context-v/` file," the link can't exist yet. In that case:

- **Title:** name the file you intend to create, exactly (Train-Case, `.md` extension implied).
- **Body:** list the prior-art files that the new file will inherit from, as links per Convention 1. Optionally add a one-line "Lands at: `<intended-repo>/<intended-path>`".

When the file is later created, edit the task to add the actual link.

### Convention 6 — Prefill the issue sidebar from queried options (2026-07-24)

A bare issue with an empty sidebar (no assignee, no label, no type) pushes
triage work onto the human later. The agent creating the issue fills what it
can at creation time — **by querying the repo/org for the actual available
options first, inferring the best fit, and asking the user only when no
option is a logical fit.** Never invent labels, types, or milestones that
don't exist; never guess when the fit isn't obvious.

**Step 1 — query the vocabulary** (cache per repo per session; it rarely changes):

```bash
gh label list --repo "$OWNER_REPO"                       # labels
gh api "repos/$OWNER_REPO/milestones" -q '.[].title'     # milestones
gh api "repos/$OWNER_REPO/assignees" -q '.[].login'      # assignable users
gh api graphql -f query='query { organization(login: "'$OWNER'") {
  issueTypes(first: 20) { nodes { id name description } } } }'   # issue types (org-level)
```

**Step 2 — infer best fit, per field:**

- **Assignee:** the operator driving the session (their `gh api user -q .login`), unless the task is explicitly for someone else.
- **Label:** map the issue's nature onto what exists — broken behavior → `bug`, new capability → `enhancement`, docs → `documentation`, etc. When the repo has richer custom labels, match on their names/descriptions.
- **Type** (when the org has issue types — lossless-group's are `Task / Bug / Feature / Improve / Refactor`): broken behavior → Bug; new capability/surface → Feature; polish of an existing surface → Improve; restructure-without-behavior-change → Refactor; process/chore → Task.
- **Milestone:** only when an existing milestone's title clearly covers the work. Stale-looking milestones (old dates, finished eras) → skip, don't guess.
- **If nothing fits logically, ask the user** — one short question naming the candidates considered — instead of leaving the field empty silently or forcing a bad fit.

**Step 3 — apply.** Assignee/label/milestone ride `gh issue create` flags
(`--assignee`, `--label`, `--milestone`). Issue **Type** has no CLI flag —
set it right after creation via GraphQL:

```bash
IID=$(gh api graphql -f query='query { repository(owner: "'$OWNER'", name: "'$REPO'") {
  issue(number: '$N') { id } } }' -q .data.repository.issue.id)
gh api graphql -f query='mutation { updateIssueIssueType(input: {
  issueId: "'$IID'", issueTypeId: "'$TYPE_ID'" }) { issue { number } } }'
```

**Creating vocabulary when the user asks for it** (never as a side effect):

```bash
gh label create "workbench" --repo "$OWNER_REPO" --description "Org Workbench surface" --color "5319e7"
# Milestones have no dedicated gh command — the API create is one line:
gh api "repos/$OWNER_REPO/milestones" -f title="v1.2 — didi crawls" -f description="…" -f due_on="2026-08-15T00:00:00Z"
```

**Projects membership and Projects-v2 fields (e.g. Priority)** remain
token-gated: they need the `project` scope (`gh auth refresh -s project`)
and go through `gh project item-add` / `item-edit` per the recipes below —
prefill them too once the scope exists.

## Practical `gh project` recipes

### Look up the IDs you'll need (one-time per project)

```bash
OWNER=lossless-group
PNUM=<project number from the URL>

# Project node ID + field metadata
gh project view "$PNUM" --owner "$OWNER" --format json | jq '.id'
gh project field-list "$PNUM" --owner "$OWNER" --format json
```

Cache the project ID, the `Status` field ID, and the option IDs for `Todo`/`In Progress`/`Done` in script variables. They don't change.

### Create a single task that points at a context-v file

```bash
# (URL produced via the recipe above)
URL="https://github.com/lossless-group/ai-labs/blob/development/context-v/explorations/Cloud-Variant-of-Dididecks-AI-Workspace.md"

ITEM_ID=$(gh project item-create "$PNUM" --owner "$OWNER" \
  --title "Close Decision 1 (architectural shape) on Cloud-Workspace spec" \
  --body  "Context:
- [Cloud-Variant-of-Dididecks-AI-Workspace.md]($URL)" \
  --format json | jq -r .id)
```

### Bulk-create tasks from sections of a spec

A common shape: a spec stub has N placeholder sections each marked `[awaits discussion]`. One task per section, each body linking to the spec.

```bash
SPEC_URL="https://github.com/lossless-group/dididecks-ai/blob/development/context-v/specs/Cloud-Workspace-for-Dididecks.md"

# Array of (title, anchor) pairs — anchor is the section's GitHub anchor (slugified)
declare -a TASKS=(
  "Fill in Section 1: Privacy-property contract|#1-privacy-property-contract--awaits-discussion"
  "Fill in Section 4: Threat model and mitigations|#4-threat-model-and-mitigations--awaits-discussion"
  "Fill in Section 5: Network and runtime topology|#5-network-and-runtime-topology--awaits-discussion"
)

for entry in "${TASKS[@]}"; do
  TITLE="${entry%%|*}"
  ANCHOR="${entry##*|}"
  gh project item-create "$PNUM" --owner "$OWNER" \
    --title "$TITLE" \
    --body  "Context:
- [Cloud-Workspace-for-Dididecks.md → $TITLE](${SPEC_URL}${ANCHOR})"
done
```

GitHub auto-generates section anchors as kebab-cased slugs of the heading text. Verify the anchor by opening the file on GitHub and clicking the link icon next to the section heading — it produces the canonical anchor.

### Add an existing issue (not a draft) to the project

```bash
gh project item-add "$PNUM" --owner "$OWNER" \
  --url https://github.com/lossless-group/dididecks-ai/issues/42
```

Use this when the work is concrete enough to be a tracked issue with its own discussion, labels, and assignees. Draft items via `item-create` are for tasks that don't deserve repo-level discussion overhead.

### Set Status (or any single-select field)

```bash
PROJECT_ID="PVT_..."           # from gh project view
STATUS_FIELD_ID="PVTSSF_..."   # from gh project field-list
TODO_OPTION_ID="..."           # from the same field-list, under .fields[].options[]

gh project item-edit \
  --id "$ITEM_ID" \
  --project-id "$PROJECT_ID" \
  --field-id "$STATUS_FIELD_ID" \
  --single-select-option-id "$TODO_OPTION_ID"
```

Field IDs are GraphQL node IDs (long opaque strings). Fetch once with `field-list --format json`, cache in the script.

## Auth

```bash
gh auth status                # confirm token has 'project' scope
gh auth refresh -s project    # add the scope if missing
```

The `project` scope is separate from `repo`. A token that creates issues fine may still 403 on `gh project` calls until refreshed.

## When `gh project` isn't enough

Anything `gh project` doesn't expose (custom field schemas, complex field updates in one call, project iteration / views) is reachable via the same auth with raw GraphQL:

```bash
gh api graphql -F query='
  query($org: String!, $num: Int!) {
    organization(login: $org) {
      projectV2(number: $num) {
        id
        title
        fields(first: 20) { nodes { ... on ProjectV2FieldCommon { id name } } }
      }
    }
  }
' -F org="$OWNER" -F num="$PNUM"
```

Same token, more flexibility. Don't reach for it until `gh project` actually fails — the CLI is easier to read in a script.

## Anti-patterns

**Don't point a project task at the parent monorepo path of a submodule file.** `github.com/lossless-group/lossless-monorepo/blob/.../ai-labs/context-v/...` does NOT exist on GitHub — the parent only has a submodule pointer at `ai-labs`, not the file tree. The link 404s. Use the child repo's own URL.

**Don't paste a long prose summary into the task body and skip the link.** The collaborator can read the file. The body's job is to send them to it.

**Don't use the wrong branch in the URL.** The default tier for in-motion work is `development`, not `main`. Build the URL from the repo's actual current branch, not from convention.

**Don't inherit the branch from an ambient worktree when scripting.** `git rev-parse --abbrev-ref HEAD` answers for whichever worktree the shell is standing in. With a `development` worktree and a `main` worktree side by side, the two directories look identical and the wrong one yields a well-formed URL that 404s. Pin `BRANCH` explicitly for bulk generation (Convention 3b).

**Don't grep `git branch -vv` for `*` to find the current branch.** Branches checked out in *another* worktree are marked `+`, not `*`. Use `git worktree list --porcelain`.

**Don't `gh project item-create` for work that genuinely belongs as a repo issue.** Draft items are for "tasks at the project layer that don't need their own labels / assignees / repo-level discussion." If reviewers need to comment, if there's a PR coming, if there are CI checks — make an issue first (`gh issue create`), then `gh project item-add`.

**Don't lose track of the project ID and field IDs.** Every `item-edit` needs them. A `.env`-style file at the project's working directory (`PROJECT_ID=…`, `STATUS_FIELD_ID=…`, `TODO_OPTION_ID=…`) is fine; just don't re-fetch them on every call.

**Don't auto-bump project status as a side effect of merging code.** That's [[git-conventions]]-adjacent and belongs in deliberate post-merge updates, not in workflow magic. (Provisional rule; may evolve.)

## After authoring or editing this skill

Per [[../../AUTHORING.md]]:

```bash
bash sync-skills.sh
```

This is **not** automatic. Both Claude Code and Pi need per-skill symlinks at `~/.claude/skills/<name>/SKILL.md` and `~/.pi/skills/<name>/SKILL.md`. The script handles that; running it is the human (or agent) step.

## Open seams (future preferences likely to live here)

Listed so they're visible as the skill grows:

- Status discipline — when a project item moves from Todo → In Progress → Done, who moves it and based on what signal.
- Worktree-aware auditing — whether the HARD STOP preconditions in [[pseudomonorepos]] need updating for the `+` prefix and for commits reachable only from a linked worktree's reflog.
- Priority discipline — the Priority field exists on the project but stays token-gated (`project` scope) and semantically undefined; when unlocked, define what its options mean and prefill per Convention 6.
- Label taxonomy — Convention 6 maps onto the default labels today; a richer house set (surface/domain labels) is deliberately deferred until the user names one.
- Project layout — one project per app vs one per engagement vs one per quarter. Currently undecided.
- Custom field conventions — Repo, Engagement, Type, etc.
- Iteration / sprint conventions — if we adopt them.
- Cross-app project rollups — if a parent-level project ever aggregates child-app items.
- Auto-archival rules — when Done items leave the active view.

When any of these settle, add the convention here. Until then, defer to whatever the user wants in the moment.

## Related

- [[pseudomonorepos]] — load before this skill; the tree-walking discipline is what makes Convention 2 correct.
- [[context-vigilance]] — what `context-v/` files look like, so the things being linked to follow the discipline.
- [[git-conventions]] — commit-message shape, branch tiering. Task-body links to a context-v file inherit the branch tier from the same model.
- [[Git Worktrees]] (`content-md/lossless/`) — full treatment of the worktree mechanics behind Convention 3b: what is shared vs. per-worktree, the submodule and gitignored-file gotchas, and how one-worktree-per-issue composes with this skill.
- [[changelog-conventions]] — when a project task is "ship this," the corresponding changelog entry lives in `<repo>/changelog/` per that skill.
- External — gh CLI Projects docs: <https://cli.github.com/manual/gh_project>
- External — GitHub ProjectV2 GraphQL reference: <https://docs.github.com/en/graphql/reference/objects#projectv2>
