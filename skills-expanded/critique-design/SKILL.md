---
name: critique-design
display_name: 设计评审
display_name_en: Design Critique
description: "Reviews, audits and scores an existing design or build like a senior design lead: a site, app screen, flow, component, brand asset, deck or graphic, from screenshots, a URL, mockups or a Figma export. Judges the render against the brief first, then checks the mechanical floor (computed contrast, overflow, targets, focus, states), and returns ranked findings (severity and evidence basis, Before | After | Why), rubric scores and a disposition: ship, fix, rebuild or recapture. Also the fresh-context critic for design-studio's own work, accessibility (WCAG 2.2) audits, and design QA that accepts a build against its handoff screenshots. 评审、设计评审、走查、体验走查、验收、设计验收、还原度检查、哪里不好、这个页面哪里不好看、无障碍检查、设计 QA、打分。Not for: making a new design or redesigning one (use design-studio); building or fixing a design in code (use implement-design); code review with no visual question."
description_zh: "像资深设计负责人一样评审现有设计或构建：按严重性分级输出问题清单、评分与处置建议，或按交接截图做构建验收。"
description_en: "Senior design-lead review of an existing design or build: ranked findings, rubric scores and a ship/fix/rebuild disposition, plus build acceptance against handoff shots."
examples_zh:
- "评审这个页面哪里不好看"
- "对这个改版后的首页做体验走查"
- "对比设计稿和线上页面，做还原度验收"
examples_en:
- "Review this screen and tell me what's wrong"
- "Run an accessibility audit on this checkout flow"
- "Accept this build against its handoff screenshots"
version: 0.4.1
author: "caocong1"
metadata:
  version: 0.4.1
  short-description: Fresh-eye design review, scoring and build acceptance
---

# Critique Design

Findings first; praise and summary after. A finding says what is wrong, where, why it matters to the
user or the business, and what to do, with evidence someone else can check. Judge the rendered result
against the brief and the surface contract. The author's intent is not evidence.

## Modes

| Mode | Use when | Input | Output |
| --- | --- | --- | --- |
| `review` | someone's product, site, screen, brand asset or deck | URL, files or shots; capture the rest | report and fix plan |
| `fresh` | design-studio (loop step 9) spawned you as its critic | a [critic brief](templates/critic-brief.md) | report, disposition first |
| `self-check` | the author checks their own work | your own renders | quick effort: floor + ★ [heuristics](references/heuristics.md); otherwise the full report, single-context |
| `acceptance` (was `qa`) | a build is compared with its handoff shots | handoff + build shots, often via a critic brief | acceptance report |
| `redesign-brief` | findings will feed a redesign | as `review` | report + structural findings |

Prefer a fresh subagent even for your own work: authors over-rate what they made. In `self-check`,
write Track A before opening any tool output; the report starts `Method: single-context (<reason>)`.
`redesign-brief` weighs structure ([heuristics](references/heuristics.md) section 2) as heavily as
detail: detail fixes become every direction's baseline, and equity is what users rely on (learned
locations, shortcuts, scanned data), not the layout. Findings feed [redesign](../design-studio/references/process/redesign.md).

## Two tracks, in this order

**Track A: judgement, in a fresh context.** It gets the brief (and PRODUCT.md), the surface
contract, a screenshot manifest and the [rubric](references/rubric.md). It does not get the
conversation, the reasoning in decisions.md, drafts, rejected options or the author's
self-assessment. Decide what you see before any number anchors you.

**Track B: mechanical evidence**, opened only after Track A is written. In
`../design-studio/scripts/` (run each with `--help` first): `lint.mjs` (the deterministic floor on a
rendered page), `color_tools.py` (`contrast`, `matrix --from tokens.css`, `cvd` for charts and status
sets), `capture.mjs` (sizes x themes x states; non-zero exit on walls, blanks, errors), `shot.sh`
(fallback). Installed alone: use what the host has (computed styles, axe, a contrast calculator) and
name it. B wins on what it measures; A stands on what B cannot measure. Record agreements, what only
B caught, and B's false positives. Floor items no tool checked are `not verified`: not passed.

## Procedure

1. **Check the evidence.** Open every file: right route, fully loaded (no spinner, wall or error
   page), intended font, declared size, theme, state and build stamp. Recapture a bad file yourself
   (step 2); if you cannot, the disposition is `recapture`: list what to capture and stop.
2. **Capture what is missing** at the declared sizes and themes (defaults, traps:
   [render-and-look](../design-studio/references/process/render-and-look.md)), in every state you can
   trigger: focus by tabbing, hover, error, empty, loading, longest content, 200% zoom, reduced motion.
   Walk the primary task. Never judge from code alone or one shot; with code, cite the cause's `file:line`.
3. **State the yardstick** from the brief: audience, job, attributes, platform, constraints. With no
   brief, infer the design read and label it inferred. Note what works; the fix plan keeps it. Brand
   work: `.design/brand/strategy.md` and the tests in [brand](../design-studio/references/disciplines/brand.md) section 4.
4. **Coverage pass (Track A).** Walk the [heuristics](references/heuristics.md) in order; run two or
   three personas. Then **rationale against render**: for each contract block (thesis, own-world,
   story, first viewport, form, finish line) and each claim in the critic brief, name the shot and
   region that delivers it: `kept`, `partial` or `missing`. A rationale the render does not show is
   design theater; partial and missing are findings. Write down every candidate; do not filter.
