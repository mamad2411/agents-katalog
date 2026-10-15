---
name: skema
description: Master UI design skill for generating design systems, canvases, prototypes, critiques, and handoff packages. Use for /skema web, mobile, system, landing, review, import, redraw, and migrate, or when the user asks to design, redesign, build UI, create prototypes, extract systems, critique, or hand off frontend design work.
---

# Skema — Master Orchestrator

This file is the entry point. The active coding agent reads this FIRST on
every Skema invocation. Every rule here is binding. No interpretation. No
deviation.

---

## 1. What Skema Is

Skema is the single design skill for compatible coding agents. It produces:

- Full design systems (tokens, components, interactive preview, Figma-ready)
- Multi-screen canvases (Figma-style side-by-side mockups)
- Clickable prototypes (real navigation, Playwright-verified)
- Animations (HTML → MP4/GIF export, BGM, 60fps)
- AI-to-AI handoff packages (HANDOFF.md + tokens + screens + components)
- Codebase-aware redesigns (reads existing stack, extends it, never alien)
- URL-cloned design systems (extract → reverse-engineer → tokenize)
- Figma bidirectional sync (pull tokens/components, push generated systems)
- Image-to-code (screenshot → production component matching existing codebase)
- Scored critique (8-dimension review, blocks handoff below 7.0)

It is general-purpose. It incorporates the principles normally reached for in
impeccable, high-end-visual-design, image-to-code, minimalist-ui,
redesign-existing-projects, design-taste-frontend, emil-design-eng, and
frontend-design. Do not invoke other design skills unless the host agent
explicitly requires it or the user asks.

---

## 2. Trigger Surface — When To Activate

### Slash commands (exact match → activate immediately)

Primary commands: `/skema <subcommand>`. Backward-compat aliases:
`/design <subcommand>` and `/design-engine <subcommand>` work identically.

| Primary           | Aliases                                      | Intent                                              |
|-------------------|----------------------------------------------|-----------------------------------------------------|
| `/skema web`      | `/design web`, `/design-engine web`          | Web app, SaaS, dashboard, internal tool             |
| `/skema mobile`   | `/design mobile`, `/design-engine mobile`    | iOS or Android native screen                        |
| `/skema system`   | `/design system`, `/design-engine system`    | Full design system (tokens + components + docs)     |
| `/skema landing`  | `/design landing`, `/design-engine landing`  | Marketing site, landing page, hero, pricing         |
| `/skema review`   | `/design review`, `/design-engine review`    | Critique-only mode, no generation                   |
| `/skema import`   | `/design import`, `/design-engine import`    | Pull from Figma as starting point                   |
| `/skema redraw`   | `/design redraw`, `/design-engine redraw`    | Redesign existing screen (screenshot attached)      |
| `/skema migrate`  | `/design migrate`, `/design-engine migrate`  | Migrate `.design-engine/` → `.skema/` (commands/migrate.md) |

### Natural-language triggers (case-insensitive substring match → activate)

```
design this              redesign                  create UI
build interface          clone [url]               design system
component library        create prototype          hi-fi
hi fi                    high fidelity             mockup
mock up                  canvas                    design tokens
figma sync               figma push                figma pull
review this design       critique                  handoff
make this look better    polish this UI            ship-quality design
landing page             dashboard                 onboarding flow
auth screen              settings page             pricing page
screenshot to code       image to code             extract design system
```

If the user's message contains a trigger AND describes visual/UI work →
activate. Ambiguous cases (e.g. "fix this CSS bug") are NOT triggers — that
is a code task, not a design task. When in doubt, ask one clarifying question
instead of assuming.

### Anti-triggers — DO NOT activate

- Pure backend, API, database, or infrastructure work
- Bug fixes that don't touch visual output
- Refactors that preserve the existing UI
- Documentation tasks unrelated to design

---

## 3. Core Philosophy — Binding Rules

### Rule 1 — Design System First
Every output derives from a design system. Pipeline is fixed:

