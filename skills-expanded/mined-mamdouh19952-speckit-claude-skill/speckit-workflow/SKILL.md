---
name: "speckit-workflow"
description: "Use when the user wants to build a project or feature with Spec-Kit / spec-driven development (speckit, /speckit-*, /speckit.*, specify init, spec → plan → tasks → implement) — on a new project or adding a feature to an existing one — or needs help installing or running GitHub Spec-Kit."
---

# Spec-Kit Workflow (Spec-Driven Development)

Use Spec-Kit to build features in a structured way instead of one giant prompt:
constitution → specify → clarify → plan → checklist → tasks → analyze → implement.

Reply in the user's language; keep commands/code in English.

## 0. Before starting — pick the scenario

1. Confirm the working folder (project root). Ask if unclear.
2. Check the tooling: `specify --version` (and `uv --version`). If missing, install (step 1).
3. Decide which scenario this is — they start differently:

| Scenario | How to tell | Start with |
|---|---|---|
| **A. New project** | Empty (or almost empty) folder | Step 2 init → constitution → first feature |
| **B. Existing project, Spec-Kit not set up yet** | Has code, no `.specify/` folder | Read the code (and `CLAUDE.md` if any) → step 2 init → constitution from the existing code → the new feature |
| **C. Existing project, Spec-Kit already set up** | `.specify/` exists | **Skip init.** Constitution only if still a placeholder. Go straight to `/speckit-specify` for the new feature |

4. Find out the stack (from `CLAUDE.md`, `package.json`, `composer.json`, etc., or ask). The plan must name it explicitly.

### CLAUDE.md
- `specify init` does **not** create or change `CLAUDE.md`. It is a Claude Code file, separate from Spec-Kit.
- Scenario B with no `CLAUDE.md`: suggest the user runs Claude Code's `/init` first so Claude learns the codebase. Optional, but it makes the spec and plan match the existing code.
- Scenario A: no need up front. After the first plan is approved, a short `CLAUDE.md` (stack, run/test commands) can be added if the user wants.
- Never copy the constitution into `CLAUDE.md` or the reverse — see section 4.

## 1. Install (only if missing)

```bash
# uv — macOS / Linux (then open a new terminal)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# uv — Windows (PowerShell, then open a new terminal)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# specify-cli — latest
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
# upgrade later
specify self upgrade
```

- `uv` downloads a Python for itself if none is installed; Git must be installed (the CLI is installed from a git URL).
- If `specify` is "not found" after installing, run `uv tool update-shell` and open a new terminal.

## 2. Init the project (scenarios A and B only)

Run this inside the project folder — the same command for a new or an existing project:

```bash
specify init --here --force --non-interactive --integration claude
```

Why every flag matters when Claude runs it:
- `--integration claude` — without it, a non-interactive run silently defaults to **Copilot**.
- `--non-interactive` — Claude's shell can't answer the arrow-key prompts; without it init can hang.
- `--force` — needed in any folder that already has files; without it init stops with "Current directory is not empty". Two normal hyphens, not an em dash (`—force`).

What init does and doesn't touch (verified on specify 1.2.x):
- Adds `.specify/` (templates, scripts, `memory/constitution.md`) and the Spec-Kit skills under `.claude/skills/speckit-*`.
- Does **not** touch your code, `CLAUDE.md`, or `.claude/settings.json`.
- Re-running it keeps an existing `.specify/memory/constitution.md` and `specs/`. Still, don't re-run it to add a feature — only to upgrade Spec-Kit (`specify self upgrade`, then init again).
- Picks the script type for the OS (PowerShell on Windows, sh on macOS/Linux) automatically.
- Optional: `--extension git` makes each new feature create its own git branch.

After init:
- The `/speckit-*` commands are new skills under `.claude/skills/`, so they do **not** load in the session that ran init. Don't stop: in this session, run each stage by reading `.claude/skills/speckit-<stage>/SKILL.md` **in full** and following it exactly (its scripts, templates, and file paths) — that file *is* the command. From the next Claude Code session the commands are available directly.
- Command names depend on the Spec-Kit version: `/speckit-specify` (1.x, installed as skills) or `/speckit.specify` (older, installed as commands). Same command — use whichever exists.

