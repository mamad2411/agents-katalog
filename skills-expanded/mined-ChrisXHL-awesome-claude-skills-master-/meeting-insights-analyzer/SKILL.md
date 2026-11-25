---
name: meeting-insights-analyzer
description: 分析会议记录和录音，发现行为模式、沟通见解和可操作的反馈。确定您何时避免冲突、使用填充词、主导对话或错过倾听机会。非常适合寻求提高沟通和领导技能的专业人士。
---

# 会议见解分析器

此技能将您的会议记录转化为关于您沟通模式的可操作见解，帮助您成为更有效的沟通者和领导者。

## 何时使用此技能

- 分析您在多次会议中的沟通模式
- 获取关于您的领导和促进风格的反馈
- 识别您何时避免艰难的对话
- 了解您的说话习惯和填充词
- 跟踪沟通技能随时间的提高
- 准备包含具体示例的绩效评估
- 指导团队成员的沟通风格

## 此技能做什么

1. **模式识别**: 识别会议中经常出现的行为，如：
   - 冲突避免或间接沟通
   - 说话比例和轮流发言
   - 提问与陈述模式
   - 积极倾听指标
   - 决策方法

2. **沟通分析**: 评估沟通有效性：
   - 清晰度和直接性
   - 填充词和模糊语言的使用
   - 语气和情绪模式
   - 会议控制和促进

3. **可操作的反馈**: 提供带有时间戳的具体示例：
   - 发生了什么
   - 为什么这很重要
   - 如何改进

4. **趋势跟踪**: 在分析多次会议时比较随时间变化的模式

## 如何使用

### 基本设置

1. 将您的会议记录下载到文件夹 (例如 `~/meetings/`)
2. 在 Claude Code 中导航到该文件夹
3. 请求您想要的分析

### 快速入门示例

```
Analyze all meetings in this folder and tell me when I avoided conflict.
```

```
Look at my meetings from the past month and identify my communication patterns.
```

```
Compare my facilitation style between these two meeting folders.
```

### 高级分析

```
Analyze all transcripts in this folder and:
1. Identify when I interrupted others
2. Calculate my speaking ratio
3. Find moments I avoided giving direct feedback
4. Track my use of filler words
5. Show examples of good active listening
```

## 说明

当用户请求会议分析时：

1. **发现可用数据**
   - 扫描文件夹中的记录文件 (.txt, .md, .vtt, .srt, .docx)
   - 检查文件是否包含说话者标签和时间戳
   - 确认会议的日期范围
   - 在记录中识别用户的姓名/标识符

2. **澄清分析目标**
   
   如果未指定，询问他们想了解什么：
   - 具体行为 (冲突避免、打断、填充词)
   - 沟通有效性 (清晰度、直接性、倾听)
   - 会议促进技能
   - 说话模式和比例
   - 改进的增长领域
   
3. **分析模式**

   对于每个请求的见解：
   
   **冲突避免**:
   - 寻找模糊语言 ("maybe", "kind of", "I think")
   - 间接措辞而不是直接请求
   - 当紧张局势出现时改变话题
   - 没有承诺的同意 ("yeah, but...")
   - 不解决明显的问题
   
   **说话比例**:
   - 计算说话时间的百分比
   - 统计打断次数 (由用户打断和打断用户)
   - 测量平均说话轮次长度
   - 跟踪提问与陈述的比例
   
   **填充词**:
   - 统计 "um", "uh", "like", "you know", "actually", 等
   - 注意每分钟或每轮说话的频率
   - 识别它们增加的情况 (紧张、不确定)
   
   **积极倾听**:
   - 引用他人先前观点的提问
   - 解释或总结他人的想法
   - 建立在他人的贡献之上
   - 提出澄清问题
   
   **领导与促进**:
   - 决策方法 (指令性 vs. 协作性)
   - 如何处理分歧
   - 包含较安静的参与者
   - 时间管理和议程控制
   - 后续行动和行动项目的清晰度

4. **提供具体示例**

   对于发现的每个模式，包括：
   
   ```markdown
   ### [Pattern Name]
   
   **发现**: [One-sentence summary of the pattern]
   
   **频率**: [X times across Y meetings]
   
   **示例**:
   
   1. **[Meeting Name/Date]** - [Timestamp]
      
      **发生了什么**:
      > [Actual quote from transcript]
      
      **为什么这很重要**:
      [Explanation of the impact or missed opportunity]
      
      **更好的方法**:
      [Specific alternative phrasing or behavior]
   
   [对 2-3 个最强示例重复]
   ```

