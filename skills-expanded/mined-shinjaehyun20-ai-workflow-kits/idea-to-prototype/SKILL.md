---
name: idea-to-prototype
description: >
  아이디어 한 줄이나 rough brief, design.md, 기존 화면설계서, 브랜드/소스 자료를
  입력받아 적용하고, 소스가 없으면 기준 소스를 생성한 뒤 opportunity memo,
  source inventory, screen map, prototype brief, build spec, clickable
  prototype scaffold까지 이어주는 아이디어-투-프로토타입 스킬이다.
---

# Idea To Prototype

## Purpose

Turn a rough product idea and any supplied or generated design/source package
into a bounded, inspectable prototype package. The skill should preserve the
intent of the idea, read source materials before inventing UI when they exist,
generate a usable source baseline when they do not, narrow the first wedge,
define the screens before coding, build only the agreed scaffold, and close with
explicit verification evidence.

This is the third plugin in the local product suite after Proposal Workbench and
Meeting Intelligence. It can reuse the same discipline: evidence first, a
storyboard/spec gate before build, and verification before completion.

## Use When

- 사용자가 제품/서비스 아이디어를 던졌고 바로 만져볼 수 있는 프로토타입이 필요하다.
- 사용자가 `design.md`, 화면설계서, 기존 산출물, URL, 이미지, 브랜드 가이드 같은
  소스를 주고 그것을 프로토타입에 반영해야 한다.
- 사용자가 별도 소스를 주지 않았지만, 프로토타입을 만들기 전에 재사용 가능한
  디자인/콘텐츠/화면 기준 소스를 먼저 생성해야 한다.
- 코드를 만들기 전에 화면 흐름, 기능 범위, 검수 기준을 고정해야 한다.
- 제안/세일즈용 working prototype scaffold가 빠르게 필요하다.
- A one-day or short-cycle MVP needs a clear product memo, screen map, and
  build-ready prototype brief.

## Inputs To Capture

- Raw idea or rough brief.
- Target user and painful job.
- One promise the prototype must prove.
- Non-goals for the first version.
- Preferred platform: web app, mobile web, large-screen page, or deck-style working prototype.
- Any source evidence, examples, brand constraints, or existing files.
- Source inputs to apply: `design.md`, `DESIGN.md`, screen specs, PPTX/PDF/DOCX,
  screenshots, Figma/exported specs, brand guides, official URLs, existing
  prototypes, or prior local output folders.
- Source authority: which files are hard constraints, which are reference-only,
  and which are examples or inspiration.
- Known source conflicts, stale files, or screens that must not be reused.
- If no source is supplied, infer enough to generate a reusable baseline source:
  domain assumptions, target platform, tone, visual direction, component set,
  content model, and workflow evidence that still need validation.
- Output location, if the user has already specified one.

## Workflow

1. Clarify product wedge: target user, painful job, one promise, non-goals, and
   first release success criteria.
2. Choose a source mode before writing UI:
   - `provided-source mode`: when the user gives `design.md`, specs, URLs,
     screenshots, existing prototypes, or source folders, locate/read them,
     extract constraints, decide authority, and create `00b_source_inventory.md`.
   - `generated-source mode`: when no source is supplied, create
     `00c_generated_source.md` first, then list it as a generated hard/soft
     source in `00b_source_inventory.md`.
3. Apply `design.md`, supplied sources, or `00c_generated_source.md` into
   `03_design_contract.md`:
   tokens, layout rules, components, states, content style, naming rules, and
   explicit do-not-use constraints must be carried forward before coding.
4. Run the anti-generic gate before writing UI: name why this product cannot be
   served by a stock landing page, generic dashboard, or prior prototype shell.
5. Create opportunity memo: buyer/user, problem, offer, differentiator, proof,
   risk, and optional pricing hypothesis.
6. Build screen map: entry screen, primary workflow, secondary screens, states,
   empty/error/success paths, navigation rules, and the source IDs behind each
   screen or component.
