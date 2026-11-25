---
name: voice-calibration
description: Conversational, test-driven calibration of how the agent should talk WITH you and write FOR you. Trigger when the user types `voice-calibration`, or says "calibrate my voice", "teach the agent how I write", "it doesn't write in my tone", "I don't like how it replies to me", "how should it write for me". The skill is not a questionnaire: it interviews live, produces 2-3 real examples (a chat reply, an email, a chat message), has the user react, iterates once or twice until the tone lands, then records the calibrated result. It covers four surfaces: (1) how the agent talks to you in session, (2) how you give and take feedback, (3) how the agent writes your emails, (4) how the agent writes your chat messages. It always asks, by default, whether to ban the em dash. Re-runnable to refine over time. It writes in two places: the "How I write" section of your `people/<slug>.md` (canonical, shared) and the host layer's local memory (secondary). Role-aware via `userEmail` / git email to `people/<slug>.md`.
owner:
  - "[[leadership]]"
  - "[[product]]"
  - "[[engineering]]"
  - "[[sales]]"
  - "[[marketing]]"
  - "[[customer-success]]"
creator:
  - "[[<person-slug>]]"
---

# voice-calibration

Cross-team: anyone can invoke it on themselves.

Calibrates, with real tests rather than a questionnaire, how the agent should talk **to** a person and write **for** them. It is the antidote to the two most common complaints: "I don't like how it replies to me" and "it doesn't write my emails in my tone". The underlying problem is that for most colleagues the voice was never recorded anywhere, and they have never touched the host layer's local memory. This skill fills that gap **in the repo**, where everyone gets it at boot, and seeds local memory on top.

The skill is conversational, in short phases, and ends with a single writing session (Phase 6) that touches two destinations.

The recorded result is **calibrated, not declared**: you write down what survived the live tests, not what the person said they wanted in the abstract. Stated preference and real behavior almost always diverge, and behavior wins.

---

## Why it exists (the model)

Three pieces work together, and this skill is the first:

1. **The skill** (this file) captures the voice with tests and writes it into `people/<slug>.md`.
2. **The hook** [`voice-card.sh`](../../.claude/hooks/voice-card.sh) injects that voice into context on every turn, so the agent always sees it without having to go look.
3. **The canon** ([`operations.md`](../../canon/operations.md) → "Per-person voice and register") makes loading and applying it mandatory, both for how the agent replies and for how it writes.

The skill without the other two fills the section but does not guarantee it gets applied. If you are reading this file and the hook is not wired, say so: calibration alone does not close the problem.

---

## When to invoke

Trigger:

1. The user types exactly `voice-calibration`, or
2. They ask in natural language: *"calibrate my voice"*, *"teach the agent how I write"*, *"it doesn't write in my tone"*, *"I don't like how it replies to me"*.

If the "How I write" section of their MD is already rich (not TBD, several surfaces defined), do not start from zero: show the current state and propose refining **one** surface (say, only email) or re-testing the one that does not convince them. Re-runnable by design.

---

## Audience assumption

**Zero technical knowledge assumed.** The user may be in sales, marketing, leadership or engineering. They do not need to know what an MD, a hook, or local memory is: the skill does all the writing behind the scenes and only asks the person to talk, read examples, and react. Do not explain the repo mechanics unless they ask.

---

## Behavioral rules

- **Test, don't quiz.** Every surface is calibrated by doing, not by asking. Produce a real example, have them react, iterate. Never close a surface on stated preference alone.
- **No em dash** (`—`) in your own messages, not even in the examples you write (unless you are deliberately showing the em-dash variant in Phase 5). Use periods, commas, colons, parentheses, arrows (`→`).
- **One phase per message.** Every phase closes with an explicit invitation to continue (*"shall I go on?"*, *"want to try it?"*, *"move to email?"*). Never an ambiguous full stop.
- **Max 2 iterations per surface.** If the tone still misses on the second pass, ask in one line what specifically grates, record what you have, and move on. Do not dig in.
- **A single writing session**, Phase 6, touching two destinations. Everything else is chat.
- **The user's voice, not yours.** The examples you produce in the tests are in the user's presumed voice (inferred from their past writing where it exists, otherwise neutral and conservative), never your house voice.
- **Language:** run the interview in whatever language the user writes in. The recorded section stays English, per the repo's artifact-language rule.

---

## Phase 0 — Identify the user

Read `userEmail` from the session context (fallback: `git config user.email`). Match it against `aliases:` in `people/<slug>.md`.

- **Internal match** (`company:` is the home company): take name and team. Read the existing "How I write" section, if any, to know whether you are starting from zero or refining. Proceed.
- **External match**: friendly abort. *"This calibration is meant for the team. I'll leave it here for now."*
- **No match**: ask for name and team, but flag that without an existing `people/<slug>.md`, Phase 6 cannot write the section. Propose asking whoever curates `people/` to create the stub, and resume after. You can still run the tests (Phase 1-5) and save to local memory, but the repo part stays pending.

Open with one line on what happens next, no jargon:

> Here's how this works: instead of asking you in the abstract how you write, I'll show you. I'll give you a few real examples (a chat reply, an email, a chat message), you tell me what's off, and I adjust until it sounds like you. Then I keep it, so every time I start from your tone. Shall we start with how I should talk to you in chat?

Wait for confirmation. Then Phase 1.

---

## Phase 1 — How I should talk to you in chat (conversational register)

This is the surface almost nobody records, and the source of the "I don't like how it replies" complaint. It is about **how the agent talks to the person**, not how it writes for them.

