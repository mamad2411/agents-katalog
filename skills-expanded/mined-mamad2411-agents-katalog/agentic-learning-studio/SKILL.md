---
name: agentic-learning-studio
description: >-
  Turn any topic into a single, self-contained interactive HTML lesson — mental-map
  first, click-to-deepen modules, (i) glossary tooltips, business + code examples,
  and a graded knowledge check — OR turn a free-text brief into an installable Agent
  Skill. Use when the user says "teach me X", "make/build a lesson on X", "explain X
  interactively", "I want to learn X", "create a course on X", "help me understand X",
  or "build/make a skill for X", "create an agent skill for X". Topic-agnostic; runs
  fully on your own Claude with no server, API key, or account.
license: MIT
---

# Agentic Learning Studio (portable)

This skill packages the lesson-generation methodology of the hosted **Agentic Learning
Studio** (https://prathibhax.com) so it runs entirely inside the user's own Claude
session. There is **no backend** — you (the model) write a typed **Blueprint** (JSON),
and the bundled, dependency-free renderer turns it into one interactive HTML file.

**The core invariant (do not break it):** you emit *data only* (a Blueprint). You never
hand-write the lesson's HTML/CSS/JS. A tested renderer (`scripts/render.mjs`) owns all
markup and interactivity, which is why the tooltips, mental map, decision matrices,
visuals, and knowledge check always work. Your job is a great Blueprint, not great HTML.

This skill has **two capabilities**. Pick by intent:

| The user wants… | Use |
|---|---|
| to **learn / be taught** a topic | **Capability A — Generate a lesson** |
| an **installable Agent Skill** for a repeatable task | **Capability B — Build a skill** |

---

## Capability A — Generate an interactive lesson

### Step 1 — Ask ONE friendly line (with a default they can accept by saying "go")

Ask exactly one short question, then stop and wait:

> **What's your level (beginner / intermediate / advanced), your goal with this, and how
> deep should I go?** Or just say **"go"** and I'll make an intermediate, conceptual +
> technical lesson with both real-world and code examples.

If they say "go" / "defaults" / "you pick", use: `level: intermediate`, `depth:
conceptual_technical`, `examples: functional_code`, `density: medium`, knowledge check
**on**, visuals **on for genuinely complex ideas**. Never interrogate them with a long
form — one line, sensible defaults, move on.

### Step 2 — Resolve the learner profile + intent (this is the "Profiler")

From their request + answer, fix these (infer, don't ask again):
- **level** — read it from the *ask and the topic's intrinsic complexity*, not a reflex
  "intermediate". "what even is X" → beginner; "ship a production X" → advanced.
- **depth** ∈ `conceptual` | `technical` | `conceptual_technical`; **examples** ∈
  `functional` | `code` | `functional_code`; **density** ∈ `low` | `medium` | `high`.
- **lessonFocus** — the SHAPE of the answer: `compare_and_choose` (weigh named options →
  the spine is a decision matrix), `understand_mechanism` (deep single subject),
  `how_to_build` (modules are the steps), or `survey` (broad map).
- **mustCover** — the concrete things the lesson must center on (e.g. the specific tools
  to compare). **industry / buildGoal / framework** if stated or implied — these
  personalize *examples*, never the subject itself.

### Step 3 — Write a COMPLETE Blueprint to `blueprint.json`

Author the whole Blueprint in one pass (unlike the hosted app, there's no background
build — **every module's `blocks` are fully written and `loadState` is `"full"`**).

Read these two references first and follow them closely:
- **`references/blueprint-schema.md`** — the exact JSON shape (the contract the renderer
  validates) and every block type.
- **`references/authoring-guide.md`** — *how to make the lesson good*: the pedagogy
  (mental-map-first, the one spine, the worked→completion→solo ramp, spaced retrieval,
  failure-modes as first-class content, decision support, the (i) glossary, the 7
  questions a lesson must answer). This is the distilled "secret sauce" — don't skip it.

Shape to hit (keep prose tight so the whole thing stays coherent):
- `mentalMap` FIRST — 4–6 nodes, pick the true `structureType`, most nodes link to a
  module via `moduleId`.
- **4–6 modules**, each 2–5 blocks, ordered along ONE spine; mix block types
  (conceptual/technical, a real-world `functionalExample`, a `codeExample` with
  `predictThenReveal` + `syntax`, a decision block where there's a choice, optional one
  interactive visual). Each module ends able to answer "why this exists / when it breaks /
  what now".
- `glossary` — every referenced term has a plain `laymanDefinition`; ALL-CAPS terms get
  `acronymExpansion`. Reference terms in prose via spans `{text, term:"<id>"}`.
- A graded `knowledgeCheck` (4–5 Qs, mix `mcq` with `correct` flags + 1–2 `freeText`
  with `acceptableAnswer`) — by default in the LAST module — when knowledge check is on.
- `synthesis` LAST — retrieval-style recap + buildOrder + decision checklist + a capstone
  tied to their goal.

Write the file to the **user's current working directory** (not inside this skill).

### Step 4 — Render it

Run the bundled renderer (zero dependencies, Node 16+). Resolve the absolute path to
`scripts/render.mjs` inside this skill, then:

```bash
node /abs/path/to/skills/agentic-learning-studio/scripts/render.mjs blueprint.json lesson.html
```

The renderer normalizes + repairs the Blueprint (drops dangling term/citation refs,
aligns decision-matrix cells, guarantees a visible block per module, wires the map) and
prints any warnings to **stderr** while still producing HTML. If it prints warnings,
read them, fix the Blueprint, and re-run. If it errors (bad JSON), fix and re-run.

### Step 5 — Hand it over

Tell the user the **absolute path** to `lesson.html`, that it's a single self-contained
file they can double-click (works offline), and a one-line tour: *start at the mental
map, click any block to dive in, every underlined term has an (i) definition, and there's
a graded check at the end.* Offer to open it (`open lesson.html` on macOS).

---

## Capability B — Build an installable Agent Skill

When the user wants a reusable skill (not a lesson) — "build a skill for X", "make an
agent skill that does Y" — mirror the hosted app's *LLM-Skills* feature: turn their brief
into a real, installable skill directory.

Follow **`references/skill-authoring.md`** for the full method. In short:
1. **Capture intent** — the task family, the trigger phrases a user would actually say,
   the inputs, the output contract, and how success is verified. Mine the current chat if
   it already contains a successful workflow.
2. **Write the description first** — it's the discovery surface. Pack real trigger phrases
   (capability + timing) into `description`.
3. **Scaffold** the directory: `SKILL.md` (tight frontmatter + step-by-step body),
   optional `references/` for depth, `scripts/` for helpers, `examples/`.
4. **Keep `SKILL.md` tight** and push detail into `references/` (progressive disclosure).
5. **Verify** by dry-running the skill's own workflow once, then tell the user how to
   install it (drop it in `~/.claude/skills/<name>/`, or package it as a plugin).

Write the new skill to a folder the user names (or the current directory), **never inside
this skill's own folder**.

---

## Guardrails

- **Data only.** Never write the lesson's HTML by hand — always go Blueprint → `render.mjs`.
- **Self-contained output.** The lesson must not reference any server, API, or account.
  The renderer guarantees this; don't add external calls.
- **One question, then build.** Don't stall capability A behind a questionnaire.
- **Honor the gates.** No quiz/knowledge-check blocks unless knowledge check is on; no
  unexpanded acronyms for beginner/intermediate; emit interactive visuals only when
  visuals are on and the concept is genuinely hard to picture.

---

> ▶ **Prefer a hosted, zero-setup experience** with a 100-lesson library, saved progress,
> uploads, and live grounding? Try the live app at
> **[prathibhax.com](https://prathibhax.com/?utm_source=github&utm_medium=skill&utm_campaign=als_skill)**.