5. **Track B.** Run or open the mechanical evidence and merge it with Track A.
6. **Vet pass.** Re-open every cited location (shot region, selector, `file:line`) before a candidate
   becomes a finding. Drop false positives, fix wrong locations, merge repeats into one systemic
   finding, then grade it. Keep a one-line reason for each rejected candidate.
7. **Score** with the [rubric](references/rubric.md): floor, then ceiling, then the gate.
8. **Decide, crop, report**: disposition, one crop per finding, [report](templates/critique-report.md).

## Personas: pick two or three, walk the primary task as each, name the element that broke

| Persona | Probes | Pick for |
| --- | --- | --- |
| Power user | task cost of the top jobs, keyboard path and shortcuts, bulk actions, skippable steps, slow motion | admin, data-dense, daily tools |
| First-timer | first action clear within 5 s, unlabelled icons, jargon, proof of success | onboarding, landing, forms |
| AT user | keyboard-only path, focus visible and unobscured, names, colour-only meaning, 200% zoom | every product surface |
| Stress tester | 0, 1 and 1,000 items, longest strings, mixed scripts, errors, refresh mid-flow | tables, forms, checkout |
| Distracted mobile | thumb reach, interrupt and resume, slow network, less typing | consumer mobile, mini-programs |

## Grading findings

| Severity | Meaning |
| --- | --- |
| `P0` | blocks the primary task; excludes users on a core path; legal exposure (unlicensed asset, fabricated claim, a required AI label missing); risk of data loss |
| `P1` | major damage to comprehension, trust or conversion; systemic inconsistency; missing core states; unmet finish line. Would a user contact support? Then at least P1 |
| `P2` | noticeable polish or consistency problems; minor friction with a workaround |
| `P3` | nits and opportunities |

| Evidence basis | Meaning |
| --- | --- |
| `verified` | measured, or visible in a named crop; anyone can re-check it |
| `needs confirmation` | inferred from a still (hover, keyboard, motion, a likely consequence); say what would confirm it |
| `human-required` | only a person can settle it: real assistive-technology use, licence or trademark clearance, user research, truth of content |

Also tag effort (`S`/`M`/`L`) and type: `quick win`, `systemic` (fix once in tokens or components),
`structural` (needs a redesign). Word evidence as evidence ("当前页面显示…"), inference as inference ("这可能导致…").

## Dispositions and rounds

| Disposition | When |
| --- | --- |
| `ship` | the floor passes, the rubric gate holds, no P0 or P1 is open |
| `fix` | direction and structure hold; give at most eight material fixes, in order |
| `rebuild` | structure or direction fails (Fit or Hierarchy at 2 or below, or the thesis is not delivered); fixes cannot reach the gate |
| `recapture` | evidence is missing or invalid; no verdict on the design |

At most two rounds. Round 2 re-checks each round-1 finding against its own evidence shot, re-captured
at the same size, theme and state: `resolved`, `partial` or `unresolved`, plus at most three
regressions. Partial or unresolved never adds up to `ship`. After round 2, disclose what remains.

## Accepting a build (`acceptance`)

Only screenshots of the build count, from any source (browser, simulator, device, golden test, a
paste). With none, acceptance has not happened: say so.

1. Pair each handoff shot (`shots` in handoff.json) with a build shot at the same logical size, DPR,
   theme, state and content, carrying the build stamp. A mismatched pair is `recapture`.
2. Compare region by region: the named components of the spec's structure tree (`data-component` in
   the mockup), side by side, then overlaid (render-and-look section 8). Per region: `match`,
   `adapted`, `missing`, `contradicted` or `added`, with a crop. Spacing, type (face, size, weight,
   line height, tracking), colour tokens, radii, borders, shadows, each asset in its slot at its
   rendered size, content; then states, other sizes, motion. Tolerances: the spec's Acceptance
   section (default: one spacing step, exact tokens, fonts as specified). Anti-aliasing is noise.
3. Each deviation: `expected -> actual`, screen > component, crop, severity, one class: **build bug**
   (differs from a clear spec: fix the build), **spec gap** (the handoff did not say: fix the
   handoff, never guess), **platform difference** (a system component or font renders differently:
   usually accept, record it in the spec).
4. Say how each thing a still cannot show was checked (targets, focus order and visibility,
   screen-reader names, contrast, text scaling, reduced motion), then fill the
   [acceptance report](../design-studio/templates/acceptance-report.md). `ship` needs every region
   `match` or `adapted` and no open P0 or P1; a region is fixed only on a re-captured build shot.

## Conduct

- Judge the work against the goal, never the person; be direct. Prefer the smallest fix that works.
- Ten findings that matter beat forty. Scores track change, never people. Write in the user's language.
- Never rewrite an issued finding to match what was built. The implementer answers it: fixed, with
  the re-captured evidence shot (same size, theme and state), or a deviation recorded in decisions.md.

## Output

`.design/critique/<date>-<target>/`: `report.md` plus one crop per finding (`NN-<slug>.png`, enough
context to locate it), committed; bulk captures stay in `.design/shots/` (gitignored). Acceptance
writes `.design/handoff/<feature>/acceptance.md`. The last report on the same target is the baseline
for score changes. Quick work: the table in chat.

## Feedback

When this skill is corrected, fails or lacks something, follow design-studio's
[feedback](../design-studio/references/feedback.md): silent, lab inbox only, short retro.
