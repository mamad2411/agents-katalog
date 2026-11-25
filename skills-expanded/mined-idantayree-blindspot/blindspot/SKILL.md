---
name: blindspot
description: "Turn an idea — or a half-planned project already underway — into a buildable blueprint, verified multi-source component harvest, and phased implementation plan. Interviews the user one question at a time until the unknowns run out, harvests and verifies real open-source components and field signals across user-selected sources (GitHub, HuggingFace, arXiv, Hacker News, Reddit, Web/Google, X) using Blindspot Harvester, and offers to split the settled choices into phased build plans and atomic tasks. Use this whenever someone describes something they want to build ('I want to build an app that…', 'I have an idea for…', 'help me plan/spec/scope this', 'turn my idea into a plan'), asks for a PRD, spec, or build plan, says an existing project feels under-planned or full of gaps ('I think we're missing things', 'audit my plan', 'what haven't I thought about'), or asks what open-source components exist for what they are building."
---

# blindspot

Named for what it looks for: the two things nobody can self-report — what you assumed was too obvious to say,
and what you never considered at all.

Someone arrives with one sentence: *"an app that helps dog walkers find clients."* A plan written straight
from that sentence is fiction — every important decision gets made by whoever writes it, not by the person
who has to live with it.

This skill replaces that with **two core phases plus an opt-in third phase**:

1. **Interview** — one question per message until the unknowns stop appearing, writing every answer to disk
   as it arrives.
2. **Harvest** — ask the user which scope and which sources to scrape (GitHub, HuggingFace, arXiv, Hacker
   News, Reddit, Web/Google, X, or custom), handle any required **Blindspot Harvester** browser login before
   scraping begins, then discover candidates and field signals, **deep-read their documentation for technical
   fit**, and **verify** live GitHub metadata before recommending anything.
3. **Build Plan (opt-in)** — once the user has reviewed the harvest dashboard and locked their picks, turn
   the blueprint decisions and verified stack into dependency-ordered **phases and atomic, gateable tasks**.

Phase 2 depends on Phase 1, and Phase 3 depends on Phase 2. Harvesting against a half-formed idea produces a
list of libraries for a product nobody has decided on yet; planning before reviewing the harvest produces
tasks built on unverified placeholders.

## Two ways in

**From nothing** — one sentence and an intention. Start at "before the first question" below.

**From a project already underway** — someone with code, docs and momentum who says it was never planned
properly, that it is full of gaps, or that they are no longer sure what they have actually decided. This is
the more common case and the more valuable one, because the gaps are load-bearing by the time anyone notices
them.

The mid-project entry changes the opening, not the method:

1. **Read what exists before asking anything.** Their README, plan docs, ADRs, issues, the directory layout,
   recent commits. An audit that opens by asking things already written down burns the user's patience on
   work they have already done, and they will answer more shallowly for the rest of the interview.
2. **Populate the blueprint from those artefacts**, marking each entry with where it came from — *from your
   docs* or *from you*. Provenance matters here: a decision recorded in a doc nobody has revisited in six
   months is not the same as one they just confirmed, and the difference is often the gap itself.
3. **Then run a collision pass over what already exists**, before asking anything new. This is the highest
   yield move in the whole skill for an existing project: decisions made months apart contradict each other
   constantly, and nobody has put them side by side. Open with one of those, not with a beginner question.
4. **Name the untouched areas** — what a project of this shape normally has to decide and theirs never has.
   Say them plainly as a list; that list is usually why they came.

After that, the loop below is identical. Expect the interview to be **longer** than a from-scratch one, not
shorter: an existing project brings its own contradictions with it, and every artefact you read raises
questions a blank page never would.

## Phase 1 — the interview

### Before the first question

1. **Reflect the idea back in one sentence** so a misunderstanding surfaces now rather than at question
   thirty. "So: a mobile app where dog walkers list availability and owners book them. Right?"