## 3. The workflow (in order)

| # | Command | What it does | Gate |
|---|---------|--------------|------|
| 1 | `/speckit-constitution` | Project principles (`.specify/memory/constitution.md`) — once per project | User provides/approves rules |
| 2 | `/speckit-specify` | Feature description (AR/EN) → `specs/NNN-name/spec.md` | User reviews spec |
| 3 | `/speckit-clarify` | Optional but recommended: asks questions about ambiguities | User answers |
| 4 | `/speckit-plan` | `plan.md` architecture/design — state the stack explicitly | User reviews plan |
| 5 | `/speckit-checklist` | Quality gate for requirements (design / UX / RTL / accessibility) | Fix gaps |
| 6 | `/speckit-tasks` | Split plan into executable tasks | — |
| 7 | `/speckit-analyze` | Optional: check spec / plan / tasks are consistent | Resolve issues |
| 8 | `/speckit-implement` | Execute tasks and write code | — |
| + | `/speckit-converge` | Optional (1.x): compare the code to the spec and add any unbuilt work to `tasks.md` | — |

Adding a feature later (scenario C): skip init and constitution — start again from `/speckit-specify`. Each feature gets the next numbered folder in `specs/`.

How stages find the current feature: `/speckit-specify` creates `specs/NNN-name/` itself (next free number) and writes its path to `.specify/feature.json`; plan, tasks, and implement read that file. Don't create feature folders by hand, and when switching back to an older feature, update `.specify/feature.json`. On Windows PowerShell 5.1, write JSON and Markdown as UTF-8 **without** BOM (`Set-Content -Encoding utf8` adds one).

Rules:
- Stop at each gate and show the user a short summary of the generated file before moving on. Never jump to implement without an approved spec + plan.
- Short path when the user wants speed: constitution → specify → plan → tasks → implement. Arabic/RTL projects keep the checklist (section 8) even on the short path.
- Checklist items are created **unchecked on purpose** — they are for the user to confirm. Show them, tick the ones the user confirms (or fix the spec/plan for the ones that fail). `/speckit-implement` stops and asks while any item is unchecked; that is expected, not an error.
- New project with authentication: make login work end to end before any other feature.
- Model hint (Claude Code): a stronger model (Opus) for constitution/specify/clarify/plan; a faster one (Sonnet) is fine for implement.

## 4. Constitution vs CLAUDE.md

- `.specify/memory/constitution.md` = the principles for THIS project (code style, testing rules, security rules, stack choices). Written by `/speckit-constitution`.
  - Right after init it is only a template full of placeholders like `[PROJECT_NAME]` and `[PRINCIPLE_1_NAME]`. If you see those, the constitution has **not** been written yet — run `/speckit-constitution` before `/speckit-specify`.
  - Existing project (scenario B): tell `/speckit-constitution` to derive the principles from the existing code and `CLAUDE.md` (stack, folder structure, naming, test style) so new work matches what's already there.
  - Already filled (scenario C): don't re-run it for each feature — only when a principle really changes.
- `CLAUDE.md` (if the project has one) = project facts and conventions Claude reads every session. Don't duplicate it into the constitution — reference it instead ("Also follow CLAUDE.md").
- The plan's Constitution Check covers both.

## 5. `/speckit-plan` details

It takes `spec.md` and produces the technical plan:
- Reads `constitution.md` + `spec.md`.
- Fills **Technical Context** with the stack and versions (e.g. PHP 8.3, Laravel 12, MySQL, Blade + Bootstrap; or Vue 3 + Vite + Pinia + Tailwind + Axios).
- Runs the **Constitution Check gate** — the plan must comply with the constitution.
- **Phase 0 → `research.md`**: resolves ambiguous technical decisions (local vs S3 image storage, how net profit is calculated…).
- **Phase 1 → `data-model.md`** (entities & relations) + `contracts/` (API endpoints, or web routes + forms for server-rendered apps) + `quickstart.md` (run/test steps).

