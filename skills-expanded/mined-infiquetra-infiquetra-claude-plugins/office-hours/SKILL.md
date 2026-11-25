---
name: office-hours
description: The two-mode frame-finding front door for early Infiquetra thinking. Startup mode runs the six market/customer forcing questions (stage-aware); Builder mode runs discovery/shaping for infra, workflow, and internal-tooling. Finds the right frame, then routes — to /ideate, /brainstorm, /plan, or /strategy. Triggers on "office hours", "is this worth building", "help me think through this", "I have an idea but I'm not sure what it even is", "what's even the right frame here".
---

# Office Hours

Office-hours is the **frame-finding front door**. It answers the one question that sits upstream of
every other Think-phase command: *"What is even the right frame here?"* It does not generate idea
lists, write requirements, or build anything. It pressure-tests a half-formed ask until you can name
the real problem and the key assumptions under it — and then it routes to the command that does the
next real thing.

Two modes, one engine, one voice:

- **Startup mode** — the six market/customer forcing questions, **stage-aware**. Infiquetra is a real
  startup heading toward paying customers but currently pre-revenue greenfield, so pre-product runs in
  a **hypothesis-forming register**, not an evidence-auditing one.
- **Builder mode** — discovery and shaping for infra, workflow, and internal-tooling work. This is
  Infiquetra's high-frequency mode. It carries real rigor; it is not a one-liner.

## Position in the lifecycle

Office-hours sits at the very front of the Think phase, before `/ideate`, `/brainstorm`, and `/plan`:

- `/office-hours` answers: **"What is even the right frame?"**
- `/ideate` answers: "What are the strongest ideas worth exploring?" (many ideas)
- `/brainstorm` answers: "What exactly should one chosen idea mean?" (deepen one)
- `/plan` answers: "How should it be built?" (build it)
- `/strategy` answers: "What direction are we even pointed?" (direction)

