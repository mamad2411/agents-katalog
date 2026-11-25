---
name: tt
description: "TickTick 日程管理。触发词：/tt、日程、待办、计划、任务、滴答清单、日程复盘、时间都去哪了、今天干了什么、补全日程、回顾今天。"
---

# tt

TickTick（滴答清单）日程管理 Skill，通过 `tt` CLI 提供完整的任务读取、写入和项目管理功能。

> **IMPORTANT**: 在执行任何任务操作前，必须先读取 `references/humanization.md` 并遵循其中的人性化关怀规则。这是一份强制加载的参考资料。

<gsd:workflow>
  <gsd:meta>
    <name>tt</name>
    <trigger>/tt、日程、待办、计划、任务、滴答清单、日程复盘、时间都去哪了、今天干了什么、补全日程、回顾今天</trigger>
    <requires>tt CLI (npm install -g @wangjs-jacky/ticktick-cli), Bash, AskUserQuestion</requires>
    <checkpoints>
      <checkpoint order="0">CLI 可用性检测完成后，提示用户安装或登录</checkpoint>
      <checkpoint order="1">首次查询后展示结果，等待用户下一步指令</checkpoint>
      <checkpoint order="2">执行修改前确认操作内容</checkpoint>
      <checkpoint order="3">所有询问结束后，展示汇总并确认是否创建任务</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>Phase 0 必须首先执行，检测 tt CLI 可用性</constraint>
      <constraint>未安装时，必须提供安装引导，不得直接报错退出</constraint>
      <constraint>禁止硬编码 projectId，首次通过 tt project-list 获取后缓存映射，失败时才刷新</constraint>
      <constraint>禁止串行调用 CLI，必须并行调用（已完成/未完成/项目列表）</constraint>
      <constraint>用户说"更新/修改"时，直接查找现有任务，不要问"是要修改还是要创建"</constraint>
      <constraint>日程复盘由主会话直接执行，3步完成：①并行获取数据 ②AskUserQuestion展示空白时段 ③批量创建任务</constraint>
      <constraint>历史任务（时间已过）必须自动标记为完成</constraint>
      <constraint>时区规则：API 返回的时间为 UTC（+0000/Z 后缀），必须 +8 转换为上海本地时间（CLI 已修复，直接使用 new Date() 解析即可）</constraint>
      <constraint>非今日任务查询必须用 --start/--end 日期范围参数，禁止用 --query yesterday（不支持）</constraint>
      <constraint>⚡ 效率要求：任务操作必须在 1 分钟内完成。优先使用 --json 获取结构化数据，避免文本解析和多次 CLI 调用</constraint>
      <constraint>批量更新任务时，必须用 --json 获取 task ID，然后用 tt task-batch-update --stdin 一次完成，禁止逐个更新</constraint>
      <constraint>获取 task ID 的优先路径：tt task undone --json → tt project-tasks <id> --json → tt task-search --json（按可用性降序）</constraint>
      <constraint>标题与内容规则：标题必须简短（≤15字），具体细节写入 --content。禁止把所有信息塞在标题里。详见「标题与内容规则」小节</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>通过 tt CLI 提供完整的 TickTick 任务读取、写入和项目管理功能</gsd:goal>

  <gsd:phase name="前置检测" order="0">
    <gsd:step>检测 tt CLI 是否已安装（tt --version）</gsd:step>
    <gsd:step>检测是否已登录（tt whoami）</gsd:step>
    <gsd:step>未安装时提供安装引导</gsd:step>
  </gsd:phase>

  <gsd:phase name="任务读取" order="1">
    <gsd:step>并行调用 CLI 获取今日任务数据</gsd:step>
    <gsd:step>合并数据并按时间排序</gsd:step>
    <gsd:step>输出格式化表格</gsd:step>
    <gsd:step>自动检测时间紧张度分析需求</gsd:step>
  </gsd:phase>

  <gsd:phase name="任务写入" order="2">
    <gsd:step>解析用户输入，提取任务名称和时间</gsd:step>
    <gsd:step>生成简洁标题 + 详细内容（见「标题与内容规则」）</gsd:step>
    <gsd:step>智能清单分配</gsd:step>
    <gsd:step>判断是否为历史任务</gsd:step>
    <gsd:step>创建任务（必须包含 --content）并处理完成状态</gsd:step>
  </gsd:phase>

  <gsd:phase name="项目管理" order="3">
    <gsd:step>获取所有项目清单</gsd:step>
    <gsd:step>分类展示活跃/已归档清单</gsd:step>
  </gsd:phase>

  <gsd:phase name="日程复盘" order="4">
    <gsd:step>并行获取今日任务（已完成+未完成）+ 历史7天数据 + 项目列表</gsd:step>
    <gsd:step>生成时间轴，识别 ≥30min 空白时段，智能推断推荐活动</gsd:step>
    <gsd:step>使用 AskUserQuestion 展示所有空白时段选项</gsd:step>
    <gsd:step>根据用户选择批量创建任务</gsd:step>
  </gsd:phase>
