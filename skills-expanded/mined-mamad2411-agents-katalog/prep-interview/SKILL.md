---
name: prep-interview
description: One-command interview prep package — question mapping, company context digest, and tactics/logistics — saved as a single output document
argument-hint: <company> [role] [context]
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Glob(output/**), Glob(coaching/**), Write(output/**), Write(data/job-todos.md), Bash(python3 tools/pipe_write.py:*), Task, mcp__exa__web_search_exa, mcp__exa__web_fetch_exa, WebSearch, WebFetch
---

# Prep Interview — One-Command Interview Prep Package

Generates a comprehensive interview prep document for a scheduled or upcoming interview. Uses 3 parallel agents to map questions to coached answers, condense the company context, and build a tactics + logistics section. Produces a single output file and creates a follow-up debrief to-do.

## Arguments

- `$ARGUMENTS`:
  - **`<company>`** (required) — company name; matched against pipeline and company research dossier
  - **`[role]`** (optional) — role title if there are multiple pipeline entries for the same company
  - **`[context]`** (optional) — interview type (`recruiter`, `hiring-manager`, `panel`), date, or specific focus (e.g., `"hiring manager round, 2026-03-05"`, `"focus on operations experience"`)

Examples:
- `/prep-interview "Beacon"` — full prep for Beacon
- `/prep-interview "Acme AI" "Strategy & Operations"` — specify role
- `/prep-interview "Northwind" "hiring manager, 2026-03-10"` — with date and type
- `/prep-interview "Beacon" "Chief of Staff" "panel interview, focus on leadership"` — full args

If no company provided, display usage:
```
Usage: /prep-interview <company> [role] [context]

Examples:
  /prep-interview "Beacon"
  /prep-interview "Acme AI" "Strategy & Operations"
  /prep-interview "Northwind" "hiring manager, 2026-03-10"
```

## Instructions

### Step 1: Parse Arguments and Look Up Pipeline

1. Parse `$ARGUMENTS` into company name, optional role, optional context string.
2. **Infer interview type** from context string:
   - Contains "recruiter" or "phone screen" or "screening" → `recruiter`
   - Contains "hiring manager" or "HM" → `hiring-manager`
   - Contains "panel" or "loop" → `panel`
   - Otherwise → `general` (default)
3. **Extract interview date** if present in context (look for YYYY-MM-DD or natural date like "March 10").
4. Read `data/job-pipeline.md`. Search for the company name (case-insensitive, fuzzy — company name as substring). If multiple roles for the same company, and a role was specified, match on that. If still ambiguous, use the most recently updated entry.
5. From the matching pipeline entry, note: **stage**, **role**, **CV Used** (output filename), **URL**, **notes**.
6. Generate a slug from the company name (lowercase, hyphens).

### Step 1b: Pre-Flight Gates (interview-prep-discipline.md)

Set these before loading context; they gate which sections the prep produces. Canon: `framework/interview-prep-discipline.md`.

1. **Comp pre-flight (E1/E2).** Is compensation on THIS call's agenda? Default **No** for `recruiter`, `hiring-manager`, `panel`, and `general` screens unless the context string says "comp", "offer", or "salary", or the pipeline stage is offer. If **No**: produce NO comp script, floor, walk-away, or structure probe; if comp surfaces live, the one-line deferral is "comp lives at offer stage for me; happy to use this time on the seat itself." If **Yes** (comp-agenda call or offer stage): Agent 2 includes a comp-structure question set (base/bonus/equity/vesting; for startups, percent ownership + 409A + cliff), and do not volunteer Nick's floor when their quote sits above it.
2. **Round-type branch.** If the context signals a detail/PEI-style round (deep behavioral drilling, "go deep on one story", McKinsey-style) set `pei-round = true` (drives Agent 1 PEI Deep-N and the Drill Plan in Step 4d). If the call is a discovery / first-call / recruiter screen set `discovery = true` (drives the "What I'm Testing About Me" block in Step 4e).
3. **Audience-fluency (C1).** If the interviewer's professional background is known (company-notes, pipeline, or research, e.g. ex-MBB/consulting), flag their fluency and pass it to Agent 2. MBB/consulting-fluent means the prep deploys structure AND updates it (never "drop the consulting voice"); operator/founder without that background keeps the "don't perform structure" guidance.

### Step 2: Load Context (parallel)

Read the following in parallel — skip any that don't exist:

1. Company dossier — `output/<slug>/<slug>.md`

   **Staleness check:** After reading, grep for `Last updated:` in the first 10 lines of the dossier. Parse the date. If the dossier is more than 30 days old (or if no `Last updated:` line is found), display this inline warning — then continue, never block:
   > ⚠️ Company dossier is [N] days old (last updated YYYY-MM-DD). Consider refreshing: `/research-company "[Company]"`
2. Company notes — `data/company-notes/<slug>.md` — personal notes, call context, recruiter observations
2b. Interviewer dossier — `data/people/<slug>.md` (if the interviewer is known; slug = interviewer name lowercased, accents folded, spaces→hyphens) — synthesized relationship context (what they care about, pressure points, prior touchpoints, what Nick owes them). Feeds the audience-fluency read (Step 1b C1) and the Agent 3 Live-Need Bridge block. Example: `data/people/jane-doe.md`.
3. `data/profile.md`
4. `data/professional-identity.md`
5. **`coaching/coached-answers/`** — the directory, ALL of it. Glob `coaching/coached-answers/*.md` and read every match, plus `_backlog.md` to see what is NOT coached yet. These are the validated SPOKEN answers and they outrank `data/projects/*.md` for anything said out loud: they carry the reconciled numbers, the framing that survived a live rep, and a delivery note naming what already went wrong. **Read them BEFORE writing any proof into the doc, and carry a matched answer's delivery note into the prep verbatim.** The legacy single file `coaching/coached-answers.md` was merged into this directory on 2026-09-21 and no longer exists. Origin: 2026-09-21, a prep shipped a proof framed from the project file while a validated coached version said the opposite, per `memory/feedback_coached_answers_has_two_surfaces.md`.
6. `coaching/anti-pattern-tracker.md`
7. `coaching/pressure-points.md`
8. `framework/answering-strategies/anti-patterns.md`
8b. `framework/answering-strategies/bridge-to-stated-need.md` — the live-need bridge strategy (hypothesis H4). REQUIRED: used to generate the "Live-Need Bridge" block in the Agent 3 cheat sheet (predicted live-need sentence + in-call governor).
8c. `framework/interview-prep-discipline.md` — REQUIRED. The 13-discipline canon (Family V + Family II). Its CHECK lines drive the Step 1b pre-flight gates, the agent enhancements below, and the inline Self-Doubt / Drill Plan / Discovery sections (Steps 4c-4e). Load before dispatching agents.
9. If CV Used field is populated in pipeline: read `output/<cv-filename>` to get the exact projects and language used

Also Glob `data/projects/*.md` to have project files available for question mapping.

### Step 3: Web Research if No Company Dossier

If no company dossier was found (neither subfolder nor flat format):
- Run 2 searches in parallel via Exa MCP (`mcp__exa__web_search_exa`) as primary; fall back to WebSearch only if Exa returns nothing. Per the 2026-05-19 A/B verdict, Exa decisively outperforms web on primary-source reach for company/interview research.
  1. "[Company] recent news developments 2026" — recent developments
  2. "[Company] [role] interview process Glassdoor first-person" — interview-specific info (this query type is exactly the Glassdoor/paywalled class WebFetch tends to 403 on)
- Use the results to construct a minimal company context.
- Note prominently in the output: "⚠️ No dossier found for [Company] — prep is based on quick Exa search. For deeper prep, run `/research-company "[Company]"` first."

### Step 3b: Cross-Skill Consistency Check

Before launching agents, verify consistency between the data sources loaded in Steps 2-3. Check for and flag any contradictions:

1. **CV vs. research dossier:** If both a CV (from pipeline's "CV Used" field) and a company research dossier exist, verify:
   - The company description/framing in the CV aligns with the dossier's findings (e.g., CV doesn't describe the company as "Series A" if the dossier shows Series C)
   - The role framing in the CV matches what the dossier says the company is hiring for

2. **CV vs. coached answers:** If both exist, verify:
   - Experience claims are consistent (e.g., CV says "5 years React" but coached answer says "about 3 years with React")
   - Project descriptions don't contradict each other across the two files
   - The professional summary narrative aligns with coached pitch answers

3. **Coached answers vs. professional-identity.md:** If both exist, verify:
   - Strengths claimed in coached answers align with those in professional-identity.md
   - Career direction framing is consistent

If inconsistencies are found, include a **Consistency Warnings** section in the output file (after the At a Glance table) listing each discrepancy with:
- What conflicts (file A says X, file B says Y)
- Suggested resolution (which version to use in the interview, or flag for the user to decide)

Pass any found inconsistencies to Agent 1 (Question Mapping) so it can account for them in answer frameworks.

### Step 4: Launch 3 Parallel Agents

Use the Task tool to launch **3 parallel subagents** (`subagent_type: "general-purpose"`, `model: "sonnet"`, `max_turns: 10`).

Pass to each agent:
- The company name, role, interview type, and interview date (if known)
- The candidate's key background points (from professional-identity.md and profile.md)
- The CV used (if available)
- The coached answers text (if available)
- The anti-pattern tracker text (if available)
- The company context (from dossier or web search results)
- Their specific focus and output format instructions below

---

#### Agent 1: Question Mapping

**Focus:** Likely interview questions → coached answers. Identify coverage gaps.

**Instructions:**
```
You are preparing [Candidate Name] for a [interview type] interview at [Company] for the [Role] position.

Your job: Map the most likely interview questions to existing coached answers, and flag gaps.

Context provided:
- Role requirements: [from JD/pipeline notes]
- Interview type: [recruiter/hiring-manager/panel/general]
- Company: [Company] — [brief context from dossier/search]
- Coached answers available: [coached-answers content]
- Projects/experience: [from CV if available, otherwise project summaries]

Step 1: Generate 10–12 likely questions for this specific role and interview type.
For a recruiter screen: focus on background, motivation, logistics, fit.
For a hiring manager: focus on behavioral STAR questions, strategic thinking, specific experience.
For a panel: mix of above plus role-specific technical/functional questions.
Tailor to [Company]'s stage/industry/culture signals from the context.

Step 2: For each question, check EVERY file in coaching/coached-answers/ and the project experience for a good answer. The coached directory outranks the project files for anything spoken.
- If a strong coached answer exists: note the answer framework and key points to hit.
- If a partial match exists (related but not exact): note what to adapt.
- If no coached answer exists: flag as GAP.

Step 2b: For questions that draw on the candidate's personal experience or industry knowledge, ensure answer frameworks include HYPOTHESES about the company's challenges, not just observations of the problem space. "Observer thinking" (describing what you saw) is weaker than "operator thinking" (positing what the operational challenge actually is and what you'd investigate). This is especially important for S&O, operations, and strategy roles.

Step 2c (PEI Deep-N — B1): If this is a detail/PEI-style round, designate 2-3 "Deep-N" stories where the candidate OWNED the action with a QUANTIFIED, validated result. Pre-load each to four layers (Situation one line / granular first-person Action / quantified Result / Learning) and list 10+ second-order probes per story (decision rationale, others' reactions, the moment-level "what were you thinking", the trade-off, what you'd do differently). Demote any observed-not-owned or unquantified story to "frame/why-now", never a drill target (drilling it walks into an overclaim). Name THE single deepest story explicitly. Discipline line: "layer 3 of one, not layer 1 of three." Note the mid-2025 dimension relabel (Connection, Drive, Leadership, Growth); tag each Deep-N story to a dimension.

Step 2d (tag by job — F1): Tag every prep item carry/anchor (proves listening), screen (maps to goals.md, decides if Nick wants the seat), or answer (defends candidacy). Preserve any goals.md screen item even under compression.

Step 3: List the top 5 GAPS — questions where no good coached answer exists. These need new prep.

Output format:

## Likely Questions → Coached Answers

### Q1. [Question]
**Type:** [behavioral/motivational/situational/logistics]
**Answer framework:**
- [Key point 1 — cite specific project if relevant]
- [Key point 2]
- [Key point 3]
**Coached answer reference:** [file in coaching/coached-answers/ and its section, or "CONSTRUCT FROM: [project]"]
**Anti-patterns to avoid:** [1-2 relevant warnings]

### Q2. [Question]
...

## Answer Gaps (prep these before the interview)
| Question | Why it's a gap | Suggested approach |
|----------|---------------|-------------------|
| [Question] | No coached answer, no direct project | Use [gap-reframing strategy] |

## PEI Deep-N Designation (if pei-round)
[2-3 owned + quantified stories, each with 4 layers + 10+ probes; mark THE deepest and its dimension. List demoted (observed/unquantified) stories separately as frame-only.]

## Item Tags
[Each question/story tagged carry / screen / answer.]
```

---

#### Agent 2: Company Context Digest

**Focus:** Condense company research to what matters for THIS specific interview.

**Instructions:**
```
You are preparing [Candidate Name] for a [interview type] interview at [Company] for the [Role].

Your job: distill the company dossier (or web research) into only what matters for this interview.

Company context provided: [dossier or web search summary]
Interview type: [recruiter/hiring-manager/panel/general]
Candidate background: [brief summary from professional-identity.md]

Produce a tight, interview-ready company brief. NO fluff. Be specific and actionable.

Evidence weighting (F5 + F4): Weight evidence by source type. PR/keynote/brand content shows what they VALUE (frame as "they value X", never "they do X"); a call transcript or org-chart/calendar shows what they DO now, and the transcript overrides PR for the current job. Real values show in who a company hires, fires, promotes, and celebrates, not in perks or mission statements. For any intermediary intel (recruiter/referrer), weight by skin in the game: discount pure-commission recruiter pitch ~50%; treat an outgoing operator, advisor-equity holder, or long-relationship source as candid (downsides included).

## Company Context Digest

### Mission in 2 Sentences
[What [Company] does and why it matters — in plain language]

### Key Business Challenge Right Now
[The most important problem or opportunity the company is facing — what this team/role is hired to solve]

### Recent News to Reference
[1-3 specific, recent developments the candidate can mention to show they've done their homework. Include "I noticed that..." conversation starters.]

### What This Interviewer Probably Cares About
[2-3 things the hiring manager or recruiter at [Company] at this stage likely cares about most — based on role, stage, interview type, and company context]

### Cultural Signals
[2-3 specific cultural cues from the research — how the company talks about itself, what they value, any phrases or themes to mirror]

### Interviewer Fluency Read (C1)
[If the interviewer's background is known: MBB/consulting-fluent or operator/founder? If fluent, the prep deploys structure AND updates it (answer-first, MECE, then revise when data breaks it), do NOT drop structure. If not, keep "don't perform structure." State which applies.]

### Things to Avoid Mentioning
[Any sensitive topics, competitors to avoid comparing, assumptions to steer clear of]
```

---

#### Agent 3: Tactics & Logistics

**Focus:** Pre-call checklist, opening/closing strategy, questions to ask, logistics.

**Instructions:**
```
You are preparing [Candidate Name] for a [interview type] interview at [Company] for the [Role].

Your job: tactical preparation — how to handle the call, not just what to say.

Anti-patterns available: [anti-patterns.md content]
Anti-pattern tracker: [anti-pattern-tracker.md content — personal persistent patterns]
Company stage and interview type: [Company], [interview type], [stage from pipeline]

## Pre-Call Checklist (60-second scan before the call)

**Item 1 is fixed and MANDATORY — emit it verbatim as the first line of every generated checklist, above any tailored items:**

- [ ] **T-MINUS-2 SCAN, then the reps, then dial. Nothing substantive in between.** Re-read exactly three things in this doc: **THE ONE THING**, the **predicted live-need sentence**, and the **questions list**. Then run **two** aloud reps: the filler reset, and the **embedded-need rehearsal** sentence. Then dial. (~2 min total.)

[Then top 6-9 tailored checklist items — pulled from anti-patterns.md + personal anti-pattern tracker, specific to this interview type and company]
- [ ] [Item]
- [ ] [Item]

## Live-Need Bridge (REQUIRED — strategy: framework/answering-strategies/bridge-to-stated-need.md / hypothesis H4)

This is the highest-EV move and the #1 recurring miss. Produce all four:

**Predicted live-need sentence(s):** [1-2 sentences predicting how THIS interviewer will state what they need — a constraint they're under, a problem they're living, OR how they'll describe the role / what excites them. Ground in dossier + company-notes + interview type. e.g. founder: "we need X shipped before <event>"; hiring manager: "this person has to own <gap> from day one".]

**My match (specific, quantified):** [the 1-2 owned, quantified proofs from profile/projects that map onto the predicted need — NOT a value restatement. e.g. "call-center pilot: built the listening framework, drove $10M rollout".]

**In-call governor (read this line in the call):** *"Every time it comes back to me, FIRST name what they just said they needed. Then answer. One specific bridge sentence + 'that's why I want this' → then stop. No default story. No generic affirm."*

**Why the governor is unconditional, not triggered (do not 'improve' this back into a cue).** Sorted by how the need was delivered, the H4 log splits 7-for-7 on needs asked DIRECTLY at Nick and **0-for-10 on needs embedded in the interviewer's own narration** (as of 2026-08-26). The old wording — "when they *name* the live need" — only fires on the direct shape, because an embedded need is never named. Two cue-shaped mitigations have been tested and failed (proof-binding 8/05 half-failed; trigger-detector 8/11 never built), and the sibling three-gesture close failed the same way on 2026-09-04 with the cue fired exactly as prescribed. What works in this corpus is the filler reset: an unconditional rehearsed action, never a live detection. This governor fires on EVERY handoff so there is nothing to notice. Full reasoning: `framework/answering-strategies/bridge-to-stated-need.md`, "The delivery-shape split".

**Embedded-need rehearsal (aloud, once, in the T-minus-2 block):** [one sentence Nick says out loud before dialing, in the shape he would use if the need arrived buried in the interviewer's narration rather than as a question — e.g. *"So what you're describing is <their need in their words> — that's exactly what <one owned proof> was."* Modeled on the filler reset, which is the only mitigation in this corpus with a winning record: rehearse the shape cold so it is warm, rather than trusting live detection.]

## Frame-Import Guard (B2)
The bridge and any story draft use ONLY details Nick explicitly provided: his verbatim numbers, sequence, and words. Do NOT import settings, durations, or actions from the interviewer's vocabulary because they would "land well." The mirror to the interviewer happens at the observation level (a closing "sounds like the same shape as how you built it at X"), never inside Nick's own story. Test each line: could Nick say this cold, without the prep doc? If no, cut it.

## Opener & Bridge Authorship (B2b — components, never a finished line)

**Never write a finished opener or seam sentence into the prep doc and mark it as "the line to land."** Nick does not recite well; a line he did not generate reads as someone else's framing and he will either reject it live or deliver it flat. He thinks by reacting.

**What the doc supplies instead:** the raw components — his current role, what the work *actually* was (per the role-title rules in CLAUDE.md Hard Rules), and the seam to the target role. Frame it as a question: *"the bridge is X + Y — what does that sound like in your words?"* Then refine from his language.

Two refinements, both learned the hard way:

1. **Lead with a concrete ownable fact, not an abstraction.** "Operator at the intersection of strategy and implementation" is the tracked generic-self-description anti-pattern — Nick's own verdict was "too not very unique." A concrete opener leads with a number or a named thing he actually did, then bridges. "Intersection of X and Y" buries the one differentiator only he can claim.
2. **When he is BLOCKED generating** ("I don't know how to do a concrete first sentence"), give **2-3 concrete, disposable options to react to** — never one line to memorize. Plural options unblock without anchoring; he assembled a strong opener immediately after seeing three. The unlock is optionality plus a model of the shape, not a script.

This is B2 (above) applied to authorship rather than content: B2 bans importing the *interviewer's* framing into Nick's story; this bans importing *Claude's*. Same test — could he say this cold, without the doc? Origin: 2026-06-16 and 2026-06-22 drills. See `memory/feedback_interview_opener_components_not_finished_line.md`.

## Polished-Arc Guard (B3)
Add this pre-call checklist item: "Count my clarifying questions before my first action verb; zero means the polished-arc reversion fired." The tell is a smooth problem-to-goal-to-action answer in under two minutes with no clarifying questions (it looks collaborative, so the "did a framework fire" check misses it). In case/behavioral drills, require 3+ self-generated clarifying questions before proposing any action.

## Bare Definitions Rehearsal (B4 — MANDATORY whenever Nick brings his own framework)

**Fires when** the round involves Nick presenting or defending a frame he authored: a take-home deck, a presentation defense, a case where he proposes criteria, a scorecard, a recommendation ranked along named dimensions. Skip only for pure behavioral rounds where Nick names no framework of his own.

**Produce a two-column table in the prep doc — every named term in Nick's frame, and its operational definition in UNDER EIGHT WORDS:**

| Term in my frame | What it IS, in <8 words |
|---|---|
| [criterion / metric / rung / threshold] | [the noun, not the reasoning] |

**Rules:**
- **If a term needs more than eight words, it is not a criterion yet.** It is a mood, and the interviewer will spend the block discovering that.
- Each definition must name **what is measured**, not why it matters. "Contained conversations plus CSAT" is a definition. "The outcome of those actions" is a rationale wearing a definition's clothes.
- Rehearse them **aloud, as bare definitions** — not as arguments. The live failure is answering *why* when asked *what*.
- Add the in-call governor to the checklist: *"Asked what something means → lead with the noun in under eight words, then stop. Rationale is the second sentence, only if they ask."*

**Orthogonality line (one sentence, also required):** name the pair of criteria most likely to be accused of overlap, and the one-sentence distinction. If an input appears under two criteria, that is a MECE defect and it must be resolved before the round, not defended in it. Full gate: `framework/adversarial-analysis-pipeline.md` §7.4.

**Origin:** an onsite at a target company. Eight turns to establish what a named scoring criterion actually meant, and the interviewer found a real MECE violation (one metric load-bearing in two different criteria) that six days of review had never checked. Same defect fired in the other block on an integration primitive. See [[feedback_audit_frame_structure_not_only_claim_truth]] and the tracker's "Supplies a rationale when asked for a definition".

## Grounded Decision Panel (B4b — whenever Nick brings a deliverable, NOT a generic critic)

**Fires with B4** — any round where Nick presents or defends something he authored (take-home deck, brief, case recommendation, scorecard).

**Build the actual decision panel, not a McKinsey-partner critic.** A generic senior-partner persona attacks at the wrong altitude: it critiques craft and structure, while the real room asks "does this change what I do on Monday?" Construct one seat per real decision-maker from the dossier + `data/people/<slug>.md` — their function, what they own, what this deliverable costs or gains them — and critique through those seats.

**Run it twice, and the second run is the one that gets skipped:**

1. **Prep pressure-test** — before drafting, to find the shape.
2. **Pre-send QC on the FINISHED artifact** — give each seat the verbatim prompt *plus* the actual built deliverable, isolated from each other (anti-anchoring, per the global multi-agent rule), and ask for **concrete corrections** ("the brief claims X but…"), never approval.

**Cross-seat convergence is the signal.** When independent seats name the *same* hole, that is must-fix. Single-seat hits are triage. On one deliverable, all four seats independently named the same methodological hole (a recalibration read from rejected-only data — selective-labels censoring), caught with ~2 hours left to fix it.

**Origin:** 2026-06-27 + 2026-06-29, two fires. See `memory/feedback_ground_pressure_test_in_decision_panel_not_generic_partner.md`. Composes with B4 above (bare definitions) and the frame hygiene gate at `framework/adversarial-analysis-pipeline.md` §7.4 — B4 tests whether the terms are defined, this tests whether the *decision* lands.

## Custody Rehearsal (B5 — presentation-defense rounds only)

**One rep, five minutes, before any round where Nick presents slides.** The counterpart halts him on the frame page and refuses to let him advance; he delivers the rest of the argument with no visual aid.

Every delivery rehearsal assumes the deck advances. **The likeliest real failure is being stopped on the page that carries the frame and never regaining the narrative** — in that room, slides 6 through 13 were never delivered as designed. Add to the checklist: *"If they take the floor at the frame page, I still owe them the argument. Know which three sentences carry it without the slides."*

## Reset-Carrier Rule (B6 — MANDATORY on every prep doc, no exceptions)

**The problem this solves:** a prep doc that is correct and never read is worth zero. On one founder screen the doc was generated that morning, carried a same-day dossier refresh, and Nick did not open it. Consequence: **zero of six prepared questions asked**, the strongest unfakeable proof unused, the company's own role framing unused — and he led with five enterprise-scale signals at a small-business-motion company, which was the founder's stated reason for passing. The role mismatch was real; the doc had already corrected the frame that made it look bigger.

This is a **different and upstream** defect from the known read-but-not-retrieved failure (2026-07-22: the governor line was read back aloud and still did not fire live). Here the artifact never entered the loop, so every prep-doc-resident behavior-change clause — H4's live-need bridge and governor, B3's clarifying-question count, B4's bare definitions, the NN probe questions — silently did not run. **Any debrief of such a call will misattribute the resulting misses to skill rather than to non-consumption.**

**The rule: bind the doc to the reset, because the reset is the only pre-call ritual with a proven execution record.**

The filler reset runs reliably as the literal last action before dialing (confirmed 2026-08-06: full protocol compliance produced the corpus's best real-call filler density, 2.8%). The prep doc has no such carrier. So attach it to the one that works rather than hoping it gets read on its own:

**T-minus-2 → scan · T-minus-1 → reset · dial.** Nothing substantive in between.

The scan is exactly three things, and the prep doc must be structured so all three are findable in under two minutes:
1. **THE ONE THING** — the single framing sentence for this call.
2. **The predicted live-need sentence** + the one bridge proof (H4).
3. **The questions list.**

**Generation-side requirements (enforce when writing any prep doc):**
- The mandatory checklist item 1 above is emitted verbatim, before any tailored items.
- **THE ONE THING**, the Live-Need Bridge block, and the questions list must each be reachable without scrolling past a wall of context — put them in the first third of the doc, or repeat them in a scan block at the top.
- **Whose-customers line (REQUIRED, one sentence, inside THE ONE THING):** *"Their customers are ___, so the proof of mine shaped like their customer is ___."* Enterprise-scale proofs at a small-business-motion company read as mismatch even when the underlying skill transfers — and vice versa. This line is what was missing on 8/06.
- If a late addition or dossier refresh lands after the doc is written, **fold its consequences into THE ONE THING**, do not only append a section at the bottom. On 8/06 the 09:45 refresh was appended below a 215-line doc and was never reached.
- **Primary AND reserve proof (REQUIRED, two lines, inside THE ONE THING — no new section, no new heading).** Emit exactly this shape:

  ```
  **Primary proof** (domain: <canonical-tag>): <proof>
  **Reserve proof** (domain: <canonical-tag>): <proof>
  ```

  - Both tags come from `proof_domains.valid_tags()` — run `PYTHONIOENCODING=utf-8 python3 tools/proof_domains.py --list` to see them, or `--canonicalize <tag>` if the natural label is not in the enum. **Do not invent a tag**; pick the nearest canonical one.
  - **The two domains MUST differ after canonicalization.** `customer-experience` and `customer-ops` are the same domain wearing two labels — one exclusion sentence takes out both, which is exactly the failure this line exists to prevent. Step 6a's checker (check 3) blocks the PDF render if they collapse.
  - The reserve is not a second-favorite proof. It is the one to reach for when the interviewer rules the primary's whole domain out of scope mid-call.

  **Origin:** a prep doc pre-bound a single proof and said not to substitute it. Partway into the call the counterpart ruled that entire domain out of scope and called the proof's central deliverable commoditizable. There was no fallback, and the follow-up led with the dead proof anyway. `/follow-up` Step 3e now reads this reserve line when a transcript shows the primary was excluded.

**Debrief-side requirement:** `/debrief` must ask whether the prep doc was read before scoring any bridge or question-quality miss. A miss under non-consumption is logged against **prep artifact not consumed**, not against the skill it appears to be.

**Origin:** 2026-08-06 founder screen. See `coaching/anti-pattern-tracker.md` § "Prep artifact not consumed" and that date's file in `coaching/progress/`.

## Opening Strategy (first 60 seconds)
[How to open the call — tone, the one thing to establish immediately, what NOT to do in opening]
[Specific suggested opening line for a [interview type] call]

## Closing Strategy
[How to close the call — what to ask, what to confirm, how to leave a strong impression]
[Specific suggested closing move for [interview type] at [Company]]

## Questions to Ask — [Interview Type] at [Company]
[5–7 strong questions tailored to this interview type and company. For each: the question + one-line note on what it signals.]

For recruiter: focus on role clarity, team dynamics, next steps, timeline.
For hiring manager: focus on team priorities, success metrics, company direction, role impact.
For panel: mix — some technical/functional, some culture, some about the panel members' work.

1. [Question] — *signals: [what this shows]*
2. [Question] — *signals: [what this shows]*
...

## Format & Logistics Reminders
- Interview type: [recruiter/hiring manager/panel]
- Platform: [if known from context, otherwise "confirm platform before the call"]
- Duration: [if known, otherwise "typically N minutes for [type]"]
- Who you're talking to: [from pipeline notes or company research, if known]
- Dress: [appropriate level — video call defaults to business casual unless context suggests otherwise]
- Pre-call: [specific prep actions — review notes, test tech, etc.]
- Send-state of any artifact (CV, cover letter, deck): [ONLY from an `outreach_status.py --stamp` call made this run — see the mandatory gate below]
```

**Send-state claims in Logistics are gated (MANDATORY — do not paraphrase this away).**

Every claim about whether Nick already sent someone something comes from a stamp generated **this run**, with `--artifact` set to the artifact the claim is about:

```
PYTHONIOENCODING=utf-8 python3 tools/outreach_status.py \
  --recipient "<name>" --company "<company>" --artifact <cv|cover-letter|deck|portfolio|writeup|link> \
  --as-of <doc date YYYY-MM-DD> --stamp
```

Paste the returned `<!-- outreach_status: … -->` comment into the Logistics block. Then:

- **Never infer a send from the existence of a file under `output/`.** `output/` is a *draft archive*: a file there proves a draft was generated, not that it was attached, not that it was sent, and not that it arrived. This inference is the entire mechanism of the 2026-08-10 defect.
- `resolution: not_found` → render `[unverified: no outreach-log row for <name> as of <date>]`. Do not fill the gap from memory.
- `resolution: ambiguous` → render `[unverified: ambiguous recipient — candidates: …]`. The tool exits 2 and never guesses; neither do you.
- **Suppressive phrasing** ("do not re-offer it", "already sent", "no need to send") must **(a) name the artifact it suppresses** and **(b)** be backed by a stamp for *that same artifact* reading `delivered=true`.
  - `delivered=unknown` is **not** a license. The correct phrasing is *"sent <date>, no delivery confirmation — offer it again if asked."*
  - A recipient-level stamp (`artifact=none`) **never** licenses an artifact-level suppression. The recipient may have replied on an unrelated thread.
  - `delivered=false` means it bounced. Say so, and say to re-send.

**Step 6a runs `tools/check_prep_doc.py` against the saved doc and blocks the PDF render on failure** — checks 4-6 enforce (a) and (b) mechanically. This instruction is what makes the doc pass on the first try.

**Origin:** on 2026-08-10 a Logistics block asserted *"CV already sent 8/4, do not re-offer it."* No such row existed in the outreach log; the address had bounced on 8/4 (a fact recorded two lines above in the same block); the recipient asked for the CV again on 8/11. The suppressive half is the damaging half — it instructed Nick not to take the corrective action.

---

### Step 4b: Cross-Call Read-Forward (inline, not an agent)

After agents are dispatched, do these reads inline (in parallel with the agents). Output feeds three sections in the final document.

**1. Active anti-patterns** — read `coaching/progress/_summary.md` Anti-Pattern Scorecard. Take the top 3 by Total Occurrences (excluding zero-count rows). For each, look up its defense one-liner from `coaching/anti-pattern-tracker.md`.

**2. Promoted hypotheses for this format** — read `coaching/hypotheses.md`. Filter to Ladder = Promoted. For each, check whether the call's anticipated format tag appears in the hypothesis's Boundary clause. If yes, inject the Behavior-change clause directly. If no Promoted hypotheses exist, omit the section.

**3. Last session's predictions** — find the most recent `coaching/progress/<date>-*.md` (excluding `_summary.md`, the retrospective, and any drill files). Extract the `## Predictions for Next Session` block verbatim. Phrase as "From <date> <call> debrief: …" then prompt: "→ Has this work happened? Drill those answers before this call if not."

If any source is missing or empty, skip that section in output (graceful degradation per global CLAUDE.md rule).

### Step 4c: Expected Self-Doubt Firings (inline, mandatory; D1)

Per `framework/interview-prep-discipline.md` D1. REQUIRED in every prep doc (not agent-generated, since the belief catalog is Nick-specific). Read `data/professional-identity.md` for growth edges. Seed beliefs (use the ones that fit this call): not-smart-enough, don't-deserve-the-room, can't-ask-for-help, fraud, must-be-polished-before-sharing, disagree-pays-social-cost, too-generalist.

Build a table for 3-5 beliefs likely to fire in THIS call:

| Belief (verbatim) | Likely trigger in this call | Rehearsed counter-move (if-then) | Somatic signal |

Counter-moves must be if-then implementation intentions ("If the BCG-pedigree interviewer pushes twice, then I restate my position once before conceding"), not a vague "stay calm." Tie each belief to a professional-identity growth edge. Add one in-call reframe line: name the arousal as readiness, do not suppress it (suppression costs working memory).

### Step 4d: Drill Plan (inline, A1-A3; when pei-round OR 2+ gaps exist)

Per `framework/interview-prep-discipline.md` A1-A3 + B1. For the Deep-N stories (Agent 1) and the top gaps, produce a drill plan, not just "prep these":
- **Calibrate (A1):** for unfamiliar-domain content the drill is "read once, apply live", never "recall from memory." Name the drill type (recall / application / synthesis) and the baseline it assumes; a blank page means the design is wrong, not the candidate.
- **Cold spoken retrieval (A2):** each drill is a cold, aloud, timed, no-notes delivery before any review. For high-stakes calls add one rep under added pressure (cold-open or hostile follow-up).
- **Space + interleave (A3):** if there is more than one day, schedule spaced re-drills (next-day, +3 days) and interleave question types rather than block-repping one story.

Output each as: story/gap, drill type, one cold-delivery prompt, spacing note.

### Step 4e: What I'm Testing About Me (inline, F3; when discovery = true)

Per `framework/interview-prep-discipline.md` F3. Only for discovery / first-call / recruiter screens. Before the questions-to-ask-them list, write 2-3 of Nick's own-clarity probes: questions whose purpose is to test whether this seat energizes him when he describes it back, mapped to `data/goals.md` non-negotiables. Require that the reverse questions (Agent 3) each carry a behavioral anchor ("tell me about the last time...") rather than an abstract values question. Note inline: the post-call `/debrief` is mandatory for this rep to count.

---

### Step 5: Compile Output Document

After all 3 agents return, compile their outputs into a single document. Do not just concatenate — synthesize:
- Ensure question mapping (Agent 1) and company context (Agent 2) don't repeat the same facts
- Merge any overlapping anti-pattern warnings between Agent 1 and Agent 3 into one unified list
- Cross-link where relevant (e.g., if Agent 2 identified a key business challenge, and Agent 1 has a question about it, note the link)

**Staging gates:** If the interview type is `recruiter`, add explicit staging labels throughout:
- Mark any content that references personal experience, deeper disclosure, or operational insights with `[HM-STAGE ONLY]` or move to a separate "If You Advance" section at the bottom.
- Recruiter-stage answer frameworks should use the most guarded framing of personal motivation (e.g., "X is personal to me" not "going through X myself").
- For healthcare/behavioral health companies specifically: recruiters in the clinical space can infer program types from specific language. Heighten disclosure awareness in anti-patterns.

**Self-reported metrics:** When citing company-reported outcomes (readmission rates, NPS, adherence, cost savings) in answer frameworks or company context, qualify with "they report" or "self-reported." Presenting unverified metrics as fact undermines credibility with knowledgeable interviewers.

**Cross-reference reduction:** If existing research briefs (SMI brief, industry dossier, comparison briefs) cover a topic in depth, cross-reference them in the prep doc rather than reproducing the content. The prep doc should be a quick-scan interview tool, not a second copy of the research.

**Time-boxed compression (F2):** A usable doc beats a comprehensive one. Compute a realistic item budget for the call length (30 min is roughly 2-3 deep stories + 3-4 questions). Put the non-negotiable few at the top (carry-these, the Deep-N stories, the decision-aligned question shortlist); move everything else under an explicit "Depth Bank (only if the conversation goes there)." Tag each kept item with the decision it serves and its job (carry / screen / answer per F1). When in doubt, cut; do not defend volume.

### Step 6: Determine Output Filename and Save

- Use the company slug from Step 1 as the subfolder: `output/<company-slug>/`
- Generate: `output/<company-slug>/MMDDYY-prep.md`
  (company is already in the folder name, omit from filename)
- If file exists, append `-v2`, `-v3` etc.
- Write the compiled document to that path.

### Step 6a: Compliance Gate (MANDATORY — runs before the PDF, never after)

Run the checker on the file just saved:

```bash
PYTHONIOENCODING=utf-8 python3 tools/check_prep_doc.py output/<company-slug>/MMDDYY-prep.md
```

**This runs before Step 6b by design.** The PDF is the artifact Nick reads on paper, morning-of. A false send-state claim or a missing reserve proof that reaches the printed page is exactly the failure mode this gate exists to stop — catching it after the render means catching it after he has already read it.

- **Exit 0 (`compliant: true`)** → proceed to Step 6b.
- **Exit 2** → the path is wrong. Fix the path and re-run; do not skip.
- **Exit 1** → **do NOT render the PDF.** Fix the doc, re-save, re-run this step until it exits 0. Each failure names its check:

| Check | Fix |
|---|---|
| 1 / 2 | Add the missing `**Primary proof**` / `**Reserve proof**` line inside THE ONE THING, in the frozen format with a `(domain: <tag>)` tag. |
| 3 | The two domains collapse to one, or a tag is not in the enum. Run `PYTHONIOENCODING=utf-8 python3 tools/proof_domains.py --list` and pick a genuinely different domain — **do not** just relabel the same proof. A reserve in the primary's domain dies to the same exclusion sentence. |
| 4 | A suppressive sentence in Logistics either names no artifact or has no `delivered=true` stamp for the artifact it names. Either generate the stamp (see the Logistics gate above) or **rewrite the sentence** — *"sent \<date\>, no delivery confirmation — offer it again if asked."* Rewriting is usually the correct fix; the stamp is only correct when the artifact genuinely arrived. |
| 5 | A stamp predates the doc. Re-run `outreach_status.py --stamp` with `--as-of` set to the doc's own date and replace it. |
| 6 | A stamp is malformed or v1 (no `artifact=`). Regenerate it; never hand-edit a stamp. |

**Do not fix a failure by deleting the offending line and moving on** when the underlying claim is what matters — a suppressive sentence removed without checking the send-state leaves Nick with no guidance where he previously had wrong guidance. Resolve the fact, then write the line.

If Nick explicitly overrides a failure, note the check number and his reason inline in the doc. An unexplained override is indistinguishable from a skipped gate.

### Step 6b: Render PDF (mandatory terminal artifact)

After the Step 6a gate passes, render a printable PDF as the closing action. Per `memory/feedback_print_prep_pdfs`, Nick reads high-stakes prep on paper.

```bash
PYTHONIOENCODING=utf-8 python3 tools/md_to_pdf_doc.py output/<company-slug>/MMDDYY-prep.md
```

This produces `output/<company-slug>/MMDDYY-prep.pdf` (weasyprint, Georgia, multi-page).

Then offer print:

> Generated `output/<company-slug>/MMDDYY-prep.pdf`. Run `lpr output/<company-slug>/MMDDYY-prep.pdf` to send to default printer (recommended for high-stakes calls).

Do NOT auto-print without Nick's confirmation. The offer is the closing beat.

### Step 7: Add Debrief To-Do

1. Read `data/job-todos.md`.
2. Add a new to-do:
   - **Task**: `Debrief after [Company] interview — run \`/debrief\``
   - **Priority**: `High`
   - **Due**: interview date (if known from context), otherwise today
   - **Notes**: `From /prep-interview on [today's date]`
3. Write updated file.

### Step 7b: Advance Pipeline Stage (deterministic — only when this is a scheduled round)

Prepping for a **confirmed, dated** round is a state change: the pipeline row must reflect it. This step closes the gap where `/prep-interview` (a pipeline read-consumer) left the stage stale because it never wrote back. Origin: 2026-06-09 a target company — prep ran the morning the Executive Screen was booked, created the debrief to-do, but left the pipeline reading "awaiting next-step read / nudge the recruiter by 6/13" (a stale gate against booked intel). See `memory/feedback_prep_interview_must_advance_pipeline_on_scheduled_round.md`.

**Gate (this is the only judgment, and a date resolves it):**
- Proceed **only if** the round has a **known/confirmed date** — a date in the context string, or a calendar invite, i.e. the interview is actually scheduled.
- **Skip** (and note why) if: the prep is exploratory / no date is known; the company is not in the pipeline (handled by the `/pipe add` edge case); or the pipeline stage already reflects this exact booked round (idempotent — do not rewrite an unchanged stage).

When the gate passes, advance the row via `pipe_write.py` (atomic; never Edit `job-pipeline.md`):

```bash
PYTHONIOENCODING=utf-8 python3 tools/pipe_write.py --repo-root . update "<Company>" "<interview-type> booked (<interviewer if known>, <date>)" --next-action "Prep complete; run /debrief after <date>. Hold geography + comp discipline."
```

- Build `<new stage>` from what this run already knows (Step 1 stage + Step 1b round type + interviewer + date). Example: `Executive Screen booked (Jane Doe, Mon 6/15 9:30 AM PDT)`.
- Do NOT overwrite a richer existing next-action with judgment in it unless it's the now-stale gate this round supersedes; prefer advancing the stage + replacing only the superseded gate. When unsure which of multiple roles for the company, use the same match resolved in Step 1.
- Report the before→after stage in Step 8.

### Step 8: Display Summary

```markdown
## Interview Prep Ready — [Company] / [Role]

**Interview type:** [recruiter/hiring-manager/panel/general]
**Date:** [date if known, or "not specified"]
**Stage:** [from pipeline]

**Saved:** `output/<company-slug>/MMDDYY-prep.md`

### Coverage
- Questions mapped: N (N with coached answers, N gaps)
- Company dossier: [✅ Full dossier used] / [⚠️ Quick web search only — run `/research-company "[Company]"` for depth]
- Anti-patterns checklist: N items

### Top 3 Answer Gaps (prep these)
1. [Question with no coached answer]
2. [Question with no coached answer]
3. [Question with no coached answer]

### Pipeline
[✅ Advanced: "[old stage]" → "[new stage]"] / [— Not advanced: no confirmed date / not in pipeline / already current]

### To-Do Created
✅ "Debrief after [Company] interview" added to job-todos.md [due: date]

---
Full prep doc: `output/<company-slug>/MMDDYY-prep.md`
After the interview: `/debrief` to log session and update coached answers
```

## Output File Format

```markdown
# Interview Prep — [Company] / [Role]
> [Interview type] | [Date if known] | Generated [today]

## At a Glance
| Field | Detail |
|-------|--------|
| Company | [name] |
| Role | [title] |
| Stage | [pipeline stage] |
| Interview type | [recruiter/hiring-manager/panel/general] |
| Date | [date or "TBD"] |
| Key contact | [if known from pipeline or research] |
| CV used | [filename or "not specified"] |

[IF INCONSISTENCIES FOUND IN STEP 3b]:
## ⚠️ Consistency Warnings

| # | Conflict | Source A | Source B | Suggested Resolution |
|---|----------|----------|----------|---------------------|
| 1 | [What conflicts] | [File A says X] | [File B says Y] | [Which to use / user to decide] |

> Review these before the interview. Use the suggested resolution or update the source files.

## 15-Second Pitch (for this role)
[Tailored from professional-identity.md + specific role requirements at this company]
Format: "[Who you are] with [key credential/experience]. Most relevant: [2 projects/roles]. Looking for [role type] — interested in [Company] because [specific, researched reason]."

## Likely Questions → Coached Answers
[From Agent 1 — 10–12 questions with answer frameworks, key points, coached answer references, and per-answer anti-patterns]

## Answer Gaps (no coached answer exists — prep these)
[From Agent 1 — questions flagged as gaps, with suggested approach for each]

## Section: Active Anti-Patterns to Watch For

> Inline-populated by Step 4b. Pulled from `coaching/progress/_summary.md`
> Anti-Pattern Scorecard. Top 3 by total occurrences. For each: name,
> last seen, defense (one line from `coaching/anti-pattern-tracker.md`).

Example output:
```
1. **Filler hedging** (11 occurrences, last seen 2026-05-05).
   Defense: cold drill 5 min pre-call to "0 fillers" target.

2. **Proper noun error under pressure** (4 occurrences, last seen 2026-05-05).
   Defense: write target proper nouns out longhand before every call.

3. **Chronological career walkthrough** (4 occurrences, last seen 2026-04-20).
   Defense: McKinsey-first descending-size opening.
```

## Section: Promoted Hypotheses for This Format

> Inline-populated by Step 4b. Pulled from `coaching/hypotheses.md` where
> Ladder = Promoted AND the hypothesis's claim or boundary mentions
> this call's anticipated format tag. Inject the behavior-change clause
> directly.
>
> If no hypotheses are Promoted yet: skip this section. (At v1 launch
> H1 is Active, not Promoted, so this section will likely be empty for
> the first batch of calls.)

## Section: Last Session's Focus

> Inline-populated by Step 4b. Pulled from the most recent
> `coaching/progress/<date>-*.md` file's "## Predictions for Next
> Session" block.

Example output:
```
From 2026-05-06 Acme AI / hiring-manager debrief:
- Sharpen "what's not on your resume" — replace generic expertise framing
  with a named anecdote.
- Tighten "dream job in 4-6 years" answer — name a specific outcome.

→ Has this work happened? Drill those two answers before this call if not.
```

[IF pei-round OR 2+ gaps]:
## PEI Deep-N + Drill Plan
[From Agent 1 + Step 4d — the 2-3 designated owned+quantified Deep-N stories (4 layers, 10+ probes each, tagged to a dimension), plus the calibrated cold-spoken-retrieval drill plan for Deep-N stories and top gaps.]

## Expected Self-Doubt Firings
[From Step 4c — REQUIRED. 3-5 beliefs: verbatim / trigger / if-then counter / somatic, tied to growth edges. Plus the one in-call reframe line.]

[IF DISCOVERY/RECRUITER CALL]:
## What I'm Testing About Me
[From Step 4e — 2-3 own-clarity probes mapped to goals.md non-negotiables, placed before the questions-to-ask-them list.]

## Company Context (condensed)
[From Agent 2 — mission, key business challenge, news to reference, what they care about, cultural signals, interviewer fluency read, things to avoid]

## Questions to Ask
[From Agent 3 — 5–7 tailored questions with "signals:" notes]

## Pre-Call Checklist
[From Agent 3 — 7–10 checkbox items, tailored to interview type and personal anti-patterns]

## Opening & Closing Strategy
[From Agent 3]

## Logistics
[From Agent 3 — format, platform, duration, who you're talking to, dress, pre-call reminders]

[IF INTERVIEW TYPE IS RECRUITER]:
## If You Advance — Hiring Manager Prep References

[Table linking existing research briefs and dossiers relevant to this company/role. Each row: document path, what it covers, when to use it. Include a staging rule summary: what shows up at recruiter stage (confidence only) vs. HM stage (deeper framing, operational insights).]
```

## Edge Cases

- **Company not in pipeline**: Proceed with available data. Note: "⚠️ [Company] not found in pipeline — consider adding with `/pipe add`."
- **No coached answers file**: Skip coached answer cross-referencing. Note the gap in all question mapping entries.
- **No company dossier and web search fails**: Proceed with whatever context is available from the pipeline and profile. Flag prominently.
- **Agent fails**: Proceed with remaining agents' data. Note which section is thin.
- **No interview date provided**: Omit date from output. Set debrief to-do due date as "—" (no deadline).
- **Multiple pipeline entries for same company**: If role was specified, use the matching one. If not, use the most recently updated entry. Note which entry was matched.
