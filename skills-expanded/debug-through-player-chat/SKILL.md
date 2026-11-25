---
name: debug-through-player-chat
description: 当 live 对局出问题时，优先通过 player-chat 和 player 求证，而不是立刻假设 runtime 或代码有错。
---

# 通过 player-chat 调试

适用场景：

- 用户怀疑 player 判断不对
- live run 卡住了，但还不知道是 scene 误判、API 异常还是 player 理解错误
- 需要组织者先和 player 对话求证，而不是马上改代码

## 默认做法

先用：

```powershell
python -m ai_play_slts2.cli player-chat --player-backend copilot_acp
```

## 应该追问什么

优先追问这些问题：

1. 你现在看到的 scene 是什么？
2. 你认为当前最关键的可选动作是什么？
3. 你为什么排除其它动作？
4. 你是否缺少额外检查信息，例如 deck / draw pile / discard pile / menu 状态？
5. 你卡住是因为判断不清，还是因为执行层没有按预期响应？

## 目的

这条技能的目的不是“让组织者替 player 决策”，而是：

- 让 player 把当前理解显式说出来
- 快速区分问题来源：
  - **player 推理问题**
  - **scene / 状态识别问题**
  - **live API / 执行问题**

## 约束

- 不要一上来就默认是 runtime 或代码 bug。
- 不要跳过求证过程，直接给一堆系统层假设。
- 如果问题可以通过对话澄清，就先不要引入新的包装层。