</gsd:workflow>

## 🌙 人性化关怀

> 详细规则见 `references/humanization.md`。核心原则：**自然、克制、优先关心人**。
>
> 关怀仅在三个节点输出：任务创建后、日程展示后、日程复盘结尾。每类关怀每会话最多 1 次。

## 🎭 输出风格

> 核心原则：**像一个有趣的室友在帮你管日程**，不是冷冰冰的管家。

**语气基调**：轻松俏皮、偶尔抖机灵、但不油腻不尬聊。

| 场景 | 示例 |
|------|------|
| 创建任务 | "✅ 搞定！**逛五角场** 19:00-20:39 → 红（娱乐）" |
| 创建无聊任务 | "好的好的，**写周报** 已安排上了（勇敢面对 💪）" |
| 创建娱乐任务 | "嘿嘿，**看电影** 已就位，玩得开心~" |
| 创建技术尝试类任务 | "✅ 记下了！**研究 PaperWM** → 蓝（学习），折腾使人快乐" |
| 历史任务 | "帮你补上了，过去的事就让它过去吧~" |
| 日程很空 | "今天意外的空旷，像周一早上的地铁 🚇" |
| 日程很满 | "今天塞得有点满...注意留白给自己喘口气" |
| 深夜操作 | "这个点还在安排日程？卷王本王了 🌙" |
| 没有任务 | "一片空白，自由如风~" |

**禁止**：
- ❌ 每句话都强行加俏皮（正常信息直接说）
- ❌ 用过时的网络用语（"亲"、"yyds" 等）
- ❌ 过度使用 emoji（一句话最多 1 个）
- ❌ 说教语气（"你应该..."）

<commands>
```
/tt               # 主命令，显示今日任务
/tt today         # 今日任务
/tt tomorrow      # 明日任务
/tt add <任务>     # 创建任务
/tt done <任务ID>  # 完成任务
/tt review        # 日程复盘，补全空白时段
```
</commands>

## CLI 命令映射

所有操作通过 `tt` CLI 完成，替代 MCP 工具调用：

> **⚡ 效率提示**：批量操作（更新/删除/移动）需要 task ID 时，优先使用 `--json` 标志获取结构化数据，一步拿到 ID，无需文本解析。
> 支持 `--json` 的命令：`task-undone`、`task-list`、`project-tasks`

### 任务查询

**`--query` 支持的预设值**：`today`、`tomorrow`、`last24hour`、`next24hour`、`last7day`、`next7day`

> ⚠️ **不支持 `yesterday`！** 查询非今日任务必须使用 `--start` 和 `--end` 参数。

| 场景 | CLI 命令 |
|------|---------|
| 查看未完成今日任务 | `tt task undone --query today` |
| 查看未完成今日任务（结构化） | `tt task undone --query today --json` ⚡ |
| 查看未完成昨日任务 | `tt task undone --start 2026-04-03 --end 2026-04-04` |
| 查看未完成指定日期任务 | `tt task undone --start <startDate> --end <endDate>` |
| 查看已完成今日任务 | `tt task completed --start <date> --end <date>` |
| 搜索任务（全清单，搜全） | `tt task-search <keyword>`（CLI ≥0.1.2 已遍历所有清单兜底，覆盖无日期/非收集箱任务，并匹配 tags） |
| 搜索任务（结构化） | `tt task-search <keyword> --json` ⚡（CLI ≥0.1.2） |
| 按ID查找任务 | `tt task-find <taskId>` |
| 创建任务（不含时间） | `tt task-add <title> -p <projectId> --content <text>` |
| 创建任务（两步法，含时间） | 先 `tt task-add`，再 `tt task-update <taskId> -p <projectId> --startDate 'YYYY-MM-DDTHH:mm' --dueDate 'YYYY-MM-DDTHH:mm'` |
| 批量创建任务 | `echo '[...]' | tt task-batch-add --stdin` |
| 完成任务 | `tt task-done <projectId> <taskId>` |
| 批量完成 | `tt task-batch-done <projectId> --task-ids <ids>` |
| 更新任务 | `tt task-update <taskId> -p <projectId> [options]` |
| 列出项目 | `tt project-list` |
| 查看项目任务 | `tt project-tasks <projectId>` |
| 查看项目任务（结构化） | `tt project-tasks <projectId> --json` ⚡ |
| 筛选任务（结构化） | `tt task-list -p <projectId> --json` ⚡ |
| 用户信息 | `tt user-pref` |
| 登录 | `tt login` |
| 登录状态 | `tt whoami` |
| 切换区域 | `tt config --region cn\|global` |

