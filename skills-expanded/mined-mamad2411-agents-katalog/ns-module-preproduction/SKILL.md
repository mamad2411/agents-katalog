---
name: ns-module-preproduction
description: Pre-production for New Society course modules using tldraw. Use when David wants to design, outline, or build visual canvases for NS modules before recording. Triggers on NS module prep, module visual, module canvas, pre-production, recording prep.
user-invocable: true
---

# NS Module Pre-Production

Build visual pre-production canvases for New Society course modules using the tldraw SDK. Each module gets its own tldraw canvas that David uses as a visual aid while recording.

## Context Files (read before starting)
1. `work/new-society/classroom.md` — master index + cross-cutting decisions
2. **Per-course files** — `week-1.md`, `week-2.md`, `week-3.md`, `month-2.md` through `month-7.md` — each contains the module outline AND detailed talking points for that course
3. `work/new-society/sprint.md` — sprint progress, recording status
4. `work/new-society/module-details.md` — **DEPRECATED (17-04-2026). DO NOT USE.** Content migrated to per-course files.

## File Management (CRITICAL — update files proactively, not just when asked)

**After EVERY interaction where David shares decisions, progress, or preferences, update the relevant files immediately:**

### `classroom.md` — The Master Index
- Links to per-course files
- Cross-cutting design principles
- **Does NOT contain:** module outlines, talking points, or course-specific design decisions — those go in the per-course files

### Per-course files (week-1.md, month-2.md, etc.) — The Source of Truth
- Module-by-module outline (titles + status ✅/🟡)
- Talking points, bullet points, key messages for each module
- Sources, references, quotes David wants to use
- Tldraw canvas content decisions (what sections, what visuals)
- David's exact words when he describes what he wants in a module — save them verbatim
- Course-specific design decisions and notes
- **Write to the correct per-course file as soon as content is decided** — don't wait until the canvas is built