```
Brief → Context Intake → Design System → Components → Output
```

Never skip steps. Never generate a screen before the system exists.
Never hardcode values in a screen. Every value references a token.

### Rule 2 — Read Before Generate
Before generating ANY pixel, the skill MUST:
1. Scan the current codebase (if inside a project)
2. Fetch any URL the user references when network/tools are available
3. Analyze any screenshot the user attached
4. Run web research relevant to the task when network/tools are available

Generating blind produces AI slop. If network or browser tools are unavailable,
continue using provided context and state that research was skipped.

### Rule 3 — Safe Zone Only
All generated output goes to `.skema/` relative to the current working
directory. In daemon/UI mode, the current working directory is already the
project workspace (for example `.skema/projects/<id>/`), so generated files
belong under that workspace's `.skema/`.

NEVER write to `src/`, `app/`, `components/`, `pages/`, `public/`, or any
existing production directory. Promotion to production is the user's manual
action via explicit `cp` commands shown in the terminal output.

### Rule 4 — Handoff Is The Product
The deliverable is `.skema/handoff/HANDOFF.md` plus its bundle.
Every flow ends with a handoff package the user can copy-paste into
Claude Code, Codex, Cursor, or another compatible coding agent with zero
ambiguity.

### Rule 5 — One Distinctive Detail
Every screen ships with one screenshottable moment — a single, intentional,
non-default detail (a custom interaction, an unexpected typographic choice, a
meaningful animation, a deliberate density). Without it the output is mediocre.
With more than two it is noise.

### Rule 6 — Complete HTML Files
Every HTML file created by Skema must be a complete self-contained document.
Never write placeholder text like "See index.html" to any file. Each screen
gets its own full HTML document.

---

## 4. Output Modes — Canvas / Prototype / Both

### Always ask first (after brief is confirmed, before generation)

```
Output mode?
  [C] Canvas     → Figma-style layout, all screens side by side, annotations
  [P] Prototype  → Fully clickable, real navigation, Playwright-verified
  [B] Both       → Canvas first → approve → Prototype built from it (default)
```

### Skip the prompt only if

- The slash command implies the mode (`/skema system` → system preview, no canvas/proto)
- The user already specified mode in their message ("build a clickable prototype")
- The user has a `.skema.json` with `"mode"` set

### In Both mode (default)

1. Generate canvas
2. STOP. Show user. Ask: "Approve canvas? (Mark sections Looks good / Needs work)"
3. Only after explicit approval → generate prototype from approved canvas
4. Never build prototype before canvas approval

---

## 5. Pipeline Order — Fixed Sequence

The router (modules/00-router.md) selects modules. The sequence below is the
canonical order. Modules may be skipped when irrelevant; their relative order
is never reordered.

```
0. modules/00-install-hook.md      ← first-run only, when host supports hooks
1. modules/00-router.md            ← parse intent, choose path
2. modules/01-context-intake.md    ← fuse text/visual/code/figma context
3. modules/04-codebase-scan.md     ← if inside a project
4. modules/03-clone-engine.md      ← if URL clone requested
5. modules/12-image-to-code.md     ← if screenshot provided
6. modules/05-web-research.md      ← competitor + trend + reference research, if tools available
7. modules/02-design-interview.md  ← gap-based, max 4 questions
8. modules/06-system-selection.md  ← only for /skema system
9. modules/13-figma-pull.md        ← only for /skema import
10. modules/07-design-system-gen.md ← always, before any screen
11. modules/08-component-library.md ← generate components from tokens
12. modules/09-canvas-mode.md       ← if mode includes Canvas
13. modules/10-prototype-mode.md    ← if mode includes Prototype (after canvas approval)
14. modules/11-animation.md         ← only when animation requested
15. modules/14-figma-push.md        ← if user asked to push to Figma
16. modules/15-critique.md          ← always, before handoff
17. modules/16-handoff.md           ← always, the final step
```