Run `/speckit-plan` plain first, review `research.md` and `data-model.md`, then steer if needed, e.g.:
```
/speckit-plan Use spatie/laravel-medialibrary for images, and use Route Model Binding in all admin routes.
```

## 6. Organizing features

Each feature gets its own `/speckit-specify` and a numbered folder:
```
specs/
├── 001-authentication/spec.md
├── 002-products/spec.md
└── 003-cart/spec.md
```
Finish one feature → start the next with a new `/speckit-specify`. A "feature" = a complete capability (login, products, cart) — not every small edit. Not too small, not too big.

## 7. Figma designs

Before `/speckit-implement` on a Figma design: make sure Figma MCP is connected and authenticated, and get the specific `node-id`. Read the design first, then run the full chain:
```
using figma mcp can you read this figma pages <figma-url>?node-id=...
using speckit make all of this to implement the figma design into pages and make it in small tasks with best practice
/speckit-specify → /speckit-clarify → /speckit-plan → /speckit-checklist → /speckit-tasks → /speckit-analyze → /speckit-implement
```
Any task converting a whole Figma design or touching multiple features should go through Plan Mode / the full chain.

## 8. Arabic-first / RTL projects

If the project is Arabic-first, put RTL in the spec and always run `/speckit-checklist` with a prompt like:
> تحقق من جودة التصميم و UX لكل صفحات المشروع (ولوحة الأدمن لو موجودة): هوية بصرية موحدة (ألوان، خطوط، تباعد)، تباين لوني كافٍ (accessibility)، تصميم متجاوب (Responsive) لكل صفحة، دعم RTL واضح لكل عنصر تفاعلي، حالات التحميل/الأخطاء/النجاح موصوفة وقابلة للاختبار.

## 9. Example `/speckit-specify` prompt (medical device maintenance center)

```
مشروع لمركز صيانة أجهزة طبية، بواجهة Blade + Bootstrap. المطلوب:
1. صفحة عامة (Public) تعرض:
   - الأجهزة المعروضة للبيع بصورها وأسعارها ووصفها.
   - الأجهزة اللي تم صيانتها: صورة قبل وصورة بعد ووصف العطل.
   - صفحة خدمات المركز.
2. لوحة تحكم للأدمن بعد تسجيل الدخول:
   - إضافة/تعديل/حذف جهاز للبيع (اسم، وصف، سعر، صور، حالة التوفر).
   - إضافة/تعديل/حذف سجل صيانة: صورة قبل، صورة بعد، وصف العطل، تاريخ دخول، تاريخ خروج.
   - تسجيل تكلفة الصيانة وقطع الغيار والمبلغ المدفوع، مع حساب صافي الربح تلقائيًا.
   - قائمة بكل الأجهزة تحت الصيانة مع التواريخ والحالة (تحت الصيانة / تم التسليم) وإجمالي الأرباح.
المشروع Arabic-first، لازم دعم RTL في التصميم.
```

## 10. When `/speckit-*` commands are not available

This happens right after init (same session) or in tools without Claude Code skills. Run `specify init` in the project folder if it isn't done yet, then follow the same stages manually:
- Best source: the installed `.claude/skills/speckit-<stage>/SKILL.md` files — read each one in full and follow it; they name the exact scripts (`.specify/scripts/powershell/*.ps1` on Windows, `.specify/scripts/bash/*.sh` elsewhere) and templates.
- Otherwise read the templates in `.specify/templates/` (spec, plan, tasks, checklist) and the helper scripts in `.specify/scripts/`.
- Write `.specify/memory/constitution.md`, then `specs/NNN-feature/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `checklists/`, `tasks.md` exactly per the templates.
- Keep the same gates: stop for user review after spec, clarify, plan, and checklist; implement tasks in order and tick them off in `tasks.md`.

Reference: https://github.com/github/spec-kit