## 核心规则

### 全文搜索（task-search 已全清单覆盖）

**CLI ≥ 0.1.2 的 `tt task-search` 已遍历所有清单兜底**：合并「按日期未完成 + 已完成 + 各项目 `/project/{id}/data`」并按 id 去重，覆盖「无日期 + 非收集箱清单」的任务（典型如「任务池」、五色清单里随手记的待办），关键词同时匹配 `title + content + tags`，并支持 `--json` 输出结构化数据。**直接用即可，无需手动遍历清单。**

> ⚠️ **旧版（< 0.1.2）有盲区**：只查「收集箱 + 近期已完成 + 带日期任务」，搜不到「非收集箱 + 无日期 + 未完成」的任务，且不支持 `--json`。若发现搜不全、或 `--json` 报错，多半是 CLI 太旧 → `npm i -g @wangjs-jacky/ticktick-cli` 升级。临时兜底：`tt project-list` 拿全部活跃清单 ID（含「任务池」，动态获取勿硬编码）→ 并行 `tt project-tasks <id> --json` → 本地过滤 `title+content+tags`。

### 标题与内容规则

**创建任务时必须同时填写标题和内容，禁止只填标题。**

**标题（title）**：简短概括，≤15 字，一眼能看出做了什么
**内容（content）**：具体的细节描述，用 Markdown 列表形式

| 场景 | 标题（title） | 内容（--content） |
|------|--------------|-------------------|
| 用户说"我刚发布了一个包 v1.1.1" | 发布 jacky-skills v1.1.1 | `- 修复了 skill 链接问题` |
| 用户说"优化了 tt-cli 的性能" | tt-cli 性能优化 | `- 修复 --json 输出污染问题` |
| 用户说"研究了 PaperWM" | 研究 PaperWM | `- 了解 PaperWM 的窗口管理概念` |
| 用户说"开了一下午会" | 团队周会 | `- 讨论了 Q2 计划` |
| 简单任务（如"吃午饭"） | 午饭 | 可留空，不加 --content |

> ⚠️ **多行 content 禁止用命令行 `--content` 直接传**（换行会破坏参数解析，CLI 报 Usage 或静默丢内容）。**多行/列表要点必须走 `task-batch-add` 或 `task-batch-update` 的 `--stdin` JSON 方式**，详见下「多行内容写法」。

**内容生成规则**：
1. 根据用户描述、对话上下文，总结 2-5 个要点
2. 使用 Markdown 列表格式（`- 要点`）
3. 每个要点简洁明了，不超过一行
4. 如果用户只给了简单的任务名（如"午饭"、"休息"），可以不加 content

**批量创建时**：JSON 数组中每个任务对象也必须包含 `content` 字段（除非是简单生活类任务）。

#### 多行内容写法（`--content` 只传单行）

CLI 的 `--content` 参数在 shell 命令行里只能安全传**单行**文本。凡是内容需要 2 行以上（Markdown 列表要点），一律走 `--stdin` JSON：

**单条任务 + 多行 content**（创建后补内容）：
```bash
tt task-add "标题" -p <projectId>            # 先建任务，得到 taskId
python3 - <<'PY' | tt task-batch-update --stdin
import json
print(json.dumps([{
  "id": "<taskId>",
  "projectId": "<projectId>",
  "content": "- 要点1\n- 要点2\n- 要点3"
}], ensure_ascii=False))
PY
```

**批量创建（含多行 content）**：
```bash
python3 - <<'PY' | tt task-batch-add --stdin
import json
print(json.dumps([{
  "title": "标题",
  "projectId": "<projectId>",
  "content": "- 要点1\n- 要点2"
}], ensure_ascii=False))
PY
```

