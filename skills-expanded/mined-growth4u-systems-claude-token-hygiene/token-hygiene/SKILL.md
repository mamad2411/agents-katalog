---
name: token-hygiene
description: >
  Audits Claude Code system token overhead (CLAUDE.md, MEMORY.md, skills, MCP servers,
  daily logs) and generates a report with cleanup recommendations. Use monthly or when
  sessions feel slow. Trigger: "token hygiene", "context audit", "audit tokens".
---

# Token Hygiene — Context Overhead Audit

> Monthly audit of system files that inflate every Claude Code conversation's token cost. Reports metrics, flags issues, and recommends actions. Does NOT modify files automatically.

## Why This Matters

Every Claude Code conversation loads your system context before you type anything:

| Source | What it is | Typical size |
|--------|-----------|-------------|
| CLAUDE.md | Project instructions | 2,000-10,000 tokens |
| MEMORY.md | Auto-memory (if enabled) | 1,000-6,000 tokens |
| Skill descriptions | One line per installed skill | 50-80 tokens each |
| MCP tool listings | Every registered tool | ~15 tokens each |
| Hooks & plugins | System reminders | 500-2,500 tokens |

A typical setup can burn **15,000-35,000 tokens per conversation** just on system context — before you ask a single question. This skill measures that overhead and tells you where to cut.

## Thresholds

| Check | What it measures | Green | Yellow | Red |
|-------|-----------------|-------|--------|-----|
| CLAUDE.md size | Bytes of project instructions | <10KB | 10-20KB | >20KB |
| MEMORY.md lines | Lines in auto-memory file | <150 | 150-200 | >200 |
| Skills count | Folders in ~/.claude/skills/ | <80 | 80-100 | >100 |
| MCP servers | Servers in .mcp.json | <=5 | 6-7 | >7 |
| Stale daily logs | memory/*.md files older than 30 days | 0-5 | 6-15 | >15 |

## Workflow

### Step 1: Measure All Sources

```bash
# CLAUDE.md
wc -l CLAUDE.md && wc -c CLAUDE.md

# MEMORY.md (auto-memory location varies by project)
wc -l ~/.claude/projects/*/memory/MEMORY.md
wc -c ~/.claude/projects/*/memory/MEMORY.md

# Skills count
ls -d ~/.claude/skills/*/ 2>/dev/null | wc -l

# MCP servers
grep -c '"command"' .mcp.json 2>/dev/null

# Stale daily logs (if you use daily memory logs)
find memory/ -name "20*.md" -mtime +30 2>/dev/null | wc -l
```

### Step 2: Estimate Token Impact

| Source | Formula |
|--------|---------|
| CLAUDE.md | bytes × 0.28 |
| MEMORY.md | bytes × 0.33 |
| Skills | count × 65 |
| MCP tools | servers × avg_tools × 15 |

### Step 3: Identify Issues

For each metric in Yellow or Red:

**CLAUDE.md too large:**
- Look for reference sections (tables, examples, long command lists)
- Move them to a separate file and add a one-line pointer
- Remove stale content (tools you've uninstalled, old client lists)

**MEMORY.md too large:**
- Extract detailed content into topic files (e.g., `memory/client-details.md`)
- Keep only operational rules and pointers in MEMORY.md
- Remove entries older than 2 months that aren't actively referenced

**Too many skills:**
- Check for duplicates (same skill from different sources)
- Uninstall skills you haven't used in 30+ days
- Each removed skill saves ~65 tokens per conversation

**Too many MCP servers:**
- Remove servers with expired credentials
- Disable servers you use rarely (re-enable when needed)
- Check for duplicates (e.g., plugin playwright + project playwright)

### Step 4: Generate Report

The report uses a traffic-light dashboard:

```markdown
# Token Hygiene Report — [DATE]

## Dashboard

| Metric | Value | Status | Tokens Est. |
|--------|-------|--------|-------------|
| CLAUDE.md | X lines / Y KB | [status] | ~N tokens |
| MEMORY.md | X lines / Y KB | [status] | ~N tokens |
| Skills installed | X | [status] | ~N tokens |
| MCP servers | X | [status] | ~N tokens |
| Stale logs | X files | [status] | — |
| **Total overhead** | | | **~N tokens** |

## Issues Found
[Details per issue with recommended action and estimated savings]

## Recommended Actions (Priority Order)
1. [Action] — saves ~N tokens
2. [Action] — saves ~N tokens
```

### Step 5: Track Progress

Save results to compare month-over-month:

```json
{
  "last_audit": "2026-03-05",
  "metrics": {
    "claude_md_bytes": 5669,
    "memory_md_lines": 90,
    "skills_count": 82,
    "mcp_servers": 5,
    "stale_logs": 0,
    "estimated_overhead_tokens": 17000
  }
}
```

## Common Wins

Based on real-world optimization (40-50% reduction achieved):

| Action | Typical Savings | Effort |
|--------|----------------|--------|
| Move CLAUDE.md reference sections to separate file | 3,000-6,000 tokens | 30 min |
| Compress MEMORY.md, extract to topic files | 2,000-4,000 tokens | 20 min |
| Remove duplicate skills | 200-500 tokens | 5 min |
| Remove unused MCP servers | 500-2,500 tokens | 5 min |
| Disable cloud MCP integrations (Supabase, etc.) | 500-1,500 tokens | 2 min |
| Archive old daily logs | Reduces file scan time | 5 min |

## Notes

- This skill is **read-only**. It never modifies files automatically.
- You review the report and decide which actions to take.
- Run monthly, or whenever conversations feel slower than usual.
