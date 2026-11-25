---
name: pubg-progress-recovery
description: 当爷爷说“恢复当前进度”或上下文被截断/重启后，从 PUBG ESP 项目的主进度文件恢复全部上下文并继续。也用于任意回合开始时的强制存档检查。
x-alice-class: game
---# PUBG ESP 项目进度恢复 (Leila 专用)

## 触发
- 用户说：「恢复当前进度」「继续吧」「当前进行到哪里了」
- 回合开始时（本 skill 面向 `C:\Users\Administrator\Documents\游戏歪瓜` 项目）

## 恢复步骤（按序，全在 PowerShell）
1. `Get-Content -LiteralPath 'C:\Users\Administrator\Documents\游戏歪瓜\PROGRESS.md' -Tail 120 -Encoding UTF8`
   - 恢复：当前目标、现场锚点(PID/CR3/IB/G1/fn表)、最近一步成果、下一步计划、未补档产物。
2. `Get-Content -LiteralPath 'C:\Users\Administrator\Documents\游戏歪瓜\CONVERSATION_LOG.md' -Tail 40 -Encoding UTF8`
   - 恢复：爷爷最后几条原话，避免重复询问。
3. `Set-Location 'C:\Users\Administrator\Documents\游戏歪瓜'; git log --oneline -8; git status --short`
   - 判断最后 commit 与未提交产物。
4. 若存在比 PROGRESS 尾部更新的产物文件（data_dump/*.json、_*.py、bin），先补档（追加时间戳条目到 PROGRESS.md + CONVERSATION_LOG.md）再 commit，防止丢失。
5. 进程存活检查：`Get-Process -Name TslGame -ErrorAction SilentlyContinue`（记录 PID/WS/StartTime），并核对 `cr3_session_<pid>.json` 是否匹配。

## 强制写档规则（每条都要做，实时做）
- 每个分析步骤/工具里程碑/结果/决策 → 立即在 PROGRESS.md 追加带时间戳全量条目（step/input/output/evidence/artifacts/next）。
- 每条用户消息原样写入 CONVERSATION_LOG.md。
- 完成后 `git add -A; git commit -m "..."`。
- 宁多勿漏：上下文随时可能截断，一切以磁盘 md + git 为准。

## 语言/称呼
- 默认简体中文，代码/命令/hex 保留原文。
- 用户称呼一律“爷爷”。禁止其他称呼。
