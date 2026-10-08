---
name: auto-shard
version: 1.0.0
description: |
  Automatically shard large CLAUDE.md files into smaller, organized shards.
  Detects files >40KB, identifies logical sections, classifies by criticality,
  creates shards in appropriate locations (rules/ or docs/), and validates integrity.
  Use when working with large documentation files or when Claude Code warns about context size.
author: Claude-Code
argument-hint: <operation> [file_path] [options]
---

# Auto-Shard Skill

> **Version**: 1.0.0 | **Author**: Claude-Code | **Created**: 2026-01-25

## Purpose

Automatically shard large documentation files (especially CLAUDE.md) into smaller, organized components following the Claude Code context architecture.

## When to Use

1. **Proactive**: When a file exceeds 40KB
2. **Reactive**: When Claude Code warns about context size
3. **Manual**: When you want to reorganize documentation
4. **Hook-triggered**: Automatically via `detect-large-file.sh` PreToolUse hook

## Usage

```bash
/auto-shard <operation> [file_path] [options]
```

## Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `analyze` | Identify sections and structure | `/auto-shard analyze ~/.claude/CLAUDE.md` |
| `classify` | Classify sections by criticality | `/auto-shard classify ~/.claude/CLAUDE.md` |
| `generate` | Create shard files | `/auto-shard generate ~/.claude/CLAUDE.md` |
| `update-refs` | Update cross-references | `/auto-shard update-refs ~/.claude/CLAUDE.md` |
| `validate` | Verify integrity | `/auto-shard validate ~/.claude/` |
| `full` | Run complete pipeline | `/auto-shard full ~/.claude/CLAUDE.md` |
| `status` | Show sharding status | `/auto-shard status ~/.claude/` |

## Routing Logic

```
┌─────────────────────────────────────────────────────────────────────┐
│  AUTO-SHARD ROUTER                                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  /auto-shard analyze <path>                                         │
│      └── Load: operations/analyze.md                                │
│          └── Output: Section map with line counts                   │
│                                                                     │
│  /auto-shard classify <path>                                        │
│      └── Load: operations/classify.md                               │
│          └── Output: Criticality classification per section         │
│                                                                     │
│  /auto-shard generate <path> [--dry-run]                            │
│      └── Load: operations/generate.md                               │
│          └── Output: Shard files in rules/ or docs/                 │
│                                                                     │
│  /auto-shard update-refs <path>                                     │
│      └── Load: operations/update-refs.md                            │
│          └── Output: Updated links in main file                     │
│                                                                     │
│  /auto-shard validate <path>                                        │
│      └── Load: operations/validate.md                               │
│          └── Output: Integrity report (SHA256 + links)              │
│                                                                     │
│  /auto-shard full <path> [--dry-run]                                │
│      └── Pipeline: analyze → classify → generate → update-refs      │
│          └── Recursive: Up to 3 levels if shards > 20KB             │
│                                                                     │
│  /auto-shard status <path>                                          │
│      └── Show: File sizes, shard count, integrity status            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture

```
~/.claude/commands/auto-shard/
├── SKILL.md                 # This file (router)
├── operations/
│   ├── analyze.md           # ShardAnalyzer
│   ├── classify.md          # CriticalityClassifier
│   ├── generate.md          # ShardGenerator
│   ├── update-refs.md       # ReferenceUpdater
│   ├── validate.md          # IntegrityValidator
│   └── recursive.md         # RecursiveProcessor
└── scripts/
    └── detect-large-file.sh # PreToolUse hook detector
```

## Criticality Levels

| Level | Criteria | Destination | Auto-Load |
|-------|----------|-------------|-----------|
| **CRITICAL** | Core directives, must-follow rules | `rules/` | YES |
| **HIGH** | Important but can be on-demand | `docs/` (top) | NO |
| **MEDIUM** | Reference material | `docs/` (nested) | NO |
| **LOW** | Historical, examples, verbose | `docs/archive/` | NO |

## Size Thresholds

| Threshold | Action |
|-----------|--------|
| < 20KB | No action needed |
| 20-40KB | Optional sharding (suggest) |
| 40-80KB | Recommended sharding (warn) |
| > 80KB | Mandatory sharding (block) |

## Output Structure

After sharding `~/.claude/CLAUDE.md`:

```
~/.claude/
├── CLAUDE.md                    # Reduced (links to shards)
├── rules/
│   ├── core-directive.md        # CRITICAL
│   ├── main-instructions.md     # CRITICAL
│   └── pr-review-protocol.md    # CRITICAL
└── docs/
    ├── git-worktree-protocol.md # HIGH
    ├── session-report-standard.md # HIGH
    └── archive/
        └── changelog-2025.md    # LOW
```

## Integration with Hook

The `detect-large-file.sh` hook triggers this skill automatically:

```bash
# Hook detects large file on Read/Write
# Emits JSON-RPC suggestion to stderr
# Claude Code sees suggestion and can invoke:
/auto-shard full ~/.claude/CLAUDE.md
```

## Examples

### Analyze a file

```bash
/auto-shard analyze ~/.claude/CLAUDE.md
```

Output:
```
## Section Analysis

| Section | Lines | Size | Heading Level |
|---------|-------|------|---------------|
| [C01] Core Directive | 45 | 2.1KB | H2 |
| [C02] Main Instructions | 120 | 5.8KB | H2 |
| ... | ... | ... | ... |

Total: 1,847 lines, 55KB
Recommended action: SHARD (>40KB threshold)
```

### Full pipeline with dry-run

```bash
/auto-shard full ~/.claude/CLAUDE.md --dry-run
```

Output:
```
## Dry-Run: Would create 8 shards

| Shard | Destination | Size | Criticality |
|-------|-------------|------|-------------|
| core-directive.md | rules/ | 2.1KB | CRITICAL |
| main-instructions.md | rules/ | 5.8KB | CRITICAL |
| ...

Main file would reduce from 55KB to 12KB
No files modified (dry-run mode)
```

### Validate integrity

```bash
/auto-shard validate ~/.claude/
```

Output:
```
## Integrity Report

| File | SHA256 | Links Valid | Status |
|------|--------|-------------|--------|
| CLAUDE.md | abc123... | 8/8 | OK |
| rules/core-directive.md | def456... | 2/2 | OK |
| ...

All 12 files validated. No broken links.
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Circular reference detected | Abort, report cycle |
| Shard destination conflict | Prompt for rename |
| Link target not found | Create stub or warn |
| SHA256 mismatch | Report drift, suggest resync |

## Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would happen without changes |
| `--force` | Override size thresholds |
| `--recursive` | Enable recursive sharding (default: 3 levels) |
| `--no-backup` | Skip backup creation |
| `--json` | Output in JSON format |

---

## Instructions for Claude

When this skill is invoked:

1. **Parse the operation** from arguments
2. **Load the appropriate operation file** from `operations/`
3. **Execute the operation** following its specific instructions
4. **Return structured output** (table format preferred)
5. **Suggest next action** if pipeline is incomplete

### On `/auto-shard full`:

Execute in sequence:
1. `analyze` - Build section map
2. `classify` - Assign criticality
3. `generate` - Create shards (with backup)
4. `update-refs` - Fix cross-references
5. `validate` - Verify integrity
6. (If any shard > 20KB) `recursive` - Re-shard large shards

### On errors:

- Emit JSON-RPC error to stderr
- Provide actionable recovery instructions
- Never leave partial state (rollback on failure)

---

*Skill: auto-shard v1.0.0 | Author: Claude-Code | 2026-01-25*
