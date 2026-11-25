---
name: nsfc-academic-research
description: NSFC-style deep academic research workflow with Tavily + long-form Chinese report generation. Use when users ask for 国自然选题分析、学术综述、深度文献检索、50+网址来源、PDF原文链接、或需要 Mermaid 思维导图。
---

# NSFC Academic Research Skill

## Use This Skill When

- 用户要求做国自然相关选题调研、立项背景综述、前沿进展梳理。
- 用户要求必须提供真实来源链接、PDF原文链接。
- 用户要求输出 5000 字以上中文深度报告，并附 Mermaid 思维导图。

## Inputs

- `topic`: 用户原始问题（中文或英文）。
- `min_results`: 目标来源数，默认 `50`。

## Workflow

1. 优化检索词
   - 将中文问题改写成专业英文检索词。
   - 保留核心实体（疾病、机制、药物、终点、方法学）。

2. 执行 Tavily 深度检索（50+）
   - 运行：
     - `python "$SKILLS_ROOT/nsfc-academic-research/scripts/tavily_search.py" --query "<optimized_query>" --min-results 50 --out tavily_results.json`
   - 强制要求：
     - 来源数不足 50 时自动扩展子查询并继续检索。
     - 去重（按 URL）。

3. 生成可注入上下文
   - 运行：
     - `python "$SKILLS_ROOT/nsfc-academic-research/scripts/format_context.py" --in tavily_results.json --out context.md`
   - 输出包含：
     - 编号来源清单
     - PDF 链接优先标注
     - 简明综合结论

4. 生成学术报告
   - 读取模板：
     - `$SKILLS_ROOT/nsfc-academic-research/templates/report_prompt.md`
   - 用 `context.md` 作为证据上下文，输出中文报告：
     - 字数 > 5000
     - 每个关键事实标注 `[Source X]`
     - 包含“争议与分歧”“局限性”“负外部性”

5. 输出思维导图
   - 在报告末尾追加一段 Mermaid `mindmap` 或 `graph TD`。

## Environment

- 必须设置 Tavily Key：
  - `TAVILY_API_KEY`

## Quality Gates

- 网址来源 `>= 50`
- 至少包含一组可访问 PDF 原文链接（若检索结果存在 PDF）
- 报告结构完整：摘要、引言、机制、实证、批判讨论、结论、参考文献
- 引用标注与来源编号一一对应

## Failure Handling

- Tavily 请求失败：检查 `TAVILY_API_KEY`、网络与速率限制，指数退避后重试。
- 来源不足 50：扩展检索词（同义词、机制词、方法词、时间限定）继续检索。
- PDF 过少：追加 `filetype:pdf` 与 `site:nih.gov|nature.com|thelancet.com|nejm.org|bmj.com|sciencedirect.com` 子查询。