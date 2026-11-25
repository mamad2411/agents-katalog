---
name: academic-paper-revision
description: >-
  Revise an academic research paper draft (LaTeX) toward a specific target venue's
  conventions and a fluent, accepted-paper writing style. Use this whenever the user
  wants to prepare, tighten, restructure, or "clean up" a paper for submission — e.g.
  "get this ready for EMNLP", "make this read like an accepted ACL paper", "trim to the
  page limit", "remove the RQ/RO scaffolding", "add an algorithm/equation for the
  method", "why does this look like a student draft", "evaluate the novelty", "how did
  this line of work develop / what's the prior work / how is this different", or when
  they mention a venue
  (ACL, NAACL, EMNLP, AJCAI, NeurIPS, etc.) together
  with a manuscript. Trigger even if the user does not say the word "revise" — any
  request to make a paper draft match a venue or read more like a real published paper
  should use this skill. Accepts a target venue as input.
---

# Academic paper revision toward a target venue

Turn a rough or student-style paper draft into a submission that reads like an
*accepted* paper at a **specific venue**. The single most common failure mode is
applying generic "good writing" advice that is wrong for the target venue (trimming a
mandatory section, adding a page-costly section that is actually free, keeping
RQ/RO scaffolding that reviewers read as unpolished). So the work is always
**venue-first**: nail the target's rules, study its accepted papers, then rewrite.

## Inputs, outputs, and communication (read before Step 0)

**Expected input — the LaTeX source, not a PDF.** You edit source, so you need the
compilable project: the main `.tex` (often `main.tex`), `references.bib`, the venue class
/ style (`llncs.cls` + `*.bst`, or `acl.sty`, etc.), and `figures/`. This usually arrives
as a local repo or an **Overleaf project export (a zip)**. A rendered `main.pdf` is a
useful *secondary* input for verifying render-time properties (page count, float
placement) but is never sufficient on its own.
- If the user gives you **only a PDF**, ask for the LaTeX source — you cannot make surgical
  edits to a PDF, and reconstructing source loses their formatting and risks their numbers.
- If the user works in Overleaf, the round-trip is: they *Download Project* → you edit the
  source → you hand back a rebuilt zip → they re-upload and recompile. Package only the
  build inputs (`.tex`, `.bib`, class/style, `figures/`); exclude `main.pdf`, `README`, and
  git files.

