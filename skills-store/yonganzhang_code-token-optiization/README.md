<div align="center">

# Token Optimization Plan

**A practical system for cutting AI coding assistant token usage by 50-60% through progressive disclosure.**

Built for Claude Code, Codex, and skill-based agent workflows.

[![Claude Code](https://img.shields.io/badge/Claude_Code-Supported-111827)](./references/setup-claude-code.md)
[![Codex](https://img.shields.io/badge/Codex-Supported-F97316)](./references/setup-codex.md)
[![Progressive Disclosure](https://img.shields.io/badge/Pattern-Progressive_Disclosure-2563EB)](./references/patterns.md)
[![Token Savings](https://img.shields.io/badge/Token_Saved-50--60%25-16A34A)](./references/cost-model.md)
[![Stars](https://img.shields.io/github/stars/YonganZhang/code-token-optiization?style=social)](https://github.com/YonganZhang/code-token-optiization/stargazers)

[Quick Start](#quick-start) · [How It Works](#how-it-works) · [Core Patterns](#core-patterns) · [Academic Research Stack](#academic-research-stack) · [中文](#中文说明) · [日本語](#日本語) · [한국어](#한국어)

</div>

---

## Why This Exists

Most AI coding projects waste context on the same mistake:

- huge project instructions loaded every turn
- skills that act like long documents instead of indexes
- implementation details stored in the wrong layer
- rules that are too long and too static

This repository packages a reusable operating model for skill-based coding agents: keep always-loaded context small, then reveal detail only when triggered.

## What You Get

- A complete token optimization methodology for Claude Code and Codex
- A self-contained skill package with `SKILL.md` and `references/`
- Installation guides for both platforms
- Example rules and example skills
- A layered architecture you can copy into your own projects

## Quick Start

### Claude Code

```bash
git clone https://github.com/YonganZhang/code-token-optiization.git ~/.claude/skills/top
```

Then read:

- [`references/setup-claude-code.md`](./references/setup-claude-code.md)

### Codex

```bash
git clone https://github.com/YonganZhang/code-token-optiization.git ~/.codex/skills/top
```

Then read:

- [`references/setup-codex.md`](./references/setup-codex.md)

## How It Works

The core idea is a four-layer progressive disclosure model:

```text
L0  tiny rules / trigger index        -> loaded every turn
L1  SKILL.md index                    -> loaded when triggered
L2  references/*.md detail files      -> read only as needed
L3  source code / project files       -> read only as needed
```

If you move volatile or verbose information downward, you reduce recurring token cost without losing capability.

## Core Patterns

### 1. Trigger Index + Skill Loading

Rules should trigger the right skill, not duplicate its full content.

### 2. SKILL.md as an Index, Not a Manual

`SKILL.md` should stay short and route the agent to the right reference files.

### 3. Slim Project Instructions

Keep `CLAUDE.md` / `AGENTS.md` focused on identity, constraints, and stable project facts.

### 4. Self-Maintained Indexes

When modules or workflows change, regenerate the relevant skill indexes instead of growing global instructions.

### 5. On-Demand Tool and Context Loading

Only load what the current task actually needs.

## Before vs After

| Scenario | Before | After |
| --- | --- | --- |
| project instructions | loaded in bulk every turn | slim stable core only |
| rule files | long explanatory text | short triggers |
| skills | monolithic docs | layered indexes |
| deep details | preloaded | fetched when relevant |
| total context cost | high and repetitive | materially lower |

## Repository Layout

```text
code-token-optiization/
├── SKILL.md
├── references/
│   ├── cost-model.md
│   ├── patterns.md
│   ├── setup-claude-code.md
│   └── setup-codex.md
├── examples/
│   ├── rules/
│   └── skills/
└── docs/
    └── posts/
```

## Who This Is For

- heavy Claude Code users
- Codex users maintaining larger projects
- people building custom agent workflows with skills
- teams that care about context efficiency, reproducibility, and maintainability

## Academic Research Stack

This repository is part of a broader collection around academic research and vibe coding:

| Project | What It Helps With |
| --- | --- |
| [code-token-optiization](https://github.com/YonganZhang/code-token-optiization) | token-efficient architecture for coding agents |
| [mathpix-converter](https://github.com/YonganZhang/mathpix-converter) | convert academic PDFs and equations into Markdown |
| [gemini-research-oauth](https://github.com/YonganZhang/gemini-research-oauth) | run Gemini Deep Research from CLI with OAuth |
| [SpeakFlow](https://github.com/YonganZhang/SpeakFlow) | offline voice input for writing and prompting |
| [openakita](https://github.com/YonganZhang/openakita) | open AI assistant framework with skills and agent architecture |

Together these repos cover ingestion, research, prompting, and agent engineering.

## 中文说明

这个仓库本质上是一套 AI 编程助手上下文治理方法论，不是单一脚本。

它要解决的问题是：

- `CLAUDE.md` / `AGENTS.md` 越写越长
- Rule 和 Skill 职责混乱
- 每轮对话都重复加载大量没必要的信息
- 项目一大，Token 消耗明显失控

核心思路是“渐进式披露”：

- 每轮都加载的内容尽量短
- 只有触发时才加载 `SKILL.md`
- 只有确实需要时才读 `references/`
- 源码和实现细节放在最底层按需读取

如果你在重度使用 Claude Code 或 Codex，这个仓库会比较有价值。

## 日本語

このリポジトリは、Claude Code や Codex のような AI コーディング支援ツールで、毎ターンのトークン消費を減らすための実践的な設計手法をまとめたものです。

- ルールは短く保つ
- `SKILL.md` は索引として使う
- 詳細は `references/` に分離
- 必要な時だけ情報を読む

大きめのプロジェクトや skill ベースの運用に特に有効です。

## 한국어

이 저장소는 Claude Code나 Codex 같은 AI 코딩 도구에서 매 턴 반복되는 토큰 비용을 줄이기 위한 실전 설계 방법을 정리한 것입니다.

- 규칙 파일은 짧게 유지
- `SKILL.md`는 인덱스로 사용
- 자세한 내용은 `references/`로 분리
- 필요한 순간에만 정보를 읽도록 설계

프로젝트 규모가 크거나 skill 기반 워크플로를 운영할 때 특히 유용합니다。

## License

No `LICENSE` file is included in this repository yet. Adding one would make reuse and contributions much clearer.
