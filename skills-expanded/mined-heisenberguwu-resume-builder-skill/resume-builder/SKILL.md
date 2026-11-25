---
name: resume-builder
description: Build a polished single-file HTML resume from scattered historical data. Supports packing up materials from .eml emails, .msg Outlook files, .txt/.html reports, old resumes, class notes, lab reports, project docs, and photos into a single resume. For students, course notes and academic materials are auto-extracted into skills and project experience. Includes resume writing guides for multiple career paths (computer science, human resources, marketing) and swappable CSS style themes (apple, minimal, corporate). Avatar is auto-cropped and Base64-embedded for offline use.
version: 1.0.0
author: community
license: MIT
prerequisites:
  commands: [python3]
  pip_deps: [Pillow]
metadata:
  hermes:
    tags: [resume, HTML, multi-source, data-extraction, writing-guide, swappable-styles, productivity]
    category: productivity
---

# Resume HTML Builder — Multi-source Resume Generator

Build a modern, single-file HTML resume from scattered historical data (.eml reports, old resumes, photos, publications).

## When to Use

- User wants to rebuild a resume from scattered materials (weekly reports, old resumes, etc.)
- User asks to pack up their materials and generate a resume (zip or directory)
- Converting Markdown/PDF resume to a single-file HTML
- Need avatar cropping + Base64 embedding for offline viewing
- Multi-career resume writing guidance (tech, HR, etc.)
- Multi-style design choices (apple, minimal, corporate)
- Multi-source data extraction and merging
- Student course notes, lab reports, and project docs for skill extraction

## Typical User Prompts

These are the most common ways users trigger this skill:

| Prompt | What happens |
|--------|-------------|
| "把周报打包成一份简历" | Extract .eml/.txt, merge, render HTML |
| "把我的资料整理成简历" | Categorize files, extract text, draft resume |
| "用这些材料帮我生成一份简历" | Full pipeline: extract → draft → style → deliver |
| "用我的课程笔记和实验报告提取一份在校生简历" | Extract skills and projects from academic materials, render HTML |
| "把旧简历转成 HTML 格式" | Parse existing resume, apply chosen theme |

## Language Rule (IMPORTANT)

Match the user's input language throughout the entire workflow:

| User speaks | Guide | HTML template | Resume content |
|-------------|-------|---------------|----------------|
| English | `*-guide.md` | `resume-html.html` | English |
| 中文 | `*-guide-cn.md` | `resume-html-cn.html` | 中文 |

If the user doesn't specify, default to English. This applies to every step — guide selection, template selection, and all generated resume content.

## Workflow

```
Collect sources → Extract data → Deduplicate & merge → Draft → Render HTML → Embed avatar → Deliver
```

### Two Execution Modes

#### Mode A: Full Pipeline (Recommended)

Run `pipeline.py` to automate all script steps. Manual steps (drafting, Markdown) will print TODO prompts:

```bash
# From zip
python scripts/pipeline.py --zip "resume-sources.zip" --output-dir ./output

# From directory
python scripts/pipeline.py --dir /path/to/sources --output-dir ./output

# Provide pre-built HTML to skip draft step
python scripts/pipeline.py --dir /path/to/sources --output-dir ./output --html ./my-resume.html

# Skip specific steps
python scripts/pipeline.py --dir /path/to/sources --output-dir ./output --skip embed-avatar,html-to-pdf
```

Pipeline output flow:
```
[1/6] Extract & categorize sources    (AUTO)   → extracted_manifest.json
[2/6] Extract text from files          (AUTO)   → extracted_texts.json
[3/6] Draft resume + render HTML       (MANUAL) → read extracted_texts.json, draft, save resume-<name>-final.html
[4/6] Crop & embed avatar              (AUTO)   → overwrites HTML with embedded avatar
[5/6] Generate Markdown                (MANUAL) → convert HTML to resume-<name>-final.md
[6/6] Convert HTML to PDF              (AUTO)   → resume-<name>-final.pdf
```

**Agent workflow with pipeline:**
1. Run `pipeline.py` — it completes steps 1-2 then prints TODO for step 3
2. Read `output_dir/extracted_texts.json` to understand source material
3. Follow steps 3-4.6 below to draft resume content
4. Save HTML to `output_dir/resume-<name>-final.html`
5. Re-run pipeline with `--skip extract-sources,extract-text,draft-resume` to continue from step 4
6. Generate Markdown (step 5)
7. Re-run pipeline with `--skip extract-sources,extract-text,draft-resume,embed-avatar,generate-markdown` for final PDF

