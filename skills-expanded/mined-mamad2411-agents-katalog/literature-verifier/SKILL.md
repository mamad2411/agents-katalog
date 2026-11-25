---
name: literature-verifier
description: Verify the authenticity of literature references and detect hallucinations in both English and Chinese (中文) sources. Use when users need to check if a citation is real, verify a DOI, confirm a paper/article/book exists, cross-check author-title-journal-year metadata, detect fabricated references, validate URLs of online articles, or audit a reference list for accuracy. Covers journal papers, conference papers, preprints, books, monographs, newspaper articles, magazine articles, web articles, dissertations, government documents, and any other published works. Supports Chinese academic databases including CNKI (知网), Wanfang (万方), CQVIP (维普), Baidu Scholar (百度学术), and core journal list verification (北大核心, CSSCI, CSCD).
---

# Literature Verifier

Verify authenticity and detect hallucinations in literature references of any type and any language: journal articles, books, web articles, conference papers, preprints, newspaper/magazine articles, dissertations, government documents, and more. Full support for both English and Chinese (中文) literature verification.

## Verification Workflow

1. **Detect language**: Determine if the reference is Chinese or English (or mixed)
2. **Parse** the reference to extract structured fields (title, authors, year, journal/venue, DOI, URL, ISBN)
3. **Verify existence** using appropriate sources:
   - English: DOI → CrossRef; URL → HTTP check; title → CrossRef search
   - Chinese: title → CNKI via Chrome CDP (primary), WebSearch (fallback); DOI → CrossRef (if available)
4. **Cross-check metadata** between claimed and actual values
5. **Assess confidence** and report findings
6. **Verify claims** if the user asks about specific content attributed to the source

## Verification by Identifier Type

### Has DOI

Run `scripts/verify_doi.py "<doi>"`. Compare returned metadata (title, authors, journal, year) against the user's citation. Flag any mismatch.

### Has Title (No DOI)

Run `scripts/search_crossref.py --title "<title>"`. If results return, compare the top match's metadata against the citation. If no match, try adding `--author "<last_name>"`.

### Has URL

Run `scripts/verify_url.py "<url>"`. Check reachability, page title, and extracted metadata (citation_doi, citation_title, article_author). If URL is dead, suggest Wayback Machine: `web.archive.org/web/<url>`.

### Has ISBN (Books)

Use WebSearch to query `"ISBN <number>" site:openlibrary.org OR site:worldcat.org` and verify the book record.

### Minimal Information

Use WebSearch to search for the claimed title + author + year. Cross-reference results from Google Scholar (`site:scholar.google.com`), publisher sites, and library catalogs.

## Chinese Literature Verification (中文文献核查)

Chinese literature requires different verification strategies because most Chinese publications are not indexed in CrossRef. **当 Chrome MCP 工具可用时，必须使用知网 CDP 直接检索作为首选核查方法**；MCP 工具不可用时，以 WebSearch 作为备选。不得仅生成搜索链接或以"需知网核实"搪塞。每条中文文献必须给出明确判定。

### 知网 CDP 直接检索（中文期刊论文首选方法）

当 Chrome MCP 工具可用时（navigate_page、take_snapshot、take_screenshot、fill、click、evaluate_script、wait_for），对每条中文期刊论文优先使用此方法。此方法直接查询知网数据库，准确率远高于 WebSearch。

**前置检查**：尝试对任意页面执行 `take_snapshot`，若 MCP 工具正常响应则使用 CDP 方法；若不可用（报错/超时）则跳至下方 WebSearch 备选流程。

**批量核查注意**：连续检索多篇论文时，每次检索间隔 2-3 秒，避免触发知网反爬机制。

#### CDP Step 1: 打开知网高级检索页面

```
navigate_page → https://kns.cnki.net/kns8s/AdvSearch
```

**验证码处理**：snapshot 的 DOM 中可能始终包含隐藏的"拖动下方拼图完成验证"文本，**不能仅凭 snapshot 文本判断验证码是否出现**。必须用 `take_screenshot` 截图查看页面实际显示状态：
- 若截图中**可见**验证码滑块弹窗遮挡页面，提示用户："知网需要安全验证，请在浏览器中完成滑块验证，完成后告诉我。"
- 若截图中页面正常显示检索表单（无遮挡），直接继续。

#### CDP Step 2: 输入待核查论文的精确标题

