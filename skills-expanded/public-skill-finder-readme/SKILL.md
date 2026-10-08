# Public Skill Finder

`public-skill-finder` helps users discover and install publicly available agent skills from external/open-source registries.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## How to Help Users Find Skills

### Step 1: Extract Search Keywords (CRITICAL)

The public skill registry search supports traditional keyword search. It does not understand natural language or semantic queries. Before running the find command, convert the user's intent into concise, space-separated keywords.

Keyword extraction rules:

1. Remove filler words (how, do, I, can, you, help, me, want, need, etc.)
2. Keep domain-specific terms (react, go, kafka, docker, kubernetes, etc.)
3. Keep action verbs that describe the task (deploy, test, monitor, review, lint, etc.)
4. Use lowercase
5. Aim for 2-4 keywords for best results

### Step 2: Search for Skills

Run the find command with the extracted keywords:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 6
```

Manual CLI equivalent:

```bash
npx -y skills@latest find resume generator --source external -y
```

### Step 3: Interpret the Results

The CLI output groups public registry results under headers such as `EXTERNAL SKILLS`. The helper script parses that output, ignores non-public sections if they appear, deduplicates package identifiers, and renders matches as `[Public]` candidates.

### Step 4: Verify Quality Before Recommending

Do not recommend a skill based solely on search results. Always verify:

- Install/star count: Prefer skills with higher adoption. Be cautious with very low counts.
- Source reputation: For public skills, official or well-known sources such as `vercel-labs`, `anthropic`, and `microsoft` are more trustworthy.
- Relevance: Make sure the skill actually matches what the user needs, not just keyword overlap.

### Step 5: Present Options to the User

When you find relevant skills, present them clearly with the source labeled:

```markdown
**[Public]** `owner/repo@skill-name`
Source: https://skills.sh/owner/repo/skill-name
Best for: [specific use case]
Caveats: [none / needs API key / low adoption / verify docs]
Install: `npx -y skills@latest add "owner/repo@skill-name" -g -y`
```

### Step 6: Offer to Install

If the user wants to proceed, install the skill for them:

```bash
npx -y skills@latest add "owner/repo@skill-name" -g -y
```

## What It Does

- Converts natural-language requests into concise registry search keywords.
- Searches public skills through `skills@latest`.
- Cleans CLI output, deduplicates results, and renders Markdown or JSON summaries.
- Guides agents to verify a candidate skill before recommending it.

## Install

Install this skill from the repository:

```bash
npx -y skills@latest add 3299129776-a11y/public-skill-finder --skill public-skill-finder -g -y --full-depth
```

## Usage

Ask Codex:

```text
Use $public-skill-finder to find a skill for resume generation.
```

Or run the helper script directly from the skill directory:

```bash
python scripts/find_public_skills.py "resume generator" --extra-query "cv resume" --limit 5
python scripts/find_public_skills.py "social media analytics" --format json --limit 3
```

## Repository Layout

```text
skills/
  public-skill-finder/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      find_public_skills.py
    references/
      github-publishing.md
      search-and-evaluation.md
```

## Notes

This repository is scoped to public/open-source skill discovery. It does not include private registry configuration, organization-specific authentication flows, package mirrors, or telemetry hooks.
