---
name: demo-skill
description: 统计目录文件——教模型用 bash 数某个目录里有几个文件
---

# Demo Skill：统计目录文件数

当用户要统计某个目录下有几个文件时，按这个步骤做：

1. 用 bash 工具执行 `ls <目录>` 列出内容
2. 数一数输出里的文件名条目
3. 用一句话报告：总数 + 文件名清单

注意：这段正文是「贵的部分」，只在用户 `/demo-skill` 斜杠激活时才注入上下文；
平时模型只从 system prompt 看到本技能的一句话 description（渐进披露）。