2. **Ask which depth to run at**, in the same message. This is the one question worth asking up front,
   because getting it wrong wastes the whole interview: a beginner asked about durability guarantees goes
   quiet, and an expert asked "do you want it on a phone or a computer?" gets bored and stops answering
   properly.

   > **1 — Absolute beginner.** You know what you want, not how software gets built. Plain language, no
   > jargon, always a choice between two options with what each costs you.
   > **2 — Moderate.** You have built or shipped something before. A mix of choices and open questions.
   > **3 — Pro.** You know the stack. Open questions, blunt trade-offs, and I will chase contradictions hard.

3. **Create the blueprint file immediately** — `<slug>-blueprint.md` in the working directory — and write the
   idea and the chosen depth into it. This is not tidiness. Long interviews outlive the context window; an
   interview that lives only in the conversation dies when the conversation is compacted, and the user loses
   an hour of decisions.
4. Say where the file is, and that every answer lands there as it comes.

The depth is a starting point, not a cage. If someone at level 1 starts using precise language, move up and
say so in a clause. If someone at level 3 stalls on a question, drop to a forced choice for that one question.
They can also just say "go deeper" or "simpler" at any point.

Per-level question style, pacing and stopping points are in **`references/interview.md`**.

### The loop

**Ask exactly one question per message.** Not two, not a numbered list of four. A batch turns a conversation
into a form, people answer forms shallowly, and the shallow answers are the ones that produce a wrong build.
One question feels like a conversation and gets real answers.

After each answer:

1. **Write it to the blueprint file** — their words for the decision, kept separate from your reading of what
   it implies. Where those blur, their words win.
2. **State the consequence in one or two lines.** "That means the reviewer needs a rubric before it can run."
   This lets them catch a bad implication immediately instead of living with it.
3. **Check whether the new answer collides with an earlier one.** Do this *before* looking at the open
   question queue. Collisions are where the unknown-unknowns live — nobody can answer "what haven't you
   thought of?", and everyone can answer "earlier you said X, just now you said Y, and both cannot hold —
   which gives?" When you find one, that is the next question.
4. **Otherwise, pick the highest-leverage open question** — the one whose answer will close or reshape the
   most other questions — and ask it.

### Three rules that make the loop work

- **Offer a forced choice when an open question would stall.** "Do you want users to sign in with Google, or
  with an email and password? Google is faster to build and means no password resets; email works for people
  who avoid Google accounts." People can react to options even when they cannot generate them. At level 1, do
  this on *every* question.
- **Make small assumptions explicitly rather than asking about everything.** If a detail is low-stakes and
  reversible, state a sensible default — "I'll assume UTF-8 Markdown files for now; tell me if not" — and
  record it under *Assumptions* in the blueprint so it stays visible and correctable. Save the questions for
  decisions that are expensive to reverse.
- **Verify factual claims instead of writing them down.** If the user says a library does X, a licence allows
  Y, or their hardware can run Z, check it — with a command on their machine or a quick search — and record
  what is actually true. An unverified premise in a blueprint is worse than a gap, because nobody looks at it
  again until the build breaks.

### Every ten questions: show where things stand

At Q10, Q20, Q30 and so on, before asking the next question, print a short progress block: the four-quadrant
count, the current question-spawn rate, the areas not yet touched, and a rough remaining range computed from
those numbers.

Do this unprompted, because a long interview with no visible horizon feels endless even when it is going
well. The table also exposes an under-probed quadrant, which is invisible from the inside — a quadrant that
has stopped producing looks identical whether it is finished or being neglected.

The four quadrants, how to recognise each, the table format, and the full worked technique are in
**`references/interview.md`** — read it before the first question.

## Phase 2 — the harvest

Once the blueprint names the parts that have to be built, use **Blindspot Harvester** to discover real
projects, research papers, and practitioner field signals for each of them.

