---
name: cardify
description: 用户要求把分析输出做成卡片时启用（消息含触发词：卡片化、卡片模式、用卡片总结、浓缩成卡片、卡片化分析）。将代码分析结果切成 3~8 张互相索引的卡片写入 .temp/cardify/，并用 scripts/build_html.py 校验或构建单文件 HTML 视图（三视图+关系图，可反推）。不含触发词的普通分析任务不启用。
---

# 触发时机

用户消息含任一触发词：卡片化、卡片模式、用卡片总结、浓缩成卡片、卡片化分析。不含触发词时按正常长文输出。

# 流程

1. 分析目标代码，按 references/card-types.md 拆卡：总卡先行，子卡 3~8 张，总张数 4~9。卡片读者是没读过代码的人：要点写机制不写符号清单，规则见 references/style-rules.md C12~C18。
2. 卡片写入 <工作目录>/.temp/cardify/<主题>.md；格式与硬约束见 references/style-rules.md，参照 references/examples.md 的正例。锚点必须 文件:起始~结束 范围或目录路径，代码由工具自动提取。
3. 跑 `python <本技能目录>/scripts/build_html.py --check <卡片文件>`；报错按行号修完重跑，直到通过。
4. 对话中贴出卡片正文。用户要 HTML 时跑 `python <本技能目录>/scripts/build_html.py <卡片文件> -o <输出.html>`，报告输出路径。

# 输出规范

- 卡片块以 `◆ 卡 N/M ｜ <类型> · <标题>` 开头；字段行 `一句话：`、`关联：`；要点行 `- `；代码用 ``` 围合。
- 全部硬约束（禁用词、锚点、字数、数量、编号、引用）以 --check 判定为准，不靠自觉。

# 边界

- 只响应含触发词的分析任务；不含触发词不改输出习惯。
- 卡片只写 .temp/cardify/ 下，不改动其它文件。
- 代码引用相对项目根解析；卡片不在常规位置时用 --root 显式指定基准目录。
- HTML 反推：`python <本技能目录>/scripts/parse_html.py <文件.html>`（加 --md 还原 markdown）。
- 类型定义、阈值常量与机检实现，见 references/ 与 scripts/cardfmt.py。