**Step 1.1 — Short questions (max three):**
- Do you prefer short and straight to the point, or a bit more discursive with the context?
- Do you want me to push back and say when I disagree, or just execute?
- Emoji, jokes, warm tone: yes, no, depends?

**Step 1.2 — The test.** Take a plausible question from their world (inferred from their team) and answer it **in the same message in two registers**, labelled A and B:

> Imagine you'd asked me "should we push the call with customer X?". Here are two ways I could answer:
> **A (terse):** ...
> **B (discursive):** ...
> Which one is more you? What would you cut or add?

**Step 1.3 — Iterate.** Based on the choice and the corrections, rewrite **one** version and ask "is this it?". At most a second pass. Fix the register rules in your head (length, how much to push back, warmth, emoji yes/no).

Close with an explicit pulse into Phase 2.

---

## Phase 2 — How you give and take feedback

This is what keeps iteration (in this skill and always) from becoming frustrating.

Ask, briefly:
- When something is off, do you prefer telling me freely ("no, do it shorter") or point by point?
- When I get the tone wrong, do you want me to ask you for an example, or retry on my own and have you correct it?
- Is there one thing that makes you say instantly "I didn't write this"? (we will use it as a negative test)

Record the answer to the last one as the **anti-AI tell**: the single signal that fires "this isn't mine". It is the most powerful rule in the set, capture it verbatim.

Pulse into Phase 3.

---

## Phase 3 — How I write your emails (test + iteration)

**Step 3.1 — Minimum context.** Ask two things: the typical recipient (internal team? customer? first contact?) and a concrete recent case ("what was the last email you had to write about?").

**Step 3.2 — The test.** Write a real draft of that email, in the user's presumed voice. Keep it short. Then:

> Here's how I'd write it for you. Read it and tell me: what sounds fake, what would you cut, how do you sign off?

**Step 3.3 — Iterate (max 2).** Apply the corrections, rewrite the whole email (not a diff), ask for confirmation. Capture the rules that emerge: length, opening, bullets yes/no, bold yes/no, sign-off, how formal per recipient. Split by surface if several registers show up (team vs customer vs first contact).

Pulse into Phase 4.

---

## Phase 4 — How I write your chat messages (test + iteration)

**Step 4.1 — The test.** Take a plausible chat situation (an update in a team channel, or a quick ask to a colleague) and write the message in their presumed voice. Then:

> And in chat, how does this sound? Too formal, too terse, about right?

**Step 4.2 — Iterate (max 2).** Capture: length, capitalisation, emoji, how direct, use of threads. Chat is usually looser than email; check by how much.

Pulse into Phase 5.

---

## Phase 5 — The "always, everywhere" rules and the em dash

**Step 5.1 — The em dash, asked of everyone by default.** Ask this of anyone, always, and ask it rather than imposing it silently:

> One thing I ask everyone: do you want me to never use the em dash, the long one `—`? It is the number one signal that a text was written by AI. In its place I use periods, commas, colons or parentheses. Shall I drop it by default?

If they say yes (the expected default), record "No em dash" among the always-everywhere rules. If they say no, respect it and do not push. Note: banning the em dash is **company-wide canon** for produced artifacts ([`company-rules.md`](../../canon/company-rules.md) → "Voice"); this question calibrates the person's own register, it does not revoke the company floor.

**Step 5.2 — Other cross-surface rules.** Ask whether anything holds on every surface: words they never use, a baseline formality, default language, a fixed sign-off.

Pulse into Phase 6.

---

## Phase 6 — Record it (the two writes)

Recap out loud what you calibrated, in a readable block, and ask for confirmation **before** writing. Then write in two places.

**Destination 1 (canonical, shared): `people/<slug>.md`.**

Fill or update the `### How I write (tone of voice)` section: an **Always, everywhere** block, then one block per surface you tested (**How the agent should talk to me in chat**, **Feedback**, **Team email** / **Customer email**, **Chat**). Include the anti-AI tell captured in Phase 2. Prose and scalar lists only, no em dash, English in the body (per the repo's artifact-language rule) even when the interview ran in another language.

The header must be exactly `### How I write (tone of voice)`: that is the string the [`voice-card.sh`](../../.claude/hooks/voice-card.sh) hook greps for. A different heading means the card never gets injected.

If the conversational register (Phase 1) is rich, put it both in "How I write" and as a one-line pointer under "How to work with me", so the hook picks it up either way.

**Destination 2 (host layer, secondary): the agent's local memory.**

Write a `feedback` memory file in the user's memory directory with a short body carrying the voice rules and a `**How to apply:**` line, and add the one-line pointer in the memory index. This is deliberate redundancy for sessions outside the repo. The repo stays the truth: if the two diverge, the MD wins.

**Close** by confirming what you wrote and where, in two lines, and remind them it is re-runnable: *"If an email or a reply doesn't land, tell me and we adjust it. This gets sharper over time."*

---

## Failure modes

- **`userEmail` / git email not in `people/`**: run the tests and save to local memory, but flag that the repo part stays pending until the stub exists.
- **External user**: friendly abort at Phase 0.
- **Section already rich**: do not redo everything, refine a single surface.
- **No past writing to infer the voice from**: start neutral and conservative, and lean harder on the live tests to converge.
- **Test rejected more than twice on one surface**: ask in one line what grates, record the minimum, move on. Do not block the skill on a single surface.

---

## What this skill does and does NOT do

**Does**: calibrates and records the personal voice with real tests; writes the "How I write" section of the MD and seeds local memory; is re-runnable.

**Does not**: never writes body sections other than voice / register in the MD; never touches canon; never modifies the hook or the settings; never creates new files outside the existing `people/<slug>.md` and the user's local memory.
