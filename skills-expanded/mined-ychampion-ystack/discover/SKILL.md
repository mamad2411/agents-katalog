---
name: discover
description: >-
  Customer discovery for a startup idea. Sharpens the hypothesis, researches 20 real prospects with
  sources, drafts outreach and a Mom Test interview script, and logs call notes as evidence with a
  commit / sharpen / keep testing / kill call. Use when testing whether an idea has real demand, when
  asked to find prospects or write a customer interview script, or when the user pastes notes from a
  customer conversation.
argument-hint: "<idea name> | log <idea> (then paste call notes)"
---

# /discover: find out if real people have the problem

## The founder hub

This skill reads and writes a **founder hub**: one folder holding the startup's truth.

- **Location:** the `FOUNDER_HUB` environment variable, default `~/founder`. Below, `<hub>` means that
  folder.
- **Files this skill uses:**

| File | What it holds |
|---|---|
| `<hub>/README.md` | The decision rule and evidence rules (below). Read it; the hub's version wins over the defaults here |
| `<hub>/bottleneck.md` | The current bet, this week's single bottleneck, the goal and its deadline |
| `<hub>/ideas.md` | A table of candidate ideas: one line, who pays, evidence so far, status (candidate, testing, committed, parked, killed) |
| `<hub>/evidence/<idea>.md` | Hypothesis, interview script, conversation log and running tally for one idea |
| `<hub>/evidence/<idea>-prospects.md` | Researched prospects, drafted outreach and outreach status |

**If the hub or a file is missing,** say so and offer to create the minimal structure: the folder,
`README.md` holding the two rule blocks below, a `bottleneck.md` with empty headings (current bet,
bottleneck, goal, deadline), an `ideas.md` with the table header, and an empty `evidence/`. Create
per-idea files as you need them. Never skip a write silently because a file wasn't there.

**Default decision rule** (one for every idea):
- **Commit** when at least 3 target users show strong pull: they agree to a pilot, share real data or
  access, pay, or sign a letter of intent.
- **Sharpen** when the pain is real but the framing or the buyer is wrong.
- **Kill** after about 15 targeted conversations with no strong pull.
- Compliments, "interesting" and "send me more info" don't count as pull.

**Default evidence rules:**
- Log only what real people said or did, with a date and a source.
- Past behaviour beats opinions about the future. "We spent 3 weeks on this last month" counts; "I'd
  probably use that" doesn't.
- The agent drafts outreach; the human sends it. Nothing goes out automatically.

Before anything else, read `bottleneck.md`, `ideas.md` and `evidence/<idea>.md`.

## Mode A: test an idea (`/discover <idea>`)

1. **Sharpen the hypothesis** in 5 lines, written at the top of `evidence/<idea>.md`:
   - who has the problem (role, company type, size);
   - the problem, in their words;
   - what they do today instead (the workaround, and what it costs them);
   - why now;
   - the riskiest assumption.

   If the idea is too vague to fill these in, ask the user up to 3 pointed questions first.
2. **Research 20 real prospects** with web search and fetch, in the market the user is targeting (ask
   if `bottleneck.md` doesn't say). For each: name, role, company, why they fit (a concrete, recent
   signal: a post, a job listing, a launch, a complaint), a source URL, and the best channel (LinkedIn,
   X, email, a community). Write them to `evidence/<idea>-prospects.md` as a table with a `status`
   column. **Never invent people or details.** Every row needs a source. Fewer real rows beat 20
   padded ones.
3. **Draft outreach** for each prospect in that file:
   - under 90 words, personal, referencing their signal;
   - it asks for 15 minutes to learn how they handle the problem, not to pitch;
   - one follow-up for 4 days later.

   **The user sends everything. Never send, post or email anything yourself**, even if a tool for it
   is available.
4. **Interview script** (Mom Test style) in `evidence/<idea>.md`: questions about past behaviour and
   real costs ("tell me about the last time...", "what did it cost?", "what have you tried?"). No
   hypotheticals like "would you use...". End with a commitment ask: a pilot, access to real data, a
   paid trial or an intro.
5. Set the idea's status to `testing` in `ideas.md` (add a row if it's new) and report: the hypothesis,
   the prospect count, and the 3 best prospects to contact first.

## Mode B: log a conversation (`/discover log <idea>`, then the notes)

1. Append to the log in `evidence/<idea>.md`: date · person · role · company · pain 1-5 · current
   workaround and its cost · buying signal (pilot / data access / pay / intro / none) · best verbatim
   quote.
2. Separate facts they stated from your interpretation. Treat compliments and "interesting" as no
   signal.
3. Update the running tally: conversations held, strong-pull count, average pain.
4. Apply the decision rule. State commit / sharpen / keep testing / kill, with the reason. If sharpen,
   propose the new framing.
5. Update the prospect's status in the prospects file, and draft the follow-up message for the user to
   send.