The failure mode this phase exists to prevent: **a confident dashboard full of recalled numbers and unread
READMEs.** A model asked for "highly starred repos" will produce plausible names with plausible star counts
and plausible dates, and some of them will be wrong — wrong platform, unmaintained, demanding `24 GB` of VRAM
on an `8 GB` machine, or a hosted service being recommended as a local library.

So the rule for this phase: **every number and technical-fit claim that appears in the output was fetched,
not remembered.**

### Before searching, ask two quick setup choices

1. **What the hunt should cover (scope):**
   > **1 — The components.** Only the parts the blueprint says have to be built. Focused; every result maps
   > to something already decided.
   > **2 — Anything that saves work (default).** Those parts *and* the layer no blueprint ever lists —
   > loaders, command palettes, diff viewers, log terminals, onboarding tours, empty states, drag-and-drop.
2. **Which sources Blindspot Harvester should scrape:**
   Pre-recommend a tailored set from the blueprint and let the user add or remove any:
   - **No-login sources:** `github` (GitHub repos), `huggingface` (open-weight models), `arxiv` (research
     papers), `hn` (Hacker News), `reddit` (public discussions; optional login if rate-limited), `web`
     (Web / Google articles & benchmarks).
   - **Login-assisted sources:** `x` (X / Twitter — **requires login before harvest**), plus any custom
     authenticated site the user names.

### Pre-harvest login gate (BEFORE scraping starts)

Run `--auth-check` on the user's selected sources **before** starting the harvest:

```bash
python3 scripts/blindspot_harvester.py --auth-check github huggingface arxiv hn reddit web x
```

If **any** selected source requires login and has no valid saved session at `~/.blindspot/sessions/<source>.json`:

1. **Tell the user plainly** which source(s) require login before harvesting can start.
2. **Help them sign in with the Blindspot Harvester browser** (visible window, `headless=False`) — either via
   your agent's Blindspot Harvester browser tools (`browser_open(headless=False)` → `browser_fetch(login_url)`
   → wait for the user to finish login / 2FA → `browser_save_state` to `~/.blindspot/sessions/<source>.json`)
   or via `python3 scripts/blindspot_harvester.py --login <source>`.
3. Do not request passwords in chat and do not attempt to bypass CAPTCHAs or bot checks; let the user sign in
   directly in the visible browser window. Once saved (`chmod 600`, outside git), future harvests reuse the
   session automatically.

### The harvest pipeline

1. **Derive the component list** from the blueprint — named by the **job** ("Speech input", "Diff review"),
   never by a product name — plus the polish layer if they chose scope 2.
2. **Discover candidates & field signals across selected sources (`scripts/blindspot_harvester.py` + browser):**
   - Run `python3 scripts/blindspot_harvester.py --discover "<component query>" --sources <selected> > discovery.json`
     to gather live repo slugs, arXiv papers, Hacker News threads, Reddit discussions, and web write-ups.
   - For logged-in or JS-heavy sources (such as `x`), load `~/.blindspot/sessions/<source>.json` into the
     **Blindspot Harvester browser** session, fetch the target queries/threads, extract field warnings and
     mentioned `owner/repo` slugs, and close the session when done.
   - Aim for at least **3–4 adoptable candidates per component** plus field signals.
3. **Deep-read candidate READMEs (`scripts/blindspot_harvester.py`) & verify repo metadata (`scripts/verify_repos.py`):**
   - Run `python3 scripts/blindspot_harvester.py owner/repo1 owner/repo2 ... > dossier.json` to digest each
     candidate's actual `README.md` / model card for install commands, VRAM/hardware constraints (`Q4_K_M`,
     `Q5_K_M`, `CUDA`, `MLX`), benchmark claims, and platform caveats.
   - Run `python3 scripts/verify_repos.py --strict owner/repo1 owner/repo2 ... > verified.json` to fetch real
     stars, last push date, licence, language and archived status from the GitHub API.
