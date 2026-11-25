---
name: prompt-hygiene-audit
description: Weekly audit — your config files vs Claude best practices, skill extraction candidates. EXAMPLE.
---

# Prompt Hygiene Audit (example)

> **EXAMPLE.** Meta-skill: audits your OWN slash commands and memory files for drift from prompt-engineering best practices.

Spawn a Sonnet sub-agent if `[cron ...]` suffix present.

## Procedure

### STEP 1 — Fetch latest best practices

```
WebFetch: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
Prompt: "Extract the concrete rules for prompt engineering — anti-patterns, techniques, and prompt-structure recommendations. Concise list only."
```

### STEP 2 — Read all your config files

```bash
for f in SOUL.md IDENTITY.md USER.md MEMORY.md HEARTBEAT.md AGENTS.md TOOLS.md; do
  cat "$NOLTY_HOME/$f" 2>/dev/null
done

ls ~/.claude/commands/*.md   # your slash commands
```

### STEP 3 — Compare

Look for:
- **Anti-patterns** Claude docs recommend against — vague role descriptions, missing examples, ambiguous instructions
- **Missing techniques** — XML tags for structure, chain-of-thought prompts, explicit output format specs
- **Unclear wording** — phrases that could be interpreted multiple ways
- **Skill extraction candidates** — procedures repeated across multiple files that should be extracted to a shared skill file

### STEP 4 — Write report

Save to `memory/prompt-audit-YYYY-MM-DD.md`:

```markdown
# Prompt Hygiene Audit — [date]

## Top Findings
1. [finding] — where it lives — suggested fix
2. ...

## Skill Extraction Candidates
- [procedure] currently inline in [files] — extract to `skills/<name>/SKILL.md`

## Wins (things already done well)
- ...
```

Skip anything that's already fine — only flag changes worth making.

### STEP 5 — Telegram top 3 findings

```
🧹 *Prompt Audit — [date]*
1. [top finding]
2. [second finding]
3. [third finding]

Full report: memory/prompt-audit-[date].md
```

`reply` MCP with `chat_id` from `USER.md`. End with `AUDIT_OK <timestamp>`.

### On failure

If WebFetch fails to pull the best-practices doc, audit against known patterns from MEMORY.md and past audits. Don't exit silently — always produce a report, even if shorter.
