---
name: trellis-migrate-skill
description: "Migrate an existing /trellis:<X> command to a skill; syncs target project + skill-garden copies."
---
# Migrate Command → Skill

把 `.claude/commands/trellis/<name>.md` 命令迁移到 `.claude/skills/trellis-<name>/` skill 形态，同步所有副本 + skill-garden 分发。

---

## 适用场景

- 命令更适合自然语触发（查询 / 分析 / 检查类：如 check-all、analyze-task）
- 命令内部引用已过时（agent 重命名、multi_agent 已删除、check-cross-layer 已合并等）
- 多个相邻命令语义重复，想融合成一个宿主 skill
- trellis 脚手架升级后要同步 skill-garden 的分发包

## 前置条件

- **`<target>`（目标项目）**：默认 = 当前工作目录（`pwd`）。如需迁移其他项目的命令，由用户显式指定绝对路径；本 skill 不主动 `cd`
- **`<skill-garden>`（分发源）**：默认 `/root/project/skill-garden`。路径不存在或与用户期望不符 → 询问用户
- 目标命令存在于 `<target>/.claude/commands/trellis/<name>.md` 或 `<target>/.agents/skills/<name>/SKILL.md`
- 若 `<target>` 与 `<skill-garden>` 是同一路径（在 skill-garden 仓库里迁移），副本去重、只写一次
- skill-garden 使用 variant 结构（`.trellis/0.5/` 对应新版，`.trellis/old/` 向后兼容）

---

## 执行步骤

### Step 1: 读两份副本 + 对齐扫描

读取当前内容：

```bash
cat <target>/.claude/commands/trellis/<name>.md
cat <target>/.agents/skills/<name>/SKILL.md
```

对齐扫描（grep 过时引用）：

```bash
# 旧 multi_agent 脚本
grep -nE "multi_agent|scripts/(start|plan|cleanup|create_pr|status)\.py" <target_files>

# 旧 agent 名（应改 trellis-*）
grep -nE 'subagent_type: "(check|implement|research)"' <target_files>

# 悬空 skill（已合并）
grep -n "check-cross-layer" <target_files>

# 已删除命令
grep -nE "/trellis:(start|brainstorm)" <target_files>

# 已废弃目录
grep -n ".cursor/commands" <target_files>
```

把扫描发现汇总成 `清单 (文件 → 行号 → 过时引用 → 应替换为)` 呈现给用户。

### Step 2: 形态决策

询问用户：

| 选项 | 适用 | description 策略 |
|------|------|------------------|
| 仅对齐修复 | 保持 command 形态，只修过时引用（finish-work / continue 这类显式动作） | — |
| skill 化（Auto-routing） | 删 command 副本，改/新增 agents + skill；**需要** Claude 按自然语自动加载（查询 / 分析 / 检查类：analyze-task、check-all） | 80–300 字三段式 |
| skill 化（Manual-only） | 删 command 副本，改/新增 agents + skill；用法明确、频率低、不希望占 skill 列表 token（管理工具：migrate-skill、create-command） | 15–20 tokens 单句 |
| 融合到宿主 skill | 内容内嵌到 check-all 这类宿主，删除本身所有副本 | — |

> **推荐原则**：日常工作流（check / analyze / draw / sync）走 Auto-routing；低频管理工具走 Manual-only；迁移时有疑问就默认 Auto-routing（更灵活）。

### Step 3: 融合判断（仅形态 = 融合时）

| 问法 | 对应动作 |
|------|---------|
| 彻底融合 | 删所有副本（command + agents 各 2 份），内容并入宿主 |
| 仅删 command | 保留 agents 作为宿主引用的组件 |
| 保留现状 | 不融合（与"仅对齐修复"等价） |

彻底融合时注意 diff 对比宿主和被融合者：识别 Step/原则/反模式/报告模板等模块，合理合并，避免遗漏关键 checklist。

### Step 4: 执行同步（skill 化模式）

对每个要 skill 化的 `<name>`，共 6 步、涉及 4 份副本：

```bash
# (1-2) 删 command 副本
rm <target>/.claude/commands/trellis/<name>.md
rm <skill-garden>/.trellis/0.5/.claude/commands/trellis/<name>.md

# (3-4) 更新 agents 副本（正文 + frontmatter 完全对齐 skill 版，name=trellis-<name>）
# — 用最新已对齐的内容覆盖写入；路径为 .agents/skills/trellis-<name>/SKILL.md

# (5-6) 新增 skill 副本
mkdir -p <target>/.claude/skills/trellis-<name>
mkdir -p <skill-garden>/.trellis/0.5/.claude/skills/trellis-<name>
# 写入 SKILL.md（frontmatter name=trellis-<name>）
```

### Step 5: 执行同步（融合模式）

```bash
# 删 4 份副本
rm <target>/.claude/commands/trellis/<name>.md
rm <skill-garden>/.trellis/0.5/.claude/commands/trellis/<name>.md
rm -rf <target>/.agents/skills/trellis-<name>/
rm -rf <skill-garden>/.trellis/0.5/.agents/skills/trellis-<name>/

# 编辑宿主 skill 的 4 份副本，内嵌融合内容
# 注意保留：原核心原则 / 报告模板 / 反模式 / Dimension checklist 等关键段
```

### Step 6: frontmatter 规则

**name**：两份副本的目录名和 frontmatter `name:` 字段都统一使用 `trellis-<X>`。

