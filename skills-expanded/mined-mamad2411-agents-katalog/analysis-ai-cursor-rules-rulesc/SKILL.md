# Analysis AI — Agent Instructions

> This is the canonical agent instructions file. All tool-specific files
> (CLAUDE.md, GEMINI.md, .cursor/rules/rules.mdc) are copies of this file.
> Edit AGENTS.md, then propagate to copies.

## Project

Analysis AI — internal BI assistant. Users upload contracts/documents (PDF, DOCX),
chat with them, get answers grounded in document content and BigQuery data with
inline source citations. Frontend only. No backend. Mock data for all states.

## Stack

- **Framework**: Next.js 16 App Router, TypeScript strict
- **Styling**: Tailwind CSS with design tokens from docs/DESIGN.md
- **Icons**: lucide-react (no other icon lib)
- **Utilities**: clsx + tailwind-merge via `frontend/src/lib/cn.ts`
- **Fonts**: Space Grotesk (display), Inter (body/UI), JetBrains Mono (mono) — Google Fonts
- **Node**: ≥18, package manager is npm

## Commands

```bash
npm run dev              # Start dev server (proxied to frontend/)
npm run build            # Production build — must exit 0
npm run lint             # ESLint — must exit 0
cd frontend && npx tsc --noEmit  # Type check — must exit 0
bash scripts/verify.sh   # Full pipeline: lint + typecheck + build
```

## Project Structure

```
analysis-ai/
├── frontend/                     ← Self-contained Next.js app
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       Root layout (fonts, metadata, globals, dark class)
│   │   │   ├── page.tsx         Root page (view state: "chat" | "documents")
│   │   │   └── globals.css      Tailwind v4 @theme + global styles
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── Sidebar.tsx  Fixed left nav (Chat, Documents, dark mode toggle)
│   │   │   ├── chat/
│   │   │   │   ├── ChatView.tsx      Chat container (thread + input bar)
│   │   │   │   ├── MessageThread.tsx Scrollable message list + typing indicator
│   │   │   │   ├── MessageBubble.tsx Single message with citation badges
│   │   │   │   ├── SourcesBlock.tsx  Collapsible citation details
│   │   │   │   ├── InputBar.tsx      Pinned textarea + send button
│   │   │   │   ├── ChatEmptyState.tsx Welcome state with suggested prompts
│   │   │   │   └── TypingIndicator.tsx Animated typing dots
│   │   │   └── documents/
│   │   │       ├── DocumentsView.tsx Documents container (upload + list)
│   │   │       ├── UploadZone.tsx    Drag-and-drop zone
│   │   │       └── DocumentList.tsx  File list with status badges + progress bars
│   │   ├── lib/
│   │   │   ├── cn.ts            className merge: twMerge(clsx(...inputs))
│   │   │   └── id.ts            getUniqueId(), getNextDocId()
│   │   ├── types/
│   │   │   ├── index.ts         Message, Citation, Document interfaces
│   │   │   ├── api.ts           API request/response contracts
│   │   │   └── domain.ts        Domain entity types (backend)
│   │   ├── constants/
│   │   │   └── prompts.ts       EXAMPLE_PROMPTS
│   │   ├── fixtures/
│   │   │   ├── messages.ts      INITIAL_MESSAGES mock data
│   │   │   └── documents.ts     INITIAL_DOCUMENTS mock data
│   │   ├── core/                Pure business logic (zero I/O, zero React)
│   │   │   ├── pipeline/
│   │   │   │   └── orchestrator.ts simulateResponse() + future pipeline
│   │   │   ├── types/
│   │   │   ├── document/
│   │   │   └── generate/
│   │   ├── server/              I/O services scaffold (BigQuery, LLM, etc.)
│   │   │   ├── services/
│   │   │   ├── clients/
│   │   │   ├── parsers/
│   │   │   ├── config/
│   │   │   └── middleware/
│   │   ├── config/              Client-side config scaffold
│   │   ├── hooks/               React hooks scaffold (useChat, useDocuments)
│   │   └── app/api/             Next.js API route scaffolds
│   │       ├── chat/
│   │       ├── documents/[id]/
│   │       └── query/bigquery/
│   ├── public/                  Static assets
│   │   ├── icons/
│   │   ├── images/
│   │   └── robots.txt
│   ├── tests/
│   │   ├── integration/
│   │   └── e2e/
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── eslint.config.mjs
│   ├── postcss.config.mjs
│   ├── vitest.config.ts
│   ├── vitest.setup.ts
│   └── package.json
├── docs/                        Project documentation
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── PROGRESS.md
│   ├── EVAL.md
│   ├── REVIEW.md
│   ├── GOAL.md
│   ├── PLAN.md
│   └── README.md
├── scripts/
│   ├── verify.sh                Lint + typecheck + build verification
│   ├── verify.ps1               Windows PowerShell version
│   ├── testing/                 Test infrastructure scripts
│   └── perf/                    Performance/QA scripts
├── .agents/                     Agent audit checklists
├── .cursor/                     Cursor IDE rules
├── AGENTS.md                    ← Canonical agent instructions (this file)
├── CLAUDE.md                    Claude-specific copy
├── GEMINI.md                    Gemini-specific copy
├── package.json                 Root orchestration (proxies to frontend/)
└── .gitignore
```

