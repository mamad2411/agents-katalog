---
name: project-onboard
description: Analyze any project directory and generate AGENTS.md for AI context. Use when the user asks to "onboard", "analyze this project", "understand this project", "generate AGENTS.md", or provides a project path they want to understand. Supports auto-detection of Unity, Unreal, Node.js, Python, Rust, Go, Java, C/C++, C#, Lua, and general projects.
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Project Onboard

Turn any project directory into an AGENTS.md that gives the AI agent instant project context. Auto-detects project type and applies type-specific analysis rules. Zero external dependencies — uses only built-in tools.

## When This Skill Triggers

- "onboard this project"
- "analyze my project"
- "help me understand this project"
- "generate AGENTS.md for this project"
- "what does this project do?"
- User provides a project path without context

## Parameters

- **path** (required): Project directory path
- **type** (optional): Force project type, skip auto-detection. Values: `unity`, `unreal`, `nodejs`, `python`, `rust`, `go`, `java`, `cpp`, `csharp`, `lua`, `general`
- **output** (optional): Where to save AGENTS.md. Default: `<project_root>/AGENTS.md`

## Execution Flow

### Step 1: Confirm the Target

If no path given, ask the user which project to analyze. If path is relative, resolve to absolute. Confirm with user before proceeding.

### Step 2: Quick Scan for Project Type (if --type not specified)

Use `glob` to look for 50-100 top-level entries. Match against the detection table:

| Signature | Type | Rule Pack |
|---|---|---|
| `Assets/` + `ProjectSettings/` | unity | `references/unity.md` |
| `Source/` + `.uproject` | unreal | `references/unreal.md` |
| `package.json` without `Assets/` | nodejs | `references/nodejs.md` |
| `pyproject.toml` or `requirements.txt` or `setup.py` | python | `references/python.md` |
| `Cargo.toml` | rust | `references/rust.md` |
| `go.mod` | go | `references/go.md` |
| `pom.xml` or `build.gradle` | java | `references/java.md` |
| `CMakeLists.txt` | cpp | `references/cpp.md` |
| `*.csproj` or `*.sln` without `Assets/` | csharp | `references/csharp.md` |
| `*.rockspec` or `lua_modules/` or `.luacheckrc` | lua | `references/lua.md` |
| `Dockerfile` + `docker-compose.yml` | docker | `references/general.md` |
| `*.sql` + `migrations/` | database | `references/general.md` |
| `.glsl` or `.hlsl` files in top-level search | shader | `references/general.md` |
| None of the above | general | `references/general.md` |

Check in order. First match wins. If unsure, use `general`.

### Step 3: Load the Rule Pack

Read `references/<type>.md` for type-specific scanning instructions. Each rule pack defines:
- Key files to read first
- Directory structure conventions
- Dependency file location
- Entry point location conventions
- Type-specific patterns to grep for

### Step 4: Deep Scan

Follow the rule pack's instructions to:
1. Read project metadata (name, version, description)
2. Read dependency manifest (which packages/frameworks are used)
3. Map directory structure (what each top-level folder contains)
4. Identify entry points (main file, startup scene, bootstrap script)
5. Find core modules/classes and their responsibilities
6. Detect architectural patterns (MVC, ECS, layered, etc.)

Use `grep` to find key patterns. Use `read` with 30-80 line limits per file to extract structure without bloating context. Use `glob` to verify directory contents.

### Step 5: Generate AGENTS.md

Write `<project_root>/AGENTS.md` with EXACTLY this structure:

```markdown
# [Project Name]

## Basic Information
- **Type**: [Unity/Node.js/Python/etc.]
- **Language**: [primary language]
- **Framework/Engine**: [specific version if known]
- **Key Dependencies**: [3-8 most important packages]

## Directory Structure
[3-10 top-level directories with one-line descriptions]

## Entry Points
- [How to run/start the project]
- [Startup scene/file and what it does]

## Core Architecture
[BULLET LIST of 3-10 key files/classes and their roles. NOT verbose prose.]

## Dependencies
[TABLE: package name | purpose]

## Build & Run
- How to build: [command]
- How to run: [command]
- How to test: [command]

## Notes
- [Anything unusual or non-standard]
- [Known pitfalls if user has recorded any]
```

### Step 6: Report

Tell the user what was detected and where AGENTS.md was saved. Offer to add any project-specific notes or pitfalls they want recorded.

## Principles

- **Concise**: AGENTS.md target is 200-400 lines. Not a novel — a reference card for the AI.
- **Accurate**: Don't guess. If unsure, state uncertainty rather than fabricate.
- **Structured**: Bullet points and tables over prose. AI parses structure faster.
- **Actionable**: Every line should help the AI make better decisions in future conversations.
- **Incremental later**: The user can update AGENTS.md by saying "update AGENTS.md with [new information]".

## Adding New Project Types

When the user encounters a project type this skill doesn't recognize, offer to create a new rule pack. Ask:
1. What is the project type called?
2. What file or folder signatures identify it?
3. Where are dependencies declared?
4. Where are entry points typically found?
5. Any special file formats the AI should understand?

Then write the rule pack to `references/<name>.md` following the existing format.

## 🚫 Anti-Pitfalls

- Do NOT run external tools (npm install, cargo build, etc.) — read-only analysis only
- Do NOT modify any project files except writing AGENTS.md
- Do NOT read more than 50 files total — focus on the most important ones
- If the project has 500+ files, rely more on directory structure and less on reading individual files
- Do NOT generate user-facing documentation — this is for the AI agent's context
- If `references/<type>.md` doesn't exist yet, use `references/general.md` and suggest creating a type-specific rule pack
