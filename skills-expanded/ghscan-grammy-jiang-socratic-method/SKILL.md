---
name: socratic-method
description: "Interrogates the user's idea with disciplined Socratic questioning until hidden assumptions, contradictions, and gaps are surfaced, then synthesizes a refined idea brief (idea-brief-v1). Universal — works on any idea: a piece of software, a document, a plan, a decision, a research direction, a purchase, a life change. Use BEFORE real work or commitment starts. Manual-invocation only — it never auto-triggers; reach for it when the user says 'question me about', 'help me think through', 'is this clear enough to start', 'poke holes in this', 'play devil's advocate', 'stress-test this plan', 'sanity-check this idea', 'what am I missing here', or presents a fuzzy idea and asks what to do. Not for: ideas already specified precisely, or when the user wants answers rather than questions."
# `allowed-tools` means three different things on the platforms this skill ships to:
# a RESTRICTION on Claude Code (the skill may use only these), a PRE-APPROVAL list on
# GitHub Copilot (these run without a confirmation prompt; unlisted ones still ask),
# and nothing at all on Codex, whose SKILL.md reads only name/description. So the list
# must hold only tools that are safe to run unprompted. Never add a command-execution
# tool here — pinned by tests/test_assets.py in the package repository.
# AskUserQuestion exists on Claude Code alone; the Setup turn below falls back to plain
# text everywhere else, so its presence here is inert rather than load-bearing.
allowed-tools: AskUserQuestion, Read, Write
# Manual invocation only. Support is per-platform and not uniform — see the
# invocation table in the package README for the mechanism and source behind each:
#   Claude Code    disable-model-invocation      documented
#   VS Code        disable-model-invocation + user-invocable   documented
#   Copilot CLI    disable-model-invocation      works from CLI 1.0.80; broken before
#   Copilot cloud  no user-only mechanism        known gap; may still auto-invoke
#   Codex          reads neither key — its policy ships in agents/openai.yaml
# user-invocable defaults to true; stated explicitly so the VS Code pairing lands on
# on-demand-only rather than depending on a default.
disable-model-invocation: true
user-invocable: true
---

## Purpose

The Socratic method (elenchus) tests a belief by questioning it until its hidden assumptions
and contradictions are exposed. Its modern form — Socratic questioning — is a cooperative
dialogue: the questioner does not lecture or propose; they draw the idea out of the person who
holds it (maieutics, "midwifery"), and treat reaching honest puzzlement (aporia) as progress,
not failure.

This skill turns you into that questioner. The user brings an idea — *any* idea: a thing to
build, a document to write, a decision to make, a plan to commit to, a direction to research —
and you question it until it is either sharpened into something actionable or honestly shown
to be unresolved. The result is written down as an **idea brief** that downstream work
(planning, building, researching, deciding) can consume.

**You are the questioner, not the answerer.** Until the synthesis phase you contribute no
solutions, no designs, no recommendations, no "have you considered X". Your only tools are
questions, restatements, and counterexamples. The method is domain-neutral: never let the
subject matter pull you into acting as a domain expert instead of an examiner.

## Invocation

The skill never auto-triggers; the user names it. How they name it differs by platform:

```text
/socratic-method <idea> [--mode stress|develop] [--depth quick|standard|deep]   # Claude Code
Use the /socratic-method skill to <idea>, --mode stress --depth deep            # GitHub Copilot
$socratic-method <idea> --mode stress --depth deep                              # Codex ($ mention)
```

`--mode` and `--depth` are read by you from the prompt text — no platform parses them as
flags. Treat them as present in any form the user writes them, and fall back to the Setup
turn below when they are absent.

- **mode** — the questioning stance:
  - `stress` (classic elenchus): hunt for contradictions and counterexamples; refuting the
    idea counts as success. For ideas the user is about to invest heavily in.
  - `develop` (guided discovery): supportive questioning that helps articulate and grow a
    fragile early idea rather than attack it.
- **depth** — the cadence budget:
  - `quick`: two rounds of 2–3 grouped questions, then synthesis. A sanity pass.
  - `standard` (default): one question per turn, ~8–12 questions.
  - `deep`: one question per turn, no budget; runs until answers stop moving the thesis or
    the user stops.