> 不要用 `$'...\n...'` 或字面 `\n` 传给命令行 `--content`——实测都会被参数解析吃掉或报 Usage。用 Python `json.dumps(ensure_ascii=False)` 生成 JSON 最稳（自动处理换行与中文）。

### 时区处理

CLI 输出的时间已自动格式化为 `HH:mm-HH:mm`，但仍需注意 API 返回原始数据为 UTC。

### projectId 缓存策略

首次使用时运行 `tt project-list` 获取清单并缓存映射：

```bash
tt project-list
```

**缓存规则**：同一会话内只调一次 `tt project-list`，后续直接用缓存。仅在命令报 projectId 无效时才刷新。

### 智能清单分配

**优先规则：AI 自动分配的任务（如需求拆分、自动规划等由大模型生成的批量任务）统一放入「大模型」清单，不走下方的关键词匹配。** 仅当用户手动指定清单或单条手动创建任务时，才使用关键词匹配。

| 任务关键词 | 清单 | projectId |
|-----------|------|-----------|
| 睡觉、休息 | 紫（休息） | 紫的 ID |
| 午休、午睡、午饭、午餐、早饭、早餐、晚饭、晚餐、吃饭 | 黄（午休） | 黄的 ID |
| 游戏、娱乐、看电影、刷剧 | 红（娱乐） | 红的 ID |
| 研究、调研、学习、尝试、折腾、探索、阅读 | 蓝（学习） | 蓝的 ID |
| AI 自动分配的任务（批量拆分/规划） | 大模型 | 大模型的 ID |
| 其他 | Inbox | inbox |

> 映射通过 `tt project-list` 动态获取，禁止硬编码。

### 时间解析

自然语言 → CLI 日期参数：
- "晚上7:30" → `--startDate '2026-04-04T19:30'`
- "下午3点" → `--startDate '2026-04-04T15:00'`
- "早上9点到10点" → `--startDate '2026-04-04T09:00' --dueDate '2026-04-04T10:00'`

> ⚠️ **重要**：`task-add` 的 `--startDate`/`--dueDate` 参数有 bug，创建时传入会被忽略。必须分两步：
> 1. `tt task-add "标题" -p <projectId> --content "内容"`（不含日期）
> 2. `tt task-update <taskId> -p <projectId> --startDate 'YYYY-MM-DDTHH:mm' --dueDate 'YYYY-MM-DDTHH:mm'`
>
> 日期格式用 `'YYYY-MM-DDTHH:mm'`，**不要带时区后缀**（`+08:00` 会被 shell 解析为选项导致报错）。

## 执行流程

### Phase 0: 前置检测

```bash
# 检测 CLI
tt --version

# 检测登录状态
tt whoami
```

**未安装时引导**：
```bash
npm install -g @wangjs-jacky/ticktick-cli
tt login
```

**未登录时引导**：
```bash
tt login
# 需要 Client ID 和 Client Secret
# 注册应用：https://developer.ticktick.com/app
# Redirect URI: http://localhost:3000/callback
```

> 🛑 **Checkpoint**：安装/登录完成后验证连接

### Phase 1: 任务读取

**并行调用**（Bash 并行）：

**查询今日任务**：
```bash
tt task undone --query today &
tt task completed --start 2026-04-04 --end 2026-04-05 &
tt project-list &
wait
```

**查询指定日期任务**（如"昨天"、"前天"等，禁止用 `--query yesterday`）：
```bash
# --query 仅支持: today, tomorrow, last24hour, next24hour, last7day, next7day
# 非 today/tomorrow 的查询必须用 --start/--end 日期范围
tt task undone --start 2026-04-03 --end 2026-04-04 &
tt task completed --start 2026-04-03 --end 2026-04-04 &
tt project-list &
wait
```

**处理**：
1. 解析 CLI 输出，提取任务列表
2. 合并已/未完成，按开始时间排序
3. 输出表格，标注状态（✅已完成 / ⏳待办 / ⚠️已过期 / 🔜即将）

**自动触发时间分析**（用户问"紧不紧张/满不满/够不够"时）：

| 紧张度 | 判定 | 标准 |
|--------|------|------|
| 🟢 宽松 | 任务时长 < 可用时间 60% | |
| 🟡 适中 | 占 60%-80% | |
| 🔴 紧张 | > 可用时间 80% | |

