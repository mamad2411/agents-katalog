---
name: ideate
description: Generate and critically evaluate grounded Infiquetra product, architecture, or workflow ideas. Multi-agent divergent→convergent engine — generate many, critique all, explain survivors only. Triggers on "ideate on X", "give me ideas", "what should I improve", "surprise me", "what would you change".
---

# Ideate

Generate and critically evaluate grounded Infiquetra ideas. The engine generates many
candidates across parallel frames, critiques all of them, and explains only the survivors —
with their rejection reasons preserved and revivable.

`/ideate` sits in the Think phase, before `/brainstorm` and `/plan`:

- `/office-hours` answers: "What is even the right frame here?"
- `/ideate` answers: "What are the strongest ideas worth exploring?"
- `/brainstorm` answers: "What exactly should one chosen idea mean?"
- `/plan` answers: "How should it be built?"

This skill produces a ranked ideation artifact under `docs/ideation/`. It does **not** produce
requirements, plans, or code.

## Core principles

1. **Ground before ideating.** Scan the actual repo, journal, and relevant context-libraries
   first. Do not generate abstract advice detached from the infiquetra world.
2. **Generate many → critique all → explain survivors only.** The quality mechanism is explicit
   rejection with reasons, not optimistic ranking. Extra process must not obscure this.
3. **Two-way partnership.** AI-generated and user-supplied ideas enter the **same** pool and face
   the **same** critique. User seeds are fed **into** the frame agents to build on / challenge /
   combine — never just judged at the end, never rubber-stamped, never silently dropped.
4. **Rejection is first-class and revivable.** Cut ideas keep stable IDs and can be revived — but
   only by re-entering the filter with new evidence (see the convergence reference).
5. **Durable source material only — never issue creation.** Ideate produces durable source material
   (the ranked ideation artifact under `docs/ideation/`) and creates or mutates no GitHub issue: it
   never runs `gh issue create`. Mission Control owns issue creation; route there.

## Interaction method

Use the platform's blocking question tool: `AskUserQuestion` in Claude Code (call `ToolSearch`
with `select:AskUserQuestion` first if its schema isn't loaded). Fall back to numbered options in
chat only when no blocking tool exists or the call errors. In a channel session, inline the
choices in the reply text. Never silently skip a gate question. Ask one question at a time.

