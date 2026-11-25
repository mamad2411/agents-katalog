---
name: impeccable
description: Frontend design guidance, upstream-maintained (impeccable).
version: 4.1.2
author: Paul Bakaus (pbakaus)
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, frontend, ui, ux, web-design, anti-slop]
    category: creative
    related_skills: [claude-design, popular-web-designs]
    upstream:
      repo: pbakaus/impeccable
      path: .hermes/skills/impeccable
---

# Impeccable（由上游团队维护）

> **目录条目占位符。** 此条目由上游项目
> [pbakaus/impeccable](https://github.com/pbakaus/impeccable)负责维护：该项目会在`.hermes/skills/`目录下提供并验证专为Hermes设计的技能包。执行`hermes skills install impeccable`命令即可从该仓库直接获取最新版本的技能包（与通过其他方式安装的技能包一样，会经过隔离处理和扫描）——该目录仅存储目录元数据，因此所引入的技能包永远不会过时。

Impeccable是一种专为AI编程智能体设计的规范语言：它包含一个可调用23个子命令的技能（如`/impeccable init`、`craft`、`shape`、`critique`、`audit`、`polish`、`bolder`、`quieter`、`distill`、`harden`、`onboard`、`animate`、`colorize`、`typeset`、`layout`、`delight`、`overdrive`、`clarify`、`adapt`、`optimize`、`extract`、`document`、`live`），还提供了明确的反模式指导（如过度使用的字体、紫色渐变、嵌套卡片效果以及弹跳式动画过渡），此外还有一个基于61条规则的确定性检测命令行工具（`npx impeccable detect`），该工具无需依赖LLM或API密钥。

安装完成后，可先执行以下操作：

```
/impeccable init
```

完整文档：https://impeccable.style