## Rules

Every rule has a reason. If a rule no longer applies, delete it.

1. **No hardcoded colors.** All colors come from DESIGN.md tokens defined in
   `globals.css` via Tailwind v4 `@theme`. Grep for `#[0-9a-fA-F]` in `frontend/src/components/` — must return 0.
   _Why: The design system is the source of truth. Hardcoded values drift._

2. **No inline styles.** Use Tailwind classes only. No `style={{}}` attributes.
   _Why: Inline styles bypass the design system and resist dark mode._

3. **No `any` type.** Every component has explicit prop interfaces. No implicit any.
   _Why: TypeScript is the safety net. `any` defeats it._

4. **Components ≤ 150 lines.** If a file exceeds 150 lines, split it.
   _Why: Small files = small context windows = fewer agent mistakes._

5. **Animations ≤ 250ms.** All transitions, hovers, and micro-interactions use
   `duration-150` or `duration-200`. Never exceed 250ms.
   _Why: User requirement. Snappy interactions feel premium._

6. **Icons from lucide-react only.** Do not install or use other icon libraries.
   Import icons as named imports: `import { MessageSquare } from "lucide-react"`.
   _Why: One icon source. No bundle bloat. Consistent visual weight._

7. **Design system wins.** If a coding decision conflicts with DESIGN.md,
   change the code, not DESIGN.md. Read `.agents/DESIGN-AUDIT.md` before
   any design decision.
   _Why: DESIGN.md was pulled from a curated system. Respect it._

8. **Verify after every phase.** Run `scripts/verify.sh` (or `verify.ps1` on
   Windows) after completing each phase. Do not advance to the next phase
   if verification fails.
   _Why: A type error in Phase 1 compounds through 5 more phases._

## Conventions

- **Imports**: Use `@/*` path alias. Group: React → external libs → local.
- **Exports**: Named exports for components. No default exports.
- **Naming**: PascalCase components, camelCase functions/variables, kebab-case files in src/app/.
- **Dark mode**: Tailwind v4 `@custom-variant dark` on `<html>`. Use `dark:` variants.
- **State**: Local `useState` only. No Context, Redux, or Zustand.
   Two isolated views, no cross-view data dependencies.
- **cn() helper**: Always use `cn()` from `frontend/src/lib/cn.ts` for conditional classes.

## Design Token Reference

Use these Tailwind class names (defined in `frontend/src/app/globals.css` via `@theme`):

**Colors**: `primary`, `cohere-black`, `ink`, `deep-green`, `dark-navy`, `canvas`,
`soft-stone`, `pale-green`, `pale-blue`, `hairline`, `border-light`, `card-border`,
`muted`, `slate`, `body-muted`, `action-blue`, `focus-blue`, `coral`, `coral-soft`,
`form-focus`, `on-primary`, `on-dark`, `error`

**Spacing**: `xxs`(2px), `xs`(6px), `sm`(8px), `md`(12px), `lg`(16px), `xl`(24px),
`xxl`(32px), `section`(80px)

**Radius**: `xs`(4px), `sm`(8px), `md`(16px), `lg`(22px), `xl`(30px), `pill`(32px),
`full`(9999px)

**Font families**: `font-display`, `font-body`, `font-mono`

For full specifications see → [DESIGN.md](./docs/DESIGN.md)

## Agentic Loop Contract

Each loop iteration starts with a **fresh context session** (Ralph Wiggum pattern).
State lives on disk in markdown files, not in conversation history. This prevents
context degradation and makes the loop resumable after any failure.