#### Mode B: Individual Scripts

Run each script manually for full control. See individual step sections below.

## Prerequisites

```bash
pip install Pillow          # avatar cropping (recommended)
pip install weasyprint      # PDF generation (recommended)
pip install msgreader       # .msg support (optional)
```

## Step 1: Extract and Categorize Source Data

User typically provides a zip archive. Supported file types:

| Extension | Content | How it's read |
|-----------|---------|---------------|
| `.eml` | Standard email (Thunderbird/Mail.app export) | MIME parser |
| `.msg` | Outlook email | `extract-msg` (pip install) |
| `.txt`, `.text` | Plain text reports | Direct read |
| `.html`, `.htm` | HTML emails/reports | Tag stripped |
| `.md`, `.sg`, `.pdf` | Old resume drafts, class notes, lab reports, project docs | Text/pdf parser |
| `.jpg`, `.png` | Avatar photos | Image picker |

```bash
# From zip
python scripts/extract_sources.py --zip "resume-sources.zip" --output extracted

# From directory
python scripts/extract_sources.py --dir /path/to/sources
```

Outputs categorized file lists + JSON. Auto-selects best avatar (prefers `avatar`/`photo`/`head` in filename, else largest file).

**Supported email formats:**
- `.eml` — standard MIME (Thunderbird, Mail.app, generic export) — no extra deps
- `.msg` — Outlook format — needs `pip install msgreader`
- `.txt` / `.html` — plain text or HTML saved from email clients — direct read

## Step 2: Extract Text from Reports

The script converts any file to readable text — it does **not** structure content.

```bash
# Single file
python scripts/extract_text.py report.eml

# Directory of reports
python scripts/extract_text.py reports/ --json

# Recursive
python scripts/extract_text.py reports/ -r --json
```

**Output format (JSON):**
```json
[{"filename": "report.eml", "content": "From: ...\nSubject: ...\n\nBody content..."}]
```

**Agent interprets the text:** Feed the `content` to yourself and use natural language understanding to extract dates, subjects, key achievements, and metrics. The script handles MIME decode, HTML tag stripping, and encoding — you handle meaning.

**Supported formats:**
- `.eml` — standard MIME email — no extra deps
- `.msg` — Outlook — needs `pip install msgreader`
- `.html` / `.htm` — auto-stripped to text
- `.txt` / `.md` / `.sg` / anything else — direct read

## Step 3: Extract from Old Resumes

Markdown: parse `#` section headers and group content under each.

PDF: use the `ocr-and-documents` skill (pymupdf or marker-pdf).

## Step 4: Select Career Path and Draft Resume Content

Pick a career path from `references/<career>/resume-guide.md` (EN) or `resume-guide-cn.md` (CN).

| Career Path | Focus | Guide path |
|-------------|-------|-----------|
| **Computer Science** (default) | FAB pattern, per-stack focus (backend/frontend/mobile/C++/Go/architecture), ATS keywords | `references/computer-science/` |
| **Human Resources** | Recruitment metrics, employee relations, HRBP alignment, labor compliance | `references/human-resources/` |
| **Marketing** | Growth metrics (CAC/ROI/LTV), brand campaigns, user ops, content marketing, GTM | `references/marketing/` |

**Language:** Use English guide if user speaks English, Chinese guide (`-cn.md`) if user speaks 中文. Default to `computer-science` if role is unclear.

**Adding a career path:** Create `references/<career>/resume-guide.md` + `resume-guide-cn.md`. Cover: key metrics to emphasize, per-role focus areas, ATS keywords, and concrete before/after writing examples.

**Key merge principles:**
- **Timeline alignment:** Match report dates to employment periods for correct attribution
- **Deduplication:** Merge overlapping weekly report content
- **Role evolution:** Highlight promotions (e.g., "Engineer → Lead")
- **Quantify:** Extract metrics (users, performance gains, data volume)

## Step 4.5: Deep-Dive Detailing (IMPORTANT)

After the initial draft, you must go back and significantly expand the **most recent 2 entries** — everything else stays concise.

