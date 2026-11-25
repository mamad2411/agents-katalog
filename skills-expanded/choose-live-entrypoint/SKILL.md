---
name: choose-live-entrypoint
description: 判断当前应该走 standalone-player-live、player-chat，还是只做环境检查，并解释 CLI 在这个仓库里的角色。
---

# 选择当前入口

适用场景：

- 用户问“现在该怎么启动”
- 用户问“CLI 有什么用”
- 用户问“该用哪个命令”
- 需要在 **直接打牌**、**对话调试**、**环境检查** 三类动作里做选择

## 先判断目标

先判断用户当前真正想做什么：

1. **直接继续当前 run / 让 player 打牌**
2. **先和 player 聊天，确认它看到了什么、怎么想**
3. **先检查环境、API、菜单、当前状态**

## 推荐映射

### 1. 直接继续当前 run

用：

```powershell
python -m ai_play_slts2.cli standalone-player-live --steps 20
```

说明：

- 这是当前活动体系里的主执行路径
- 含义是 **player 直接连 live API 打牌**
- 适合“先让系统继续往前走”

### 2. 先和 player 对话调试

用：

```powershell
python -m ai_play_slts2.cli player-chat --player-backend copilot_acp
```

说明：

- 这是组织者和 player 的对话入口
- 适合“先问清楚它为什么这么判断”
- 不替 player 落子，而是帮助暴露问题

### 3. 先检查环境 / API / 当前状态

常用命令：

```powershell
python -m ai_play_slts2.cli doctor
python -m ai_play_slts2.cli read-state
python -m ai_play_slts2.cli read-menu
python -m ai_play_slts2.cli bootstrap-live
```

说明：

- `doctor`：检查 live API 是否可用
- `read-state`：读取当前游戏状态
- `read-menu`：读取当前菜单状态
- `bootstrap-live`：做 live 环境准备

## 应该怎么解释 CLI

当用户问“CLI 是什么”时，默认这样解释：

> CLI 是这个仓库的命令行入口。  
> skill 负责教 agent 怎么想，CLI 负责把这些能力以终端命令的形式启动出来。

可以进一步拆成三类：

- **执行入口**：`standalone-player-live`
- **对话调试入口**：`player-chat`
- **运维检查入口**：`doctor` / `read-state` / `read-menu` / `bootstrap-live`

## 约束

- 不要再把 `loop-live-runtime`、`supervise-live` 说成当前推荐入口。
- 不要把 CLI 说成“额外的一层智能”。
- 遇到入口选择问题，优先按“用户当前目标”来分流，而不是按旧 runtime 习惯回答。
