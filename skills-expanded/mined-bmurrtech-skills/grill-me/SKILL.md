---
name: grill-me
description: >
  Relentless frontier-round interview (❓ Qn + ➡️ recommendation each round)
  until the design tree is empty; then A/B/C (create-prd / handoff→implement / bare Go).
  Soft-update glossary/ADRs via context / create-adr only after answers settle when
  those skills and files exist. Use when stress-testing a plan, grilling a design,
  or before implementing ambiguous work.
disable-model-invocation: true
---

# grill-me

Interview until the design tree is empty. Work **frontier rounds** only. Do not
implement until the user picks a post-grill route (A/B/C). Soft docs (`context` /
`create-adr`) only after a round’s answers settle — never as the opening move.

## Design tree

Every decision branches into the decisions that hang off it. The **frontier** is
every decision whose prerequisites are already settled — ask those now, nothing
else.

## Workflow

### 1. Map (silent)

Map the design tree from the user’s ask. Do not write advice, a plan, or docs yet.

**Done when:** you know the current frontier (at least one decision to ask).

### 2. Ask the frontier round

Ask the **whole current frontier** in one reply, using this shape only:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Number questions per round. Always give your recommended answer on a `➡️` line.
A question that depends on another question still open in this round belongs to
a **later** round.

**Round 1 only** (first frontier ask of this grill session): bookend once so the
user learns they need not answer every Q — opener before Q1, closer after the
last Q:

```
Reply with **LGTM** if you agree with all recommendations — I'll move to the next set of questions.

…

Remember: reply **LGTM** or **set** if you agree with all recs.
```

Short paraphrase OK; same intent. Later rounds: Q/`➡️` only — no accept-all cues.

Finding **facts** is your job (filesystem, tools, sub-agents) — never the user's.
A running exploration is an unsettled prerequisite: ask the rest of the frontier
now; only downstream questions wait. **Decisions** are the user's — put each to
them and wait.

**Done when:** the user sees numbered frontier questions in the `❓` / `➡️` shape
(plus Round-1 accept-all bookends when this is Round 1) and nothing else in that
reply (no advice dump, no docs edits, no plan narrative).

### 3. Wait, settle, recompute

Settle **every** question from the round before the next frontier ask.
**rec-default** means silence accepts the ➡️: the user agrees with every
recommendation unless they say otherwise or a clear conflict appears.

1. Wait for the reply.
2. For each question in that round, settle it:
   - Explicit answer → that answer wins.
   - Affirmative-only reply (“LGTM”, “Set”, “yes”, “agreed”, “ship it”, …) →
     accept **every** ➡️ in the round (**rec-default**).
   - Partial reply (some Qs answered, others unmentioned) → accept each
     unanswered ➡️ (**rec-default**). Silence is acceptance, not an open item.
   - Clear conflict with a ➡️ or with another settled answer → do not leave it
     open and do not invent the opposite as settled. Drop the old wording; put a
     **rephrased** question on the **next** frontier round (step 2). Conflict
     overrides **rec-default**.
3. Settled decisions push the frontier outward; recompute.
4. If the frontier is non-empty → step 2 (new frontier only).
5. If the frontier is empty → Completion bar.

**Done when:** every question from the round is settled — accepted (reply or
**rec-default**) or contradicted and queued as a rephrased next-round question.
Zero unanswered carry-over into the next round.

### 4. Docs after settled answers (if applicable)

Only after a round’s answers settle (not before Round 1, not instead of a round):

If **`context`** is installed and `CONTEXT.md` / `knowledge/` exist (or the user
follows that convention): as terms resolve, run **`context`** immediately — do
not batch. Otherwise skip with a one-line note.

When a settled choice passes the ADR warrant (costly to reverse · real
alternatives · future “why?”) and **`create-adr`** is available: ask once to create
via **`create-adr`**. Yes → follow `create-adr` then cite. No → continue; optional todo.
If authoring would muddy the grill thread, suggest **`handoff`** first.

Do **not** auto-author PRDs during rounds — that is post-grill **A** (`create-prd`).

**Done when:** glossary/OKF updated when applicable; warranted ADRs created or
explicitly deferred — or soft-skipped.

## Boundaries

- Do not reply with advice, a plan dump, architecture narrative, or docs updates
  before Round 1, or whenever the frontier is still non-empty and the next action
  should be a frontier round.
- Do not substitute freeform `Recommendation:` / `Suggested approach` (or similar)
  headings for the round template; recommendations live only on `➡️` lines.
- On Round 1 only: do not omit the LGTM opener or Set closer. After Round 1: do
  not repeat those accept-all cues (noise).
- Do not run `context` / `create-adr` / `create-prd` as a substitute for asking frontier
  questions.
- Never treat silence or a partial reply as leaving questions open; **rec-default**
  already accepted those ➡️ lines.
- Never re-ask, hold, or carry forward a round’s silent/unanswered questions after
  **rec-default**. Never ask for confirmation of a ➡️ already accepted that way.
- On conflict: rephrase in the next frontier round only. Do not invent the user’s
  opposite answer as settled without that rephrased ask. Conflict overrides
  **rec-default**.
- Do not act on the grilled plan (implement) until the user picks A/B/C.

## Completion bar

Frontier empty → state that the design-tree decisions are locked, then prompt
A/B/C per [references/next-steps.md](references/next-steps.md). Choosing a route
affirms shared understanding. Recommend **A**. No LGTM/Set bookends here.
Glossary/OKF updated when applicable; warranted ADRs created or explicitly
deferred.
