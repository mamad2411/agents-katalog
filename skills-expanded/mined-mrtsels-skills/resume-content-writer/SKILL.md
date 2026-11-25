---
name: resume-content-writer
description: "Use when writing resume content — bullet formula, EN style rules, metrics, section templates, ATS formatting, tailoring, Chinese finance/AM bullets."
---

# Resume Content Writer

Trigger: use when writing, rewriting, or tailoring resume bullet points and sections from raw experience notes or existing drafts — English or Chinese. The sections follow the content pipeline in execution order: draft achievement bullets → quantify impact → apply voice/style rules → assemble sections → format for ATS → tailor to a target job → write finance/AM bullets (EN and 中文).

## 1. Bullet Formula — Achievement-Focused Writing

Every bullet is an achievement statement, not a duty description. Build each one with:

```
Action Verb (past tense) + What You Did + How You Did It + Measurable Result
```

- Lead with the strongest past-tense action verb; never start with "Responsible for".
- Use STAR (Situation, Task, Action, Result) as a drafting aid, then compress to one sentence.
- Stay truthful while maximizing impact; where the metric is unknown, estimate from known scope (see §2).

### Strength scale

| Level | Example | Score |
|-------|---------|-------|
| Weak | Responsible for managing team | 1/5 |
| Better | Led team of 5 engineers | 3/5 |
| Strong | Led team of 5 engineers to ship 3 products, increasing revenue by $2M | 5/5 |

### Common mistakes to fix
- Starting with "Responsible for" → lead with the action verb instead.
- Listing duties without results → end every bullet with an outcome.
- No numbers or metrics → quantify per §2.
- Passive voice ("was responsible", "was involved") → convert to active per §3.
- Vague language ("various", "several", "multiple") → replace with scope figures.
- Wrong length (over 2 lines or under half a line) → keep 1–2 lines.

### Diagnosis checklist (for reviewing existing bullets)
1. **Categorization** — one function per bullet, or mixed unrelated work?
2. **Quantification** — is there a number (count, volume, %, entities)? If not, add one or estimate (§2).
3. **Impact** — does it say who used the work or what decision it supported?
4. **Verb strength** — is the first word a strong past-tense action verb?
5. **Conciseness** — does it fit 2 lines after compilation?

## 2. Quantifying Impact

Add metrics to every bullet, even when exact data is missing.

### Metric types
- **Scale**: users served, revenue handled, team size
- **Efficiency**: time saved, cost reduced, process improved
- **Impact**: revenue generated, adoption rate, satisfaction score
- **Scope**: projects managed, regions covered, budget size

### Estimation guidelines
- Use ranges when exact numbers are unknown (10–15 people, $500K–$1M).
- Use approximate indicators ("over", "nearly", "approximately").
- Be conservative — understating beats overstating.
- Never fabricate precise numbers; estimate from known scope, flag the estimate, and use industry benchmarks when available. (This user permits estimated metrics where the scope is known — e.g. "10+ clients" from a real client list.)

### Where to add metrics (by function)
- **Leadership**: team size, budget, project count
- **Engineering**: system scale, performance gains, uptime
- **Sales/BD**: revenue targets, deal size, quota attainment
- **Product**: users impacted, feature adoption, NPS
- **Operations**: cost savings, efficiency gains, error reduction

## 3. Voice & Style Rules (English)

Resume-specific grammar that overrides standard English — non-negotiable in final output.

| Rule | Wrong | Right |
|------|-------|-------|
| No articles a/an/the (unless unavoidable) | Developed a system that reduced the latency | Developed system reducing latency |
| Past-tense action verb, no subject | Was responsible for backend; He built the API | Designed RESTful API |
| No passive voice | Was involved in testing; Was hired to lead | Led QA team of 5 |
| Replace be/have with strong verbs | Was the lead engineer; Had responsibility for | Architected microservices pipeline |
| Nouns over gerunds | Helped in reducing latency | Reduced latency by 40% |
| No filler words: various, several, multiple, significant, very | Processed various data sources | Processed 15+ data sources |

