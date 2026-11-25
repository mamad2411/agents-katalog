---
name: add-skill-from-repo
description: Import third-party skills from a git repository into the home agent system by cloning into ~/.agents/vendor, exposing selected skills through ~/.agents/skills, and creating same-name command wrappers in ~/.agents/commands. Use when the user provides a skill repository URL or wants to bring external skills into the local canonical layout.
---

# Add Skill From Repo

Import external skill repositories into the home-global skill system.

Use this pattern:

1. clone into `~/.agents/vendor/...`
2. choose which upstream skills to expose
3. symlink selected skills into `~/.agents/skills/...`
4. create same-name wrappers in `~/.agents/commands/...`

## Reference Skills

Before acting:

1. Read `~/.agents/skills/create-my-skill/SKILL.md` for the local skill and wrapper pattern.
2. Read `~/.agents/skills/manage-agent-skills/SKILL.md` for consolidation rules and validation expectations.

Use them as references only.

## Goal

Bring third-party skills into your system without making the upstream repo itself the canonical public interface.

Keep this separation:

- upstream source: `~/.agents/vendor/<source>/...`
- your canonical exposure: `~/.agents/skills/<canonical-name>`
- your command wrapper: `~/.agents/commands/<canonical-name>.md`

## Step 1: Gather Inputs

From the user, collect or infer:

- git repo URL
- optional branch or ref
- which upstream skills to expose
- optional canonical rename for each exposed skill

If the repo contains many skills and the user did not specify which ones to use, inspect the upstream `skills/` directory and ask one targeted question listing the choices.

## Step 2: Choose Vendor Path

Clone the repository into a stable vendor path under:

`~/.agents/vendor/<source-name>/`

Choose a predictable vendor directory name derived from the repo owner and repo name, for example:

- `vercel-labs-agent-skills`
- `acme-internal-skills`

Do not clone directly into `~/.agents/skills/`.

## Step 3: Inspect Upstream Layout

Look for upstream skills under paths such as:

- `skills/<skill-name>/SKILL.md`
- `<repo-root>/<skill-name>/SKILL.md`

Prefer upstream skills that already follow the skill directory pattern.

If the repo does not contain a clear skills layout, stop and explain what is missing.

## Step 4: Select Canonical Names

For every exposed skill, choose a canonical name in `~/.agents/skills`.

Default rule:

- add a source prefix when the name is generic or likely to collide

Examples:

- upstream `react-best-practices` -> `vercel-react-best-practices`
- upstream `composition-patterns` -> `vercel-composition-patterns`

Keep the upstream vendor path unchanged. Only the exposed name should change.

## Step 5: Expose Through ~/.agents/skills

Create a symlink for each selected skill:

- source: `~/.agents/vendor/<source>/.../<upstream-skill-dir>`
- target: `~/.agents/skills/<canonical-name>`

Use symlink when:

- you want to track upstream content closely
- you are not modifying the skill content locally

Use copy instead of symlink only when:

- you need to modify the skill
- you want a frozen local fork
- you need to combine or trim upstream content

## Step 6: Create Same-Name Command Wrappers

For every exposed skill, create:

`~/.agents/commands/<canonical-name>.md`

Use this wrapper template:

```md
---
description: Run the <canonical-name> workflow
---

Load and follow the `<canonical-name>` skill.

If arguments were provided, treat them as additional context:

$ARGUMENTS
```

## Step 7: Validate

Verify:

- the vendor repo exists under `~/.agents/vendor`
- each selected canonical skill exists under `~/.agents/skills`
- each selected canonical command exists under `~/.agents/commands`
- each canonical skill symlink resolves correctly when symlink mode is used
- there are no name collisions with unrelated existing skills

## Important Rules

- do not expose the whole vendor repo blindly if the user only needs a subset
- do not place third-party skills directly in repo-local `.cursor` or `.claude` directories
- do not use upstream generic names if they collide with your current skill set
- prefer source-prefixed canonical names for third-party imports
- keep wrappers thin

## Output Back To User

When done, report:

- vendor repo path
- upstream skills discovered
- canonical skills exposed
- command wrappers created
- whether symlink or copy was used
- any collisions or follow-up recommendations
