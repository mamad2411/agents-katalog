---
name: nmt-diagnose
description: >-
  Diagnose a live product against Ivan Zamesin's Next Move Theory / Advanced
  Jobs To Be Done methodology (distinct from generic Christensen JTBD) and route
  to the next move. A conversational, chat-first skill: it first offers to read
  the product context already in your folder (README, surveys, reviews — with
  your permission), then asks up to ~15 adaptive questions covering only the
  gaps. It challenges the goal you walked in with,
  traces weak metrics upstream through the chain to profit, surfaces risks,
  growth points, and risky assumptions in current initiatives, then recommends
  which issue to tackle first and which skill executes it. Use when the user says
  "diagnose my product", "what should I do next", "a metric dropped", "where are
  my risks / growth points", "where is this breaking", or is unsure what to work
  on. Writes nothing unless asked; recommends the next skill but the user
  launches it. Plain language; defaults to English.
user-invocable: true
---

# Diagnose — the Next Move Theory product diagnostic

A chat-first diagnostic for a live product. It finds your real risks and best growth moves, says which one to tackle first, and points you to the skill that does it.

> **New here, or not sure this is the right skill?** Start right here — or run `$nmt-chat`, describe your situation, and it points you to the right one. Quick map: **new idea →** `$nmt-market-research` · **live product or a metric moved →** `$nmt-diagnose` · **have customer interviews →** `$nmt-analyze-interviews` · **ready to build →** `$nmt-product-requirements` · **positioning / launch copy →** `$nmt-craft-value-proposition` → `$nmt-craft-go-to-market`.

---

## What this skill is — and is not

- **Is:** a conversational diagnostic. It reads the product context already sitting in your folder (with your permission) and then, through ≤15 adaptive questions on what's still missing, challenges your goal, and surfaces all risks, all growth points, and the risky assumptions in your current initiatives, prioritizes the first move, and points you to the skill that does it.
- **Is not:** a report generator. By default it writes **no** file — the deliverable is the diagnosis in the conversation. It writes one file only if you ask.
- **Is not:** an auto-launcher. It *recommends* the next skill and says why; **you** launch it.
- **Is not:** a generic feature-by-feature audit. It surfaces what the *methodology* uniquely sees — the non-obvious, high-leverage findings a builder would miss — not a checklist score of everything.

---

## Core methodological principle — never invent methodology

**The only source of truth is the Next Move Theory canon, read at runtime.** Do not diagnose from generic Jobs-To-Be-Done in LLM training — Ivan's methodology diverges substantially from Christensen / Moesta / Ulwick. The biggest failure mode is a confident, plausible, *wrong* diagnosis built on training-data JTBD.

**The five terminology mis-defaults to never propagate** (project `AGENTS.md` Rule 1):
- **A Job ≠ "progress."** A Job specifies a desired transition — situation (State A) → expected outcome (State B), in order to perform a higher-level Job. A unit of motivation.
- **Value = greater energy efficiency for the brain in performing a Job, vs. the brain's prediction.** The **Aha Moment** is the customer-experience of value beating prediction; the **Problem** is value below it. Never use the abbreviations PPE/NPE (Rule 22).
- **`I want to + verb` is the primary element, not the whole Job** (eight elements). Each infinitive verb is a separate Job (Rule 7).
- **A Problem ≠ a root cause** — it's the consequence of a Solution hired for a Job and underperforming its success criteria.
- **A Solution is a thing in the world AND a label for the sub-graph it installs.**

**The load-bearing diagnostic thesis** (`the-algorithm.md §2`): *a broken metric almost never means a problem at that metric.* Low conversion, high CAC, high churn are usually **upstream** — a wrong Segment+Job, value that doesn't beat the alternatives, or one of the three parallel conditions failing. Every symptom is traced **up** the chain to its real cause.

**Use the human-language terms** (Rule 22): *Aha Moment* / *Problem* for the customer-experience side; *Positive / Negative Prediction Error* (spelled out) only for the neuroscience side.

---

## Methodology — source of truth (progressive loading)