5. **综和见解**

   在分析所有模式后，提供：
   
   ```markdown
   # 会议见解摘要
   
   **分析期间**: [Date range]
   **分析的会议**: [X meetings]
   **总时长**: [X hours]
   
   ## 识别的关键模式
   
   ### 1. [Primary Pattern]
   - **观察到**: [What you saw]
   - **影响**: [Why it matters]
   - **建议**: [How to improve]
   
   ### 2. [Second Pattern]
   [Same structure]
   
   ## 沟通优势
   
   1. [Strength 1 with example]
   2. [Strength 2 with example]
   3. [Strength 3 with example]
   
   ## 增长机会
   
   1. **[Area 1]**: [Specific, actionable advice]
   2. **[Area 2]**: [Specific, actionable advice]
   3. **[Area 3]**: [Specific, actionable advice]
   
   ## 说话统计
   
   - 平均说话时间: [X% of meeting]
   - 提问: [X per meeting average]
   - 填充词: [X per minute]
   - 打断: [X given / Y received per meeting]
   
   ## 下一步
   
   [3-5 concrete actions to improve communication]
   ```

6. **提供后续选项**
   - 在未来的会议中跟踪这些相同的指标
   - 深入研究特定会议或模式
   - 与行业基准进行比较
   - 创建个人沟通发展计划
   - 为绩效评估生成摘要

## 示例

### 示例 1: 冲突避免分析 (受 Dan Shipper 启发)

**用户**: "I download all of my meeting recordings and put them in a folder. Tell me all the times I've subtly avoided conflict."

**输出**: 
```markdown
# 冲突避免模式

在 15 次会议中发现 23 个实例，其中您使用了间接沟通或避免直接解决紧张局势。

## 模式: 对关键反馈含糊其辞

**频率**: 7 次会议中 8 次

**示例 1: 与 Sarah 的 1:1** - 00:14:32

**发生了什么**:
> "So, I was thinking... maybe we could, like, potentially 
> consider looking at the timeline again? I mean, if you 
> think that makes sense. But whatever you think is best!"

**为什么这很重要**:
您需要指出 Sarah 的项目落后于计划，但模糊的语言 ("maybe", "potentially", "if you think") 和最后的偏转 ("whatever you think") 使她很容易忽视紧迫性。

**更好的方法**:
"Sarah, the project is two weeks behind schedule. We need to 
discuss what's blocking progress and create a new timeline 
today."

[其他示例...]

## 建议

1. **直接指出问题** 在第一句话中
2. **移除模糊词** 如 "maybe," "kind of," "sort of"
3. **提出具体问题** 而不是暗示
4. **安排艰难的对话** 而不是随意提出
```

### 示例 2: 领导力促进

**用户**: "Analyze my team meetings and tell me about my facilitation style."

**输出**: 提供有关以下内容的见解：
- 您与团队成员说话的比例 (60% vs. 40%)
- 您提问还是陈述 (3:1 比例)
- 您如何处理分歧 (倾向于太快解决)
- 谁说话最少以及您是否吸引他们
- 良好和错过的促进时刻的示例

### 示例 3: 个人发展跟踪

**用户**: "Compare my meetings from Q1 vs. Q2 to see if I've improved my listening skills."

**输出**: 创建比较分析，显示：
- 打断减少 (每次会议 8 次 → 3 次)
- 澄清问题增加 (每次会议 2 次 → 7 次)
- 在他人想法基础上构建的改进
- 显示差异的具体示例
- 剩余的增长领域

## 设置提示

### 获取会议记录

**来自 Granola** (订阅 Lenny 的时事通讯免费):
- Granola 自动转录您的会议
- 导出记录到文件夹: [Instructions on how]
- 将 Claude Code 指向该文件夹

**来自 Zoom**:
- 启用带有转录的云录制
- 会议后下载 VTT 或 SRT 文件
- 存储在专用文件夹中

**来自 Google Meet**:
- 使用 Google Docs 自动转录
- 将记录文档保存到文件夹
- 下载为 .txt 文件或授予 Claude Code 访问权限

**来自 Fireflies.ai, Otter.ai, 等**:
- 批量导出记录
- 存储在本地文件夹中
- 对文件夹运行分析

### 最佳实践

1. **一致命名**: 使用 `YYYY-MM-DD - Meeting Name.txt` 格式
2. **定期分析**: 每月或每季度审查趋势
3. **具体查询**: 每次询问一个行为以获得深度
4. **隐私**: 将敏感会议数据保留在本地
5. **行动导向**: 一次专注于一个改进领域

## 常见分析请求

- "When do I avoid difficult conversations?"
- "How often do I interrupt others?"
- "What's my speaking vs. listening ratio?"
- "Do I ask good questions?"
- "How do I handle disagreement?"
- "Am I inclusive of all voices?"
- "Do I use too many filler words?"
- "How clear are my action items?"
- "Do I stay on agenda or get sidetracked?"
- "How has my communication changed over time?"

## 相关用例

- 根据见解创建个人发展计划
- 准备带有示例的绩效评估材料
- 指导直接下属的沟通
- 分析销售或支持模式的客户电话
- 研究谈判策略和结果
