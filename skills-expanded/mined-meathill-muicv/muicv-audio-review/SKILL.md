---
name: muicv-audio-review
description: 录音复盘。用户拖一段已有录音（自己面试 / 客户沟通 / 演讲 / 答辩等）进 muicv，skill 调 STT 转写后按场景分析（STAR 完整度 / 表达冗余 / 填充词 / 时长 / 互动），把转写全文 + 分析写到 `audio-reviews/<source>-<date>.md`。触发词：录音复盘、分析这段录音、拖了一段音频、复盘音频、analyze recording、transcribe and review、聊天录音、客户沟通录音、演讲录音、答辩录音。仅 muicv 桌面 app 可用（需要本地文件读取）。
---

# muicv-audio-review · 录音复盘

把用户的真实录音转写后做复盘分析。跟 [muicv-debrief](../muicv-debrief/SKILL.md)（用户口述写下来）的差别：

| | muicv-audio-review | muicv-debrief | muicv-interview |
|---|---|---|---|
| 输入 | 已有的音频文件 | 用户当下口述 | 实时模拟（语音 / 打字）|
| 关键能力 | STT 转写 + 文本分析 | 引导用户回忆 | 扮演面试官 |
| 输出 | `audio-reviews/<source>-<date>.md` | `debriefs/<company>-<date>.md` | `interviews/<company>-...md`（题目打分）|
| 适合 | 真实场景留了录音的复盘 | 真实场景没录音的复盘 | 面试**前**练习 |

**关键约束**：录音文件**只在用户本地或 muicv 服务器**（取决于用户的 STT 偏好——本地 whisper.cpp 或云端 Workers AI Whisper），**不**上传到任何第三方。如果用户没装本地引擎且没用过云端，先告知再确认。

---

## 工作流

### 第一步：收集背景（一次问完，不挤牙膏）

跟用户说"我帮你复盘这段录音。先一次答几个问题"，然后列：

1. **音频文件路径**（必填）
   - 用户拖进来 → 路径自动填
   - 用户复制粘贴路径 → 直接拿
   - 用户给个文件名（如 "我桌面的 interview.mp3"）→ 让用户给完整路径，**不要猜**
2. **录音场景**（必填，决定分析维度）：
   - `interview`（求职面试 / 答辩）
   - `client`（客户沟通 / 销售 / 客户成功）
   - `pitch`（产品演示 / 路演 / 演讲）
   - `meeting`（会议 / 一对一 / 项目讨论）
   - `other`（自由文本，用户描述）
3. **目的**（可空）：你想优化什么——内容质量？表达流畅？说话速度？被打断处理？
4. **关联背景**（可空）：哪个公司 / 客户 / 演讲场合？时间？

不要一条一条挤牙膏，列出来让用户一次性填。

### 第二步：转写

调 agent tool `transcribe_audio_file`：

```typescript
transcribe_audio_file({ filePath: "<绝对路径>", language: null /* auto-detect */ })
```

**不要假装转写完成**——必须等工具返回。返回结构：

```json
{
  "transcript": "完整转写文本",
  "durationMs": 543210,
  "language": "zh",
  "segments": [
    { "start": 0.0, "end": 5.2, "text": "今天面试..." },
    ...
  ]
}
```

工具失败的几种情况：
- 文件不存在 → `录音失败：找不到文件 ...`
- 转码失败 → `录音失败：音频解码失败 ...`（用户音频可能是非常规格式，让用户先转 wav / mp3）
- 云端 STT 余额不足 → 提示用户充值或下载本地引擎
- 本地引擎缺装件 → 自动 fallback 云端（M3 行为）

工具返回 transcript 后，**先把前 200 字给用户看**："这是不是你想复盘的内容？"——防拖错文件。

### 第三步：分析（按场景维度选）

每种场景分析维度不同。**不要全维度套**，按 step 1 的 scenario 选：

#### `interview`（求职面试）
- **STAR 完整度**：每个回答有 Situation / Task / Action / Result 吗？哪个段落 R 缺失？
- **量化指标**：用了几个 **outcome 数字**（% / 倍数 / 前后对比 / 收益变化 / 排名）？是不是关键 Action 全是空话动词（"负责"、"推动"、"参与"）？

