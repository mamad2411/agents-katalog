---
name: learning-curriculum
description: Write a newbie learning curriculum for a codebase so readers can rebuild it and leave with an engineer mindset. Use when the user asks for learning docs, a study guide, 開發文件, "teach this repo", "how would you build this from scratch", 從頭開發, or a course that covers framework, layers, logging, tests, mocks, DI, context, SQL, or OTel.
---

# Learning Curriculum

Turns a real codebase into a **numbered course**: tool chapters first, then a day-by-day rebuild. The reader must be able to recreate the project without copying files, and leave with the habits (vertical slices, consumer-owned interfaces, context, cheapest fake) rather than a folder tour.

This is **not** reverse-architect (knowledge map) and **not** systems-analyst (observability gaps). Those explain a system. This skill **teaches someone to build one**.

## Core Philosophy

> **"After reading, a newbie can rebuild the same project from an empty folder — and every file they write has a reason."**

A tour of `internal/` fails that test. A curriculum passes it.

**Anti-patterns to avoid:**

- A single "how the code works today" essay (the user will say: that's not how I'd *build* it)
- Generic tutorials that never cite this repo's types, paths, or tests
- Finishing one layer (all SQL, then all HTTP) instead of one **vertical slice**
- Trusting README / Copilot instructions over Makefile, OpenAPI `paths:`, and tests
- Hiding design flaws; "what not to copy" is part of the lesson
- Dumping entire source files into markdown

Put long templates in `references/`. Keep this file as the thinking process.

---

## Thinking Process

When activated, follow these steps in order. If the user rejects the genre ("I wanted build order, not a tour"), go back to Step 1 — do not patch the wrong document.

### Step 1: Lock Outcome and Audience

**Goal:** Know who reads this and what they can *do* when they finish.

**Key Questions to Ask:**

- Newbie rebuilding, or experienced engineer contributing? (This skill assumes **newbie rebuild** unless they say otherwise.)
- Which stack topics must be taught explicitly? (Gin, layers, Zap, `testing`, mocks, OTel, SQL, DI, context — teach any the user named.)
- Language of the docs: match the user's latest message; keep code identifiers in English.

**Thinking Framework:**

- "The exam is: empty folder, same product, tests green."
- "Mindset is the residue after they forget the file names."

**Actions:**

1. Write one outcome sentence: "When they finish they can _____ and they will habitually _____."
2. List required tool chapters from the user's request (do not invent a 20-chapter book).
3. If they already have `learning/` docs of the wrong genre, plan to replace or split — do not append a tour to a rebuild guide.

**Decision Point:** You can complete:

- "Audience is [newbie]; success is [rebuild + named habits]; tool chapters are [list]; rebuild is last."

---

### Step 2: Ground in Executable Sources

**Goal:** Inventory the *real* system so every claim is verifiable.

**Key Questions to Ask:**

- What does Makefile / CI / Dockerfile actually run?
- Where is the HTTP contract (`openapi.yml` `paths:`, proto, routes)?
- Where is `main` / composition root?
- Which tests exist at handler, service, and DB layers?

**Thinking Framework:**

- Docs and comments lie. Tests, generated interfaces, and compose files do not.
- Run `scripts/scan-repo.sh` for a first pass; then **read** entry points, one handler, one service, one repo, one test of each kind.

**Actions:**

1. Run the scan script on the project root (see Usage).
2. Read composition root, consumer-owned interfaces, one request path, schema/migrations, mock tests.
3. Note drifts (README path vs generated path, 404 vs 409) — they become "do not copy" callouts.

**Decision Point:** You can complete:

- "I trust [Makefile/OpenAPI/tests] over [README/copilot-instructions] because [concrete mismatch]."

---

### Step 3: Extract Seams the Curriculum Must Teach

**Goal:** Name the boundaries a rebuilder must reproduce, not every function.

**Key Questions to Ask:**

- Who owns each interface — the **caller** or the implementer?
- Where is DI? (constructors in `main`, no framework, tests inject mocks)
- How does `context.Context` travel? (`c.Request.Context()` → service → `*Context` SQL)
- How is SQL shaped? (wide row vs mapping table, JSONB vs arrays, indexes vs queries)
- What is the cheapest fake per layer? (httptest mock, function-field mock, sqlmock, E2E last)

**Thinking Framework:**

| Seam | Newbie must be able to say |
|------|----------------------------|
| Layers | Handler may not SQL; service may not import Gin |
| DI | `main` news concretes; tests pass fakes into the same `New*` |
| Context | Request ctx downward; `Background()` only at process start |
| SQL | One query ↔ one product question; parameterized `*Context` |
| Tests | Prove the rule at the cheapest layer that can fail |

**Actions:**

1. Fill the seam table from real types (`CaseService` in handler, `CaseRepository` in service, etc.).
2. Trace **one** request (create/get) across all seams — that becomes the first rebuild slice.
3. List domain rules a clone must hit or it is a different product (duplicate key, 409, TTL, auth header).

**Decision Point:** You can complete:

- "If they skip [seam], they will [specific failure in tests or production]."

---

### Step 4: Design the Curriculum Map

**Goal:** Order files so tools are learned *before* they are required in the rebuild.

**Thinking Framework — File order:**

```
learning/README.md          path + outcome
00-mindset.md               habits (pain, slices, caller-owned interface, ctx)
01-… tool chapters          one concern each (layers, SQL/DI/ctx, framework, logs, tests, otel)
NN-rebuild.md               last: vertical slices that *use* the tools
```

**Key Questions to Ask:**