用 `take_snapshot` 找到检索输入框，然后：

```
fill → [检索输入框] → "<待核查论文的完整标题>"
```

默认检索字段为"主题"，对精确标题核查已足够，无需修改字段类型或添加其他筛选条件。

#### CDP Step 3: 执行检索

点击"检索"按钮，等待结果页加载：

```
wait_for → "检索结果" 或结果列表出现
```

若此时出现验证码，按 Step 1 处理。

#### CDP Step 4: 读取并解析结果

先用 `take_snapshot` 查看结果页，然后用 `evaluate_script` 提取结构化数据：

```javascript
evaluate_script → () => {
  const rows = document.querySelectorAll('.result-table-list tbody tr');
  if (!rows || rows.length === 0) return JSON.stringify({found: false, results: []});
  const results = [];
  rows.forEach((row, i) => {
    if (i >= 10) return;
    const titleEl = row.querySelector('.name a');
    const authorsEl = row.querySelector('.author');
    const sourceEl = row.querySelector('.source');
    const dateEl = row.querySelector('.date');
    results.push({
      title: titleEl ? titleEl.textContent.trim() : '',
      authors: authorsEl ? authorsEl.textContent.trim() : '',
      source: sourceEl ? sourceEl.textContent.trim() : '',
      date: dateEl ? dateEl.textContent.trim() : ''
    });
  });
  return JSON.stringify({found: results.length > 0, count: results.length, results});
}
```

**若 JS 选择器不工作**（知网可能更新 DOM 结构），回退到直接阅读 `take_snapshot` 的文本输出，其中包含可读的标题、作者、期刊、日期信息，手动解析即可。

**若结果为零**：论文未在知网检索到。这是重要信号但不是唯一依据，继续执行 WebSearch 备选流程检查万方和百度学术后再下结论。

#### CDP Step 5: 元数据比对

将知网结果与声称的引用信息逐项比对：

| 字段 | 比对方法 |
|------|----------|
| **标题** | 去除空白后精确匹配。若知网结果标题包含声称标题（或反之），视为匹配。 |
| **作者** | 检查声称的第一作者是否出现在知网作者列表中。作者顺序可能不同。 |
| **期刊** | 精确名称匹配。注意缩写差异（如"北京大学学报" vs "北京大学学报(哲学社会科学版)"），任一方向的子串匹配算作匹配。 |
| **年份** | 知网日期字段中的年份必须与声称年份一致。 |

#### CDP Step 6: 根据 CDP 结果判定

| CDP 结果 | 判定 |
|----------|------|
| 标题精确匹配 + 作者匹配 + 期刊匹配 + 年份匹配 | **Confirmed** |
| 标题精确匹配 + 其余3项中2项匹配 | **Likely Real**（标注差异项） |
| 标题精确匹配 + 期刊或作者不匹配 | **Metadata Error**（论文存在但引用信息有误） |
| 前10条结果中无标题匹配 | 继续执行 WebSearch 备选流程后再判定 |

#### CDP 异常处理

- **MCP 工具不可用**：整体跳过，使用 WebSearch 备选流程
- **验证码持续阻塞**：请用户处理；用户无法处理则跳至 WebSearch
- **页面加载后搜索报错**：重试一次；仍失败则跳至 WebSearch
- **知网不可访问**：跳至 WebSearch
- **DOM 选择器返回空**：改用 `take_snapshot` 文本手动解析；也失败则跳至 WebSearch

### WebSearch 中文核查流程（备选方法 / CDP 不可用时使用）

当 Chrome MCP 工具不可用时，或知网 CDP 检索返回零结果需要交叉验证时，或需要补充强化 CDP 判定时，使用以下 WebSearch 流程。执行以下所有搜索，不得跳过任何步骤，不得在未完成所有搜索前标记为"Uncertain"。

#### Step 1: Multi-source WebSearch (必做 — 至少3次搜索)

Execute these WebSearch queries in sequence for each paper:

1. **Exact title search**: `"<完整论文标题>"` (with quotes, no site restriction)
2. **Title + author search**: `<论文标题> <作者姓名>` (without quotes, broader match)
3. **Title + journal search**: `<论文标题> <期刊名>` (cross-validate venue)
4. **CNKI-targeted search**: `"<论文标题>" site:cnki.net` (知网)
5. **Wanfang-targeted search**: `"<论文标题>" site:wanfangdata.com.cn` (万方)