The handshake with its neighbors is deliberate. `/ideate` routes an **unframed ask** here ("There's no
settled subject for the agents to work on — `/office-hours` is built for finding the frame first").
`/brainstorm` **bounces back** here when a topic turns out to be open thought-partner work rather than
a concrete requirements ask. Keep that handshake intact: office-hours is where unframed work goes to
get a frame, and the place it points to once it has one.

Office-hours is **upstream of execution**. It routes to a *next command*, never to an execution
backend. It does not consume `references/operator-choice.md` and never selects a runner — that is the
job of the commands it routes to.

## Core principles

1. **Frame-finding ONLY.** The deliverable is a settled frame plus a route — not ideas, not
   requirements, not a plan, not code. Stop the moment you can name the real problem and a next
   command. Do not keep digging past that point looking for more.
2. **HARD GATE (absolute).** Never implement, never write a plan, never scaffold, never file an SDLC
   issue from this session. Office-hours diagnoses and routes; it does not execute. This gate holds
   even when the operator says "just build it" — the answer is "that's `/plan`'s job; here's how to
   hand off to it," not to build.
3. **Anti-sycophancy, re-targeted.** Push hard — but on the right thing. Push on **vagueness** and
   **ungrounded assumptions** (an unfalsifiable hypothesis, an undefined term, a category masquerading
   as a customer, a "make it better" with no failing line named). Do **not** push on the operator's
   judgment or right to pursue the thing. The rigor is aimed at the *framing*, not at the person.
   Push twice, then respect the answer (see escape hatches).
4. **Route always; frame note optional.** Every session ends by naming a concrete next command. A
   written frame note is the *exception*, not the rule — write one only when the frame is substantive
   enough to be worth a durable artifact. The common case is route-only, no file.

## Interaction method

Use the platform's blocking question tool: `AskUserQuestion` in Claude Code (call `ToolSearch` with
`select:AskUserQuestion` first if its schema is not loaded). When you present options, **pre-select the
recommended one** — take a position, then let the operator override. Fall back to numbered options in
chat only when no blocking tool exists or the call errors. In a channel session, inline the choices in
the reply text rather than calling `AskUserQuestion` — follow the redis-channel convention documented
in `saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here). Ask one
question at a time and never silently skip a gate question.

The full question banks, the mode rubric, the pushback patterns, the "never say" list, the escape
hatches, the frame-note template, and the routing rubric live in
`saga/skills/office-hours/references/frame-diagnostic.md`. Load it at Phase 1 and work
from it — do not improvise the diagnostic from memory.

---

## Phase 0: Enter — topic, resume, mode

### 0.1 Topic capture

Take the topic from command arguments, the active artifact, or a `/ideate` / `/brainstorm` bounce. If
none is supplied, ask: "What's on your mind? Name the thing you're chewing on — even if it's fuzzy.
Fuzzy is exactly what this is for." Do not proceed without a topic.

### 0.2 Light resume scan

Glob `docs/office-hours/` for a recent `*-<topic>-frame.md` (a frame note from a prior session, by
matching topic or obvious overlap). If one exists, read it and ask whether to **continue** (summarize
the settled frame so far, pick up its open threads) or **start fresh**. This scan is deliberately
light — office-hours rarely leaves an artifact, so a hit is the exception. **Scan only
`docs/office-hours/`** — never `docs/ideation/`, which belongs to `/ideate`'s resume scan; reading it
here would collide.

### 0.3 Mode selection — detect, ASK when not high-confidence

Two modes, no third. Detect from the topic; **ask** (do not silently auto-route) when the call is not
high-confidence — silent misclassification is the failure this gate exists to prevent.

- **Customer-facing product bet** (a thing that could leave the building and be sold or adopted by an
  outside user) → **Startup mode**.
- **Infra / workflow / internal tooling / learning** (a thing that stays inside Infiquetra and makes
  the operator or the system better) → **Builder mode**. This is the high-frequency case.
- **Genuinely both** — most often a dev-tool that is *itself* the product (the thing we build to make
  ourselves faster might also be sellable) → run **Builder framing for the build**, *plus* one startup
  wedge probe: *"Who is the first paying user if this ever leaves the building?"* This is not a third
  mode — it is Builder mode with a single startup-flavored question stapled on.

State the inferred mode in one plain sentence ("Treating this as a Builder-mode question — internal
workflow tooling") and proceed. When confidence is low, ask which mode fits before running the
diagnostic.

### 0.4 Optional light grounding

A *single* repo or journal scan is allowed when it would sharpen the diagnostic (e.g. "does this
overlap something we already shipped?"). This is **light** — one scan, not `/ideate`'s heavy
multi-source grounding fan-out. Skip it entirely when the topic is conceptual enough that grounding
adds nothing. Never block the diagnostic on a grounding miss.

---

## Phase 1: Diagnostic (mode-specific)

Load `saga/skills/office-hours/references/frame-diagnostic.md` now. Run the
mode-specific diagnostic from it. Ask questions **one at a time** via `AskUserQuestion`, push on each
answer until it is specific and grounded (or the escape hatch fires), and STOP after each question to
wait for the response.

### 1A: Startup mode — the six forcing questions, stage-aware

Run the six forcing questions — **Demand Reality, Status Quo, Desperate Specificity, Narrowest Wedge,
Observation & Surprise, Future-Fit** — using the stage-routing table (pre-product / has-users /
has-paying-customers; the pure-engineering subset is Q2 + Q4 only). The full question text, the
stage-routing table, and the pushback patterns are in the reference.

**Pre-traction register (this is the Infiquetra adaptation).** Infiquetra is pre-revenue greenfield, so
when the stage is **pre-product**, frame each forcing question as **hypothesis-forming, not
evidence-auditing**. Ask for *"the falsifiable bet plus the cheapest test that would prove you wrong,"*
not *"the customer who paid you." Push-twice targets the **vagueness of the hypothesis**, not the
absence of evidence:

- "I think enterprises will want this" gets pushed — **because it is not falsifiable**, not because
  there is no proof yet. Force it to "I bet *this named kind of team* will *do this specific thing*,
  and I'd know I'm wrong if *this* happens."
- Do **not** punish a pre-product founder for having no paying customer — that is the stage, not a
  failure. Punish a bet you cannot state crisply enough to test cheaply.

Apply the anti-sycophancy "never say" list and the escape hatches throughout.

### 1B: Builder mode — discovery / shaping (DEPTH FLOOR: not a one-liner)

Builder mode runs a real discovery register, not a single question. Its bias is toward **the right,
most-capable version of the thing** and **shipping over premature optimization** — but it earns that by
pushing on **grounding** and **leverage**, with its own worked anti-sycophancy / push-twice examples on
infra and workflow vagueness:

- "Make `/plan` better" → push: *"Better how? Which of its lines fails an agent consumer today? Which
  actual work-session did it produce badly?"* "Better" with no failing line named is the vagueness this
  mode pushes on.
- "Speed up the build" → push: *"Speed up which step, measured how? What's slow today and how do you
  know — a profile, a stopwatch, or a vibe?"*
- "We should have observability for X" → push: *"What decision would the observability change? If the
  number came back, what would you do differently? If nothing, it's a dashboard, not a need."*

Reuse the proven internal-work register that `/ideate` and `/brainstorm` already apply (verify before
claiming; ground in the actual repo and journal; name the failing line, not the abstract desire). The
full builder question bank and worked examples are in the reference. Builder mode pushes on grounding
and leverage; it never pushes on the operator's right to build the thing.

### 1C: Mid-session mode-switch

A first-read mode call can be wrong. Self-correct without a restart:

- **Upgrade (builder → startup):** the operator starts framing internal tooling but says "actually
  this could be a real company" or mentions outside customers, revenue, or selling it. Switch
  naturally: *"Okay — now we're talking about a product that leaves the building. Let me ask you the
  harder market questions."* Move to the 1A forcing questions.
- **Downgrade (startup → builder):** the "product" turns out to be an internal tool with no outside
  user — there is no customer because there was never meant to be one. Switch: *"This isn't really a
  market bet — it's a build. Let me reframe around grounding and leverage instead."* Move to 1B.

A misclassification self-corrects mid-flight; it never forces the operator to start over.

---

## Phase 2: Synthesize the frame

When you can name the real problem and the assumptions under it, stop the diagnostic and state the
**settled frame** back to the operator in plain prose:

- **The real problem** — what this is actually about, after the pushback stripped the vagueness.
- **Key assumptions / hypotheses** — what has to be true (and, in pre-product startup framing, the
  falsifiable bets plus their cheapest tests).

Write a **frame note only if it is substantive** — a frame worth preserving across sessions, not a
two-line route. The common case is route-only with no file. When you do write one, put it at:

```
docs/office-hours/<YYYY-MM-DD>-<topic>-frame.md
```

with frontmatter `kind: frame-note` (plus `date`, `topic`, and the command to run next). The
frame-note template is in the reference. **Never write to `docs/ideation/`** — that path belongs to
`/ideate` and a frame note there would collide with its resume scan. Frame notes live in their own
`docs/office-hours/` directory.

---

## Phase 3: Route + HARD GATE

Every session ends by naming the next command and offering **plural clean exits**. Recommend one
(pre-selected in the `AskUserQuestion`), but make the alternatives real choices:

- **`/ideate`** — the frame is settled but the *solution space* is open; you want many candidate ideas.
- **`/brainstorm`** — this turned out to be "really a requirements question" about one chosen thing;
  go deepen it into a requirements doc.
- **`/plan`** — the frame revealed the thing is "already buildable" — the problem and approach are
  clear enough to plan directly.
- **`/strategy`** — this is really a "direction" question about where Infiquetra is pointed, not a
  single build.
- **"Drop it"** — the diagnostic showed the thing isn't worth pursuing; a clean exit is a valid
  outcome.

**Advisory typed judgment — the `route` distribution.** Before asking the routing question, you may
ask `plugins/saga/scripts/shaping_judgments.py route` over the **settled frame from Phase 2** — the
real problem and the key assumptions, never the dialogue that produced it, because the fleet-core
data rule excludes a raw transcript. Show the full distribution over the five routes as one line of
evidence beneath the question, and use it to pre-select. It is **advisory**: it never routes, it
never replaces the blocking question, and the hard gate below is untouched. It **fails open** — when
the call fails or the key is absent, ask the routing question exactly as described above with no
distribution line.

```bash
python3 plugins/saga/scripts/shaping_judgments.py route --doc docs/office-hours/<frame-note>.md
```

Hand off with the frame: pass the settled problem statement (and the frame-note path, if one was
written) to the next command so it does not re-derive what office-hours just settled.

**End with an assignment.** Close with one concrete next action — the command to run and the framed
problem to carry into it — not a vague "let me know."

**HARD GATE (restated, absolute):** from this session you never implement, never write a plan, never
scaffold, and never file an SDLC issue. Office-hours produces durable source material only — it never
creates or mutates a GitHub issue and never runs `gh issue create`.
Mission Control owns issue creation; route there.
Office-hours is upstream of execution: it routes to a next command and stops there. It does not
select an execution backend and does not consume `references/operator-choice.md`.
