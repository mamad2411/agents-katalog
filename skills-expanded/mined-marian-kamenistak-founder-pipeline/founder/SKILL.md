---
name: founder
description: "Use when the owner wants to design, validate or launch a new revenue stream, service, product, SKU, community tier or partnership package, monetize a side project, or decide \"should I build X?\", even if they never say \"revenue stream\" or \"founder\". Load it first for any message about a stream already in the pipeline (\"founder pipeline\", a step ID such as P1.S4, `PROGRESS.md`), including a request to estimate, skip or fill in a value, because its rules decide what may be estimated. Runs a gated 25-step pipeline in 6 phases (ideation, viability, clients, build, activation, adoption): every step needs evidence, a critic pass and the owner's sign-off, and three gates can kill the idea. Has a 48-hour smoke test (`smoke`) and an unattended mode (`overnight`). Runs standalone; other skills and tools are optional upgrades."
---

# Founder — design a new revenue stream end to end

Design a new revenue stream the way the best operators do it: problem first, evidence over wishful thinking, demand data before design lock-in, pricing tied to willingness-to-pay, and execution gated by validation. 25 steps in 6 phases, one step at a time, one `.md` file per step in a stream folder.

The skill refuses to name a service before the problem is known, to lock a niche before the demand data is on the table, to set a price without willingness-to-pay evidence, and to greenlight execution without LOIs, pre-sales or paid pilots. Those refusals are the product: they separate streams that ship from streams that die in a document nobody reopens.

All paths in this skill are relative to its own folder: `${CLAUDE_SKILL_DIR}`.

## How to run it

**One stage file at a time.** Each step's full instructions live in `stages/`. At each step:

1. Read ONLY the current stage file (e.g. `stages/P1-Ideation.S2-Problem.md`). Never load several stage files at once.
2. Run the step as the file says: the grill pass, the questions, the output file.
3. Run the per-step validation loop (below). No step is complete without it.
4. Update `brief.md` (business state) and `PROGRESS.md` (pipeline state).
5. Move to the file named under **Next:** at the bottom of the stage file.

**Each stage file opens with a `Routing:` line**: the execution mode, the model tier per role, and the gate critic's tier. That line is all a step needs. `references/engine-routing.md` holds the full map and is read only when designing a fan-out the line does not cover.

| Mode on the Routing line | What runs |
|---|---|
| `plain` | the main loop, single-threaded |
| `fan-out` | one `founder-pipeline:evidence-scout` per item (CHEAP), then `founder-pipeline:claim-refuter` on every load-bearing claim (PEAK), then `founder-pipeline:completeness-critic` (PEAK). Above about six items, offer the owner the `/founder-pipeline:gather-verify` workflow, which runs the same shape in the background and resumes after a crash |
| `judge panel` | independent `founder-pipeline:gate-critic` agents, one per lens or framing, blind to each other; or the `/founder-pipeline:judge-panel` workflow |
| `delegated` | one subagent runs a whole sub-pipeline on its own context and returns only its conclusion |

The agents and workflows ship with the full plugin. In a founder-only install, run the same roles as generic subagents from the cards in `references/capabilities.md`. A workflow spends many agents at once, so start one only when the owner says yes.

**Serial gates, parallel work.** The step sequence is serial and human-gated. Inside it, research fan-out is always fine, the pairs marked ∥ in the table may be drafted together (each still gates on its own), and the web build (P4.S3) may run as one background subagent. Never parallelise across a kill gate or on top of an unapproved artifact. The no-dependency reasoning per pair is in `references/pipeline-contract.md`.

## The 6 phases

25 steps: 7 + 4 + 1 + 6 + 4 + 3. Step IDs are `P<X>-<PhaseName>.S<Y>-<StepName>`, short form `P1.S5`. Stage files, templates and output files all carry the same ID.

