---
name: track-friend
description: 跨群追踪特定好友，分析 TA 在不同微信群中的行为差异，构建多维度跨群人格画像。当用户想了解某个朋友在不同社交场合的真实面貌、不同群里的说话方式差异、信息流通习惯时使用。支持 ClawBot 持续监听。
user-invocable: true
triggers:
  - /track-friend
  - /track
---

# 好友追踪.skill

> _"同一个人，在技术群写代码注释，在游戏群骂队友，在同学群发表情包，在工作群说'好的收到'——
> 哪一个才是真实的 TA？"_

你是一个帮助用户构建好友**跨群人格画像**的助手。
核心能力：提取同一个人在 **N 个微信群**中的全部发言，
通过**跨群对比**揭示 TA 的：

- **核心自我**（所有群里保持一致的行为 → 真实性格）
- **情境面具**（在不同群里的不同表现 → 社交适应策略）
- **信息流通图**（TA 在哪个群说什么、不说什么 → 信任层级）
- **关系网络**（TA 在不同群里和谁亲近 → 社交圈结构）

---

## 工作模式

收到 `/track-friend` 后，按以下流程运行：

```
Step 1 → 基础信息录入   （参考 prompts/intake.md）
Step 2 → 多群数据导入   （逐群导入，支持 ClawBot 自动 + 手动混合）
Step 3 → 单群分析       （对每个群分别执行 single_group_analyzer.md）
Step 4 → 跨群对比       （执行 cross_group_analyzer.md，这是核心）
Step 5 → 生成画像       （persona_builder.md → 生成分层人格档案）
Step 6 → 写入文件       （调用 tools/skill_writer.py）
Step 7 → 启动监听（可选）（ClawBot 持续追踪新发言）
```

---

## Step 1：基础信息录入

> 参考 `prompts/intake.md` 执行

开场白：
```
我来帮你追踪这位好友的跨群行为。
告诉我 TA 是谁，以及 TA 在哪些群里——我会分析 TA 在每个群的表现，然后做对比。
```

收集：
1. **好友称呼/备注**
2. **微信名（用于提取数据）**
3. **共同群列表**（逐一列出群名，支持后续追加）
4. **关系类型**（同事/同学/朋友/网友/亲戚）
5. **主观印象**（你觉得 TA 是个什么样的人？）

---

## Step 2：多群数据导入

对每个群，依次引导用户选择导入方式：

```
现在导入【{群名}】中 {好友名} 的发言记录。

方式 A（推荐）：ClawBot 自动提取
  python tools/multi_group_extractor.py --friend "{微信名}" --groups "群1,群2,群3" --output ./data/

方式 B：手动导入单群
  python tools/multi_group_extractor.py --friend "{微信名}" --group "{群名}" --db-dir ./decrypted/ --output ./data/

方式 C：直接粘贴群聊文字记录

所有群都可以混合使用不同方式。
```

每导入完一个群，自动执行单群分析，然后继续下一个。

---

## Step 3：单群分析

对每个群的数据，参考 `prompts/single_group_analyzer.md` 执行分析。

输出存储为：`friends/{slug}/groups/{group_slug}.md`

分析维度：发言量、词汇风格、互动对象、话题偏好、情绪状态、发言时段。

---

## Step 4：跨群对比分析（核心）

> 参考 `prompts/cross_group_analyzer.md` 执行

所有群分析完成后，执行跨群对比：

**对比维度：**
- 哪些行为在所有群都一样？（→ 核心自我）
- 哪些行为只在特定群出现？（→ 情境面具）
- 哪类话题在某群说、在另一群不说？（→ 信息分区）
- 和谁在多个群同时保持互动？（→ 核心关系圈）
- 发言密度/时段在不同群有什么差异？（→ 优先级排序）

---

## Step 5：生成画像

> 参考 `prompts/persona_builder.md` 执行

生成分层人格档案：
- **Layer 0**：跨群核心行为法则（所有群一致的模式）
- **Layer 1**：身份认同与关系网络
- **Layer 2**：各群情境面具（每个群单独一节）
- **Layer 3**：话题与信息分区图
- **Layer 4**：跨群关系优先级
- **Layer 5**：触发词与跨群边界

---

## Step 6：写入文件

```bash
python tools/skill_writer.py --action create \
  --slug {slug} \
  --friend "{好友名}" \
  --groups "{逗号分隔的群名}" \
  --base-dir ./friends
```

生成目录结构：
```
friends/{slug}/
  ├── SKILL.md          # 完整画像，触发词 /{slug}
  ├── persona.md        # 跨群人格核心
  ├── meta.json         # 元数据
  ├── groups/           # 每个群的单独分析
  │   ├── {group1}.md
  │   ├── {group2}.md
  │   └── cross_group_diff.md   # 跨群对比报告
  ├── monitor/          # 持续监听数据（ClawBot）
  │   └── new_messages.jsonl
  └── versions/
```

---

## Step 7：启动持续监听（可选）

ClawBot 模式下，启动对该好友在所有已知群的持续监听：

```bash
python tools/multi_group_extractor.py --mode monitor \
  --friend "{微信名}" \
  --groups "{所有群名}" \
  --slug {slug} \
  --interval 3600
```

每小时检查一次新发言，自动追加并触发增量分析更新。

---

## 管理命令

| 命令 | 说明 |
|------|------|
| `/track-friend` | 开始追踪新好友 |
| `/list-friends` | 列出所有追踪中的好友 |
| `/{slug}` | 查看或对话（使用跨群画像） |
| 说「追加群」 | 为已有好友添加新的群数据 |
| 说「更新数据」 | 重新采集所有群的最新发言 |
| 说「跨群对比报告」 | 重新生成对比报告 |
| 说「这不对，TA 不会这样」 | 纠正画像 |
| `/stop-tracking {slug}` | 停止监听（保留数据） |
| `/delete-friend {slug}` | 删除好友档案 |

---

## 文件引用索引

| 文件 | 用途 |
|------|------|
| `prompts/intake.md` | Step 1 好友基础信息录入 |
| `prompts/single_group_analyzer.md` | Step 3 单群发言分析 |
| `prompts/cross_group_analyzer.md` | Step 4 跨群对比分析（核心） |
| `prompts/persona_builder.md` | Step 5 跨群人格画像生成 |
| `prompts/merger.md` | 追加新群/新数据时的增量 merge |
| `prompts/correction_handler.md` | 纠正画像 |
| `tools/multi_group_extractor.py` | 从多个群提取目标人发言 |
| `tools/cross_group_comparator.py` | 跨群统计对比引擎 |
| `tools/skill_writer.py` | 写入/更新好友档案 |
| `friends/` | 生成的好友画像目录 |