Apply in this order:

1. **Delete filler words** — strip `various`, `several`, `multiple`, `significant`, `very`, `extremely`, `quite`, `really`; frame scope (`10+ clients`) when the metric is unknown.
2. **Delete articles** — strike every `a`/`an`/`the` unless removal breaks grammar ("the S&P 500"). Test: read the sentence aloud without the article — if it still parses, cut it.
3. **Convert passive to active** — rewrite `was/were/has been/have been` + past participle as a single past-tense verb; if the subject is missing ("was responsible for"), pick a verb and lead with it.
4. **Replace weak verbs** — scan for `was`, `had`, `has`, `did`, `made`, `got`, `helped`, `participated in`, `involved in`, `responsible for`, `tasked with`, `worked on`; substitute a strong verb: `Designed`, `Implemented`, `Optimized`, `Reduced`, `Architected`, `Built`, `Developed`, `Led`, `Deployed`, `Automated`, `Engineered`, `Delivered`, `Secured`, `Generated`, `Established`, `Authored`, `Benchmarked`, `Proposed`, `Conducted`, `Analyzed`, `Structured`, `Produced`, `Constructed`, `Integrated`, `Configured`, `Orchestrated`, `Standardized`, `Streamlined`, `Consolidated`, `Accelerated`.
5. **Convert gerunds to nouns** — replace `-ing` phrases (`Helped in reducing`, `Contributed to building`, `Assisted in developing`) with bare past-tense verbs: `Reduced`, `Built`, `Developed`.
6. **Verify length** — each bullet must be 1–2 lines in the final PDF (10pt, 1.5em left margin, 504pt line width); run the LaTeX bullet-fill check after typesetting.

### Verb groups by category
| Category | Verbs |
|----------|-------|
| Research | Conducted, Performed, Investigated, Examined, Evaluated, Assessed, Reviewed |
| Financial | Modeled, Forecasted, Projected, Estimated, Valued, Benchmarked |
| Data | Collected, Compiled, Analyzed, Processed, Synthesized, Visualized |
| Deliverables | Produced, Presented, Delivered, Recommended, Identified, Generated |

## 4. Section Templates

### Professional Summary
- Experienced hire: `[Title] with [X] years in [industry], specializing in [key skill]`
- Entry level: `[Degree] graduate with experience in [area], passionate about [field]`
- Career changer: `[Previous role] transitioning to [new field], bringing [key transferable skill]`

### Skills Section
- Technical: languages, frameworks, tools, platforms
- Soft skills: leadership, communication, collaboration
- Domain: industry-specific knowledge
- Certifications: relevant credentials

### Experience Section
- Most recent first; group by company, then role.
- 3–6 bullets per role; lead each role with its most impressive achievement.

### Education Section
- Degree, institution, year.
- GPA only if 3.5+ or a recent grad.
- Honors, relevant coursework, thesis (if applicable).

## 5. ATS Formatting Rules

### Core rules
- Single-column layout; no tables, text boxes, columns, graphics, images, or charts.
- Standard fonts only (Arial, Calibri, Georgia, Times New Roman).
- 10–12pt body, 14–16pt headers; consistent spacing throughout.
- Bullet points for experience items; reverse chronological order.

### Format checklist
- Margins 0.5–1 inch all around; line spacing 1.0–1.15.
- Section headers bold, consistent style; no orphan headings at page breaks.
- Contact info at the top of the body (not in the page header).
- File name: `FirstName_LastName_Resume.pdf` or `.docx`.
- Black text only; the PDF must be text-searchable.

## 6. Tailoring to a Job Posting

1. Analyze the job description's requirements.
2. Compare against the master resume.
3. Prioritize relevant experience — reorder bullets, emphasize matching projects.
4. Add missing keywords naturally.
5. Remove or de-emphasize irrelevant content.
6. Adjust the professional summary for the role.
7. Maintain truthfulness — never fabricate experience.

