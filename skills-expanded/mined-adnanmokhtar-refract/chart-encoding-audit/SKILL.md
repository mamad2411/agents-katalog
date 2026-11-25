---
name: chart-encoding-audit
description: "Chart honesty detector per chart library: wrong mark, truncated baseline, radius-scaled size, dual axes, gaps drawn as data, colour-only or unsafe series, missing units — proved on the rendered chart."
kind: skill
pack: ui-ux
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: chart-encoding-audit

## Premise

A re-themed chart passes every other gate in this pack and can still mislead the person reading it. A bar chart whose axis starts at 50 triples a 10 % difference. A line that bridges a missing week invents a reading nobody took. Red and green series are one series to a reader with red–green colour-vision deficiency. This skill walks the project's chart surface, library by library, and asks the question re-theming never asks: is this drawing true.

Find real encoding defects, no hand-waves. **Every finding cites the chart config's `<file:line>` (the component, the options object, the spec or the data transform) + the route that renders it + the question the chart answers + what a reader would conclude wrongly + the proof + the fix.** "The chart is confusing" is the symptom that prompted the audit, not a finding. A grep hit is never a finding by itself, and "no chart issues" is never printed without the class-coverage block (§ Output).

**This skill does NOT own the rules.** Mark selection, the three scale families and the honesty rules come from [`data-visualization.md`](../../ai-patterns/data-visualization.md). This skill detects and cites; a threshold here that disagrees with that file is drift, and that file wins.

**It also does not own the paint.** Whether a chart matches the design language is `ui-design-sweep § normalize-surface` and the `tokens` axis. A chart can be perfectly on-brand and fail every check below; that is the whole reason this audit exists separately.