| Phase | Steps | What it settles |
|---|---|---|
| **P1-Ideation** (7) | `S1-Init`, `S2-Problem`, `S3-ICP`, `S4-Prediction`, `S5-Competition`, `S6-Offer`, `S7-Name` | The problem, who has it, measured demand (S4 runs `/prediction` before the niche is locked), the landscape, the offer. S1 carries the portfolio-trade kill gate. The name comes last. |
| **P2-Viability** (4) | `S1-Economics` ∥ `S2-Tooling`, `S3-Pricing`, `S4-Validation` | Hours and money in one model, `/pricing` at ≥95/100 with price floors, then the `PROFIT VERDICT` kill gate. |
| **P3-Clients** (1) | `S1-Outreach` | Named accounts and first touches, straight after the verdict. Nothing in P4 may delay it. |
| **P4-Build** (6) | `S0-Email`, `S1-Keywords`, `S2-Copy`, `S3-Web`, `S4-SourceGap`, `S5-Deck` | The compounders: mail on the domain, keyword contract and locale decision, copy, the site on the declared house stack, competitor HTML teardown, deck. Steps skip cleanly when the stream has no web asset or no client-send motion. |
| **P5-Activation** (4) | `S1-Launch` ∥ `S2-Links`, `S3-Queues` ∥ `S4-PredictionCadence` | Launch is execution: first posts, listings, links, the three queues, the prediction cadence. |
| **P6-Adoption** (3) | `S1-GTM` ∥ `S2-KPIs`, `S3-Execute` | Channels locked from real outreach and activation data, one north-star metric, the 90-day plan. |

`stages/smoke_test.md` is a 48-hour go/no-go (5 questions, 10 real outreaches) that runs before the pipeline and is not one of the 25 steps. Recommend it for any "should I even build X?" hunch.

Read `references/pipeline-contract.md` when you create or resume a stream folder, when a step needs to know which step owns an artifact, or before drafting two steps in parallel. It holds the full phase notes, the one numbering exception (`P4-Build.S0-Email`), the file-naming and step-folder rules, and the artifact-ownership list.

## What it produces

One folder per stream at `<parent>/<slug>/`. The parent is whatever directory the owner names at P1.S1; never assume a default. Each step writes exactly one file named after its step ID (`P1-Ideation.S6-Offer.md`), copied from `templates/stream-folder/` when the step starts. Filenames never carry status.

**`PROGRESS.md` is the single source of truth for pipeline state**; `brief.md` holds the business state. Never merge them. One row per step: `Step | Name | Status | Updated | CRITICAL | Def-of-success | Note`. Statuses: `pending` → `in progress` → `awaiting approval` → `approved`, plus `skipped` (with the why) and `killed` (kill gates only). A step file existing means nothing; only an `approved` row means approved. Update the row at every transition, so a crash never loses state. With the full plugin installed, a hook turns any edit that adds an `approved` row into a permission prompt, so the row cannot land without the owner's click.

**Every recurring artifact has one owning step.** Later steps cite the owner's file; they never re-ask or re-produce it. If the owner's artifact turns out inadequate, that is a loop-back, not a rewrite elsewhere.

## Hard rules (every step)

**Declare once at P1.S1, reference everywhere after:** the house stack (web framework and host, analytics, forms and transactional mail, CRM, automation runner), the currency (written `<CUR>` throughout), and the home market plus primary export market. Later steps build on the declared stack and never re-litigate it.

**Runs standalone.** This skill needs nothing but Claude Code. Every `/name` it calls and every tool it uses is an upgrade, resolved bundled → the owner's own → the inline fallback card in `references/capabilities.md`. P1.S1 opens with a capability preflight that writes `<stream>/CAPABILITIES.md`; later steps read that file instead of re-probing. A missing capability changes how a step works, never whether its gate runs. A missing data source marks the criterion `BLOCKED`; it is never filled with an estimate.

**Honesty rules for every number.** A fabricated figure survives into the viability gate, the price and the 90-day plan.
1. Every number comes from a call or a named source. Never estimate, never round a figure you did not receive, never reconstruct one from memory. Derived figures state what they were derived from.
2. An unavailable metric prints "not available" and says why. Not blank, not zero, not a plausible placeholder: blank reads as "nothing here" and zero reads as a measurement.
3. Low confidence is labelled, with the specific missing input that would raise it.
4. No padding, and name what you did not cover. A silent top-25 sample of 400 rows reads as complete; state the cap and the total.
5. Tag every revenue figure, conversion rate, market size and growth assumption inline: `[source: <citation>]` or `[assumption — validation: <how we'll test>]`. If you cannot say where a number came from or how you would test it, do not write it.

