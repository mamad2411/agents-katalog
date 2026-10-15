---
name: keep-learning
description: "Learn and memorize knowledge from local directories. Supports Markdown and code files. Extracts key insights, builds knowledge index, and stores in agent memory. Trigger with '持续学习知识' or 'keep learning'."
license: MIT-0
compatibility: "Requires local filesystem access and git (optional, for auto-pull)."
metadata:
  author: nileader
  version: "0.0.1"
  repository: https://github.com/nileader/keep-learning
---

# Keep Learning

Learn knowledge from local directories and store it in agent memory for future reference.

## When to Use This Skill

Activate this skill when user says:
- "持续学习知识"
- "keep learning"
- "learn knowledge base"
- "学习知识库"

## Supported File Formats (v0.0.1)

| Format | Extensions | Support |
|--------|------------|---------|
| Markdown | .md, .markdown | Full |
| Python | .py | Full |
| JavaScript/TypeScript | .js, .ts, .jsx, .tsx | Full |
| Java | .java | Full |
| Go | .go | Full |
| Rust | .rs | Full |
| C/C++ | .c, .cpp, .h, .hpp | Full |
| Shell | .sh, .bash, .zsh | Full |
| YAML/JSON/TOML | .yaml, .yml, .json, .toml | Full |
| SQL | .sql | Full |
| Other text | .txt, .csv | Full |

Not supported in v0.0.1: PDF, Word, Excel, PowerPoint, Keynote, audio, video files.

## Three-Layer Knowledge Architecture

| Layer | Storage | Content | Purpose |
|-------|---------|---------|---------|
| L1 Core Memory | Agent Memory | Key conclusions, core concepts, decisions | Auto-surface in daily conversations |
| L2 Knowledge Index | Agent Memory | File paths, summaries, keyword mappings | Know where knowledge lives |
| L3 Source Files | Local filesystem | Complete original content | Deep-dive when needed via read_file |

How It Works:
1. Daily conversations: L1 memories automatically appear in memory_overview
2. Need more detail: Query L2 index to find relevant files
3. Deep investigation: Use read_file to access L3 source files

## Runtime Data Directory

All runtime data is stored in ~/.keep-learning/:

| File | Purpose |
|------|---------|
| last-commit | Git commit hash of last learning session |
| config.json | User configuration (knowledge base path, etc.) |

## Learning Workflow

### Step 1: Get Configuration

First time users must specify knowledge base path (e.g., ~/knowledge/work-assistant).
Store configuration in memory using update_memory with category project_environment_configuration.
For returning users, retrieve config from memory first.

### Step 2: Git Pull (If Applicable)

Check if knowledge base is a git repository and pull latest changes before learning.

### Step 3: Scan Files

Scan for supported files. Exclude: .git, node_modules, .obsidian, __pycache__, .venv

### Step 4: Detect Changes (Incremental Learning)

If git repository, use git diff to find changed files since last learning.
Store last commit hash in ~/.keep-learning/last-commit

### Step 5: Read and Extract Knowledge

For each file: read content, identify theme/concepts/conclusions, extract key knowledge.

### Step 6: Store L1 Core Memory

Create L1 memory entries using update_memory with appropriate category:
- expert_experience: Domain expertise, best practices
- project_introduction: Project/product overviews
- learned_skill_experience: Reusable methods, procedures

Title format: [Domain] Concise Topic Description

### Step 7: Build L2 Knowledge Index

Create knowledge index with file path, theme, keywords mappings.

### Step 8: Generate Learning Report

Output: Timestamp, Statistics, L1 Memories list, L2 Index summary, Notes.

## Memory Deduplication

Before creating: search_memory first. If exists, update; if not, create.

## Quick Reference

| Situation | Action |
|-----------|--------|
| First time user | Ask for knowledge base path |
| Git repo detected | Run git pull before scanning |
| Large file | Read in chunks, summarize each section |
| Duplicate knowledge | Update existing memory |
| Unsupported file | Skip and note in report |

## Limitations (v0.0.1)

- Only Markdown and code files supported
- No PDF/Word/Excel/PPT support
- Memory entries have size limits