Below, `ui § n` means [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § n; a bare `§n` is a detector in this skill.

## The rule

A candidate is a finding when all four hold:

1. **The chart renders** on a route a user reaches, with real data shapes (not only a story or a demo page).
2. **The question is stated.** The finding names the question the surrounding surface asks. Without it, mark selection is taste and the finding will be argued rather than fixed.
3. **The encoding contradicts the rule** in `data-visualization.md` for that question, and no stated exception applies (a line axis zoomed *and labelled*, an ordinal axis keeping its order).
4. **The proof holds.** A config fact (`beginAtZero: false` on a bar chart) is a static fact with the two-ended trace. A colour-safety verdict is always **computed**. A rendered claim (the gap is bridged, the radius scales linearly) is shown on the rendered chart (§ Proof).

## Boundaries

- **The chart's accessibility** — a text alternative (1.1.1), keyboard access to data points, an accessible data table — is `a11y-code-scan` and `a11y-scan` (frontend pack, when installed). Without it, the row prints `N/A (owner pack frontend not installed)` and is listed for the human pass.
- **Series contrast against the plot background** (≥ 3:1, WCAG 2.2 SC 1.4.11) is computed here because the encoding needs it; when the frontend pack is installed the SC finding is credited to `a11y-scan` §3 and this row corroborates (dedupe by `<file:line>`).
- **Whether colours come from the system** (a hex in a chart config where a token exists) is `design-token-audit` §1. Whether a **data ramp** exists separately from the UI accent ramp is this skill's §6.
- **Re-theming** ("the chart does not match the new palette") routes to `ui-design-sweep` § `normalize-surface`. Filing it here counts it twice and gets it fixed by nobody.
- **A missing period control or a composite-surface gap** on a dashboard is `ui-design-sweep` § `normalize-surface`, not an encoding defect.

## Adapt to the codebase — lane table

Read each chart library **and its version** from the lockfile and print the lanes you ran in the output header. Hand-rolled SVG and `<canvas>` charts count: they are where the worst offenders hide, because no library default protected them.

| Lane | Truncated baseline (§2) | Size channel (§3) | Two value axes (§4) | Gaps (§5) |
|---|---|---|---|---|
| **Recharts** | `<YAxis domain={[n, …]}>` with n ≠ 0, `'dataMin'` | `<ZAxis range>` on a scatter | two `yAxisId` | `connectNulls` |
| **Chart.js** (react-chartjs-2, vue-chartjs, ng2-charts) | `beginAtZero: false`, `min:` | `type: 'bubble'`, data `r` | a second scale (`y1`), `position: 'right'` | `spanGaps` |
| **ECharts** (echarts-for-react, vue-echarts, ngx-echarts) | `min:`, value axis `scale: true` | `symbolSize` mapping a value | `yAxis: [ {…}, {…} ]` | `connectNulls: true` |
| **ApexCharts · Highcharts · AG Charts · MUI X · Tremor** | `min:` on the value axis | bubble series sizing | an array of y-axes, `opposite: true` | gap / connect options |
| **Nivo · Visx · Victory · d3 (hand-rolled)** | `minValue`, a `domain` not from 0 | a linear scale feeding `r` (not `scaleSqrt`) | a second `axisRight` scale | `defined()` absent; `?? 0` in the transform |
| **Vega / Vega-Lite · Observable Plot** | `"zero": false`, a `domain` | `size` encoding | `"resolve": {"scale": {"y": "independent"}}` | — |
| **Mobile** (victory-native, react-native-gifted-charts, react-native-chart-kit, `fl_chart`, Swift Charts, Vico, MPAndroidChart) | `minY`, `.chartYScale(domain:)`, `axisMinimum` | per library | per library | per library |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Chart greps run **only over the chart files grep 0b lists**: across a whole app, `<Tooltip>`, `<Cell>`, `domain=` and `min:` collide with dialog tooltips, table cells and form props. Every `rg` names its path; any rg error (exit 2) is a failed grep, never zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|lit|react-native)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
{ [ -f pubspec.yaml ] || [ -d ios ] || [ -d android ]; } && ROOTS+=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static,generated,__generated__,Pods,DerivedData}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress,scripts,tools}/**' -g '!**/*.{test,spec,stories,story,e2e,cy,mock}.*' -g '!**/*.{test-data,fixture,fixtures}.*'
   -g '!*.{md,mdx,snap,map,lock}' -g '!**/{locales,locale,i18n,translations,docs,vendor}/**' -g '!/ai/**' -g '!**/*.min.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--)')
LIB='recharts|chart\.js(?:/auto)?|react-chartjs-2|vue-chartjs|ng2-charts|echarts(?:-for-react)?|vue-echarts|ngx-echarts|(?:react-|vue3-|ng-)?apexcharts|@nivo/[\w-]+|@visx/[\w-]+|victory(?:-native)?|highcharts(?:-react-official)?|vega(?:-lite|-embed)?|react-vega|@observablehq/plot|d3(?:-[\w-]+)?|@tremor/react|@mui/x-charts[\w/-]*|ag-charts-[\w-]+|uplot|plotly\.js[\w-]*|react-plotly\.js|layerchart|@unovis/[\w-]+|lightweight-charts|react-native-gifted-charts|react-native-chart-kit'
CFL="${TMPDIR:-/tmp}/chart-files.txt"
# 0a libraries and versions. 0b chart files: library imports, lazy imports, hand-rolled chart files by path (read: a
#    "chart of accounts" screen matches by name). 0c a data ramp in the token layer (§6 asks whether one exists).
rg -n --no-heading --pcre2 '"(?:'"$LIB"')"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"; rg -n --pcre2 '^\s*(?:fl_chart|syncfusion_flutter_charts|graphic)\s*:' -g 'pubspec.yaml' "${ROOTS[@]}"
{ rg -l --pcre2 'from\s+["\x27](?:'"$LIB"')["\x27/]|require\(["\x27](?:'"$LIB"')["\x27]|package:(?:fl_chart|syncfusion_flutter_charts)/|^import\s+Charts\b|com\.patrykandpatrick\.vico|com\.github\.mikephil\.charting|"\$schema"\s*:\s*"https://vega\.github\.io' -g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,dart,swift,kt,json}' "${X[@]}" "${ROOTS[@]}"
  rg -l --pcre2 'import\(\s*["\x27](?:'"$LIB"')["\x27]' -g '*.{js,jsx,ts,tsx,vue,svelte}' "${X[@]}" "${ROOTS[@]}"
  rg --files -g '*.{jsx,tsx,vue,svelte,astro}' "${X[@]}" "${ROOTS[@]}" | rg -i --pcre2 '(?:^|/)(?:charts?|viz|graphs?)/|(?:chart|graph|sparkline|donut|gauge|histogram)[\w.-]*\.(?:tsx|jsx|vue|svelte|astro)$'; } | sort -u > "$CFL"; cat "$CFL"