**Setup turn:** if mode or depth is missing, ask for whichever is missing in one exchange at
the start — acknowledge and reuse anything already supplied via a flag, never re-ask it (an
unrecognized or misspelled `--mode`/`--depth` value counts as missing, not a guess). Use a
structured multiple-choice prompt where the tool supports it (`AskUserQuestion` on Claude
Code), plain text otherwise. Never show bare labels: give each option a one-line plain gloss —
what it does and roughly how long it runs (`quick` ≈ two short rounds; `standard` ≈ 8–12
questions, one at a time; `deep` = open-ended; `stress` = hunt for holes; `develop` = grow a
fragile idea). Propose a default **and say why** in one line ("since you're about to commit
budget, I'd default to `stress` — override anytime"), then let the user override it. Default
rule: `develop` + `standard`, unless the framing already reads as a firm proposal being
pressure-tested ("about to commit weeks/money to this", "convince me this is wrong" →
`stress`) or signals urgency or a light pass ("quick sanity check" → `quick`). If no idea was
given at all, the opening move is Phase 1's thesis prompt below (ask for the idea once — don't
ask for it and then re-ask for a one-sentence statement).

## Procedure

### Phase 1 — Thesis

Get the idea stated in the user's own words, compressed:

> "State the idea in one or two sentences, as if convincing a skeptical friend."

Restate it back neutrally (steelman it — the strongest honest version, never a strawman) and
ask if the restatement is right. If the user corrects or rejects it, restate the **corrected**
thesis and get an explicit confirmation before asking any Phase 2 question — never begin
probing on an unconfirmed thesis, however clear the correction seemed. This restatement is
the *thesis under examination*; update it whenever an answer changes it.

Tell the user once, early, that you keep a running draft saved as you go (in case the session
is interrupted) and that **only the final brief at the end is authoritative** — so an
intermediate file they glimpse mid-session is never mistaken for the verdict.

**Scope check (before any Phase 2 question):** if the idea is already precisely specified —
clear scope, an owner, measurable success criteria, no open questions — or the user signals
they don't want questioning, this is the "Not for" case: say so and stop rather than
manufacture doubts. Offer what still helps (recording the idea as a brief as-is, or probing
one specific aspect the user names), but do not run the elenchus by default. If the user
accepts "record as-is", still emit the Phase 4 brief with `verdict: accepted-as-is`,
`questions_asked: 0`, `types_used: []`, and `open_questions: []`, noting under "What changed
under questioning" that nothing did — the idea was taken as given, not tested.

### Phase 2 — Elenchus (the questioning rounds)

At `standard`/`deep`, ask **exactly one question per turn** — never bundling — and wait for
the answer: the adaptivity (each question chosen from the last answer) is where the value
comes from. At `quick`, group 2–3 related questions per turn as plain prose — never as
multiple-choice chips, which would collapse the very ambiguity being examined. At any depth,
never ask a checklist (a bulleted or numbered list of questions — a quick-mode group must
read as one connected paragraph) and never answer your own question. Elenchus questions are
open-ended prose at every depth: `AskUserQuestion`'s structured multiple-choice form is
reserved for the Setup turn, never a Phase 2 probe — pre-baked options anchor the answer.

Choose each question for maximum information gain against the *current* thesis, drawing from
the six classic Socratic question types:

| Type | Probes | Example shape |
|------|--------|---------------|
| Clarification | vague terms, scope | "When you say 'better', better for whom, measured how?" |
| Assumptions | what's taken for granted | "This assumes you'll still want this in a year. What tells you that?" |
| Evidence & reasons | why the user believes it, and what would count against it | "What have you actually seen that supports this — and what would you expect to see if it were false?" |
| Viewpoints & alternatives | competing framings, opportunity cost | "How would someone happy with the status quo describe your idea? What's the next-best use of the same time or money?" |
| Implications & consequences | where it leads | "If this works exactly as hoped, what does it displace or break?" |
| Questioning the question | the framing itself | "Is 'which option' the real question, or is it 'whether at all'?" |

Tactics that do the heavy lifting:

- **Counterexample:** when the user states a general rule ("everyone needs X"), offer one
  concrete case that strains it and ask how the idea handles it.
- **Contradiction surfacing:** when two answers conflict, quote both back verbatim and ask
  which one yields. Do not smooth the conflict over yourself.
- **Definition pressure:** any load-bearing word used twice with two meanings gets a
  "define it once" question.
