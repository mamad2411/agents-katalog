# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/p/pdf-fin-parse/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 解析金融行业 PDF 文档（A股年报、港股财报、美股10-K、招股说明书等）为结构化 Markdown + JSON。专为跨页表格、无边框表格、多级表头、密集数值、多栏排版等金融场景设计。底层调用火山 LAS las_pdf_parse_doubao 算子做通用解析，再经 6 层金融后处理（HTML 表格解析 / 多级表头 / 跨页合并 / 数值规整 / 财务术语对齐 / 业务规则校验）输出 sc
