# Repo Ref
- source: https://github.com/yehuzi2026/workbuddy-skills-hub (path: categories/02-document-processing/docx-fill-pageindex/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 给 .docx 里的表格填数据，并自动回填「证明文件所在页码」这类需要真实排版页码的列。做法：python-docx 填格（保留原格式）→ 用 PowerShell 工具调本机 Word COM 把 docx 导出 PDF → pymupdf 搜标题文本定位页码 → 回填 → 重转 PDF 复核页码未漂移。适用于投标业绩表/索引表/目录页码、附录页码引用。触发词：填写业绩表、补页码、证明文件所在页
