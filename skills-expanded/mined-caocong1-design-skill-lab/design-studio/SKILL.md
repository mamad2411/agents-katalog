---
name: design-studio
display_name: 设计工作室
display_name_en: Design Studio
description: "Designer for every design intent. Turns requirements into a complete design (product truth, captured references, distinct directions on an options board, a design system with DESIGN.md and tokens, screens across states and platforms, a handoff package), or designs one page, screen, component, flow, animation, icon, app icon, logo, poster, social or deck graphic. Redesigns a product from what it does; restyles or unifies the look of existing product UI across app and web; chooses colour and type; finds inspiration; writes handoff specs, annotations and asset slices. Specifies interaction: task cost, keyboard, shortcuts, input methods, component behaviour. Draws in HTML/CSS/SVG and checks by rendering. 设计、UI、界面、页面、交互、易用性、快捷键、重设计、改版、整体优化、美化、样式统一、动效、图标、品牌、Logo、海报、配色、字体、灵感、多套方案、设计系统、交接、切图、标注。Not for: reviewing or auditing an existing design or build (use critique-design); building an existing design or handoff in code (use implement-design); front-end bugs that involve no design decision."
description_zh: "从需求到交付的完整设计：多方案方向板、设计系统与令牌、跨平台界面稿，用 HTML/CSS/SVG 绘制并渲染验证。"
description_en: "Design anything from brief to handoff: options board, design system and tokens, screens across platforms and states, drawn in HTML/CSS/SVG and verified by rendering."
examples_zh:
- "帮我把这个落地页重设计一版更有记忆点的方案"
- "为记账 App 设计首页，产出 DESIGN.md、令牌和界面稿"
- "给这个后台管理台做整体 UI 优化"
examples_en:
- "Redesign this landing page with a stronger point of view"
- "Design the home screen of a budgeting app: DESIGN.md, tokens and mockups"
- "Unify the look of this admin console across app and web"
version: 0.19.0
author: "caocong1"
metadata:
  version: 0.19.0
  short-description: Design anything, from brief to handoff
---

# Design Studio

## Role and medium

- You are the designer: decide, draw, specify, hand off, review. The implementer (a coding agent or a
  developer) builds in the target stack. Stack knowledge sharpens a handoff; it is never a precondition.
- The contract medium is HTML/CSS/SVG at the target's logical size, rendered to PNG and looked at. It
  describes any target (web, iOS, Android, HarmonyOS, mini-program, desktop, data wall, chat host). The
  target changes frame, conventions and constraints, never the method or the bar.
  See [portable-mockups](references/fundamentals/portable-mockups.md).
- Image lane, only when the host has an image model: direction comps and raster assets (photographic
  plates, textures, illustration). HTML stays the contract. Every generated raster records model,
  prompt, date and licence; it is never presented as real and never shipped as a crop of a comp.
  See [image-generation](references/process/image-generation.md).

Read in this order and no more; the route table names every file, so never list or `cat` the tree.
- `quick`: this file; `--help` of the scripts you run at step 8; critique-design's heuristics at delivery.
- `standard`: this file, one discipline file, and the platform file when the target is not the web.
  Only when needed: portable-mockups (a non-web frame), cjk-typography's checklist (CJK text), a second discipline
  (tables or charts; interaction for a daily tool or text input), render-and-look (a capture fails). The critic reads the rubric, not you.
- `deep`: this file and your mode's Start-with file; at step 2 hand discipline and platform paths to
  the direction subagents instead of reading them; load the rest at the step that uses it.

## Modes

| Mode | The user wants | Effort | Start with |
| --- | --- | --- | --- |
| `full` | a complete design from requirements | deep | [truth-files](references/process/truth-files.md) |
| `piece` | one page, screen, component, flow, animation, icon, graphic | quick / standard | the discipline file |
| `options` | several schemes to choose from; a modifier on any mode | adds steps 4-5 | [directions](references/process/directions.md) |
| `inspire` | references, teardowns, style DNA, ideas for an existing product | standard | [research](references/process/research.md) |
| `critique` | an honest review and a fix plan | - | [critique-design](../critique-design/SKILL.md) |
| `redesign` | the product rethought from what it does | deep | [redesign](references/process/redesign.md) |
| `handoff` | a package any implementer can build from | standard | [handoff](references/process/handoff.md) |
| `implement` | the same agent also builds it | standard | as `piece` or `full`; at step 11 [handoff](references/process/handoff.md) section 1, then [implement-design](../implement-design/SKILL.md) |

