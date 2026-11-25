---
name: translate-readme-and-skills
description: 当用户要求翻译 readme 或 skills 时启用, 将会把 skills/bro-mode/locales/zh-CN.md 内容同步翻译为 skills/bro-mode/locales/*.md, 把 README.zh-CN.md 同步翻译到其他语言的 readme 文件
---

## 介绍
本技能只做三件事:

- **当 `skills/bro-mode/locales/zh-CN.md` 有改动时**, 阅读 `skills/bro-mode/locales/zh-CN.md`, 并将同目录下的其他语言的文件内容同步翻译为 `zh-CN.md` 中的内容
- **当 `skills/lover-mode/locales/zh-CN.md` 有改动时**, 阅读 `skills/lover-mode/locales/zh-CN.md`, 并将同目录下的其他语言的文件内容同步翻译为 `zh-CN.md` 中的内容
- **当 `README.zh-CN.md` 有改动时**, 阅读 `README.zh-CN.md`, 并将同目录下的其他语言的 readme 文件内容同步翻译为 `README.zh-CN.md` 中的内容

## 要求
- 如果 `skills/bro-mode/locales/zh-CN.md` 或 `skills/lover-mode/locales/zh-CN.md` 或 `README.zh-CN.md` 没有改动, 则禁止做任何事情
- 如果 `skills/bro-mode/locales/zh-CN.md` 或 `skills/lover-mode/locales/zh-CN.md` 或 `README.zh-CN.md` 有改动, 则必须完整阅读它们, 禁止只翻译改动的部分
- `skills/bro-mode/locales/*.md` 文件中禁止包含顶部的 `meta` 内容
- `skills/bro-mode/locales/*.md` 和 `README.*.md` 中的内容必须与 `skills/bro-mode/locales/zh-CN.md` 和 `README.zh-CN.md` 中的内容一一对应
- 禁止以任何形式执行任何命令或脚本