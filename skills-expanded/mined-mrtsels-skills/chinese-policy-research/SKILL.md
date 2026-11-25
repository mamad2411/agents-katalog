---
name: chinese-policy-research
description: "Research, document, and analyze Chinese government industrial/SME support policies across province/city/district levels. Produces traceable markdown archives + xlsx mapping to enterprise system scoring rules."
---

# Chinese Policy Research — SME & Industrial Policy Analysis

Systematic methodology for researching Chinese government policies (专精特新/中小企业扶持/产业政策), producing fully traceable documentation with clause-level citations and system-business mapping.

## Triggers

Use when the user asks to:
- "收集XX省/市/区的中小企业扶持政策"
- "分析政策与系统的关联" / "做业务需求分析"
- "把政策原文转成markdown存档"
- "查找专精特新/小巨人相关奖励金额"
- Any policy-to-system mapping task for the enterprise platform

## Workflow

### Phase 0: Save ChatGPT Output Immediately

**CRITICAL RULE — User corrected this hard:** When the user sends ChatGPT search results via WeChat, **save them first as-is**. Do NOT:
- ❌ Add "待补充" markers for missing URLs — save what you have, mark gaps later
- ❌ Wait to verify URLs before saving — save first, verify in a separate step
- ❌ Rewrite the user's content before saving — preserve the exact structure they sent
- ✅ Create the summary markdown file immediately with what you have
- ✅ Mark genuinely missing info (e.g., "URL来自ChatGPT，待验证") in a separate note
- ✅ Then refine and verify URLs independently

### Phase 1: Search Methodology

**DO NOT use Hermes's browser/search tools for government policy searching.** Chinese government websites (gov.cn, gd.gov.cn, etc.) are unreliable via API/browser automation. Instead:

1. **Use web-based AI** — Ask the user to search via DeepSeek/ChatGPT web version
2. **Provide structured prompts** — Write a `search-prompts-guide.md` with exact prompts organized by:
   - Province-level: 主干政策 → 配套政策 → 资金额度
   - City-level: 主干政策 → 配套政策
   - District-level: 产业扶持 → 专项政策
3. **Each prompt must specify**:
   - Exact output format (see Phase 2)
   - Requirement for original URLs — **raw strings only (`https://...`), NOT markdown links** (ChatGPT defaults to `[text](url)` format — explicitly tell it not to)
   - Which departments to search (工信厅/科技厅/财政局/人社局/市场监管局等)

### Phase 2: Markdown Documentation (TWO files per policy)

Every policy produces **exactly two files**:

**File A: Summary + System Mapping** (`XX-政策简称.md`)
- 政策基本信息表 (name, document number, date, department, URL)
- 核心条款摘要 per category (资金奖励/融资/人才/技改/认定标准)
- **与系统的关联** section — table mapping policy clauses to enterprise system rules

**File B: Full Original Text** (`XX-政策简称-原文.md`)
- Complete verbatim transcription of the policy PDF/HTML source
- Include attachments, annexes, contact information
- Use `fitz` (PyMuPDF) for PDF extraction, terminal `curl` for HTML

**Format requirements:**
- **URLs must be raw strings** (`https://...`), NOT markdown links `[text](url)` — this kills traceability when pasted into reports/Word/PDF
- **Each clause must cite its article number** in parentheses — e.g., "（依据：第十九条）" not "（依据：19条）"
- **Article numbers must match the original exactly** — "第十九条" not "第19条" or "十九条"
- **AI-hallucinated URLs are a known pitfall** — gov.cn URLs from ChatGPT are frequently wrong. Verify by accessing the URL. If 404, search via Google or the issuing department's site
- **中央政策URL may 404** — gov.cn policy library URLs sometimes die after content migration. Use the附件PDF from provincial implementation notices as fallback

### Phase 3: URL Verification

After initial markdown is saved:
1. Test each URL with `curl -sL -o /dev/null -w "%{http_code}" <url>`
2. If 404, search for the correct URL on the issuing department's site
3. If the URL was from ChatGPT and is wrong, note it explicitly: "URL由ChatGPT提供但已失效，需人工搜索"
4. For PDFs that are attachments, the full URL including Chinese filename is valid — don't strip or URL-encode it

### Phase 4: System Mapping xlsx