**Per-step validation loop (no exceptions, no auto-advance).**
1. Copy the step's template to its canonical filename, flip the `PROGRESS.md` row to `in progress`, and draft.
2. Send the draft to a fresh-context critic: the `founder-pipeline:gate-critic` agent with the step file path and the stage file's def-of-success list pasted in, or `/critical` resolved through `references/capabilities.md`. Each stage file names what to attack hardest.
3. **The verdict is computed, not felt.** The critic judges every def-of-success criterion PASS or FAIL with one line of evidence and lists blocking findings. The step passes only when every criterion is PASS and nothing blocking is open. The numeric `CRITICAL SCORE` is advisory: self-scores drift between runs, binary criteria carry the gate. The kill steps use framed critics: P1.S1 runs one focus-refutation pass, and P2.S4 runs a profit-refutation and a focus-refutation pass independently, and each must pass.
4. **A failed gate means an improvement loop, not an advance.** Revise with every relevant tool: the stage's specialist skills, research fan-out, `/brand-voice`, a new critic pass. Token spend is not a reason to stop, because a weak step compounds through every step after it. After 3 loops with no movement the missing ingredient is real-world evidence, not better prose: name exactly what is missing and go get it. Never soften the critic to fish for a pass.
5. When the gate passes, flip the row to `awaiting approval` and present the draft, the critic's findings, the score and the criteria checklist. **Wait for the owner's explicit approval.** The owner may override a failed criterion; record the override in the file.
6. On approval, flip the row to `approved` with the date, the score, the def-of-success result and a one-line "so what" note.

**Context budget.** The main conversation holds only the current stage file, `brief.md` and at most ONE prior artifact the step needs. Anything that would pull more than about 15 KB of prior work into the main context goes to a subagent that reads on its own context and returns only its conclusion, never raw dumps.

**Model floor.** The main loop, both kill passes, every refuter and completeness critic, and every customer-facing word (`/brand-voice`, translations, blog drafts) run on the owner's top-tier model. Gathering fan-outs run on the small model, with the output schema, the evidence rules and the judging criteria pasted into the prompt. Analysis and verification run at high effort. Name tiers, never model codenames; the dated mapping is in `INSTALL.md`.

**Profit floor.** Captured at P1.S1, enforced at P2.S1 and P2.S4: the owner's hurdle rate (profit per founder-hour of their best current stream) and an absolute floor (the minimum 12-month profit that justifies the focus). A new stream must project **≥ 1.5× the hurdle rate per founder-hour at the 50% scenario** and clear the absolute floor, or it dies at P2.S4. The same bar goes into P1.S4 as the prediction run's pre-registered money floor. "Profitable but mediocre" is a KILL, not a maybe.

**Focus guard.** One stream in design or build at a time. P1.S1 scans the candidate parents for a stream with unfinished rows and, if it finds one, stops and forces a decision: finish it, park it with a dated re-entry note, or kill it. Every plan names the people and tools that carry what the owner cannot; a plan where everything lands on the founder's calendar fails at P2.S1.

**Two zones.** In the documents zone (P1.S1 to P2.S4), resolve every contradiction by asking the owner before drafting on top of it, and never demand 95% market confidence from documents; that comes from the evidence gates. In the build zone (P4.S2 to P4.S5, decks, apps), nothing is built below 95% confidence in what to build, backed by named artifacts: approved copy sources, a locked keyword contract. A confidence number with no artifact behind it is 0%.

**Loop back, don't patch forward.** When a later step contradicts an earlier one: name the target step and the contradiction with its evidence, get the owner's approval to rewind, re-open the step (row back to `in progress`, a Rewind log entry in `PROGRESS.md`) and re-run its full validation loop, then re-validate every later approved step that cites the changed file and record the cascade result.

**Would I bet money?** Every output names real names, real numbers and measurable outcomes. Reject a generic output and re-run the step.

