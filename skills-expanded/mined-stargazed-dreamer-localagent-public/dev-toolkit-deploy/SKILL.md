---
name: dev-toolkit-deploy
description: >
  把 <project_root>\workspace\dev_toolkit（34 个 skill 蓝图）部署到某个项目。
  当用户说「部署 dev_toolkit」「把 toolkit 弄过来」「这个项目的 skill 太少」时使用。
  关键不是拷贝，而是**增量合并**——目标项目多半已有自己的 .agents/ 资产（业务 skill、
  AGENTS.md、memory），全量覆盖会毁掉真机实测结论。按本流程做差异比对、裁剪、索引合并。
agent_created: true
task_type: dev.dev_toolkit_deploy
---

# dev_toolkit 部署（增量合并，不是覆盖）

## 何时用

- 用户要求把 dev_toolkit 部署到某项目
- 某项目 `.agents/skills/` 只有几个自研 skill，缺少通用工作流（SDD 链、TDD、防幻觉等）

**toolkit 位置**：`<project_root>\workspace\dev_toolkit`
（内含 `DEPLOY.md` 6 步流程、`AGENTS.md` 模板、`.agents/skills/` 34 个目录式 skill、
`.agents/rules/`、`manifest.toml`；`dev_toolkit_v3.zip` 是打包副本，不要拷）

## 核心判断：先分清「全新项目」还是「已有资产」

`DEPLOY.md` 假设全新项目。实际多数目标是**已有 `.agents/`** 的半成熟项目，
此时直接拷贝会毁掉业务 skill。分三路：

| 目标现状 | 做法 |
|---------|------|
| 无 `.agents/` | 按 DEPLOY.md 6 步走：拷全部 → 填 `TODO_DEPLOY` 占位符 → 裁剪 → 删 DEPLOY.md |
| 有 `.agents/skills/*.md`（平铺） | **增量合并**（本 skill 主流程） |
| 已有目录式 skill | 只补齐缺失的，逐个 diff 版本后决定谁覆盖谁 |

## 增量合并流程（6 步）

### 1. 摸清目标现有资产
```bash
find .agents -type d | sort && ls -la .agents/skills/ .agents/memory/ .agents/wip/
diff <目标>/AGENTS.md <toolkit>/AGENTS.md | grep -c "^[<>]"
```
**判断 AGENTS.md 是否已定制**：差异 >100 行基本说明已填好项目内容 → **绝不覆盖**，
只改 Skill 章节与目录树。toolkit 那份带 `TODO_DEPLOY` 的模板存档到 `temp/` 备查。

### 2. 备份将被替换的文件
```bash
mkdir -p temp/_skills_backup_<日期>
cp .agents/skills/<同名文件> temp/_skills_backup_<日期>/
```
平铺 `.md` 与 toolkit 的目录式 `<name>/SKILL.md` 重名时（neat-freak / skill-creator /
wip-tracker），用目录版取代，但**必须先备份** —— 旧版可能含项目特定的记忆路径约定。

### 3. 按项目类型裁剪
toolkit 34 个不必全要。判据：

| skill | 保留条件 |
|-------|---------|
| SDD 链（grill-me/spec/plan/tasks/analyze/implement）+ verify + anti-hallucination + diagnosing-bugs | 一律保留 |
| `dev/*`（tdd / codebase-design / domain-modeling / goal_engineering / leader / resolving-merge-conflicts） | 一律保留 |
| `dev/prototype` | 有 UI 或需探索设计时保留 |
| **`dev/impeccable`（2.7M）+ `dev/hallmark`（952K）** | 仅 Web 前端项目保留；其它一律删（含浏览器脚本，体积大头） |
| **`ui-ux-pro-max`（1.5M data）** | Web/UI 项目保留；纯 CLI 可删 |
| `daily/*`（11 个，共 108K） | 通用思维工具，体积小，一般保留 |

**经验**：Python 库 + PySide6 桌面 UI → 删 impeccable + hallmark，保留 ui-ux-pro-max。
删完总体积约 2M，`.git` 增长 <1M，可接受。

### 4. 拷入（排除裁剪项）
```bash
SRC="<project_root>/workspace/dev_toolkit/.agents/skills"
DST="<目标>/.agents/skills"
for d in analyze anti-hallucination daily diagnosing-bugs grill-me implement \
         neat-freak plan skill-creator spec tasks ui-ux-pro-max verify wip-tracker; do
  cp -r "$SRC/$d" "$DST/"
done
mkdir -p "$DST/dev"
for d in codebase-design domain-modeling goal_engineering leader prototype \
         resolving-merge-conflicts tdd; do cp -r "$SRC/dev/$d" "$DST/dev/"; done
cp -r "$SRC/../rules" "<目标>/.agents/"
```

### 5. 合并 `_index.md`（最关键）
**不要覆盖**。目标是两段式：

1. **第一部分：项目业务 skill**（原样保留原有详细描述 —— 真机基线、陷阱、commit 号都在这）
2. **第二部分：通用 skill 清单**（toolkit 的表格，精简 description 到一行）

理由：通用 skill 有 31 个，平铺会把业务 skill 的实测结论淹没，agent 每次会话读索引时
看不到最该看的东西。顺序即优先级。

同步改：`.gitignore` 补 `.agents/specs/`；`AGENTS.md` 的目录树 + Skill 章节
（说明两类 skill 共存、业务优先）；`checklist.md` 补 SDD 产物检查项。

### 6. 校验
```bash
# 每个目录都有 SKILL.md 且带 frontmatter name；索引无遗漏；无 TODO_DEPLOY 残留
```
再 `git add -A .agents/ && git commit`，工作区保持干净。

## 坑

- **`_index.md` 直接覆盖** → 业务 skill 的实测结论全丢。这是最容易犯的错。
- **`wip_tracker.md`（下划线）vs `wip-tracker/`（连字符）** 是同一 skill 的两种命名，
  两套并存会让 agent 触发时命中两个实现，必须只留一个。
- **`.agents/memory/` 别顺手 gitignore**：toolkit 的 DEPLOY.md 建议排除，但项目若已把
  memory 当跨会话状态用（如 `v4_migration.json`），排除即丢状态。先看 `git ls-files` 再决定。
- **拷贝前先 `du -sh`**：impeccable + hallmark 3.7M、ui-ux-pro-max 1.5M，
  不裁剪会让小项目仓库无谓膨胀。
- 部署完**不要**"完善" skill 方法论文件（改流程/加步骤）。DEPLOY.md 明令：
  "完善"= 填占位符 + 裁剪 + 适配，不是改方法论。

## 实测记录

2026-09-18 部署到 `<projects_parent>\wechatDecode`：
保留业务 skill `wechat_v4_decrypt.md`（18K，含 27 库真机基线）/ `task_room_digest.md`；
删 impeccable + hallmark；平铺三元 skill 换目录版（旧版备份
`temp/_skills_backup_20260918/`）；新增 `.agents/rules/`；commit `3a8bbb4`。
