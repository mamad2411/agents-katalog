---
name: problem-description
description: Use when the user wants an interactive step-by-step HTML walkthrough explaining a complex technical problem (DB error, race condition, design issue, conceptual blocker) using concrete data and manual navigation. Triggers on phrases like "make me a walkthrough", "explain step by step with data", "interactive explanation", "make an animation", "walk me through with real examples", "อธิบายแบบ step by step", "ทำ animation/walkthrough/visualization", "ทำเป็น diagram", "วาด diagram". Do NOT use for one-line clarifications, conceptual Q&A answerable in a paragraph, or simple "what does X mean" questions — only when an interactive HTML artifact would clearly help.
effort: max
---

# Problem Description — Interactive Step-by-Step Walkthroughs

## Overview

Generate a self-contained HTML page that explains a technical problem using:

- **Concrete data** — real names, real numbers, culturally appropriate context (e.g., Thai names for Thai users)
- **Manual step-through navigation** — `Next →`, `← Previous`, `↻ Reset` buttons. Reader controls pace.
- **Visual state changes** — at each step, the right thing highlights and the reader can point at it
- **Color-coded narration** — info / warn / error / success / magic boxes explaining what fires + WHY

**Core principle:** The reader should be able to point to any specific element at each step and say *"yes I understand why this is in this state right now."*

## Output location — REQUIRED (do this, don't default elsewhere)

The finished `.html` **must** land inside the **project/workspace the user has open in their
editor**. Identify that project from the workspace the user is working in — **not** from your
own current working directory, which on some harnesses (e.g. Antigravity) is an agent
scratch/sandbox dir that is *different* from the user's project. Save it to:

> **`<project-root>/docs/problem-description/<name>.html`** — where `<project-root>` is the
> user's open project. Create `docs/problem-description/` if missing (`mkdir -p`). `<name>` =
> `YYYY-MM-DD-<topic>-walkthrough` (diagram) or `<topic>-explained` (tables).

This is the rule most often dropped on a long read, and the one harnesses get wrong:
- **Do NOT write it to your agent scratch/sandbox/working directory** (e.g. Antigravity's
  `~/.gemini/antigravity/brain/<id>/scratch/`). That hides the file from the user.
- **Do NOT drop it in the project root** or under a generic name like `walkthrough.html`.
- Resolve `<project-root>` to the **actual open project** (e.g.
  `C:\Repo2\my-app\docs\problem-description\…`), never a literal `<project-root>` placeholder.

**Verify-and-move — mandatory final action.** Harnesses often ignore a "save here" instruction
and write to their own default location anyway. So after writing the file, **get its absolute
path and check it is inside the open project's `docs/problem-description/`.** If it landed
anywhere else — a scratch/sandbox/temp dir, the project root, or a generic filename — **move it**
to `<project-root>/docs/problem-description/<name>.html` now (create the folder first).
**Exception:** if the user specified an explicit path, honor *that* path and skip the move. The
skill is **not done** until the file is in the right place; then report its final absolute path.
(If no project is open, *or* your harness genuinely cannot write into the project, save to the
session scratchpad, report the absolute path, and tell the user to move it.)

## Architecture — one engine, plug-in mode packs

A generated walkthrough is **assembled at generation time** from single-source references
into ONE self-contained `.html` (no build, no external assets):

```
walkthrough.html  =  references/walkthrough-engine.html   (§ the shared engine)
                  +  references/mode-<name>.html           (§ ONE chosen mode pack)
                  +  references/term-drilldown.html        (§ the drawer, optional)
                  +  authored scenes[] + GLOSSARY          (the bootstrap)
```

- **The engine** owns the step loop, navigation, `:root` palette tokens, the canonical
  nested narration, the 5 SVG markerheads, `RENDER_HOOKS`, and `modeRenderers`. Never edit
  it to add a mode.
- **A mode pack** registers exactly one renderer — `modeRenderers['<name>'] =
  {registry, clear, <setters>, assertRegistryComplete}` — plus its content DOM and state
  CSS. Each pack is verified by **assembly**, not by opening it raw.
- **Assembly is a script:** `scripts/assemble-walkthrough.py` does the splice
  deterministically; `scripts/check-walkthrough.py` is the mandatory post-assembly
  self-test (the no-build safety net).

### Pick the mode — flat decision table

Ask **"what is the problem ABOUT?"** (one distinct noun per row) and read across:

