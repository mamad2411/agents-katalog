---
name: backlink-expansion-matrix
description: "Orchestrate an end-to-end backlink expansion project from Semrush or local source files through batch and editorial screening, historical deduplication, workbook delivery, and QA. Use when the request spans more than one backlink stage; do not treat candidates as submitted or published links."
---

# 外链扩量总控

把源表获取、候选压缩、批量提交线、质量投稿线、历史去重和表格交付串成一个可恢复的项目。总控只负责冻结范围、选择技能、检查交接和验收结果，不代替各阶段的专业判断。

## 启动时冻结

记录目标品牌、输入材料、需要处理的线路、数量目标、是“补足到 N 条”还是“新建 N 条”、费用分组、历史去重范围、最终列名、输出目录、是否允许浏览器操作，以及是否明确允许子代理并行。用户已说明的信息不得重复询问。

## 路由

- 缺少标准候选源表，或需要整理 Semrush 导出：使用 `backlink-source-prep`。
- 工具目录、产品导航、创业项目库、社区资料页和资源推荐页：使用 `backlink-batch-expansion`。
- 文章投稿、行业媒体、编辑资源页和专家贡献计划：使用 `backlink-quality-expansion`。
- 历史去重、批次冻结、免费/付费工作表、重新导入和视觉检查：使用 `backlink-workbook-delivery`。

完整路由和阶段交接见 [references/workflow-routing.md](references/workflow-routing.md)。状态含义和禁止混用的结论见 [references/status-boundaries.md](references/status-boundaries.md)。

## 端到端顺序

1. 冻结范围并登记原始文件，不覆盖源文件。
2. 将自然搜索竞品、反向链接差异、引荐域名、历史表和公开资源整理成可追溯源表。
3. 标准化 URL 和域名，记录来源文件、目标品牌和来源竞品；先压缩数据，再做站点级判断。
4. 按入口性质分流到批量线或质量线。无法判断的进入备用池，不强行归类。
5. 各线路只写独立中间表；总候选库和最终工作簿只允许一个写入者合并。
6. 统一执行历史去重、跨线路去重和已导出批次去重。
7. 冻结批次并生成工作簿；重新导入检查内容，再检查顶部、底部和新增区域。
8. 交付时报告候选数、排除数、去重数和最终行数，不把这些数字说成实际提交数或收录数。

## 不可破坏的规则

- Semrush、竞品外链和公开清单只是候选来源，不证明平台适合投递。
- 未经明确授权，不注册、不登录、不付款、不提交、不联系站方。
- 批量线以扩量为先；质量线兼顾主题、准入难度和预期回报，两者不能套用同一淘汰门槛。
- “费用未说明”不等于免费；“页面可打开”不等于入口有效；“已导出”不等于已提交。
- 已导出的批次集合冻结。后续改变排序或批次大小，只影响尚未分配的候选。
- 子代理只在用户明确要求时使用。每个分片只写自己的中间文件，主代理统一合并和交付。
- 制作公开版本时，只保留通用方法、空白模板和通用校验脚本。删除真实品牌、域名、项目数据量、内部文件名、个人路径、账号或会话细节、历史投递记录和源资料摘录；示例统一使用变量或明确标注的虚构值。
- 公开发布前，对整个交付目录执行敏感信息扫描并人工查看差异。没有确认内容已匿名化，不得上传或推送。

## 完成条件

只有各阶段交接文件存在、来源可追溯、去重记录可解释、工作簿通过机械和视觉检查、状态边界写清楚，才算完成。缺少外部提交证据时，最高只能报告为“待执行候选”。
