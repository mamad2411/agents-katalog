---
name: update-context
description: Lightweight update of project context for a feature branch. Updates plan status, review items, PR comments, and recent git activity without re-extracting API docs or re-analyzing source code. Supports both tiered contexts (`api-context.md` + `project-context.md`) and legacy single-file `context.md` branches. Use when user says "update context", "refresh context", or between sessions when the full /build-context is overkill.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Update Context

Lightweight update of the dynamic project context (~1 min). Skips API docs (cached), source code analysis (stable), and test analysis (stable). Only refreshes what actually changes between sessions: plan status, review items, PR comments, and git activity.

**When to use:**
- Between sessions on the same feature branch
- After merging PRs or resolving review comments
- After updating plans or completing tasks
- When `/load-context` warns that project context is stale

**When NOT to use — use `/build-context` instead:**
- First time on a new feature (no context files exist)
- After significant code restructuring (must-read files may have changed)
- When upstream-integration or third-party docs have been updated

## Instructions

### Step 1: Validate Context Exists

1. Get the current git branch: `git branch --show-current`
2. Check for tiered context files at `contexts/{branch-name}/api-context.md` and `contexts/{branch-name}/project-context.md`
3. If both exist, operate in **tiered mode**
4. Otherwise, check for legacy single-file context at `contexts/{branch-name}/context.md`
5. If the legacy file exists, operate in **legacy mode**
6. If neither tiered nor legacy context exists:
   - Tell the user: "Context files not found for `{branch-name}`. Run `/build-context` first."
   - Stop here.

### Step 2: Gather Fresh Data (parallel)

Launch up to 3 lightweight operations in parallel:

#### 2a. Plans & Reviews

Read `plans/{branch-name}/` to extract:
- Current plan task statuses (done, in progress, blocked)
- Open review items and severity
- Key decisions and rationale
- Remaining work items

If no plans directory exists, note "No plans found for this branch."

#### 2b. PR Comments (if applicable)

Use the available GitHub/PR review tooling in the current environment to check for open PRs on the current branch and read their comments.

Extract:
- Open review comments and resolution status
- Reviewer feedback themes
- Requested changes not yet addressed

If no open PRs, note "No open PRs for this branch." If GitHub/PR tooling is unavailable, note that PR comments could not be refreshed.

#### 2c. Recent Git Activity

```bash
# Commits since the last context build
git log --oneline --since="{project-context generated_at}" --no-merges
```

Summarize:
- Number of commits since last context
- Key changes (from commit messages)
- Files changed (high-level: "5 handler files, 3 test files")

### Step 3: Read Current Project Context

Read the existing context file(s) for the current mode:

- **Tiered mode:** read `contexts/{branch-name}/project-context.md` to preserve sections that aren't being refreshed (must-read files, architecture patterns, source code insights, test patterns, review rules). Also read `contexts/{branch-name}/context.md` so the combined file can be updated without disturbing unrelated sections.
- **Legacy mode:** read `contexts/{branch-name}/context.md` and preserve every section except the ones being refreshed.

### Step 4: Update Project Context

Update the current-mode project context:

- **Tiered mode:** edit `contexts/{branch-name}/project-context.md`
  1. Update the `generated_at` timestamp in the YAML front matter
  2. **Replace** the `## Plan Status` section with fresh data from Step 2a
  3. **Replace** the `## Open Review Items` section with fresh data from Step 2b
  4. **Add/update** a `## Recent Activity` section after Open Review Items:
     ```markdown
     ## Recent Activity

     {N} commits since last context build ({date}):
     - {commit summary 1}
     - {commit summary 2}
     ...
     ```
  5. **Preserve all other sections unchanged** (Critical Path, Current State & Gaps, Must-Read Files, Internal Architecture, Source Code Insights, Test Patterns, Review Rules)

- **Legacy mode:** edit `contexts/{branch-name}/context.md` directly
  1. Update the top-level `Generated:` date if present
  2. **Replace or add** the `## Plan Status` section with fresh data from Step 2a
  3. **Replace or add** the `## Open Review Items` section with fresh data from Step 2b
  4. **Replace or add** a `## Recent Activity` section after Open Review Items
  5. **Preserve all other sections unchanged**

### Step 5: Re-assemble Combined Context

Only in **tiered mode**, read `contexts/{branch-name}/context.md`, then update it:

1. Update the `Project Context:` date in the header
2. **Replace** the `## Plan Status` section with the fresh version
3. **Replace** the `## Open Review Items` section with the fresh version
4. **Replace or add** the `## Recent Activity` section with the fresh version
5. **Preserve all other sections unchanged**

In **legacy mode**, skip this step because `context.md` was already updated in Step 4.

### Step 6: Summary

```
Context refreshed for branch `{branch-name}`.

Mode: {tiered | legacy}

Updated:
  - Plan status: {N} completed, {N} in progress, {N} remaining
  - Review items: {N} open ({N} new since last refresh)
  - Git activity: {N} commits since {last context date}

Unchanged:
  - Must-read files: {N} critical, {N} important
  - Source code insights, test patterns, review rules
  {If tiered mode:}
  - API context: {api-context generated_at}
  {End if}

Files updated:
  {If tiered mode:}
  - contexts/{branch-name}/project-context.md
  - contexts/{branch-name}/context.md
  {Else legacy mode:}
  - contexts/{branch-name}/context.md
  {End if}
```

## Critical Rules

- **Support both formats** — tiered contexts use `api-context.md` + `project-context.md`; legacy branches may only have `context.md`. Do not force a rebuild solely because the branch still uses the legacy format.
- **Never touch api-context.md in tiered mode** — that's Tier 1 (cached). Only `/build-context --force` rebuilds it.
- **Preserve non-refreshed sections** — must-read files, architecture patterns, source code insights, test patterns, and review rules are expensive to rebuild. Only replace plan status, review items, and activity.
- **Edit, don't rewrite** — use targeted edits on project-context.md and context.md rather than full rewrites to minimize diff noise.
- **Fail fast if no context exists** — this is an update skill, not a build skill.
- **Include git activity** — recent commits since last context build are cheap to gather and high-value for orientation.
- **Use environment-appropriate PR tooling** — describe the action generically and use whichever GitHub/PR review tooling is available.

## Checklist

- [ ] Context files exist for current branch (tiered or legacy)
- [ ] Plan status refreshed from plans/{branch-name}/
- [ ] PR comments checked via available PR tooling (or explicitly noted unavailable)
- [ ] Recent git activity gathered
- [ ] project context updated (project-context.md in tiered mode, context.md in legacy mode)
- [ ] context.md re-assembled in tiered mode
- [ ] Summary presented with what changed vs what's preserved

## Reference

- `.agents/skills/build-context/SKILL.md` — full context build with tiered caching
- `.agents/skills/load-context/SKILL.md` — read-only context loading into conversation