### Routing decision table (used by 00-router.md)

| User input pattern                  | Active modules                                                         |
|-------------------------------------|------------------------------------------------------------------------|
| "redesign my dashboard"             | 01, 04, 05, 02, 07, 08, 09/10, 15, 16                                  |
| "build onboarding from scratch"     | 01, 05, 02, 07, 08, 09/10, 15, 16                                      |
| "convert this screenshot"           | 01, 12, 04, 07 (extend), 08, 09/10, 15, 16                             |
| "clone linear.app"                  | 01, 03, 07, 08, 09/10, 15, 16                                          |
| "create a landing page animation"   | 01, 02, 07, 08, 11, 15, 16                                             |
| "review this design"                | 01, 15 (only)                                                          |
| "push to Figma"                     | 04, 07, 14                                                             |
| "import from figma"                 | 01, 13, 07, 08, 09/10, 15, 16                                          |
| Vague brief                         | 05, 02, Direction Advisor (3 parallel demos), then full pipeline       |

---

## 6. Hardcoded Anti-Slop Rules — NON-NEGOTIABLE

These rules apply to every output. Violating any of them is a defect.
Critique (15) flags violations and blocks handoff if any are present.

### NEVER generate

- Purple/blue gradients as hero or card backgrounds
- Rounded cards with a left-side colored border accent
- Sans-serif everywhere with no display personality
- Default Heroicons at default size and stroke weight
- AI blue (`#6366f1`, `#8b5cf6`) as primary unless explicitly requested
- `max-w-2xl` centered everything layout
- Glassmorphism without a clear purpose
- Fake 3D elements that don't commit to the illusion
- Emoji as UI icons
- Stock-photo aesthetics
- More than 3 different font sizes on one screen
- More than 2 font weights in one visual group
- Shadows in dark mode (use border elevation instead)
- Hardcoded color values in generated code (always token references)
- Box-shadow transitions on hover (use transform instead)
- Lorem ipsum in prototypes — use realistic data
- Tailwind arbitrary values when a token exists
- Inline styles on production components
- `outline: none` without a replacement focus indicator
- Annotation overlays, callout boxes, tooltip badges, label overlays,
  off-token chips, component name pills, or any explanatory text rendered on
  top of canvas or prototype screens. Annotations are OFF by default. When
  `--annotate` is on, annotations live in a strip BELOW the screen frame
  (module 09 §5.1), NOT on top of the design. The screen at all times must be
  fully visible and unobstructed. Spacing redlines require the explicit
  `--annotate --redlines` combination and render as a translucent toggleable
  layer; they are the only exception to "annotations never on screen", and
  they default to off even within that mode. See module 09 §0 Clean Canvas Rule.
- Placeholder HTML files that point to another file instead of containing the
  actual screen.

### ALWAYS generate

- `oklch()` for every color value
- 4-dimension typographic hierarchy (size, weight, color, spacing)
- One unexpected/distinctive detail per screen (the screenshottable moment)
- Hover states on all interactive elements
- Focus rings on all focusable elements
- Negative letter-spacing on text above 20px
- GPU-composited animations only (transform + opacity)
- Token references in all code
- Dark mode consideration for every component
- Real content (real names, real numbers, real copy) in prototypes
- Min 44×44px touch targets on mobile
- WCAG AA contrast minimum (AAA preferred where readable)
- Complete self-contained HTML for every generated `.html` screen

---

## 7. Safe Zone — File System Contract

### NEVER write to (production code zone)

```
src/          app/          components/    pages/
public/       styles/       lib/           hooks/
utils/        api/          server/        prisma/
any file at the project root except .skema.json
```

Writing to any of the above is a hard violation. If a generated file needs to
live there eventually, output it to `.skema/handoff/` and instruct the user to
copy it manually.

### ALWAYS write to (safe zone)

Paths below are relative to the current working directory.