| Mode | Problem is ABOUT… | NOT when → use | Pack |
|---|---|---|---|
| **diagram** | data flow between components (A→B→C) | rows changing state → tables | `references/mode-diagram.html` |
| **tables** | rows changing state under FK/cascade rules | one entity's lifecycle → state-machine | `references/mode-tables.html` |
| **state-machine** | one entity's legal state transitions; an illegal/stuck transition | many rows mutating → tables | `references/mode-state-machine.html` |

Sharp disambiguators: **state-machine** = "ONE entity's status transitions" (*not* "many
rows mutating" → tables); a future **timeline** = "WHEN it happened / ordering" (*not* "what
connects to what" → diagram). Tie-break: **when in doubt → diagram**. Every new mode row
must name its nearest neighbour in the "NOT when" column.

## When to Use This Skill

- User wants an interactive walkthrough of a non-trivial technical problem
- Verbal/text explanation has failed and the user is still confused
- The problem involves multiple components or entities + a chain of cause-and-effect
- The "aha moment" hinges on seeing data move through the system
- Teaching a concept where the reader benefits from controlling pace

**Don't use when:**

- The answer fits in 1-3 sentences
- It's a "what does X mean?" definition question
- It's a simple bug fix where understanding is trivial
- The user wants to read code (use `drive-to-legacy` instead)
- The user wants a polished UI/component (use `frontend-design` instead)
- The user wants to *find* the bug, not *teach* it (use `debug-mantra` instead)

## The Process — 6 Phases

### Phase 0 — Confirm the artifact is wanted

Before generating ~500 lines of HTML, ask:

> "อยากได้ interactive step-by-step walkthrough (HTML page เปิดในเบราว์เซอร์), หรือคำตอบสั้นๆ พอ?"

**Skip Phase 0** if the user explicitly asked for "walkthrough", "animation", "visualization", "step by step", "ทำ animation", "diagram", "interactive", or similar artifact-shape language.

**Then ask the second artifact-shape question — the app screen mock:**

> "อยากให้ walkthrough มี mock หน้าจอจริงของแอป (เช่น grid/form ที่ผู้ใช้เห็น) ด้วยไหม, หรือเอาแค่ diagram ของ flow?"

Ask this whenever the problem is visible *on a screen* — a wrong number in a column, a
button that is disabled, a row that vanishes. A mock earns its place because the reader
recognizes the screen they actually use, which turns an abstract column name into the cell
they have looked at a hundred times. Skip the question only when nothing about the problem
reaches the UI (a build gate, a migration script, a server-side race).

If they say yes:
- **Build the mock from the mode pack's own state model** — render the changing cells as
  `.comp` groups registered in the renderer's `COMPONENTS`, so the pack's existing state
  CSS (`active`/`error`/`done`/`locked`) drives them. Do NOT invent new CSS states or hexes.
- **Match the real columns**, in the real order, read off the component source — not from
  memory of what the screen probably shows.
- **Fill the cells with MEASURED values if the system is live and queryable.** One
  read-only query beats invented rows, and grounded data routinely surfaces a sharper
  story than the one you set out to tell.

### Phase 1 — Identify the core misunderstanding AND pick the mode

Articulate these in one sentence each:

1. **The ONE concept** the reader should grasp by the end (e.g., "the UPDATE-on-ctg_name trick is what acquires the row-level write lock")
2. **The misunderstanding** they have now (e.g., "they think the workflow and the counter entity are two unrelated things")
3. **The prerequisites** they already have (e.g., "they know Dataverse entities and that workflows trigger on Create")
4. **The unfamiliar terms** — list the terms the narration will use that fall *beyond*
   the prerequisites (domain jargon, schema names, project concepts). These become
   **drillable terms** (Phase 4). Read the project's `CONTEXT.md` (or the mapped context
   via `CONTEXT-MAP.md`) and pull the definition for each term that exists there; for a
   beyond-prerequisite term **not** in the glossary, write a one-line definition yourself.
   A term the reader already knows is **not** made drillable — over-marking turns the
   narration into a sea of dotted underlines.

Then pick the mode using the "How to choose" rule above. Tell the user which mode you're using in your first message.

If you can't articulate (1) and (2) in one sentence each, **ask the user before continuing**. Vague misunderstandings produce vague walkthroughs.

### Phase 2 — Choose concrete data

