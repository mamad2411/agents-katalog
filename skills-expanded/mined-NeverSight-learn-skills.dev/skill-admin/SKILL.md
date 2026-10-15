---
name: skill-admin
description: Manage skills across 20+ AI platforms (Claude Code, Cursor, Copilot, Gemini, OpenClaw, Hermes, etc.). Includes a zero-dependency web UI (`web` command) for visual skill CRUD. Default behavior is listing skills only; only guide/recommend when the user explicitly asks what skill to use.
---

# Skill Admin

Manage skills across **20+ AI platforms** with single source of truth architecture.

## Supported Platforms

`claude` `cursor` `copilot` `vscode` `cline` `roo` `goose` `codex` `windsurf` `trae` `kiro` `opencode` `openclaw` `hermes` `qoder` `qoderwork` `gemini` `antigravity` `agents`

## CLI Commands

```bash
# Web UI (zero-dependency, runs in background)
python3 skill-admin.py web          # Start on port 8080
python3 skill-admin.py web 9000     # Custom port
python3 skill-admin.py web-stop     # Stop background server

# Unified list / scan
python3 skill-admin.py list [platform]

# Backward-compatible alias
python3 skill-admin.py scan

# Sync all to .agents + symlink others
python3 skill-admin.py sync-all

# Delete skill from all platforms
python3 skill-admin.py delete <name>

# Generate category graph
python3 skill-admin.py graph [platform]

# Install from GitHub
python3 skill-admin.py install <url> [platform]

# Compare two platforms
python3 skill-admin.py compare <p1> <p2>

# Show symlink topology
python3 skill-admin.py topology

# Security scan (11 dimensions)
python3 skill-admin.py security [path]

# Backup all skills
python3 skill-admin.py backup
```

## AI Output Templates

**CRITICAL**: After running CLI, format output using templates below. Do NOT dump raw script output.

## Guide Flow

Default:
1. Run `python3 skill-admin.py list [platform]`
2. List installed skills

Only when the user explicitly asks what skill to use:
1. Run `python3 skill-admin.py list [platform]`
2. Use only each skill's `name` and `description` to identify relevant skills
3. Explain what the relevant skills do and why they fit the current task
4. Do not read full skill bodies unless the user explicitly asks

## List Output Contract

`list` outputs stable structured text for AI consumption:

- `SKILL_LIST_BEGIN`
- `SUMMARY ...`
- `PLATFORM ...`
- `SKILL ...`
- `EMPTY_DIR ...` if any
- `SKILL_LIST_END`

Parsing rules:
- Fields are tab-separated
- Each field is `key=value`
- Use `SKILL.name` and `SKILL.description` for guide/recommendation
- Do not depend on colors or box-drawing characters

### Template 1: Summary (for "how many skills")

| 统计项 | 数量 |
|--------|------|
| 总技能数 | XXX |
| 已安装平台 | XXX |
| 去重后唯一技能 | XXX |

### Template 2: Full Skill List (for "list all skills")

| 分类 | 数量 | 技能列表 |
|:-----|-----:|:---------|
| 💻 **开发工具** | XX | `skill-a` `skill-b` ... |
| 🎨 **设计工具** | XX | `skill-a` `skill-b` ... |
| 📚 **文档工具** | XX | `skill-a` `skill-b` ... |
| 🌐 **网络交互** | XX | `skill-a` `skill-b` ... |
| 🤖 **AI 能力** | XX | `skill-a` `skill-b` ... |
| ⚙️ **系统自动化** | XX | `skill-a` `skill-b` ... |
| 🧪 **测试质量** | XX | `skill-a` `skill-b` ... |
| 📊 **数据分析** | XX | `skill-a` `skill-b` ... |
| 📦 **其他** | XX | `skill-a` `skill-b` ... |
| **总计** | **XXX** | |

**List ALL skills, NO truncation.**

### Classification Rules

| 类别 | 关键词 |
|------|--------|
| 💻 开发工具 | code, dev, debug, test, tdd, review, git, typescript, react, rax, fliggy, ship, ultron, clamjs |
| 🎨 设计工具 | design, ui, ux, figma, mobile, ios, web-design, generative, canvas, infographic, drafter |
| 📚 文档工具 | doc, pdf, docx, pptx, xlsx, obsidian, notebook, writing, guide, release |
| 🌐 网络交互 | web, browse, browser, gstack, opencli, fetch, search, screenshot, websearch, webfetch |
| 🤖 AI 能力 | ai, llm, claude, gemini, agent, pua, superpowers, brainstorm, plan, office-hours |
| ⚙️ 系统自动化 | freeze, guard, sync, backup, file, organizer, loop, scheduler, health |
| 🧪 测试质量 | qa, test, quality, verify, doctor, investigate, security |
| 📊 数据分析 | data, odps, query, rum, analytics, yfinance, stock, finance, correlation |

## Security Scan

11 dimensions: Prompt Injection, Permission Abuse, Hook Behavior, Data Exfiltration, Social Engineering, Scope Creep, Obfuscation, Destructive Ops, Supply Chain, Identity Impersonation, Sensitive Data.

| Score | Label | Action |
|-------|-------|--------|
| 85-100 | TRUSTED | APPROVE |
| 70-84 | LIKELY_SAFE | APPROVE_WITH_CAUTION |
| 50-69 | SUSPICIOUS | APPROVE_WITH_CAUTION |
| 25-49 | HIGH_RISK | REJECT |
| 0-24 | DANGEROUS | REJECT |

Edit `scripts/security-rules.yaml` to customize rules.

## Requirements

Python 3.8+, stdlib only (no dependencies).
