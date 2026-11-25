---
name: extract-app-knowledge
description: Extract evidence-checked business and engineering knowledge from pinned source revisions, then validate and publish a searchable knowledge base.
---

# Knowledge extraction: select one instruction language

This is an **AI task router**, not a human usage guide or knowledge content. Load exactly one workflow below; do not combine both translations as separate sets of requirements.

| Task interaction language | AI workflow | Human guide |
| --- | --- | --- |
| 简体中文 | [中文执行指引](contracts/chinese-workflow.md) | [中文使用指南](../../docs/usage.md) |
| English | [English workflow](contracts/english-workflow.md) | [English usage guide](../../docs/usage.en.md) |

When using the bundled plugin, find the toolkit root two directories above this skill file. With Git and Python 3.9+ available, use the bundled `validation/knowledge.py` as the CLI entry point. For project commands, pass `--project-root` followed by the knowledge project path as a separate argument.

Choose the interaction language requested by the user. Knowledge output follows the project’s `content_language` (`zh-CN` by default, or `en`), independently of the conversation language and source programming language.

协议文件名、固定表头、枚举、ID 和 JSON 键保持原样；它们不是需要翻译的知识正文。
Protocol filenames, fixed headers, enums, IDs and JSON keys stay literal. They are not prose to translate.
