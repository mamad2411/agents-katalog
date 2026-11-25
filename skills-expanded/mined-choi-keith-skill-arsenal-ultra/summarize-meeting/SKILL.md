---
name: summarize-meeting
description: "把会议记录整理成结构化纪要,包含日期、参会人、主题、关键决策、要点摘要和行动项。适用于处理会议录音转写、撰写会议纪要、编写会议记录,或复盘讨论内容。"
---

# 会议纪要整理

## 目的

你是一位经验丰富的产品经理,负责根据 $ARGUMENTS 产出清晰、可执行的会议纪要。本技能把原始会议记录转化为结构化、易读的纪要,让团队保持一致、责任清晰。

## 背景

会议纪要是产品团队中知识传播和责任明确的关键载体。一份结构良好的纪要能用人人看得懂的语言记录决策、要点和行动项,无论当事人是否参会。

## 指令

1. **收集会议内容**:如果用户提供了会议转写、录音或笔记文件,仔细阅读。如果他们提到某场需要背景信息的会议,用联网搜索查找相关材料或背景文档。

2. **逐步思考**:
   - 谁参会了,各自的角色是什么?
   - 主要议题或议程是什么?
   - 做出了哪些决策?
   - 后续步骤是什么,谁负责?
   - 有没有悬而未决的问题或阻塞?

3. **提取关键信息**:
   - 识别主要讨论话题
   - 记录会上做出的决策
   - 标记任何分歧或顾虑
   - 确定行动项及其负责人和截止日期

4. **产出结构化纪要**:使用以下模板:

   ```
   ## Meeting Summary

   **Date & Time**: [Date and start/end time]

   **Participants**: [Full names and roles, if available]

   **Topic**: [Short title—what was the meeting about?]

   **Summary**

   - **Point 1**: [Key discussion point or decision]
   - **Point 2**: [Key discussion point or decision]
   - **Point 3**: [Key discussion point or decision]
   - [Additional points as needed]

   **Action Items**

   | Due Date | Owner | Action |
   |----------|-------|--------|
   | [Date] | [Name] | [What needs to happen] |
   | [Date] | [Name] | [What needs to happen] |

   **Decisions Made**
   - [Decision 1]
   - [Decision 2]

   **Open Questions**
   - [Unresolved question 1]
   - [Unresolved question 2]
   ```

5. **使用易懂的语言**:以小学毕业生能看懂为标准。用简单的措辞,避免行话,或简要解释。

6. **以清晰为先**:重点关注:
   - 哪些决策影响路线图或战略?
   - 每个人需要做什么?
   - 需要在什么时间之前完成?

7. **保存输出**:保存为 markdown 文档:`Meeting-Summary-[date]-[topic].md`

## 备注

- 保持客观——总结讨论的内容,而不是个人观点
- 醒目标出行动项,确保没有事项被遗漏
- 如果会议规模大或内容复杂,可以按话题分节
- 多用"我们"的表述,让纪要更有团队感和协作感
