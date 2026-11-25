---
name: find-skills
description: Search and discover agent skills from skills.sh, then install them into the workspace. Use when the user asks to find, search for, or install new skills, says "find a skill for X", "is there a skill that can...", asks "how do I add a skill", or wants to extend the agent with new capabilities from the skills ecosystem.
---

# Find Skills

Search for skills from the open agent skills ecosystem at [skills.sh](https://skills.sh/) and install them into the workspace.

## When to Use

- User asks to find, search for, or browse skills
- User asks "is there a skill for X" or "find a skill for X"
- User wants to install a new skill from skills.sh
- User asks to extend the agent's capabilities with a new skill

## How to Search

Use the `npx skills find` command to search by keyword:

```bash
npx -y skills find [query]
```

Examples:
- `npx -y skills find react testing`
- `npx -y skills find deployment`
- `npx -y skills find code review`

The command outputs matching skills with their names and sources.

You can also browse the leaderboard at https://skills.sh/ to find popular skills.

## Presenting Results

When presenting search results to the user, include for each relevant skill:

1. **Skill name** and a short description of what it does
2. **Source** (owner/repo)
3. **Skills.sh URL** so the user can review it: `https://skills.sh/<owner>/<repo>/<skill-name>`

Example:

> I found these skills:
>
> 1. **react-best-practices** — React and Next.js optimization guidelines
>    Source: `vercel-labs/agent-skills`
>    Details: https://skills.sh/vercel-labs/agent-skills/react-best-practices
>
> 2. **frontend-design** — Production-grade frontend interface design
>    Source: `anthropics/skills`
>    Details: https://skills.sh/anthropics/skills/frontend-design
>
> Would you like to install any of these?

## Installation

**Always ask the user for confirmation before installing.** Include the full skills.sh URL so they can review the skill details first.

Once the user confirms, install the skill directly into the workspace skills directory:

```bash
npx -y skills add <owner/repo> --skill <skill-name> --agent universal --copy -y
```

The `--agent universal` flag installs to `.agents/skills/` which maps to the cawpilot skills directory. The `--copy` flag copies files instead of symlinking. The `-y` flag skips the CLI's own prompts.

After installation, copy the skill from `.agents/skills/<skill-name>/` to the workspace's `.cawpilot/skills/<skill-name>/` directory:

```bash
cp -r .agents/skills/<skill-name> <workspace>/.cawpilot/skills/<skill-name>
```

Then clean up the `.agents/skills/` directory created by the CLI:

```bash
rm -rf .agents/skills/<skill-name>
```

Finally, inform the user the skill is installed and will be available from the next task onward.

## Important Rules

- **Never install without user confirmation.** Always show the skills.sh URL first.
- **Only install to `.cawpilot/skills/`** inside the workspace. Never install globally or to other agent directories.
- **One skill at a time.** If the user wants multiple skills, confirm and install each separately.
- **Clean up** the temporary `.agents/skills/` directory after copying.

## When No Skills Are Found

If no matching skills exist:

1. Tell the user no skills were found for their query
2. Suggest trying alternative search terms
3. Offer to help with the task directly using existing capabilities. Alternatively, offer to create a custom skill for their needs if it's a common request using the `skill-creator` skill.
