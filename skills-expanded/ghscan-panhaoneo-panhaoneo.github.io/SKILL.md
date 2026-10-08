+++
title = 'Claude配置的skill'
date = 2026-04-29T13:32:39+08:00
draft = false
+++

> 导出日期：2026-04-29

  ---

  ## 一、插件 (Plugins)

  ### 1. superpowers (核心技能库)

  - **来源**: `claude-plugins-official`（官方注册表，默认自带）
  - **版本**: 5.0.7
  - **包含技能**: brainstorming、systematic-debugging、test-driven-development、writing-plans、execut
  ing-plans、subagent-driven-development、dispatching-parallel-agents、using-git-worktrees、finishing
  -a-development-branch、verification-before-completion、requesting-code-review、receiving-code-revie
  w、writing-skills、using-superpowers

  ```bash
  /plugin install superpowers@claude-plugins-official

  2. clangd-lsp (LSP 支持)

  - 来源: claude-plugins-official
  - 版本: 1.0.0

  /plugin install clangd-lsp@claude-plugins-official

  3. andrej-karpathy-skills (编码规范)

  - 来源: karpathy-skills 市场
  - 版本: 1.0.0
  - 包含技能: karpathy-guidelines

  /plugin marketplace add forrestchang/andrej-karpathy-skills
  /plugin install andrej-karpathy-skills@karpathy-skills

  4. claude-hud (状态栏 HUD) https://github.com/jarrodwatts/claude-hud

  - 来源: github:jarrodwatts/claude-hud
  - 版本: 0.1.0
  - 包含技能: claude-hud:setup、claude-hud:configure

  /plugin marketplace add jarrodwatts/claude-hud
  /plugin install claude-hud

  5. claude-mem  https://github.com/thedotmack/claude-mem

  6. 

  ---
  二、独立技能 (Standalone Skills)

  位于 ~/.claude/skills/，版本均为 3.15.0：

  此skill来自：https://github.com/tw93/Waza
  安装命令：npx skills add tw93/Waza -a claude-code -g -y

  ┌────────┬────────────────────────────────────────────┐
  │  技能  │                    用途                    │
  ├────────┼────────────────────────────────────────────┤
  │ check  │ 代码审查、diff 检查、自动修复安全/架构问题 │
  ├────────┼────────────────────────────────────────────┤
  │ design │ UI 页面/组件设计与样式迭代                 │
  ├────────┼────────────────────────────────────────────┤
  │ health │ Claude Code 六层配置栈健康度审计           │
  ├────────┼────────────────────────────────────────────┤
  │ hunt   │ 系统性排查 bug、崩溃、测试失败根因         │
  ├────────┼────────────────────────────────────────────┤
  │ learn  │ 六阶段研究学习工作流，输出发布级内容       │
  ├────────┼────────────────────────────────────────────┤
  │ read   │ URL/PDF 抓取为 Markdown，支持付费墙        │
  ├────────┼────────────────────────────────────────────┤
  │ think  │ 方案设计、架构决策、价值判断               │
  ├────────┼────────────────────────────────────────────┤
  │ write  │ 中英文写作润色、去 AI 味                   │
  └────────┴────────────────────────────────────────────┘

  安装方式（二选一）：

  # 方式 A: 从旧环境直接复制
  scp -r ~/.claude/skills/{check,design,health,hunt,learn,read,think,write} \
    new-host:~/.claude/skills/

  # 方式 B: 打包传输
  tar czf skills-backup.tar.gz -C ~/.claude/skills \
    check design health hunt learn read think write
  # 在新环境解压
  tar xzf skills-backup.tar.gz -C ~/.claude/skills/

  ---
  三、一键安装脚本

  #!/bin/bash
  # Claude Code 技能环境初始化

  echo "=== 安装官方注册表插件 ==="
  claude plugins install superpowers@claude-plugins-official
  claude plugins install clangd-lsp@claude-plugins-official

  echo "=== 添加市场 & 安装第三方插件 ==="
  claude plugins marketplace add karpathy-skills
  claude plugins install andrej-karpathy-skills@karpathy-skills

  claude plugins marketplace add claude-hud --source github:jarrodwatts/claude-hud
  claude plugins install claude-hud@claude-hud

  echo "=== 恢复独立技能 ==="
  # 确保 skills-backup.tar.gz 在当前目录
  tar xzf skills-backup.tar.gz -C ~/.claude/skills/

  echo "=== 完成 ==="
  claude plugins list

  ---