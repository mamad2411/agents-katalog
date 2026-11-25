---
name: codestyle
description: |
  Code template search and generation tool. Auto-initializes on first use.
  
  Use when:
  1. search/get - user needs code templates, "检索模板", "search template"
  2. generate - user wants to create template from code/file/repo/url, "生成模板"
  3. upload - user has prepared template files, "上传模板"
  
  Requirements: JDK 17+, Git (for first-time setup)
---

# Codestyle

Code template management: CLI tools for search/get/upload + AI-guided generation.

## Decision Tree

```
User request
    │
    ├─ "search" / "检索" ──→ Search Workflow (CLI, local+remote)
    │
    ├─ "get" / "获取" ──→ Get Workflow (CLI, local+remote)
    │
    ├─ "generate" / "生成" ──→ Generate Workflow (AI dialog, then upload)
    │
    └─ "upload" / "上传" ──→ Upload Workflow (CLI, remote)
```

## Commands

| Command | Execution | Description |
|---------|-----------|-------------|
| `search` | CLI (JAR) | Search templates (local Lucene + remote API) |
| `get` | CLI (JAR) | Get full template content |
| `generate` | AI Dialog | Multi-turn conversation, then call upload |
| `upload` | CLI (JAR) | Upload template to server |

## Quick Start

### Windows

```bash
"<SKILL_DIR>\scripts\codestyle.bat" search "keyword"
"<SKILL_DIR>\scripts\codestyle.bat" get "template-path"
"<SKILL_DIR>\scripts\codestyle.bat" upload --path ./my-template
```

### Linux/macOS

```bash
bash <SKILL_DIR>/scripts/codestyle search "keyword"
bash <SKILL_DIR>/scripts/codestyle get "template-path"
bash <SKILL_DIR>/scripts/codestyle upload --path ./my-template
```

### Generate (AI Dialog)

```
User: 把这段代码做成模板：[代码]
AI: [多轮对话引导生成模板]
AI: [调用 upload 存储]
```

## Workflows

See references/ for detailed workflow instructions:

- **[Search Workflow](references/search-workflow.md)** - Find templates (local+remote)
- **[Get Workflow](references/get-workflow.md)** - Retrieve template content by full path
- **[Generate Workflow](references/generate-workflow.md)** - AI-guided template creation
- **[Upload Workflow](references/upload-workflow.md)** - Submit templates (remote)

### Generate Workflow Overview

Generate workflow is **pure AI dialog**, no script calls until final upload.

| Input | Example | Pre-processing |
|-------|---------|----------------|
| Code snippet | `@RestController ...` | None |
| Current file | "当前这个文件" | Read file |
| Local path | `/path/to/file.java` | Read file |
| GitHub URL | `https://github.com/xxx/repo` | Clone repo |
| Web URL | `https://blog.xxx.com/...` | Crawl content |

Process: `识别输入 → 预处理 → 分析结构 → 选择模板 → AI生成 → 去重检测 → 用户确认 → 调用upload`

## First-Time Use

Automatic initialization on first command:

1. Detect no `.initialized` marker
2. Download JAR file (if needed)
3. Clone template repository
4. Create `.initialized` marker
5. Execute original command

## Configuration

See [references/config.md](references/config.md) for configuration options.

## Template Format

### Directory Structure

Standard template structure with **meta.json in version directory**:

```
<artifactId>/
└── <version>/
    ├── meta.json          # Template metadata (required)
    ├── README.md          # Documentation (optional)
    └── <subdirectories>   # Template files (.ftl)
```

Example:

```
CRUD/
└── 1.0.0/
    ├── meta.json
    ├── README.md
    ├── backend/
    │   ├── sql/Menu.ftl
    │   └── src/main/java/...
    └── frontend/
        └── src/...
```

See [references/template-format.md](references/template-format.md) for complete format specification.

See [references/template-syntax.md](references/template-syntax.md) for template syntax.

## Requirements

- JDK 17+
- Git 2.0+ (for first-time setup and repo cloning)
- Internet connection (for remote API calls)