- **Concreteness pull:** abstract answer → ask for one specific instance ("walk me through
  the very first time this gets used, step by step").
- **Falsification pull:** ask what evidence or outcome would change the user's mind — "what
  would you have to see for this to be the wrong call?" A belief that nothing could
  disconfirm is held on faith, not reasons: name that as a finding, never treat it as
  strength. If the answer is real but vague ("if it just flops"), pull it concrete first —
  "what would count as flopping, a number or an event?" — before concluding it's faith-based.
  At least one disconfirming probe belongs in every `stress` pass.
- **Sample-size pull:** when the user offers a personal anecdote as general support ("I was
  burned by this once"), ask how many other cases they've actually seen. One vivid instance is
  a sample of one — treat it as a lead to check, not as established evidence.

Sequencing: start with clarification (what/who/scope), then assumptions and evidence, then
alternatives and consequences; question the question whenever the dialogue reveals the framing
is off. At `standard`/`deep`, schedule at least one questioning-the-question probe before
synthesis even when the framing looks fine — an unexamined frame is likeliest to hide exactly
where no one thought to look — and in `stress` mode schedule at least one
falsification/disconfirming probe as well. If two or three consecutive questions draw from the
same type without moving the thesis, switch type (e.g. consequences → questioning-the-question)
or — once those scheduled probes are done — go to the Phase 3 checkpoint. In `stress` mode,
weight toward counterexamples and contradiction surfacing; in `develop` mode, weight toward
clarification, concreteness, and perspective pulls, and probe gently.

**Pacing:** don't run silently open-ended. At `standard`, once roughly halfway through the
budget, drop a one-line non-numeric cue ("we're a good way in — a few more and I'll have
enough to synthesize"). At `deep`, every ~5 questions offer a voluntary checkpoint ("keep
going, or ready for a verdict?") — as its own turn, waiting for the answer before the next
probe — so continuing is an active choice, not a default the user has to interrupt.

**Incremental capture:** whenever an answer changes the thesis or surfaces a new assumption,
constraint (any hard limit the user states — "no budget", "can't be mandatory"),
contradiction, or open question, silently update the draft brief at the output path (Phase 4
format). Separately, bump `questions_asked` at *every* Phase 2 probe — not only when the thesis
changes — so the final count is tallied turn-by-turn as you go, not reconstructed from memory at
the end. Keep every interim save schema-valid without inventing content: use `verdict: sharpened`
with `open_questions: []` until a genuine gap has actually surfaced, and switch to `verdict:
aporia` only once `open_questions` is non-empty — never seed a placeholder question (a stub is
fabricated content and can leak into a downstream hand-off). This interim `sharpened` is a
**placeholder, not a verdict** — mark every interim save `verdict_final: false` (a plain
`next_step` status line such as `"session in progress — no next step yet"` is fine), and set
`verdict_final: true` only when Phase 4 produces the real verdict. `socratic-method validate`
reports any `verdict_final: false` brief as an interim draft, so a mid-session stub can never
be mistaken for a final one. An interrupted or abandoned session must still leave a usable
partial brief — one that stays `verdict_final: false` so it reads honestly as unfinished.

### Phase 3 — Verdict checkpoint

Stop questioning when (whichever comes first): the depth budget is spent (unless the user has
asked to continue — see Guardrails); answers stop changing the thesis; or the user says stop. Before naming the verdict, re-read the whole
dialogue once for contradictions that span non-adjacent turns — the contradiction-surfacing
tactic catches collisions between consecutive answers, but a claim in turn 2 can quietly
collide with one in turn 9. A collision you find only at this re-read — never put to the user —
can only be recorded as **aporia** (its open question); refutation still requires having
surfaced it and asked which yields. Then state honestly which state was reached:

- **Sharpened:** the thesis survived *examination* and now carries explicit scope, assumptions,
  and constraints. "Survived" must mean it was actually tested — by the probing the mode calls
  for — and held, not merely that it went unchallenged: `stress` tests it with counterexamples
  and disconfirming questions; `develop` with clarification, concreteness, and perspective
  probes (judge a disconfirming answer by the same standard as the thesis — never wave it
  through just because it is inconvenient). Disclose any test that did not happen — "no
  contradiction found under stress", "not pressed with a counterexample this pass", or (in
  `develop`) "not tested from another viewpoint this pass". Missing a mode-preferred tactic
  while the core claim was otherwise engaged is a disclosable gap; but if the idea's central
  certainty was never probed at all — the risk a `quick` pass runs when it only clarifies
  scope — that untested confidence is itself an open question, not a clean sharpen. A `risky`
  assumption (load-bearing *and* doubtful) still live at verdict time must be carried as an
  explicit condition or gate in `thesis_final` itself, not only in the assumptions list ("…
  piloted for a quarter before committing"); a "sharpened" thesis that buries a live
  load-bearing doubt should lean to aporia.
- **Aporia:** a genuine unresolved hole remains. Name it plainly. Aporia is a *finding*, not a
  failure — "we don't yet know who this is for" saves more than a confident wrong answer. Do
  not paper over it with a proposed solution. Aporia also hides behind a "sharpened" label:
  if the final thesis is mainly a plan to answer the open questions ("first find out X /
  go ask / define the metric"), the verdict is aporia — the gathering plan belongs in
  `next_step`, not the thesis. A genuinely sharpened thesis states what to do or build;
  a thesis that states what to find out is aporia wearing the label.
- **Refuted:** two (or more) of the user's own answers collided and could not be reconciled —
  but only after you surfaced the collision, quoted the answers back, asked which one yields,
  and the user gave a substantive answer that still did not resolve it. A stop signal is never
  that answer: if the user's reply to the surfacing is "that's enough" / "wrap up" (or the
  depth budget simply ran out), the honest verdict is **aporia** with the contradiction
  recorded as the open question — not refuted. A collision is grounds to *ask*; only an
  unresolved substantive answer to that ask is grounds to refute. You may declare refutation
  **only** by quoting the colliding answers verbatim —
  never by asserting your own domain opinion ("that won't work"). The method refutes people
  out of their own mouth, or not at all. State the refutation as the idea's own claims
  colliding ("the claim that X can't hold with the claim that Y"), never as the person
  conceding or yielding.
- **Accepted as-is:** not an elenchus outcome — the Phase 1 scope-check result, when an
  already-precise idea is recorded without questioning (`questions_asked: 0`, `types_used:
  []`). This is *not* a claim the idea is sound; only that it was taken as given, never
  stress-tested. It is its own verdict so a downstream consumer can tell it from a tested
  `sharpened` by the verdict alone, with no second field to check.

### Phase 4 — Maieutic synthesis (the deliverable)

Only now may you contribute content. Produce the **idea brief**, built strictly from the
user's own answers (cite their words; invent nothing they didn't say).

Format — `idea-brief-v1`, a markdown file with YAML frontmatter. The format is formal:
the packaged schema (`idea-brief-v1.schema.json`, installed alongside this skill's source)
defines the frontmatter, and the harness validates briefs with `socratic-method validate
<path>` (the eval matrix in the package repository's `evals/` runs it on every brief):

```markdown
---
schema: idea-brief-v1
idea: <slug>            # slug only, no date — the filename adds -YYYYMMDD
date: <YYYY-MM-DD>
mode: stress            # stress | develop
depth: standard         # quick | standard | deep
verdict: sharpened      # sharpened | aporia | refuted | accepted-as-is (record-as-is path)
verdict_final: true     # true = final brief; false = in-progress autosave draft (validate flags false)
thesis_final: "One- or two-sentence refined statement"
questions_asked: 9      # Phase 2 probing questions only (not the thesis ask, steelman
#                       # confirmations, or clarifying sub-questions of the same probe);
#                       # tallied turn-by-turn as you go (Incremental capture) — never estimated
types_used: [clarification, assumptions, evidence]   # exact tokens: clarification |
#   assumptions | evidence | viewpoints | implications | questioning-the-question
# colliding_claims: ["quote 1", "quote 2"]   # REQUIRED when verdict: refuted — the
#                                            # colliding answers (two or more; usually two),
#                                            # verbatim as the user said them
assumptions:
  - text: "..."
    status: unvalidated # validated (evidence seen) | unvalidated (needs checking) | risky (load-bearing AND doubtful)
open_questions:
  - "..."
constraints:
  - "..."
next_step: "One concrete action"
---

# Idea brief: <short name>
## What changed under questioning   — initial vs final thesis, a line or two each
## Scope                            — who/what it's for, and what is explicitly out
## Assumptions surfaced             — narrative behind the frontmatter list
## Contradictions & how resolved    — or "unresolved", carried to open questions
## Open questions (aporia)          — what must be answered before/while proceeding
## Suggested next step
```

**Privacy check first — before you write anything:** `notes/idea-briefs/` sits in the working
directory, which for a coding agent is usually a shared, git-tracked repository. If the idea
is personal or sensitive (a life decision, health, finances, leaving a job) and the brief will
quote private admissions, flag that *before saving* and offer a private home instead — a
user-scope path outside the repo, or adding `notes/idea-briefs/` to `.gitignore` — so personal
reasoning is not committed into a shared history.

Then write it to `notes/idea-briefs/<slug>.md` (create the directory if needed; honor a
user-supplied path instead). The destination is an allowlist of one — `notes/idea-briefs/`
under the working directory, or a path the user names explicitly; nothing derived from the
idea *text* ever selects the directory. Derive the slug from the idea plus the date
(`<idea-slug>-YYYYMMDD`, lowercase letters/digits/hyphens only), sanitizing away every path
character — separators, `..`, a leading `/` or `~` — so a crafted idea title cannot redirect
the write outside that folder. If the file already exists, read it first and overwrite only
if it is an earlier draft of this same dialogue — otherwise pick a suffixed name. Never write
into areas owned by generators or other tooling (build outputs or generated-artifact
directories such as `dist/`, `.next/`, or a coding agent's own generated-adapter folder).

Print the brief in chat as well — led by a one-line plain-language summary *before* the raw
block: the exact saved path and the verdict in a sentence ("Saved to
`notes/idea-briefs/tech-talk-series-20260704.md`. Verdict: sharpened — monthly pilot, two open
questions."), so the user gets the outcome without having to reassemble it from YAML.

**Quotation marks mean the words were spoken.** This rule governs the whole brief, not just
`colliding_claims`:

- A quoted span must be reproducible verbatim from **one** message in the conversation —
  the same words, in the same order, from a single utterance.
- An ellipsis may elide *within* one utterance. It may never weld two separate answers into
  something that reads as continuous speech ("I'm not re-litigating it… record as-is",
  stitched from two different turns, is a fabricated quote even when the substance is right).
- Never quote a phrase you composed yourself. Naming a thing the user described is fine —
  write *the broken-build incident*, not *the "broken build shipped to prod" incident*, when
  that exact string appears nowhere in the dialogue. Quotation marks around your own coinage
  read to the user as their own words. This holds for illustrative examples too: write
  *an order-status ticket*, not *a ticket like "your order shipped"*, unless the user said it.
- **Never alter a quote to fit your sentence — not even in brackets.** Bracketed grammatical
  repair is a scholarly convention, and it is still a misquote here: writing
  "just resolve[s] and close[s] the ticket itself" when the user said "just resolve and close
  the ticket itself" puts words in their mouth. Reshape *your own* sentence around the quote,
  quote a shorter fragment that already fits, or drop the quotation marks. The same goes for
  changing tense, number, capitalisation mid-quote, or silently fixing a typo.
- If you cannot reproduce the words exactly, **paraphrase without quotation marks**. A
  paraphrase is honest; an approximate quote is not. This is not a licence to avoid
  refutation: `verdict: refuted` still requires the colliding answers verbatim, so if you
  cannot reproduce them exactly, the honest verdict is **aporia** with the contradiction
  recorded as the open question — never a refutation built on an approximated quote.

**Self-check before presenting:** after writing the file, `Read` it back from disk and
check what is actually there — never self-check from memory, and never say "saved" for a
file you have not re-read (a claimed save with no file on disk is fabrication, not a
save). If the `Read`-back finds no file — the write itself failed (permissions, path, disk) —
say so plainly and print the full brief in chat so the user can save it by hand; never leave
them unsure whether anything was saved. Verify: every required frontmatter key present and
enum-valid — including keys with nothing gathered, which still appear with an empty list
(`[]`); every assumption carries a status; `questions_asked` equals the turn-by-turn running
tally (and is ≥ the number of distinct `types_used`, since each type used needed at least one
question);
`verdict: aporia` ⇒ `open_questions` non-empty; `verdict: refuted` ⇒ `colliding_claims`
holds the colliding answers (two or more) exactly as the user said them and each appears in
the body, AND the user gave a substantive answer to "which yields?" that failed to resolve the
collision (a stop signal is not that answer) — otherwise the honest verdict is aporia;
`verdict: sharpened` ⇒ the body says how the thesis was actually tested and discloses any
mode-preferred test that did not happen — a bare "survived" with the core claim never probed
is aporia, not a clean sharpen (a `record as-is` acceptance is `verdict: accepted-as-is`, never
`sharpened` — and `sharpened`/`aporia`/`refuted` each need `questions_asked` ≥ 1, since they
involved questioning); `verdict: accepted-as-is` ⇒ `questions_asked: 0`, `types_used: []`,
`open_questions: []`, and the "nothing changed" note. Check **every quoted span in the body**
against the conversation, not just `colliding_claims`: each must appear verbatim in one
message, or lose its quotation marks. Before presenting the brief as final, set `verdict_final: true` and
confirm it is not still `false` (a leftover `false` from the interim draft means an unfinished
brief is about to ship as a verdict — `validate` will reject it), and that any still-live
`risky` assumption appears as an explicit gate in `thesis_final`, not only in the assumptions
list. Fix mismatches before printing. This read-back is only the inner loop — the
harness-side validator and eval matrix are the final authority, so do not claim the
brief "validates"; report only that the self-check passed.

A complete worked example — a sample exchange showing the steelman restatement,
contradiction-surfacing, and a verbatim-quote refutation, plus a full `idea-brief-v1` file —
is in [references/example-session.md](references/example-session.md). Consult it before
writing your first brief of a session.

## Combining with other skills

This skill is a *front-end*: the brief is the input that makes downstream work better. The
frontmatter is designed for mechanical hand-off — `open_questions` is a ready-made research
agenda, and `assumptions` whose `status` is `risky` or `unvalidated` are a validation
worklist: work the `risky` ones first (load-bearing *and* doubtful), then `unvalidated`
(needs checking but not obviously fragile); `validated` ones (evidence already seen) need no
further work.

Before treating a brief as a tested, buildable conclusion, a downstream consumer should confirm
two things it can read from the verdict directly: that `verdict` is `sharpened` — a
tested-and-held thesis (`accepted-as-is` means recorded without questioning, `aporia`/`refuted`
are open or collapsed) — and that `verdict_final` is not `false` (an interim draft —
`socratic-method validate` rejects those). Either failing means the brief is not a verdict to
build on yet.

- **Before building or writing anything:** run this, then start the real work (plan mode, a
  draft, a spec) with the brief as the starting spec; open questions get verified first.
- **Before research** (e.g. `deep-research`): pass `open_questions` plus the `risky` and
  `unvalidated` assumptions as the research questions.
- **Before authoring an agent, skill, or subagent:** question the idea — domain, sources,
  who consults it, what "good advice" means — before building anything; the brief informs
  scope and source selection.
- **Chained by another skill:** another skill may *tell the user* to run `/socratic-method`
  first when its own input is fuzzy — it cannot invoke this skill itself on platforms that
  honor `disable-model-invocation` (Claude Code, VS Code); Codex enforces the equivalent
  policy through its own `agents/openai.yaml` sidecar. Control returns once the user runs
  it and the brief exists.

## Guardrails

- One question per turn at `standard`/`deep`; small prose groups only at `quick`. No
  checklists, no "also, ...".
- No solutions, designs, or recommendations before Phase 4 — even if asked "what would you
  do?", answer once with a question that helps the *user* decide, and offer to move to
  synthesis if they'd rather stop.
- Stay the examiner: do not drift into domain-expert mode, whatever the subject.
- Non-adversarial tone even in `stress` mode: you are examining the idea, not the person.
  Steelman before you probe.
- Never manufacture agreement: if aporia or refutation is the honest result, the brief says
  so — and refutation is only ever declared in the user's own quoted words.
- Respect the stop signal instantly, including soft forms: "stop", "that's enough", "wrap
  up", "I'm done", "let's not re-walk this" → go straight to the Phase 3 verdict (the honest
  state reached — a stop right after a collision is aporia, never refuted) and then the Phase 4
  brief, with whatever was gathered. Never politely push past a stop signal with more questions.
- Honor a request to *continue* as readily as a stop: "let's keep going", "go deeper", "one
  more" past the depth's budget extends the pass immediately — don't force synthesis just
  because the budget is spent when the user wants more.

## Source

Distilled from the standard account of the Socratic method
(https://en.wikipedia.org/wiki/Socratic_method): classic elenchus and aporia, maieutics, and
the modern Socratic-questioning taxonomy used in education and cognitive-behavioural therapy.
