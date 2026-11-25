---
name: brainstorm-plan
description: "docs/plan/PLAN.md: the execution plan the orchestrator delegates from: waves (foundation, build, check, fixes), each part with its agent, scope, owned files, the documents and requirements it reads, what it depends on and its done-when, the checks, the risks, and a status kept current as reports come back. Read when splitting a planned task into delegations."
---

# PLAN.md: the waves, the parts, and where each stands

`PLAN.md` turns the other documents into delegations. It is what the
`todo` list mirrors, what each brief is written from, and where the state
of the run is kept, so a failed part, a second wave or a resumed session
starts from a written record rather than from memory. The split follows
`orchestration`; this is the document that holds it.

## 1. The template

```markdown
# Plan: <product or feature>

Documents: PRD.md, DESIGN.md, ARCHITECTURE.md, ERD.md, API.md (in docs/plan/ and the root)
Updated: <date, after wave N>

## Wave 1: foundation
| Part | Agent | Scope | Owns | Reads | Done when | Status |
|---|---|---|---|---|---|---|
| F1 | fe | Next.js scaffold, root layout, tokens, shared types | package.json, src/app/layout.tsx, src/styles/**, src/shared/types.ts | ARCHITECTURE, API (Types), DESIGN | builds; types match API.md | planned |

## Wave 2: build
| Part | Agent | Scope | Owns | Reads | Done when | Status |
|---|---|---|---|---|---|---|
| B1 | fe | Catalogue page | src/app/catalogue/** | PRD FR-1–FR-3, DESIGN (Catalogue), API (Products) | FR-1–FR-3 acceptance; preview clean 360/768/1440 | planned |
| B2 | fe | Product page | src/app/products/** | PRD FR-4, DESIGN (Product), API (Products) | FR-4 acceptance | planned |
| B3 | be | Products and cart API | src/server/**, src/app/api/** | API, ERD, PRD FR-1–FR-6 | routes as in API.md; tests pass | planned |
| B4 | db | Schema, migrations, seed | db/** | ERD | migrates from empty; seed loads | planned |

## Wave 3: check
| Part | Agent | Scope | Reads | Done when | Status |
|---|---|---|---|---|---|
| C1 | test | Checkout flow end to end, API tests | PRD acceptance, API | acceptance lines pass | planned |
| C2 | review | All changes | all | no blockers | planned |

## Risks
- <What could go wrong and what the plan does about it: "stock may go negative under parallel checkouts: be uses a conditional update; C1 tests it">

## Log
- <date> wave 1 done: F1 built; tokens in src/styles/tokens.css.
- <date> B3 partial: /cart/items returns 422 without a code; fix sent to be.
```

## 2. Splitting

- Parts follow `orchestration`: one area and its files, one agent, sized
  to finish in one run; never split by activity on the same files.
- **Foundation** only when the build parts stand on something that does
  not exist: the scaffold, the root layout, shared types, tokens. One
  part.
- **Build** as wide as the files allow: each screen from `DESIGN.md`'s
  table its own `fe` part, the API a `be` part (or one per resource),
  the schema a `db` part, animation a `motion` part once the markup
  exists.
- **Check**: `test` against the PRD's acceptance lines, `review` over the
  changes, `security` where there is sign-in, payment, upload or anything
  public.
- **Fixes** go to the owner of the files, the finding as the brief.

## 3. Each part

- **Owns**: the files and folders it may change. No two parts of one wave
  own the same file; shared files belong to the foundation.
- **Reads**: the documents and the exact sections or requirement numbers.
  The brief names them; the specialist reads them.
- **Done when**: the PRD's acceptance for its requirements plus the
  checks that apply (builds, tests pass, preview clean). A part without a
  done-when cannot be judged when it reports.
- **Depends on**: implied by the wave. A part that needs another's output
  goes in a later wave.

## 4. From plan to delegation

1. Mirror the parts in `todo`, grouped by wave.
2. Delegate a whole wave in one step, one brief per part, each written
   from its row: goal, the user's decisions, scope and owned files, the
   parts beside it, the documents to read, the contract copied from
   `API.md`, done-when.
3. When the wave reports, update Status (done, partial, failed, with a
   line in Log), fix the documents if a report changed a decision, and
   write the next wave's briefs from the updated plan.

## 5. Status is a record, not a hope

Planned, running, done, partial, failed. "Done" only after the report's
`VERIFIED` line says how it was checked. A failed part keeps its row, with
the retry as a new line in Log. The user can open `PLAN.md` at any point
and see what is built, what was checked, and what is left.

## Check it

- Every Must requirement in `PRD.md` is in some part's Reads and some
  check's scope.
- No file is owned by two parts of one wave; shared files are in the
  foundation.
- Every part has an agent, owned files, what it reads, and a done-when.
- Status and Log match the reports that came back.

## Avoid

Parts split by activity; a foundation that builds features; parts with
no done-when; briefs that drift from their row; statuses marked done
without a verification; a plan never updated after the first wave.
