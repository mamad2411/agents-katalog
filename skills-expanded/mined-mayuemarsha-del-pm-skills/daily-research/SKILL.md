---
name: daily-research
description: >-
  Daily research briefing. When the user says "今天的调研""跑一份调研简报""每日调研""今日行业动态""扫一下最近有什么新东西""补一下今天的简报"，或在会话里要求生成 / 补一份当日情报简报时，触发本 skill。它在当前会话里实时联网调研用户配置的领域（默认是 AI 应用层 / 框架 / 论文 / 模型 / 研究员与厂商落地动态），产出一份中文简报写入 `<RESEARCH_DIR>/YYYY-MM-DD.md`。即使用户没说"用 skill"、只说"今天调研呢""帮我看下今天有什么进展"也要触发。本 skill 只生成简报，不自动归档。
---

1. # 每日调研简报

   1.1. **这个 skill 做什么**

   按需在**当前会话里**跑一次领域调研，产出当日中文简报。

   会话里联网（WebSearch / WebFetch）走的是 Claude Code 自带通道，代理和登录都正常，比无人值守跑（容易被 `403 Request not allowed` 拒）更可靠。

   1.2. **调研规格的唯一来源**

   调研范围、重点对象、输出三段式格式、链接真实性自检等**全部规则，以下面这个文件为准**，每次执行前先完整读一遍：

   ```
   <RESEARCH_DIR>/prompt.md
   ```

   `<RESEARCH_DIR>` 由用户在 CLAUDE.md 中配置（如 `/Users/you/research/daily/`）。

   **首次使用前**：把 `references/example-prompt.md` 复制到 `<RESEARCH_DIR>/prompt.md`，改成你关心的方向（金融监管 / 跨境电商 / 某垂直行业 / AI 应用层 等），不要把规则抄进本 skill。调整调研内容的方式就是改那个 `prompt.md`；本 skill 只负责「按它执行 + 落到正确的文件」。这样两边不会漂移。

2. ## 执行步骤

   2.1. 读 `<RESEARCH_DIR>/prompt.md`，作为本次调研的完整规格。
   2.2. 确定今天日期（用环境里的当前日期，格式 `YYYY-MM-DD`），作为 prompt.md 里说的【今日日期】。
   2.3. 先用 Glob / Read 看 `<RESEARCH_DIR>/` 下最近几份历史简报，与历史去重，不重复昨天已报的内容。
   2.4. 按 prompt.md 的范围用 WebSearch / WebFetch **实际联网**调研。链接必须是本次真实打开过的页面；找不到一手来源的条目整条删掉，宁缺毋造。
   2.5. 按 prompt.md 的「输出要求」组织简报。
   2.6. 写文件前自检：每条非 `〔判断〕` 的事实条目必须带本次真实访问过的链接，否则整条删掉。
   2.7. 用 Write 写入 `<RESEARCH_DIR>/<今天日期>.md`。当天文件已存在时，先读一眼确认是同日重跑，再覆盖。

3. ## 边界（重要）

   3.1. 只产出 `<RESEARCH_DIR>/<日期>.md` 这一个文件。
   3.2. **不要自动归档**到长期知识库（用户可能有 `competition/` `research/` 这种长期目录）—— 简报末尾给「归档建议清单」就行，归档由用户 review 后自己做。

4. ## 完成后

   给用户一句话回执：当天日期、简报文件路径、今日最值得看的 2–3 条，让用户决定要不要归档。

5. ## References

   5.1. `references/example-prompt.md` — 调研规格示例（**示例文件，用户应复制到 `<RESEARCH_DIR>/prompt.md` 并按自己关心的方向改写**）。
