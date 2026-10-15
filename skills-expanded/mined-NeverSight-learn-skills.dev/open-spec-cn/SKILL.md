<!--
UpdatedAt: 2026-04-08 17:20:29 +0800
LatestChange: 初始化脚本升级为自动为全部 opsx 命令生成 -cn 版本，不再只生成 opsx-onboard-cn。
-->

# open-spec-cn

## 目标

为 OpenSpec 提供可跨项目复用的中文规范与命令包装，确保以下约束长期稳定生效：

- 规格文档以中文为主，保持人类可读性。
- Requirement 语句必须包含 `MUST` 或 `SHALL`（推荐：`必须（MUST）` / `应当（SHALL）`）。
- `Purpose` 不允许保留 `TBD` 占位文本。
- 归档前后自动校验，减少在 `archive` 阶段被阻塞的返工。

## 触发时机

当用户提到以下意图时应优先使用本技能：

- “OpenSpec 中文规范如何固化”
- “要让 spec 可读且可校验”
- “给 openspec 命令套一层 wrapper”
- “跨项目统一 OpenSpec 文档标准”

## 规范（强制）

### 1) 写作语言

- `openspec/changes/*/specs/**/spec.md` 与 `openspec/specs/**/spec.md` 的正文默认使用中文。
- 标题建议中文化（如 `Requirement` 标题可写中文语义标题）。

### 2) 规范关键词

- 每条 Requirement 必须显式出现 `MUST` 或 `SHALL`。
- 推荐句式：
  - `系统必须（MUST）...`
  - `系统应当（SHALL）...`

### 3) Purpose 约束

- `## Purpose` 下不得出现 `TBD` 占位文本。
- 必须写清能力目标与边界（1-3 句即可，简洁优先）。

### 4) 归档前自检（最小）

```bash
rg "MUST|SHALL" openspec/changes/<change>/specs
rg "TBD - created by archiving|^TBD$" openspec/specs
```

## Slash 命令初始化

本技能提供 `scripts/install-open-spec-cn.sh`，仅负责在项目内生成 Slash 命令文件：

- 自动扫描 `<project-root>/.cursor/commands/opsx-*.md`（排除已带 `-cn` 的文件）。
- 为每个命令生成对应 `<name>-cn.md`（例如 `opsx-new.md` -> `opsx-new-cn.md`）。

## 命名约定（重要）

本技能区分两类命令命名：

- **Cursor Slash 命令**：统一使用 `/opsx-<action>-cn`（例如 `/opsx-onboard-cn`）。
- **终端命令**：继续使用标准 `openspec <action>`，不额外创建 `-cn` 包装。

不要使用 `/openspec-<action>-cn` 作为 Slash 命令名，避免与现有 OpenSpec 命令体系不一致。

## 安装与使用

### 初始化（仅 Slash 命令）

```bash
bash /path/to/shared-skills/open-spec-cn/scripts/install-open-spec-cn.sh [project-root]
```

初始化动作包含两部分：

- 在 `<project-root>/.cursor/commands/` 自动生成全部 `/opsx-*-cn` 命令文件（默认 `<project-root>` 为当前目录）。

### 使用示例

```bash
openspec new change "improve-xxx"
openspec instructions proposal --change "improve-xxx" --json
openspec archive "improve-xxx" --no-interactive
```

## 输出要求（给 Agent）

- 结论优先：先说明是否符合规范，再给修复建议。
- 最小改动：默认不改业务语义，只修订文档结构与规范文本。
- 校验透明：明确告知执行了哪些校验命令与结果。