**Eager core — always loaded, every run (mandatory):**

| File | What it powers | ~tokens |
|---|---|---|
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md` | **mandatory.** The base methodology: the eight-element Job, the four Job levels, the Job Graph, value & the Aha Moment, segmentation. Grounds every finding; without it the diagnosis drifts into generic JTBD. | ~13k |
| `Next-Move-Theory-Canon/Riskiest-Assumption-Test/rat-key-theses.md` | **mandatory.** The engine for challenging the goal and for the "risky assumptions in current initiatives" component; riskiest-cheapest-to-falsify ordering; MVP = probe. | ~6.5k |
| `Next-Move-Theory-Canon/Algorithms/the-algorithm.md` | the diagnostic spine: §2 the chain to profit; §4 Step 1 (challenge the goal, 5 Whys, local-vs-global), Step 2 (diagnose state); §5 branches by PMF stage / product type; §6 where unfound value sits. | ~9k |
| `Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md` | §4 the chain (sequential to value, then three parallel conditions); §5 the diagnostic discipline; §8 focus; §9 local vs global; §11 NMT as a diagnostic. | ~5.4k |

**Staged — load only at the stage that needs it:**

| File | Load when | Used by |
|---|---|---|
| `ABCDX-Segmentation/abcdx-segmentation-key-theses.md` | live product, segment unknown | ABCD the base; *"why do they stay"* before *"why do they leave"* |
| `Advanced-Jobs-To-Be-Done/segmentation.md` | a segment question arises | segment = similar Core Jobs + similar success criteria (not a demographic) |
| `Advanced-Jobs-To-Be-Done/value-creation-mechanics.md` + `Advanced-Jobs-To-Be-Done/job-graph.md` | sweeping for growth points | where unfound value sits: Previous/Next Job, climb a level, kill a Job, adjacent Small Jobs |
| `Advanced-Jobs-To-Be-Done/value-creation.md` | the constraint is value | what "value" means, the Aha Moment, the Red Queen |
| `Advanced-Jobs-To-Be-Done/behaviour-change.md` | activation / retention constraint | Aha Moment / Problem, activation, homeostasis-exit triggers |

**Load per stage, not up front.** Read the eager core, then pull a staged file the moment its stage arrives — never the whole canon, and never a file no stage in this run needs.

> **Path note.** Use `Next-Move-Theory-Canon/...`; if not found, retry with a `1-` prefix (`1-Next-Move-Theory-Canon/...`) — the source repo numbers folders, the public mirror strips the prefix.

This skill grounds **only in the public canon** (all files above are public). For proprietary depth (the 100+ mechanics catalog, unit-economics theory, per-task algorithms) it gives the public-canon foundation and routes to a producer skill or the newsletter.

---

## The diagnostic model — the chain, the symptom map, the growth lens

The chain to profit (`the-algorithm.md §2` / `nmt §4`) — **sequential up to value, then three parallel conditions, then convergence:**

```
Market with money
  → Segment + Job            (one entity: similar Core Jobs + similar success criteria)
  → Added Value              (noticeable vs. the current way — the Aha)
  → ┌─ Unit economics        (positive per-unit math)
    ├─ Demand & acquisition  (reachable at target CAC + lead quality)
    └─ Scale incl. service   (no quality decay)
  → Conversion + Retention + Repeat
  → Target Profit