Rules: one resume version per application; track changes against the master; keep the format ATS-compatible (§5).

## 7. Domain Bullet Templates (Equity Research / AM / PE)

For research-oriented roles, bullets follow:

```
Action Verb + Research Scope + Methodology/Tools + Deliverable + Quantified Impact
```

### Template formulas
- Industry research: `Researched [industry] via [methods]; produced [report] on [findings]`
- Company/equity: `Analyzed [company] with [methodology]; delivered [valuation/thesis] for [decision]`
- Competitive benchmarking: `Benchmarked [N] competitors on [dimensions]; identified [insight]`
- Financial modeling: `Built [model] for [purpose]; supported [decision] with [assumptions]`
- Data analysis: `Processed [data scope] with [tools]; surfaced [finding]`
- Policy research: `Reviewed [regulations] across [jurisdictions]; summarized [impact]`
- Competitive landscape: `Mapped [landscape]; positioned [company] vs [peers]`
- Expert interviews: `Interviewed [N] [experts]; synthesized insights into [output]`
- Report output: `Authored [report] covering [contents]; read by [audience]`
- Investment recommendation: `Recommended [action] on [asset] with [rationale]`

### Daily market briefing + trade execution (AM/trust)
Structure: `[market analysis method] + [analysis scope] + [trading method] + [volume/scope]`
- Analysis first: lead with the market review/outlook, then execution.
- Name the methods: index breadth ratios, sector capital flow rankings, moving averages, RSI, VaR, factor attribution for style-rotation signals — never vague "market analysis".
- Intern roles use `Completed` / `Delivered` / `Executed`, NOT `Orchestrated` / `Led` / `Managed` (overstates junior authority).

**Example**: *Delivered daily market briefings using index breadth ratios, sector capital flow rankings, and technical indicators (moving averages, RSI, VaR) with factor model attribution for style rotation signals; executed 30+ daily bond repo and reverse repo orders (GC001–GC014) on [platform] with ¥800M+ daily turnover across exchange and interbank markets.*

### Post-investment / fund monitoring
Structure: `[holdings analysis with methods] + [monitoring method] + [report with contents]`
- Name the methods: concentration ratios, sector exposure, NAV trend comparison, financial news platform search.
- Spell out report contents — "authored post-investment reports covering market review, holdings analysis, and sub-advisor assessments", not just "authored reports".

**Example**: *Completed Q2 portfolio holdings analysis (concentration, sector exposure, NAV trends) for 10+ FoF products and monitored sub-advisor negative news via financial news platforms and web searches; authored post-investment reports covering market review, holdings analysis, and sub-advisor assessments across dozens of partner fund managers (¥10B+ total AUM).*

### ATS keywords (ER / AM / PE)
Naturally include: Equity Research, Fundamental Analysis, Financial Statement Analysis, Financial Modeling, DCF Valuation, Comparable Company Analysis, Sensitivity Analysis, Investment Thesis, Bloomberg, Wind, Capital IQ, FactSet.

## 8. 中文简历 Bullet 风格（金融 / AM / FoF）

面向金融方向实习岗（资产管理、FoF、信托）的中文 bullet 写作规则，与英文主体规则互补。

### 1. 动词强度不越级
实习岗用执行级动词，不用管理级：

| 避免（过于宏大） | 改用 |
|---|---|
| 统筹 | 完成、参与、执行 |
| 管理全流程 | 完成X、Y、Z |
| 产出 | 编制、撰写、完成 |
| 负责 | 参与、协助、执行 |

对：`完成十余只FoF产品二季度持仓分析…覆盖数十家合作基金公司、总规模超百亿`
错：`统筹公司FoF产品投后全流程`

### 2. 必须带范围数字
- 产品数量：`十余只FoF产品`、`30+笔`
- 主体数量：`数十家合作基金公司`、`30+家公司`
- 规模：`总规模超百亿`、`日均成交超8亿元`、`50亿元资产配置`

### 3. 行情分析必须点名方法
泛泛的"分析市场行情"太含糊，须写明具体技术：

