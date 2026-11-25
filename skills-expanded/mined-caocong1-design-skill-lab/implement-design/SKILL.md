---
name: implement-design
display_name: 设计实现
display_name_en: Implement Design
description: "Use when a design, handoff package or mockup already exists and must be built in a specific stack: a .design/handoff package, HTML/CSS mockup, Figma frame, approved PNG, or specs and tokens turned into code in the host project (React, Next, Vue, Nuxt, Tailwind, Ant Design, Element Plus, uni-app, Flutter, SwiftUI, Compose, ArkUI, mini-programs, Electron, Tauri, WinUI), or a build fixed until it matches its design. Lands tokens in the host theme, builds every state, proves fidelity with build screenshots, acceptance and visual-regression baselines. 按设计稿实现、照设计图开发、设计稿还原、还原度修正、交接包落地、静态稿接入项目。Not for: deciding or improving what the design should be, UI polish, 整体优化, design-then-build from scratch, 切图/标注 or dev specs (use design-studio); reviews or acceptance reports without fixing (use critique-design); CSS refactors, front-end bugs or single property edits with no design to match."
description_zh: "把已有设计稿、交接包或 Figma 高保真落地为宿主项目代码：令牌进主题、状态全可达，用构建截图证明还原度。"
description_en: "Build an existing design, handoff package or Figma frame faithfully in the host stack: tokens into the theme, every state reachable, fidelity proven with build screenshots."
examples_zh:
- "按这份交接包在我的 React 项目里实现"
- "把这个 Figma 页面还原成 Vue 组件"
- "修复线上页面和设计稿的还原度偏差"
examples_en:
- "Implement this handoff package in my React project"
- "Rebuild this Figma screen as a Vue component"
- "Fix the fidelity drift between this build and its design shots"
version: 0.4.0
author: "caocong1"
metadata:
  version: 0.4.0
  short-description: Build an existing design in code, verified by screenshots
---

# Implement Design

You are the implementer. A design already exists; build it faithfully in the host project and prove
the fidelity by looking. You do not redesign. When the design is missing, ambiguous or wrong for the
platform, report a spec gap: design decisions go back to the designer ([design-studio](../design-studio/SKILL.md)).

This file works alone. [stacks](references/stacks.md) adds per-stack token homes, native primitives,
system components, platform APIs and screenshot tooling; read only your stack's section.

## 0. What you were given

| Input | Treat as | Read first |
| --- | --- | --- |
| Handoff package `.design/handoff/<feature>/` ([format](../design-studio/references/process/handoff.md)) | the contract | README.md (spec and build plan), handoff.json (shots, assets, motion), then the mockups |
| design-studio `implement` mode (you designed it too) | shots + tokens are the contract | `.design/system/` tokens, `.design/screens/`; write the screen x state x target x theme list yourself |
| HTML/CSS mockup | structure + tokens | `:root` tokens; flex rows and columns = widget tree; `data-component` / `data-state` = components and variants |
| Figma frame (Figma MCP) | design context + visual target | variables, components, Code Connect mappings; the screenshot is the target, never an asset |
| Approved PNG or screenshot | visual target only | extract the system first (section 2) |
| An existing build that drifted from its design (还原度) | the design shots are the contract | capture the build first (section 4), list `expected > actual`, then fix |
| Words only, or "make it nicer" | not this skill | design-studio |

A README Build plan runs step by step: every Verify command against its expected output, a stop at
every STOP condition. Missing screens, states, targets or tokens beyond a detail: ask, or hand back to
design-studio. Build what is specified, list every guess as a spec gap, never improvise a look.

## 1. Inspect the host

Before writing code, establish and note in a few lines:

- Framework, version, rendering model. Read the lockfile and code against the installed major. An
  API, prop or token you cannot find in the installed source is not used.
- The styling system (utility CSS, CSS modules, preprocessor, CSS-in-JS, the kit's theme API). Use it;
  never add a second one.
- Where tokens live; breakpoints; dark-mode and density mechanism; component library and which
  components exist; icon family; fonts and how they load; i18n and RTL; image pipeline; browser matrix.
- Conventions (file layout, naming, lint, previews, screenshot tests) and three similar existing
  screens or components. Follow their patterns for state, data, file layout and tests.
- A new dependency (motion library, icon pack, UI kit) needs a reason the stack cannot meet. Name it.

## 2. Land the tokens

- Tokens go into the host's source of truth (theme object, CSS variables, Tailwind `@theme`,
  `ThemeData`, asset catalogue, `resources/*/element/*.json`): one source, modes as re-mappings of
  semantic tokens.
- Keep a mapping, design token > host token > value, marked new or existing. It ships with the work.
- No raw hex, px, ms or z-index in components where a token exists. A missing token is added to the
  system, not inlined.
- Design and system disagree (13 px body, system 14): do not fork. The design adopts the system value
  or the system changes for everyone; ask the owner, record the answer in the handoff's open questions.
- From an image: extract grid, spacing, type sizes, colour roles and radii; snap to the nearest host
  token and list the snaps. Identify fonts; unavailable or unlicensed: the closest licensed face, said.

## 3. Build

Order: tokens > layout primitives > components with every state > composition > real data and edge
content > motion > accessibility pass > targets and breakpoints pass.

- Follow the spec's structure. Parts marked SYSTEM use the platform's component (navigation bar, tab
  bar, sheet, picker, switch); never rebuild native chrome from the drawing. Units carry one-to-one:
  1 px = 1 pt / dp / vp, 2 rpx at 375 wide ([portable-mockups](../design-studio/references/fundamentals/portable-mockups.md)).
