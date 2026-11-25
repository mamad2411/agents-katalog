---
name: research-report
description: Use when the user asks to write a Chinese technical, product, vendor, or market research report (调研报告), product/vendor/system comparison (产品/厂商/系统对比), or selection recommendation report (选型报告) delivered as a formatted Word (.docx) document. Do not use for academic papers, patent disclosures, grant proposals, requirement lists, or pure fact-checking.
---

# 调研报告（Research Report）

把调研材料整理成可交付的中文调研报告 DOCX。报告遵循总分总结构：摘要给出结论；正文开头是面向非专业读者的技术背景（按时间线梳理发展阶段、文献与政策）；主体按分类逐项调研；末尾给出选型建议与实施路径，并以"综上所述"收束，写清竞品缺口、缺失层面（可由科研立项反推）、未来发展方向与我方差异化。全文须贯穿两条判断线——这项技术难在哪、现在能做到什么程度；这部分能力自己做还是买——而不是只罗列功能与厂商。版式统一为仿宋正文、宋体标题、黑白表格、三级自动目录。

## 适用与边界

- 适用：市场调研、技术路线调研、产品/厂商/系统对比、选型建议报告。
- 不适用：学术论文、专利披露、科研立项申请书、采购需求清单、纯事实核验。
- 只整理用户提供或经公开检索核实的调研材料，不凭空编造市场规模、市占率、厂商名称、产品参数、金额等事实；技术背景中的时间、文献、政策与综合总结中的科研立项信息同样必须可溯源；每项关键数据都要能对应到资料来源，无法取得来源的数字不写。

## 输入与输出

- 输入：调研主题、范围、被调研对象清单、资料来源（厂商官网、行业报告、公开资料、访谈记录；若用户仅提供调研主题，须先通过搜索工具采集可溯源资料）。
- 中间产物：一份按模板结构编写的 Markdown 源稿。
- 最终交付：一份规范化 DOCX。

## 工作流

1. **确定范围与采集素材**：先确定调研范围、对象分类维度和资料来源。若用户仅给定主题而未提供现成材料，先分四轮检索收集有据可查的公开资料：①标志性文献、标准号与产业政策（带年份与发布机关）；②行业市场规模与竞争格局数据；③分层代表厂商、产品定位与核心参数；④国家级/省部级/行业公开科研立项课题（用于反推行业未闭环缺口）。
2. **搭建骨架与正文写作**：按 [references/structure-and-logic.md](references/structure-and-logic.md) 组织章节骨架、论证逻辑和文风（含 2.1 技术背景时间线与 9.4 综合总结），写成 Markdown。
3. **编入两条贯穿判断线**：按 [references/problem-and-inhouse.md](references/problem-and-inhouse.md) 把两条线索编进正文（核心问题与技术难点、自研优劣），贯穿式论述、不单列章节，硬要求见下文「内容主线」。
4. **规范化对比表格**：按 [references/tables.md](references/tables.md) 组织表格，保证同一批被调研对象用同一套列、可横向对比。
5. **线索自检与生成 DOCX**：先运行 `python scripts/check_threads.py <报告.md>` 检查两条线索密度；再运行 `python scripts/build_docx.py <报告.md> --out <调研报告.docx>` 一键完成 DOCX 转换、三级自动目录注入与 Word 字段刷新（分步命令与版式细节见 [references/format.md](references/format.md)）。

## 内容主线（两条贯穿线索）

报告不能只回答"有什么"，还要回答"难在哪、能不能做到"和"自己做还是买"。这两条线索的判据、落点、反模式见 [references/problem-and-inhouse.md](references/problem-and-inhouse.md)，硬要求如下：

- **难点线**：每章末答三问（核心矛盾是什么 / 为什么难 / 现在到哪一步），断言要有可观测判据；全文只在结论章用一张难点矩阵表收口，不设独立"难点分析"章。
- **自研线**：每章末给分层判断（自研 / 采购 / 拆开），优势与代价成对出现，代价必须给补偿手段；不设"自研可行性"章，分类体系表增加「自制/采购判断」列承载分层结论。
- 两条线索在结论章合成一条论证：已闭环的难点→照搬范式；数据在己方的未闭环难点→自研；需外部公信力的未闭环难点→采购加第三方背书。
- 定稿前跑 `python scripts/check_threads.py <报告.md>`，按提示回看原文修订，不机械加词。

## 内容边界

- 保留用户给定的结论、优先级、数字、单位、日期、厂商名、产品名和责任分工，不因"更像套话"而删除。
- 结论用正文材料支撑，不用"行业领先、全面赋能、深度融合"等无边界宣传语替代证据。
- 不确定的信息标"据公开资料/厂商介绍"，不把厂商宣传数字写成实测结果。
- 表格空值保留，不补写没有来源的数据。
