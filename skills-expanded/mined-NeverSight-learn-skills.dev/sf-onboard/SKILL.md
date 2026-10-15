---
name: sf-onboard
description: 将新仓库或已有仓库接入 SpecForge；初始化唯一项目目录 .specforge/，补齐 core、wiki、hooks、registry 与 work 工作区，并判断下一步是否应进入 sf-steering。
---

# sf-onboard

## 运行目录

开始 onboard 前，先确认当前目录是要接入 SpecForge 的业务项目根。若当前在 `frontend/`、`backend/` 等子目录，先回到仓库根；不要在子目录里初始化 `.specforge/`，除非用户明确说明该子目录就是独立项目。

`sf-onboard` 只做三件事：搭骨架、识别存量项目、报告迁移建议。骨架完成后其他 `sf-*` 技能才能运行；已有代码的项目应先进入 `sf-steering` 建立 wiki 基线，再处理新需求或 bug。

## 必读

- `references/structure-and-migration.md`：安装命令、标准骨架、starter 来源、覆盖规则和迁移映射。
- `.specforge/core/workflows/stages/steering/SKILL.md`：项目画像、长期约束和 wiki 归档判断；仅在 `.specforge/` 已存在或初始化完成后读取。
- `.specforge/core/standards/workflow.md`：初始化边界、上下文加载和中文输出；仅在 `.specforge/` 已存在或初始化完成后读取。

## 核心原则

- 项目接入后只新增或补齐 `.specforge/`。
- 不创建根 `specs/`、根 `scripts/`，也不强制修改业务项目 `package.json`。
- 初始化素材来自 CLI 生成的唯一 starter 快照：GitHub 发行包中的 `starter/.specforge/`。
- 项目内命令直接运行 `node .specforge/core/scripts/<name>.mjs`。
- 已有 `.specforge/wiki/`、`.specforge/work/`、`.specforge/registry.yaml` 不覆盖。
- 已有业务代码的项目，onboard 后不直接开始需求实现；先运行 `codebase-index.mjs` 并路由到 `sf-steering`。

## 执行序列

### A. 启动扫描

1. 检查 `.specforge/` 是否存在。
2. Glob 全仓库 Markdown 文档，排除 `.git/`、`node_modules/`、`.specforge/work/archive/`。
3. 检查是否有旧版根 `specs/` 或根 `scripts/`。
4. 如果 `.specforge/` 已存在，运行 `node .specforge/core/scripts/codebase-index.mjs --json` 判断是否已有业务代码和 provider 支撑。
5. 汇报本次路径：空仓库、存量项目、已有 `.specforge/` 补齐，或迁移建议。

### B. 空仓库 / 新接入路径

执行：

```bash
npx github:huangrx6/SpecForge init --dir .
node .specforge/core/scripts/doctor.mjs
node .specforge/core/scripts/codebase-index.mjs --json
```

不要在普通业务项目中搜索 `/Users/.../workspace/specforge` 或其他个人目录来寻找 CLI。只有用户明确说“用本地 SpecForge 源码版本测试”时，才改用：

```bash
node cli/specforge.mjs init --dir /path/to/project
```

只允许根据用户已给出的项目信息补充 `.specforge/AGENTS.md` 的项目约束段，不要凭空补业务事实。

### C. 已有 `.specforge/` 路径

1. 只补齐缺失 core/starter 资产。
2. 保留现有 `.specforge/wiki/`、`.specforge/work/`、`.specforge/registry.yaml`。
3. 运行 `node .specforge/core/scripts/doctor.mjs`。
4. 运行 `node .specforge/core/scripts/codebase-index.mjs --json`。
5. 如果仓库已有业务代码，输出下一步为 `sf-steering`，先建立项目画像。

### D. 迁移路径

1. 按 `references/structure-and-migration.md#迁移映射` 生成迁移建议表。
2. 高置信度可列出执行计划；中/低置信度必须问用户。
3. 不移动、不删除用户未确认的文件。
4. 迁移后运行 `node .specforge/core/scripts/codebase-index.mjs --json`。
5. 只要仓库已有业务代码，下一步路由到 `sf-steering`。

## 判定表

| 条件 | 状态 |
|---|---|
| 当前目录不是业务项目根 | 停止：先切到项目根或请用户确认 |
| 用户要求安装 AI 工具技能 | 参考 `references/structure-and-migration.md#技能安装`，但不要混入业务项目初始化 |
| `.specforge/` 不存在 | 执行新接入路径 |
| `.specforge/` 存在但 core 缺失或过期 | 补齐后 doctor |
| 已有业务代码且 wiki 为空或明显不足 | 完成 onboard 后路由 `sf-steering` |
| 存在旧版 `specs/` / 根 `scripts/` | 只给迁移建议；低置信度先问用户 |

## 验收

- `.specforge/AGENTS.md` 存在。
- `.specforge/registry.yaml` 存在。
- `.specforge/wiki/`、`.specforge/work/`、`.specforge/core/scripts/` 存在。
- `node .specforge/core/scripts/doctor.mjs` 通过。
- 已有业务代码时，已明确提示下一步 `sf-steering`，用于生成项目画像和 wiki 基线。

## 不做

- 不在项目根目录创建 `specs/` 或 `scripts/`。
- 不在 onboard 过程中自动安装或同步 AI 工具技能；项目级技能安装必须由用户单独明确要求。
- 不替用户迁移低置信度文档。
- 不在已有代码项目中绕过 `sf-steering` 直接进入新需求实现。
