---
name: cc-history
description: "查询 Claude Code 会话历史记录。触发词：cc-history、CC 历史、今天做了什么、昨天做了什么、工作记录、会话记录。"
---

# cc-history

通过 Python 脚本读取 `~/.claude/projects/<encoded-path>/*.jsonl` 会话文件，解析时间戳和用户/助手消息，**无需大模型参与**即可输出结构化工作摘要。

## ⚠️ 强制规则

> **当用户问"今天做了什么/工作记录/CC 历史"时，必须第一时间运行本脚本，禁止手动 git log / find / grep 搜索。**

执行优先级：

```
1. python3 <脚本路径> [参数]              # 第一步：查询历史记录
2. 根据 --summary 输出 → 提交滴答清单     # 第二步：按需提交（可选）
3. python3 <脚本路径> --all --ticktick    # 第三步：生成滴答清单 JSON（可选）
```

<gsd:workflow>
  <gsd:meta>
    <name>cc-history</name>
    <trigger>cc-history, CC 历史, 今天做了什么, 昨天做了什么, 工作记录, 会话记录</trigger>
    <requires>Python 3, Bash</requires>
    <checkpoints>
      <checkpoint order="1">脚本可执行性验证（python3 可用）</checkpoint>
      <checkpoint order="2">输出结果展示后等待下一步指令</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>时间自动从 UTC +8 转换为本地时间（脚本已内置处理）</constraint>
      <constraint>脚本路径使用绝对路径，支持在任意目录执行</constraint>
      <constraint>默认查看今天，不加参数时只查当前项目</constraint>
      <constraint>用户要求查看所有项目时使用 --all 参数</constraint>
      <constraint>禁止在大模型中手动解析 JSONL，必须通过脚本完成</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>快速查询 Claude Code 会话历史，支持按日期、项目、范围过滤，并可联动 tt skill 提交到滴答清单。</gsd:goal>

  <gsd:phase name="query" order="1">
    <gsd:step>解析用户意图：日期（今天/昨天/指定日期）、范围（当前项目/所有项目/指定项目）</gsd:step>
    <gsd:step>构建并执行 Python 脚本命令</gsd:step>
    <gsd:step>展示输出结果</gsd:step>
    <gsd:step>询问用户是否需要进一步操作（提交到滴答清单等）</gsd:step>
  </gsd:phase>

  <gsd:phase name="submit" order="2" condition="用户要求提交到滴答清单">
    <gsd:step>根据工作记录内容，总结用户当天的工作事项</gsd:step>
    <gsd:step>调用 tt skill，将总结的工作事项创建为滴答清单任务</gsd:step>
    <gsd:step>历史任务（时间已过）自动标记为完成</gsd:step>
  </gsd:phase>
</gsd:workflow>

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| （无参数） | 查看今天，当前项目 | `python3 cc-history.py` |
| `--all` | 扫描所有项目的会话 | `python3 cc-history.py --all` |
| `--project <path>` | 指定项目路径 | `python3 cc-history.py --project ~/jacky-github/tt-cli` |
| `--yesterday` | 查看昨天 | `python3 cc-history.py --yesterday` |
| `--date YYYY-MM-DD` | 查看指定日期 | `python3 cc-history.py --date 2026-04-04` |
| `--summary` | 汇总模式（每会话一行） | `python3 cc-history.py --all --summary` |
| `--ticktick` | 输出滴答清单 JSON（自动合并相近会话） | `python3 cc-history.py --all --ticktick` |
| `--merge-gap <min>` | 滴答清单合并间隔（默认 15 分钟） | `python3 cc-history.py --all --ticktick --merge-gap 30` |
| `--no-merge` | 滴答清单不合并（每个会话一条任务） | `python3 cc-history.py --all --ticktick --no-merge` |

参数可组合使用，如 `--all --yesterday` 表示查看所有项目昨天的记录。

## 意图解析

| 用户说法 | 日期参数 | 范围参数 |
|----------|---------|---------|
| "今天做了什么" / "CC 历史" | （默认今天） | （默认当前项目） |
| "昨天做了什么" | `--yesterday` | （默认当前项目） |
| "所有项目今天做了什么" | （默认今天） | `--all` |
| "4月3号的工作" | `--date 2026-04-03` | （默认当前项目） |
| "所有项目昨天做了什么" | `--yesterday` | `--all` |

## 执行流程

### Phase 1: 查询历史记录

**Step 1 — 解析意图，执行脚本**

脚本绝对路径：
```
${JACKY_SKILLS_DIR:-$HOME/jacky-github/jacky-skills}/plugins/monitoring/cc-history/scripts/cc-history.py
```

```bash
# 基本格式
python3 <脚本路径> [日期参数] [范围参数]

# 示例
python3 <脚本路径>                        # 今天，当前项目
python3 <脚本路径> --all                  # 今天，所有项目
python3 <脚本路径> --yesterday            # 昨天，当前项目
python3 <脚本路径> --date 2026-04-04      # 指定日期
python3 <脚本路径> --project ~/jacky-github/tt-cli  # 指定项目
python3 <脚本路径> --all --yesterday      # 所有项目 + 昨天
```

