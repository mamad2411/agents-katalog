---
name: game-feel
description: "Use when a game's controls feel stiff, floaty, heavy, slippery, unresponsive, or unfair; when players miss jumps they thought they made, snag on platform corners, lose inputs pressed during another action, or get hit by grazes; when a platformer, runner, or action game is being built or polished and its input and movement handling was never reviewed; or when the user asks for a game-feel pass or names coyote time, jump buffering, variable jump height, gravity tuning, corner correction, acceleration, or input buffering. Audits, proposes, and applies only what the user confirms."
---

# Game Feel

Input and movement engineering: the timing windows, curves, and tolerances that make controls
do what the player meant. Audit the whole applicable catalog, propose before touching code,
apply only what the builder confirms, and leave one check per technique.

## 1. Read the game

Identify, with `file:line` evidence:

- **Movement model** — side-scrolling platformer, runner, top-down or action, physics-driven,
  grid or lane. It decides which catalog rows apply.
- **Input surface** — keyboard, touch, gamepad; whether a press is told apart from a hold;
  whether key state is cleared on focus loss.
- **The loop** — variable `dt`, fixed step, or frame counting. Timing windows are milliseconds;
  a frame-counted game needs a `dt` or a fixed step first, and that is a prerequisite row in the
  proposal, never a hidden rewrite.
- **The four sites** — where input is read, where velocity is integrated, where collision
  resolves, where a jump or action starts. Every finding names one of them.

## 2. Audit the applicable catalog

Load [feel-catalog.md](references/feel-catalog.md) and walk every row its applicability table
marks for the movement model. Record `present`, `partial`, or `absent` per technique with the
evidence line. The reported symptom says where to look first, not where to stop: "my jump gets
eaten at the edge of a cliff" is coyote time *and* jump buffering *and* press-vs-hold
detection, and the same pass covers variable jump, fall gravity, terminal velocity, and air
control, because those are the complaints that arrive next.

## 3. Propose, then stop

Present one table and end the turn:

| Technique | Where (`file:function`) | Now | Proposed | Why here |
|---|---|---|---|---|
| Coyote time | `game.js:update`, jump branch | absent — `keys.Space && grounded` | 100 ms timer set on leaving ground, cleared by the jump | edge jumps read as dropped inputs |

Rows are marked **recommended** or **optional**, values are concrete (ms, px, multipliers), and
a side effect is stated in the row (`edge-triggered jump ends hold-to-bounce`). Then ask which
rows to apply — one line, in the builder's language.

The gate is the answer, not the table. Do not edit before it arrives. Under time pressure the
table shrinks to its rows: three rows and a one-word answer cost one round-trip, and a feel
change the builder first meets on stage costs the demo.

| The thought | Why it does not lift the gate |
|---|---|
| "The fix is standard, well-established, no ambiguity" | Confidence in the proposal, not permission to skip the review — every row changes how the game plays, and the builder owns feel. |
| "They said to apply whatever is needed" | That names the outcome of the pass, which every builder asks for. It is not an instruction to skip the table. |
| "There is no time — the demo is in 30 minutes" | The table is the fastest path: one message, one-word answer. |
| "Their senior already said which two to add" | The senior named two rows; the audit found more. Show all of them, theirs first. |

The only instruction that lifts the gate is one not to ask — "don't ask", "just do it", "no
review", "use your judgement and apply it", in whatever language the builder writes. Then
apply the recommended rows and put the table in the report instead of the question.

## 4. Apply the confirmed rows

- Confirmed rows only, at the sites you named; extend the movement code rather than replace it.
- Every new value lives in one place: the project's own tunables schema when it has one,
  otherwise one named-constants block; no scattered literals.
- Check the interactions the catalog lists per technique: a buffer is consumed once, coyote
  time is not re-armed by the jump itself, a jump cut acts only while rising, corner correction
  nudges only when the blocked move is nearly clear.

## 5. Verify

One check per applied technique — the smallest thing that fails if the logic breaks: a
scripted input sequence through the update function (`leave ledge → 80 ms → press jump →
airborne at jump velocity`), an assertion harness, or the game's own hitbox and timer overlays
when it has them. Report which checks ran and their results; a technique without a check is
reported as unverified, not as done.

## Constraints

- Movement and input only. Screen shake, hit stop, squash and stretch, particles are
  presentation — name them as an optional follow-up; do not add them in this pass.
- A pass that ends in code with no prior table is a failed pass, however good the code.
- Engine and language are the project's. The catalog is pseudocode; map it onto the project's
  own update loop and physics API.