CF() { tr '\n' '\0' < "$CFL" | xargs -0 -r rg -n --pcre2 "$@" | "${NC[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*import\b'; }
rg -n --pcre2 -e '--(?:chart|data|viz|series)-[\w-]*\s*:' -g '*.{css,scss,ts,js,json}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 1. Marks to check against the question: pie, donut, radar, funnel, gauge, 3-D (read each with its surface).
CF '<(?:Pie|PieChart|RadarChart|Radar|RadialBarChart|Funnel|Treemap)\b|\btype\s*:\s*["\x27](?:pie|doughnut|polarArea|radar|funnel|gauge|bar3D|scatter3D)["\x27]|\b(?:ResponsivePie|VictoryPie|PieChart|DonutChart)\b|\boptions3d\b|\bPieChartData\b|\bSectorMark\b'
# 2. A value axis that does not start at zero.
CF '\bbeginAtZero\s*:\s*false|\b(?:min|suggestedMin|minY|minValue|yMin)\s*[:=]\s*\{?\s*(?!0\b)-?(?:\d|[\x27"]?data[Mm]in)|\bdomain\s*=\s*\{\s*\[\s*(?!0\s*,)[^,\]]+,|\bscale\s*:\s*true\b|\bzero\s*:\s*false|"zero"\s*:\s*false|\.chartYScale\(\s*domain\s*:|\baxisMinimum\b|\bincludeZero\s*:\s*false'
# 3. A size channel (read: is the value mapped to radius, or to area?).
CF '<ZAxis\b|\btype\s*:\s*["\x27]bubble["\x27]|\bsymbolSize\s*:|\.attr\(\s*["\x27]r["\x27]|\br\s*[:=]\s*\{?\s*(?:\w+\.)?(?:value|count|size|amount|total)\b|scaleLinear\(\)[^;\n]*\.range\(\[\s*\d+\s*,\s*\d+\s*\]\)|\bBubbleChart\b|\bScatterChart\b'
# 4. Two value axes.
CF '\byAxisId\s*=\s*\{?["\x27]?(?!left\b|0\b)\w+|\by1\s*:\s*\{|\bposition\s*:\s*["\x27]right["\x27]|\b[yY][aA]xis\s*:\s*\[\s*\{[^\]]*\}\s*,\s*\{|"resolve"\s*:\s*\{\s*"scale"\s*:\s*\{\s*"y"\s*:\s*"independent"|\bopposite\s*:\s*true|\brightAxis\b|\baxisRight\b'
# 5. Missing data drawn as data: gap bridging, and nulls coerced to zero in the transform. 5b: the model and view-model
#    files that feed the charts (the chart file's feature, two directories up, past components/pages/views): a division
#    whose empty-denominator branch is 0 (`d > 0 ? n / d : 0`, `n / d || 0`). Read whether the value reaches a series.
CF '\bconnectNulls\b(?!\s*=\s*\{\s*false)|\bspanGaps\s*:\s*(?:true|\d)|\bconnectNulls\s*:\s*true|\?\?\s*0\b|\|\|\s*0\b|\bfillna\(0\)|Number\([^)]*\)\s*\|\|\s*0'
grep -v -E '/shared/|/ui/|/design-system/' "$CFL" | while IFS= read -r f; do d=$(dirname "$(dirname "$f")"); case "$d" in */components|*/pages|*/views) d=$(dirname "$d") ;; esac; echo "$d"; done | sort -u | tr '\n' '\0' | xargs -0 -r rg -n --pcre2 '\?\s*[^:;?\n]*\w\s*/\s*[\w(][^:;?\n]*:\s*0\b(?![.\w])|/\s*[\w.]+\s*\)?\s*(?:\|\||\?\?)\s*0\b(?![.\w])' -g '*.{ts,js,mjs}' -g '!*.d.ts' "${X[@]}" | "${NC[@]}"
# 6. Series colour chosen at the call site: literal hexes, palette arrays, a hex picked per point by a ternary (also
#    inside a `.map` callback: up/down, hit/miss), semantic red/green on series.
CF '(?:fill|stroke|color|colors|backgroundColor|borderColor)\s*[:=]\s*\{?\s*\[?\s*["\x27]#[0-9a-fA-F]{3,8}["\x27]|\?\s*["\x27]#[0-9a-fA-F]{3,8}["\x27]\s*:\s*["\x27]#[0-9a-fA-F]{3,8}["\x27]|\b(?:COLORS|PALETTE|SERIES_COLORS|CHART_COLORS)\w*\s*[:=]|\bcolors\s*:\s*\[|\b(?:red|green|success|danger|destructive)\b[^\n]*\b(?:fill|stroke|color)\b'
# 7. Chart files with no unit, value label or tick formatter anywhere (read: axis titles, legend order, hover-only values).
tr '\n' '\0' < "$CFL" | xargs -0 -r rg --files-without-match --pcre2 '\btickFormatter\b|\bvalueFormatter\b|\bformat\w*\s*=|\bunit\s*=|\blabel\s*=\s*\{|\baxisLabel\b|\btitle\s*:\s*\{|\bformatter\s*[:=]|<LabelList\b|\bdataLabels\b|\bticks\s*:\s*\{[^}]*callback'
# 8. Sort and aspect (read): declared plot shapes to compare across comparable charts.
CF '<ResponsiveContainer\b[^>]*\b(?:aspect|height)\s*=|\baspectRatio\s*:|\bmaintainAspectRatio\s*:'
```

**Measured** (2026-10-05). On a seeded pos/neg set (Recharts, Chart.js, ECharts), every positive is caught: a `domain={[50,'auto']}` bar axis, `beginAtZero: false`, ECharts `scale: true`, two `yAxisId`, a second Chart.js scale, an ECharts `yAxis` array, `connectNulls`, `spanGaps: true`, `?? 0` in a transform, a hex palette array, a `<ZAxis range>`. The decoy file (`domain={[0,'auto']}`, `fill="var(--chart-1)"`, `connectNulls={false}`, a `tickFormatter`) returns nothing. The 12 `benchmarks/fixtures` trees have no chart library. On a read-only real React 19 + Recharts 2.15.4 application:
- 0b: 17 chart files — 9 Recharts imports, a lazy loader and the hand-rolled primitives under `shared/ui/charts`. One is a "chart of accounts" screen matched by name only.
- 0c: a full data ramp. `--series-1…6` per theme carries the series; a `--chart-1…5` set is left over beside it (`design-token-audit` §9 finds it unreferenced).
- 1: 1 (a donut).
- 2, 3, 4, 6: 0.
- 5: 3, all refuted on read. An earlier version of this line called `row[w.name] = d.values[w.id] ?? 0` a real candidate; read in full (2026-10-15) it sums hourly quantities into a stacked bar, where an hour with no movement is a true zero (§ 97). Another is an emptiness check and the third an accumulator.

**Re-measured 2026-10-15** on the same app inside a real NestJS + React monorepo. Grep 5b reads the 14 division-to-zero lines in the model files next to the chart files; one is the defect grep 5 could not see: a `pct(n, d)` helper returns 0 when nothing has shipped yet, and the daily delivery- and rejection-rate lines plot it as 0 % on the most recent days (high, § 103). Grep 7 fell from 10 files to 7 once `formatValue=` and other `format…=` props count as a value label (the shared donut and ranked-list callers carry them); a caller of the money mini-trend that shows no currency is still among the 7. The fixtures return 0 for 5b.
- 7: 7 files with no unit or formatter; the shared chrome formats values for some of them, so read each.

## The 3,000-hit path

1. **Intersect** with the route table: a chart only a demo or design-system gallery renders is one group, dismissed by one read.
2. **Group** by the shared chart primitive or options builder. A truncated axis in a shared `ChartChrome` is one finding with N charts.
3. **Rank** by consequence: charts users act on (finance, inventory, SLA, alerting) first, then reporting, then marketing pages.
4. **Read the top 30 groups fully**, with each chart's question written down.
5. **Prefer the rendered bulk check at scale:** one Playwright pass per chart route reads every SVG chart's lowest tick, bar heights against values and series colours (§ Proof); one CVD-emulated screenshot per chart route covers §6 in bulk.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

| § | Class | `data-visualization.md` § | Default |
|---|---|---|---|
| 1 | Mark does not answer the question (or answers two) | The chart-selection map | medium; the strongest finding of a run when no question can be stated |
| 2 | Bar, column or area value axis not at zero; a zoomed line axis not labelled | Encoding honesty | **high** (bars) · medium (unlabelled line zoom) |
| 3 | Size encodes radius, not area | Encoding honesty | **high** |
| 4 | Two value axes with independent domains | Encoding honesty | **high** — it manufactures a correlation |
| 5 | Missing data drawn as data (gaps bridged, nulls coerced to zero) | Encoding honesty | **high** — it invents readings |
| 6 | Data colour: no data ramp, wrong family, over the categorical ceiling, colour as the only channel, semantic collision, series below 3:1, a ramp that inverts in dark | Data colour is not UI colour | high when series cannot be told apart under CVD emulation; medium otherwise |
| 7 | Units, labels and legend: no unit or period, legend order ≠ series order, a value reachable only on hover | Labeling | medium; low for a legend where direct labels fit |
| 8 | Order and aspect: categories not sorted where rank is the question; differing aspect across comparable charts | Encoding honesty | medium (sort) · low (aspect) |

### 1. Mark does not answer the question

For each chart, write the question the surrounding surface asks, then check the mark against `data-visualization.md` § The chart-selection map. **Read the code:** what does the page around it ask (a share of a whole, a trend, a comparison, a distribution)? Does the chart answer two questions at once? **Finding when** the mark contradicts its row: cite the row and the mark it prescribes. A chart whose question cannot be stated from the surface is the strongest finding of the run: nobody knows what it is for. **Proof:** the stated question, the map row and the mark; this is a judgement row, so without a stakeholder or spec naming the question it stays `[report-flagged]`.

### 2. Value axis not at zero

```
BAD:   <BarChart><YAxis domain={[50, 'auto']} /></BarChart>   ·   scales: { y: { beginAtZero: false } } on type 'bar'
GOOD:  a bar axis from zero  ·  a zoomed line axis whose range is printed on the axis
```
**Read the code:** is the mark a bar, column or area (length encodes value) or a line (position does)? Is the domain computed from data (`'dataMin'`)? For a line, is the zoom visible to the reader? **Finding when** a length-encoding mark's axis starts above zero, or a zoomed line axis hides its range. **Proof:** the rendered lowest tick label on the value axis is not 0, and two bars' rendered heights differ in ratio from their values.

### 3. Size encodes radius

```
BAD:   r={d.value}  ·  d3.scaleLinear().domain([0, max]).range([2, 40]) feeding `r`
GOOD:  r ∝ √value (d3.scaleSqrt), or a mark that encodes by length
```
**Read the code:** does the library map the size channel to area or to radius (read its docs for the installed version, never from memory)? Is the scale linear in radius? **Finding when** value maps linearly to radius. **Proof:** two rendered circles: their area ratio differs from their value ratio.

### 4. Two value axes

```
BAD:   <YAxis yAxisId="revenue" /><YAxis yAxisId="orders" orientation="right" />   ·   yAxis: [{…}, {…}]
GOOD:  two charts sharing the x-axis (small multiples), or both series indexed to a common baseline
```
**Read the code:** do the two axes carry different units with independently chosen domains? **Finding when** they do. **Proof:** static (both axis declarations cited); the rendered chart shows two scales on one plot.

### 5. Missing data drawn as data

```
BAD:   <Line connectNulls />  ·  spanGaps: true  ·  row[s.name] = d.values[s.id] ?? 0 before plotting
GOOD:  the line breaks at the gap, or the gap is marked; a real zero stays zero, a missing reading stays null
```
`spanGaps` and null-to-zero coercion are the two that hide furthest from the chart config: check the data transform, not only the options object. The transform often lives in a model or view-model file the chart file never names (grep 5b): a rate helper that returns 0 on an empty denominator draws "no rate yet" as 0 % (`precedents/ui.md` § 103). **Read the code:** can the source return no reading for a bucket (a store with no sales that day versus no report)? Is zero meaningful? **Finding when** a missing reading is bridged or plotted as zero. **Proof:** render with one null in the fixture data: the path stays continuous across the gap, or a zero bar or point appears.

### 6. Data colour

1. **Where does it come from?** Series colours drawn from the UI accent ramp or brand tokens mean the project has no data ramp: the fix is to add one, not to hand-pick hexes at the call site.
2. **Is the family right?** Sequential for magnitude, diverging only around a *real* midpoint, categorical for identity. A rainbow used as sequential is a finding every time: hue carries no order.
3. **Categorical ceiling.** More than about 8 series is a finding; propose grouping the tail.
4. **Second channel.** A series set separated by colour alone fails. Emulate a colour-vision deficiency and check greyscale (which also covers print).
5. **Semantic collision.** A series in the system's destructive or success hue is making a claim; flag it.
6. **Contrast.** Marks a reader must distinguish are UI components: **≥ 3:1** against the plot background (WCAG 2.2 SC 1.4.11). Compute it. Gridlines and non-essential decoration are exempt.
7. **Dark mode.** A ramp tuned on a light plot can invert its perceptual order on a dark one. Check both themes, or record that dark is unshipped.

**Finding when** any of the seven fails on a rendered chart. **Proof:** computed — the CVD-emulated screenshot per deficiency type with the series still distinguishable (or not), and the contrast ratio per series per theme. "Looks distinguishable to me" is the failure this skill exists to catch, and the auditor is not exempt from it.

### 7. Units, labels and legend

- A chart with no unit, currency or period on an axis title, value label or tile suffix → finding.
- A legend where direct labels would fit → finding (low, high value): direct labels remove the colour-matching round trip.
- Legend order not matching the visual series order → finding.
- A value reachable only by hover → finding on any surface that must work on touch or in print.
- No title, or a title naming the fields where the surface has a finding to state → a choice to confirm, not an automatic fix.

**Proof:** the rendered chart (axis title text, legend order against series order), cited.

### 8. Order and aspect

**Read the code:** is rank the question (then sort by value; time and ordinal scales keep their own order)? Do comparable charts of the same series family share a plot shape? **Finding when** a categorical axis sits in source or alphabetical order where rank is asked, or comparable charts differ in aspect. **Proof:** the rendered category order against the values; the rendered plot boxes.

## Proof

Run on a production build at the chart's route, with the data the route really serves (or a seeded fixture with a null, a zero and a large value). The CVD emulation uses the Chrome DevTools Protocol's `Emulation.setEmulatedVisionDeficiency` (types `achromatopsia`, `deuteranopia`, `protanopia`, `tritanopia`, plus `blurredVision` and `reducedContrast`; read from the protocol's `Emulation.pdl`, 2026-10-05), which Playwright reaches through a CDP session on Chromium. Both checks are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states: *Rendered chart geometry* and *Colour-vision emulation* (V144). The geometry reader below is this skill's helper; the CVD loop (one screenshot per deficiency, then `type: 'none'`) is the snippet's.

```ts
// §2 / §3 / §8: read the rendered SVG. Recharts, Nivo, Visx, Victory, ECharts' SVG renderer and d3 all draw <text> ticks and
// <rect> / <circle> marks; a canvas renderer has no DOM marks — switch it to its SVG renderer or read its option model.
export const geometry = (page: Page, chart: string) => page.locator(chart).evaluate((root) => {
  const ticks = [...root.querySelectorAll('text')].map((t) => t.textContent?.trim()).filter(Boolean);
  const bars = [...root.querySelectorAll('rect')].map((r) => r.getBoundingClientRect().height).filter((h) => h > 0);
  const dots = [...root.querySelectorAll('circle')].map((c) => Number(c.getAttribute('r')));
  return { ticks, bars, dots };
});
// §6: the Colour-vision emulation loop in proof-oracles.md; the series must stay distinguishable in every screenshot,
// and each series colour clears 3:1 on the plot.
```

**Fails first:** before the fix, the lowest value tick reads above 0 on a bar chart; bar heights are out of ratio to their values; two circles' area ratio departs from their value ratio; the seeded null draws a continuous path or a zero; a CVD screenshot merges two series, or a series computes below 3:1 (contrast with `a11y-scan`'s `contrastOf` helper when the frontend pack is installed, else the WCAG relative-luminance formula on the computed fills). After the fix each check passes on the same route and data. Write the colour-vision artifact paths into the report; with no browser, print `Colour-vision check: NOT RUN` and keep every §6 row `[report-flagged]`.

**Whole-class variants:** each chart library in the lane table and hand-rolled SVG or canvas; light and dark; the mobile width; print; a series set of 2, 8 and 12; a null, a zero and a negative value; the same chart reused from a shared builder.

## Output

```
chart-encoding-audit — lanes: recharts 2.15.4 (apps/web/package.json); hand-rolled SVG primitives (shared/ui/charts)
Inventory: 17 chart files · 1 by name only (chart of accounts) · data ramp: --series-1…6 per theme (shared/ui/charts/chart-palette.ts:162)
Colour-vision check: CDP emulation, 4 types — artifacts at ai/audits/charts-2026-10-05/ | NOT RUN

