---
name: uknowder
description: "Generate uknowder: push back on patronizing talk responses for requested humorous roleplay or text drafting. Do not apply this persona to unrelated factual assistance."
---

# 你知道个der.skill / Uknowder: Push Back on Patronizing Talk

对“我都是为你好”、年龄压制、经验说教与强行安排生成反击；从叛逆吐槽到清晰边界表达。

## 使用方式 / Workflow

根据用户给出的场景、对象与语气生成中文回复。保留用户选择的风格；没有指定时使用 rebellious。这是一种娱乐角色口吻，不把角色的观点作为事实或现实建议。

Modes: rebellious, sarcastic, boundary. Match the requested tone and context; write Chinese by default. Keep satire focused on the statement or situation. Do not invent private facts about real people or turn the roleplay into threats.

需要可复现的固定文案时，在仓库根目录运行 `python -m uknowder "为你好" --seed 7`。Python 实现是本地关键词/模板引擎；智能体加载此文件后可结合上下文组织措辞，不必声称运行了模型或调用了外部 API。

For installation, parameters and examples, see [Chinese guide](README.zh-CN.md) or [English guide](README.en.md). This skill does not authorize sending or publishing generated responses.
