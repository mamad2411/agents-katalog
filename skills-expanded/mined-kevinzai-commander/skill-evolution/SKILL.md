---
name: skill-evolution
description: "Self-evolving skills — analyzes session corrections, error patterns, and successful approaches to automatically propose improvements to SKILL.md files. Use when the user says 'evolve skills', 'improve skills from history', 'what have we learned'."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Skill Evolution — Self-Improving Skills

Analyzes CC Commander's knowledge base and session history to propose concrete improvements to SKILL.md files.

## How It Works

1. **Scan knowledge base** — Read ~/.claude/commander/knowledge/*.json for patterns
2. **Identify corrections** — Find sessions where approach A failed but approach B succeeded
3. **Match to skills** — Map error/success patterns to relevant SKILL.md files
4. **Propose changes** — Generate specific edits (add gotchas, update examples, flag anti-patterns)
5. **User approval** — Present changes via AskUserQuestion before applying

## Trigger Conditions

Run skill evolution when:
- Knowledge base has 10+ lessons
- A skill was involved in 3+ failed sessions
- A new pattern was discovered that contradicts skill guidance

## Process

### Step 1: Analyze Knowledge Base

```bash
# Read all lessons
ls ~/.claude/commander/knowledge/*.json | wc -l
```

For each lesson with outcome "error":
- Extract the error pattern
- Identify which skill category it falls into
- Check if the relevant SKILL.md already warns about this

### Step 2: Generate Proposals

For each skill with improvement opportunities:

Use AskUserQuestion:
```
Skill: {skill-name}
Based on {N} sessions, I found:
- {pattern}: happened {count} times
- Current SKILL.md does NOT warn about this

Proposed addition to SKILL.md:
## Known Gotchas
- {description of the gotcha}
- Workaround: {what worked}

Apply this improvement?
❯ Yes, update the skill
  Show me the full diff first
  Skip this one
```

### Step 3: Apply and Log

After user approval:
1. Edit the SKILL.md file
2. Log the evolution to ~/.claude/commander/knowledge/ with category "skill-evolution"
3. Report what was changed

## Safety

- NEVER modify skills without user approval
- Only ADD content (gotchas, examples, warnings) — never remove
- Keep a log of all evolutions in ~/.claude/commander/skill-evolution-log.json
- Maximum 5 proposals per run (don't overwhelm)

## Example Output

```
Skill Evolution Report:
━━━━━━━━━━━━━━━━━━━━━

Analyzed: 47 lessons across 12 categories
Proposals: 3 improvements

1. skills/ccc-saas/auth-patterns/SKILL.md
   + Added: "next-auth conflicts with custom Prisma adapters" to Gotchas
   Evidence: 2 failed sessions, 1 workaround found

2. skills/frontend-patterns/SKILL.md
   + Added: "middleware.ts matcher needs exact paths, not wildcards" to Tips
   Evidence: 3 sessions hit this issue

3. skills/ccc-testing/SKILL.md
   + Added: "Mock database tests can mask real migration failures" to Anti-Patterns
   Evidence: 1 production incident traced to mocked tests

Applied: 3/3 (user approved all)
```