- States are code paths: loading, empty, error, disabled, long content, offline. Make each reachable
  (story, fixture, query parameter, preview) under the handoff's state names, so it can be captured.
- Semantics first: headings, landmarks, lists, buttons vs links, labelled inputs, names for icon-only
  controls; a keyboard path and visible focus for everything interactive.
- Text survives: longest strings, mixed CJK/Latin, 200% zoom or the largest text setting, locale
  formats through the platform formatter. No fixed heights on text containers.
- Images: size reserved, responsive sources, modern formats, alt text. Icons: the one family, SVG with
  `currentColor` or the platform's symbols.
- Motion from the motion tokens (spring, or duration + easing), `transform` and `opacity` first,
  interruptible, the spec's reduced-motion variant, nothing blocking input.
- Glass and blur come from the platform API ([stacks](references/stacks.md)). An effect with no cheap
  native equivalent uses the fallback the handoff names; otherwise ask.
- Assets: check every visible asset in its slot, at its call site, at rendered size; one substituted
  asset fails acceptance. Licence files travel with fonts and assets. No trial fonts, no crop of a
  comp, no screenshot used as an image.
- Someone else's product as input: rebuild structure and behaviour, never logos, copy or trade dress.

## 4. Verify by looking

Build everything first; then one batched capture round, one fix batch, at most one confirm round.

1. Run the app, preview or simulator. Capture every row of the handoff's shot list at the same size,
   scale, theme, state and content into `.design/handoff/<feature>/build/`, named like the design shots
   (`<screen>-<state>-<target>-<theme>.png`); stamp the build and check the stamp in every shot. Web:
   `../design-studio/scripts/capture.mjs --name <screen> --viewports <target WxH>`, renamed as [handoff](../design-studio/references/process/handoff.md)
   section 3 shows; else `shot.sh` or the project's Playwright; native: simulator, goldens or an offscreen render ([stacks](references/stacks.md)).
2. Open every file: right screen, fully loaded, the state its name claims.
3. Compare side by side, then overlaid (recipe: [render-and-look](../design-studio/references/process/render-and-look.md)
   section 8). List deviations as `expected > actual`. A screen with no design shot of its own is
   compared with the drawn screen of its family, control by control ([heuristics](../critique-design/references/heuristics.md)
   section 6); a family with no drawn screen goes back to the designer before it is built (exception: [handoff](../design-studio/references/process/handoff.md) section 1).
4. Run the mechanical checks: grep the changed files for raw colour and size literals (none where a
   token exists); web: `../design-studio/scripts/lint.mjs` on the running page.
5. Fix in one batch. A finding is fixed only when its own evidence shot, re-captured at the same size,
   theme and state, shows it fixed.
6. Check what a still cannot show: focus order and visibility, target sizes, screen-reader names on the
   primary flow, text scaling, reduced motion, computed contrast (`../design-studio/scripts/color_tools.py`).

Then disclose what remains. Cannot render? Say what was not verified; never claim fidelity from code.

## 5. Acceptance

Acceptance belongs to [critique-design](../critique-design/SKILL.md), mode `acceptance`. You run it;
you do not grade yourself.

- `quick` (one component, a bounded fidelity fix): section 4's comparison is the acceptance; list the shots.
- `standard` and up (a screen, flow or feature): spawn a fresh critic subagent with a
  [critic brief](../critique-design/templates/critic-brief.md) set to mode `acceptance`: handoff
  README, handoff.json, design shots, build shots, build stamp. Not your reasoning.
- The critic writes `.design/handoff/<feature>/acceptance.md` ([template](../design-studio/templates/acceptance-report.md))
  and puts evidence crops in `.design/critique/<date>-<target>/`.
- Per deviation: **build bug** > fix and re-capture that row; **spec gap** > report to the designer,
  do not improvise; **platform difference** > usually accept, and record it.
- Issued findings are never rewritten. Answer each: fixed (with the re-captured shot), or a deviation
  recorded in decisions.md with the reason.
- No subagents: re-read only the handoff and the shots, run it yourself, and say it was single-context.

## 6. Make fidelity durable

Add or update visual-regression coverage in the project's own tooling (browser screenshot assertions,
Storybook snapshots, Flutter goldens, Compose or iOS snapshot tests). Baselines come from the accepted
build at the handoff's sizes, themes and states, fonts loaded, motion settled: the gate against drift.

## Rules

- Build exactly what the design shows. Add no colours, shadows, gradients, animations, badges or
  sections it does not have; a missing detail is a spec gap, not an invitation.
- Theme API first: no `!important` or deep selectors over a component library; no magic numbers,
  one-off colours or z-index wars. No second icon family, date or motion library "just for this page".
- No unrelated refactors or "improvements". A design change you believe in goes to the designer as a proposal.
- Do not deviate silently. If the design looks wrong, build it as specified and raise it, or ask first.
- A build that is wrong in a way no rule explains: [casebook](../design-studio/references/casebook.md).

## Deliverables

Code in the host's conventions · token mapping · reachable states · build shots beside design shots ·
acceptance report · visual baselines · deviations, spec gaps, platform differences, unverified areas.

## Feedback

When this skill is corrected, fails or lacks something, follow [feedback](../design-studio/references/feedback.md):
it writes to the lab inbox only when that resolves, silently, and closes with a short retro.