If steps 1-3 already confirm the paper exists with matching metadata, steps 4-5 are supplementary. If steps 1-3 yield no results, steps 4-5 are MANDATORY.

#### Step 2: Metadata Cross-check (元数据交叉核验)

From the search results, verify:
- Author name matches
- Journal name matches exactly (beware 学报/杂志/期刊 confusion)
- Publication year matches
- Volume/issue/page numbers if available

#### Step 3: Verdict (必须给出明确判定)

Based on search results, assign ONE of these verdicts — **"Uncertain" is NOT acceptable as a final verdict for Chinese literature**:

| Verdict | Criteria |
|---------|----------|
| **Confirmed** | Found on 2+ sources (CNKI, Wanfang, Baidu Scholar, Google Scholar) with matching metadata |
| **Likely Real** | Found on 1 source with matching metadata, OR found with minor metadata discrepancies |
| **Likely Fabricated** | No results from any search, OR title/author/journal combination not found anywhere |
| **Confirmed Fabricated** | Multiple fabrication indicators: journal doesn't exist, author not in claimed institution, impossible date, etc. |
| **Metadata Error** | Paper exists but with different author/year/journal than claimed |

### Chinese Journal Articles (中文期刊论文)

1. **首选**：执行上方"知网 CDP 直接检索"流程（需 Chrome MCP 工具）
2. **备选**：若 CDP 不可用或返回零结果，执行"WebSearch 中文核查流程"
3. **补充**：运行 `scripts/search_cnki.py --title "<中文标题>"` 尝试 CrossRef 查找（部分中文期刊有 DOI）
4. 若文献有 DOI，运行 `scripts/verify_doi.py`（注意：多数中文文献无 DOI，无 DOI 不代表虚构）

### Chinese Books / Monographs (中文图书/专著)

1. Use WebSearch to query `"<书名>" "<作者>" site:book.douban.com` (豆瓣读书)
2. Use WebSearch to query `"ISBN <号码>"` if ISBN is provided
3. Search National Library of China: `"<书名>" site:opac.nlc.cn`
4. Verify publisher exists and has published the claimed work

### Chinese Dissertations (学位论文)

1. Use WebSearch to query `"<论文标题>" 学位论文 site:cnki.net`
2. Use WebSearch to query `"<论文标题>" 学位论文 site:wanfangdata.com.cn`
3. Verify the degree-granting institution has the relevant discipline

### Chinese Government Documents (政策文件)

1. Use WebSearch to query `"<发文字号>" site:gov.cn`
2. Verify the issuing agency and document number format

### Chinese News Articles (新闻报道)

1. Use WebSearch to query on the claimed media's domain: `"<标题关键词>" site:<媒体域名>`
2. For People's Daily: `site:people.com.cn`; for Xinhua: `site:xinhuanet.com`

### Core Journal Verification (核心期刊验证)

When a reference claims the journal is a core journal (核心期刊), verify against:
- **北大核心**: 《中文核心期刊要目总览》— use WebSearch to check
- **CSSCI (南大核心)**: 中文社会科学引文索引来源期刊 — use WebSearch to check
- **CSCD**: 中国科学引文数据库来源期刊 — use WebSearch to check
- Note: Core journal status changes across editions; verify for the specific year claimed

### Key Differences for Chinese Literature

- **No DOI ≠ fabricated**: Most Chinese journal articles lack DOIs; absence of DOI is not evidence of fabrication
- **Author name formats**: Chinese names in English contexts may appear as "Zhang San", "San Zhang", or "S. Zhang"
- **Indexing lag**: Recently published papers may not yet appear in CNKI
- **Paywall**: CNKI/Wanfang require paid access for full text, but search results and abstracts are usually visible
- **绝不推迟核查**：不得以"需知网核实"或"Uncertain (needs CNKI verification)"作为最终结果。必须使用知网 CDP 或 WebSearch 实际搜索并给出明确判定。
- **知网 CDP 优先**：当 Chrome MCP 工具可用时，优先使用 CDP 直接在知网检索页面搜索，比 WebSearch（通过 Google 间接搜索知网）更可靠，能找到 Google 未索引的知网论文。MCP 不可用时以 WebSearch 为备选。Python 脚本（verify_chinese.py、search_cnki.py）仅作补充。

## Hallucination Detection