可用时间 = 当前时间到 22:00。

> 🛑 **Checkpoint**：展示结果后等待用户下一步指令

### Phase 2: 任务写入

**创建任务**：
1. 解析用户输入 → 提取任务名 + 时间
2. 生成简短标题（≤15字）+ 总结要点作为 content（见「标题与内容规则」）
3. 缺少必填字段时用 `AskUserQuestion` 询问
4. 智能清单分配
5. 判断是否历史任务（dueDate < 当前时间）

**历史任务**（时间已过）：
```bash
# 第一步：创建任务（不含日期）
tt task-add "简短标题" -p <projectId> --content "要点1\n要点2"
# 第二步：补上时间
tt task-update <taskId> -p <projectId> --startDate '<start>' --dueDate '<end>'
# 第三步：标记完成
tt task-done <projectId> <taskId>
```

**未来任务**（时间未到）：
```bash
# 第一步：创建任务（不含日期）
tt task-add "简短标题" -p <projectId> --content "要点1\n要点2"
# 第二步：补上时间
tt task-update <taskId> -p <projectId> --startDate '<start>' --dueDate '<end>'
```

**批量创建**（日程复盘等场景）：
```bash
echo '[{"title":"简短标题","content":"- 要点1\n- 要点2","projectId":"...","startDate":"...","dueDate":"..."}]' | tt task-batch-add --stdin
```

**修改任务**：
- 用户说"更新/修改" → 直接搜索相似任务，确认修改细节
- `tt task-update <taskId> -p <projectId> [options]`

> 🛑 **Checkpoint**：执行修改前确认操作内容

### Phase 3: 项目管理

```bash
tt project-list
```

### Phase 4: 日程复盘

**触发词**：一天结束、日程复盘、时间都去哪了、今天干了什么、补全日程、完善行程、回顾今天

**Step 1** — 并行获取 4 类数据：
```bash
tt project-list &
tt task undone --query today &
tt task completed --start 2026-04-04 --end 2026-04-05 &
tt task completed --start 2026-03-28 --end 2026-04-04 &
wait
```

**Step 2** — 分析 + 展示：
1. 合并任务，按时间排序
2. 生成 06:00-22:00 时间轴，识别 ≥30min 空白时段
3. 智能推断推荐活动：

| 时间段 | 推断优先级 |
|--------|-----------|
| 06:00-09:00 | 相邻任务 > 习惯 > 默认（通勤/早餐） |
| 11:30-14:00 | 习惯 > 默认（午餐/午休） |
| 17:00-19:00 | 相邻任务 > 习惯 > 默认（下班通勤） |
| 19:00-22:00 | 习惯 > 默认（晚餐/娱乐） |

推断权重：相邻任务 0.4 / 历史习惯 0.4 / 时段特征 0.2

4. 用 `AskUserQuestion` 直接展示所有空白时段选项

**Step 3** — 批量创建：
```bash
echo '[<tasks json array>]' | tt task-batch-add --stdin
# 历史任务创建后批量标记完成
tt task-batch-done <projectId> --task-ids <ids> --force
```

> 🛑 **Checkpoint**：批量创建前展示汇总确认

## Check List

- [ ] tt CLI 已安装且已登录
- [ ] 首次查询并行获取数据
- [ ] 时间已从 UTC +8 转换为上海时区
- [ ] 非今日查询使用 --start/--end 日期范围（禁止 --query yesterday/today 以外的值）
- [ ] 表格包含清单名称列
- [ ] projectId 已缓存，非首次不重复调 tt project-list
- [ ] 创建任务：判断是否为历史任务，自动标记完成
- [ ] 修改操作前已确认
- [ ] 日程复盘：主会话直接执行（不使用 Agent）
- [ ] 日程复盘：并行获取 4 类数据
- [ ] 日程复盘：时区 +8 转换正确
- [ ] 日程复盘：基于相邻任务/历史习惯/时段特征智能推断
- [ ] 日程复盘：AskUserQuestion 直接展示所有空白时段选项
- [ ] 日程复盘：批量创建使用 tt task-batch-add
- [ ] 人性化：深夜操作（23:00-06:00）输出休息提醒，每会话最多 1 次
- [ ] 人性化：凌晨时段任务（00:00-06:00）关心睡眠状况
- [ ] 人性化：过载/连续工作时善意建议，不说教不轰炸
- [ ] 人性化：完成成就时真诚庆祝
