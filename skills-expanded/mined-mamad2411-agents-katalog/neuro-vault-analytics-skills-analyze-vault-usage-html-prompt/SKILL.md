# /analyze-vault-usage HTML companion prompt

You are producing a single-file HTML report that visualises the same usage analysis you just produced as Markdown in Step 3. Emit one complete HTML document — no preamble, no commentary, no trailing prose. Output starts with `<!doctype html>` and ends with `</html>`.

The HTML is a visual companion to the MD note. **Do not re-do the critique work** — reuse the TL;DR, patterns observed, and suggestions you already wrote in Step 3, verbatim, where this template asks for them.

## Inputs

`AnalyticsReport` (full JSON, same as `prompt.md`):

```json
<<REPORT_JSON>>
```

Plus, in your working memory: the Markdown body you produced in Step 3. Reuse its TL;DR, patterns, and suggestions sections directly.

## Output scaffold

Emit exactly this HTML structure, filling the `{{ ... }}` slots. Remove any optional section if its skip-condition fires (see "Section rules" below). Do not add comments to the output.

The `<!-- ... -->` comments inside the scaffold mark *where* each section goes — strip them from the output. Replace each comment with the real section markup (or omit the section if its skip-condition fires).

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Usage analytics {{label}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
      h1, h2 { font-family: "Iowan Old Style", "Palatino Linotype", Palatino, serif; }
      .mass-cell { display: flex; flex-direction: column; align-items: center; }
      .mass-rect { background: rgb(51, 65, 85); border-radius: 4px; }
      .mass-label { margin-top: 6px; font-size: 11px; line-height: 1.2; text-align: center; color: rgb(51, 65, 85); max-width: 120px; word-break: break-word; }
    </style>
  </head>
  <body class="max-w-5xl mx-auto p-12 text-slate-900">

    <header class="mb-12">
      <h1 class="text-4xl mb-2">Usage analytics {{label}}</h1>
      <p class="text-sm text-slate-500">{{period_start_iso}} → {{period_end_iso}}</p>
      <div class="mt-4 flex gap-2">
        <span class="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full text-xs font-medium">vault: {{buckets.vault.sessionsTotal}} sessions</span>
        <span class="bg-amber-100 text-amber-800 px-3 py-1 rounded-full text-xs font-medium">projects: {{buckets.projects.sessionsTotal}} sessions</span>
        <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-xs font-medium">total: {{buckets.total.sessionsTotal}} sessions</span>
      </div>
    </header>

    <section class="mb-12">
      <blockquote class="border-l-4 border-slate-400 pl-6 text-xl italic" style="font-family: 'Iowan Old Style', serif;">
        {{TL;DR — reuse the 2-3 sentences from MD Step 3}}
      </blockquote>
    </section>

    <!-- Where the context goes — see "Mass diagram" rule -->
    <!-- Vault vs Projects — see "Vault vs Projects" rule -->
    <!-- Tools by bucket — see "Tools by bucket" rule -->
    <!-- Unused tools — see "Unused tools" rule -->
    <!-- Cache & dead ends — see "Cache & dead ends" rule -->
    <!-- Patterns observed — see "Patterns observed" rule -->
    <!-- Suggestions — see "Suggestions" rule -->
    <!-- Per-project breakdown — see "Per-project" rule -->
    <!-- Raw aggregates — see "Raw aggregates" rule -->

  </body>
</html>
```

`{{label}}` is the derived filename label, matching the MD filename rule in `SKILL.md` Step 3: ISO week `YYYY-Www` of `period.endMs` if `(period.endMs - period.startMs) / 86400000 >= 7`, otherwise `<YYYY-MM-DD of period.startMs>_to_<YYYY-MM-DD of period.endMs>`. It is NOT the raw `period.label` field (which is the user's `--period` argument, e.g. "7d"). Compute it yourself from the timestamps. `{{period_start_iso}}` / `{{period_end_iso}}` are `period.startMs` / `period.endMs` formatted as `YYYY-MM-DD`.

## Section rules

### Where the context goes — mass diagram

**Skip this section entirely** if `buckets.total.sessionsTotal === 0`.

Pick the top 8 tools by `buckets.total.largestResultTools[].avgSizeBytes`. For each, look up its call count in `buckets.total.topTools` (match on the same key). If a tool is not in `topTools`, use count = 1.

Compute:

- `maxBytes` = the largest `avgSizeBytes` across the 8 tools
- `maxCount` = the largest call count across the 8 tools
- For each tool T:
  - `heightPx = clamp(40, round(avgBytes[T] / maxBytes * 200), 200)`
  - `widthPx  = clamp(60, round(count[T]    / maxCount * 180), 180)`

Render:

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Where the context goes</h2>
  <div class="flex flex-wrap gap-3 items-end">
    <div class="mass-cell">
      <div class="mass-rect" style="height:{{heightPx}}px; width:{{widthPx}}px;"></div>
      <div class="mass-label">{{tool_name}}<br>{{avg_kb}} KB · {{count}} calls</div>
    </div>
    <!-- one per tool, in descending avgSizeBytes order -->
  </div>
  <p class="text-sm text-slate-600 mt-3">Area ≈ total bytes the tool shipped to the model (height = avg bytes per call, width = call count).</p>
</section>
```

Strip the `mcp__neuro-vault__` prefix from `{{tool_name}}`. `{{avg_kb}}` is `round(avgSizeBytes / 1024)`.

### Vault vs Projects

**Skip this section** if `buckets.total.sessionsTotal === 0`.

Two cards side-by-side. Each card lists, for its bucket:

- Sessions total
- Top 5 tools as `name (count)`, comma-joined
- Top sequence: `topSequences[0].sequence` joined with ` → `, plus its count
- Dead-end count

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Vault vs Projects</h2>
  <div class="grid grid-cols-2 gap-6">
    <div class="border border-slate-200 rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-3">Vault</h3>
      <dl class="space-y-2 text-sm">
        <div><span class="text-slate-500">Sessions:</span> {{buckets.vault.sessionsTotal}}</div>
        <div><span class="text-slate-500">Top tools:</span> {{top 5 from buckets.vault.topTools, prefix-stripped}}</div>
        <div><span class="text-slate-500">Top sequence:</span> <span class="font-mono text-xs">{{seq joined with →}}</span> <span class="text-slate-500">×{{count}}</span></div>
        <div><span class="text-slate-500">Dead ends:</span> {{buckets.vault.deadEndCount}}</div>
      </dl>
    </div>
    <div class="border border-slate-200 rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-3">Projects</h3>
      <dl class="space-y-2 text-sm">
        <div><span class="text-slate-500">Sessions:</span> {{buckets.projects.sessionsTotal}}</div>
        <div><span class="text-slate-500">Top tools:</span> {{top 5 from buckets.projects.topTools, prefix-stripped}}</div>
        <div><span class="text-slate-500">Top sequence:</span> <span class="font-mono text-xs">{{seq joined with →}}</span> <span class="text-slate-500">×{{count}}</span></div>
        <div><span class="text-slate-500">Dead ends:</span> {{buckets.projects.deadEndCount}}</div>
      </dl>
    </div>
  </div>
</section>
```

If a bucket has no `topSequences`, omit the "Top sequence" row from that card only.

### Tools by bucket

**Skip this section** if `buckets.total.sessionsTotal === 0`.

Build a union table over `buckets.vault.topTools` and `buckets.projects.topTools`. Include every tool from either list — generic tools like `Bash`, `Read`, `Edit`, `Write` matter because their volume (and bucket asymmetry) reveals how time is actually spent. For each unique tool key across both lists:

- `vaultCount` = count from `buckets.vault.topTools` if present, else `0`.
- `projectsCount` = count from `buckets.projects.topTools` if present, else `0`.
- `total` = `vaultCount + projectsCount`.
- `isVaultTool` = `true` if the key starts with `mcp__neuro-vault__`, else `false`.

Sort rows by `total` descending. Strip the `mcp__neuro-vault__` prefix from displayed names (it's what the report is about — the namespace is implicit and the prefix is noise). Leave foreign `mcp__<server>__` prefixes intact.

Resolve each row's optional class slots at generation time — do not emit the `{{ ... }}` placeholders literally:

- `{{rowTintClass}}`:
  - `vaultCount === 0 && projectsCount > 0` → ` bg-amber-50` (note the leading space so it concatenates onto the existing class list)
  - `projectsCount === 0 && vaultCount > 0` → ` bg-slate-50`
  - both `> 0` → empty string
- `{{toolNameWeight}}`:
  - `isVaultTool === true` → ` font-semibold text-slate-900`
  - else → empty string
- `{{vaultBadge}}`:
  - `isVaultTool === true` → ` <span class="ml-2 inline-block text-[10px] uppercase tracking-wide bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded">vault</span>`
  - else → empty string

These three classifications are independent. A vault tool used only in vault gets both the slate tint AND the bold + emerald badge.

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Tools by bucket</h2>
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr class="border-b border-slate-300 text-left">
        <th class="py-2 pr-4">Tool</th>
        <th class="py-2 pr-4 text-right">Vault</th>
        <th class="py-2 pr-4 text-right">Projects</th>
        <th class="py-2 text-right">Total</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b border-slate-100{{rowTintClass}}">
        <td class="py-2 pr-4 font-mono text-xs{{toolNameWeight}}">
          {{tool_name}}{{vaultBadge}}
        </td>
        <td class="py-2 pr-4 text-right font-mono">{{vaultCount}}</td>
        <td class="py-2 pr-4 text-right font-mono">{{projectsCount}}</td>
        <td class="py-2 text-right font-mono font-semibold">{{total}}</td>
      </tr>
      <!-- one row per unique tool in the union, sorted by total desc -->
    </tbody>
  </table>
  <p class="text-sm text-slate-600 mt-3">All tool calls across vault + projects, sorted by total. <span class="inline-block text-[10px] uppercase tracking-wide bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded">vault</span> badges mark <code class="text-xs bg-slate-100 px-1 rounded">mcp__neuro-vault__*</code> tools — these are the report's lens. Amber rows are projects-only tools (the canonical "external workflow" signal); slate rows are vault-only. Counts come from per-bucket top-N tables emitted by the CLI; a low-rank tool in one bucket may appear as <code class="text-xs">0</code> even with a handful of calls.</p>
</section>
```

### Unused tools

**Skip this section entirely** only if `buckets.total.sessionsTotal === 0`. When sessions > 0 but the JSON's top-level `unusedTools` array is empty, still render the section — see the empty-array note below the scaffold.

The top-level `unusedTools` field lists catalog tools that received zero calls across vault and projects for the period. Render as a compact list. Strip the `mcp__neuro-vault__` prefix; leave foreign prefixes intact.

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Unused tools</h2>
  <ul class="grid grid-cols-2 gap-x-6 gap-y-1 text-sm font-mono">
    <li class="text-slate-600">{{tool_name}}</li>
    <!-- one per entry in unusedTools -->
  </ul>
  <p class="text-sm text-slate-600 mt-3">Catalog tools never called this period — candidates for review or removal if the pattern persists across multiple periods.</p>
</section>
```

If `unusedTools` is empty but `sessionsTotal > 0`, still render the section heading with a single line `<p class="text-sm text-slate-600">Nothing unused this period.</p>` instead of the `<ul>`. (Empty array specifically signals "good coverage", which is worth showing, not silently omitting.)

### Cache & dead ends

**Skip this section** if `buckets.total.sessionsTotal === 0`.

Use `buckets.total.cacheHitDistribution` and `buckets.total.deadEndCount`. Cache values are 0..1; render the bar widths as percentages (`value * 100`).

Resolve `{{deadEndColorClass}}` to a concrete Tailwind class while generating the HTML — emit `text-red-600` if `deadEndCount >= 5`, otherwise `text-slate-600`. Do NOT emit the conditional expression verbatim; Tailwind's CDN scanner only picks up class names that appear literally in the output.

```html
<section class="mb-12 grid grid-cols-2 gap-6">
  <div class="border border-slate-200 rounded-lg p-6">
    <h3 class="text-sm uppercase text-slate-500 mb-3 tracking-wide">Cache hit ratio</h3>
    <div class="space-y-2">
      <div class="flex items-center gap-3">
        <span class="text-xs w-12 text-slate-500">p50</span>
        <div class="flex-1 bg-slate-100 h-3 rounded"><div class="bg-emerald-500 h-3 rounded" style="width:{{p50*100}}%"></div></div>
        <span class="text-xs w-12 text-right font-mono">{{p50 to 3dp}}</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-xs w-12 text-slate-500">p90</span>
        <div class="flex-1 bg-slate-100 h-3 rounded"><div class="bg-emerald-500 h-3 rounded" style="width:{{p90*100}}%"></div></div>
        <span class="text-xs w-12 text-right font-mono">{{p90 to 3dp}}</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-xs w-12 text-slate-500">mean</span>
        <div class="flex-1 bg-slate-100 h-3 rounded"><div class="bg-emerald-500 h-3 rounded" style="width:{{mean*100}}%"></div></div>
        <span class="text-xs w-12 text-right font-mono">{{mean to 3dp}}</span>
      </div>
    </div>
  </div>
  <div class="border border-slate-200 rounded-lg p-6 flex items-center justify-center">
    <div class="text-center">
      <div class="text-4xl font-bold {{deadEndColorClass}}">{{deadEndCount}}</div>
      <div class="text-sm text-slate-500 mt-1">Dead ends</div>
    </div>
  </div>
</section>
```

### Patterns observed

**Skip this section** if `buckets.total.sessionsTotal === 0`.

Reuse your MD `## Patterns observed` body. Convert each `### High-value patterns` and `### Dead ends` MD subsection to `<h3>` blocks. Render bullets as `<ul class="space-y-2 list-disc pl-6">`. Wrap session IDs in `<code class="bg-slate-100 px-1 rounded text-xs">`.

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Patterns observed</h2>
  <h3 class="text-lg mt-6 mb-2">High-value patterns</h3>
  <ul class="space-y-2 list-disc pl-6 text-sm">
    {{converted from MD bullets}}
  </ul>
  <h3 class="text-lg mt-6 mb-2">Dead ends</h3>
  <ul class="space-y-2 list-disc pl-6 text-sm">
    {{converted from MD Dead ends bullets, or omit this h3 + ul pair if MD omitted the Dead ends subsection}}
  </ul>
</section>
```

If your MD omitted one of the subsections (e.g. no dead ends to mention), omit the same one here.

### Suggestions

**Skip this section** if `buckets.total.sessionsTotal === 0` OR if your MD `## Suggestions` had no entries.

Reuse your MD `## Suggestions` body. Group into three subsections (`MCP features` / `Vault structure` / `Prompt tuning`), emitting only those with content. Each suggestion becomes a card; pick the card colour from the confidence tag at the start of the line:

| Tag prefix | Card classes |
| ---------- | ------------ |
| `[HIGH ...]` | `border-emerald-300 bg-emerald-50` |
| `[MED ...]` | `border-amber-300 bg-amber-50` |
| `[LOW ...]` | `border-slate-300 bg-slate-50` |
| `[BLOCKED ...]` | `border-red-300 bg-red-50` |
| `[REQUIRES_VERIFICATION ...]` | `border-sky-300 bg-sky-50` |

Card shape:

```html
<div class="border-2 border-emerald-300 bg-emerald-50 rounded-lg p-4 mb-3">
  <div class="text-xs font-mono text-emerald-800 mb-1">[HIGH | 16 sessions | ~48 KB/run]</div>
  <div class="font-semibold mb-1">{{Title}}</div>
  <div class="text-sm text-slate-700">{{Action}}</div>
</div>
```

Chip-text colour per tier (the `text-...` class on the `<div class="text-xs font-mono ...">` inside the card):

- HIGH → `text-emerald-800`
- MED → `text-amber-800`
- LOW → `text-slate-700`
- BLOCKED → `text-red-800`
- REQUIRES_VERIFICATION → `text-sky-800`

LOW uses `-700` rather than `-800` because `text-slate-800` is nearly indistinguishable from `text-slate-900` body text on `bg-slate-50`; `text-slate-700` keeps the chip readable but visually de-emphasised.

Section wrapper:

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Suggestions</h2>
  <h3 class="text-lg mt-6 mb-3">MCP features</h3>
  {{cards for this group, one per suggestion, using the card shape above; omit the preceding <h3> if this group has no suggestions}}
  <h3 class="text-lg mt-6 mb-3">Vault structure</h3>
  {{cards for this group, one per suggestion, using the card shape above; omit the preceding <h3> if this group has no suggestions}}
  <h3 class="text-lg mt-6 mb-3">Prompt tuning</h3>
  {{cards for this group, one per suggestion, using the card shape above; omit the preceding <h3> if this group has no suggestions}}
</section>
```

### Per-project breakdown

**Skip this section** if `perProject` is empty.

Render as a table. `decodedPath` is human-readable; show it instead of the encoded `project`. Top tools = top 5 from `perProject[].topTools`, prefix-stripped, comma-joined.

```html
<section class="mb-12">
  <h2 class="text-2xl mb-4">Per-project breakdown</h2>
  <table class="w-full text-sm border-collapse">
    <thead>
      <tr class="border-b border-slate-300 text-left">
        <th class="py-2 pr-4">Project</th>
        <th class="py-2 pr-4">Sessions</th>
        <th class="py-2 pr-4">Top tools</th>
        <th class="py-2">Unique tools</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b border-slate-100">
        <td class="py-2 pr-4 font-mono text-xs">{{decodedPath}}</td>
        <td class="py-2 pr-4">{{sessionsTotal}}</td>
        <td class="py-2 pr-4 text-xs">{{top 5 tools, prefix-stripped}}</td>
        <td class="py-2 text-xs">{{uniqueTools joined or "none"}}</td>
      </tr>
      <!-- one row per perProject entry -->
    </tbody>
  </table>
</section>
```

### Raw aggregates

**Always render**, including in the empty-period case (everything zero/empty is still a consistent shape).

```html
<details class="mt-12 border-t pt-6">
  <summary class="cursor-pointer text-sm uppercase text-slate-500 tracking-wide">Raw aggregates</summary>
  <div class="mt-4 space-y-6">
    <details class="border border-slate-200 rounded p-4">
      <summary class="cursor-pointer font-semibold">Vault bucket</summary>
      <pre class="mt-3 text-xs whitespace-pre-wrap">{{vault raw}}</pre>
    </details>
    <details class="border border-slate-200 rounded p-4">
      <summary class="cursor-pointer font-semibold">Projects bucket</summary>
      <pre class="mt-3 text-xs whitespace-pre-wrap">{{projects raw}}</pre>
    </details>
    <details class="border border-slate-200 rounded p-4">
      <summary class="cursor-pointer font-semibold">Total (union)</summary>
      <pre class="mt-3 text-xs whitespace-pre-wrap">{{total raw}}</pre>
    </details>
    <p class="mt-4 text-xs text-slate-500"><span class="font-semibold">Warnings:</span> {{warnings joined or "none"}}</p>
  </div>
</details>
```

For `{{vault raw}}` / `{{projects raw}}` / `{{total raw}}`, emit the per-bucket fields the MD's "Raw aggregates" section emits: top tools, top 2-grams, top 3-grams, largest result tools, stale-path hits, current-note anchors, cache-hit distribution, subagent budget, dead-end count. Plain text, one field per labelled paragraph. `warnings` is a top-level `AnalyticsReport` field — emit it once at the bottom of the outer `<details>` block, after the three nested bucket details, not inside each bucket.

If a field is empty for a bucket — `null`, `[]`, or otherwise absent (e.g. `currentNoteAnchors` is always empty for `projects`; `stalePathErrors` may serialise as `null`) — write "none" rather than emitting an empty list or the literal `null`.

## Empty-period handling

If `buckets.total.sessionsTotal === 0`:

- Render the header with all three badges showing `0`.
- Render the TL;DR with: *Sessions touching the vault: 0. No patterns observed.*
- **Omit entirely**: "Where the context goes", "Vault vs Projects", "Tools by bucket", "Unused tools", "Cache & dead ends", "Patterns observed", "Suggestions", "Per-project breakdown".
- **Render**: "Raw aggregates" (everything zero/empty, just for shape).

## Style rules

- One self-contained HTML document, no external JS beyond the one CDN script in `<head>`.
- No external CSS beyond Tailwind CDN.
- Strip the `mcp__neuro-vault__` prefix from user-visible tool names. Do NOT strip other `mcp__<server>__` prefixes (e.g. `mcp__ccd_session__mark_chapter` stays as-is — those are foreign tools called from external projects in the `projects` bucket and the prefix is the actual disambiguator). Raw aggregates may keep all prefixes — they are debug data.
- Generous whitespace: section margins `mb-12`, card padding `p-6`, gap `gap-6` inside grids.
- Do not emit HTML comments to the output. They're noise.
- Do not emit any prose outside the template (no preamble, no trailing notes).