```

**Diagnostic rule: walk top-down, but sweep the whole chain — don't stop at the first broken node.** Each node inherits the quality of the node above it, so the *highest* broken node is the binding constraint (act on it first). But surface **every** weak node, traced to its upstream cause — the user asked for all of them, not just the headline.

**Symptom → usual real cause (downstream symptoms point upstream):**

| Reported symptom | Usual real constraint (upstream-first) | On the chain |
|---|---|---|
| Low / falling conversion | Wrong Segment+Job, or value doesn't beat alternatives | Segment+Job / Value |
| High / rising CAC | Wrong segment, or value not noticeable | Segment+Job / Value / Demand |
| High churn, low satisfaction | Value below the success-criteria threshold; or wrong segment retained | Value / Segment+Job |
| Low activation | Aha Moment too late or absent on the Critical Chain of Jobs | Value / activation |
| Revenue flat despite usage | Monetization / unit economics; value captured by the wrong tier | Unit economics |
| "Busy but not growing" | No focus (effort on non-binding nodes); or local optimum when a global move is needed | Focus / local-vs-global |
| "Don't know our best customers" | Segment not defined by Jobs (ABCDX never run) | Segment+Job |
| "Idea, no customers yet" | Not a constraint problem — discovery | → route to `$nmt-market-research` |

**The growth-points lens** (`the-algorithm §6`): the real value usually sits **outside** the current Core Jobs — in the Previous and Next Jobs, the Big Jobs (climb a level), an adjacent segment's Small Jobs, emotional/Orientation Jobs, kill-a-Job moves, and Critical Chain of Jobs repairs. Sweep for these, not only for what's broken.

**"Only we can find it" — the methodology's unique lens.** Flag prominently the findings a builder wouldn't see alone: a wrong segmentation cut (demographics mistaken for a segment), value below the success-criteria threshold, a Fake Job (future-intent no one paid for), a Previous/Next-Job growth move, a kill-a-Job opportunity, a symptom whose cause is two nodes upstream. These are the skill's reason to exist.

**"I don't know" is a diagnosis, not a gap.** If the user can't say whether new users hit the Aha, or who their A-segment is, the constraint is often *no instrumentation / no segment definition* → the move is to go measure or research (run AJTBD customer interviews per the canon interview guide, or ABCDX the paying base).

---

## The flow — a handful of adaptive questions (up to ~15)

Chat-first. **Make it feel like a few questions, not an interrogation.** Ask only the ones that challenge the goal and narrow the findings; never run the full bank. Start with the smallest set that lets you say something useful, and only go deeper if the situation needs it or the user wants the thorough pass. Batch ~3–4 at a time, cap at 15, respect the user's time. "I don't know" is a valid, informative answer.

### 0 — Orientation (one short block, then the first question)
Before the first question, one short plain block — keep it tight:
> **What this does:** finds the risks and growth moves holding your product back — including risky guesses in what you're already doing — then points you to the right next step. **A few quick questions** (more only if it helps). **You decide:** you confirm the goal and launch the recommended skill; I don't run it for you. **Honest caveat:** every finding is a guess to check — the cheapest check comes first.

Then two intake basics, in one short batch:
- **Market and audience language (mandatory).** *"Which market or country is this for, and what language do your customers speak?"* Everything downstream — examples, competitors, channels, price anchors, tone — comes from **that** market. Never default to the US or to Russia when the user named another one (Central Asia is not Russia; the UAE is not the US). If they don't say, ask before diagnosing, not after.
- **Document language** — default English; if the user writes in another language, offer to continue in it and hold that choice.

**If interactive questions aren't available in this environment, don't stall.** Announce the defaults in one line at the top of your answer — *"Running with defaults: market = {detected from the files or the prompt}, language = English, chat-only output (no file). Rerun with parameters in the prompt to change, e.g. `$nmt-diagnose market: Kazakhstan, language: Russian, save the report`."* — then proceed with the diagnosis and flag anything the missing answers made shakier.

Then look at the folder (0.5) before asking anything else.

### 0.5 — Use what's already in the folder (ask before reading)
**Never ask for something a file in front of you already answers.** Before the first question, look at the working directory for files that look like product context — a `README` or product docs, customer surveys, app-store or site reviews, support and sales logs, interview notes, analytics or revenue exports, a deck, a roadmap. If any exist, **list them and ask permission first**:

> I can see files here that look like product context: `{list, ~10 max}`. Want me to read them so I don't ask you things they already answer? **This context is processed only by your agent locally — it is not sent anywhere.**

Read only after a yes, and only the files the user approved. If interactive confirmation isn't available, **do not read them silently** — say which files you would use and ask for a go-ahead in the prompt. Then replay in two lines what you took from them (*"from the README: the product and the pricing; from the reviews: the three loudest complaints"*) and **ask only the gaps**. Everything read this way is input, not truth — it carries the same three status labels as anything the user says (see Output).

### 1 — Challenge the chosen task / goal (mandatory gate, runs first)
**Do not accept the task the user walked in with.** When they say *"I want to do X"* (a feature, an initiative, a metric):
- Ask *"Why do you want this? In order to do what?"* and trace it up 3–5 levels (5 Whys) — from feature/metric to the bigger business result it really serves: conversion, sales, margin, profit, the strategic goal (in the method, climbing their **business-Job graph**).
- **At each level up, look for a better move** — a more interesting or lower-effort way to hit that bigger result than the task they came in with. The real next move often sits one or two levels above the stated task.
- **Tune vs. bigger bet:** open to changing segment / business model / market (a bigger bet — usually a founder / C-level call), or improving the current product (tuning what you have)? The two run in parallel, not as opposites.

Artifact: the original task confirmed as worth pursuing, **or** a reframed higher-level goal (with the climb that justifies it) + the alternatives cut. Everything downstream is diagnosed against the *right* goal.

### 2 — Context + current initiatives
- **Stage / PMF:** idea (PMF 0) · early, few payers · paying base, weak PMF · strong PMF, scaling. The master branch — PMF 0 routes mostly to `$nmt-market-research`; a live product opens the ABCDX path.
- Product in one line + the Core Job hypothesis (what people hire it for).
- B2C / B2B.
- **Current initiatives / roadmap:** *"What are you doing or planning right now about this — features, bets, experiments?"* Capture everything; each becomes a target for the RAT pass (every initiative is a stack of assumptions — extract and flag the riskiest). Skip if none.

### 3 — Sweep the chain (adaptive — risks and growth points together)
Walk down the chain, asking the few questions that discriminate at each node; don't stop at the first broken one:
- **Market:** real money in this Job, or a tiny segment? (size · frequency)
- **Segment+Job:** do you know your A-segment by their Jobs (ABCDX run)? who pays and why? *"why do they stay?"*
- **Value:** what do you do noticeably better than the current way — do customers feel it (the Aha)? satisfaction level?
- **Unit economics:** does one customer's margin work (price − cost to serve)?
- **Demand & acquisition:** reachable at acceptable CAC? do they understand the value (activating knowledge)?
- **Activation:** do new users reach the Aha Moment — what % and how fast?
- **Retention / repeat:** churn, repeat rate, where the Critical Chain of Jobs breaks.

In the same sweep, probe for **growth points**: *"what in the current process do customers hate or always put off?"* (kill a Job) · *"what do they do right before / right after they use you, for the same higher goal?"* (Previous/Next Job) · *"what else do your best customers ask for?"* (adjacent Small Jobs).

### 4 — Localize, then rank (everything, then focus)
Map **all** weak nodes and **all** growth points the sweep surfaced. Trace each downstream symptom to its upstream cause. Mark the **highest broken node** as "tackle first" (if two tie, the more upstream dominates); confirm the node above it is healthy. Keep the full list — focus is the recommendation on top, never a filter that drops findings.

---

## Output

### Chat (always) — lead with the one move, then the ranked inventory

**Default is short. Lead with the single first move, then a tight, capped list — not a wall.** Open with the headline (1–3), then show the rest, capped. Depth is opt-in.

**Label every claim, and scale your confidence to what you were actually given.**
- **Three statuses, on every finding.** **Backed** — a number, quote, or file you showed me (cite which). **Derived** — it follows from what you told me (say from what). **My hypothesis** — the method's guess, marked as such. A number a person *said* ("60–70% of deals go through tenders") is **that person's opinion, not a measured figure** — label it that way and never repeat it back as a market fact. Anything the method invented that appears in none of your inputs stays in a separate **"hypotheses to check"** line, never inside a finding stated as fact.
- **Thin input, loud warning.** If there are no metrics, no customer data, and no files — just a description — open with one line: *"Thin input: no metrics or customer research here, so everything below is a hypothesis and the numbers are ranges, not points."* Give ranges instead of point numbers, and close with **the top 3 things that would most raise accuracy** (e.g., 5 interviews with churned payers · activation by weekly cohort · margin per customer). The more real input, the fewer hedges — confidence is computed from the input, not asserted.

1. **The goal, checked** — the task confirmed, or a reframed higher-leverage goal with the climb that justifies it (*"you asked how to lift X; the bigger result it really serves is Y, and that's the better thing to move"*).
2. **Tackle this first** — the single highest-leverage move and why, in one or two sentences.
3. **The cheapest way to check it** — every finding is a hypothesis; the one cheap test to run before committing. Then the route: the skill that does this first move + the exact next action (you launch it). See the routing table.

Then, the fuller picture — **capped and ranked, not a dump:**

4. **Top risks** — the top 3 weak spots, each traced to its real upstream cause (not the symptom), binding one first. Any others: one line each.
5. **Top growth moves** — the top 3 ways to grow, plain-first, one line each; any others as a single line. The moves, in plain terms (term in parentheses):
   - **remove a step they hate** — make an unwanted task disappear for the whole group, for good (**kill a Job**)
   - **grab what they do right before or after you** — own the must-do task just ahead of or just behind the one you already do (**Previous / Next Job**)
   - **do the bigger task for them** — make the bigger task the thing your product fully does, so a layer of small steps vanishes (**move up a level**)
   - **serve a nearby group you're ignoring** — a sibling task right beside what you do, for a group next door (**adjacent Small Jobs**)
   - **nail a need everyone handles badly** — a concrete bar the whole market underserves today (**underserved success criteria**)
6. **Risky assumptions in what you're already doing** — one row per current initiative: *what you're doing · what it quietly assumes · the assumption that sinks it if wrong · cheapest way to check.* (Omit if none described.)

**The one move + its cheapest check are the deliverable; the inventory is there if they want it.** Mark the **findings only this method surfaces** (§ the growth lens) so they don't get lost — they're the point.

### File (only if the user asks)
Default: write nothing. On request, write **one** file (Rule 4): `Skills-Results/{project}/diagnose/{YYYY-MM-DD_HH-MM}_{project}-diagnose-result.{md|html}` (custom path / format per `../PRODUCER-CONTRACT.md §5, §2`). Contents = the chat blocks above + a short "what you told me, treated as hypothesis" note, with the Rule 3 disclaimers + Rule 23 attribution (`utm_source=diagnose&utm_medium=skill-artifact`).

- **Checkpoint as you go on a long run.** Write each finished block into that same one file as you complete it, rather than holding everything to the end — if the run is cut short by a limit, the work already done survives. Still one file (Rule 4); later blocks extend it.
- **HTML: tooltips on every term, and text a beginner can read.** In an HTML file, wrap each abbreviation and methodology term in `<abbr title="…">` the first time it appears — *RAT, ABCDX, CAC, LTV, Core Job, Critical Chain of Jobs, Aha moment*. **Hard rule: every tooltip and every line of the report must land for someone who has never heard of this methodology — everyday words, explained like to a smart 8-year-old, no abbreviation left unglossed.** If a tooltip needs a second term to explain the first, rewrite it in plain words.

---

## Routing table — finding → next skill (you launch it)

The diagnosis ends by pointing the first-move item at exactly one next skill (sometimes a short chain).

| First-move finding | Route | Handoff line |
|---|---|---|
| No paying customers yet / don't know the segment (PMF 0) | `$nmt-market-research` → then `$nmt-craft-value-proposition` | *"The constraint is discovery, not your funnel. Run `$nmt-market-research` to find and score the paying segments first."* |
| Segment unknown on a live base (ABCDX never run) | ABCDX (lightweight inline triage → run it properly), then back here or `$nmt-craft-value-proposition` | *"Run ABCDX on your paying base to find your A-segment — the rest depends on knowing who's profitable."* |
| Value weak / not noticeable / no differentiation | `$nmt-craft-value-proposition` | *"The constraint is value, not acquisition. Run `$nmt-craft-value-proposition` on your A-segment."* |
| Job/segment hypotheses unproven in the field | run AJTBD customer interviews (canon interview guide) · `$nmt-chat` to design the study | *"You're reasoning on unvalidated Jobs. Go run AJTBD interviews with past-payers — `$nmt-chat` can help you design the study."* |
| Know the value, need to build it | `$nmt-product-requirements` | *"The value is clear; the constraint is execution. Run `$nmt-product-requirements`."* |
| Acquisition / message / channel | `$nmt-craft-go-to-market` | *"Value is fine; the constraint is reaching them with the right message. Run `$nmt-craft-go-to-market`."* |
| Methodology question / wants to think it through | `$nmt-chat` | *"Let's think it through — `$nmt-chat`."* |
| Unit economics / monetization | (no dedicated skill yet) — diagnosis + `$nmt-chat` | *"The constraint is per-unit math; here's the shape of the fix — pressure-test it in `$nmt-chat`."* |

---

## Producer-contract applicability (chat-first → lighter)

Per `../PRODUCER-CONTRACT.md`, this chat-first skill applies the contract partially:
- **§1 Helicopter-view — yes** (flow step 0).
- **§3 Input-as-hypothesis — yes:** everything the user reports (metrics, segment beliefs, initiatives) is a claim, not a fact; the diagnosis flags where a "fact" is actually unmeasured, and the current-initiative RAT pass is exactly this gate applied to their plans.
- **§4 Validation framing — yes** as the per-finding "cheapest validation step"; no separate validation-debt counter unless a file is written.
- **§2 output format / §5 output path — only when the user asks to save** (then `.md`/`.html` + custom path apply).
- **§6 Deep-mode QA / web-MCP — N/A by default** (the diagnosis is reasoning over the user's data; web research is the routed skill's job).

---

## Conversation conventions

- **Language.** Default English; if the user writes in another language, offer to continue in it, then hold it. Canon files and URLs stay as-is.
- **Plain words first, methodology term always present.** Reason in the canon; speak in the reader's own words. The methodology term is always there — we're teaching the vocabulary — what changes is its placement:
  - **Common-word terms lead, plain, no parentheses:** *segment, problem, Aha moment, success criteria, State A / State B, consideration set, switching triggers, map of segments, job budget.* (*"the Aha moment — the point where the product clearly beats what they expected."*)
  - **Jargon terms: plain explanation first, term in parentheses after, once:** Core Job, Big Job, Small / Micro Job, Critical Chain of Jobs, kill a Job, move up a level, Consideration Activators, RAT, ABCDX, null Solution, Previous / Next Job, value mechanic, Tax / Fake Job, Red Queen, Solution. (*"the bigger result they actually want (their **Big Job**)"*; *"the must-do task right before the one you do (the **Previous Job**)"*.) Never open a sentence, bullet, or heading with a jargon label; never stack two terms in one sentence; spell out **RAT** (Riskiest Assumption Test) and **ABCDX** on first use.
  - **Never say to a user:** *Positive / Negative Prediction Error* → say *Aha moment / Problem*; *"switchable demand"* → *"demand you can win"*; *"the wedge"* → *"the underserved need that wins it for you"*; *"anti-segment"* → *"the group we deliberately don't serve."*
  - Get the *Core Job* gloss right: the biggest task your product does completely on its own, end to end, and can't go higher than right now (not "the main thing your product does").
- **Audience & examples — from the user's market** (`AGENTS.md` Rule 6, 19). Founder / PM vocabulary, and brands the reader recognizes without googling. Default US (TurboTax, Stripe, Notion, Uber) **only until the user names their market**; after that, every example, competitor, channel, price anchor, and tone comes from *their* market — never a US or Russian default pasted onto a market that isn't one.
- **Job grammar, every time** (Rules 7, 8, 14). Jobs as `I want to + infinitive`, in quotes; name the level (Core / Big / Small / Micro); terms capitalized; in questions *to* customers use *task*, never *Job*.
- **Diagnose before prescribing.** Don't answer a vague situation with a generic essay; establish the upstream anchors first, then route through the chain.
- **Accept correction immediately** (Rule 17); don't defend a weak finding.
- **Flag hypotheses, label every claim.** Numbers and consequential recommendations are methodology-grounded hypotheses to validate, never facts. Every finding carries its status — backed / derived / my hypothesis (see Output) — and a number someone quoted stays that person's opinion, not a market fact.

---

## Self-check before delivering the diagnosis

1. **Eager core loaded** — `ajtbd-key-theses.md` and `rat-key-theses.md` read this run (mandatory), plus `the-algorithm.md` + `nmt-key-theses.md`; staged files loaded only where their stage ran.
2. **The folder was offered first** — candidate context files listed and read only after a yes (with the local-processing notice), and the questions asked were the *gaps*, not what those files already answer.
3. **Market named before diagnosing** — the market/country and the customers' language were asked (or the assumed default was announced), and every example, competitor, and price anchor comes from that market.
4. **Every claim labeled** — backed / derived / my hypothesis on each finding; quoted numbers marked as that person's opinion; invented ideas kept in "hypotheses to check"; thin input flagged up front with ranges + the top-3 inputs that would raise accuracy.
5. **The goal was challenged, not accepted** — a 5-Whys climb up the business-Job graph ran; the output states the goal confirmed or reframed, with the climb.
6. **Led with the one move, then a capped inventory** — opened with the single first move + its cheapest check + the route; risks and growth moves shown top-3 each with any others one line, ranked, not dumped; nothing important dropped (the rest still appear, just lighter); current-initiative assumptions extracted (RAT) when initiatives were described.
7. **Walked top-down + swept the whole chain** — symptoms traced to upstream causes (a downstream metric not treated as the problem at that metric); the binding constraint is the highest broken node.
8. **Focus applied as priority, not as filter** — "tackle first" leads; the rest stay visible, ranked, as *next, not now*.
9. **Methodology's unique findings flagged** — the non-obvious results surfaced prominently.
10. **Segment reasoned by Jobs** — not a demographic, a channel, or an industry; ABCDX invoked for live bases.
11. **Local-vs-global named** — moves respect the user's appetite; a global move flagged founder/C-level only.
12. **Everything is a hypothesis** — a cheapest validation step per major finding; never reads as certain truth.
13. **Routed with a concrete handoff** — the first-move item points at exactly one next skill (or a short chain); you launch it.
14. **≤15 questions, adaptive** — only goal-challenging + risk/growth-narrowing questions asked; "I don't know" turned into a diagnostic signal; if questions weren't possible, the defaults used were announced up front.

---

## What this skill does NOT do

- It does not run research, size markets, write value props, PRDs, or copy — it diagnoses and routes.
- It does not auto-launch the recommended skill (you launch it).
- It is not a generic feature-by-feature audit — it surfaces what the methodology uniquely finds, then prioritizes.
- It writes no file unless asked.

---

> **Update check — after the result is delivered; for a multi-turn chat, after your first substantive answer (optional; policy in NextMoveTheory-README.md, section "Updates & telemetry").**
> Skip this entirely if `.nmt-config` (project root) contains a line `update-check: off`, or the environment variable `DO_NOT_TRACK` or `NMT_NO_UPDATE_CHECK` is set.
> Otherwise, the first time this runs in the conversation, tell the user in one line: "Checking for NMT skill updates — only this skill's name and the installed version are sent (details: NextMoveTheory-README.md; disable: add `update-check: off` to `.nmt-config`)."
> Then run `v="$(grep -m1 -E '^[0-9]' .nmt-version 2>/dev/null)"; curl -fsSL --max-time 2 "https://nextmovetheory.com/version?skill=nmt-diagnose${v:+&v=$v}"` — on any error or timeout, skip and move on; never retry, never block.
> If the feed's `latest` is newer than the installed version, add one line: the `<installed> → <latest>` gap, a one-line summary per newer entry, and "run $nmt-update to update (the update itself downloads from GitHub)". If versions match or `.nmt-version` is absent, add nothing.