```
指数涨跌比           → index breadth ratios
板块资金流向排名      → sector capital flow rankings
技术指标（均线、RSI） → moving averages, RSI, VaR
因子归因              → factor model attribution
```

顺序：先分析/展望，后执行/交易。

### 4. 投后 bullet 三段结构（FoF/信托）
1. **持仓分析** — `个股集中度、行业暴露、净值变化`
2. **负面舆情监控** — `通过网络及财经资讯平台检索投顾负面舆情`
3. **报告** — `编制含市场复盘与持仓分析的投后管理报告`

用范围数字收尾：`覆盖N家合作基金公司、总规模超¥X亿`

### 5. LaTeX 注意
- `%` 必须转义：`60\%`、`94\%`
- 日期区间用 `\textendash`：`2026/07\textendash 2026/08`
- 教授链接用 `\ResumeUrl{URL}{text}`，可放在 `[]` 副标题参数内
- linespread 只在 cls 文件设置，不要在 main `.tex` 重复设置

### 中文快速模板
```
完成[数量]FoF产品二季度持仓分析（个股集中度、行业暴露、净值变化），
通过网络及财经资讯平台检索投顾负面舆情；
编制含市场复盘与持仓分析的投后管理报告，
覆盖[数量]家合作基金公司、总规模超¥[数字]亿
```

```
每日复盘市场行情，运用指数涨跌比、板块资金流向排名及技术指标（均线、RSI），
结合因子归因识别轮动信号；
在xQuant OMS执行[数量]笔日频债券回购与逆回购，日均成交超¥[数字]亿元
```

### 中文自查
1. 无 `统筹` / `管理全流程` / `产出`，换用级别合适的动词
2. 至少一个范围数字
3. 行情类 bullet 点名具体方法
4. 先分析后执行
5. 所有 `%` 已转义为 `\%`

## 9. Pitfalls

- Article deletion mangles technical terms and proper nouns (GPT-o3-mini, LoRA, PDE) → the rules apply to prose, not names; keep proper nouns intact for scannability.
- Fixed phrases break ("the S&P 500", "the University of Hong Kong", "a priori") → never strip articles from fixed phrases.
- Style pass runs during the first draft and blocks content → write for completeness first; voice editing is a separate pass.
- Precise numbers get invented when data is missing → estimate with ranges/approximate indicators from known scope and flag them.
- Intern bullets overstate authority (统筹, Orchestrated, Led) → use execution verbs (完成/参与/执行, Completed/Delivered/Executed).
- Market bullets say "分析市场行情" with no method → name the techniques (breadth ratios, capital flows, RSI, factor attribution).
- Reports are claimed generically ("authored reports") → spell out contents (market review, holdings analysis, sub-advisor assessments).
- Bullets overflow to 3+ lines after typesetting → keep 1–2 lines and re-check in the final PDF.
- `%` in LaTeX bullets is parsed as a comment → escape every `%` as `\%`.
- Experience is fabricated while tailoring → never add experience that does not exist; track changes against the master resume.
- ATS parser drops content on fancy layout → single column, standard fonts, no tables/images, text-searchable PDF.

## 10. Verification

Pick any 3 bullets from the output and check each against the EN rules:

```
Rule 1 (articles): PASS/FAIL
Rule 2 (no passive): PASS/FAIL
Rule 3 (strong verb): PASS/FAIL
Rule 4 (past tense): PASS/FAIL
Rule 5 (nouns > gerunds): PASS/FAIL
Rule 6 (filler): PASS/FAIL
Rule 7 (length ≤2 lines): PASS/FAIL
```

Also verify: the §5 format checklist (margins, fonts, searchable PDF), the tailoring diff against the master (§6), and §8's 中文自查 for any Chinese bullets.

## 11. References

- `project-to-resume` — extract project context and generate resume-ready bullets from a project directory.
- `resume-latex-workflow` — LaTeX typesetting, bullet-fill/length checks, and iterative resume editing.