When verification fails or metadata doesn't match, consult `references/hallucination-patterns.md` (English) or `references/chinese-hallucination-patterns.md` (中文) to identify which hallucination pattern applies. Common red flags:

- DOI doesn't resolve → likely fabricated DOI (but NOT for Chinese literature without DOI)
- Title search returns no results → likely fabricated title
- Authors don't match → author hallucination
- Journal doesn't exist → venue hallucination
- Year is off → date hallucination
- Chinese journal claimed as core but not in official list → core journal hallucination
- CNKI + Wanfang + Baidu Scholar all return no results → strong indicator of fabrication for Chinese literature

## Batch Verification

When the user provides a reference list, verify each entry sequentially. Produce a summary table:

```
| # | Citation (short) | DOI verified | Title match | Author match | Year match | Confidence |
|---|-----------------|-------------|-------------|--------------|------------|------------|
| 1 | Smith 2020...   | Yes         | Yes         | Yes          | Yes        | Confirmed  |
| 2 | Jones 2019...   | No DOI      | No match    | -            | -          | Likely Fabricated |
```

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **Confirmed** | DOI resolves AND metadata matches across sources |
| **Likely Real** | DOI resolves OR title+author match found, minor discrepancies |
| **Uncertain** | No DOI, no exact title match, but components are plausible. **For Chinese literature, this level is NOT acceptable as final verdict — must execute full WebSearch procedure first.** |
| **Likely Fabricated** | DOI doesn't resolve, no matching work found, hallucination patterns detected |
| **Confirmed Fabricated** | Multiple fabrication indicators, no trace in any database |

## Content Claim Verification

When the user asks whether a specific claim is actually stated in a source:

1. Retrieve the source (via DOI link, publisher URL, or web search)
2. Use WebFetch to read the page content if accessible
3. Search for the specific claim, statistic, or quote
4. Report whether the claim is supported, unsupported, or contradicted

## Report Format

For each verified reference, output:

```
**Reference**: [original citation text]
**Status**: [Confirmed / Likely Real / Uncertain / Likely Fabricated / Confirmed Fabricated]
**Findings**:
- DOI: [resolves / not found / not provided]
- Title: [exact match / partial match / no match]
- Authors: [match / mismatch / details]
- Journal/Venue: [verified / not found]
- Year: [correct / incorrect (actual: XXXX)]
**Issues**: [list any discrepancies or hallucination patterns detected]
**Actual Source** (if different): [correct metadata if the reference is a distortion of a real work]
```

## Resources

- **`scripts/verify_doi.py`** — Verify DOI existence via CrossRef and DOI.org APIs. Returns metadata for comparison.
- **`scripts/search_crossref.py`** — Search CrossRef by title/author/keywords. Find whether a claimed work exists.
- **`scripts/search_cnki.py`** — Generate search URLs for Chinese databases (CNKI, Wanfang, CQVIP, Baidu Scholar) and attempt CrossRef lookup. Supplementary tool — always use WebSearch as primary verification method for Chinese literature.
- **知网 CDP 直接检索（通过 MCP 工具）** — 使用 Chrome DevTools Protocol 直接在知网检索页面搜索，核查中文期刊论文的首选方法。需要 MCP 工具：navigate_page、take_snapshot、take_screenshot、fill、click、evaluate_script、wait_for。详见上方"知网 CDP 直接检索"章节。
- **`scripts/verify_chinese.py`** — Attempt direct HTTP verification against Baidu Scholar, CNKI, and Wanfang. May be blocked by anti-bot measures — if so, fall back to WebSearch. Usage: `python scripts/verify_chinese.py --title "<中文标题>" --author "<作者>"`
- **`scripts/verify_url.py`** — Check URL reachability and extract page metadata (title, author, DOI from meta tags).
- **`references/hallucination-patterns.md`** — Catalog of common hallucination types for English literature. Read when fabrication is suspected.
- **`references/chinese-hallucination-patterns.md`** — Catalog of hallucination types specific to Chinese literature (中文文献幻觉模式). Read when Chinese reference fabrication is suspected.
- **`references/verification-checklist.md`** — Comprehensive step-by-step checklist for English literature verification.
- **`references/chinese-verification-checklist.md`** — Comprehensive checklist for Chinese literature verification (中文文献核验清单), including CNKI, Wanfang, core journal, dissertation, and government document checks.