> **「量化」= Action 之后产出的 outcome 指标**（成果/效率/收益变化），不是 scope/编制/时长/件数。
> ✅ 转化率 +12% · 退货率 8%→3% · P75 800ms→320ms · GMV ¥80k→¥260k · 排名 #1（绑结果）
> ❌ "覆盖 3 个站点" · "带 4 人团队" · "维护 30+ 仓库" · "做了 3 年"——这些是 scope，**不算量化**，应当出现在 Action 里。
> 素材里没有 outcome 数字时，保留定性描述，**不要为了凑量化而编数字、也不要把 scope 升格成量化**。
> 完整定义见 [docs/quantification-guideline.md](../../docs/quantification-guideline.md)。

- **填充词频次**：嗯 / 那个 / 就是 / um / like 平均几秒一次？> 1 次/15s 时面试官会扣分
- **时长**：BQ 题 60-90s 合理；< 30s 太浅；> 3min 啰嗦。看 segments 拍判断
- **追问应对**：被打断 / 追问时是接住了还是被带偏？
- **关键词覆盖**：跟用户说的目标 JD 关键词覆盖了多少？

#### `client`（客户沟通 / 销售）
- **需求澄清**：开场有没有问 client 的痛点 / 现状 / 期望？还是直接推方案
- **异议处理**：client 反对时是直接 push back，还是先承认再引导？
- **推进度**：有没有明确 next step（"周三 demo" / "拉个 group call"），还是漂着结束
- **占场比**：你说话占多少 vs client 说话占多少？粗略估（segments 时间戳 / 关键词）

#### `pitch`（演讲 / 演示 / 路演）
- **开场**：3 句话内有没有抛出钩子（problem / number / 故事）？
- **节奏**：每分钟多少字？120-180 字/min 合理
- **高潮 / 收尾**：有 takeaway 句子吗？还是淡出

#### `meeting`（一对一 / 团队会议）
- **目的明确**：开场 30s 内有 agenda 吗？
- **决策 / next step**：会议输出是什么？有没有谁负责什么 by when

#### `other`
- 通用维度：表达冗余、停顿过长（segments 间隔 > 5s 多次）、关键论点是不是被埋

每条分析**引用 transcript 具体片段**（用 segment 时间戳 + 原话），不要泛泛而谈。

### 第四步：写到 `audio-reviews/<source>-<date>.md`

文件命名：`audio-reviews/<source-slug>-<YYYY-MM-DD>.md`

- `source-slug`：从 step 1 的"关联背景"或文件名推：`google-interview` / `acme-client-call` / `keynote-2026q2`
- 同一天同一 source 第二次复盘 → `-r2` `-r3` 后缀

### 文件格式

```markdown
---
type: audio_review
scenario: interview                  # interview / client / pitch / meeting / other
source: ~/Downloads/interview.mp3    # 原音频文件路径（用户视角，便于回放）
duration_min: 9
date: 2026-05-06                     # 复盘当天
language: zh                         # transcribe_audio_file 返回的
related_target: targets/google-senior-fe.md   # 可选，如果是面试录音
---

## 背景

简短 1-2 段：什么场景、目的、相关人或岗位。

## 转写全文

> 折叠提示：长录音的 transcript 全文放这里。Markdown 可以让用户在编辑器里搜段落。

[Whisper 转写结果，按 segment 段落断行，每段前面带 [mm:ss] 时间戳]

例：
[00:00] 你好，我是张三。今天来面试 Google 高级前端工程师...
[01:23] 我之前在 ACME 做的项目主要是设计系统迁移...

## 分析

按场景维度逐条评，每条**引用具体片段**（带时间戳）：

### STAR 结构
- Q1 [02:30 - 04:15]: S/T/A 完整，但 R 没量化（"提升了用户体验"应该改成"P75 加载时间从 800ms 降到 320ms"）
- Q2 [05:00 - 06:30]: 全是 Action 描述，缺 Situation（面试官不知道你为什么做这件事）

### 填充词
- "嗯/那个" 共 28 次，平均 19 秒一次。集中在 [03:00-04:00] 这段（被追问时）

### 时长
- 平均答题时长 95 秒，整体 OK
- Q3 [06:30 - 09:50] 答了 3 分多，偏长——可以剪一半

### 追问应对
- [04:50] 面试官追问"为什么不用 X 方案"，你 reflexively 解释了 Y 方案的好处，但没正面回应 X 的问题。下次先承认追问的合理性再分析

## 整体感觉

简短 2-3 句：哪几道答得稳，哪几道翻车，整体水平评估。**不下"过/挂"结论**。

## 改进点

1-3 条具体可执行的。每条都是**可以练**的（"BQ 答 R 时先准备 1 个 **outcome 量化指标**——% / 前后对比 / 收益变化，不是'3 个站点'这种 scope"），不是空话（"加强表达"）。

## 下一步建议

- 简历有具体问题 → muicv-critique
- 想再练一轮模拟 → muicv-interview
- 想沉淀成 debrief → muicv-debrief（或者直接说"基于这份 audio-review 写一份 debrief"）
```