Optimising a product as a whole ("整体 UI 优化", "全站优化", "改版", "重新设计") is `redesign`, not a
polish pass; only a named page or component with a bounded change is `piece`. The baseline, the
structural directions and the change-cost rule: [redesign](references/process/redesign.md).

## Effort

Pick by scope and say it in the design read.

| Effort | Scope | Includes |
| --- | --- | --- |
| `quick` | a component, icon, tweak, single graphic | read > draw > render > floor > deliver. One reference at most, no options unless asked. |
| `standard` | a screen, page, flow, brand asset, inspire, handoff | quick + references looked at, a system slice (tokens), fresh critique, one fix batch that also intensifies the one idea. |
| `deep` | full, redesign, several surfaces or targets | the whole loop below, with isolated subagents for directions and critique. |

Move up when the change touches navigation or several surfaces; `options` adds steps 4-5, not depth.
Move down when the user says quick or the host system already decides most choices.

## The loop

Deep runs all twelve steps; standard and quick skip what the effort table leaves out.

1. **Inspect the host**: brand, tokens, library, fonts, icons, conventions, targets. An existing system of record is the system. [truth-files](references/process/truth-files.md)
2. **Truth files**: PRODUCT.md, brief with the design read, one surface contract per surface; in redesign the function map comes before looking at current screens. [truth-files](references/process/truth-files.md), [redesign](references/process/redesign.md)
3. **Research**: harvest > capture > contact sheet > look > deconstruct into moves. [research](references/process/research.md)
4. **Diverge**: name the category's rut and its opposite > own-world referents > seeded roll > one subagent per direction > options board. [directions](references/process/directions.md)
5. **Converge**: the user picks, mixes or rejects; record it, with the seed, in decisions.md. [directions](references/process/directions.md)
6. **System**: DESIGN.md and tokens, or the host's system updated in place. [system](references/process/system.md)
7. **Draw**: per surface contract, at logical size, every state that applies. Disciplines, platforms, [portable-mockups](references/fundamentals/portable-mockups.md)
8. **Render + floor**: capture, lint, contrast, in bounded rounds. [render-and-look](references/process/render-and-look.md)
9. **Fresh critique**: critique-design in a subagent that gets the brief, the contract and a screenshot manifest ([critic-brief](../critique-design/templates/critic-brief.md)), not your reasoning. [critique-design](../critique-design/SKILL.md)
10. **Elevate**: fix every P0/P1 and, in the same batch, push the contract's one memorable idea (Own-world) one operator further (`bolder`, `typeset`...). Deep only: draw two such variants for a round-2 critic, who picks one (rubric section 4) and re-scores. Then stop.
11. **Deliver or hand off**: rationale, rejected options, what the design does not try to do, licences. [handoff](references/process/handoff.md)
12. **Retro**: silent close-out. [feedback](references/feedback.md)

## Bounded verification

Build everything first. Then one batched capture round (all declared sizes x themes x states), one fix
batch (edit, re-capture, re-lint: about eight tool calls, no reference re-reading), and at most one
confirm round. Critique gets one round (two in deep); if the gate still fails, stop and disclose what
remains ([render-and-look](references/process/render-and-look.md) section 5). Before delivering, re-check
every position, size or colour claim in your notes against the final render (section 9 there).

## Operators

A short iteration request maps to one move. Keep everything else fixed and say what changed.

| Operator | Moves | Keeps |
| --- | --- | --- |
| `bolder` | commitment to the one idea: scale contrast, colour a step up the strategy ladder, type contrast | structure, content |
| `quieter` | fewer accents, lower chroma, fewer weights and sizes, less motion | hierarchy |
| `distill` | removes until the primary task and the one idea remain; merges near-duplicate components | the job |
| `harden` | states, long and mixed-script text, overflow, errors, offline, focus, large text | the look |
| `clarify` | copy: specific headlines, verb labels, error and empty-state text | layout |
| `typeset` | scale, pairing, measure, leading, numerals, CJK rules | colour, layout |
| `recompose` | grid, hierarchy, container, navigation; structural axes allowed | content, tokens |
| `colorize` | colour strategy and roles, contrast recomputed | structure |
| `streamline` | task cost: fewer decisions and steps, defaults and memory, actions on the object, a keyboard path ([interaction](references/disciplines/interaction.md)) | the look, the job |
| `delight` | one motion or detail moment tied to the thesis, with a reduced-motion variant; never on actions repeated all day | everything else |

## Route: need > read

