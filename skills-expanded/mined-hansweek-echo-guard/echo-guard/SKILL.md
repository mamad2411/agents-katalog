---
name: echo-guard
description: Finalize deliverables after corrections or rejected proposals without echoing them. Use when the session contains user rejections (remove/delete/去掉/删除/不要/换成) and the user asks for the final version of documents, tables, titles, filenames, slides, code comments, commits, PRs, or handoffs. 修订/否决/多轮修改后输出最终交付物（定稿/最终版/收口）时使用；普通删除任务不适用。
license: MIT
---

# Echo Guard — 交付收口终检

Treat the final deliverable as a product for readers who never saw this session: generate every user-facing surface from the accepted final state, and let rejected alternatives stay silent.

把最终交付物当成给"没见过本次会话的读者"的成品：从已采用的最终状态生成每个交付面，不回放被否内容和修订过程。

## 生成前：判定归属

内部列出三张清单（不输出给用户）：

1. **正向目标**：最终采用的状态；标题、正文、列头分别长什么样
2. **读者必需事实**：没看过会话的读者真正需要什么
3. **应静默内容**：只在会话中讨论过、被用户否决、从未进入最终基线的方案与措辞

对拿不准的内容问三个问题：

- 没看过这次对话的读者，需要这条信息吗？
- 省略它会造成不准确、不安全、误导或兼容问题吗？
- 它是相对任务初始基线的真实变化，且当前交付面需要解释吗？

三问全否 → 静默。

**保留例外**（不要误杀）：公开接口删除的迁移说明、安全/合规/审计必需事实、用户明确要求的对比与选型理由、兼容期保留的旧名称、领域规则自身的否定表述（如"未经授权不得重试"照常保留）。

## 生成：从正向状态出发

- 标题、文件名、开篇、图表标题、表格列头等高显著度文本：从正向目标**重新生成**，不逐词修改被否文案
- 同义改写不算合规：把对比表述换个说法（"按最新口径""已去除X维度""精简版"）同样违规——整个对比要消失，不是换词
- 表格和正文按最终口径直接写，不新增说明列、说明行、脚注来解释变化

## 回复正文同样受控

- 直接给出结果和验证状态；处理方法的叙述（"我会按X处理""根据你的要求""这次做了修正"）一律不出现
- 结尾不加"已清理/无残留/已统一口径"类自我声明

## 交付前：验证

通读全部用户可见面：标题、文件名、目录、列头、页眉页脚、代码注释、说明栏，以及自己回复的每一段。重点核对被移除元素的表述变体：

> 不做X / 无X / 不含X / 已去掉X / 已移除X / 已删除X / 去X版 / X已按新口径 / 不再包含X / 本版本不涉及X / 应要求调整 / 已按要求统一 / removed / no longer / without X

可用环境中可用的文本搜索工具检查被移除元素的本名是否残留；零匹配不代表语义合规，通读不可省。内容变化后重新验证一遍。

发现问题：静默修正后整体重出，不解释修了什么。

## Known Limitations

- 提示词层缓解，无确定性保证；本skill自身的措辞也可能被复述进回复——发现即静默修正
- 隐式触发不可靠，重要交付建议显式点名（如"用 echo-guard 终检"）
- 无法清除模型已读上下文；同会话纠正两轮以上，优先提取正向规格、在新会话中重写，本skill只做终检
- 纯文本指令：无脚本、无网络访问、无文件系统依赖

## Evolution Log

- v2.0 2026-08-26：公开发布版。适配 Agent Skills 规范，多平台通用，脱敏重构。设计思想参考 no-negative-echo（MIT，见 README 致谢），场景扩展至中英文商务文档，新增"回复正文禁方法叙述"条款与中文表述变体清单。