写完文件后**告诉用户路径**，不要默默写。

### 第五步：复盘讨论

文件落盘后，给用户口头总结：

1. **关键改进点**（1-3 条，最有价值的）
2. **整体水平判断**（达标 / 边缘 / 偏弱；不下结论）
3. **下一步建议**（参考 SKILL 文件结尾的 next step 列表）

如果用户要进一步分析具体某段（"[03:30] 那段我答得啥意思都不知道"）—— 直接 grep transcript / segments 把那段贴出来，跟用户讨论。

---

## 角色 / 语气

- **中立分析者**，跟 muicv-debrief 同款
- **基于 transcript 事实分析**，不替用户编故事
- 不灌鸡汤、不打击；用户情绪激动 → 共情一两句再分析
- 引用片段时用 `[mm:ss]` 时间戳，让用户能精确回放对照

---

## 边界

- **录音文件位置**：默认在用户本地 / muicv 服务器（取决于 STT 偏好）。**不**传到第三方
- **不替用户回放音频**：muicv 不内置音频播放器；需要回听让用户在系统播放器打开
- **不强行覆盖现有 audio-review 文件**：同 source-date 已存在 → 加 `-r2` 后缀
- **不下"做得好/做得不好"的判决**：列事实 + 改进点
- **不假装能听出语调 / 情绪**：whisper 只给文本，**不要**说"你那段听起来很紧张"——除非用户自己说他紧张
- **不替用户写 debrief 文件**：跟 muicv-debrief 是不同 skill，硬区分两个目录避免混

---

## 与其他 skill 的协作

- **录音 → 文字 + 分析** ← 你现在这里
- 录音里发现简历有空话 → `muicv-critique`
- 录音是面试，想再练一轮 → `muicv-interview`
- 想把 audio-review 转成 debrief 形态（按公司 / 轮次结构化）→ `muicv-debrief`
- 多份 audio-review 想看趋势 → `muicv-core` 做总结

---

## 调用示例

```
用户：我桌面有段昨天面试 Google 的录音，帮我复盘下：~/Desktop/google-mock.m4a

Claude:
  1. 一次问完背景：场景 / 目的 / 关联岗位
     用户答：interview / 想看 BQ 答得怎么样 / Google Senior FE
  2. 调 transcribe_audio_file({ filePath: "~/Desktop/google-mock.m4a" })
     等待返回 transcript + segments
  3. 把前 200 字给用户看："是这段吗？"
     用户：是
  4. 按 interview 维度分析：
     - STAR：Q2 R 缺量化
     - 填充词：32 次 / 9 分钟，> 1 次/15s
     - 时长：Q3 偏长 3:20
  5. 写到 audio-reviews/google-mock-2026-05-06.md
  6. 整体：BQ 中等，技术深度 OK，主要问题是没量化 R
  7. 建议：练 muicv-interview 的 BQ 模式 5 道题，每题先准备数字
```
