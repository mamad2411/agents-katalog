---
name: team-brain-onboard
description: "Generate onboarding context for new team members from team brain knowledge. Use when user says 'onboard', 'onboarding', 'new developer', 'getting started', or '/team-brain onboard'."
allowed-tools: Bash, Read, Grep
---

# Team Brain Onboard

Generate a comprehensive onboarding document from all team brain entries.

## Process

1. First, find the project root and read all entries:
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/store.js" list
```

2. Read individual entries that seem most important (conventions first, then decisions, then lessons):
```bash
node "${CLAUDE_SKILL_DIR}/../../scripts/store.js" list "" conventions
node "${CLAUDE_SKILL_DIR}/../../scripts/store.js" list "" decisions
node "${CLAUDE_SKILL_DIR}/../../scripts/store.js" list "" lessons
node "${CLAUDE_SKILL_DIR}/../../scripts/store.js" list "" knowledge
```

3. Read the full content of key entries using the Read tool on their file paths.

4. Generate a structured onboarding document with these sections:

### Output Format

```markdown
# Onboarding Guide
> Auto-generated from Team Brain on DATE

## Project Overview
[Synthesized from knowledge entries]

## Coding Conventions
[All active conventions, clearly stated]

## Architecture Decisions
[Key decisions with brief context on WHY]

## Lessons Learned
[Important gotchas and insights the team has discovered]

## Key Things to Know
[Anything else a new developer should know on day 1]

## Contributors
[Who to ask about what, based on contributor data]
```

5. Keep the document practical and actionable — new devs should be able to read this in 10 minutes and understand the project's norms.
