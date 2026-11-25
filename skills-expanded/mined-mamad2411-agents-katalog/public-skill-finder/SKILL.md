---
name: public-skill-finder
description: Helps users discover and install publicly available agent skills from external/open-source registries when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Use when the user is looking for functionality that might exist as an installable skill.
---

# Public Skill Finder

Find publicly available installable agent skills that match the user's described task.

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

If results are weak, run alternate queries:

- Use synonyms: `resume`, `cv`, `career`, `job application`.
- Pair domain + action: `react testing`, `seo audit`, `pdf extraction`.
- Try narrower or broader terms.

### Step 3: Interpret the Results

The CLI output groups public registry results under headers such as `EXTERNAL SKILLS`. The helper script parses that output, ignores non-public sections if they appear, deduplicates package identifiers, and renders matches as `[Public]` candidates.

### Step 4: Verify Quality Before Recommending

Do not recommend a skill based solely on search results. Always verify:

- Install/star count: Prefer skills with higher adoption. Be cautious with very low counts.
- Source reputation: For public skills, official or well-known sources such as `vercel-labs`, `anthropic`, and `microsoft` are more trustworthy.
- Relevance: Make sure the skill actually matches what the user needs, not just keyword overlap.

Read `references/search-and-evaluation.md` when judging quality or relevance. For package inspection, open the `skills.sh` or public GitHub link when available.

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

## Manual Fallback

If the helper script cannot run, call the skills CLI directly:

```bash
npx -y skills@latest find resume generator --source external -y
```

When no relevant skills are found, say what searches were tried, suggest alternate keywords, and offer to help directly or create a new skill.

## Publishing Reference

Read `references/github-publishing.md` when the user asks how to publish, package, or install this skill from a GitHub repository.
