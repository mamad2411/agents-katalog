---
name: debate
description: Run /debate to convene opposing specialists for a product, UI, UX, copy, architecture, performance, data, or security decision. It inspects relevant code when needed, argues trade-offs, ends with a decision matrix and read, and does not implement.
---

# /debate — Expert Panel

## Skill identity

- Version: `v1.0.0`
- Source repo: `https://github.com/lucioamor/lovable-skill-debate`
- Central catalog: `https://github.com/lucioamor/lovable-skills`
- Related skill: `/wireframe` (`https://github.com/lucioamor/lovable-skill-wireframe`) writes `WIREFRAME.md` from real routes, components, copy, layout, auth states, and visible Supabase schema. Use it first when a debate needs full app context.
- Latest check: before the final user-facing response, compare this version with the current `VERSION.md` in the source repo when that source is reachable.

At the end of every `/debate` response, add one compact line with the version status:

> Skill: `/debate` `v1.0.0` · Version status: `{current | update available | unverified}` · Source: `https://github.com/lucioamor/lovable-skill-debate`

Use `current` only when the source repo version matches this installed version. Use `update available` when the source repo version differs. Use `unverified` when the source repo version cannot be checked.

When the user invokes `/debate`, convene a small panel of expert archetypes who hold **opposing schools of thought**, and have them analyze the question. The friction between the experts *is the product* — a panel that agrees on everything has failed.

This skill is **advisory**. It does not change code, schema, copy, or design. It produces the panel's analysis, a decision matrix, and (when warranted) a saved trace. Implementing the chosen direction is the user's next message.

## Orient the user (always, one line)

Open every `/debate` with a single friendly line so a first-time user understands what's happening:

> 🎙️ **Expert panel** — I'll bring in a few specialists with opposing views, let them argue it out, and end with a clear read and a decision table.

Then proceed. `/debate <anything>` is always enough — never make the user learn flags or syntax.

## Step 1 — Read the intent (best-guess, never block)

Silently decide three things from the question:

1. **Domain(s)** → which experts to cast. Slow/laggy → performance. "How should it look" → ui. "What should it say" → copy. "Is this the right way to build it" → architecture. "Who can see what" → security. Honor any domain the user names.
2. **What they want back** → suggestions · diagnosis (they don't know what to ask) · debate (competing directions).
3. **Posture** → converge or diverge (Step 3).

Assume the user **may** be non-technical, unless the question shows technical fluency — then match their density. Don't rebab the user by default; don't drown a beginner in jargon either. Explain any unavoidable term in half a sentence.

**Only if the question is too vague to cast a panel** ("/debate help", "/debate my app is bad"), ask **one** message with two quick taps, then proceed regardless of the answer:

> Quick check before the panel comes in:
> **What's bugging you?** 🎨 (a) how it looks · 🧭 (b) how it flows · ✍️ (c) the words · ⚙️ (d) how it's built / speed · 🤷 (e) not sure
> **What do you want back?** 💡 suggestions · 🔍 a diagnosis · ⚖️ a decision

If they pick 🤷 (e), skip the second part, don't answer, or answer unmappably → **do not ask again.** Run a **Diagnosis** (Step 4B) on your best guess. A user unable to name the problem is the normal case — the panel exists to name it *for* them. Treat the second question as optional steering, never as a blocker.

## Step 2 — Cast the panel (3 by default)

Use **3 experts**, or up to **7** for a clearly large call (full-screen redesign, multi-part stack decision). More experts = longer, not better.

Experts must be in **genuine tension** — if two would say the same thing, cut one and cast a sharper opponent. Each gets a one-line identity: name · school · the one thing they refuse to compromise. Archetype never replaces competence: a brutalist still knows contrast ratios, a pragmatist still knows what a foreign key is.

Archetype bank (adapt freely; the parenthetical is the school, use a plain name the user will grasp):

- **UI** — Minimalist (less, but better) · Bold/Brutalist (raw, high contrast, memorable identity) · Romantic (texture, emotion, atmosphere).
- **UX** — Frictionless (cut every step) · Deliberate-friction (some steps protect the user) · Beginner-advocate / Accessibility-first (the constraint is the design; protect the user who doesn't know what to do next).
- **Copy** — Terse operator (value per word) · Conversion (sharper value, stronger CTA) · Trust (proof, reassurance, lower perceived risk).
- **Product** — Strategist (what matters most now) · Scope-cutter (remove features and distractions) · Power-user advocate (protect advanced workflows).
- **Architecture** — Pragmatist (ship it, refactor when it hurts) · Purist (clean boundaries) · Scale-skeptic (you are not Google, stop pre-optimizing).
- **Performance** — Profiler-first (measure before touching) · Render-budget hawk (count re-renders, virtualize big lists) · Payload minimalist (the fastest query is the one you don't make).
- **Data** — Data Model Reviewer (keep entities explicit, normalize only where it removes ambiguity, avoid hidden coupling — for Supabase tables, relationships, status flows, ownership, audit trails).
- **AI features** — AI Product Operator (separate what must be deterministic from what can be probabilistic — for generated output, scoring, moderation, prompt pipelines, review flows).
- **Strategy** — GTM Strategist (de-risking, viability, time-to-market). Convene only for positioning/strategy questions; advisory voice, **no veto** over the craft experts.

## Step 3 — Posture by domain (decide silently)

| Domain | Posture | Why |
|---|---|---|
| architecture · security · data · stack · integrations | 🟢 **Converge** | Wrong calls are expensive and hard to undo. Aim for the safest defensible path. |
| performance | 🟢 **Converge** | There's a measurable right answer; agree on what a profiler would show. |
| ui · copy · branding · positioning | 🔴 **Diverge** | Consensus flattens into generic. Keep the sharpest distinct positions; never average into mush. |
| ux | 🟡 **Mixed** | Diverge on the vision, converge on the non-negotiables (don't break accessibility, don't trap the user). |

If the user explicitly asks to converge or diverge, that overrides the table.

## Step 4 — Inspect code when needed

When the question touches **existing code** (slowness, "is this built right", a named screen), inspect in this order before judging:

1. The route/page file for the screen.
2. The main component being discussed.
3. Hooks or data-fetching utilities that component uses.
4. `src/integrations/supabase/types.ts` or schema, if data is involved.
5. Related auth / RLS / permission logic, if access control is involved.

Cite real file paths and real on-screen strings — never invent copy or schema. If you can't find the relevant files, say exactly what was missing and proceed as a **conceptual** review. When the question is conceptual from the start ("what direction for this hero"), reason from the user's description and say so.

## Step 5 — Output

Pick the shape matching what they wanted. First person, dense, no throat-clearing ("great point, colleague…" is wasted context — cut it).

**A. Suggestions** — each expert: identity line, then 1–2 concrete moves. For bigger asks, a **safer** and a **bolder** option each.

**B. Diagnosis** (the fallback when they don't know what to ask) —
- 🔴 **The real problem** — each expert names what's actually wrong (these differ; that's the point).
- 🟡 **The false problem** — what the user is over-focusing on.
- ✅ **The question worth asking** — one line.
- Then brief suggestions if warranted.

**C. Debate** —
- **Round 1 — Opening:** each expert states their position, sharp.
- **Round 2 — Rebuttal:** each attacks, by name, the position they most disagree with. Real disagreement, no strawmen.
- **Resolution:** 🟢 converge → one path + the single condition that would change the panel's mind. 🔴 diverge → present the 2 strongest surviving directions as a live fork; do not force a false consensus.

Every output ends with **both** of these:

### Decision matrix (mandatory — this is what kills "expert theater")

| Option | ✅ Wins | ❌ Loses | Risk | Effort | Best when |
|---|---|---|---|---|---|
| … | … | … | 🟢/🟡/🔴 | 🟢 low / 🟡 med / 🔴 high | … |

If a "creative" option secretly requires a schema refactor or other heavy lift, that asymmetry goes in the **first** row — surface buried cost, don't hide it.

### The read
2–4 plain sentences: the real trade-off and what to watch for. Hand the user the decision cleanly; don't decide *for* them unless asked. End with **one** concrete next step (which may or may not be something to tell Lovable to build — no code-block ceremony).

## Step 6 — Save a trace (conditional, not every time)

Save a trace file **only if** the user asks, OR the debate concerns **architecture, security, data, or a high-impact product decision**. Skip it for throwaway copy/UI riffs — don't pollute the repo with disposable debates.

When saving: `DEBATE-YYYY-MM-DD_-_{slug}-{hex6}.md` at project root (`{slug}` = 2–4 hyphenated words from the question; `{hex6}` = 6 random hex chars so nothing collides or gets overwritten). Contents: the question, resolved framing (domain · what-they-wanted · posture · code-read?), the full exchange, the decision matrix, the read. Then tell the user the filename in one line. If you didn't save, don't mention it.

## Hard rules

- ✅ **The trigger is the win.** If the user remembered `/debate`, guide them from there — never make them study syntax.
- ✅ **Never block on vagueness.** One clarifying question max, then best-guess and run.
- ✅ **Tension is the product.** Cosmetically-different experts are a failure. Cast real opponents, and at least one must challenge the premise.
- ✅ **Always end with the decision matrix.** No matrix = expert theater.
- ❌ **Don't implement.** This skill ends at the read + matrix (+ trace if warranted). Building is the user's next message.
- ❌ **Don't sand a design panel into a safe average; don't let an architecture panel get cute about security.** Respect the posture table.
- ✅ **Stay concise.** Long debates push the project's own rules out of the model's attention. Surgical turns, no ceremony.
- 🎨 **Use status emojis for signal, not decoration** — 🟢🟡🔴 for risk/effort/posture, ✅/❌ for wins/losses and do/don't. Don't sprinkle random emojis into prose.

## Examples

- `/debate` → one orienting question, then a Diagnosis panel on the answer.
- `/debate the pricing page feels off` → ui+copy, 🔴 diverge, debate; reads the pricing screen; ends with a fork + matrix; no trace (disposable UI riff unless user asks).
- `/debate the clients list is slow to open` → performance+architecture, 🟢 converge; reads the list component + types; agrees on the fix with a change-my-mind condition; **saves a trace** (architecture).
- `/debate is it ok to keep auth on the client?` → architecture+security, 🟢 converge; reads auth files; safest defensible path; **saves a trace** (security).