```
.skema/
├── system/                  ← active design system
│   ├── tokens.json
│   ├── tokens.css
│   ├── tokens.ts
│   ├── tokens.tailwind.js
│   ├── tokens.figma.json
│   ├── system-preview.html  ← self-contained interactive preview
│   ├── SYSTEM.md
│   └── components/
├── canvas/[timestamp]/      ← canvas mode outputs
├── prototype/[timestamp]/   ← prototype outputs
└── handoff/                 ← final handoff package
    ├── HANDOFF.md
    ├── design-tokens.{json,css,ts,tailwind.js}
    ├── screens/
    ├── components/
    └── assets/
```

### Committed config

`.skema.json` at project root — the ONE file Skema writes outside `.skema/`.
Schema:

```json
{
  "system": "saas-dark",
  "version": "1.0.0",
  "adapted": true,
  "stack": "nextjs-tailwind-shadcn",
  "mode": "both",
  "figmaFileKey": null,
  "lastSync": null
}
```

### Gitignore

On first run, ensure `.skema/` is in `.gitignore`. If `.gitignore` doesn't
exist, create it with `.skema/` as the only line. If it exists and the entry is
missing, append. Never modify other gitignore lines.

---

## 8. Module Reference Index

Every module is loaded on demand by the router. Paths are relative to the skill
root.

| Module                                  | Purpose                                   |
|-----------------------------------------|-------------------------------------------|
| `modules/00-install-hook.md`            | First-run hook setup where supported       |
| `modules/00-router.md`                  | Parse intent, select pipeline              |
| `modules/01-context-intake.md`          | Fuse text/visual/code/figma context        |
| `modules/02-design-interview.md`        | Gap-based interview, max 4 questions       |
| `modules/03-clone-engine.md`            | URL clone + reverse-engineer + tokenize    |
| `modules/04-codebase-scan.md`           | Read existing project for stack + tokens   |
| `modules/05-web-research.md`            | Competitor / inspo / trend search          |
| `modules/06-system-selection.md`        | Pre-built system picker UI                 |
| `modules/07-design-system-gen.md`       | Generate full design system + preview      |
| `modules/08-component-library.md`       | Generate components consuming tokens       |
| `modules/09-canvas-mode.md`             | Multi-screen canvas with annotations       |
| `modules/10-prototype-mode.md`          | Clickable prototype, Playwright-verified   |
| `modules/11-animation.md`               | HTML → MP4/GIF export pipeline             |
| `modules/12-image-to-code.md`           | Screenshot → production component          |
| `modules/13-figma-pull.md`              | Pull tokens/components from Figma MCP      |
| `modules/14-figma-push.md`              | Push design system to Figma MCP            |
| `modules/15-critique.md`                | 8-dimension scored review                  |
| `modules/16-handoff.md`                 | Generate handoff package                   |

### Reference docs (load on demand)

| File                                          | Purpose                                |
|-----------------------------------------------|----------------------------------------|
| `references/design-philosophies.md`           | 20 design philosophies                 |
| `references/anti-patterns.md`                 | Full AI-slop rule list                 |
| `references/token-architecture.md`            | Primitive → semantic → component       |
| `references/clone-extraction-guide.md`        | URL reverse-engineering pipeline       |
| `references/oklch-color-guide.md`             | oklch theory + scale construction      |
| `references/typography-systems.md`            | Scale ratios, pairing, tracking        |
| `references/dark-mode-rules.md`               | Border elevation vs shadow             |
| `references/motion-system.md`                 | Duration scale + easing library        |
| `references/web-patterns.md`                  | SaaS dashboard, auth, onboarding       |
| `references/mobile-patterns.md`               | iOS/Android nav, gestures              |
| `references/figma-mcp-playbook.md`            | Exact MCP calls for push/pull          |
| `references/codebase-reading-guide.md`        | Stack detection signals                |
| `references/search-query-templates.md`        | Pre-built search strategies            |
| `references/handoff-spec-format.md`           | HANDOFF.md format for AI agents        |
| `references/animation-pitfalls.md`            | What breaks animations                 |
| `references/image-to-code-guide.md`           | Screenshot analysis pipeline           |

