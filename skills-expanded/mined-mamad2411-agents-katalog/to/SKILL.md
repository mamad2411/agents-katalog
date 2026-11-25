---
name: to-skill
description: "One-click convert any content into a Claude skill — the main entry point"
argument-hint: "[file, URL, or paste text]"
allowed-tools: Read Bash Grep Glob Write WebFetch
---

# /to-skill

一键将任何内容转化为 Claude skill。这是 content-to-skill 的主入口命令。

## Usage

```
/to-skill
```

用户在调用前或调用后提供素材（文本、文件、URL、图片等均可）。

## Behavior

1. 读取用户提供的素材（文本/文件/URL/图片/音视频）
2. 自动识别内容类型和语言
3. 自动判断推荐 知识型 还是 动作型（展示判断依据）
4. 展示生成计划（哪些组件会生成），等待用户确认或调整
5. 生成完整 skill 文件夹（SKILL.md + 按需生成 scripts/references/commands/hooks/agents）
6. 打包交付

等同于按顺序执行: `/skill-ingest` → `/skill-classify` → `/skill-generate` → `/skill-package`
