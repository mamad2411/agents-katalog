---
name: nmt-analyze-interviews
description: >-
  Extract the AJTBD structure from customer-interview files you already have —
  segments by Core Jobs, personas, the Consideration Set, existing Solutions and
  Problems, and value hypotheses — using Ivan Zamesin's Next Move Theory /
  Advanced Jobs To Be Done methodology. Input — one or many files (transcripts,
  notes, sales or support calls, survey open-ends), AJTBD or not. It reads each
  interview in its own context so it never overflows, scores each extraction's
  confidence, clusters into segments by similar Core Jobs, and writes one report —
  data-quality summary, segments with personas, structured Solutions and Problems,
  a Consideration Set, value hypotheses, and what to interview next. Use for
  "analyze my interviews", "extract jobs from these transcripts", "find the
  segments in these calls". Defaults to English.
user-invocable: true
---

# Analyze Interviews v1

> **v1 in one breath.** You already ran the interviews; this skill pulls the methodology out of them. It takes **one or many** interview files (transcripts, notes, sales calls, support logs, survey open-ends — AJTBD or not, good or bad), asks **which business task** you're solving (and helps you pick one if you can't), then reads **each interview in its own subagent** — a fan-out that keeps the run from ever overflowing context no matter how many large transcripts you load. Each interview is distilled to the AJTBD constructs with an **honest confidence** (a clean Core-Job extraction vs. a weak hypothesis) and **per-interview feedback** (what was found, what's missing, whether this interview can serve your task). The distillations are clustered into **segments by similar Core Jobs + similar success criteria + similar priority order**, and each segment's confidence is **computed from its supporting interviews' confidence**. Output — one report: data-quality summary, segments with personas, structured Solutions + Problems, a Consideration Set per segment, value hypotheses, and what to interview next.

> **Producer contract (binding) — `../PRODUCER-CONTRACT.md`.** Eleven cross-cutting behaviors shared by all producer skills: (1) print a **helicopter-view** before the first question; (2) ask **Markdown or HTML** output; (3) treat **all** user input as hypothesis and emit a *"risks I see in what you gave me"* block — here the inputs are interviews, so this becomes the per-interview quality read; (4) print **validation framing** — extracted Jobs are hypotheses with a confidence, only as strong as the interviews behind them; (5) accept a **custom output path**; (6) Deep mode runs an **evidence floor + self-critic loop** and offers a **web-MCP fallback**. Five more came from the anti-hallucination pass: (7) ask the **market + audience language** and build every example, channel, and price anchor from it; (8) **list the repo-context files found on disk and read them only after a yes**; (9) every claim carries its **status** — backed, derived, or the model's own hypothesis; (10) **frequency counts on every aggregated claim**, and a single source never carries a segment-level conclusion; (11) **confidence scaled to the input** — thin input gets ranges, a visible warning, and the top-3 inputs that would fix it. The hooks below wire each into this skill.

> **New here, or not sure this is the right skill?** Start right here — or run `$nmt-chat`, describe your situation, and it points you to the right one. Quick map: **new idea →** `$nmt-market-research` · **live product or a metric moved →** `$nmt-diagnose` · **have customer interviews →** `$nmt-analyze-interviews` · **ready to build →** `$nmt-product-requirements` · **positioning / launch copy →** `$nmt-craft-value-proposition` → `$nmt-craft-go-to-market`.

## Where this skill sits

The **post-fieldwork half of the interview loop** — the study design and interview guide *before* the field are a separate (not publicly shipped) product; ask `$nmt-chat` to help you prepare interviews. This skill analyzes the transcripts *after*. Distinct from `$nmt-market-research`, which **invents** segments from web research and reasoning — this skill **reconstructs** segments from *your real interviews* and tells you how far the data can be trusted. Its output feeds `$nmt-craft-value-proposition`, `$nmt-diagnose`, and `$nmt-craft-go-to-market`.

| Skill | Input | Answers |
|---|---|---|
| `nmt-chat` (interview prep) | segment + Job hypothesis | help designing the study before the field |
| **`nmt-analyze-interviews`** | **the interview files you already have** | **what's in them, the segments by Core Jobs, and whether the data can solve your task** |
| `nmt-market-research` | an idea / product | market size + GO/NARROW/PIVOT (segments invented from research) |

## What this skill produces

**A single file** (one file per run — `AGENTS.md` Rule 4) with:

1. **Data-quality summary** — how many files, the type/quality mix (AJTBD / partial / non-AJTBD; well / poorly conducted), and whether the set can serve the chosen business task.
2. **Segments by Core Jobs** — each with a persona (= the causal criteria), Core Jobs in canon grammar, Big Jobs, **a confidence level and the interviews it stands on.**
3. **What they use today and where it falls short** — for each tool they hired, the set of tasks it does for them, and each problem traced to the task it botched (task → tool → problem). DIY counts as a tool.
4. **What they weighed before choosing** — the options, how they compare, the named products plus a way in, and their fears (their consideration set), as its own block.
5. **Value-creation hypotheses** — underserved success-criteria + a one-line mechanic direction (no feature list — that is `$nmt-craft-value-proposition`'s job).
6. **Single signals** — everything said by exactly one person, held out of the segment conclusions until it's checked.
7. **Hypotheses to validate** — ideas the model added that nobody in your files said, kept clearly apart from the findings.
8. **Source → segment map + per-interview appendix** — every file, its assigned segment, an anchor quote, and what was extracted from it.
9. **Gaps + what to interview next** — what the current data cannot answer for the task, and whom to re-recruit (past-payment screener).

**Two modes:**
- **Quick (default):** no internet. Subagents distill each interview; one Codex agent synthesizes the segments.
- **Deep (opt-in, longer):** also sends web subagents to enrich the competitor / Consideration-Set picture and mine real review language around the Jobs surfaced. See "Deep mode" at the end.

---

## Methodology — source of truth (progressive loading)

The **only** source of methodology is the Next Move Theory canon, read at runtime. **Don't load all of it up front** — read the eager core first; pull staged files only when the run reaches the stage that needs them.

**Eager core (the orchestrator reads before synthesis — every run):**

| File | What it powers | ~tokens |
|---|---|---|
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md` | the whole model: Job, Job Graph, value, the Aha Moment, the segmentation root | ~13k |
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/segmentation.md` | clustering into segments; causal vs. symptomatic criteria; persona = causal criteria | ~5k |

**Each distiller subagent reads (its slice only):**

| File | Why | ~tokens |
|---|---|---|
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/job-structure.md` | the eight Job elements + the per-element extraction question + the quality signals | ~9k |
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/job-types-and-properties.md` | typing the Job (Fake / Tax / Orientation / Emotional / Viral / Regular); the Fake-Job past-behaviour test | ~5k |

**Staged — the orchestrator loads only at the stage that uses it:**

| File | Load when | Used by | ~tokens |
|---|---|---|---|
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/consideration-activators.md` | writing the Consideration Set per segment | the four-slot container + the five Activators | ~4k |
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/critical-chain.md` | the task is conversion / retention / acquisition | Previous / Next Jobs, chain breaks, Aha placement | ~6k |
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/behaviour-change.md` | extracting switching barriers / fears | the blockers, Solution-as-label, habit, fears | ~10k |
| `Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/value-creation-mechanics.md` | generating value hypotheses (Section 5) | the published mechanic menu | ~5k |

> **Path note.** Use the paths above. If a file is not found, retry with a `1-` prefix on the canon folder (`1-Next-Move-Theory-Canon/...`) — the source repo orders folders with a numeric prefix the public repo strips.

**Do NOT use generic JTBD from the internet or prior training.** Ivan Zamesin's AJTBD diverges substantially. The mis-defaults to never propagate (per the project `AGENTS.md`):
- A **Job** is a desired *transition* — State A (situation) → expected outcome (State B), in order to perform a higher-level Job. Not "a struggle for progress."
- `I want to + verb` is the **primary element** of an eight-element Job, not the whole Job. **Each infinitive verb is a separate Job** — parse multi-verb statements into the hierarchy.
- A **Problem** is a consequence of a Solution hired for a Job and underperforming its success criteria — not a root cause.
- **Value** is greater energy efficiency for the brain in performing a Job, vs. its prediction; the **Aha Moment** is the customer-experience of value beating prediction; the **Problem** is value falling below it. Never use the abbreviations PPE/NPE.
- A **Solution** is a real thing in the world *and*, inside the Job Graph, a label for the sub-graph of Core + Micro Jobs it installs. DIY ("I just did it myself") is a Solution too.

**Methodological invariants — output is invalid if any is violated:**
- Segments are formed by **similar Core Jobs sharing similar success criteria *in a similar priority order*** — never by demographics, industry, or Big Job as the primary cut. *Speed-first* vs *no-stress-first* on the same Job = different segments.
- A "real / causal" segmentation criterion is a **cause** (a behaviour or characteristic that changes value, margin, or demand), never a paraphrased value or a consequence.
- **Study Jobs by past expenditure (money / time / energy), never by future intent.** Future-tense intent with no past commitment is a **Fake Job** — extract its Big Job, never the Fake Job itself.
- Personas are the **causal criteria**; demographics are second-order correlates, never the first cut.

---

## The fan-out architecture (this is what makes the skill scale)

**The orchestrator never reads the raw transcripts into its own context.** It spawns **one distiller subagent per interview** (or per batch of 3–4 short files). Each distiller reads *its* file plus its canon slice and returns **only a compact structured distillation** (~600–1,200 tokens with 2–3 anchor quotes), not the raw text. The orchestrator synthesizes segments from the distillations.

Why this matters: 18 deep interviews at ~8–10k tokens each are ~150k tokens — they cannot fit one 200k window alongside the canon and the report, and forcing them in triggers compaction that *summarizes away the verbatim customer utterances AJTBD depends on*. Fan-out turns ~150k of raw transcript into ~15k of distillation, fits comfortably, and **preserves the exact quotes on purpose.** The concurrency cap handles the rest — pass all N files; they run in waves.

- Distillers run with Codex's available execution (parallel subagents if your build supports them, otherwise sequentially in one context); the orchestrator waits for the wave, collects the returns.
- **No per-interview files.** Each distiller returns its distillation in its final message. The orchestrator holds them in context and writes the one report (Rule 4).
- **Run in waves and checkpoint into the one result file.** Take the set wave by wave (~4–6 files at a time; sequentially if this build has no parallel subagents). After each wave, write that wave's rows into the result file's source → segment map and per-interview appendix — the file is created early, in draft, and grows. If the run is cut off by a context or usage limit, the finished distillations are already on disk and the rerun starts at the first un-checkpointed file instead of from zero. Say in chat which wave just landed and how many files remain. **Without parallel subagents this checkpointing is what makes a large set survivable at all** — after each file, drop its raw text from context and keep only the distillation.
- **Never let raw transcript text stay in the orchestrator's context.** If a distillation runs past ~1,200 tokens or pastes long stretches of transcript, compress it again. The only verbatim text that is carried forward is the anchor quotes.
- **Load canon by stage, not up front.** The orchestrator holds only the eager core and reads each staged file at the stage that uses it (see the loading table above); distillers read their two-file slice only, never the whole canon. This is what leaves room for 18+ transcripts' worth of distillations plus the report.

---

## Plain-language output — the reader is a builder, not a methodologist

Write the report in the plain language the user speaks; when a methodology term genuinely adds precision, lead with the plain meaning and put the term in parentheses the first time — never lead a sentence or heading with a raw term. Keep quotes verbatim. Confidence is reported in plain words (clean read / directional / weak / not usable), with the methodology rubric behind it.

**The zero-knowledge test (hard rule).** Every line of the report — and every tooltip inside it — has to land for someone who has never heard of this methodology. Explain it the way you would explain it to a smart 8-year-old, in everyday words. This covers research and audio jargon too (*speech-to-text*, *speaker separation*, *saturation*, *screener*, *open-end*), not only AJTBD terms. If a sentence only works for a reader who already knows the term, rewrite it.

**In HTML output, every abbreviation and methodology term gets a tooltip on its first use** — `<abbr title="the task a person hires a product to do for them">Core Job</abbr>` — and the tooltip text is the plain-words explanation, not the canon definition. In Markdown the same rule applies without the markup: a short plain parenthetical on first use. (Same as the shared readability gate — `../READABILITY-CONTRACT.md` Gate 9.)

---

## Evidence discipline — how many people said it, and what kind of claim it is

Two labels ride on **every** claim in the report. They are what stops one vivid quote from becoming "the segment's main pain."

**1. How many said it, and which ones.** Any claim made at segment or market level carries a count and the sources behind it: *"said by 7 of 22 interviews: #3, #7, #9, #11, #14, #18, #21."* No count — the claim does not ship.

- **A claim supported by exactly one source may not appear in a segment-level conclusion.** It goes to the separate **"Single signals — verify before acting"** list (report §6) with its interview number and the quote. It may well be true and important; it just isn't yet evidence about a group.
- Count against the people who *could* have said it, and state that denominator: *"4 of the 9 who had used a competing tool"* is a real number, *"4 of 22"* hides one.
- The quote illustrates a counted claim, never replaces it. Pick the anchor quote **after** the count, from inside the counted set.

**2. What kind of claim it is.** Every claim is one of three and says which:

| Status | How it is written |
|---|---|
| **Backed** — a quote or a figure taken from the source material | cite it: the verbatim quote + the interview # |
| **Derived** — worked out from the data | say from what: *"derived from the 6 interviews where the trial stalled before the first export"* |
| **The model's own hypothesis** | marked as such, and it lives only in "Hypotheses to validate" (report §7) |

- **A number a respondent says out loud is that person's opinion, not a market fact.** *"60–70% of deals go through tenders"* is written *"per the sales lead in #4 — their estimate, not a measured figure."* Never promote such a number to a headline, never average several of them into one figure.
- **Explanations from founders, managers, and salespeople are claims about the world, not observations of it.** What they did and saw is data; why they think it happens is their opinion, recorded with the role attached.
- **An idea that appears in none of the sources may never enter the segments, the Problems, or the value hypotheses as fact** — a warranty nobody mentioned, a price sensitivity nobody voiced. If it is worth keeping, it goes to "Hypotheses to validate" with the cheapest check that would confirm or kill it.

---

## Output file (one file per run — `AGENTS.md` Rule 4)

The skill writes **exactly one** file. Default location (unless the user gave a custom output path in intake — `PRODUCER-CONTRACT.md §5`):

```
Skills-Results/{product-slug}/analyze-interviews/{YYYY-MM-DD_HH-MM}_{product-slug}-analyze-interviews-result.{md|html}
```

- **Extension follows the chosen output format** (`PRODUCER-CONTRACT.md §2`): `.md` (default) or one self-contained `.html` (inline CSS, working in-page anchors, `<details>` for the per-interview appendix and the long segment blocks, `<abbr title="…">` tooltips on every term's first use, source links opening in a new tab). HTML carries identical content. Never write both; one file per run.
- If the user gave a custom path, write the one file there with the same filename pattern.
- `{YYYY-MM-DD_HH-MM}` (24h local time) makes each run unique; reruns never overwrite.
- Everything internal (the distillation traces, discarded clusters, the climb from a Fake Job to its Big Job) stays in-context, not in a separate file.

**Disclaimers (Rule 3) at the very top of the file (once):**

> ⚠️ **Numerical disclaimer.** Every confidence level, segment size, and Job-budget figure here is an LLM-generated estimate from your interviews — including the confidence scores themselves. Treat them as a reading of your data's strength, not a measurement. Validate before any expensive decision.
> ⚠️ **Hallucination disclaimer.** This document is generated by an LLM and may contain hallucinations in unknown places — including Jobs read into a transcript that the respondent didn't actually express. For decisions with expensive consequences, re-read the anchor quotes and run a confirming interview pass; do not act on this document alone.

**Attribution (Rule 23).** Open with the attribution top-line (first content, above the disclaimers) and close with the attribution block — `utm_source=nmt-analyze-interviews&utm_medium=skill-artifact`.

---

## STAGE 0 — Orientation (helicopter view) + language & market

**First, the orientation block** (`PRODUCER-CONTRACT.md §1`) — before any question, in plain words:

> **What you'll get:** one report — the customer segments hiding in your interviews (grouped by what they hire a product to do), each with a persona, the existing solutions they use and where those fall short, what they weigh before choosing, value ideas, and — honestly — how much your interviews can be trusted to answer your question.
> **The steps:** (1) you tell me the business task you're solving (I'll help if you can't name one) → (2) you point me at your interview files → (3) I read each one separately and pull out the tasks people hire a product for, with an honest confidence → (4) I tell you, per interview, what I found and what's missing → (5) I cluster them into segments and tell you which ones the data really supports → (6) one report, plus what to interview next.
> **Where I work vs. where you decide:** I extract and cluster what's in the transcripts; I can't add what isn't there. Where an interview is thin, I'll say so and tell you what to ask next time.
> **Two modes:** *Quick* (default — no internet; reads and synthesizes your files) · *Deep* (opt-in — also researches the real competing products and review language around the tasks I find, to enrich the competitive picture).
> **Honest caveat:** the output is only as good as your interviews. If they're about hypotheticals or never touched a real past purchase, I'll flag that — and the right next step is better interviews, not a prettier report.

Then **document language.** Default to **English**; if the user writes in another language, offer to work in it (`request_user_input`: English (Recommended) / their language; for another language, ask directly in chat). Hold the choice; all communication and the file use it; canon files and URLs stay as-is.

Then **the market** (`PRODUCER-CONTRACT.md §7` — mandatory, never inferred). Ask in the same breath: *"Which market or region are these customers in, and what language do they speak?"* Never infer it from the user's own language or from the fact that most examples you know are American. Everything market-shaped in the report comes from that answer — the named competitors and Consideration Set, price and Job-budget anchors, the channels in §9. If the interviews themselves name a different market, say so and confirm which one to write for.

> **If interactive input isn't available — don't stall, announce the defaults and proceed.** Codex often can't collect answers mid-run. In that case state them in one line at the top of your answer: *"Running with defaults: Quick mode, business task inferred as {…}, language {detected}, market {detected from the files — say which}, output MD, files {the paths you gave me} — rerun with parameters in the prompt to change, e.g. `$nmt-analyze-interviews deep, task: retention, market: Kazakhstan, output: html`."* Then run. The one thing you may not default away is the file list — with no interview files and no way to ask, say so and stop. Every inferred default is flagged again in §1 of the report as an assumption.

---

## STAGE 1 — The business task (asked first — it is the spec on the extraction)

The chosen business task changes *what to dig for and at what altitude* — the canon: *"the shortlisted mechanics are the spec on the research… without them you interview blind"* (`Next-Move-Theory-Canon/Algorithms/the-algorithm.md`). So pin it before extracting. Run this waterfall:

1. **Ask directly** (`request_user_input`) — *"What business task are you trying to solve with these interviews?"* — offer the menu below.
2. **If the user can't name one** → *"Describe in your own words what you're trying to figure out or fix."* (free text).
3. **Infer from the description.** If you can confidently map it to a task on the menu, **play it back in one sentence and confirm.**
4. **If you can't confidently map it** → propose the **2–4 most likely tasks** (`request_user_input`) and let the user pick.
5. **If several tasks apply** → ask them to rank; the top one drives extraction emphasis, the rest are secondary.

**Business-task menu** (distilled from the canon's Algorithms + mechanics catalog — `Next-Move-Theory-Canon/Algorithms/the-algorithm.md`, `Next-Move-Theory-Canon/Next-Move-Theory/mechanics-catalog.md`; cited as provenance, no need to read them for the menu):

- **Create value / beat competitors** — perform the Jobs more efficiently than the alternatives.
- **Increase conversion to sale / activate customers into value** — repair the path to the first Aha Moment.
- **Increase retention / decrease churn** — keep customers using it over time.
- **Increase repeat / return rate** — get the same customer back more often.
- **Increase average order value / improve unit economics** — lift value per customer / make the math close.
- **Launch / find PMF / find a segment / validate value** — for an early product.
- **Position & differentiate** — communicate validated value to a validated segment.
- **Grow / scale an existing product** — more segments, sub-segments, geographies, or more of one customer's Jobs.
- **Escape direct competition / climb a level** — relocate where you compete.
- **Not sure / challenge my goal** — a "broken metric almost never sits where it shows" → diagnose upstream (route to `$nmt-diagnose` if it turns out there are no interviews to analyze yet).

**Hold the chosen task** — STAGE 3 conditions the extraction on it (see "Business-task → extraction emphasis").

---

## STAGE 2 — Intake the interviews + run settings

Collect in a short stream + one or two batched `request_user_input` calls (max 4 each).

### Step 1 — The interview files
> Point me at your interviews — a folder, or a list of files. They can be deep-interview transcripts, interview notes, sales-call or demo recordings turned to text, support or chat logs, or open-ended survey answers. One file or many; AJTBD-style or not; polished or rough — I'll sort the quality myself.

- Accept a **folder path** (read every text-like file inside) or a **list of paths**. Supported: `.md`, `.txt`, `.docx` (read as text), `.vtt` / `.srt` (strip timestamps), `.csv` (survey open-ends — one row = one mini-interview).
- Everything taken from the files is tagged **[user data]** in-context. **All of it is hypothesis** (`PRODUCER-CONTRACT.md §3`) — an interview is the respondent's account, not ground truth; a sales call is a pitch, not a Job study.
- **Light context (optional, free text):** the product these interviews are about, and the segment(s)/Jobs the user already believes exist — held as *prior hypotheses to test against the data*, never merged in as fact.

### Step 1b — Files already sitting in the working folder (ask before opening any of them)
If the working directory holds anything that looks like product context — a `README`, product docs, a survey export, a review dump, an analytics or CRM/deal export, older interview notes — **list the candidates and ask permission before reading them**:

> I see these files in your folder that might be useful context: {list}. Want me to read them? **This context is processed only by your agent locally — it is not sent anywhere.**

Read only what the user says yes to; a "no" is final, don't re-ask mid-run. If interactive input is unavailable, the default is **not** to read them — list what you saw and say the rerun can include them. Anything read this way is [user data] and hypothesis like everything else (`PRODUCER-CONTRACT.md §3`) and enters the same evidence discipline: a deal export is data you can count, a README is the team's claim about their own product.

### Step 2 — Batch: mode, output format, output path
- **Mode** — Quick (default; no internet) / Deep (subagents + web — enrich competitors + Consideration Set + review language).
- **Output format** (`PRODUCER-CONTRACT.md §2`) — Markdown (default; faster) / HTML (collapsible appendix + working navigation; links stay clickable).
- **Where to save the result** (`PRODUCER-CONTRACT.md §5`) — default `Skills-Results/{product}/analyze-interviews/…` / or a folder path to match your repo. One file per run regardless (Rule 4).

**Hold** everything in context.

---

## STAGE 3 — Per-interview distillation (the fan-out)

Spawn **one distiller subagent per interview** (batch 3–4 short files into one agent). Each distiller reads its file + `job-structure.md` + `job-types-and-properties.md`, applies the **extraction schema** and the **quality rubric** below, conditions its dig on the **chosen business task**, and returns a structured distillation. The orchestrator collects all returns.

### The extraction schema (what each distiller pulls)

For every distinct Job episode in the interview, extract the **eight Job elements** and the companion Solution (`job-structure.md`; `ajtbd-key-theses.md §3`):

1. **Context** — the person/situation features that make them want *this* outcome with *these* criteria (keep only features that change a criterion; discard background noise).
2. **Negative emotions (State A)** — what they felt *before*, while the result wasn't reached. Absence is not evidence of absence — flag "not surfaced," don't record "none."
3. **Consideration Set** — which ways of getting the higher-level outcome they weighed (four slots: known Job Graphs · comparative efficiency · named products + entry path · fears).
4. **Trigger** — the concrete moment that flipped them from thinking to acting (a moment in time, not "when I felt ready"). For recurring Jobs, the schedule substitutes.
5. **Expected outcome** — the `I want to + verb` clause, captured **verbatim**. A noun ("rental management") has the verb amputated — push to the verb. **Each infinitive verb is a separate Job** — parse stacks.
6. **Success criteria + priority order** — the concrete, measurable conditions for "good enough" (direction + level). Adjectives ("fast," "reliable") are wishes — push to a number/fact. **Capture the ranking** — which criterion is non-negotiable, what's traded off. The priority order is itself a segmentation criterion.
7. **Positive emotions (State B)** — how they wanted to feel after (dig past first-pass facts to the named emotion).
8. **Higher-level / Big Job** — climb "in order to…" until answers repeat (repetition = you hit the need; don't record the need as a Job). Don't claim the Big Job as what the product delivers.

Plus, on each Job: **frequency**, **Job budget** (what they paid / spent), **importance** (if elicited); **the chosen Solution** (brand / route / DIY) structured as *label + the sub-graph of Core + Micro Jobs it installs*; the **Job type** (Regular / Orientation / **Tax** / **Fake** / Emotional / Viral); the **Aha Moment** (a pleasant surprise *while using a product*, beating the criteria they came in with); every **Problem** on its `Job → Solution → Problem` chain; **switching barriers & fears** (habit, identity, objective barriers, fears from real past experience vs. imagination); and the **Previous / Next Jobs** in the chain.

**Tag what kind of thing each captured item is** (the distiller does this, so the orchestrator never has to guess — see "Evidence discipline"):
- **Did / saw** — what this person actually did, paid, or witnessed (paid $400 in March, called support twice, switched after the second outage). Data.
- **Their estimate about the world** — a number or share they state about the market, their industry, or other people (*"60–70% of deals go through tenders"*, *"everyone here uses X"*). Record it with the speaker's role and the label *their estimate, not a measured figure*. Never carry it forward as a fact.
- **Their explanation / argument** — why they think something happens, especially from founders, managers, and sales people. Opinion, attributed to the role.
Keep the verbatim wording for all three; the tag rides alongside, it doesn't replace the quote.

### The quality rubric (per interview → a confidence on its Core Jobs)

**Hard gates** (a "no" caps the interview's Core Jobs at *not usable* — Fake-Job risk):
- **G1 — real past expenditure.** Did the respondent actually pay money / spend time / burn energy on this outcome in the past?
- **G2 — they performed the Job themselves.** Are they narrating their own past behaviour (not hypotheticals, not "users in general")?
- **G3 — a concrete past episode exists.** A specific reconstructable instance (one-off) or a clear habitual pattern + frequency (recurring).

**Quality dimensions** (each strong / partial / absent): trigger present · context present · expected outcome as a verb · **success criteria concrete (+ ranked)** · Big Job laddered · emotions surfaced · Consideration Set present · low leading-question contamination · respondent's own words preserved · awareness zone right (a status/identity *why* taken at face value is a quality failure even in a smooth interview).

**Roll-up to a confidence on the Core Jobs from this interview:**
- **Clean read (High)** — gates pass; trigger, context, outcome, concrete ranked criteria, and Big Job all strong; open-first + no leading; Consideration Set present. The eight elements are essentially reconstructable.
- **Directional (Medium)** — gates pass; the outcome and some concrete criteria are there, but gaps (no Big-Job ladder, thin Consideration Set, criteria only partly concrete, some leading). Usable directionally.
- **Weak (Low)** — gates pass but the dig is shallow: abstract criteria only, no trigger, opinions/satisfaction-heavy, heavy leading, or a Zone-2 *why* taken as fact. Only candidate hypotheses survive.
- **Not usable** — G1 or G2 fails, or pure future/hypothetical/feature-wishlist talk with no real episode. Do **not** extract Core Jobs as findings.

### What to still salvage from a Weak / Not-usable interview
Even unusable transcripts aren't zero: climb to the **Big Job above a Fake Job** (often real — "learn Spanish someday" → "feel at home with my partner's family"), record **named Solutions / competitors**, capture **stated Problems** (as orphan symptoms, flag the missing Job), and mine **behavioural signals over self-report**. Label every one a *hypothesis to validate*, never a finding, and route the respondent to a re-recruit on a past-payment screener.

### Distiller return shape (in its final message — no files)
Per interview: usability classification (AJTBD / partial / non-AJTBD; well / poorly conducted) · the rubric verdict (gates + roll-up) · each Job episode with the eight elements + Solution + type + Aha + Problems + barriers + Previous/Next Jobs, **each item tagged did-saw / their-estimate / their-explanation** · 2–3 anchor quotes per Core Job · the per-Job confidence · what's **missing** for the chosen business task · **one candidate anchor quote for the source → segment map.** Cap the return at ~1,200 tokens; compress rather than paste transcript.

### Business-task → extraction emphasis (the delta beyond the always-on spine)
The spine (Core Jobs + ranked success criteria + Solutions) is always extracted. The chosen task tells the distiller what to dig *deeper* on:

| Business task | Dig deeper on |
|---|---|
| Create value / beat competitors | Big Jobs · Consideration Set · Jobs outside Core (Previous / Next / sibling Small) · Problems with current Solutions |
| Increase conversion / activation | Critical Chain breaks before first value · Aha placement · the 3 barriers (don't-see-value / fears / cost) · triggers |
| Retention / churn | Next Jobs · the Aha stream over time · "why they stay" + "why they left" · Problems after start · habit & switching cost · frequency |
| Repeat / return rate · AOV · unit economics | multiple Jobs per person · Job budget · frequency · high-margin criteria |
| Grow / scale | adjacent & sub-segment Job Graphs · Common Jobs across graphs · budget per Job |
| Position & differentiate | Core Jobs + ranked criteria · Big Job · barriers & fears · Aha · triggers |
| Escape competition / climb a level | Consideration Set incl. out-of-category Solutions · the Big Job above · Previous / Next Jobs |

---

## STAGE 4 — Per-interview feedback (what was found + can it serve the task)

From the distiller returns, build the **per-interview feedback** the user asked for — one row per file:
- **Type & quality** — AJTBD / partial / non-AJTBD; well / poorly conducted (with the one decisive reason).
- **What was extracted** — the Core Jobs found (with their per-Job confidence) + the key elements present.
- **What's missing** — the elements absent or thin.
- **Serves the task?** — given the chosen business task, can this interview contribute? (e.g., *"for retention you need Next Jobs and reasons-to-leave; this interview has neither — usable only for Core-Job hypotheses."*)

This is this skill's version of the producer contract's *"risks I see in what you gave me"* block (`PRODUCER-CONTRACT.md §3`): the inputs are interviews, so the risk read is the quality read.

---

## STAGE 5 — Synthesis into segments + confidence propagation

Cluster the distilled Job extractions across all interviews into candidate segments, then score each segment's confidence.

**Clustering rule (the segmentation root).** Two interviewees are the **same segment** when they perform **similar Core Jobs with similar success criteria *in a similar priority order*** (`segmentation.md §2`; `ajtbd-key-theses.md §12`). They are **different segments** if any of these differs: the Core Job; the criteria (same outcome + different criteria = different Job); **or the priority order** (*control-first* vs *done-for-me-first* = different segments). Same surface verb ≠ same segment. One person with several Jobs is **one segment** (their whole graph places them), not many.

**Anti-pattern checklist — run it on every candidate segment before it is written down** (`segmentation.md §2`, `§7`, `§14`). A candidate that trips one of these gets fixed or merged back, and the report says which check fired:

- **A purchase channel is not a segment.** *"Buys through tenders," "came via the marketplace," "inbound vs. outbound"* describes how the money arrived, not what the person hires a product to do. One tender queue holds resellers (Core Job: *"win my client's order at a workable margin"*) next to end users (Core Job: *"keep the line running"*) — different Jobs, different criteria, different products. Split the channel by Core Job; never let the channel itself be the segment.
- **An industry or vertical is not a segment when the Core Jobs and success criteria coincide.** Don't cut a B2B set into "manufacturing / logistics / retail" if all three perform the same Core Job with the same ranked criteria — that is one segment wearing three industry labels. Industry turns causal only when it actually changes the Job, the criteria, the margin, or the buying chain (a certification, an audit, a procurement route). Name the change, with the interviews that show it, or merge (`segmentation.md §14`).
- **Every segment is defined through Core Jobs + success criteria + their priority order.** If the cut in your hand is demographic, firmographic, channel-based, or industry-based, write the causal sentence — *this property changes the value we can create, the margin, or the demand* (`segmentation.md §7`) — and back it with interview numbers. No causal sentence, no segment: merge it and re-cluster on the Jobs.
- **A segment needs more than one source.** A cluster standing on a single interview is a *Hypothesis*, and whatever makes it look distinctive goes to "Single signals," not into a segment description.

**Persona = the causal criteria** (`segmentation.md §7`): the Core Jobs + ranked criteria + the cause-level situational facts that produce them. Demographics are second-order correlates, never the first cut. Each criterion that survives must be a **cause** that changes value, margin, or demand — not a restated value ("they'll save $2,000" is value, not a criterion). Each persona bullet carries its count and interview numbers, like every other segment-level claim.

**Confidence propagation (compute it, show the math — no false decimals).** Each extraction carries its interview's confidence weight: **Clean = 1.0 · Directional = 0.66 · Weak = 0.33 · Not-usable = 0** (Not-usable contributes only Big-Job hypotheses, not segment evidence). For each segment:

- **Support weight** = the sum of the confidence weights of the interviews whose extractions land in the cluster.
- **Saturation** = did new interviews stop adding new Core Jobs / criteria to the cluster? (a qualitative yes/partial/no).
- **Coherence** = how tightly the criteria *and* the priority order agree inside the cluster. A split priority order is a signal to **split into two segments**, not to average.

Roll up to a plain-language segment confidence (tune the thresholds to the data, state them):
- **Solid** — support weight ≥ ~3, coherent, saturating.
- **Emerging** — support weight ~1.5–3, some coherence.
- **Hypothesis** — support weight < 1.5, a single supporting interview, or incoherent.

Always render the support transparently: *"Segment B — Emerging; stands on interview #2 (Clean), #5 (Directional), #9 (Directional)."*

**Inverse read (the data-quality honesty gate).** Report how many interviews were Weak / Not-usable, what that does to the overall trust, and — given the chosen business task — **which task questions the current data cannot answer.** That list becomes "what to interview next."

---

## STAGE 6 — Assemble the report

Build the single file in this order (top attribution → disclaimers once → the sections below). Compute the **"What your calls are telling you"** Layer-1 block and the data-quality summary **last**, from the finished work — the Layer-1 block is the one-screen verdict (can the data answer the task · the top 2–3 segments with an anchor quote each · the single biggest data risk); §1 is its fuller breakdown.

**Scale the confidence you claim to the input you actually got — compute this, never reuse boilerplate.** Count the usable interviews (Clean + Directional) and the support weight per segment:

- **Thin input** — fewer than ~5 usable interviews overall, or a segment standing on less than ~2 support weight, or files that are notes and sales pitches rather than Job interviews. Then: put a warning line at the very top of the report — *"Thin input: {N} usable interviews out of {total}. Everything below is a hypothesis; numbers are ranges, not points."* — write every number as a range (*"2–4 of the 7"*, *"somewhere between a week and a month"*), label every segment *Hypothesis*, and list the **top 3 things that would raise accuracy most** (e.g. *"5 more interviews with people who paid in the last 90 days," "your churn export," "the Q2 sales-call recordings"*) in §9.
- **Enough input** — usable interviews behind every segment, and saturation reached at least in the top segment. Point figures are allowed then, each with its count and interview numbers.

This is computed from the files at hand and sits *on top of* the fixed disclaimers, which never change.

### Report structure

```markdown
{Thin-input warning line — only when the input is thin, per the rule above.}

## What your calls are telling you (read this first)
- **Can these interviews answer "{business task}"?** {Yes / partly / not yet} — {one line on why}.
- **The segments that showed up:** {top 2–3, most-supported first} — each one line, with how many interviews back it + one anchor quote.
  - {Segment name} ({Solid / Emerging / Hypothesis} — {n} of {N}: #{a}, #{b}, #{c}): {one line}. *"{anchor quote}"* — #{a}.
- **The single biggest data risk:** {e.g., "11 of 18 are hypothetical-heavy; segment sizes below are directional at best"}.

## 1. Data-quality summary
- Files analyzed: {N}. Type mix: {AJTBD x / partial y / non-AJTBD z}. Quality: {clean a / directional b / weak c / not-usable d}.
- **Can these interviews serve "{business task}"?** {Yes / partly / not yet} — {one line on the binding gap}.
- The single biggest data risk: {e.g., "11 of 18 are hypothetical-heavy; segment sizes below are directional at best"}.
- **How far to trust the numbers below:** {point figures / ranges only} — {the count that decided it}.
- {Any defaults assumed because interactive input wasn't available.}

## 2. Segments by Core Jobs
{Comparison table: Segment · Core Jobs (short) · dominant ranked criteria · confidence · interviews supporting ({n} of {N}, with the #s). Ordered by confidence.}

### {Segment name — tied to the Jobs and real criteria} — {Solid / Emerging / Hypothesis}
> **Confidence:** {level} — stands on {n} of {N} interviews: {#s with their per-interview confidence}.
**Persona (the causal criteria):** {one paragraph, then 3–5 causal-criterion bullets, each with the cause it drives and its count — "{criterion} — {n} of {N}: #…"}.
**Core Jobs:**
1. **When** {context + trigger + negative emotions}, **I want to** {expected outcome}, **with success criteria** {concrete, ranked}, **in order to** {Big Job + positive emotions}. — {n} of {N}: #{…}
**Big Jobs (motivation above the Core Jobs):** {…}
**Anchor quotes:** {1–3 verbatim, with the interview #}.
**Why this is one segment and not several:** {one line from the anti-pattern checklist — e.g. "three industries in here, same Core Job and same ranked criteria, so one segment, not three"}.

## 3. What they use today and where it falls short
{For each tool the segment hired: the tool · the set of tasks choosing it does for them (its core + micro tasks) · where it underperforms, each problem traced to the task it botched (task → tool → problem), each line with its count ({n} of {N}: #s). DIY counts as a tool. (Structurally: each tool is a Solution = label + the sub-graph it installs.)}

## 4. What they weighed before choosing
{The options they knew · how those compare · the named products plus a way in · their fears (their consideration set), each with its count. What they weigh before choosing, and what they'd need to learn or believe to switch.}

## 5. Value-creation hypotheses
{Underserved success-criteria intersections + a one-line mechanic direction per segment — no feature list. Each one names the counted criteria gap it answers. "What to build to deliver this is $nmt-craft-value-proposition's job."}

## 6. Single signals — verify before acting
{Everything said by exactly one person: the claim · who said it (#) · the verbatim quote · what would confirm it. A single vivid quote lives here, never inside a segment description.}

## 7. Hypotheses to validate (mine, not your interviews')
{Ideas the model added that appear in none of your files — each marked as the model's own, with the cheapest check that would confirm or kill it. Nothing here may be repeated elsewhere in the report as a finding.}

## 8. Source → segment map + per-interview appendix
{One row per source file, every file present exactly once — this is what makes counts like "16 deals in this segment" re-checkable:}

| # | File / deal | Type & quality | Assigned segment (or "unassigned — why") | Anchor quote | Serves the task? |
|---|---|---|---|---|---|

{Any count anywhere in the report must be reproducible by filtering this table. If it isn't, the count is wrong — fix it before shipping. Then, per file: Core Jobs found (+ per-Job confidence) · what's present · what's missing · the one decisive quality reason. In HTML, a <details> block.}

## 9. Gaps + what to interview next
{What the data can't answer for the chosen task; the top 3 inputs that would raise accuracy most; whom to re-recruit (past-payment screener); which segments need more interviews to move from Hypothesis → Emerging → Solid. Suggest preparing the next round of interviews with $nmt-chat.}
```

**Hand-off (`PRODUCER-CONTRACT.md §4c`).** End with the next step: a **Solid** segment + its value hypothesis → `$nmt-craft-value-proposition`; a live product to grow/fix → `$nmt-diagnose`; only **Hypothesis** segments → more fieldwork; prepare it with `$nmt-chat`.

---

## Quick mode (default) — step ledger
1. Hold the user's inputs in context (the business task, the file list, any prior segment hypotheses).
2. Read the eager core (`ajtbd-key-theses.md` + `segmentation.md`).
3. Fan out the distillers in waves (STAGE 3); collect returns; checkpoint each finished wave into the draft result file. Pull each staged canon file the first time a section needs it.
4. Build per-interview feedback (STAGE 4).
5. Cluster into segments + compute confidence (STAGE 5).
6. Run the self-critic criteria; fix in place.
7. Assemble the one report (STAGE 6); compute the data-quality summary last.
8. Chat output (below).

A skipped stage is never silent — say which and why.

## Deep mode (opt-in)
Everything Quick does, plus a web wave **after** synthesis: subagents take the named Solutions / Consideration Set surfaced from the interviews and (a) confirm the real competitors and their positioning, (b) mine real review language around the Core Jobs to corroborate or challenge the extracted criteria, (c) flag Jobs the interviews missed that the market clearly shows. Web caps + the evidence floor + the self-critic loop + the web-MCP fallback all per `PRODUCER-CONTRACT.md §6`. Source links mandatory (Rule 2). Never let web data overwrite the interview evidence — it annotates, the interviews lead. **Web findings carry their own status and their own count** (how many reviews said it, with the linked source) and are counted separately from the interviews — they never get folded into a segment's interview count.

## Self-critic criteria (before the report ships)
1. **Segments = similar Core Jobs + similar ranked success criteria** — not demographics, not Big Job, not industry; a split priority order was split, not averaged.
2. **Every Core Job carries a confidence traceable to specific interviews**; no segment is presented as Solid on a single Directional interview.
3. **Fake Jobs were not promoted to findings** — future-only respondents contributed Big-Job hypotheses, named Solutions, and orphan Problems only, all labeled as such.
4. **Criteria are concrete** (direction + level), not adjectives; abstract ones are flagged as "re-elicit," not recorded as criteria.
5. **Personas are causal criteria**, demographics second-order; each surviving criterion is a cause, not a restated value.
6. **Problems sit on a Job → Solution → Problem chain**; Solutions structured as label + sub-graph; DIY counted.
7. **Job grammar holds** — `When … I want to {outcome} with success criteria … in order to …`; one verb per Job; levels named and product-relative.
8. **The data-quality honesty gate fired** — weak/unusable counts reported, and the task questions the data can't answer are named with a re-interview plan.
9. **Plain-language-led**; methodology terms only in parentheses; quotes verbatim; every term explained on first use (in HTML, as a tooltip) so a reader with zero methodology knowledge can follow every line.
10. **One file** (Rule 4); disclaimers once at top (Rule 3); attribution top + bottom (Rule 23).
11. **Every segment-level claim carries "{n} of {N}" plus the interview numbers**, and no single-source claim sits inside a segment conclusion — those are all in §6 Single signals.
12. **Every claim shows what kind of claim it is** — backed (quote cited) / derived (from what) / the model's hypothesis (§7 only). Numbers a respondent estimated are attributed as their estimate, never printed as a market fact.
13. **The segmentation anti-pattern checklist ran** — no channel-as-segment, no industry split where the Core Jobs and ranked criteria are the same, and every non-Job cut carries its causal sentence.
14. **The source → segment map covers every file exactly once**, and every count in the report can be reproduced by filtering it.
15. **Claimed confidence matches the input volume** — thin input carries the top-of-report warning, ranges instead of point numbers, and the top-3 accuracy-raising inputs in §9.
16. **Any default assumed for missing interactive input was announced up front** and is repeated in §1.

## End-of-run chat output
1. **Brief outcome** — 3–5 lines: how many usable interviews, the segments found and their confidence (each with its {n} of {N}), whether the data can serve the chosen task, and — if the input was thin — that line first.
2. **The data-quality summary + the segment table**, printed inline.
3. **Next step** — the hand-off recommendation (which skill, for which segment).
4. **Path** — the single result file.

## What this skill does NOT do
- It does not run the interviews or recruit respondents — that's the user's fieldwork; `$nmt-chat` can help design it.
- It does not invent segments from the market — that's `$nmt-market-research`. It only reconstructs what the interviews support, and says where they don't.
- It does not size the market quantitatively or build a unit-economics model — separate skills.
- It does not turn a value hypothesis into features or a PRD — that's `$nmt-craft-value-proposition` → `$nmt-product-requirements`.
- It never fabricates a Job, a quote, or a confidence — thin data is reported as thin.

---

> **Update check — after the result is delivered (optional; policy in NextMoveTheory-README.md, section "Updates & telemetry").** For a multi-turn chat, after your first substantive answer.
> Skip this entirely if `.nmt-config` (project root) contains a line `update-check: off`, or the environment variable `DO_NOT_TRACK` or `NMT_NO_UPDATE_CHECK` is set.
> Otherwise, the first time this runs in the conversation, tell the user in one line: "Checking for NMT skill updates — only this skill's name and the installed version are sent (details: NextMoveTheory-README.md; disable: add `update-check: off` to `.nmt-config`)."
> Then run `v="$(grep -m1 -E '^[0-9]' .nmt-version 2>/dev/null)"; curl -fsSL --max-time 2 "https://nextmovetheory.com/version?skill=nmt-analyze-interviews${v:+&v=$v}"` — on any error or timeout, skip and move on; never retry, never block.
> If the feed's `latest` is newer than the installed version, add one line: the `<installed> → <latest>` gap, a one-line summary per newer entry, and "run $nmt-update to update (the update itself downloads from GitHub)". If versions match or `.nmt-version` is absent, add nothing.
