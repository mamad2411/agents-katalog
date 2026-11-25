---
name: structured-research-report
description: Write a structured research report from task instructions (email + PDF), then iteratively refine based on user feedback. Covers plan-first, source-accurate terminology, section structure, code+mermaid for algorithms, and format preferences.
version: 1.0.0
---

# Structured Research Report

Use this skill when the user provides a task description (email, message) plus PDF reading material(s) and asks you to write a report.

## Workflow

### Phase 1 — Gather sources
1. Read the task instruction (email, chat message, attached file).
2. If a PDF is attached, read it with `vision_analyze` (PDFs may be image-based). Save extracted text for reference.
3. **If sources come as a JSON file of pre-extracted texts**: 
   a. First `read_file` the JSON to list all entries (filename, pages, text_len) — this shows what's available.
   b. For multi-document JSON: write a small Python script that loads the JSON, filters entries by target filenames (use partial string matching against a known list), and reports which matched/missed. Refine matching if needed.
   c. Extract matched entries into individual text files — write a Python script that iterates the target indices and writes `entry["text"]` to separate files. Convention: `/tmp/report_{index:02d}_{shortened_filename}.txt`.
   d. Read each file with `read_file` (short docs: full read; long docs: limit to 200-500 lines per read, use search with context+offset for deep navigation).
   e. For very large documents (40K+ chars): use `search_files` with `context=3-5` and targeted regex patterns to pinpoint relevant sections (e.g., the liquid cooling specific parts of a broader AIDC white paper).
4. Combine email instructions + reading material content into a complete picture.
5. Write a `plan.md` in the task directory covering all sections the report must address.

### Phase 2 — Write report
1. Write `report.md` as the deliverable.
2. Structure follows the source document's section numbering (01, 02, 03, 04).
3. Use the **exact section titles** from the source documents — match capitalization and wording.
4. Section 03 (algorithms) format for each algorithm:
   - Definition (from source)
   - Use case (from source)
   - Parameter table (use dot list if user prefers, or table)
   - Mermaid flowchart
   - Python code
   - Edge cases (Order incompletion, Inadequate liquidity, Open & close auctions)
5. Section 04: broker implementation differences in table with `维度 | Side A | 后果 | Side B | 后果` format.

### Phase 3 — Iterate on details
The user will give micro-corrections one at a time. Apply each immediately without asking "do you want me to also do X for others" — fix what's asked, wait for next instruction.

## Format Rules (general)

- **Time format** — X:XX AM/PM ET (e.g., 9:30 AM – 4:00 PM ET, with spaces around dash)
- **No AI-isms** — Don't use: comprehensive, delve into, in conclusion, it is important to, it should be noted
- **Tables** — Use markdown tables for comparisons, dot lists (with — separator) for parameter lists
- **Don't duplicate** — When two entities (e.g., Nasdaq/NYSE) are identical, state once and note they're the same
- **No placeholder names** — A/B labels without meaning are useless. Describe the actual difference and its consequence
- **Source-accurate titles** — Match source document title casing exactly. If source says "Agency Trading algorithms" (lowercase a), use that
- **Edge cases** — Label exactly as: "Order incompletion", "Inadequate liquidity", "Open & close auctions"

## Sell-side / Brokerage Research Report Mode (券商研报格式)

Trigger when: user provides a sell-side research report as a style reference (e.g. 广发证券/中信/中金 report) and asks you to write industry research in the same format.

### Section-level structure

1. **Each paragraph begins with a summary sentence** — The first sentence of every paragraph must state the core claim of that paragraph. Subsequent sentences provide supporting data, logic, and commentary. This is non-negotiable: a reader should be able to skim the first sentence of every paragraph and get the full thesis.
2. **Focus on "logic" and "data", not description** — Every claim must be supported by a data point or a logical chain. Pure description ("X does Y") without a "why it matters" or "what it implies" is unacceptable.
3. **Charts and tables ≈ 1:1 with text** — Every ~100 words of narrative should have a corresponding chart, table, or diagram. Avoid long text blocks without visual breaks. Use:
   - ASCII/Unicode bar charts for simple value comparisons (`███████` style)
   - Markdown tables for structured data
   - ASCII tree/flow diagrams for frameworks and processes
   - Mermaid only when you need complex or standard flowcharts