**Communication language — ask once, up front; any language is fine.** The user may work
in and receive results in **any language** (Chinese, Spanish, Arabic, …). Ask which
language they want for the conversation, and default to the language they are writing to
you in. All briefings, findings, comments, and summaries are delivered in that chosen
language. **This is orthogonal to the manuscript:** the paper stays in **English** (or the
venue's required language) no matter what chat language you use — never translate the
manuscript, section text, or figure labels into the chat language unless the user
explicitly asks. Deliverables to the author go in their language; edits to `.tex`/`.bib`
stay in the venue's language.

**How you edit files.** Make **surgical `Edit`s** to the `.tex` and add any new citations to
`.bib`. Preserve the author's technical content and never alter result numbers (see Step 8).
When you add equations or an `algorithm` float, **offset the added length with content-
preserving prose trims** so the page limit holds. Do not commit, push, or re-zip-and-send as
shared actions without the user asking; when you do rebuild the upload zip, say where it is.

## Sample output — how to report findings

Match this shape (it mirrors an accepted-paper reviewer's memo). Keep each part tight; use
the user's chosen language.

1. **Orientation briefing** (Step 0): *What the draft is* · *Core contribution* ·
   *Novelty — candid* (with reviewer-attack bullets) · *State of completeness*. End by
   **confirming the venue** and asking what scope the user wants.
2. **Findings list** — one line per issue, grouped and severity-ordered, each naming the
   fix. Example rows:
   - `[venue]` Target = ACL (ARR): 8-page body, Limitations/Ethics free, double-blind — confirm via current CFP.
   - `[structure]` Explicit RQ1–RQ3 scaffolding → convert to prose contributions.
   - `[formalization]` Zero equations though the scoring rule is central → add 2–3 numbered eqs.
   - `[rigor]` Headline gain has no significance test, single split, threshold tuned on train → flag as the top weakness.
   - `[bug]` `\ref{fig:pipeline}` targets a figure with no `\label` → renders as `??`; add the label.
   - `[cross-ref]` Related work is a dated list → regroup into thematic paragraphs.
   - `[page-fit]` +0.5 page over after additions → list the exact offsetting trims.
   - `[trim]` The concrete moves for the page-fit line above: merge two redundant intro paras, move the worked example to an appendix.
3. **Change summary** (after editing) — bullet what changed and *why*, in this order:
   venue conventions applied · framing/structure · formalization added · figures ·
   build/cross-ref fixes · page-fit. Then **what the user must do**: recompile on Overleaf,
   verify the named render-time items (page count, a specific glyph/float), and the *next
   concrete lever* if a check fails. Flag anything you could not verify locally (e.g. no
   local LaTeX toolchain) and any unconfirmed venue rule.
4. **One honest caveat** — the single biggest reviewer risk or unresolved item, stated
   plainly (e.g. "the headline gain is within noise — no significance test is reported").

## Step 0 — Orient: brief the draft, the idea, and its novelty

Before proposing or making a single edit, read the whole draft and give the user a
short, honest **overview**. You and the user need a shared mental model of what the paper
*is* before you start changing how it reads — otherwise "improvements" drift from the
author's intent. Present:

- **What the draft is:** the problem it tackles, the proposed system/idea in 2–3
  sentences, and the current section structure (so gaps and misordering are visible).
- **The core contribution:** what the paper claims to add, stated plainly.
- **Novelty assessment — be specific and candid.** What is genuinely new here versus the
  closest prior work? Name the differentiator (a new task framing, mechanism, guarantee,
  dataset, or evaluation). Then flag the likely reviewer challenges: "this looks close to
  X — the paper needs to sharpen how it differs", "the novelty is in the protocol, not the
  agent count", etc. Do not inflate; if the novelty is thin or under-argued, say so — it is
  cheaper to hear it now than from a reviewer.
- **State of completeness:** what is done vs placeholder (missing results, TODO notes,
  unresolved references), so the revision plan is realistic.
- **Claims and rigor — does the evidence support the headline?** Check statistical
  validity, not just prose: is there a significance test, variance/confidence intervals,
  more than one split or seed, and no train/test leakage or threshold tuned on the test
  set? If the central claim rests on an uncontrolled or within-noise result, say so
  plainly — this is usually the top reviewer risk, and no amount of rewriting fixes it.

Keep this to a tight briefing, then confirm with the user (and correct your understanding
if they push back) before moving on. This orientation also feeds every later step: the
novelty you identify is exactly what the equations, algorithms, figures, and framing must
be made to protect and foreground.

### Deep novelty, lineage, and positioning analysis

Trigger this whenever the user asks any of "evaluate the novelty", "how did this line of
work develop / evolve", "what's the prior work", "how is this different / what's the
innovation", or whenever novelty is the paper's crux (reframing papers, "yet another
benchmark" risk, a contribution close to one prior system). A flat list of related work is
not enough — place the paper on a **trajectory** so its true contribution is legible. Deliver
four things:

- **Genealogy (how the line evolved).** Reconstruct the intellectual lineage as ordered
  *generations*, each defined by the **question it could newly ask**, not just by date.
  A good template: G0 *establish the paradigm and its first failures* → G1 *deepen
  reliability within one setting* → G2 *expose a new axis of variation* → G3 *ask which
  variation matters* → G4 (**the paper**) *the finer question no prior construction could
  pose*. For each generation name 1–3 representative works and the one-line advance. The
  payoff: the paper's contribution is exactly "the question the previous generation's
  construction structurally could not observe."
- **Prior-work grouping (thematic, not chronological).** Cluster the closest work into 2–4
  themes; for each, state what it settled and the residual gap. This is the raw material for
  the Related Work rewrite in Step 3 — reuse it.
- **Differentiator table.** Build an explicit *axis × (closest prior work vs this paper)*
  table (manipulation unit, evaluation target, core construct/claim, statistical stance,
  etc.). The rows are chosen so the paper wins at least one on a *structural* basis — a
  difference the prior design could not erase by adding scale. If you cannot fill such a
  row, the novelty is thin; say so.
- **Candid novelty verdict + reviewer-attack list.** State plainly what is *genuinely* new
  (concept/reframing, protocol/construction, guarantee, dataset, or evaluation — name which)
  and what is not. Then list the specific challenges a reviewer will raise, e.g.:
  *headline-vs-confirmatory tension* (the loudest number is descriptive while the confirmatory
  tests are null); *missing control* that would collapse the new construct into a known
  generic effect (name the exact follow-up experiment); *proximity to the single closest
  system* (the differentiator must stay structural, not cosmetic); *underpowered statistics*.
  Do not inflate. For reframing/"hidden-assumption" papers, also identify the **fallback
  claim** that survives even if the sharpest challenge succeeds — a robust paper has one, and
  naming it is often the highest-leverage framing fix you can make.

Distinguish the *kind* of novelty and judge it on its own terms: **conceptual/reframing**
(names a shared hidden assumption and shows it is wrong), **methodological/protocol** (a new
construction that observes something old designs could not), **artifact** (dataset/benchmark),
or **empirical** (scale/coverage). Reframing and protocol novelty are often more impactful
than one more benchmark, but their value hinges entirely on surviving the "this is just a
known generic effect" alternative — so protecting that is where framing effort should go.

## Step 1 — Establish the target venue (do this before touching prose)

Ask for or confirm the **target venue** if it is not already clear. This is
load-bearing: conventions differ so much between venues that the same edit can be
correct for one and a desk-reject for another. A filename or a memory note is *not*
authoritative — if a manuscript's filename names one venue but the user's notes name
another, surface the discrepancy and ask. Never assume.

Once confirmed, load the venue's conventions. Common families are documented in
`references/venue-conventions.md` — read it now for the relevant family (ACL-family vs
Springer/LNCS vs ML-conference). If the venue is not covered there, look up its
current call-for-papers (page limit, mandatory sections, anonymity, template) before
editing, and add what you learn to the reference file.

## Step 2 — Study accepted papers in the venue *and* subgenre

You cannot imitate a house style you have not read. Pull 2–4 recently **accepted**
papers that are (a) at the target venue and (b) in the same subgenre as the draft
(e.g. multi-agent + verification, a benchmark paper, an empirical audit/evaluation
study). Note concretely, per paper:

- Do they label contributions as "RQ1/RO2/O3", or write them as prose? (Accepted
  ACL-family papers almost always use prose.)
- Section-heading style: declarative noun phrases ("Falsification-first reasoning")
  vs generic ("Approach", "Experiment 1").
- Related-work organization: thematic/topic paragraphs vs chronological list.
- Do method sections use numbered **equations** and/or **algorithm** floats? How is the
  figure/equation/algorithm labor divided?
- Result subheadings: declarative statements of the finding vs bland ("Results").

Use these observations as the concrete target, not vague "make it academic". When you
lack local copies, fetch the arXiv/anthology HTML; if that fails, tell the user rather
than guessing at a paper's internals.

## Step 3 — Rewrite for fluent, accepted-paper tone

> **Review-only mode.** If the user asks for an overview/comments only (or is using the
> hosted read-only reviewer), stop after the Step 0 orientation briefing, findings list,
> and suggestions — make **no edits** to any file. Steps 3–8 below apply only to the
> full-revision mode.

The goal is prose that a reviewer reads as *finished*, not a lab notebook.

- **Remove RQ/RO/O scaffolding.** Replace explicit "Research Question 1 / Objective 2"
  machinery with prose contributions and declarative claims. The intellectual content
  stays; the scaffolding goes.
- **Declarative noun-phrase headings** that name the idea, not the slot.
- **Topic-organized related work**: group by theme, one claim per paragraph, end each
  with how the paper differs.
- **Strip author/project history** ("we previously built…", internal milestones) — it
  reads as a report, not a paper, and can break anonymity.
- **Merge overlapping paragraphs** and cut hedging. Prefer one precise sentence to three
  vague ones.
- Keep everything **in English** unless the user asks otherwise; venue submissions are
  English even when you are chatting with the user in another language.

## Step 4 — Fit the page limit (know what is free)

Trim the *main body* to the limit, but only after you know what counts. For ACL-family
venues, **Limitations, Ethics/Broader Impacts, References, and Appendix do not count**
toward the page limit — so never trim a mandatory Limitations section to save space,
and never treat Ethics as a luxury. See `references/venue-conventions.md`.

Pair the diagnosis with the concrete move: a `[page-fit]` finding ("+N pages over") should
always name the exact `[trim]` actions that offset it, so the fix is auditable.

Effective, content-preserving trims:
- Merge redundant paragraphs; fold two overlapping "discussion" points into one.
- Move a **worked example** or long derivation into the Appendix, leaving a one-sentence
  pointer in the body. This needs `\appendix` in the preamble/body; first confirm the
  appendix is page-free for the target venue (it is for ACL-family; verify others).
- Tighten Related Work by merging thematically adjacent paragraphs.

After trimming, verify the last main-body section still lands inside the limit on the
rendered PDF (page count is a render-time property, so confirm after compiling).

## Step 5 — Fix structural and cross-reference bugs

Student drafts commonly have build-level defects that make a paper look unfinished:

- A section file (e.g. `appendix.tex`) that is written but never `\input`-ed, leaving
  `\ref{...}` rendering as `??`. Wire it in (`\appendix` + `\input{...}`) and confirm the
  reference resolves.
- Dangling `\ref`/`\cite`, duplicate labels, `Figure ??`, missing `\label`s.
- Missing preamble packages for anything you add (e.g. `algorithm`, `algpseudocode`).

## Step 6 — Add and improve equations and algorithms

Formalization should be **balanced** and should **reinforce**, never undercut, the thesis.

- **Spot asymmetric formalization.** If the verdict/output is heavily formalized with
  equations but an equally central mechanism (retrieval, scoring, selection) is only
  prose, add an equation for it so the paper does not look lopsided.
- **Guard every formula against misreading.** When a component is deliberately *outside*
  the core decision (e.g. embedding similarity that feeds ranking only, not the verdict),
  state that explicitly right after the equation. A formula that seems to feed the
  decision when it must not will read as self-contradiction and can sink the core claim.
- **Use `algorithm` floats for deterministic procedures.** Any fixed, reproducible
  pipeline (extraction → reasoning → verify → route; a decoding/search loop) is clearer as
  pseudocode than as a bulleted list. Load `\usepackage{algorithm}` +
  `\usepackage{algpseudocode}`. This also strengthens reproducibility/"decision isn't the
  agent's opinion" arguments.
- **Full-width vs single-column.** Single ACL columns are ~3.2in wide, so pseudocode with
  long right-aligned `\Comment{...}` lines wraps and looks cramped. When comments are long,
  make it two-column with `algorithm*` (like `figure*`/`table*`); it must float to a page
  top. If the code is narrow with short comments, keep single-column `algorithm`.
- Keep the algorithm faithful to the real implementation and to any decision figure —
  do not invent control flow the code/method does not have.

## Step 7 — Reference-standard figures

Match the venue's figure conventions rather than reusing rough originals:

- **Vector, grayscale-friendly, colorblind-safe.** ACL-family venues allow color but require the
  figure to stay legible in grayscale and for colorblind readers, so never rely on color
  alone — pair it with shape, line style, or labels.
- Staged **box-and-gate pipeline** for system/architecture figures (labeled stages,
  arrows, gate/diamond for deterministic checks). Full-width system figure = `figure*`;
  single-column flowchart = `figure`.
- Deliver editable **vector** (TikZ or SVG the student can restyle), not bitmap PNG/JPG;
  final artifact should be PDF/vector.
- If the machine has no LaTeX/`pdftoppm`, you can preview a figure by building an
  equivalent HTML/SVG and rendering it, then hand off TikZ for the real compile on Overleaf.

## Step 8 — Research integrity (non-negotiable)

For preregistration-style papers, **fill result placeholders only from real, saved,
registered runs**. Never infer, estimate, or fabricate numbers from demos, scaffold
tests, or "it's probably around…". The discipline is **freeze → run → fill**, in that
order. If results do not exist yet, leave the placeholders and say so; a polished
manuscript without independent results is not submission-ready. When in doubt, stop and
ask the user rather than inventing a value.

## Working style notes

- Read a file before editing it; understand the existing structure before restructuring.
- Prefer surgical edits to wholesale rewrites; preserve the author's technical content.
- If you cannot compile locally, say so and have the user render on Overleaf; then adjust
  based on the actual rendered PDF (page count, float placement).
- Commit/push and other shared actions: only when the user asks, and confirm the target
  (branch, public vs private repo — watch anonymity for double-blind venues).