| User type | What to detail |
|-----------|---------------|
| **Working professional** | The most recent **2 employers** (work units) |
| **Student / fresh graduate** | The most recent **2 projects** (course projects, lab work, competitions, open-source, internships) |

**How to expand — the "elevate" (拔高) framework:**

For each of the 2 detailed entries, rewrite with the following layers:

1. **Context & scale:** Describe the business background, team size, data scale, or system complexity. Example: "负责日均 PV 500 万的核心交易系统" instead of "负责交易系统".
2. **Technical depth:** Highlight architectural decisions, design patterns, and why you chose a particular approach over alternatives. Example: "采用 CQRS 读写分离架构，将查询 QPS 从 2000 提升至 15000" instead of "优化了查询性能".
3. **Business impact:** Connect your technical work to business outcomes — revenue growth, cost reduction, user retention, risk mitigation. Example: "通过智能限流方案降低系统故障率 92%，保障了双十一期间零宕机".
4. **Leadership & ownership:** Show initiative — code reviews, mentoring, cross-team collaboration, technical planning. Example: "主导跨 3 个团队的微服务拆分方案，制定接口规范并推动落地".
5. **Quantification (always):** Every bullet must have at least one number — QPS, latency, percentage improvement, team size, data volume, cost saved.

**Before vs After (Chinese example):**

| Before (too plain) | After (elevated) |
|---------------------|-----------------|
| 负责用户系统的开发 | 主导日均 DAU 200 万的用户中心微服务重构，采用 DDD 划分 5 个bounded context，团队从 3 人扩展至 8 人 |
| 优化了数据库查询 | 设计多级缓存架构（本地缓存 + Redis Cluster + DB），将核心接口 P99 延迟从 320ms 降至 18ms，提升 94% |
| 参与了 API 网关项目 | 作为技术负责人主导 API 网关建设，集成 JWT 鉴权、动态路由和全链路 TraceId，日均处理 200 万+ 请求，零安全事故 |

**Bullet count guidance:**
- Detailed entries: **4-6 bullet points** each, each 1-2 lines
- Non-detailed entries: **1-2 bullet points**, keep concise
- Non-detailed entries can be shortened to a single line or collapsed entirely if they're older or less relevant

**For students detailing projects:**
- Frame course/lab projects as real engineering challenges
- Emphasize the **problem you solved**, the **technical approach**, and the **measurable outcome**
- Example: "基于 PyTorch 实现图像分类模型，在 CIFAR-10 上达到 93.2% top-1 accuracy，较 baseline 提升 6.8%，代码开源获 120+ stars"
- Highlight teamwork, code quality (tests, CI/CD), and any competitive results

**⚠️ Critical rules:**
- **NEVER fabricate data.** If a metric isn't in the source material, estimate conservatively and phrase as "约" or "约 X+" rather than inventing precise numbers.
- **Always match the user's language** — Chinese descriptions for 中文 resumes, English for English resumes.
- Keep the career path guide's FAB pattern (Feature → Advantage → Benefit) as the underlying structure.

## Step 4.6: Thin-Source Expansion (材料少时如何合理扩写)

When the user provides very little source material (e.g., only a few bullet points, a short self-introduction, or sparse data), you must expand the resume content to make it substantive and competitive — **without exaggeration or fabrication**.

**Core principle:** You're not inventing new achievements, you're **unpacking implicit work** that every real developer/engineer does but rarely writes down. Think of it as translating "I did this" into "here's what doing this actually involved."

**How to expand from thin sources:**

### 1. Implicit task decomposition
A single short description like "负责用户模块开发" implies many concrete activities. Unpack it by asking what the role actually entails:

| Source statement | What it actually involves (expandable bullets) |
|-----------------|------------------------------------------------|
| 负责用户模块 | 需求评审 → 接口设计 → 编码 → 自测 → 联调 → 上线 → 线上问题排查 |
| 写了个爬虫 | 目标站分析 → 反爬策略 → 数据清洗 → 存储设计 → 定时调度 → 异常监控 |
| 做了前端页面 | 原型评审 → 组件拆分 → 状态管理 → 接口对接 → 多端适配 → 性能优化 |
| 维护数据库 | 建表规范制定 → SQL 审核 → 慢查询分析 → 索引优化 → 数据迁移 → 备份方案 |