After collecting all policies, create TWO xlsx files:

**xlsx A: Policy-Score Mapping** (`policy-score-mapping.xlsx`)
- Sheet 1: 条款→系统评分映射 — 8 columns: 政策类别, 政策名称, 条款类型, 具体条款/金额, 企业需满足条件, 对应系统评定规则, 系统已有/需补充, 备注
- Sheet 2: 系统缺口分析 — 5 columns: 缺口编号, 缺口领域, 具体缺口描述, 建议新增功能, 优先级
- Priority: P0-高 (blocking), P1-中 (important), P2-低 (nice to have)
- Use openpyxl (available) with frozen header row

**xlsx B: Master Summary** (`policy-master-summary.xlsx`)
- Sheet 1: 政策汇总表 — **10 columns** (user's exact format):
  ```
  政策名称 | 文号 | 发布日期 | 发文部门 | 政策层级 | 主要扶持对象 | 扶持类型 | 奖补金额/标准 | 申报条件摘要 | 政策链接URL
  ```
- Sheet 2: 按扶持类型分类 — for cross-cutting analysis by subsidy type

### Phase 5: Parallel Batch Fetching

When the user provides multiple policy URLs for original text extraction, **use `delegate_task` with sub-agents in parallel** (up to 3 concurrent children):
1. Each sub-agent handles ONE policy
2. Give it the URL, known info, and exact file paths
3. Each creates both `-原文.md` and `.md` files independently
4. Each sub-agent should fetch the URL with `curl`, extract with `python3` or `fitz` for PDF
5. After all sub-agents complete, verify all files were created, then update xlsx summaries

### Phase 6: Full Original Text Transcription (from URL)

When the user asks "把原文转下来" or provides corrected URLs:
1. Fetch the URL using `curl -sL -A 'Mozilla/5.0'`
2. For HTML: use `python3` to strip tags and extract readable text
3. For PDFs: use `fitz` (PyMuPDF) — `doc = fitz.open(path)` then `page.get_text()`
4. Save as a complete markdown file with `-原文.md` suffix
5. Include full text: attachments, annexes, forms, footers
6. Preserve article numbering exactly as in the original
7. Verify no content was lost — check total output size vs source

## Directory Structure

```
docs/policy-research/
├── province/                    # 省级政策
│   ├── 01-梯度培育管理实施细则.md     # 摘要+系统映射
│   ├── 01-梯度培育管理实施细则-原文.md # 原文全量
│   └── ...
├── city/                        # 市级政策
│   └── ...
├── district/                    # 区级政策
│   └── ...
├── analysis/
│   ├── policy-score-mapping.xlsx     # 条款→评分映射表
│   └── business-requirements.md      # 业务需求分析
└── search-prompts-guide.md          # 搜索提示词文档
```

## Pitfalls

1. **ChatGPT hallunicates government URLs** — Always verify URLs work before saving. If 404, search via Google or the issuing department's official site
2. **政策层级混淆** — Distinguish between: 正式政策文件 vs 申报通知 vs 公示名单. Only the first counts as policy; the others are references
3. **金额核对** — 区分"省市叠加"和"不重复享受". Note: 广东省级无统一认定奖励标准（由各市/区配套）
4. **不要重复计算** — 有些奖励是"省市叠加申报"，有些是"同一笔钱分两级表述"
5. **条款引用必须精确** — 政策原文的"第十九条"不能写成"十九条"或"第19条"，保持与原文一致
6. **中央政策URL可能已404** — gov.cn的政策文件库URL可能在文件更新后失效，用附件PDF路径替代

## User Preferences

- 格式：表格化的政策基本信息 + 逐条引用（带条款号）+ 系统关联分析
- 语言：简洁直接，不要AI文案腔
- 每份政策必须是独立文档，不可多政策混编
- **URL必须是纯字符串**（`https://...`），不可用 markdown 链接 `[text](url)` 格式
- **原文是首要产出**，摘要只是辅助——先存原文再写分析

## Reference Files

| File | Purpose |
|------|---------|
| `references/policy-format-template.md` | Standard template for individual policy markdown files |
| `references/search-prompts.md` | 7 search prompts for province/city/district policy research |
| `references/master-summary-template.md` | 10-field master xlsx template + known subsidy amounts |
