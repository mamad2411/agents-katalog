---

name: research-presentation-studio

description: Use when the user wants to create, redesign, polish, audit, or export research presentations, PPT, PPTX, slides, deck, PowerPoint, Google Slides, defense slides, seminar talks, project reports, paper-to-slides, visual briefings, or web-based horizontal presentation pages. For HTML web decks, delegate visual execution to the installed original guizang-ppt-skill.

---



# Research Presentation Studio



This skill owns presentation work: PPTX, web decks, defense decks, seminar reports, project updates, paper-to-slides, and visual briefings.



Local source of truth:



- Workflow contract: `skills/catalog/research_presentation_workflow.json`

- Visual execution skill: `$CODEX_HOME/skills/guizang-ppt-skill`

- Swiss validator: `$CODEX_HOME/skills/guizang-ppt-skill/scripts/validate-swiss-deck.mjs`

- Official PPTX tool: `Presentations` / `presentations@openai-primary-runtime`



This skill is a VELA research workflow wrapper. It does not fork, simplify, or rewrite guizang-ppt-skill's visual system. When making HTML web decks, first activate and follow the installed original `guizang-ppt-skill`; this wrapper only adds research-route confirmation, evidence boundaries, output-mode decisions, and final QA.



## Boundary



- Use this skill for slides and presentations.

- Use `research-figure-studio` for formal paper figures, mechanism diagrams for manuscripts, conceptual paper diagrams, and image2-first academic figures.

- Use `figure-table-studio` for real-data charts, regression tables, coefficient plots, event-study plots, and publication figures from data.

- Use `evidence-based-literature-workflow` or `writing-reference-capture` for citation evidence. A slide deck never replaces reference verification.



## Default Posture



Prefer the guizang visual system unless the user asks for a different style:



- Style A: electronic magazine and e-ink. Use for humanities/social-science talks, industry observation, narrative sharing, and visually warm presentations.

- Style B: Swiss International. Use for data reports, methods, computational social science, product/toolchain presentations, technical summaries, and any request for Swiss Style, grid, Helvetica, or minimalist keynote visuals.



If the user says only "make a PPT", ask at most three questions before working:



1. Output: web deck, PPTX, or both?

2. Audience and length: who will see it and how many minutes/pages?

3. Style and theme: electronic magazine/e-ink or Swiss International, then one theme from that style's preset list.



If the user already gave enough material, proceed with explicit assumptions.



Do not skip theme choice. After the style is selected, show the matching preset list and ask the user to pick:



- Style A themes: 墨水经典, 靛蓝瓷, 森林墨, 牛皮纸, 沙丘.

- Style B themes: 克莱因蓝, 柠檬黄, 柠檬绿, 安全橙.



If the user explicitly asks Codex to choose, use the recommended preset from the source theme guide and record the reason in the slide manifest.



## Workflow



1. Confirm scope.

   - State whether this is `research-presentation` or another route.

   - If it might actually be a paper figure, table, manuscript rewrite, or evidence check, clarify first.



2. Build the slide manifest before generation.

   - Page number.

   - Page purpose.

   - Visual system.

   - Layout or PPT section.

   - Image slot and ratio.

   - Evidence/source boundary.

   - Output mode: HTML, PPTX, or hybrid.



3. Select the visual system.

   - For Style A, follow `$CODEX_HOME/skills/guizang-ppt-skill/references/themes.md`, `layouts.md`, `components.md`, and `checklist.md`.

   - For Style B, follow `$CODEX_HOME/skills/guizang-ppt-skill/references/themes-swiss.md`, `swiss-layout-lock.md`, `layouts-swiss.md`, and `checklist.md`.

   - For maps or place relationships in Style B, also read `swiss-map-component.md`.

   - Ask the user to select one preset theme from the chosen visual system before generating pages, unless the user explicitly delegates the choice.



4. Plan assets.

   - User screenshots are evidence assets. Preserve them when the content matters.

   - Read `screenshot-framing.md` before beautifying screenshots.

   - Use image2 for presentation visuals when needed; lock ratio, language, text, and no-fabrication constraints first.

   - Use `image-prompts.md` as the prompt pattern library.



5. Generate.

   - HTML web deck: delegate to the installed original `guizang-ppt-skill`; copy its matching template into the project presentation folder and follow its SKILL.md exactly.

   - PPTX: use the official `Presentations` plugin and mirror the same visual system with PowerPoint-compatible layouts.

   - Hybrid: make the HTML visual prototype first, then produce PPTX or exported preview assets if required.



6. Verify.

   - Open the deck in a browser or render/preview the PPTX.

   - For Style B HTML, run:



```powershell

node $env:CODEX_HOME\skills\guizang-ppt-skill\scripts\validate-swiss-deck.mjs path\to\index.html

```



   - Check typography, page rhythm, image ratios, bottom navigation space, page numbers, screenshot fidelity, and reading distance.

   - For research decks, check that claims, data, and literature references do not exceed available evidence.



## Style A Rules



- Use the magazine/e-ink template from `$CODEX_HOME/skills/guizang-ppt-skill/assets/template.html`.

- Use one theme from `themes.md`; do not freely mix colors.

- The user-facing theme options are: 墨水经典, 靛蓝瓷, 森林墨, 牛皮纸, 沙丘.

- Do not introduce custom hex colors, mixed palettes, or ad hoc inline color blocks. Use the selected theme variables only: `--ink`, `--paper`, `--paper-tint`, `--ink-tint`, and `rgba(var(--ink-rgb|--paper-rgb), alpha)`.

- Use layout skeletons from `layouts.md` instead of inventing pages from scratch.

- Match the original guizang effect before local convenience: hero pages, theme backgrounds, image/screenshot slots, and page rhythm matter more than passing a minimal static layout check.

- Keep title, body, and metadata typography distinct.

- Use standard image ratios; do not use odd original screenshot ratios as the layout contract.

- Avoid emoji icons. Use Lucide or clean text labels.



## Style B Rules



- Use the Swiss template from `$CODEX_HOME/skills/guizang-ppt-skill/assets/template-swiss.html`.

- Use one accent color from `themes-swiss.md`.

- The user-facing theme options are: 克莱因蓝, 柠檬黄, 柠檬绿, 安全橙.

- Do not introduce additional accent colors, gradients, shadows, rounded SaaS cards, or arbitrary hex values. Use the selected Swiss theme variables only: `--paper`, `--ink`, `--grey-1`, `--grey-2`, `--grey-3`, `--accent`, and `--accent-on`.

- Body pages must use registered S01-S22 layouts and `data-layout`.

- For smoke tests or "show me the effect", cover the original guizang range: cover, closing, one comparison/timeline page, one structure page, and one image page. Do not replace those with plain three-card layouts.

- Keep everything straight-edged: no gradients, shadows, rounded cards, or decorative SaaS styling.

- Large type should be light; small type must stay readable.

- Every local image should declare a layout image slot.

- Run the Swiss validator before delivery.



## PPTX Mode



When the user needs an actual `.pptx`, use the official `Presentations` plugin. Do not treat the HTML template as the only valid output.



Still apply the same discipline:



- slide manifest first;

- one visual system per deck;

- consistent grid, type scale, accent color, image ratio, and section rhythm;

- screenshot preservation when content matters;

- final preview before delivery.



## What To Report



At the end, briefly state:



- output files;

- visual system used;

- selected theme and whether it was user-selected or recommended;

- whether image2 was used;

- whether the Swiss validator or PPTX preview passed;

- any evidence or formatting limits that remain.
