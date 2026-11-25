---
name: replication-navigator
description: Use this skill to navigate a paper's replication package. Given the README and directory listing, it produces a run roadmap (entry script to final outputs), explains what each folder holds and how the master script calls sub-scripts, describes the raw/intermediate/analysis/output data layers, and judges how far the package can be reproduced. Helps identify the main program, data-processing scripts, and result-output scripts. Only uses what the README/listing state; never invents file names.
---

# replication-navigator（复现包导航）

第一次打开一个复现包时，帮你回答四个问题：**入口在哪、目录怎么分、数据分几层、能复现到什么程度**。产出复现路线图、目录职责、主程序调用关系和可复现层级，并帮你识别哪个是主程序、哪个做数据处理、哪个出图出表。对应第 1 讲配套阅读笔记的「复现材料导览」，也用于第 6 讲综合实操。

## 何时用

- 拿到一个陌生的复现包，不知从哪个脚本开始跑；
- 想弄清各目录（code / data / output 等）分别装什么、主程序怎样一层层调用子脚本；
- 想理清原始数据、中间数据、分析样本、图表结果之间的关系；
- 想让 AI 阅读一段 Stata / R 代码，说明它在复现流程中的位置。

## 使用方式（提示词）

把复现包的 `README.md` 和目录清单发给 agent：

> 这是一篇顶刊论文复现包的 `README.md` 和文件目录清单。请帮我写一份中文导览，包含：
>
> - 怎么开始跑：主程序（入口脚本）是哪一个？运行顺序是什么？
> - 文件夹结构：每个主要目录是干什么的？
> - 数据分几层：原始数据、中间数据、最终结果分别放在哪、什么关系？
> - 能复现到什么程度：有没有不公开的数据？缺了它还能跑哪些部分？
> - 软件和依赖：需要什么软件、要装哪些包？
>
> **只依据我给的 `README` 和目录，不要编造文件名**；不确定的地方标出来让我核对。

读单个脚本时追加：

> 这是复现包里的一段代码（Stata 或 R）。请说明它大致在做什么、读入什么、产出什么、对应论文的哪张图或哪张表、处在流程的哪一步。不用教我语法，只讲它在整个复现流程里的位置。

## 输出约定

- 一张「入口 → 子脚本 → 图表」的运行路线图；
- 识别主程序的法则：**被反复调用的是子脚本，调用别人的是主程序**；名字带 `master`/`main`/`run`/`0_` 前缀的通常是主程序；
- 数据分层：原始/输入 → 中间（运行时生成）→ 分析样本 → 图表结果；
- 可复现层级如实分级（完整 / 公开子集 / 仅代码审查），缺数据或缺许可的步骤要标出。

## 最小使用示例

> 用 replication-navigator 读一下这个复现包的 README，给我一张复现路线图，并指出哪个是主程序、哪些是数据处理脚本。

## 人工检查清单

- 路线图、脚本名、图表编号对照 `README` 的脚本清单逐一核对，AI 若杜撰脚本要揪出来；
- **不整包再分发**受版权限制的复现数据；按官方渠道（如 Dataverse）下载。
- **AI 辅助、不替代判断**：复现流程和结论是否可信，最终由你把关。

## 来源与许可

- 原创：本课程为「连享会 2026 暑期班·初级班」编写，Agent 无关的开放 Skill，MIT（随仓库 `LICENSE-CODE`）。
- 最后验证日期：<!-- TODO: T7 彩排双端实测后填写 -->