- Does each tool chapter answer: pain, how *this* repo does it, what not to do, one exercise?
- Does rebuild say "learn first: chapter X" before a phase that needs X?
- Can they stop after slice 1 (health + one POST) and still have a running process?

**Actions:**

1. Optionally run `scripts/scaffold-curriculum.sh` to create stubs (see Usage).
2. Keep README to a table of files and the exam (rebuild, don't peek).
3. Number tool chapters so rebuild can stay last even if you insert `01a`.

**Decision Point:** You can point at a README table and say:

- "Chapters 0–K are tools; chapter N is when they use them in order."

---

### Step 5: Write Tool Chapters (Pain → This Repo → Exercise)

**Goal:** Each tool file teaches a mechanism using **this** codebase's names.

**Structure for every tool chapter:**

1. **Pain** — one sentence, no library name.
2. **How this repo does it** — real types, file paths, short snippets (not whole files).
3. **What not to do** — including flaws in *this* repo (e.g. service importing handler errors).
4. **Exercise** — they must produce or point at something without memorizing the tree.

**Actions:**

1. Write mindset first (vertical slice, caller-owned interface, ctx first param, composition root, cheapest fake).
2. Write named topics the user asked for (framework, layers, logger, `testing` + mocks, OTel, SQL, DI, context). Combine SQL+DI+context if they share one request picture.
3. Cite `path` or `path:line` for hops.

**Decision Point:** A reader can explain the chapter out loud without opening the file.

---

### Step 6: Write the Rebuild Playbook (Vertical Slices)

**Goal:** Day-by-day construction order. Interface methods are added **per slice**, not on day one.

**Thinking Framework — one slice:**

```
contract (OpenAPI/proto) → generate
  → add 1 method to the *caller* interface
  → repo + sqlmock
  → service + mock repo
  → handler + mock service
  → pass request ctx
  → go test green
  → next API
```

**Phase order that usually works for an HTTP+DB service:**

A skeleton (health, config, logger, no DB) → B contract for **one** path → C two tiny interfaces → D connection + minimum schema → E first write path → F deepen same path (duplicates, etc.) → G reads → H domain graph (state machine) → I remaining field updates one-by-one → J list/delete → K versioned API → L side concerns (archive/S3) → M metrics/OTel → N E2E/CI last.

**Actions:**

1. Map this repo's real APIs onto that sequence.
2. Each phase: files to create, checklist, "learn first" link to a tool chapter.
3. State the repo is the **answer key** — peek after 20 minutes stuck or after tests are green.
4. End with "differences that are fine" vs "differences that mean you drifted."

**Decision Point:** Slice 1 has a test at three layers. Later slices only add interface methods they need.

---

### Step 7: Honest Gaps and Iteration

**Goal:** Teach judgment, not worship.

**Actions:**

1. Include a copy / don't-copy table (inverted deps, missing SQL spans, stale docs).
2. If the user says the docs are the wrong *kind*, rewrite the genre (rebuild vs tour) instead of adding sections.
3. Keep `learning/README.md` as the only index.

**Decision Point:** A senior would agree the "don't copy" list is real, not generic advice.

---

## Usage

```bash
# Inventory the repo (JSON on stdout; status on stderr)
bash /mnt/skills/user/learning-curriculum/scripts/scan-repo.sh [project-root]

# Create learning/ stubs
bash /mnt/skills/user/learning-curriculum/scripts/scaffold-curriculum.sh --out learning --topics mindset,layers,rebuild
```

**Arguments (`scan-repo.sh`):**

- `project-root` — directory to scan (default `.`)

**Arguments (`scaffold-curriculum.sh`):**

- `--out` — directory to write (default `learning`)
- `--topics` — comma-separated stub names, ordered (default see script)

**Examples:**

```bash
bash /mnt/skills/user/learning-curriculum/scripts/scan-repo.sh .
bash /mnt/skills/user/learning-curriculum/scripts/scaffold-curriculum.sh --out learning --topics mindset,layers,gin,zap,testing,otel,rebuild
```

Read `references/curriculum-template.md` when filling stubs. Read `references/anti-patterns.md` before the first draft.

---

## Output

A `learning/` tree, for example:

```
learning/README.md
learning/00-mindset.md
learning/01-layered-architecture.md
learning/01a-sql-di-context.md
learning/02-gin.md
learning/03-zap.md
learning/04-testing-and-mocks.md
learning/05-otel.md
learning/06-rebuild.md
```

Each tool file: pain, this-repo mechanism, mistakes, exercise. Rebuild file: phases with checklists. README: numbered path + exam.

---

## Present Results to User

1. Point at `learning/README.md` as the start.
2. One sentence: exam = rebuild, repo = answer key.
3. List tool chapters vs rebuild chapter.
4. Do **not** paste the curriculum into chat.

Always end with:

> "Read 0–N for tools, then the rebuild. Peek at the repo only after a slice's tests are green (or after 20 minutes stuck)."

---

## Troubleshooting

**"The user wanted a tour of the current code."**

- Wrong skill. Use reverse-architect or systems-analyst. This skill's first draft of a tour will be rejected.

**"They asked in Chinese / English."**

- Write prose in that language. Keep identifiers (`CreateCase`, `ExecContext`) in English.

**"SKILL.md is not enough to cover SQL, DI, and ctx."**

- One combined tool chapter with three sections sharing a single request picture is better than three disconnected essays.

**"Rebuild chapter is repeating the tool chapters."**

- Rebuild should only sequence work and say "learn first: 04-testing". Mechanisms stay in tool files.

**"No OpenAPI / no Gin."**

- Same process. Substitute the real contract and framework. Do not invent Gin lessons for a CLI.
