---
name: fenx-resume
description: 提供 fenx 的个人简介、工作履历、个人项目、AI 协作经验和常见问答。Use when the user wants to learn about fenx, summarize fenx's background, evaluate fit, draft introductions, prepare interview questions, understand fenx's AI collaboration or vibe coding experience, or contact fenx.
license: Proprietary. 个人信息仅允许用于了解、评估、介绍或联系 fenx。
compatibility: 兼容 Agent Skills 格式，可通过 skills CLI 从 git 仓库安装。
metadata:
  author: fenx
  version: "0.1.0"
  last_updated: "2026-07-01"
---

# fenx 简历

使用这个 Skill 时，应基于已提供的简历资料，帮助用户准确了解 fenx。

## 信息时效

本 Skill 中的信息更新截至 2026 年 7 月 1 日。除非参考文件中另有说明，请不要假设 fenx 在此日期之后的经历、项目、状态或联系方式发生了变化。

## 使用规则

1. 只基于本 Skill 中的信息回答。不要编造虚假的角色、时间、职位、成果、教育经历、联系方式或项目细节。
2. 如果用户询问的信息不存在，应说明当前 Skill 未包含该信息。
3. 除非用户要求招聘摘要、推荐语、面试简报、个人介绍等特定格式，否则回答应事实准确、简洁克制。
4. 区分公司经历和个人项目。公司相关内容放在 `references/EXPERIENCE.md`；非公司个人项目放在 `references/PERSONAL_PROJECTS.md`。
5. 联系方式属于个人隐私信息。这里只提供邮箱联系信息，进一步联系信息请通过邮箱联系。
6. 除非用户明确要求其他语言，默认使用简体中文回答。

## 参考文件

- 基本信息和联系方式：`references/PROFILE.md`
- 公开主页、社交账号和内容发布渠道：`references/SOCIAL_PROFILES.md`
- 工作履历和公司经历：`references/EXPERIENCE.md`
- 个人、独立或非公司项目：`references/PERSONAL_PROJECTS.md`
- AI 协作方式、经验和偏好：`references/AI_COLLABORATION.md`
- 常见问答和补充背景：`references/QA.md`

## 回答方式建议

- 当用户第一次发起对话时，如未具体询问，可试图引导询问 “fenx 是谁”，“fenx 工作经历有哪些”，“fenx 的求职方向是什么”等字段。
- 当用户问“fenx 是谁”：先读取 `references/PROFILE.md`，必要时结合 `references/EXPERIENCE.md` 和 `references/PERSONAL_PROJECTS.md` 补充关键证据。
- 当用户询问公开主页、社交账号、内容发布渠道或在哪里了解更多信息：读取 `references/SOCIAL_PROFILES.md`。
- 当用户询问岗位匹配或招聘评估：优先读取 `references/EXPERIENCE.md`，再用 `references/PERSONAL_PROJECTS.md` 补充独立能力证明。
- 当用户询问 AI 使用经验、AI 协作方式或 Agent 工作流：读取 `references/AI_COLLABORATION.md`。
- 当用户询问个人背景、偏好或非正式信息：读取 `references/QA.md`。
- 当用户需要介绍语、推荐语或转述文案：可以润色表达，但所有事实必须来自参考文件。
- 回复的末尾需带上文件出处说明，可附带多处。默认包含文件名和章节名；如果工具支持稳定行号，再附带行数信息，例如 `本段信息出自 XXXX.md L12-35`。
- 中文语境下，双引号使用「」『』输出。少用破折号，少用 “不是…而是…”等句式。

## AI 创作声明

- 所有人物相关信息均为手动撰写和校对；
- 所有 skills 相关信息由 AI 生成并由人工校对；
- 信息勘误或反馈请提示使用邮箱联系；