**Expand each phase into its own bullet** with technology keywords and outcomes.

### 2. Standard engineering practices
Every real project involves these — add them even if the user didn't mention:

| Practice | How to describe |
|----------|----------------|
| 版本管理 | "使用 Git 进行分支管理，采用 Git Flow 规范，确保多人协作效率" |
| 代码质量 | "编写单元测试覆盖核心逻辑，测试覆盖率约 80%" |
| 接口设计 | "定义 RESTful API 规范，编写 Swagger/OpenAPI 文档，前后端联调效率提升" |
| 部署上线 | "使用 Docker 容器化部署，编写 CI/CD Pipeline 实现自动化构建" |
| 日志监控 | "集成 ELK/Prometheus 进行日志采集和告警，线上问题定位时间缩短" |
| 技术选型 | "参与技术选型讨论，评估多套方案后确定最终架构" |
| 文档编写 | "输出技术方案文档和接口文档，降低团队知识传递成本" |

### 3. Skill inference from context
If the user mentions a technology, infer what level of competence it implies:

| User says | You can safely write |
|-----------|---------------------|
| 用了 Spring Boot | "基于 Spring Boot 搭建项目骨架，整合 MyBatis/Redis 等组件" |
| 用过 MySQL | "负责数据库表结构设计，编写复杂 SQL 查询和存储过程" |
| 用过 Redis | "利用 Redis 实现缓存、分布式锁、限流等核心功能" |
| 用过 Docker | "编写 Dockerfile 和 docker-compose 配置，实现多服务容器化部署" |
| 用过 Vue/React | "使用组件化开发模式，封装可复用业务组件，提升开发效率" |
| 用过 Linux | "编写 Shell 脚本自动化运维任务，熟悉服务器排错和性能调优" |

### 4. Industry-standard metrics (conservative estimates)
When no numbers exist, use industry-typical ranges with "约" or "约 X+":

| Context | Conservative estimate |
|---------|----------------------|
| 日常业务接口 | 响应时间约 50-200ms，QPS 约数百至数千 |
| 团队协作 | 约 3-10 人小组，迭代周期约 1-2 周 |
| 代码质量 | 核心逻辑测试覆盖率约 70-85% |
| 部署频率 | 每周约 1-2 次迭代发布 |
| 文档产出 | 技术方案文档、接口文档、运维手册等 |

### 5. Project lifecycle framing
Wrap thin content in the full project lifecycle to show depth:

```
【项目背景】→ 说明为什么做这个项目（业务需求/痛点）
【技术选型】→ 说明为什么选这套技术栈
【核心工作】→ 你具体做了什么（拆解为 3-4 个 bullet）
【项目成果】→ 上线后的效果（保守估算）
```

**Before vs After (thin source):**

| Before (too thin) | After (expanded, honest) |
|-------------------|--------------------------|
| "做过一个电商项目" | "参与电商平台核心模块开发，基于 Spring Boot + MyBatis 搭建项目骨架，负责商品管理和订单模块的接口设计与实现。使用 Redis 缓存热点数据，编写 Dockerfile 完成容器化部署，输出技术方案文档和接口文档，项目按期上线运行稳定。" |
| "负责前端页面开发" | "基于 Vue3 + Vite 搭建前端项目，使用 TypeScript 进行类型约束，封装约 15+ 个可复用业务组件。对接后端 RESTful API，完成多端适配和页面性能优化（首屏加载时间约 1.5s 以内），编写单元测试覆盖核心组件。" |
| "写了几个脚本" | "编写 Python Shell 脚本实现日常运维任务自动化（日志清理、数据备份、服务健康检查等），集成 Cron 定时调度，减少人工运维操作约 60%，编写运维手册方便交接。" |

**⚠️ Boundaries — what NOT to do:**
- **NEVER** invent companies, positions, or projects that didn't exist
- **NEVER** claim leadership ("主导", "带领团队") unless the source material supports it
- **NEVER** cite specific award names, certification titles, or publications not mentioned
- **DO** frame standard engineering practices the user likely performed
- **DO** use "参与", "负责", "协助" honestly based on the implied scope
- **DO** ask the user to confirm uncertain details before finalizing

## Step 5: Choose Style and Render HTML