Replace abstract entities with realistic, culturally appropriate data.

**Data Quality Checklist:**

- [ ] ≤ 4 entities (boxes or tables) of any one kind — more is noise
- [ ] Names read aloud naturally ("BMW Group", "ครอบครัวสมศรี" not "Customer A", "Family A")
- [ ] Numbers small enough to mental-math (`5`, `42`, `80฿` — not `47,392.18฿`)
- [ ] **Identifiers must not look like sequence numbers** — if a sequence appears in the output (e.g., booking numbers 00001, 00002), avoid IDs like `cargo-1`/`cargo-2` that the reader will confuse for those. Prefer letter IDs (`cargo-A`, `cargo-B`) or source-tagged labels (`cargo (Portal)`).
- [ ] At least one element participates in EVERY problematic path — so when the conflict step lights up, it's visually obvious on one element
- [ ] Schema names match the user's actual codebase (`ctg_runningnumber`, `BudgetTransactions` — not `Counter`, `Table1`)
- [ ] Cultural fit — default to Thai narration for Thai users; technical terms (workflow, CodeActivity, EntityReference, transaction) stay in English

**Bad → Good examples:**

| Bad | Good |
|---|---|
| `Entity A` references `Entity B` | `BMW Group` owns `cargo-A` |
| `cargo-1, cargo-2, cargo-3` (collides with booking #1, #2, #3) | `cargo-A, cargo-B, cargo-C` or `cargo (Portal)`, `cargo (CIT)` |
| `Table1`, `Table2` | `ctg_runningnumber`, `ctg_cargodetail` (real schema names) |
| `value1=100` | `accountnumber="BMW"` |

### Phase 3 — Sequence the steps

Build a domino chain. Each step adds **one** new piece of state.

**Standard skeleton (diagram mode):**

| Step | Purpose |
|---|---|
| **0** | Overview — show all components + arrows in idle state. No action. Reader builds mental model. |
| **1** | Trigger — what initiates the flow? (Light up the triggering component.) |
| **2..N** | Single-actor flow — ONE component activates per step, ONE arrow fires per step, ONE value shown flying along it. State accumulates visibly. |
| **N+1** | **The key question** (REQUIRED) — pose a question the reader must answer in their head before the concurrent / failure scenario reveals the answer. |
| **N+2..M** | Concurrent / failure scenario — show 2-3 actors racing, blocking, or conflicting. |
| **M+1** | Counter-example — what would go wrong with the naive approach (e.g., "what if we used MAX()+1?"). |
| **M+2** | Summary / resolution — why the architecture works AND its trade-offs / side-effects. |

**Standard skeleton (tables mode):**

| Step | Purpose |
|---|---|
| **0** | Setup — show all tables + all rules. No action. |
| **1** | Trigger — user action starts the chain. |
| **2..N** | Domino effects — ONE rule fires per step, affecting specific named rows. |
| **N+1** | Key question. |
| **N+2** | Conflict / failure step. |
| **N+3** | Resolution with side-effects named. |

Each step has:

- **Scene title** — imperative, ≤ 12 words ("Step 8 — 🔒 AcquireWriteLock: UPDATE ctg_name forces row X-lock")
- **Narration** — 2-5 sentences answering WHY (not just WHAT). Why does this fire? Why is the value chosen? Why does this matter to the reader?
- **Visual change** — light up the active component/row, fire the active arrow, show the flying-value label, highlight the active rule

### Phase 4 — Author the bootstrap, then assemble

You write **only the bootstrap** (the per-walkthrough content); the engine + mode pack +
drawer are inlined by the assembler.

1. **Read the chosen mode pack** (`references/mode-<name>.html`) to learn its renderer's
   setters and its content-DOM ids (e.g. state-machine: `setNode`/`setEdge` over
   `NODE_LIST`/`EDGE_LIST`; diagram: `setComp`/`setArrow`/`setLabel`/`setText`; tables:
   `setRowClass`/`setBadge`/`setCell`/`setRule`). If the pack's built-in content DOM doesn't
   fit your problem, edit a COPY of the pack's `§HTML` (its registry ids must match).
2. **Write a bootstrap** (a `.js` snippet) with, in order:
   - `MODE = '<name>';`
   - `const { setNode, setEdge } = modeRenderers[MODE];` — alias the pack's setters to flat
     names so scenes read like `setNode('stDraft','done')`.
   - `const GLOSSARY = { … };` — your drillable terms (only if using the drawer). Each entry
     `{term, short, seeAlso, source}` with `source: 'CONTEXT.md'` (quote the glossary) or
     `'authored'` (a fallback for a term absent from `CONTEXT.md`; consider offering to add it).
     Mark terms in narration: `<span class="term" data-term="key">…</span>`.
   - `const scenes = [ … ];` — one function per step, each fully describing DOM state via the
     flat setters + `setNarration(cls, title, bodyHTML)` + `show()/hide()` on `.wt-panel`s.
   - `TOTAL = scenes.length - 1; modeRenderers[MODE].assertRegistryComplete(); buildProgressDots(); render(0);`
     — the `assertRegistryComplete()` call makes any DOM-id-not-in-registry drift throw at load.
3. **Assemble:**
   ```
   python scripts/assemble-walkthrough.py --engine references/walkthrough-engine.html \
     --mode references/mode-<name>.html --drawer references/term-drilldown.html \
     --title "<the walkthrough's on-screen heading>" \
     --out <project-root>/docs/problem-description/<name>.html --bootstrap your-bootstrap.js
   ```
   Drop `--drawer` if the walkthrough has no drillable terms. `--title` fills both the
   browser-tab `<title>` and the on-screen `<h1>` (it falls back to the output filename stem,
   so the placeholder never ships — but pass a real title).
4. **Self-test (mandatory):** `python scripts/check-walkthrough.py <out>.html` — it must pass.

**The drawer is framework, not a scene** — never call `openTerm`/`closeDrawer`/`GLOSSARY`
from a scene; it self-registers into `RENDER_HOOKS` so stepping closes it for free.

**Critical rule:** every scene must fully describe DOM state from scratch. Never
`createElement`/`appendChild` from a scene. Declare every panel up front (`.wt-panel hidden`)
and toggle with `show()/hide()`. The engine runs `RENDER_HOOKS` → the mode's
`clear(registry)` → `scenes[step]()` on every render.

### Phase 4.5 — Save and report

**Save the artifact INSIDE the open project, in a dedicated folder** (see the Output-location contract near the top). Resolve the project root to a real absolute path, never a placeholder. Save path, in priority order:

- **The user specified a path** → use it exactly.
- **A project/workspace is open (the normal case)** → `<project-root>/docs/problem-description/YYYY-MM-DD-<topic>-walkthrough.html` (diagram mode) or `<project-root>/docs/problem-description/<topic>-explained.html` (tables mode), where `<project-root>` is the user's open project/workspace — **not** your agent working/scratch directory, which may differ. **Create `docs/problem-description/` if it does not exist** (`mkdir -p`) so it does not mix with specs, ADRs, and plans in the `docs/` root. **Never** write it to your agent scratch/sandbox directory (e.g. `~/.gemini/antigravity/brain/<id>/scratch/`) when a project is open — that hides the file from the user.
- **Only when there is genuinely no open project** (a throwaway question with nowhere to put it): use the session scratchpad directory and tell the user the absolute path. Do **not** default to a hard-coded personal path like `c:/Repo2/t/`. This branch is the exception, not the default — if a project is open, the bullet above wins.

**Then run the verify-and-move check (mandatory)** — see the Output-location contract near the top: get the file's absolute path, confirm it is inside `<project-root>/docs/problem-description/`, and if the harness wrote it elsewhere (scratch/sandbox/temp, project root, generic name), move it there before reporting — **unless the user specified an explicit path (bullet 1), in which case honor that path**. The skill is not done until the file is in the right place.

Report back:
- The absolute path of the generated file
- Which mode (diagram or tables)
- How many steps
- "Open in your browser — `ถัดไป →` / `← ย้อนกลับ` / `↻ เริ่มใหม่` ปุ่มควบคุม pace"

### Phase 5 — Verify before declaring done

Run the self-test checklist:

- [ ] Every step's narration answers WHY, not just WHAT
- [ ] The "key question" step exists and forces reader thinking
- [ ] The resolution / summary step explicitly names side-effects and trade-offs
- [ ] `scenes.length - 1 === TOTAL` in JS (step 0 is included; TOTAL is the index of the last step)
- [ ] Every `getElementById(id)` call has a matching `id` attribute in the HTML
- [ ] Every id a scene targets resolves to an `id=""` in the DOM (the checker's scene-id pass), and `modeRenderers[MODE].assertRegistryComplete()` passes at load (DOM ids ⊆ registry)
- [ ] Going `← Previous` from any step returns clean state (idempotent scene rule)
- [ ] `↻ Reset` returns to step 0 with no residual highlights, badges, or visible panels
- [ ] No `appendChild` / `createElement` inside any scene function
- [ ] **No identifier collision:** sequence numbers in the output don't conflict with element IDs (e.g., don't use `cargo-1` when booking numbers `00001` will appear)
- [ ] **Drill-down referential integrity:** every `data-term="X"` has a `GLOSSARY[X]`
      entry, and every `seeAlso` key resolves to a `GLOSSARY` entry
- [ ] **Grounding:** every `GLOSSARY` entry marked `source: 'CONTEXT.md'` matches the
      glossary wording; `'authored'` is used only for terms absent from `CONTEXT.md`
- [ ] **Drawer is orthogonal:** no scene references the drawer
      (`openTerm`/`closeDrawer`/`termDrawer`/`GLOSSARY`); the mode's `clear()` does not
      touch it; `render()` runs `RENDER_HOOKS` first (the drawer self-registers
      `closeDrawer`); `Next`/`Prev`/`Reset` close the drawer and leave no residue
- [ ] **See-also hops:** clicking a see-also chip swaps the drawer; `← back` restores the
      prior term; with no `CONTEXT.md`, drillable terms still work via `authored` defs
- [ ] **Post-assembly self-test passes:** `python scripts/check-walkthrough.py <out>.html`
      reports OK (self-contained, `MODE`+renderer ok, `RENDER_HOOKS`-first, scenes clean, order ok)

If any item fails — fix before reporting done.

## Design Decisions — engine + mode packs

**Color tokens live once in the engine's `:root`** (`walkthrough-engine.html`); never
introduce a new hex. The semantic core: `--accent #5fb4ff` (info/active),
`--amber #ffd479` (firing), `--magic #b070ff` (locked/key), `--warn #ffaa00`,
`--success #4ade80` (done), `--error #ff5757` (error/conflict), `--bg #0a0e14`,
`--panel #1a2330`. SVG marker fills come from the engine's fixed 5 markerheads
(`arrowhead`/`-active`/`-magic`/`-done`/`-error`), or `var(--token)` — never a raw hex.

**The renderer contract** every mode pack implements:

```js
modeRenderers['<name>'] = {
  registry: { /* one+ flat id-arrays */ },
  clear(reg) { /* reset every registry id to idle; hide .wt-panel; restore [data-default] */ },
  /* replace-only setters, e.g. setNode(id,state) */
  assertRegistryComplete() { /* throw if a DOM id is absent from the registry */ },
};
```

**Each pack documents its own states** (in the pack file's comments) — don't duplicate them here:
- `references/mode-diagram.html` — `setComp`/`setArrow`/`setLabel`/`setText`; comp states `active/firing/locked/blocked/done/error/dimmed`; arrow states `active/magic/done/error/dimmed`.
- `references/mode-tables.html` — `setRowClass`/`setBadge`/`setCell`/`setRule`; row states `target-delete/target-setnull/target-conflict/fixed/deleted`; badges `delete/setnull/conflict`.
- `references/mode-state-machine.html` — `setNode`/`setEdge`; node states `current/passed/illegal/stuck/key/dimmed`; the illegal/stuck transition IS the conflict step.

## Idempotent Scenes — The One Rule (both modes)

**Every scene function must fully describe DOM state from scratch. Never build cumulatively.**

Why: if scene 4 calls `appendChild(panel)` and scene 5 doesn't remove it, then `← Previous` from scene 6 to scene 4 leaves the panel duplicated. Idempotent rendering eliminates this entire class of bugs.

How:

1. Declare every possible UI element in the initial HTML, hidden with `.hidden` class (or with default content for live-text fields)
2. Scenes call `show('panelId')` / `hide('panelId')` to toggle visibility
3. Scenes call the mode's replace-only setters (e.g. `setNode`/`setEdge`, `setComp`/`setArrow`, `setRowClass`/`setBadge`) — these REPLACE state, never append
4. Scenes call `setText`/`setCell` to update live-text fields
5. The engine's `render()` runs `RENDER_HOOKS` (e.g. the drawer's `closeDrawer`) → the mode's `clear(registry)` → ONLY the current scene function

**No scene function ever does:**

- `document.createElement(...)`
- `el.appendChild(...)`
- `el.classList.add(...)` (use the wrapper setters, which replace)
- `el.innerHTML += ...`

If you need to "add" a panel mid-walkthrough, declare it once in the initial HTML with `.hidden` and `show()` it from the scene.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Wrong mode picked — tables for a flow problem | Use the flat selection table. Flow → diagram. Row state → tables. One entity's transitions → state-machine. |
| Auto-playing animation that races past the reader | Manual `Next →` only. Reader controls pace. |
| Abstract names (`A`, `B`, `Table1`, `Customer1`) | Real, domain-flavored, culturally appropriate names. |
| IDs collide with output sequence numbers (`cargo-1` vs booking `00001`) | Use letter IDs (`cargo-A`) or source-tagged labels (`cargo (Portal)`). |
| Each step changes too many things at once | One component activates per step. One arrow fires. One value moves. |
| Narration says WHAT, not WHY | Every narration explains the rule's reason. |
| No "key question" step | The conflict/concurrency reveal needs a thinking-pause beforehand. |
| Fix without side-effects called out | Resolution always has trade-offs — name them. |
| Cumulative-replay rendering | Idempotent scenes only — no `appendChild` from scenes. |
| 300+ lines of HTML for a 2-step problem | This skill is for problems with 4+ chained effects. Smaller problems → just chat or use a single mermaid diagram. |
| `← Previous` leaves stale state | Scene functions must fully describe state, not deltas. |
| Same element never highlighted in the conflict step | Pick concrete data so at least one element is hit by every problematic path. |
| Flying-label rect too small / clipped text | Measure your label text length; widen the `<rect>` to fit comfortably. |
| Invented term definitions instead of CONTEXT.md | Source from the project glossary; author a fallback only when the term is absent (ADR 0017). |
| A helper builds `data-term` dynamically (string-concatenating the key into the attribute) | `check-walkthrough.py` scans for the literal attribute, so the run fails — and a helper defeats the referential-integrity guarantee anyway. Keep spans literal; for DRY use one const per term holding the COMPLETE span. |
| Over-marking — every other word is drillable | Mark only terms *beyond* the reader's stated prerequisites. |
| Copying the drawer/engine code into a mode pack | The primitive lives once; inline via the assembler (`--drawer`, engine §). A pack is verified by assembly, not raw. (ADRs 0019, 0020) |
| A scene opens/closes/reads the drawer | The drawer is reader-driven framework, never scene state. Keep scenes pure. |
| `data-term` with no `GLOSSARY` entry (drawer no-ops) | Every `data-term` and `seeAlso` key must resolve to a `GLOSSARY` entry. |
| Editing `walkthrough-engine.html` to add a mode | A mode is a pack registering one renderer — adding a mode is **zero engine edits** (ADR 0020). |
| Hand-splicing the assembled `.html` | Use `scripts/assemble-walkthrough.py`, then `scripts/check-walkthrough.py` — a bad manual splice yields a self-contained-but-broken file. |
| Introducing a new color hex | Reuse `:root` tokens / the 5 markerheads; the checker + review reject new tokens (ADR 0022). |
| Apostrophe inside a single-quoted GLOSSARY string breaks the bootstrap JS | Use double-quotes or reword; `check-walkthrough.py` now `node --check`s the assembled `<script>`. |

## Reference files (the always-present scaffolds)

Build every walkthrough from these bundled files in this skill's folder:

- `references/walkthrough-engine.html` — the shared engine (also a standalone runnable demo).
- `references/mode-diagram.html` · `references/mode-tables.html` · `references/mode-state-machine.html` — the mode packs (each runs its own demo via assembly).
- `references/term-drilldown.html` — the term drill-down drawer.
- `scripts/assemble-walkthrough.py` — the deterministic generation splice.
- `scripts/check-walkthrough.py` — the mandatory post-assembly self-test.

Author's local examples (structural inspiration only — **may not exist** on your machine; skip if absent):

- `c:/Repo/glasshull repo/glasshull/docs/2026-05-28-polaris-booking-number-diagram.html` — a 22-step diagram-mode concurrency walkthrough.
- `c:/Repo2/t/cascade-paths-explained.html` — a 7-step tables-mode SQL 1785 cascade walkthrough.