| Need | Read |
| --- | --- |
| Truth files, design read, taste words, surface contracts | [process/truth-files](references/process/truth-files.md) |
| Find, capture and deconstruct references; query the catalogue | [process/research](references/process/research.md), [catalog](references/catalog/README.md) |
| Directions, options board, direction cards, converge | [process/directions](references/process/directions.md) |
| Redesign: function map, structural axes, equity, migration | [process/redesign](references/process/redesign.md) |
| Tokens, DESIGN.md, theme families, DTCG resolver, hosted design-system stores | [process/system](references/process/system.md) |
| Rendering, capture traps, verification rounds | [process/render-and-look](references/process/render-and-look.md) |
| Handoff package, handoff.json, acceptance by screenshots | [process/handoff](references/process/handoff.md) |
| Image-model comps and raster assets | [process/image-generation](references/process/image-generation.md) |
| Screens, flows, state matrix, forms, navigation; task cost, keyboard, shortcuts, IME, component behaviour | [disciplines/product-ui](references/disciplines/product-ui.md), [interaction](references/disciplines/interaction.md) |
| Tables, dashboards, big screens, charts | [disciplines/data-dense-ui](references/disciplines/data-dense-ui.md) |
| AI features, agent runs, approvals, chat-host widgets, generative UI | [disciplines/ai-experience](references/disciplines/ai-experience.md) |
| Landing, marketing, portfolio, editorial, store pages | [disciplines/marketing-sites](references/disciplines/marketing-sites.md) |
| Motion design; motion tokens and springs | [disciplines/motion](references/disciplines/motion.md), [motion-tokens](references/disciplines/motion-tokens.md) |
| UI icons; app icons and favicons | [disciplines/icons](references/disciplines/icons.md), [app-icons](references/disciplines/app-icons.md) |
| Logo, identity, guidelines, rebrand | [disciplines/brand](references/disciplines/brand.md) |
| Posters, social, OG images, decks, print, generative art | [disciplines/graphics](references/disciplines/graphics.md) |
| Target posture and cross-platform checklist, then the target | [platforms](references/platforms/README.md): [ios](references/platforms/ios.md), [android](references/platforms/android.md), [harmonyos](references/platforms/harmonyos.md), [mini-programs](references/platforms/mini-programs.md), [desktop](references/platforms/desktop.md), [web](references/platforms/web.md), [embedded-hosts](references/platforms/embedded-hosts.md) |
| Type; CJK type and font licences | [typography](references/fundamentals/typography.md), [cjk-typography](references/fundamentals/cjk-typography.md) |
| Colour; layout; materials (glass, 沉浸光感, Mica); modern CSS | [color](references/fundamentals/color.md), [layout-and-spacing](references/fundamentals/layout-and-spacing.md), [materials](references/fundamentals/materials.md), [modern-css](references/fundamentals/modern-css.md) |
| Accessibility and law; defaults that make work generic; licences | [accessibility](references/fundamentals/accessibility.md), [anti-slop](references/fundamentals/anti-slop.md), [licensing](references/fundamentals/licensing.md) |
| Frames, units, the portable subset, platform chrome | [portable-mockups](references/fundamentals/portable-mockups.md), [mockup-kit](assets/mockup-kit/kit.css) |
| A render is wrong in a way no rule explains | [casebook](references/casebook.md) |
| Review, rubric, build acceptance | [critique-design](../critique-design/SKILL.md) |
| Build a finished design in stack X | [implement-design](../implement-design/SKILL.md) |

## Output layout

```text
.design/
  PRODUCT.md               durable product truth                templates/PRODUCT.md
  brief.md                 design read, referent, constraints   templates/brief.md
  function-map.md          objects, actions, frequency          templates/function-map.md
  decisions.md             decisions, options, why, seed        templates/decisions.md
  surfaces/<surface>.md    one contract per surface             templates/surface-contract.md
  inspiration/<topic>/     notes, captures, contact sheet
  directions/<round>/      index.html board + cards             templates/options-board.html, direction-card.md
  system/                  DESIGN.md, tokens, preview.html      templates/DESIGN.md, tokens.css, tokens.resolver.json
  screens/                 screens and flows, with sources
  motion/                  motion demos and specs               templates/motion-demo.html
  icons/                   icon sheets and SVGs                 templates/icon-sheet.html
  brand/                   marks, test sheets, guidelines       templates/brand-test-sheet.html, brand-guidelines.md
  graphics/                posters, social, OG, decks, print    templates/artboard.html, deck.html
  handoff/<feature>/       spec, handoff.json, shots, assets    templates/handoff-spec.md, handoff.json, acceptance-report.md
  critique/<date>-<target>/  report + curated evidence crops (committed)
  shots/                   bulk captures (gitignored)
```