4. **Sort every finding into Adopt, Consult, Field Signals, or Reject:**
   - **Adopt (`ranked`, 1st / 2nd / 3rd+):** licence, platform, hardware, and maintenance all fit. Each entry
     carries `why`, `promote` (what would move it to #1), and `fit`.
   - **Consult (`consult`):** cannot be adopted (AGPL, archived, commercial, or an **arXiv paper**), *and*
     has something specific worth reading (architecture, issue tracker, API shape, algorithm — ideas, never
     code into an incompatible licence).
   - **Field signals (`signals`):** real-world notes from Reddit, X, Hacker News, or web benchmarks that
     expose caveats or confirm production stability.
   - **Reject (`excluded`):** wrong problem or nothing worth taking (the smallest category).
5. **Build the dashboard & summarise:**
   ```bash
   python3 scripts/build_dashboard.py harvest.json verified.json <slug>-harvest.html
   ```
   The split is deliberate: **you write the judgement, `blindspot_harvester.py` discovers multi-source
   candidates/signals and digests READMEs, and `verify_repos.py` writes the GitHub API facts.** Present a
   one-screen summary alongside `<slug>-harvest.html`.

The full multi-source, login, verification, and dashboard protocol is in **`references/harvest.md`**.

## Phase 3 — the build plan (opt-in, after reviewing the harvest dashboard)

Right after presenting `<slug>-harvest.html` and the summary, **offer to turn the settled blueprint and
harvest picks into a phased implementation plan with atomic tasks**:

> "Review `<slug>-harvest.html` and let me know if you want to swap any #1 pick, drop a polish card, or
> settle any open questions. Once you're ready, want me to split this into build phases and atomic tasks?"

If the user accepts:

1. **Lock the chosen stack** into `<slug>-blueprint.md` (recording any #2/#3 overrides, kept `Consult` tasks,
   and real harvested `install_commands`).
2. **Never paper over remaining open questions.** Either settle small ones in a quick pass or route unresolved
   *Known Unknowns* into explicit **Phase 0 Spike Tasks** with a decision output.
3. **Split into dependency-ordered phases** so every phase leaves the project runnable and verifiable:
   - **Phase 0 — Foundation & Spikes:** workspace bootstrap, locked dependency install, hardware/licence checks,
     and open-question spikes / `Consult` reading tasks.
   - **Phase 1 — Walking Skeleton:** smallest end-to-end vertical slice proving the core workflow.
   - **Phase 2..N — Core Feature Phases:** cohesive milestones ordered by dependency and traced back to
     specific blueprint `Q#` decisions.
   - **Final Phase — Polish & Hardening:** Mode 2 polish cards plus tests for the exact **collision
     resolutions** and failure modes decided in Phase 1.
4. **Write `<slug>-plan.md`** (and optionally `<slug>-tasks.json` for automation) where every task is atomic
   (`P1-T1`, traced blueprint decisions, chosen verified components, deliverables, dependencies, `[human]`
   flag where judgement/visual sign-off is needed, and a concrete **Done Gate**).

The full Phase 3 structure and task template are in **`references/plan.md`**.

## Output

The user ends with two core artefacts, plus an optional third:

- **`<slug>-blueprint.md`** — the idea, every decision in their own words with its consequence, the four
  quadrants, stated assumptions, locked component stack, and open questions.
- **`<slug>-harvest.html`** — the verified multi-source component & field-signal dashboard.
- **`<slug>-plan.md`** *(optional Phase 3)* — phased build plan and atomic, gateable tasks (plus optional
  `<slug>-tasks.json`).

## Handing the blueprint onward

**[Night Watch](https://github.com/IdanTayree/night-watch)** turns a settled plan into work that runs
unattended. The seam is exact: **settled decisions + verified components + gateable Phase 3 tasks can enter a
night queue; open questions and `[human]` tasks stay day work.** Because every dependency's licence and
technical fit was already verified in Phase 2, an unattended shift never has to choose a library on its own.
