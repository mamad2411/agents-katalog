---
name: consulting-html-report
description: Create polished consulting-style single-file HTML research reports from messy business notes, screenshots, metrics, and iterative user feedback. Use this skill whenever the user asks for a 咨询风/艾瑞咨询风/研究报告/汇报报告/HTML报告, wants business or AI landing-practice material turned into a management-facing report, asks to add charts/diagrams, or asks to update report metrics and keep the whole HTML report consistent.
---

# Consulting HTML Report

Use this skill to turn scattered business materials into a management-facing consulting-style HTML research report. The target output is a standalone `HTML` file that can be opened locally, printed to PDF, and iterated based on screenshots or metric corrections.

## What This Skill Produces

Create a final deliverable under `09_生成输出/` by default:

```text
09_生成输出/[report-topic]-[YYYYMMDD].html
outputs/[report-topic-render-YYYYMMDD]/
├── desktop.png
└── mobile.png
```

Use a single self-contained HTML file with embedded CSS. Avoid external CDNs so the report works offline.

## Inputs To Extract

Read the user's text, screenshots, pasted tables, and follow-up corrections. Extract:

- Report title, audience, date, and scope.
- Business practices, projects, products, tools, or departments.
- For each practice: positioning, target users, current progress, value, challenges.
- Metrics: totals, ratios, ranges, cycle time, quality, usage, document count, adoption.
- Screenshot data: table rows, labels, visible numbers, chart meanings.
- User corrections: the latest user instruction wins over older metrics.

Ask only for blocking gaps. If the user provides enough material, proceed with reasonable assumptions and make those assumptions visible in the report notes.

## Report Structure

Use this structure unless the user asks for another:

1. **Cover / Hero**
   - Report title, subtitle, date, research object, and core judgment.
   - 3-6 KPI cards with the strongest metrics.

2. **Core Findings**
   - 3-5 concise findings.
   - Each finding should connect fact, implication, and management meaning.

3. **Practice Landscape**
   - Matrix/table of initiatives.
   - Columns: name, positioning, target user, value, challenge.

4. **Key Initiative Deep Dive**
   - Quantified outcomes.
   - Delivery cycle or impact chart.
   - Flow/process comparison when the initiative changes workflow.

5. **Data / Knowledge Structure**
   - Use bar charts, tables, or composition cards.
   - Calculate totals and shares when visible data allows.

6. **Maturity / Diagnosis**
   - Scorecard, matrix, or staged maturity map.
   - Diagnose what is working and what is still increasing cost.

7. **Roadmap / Actions**
   - Next-stage priorities.
   - 3-4 phase roadmap.
   - KPI system for ongoing operation.

8. **Footer**
   - Source note, limitations, and print/PDF guidance.

## Consulting-Style Writing

Write like an internal research report, not a marketing page.

- Use the chain: facts -> interpretation -> issue -> recommendation -> metric.
- Keep claims grounded in supplied data. If a conclusion is inferred, label it as a research judgment.
- Use exact numbers and dates from the user.
- When a user changes a metric, update all related text so old and new report口径 do not conflict.
- Do not claim the report is issued by a third-party consulting firm. You may use "consulting report style" as a visual and analytical style.

## Visual Design Rules

Use restrained consulting-report visuals:

- Color: blue / white / gray base, red for strategic emphasis, green for efficiency/positive effects, orange for increased scope/cost.
- Layout: dense but readable; management-facing, not a landing page.
- Components: KPI cards, structured tables, horizontal bar charts, maturity matrix, process swimlanes, impact charts, roadmap cards.
- Avoid pure text blocks in key analytical sections. If a section explains a process, create a diagram.
- On mobile, stack cards and diagrams into one column with no page-level horizontal overflow.
- Keep report HTML print-friendly. Include `@media print` rules when practical.

## Diagram Patterns

When the user asks for "图表", "示意图", "流程对比", or points at a text-heavy section:

- **Process swimlane**: compare traditional flow vs new/AI flow.
- **Cost transfer map**: show cost shifting from later rework to earlier governance/preparation.
- **Impact bar chart**: show positive efficiency on one side and increased cost/scope on the other.
- **Matrix**: map business value vs maturity/readiness.
- **Roadmap**: show phases or quarters.

For AI or process-change reports, explicitly mark:

- Efficiency gains: demand expression, confirmation, execution, reuse, acceptance, rework control.
- Increased time/scope: research breadth, data preparation, fact-checking, prototype calibration, knowledge/skill governance.

## Iteration Rules

Users often review the HTML in a browser and give screenshot-based corrections. Treat those as precise edit requests.

1. Locate the exact section or visible text with `rg`.
2. Change only the necessary region unless the metric affects the whole report.
3. If a metric changes, search for old values and wording across the file.
4. Update related findings, cards, captions, and chart labels for consistency.
5. Re-run render validation before saying the update is complete.

Examples:

- If the user changes `完整闭环率 20.3%` to `整体提效 40%-63%` and `交付质量 99%`, replace the KPI cards and remove old closure-rate wording from findings.
- If the user says a section needs charts, replace or supplement the text cards with diagram components, not just more bullets.
- If the user changes the top brand/title, update the exact header location without renaming unrelated files unless requested.

## File Workflow

1. Inspect current workspace conventions and existing output paths.
2. If creating a new report, copy or adapt `assets/report-template.html` only as a starting point. Customize content and charts for the user's topic.
3. If editing an existing report, preserve the file unless the user asks for a new version.
4. Use descriptive Chinese filenames with date when helpful.
5. Put final report files in `09_生成输出/` by default. Put render screenshots in `outputs/`.

## Verification

Before reporting completion, verify current state.

Use `scripts/render_check.cjs` when Node and Playwright are available:

```bash
node scripts/render_check.cjs \
  --html /absolute/path/to/report.html \
  --out-dir /absolute/path/to/render-output \
  --must-contain "关键标题" \
  --must-contain "关键指标"
```

If bundled Playwright browsers are missing, use system Chrome by passing:

```bash
node scripts/render_check.cjs --chrome "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ...
```

Minimum checks:

- Required text appears.
- Old conflicting metrics do not appear when replaced.
- Desktop and mobile screenshots are generated.
- No console errors.
- No full-page horizontal overflow on desktop or mobile.

If browser validation is unavailable, run static checks with `rg` and clearly state that browser rendering was not verified.

## Useful Assets

- `assets/report-template.html`: offline consulting-report HTML starter with KPI cards, sections, tables, charts, and print/mobile CSS.
- `scripts/render_check.cjs`: reusable render validation and screenshot script.
- `evals/evals.json`: initial test prompts for future skill evaluation.