```
LOOP:
  ┌────────────────────────────────────────────────────────────┐
  │ RESET CONTEXT — Start fresh session with anchor files:     │
  │   AGENTS.md, docs/PROGRESS.md, docs/ARCHITECTURE.md        │
  │   (no conversation history carries over from previous tick) │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 1. READ STATE — check docs/PROGRESS.md for next unblocked task  │
  │    Read docs/DESIGN.md, type interfaces before implementation   │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. DECIDE — pick the task, check phase gate prerequisites   │
  │    If gate not met → STOP, flag to human                   │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 3. ACT — implement the task (one bounded unit of work)     │
  │    No scope creep. One task per tick.                      │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 4. VERIFY — run scripts/verify.sh — must exit 0            │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │   Did verify pass?   │
                  └──────┬───────────────┘
                    YES   ▼   NO
                  ┌─────────────────────────────────────────┐
                  │ 5a. Fix errors                         │
                  │     Add lesson to "Lessons Learned"     │
                  │     Re-verify (up to 5 attempts)       │
                  │     5 consecutive failures → ESCALATE   │
                  └──────────────────┬──────────────────────┘
                                     ▼ (back to step 4)
                    YES   ▼   NO (5 fails)
                  ┌─────────────────────────────────────────┐
                  │ 5b. ESCALATE → log to human, STOP loop  │
                  └─────────────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 6. PEER REVIEW — Run CODE-REVIEW.md audit                  │
  │    Spawn a fresh-context sub-agent to review the diff      │
  │    Reviewer is read-only (no edits), evaluates only the    │
  │    delivered code against type contracts and conventions.  │
  │    If review FAILS → back to step 3 (ACT)                  │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 7. UPDATE — mark task [x] in PROGRESS.md                   │
  │    Write result to disk (state persists across ticks)      │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 8. DESIGN AUDIT — check against .agents/DESIGN-AUDIT.md    │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 9. CHECK STOP CONDITIONS                                   │
  │    - No tasks completed in last 3 ticks? → ESCALATE        │
  │    - Phase iteration cap reached? → ESCALATE               │
  │    - All EVAL.md criteria PASS? → phase complete, advance  │
  └──────────────────────────┬─────────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 10. LOOP — until all EVAL.md criteria = PASS               │
  │     Then advance to next phase                             │
  └────────────────────────────────────────────────────────────┘
```

### Stop Conditions

The loop halts and escalates to a human when any condition triggers:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Consecutive task failures | 5 | Log summary, STOP |
| No progress (0 tasks done) | 3 consecutive ticks | Log summary, STOP |
| Phase iteration cap | Per phase gate budget (see below) | Log summary, STOP |
| All EVAL criteria PASS | N/A | Phase complete, advance gate |

When a stop condition triggers, write a summary to `.loop-summary.md`:
what was completed, what failed, what the next step should be. Then halt
until a human reviews and resets the loop.

### Escalation Protocol

1. Write `ESCALATION.md` with: phase, task attempted, error, last PROGRESS.md state
2. STOP the loop — do not auto-retry after escalation
3. Human reads escalation, decides: fix gate condition, adjust budget, or abort

## Phase Gates

| Phase | Prerequisite | Gate (must be true to advance) | Budget Cap |
|-------|-------------|-------------------------------|-----------|
| 1 → 2 | None | `npm run build` exits 0, `cd frontend && npx tsc --noEmit` exits 0, frontend/src/types/index.ts exists | 20 iterations |
| 2 → 3 | Phase 1 | Sidebar renders, view toggles between chat/documents | 15 iterations |
| 3 → 4 | Phase 2 | Chat view renders with mock messages, citations, sources block | 20 iterations |
| 4 → 5 | Phase 2 | Documents view renders with mock data, upload simulation works | 20 iterations |
| 5 → 6 | Phases 3+4 | All components pass design audit, dark mode works, responsive at 768px | 15 iterations |
| 6 → Done | Phase 5 | `verify.sh` exits 0, all EVAL.md criteria PASS, all REVIEW.md criteria PASS | 10 iterations |

**Parallel opportunities**: Phase 3 (chat) and Phase 4 (documents) are independent
and can run concurrently after Phase 2 completes.

## Audit Checklists

Before marking a phase complete, read and follow:
- `.agents/VERIFY.md` — verification pipeline steps
- `.agents/DESIGN-AUDIT.md` — design conformance checklist
- `.agents/CODE-REVIEW.md` — code quality checklist

## Lessons Learned

<!-- After every mistake, append: YYYY-MM-DD | What went wrong | Rule to prevent it -->
<!-- Prune entries when the model no longer makes that class of mistake -->

- 2026-06-12 | Next.js 16 CLI does not support next lint command natively; it treats 'lint' as the project directory. Use eslint directly or npm run lint.
- 2026-06-12 | React 19 ESLint flags synchronous state changes inside useEffect on mount as cascading renders. Initialize state via lazy initializer and sync DOM in useEffect without calling setState.
- 2026-06-12 | React 19 ESLint flags calling impure functions like Date.now() inside the component render body (even inside handler definitions). Move unique ID generators outside the component scope as top-level helpers.
- 2026-06-12 | React hook cleanups referencing refs (like clearing arrays of intervals) can trigger warnings if ref.current is read during cleanup. Copy the ref value to a local variable inside the useEffect body first.
