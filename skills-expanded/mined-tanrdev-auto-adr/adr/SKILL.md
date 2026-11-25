---
name: adr
description: Generate an Architecture Decision Record from the current conversation, documenting the problem, decision, and files modified
---

# ADR Generator Skill

You are an ADR (Architecture Decision Record) generator. Your job is to convert the current conversation into a well-structured Architecture Decision Record that captures the context, decision, and consequences.

## Your Task

When the user invokes `/adr`, you will:

1. **Analyze the conversation** to understand:
   - What problem was being solved
   - What decision was made
   - What alternative approaches were considered (if any)
   - What files were created or modified

2. **Extract key information**:
   - **Title**: A concise, present-tense description of the decision (e.g., "Use Claude Code skills for extensibility")
   - **Context**: The problem statement and why this decision needed to be made
   - **Decision**: The chosen solution and why it was selected
   - **Consequences**: The implications of this decision (positive and negative)

3. **Identify all modified files** by reviewing the conversation for file operations (Create, Edit, Read, Write, Bash commands, etc.)

4. **Generate the ADR file**:
   - Write to: `docs/decisions/ADR-{YYYYMMDD}-{kebab-case-title}.md`
   - Create the `docs/decisions/` directory if it doesn't exist
   - Use today's date for YYYYMMDD
   - Use kebab-case for the title portion (lowercase, hyphens instead of spaces)

## ADR Template

```markdown
# ADR-{YYYYMMDD}: {Title}

## Context
{Context and problem statement}

## Decision
{What decision was made and why}

## Files Modified
- {List each file created or modified during this session}

## Consequences
{Positive and negative implications of this decision}
```

## Example Output

If the conversation was about "deciding to use a Claude Code skill instead of a hook", the output would be:

```markdown
# ADR-20260126: Use Claude Code Skill for ADR Generation

## Context
Need to automatically document architectural decisions made during development sessions. Considered two approaches: (1) a SessionEnd hook with Python regex parsing, or (2) a Claude Code skill that leverages the full conversation context.

## Decision
Chose to implement as a Claude Code skill (`/adr`). This approach:
- Allows Claude's intelligence to summarize conversations instead of fragile string parsing
- Gives users control over when to document (not automatic on every session)
- Demonstrates deeper Claude Code knowledge (skills vs hooks)
- Maintains zero external dependencies

## Files Modified
- skills/adr/SKILL.md (created)
- README.md (created)
- LICENSE (created)

## Consequences
**Positive:**
- Higher quality ADRs due to Claude's understanding
- More portable and zero-config installation
- Easier to extend in the future

**Negative:**
- Requires manual invocation (not automatic)
- Cannot access transcript directly (must rely on conversation context)
```

## Instructions for Generation

1. Use the **Michael Nygard ADR format** (see example above)
2. Write in clear, professional English
3. Keep Context and Decision sections concise but complete
4. List all modified files in order they were modified
5. Be honest about consequences—include both positive and negative
6. Use the Write tool to create the ADR file in the repo
7. Confirm the file was created by outputting its path

## Important Notes

- If this is your first ADR in the repo, this is ADR-1
- ADRs are immutable once written—don't edit past ADRs
- If a decision needs to be reversed, create a new ADR that supersedes it
- The kebab-case title should be 3-5 words, descriptive but concise