Findings: 1 · Unconfirmed: 1

1. src/features/merchants/model/merchant-reports.ts:121                             [report-with-fix]   high
   §5 missing data drawn as data — `pct(n, d)` returns 0 when `d` is 0, and the daily delivery-rate and rejection-rate
   lines plot it (merchant-report-charts.tsx:111). Question: how did daily delivery and rejection rates move. A day with
   orders but nothing shipped yet has no rate; it plots as 0 %, which reads as delivery collapsing on the latest days.
   Route /merchant/reports. Proof: a unit test where the daily builder gets shipped = 0 expects null (it gets 0). Fix:
   return null; the area breaks at the gap by default.

2. src/features/delivery/analytics/components/DeliveryCharts.tsx:116                  [report-flagged]    medium
   §1 mark — a donut over carrier shares. Unproven link: whether the surface asks for share of whole (fits) or a ranking
   across 9 carriers (a sorted bar). Settling input: the analytics spec or the stakeholder's question.

Verification: 28 candidates → 1 finding · 1 unconfirmed · 2 hardening · 0 pre-existing · 24 refuted

Class coverage:
  §1  mark to question     checked (1 hit → 1 unconfirmed)
  §2  baseline             checked (0 hits; 17 charts' lowest ticks read 0 on the rendered pass)
  §3  size channel         checked (0 hits)
  §4  dual axes            checked (0 hits)
  §5  missing data         checked (3 hits → 0, an emptiness check, a stacked sum and an accumulator; 5b 14 → 1 finding)
  §6  data colour          checked (data ramp present; 4 CVD types on 6 chart routes → 0 findings)
  §7  units and labels     checked (7 files → 0 findings; the shared chrome formats values) · Live, unreviewed (2 files)
  §8  order and aspect     checked (rendered order read on 6 routes → 0 findings)
```

`[report-with-fix]`: the config line, the route, the question, the proof and a local fix are present. `[report-flagged]`: one link is unproven (no question stated, no harness, a library default not read), and the row names it. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the grep ran on present chart files; `N/A (no chart library and no hand-rolled chart files)` when grep 0b is empty; `blocked (<reason>)` when a grep failed; `NOT RUN` is a real state for the colour-vision check and must be printed — a §6 that quietly omits it reads as a pass. A single **missing-infrastructure** line names an absent data ramp: one fix that closes most of §6, picked up by `@design-system-architect`.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (posting rules § 1–10; contrast exemptions § 19; charts § 83, 86, 96, 97, 103) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The chart precedents, in short:

- **A zoomed line axis that prints its range** is the rule, not a breach (§ 96).
- **A real zero** (a store open with no sales) plotted as zero is correct; only a *missing* reading is §5. Read the source (§ 97).
- **An emptiness check** (`(d.value ?? 0) > 0` deciding whether to render) is not a plotted value (§ 97).
- **A sum over buckets with no events** (hourly quantities in a stacked bar) is a true zero; a **rate over an empty denominator** is a missing reading (§ 103).
- **A colour picker's palette or a legend swatch list** is data, not the series ramp (§ 86).
- **Charts that stay LTR** in an RTL locale (time axes, numeric scales) are an intended exception, not an RTL defect (§ 83).

## When to run

- Before shipping any dashboard, report or analytics surface; on a diff touching a chart config, a chart data transform or the data ramp.
- **Immediately after `/redesign` or `/art-direct` re-themes existing charts**: re-theming is the moment a wrong mark gets locked in behind a beautiful skin.
- When a stakeholder reads a number off a chart and gets it wrong. That is a reproducible encoding bug, not a training issue.
- Quarterly on an analytics surface, alongside `design-token-audit`.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on a finding without `<file:line>` for the chart config, spec or transform.
- Halt on a colour-safety verdict that was not **computed**: a contrast ratio, or a colour-vision emulation naming the tool with its artifact.
- Halt on a proposed data ramp whose values are invented rather than derived from a named perceptual scale or the project's resolved tokens.
- Halt on filing a re-theming finding here. It routes to `ui-design-sweep`.
- Halt on asserting a chart is wrong without naming the QUESTION it should answer.
- Do not report a grep hit as a finding. A class whose grep did not run is `blocked`, never `checked`.

## Related

- [`data-visualization.md`](../../ai-patterns/data-visualization.md) — owns every rule this skill cites. [`axis-catalog.md`](../../ai-patterns/axis-catalog.md) § The companion floor — why a chart-encoding finding is not a 17th axis. [`dark-mode.md`](../../ai-patterns/dark-mode.md) — the second set of ramp values.
- `design-token-audit` (this pack) — whether values come from the system; this skill asks whether the drawing is true.
- `ui-design-sweep` § `normalize-surface` (this pack) — re-theming and composite-surface completeness.
- `a11y-code-scan`, `a11y-scan` §3 (frontend pack, when installed) — the chart's text alternative and keyboard access, and series contrast as a WCAG finding.
- `@design-system-architect` — emits the sequential, diverging and categorical ramps as tokens. `@ux-reviewer` — receives findings where the misread has a task cost.
- `/frontend-audit` (frontend pack, when installed) — dispatches this skill as its Chart encoding row (`--classes=charts`) and folds this coverage block into its class ledger; `/frontend-fix` closes the rows.