<!-- gate-record: id=ideate-interaction absence=HALT transport=ask-user-question -->
**Operator-absence contract (#371).** Every known-set gate above declares what happens on
silence, and the declaration above this line is the contract. `HALT` here: stop and wait. A timeout,
a widget error, or a dropped session is never consent — do not proceed on a default and do not
invent an answer. Ask one question at a time and read the decision from the operator's actual
answer, never from a widget's raw return value.

## Advisory typed judgments

Six of the mechanical judgments around the critique can be asked as typed questions instead of
eyeballed, through `plugins/saga/scripts/shaping_judgments.py`. Every one of them is **advisory**:
it informs a judgment this skill already makes, it is never a gate, it never promotes or cuts an
idea, and the operator can ignore it. Each **fails open** — when the call fails, times out, or the
key is absent, run the phase exactly as this skill describes it below, with a one-line
non-blocking note. Never block a phase on one.

| Judgment | Phase | What it informs | Fails open to |
|---|---|---|---|
| `dedupe` | 2 (merge and dedupe) | which candidates describe the same idea; it returns **groups** and never removes a candidate | merging by reading, as today |
| `axis` | 2 (axis-coverage check) | which axis a candidate most centrally targets, with a "none" option so a real gap is visible | assigning axes by reading |
| `grounding-fit` | 0.2 | which of the four outcomes the topic falls into | asking the operator, which the gate already requires |
| `tactical-scope` | 0.4 | whether the focus opts into tactical scope | the keyword list alone |
| `rubric` | 3 (survivor scoring) | per-survivor scores beside the critics' prose verdicts | the prose verdicts alone |
| `revival` | 6.3 (step 1) | whether new evidence addresses the recorded rejection reason | adjudicating novelty by reading |

Two rules bind all six. A confident answer **never suppresses a question this skill would
otherwise ask** — the Phase 0.2 rule "ASK when unsure, never silently auto-route" is unchanged, and
an answer is evidence, not permission to skip the gate. And the keyword floor at Phase 0.4 and the
revival gate at 6.3 step 2a are **floors**: a judgment may only widen what they catch, never narrow
it.

```bash
python3 plugins/saga/scripts/shaping_judgments.py dedupe --state '{"candidates": [...]}'
```

## Reviewer-session transport

Orchestrate owns cross-vendor session transport. Do not run `engine_offer.py` and do
not launch `engine_session_runner.py`. `engine-registry.yaml` is capability metadata
only. The Phase 2 external-engine generator lane, when used, still goes through the
existing chaperone-dispatch path — never the retired saga runner. If a reviewer
session is required and is not in the Orchestrate run record, HALT.

## Focus hint

<focus_hint> #$ARGUMENTS </focus_hint>

Treat any argument as optional context: a concept (`DX improvements`), a path
(`plugins/unifi/`), a constraint (`low-complexity quick wins`), a backlog phrasing
(`themes in our open issues`), or a volume hint (`top 3`, `100 ideas`, `raise the bar`). With no
argument, proceed open-ended.

---

## Phase 0: Scope, grounding-fit gate, and seed capture

### 0.1 Resume check

Look in `docs/ideation/` for ideation docs from the last 30 days. Treat one as relevant when the
topic matches, the path/subsystem overlaps, or the request is open-ended with one obvious recent
open doc. Keep issue-grounded and non-issue ideation as distinct topics — do not offer to resume
across that boundary. If a relevant doc exists, ask whether to **continue** (read it, summarize
what was explored, preserve prior idea statuses, update the file in place) or **start fresh**.

### 0.2 Grounding-fit gate — ASK when unsure, never silently auto-route

Every downstream agent needs an identifiable subject and enough grounding to say something
specific. Weigh the **idea's breadth** against the **available grounding** — the current repo,
relevant `*-context-library` repos, and any named infiquetra repos. There are four outcomes.
When the call is not obvious, **ask** rather than auto-deciding; a vibe-check that routes silently
is the failure this gate exists to prevent.

**Outcome 1 — Clearly groundable → proceed.** The idea is bound to grounding you can actually
reach:

- Repo-bound — the idea lives inside the current repo. *Example: sitting in
  `infiquetra-claude-plugins`, `/ideate quick wins in the unifi plugin` — the plugin source
  is right here.*
- Multi-repo with named repos — the idea spans repos and names them. *Example: `/ideate how
  campps-auth and campps-identity-access should share session state` — both repos exist and are
  named, so grounding is bounded.* Record the named repos; Phase 1 grounds against each of them
  through the named-repo reader (Source 3).
- Inside a `*-context-library` with an idea that library grounds. *Example: sitting in
  `mimir-context-library`, `/ideate gaps in our mimir routing taxonomy` — the library is exactly
  the substance the idea needs.* Record that **the current repo is itself a `*-context-library`**;
  Phase 1 threads this flag so the library is read locally in place as the primary grounding
  (Source 4), not re-fetched over `gh` as if it were a remote. When it is borderline whether the
  library actually grounds the idea (vs. the idea being broader than the library's domain), lean to
  the **Case B** ask below rather than silently proceeding.

State the inferred framing in one plain sentence ("Treating this as a topic inside the unifi
plugin — about X") and proceed. Never print internal routing labels. Carry forward two facts the
gate establishes for Phase 1: **the named repos** (when the multi-repo branch fired) and **whether
the current repo is itself a `*-context-library`** (when the in-library branch fired).

**Outcome 2 — Out of the engineering domain → politely decline / redirect.** The subject has no
software surface in the infiquetra world — coffee, branding independent of a product, personal
decisions, non-digital business strategy. *Example: `/ideate names for my side coffee roastery`
→ decline: "That's outside what `/ideate` grounds against — I'd be generating ungrounded slop.
Want to take it to a general chat instead?"* Redirect kindly; do not run the engine. When a
subject sits on the engineering / non-engineering line — *"the infiquetra brand voice in our
docs"*, *"our developer-onboarding experience"* — do **not** hard-decline; **ask** which side it
is on (ground it as an engineering topic, or take it to general chat), per ASK-when-unsure.

**Outcome 3 (Case A) — Unframed / cannot settle a scope → recommend `/office-hours`.** The prompt
refers only to a quality or placeholder, not a subject — `improvements`, `ideas`, `what to
build`, `things to fix`, an empty prompt — and no repo footprint settles it. Being inside a repo
does **not** settle this: `improvements` in `infiquetra-claude-plugins` still scatters across DX,
reliability, new plugins, docs, and tests. *Example: `/ideate ideas` with nothing else → "There's
no settled subject here for the agents to work on. `/office-hours` is built for finding the frame
first — want to start there?"* Recommend `/office-hours`; proceed only if the operator declines,
and only after asking them to name a subject or pick "surprise me."

> Cheap disambiguation before asking: if a short phrase *might* name something
> (`browser sniff`, `dark mode`), Glob filenames or Grep the README/docs for it. Any footprint →
> treat as identifiable and proceed. No footprint and still reads as a bare quality → Case A.

**Outcome 4 (Case B) — Broad relative to grounding but still infiquetra → surface the mismatch
and ASK, leaning `/office-hours`.** The idea is legitimately infiquetra but far broader than the
grounding you are sitting in. *Example: sitting in `mimir-context-library`, `/ideate the whole
infiquetra plugin marketplace strategy` — real infiquetra topic, but the library grounds mimir,
not the marketplace.* Surface it plainly: "You're in `mimir-context-library`, but this idea spans
the whole marketplace — the grounding here won't carry it. `/office-hours` fits a question this
broad better. Or name the repos it should span and I'll ground against each of them. Proceed broad
in place anyway?" Lean office-hours; proceed broad in-place only if the operator declines the
redirect. If the operator takes the "name the repos" offer, record those repos and ground against
them via the named-repo reader (Source 3) — do not promise grounding the engine cannot reach. If
they decline and proceed broad in-place without naming repos, note that grounding will be thin
(only the library you are sitting in), and weight survivors accordingly.

### 0.3 Capture user seed ideas

Ask whether the operator already has ideas they want in the run. Capture each verbatim as a
`user-seed` candidate. These are **partnership inputs**: they will be passed *into* the Phase 2
frame agents to build on / challenge / combine, AND enter the merged pool, AND face the identical
Phase 3 critique. They are never rubber-stamped and never silently dropped. If the operator has
none, note "no user seeds" and proceed — generation does not depend on them.

### 0.4 Focus, volume, and adaptive frame count

Infer two things from the focus hint and intake:

- **Focus context** — concept, path, constraint, backlog phrasing, or open-ended.
- **Volume override** — honor clear hints: `top 3`, `100 ideas`, `go deep`, `raise the bar`.

**Tactical-scope detection.** Scan the focus for tactical signals: `polish`, `typo`, `typos`,
`quick wins`, `small improvements`, `cleanup`, `small fixes`, or a single narrow file/line. When
present, lower the Phase 2 ambition floor (the meeting-test is waived) — the operator has opted
into tactical scope.

**Adaptive frame count (1–6) by scope.** Frame agents run on the **inherited model — no
tier-down** (creative ideation needs full reasoning). Scale the count to scope:

- **Tactical / single narrow file or fix** → 1 frame (or a single orchestrator pass for a true
  one-liner).
- **Narrow — one flow, one stage, one plugin** → 2–3 frames.
- **Standard subsystem or component** → 4 frames.
- **Broad — whole repo, multi-repo, or a sweeping product/architecture question** → all 6 frames.

Default per-frame target is ~6–8 raw candidates; volume overrides adjust it.

### 0.5 Cost notice

Before dispatching, state the agent count in one line so multi-agent cost is not invisible. Count
= grounding agents (current-repo scan + journal-learnings, always; named-repo reader, one per
repo the gate recorded for a multi-repo or "name the repos" ask; context-library reader when a
relevant library exists; issue read+cluster only on backlog intent; web only for the cross-domain
frame or on request) + N frame agents. When backlog intent fires (Source 5), the frame count is the
theme-frame count (≤4 — see Phase 2's backlog override), not the adaptive N above; state that count.
The line is informational; the operator need not ack it.

> Example: "Will dispatch ~7 agents: current-repo scan + journal-learnings + context-library
> reader + 4 frame agents. Skip phrases: 'no web research'."
> Example (multi-repo): "Will dispatch ~8 agents: current-repo scan + journal-learnings +
> named-repo reader x2 (campps-auth, campps-identity-access) + 4 frame agents."
> Example (tactical): "Will dispatch ~3 agents: current-repo scan + journal-learnings + 1 frame
> agent."

---

## Phase 1: Grounding

Generate a `<run-id>` once (8 hex chars). Create the scratch directory and capture its absolute
path for every checkpoint write this run:

```bash
SCRATCH_DIR=".claude/saga/ideate/<run-id>"
mkdir -p "$SCRATCH_DIR"
echo "$SCRATCH_DIR"
```

Use the echoed path as `<scratch-dir>`. Scratch lives under `.claude/saga/` — it
is ignored local state, never `/tmp` and never a durable doc.

Dispatch the grounding agents **in parallel, in the foreground** (results are needed before Phase
2). Each agent below carries its **verbatim tuned prompt** — dispatch it with that prompt body, not
a generic "scan the repo" instruction. The prompt body is the repeatability guarantee.

### Source 1 — Current-repo scan (always)

Dispatch an `Explore` (or general-purpose) sub-agent on the cheapest capable model with this
prompt verbatim, substituting `{focus_hint}`:

> Read the project's `AGENTS.md` (or `CLAUDE.md` as a compatibility fallback, then `README.md` if
> neither exists). Read `STRATEGY.md` if present — it captures the repo's target problem, wedge,
> persona, non-goals, and success criteria. Discover the top-level directory layout with the
> native glob tool (`Glob` pattern `*` then `*/*`). Read `docs/engineering-journal/` if present
> for the project's own record of how it thinks.
>
> For other root-level `*.md` files: if the focus hint names one specifically (e.g. "ideate based
> on FEEDBACK.md"), fully read it and include its substantive content under a heading
> `User-named references` — Phase 2 treats these as *constraint*, so quote real content, not a
> gist. For any other root-level `*.md` files, read briefly and give a one-line gist under
> `Additional context` — Phase 2 treats these as *background*.
>
> Return a concise summary (under 40 lines, longer only if user-named references carry substantive
> content) covering:
>
> - project shape (language, framework, top-level layout)
> - notable patterns or conventions
> - obvious pain points or gaps
> - likely leverage points for improvement
> - product/technical strategy summary if `STRATEGY.md` was present — include the wedge and active
>   direction verbatim so ideation can weight toward strategy-aligned moves
> - `User-named references` section (when the focus named root-level `*.md` files)
> - `Additional context` section (when other root-level `*.md` files exist)
>
> Keep the scan shallow otherwise — top-level docs and directory structure only. Do not analyze
> GitHub issues, templates, or contribution guidelines. Do not do deep code search.
>
> Focus hint: {focus_hint}

### Source 2 — Journal-learnings (always)

Read the current repo's own engineering journal directly (no separate agent needed if the
current-repo scan already loaded it; otherwise dispatch a sub-agent with this prompt verbatim):

> Read `docs/engineering-journal/LEARNINGS.md` and `docs/engineering-journal/DECISIONS.md` in this
> repo. Return only the entries relevant to this ideation focus: prior empirical findings, the
> mechanisms behind them, and any architecture/convention/tooling decisions (with their "revisit
> when" conditions) that bear on the focus. For each, give the one-line generalizable rule and a
> `file:line` or entry-date reference. Skip everything unrelated to the focus. If either file is
> absent, say so and return nothing for it.
>
> Focus hint: {focus_hint}

Surfaced learnings/decisions become `direct:` basis material for Phase 2 — an idea that
contradicts a recorded decision must engage that decision's "revisit when" condition or be cut.

### Source 3 — Named-repo reader (when the gate recorded named repos)

Trigger when Phase 0's gate recorded named repos — a multi-repo ask (`how campps-auth and
campps-identity-access should share session state`) or the Case B "name the repos it should span"
offer. This is the source that makes the gate's multi-repo promise real: it reads each named repo
the operator actually named, not just the current repo. Dispatch **one reader sub-agent per named
repo** in parallel, each with this prompt verbatim, substituting the repo name and focus:

> You are reading the `{repo_name}` infiquetra repo for material relevant to this ideation focus —
> this repo is in scope because the operator named it. Prefer the local clone at
> `~/workspace/infiquetra/{repo_name}` when it exists (faster and matches the working tree);
> otherwise read via `gh api` / `gh repo view`. Read the repo's `AGENTS.md` (or `CLAUDE.md` as a
> compatibility fallback, then `README.md`), `STRATEGY.md` if present, and the top-level directory
> layout relevant to the focus. Keep the scan shallow — top-level docs and the layout that bears on
> the focus only; do not do deep code search. Return: (1) the repo's shape, conventions, and the
> part of it the focus touches; (2) any constraint or contract this repo imposes that a cross-repo
> idea would have to honor (e.g., the session-token shape it already emits); (3) `file:line` or
> doc-name references so Phase 2 can cite `direct:` basis. If the repo cannot be reached (no clone
> and `gh` fails), say so plainly and return nothing for it.
>
> Repo: {repo_name}
> Focus hint: {focus_hint}

The returned repo shapes and cross-repo constraints become `direct:` basis material for Phase 2 —
a cross-repo idea that violates a contract a named repo already imposes must engage it or be cut.
On a per-repo read failure, follow **warn and proceed** ("Could not ground against {repo}: {reason}.
Proceeding with the repos that read.") — never block on one unreachable repo.

### Source 4 — Context-library reader (when a relevant library exists)

**Current-repo short-circuit.** When Phase 0's gate flagged that the current repo is itself a
`*-context-library` (the in-library branch of Outcome 1), that library is the primary grounding and
is already in the working tree. Do **not** re-fetch it over `gh` — read it locally in place: point a
reader sub-agent at the current working directory using the verbatim prompt below with
`{library_name}` set to the current repo and the local-clone path being `.` (the current repo), and
treat its output as the primary context-library context. Reserve `gh`-based discovery and remote
reads for OTHER topic-relevant libraries. This keeps the explicit library framing the gate said was
"exactly the substance the idea needs" and avoids a slower, staler remote double-read of the repo
you are standing in.

Then discover any OTHER libraries by pattern (skip the current repo in the results when it is itself
a context-library — it is already covered by the short-circuit above):

```bash
gh repo list infiquetra --limit 300 --json name --jq '.[].name' | grep -i context-library
```

Pick the topic-relevant ones (e.g. `mimir-context-library` for mimir/routing topics,
`campps-context-library` for campps topics, `infiquetra-context-library` for org-wide
conventions). For each relevant library, dispatch a reader sub-agent with this prompt verbatim,
substituting the library name and focus:

> You are reading the `{library_name}` context-library repo for material relevant to this
> ideation focus. Prefer the local clone at `~/workspace/infiquetra/{library_name}` when it exists
> (faster); otherwise read via `gh api` / `gh repo view`. Read the library's `README.md` and
> top-level layout first to understand what domain it grounds, then read only the documents
> relevant to the focus. Return: (1) the context this library establishes that bears on the focus
> — conventions, taxonomies, prior analyses, constraints; (2) any explicit guidance the library
> gives that an idea would have to honor; (3) `file:line` or doc-name references so Phase 2 can
> cite `direct:` basis. Skip everything unrelated. If nothing in the library bears on the focus,
> say so plainly and return nothing.
>
> Library: {library_name}
> Focus hint: {focus_hint}

If no `*-context-library` is topic-relevant, skip this source and note it in the cost notice.

### Source 5 — Issue read + cluster (ONLY on backlog intent)

Trigger only when the topic is explicitly about the backlog — phrasings like `open issues`, `issue
themes`, `issue patterns`, `what users are reporting`, `bug reports`. Do **not** trigger on a focus
that merely mentions a bug (`bug in auth`, `the signup bug`). There is **no mission-control
dependency** — this is a read-only `gh` read plus local clustering. Dispatch a sub-agent with this
prompt verbatim, substituting the repo and focus:

> Run this read-only command and cluster the results — do not mutate any issue, do not call
> mission-control:
>
> ```bash
> gh issue list --repo {repo} --state open --json number,title,body,labels --limit 200
> ```
>
> Group the open issues into 3–6 coherent themes by what they are actually about (not by label
> alone). For each theme return: a short theme name, the issue numbers in it, a one-line
> description of the shared problem, and a rough sense of how many issues and how recent. If fewer
> than 5 open issues exist, say "insufficient issue signal for theme analysis" and return the raw
> list. Each theme becomes candidate Phase 2 material, so make the shared problem concrete enough
> to ideate against.
>
> Repo: {repo}
> Focus hint: {focus_hint}

When usable themes return, they seed the Phase 2 frames (see Phase 2). On error (gh missing, no
remote, auth failure) warn "Issue analysis unavailable: {reason}. Proceeding with standard
ideation." and continue.

### Source 6 — Web (smart-auto)

Off by default for internal topics. Engage **only** for the cross-domain-analogy frame (Frame 5)
or on explicit request. **Never pass repo contents, journal entries, or context-library material
out.** When engaged, dispatch a web-research sub-agent with this prompt verbatim:

> Research external prior art and cross-domain analogies for this ideation focus. Do not assume
> any private repository context — operate purely from the focus description below. Return: named
> prior art and adjacent solutions (with sources), and 2–3 structurally analogous problems from
> unrelated fields (other industries, biology, games, infrastructure, history) with a one-line
> note on how each solved it. Cite every source so Phase 2 can use it as `external:` basis. Push
> past the obvious first analogy.
>
> Focus hint (no private context): {focus_hint}

Honor skip phrases ("no web research"); note the skip in the grounding summary.

### Consolidate

Merge all results into one **grounding summary** with these sections (omit any that produced
nothing): **Repo context** (project shape, patterns, pain points, leverage points, strategy);
**User-named references** (constraint); **Additional context** (background); **Journal learnings**;
**Named-repo context** (per named repo, with its cross-repo constraints — when the gate recorded
named repos); **Context-library context** (per library); **Issue themes** (when backlog intent
fired); **External context** (when web ran). Grounding failures follow **warn and proceed** — never
block on a grounding miss. Phase 1.5 appends a `Topic axes` section to this same summary.

---

## Phase 1.5: Topic-surface decomposition

Decompose the subject into 3–5 orthogonal **axes** naming *what aspects to think about*. Frames
(Phase 2) determine *how to think*; axes determine *what to think on*. Without an explicit axis
list, parallel frames converge on whichever interpretation is most salient at first read and the
rest of the surface goes unexamined — lens diversity alone does not produce surface coverage.

This is a single orchestrator-side analysis against the grounding summary already in context. No
sub-agent, no extra grounding read, no user-facing question.

**Axis criteria:** 3–5 axes; **orthogonal** (one idea falls on one axis — merge heavy overlaps);
**derived from the actual grounding**, not a generic template; at the **same level** (don't mix
"the whole plugin" with "one frontmatter field"); **named in the topic's language** a reader would
recognize.

Worked examples (illustrative — derive yours from real grounding):

| Topic | Axes |
|---|---|
| Improve the unifi plugin | Endpoint coverage; dry-run ergonomics; error handling; output formatting; auth/session robustness |
| mimir routing taxonomy | Route definitions; classification signals; fallback behavior; observability of routing decisions |
| campps session-state sharing across services | Token shape; storage/replication; invalidation triggers; cross-service contract |

**Skip condition (atomic subjects).** Some subjects resist meaningful decomposition: a single
string output (a name, a tagline), a narrow tactical fix ("the typo on line 47"), or a topic where
the candidate axes *are* the deliverable. When 3+ orthogonal axes passing the criteria cannot be
generated, **skip** decomposition and note `Decomposition skipped — atomic subject` in the
grounding summary so the artifact records the choice.

Append the axis list (or skip-reason) under a `Topic axes` section. Phase 2 threads axes into
frame prompts; Phase 3 uses them for axis-spread scoring; Phase 5's artifact records them.

---

## Phase 2: Divergent ideation

Generate the full candidate list before critiquing anything.

Dispatch the **N frame agents chosen in Phase 0.4** in parallel, on the **inherited model (no
tier-down)**. Omit any `mode` parameter so the operator's permission settings apply. Each agent
targets ~6–8 raw candidates (adjust for volume overrides). Each frame is a **starting bias, not a
cage** — begin from the assigned lens but follow any promising thread; cross-cutting ideas that
span frames are valuable.

**The six frames** (select the adaptive subset; for partial counts take them in this order):

1. **Pain & friction** — what is consistently slow, broken, or annoying for the user, operator, or
   maintainer.
2. **Inversion / removal / automation** — invert a painful step, remove it entirely, or automate
   it away.
3. **Assumption-breaking & reframing** — what is treated as fixed that is actually a choice;
   reframe one level up or sideways.
4. **Leverage & compounding** — choices that make many future moves cheaper or stronger;
   second-order effects.
5. **Cross-domain analogy** — how a structurally analogous problem is solved in an unrelated field
   (other industries, biology, games, infrastructure, history). This is the frame that may engage
   web (Source 6). Push past the obvious analogy.
6. **Constraint-flipping** — invert the obvious constraint to its opposite or extreme (budget 10x
   or 0; team of 100 or 1; 0 users or 1M). Use the resulting design as a candidate even if the
   flip itself is unrealistic.

**Backlog-intent override.** When Source 5 returned usable issue themes, turn each high-signal
theme into a frame; pad from the six-frame pool (in the order above) if fewer than 3 theme-frames
exist; cap at 4 frames total.

**Frame-agent prompt (verbatim — dispatch each frame agent with this, substituting its frame, the
grounding summary, the axis list, the per-agent target, the captured user seeds, and whether the
run is tactical scope):**

> You are generating raw ideation candidates for this Infiquetra topic through ONE assigned lens.
> Generate candidates only — do not critique, rank, or filter. Your first few ideas will be the
> obvious ones; push past them to the non-obvious. Target ~{per_agent_target} candidates.
>
> **Your frame (starting bias, not a cage):** {frame_name} — {frame_description}. Begin from this
> lens but follow any promising thread; a strong idea that spans frames is welcome.
>
> **Grounding summary (your substance — every idea must be grounded in it):**
> {grounding_summary}
>
> **Focus:** {focus_hint}
>
> **Topic axes (the surface map — distribute your ideas across them; tag each idea with the one
> axis it most centrally targets; reach a plausible axis at least once before doubling up):**
> {axis_list}      ← omit this whole block when decomposition was skipped; do not invent axes
>
> **User seed ideas — engage these directly, do not just restate them.** For each seed, do at
> least one of: build on it (extend or strengthen it through your lens), challenge it (surface a
> flaw or a better alternative your lens reveals), or combine it (merge it with another seed or one
> of your own into something stronger). Treat seeds as peers to generate against, not as fixed
> requirements and not as answers:
> {user_seeds}      ← when there are no seeds, state "No user seeds — generate freely."
>
> **Constraint vs background:** the focus hint, the operator's prompt, and any `User-named
> references` are CONSTRAINTS — an idea that violates them is out regardless of basis. The rest of
> the grounding (repo context, additional context, journal learnings, context-library context,
> external context) is BACKGROUND — it can support a basis and inform direction but must not pull
> ideation toward whatever was loudest in the corpus.
>
> **Per-idea contract — every idea returns exactly this, and an idea with no articulated basis
> does NOT surface:**
> - **title**
> - **summary** (2–4 sentences)
> - **axis** — required when an axis list was given above; pick the single axis this idea most
>   centrally targets; do not span. Omit only when decomposition was skipped.
> - **basis** (required, tagged — one of):
>   - `direct:` a quoted line / specific file / named issue / explicit user-supplied context or
>     seed it builds on
>   - `external:` named prior art / domain research / adjacent pattern, with its source
>   - `reasoned:` an explicit, written-out first-principles argument for why this move applies —
>     not a hand-wave; the argument is spelled out
> - **why_it_matters** — connects the basis to why the move is significant
> - **meeting_test** — one line confirming this would warrant team discussion. **Tactical scope:
>   {tactical_scope}** — when this is "yes", waive the meeting-test and state "tactical —
>   meeting-test waived" for each idea. The orchestrator sets this flag from Phase 0.4; do not try
>   to infer tactical scope yourself.
>
> Bias toward the basis type your frame naturally produces (pain/inversion/leverage → `direct:`;
> analogy/constraint-flipping → `reasoned:` or `external:`; assumption-breaking → mixed) but do not
> exclude other types. Stay within the subject's identity: expansions, new surfaces, and pivots are
> fair game when the basis supports them, but moves that abandon or replace the subject are out
> regardless of basis. When the focus names a slice (one flow, one plugin, one stage), ideate at
> full ambition *within that slice* — do not widen the surface to the whole product.

**External-engine generator lane (additive, blind, best-effort).** In addition to the N Claude frame
agents, attempt one chaperoned external-engine generator lane. Use the existing chaperone-dispatch
posture `offload` with `sonnet/medium`; do not route this generator lane through the stage-offer
`second-opinion` default. Assign the lane an ordinary Phase 2 frame value: use the next unused frame
from the ordered frame pool when one exists, otherwise reuse the frame whose lens best fits the focus.

Give the lane the same substituted frame-agent prompt above — frame, grounding summary, focus, topic
axes, per-agent target, captured user seeds, constraint/background split, and tactical-scope flag. Do
not add an external-engine-only prompt variant, do not relax the per-idea basis contract, and do not
include any raw candidates or merged candidate pool in the prompt. The lane is blind by construction:
its output first meets the Claude frame-agent output at the merge boundary below.

If the external-engine dispatch is unavailable, lacks credentials, times out, or returns an adapter
error, record a non-blocking note and continue with the Claude-only frame-agent set. Do not halt
`/ideate`, do not create a partial-failure state, and do not ask Phase 3 to compensate for the missing
lane.

**After all available generator lanes return:**

1. **Merge and dedupe** every frame agent's candidates into one master candidate list, keeping
   sub-agent (frame) attribution. For candidates produced by the external-engine generator lane, also
   tag the candidate provenance `engine-generated`. Do not apply `engine-generated` to Claude
   frame-agent, user-seed, interview, or combined candidates.
2. **Add the user seeds to the pool** as `user-seed` candidates (if not already absorbed by a
   frame agent that built on them). A seed a frame only *challenged* or rejected — rather than
   building into a promoted idea — still enters the pool as its own peer candidate; never drop a
   seed because a frame rejected a variant of it. Seeds face the identical Phase 3 critique — they
   are peers in the pool, never auto-promoted.
3. **Synthesize cross-cutting combinations** — scan for ideas from different frames that combine
   into something stronger; expect roughly 3–5 additions. Tag combined ideas with their source
   frames.
4. **Axis-coverage check** (when Phase 1.5 produced axes; skip otherwise) — count ideas per axis
   after dedupe. For any axis with zero ideas, dispatch **one** recovery frame agent (an unused
   frame, or the frame whose lens best fits the missing axis) targeting that axis with the same
   per-idea contract and ~3–5 ideas. **Cap recovery at 2 axes** — beyond that, accept thin
   coverage and note empty axes as `axis: <name> — recovery skipped (cap reached)` for the
   rejection summary. Merge recovery output and dedupe again.
5. If a focus was given, weight the merged list toward it without excluding stronger adjacent
   ideas. Spread across dimensions when justified: workflow/DX, reliability, extensibility, missing
   capabilities, docs/knowledge compounding, quality/maintenance, leverage on future work.

**Checkpoint — raw candidates.** Immediately after cross-cutting synthesis, write
`<scratch-dir>/raw-candidates.md` with the full candidate list and frame attribution (and the
captured user seeds). This protects the most expensive output (N parallel frame dispatches +
dedupe) before Phase 3 critique compacts context. Best-effort — if the write fails, warn and
proceed; the checkpoint is not load-bearing. Do not delete the run directory at the end of the run.

---

**End of Phase 2.** Load `saga/skills/ideate/references/convergence-and-partnership.md`
and follow Phases 3–6 (adversarial filter → present survivors + revivable cut → persist → refine /
co-ideate / revive / interview / hand off), then the quality-bar self-check. This load is
non-optional — the critique rubric, revival state machine, persistence template, the Phase 6 menu,
and the quality bar live there, not in this file. Do not improvise them from memory.

## Reference files

- `saga/skills/ideate/references/convergence-and-partnership.md` — Phases 3–6 (critique, present,
  persist, refine/revive/hand off) and the quality bar.
- `saga/skills/ideate/references/ideation-artifact.md` — the persisted artifact template.
- `saga/references/formatting-style.md` — the canonical formatting contract that governs how the
  presented survivors and the persisted artifact look (lead-in summaries, short prose, compact fields
  as a table).
