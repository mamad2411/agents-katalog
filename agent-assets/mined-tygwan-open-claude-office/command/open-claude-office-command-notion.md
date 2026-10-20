---
description: "Bidirectional Notion sync. Subcommands: sync, push, pull, status, diff, init."
---

# /notion -- Notion Bidirectional Sync

Notion MCP를 통한 프로젝트 데이터 양방향 동기화.

## Usage

```
/notion <subcommand> [options]
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `init [--db-only\|--migrate]` | 초기 설정 — DB 8개 생성, 관계 설정, 마이그레이션 |
| `sync` | 양방향 전체 동기화 |
| `push [--project P] [--tasks-only] [--docs-only]` | 로컬 → Notion |
| `pull [--project P] [--changes-only]` | Notion → 로컬 캐시 |
| `status` | 동기화 상태 확인 |
| `diff` | 로컬 vs Notion 차이점 |

## Pre-requisites

1. Notion MCP configured in Claude Code
2. Notion workspace with write permissions
3. `/notion init` executed at least once (or database IDs in settings.json)

## Quick Start

```bash
/notion init          # First time setup — creates 8 DBs
/notion status        # Check connection and sync state
/notion sync          # Full bidirectional sync
```

## Skill Reference

Full documentation: `.claude/skills/notion/SKILL.md`
Architecture reference: `docs/archive/NOTION-SYNC-ARCHITECTURE.md`
