---
name: decision-questionnaire
description: "Turn an unanswerable decision into a questionnaire doc."
version: 1.0.0
author: "Matt Pocock (mattpocock/skills, to-questionnaire) + Hermes Agent"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [questionnaire, decision, async, stakeholder, discovery, communication]
    related_skills: [meeting-action-items, document-to-action-items]
---

# 决策问卷功能

该功能可将用户无法独立解答的问题转化为**问卷形式**：一种 Markdown 文档，可交由他人异步填写，也可在会议中共同完成。接收方拥有用户所缺乏的知识，而问卷则有助于将这些知识从中提取出来。

该功能基于 mattpocock/skills 项目采用 MIT 许可协议的 `to-questionnaire` 技能实现。

## 适用场景

- 决策需要依赖他人掌握的事实或判断力（如领域专家、利益相关方、供应商联系人或运维人员）；
- 用户表示“我需要就此事询问 X”或不断推迟决策，等待他人的意见；
- 为会议做准备，且需要获取明确的答复。

**注意**：如果答案可从环境中的资源（代码库、文档、网页等）中找到，则无需使用此功能——请先自行查找。

## 核心原则：询问发送对象，而非问题主题

用户确实无法回答与问题主题相关的问题（这正是该功能的意义所在），但他们始终能够回答关于**发送对象**的问题。只需通过两次简短的交流来询问相关内容：

1. **问卷将发送给谁？** 包括其角色、专业领域以及与用户的关系。这有助于确定问卷的表述风格及所需包含的背景信息量。在明确接收方是谁以及他们拥有而用户不具备哪些知识后即可完成此步骤。
2. **需要对方提供什么答复？** 即用户无法独立决定的具体事项或需要确认的事实。在列出用户离开时必须能够完成或做出的具体事项清单后即可完成此步骤。
接着**编写问卷**：根据以下结构，针对接收者现有知识与用户实际需求之间的差距来起草问题。将问卷内容写入当前目录下的 `decision-questionnaire-<slug>.md` 文件中（<slug>取自主题名称），并记录该文件的绝对路径。当文件已创建且步骤2中的每个要点都有对应问题时，即完成此步骤。

## 文档结构

应将其设计为**探索型问卷**：用户缺乏相关背景信息，而接收者掌握这些信息。请按重要性由高到低的顺序排列问题（由于是异步处理，你可能只有一次提问机会）。当问题数量超过少量时，可按主题将它们归类在 `##` 标题下。

模板：

```markdown
# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user> · **To:** <the recipient> ·
**How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough
to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful:
flag anything you're unsure of rather than skipping it.

## <Theme heading>

### <One question — a single idea, never compound>

_Why this matters: <one line, only where the question could be misread or
invite a throwaway answer>._

>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?
```

每个问题下方都会直接显示一个答案占位符（`>`）。

## 常见误区

1. **过度追问用户相关细节**。用户可能无法回答——这正是文档存在的意义。只需询问发送方即可。
2. **复合型问题**。每个问题只涵盖一个核心点；需将“且/或”关联的问题拆分开。
3. **隐藏关键问题**。应优先呈现最重要的问题，避免让次要的、异步接收方容易忽略的内容占据突出位置。
4. **信息堆砌**。只需用一段文字进行背景介绍，无需罗列全部历史记录。
5. **对模糊问题遗漏“为何重要”的说明**。这一部分能让敷衍的回答变得有用——但对于本身已明确的问题则无需添加。

## 验证清单

- [ ] 在起草前，通过两次交流确认接收方的角色/知识水平以及所需达成的结果
- [ ] 所有步骤2中的内容都至少有一个问题进行覆盖
- [ ] 问题均为单核心点、按重要性排序，并包含答案占位符
- [ ] 文件已生成，并向用户告知其绝对路径