**Questions.** One step at a time, at most 6 questions asked per step, one at a time, each with a recommended answer. In P1-Ideation the questions follow the grill pass in `references/grilling.md`: look facts up instead of asking, ask only for decisions, and never put two dependent questions in the same round. End every step with an active commitment question, never a passive "continue?".

**Owner actions go to the queue.** The moment a step produces an action only the owner or a named delegate can perform, write a row into `<stream>/queues/manual-queue.md`. "Drafted, awaiting the owner" is an open row, not a done state. Every checkpoint restates the open rows: count, oldest age, the single highest-value next. Row fields and the optional task-board mirror are in `references/owner-action-queue.md`; read it the first time a step writes a row.

**Skip honestly.** Each stage file says when the step earns its keep and when it becomes performative. Skip a step that does not apply, record the why in `brief.md`, mark the row `skipped`, and get the owner's sign-off on the skip.

## What it refuses

- Advancing without the owner's sign-off, or on a failed criterion.
- Naming before the problem, or locking a niche before the P1.S4 demand data.
- A price from "psychological mechanisms" instead of value and willingness-to-pay.
- Execution with no LOI, pre-sale or pilot.
- SEO or content as the plan for client number one. They compound over 6 to 24 months.
- Mediocre profit kept "small on the side", and a second stream opened before the first is finished, parked or killed.
- A polished brief with no cited evidence behind it.
- A funnel that never kills. If the early gates kill under roughly 20 to 30% of ideas, the gates are ritual. A killed stream is a win.

The full list, with the reason behind each refusal, is in `references/anti-patterns.md`. Read it when a request looks like a shortcut around a gate.

## Modes

**Resume.** If the stream folder already exists, `PROGRESS.md` says where things stand: the first row, top to bottom, at `in progress` or `awaiting approval` is the current step, otherwise the last `approved` row is the last one done. After an unattended run many rows sit at `awaiting approval`; the owner reviews them in order, and a rejected row re-opens that step and every step built on it. Ask: "Resume at the next step (or finish the current one), rewind to [step], or restart fresh?" Legacy streams without a `PROGRESS.md` are covered in `references/pipeline-contract.md`.

**Express** skips the "earns its keep / performative" intros and goes straight to the questions. It skips explanations, never evidence: the validation loop, the P1.S4 prediction gate, the `/pricing` ≥95/100 gate, the P2.S3 price floor, the profit verdict and the portfolio trade all apply in full. If express is requested to get around a gate, name that and refuse.

**Overnight** (unattended): read `references/overnight.md` only when the invocation carries the `overnight` flag. A fresh-context critic stands in for the sign-off, every step stays at `awaiting approval`, nothing is sent to a person, and the site goes to a preview URL unless the owner asked for production in the kickoff.

## References

Read each one when its condition applies, never all at once.

| File | Read when |
|---|---|
| `stages/*.md` | one per step; the only stage content loaded during a run |
| `templates/stream-folder/` | a step starts and needs its output template |
| `references/capabilities.md` | the P1.S1 preflight; any `/name` or tool that needs resolving or is missing |
| `references/pipeline-contract.md` | creating or resuming a stream, checking who owns an artifact, drafting two steps in parallel |
| `references/grilling.md` | before the questions of any P1 step |
| `references/engine-routing.md` | designing a fan-out or panel the stage's `Routing:` line does not cover |
| `references/owner-action-queue.md` | writing the first queue row |
| `references/anti-patterns.md` | a request looks like a shortcut around a gate |
| `references/pitfalls.md` | a step stalls, or a gate fails twice for the same reason |
| `references/question-bank.md` | the stage file's questions did not get to the bottom of it |
| `references/frameworks.md` | a step applies Lean Canvas, the Value Proposition Canvas, Dunford positioning, Monetizing Innovation or the Raskin narrative |
| `references/signals-and-scoring.md` | P3.S1 and P6.S1: intent signals, BANT × commitment scoring, call debrief |
| `references/dataforseo-playbook.md` | P1.S5, P4.S1, P4.S3, P4.S4: search-data recipes |
| `references/web-post-launch.md` | P5.S1 and P5.S2: backlink and AI-citation surfaces |
| `references/overnight.md` | the `overnight` flag is set |