7. Write prototype brief: visual tone, content model, components,
   interactions, data needed, release constraints, and source-derived states.
8. Write `03_design_contract.md`: tokens, layout constraints, states, content
   rules, source assumptions, and a source-to-design mapping.
9. Produce build spec: routes, data model, local fixtures, API candidates,
   acceptance criteria, source application tasks, and verification checklist.
10. Scaffold the clickable prototype only after the source inventory, screen map,
   brief, and design
   contract are stable enough to code without inventing the product during
   implementation.
11. Verify the result: open or render the prototype, check navigation, text fit,
   responsive layout, empty/error/success states, screen/spec round-trip,
   source/design conformance, and product-specific differentiation.

## Source Modes

Use the most convenient path for the user:

- If source exists, accept it and apply it. Do not ask the user to reformat it
  unless it cannot be read.
- If source is missing, generate it. Do not stop at a request for `design.md`.
  Create a compact but reusable baseline source package and continue.
- If partial source exists, apply the provided source and generate only the
  missing pieces as a supplement.

### Provided-Source Mode

Use this mode when the user provides or references source material.

- Resolve local paths from the current workspace first, then from the user's
  provided absolute paths. Do not guess with similarly named files when the user
  named a specific source.
- Read text sources directly. For PPTX/PDF/DOCX/HWPX or spreadsheets, use the
  available structured extraction path or a focused file parser; do not rely on
  filenames alone.
- For URLs, browse and cite current pages before using their claims or visual
  patterns. For images, inspect them before treating them as design guidance.
- Create `00b_source_inventory.md` with a table of source ID, path or URL, type,
  authority (`hard`, `soft`, `reference`, `generated-hard`, `generated-soft`,
  `stale/avoid`), extracted constraints, affected screens/components, and
  unresolved gaps.
- If `design.md`, `DESIGN.md`, or an equivalent design guideline exists, parse
  it into these buckets: tokens, typography, spacing, layout, components,
  interaction states, content rules, accessibility rules, and forbidden patterns.
- Carry those buckets into `03_design_contract.md`. The design contract must
  state which source ID supports each major visual or interaction decision.
- If sources conflict, prefer explicit user direction, then current project
  design/source files, then official/current sources, then older references.
  Record the conflict and decision in `00b_source_inventory.md`.
- Do not treat a source as applied unless it appears in the screen map, design
  contract, build spec, prototype implementation, and verification notes.

### Generated-Source Mode

Use this mode when the user gives only an idea, rough brief, budget/timeline, or
target audience without source files.

- Create `00c_generated_source.md` before the screen map. Treat it as the
  temporary design/source baseline for the prototype.
- Include these sections in `00c_generated_source.md`:
  - Source mode and assumptions.
  - Product/domain interpretation.
  - Target platform and viewport assumptions.
  - Visual direction and tone.
  - Design tokens: color roles, typography scale, spacing, radius, elevation.
  - Component rules: navigation, cards/panels, forms, buttons, status, dialogs,
    bottom sheets, empty/error/success states.
  - Content model: primary entities, fields, example data, labels, CTAs.
  - Primary workflow and required screens.
  - Accessibility and responsive rules.
  - Anti-generic differentiation rules.
  - Open questions and validation gaps.
- Add `00c_generated_source.md` to `00b_source_inventory.md` with authority
  `generated-hard` for decisions needed to build the prototype and
  `generated-soft` for assumptions that need later confirmation.
- Carry generated tokens/components/screens into `03_design_contract.md`.
- In `05_verification.md`, state that the prototype used generated source
  because no external source was supplied, and list which assumptions must be
  replaced when real source arrives.

## Outputs

Use the user's requested location. If no location is specified and files are
needed, ask once before creating a new package folder.

- `00_opportunity_memo.md`
- `00a_anti_generic_gate.md`
- `00b_source_inventory.md`
- `00c_generated_source.md` when no source is supplied or when source gaps are
  filled by generated supplemental guidance