**Step 2 — 展示结果**

脚本输出格式示例：

**单项目模式**：
```
============================================================
  Claude Code 工作记录 - 2026-04-05
  项目: ~/jacky-github/tt-cli
============================================================

--- c20d267d...7667 (14:08 -> 14:51) ---
    文件: ~/.claude/projects/-Users-jiashengwang.../c20d267d-...jsonl
    用户消息: 5 | 编辑: 11 | 命令: 45
    [14:08] > 帮我将上午没有完成的任务分配到下午...
    [14:09] $ Check tt CLI version
    [14:15] ~ Edit: task.ts
```

**全项目模式（--all）**：
```
============================================================
  Claude Code 工作记录（全部项目）- 2026-04-05
============================================================

──────────────────────────────────────────────────
  📂 ~/jacky-github/tt-cli  (3 个会话, 120 条记录)
──────────────────────────────────────────────────

--- c20d267d...7667 (14:08 -> 14:51) ---
    ...

──────────────────────────────────────────────────
  合计: 5 个项目 | 12 个会话 | 450 条记录
──────────────────────────────────────────────────
```

> **Checkpoint**: 展示结果后等待用户下一步指令

### Phase 2: 提交到滴答清单（联动 tt skill）

**触发条件**：用户说"帮我提交到滴答清单"、"记录到滴答清单"、"补全日程"等。

> ⚠️ **重叠检测规则（强制）**：滴答清单日历视图无法正常显示同时段重叠任务，创建前必须保证无重叠。

**执行步骤**：

1. **查询已有任务**：先用 `tt task completed --start <date> --end <date>` 和 `tt task undone --start <date> --end <date>` 获取目标日期的所有已有任务，展示给用户
2. **分析工作记录**：从 Phase 1 的输出中，提取用户当天完成的工作事项
3. **生成非重叠任务列表**：
   - 将 cc-history 的会话按实际活动时间排列，**跨项目重叠的会话合并为一条任务**
   - 与已有任务对比，**已有任务的时间段不可占用**
   - 每个时间段只分配一条任务（连续的 CC 会话合并为一个时间段）
   - 标题 ≤15 字，具体细节写入 content
4. **展示合并方案**：用表格展示时间线（含已有任务 + 新任务），确认无重叠后执行
5. **调用 tt skill**：使用批量创建功能提交任务
   - 工作时间已过的任务自动标记为完成
   - 使用 `echo "y" | tt task-delete` 删除被替换的旧任务
6. **确认结果**：展示最终任务清单

**重叠合并策略**：

| 场景 | 处理方式 |
|------|----------|
| 同一项目内连续会话（间隔 < 15min） | 合并为一条任务 |
| 不同项目同时段会话 | 合并为一条任务，content 列出各项目工作 |
| CC 会话与已有滴答清单任务重叠 | 优先保留已有任务，CC 会话填充空闲时段 |
| 长时间会话（> 3h）中间有其他项目活跃 | 拆分为多个时段，中间留出其他项目的时间 |

## 脚本工作原理

1. 根据参数定位会话目录：
   - 默认：当前工作目录 → `~/.claude/projects/<encoded-cwd>/`
   - `--project`：指定路径 → `~/.claude/projects/<encoded-path>/`
   - `--all`：遍历 `~/.claude/projects/` 下所有子目录
2. 遍历目标目录下的所有 `.jsonl` 会话文件
3. 按日期过滤（JSONL 内部 UTC 时间戳 +8 转本地时间）
4. 提取用户消息和关键操作（Edit/Write/Bash）
5. 按时间排序输出（`--all` 模式按项目分组）

## 注意事项

- 时间已从 UTC 自动 +8 转换为本地时间（CST）
- Skill 加载等超长内容会被自动过滤，只保留有效用户输入
- 每个会话显示统计：用户消息数、编辑数、命令数
- `--all` 模式下项目名通过读取 JSONL 文件中的 cwd 字段获取
- 脚本支持在任意目录执行，无需从 skill 目录运行

## Check List

- [ ] 脚本路径使用绝对路径
- [ ] 日期参数正确（今天/昨天/指定日期）
- [ ] 时间已从 UTC +8 转换为本地时间
- [ ] `--all` 模式按项目分组显示
- [ ] 展示结果后等待用户下一步指令
- [ ] 联动 tt skill 时：先查询目标日期已有任务，展示给用户
- [ ] 联动 tt skill 时：跨项目重叠会话合并为一条任务
- [ ] 联动 tt skill 时：每个时间段只有一条任务，无重叠
- [ ] 联动 tt skill 时：标题 ≤15 字，具体细节写入 content
- [ ] 联动 tt skill 时：历史任务自动标记完成
- [ ] 联动 tt skill 时：创建前展示合并方案表格确认