| 文件位置 | name |
|---------|------|
| `.claude/skills/trellis-<X>/SKILL.md` | `trellis-<X>` |
| `.agents/skills/trellis-<X>/SKILL.md` | `trellis-<X>` |

> 历史说明：0.5 早期 agents 版曾用无前缀 `<X>` 作为 name，迁移脚本需 `sed` 替换。自 2026-04 起统一为 `trellis-<X>`，4 份副本完全一致，不再需要 sed 替换 frontmatter。

**description** 按 Step 2 选定的策略：

| 策略 | 长度 | 写法 |
|------|------|------|
| **Auto-routing** | 80–300 字 | 三段式：What（动词开头）+ When（中英触发词）+ Exclusion（"For X, use Y instead"）。Claude 据此按自然语路由，每次对话都会注入 skill 列表 |
| **Manual-only** | 15–20 tokens | 单句动作 + 产出物。靠用户 `/trellis-<X>` 显式触发，description 不作路由依据，节省 skill 列表 token |

**body 正文和 frontmatter 都 4 份完全一致**，直接 `cp` 即可，不需要 sed 改 name：

```bash
cp <target>/.claude/skills/trellis-<X>/SKILL.md <target>/.agents/skills/trellis-<X>/SKILL.md
cp <target>/.claude/skills/trellis-<X>/SKILL.md <skill-garden>/.trellis/0.5/.claude/skills/trellis-<X>/SKILL.md
cp <target>/.claude/skills/trellis-<X>/SKILL.md <skill-garden>/.trellis/0.5/.agents/skills/trellis-<X>/SKILL.md
```

### Step 7: 更新 install.sh 支持（如需）

确认 skill-garden install.sh 已有：
- 3c 段 `.claude/skills/` 循环安装
- `should_install` 支持 `trellis-` 前缀去除匹配（`install.sh TARGET analyze-task` 能命中 `trellis-analyze-task`）

如果某次迁移涉及新路径约定，同步修改 install.sh + 端到端测试。

### Step 8: 更新 skill-garden README

必改：
- "全部技能" 表：对该 skill 标注 "0.5+ skill 化为 trellis-<name>"
- "variant 说明" 表：列举新版的变化点

可选：
- "推荐命令" 表：高频 skill 加入
- "新增 Trellis 技能" 指引：如果约定有变

### Step 9: 验证

| 检查项 | 命令 |
|-------|------|
| skill 出现在 Claude skill list | 读 `<available-skills>` 区，确认 `trellis-<name>` 存在且 description 正确 |
| `/trellis:<name>` 已消失 | 同上，原 command 不应再出现 |
| install 分发通过 | `rm -rf /tmp/sg-test && mkdir -p /tmp/sg-test/.trellis && echo "0.5.0-beta.8" > /tmp/sg-test/.trellis/.version && bash <skill-garden>/scripts/install.sh /tmp/sg-test <name>` |
| 4 份副本内容一致 | `wc -l` 对比行数；`diff` 关键段落 |

如 skill list 未刷新：harness 有缓存，在下一轮对话系统会自动刷新；不要反复确认。

### Step 10: 提交（可选）

按 skill-garden commit message 风格：

```
<type>(trellis): <概述，40 字内>

<空行>

<背景：为什么做这次迁移，引用 trellis 版本变化或业务动因>

<改动：做了什么具体动作，列关键路径和数量>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

`<type>` 参考：
- `refactor(trellis):` — 迁移/重构（典型场景）
- `feat(trellis):` — 新增能力（如首次 skill 化某类工具）
- `chore(trellis):` — 清理/对齐
- `docs(trellis):` — 仅文档

---

## 反模式（避免）

- ❌ 跳过 Step 1 对齐扫描就动手——会留下过时引用，运行时报错
- ❌ 只改目标项目不同步 skill-garden——下次 install 会被 skill-garden 旧版覆盖
- ❌ skill 版和 agents 版正文不一致——同一入口行为分裂
- ❌ 选 Auto-routing 策略但 description 过短（< 80 字）——Claude 路由不稳；Manual-only 策略无此要求
- ❌ 所有迁移都默认 Auto-routing——低频管理工具（migrate-skill / create-command 这类）可选 Manual-only 节省 token
- ❌ 融合后不删被融合者——两个入口冲突，Claude 不知选哪个
- ❌ 改动后 skill list 未出现新项就直接"验证通过"——可能 frontmatter 语法错（YAML 缩进/引号）
- ❌ skill-garden README 不更新——未来迁移者看不到新约定
- ❌ 提交时把不相关改动一起塞入 commit——应该一个迁移一个 commit

---

## 快速参考：4 份副本对照表

| 序号 | 路径 | 角色 |
|------|------|------|
| 1 | `<target>/.claude/commands/trellis/<name>.md` | command 版，skill 化后删除 |
| 2 | `<target>/.agents/skills/trellis-<name>/SKILL.md` | agents 版，trellis agent 系统读取（保留，名字带 trellis- 前缀） |
| 3 | `<target>/.claude/skills/trellis-<name>/SKILL.md` | skill 版，Claude harness 自动路由（新增） |
| 4 | `<skill-garden>/.trellis/0.5/.*` | 对应的 3 份 skill-garden 副本（分发源） |

同步顺序建议：先 skill 版（Claude harness 立刻能感知变化） → 再 agents 版 → 最后 skill-garden 副本。