4. **Do NOT use placeholder chart placeholders** — If you reference a figure/table in text, include it inline (ASCII, table, or diagram). Never write "[Insert figure here]" or "图X".
5. **Every chart/table must have a data source line** — Format: `数据来源：<source>（底稿：GF_LC_Fig_文件名.xlsx）`
6. **Every data point must have a real source** — If you don't have the data, make the claim weaker or drop it. Never invent numbers.
7. **Image/source file tracking** — At the end of each major subsection, add a note block:
   ```
   > 图X底稿存放路径：`<workdir>/fig/`（待补充图表源文件）
   > 表X数据底稿：`<workdir>/data/`（待补充Excel源文件）
   ```
8. **Sub-section numbering** — Follow the source report's numbering scheme exactly (三、1 → 三、2 → 三、3 → 三、4).

### Paragraph-level writing rules

- **Topic sentence first** — Every paragraph opens with a **bolded summary sentence** that encapsulates the entire paragraph. Example: **"冷板是液冷系统中价值量最大的单一部件，但其毛利率分化巨大。"**
- **One idea per paragraph** — If you have two distinct claims, use two paragraphs.
- **Supporting data ties back to the claim** — After the topic sentence, immediately provide the specific data point that proves it, then explain the logic.
- **End with judgment/comparison** — Last sentence should contextualize: why this matters, how it compares, or what it implies.
- **Avoid "据我们分析/我们认为" filler** — Use only when you're making an original forecast or judgment the data doesn't directly prove. For factual statements driven by data, just state the fact and cite the source.

### Workflow

1. **Start with outline** — Write an outline in `report-outline.md` showing every subsection and its logic chain. Get user approval before writing full text.
2. **Work directory** — Create `docs/jul-NN-topic/` with subdirectories `fig/` and `data/` for chart/data source files.
3. **Write section by section** — Each subsection is a complete logical unit. Don't write everything at once if complex; use `todo` to track progress.
4. **Sample report reference** — When the user provides a sample report (PDF), extract its text first with PyMuPDF and read the relevant sections to understand formatting conventions, section structure, and data source style.

### Phase 4 — Subagent Review & Fix (券商研报模式专用)

After writing the full report, dispatch a subagent to review it before delivery:

1. **Dispatch a subagent** with `delegate_task` using a stronger model (e.g. `deepseek-v4-pro`) to review the draft report file.
2. **Provide context** — Send the report path, format rules (from this skill's sell-side section), and ask for a structured optimization report covering: format compliance, logic gaps, data errors, missing sources, chart imbalance, redundancy, acronym definitions, and any data citation mistakes.
3. **Receive optimization report** — The subagent returns a categorized list (P0=must fix, P1=important, P2=nice to have).
4. **Apply fixes in priority order** — Start with P0 (data errors, missing charts), then P1 (source annotations, methodology notes), then P2 (acronyms, formatting).
5. **Re-verify** — After all fixes, do a quick check that the file still compiles/renders correctly.

### Chart Generation Step (券商研报模式专用)

ASCII charts are for drafts only. For final delivery, generate real SVG charts:

**Matplotlib setup:**
```python
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150; plt.rcParams['savefig.dpi'] = 150
```

**Palette** (use same across all charts in one report):
```python
palette = {'primary_blue': '#2E86AB', 'purple': '#A23B72', 'orange': '#F18F01',
           'red': '#C73E1D', 'green': '#6A994E', 'vibrant_blue': '#2563EB',
           'gray': '#6B7280', 'bg': '#F8FAFC'}
```

**Type-to-chart mapping:**

| Data shape | Chart type | Matplotlib pattern |
|-----------|-----------|-------------------|
| 1D value comparison | Horizontal bar | `ax.barh(cats, vals, color=palette_colors)` |
| Value + margin | Dual-axis combo | `ax1.bar(...)` + `ax2.plot(..., twinx())` for range lines |
| Difficulty/urgency 2D | Scatter + quadrant | `ax.scatter(x, y, s=size)` + quadrant lines at axis midpoints |
| Timeline | Gantt horizontal bars | `ax.barh(pos, dur, left=start, height=0.5)` |
| Multi-series trend (years) | Line chart | `ax.plot(years, vals, 'o-', lw=2.5, ms=8)` |
| Position + market share | Bubble chart | `ax.scatter(tech, comm, s=share)` with tier colors |
| Multi-entity capability | Polar radar | `subplot_kw=dict(polar=True)` + `ax.fill(angles, vals, alpha=0.08)` + `ax.plot(angles, vals, 'o-')` |
| Process flow | Annotated flowchart | `ax.text(..., bbox=...)` + `FancyBboxPatch` + `ax.annotate(arrowprops=...)` |

**Flowchart box helpers:**
```python
def box(ax, cx, cy, w, h, text, color, text_color='white', fs=10, bold=False):
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            color=text_color, fontweight='bold' if bold else 'normal',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=color, edgecolor='none'), zorder=3)

def sub_box(ax, cx, cy, w, h, text, border_color, bg='white', fs=8.5):
    p = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle='round,pad=0.08', facecolor=bg,
                       edgecolor=border_color, linewidth=1.3, zorder=2)
    ax.add_patch(p); ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, color='#1F2937', zorder=3)
```

**Flowchart rules:**
- Same-level boxes → identical w/h (even if one has line-wrapping text, give it the same height as others by adjusting font or adding padding)
- Sub-items on same Y → horizontal alignment (all starting at the same y-coordinate)
- Arrows → clean connection from box bottom center to next box top center, no gap
- Summary/conclusion section → different color (blue) + dashed connector arrows
- Verify with `browser_vision` after generation — check: alignment, contrast (no light-on-light sub-item boxes), no text overflow, consistent box dimensions at each tier

**Replace** `![图X](fig/figX_desc.svg)` in markdown. **Update** `"待补充"` → actual `fig/*.svg` paths. **Clean up** — delete generation scripts.

### Verification After Chart Swap

After replacing all ASCII charts with SVGs:
1. Run `grep -c '```' report.md` → should be 0 (no remaining code-block ASCII)
2. Run `grep -c '待补充' report.md` → should be 0
3. Check `ls fig/` has SVG for every referenced figure
4. Open the most complex SVG in browser + `browser_vision` to verify rendering

### Data Citation Cross-Check

Before finalizing, verify:
- Every percentage/number in bold claims has its cited source actually supporting it. A common error: citing Company A's data when describing Company B's metrics.
- When multiple companies produce the same class of product, each has a separate source annotation — don't collapse multiple companies under one company's source.
- If you only have data for one player but describe a market pattern involving multiple, either find sources for the others or narrow the claim.

### Acronym Definition Rule

Every acronym used in the report must have its Chinese (and English) full name on first occurrence:
- Format: `CSP（云服务提供商，Cloud Service Provider）`
- Includes: AIDC, CSP, ODM/OEM, PFAS, CDU, PUE, TDP, TCO, MGX, NVQD, UQD, etc.
- Do this even for "obvious" acronyms — a Chinese sell-side report may be read by generalist investors.

### Final Polish Pass (Chinese Typography)

Before the final delivery, run a polish pass on the entire report file:

1. **Quotation marks** — Replace all straight ASCII double quotes `"text"` with curved Chinese quotation marks `"text"` (U+201C / U+201D). Use Python: `text = re.sub(r'"([^"]*[\u4e00-\u9fff][^"]*)"', lambda m: '\u201c' + m.group(1) + '\u201d', text)`.
2. **Chinese-Western spacing** — Add spaces between Chinese characters and adjacent Latin letters/digits:
   - `re.sub(r'([\u4e00-\u9fff])([A-Za-z])', r'\1 \2', text)` (Chinese + letter)
   - `re.sub(r'([A-Za-z])([\u4e00-\u9fff])', r'\1 \2', text)` (letter + Chinese)
   - `re.sub(r'([\u4e00-\u9fff])(\d)', r'\1 \2', text)` (Chinese + digit)
   - `re.sub(r'(\d)([\u4e00-\u9fff])', r'\1 \2', text)` (digit + Chinese)
3. **Clean punctuation** — Remove spaces before Chinese punctuation: `re.sub(r' ([，。；：、」》）])', r'\1', text)`
4. **Remove AI-isms** — Run a targeted replacement pass:
   - "我们认为，" → "" (remove when used as paragraph filler; keep only for original forecasts)
   - Reduce "核心" overuse → "关键" for some instances
   - "在...背景下" → direct statement without framing
   - "随着..." → present tense without temporal framing
   - "历史性的" / "需要清醒认识到" / "至关重要" → simpler alternatives
   - "根据我们的推演" → reduce to "当...后"
   - "供给收缩为...创造了...窗口" → "供给收缩给...打开了...窗口"
   - Formulaic conclusion padding → trim to actual forecast
   - "值得注意的是" → remove entirely (empty filler)
   - **Second pass required** — Some "我们认为" may survive the first pass. Run a grep for '我们认为' after the first pass and remove any remaining. Zero tolerance.
5. **Relative paths** — All file path references in the report must be relative (e.g. `fig/fig1_chart.svg`, not `/Users/.../fig/fig1_chart.svg`).
6. **Double space cleanup** — Run `re.sub(r'  +', ' ', text)` to remove any double spaces introduced by the spacing pass.
7. **Verify after pass** — Run checks:
   ```bash
   python3 -c "
   t=open('report.md').read()
   print('Straight quotes:', t.count(chr(0x22)))
   print('We think:', t.count('我们认为'))
   print('Absolute paths:', '/Users/' in t)
   print('Dai bu chong:', t.count('待补充'))
   print('Extra blanks:', '\\n\\n\\n' in t)
   "
   ```
   All must be 0. If any >0, do a second targeted pass.
8. **Redundant whitespace** — Remove runs of 3+ blank lines: `re.sub(r'\n{3,}', '\n\n', text)`

### File Name Check

Before creating any deliverable file, verify the filename for:
- Spelling errors (e.g., `compitition` → `competition`)
- Encoding issues with Chinese characters
- Path consistency with naming conventions (`docs/jul-NN-topic/`)

### Verification After Chart Swap

After replacing all ASCII charts with SVGs, run the following checks before considering the deliverable complete:

1. `grep -c '```' report.md` → result should be **0** (no remaining code-block ASCII art)
2. `grep -c '待补充' report.md` → result should be **0** (no placeholder paths)
3. Check `ls fig/` has an SVG for every figure referenced in the report
4. Open the most visually complex SVG (flowchart or radar chart) in a browser + `browser_vision` to verify rendering
5. Run the typography verification:
   ```python
   t = open('report.md').read()
   assert t.count(chr(0x22)) == 0, f'{t.count(chr(0x22))} straight quotes remain'
   assert '我们认为' not in t, '我们认为 still present'
   assert '/Users/' not in t, 'absolute paths still present'
   assert '  ' not in t, 'double spaces present'
   ```

### Chart Generation Step (券商研报模式专用)

ASCII charts are for drafts only. For final delivery, generate real SVG charts via matplotlib.

**Matplotlib setup:**
```python
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang SC',
                                     'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150; plt.rcParams['savefig.dpi'] = 150
```

**Palette** (use same across all charts in one report):
```python
PALETTE = {
    'blue': '#2E86AB', 'purple': '#A23B72', 'orange': '#F18F01',
    'red': '#C73E1D', 'green': '#6A994E', 'vibrant_blue': '#2563EB',
    'gray': '#6B7280', 'bg': '#F8FAFC',
}
```

**Type-to-chart mapping:**

| Data shape | Chart type | Matplotlib pattern |
|-----------|-----------|-------------------|
| 1D value comparison | Horizontal bar | `ax.barh(cats, vals, color=palette_colors)` |
| Value + margin | Dual-axis combo | `ax1.bar(...)` + `ax2.plot(..., twinx())` for range lines |
| Difficulty/urgency 2D | Scatter + quadrant | `ax.scatter(x, y, s=size)` + quadrant lines at axis midpoints |
| Timeline | Gantt horizontal bars | `ax.barh(pos, dur, left=start, height=0.5)` |
| Multi-series trend (years) | Line chart | `ax.plot(years, vals, 'o-', lw=2.5, ms=8)` |
| Position + market share | Bubble chart | `ax.scatter(tech, comm, s=share)` with tier colors |
| Multi-entity capability | Polar radar | `subplot_kw=dict(polar=True)` + `ax.fill(angles, vals, alpha=0.08)` + `ax.plot(angles, vals, 'o-')` |
| Process flow | Annotated flowchart | `ax.text(..., bbox=...)` + `FancyBboxPatch` + `ax.annotate(arrowprops=...)` |

**Flowchart box helpers:**
```python
def box(ax, cx, cy, w, h, text, color, text_color='white', fs=10, bold=False):
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            color=text_color, fontweight='bold' if bold else 'normal',
            bbox=dict(boxstyle='round,pad=0.15', facecolor=color, edgecolor='none'), zorder=3)

def sub_box(ax, cx, cy, w, h, text, border_color, bg='white', fs=8.5):
    p = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle='round,pad=0.08', facecolor=bg,
                       edgecolor=border_color, linewidth=1.3, zorder=2)
    ax.add_patch(p); ax.text(cx, cy, text, ha='center', va='center',
                             fontsize=fs, color='#1F2937', zorder=3)
```

**Flowchart rules:**
- Same-level boxes → identical w/h (even if one has line-wrapping text, give it the same height as others by adjusting font or adding padding)
- Sub-items on same Y → horizontal alignment (all starting at the same y-coordinate)
- Arrows → clean connection from box bottom center to next box top center, no gap
- Summary/conclusion section → different color (blue) + dashed connector arrows
- Verify with `browser_vision` after generation — check alignment, contrast (no light-on-light sub-item boxes), text overflow, consistent box dimensions at each tier

### Data Citation Cross-Check

Before finalizing, verify:
- Every percentage/number has a source that actually supports it. A common P0 error: citing Company A's data when describing Company B's metrics.
- When multiple companies produce the same class of product, each has a separate source annotation.
- If you only have data for one player but describe a market pattern involving multiple, either find sources for the others or narrow the claim.

### Acronym Definition Rule

Every acronym used in the report must have Chinese (and English) full name on first occurrence:
- Format: `CSP（云服务提供商，Cloud Service Provider）`
- Includes: AIDC, CSP, ODM/OEM, PFAS, CDU, PUE, TDP, TCO, MGX, NVQD, UQD, etc.
- Do this even for "obvious" acronyms — a Chinese sell-side report may be read by generalist investors.

### Typography Polish Pass

Before the final delivery, run a dedicated polish pass on the entire report file:

1. **Quotation marks** — Replace all straight ASCII `"..."` with curved `"..."` (U+201C/U+201D):
   ```python
   text = re.sub(r'"([^"]*[\u4e00-\u9fff][^"]*)"', lambda m: '\u201c' + m.group(1) + '\u201d', text)
   ```

2. **Chinese-Western spacing** — Insert spaces between:
   - CJK char + Latin letter: `re.sub(r'([\u4e00-\u9fff])([A-Za-z])', r'\1 \2', text)`
   - Latin letter + CJK char: `re.sub(r'([A-Za-z])([\u4e00-\u9fff])', r'\1 \2', text)`
   - CJK char + digit: `re.sub(r'([\u4e00-\u9fff])(\d)', r'\1 \2', text)`
   - Digit + CJK char: `re.sub(r'(\d)([\u4e00-\u9fff])', r'\1 \2', text)`

3. **Clean punctuation** — Remove spaces before Chinese punctuation: `re.sub(r' ([，。；：、」》）])', r'\1', text)`

4. **Remove AI-isms** — Run targeted replacements:
   - `"我们认为，"` → `""` (zero tolerance — run TWO grep passes)
   - Reduce `"核心"` overuse → replace some with `"关键"`
   - `"在...背景下"` → direct statement
   - `"随着..."` → present tense
   - `"历史性的"` / `"需要清醒认识到"` / `"至关重要"` → simpler alternatives
   - `"值得注意的是"` → remove entirely
   - Formulaic conclusion padding → trim to actual forecast

5. **Relative paths** — All file path references must be relative (`fig/fig1.svg`, not `/Users/.../`)

6. **Double space cleanup** — `re.sub(r'  +', ' ', text)`

7. **Final verify** (must all be 0):
   ```bash
   python3 -c "
   t=open('report.md').read()
   print('Straight quotes:', t.count(chr(0x22)))
   print('We think:', t.count('我们认为'))
   print('Absolute paths:', '/Users/' in t)
   print('Dai bu chong:', t.count('待补充'))
   print('Extra blank lines:', '\\n\\n\\n' in t)
   "
   ```

### File Name Check

Before creating any deliverable file, verify the filename for:
- Spelling errors (e.g., `compitition` → `competition`)
- Encoding issues with Chinese characters
- Path consistency with naming conventions (`docs/jul-NN-topic/`)

### Pitfalls (Sell-Side Mode Only)
- **Don't let data overwhelm analysis** — Numbers are evidence, not the argument. Always explain *why* a number matters.
- **Don't use placeholder figures** — Inline the actual chart/table, or don't reference it.
- **Don't use Mermaid for simple bar charts** — ASCII `█████` is more compact in drafts.
- **Don't forget source paths** — Every chart/table needs a source line AND a file path note at section end.
- **Don't write long text walls** — >300 words without visual break → restructure.
- **Don't leave ASCII charts in final delivery** — Replace with real SVG charts via matplotlib.
- **Don't leave "待补充" path notes** — After generating real charts, update all file path notes.
- **Don't let data citations go unchecked** — Wrong source attribution (e.g. 毛利率70% attributed to wrong company) is a P0 error.
- **Don't skip subagent review** — A stronger model catching issues before delivery prevents multiple errors.
- **Don't forget typography cleanup** — Chinese text needs: curved quotes, CN-EN spacing, no leftover AI-isms. This is a separate pass, not part of the writing pass.
- **Don't leave residual "我们认为"** — One pass removing it from the text is not enough; a second pass may be needed for instances that survived the first.
- **Don't skip verify-after-passes** — After the Polish Pass and Chart Swap, run a Python count check for 0 straight quotes, 0 "待补充", 0 "我们认为", 0 absolute paths. These are P0-quality gates.
- **Don't let flowchart boxes have uneven heights** — All boxes at the same tier must have identical height/width. Sub-items on the same Y must be horizontally aligned. Verify with browser_vision after generation.
- **Don't produce redundant/duplicate charts** — Before generating a chart, check: does this show the same data as another chart already in the report? If two charts cover the same topic (e.g., fig5 国产化时间轴 and fig10 国产化路径 are nearly identical), consolidate or differentiate them (different data dimension, different time granularity, different visualization style). Redundant charts waste space and confuse readers.

## Reference Files

- `references/json-extraction-patterns.md` — workflow for multi-document analysis from a JSON of pre-extracted PDF texts.
- `references/sell-side-report-patterns.md` — multi-document extraction, parallel subagent analysis, and report structure rules for sell-side research reports.

## Pitfalls

- Don't write AI-sounding filler in the intro/outro. Just deliver the content.
- Don't invent algorithm behavior that contradicts the source document. Re-read the source if unsure.
- Don't separate Nasdaq/NYSE when they're the same — merge into one explanation.
- Don't use fake broker labels (Broker A, Broker B) without explaining what they represent.
- Don't remove edge case sections — the task explicitly requires them.
- Parameter tables: user may prefer dot lists over markdown tables. Follow what they ask.
