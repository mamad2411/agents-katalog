---
name: frontend-stack
description: Router for the frontend design stack. Use at the start of any frontend UI task (build a page or component, a settings or preferences area for a web app, desktop app, CLI or TUI, redesign or restyle an app, "it looks ugly / generic / AI-made", migrate to a component library or design system, pick a style or palette, polish, audit, animate, review UI) to decide which installed skills lead each phase of the work, which ones support, and which rule wins when the packs disagree. Also use when two design skills give contradicting advice. Points to the companion indie dev stack when the request is about the product or business rather than the UI.
---

# Frontend Stack router

Several design packs are installed side by side. Each is good alone and each
assumes it is the only one in the room. This skill decides who leads in each
phase of the work, so the agent loads one lead and at most two supporting
skills at a time instead of five competing rulebooks.

`frontend-design:frontend-design` is the base. Load it first on every frontend
task, whoever leads, and keep it loaded. It sits outside the lead/support count
in step 7. If it is not in the session's skill list, say so once and go on.

## 1. Read the project first

Before picking anything, look for what the project already decided:

- `PRODUCT.md` / `DESIGN.md` at the repo root (Impeccable's context files)
- `design-system/*/MASTER.md` (UI UX Pro Max `--persist` output)
- `docs/brand-guidelines.md`, `assets/design-tokens.*` (UI UX Pro Max `brand`
  and `design-system`)
- an existing design system: tokens, `tailwind.config.*`, `components/ui/`, a
  component library in `package.json`
- a brand guide the user pointed at

If any of these exist, follow them by default (rules 1 and 2 of the precedence
ladder). A personality, identity or "looks AI-made" complaint authorizes a
replacement visual world within the complaint's scope, even with `DESIGN.md`.

Keep one source of truth. If two of these files exist and disagree (palette,
fonts, spacing), ask the user which one wins before writing code. When the
project has none, use the identity flow below for a new brand, or Impeccable
`document` to capture an established world. `DESIGN.md` is the source of truth;
do not also run `--persist` or generate `docs/brand-guidelines.md` unless the
user asks, and if they do, keep the values identical to `DESIGN.md`.

## 2. Classify the request

Answer three questions before picking skills:

1. **Job.** Build something new; change something that exists (redesign,
   restyle, migrate to a library); review only (critique, audit, polish); one
   craft (motion, copy, color, type, layout, tokens); or assets (brand, logo,
   banners, slides).
2. **Surface.** Marketing (landing, portfolio, site); product (dashboard, chat,
   forms, settings, tables, flows); a single component; mobile web; native app.
3. **Stack signals** from step 1: a component library in `package.json`, shadcn
   (`components.json`, `components/ui/`), Tailwind, React Native/Expo, Swift.

Complaints about looks ("ugly", "generic", "looks AI-made", "slop", "cluttered")
mean the job is *change*, not *review*: the user wants a new direction, not only
a list of problems. An explicit review-only request stays read-only, even when
it names an identity failure.

### Vague complaint: ask before loading

A complaint is vague when it names no concrete problem, no "what" is wrong
("your site is still bad", "this screen is ugly", "the UX is not good",
"improve the identity"). A known target ("this screen", a named page) does not
make it concrete: it only skips the "where" question. A broad word (UX, usability,
experience, design, identity, navigation) is still vague, but it picks a base
path. Then do the basics only:

1. Load `frontend-design:frontend-design` and nothing else. Read the project
   (step 1) and the conversation: "still" means an earlier round failed, so
   find what that round changed.
2. Pick the base path in [base-paths.md](references/base-paths.md) from the
   complaint's words: UX, navigation, reading and hierarchy, flows and forms,
   starting or improving an identity, looks, copy, mobile, settings. No area named:
   the first question asks which one.
3. If a browser or screenshot tool is at hand and the app runs, look at the
   current render of the page the user most likely means, to ground the
   questions. What you saw in the code or the render only shapes the
   options; do not list problems yet.
4. Ask the path's questions in one message, with the question tool when the
   session has one: at most four, each with options. Skip what the context
   answers ("this screen" with a screenshot, an open URL or the last page
   changed). If an earlier round failed, ask what in it missed.
5. Wait for the answers. Route each answer as its path says; several answers
   become phases (step 3).

Before the answers: no critique, list of problems found, direction,
prototype, recommendation or other skill load. Describe the project in one
neutral line (what pages exist), not what is wrong with them. If the user declines to answer or says "you decide", follow
the path's fallback, or the shared one in base-paths.md; on the looks path or with no area named, treat it as
a looks complaint about the main page and run the gate in step 3.

## 3. Work in phases

Bigger tasks run in phases, in this order. Load each phase's skills when the
phase starts, not all up front. Skip a phase that the task does not need.

| Phase | When | Lead | Support |
|---|---|---|---|
| Diagnose | the job is *change* | `impeccable:impeccable` (`critique`) | `impeccable:impeccable` (`audit`) for a11y/perf debt |
| Direction | new work, or any complaint about looks | identity flow below when the product has no brand or its identity is being replaced; otherwise product: `frontend-design:frontend-design`, marketing: `taste:design-taste-frontend` | reference research before directions; `ui-ux-pro-max:ui-ux-pro-max` loaded at the start for UX and stack rules, its styles and presets only after the concept |
| Build | always | the project's component library (its docs, components, tokens, MCP server if any) | new marketing pages: `impeccable:impeccable` via `reference/new-work.md`; `ui-ux-pro-max:ui-styling` when shadcn/Tailwind; `design-handoff:design-handoff` (optional plugin) when the input is a Figma file or mockup |
| Motion | the change moves | `emil-design-eng:animate` | `emil-design-eng:animation-vocabulary` |
| Review | anything user-facing | see step 8 | - |

At the start, tell the user the phase plan with the skills of each phase, so
they see the whole route even though only the first phase is loaded.

For a new landing with no brand, or a complaint about personality, identity,
generic output or "looks AI-made", use the identity flow below first.

For any other complaint about looks, Diagnose and Direction run together: load
`impeccable:impeccable` (`critique`), the Direction lead and
`ui-ux-pro-max:ui-ux-pro-max` at the start, always, even when the request names
no stack or style. A critique alone is a list of problems, not the new direction
the user asked for. This is a gate: call the Skill tool for each of them, plus
`frontend-design:frontend-design`, before the first diagnosis, direction,
prototype or recommendation, and name them in the phase plan. Directions
proposed without them loaded are void: load them and redo the work. This
overrides "load each phase's skills when the phase starts" above. A vague
complaint (step 2) runs its questions first; the gate applies once the answers
place it here. Research references before proposing directions (see
[identity-flow.md, step 2](references/identity-flow.md#2-research-before-directions));
[reference-gallery.md](references/reference-gallery.md) seeds the board with
inspected modern sites, grouped by the problem each one solves.
UI UX Pro Max supplies UX and stack rules; category styles and presets are
finishing material after the concept, never its source. When the project has a
design system, use UI UX Pro Max for UX and stack rules only, not to replace
the palette or fonts (rule 2 of the ladder).

Write what Diagnose and Direction decided (in `DESIGN.md` or the plan) before
Build, so later phases do not need the earlier skills loaded.

### When the product has no identity

Read [references/identity-flow.md](references/identity-flow.md). It owns the
full route: product context and naming/positioning → reference board → concept
devices and Impeccable concept seed → 2-3 directions → prototype and user pick
→ brand → `DESIGN.md` and tokens → landing → screenshot finish gate.

The user picks the direction. Preserve their approved concept and praised or
fixed visual choices. Presets finish a direction; they never generate it.

## 4. Pick the skills for the task

| The task is... | Lead | Support |
|---|---|---|
| New landing for a product with no brand | the identity flow in step 3, before the landing | `references/identity-flow.md`; brand → system → Build |
| Landing page for a developer tool / API / AI product | `taste:design-taste-frontend`, or the identity flow first when there is no brand | [devtool-landing.md](references/devtool-landing.md) + [landing-anatomy.md](references/landing-anatomy.md); `impeccable:impeccable` new-work in Build |
| New landing page, portfolio, marketing site with a brand | `taste:design-taste-frontend` | `frontend-design:frontend-design` for direction; [landing-anatomy.md](references/landing-anatomy.md); `impeccable:impeccable` new-work in Build |
| New marketing page where the user names Hallmark, one of its themes, or asks for a themed or custom page | `hallmark:hallmark` (leads instead of Taste, never with it) | with a brand or `DESIGN.md` it reads that as the locked system and deals no theme; [landing-anatomy.md](references/landing-anatomy.md) |
| New product UI: dashboard, settings, tables, multi-step flows | `frontend-design:frontend-design` | `ui-ux-pro-max:ui-ux-pro-max` (stack + UX guidelines), `impeccable:impeccable` for `harden` at the end |
| Settings, preferences or configuration area, new or redone from scratch (web, desktop app, CLI, TUI) | the settings flow in [settings-pages.md](references/settings-pages.md): ask, inventory, structure, row spec, build, harden, review | the skills each step of the flow names |
| Redesign or restyle an existing product app | phases: Diagnose → Direction (`frontend-design:frontend-design`) → Build → Review | `ui-ux-pro-max:ui-styling` in Build when shadcn/Tailwind |
| Redesign an existing marketing site | `taste:design-taste-frontend` (it audits the live page before changing it), or `hallmark:hallmark` (`redesign <path>`) when the user names Hallmark | `impeccable:impeccable` (`critique`) first |
| No personality, no product identity, "looks rushed" | the identity flow in step 3 | - |
| "Looks generic / AI-made / slop" | the identity flow in step 3 | `frontend-design:frontend-design` anti-template checks during Review |
| Adopt or migrate to a component library or design system ("use our kit", "move to shadcn") | the library itself: its docs, components, tokens | `ui-ux-pro-max:ui-styling` for Tailwind/shadcn mapping, `impeccable:impeccable` (`extract`) to pull tokens |
| Chat or AI assistant UI | `frontend-design:frontend-design` + the library's chat components if it has them | `impeccable:impeccable` (`harden`) for empty, error, loading and streaming states; `emil-design-eng:animate` for streaming motion |
| Forms, onboarding, first-run | `impeccable:impeccable` (`onboard`, `harden`) | `frontend-design:frontend-design` |
| Empty, error, loading states, edge cases | `impeccable:impeccable` (`harden`) | - |
| Only critique or audit of a built page, no rebuild asked | `impeccable:impeccable` (`critique` then `audit`); `hallmark:hallmark` (`audit <path>`) when the user names Hallmark | none: the user asked for a report, not a new direction |
| Critique a Figma frame, mockup or screenshot that has no code yet | `design-handoff:design-critique` (optional plugin) | none; once built, Impeccable `critique` owns it |
| Design ready for engineering: handoff spec from a Figma file or mockup | `design-handoff:design-handoff` (optional plugin) | `ui-ux-pro-max:design-system` when the project has no tokens |
| "Plan it before coding", discovery, UX flow | `impeccable:impeccable` (`shape`) | - |
| Broad area, no detail ("improve the UX", "the navigation is bad", "work on the identity") | its base path in [base-paths.md](references/base-paths.md): questions first | the skills the answers route to |
| Vague brief, no direction yet | `frontend-stack:design-director` agent, then route its result here | - |
| Review a page, component or PR diff | `frontend-stack:ui-reviewer` agent | - |
| Set up design context for a repo | `impeccable:impeccable` (`init`, then `document`) | - |
| Polish before shipping | `impeccable:impeccable` (`polish`) | `emil-design-eng:review-animations` for interaction details |
| Accessibility, performance, responsive checks | `impeccable:impeccable` (`audit`, `optimize`, `adapt`) | - |
| Too loud, or too bland | `impeccable:impeccable` (`quieter` / `bolder`) | - |
| Only typography / only color / only layout | `impeccable:impeccable` (`typeset` / `colorize` / `layout`) | `ui-ux-pro-max:ui-ux-pro-max` for font pairings or palettes |
| Choose a style, palette, font pairing, chart type | `ui-ux-pro-max:ui-ux-pro-max` | - |
| Charts and data visualization | `ui-ux-pro-max:ui-ux-pro-max` (chart guidance) | `emil-design-eng:pick-ui-library` for the chart library |
| Dark mode, theming | `ui-ux-pro-max:design-system` | `impeccable:impeccable` (`colorize`) |
| Design tokens / design system architecture | `ui-ux-pro-max:design-system` | `impeccable:impeccable` (`extract`) |
| shadcn/ui + Tailwind component work | `ui-ux-pro-max:ui-styling` | `emil-design-eng:pick-ui-library` |
| Screenshot or mockup image to code | `taste-imagegen:image-to-code` (optional plugin) | `frontend-design:frontend-design` |
| Build an animation | `emil-design-eng:animate` | `emil-design-eng:animation-vocabulary` when the user describes motion vaguely |
| Review or fix existing motion | `emil-design-eng:review-animations` / `improve-animations` | - |
| "Where should this animate?" | `emil-design-eng:find-animation-opportunities` | - |
| Gesture, spring, Apple-feel UI | `emil-design-eng:apple-design` | - |
| Web app should feel native on phones | `emil-design-eng:mobile-native` | `impeccable:impeccable` (`adapt`) |
| Try several versions of a component | `emil-design-eng:prototype` | - |
| Which library for X (charts, OTP, virtual lists...) | `emil-design-eng:pick-ui-library` | - |
| Toasts with Sonner | `emil-design-eng:ask-sonner` | - |
| UX copy, errors, microcopy, empty-state text | `ux-research:ux-copy` | `ui-ux-pro-max:brand` voice when the project has one; `impeccable:impeccable` (`clarify`) to fix copy in an existing screen |
| User research plan, interview guide, usability test | `ux-research:user-research` | - |
| Interviews, usability notes, NPS or tickets turned into UX decisions | `ux-research:research-synthesis` | - |
| Brand voice, visual identity, brand guidelines | `ui-ux-pro-max:brand` | `ui-ux-pro-max:design-system` for tokens |
| Logo, icons, corporate identity (CIP), social photos | `ui-ux-pro-max:design` | - |
| Banners, ads, social images, website hero art | `ui-ux-pro-max:banner-design` | - |
| Slides, pitch deck | `ui-ux-pro-max:slides` | - |
| Brand-kit board as a generated image | `taste-imagegen:brandkit` (optional plugin, needs image generation) | - |
| Explicit look: minimalist, brutalist, "expensive agency" | `taste-classics:minimalist-ui` / `industrial-brutalist-ui` / `high-end-visual-design` (optional plugin) | `taste:design-taste-frontend` for the inspector and fix loop |
| Google Stitch DESIGN.md | `taste-classics:stitch-design-taste` (optional plugin) | - |
| React Native / Expo motion, Swift | `emil-native:animate-expo` / `write-swift` (optional plugin) | - |
| Mobile app screens designed with Sleek, then built in React Native or HTML | `design-mobile-apps:design-mobile-apps` (optional plugin; needs `SLEEK_API_KEY`, sends the brief to sleek.design, paid beyond a trial) only when the user asks for Sleek | `emil-native:animate-expo` for motion after the build |
| Video that goes with a UI: product demo, hero or explainer clip, changelog, captions, animated overlay | `hyperframes:hyperframes` (optional plugin; needs Node 22 and the hyperframes CLI) | `hyperframes:media-use` for music, voice and images; `emil-design-eng:animate` stays the owner of in-page UI motion |
| Mockup image first, then code | `taste-imagegen:imagegen-frontend-web` / `imagegen-frontend-mobile` (optional plugin, needs image generation) | - |
| Video written as React components (Remotion) | `remotion-best-practices` when it is in the session's skill list (Remotion's own skills, not vendored: `npx skills add remotion-dev/skills`; Remotion needs a paid company license for for-profit organizations above 3 people) | `hyperframes:hyperframes` if the user prefers plain HTML |

A request that mixes jobs ("redesign it and add animations") is several rows:
run them as phases in the order of step 3.

## 5. Cases the table does not cover

New skills arrive with every upstream sync, and requests will not always match
a row.

- **No row fits:** use the job and surface from step 2, give the lead to the
  domain owner (rule 5 of the ladder), then check the session's skill list for
  a skill whose description fits better.
- **A named skill is not in the session's skill list:** skip it and use the
  next row's lead or `frontend-design:frontend-design`. Never guess a name.
- **Not a UI question:** product strategy, positioning, what to build, specs,
  roadmap, metrics, backend architecture or running the business belong to the
  companion stack. If `indie-dev-stack:indie-dev-stack` is in the session's
  skill list, hand the request to it. Otherwise do what you can and tell the user
  once per session that the companion marketplace covers it:
  `/plugin marketplace add JaimeJunr/claude-code-indie-dev-stack`.
- **A skill not listed here fits better:** a row still wins unless the user
  names the other skill. Use it as support and tell the user this router has no
  row for it yet.

## 6. Precedence ladder

When two loaded skills disagree, the higher rule wins:

1. **The user's explicit request and brand.** "Use Inter", "purple is our
   brand", "keep it like Linear" beat every skill ban.
2. **The project's existing system.** `DESIGN.md`, tokens, the component
   library already in use. Extend it; do not swap libraries or mix systems.
   A complaint about personality, identity or "looks AI-made" authorizes
   replacing the visual world for what the complaint covers, even if
   `DESIGN.md` exists. Keep only the visual choices the user explicitly praised
   or fixed in that scope. Preserve product truth, working behavior,
   accessibility and the framework/library; leave unrelated surfaces alone.
3. **Accessibility and correctness.** Contrast, focus states, reduced motion,
   keyboard access, no layout shift. Impeccable `audit` is the referee.
4. **Scope of the lead skill.** A skill's own "not for X" line is binding.
   `design-taste-frontend` now also covers app screens, but the stack still
   leads product UI with `frontend-design` unless the user asks for Taste.
5. **Domain owner.** Motion questions go to Emil's skills, style/palette data to
   UI UX Pro Max, critique/audit/polish to Impeccable, aesthetic direction to
   frontend-design or taste.
6. **The lead skill's taste defaults.** `frontend-design`'s anti-template
   rules outrank any other lead's taste defaults.

The rules that actually collide between packs, and how each is settled, are in
[references/conflicts.md](references/conflicts.md). Read it when a supporting
skill contradicts the lead.

## 7. Load budget

- Per phase: the base `frontend-design`, one lead and at most two supporting
  skills. Big skills
  (`design-taste-frontend`, `ui-ux-pro-max`, `impeccable`) are long; loading all
  of them at once burns context and produces averaged, generic output.
- Pick support from other packs than the lead when they own part of the
  subject (rule 5 of the ladder): one pack alone loses the knowledge only the
  others carry, even when it has a command for everything.
- Say in one line which skills each phase loaded, so the user can correct the
  routing early.
- Aesthetic presets (`taste-classics`: `minimalist-ui`, `industrial-brutalist-ui`,
  `high-end-visual-design`) never stack: at most one, as finishing material
  after the concept, or as the user's explicit choice.
- One marketing-page lead per task: `taste:design-taste-frontend` or
  `hallmark:hallmark`, never both. Hallmark's Floor binds only pages it leads.
- The brand, logo, banner and slides skills above overlap (`ui-ux-pro-max:design`
  and `design-system` also cover slides and branding). Load only the row's lead.
- Prefer the specific Emil skill over `emil-design-eng:emil-design-eng` as
  support: without a direct question the umbrella replies with a stock greeting.

## 8. Finish the same way every time

For anything user-facing, end with a review pass before calling it done:

1. Capture and open desktop + mobile screenshots with the session's available
   browser/screenshot tool. Compare the render with the reference board and
   chosen concept devices. Without tooling, report the missing visual evidence;
   do not claim the screenshot gate passed.
2. `impeccable:impeccable` `audit` (or delegate to the `ui-reviewer` agent).
   For new marketing pages, Build follows Impeccable's `reference/new-work.md`
   and hands captures + direction contract to `impeccable-finish-reviewer`
   (`plugins/impeccable/agents/impeccable-finish-reviewer.md` in this repo).
   Follow its `recapture` / `rebuild` / `fix` / `ship` disposition; use its
   documented fallback only when agents are unavailable.
   A page `hallmark:hallmark` or `taste:design-taste-frontend` led ends with
   that skill's own inspector and fix loop in place of that screenshot gate;
   still run `audit` for a11y.
3. If the change has motion, `emil-design-eng:review-animations`.
4. Fix the findings and recapture affected views. For personality/identity/
   AI-look requests, a missing signature or a render interchangeable with a
   named competitor can block completion. Report evidence, verdict and gaps.