Styles live under `assets/styles/<name>/` — each has `resume-css.css` + `resume-html.html` (EN) or `resume-html-cn.html` (CN).

| Style | Description |
|-------|-------------|
| **apple** (default) | Dark hero header, large typography, grid cards, blue links — Apple.com inspired |
| **minimal** | Clean typography, centered section headers, left-border accents, no cards — Typora-inspired |
| **corporate** | Orange accent, colored section bars with arrow bullets, dark header, horizontal rules — LaTeXCV modern inspired |
| **heisenberg** | Side-by-side avatar header, soft blue accent, rounded cards, clean divider — Apple-style with subtle tweaks |
| **pulse** | Dark/light alternating sections, orange accent, hero header, skill progress bars — modern web style |

**Pick a style and render:**

1. Read `assets/styles/<name>/resume-html.html` (EN) or `resume-html-cn.html` (CN) for the HTML skeleton
2. Read `assets/styles/<name>/resume-css.css` and paste into the `<style>` block
3. Replace placeholder content with extracted data

> If user doesn't specify a style, ask. Default to `apple`.

**Adding a new style:** Create `assets/styles/<name>/` with `resume-css.css`, `resume-html.html`, and `resume-html-cn.html`. Use the same HTML class names (`.header`, `.job-card`, `.skills-grid`, `.edu-table`, etc.) so data injection works across all styles.

## Step 6: Crop and Embed Avatar

```bash
# Center-crop + Base64 embed (default 100x100px)
python scripts/embed_avatar.py avatar.jpg resume.html

# Custom size
python scripts/embed_avatar.py avatar.jpg resume.html --size 120 -o final.html
```

The script center-crops to a square and resizes — the avatar stays centered in the circular frame regardless of original aspect ratio.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Avatar not embedded — script says success but no image | `embed_avatar.py` tries 5 strategies: data URI, `<div class="avatar">`, placeholder, container/body injection. If none match, the HTML structure deviates from the template — check the HTML manually. |
| Avatar/text overlap on mobile | `flex-direction: column` + `align-items: center` below 640px |
| CSS `:root` variables lost during template injection | Ensure `:root` block is at the top of `<style>` |
| Duplicate/conflicting timeline data | Sort by date first, deduplicate, then extract |
| CJK text rendering | Include `'Noto Sans SC'` in `font-family`, ensure `<meta charset="UTF-8">` |
| Email charset detection fails | Try `part.get_content_charset()` first, fallback to `utf-8` |

## Color Reference (Apple Style)

| Use | Value |
|-----|-------|
| Background | `#f5f5f7` (Apple light gray) |
| Card | `#ffffff` |
| Border | `#d5d5da` |
| Primary text | `#1d1d1f` |
| Secondary text | `#86868b` |
| Links/accent | `#0071e3` (Apple Blue) |
| Metrics | `#34a853` (green) |
| Tags/badges | `#ff9500` (orange) |

## Footer Rules (IMPORTANT)

- The `<div class="footer">` at the bottom of the HTML should contain **only** a simple, clean closing — nothing more.
- **NEVER** write things like "Based on materials...", "Generated from...", "Built from weekly reports...", or any summary of the source data.
- **NEVER** add timestamps, watermarks, disclaimers, or attribution to the generation process.
- If in doubt, leave the footer empty or remove it entirely. Less is always better.

## Step 7: Generate Markdown Version

After the HTML is finalized, generate a clean Markdown version of the same resume content:

1. Convert each HTML section to Markdown (headers → `#`, lists → `-`, tables → pipe tables, etc.)
2. Keep the same structure and content — don't lose any information
3. Save as `resume-name-final.md`

## Step 8: Generate PDF

Convert the final HTML to PDF:

```bash
python scripts/html_to_pdf.py resume-name-final.html
```

Outputs `resume-name-final.pdf`. Uses weasyprint (preferred), falls back to wkhtmltopdf or chromium.

## Deliverable

Deliver all three:

| File | Use case |
|------|----------|
| `resume-name-final.html` | Single-file, inline CSS + Base64 avatar, opens directly, email-safe |
| `resume-name-final.md` | Plain text, version-control friendly, easy to paste into ATS systems |
| `resume-name-final.pdf` | Print-ready, shareable, consistent layout across devices |