- `01_screen_map.md`
- `02_prototype_brief.md`
- `03_design_contract.md`
- `04_build_spec.md`
- `prototype/`
- `05_verification.md`

## Prototype Defaults

- Build the usable prototype as the first screen; do not start with a marketing
  landing page unless the requested product is specifically a landing page.
- If the requested product is a website or landing page, it still needs a
  product-specific conversion mechanism, content model, and visual proof. A
  hero, cards, generic metrics, and a contact form are not enough.
- Prefer the existing app/framework in the workspace when one exists.
- For a new web prototype, choose the smallest maintainable stack that can be
  run and inspected locally.
- Use realistic sample data instead of lorem ipsum when the domain is known.
- Keep controls, navigation, empty states, and success/error feedback complete
  enough for the working prototype workflow.

## Anti-Generic Gate

Before coding, create `00a_anti_generic_gate.md` and answer these checks:

- What is the domain-specific job the prototype must perform?
- Which visible modules would be impossible or awkward in a generic template?
- Which user decision does each module help make?
- What budget, timeline, or business constraint changes the scope?
- What prior or similar local outputs were checked, and what will be different?
- Which source files or URLs constrain the design, and where will they be
  applied?
- If no source was supplied, what generated source baseline will keep the
  prototype from becoming generic?
- What asset quality is required, and which placeholder assets must be replaced
  before public delivery?
- What would make the result fail even if the HTML renders successfully?

For a high-budget or premium request, add at least one conversion or operations
module beyond basic marketing content, such as package configurator, intake
triage, quote builder, schedule lane, concierge flow, before/after proof system,
or ROI/value planner.

## Verification Checklist

- Confirm every expected output file or folder exists.
- Confirm `00b_source_inventory.md` exists and every hard source has a visible
  application target or an explicit unresolved-risk entry.
- If no source was supplied, confirm `00c_generated_source.md` exists and is
  mapped into `03_design_contract.md`, `04_build_spec.md`, and the prototype.
- Parse or build the prototype project when applicable.
- Open/render the prototype and inspect the primary workflow.
- Check mobile and large-screen layouts when the prototype is web-based.
- Compare `03_design_contract.md` against the supplied `design.md` or equivalent
  design source and list any intentional deviations.
- If generated-source mode was used, compare `03_design_contract.md` and the
  prototype against `00c_generated_source.md`.
- Compare the rendered result against `00a_anti_generic_gate.md` and fail if it
  could be swapped with another industry by changing only copy and images.
- Compare the rendered result against `00b_source_inventory.md`; fail if hard
  source constraints were ignored, reduced to prose only, or not visible in the
  prototype.
- For visual work, inspect screenshots and reject stock-like, irrelevant, blank,
  low-quality, or misleading primary assets.
- Record the exact commands, paths, and observed result in
  `05_verification.md`.
- List unresolved risks instead of treating assumptions as completed work.

## Stop Rules

- Do not jump from idea directly to code when the screen map is undefined.
- Do not jump to code when supplied source files, URLs, or `design.md` have not
  been read and summarized into `00b_source_inventory.md`.
- Do not stop just because the user did not provide source. Generate
  `00c_generated_source.md`, mark assumptions clearly, and continue.
- Do not make a landing page when the user asked for a usable prototype.
- Do not call a prototype complete if it only has hero text, generic cards,
  generic process steps, and a form.
- Do not claim a design source was applied just because it was listed. It must
  be mapped to tokens/components/screens and checked in verification.
- Do not claim prototype completion without opening or rendering it.
- Do not accept screenshot existence as visual quality. Inspect it and repair
  obvious template-like or off-domain results.
- Do not invent external evidence. If market, pricing, compliance, or competitor
  claims matter, collect or cite evidence before using them.
- Do not overwrite existing user files. Append, copy, or ask when a write would
  replace prior work.