### `sprint.md` — Progress & Insights
- Sprint progress tracking (what's done, what remains)
- Insights about creating educational content
- What makes good modules (patterns David validates)
- Timeline updates and sprint restructuring decisions

### Daily file (`work/daily/DD-MM-YYYY.md`) — David's Decisions
- Decisions made today
- Progress completed
- How David is thinking about things
- Observations and preferences spotted from his responses

**Rule: If David says something important and you DON'T save it to a file, you are failing.** David's words disappear after the conversation. The files persist. Always err on the side of saving too much rather than too little.

## Working With David

### Extraction, Not Prescription
- David has the vision. Your job is to EXTRACT it from him, not prescribe your own ideas.
- Ask short, direct questions — 1-2 sentences max. David is often sick or low energy.
- When David gives a direction, RUN WITH IT. Build immediately. Don't over-discuss.
- Suggest angles he might not have thought of — "what about X?" — but defer to his judgment.
- Save his exact words into the relevant per-course file when he describes what a module should cover.

### Speed Over Perfection
- Good enough = move on. David values speed over pixel-perfect layouts.
- Don't ask redundant questions. Read the files first — if the answer is there, don't ask.
- When David corrects you, fix it instantly. Don't explain why you were wrong.
- Batch work when possible — if 3 modules need the same type of change, do all 3 at once.

### Proactive Updates
- After David records a module: immediately mark ✅ in classroom.md, update sprint.md progress
- After content is decided: immediately save to the relevant per-course file
- After a decision is made: immediately save to daily file + relevant .md files
- Don't wait for David to ask you to update files. Just do it.

## Project Location
`work/new-society/modules/` — tldraw project (gitignored, local dev tool only)

## File Structure
Each module gets its own file. `App.tsx` imports the active one:

```
work/new-society/modules/src/
├── App.tsx                  ← imports the active module
├── modules/
│   ├── w3m17.tsx            ← Week 3, Module 17
│   ├── w3m18.tsx            ← Week 3, Module 18
│   └── ...
```

### Naming Convention
`w{week}m{module}.tsx` — e.g. `w3m17.tsx` for Week 3 Module 17. For months (Section 2+), use `m{month}m{module}.tsx`.

### Switching Modules
Change one import line in `App.tsx`:
```tsx
import { mount } from './modules/w3m18'  // ← swap this
```

### Module File Template
Each module exports a `mount(editor: Editor)` function:
```tsx
import { Editor, createShapeId, toRichText } from 'tldraw'

export function mount(editor: Editor) {
  // Header
  editor.createShape({
    id: createShapeId('header'),
    type: 'text',
    x: 300, y: 30,
    props: {
      richText: toRichText('week 3 -- module XX'),
      size: 's' as const,
      color: 'white' as const,
    },
  })

  editor.createShape({
    id: createShapeId('title'),
    type: 'text',
    x: 100, y: 80,
    props: {
      richText: toRichText('Module Title Here'),
      size: 'xl' as const,
      color: 'white' as const,
      w: 800,
    },
  })

  // Sections go here...
}
```

## Running
Auto-start the dev server if it's not already running. Check with `lsof -i` or `curl` first, then start if needed:
```bash
cd work/new-society/modules
npm run dev
```
Runs on localhost (check terminal for port). After code changes, refresh the browser. Clear localStorage if shapes persist from previous edits.

## Design Defaults
- **VARIETY IS THE #1 PRIORITY.** No two consecutive modules should look the same. Alternate between layout styles, dark/light mode, and visual density. Predictable = boring.
- Dark mode: `colorScheme: 'dark'`, white text for body content
- Light mode: `colorScheme: 'light'`, black text for body content
- **Green headers** for educational/positive sections
- **Orange headers** for limiting beliefs, fears, warnings
- **Section spacing** — use a `sections` array at the top of the mount function to define Y offsets for each section. All elements within a section use relative offsets from their section's base Y. To adjust spacing, change ONE number in the array — never hunt through individual y-values.
  ```tsx
  const S = [0, 350, 1020, 1540, 2080, 2580] // section start Y positions
  // Header uses S[0], Section 1 uses S[1], Section 2 uses S[2], etc.
  // Within a section: y: S[2] + 90 (relative offset)
  ```
  Keep 200-300px gaps between sections. To increase all gaps uniformly, add a constant to each entry.
- **Font:** `'draw'` for headers (tldraw default), `'sans'` for content in geo shapes, `'mono'` for code/technical terms

## Layout Styles (alternate between these!)

**Style A — Visual / Rich:** Lots of logos, icons, geo shapes, colored rectangles, arrows, flow diagrams, columns. Multiple assets. Feels like an infographic. Good for concept-heavy modules (e.g. frontend vs backend, tech stack comparisons).

**Style B — Clean / Minimal:** Text-only. No rectangles, no geo shapes, no arrows. Just numbered steps, plain text, maybe one logo near the title. Spacious, elegant, easy to scan. Good for setup/walkthrough modules (e.g. install Codex, deploy to Vercel).

Alternate these styles between modules. If the last 2-3 modules were visually heavy, make the next one clean. If the last one was minimal, go rich on the next. The goal is that when a student moves through modules, each one feels fresh and different.

## Visual Patterns
- **File/data type lists:** colored badge box → arrow → description text
- **Flow diagrams:** box → arrow → box → arrow → box (horizontal)
- **Talking points:** section title (colored) + indented bullet text below
- **Pro tips:** `geo` rectangle with `fill: 'semi'`, orange color
- **Comparisons:** two columns side by side (e.g. "those who quit" vs "those who finish")
- Mix shapes: rectangles, ellipses, diamonds. Don't make everything rectangles.

## Supportive Visuals (IMPORTANT)
Every module should include relevant visual assets — logos, icons, or graphics pulled from the web. This makes the canvases feel professional and helps David's students connect visually with the content.

**What to add:**
- Brand/product logos when mentioning tools (e.g. Claude logo, OpenAI logo, Vercel, Supabase, GitHub)
- Relevant icons or SVGs that illustrate concepts
- Geometric drawings or diagrams where text alone isn't enough

**How to add images:**
1. Download SVG/PNG files into `work/new-society/modules/public/logos/` (Vite serves this automatically)
2. Create assets with `AssetRecordType` from tldraw:
   ```tsx
   import { AssetRecordType } from 'tldraw'
   const assetId = AssetRecordType.createId('my-logo')
   editor.createAssets([{
     id: assetId,
     type: 'image',
     typeName: 'asset',
     props: { name: 'logo.svg', src: '/logos/logo.svg', w: 200, h: 200, mimeType: 'image/svg+xml', isAnimated: false },
     meta: {},
   }])
   ```
3. Place image shapes on the canvas:
   ```tsx
   editor.createShape({
     id: createShapeId('my-logo'),
     type: 'image',
     x: 100, y: 100,
     props: { w: 65, h: 65, assetId: assetId },
   })
   ```

**Sources:** Wikimedia Commons for clean SVGs, official brand pages, or UXWing for icon packs. Always prefer SVG over PNG.

## Shape API Reference

### Text
```tsx
editor.createShape({
  id: createShapeId('id'),
  type: 'text',
  x: 100, y: 100,
  props: {
    richText: toRichText('Text here'),
    size: 'xl',  // 's' | 'm' | 'l' | 'xl'
    color: 'white',
    w: 800,  // optional width constraint
  },
})
```

### Geo (rectangles, ellipses, diamonds, etc.)
```tsx
editor.createShape({
  id: createShapeId('id'),
  type: 'geo',
  x: 100, y: 200,
  props: {
    w: 340, h: 140,
    geo: 'rectangle',  // 'rectangle' | 'ellipse' | 'diamond' | 'star' | 'hexagon' | 'cloud'
    color: 'violet',
    fill: 'solid',     // 'none' | 'solid' | 'semi' | 'pattern'
    richText: toRichText('Content'),
    size: 'm',
    font: 'sans',      // 'sans' | 'serif' | 'draw' | 'mono'
  },
})
```

### Arrows (point-based ONLY — bindings don't work)
```tsx
editor.createShape({
  id: createShapeId('id'),
  type: 'arrow',
  x: 300, y: 400,
  props: {
    color: 'white',
    start: { x: 0, y: 0 },
    end: { x: 100, y: 0 },
  },
})
```

### Available Colors
`'black'` `'white'` `'grey'` `'violet'` `'blue'` `'green'` `'orange'` `'red'` `'light-violet'` `'light-blue'` `'light-green'` `'light-red'` `'yellow'`

## Process
1. David says which module to work on
2. Auto-start the dev server if not already running
3. Read `classroom.md` for the module title and position in the outline
4. **Read ±3 modules around the current one.** Understand what was just taught, what's coming next. This prevents overlap, ensures smooth flow, and reveals gaps where the current module needs to add unique value.
5. Read the relevant per-course file for reference on how previous modules were structured
6. **Interview David — extract his vision.** Ask short, direct questions. What does he want to cover? What should students walk away with? Suggest angles he might not have thought of — "what about X?" — to pull good ideas out of his brain. Keep questions concise (1-2 sentences max). David is often sick or low energy — don't waste his attention.
7. **Suggest ways to make the module more valuable.** Based on the ±3 module context, identify risks (too thin, overlaps with adjacent module, missing a teaching point). Propose additions that fill gaps. But always defer to David's judgment.
8. Build a draft canvas and ask David to review
9. David reviews in browser, gives feedback, iterate
10. When David confirms the outline is good and has recorded: save module details to the per-course file
11. Switch `App.tsx` import to next module, repeat

## Communication Style
- **Be extremely concise.** Short sentences. No fluff. David's attention span is limited — every word must earn its place.
- **Ask one question at a time** when possible. Don't dump 5 questions in one message.
- **Suggest, don't lecture.** "What about adding X?" is better than a paragraph explaining why X matters.
- **When David gives an idea, run with it.** Don't over-discuss — build the canvas and let him react visually.

## Rules
- **David's vision first.** Ask what he wants to cover. Don't assume or prescribe.
- **Manual edits in the browser are NOT saved to code.** Only localStorage. Always make changes in the .tsx file.
- **Update the per-course file** after finalizing each module's pre-production.
- **This is NOT a coding course.** Keep visuals simple. No code syntax on screen. Speak to non-technical people.
- **Keep text short.** Max 10-15 words per bullet point in shapes.
- **Always zoom to fit** at the end of mount: `setTimeout(() => editor.zoomToFit({ animation: { duration: 500 } }), 100)`

## Pitfalls
- **Shapes from previous module persist in browser.** If old shapes show up after switching modules, clear localStorage. The code is correct — it's a browser cache issue.
- **Building tldraw canvases WITHOUT saving content to the per-course file first.** This is the #1 past mistake. EVERY piece of content on a canvas MUST exist in the per-course .md file BEFORE or AT THE SAME TIME as the canvas is built. The per-course file is the source of truth. The .tsx file is just the visual rendering. If content exists only in the .tsx file and not in the per-course file, you have FAILED. Always write to the per-course file first, then build the canvas from it.
- **Creating modules David didn't ask for.** NEVER batch-create module files ahead of time. Only create the module David is currently working on.
- **Content jumping ahead in the curriculum.** Check `classroom.md` for what comes before and after this module. Don't cover topics that belong to later modules.
- **MODULE CANNIBALIZATION (critical, 17-04-2026).** Before writing content for ANY module, read the ±3 surrounding modules in BOTH the per-course .md file AND the tldraw .tsx files. Check for overlap. M3/M4/M5 of Month 2 nearly became the same module because kill criteria, prioritization, and Vectal stories were duplicated across all three. Each module MUST have a single specialized purpose. If content could belong to multiple modules, pick ONE home for it. Never put the same concept (even reworded) in adjacent modules. When in doubt, ask David where it belongs.
- **SVG logos not rendering.** Make sure files are in `public/logos/`, not `src/`. Vite only serves the `public/` folder as static assets.
- **SVG invisible on dark/light background.** Many SVGs from Wikimedia/FontAwesome have no `fill` attribute on their `<path>` elements, which defaults to `fill="black"`. On dark mode canvases, they're invisible. **Always inspect downloaded SVGs and add an explicit `fill="white"` (for dark mode) or `fill="black"` (for light mode) to the `<path>` elements.** If a module alternates mode, consider using a visible color like a brand color instead.
- **Forgetting to switch App.tsx import.** After creating a new module file, always update the import in `App.tsx` AND set the correct `colorScheme` (alternate dark/light).
- **Over-designing canvases.** Don't be perfectionistic. Good enough = move on. Speed matters more than pixel-perfect layouts.

## Verification
- **Browser check:** Refresh localhost — all sections render, no overlapping shapes, text is readable, logos/images load.
- **Zoom to fit works:** Canvas auto-zooms to show all content on load.
- **Per-course file updated:** After David confirms and records, the module's outline is saved to the relevant per-course file.
- **App.tsx points to correct module:** Import line matches the current working module.