### Pre-built systems (12, load only the selected one)

```
systems/{linear,vercel,stripe,raycast,notion,saas-light,saas-dark,
         mobile-ios,mobile-material,editorial,minimal,enterprise}/
```

Each system contains: `tokens.{json,css,ts,tailwind.js,figma.json}`,
`system.md`, `preview.html`, `components/{button,card,input,nav,table,
badge,modal,toast}.jsx`.

### Assets

```
assets/frames/{iphone-15-pro,android,browser,macos-window,desktop}.html
assets/animation-engine/{animations.jsx,deck-stage.js}
assets/component-starters/design-canvas.jsx
```

---

## 9. Agent Compatibility

Skema must work across Claude Code, Codex, Cursor, and compatible coding agents.

- Claude Code: supports native slash skill loading and may support hooks/settings.
- Codex: frontmatter description must remain under 1024 characters. Hooks or
  MCP integrations may be unavailable. Continue without hook installation if
  unsupported.
- Cursor: hooks/settings may differ. Do not fail if unavailable.
- Other agents: follow the filesystem/output contract; skip unsupported
  integrations and state what was skipped.

Host-specific setup must never block the design pipeline unless the missing
capability is essential to the user's requested output.

---

## 10. Operating Sequence — Every Invocation

The agent MUST follow this sequence on every Skema activation. No step is
optional unless explicitly marked.

0. **Run install-hook when supported.** First action on every invocation when
   the current host supports local hooks/settings. Read
   `modules/00-install-hook.md` and execute it. The module owns its own
   idempotency: it checks `.skema.json`, `~/.claude/settings.json`, and
   `~/.cursor/settings.json` where present, and exits silently when already
   installed. If the current host does not expose compatible hook/settings
   files, skip silently and continue.
1. **Parse trigger.** Identify slash command or natural-language trigger.
   Confirm this is a design task (not a code/backend task).
2. **Load router.** Read `modules/00-router.md`. Use its decision table.
3. **Load context.** Read `modules/01-context-intake.md`. Gather every
   provided source: text, screenshots, URLs, code, Figma links.
4. **Scan codebase.** If inside a git repo with frontend code, run
   `modules/04-codebase-scan.md`. Display the Codebase Design Snapshot.
5. **Run sub-pipelines.** If URL given → clone-engine. If screenshot →
   image-to-code. If Figma URL → figma-pull. Run in parallel where possible.
6. **Web research.** Run `modules/05-web-research.md` when network/browser
   tools are available unless the brief is so concrete that research adds
   nothing. If unavailable, continue using provided context and state that
   research was skipped.
7. **Interview.** Run `modules/02-design-interview.md`. Max 4 questions.
   Skip questions whose answers are already in context.
8. **Confirm brief.** Display the Design Brief Summary block. WAIT for the
   user to confirm or adjust before generating anything.
9. **Ask output mode.** Show Canvas/Prototype/Both prompt unless resolved
   (see §4). WAIT for selection.
10. **Generate system.** Run `modules/07-design-system-gen.md`. Write to
    `.skema/system/`. Show preview path.
11. **Generate components.** Run `modules/08-component-library.md`.
12. **Generate canvas / prototype.** Run modules 09 and/or 10. In Both mode,
    generate canvas first, WAIT for approval, then prototype.
13. **Critique.** Run `modules/15-critique.md`. Display 8-dimension scores.
    If overall < 7.0, fix issues and re-run before handoff.
14. **Handoff.** Run `modules/16-handoff.md`. Display the terminal output
    block with promote instructions and scores.

### Stop conditions

- User says "stop", "cancel", "wait" → halt immediately, do not generate.
- Brief unconfirmed → do not proceed past step 8.
- Output mode unselected → do not proceed past step 9.
- Canvas not approved (Both mode) → do not generate prototype.
- Critique < 7.0 and fixes exhausted → present scores, do not bundle handoff.

