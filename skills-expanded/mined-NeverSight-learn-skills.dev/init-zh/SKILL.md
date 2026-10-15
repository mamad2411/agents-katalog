---
name: init-zh
description: Chinese version of init command, generates CLAUDE.md in Chinese for Claude Code
---

# init-zh - Chinese Initialization Plugin

Analyze codebase and create CLAUDE.md file with Chinese content.

## When to Use

Use `/init:zh` when you need to:
- Initialize a new project with Chinese documentation
- Generate Chinese version of CLAUDE.md for existing projects
- Document project structure, build commands, and architecture in Chinese

## Usage

```
/init:zh
/init:zh /path/to/project
```

## Execution Steps

1. **Discover Project Structure**
   - Find main source code directories and file types
   - Identify project type (Delphi, Python, Java, Node.js, etc.)
   - Find build configuration files (.dpr, package.json, pom.xml, etc.)

2. **Analyze Build and Test Commands**
   - Find build scripts and configurations
   - Identify test frameworks and test commands
   - Find lint/format tools

3. **Understand Architecture**
   - Analyze core modules and their responsibilities
   - Identify key entry points
   - Discover important design patterns or conventions

4. **Generate CLAUDE.md**
   - Write all content in Chinese
   - Include necessary compile/build commands
   - Describe project architecture
   - Document non-obvious patterns and conventions
   - Do not include obvious generic advice

## Output Format

Generated CLAUDE.md must start with:

```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## Content Requirements

**Must Include (if applicable):**
- Project overview (one sentence)
- Compile/build commands
- Test execution methods
- Core architecture description
- Coding conventions (project-specific)
- Non-obvious pitfalls or notes

**Should Not Include:**
- Generic development best practices
- Obvious explanations
- Detailed file lists (can be discovered)
- Sensitive information (API keys, passwords, etc.)

## Example Output

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

此文件为Claude AI编程助手在使用本仓库中的代码时提供指导。

## 项目概述

<一句话描述项目用途>

## 编译命令

| 命令 | 说明 |
|------|------|
| `<构建命令>` | 构建/编译项目 |
| `<测试命令>` | 运行测试 |

## 架构

<项目结构说明>

## 关键文件

- `<文件路径>` - <用途说明>

## 注意事项

- <非显而易见的陷阱>
```

## Author

xiaodongde (xiaodongde2008@gmail.com)