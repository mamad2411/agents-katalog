---
name: dashboard-upgrade
description: Upgrades an app dashboard, back office or internal tool built for a specific operator into a reliable, premium tool, UX and UI together. It maps the operator's real day, fixes broken actions and data bugs first, builds shared foundations (forms that never lose input, phone-ready lists, error codes the operator can report), reshapes screens around their tasks, adds one or two signature moments, verifies in a real browser and against a local database, and ships one epic PR. Use when asked to "spice up", stabilize, polish or make premium a dashboard or admin tool. Not for marketing sites (use site-upgrade) or single-component tweaks.
license: MIT
metadata:
  version: 2.0.0
  author: vvhybe
---

# Dashboard upgrade

A method for turning a dashboard that fails its operator (lost payments, dead buttons, forms that forget what was typed) into a calm, reliable tool they trust. It was distilled from a real epic: a yoga studio's command center in Marrakech, run by one instructor, mostly on a phone between classes. Reuse the **method, building blocks and traps**, never the look or the business rules: every dashboard takes its direction from its own operator, data and brand.

The reference implementation is public: **[jnaninyoga/dashboard](https://github.com/jnaninyoga/dashboard)** (Next.js, Drizzle, Postgres, shadcn). The `Ref:` paths in the references point into it; read them on GitHub or with `gh api repos/jnaninyoga/dashboard/contents/<path>`. Never link or use its live app.

## Ground rules

1. **Reliability before spice.** A dashboard that loses a payment or a typed form isn't premium, however it looks. Order of work: data and action bugs (with tests), then shared foundations, then flows, then spice.
2. **Built for one operator's day, not a generic admin.** Screens follow their tasks, in their words, on their device. No KPI-tile walls or multi-tenant settings they will never use.
3. **Never lose input.** Create and edit happen in a surface that asks before discarding (a sheet on desktop, a drawer on phones), never in a dialog that closes on an outside click.
4. **Every action answers.** Success and failure are always visible. A failure carries a short code that matches a server log line, plus a report the operator can send to the developer.
5. **One number, one truth.** Each figure (amount due, credits left) comes from one domain module and reads the same on every screen. Money in integer cents, inputs that accept a decimal comma, dates in the business's time zone.
6. **Calm motion that answers the operator.** Motion shows what changed. Ambient and signature motion lives where they aren't working: sign-in, greeting, empty and error screens. Nothing jerky, nothing that delays a tap.
7. **Follow the target repo.** Read its README and contributing rules, use its package manager, match its framework versions, naming and comment density.
8. **Production is the owner's call.** Never query or migrate the live database; work on a local copy. Don't deploy, publish, run production migrations or change production settings: list them as owner steps. Secrets stay out of git. In a public repo, keep client names, prices and unfixed security gaps out of commits and PRs.
9. **Never call a screen done below 9/10.** Before saying a screen is finished, screenshot it at phone and desktop widths, score it against a professional bar (hierarchy, redundancy, alignment, affordance, type, density, fit to the operator's day), fix what costs points, and repeat. A self-rating of 6 or 7 offered only after "done" is the sign of skipped work.

## Workflow

Work through the phases in order; phases 3 to 5 repeat with the owner's live feedback. Read each reference only when you reach its phase.

| Phase | Do | Read |
| --- | --- | --- |
| 0. Kickoff | Branch off the default branch, set up the local database, start the dev server, add a dev-only playground, take baseline screenshots at 1440 and 390 | [references/verification.md](references/verification.md) |
| 1. Discovery | Map the operator's day, audit every route and action, find the truth sources, rate it honestly, write the phased plan, ask the owner's decisions | [references/discovery.md](references/discovery.md) |
| 2. Stabilize | Production-breaking fixes (a separate hotfix PR when production is broken), then tests and CI on the money and time logic | [references/foundations.md](references/foundations.md) § Data and money |
| 3. Foundations | Build the shared form sheet, list, row actions, feedback, confirm, empty and error screens once; move every screen onto them; delete the old variants | [references/foundations.md](references/foundations.md) |
| 4. Flows | Reshape screens around the operator's day: home, the core loops, money flows, history, navigation, sign-in | [references/flows.md](references/flows.md) |
| 5. Spice | Tokens, type scale, badges, motion, one or two signature moments, dark mode | [references/design-direction.md](references/design-direction.md) |
| 6. Verify | Browser loops at phone and desktop widths, menus and tap targets, dark mode, reduced motion, real server actions against the local database | [references/verification.md](references/verification.md) |
| 7. Ship | One epic PR verified as a whole, owner update, memory notes | [references/delivery.md](references/delivery.md) |

Check [references/gotchas.md](references/gotchas.md) whenever something behaves oddly, and [references/feedback.md](references/feedback.md) whenever the owner reacts. If a design-direction skill is installed (`frontend-design`, `impeccable`, `taste-skill`), load it in phase 5; this skill stands on its own without it.

When the owner sends live feedback, save it to memory first. If they say "no work, just save it", stop after saving.

## Scripts

`scripts/playwright/*.js` are for the Playwright MCP `browser_run_code_unsafe` tool. The MCP only reads files inside the workspace, so copy them first (`mkdir -p .playwright-mcp && cp <skill>/scripts/playwright/*.js .playwright-mcp/`) and pass `filename: ".playwright-mcp/<name>.js"`. Each file is a single function expression with no trailing semicolon. Make sure `.playwright-mcp/` is in the repo's `.gitignore`.

- `covered-controls.js` lists buttons, links and menu triggers whose centre is covered by another element: the dead "⋮" menu.
- `tap-targets.js` lists, at phone width, controls smaller than 40×40 px and visible text under 12 px.
- `overflow.js` finds what causes horizontal scroll at 320 to 1440 px and names the outermost culprits.

## Assets

- `assets/action-harness/` runs real server actions against the local database without Next.js: a tsconfig template, a `next/cache` stub and an example script. See its README.
- `assets/static-preview.tsx` renders one presentational component to a static HTML page with the app's theme tokens and CSS, for a visual check when a dev server won't fit in memory.

## Owner checkpoints

Ask these once, with options, before building on them; don't stall other work while waiting:

- the business rules behind money: how quotes become invoices, how payments are allocated, rounding and tax
- who may sign in, and whether the auth app may leave testing mode
- the language of the UI and of generated documents
- what is paid scope and what is a free extra
- anything that writes to a third party (calendar, contacts, email)
- every production step (migrations, env vars, deploys): the owner runs or approves it