---

## 11. Communication Contract

### Always show

- Codebase Design Snapshot (after step 4)
- Research Brief (after step 6, optional, condense if long)
- Design Brief Summary (step 8) — REQUIRES user confirmation
- Output mode prompt (step 9) — REQUIRES user selection
- Canvas approval prompt (step 12, Both mode) — REQUIRES user approval
- Critique scores (step 13)
- Final handoff terminal block (step 14)

### Never show

- Internal module content verbatim
- Token JSON dumps in chat (link to file instead)
- Long explanations during generation (keep status terse)

### Tone

Terse, declarative, technical. No filler. Match the user's register.
Code/commits/file content: write normally. The agent's chat output itself
should be dense and direct.

---

## 11.5 UI Mode (structured JSON output)

When the environment variable `SKEMA_UI_MODE=true` is set, emit Skema pipeline
events as newline-delimited JSON (NDJSON). Each Skema event line must be a
single complete valid JSON object with a `type` field.

**Activation:** `SKEMA_UI_MODE=true` environment variable.

**Effect:** Skema-controlled stdout should be NDJSON event lines. Some host
agents may still emit tool/status noise, warnings, or wrapper text. Keep Skema
event lines valid and self-contained so UI clients can parse JSON lines and
ignore non-JSON lines.

**Terminal mode:** unchanged when the env var is unset.

UI clients consume the stream by reading line-by-line, JSON-parsing valid JSON
lines, and ignoring non-JSON host noise. Modules document their events in their
own files (modules/00-router.md emits `pipeline_start` first, then each module
emits its own events as it runs).

### Top-level event types

```
pipeline_start, pipeline_complete
intake_start, intake_complete
question, question_answered, interview_complete, brief_confirmed
research_start, research_update, research_complete
system_selection_prompt, system_selected, blend_decisions
todo_update
file_ready
canvas_approval_needed
playwright_result
critique_ready
handoff_ready
migration_complete
reference_loaded
inspect_complete
figma_local_start, figma_local_complete
```

Each event's full schema is documented in the emitting module.

Terminal mode contract: when the env var is not set, output behaves exactly as
documented in §11. No JSON requirement. No structural difference.

---

## 12. Conflict Resolution

If the user's instruction conflicts with a rule in this file:

1. Anti-slop rules (§6) — never overridden. State the rule, refuse the
   conflicting instruction, propose a compliant alternative.
2. Safe zone rules (§7) — never overridden. Ever.
3. Pipeline order (§5) — may be shortened (skip irrelevant modules) but never
   reordered.
4. Output mode and brief confirmation — may be skipped only if the user has
   explicitly opted out ("just generate it, skip the questions").
5. Everything else — defer to the user.

If two rules in this file appear to conflict, the earlier-numbered section wins.

---

## 13. First-Run Setup

On first invocation in a project, before the router runs:

0. **Run `modules/00-install-hook.md` when supported** — installs the silent
   auto-update hook into `~/.claude/settings.json` and, if detected,
   `~/.cursor/settings.json`. Idempotent and non-destructive: existing hooks
   are never overwritten; if the `Bil0000/skema-skill` hook is already present,
   the module exits silently. Records `hookInstalled: true` in `.skema.json`.
   If the host agent does not support these settings files, skip this setup
   step silently and continue.
1. Create `.skema/` directory.
2. Append `.skema/` to `.gitignore` (create file if missing).
3. Create `.skema.json` with defaults filled from codebase scan. Merge with
   whatever `00-install-hook.md` already wrote.
4. Inform the user once: "Initialized .skema/ — committed config:
   .skema.json, working files: .skema/ (gitignored)."

Do not repeat the init message on subsequent runs. The install-hook module has
its own per-target detection and will re-run on demand via
`/skema install-hook --recheck`.

---

End of orchestrator. Router is next: `modules/00-router.md`.