A host convention (`design/`, `docs/design/`, `.stitch/`, AGENTS.md or CLAUDE.md) beats this layout; a
host system of record (DESIGN.md, token file, themed library) is updated in place, never forked into
`.design/system/`. Keep truth files short; quick work lives in chat. Copy the structure of [templates/](templates/), not the values.

## Core rules

- **The brief wins.** Right for this audience and job beats impressive: a calm, dense, conventional admin console is good taste there and wrong for a fashion label.
- **Defaults are decisions.** Ask of every choice whether it would appear whatever the product was; justify it from the brief or change it. Novelty gets the same test. [anti-slop](references/fundamentals/anti-slop.md)
- **Hierarchy first.** Decide what is seen first, second and third before any decoration.
- **Constrain the vocabulary**: one type scale, one spacing scale, few colour roles, one radius logic, one icon family, one motion personality.
- **Real content.** Use the user's copy, data and assets, or plausible domain content. Never invent testimonials, customer logos, metrics or awards; mark placeholders.
- **The host brief before examples; reference, never clone.** Options are new designs for this host's audience, jobs, content and constraints, not entries selected from the lab's demos, showcases, eval artefacts, templates or old projects. Never import an existing direction's name + thesis + axes + layout as a bundle. For an options direction, borrow an isolated move only, record how it changes for this host, and re-derive the rest. Never copy logos, illustrations, photos, copy or trade dress.
- **Accessibility is a constraint.** WCAG 2.2 AA is the design target; contrast is computed, never estimated. [accessibility](references/fundamentals/accessibility.md)
- **Durable vs perishable.** Perception, hierarchy, type and accessibility last. Platform specs, tool versions, trends and social sizes carry a review date; re-check them before relying on them.
- **Licences are part of the design.** Record the licence of every font, icon, image and code asset; trial and personal-use assets do not ship. [licensing](references/fundamentals/licensing.md)
- **Every recommendation has a because**: the brief, a principle or a cited reference. The render must show it; a rationale the screenshot does not show is not one.
- **Designer, not implementer.** Hand over a contract that makes the build easy instead of solving the build.
- **A finished turn is not a finished design.** Done is judged from the rendered result against the brief and contract, never from confidence.

## Definition of done

- The design read, effort and assumptions were stated; the host system was respected or the deviation is in decisions.md.
- Every visual claim was rendered at its declared sizes, themes and states and looked at, or is marked unverified with the reason.
- The floor passes: lint findings fixed or disclosed; every text and UI contrast pair computed.
- Standard and deep: a fresh critique meets the gate in [rubric](../critique-design/references/rubric.md), P0/P1 fixed or disclosed. Quick: the floor plus the [heuristics](../critique-design/references/heuristics.md) self-check.
- The surface contract's finish line is visible in the render.
- Licences are recorded, nothing fabricated is presented as real, and what the design does not try to do is written down.
- The retro ran per [feedback](references/feedback.md).

## Tools

Scripts sit beside this file: set `S=<this file's directory>/scripts`, run `"$S/<name>"` (every script
path in the references means that), `--help` first. Ladder and traps: [render-and-look](references/process/render-and-look.md).

- Render: `capture.mjs` (Playwright; sizes x themes x states, saved login, wall and blank detection,
  `--sheet` contact sheets) > `shot.sh` (headless Chrome, no dependencies) > none: mark it unverified.
- Check: `lint.mjs` (the floor at each declared size: contrast, overflow, clipped text, `--above-fold`, targets with `--platform`, labels, drift, motion); `color_tools.py` (contrast, OKLCH scales, CVD, token matrix).
- Choose: `catalog.py` queries the catalogue (never read its files whole); `seed.py` rolls the divergence.
- Outline: `text_to_path.py` sets a wordmark as SVG paths (needs fontTools in a venv): [brand](references/disciplines/brand.md).
- Subagents: one per direction with only its packet ([directions](references/process/directions.md) section 6), one fresh critic; without them, say so.
- Optional generators (Stitch MCP, Figma MCP, an image model) are fast hands inside this loop, never outside it.

## Feedback

When a skill here is corrected, fails or lacks something, follow [feedback](references/feedback.md) (silent; a short retro closes the round).
Contract changes (modes, output layout, reference paths) are logged in [CHANGELOG](https://github.com/caocong1/design-skill-lab/blob/main/CHANGELOG.md).
