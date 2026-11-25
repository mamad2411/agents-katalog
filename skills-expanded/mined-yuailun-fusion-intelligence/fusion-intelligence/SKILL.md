---
name: fusion-intelligence
description: >-
  Convene a panel of distinct reasoning lenses (epidemiology, causal inference, trial and measurement
  methodology, ethics, AI/ML, translation, philosophy of science) around ONE research question, ground
  them in cited evidence, run them independently, then fuse the results into consensus, divergence with
  its crux, blind spots, calibrated confidence and falsifiable next steps. Use to stress-test a research
  idea, study design, grant proposal, manuscript (Reviewer-2 pass), analysis plan, scale development,
  AI-method choice, discrepant results or an ethical dilemma, or whenever the user asks for a panel,
  council, several expert perspectives or a Pantheon-style answer. 触发词：多视角、专家会诊、圆桌、融合分析、
  课题预审、选题论证、压力测试、审稿人视角。Not for simple lookups, single-fact questions or routine coding.
---

# Fusion Intelligence

One question → a panel of **independent reasoning lenses** → **grounded in evidence** → **fused** into a
calibrated answer that shows where the lenses agree, where they split, *why* they split, and what to do
next. The value is surfaced disagreement and honest confidence, not an averaged opinion.

Distilled from the Pantheon method (K-Dense) and its Mimeographs library. Attribution: `NOTICE.md`.

## 0. Hard rules (never relax)

1. **Lenses are not people.** Never speak as, or invent quotes for, a real person. Write "through a causal-inference
   lens (after Pearl)…", never "Judea Pearl says…". Names in the library label *published frameworks*.
2. **Evidence before opinion.** Never invent a citation, DOI, PMID, statistic or guideline clause. Tag every
   claim `[E#]` (in the evidence ledger), `[R]` (reasoning), or `[A]` (assumption). If unverified, say so.
3. **Headcount is not evidence.** All lenses run on one model, so their errors correlate. Consensus is earned
   by independent evidence and by surviving a red-team attack, not by how many lenses nod.
4. **Independence.** Write each lens before reading any other lens. Never revise a lens after seeing another.
5. **Preserve dissent.** A minority position keeps its strongest argument in the report.
6. **Scope of authority.** Research-support tool, not medical, legal or financial advice. Patient-level
   decisions belong to qualified clinicians; ethics approval belongs to the ethics committee.
7. **Language.** Answer in the user's language (Chinese in → Chinese out); give English technical terms on first use.
8. **No hidden data.** Do not paste identifiable patient/participant data into prompts, ledgers or reports.

## 1. When to use / not use

Use when the answer is a **judgment under uncertainty** where several framings matter: idea selection,
design choice, interpretation, risk, ethics, feasibility, "is this convincing?". Skip for lookups, arithmetic,
code fixes, or when the user wants one fast answer with no deliberation. If unsure, offer `quick` mode.

## 2. Modes

| Mode | Panel | Evidence | Parallel agents | Output |
|---|---|---|---|---|
| `quick` | 4 lenses | light (what the user gave + 1–2 lookups) | no | ≤ 1 page |
| `standard` (default) | 6–8 lenses, ≥ 3 families | ledger of key claims | optional | 2–3 pages |
| `deep` | 10–16 lenses, ≥ 4 families + red team | full ledger + audit | recommended | full report |
| `pantheon` | all 80 (+ role lenses) in 4 batches | light | required (batches) | clustered map + fused report |

State the mode you picked in one line. For `deep` and `pantheon`, warn the user once about cost, then proceed
unless they object.

## 3. Workflow

### Step 1 — Question Brief (≤ 8 lines)
Restate: **the question** (one sentence); **the decision it feeds**; **question type** (see §4); **stakes**;
**constraints** (data, time, budget, ethics, setting); **the user's current belief** (their prior, if given);
**deliverable**. Ask at most 3 clarifying questions, and only if the answer would change panel or conclusion;
otherwise list assumptions and go.

### Step 2 — Convene the panel
Pick lenses from `references/lens-library.md` using `references/panel-presets.md`. Composition rules:
- ≥ 1 **methodologist** (design, measurement, statistics, causal structure)
- ≥ 1 **domain-substance** lens
- ≥ 1 **skeptic / red team** (always — it is mandatory)
- ≥ 1 **outside** lens from another family (ethics, philosophy of science, implementation, commercial)
- ≥ 1 **implementation realist** (who actually does this, with what time, money, staff?)
- Founder/operator lenses speak only to feasibility, resourcing and translation, never to scientific validity.

Show the panel as a list: `lens — why it is here` (one line each). Let the user swap lenses in one turn at most;
do not stall waiting for approval in `quick`/`standard`.

### Step 3 — Ground
Build an **evidence ledger** (`references/evidence-grounding.md`): `E1…En` with claim, source, design/N, direction,
strength (A–D). Use whatever retrieval exists (PubMed/literature tools, web search, the user's files) — read the
user's own documents first. Record gaps explicitly as `G1…Gn`. Do this *before* lens passes so lenses reason from
shared facts and are not each inventing their own.

### Step 4 — Lens passes
For each lens, produce the schema in `references/lens-pass-template.md` (position, 2–3 tagged claims, what it
sees that others miss, strongest objection to itself, test needed, confidence, one action). Length: quick ≈ 60
words/lens, standard ≈ 120, deep ≈ 180.
- **Parallel:** if the runtime has subagents *and* the mode is `deep`/`pantheon` (or the user asked for agents),
  launch one subagent per lens (or 3–4 lenses per agent in `pantheon`) in a single batch. Pass each agent only:
  the Question Brief, the evidence ledger, and that lens's card. Never pass other lenses' outputs.
- **Inline:** otherwise write lens sections sequentially under separate headings. Do not look back at earlier
  lenses to "harmonize" while writing a later one.

### Step 5 — Cross-examination (deep, or whenever divergence is high)
One round: take the 2–3 sharpest disagreements; have the opposing lenses answer each other's *strongest* point
in ≤ 60 words. Record concessions — a lens that moved is information.

### Step 6 — Fuse
Follow `references/fusion-protocol.md`. In short:
1. Extract atomic claims across lenses; build a **claim × lens support matrix** (support / oppose / silent).
2. Classify each claim: **Consensus** (≥ 2 independent families, no evidence-backed objection) · **Contested** ·
   **Single-lens hypothesis** · **Blind spot** (needed but nobody addressed it).
3. Diagnose each divergence by **crux type** — Factual, Methodological, Values/priorities, Definitional, Scope/
   population, or Time-horizon — and say what would resolve it.
4. **Calibrate** confidence (High / Moderate / Low / Unknown) by evidence quality + independent convergence +
   crux type. Never High on lens agreement alone.
5. Separate **no-regret moves** (good under every credible lens) from **conditional moves** (if crux X → do Y).
6. State **what would change the conclusion** (falsifiers).

### Step 7 — Deliver
Use a template from `references/report-templates.md` (full report, one-page brief, grant pre-review scorecard,
Reviewer-2 report, study-design memo). Open with the bottom line. If the user wants a file, save
`fusion-report-<slug>.md` in the working directory. Close by offering ≤ 3 follow-ups (drill into a crux · rerun
with a different panel · convert to a grant section / response letter / protocol).

## 4. Panel router (question type → preset)

| The user is asking about… | Preset in `panel-presets.md` |
|---|---|
| A new idea / "is this worth doing?" | `idea-stress-test` |
| How to design a study / protocol | `study-design` |
| Whether X causes Y / interpreting an association | `causal-claim-check` |
| Grant / project proposal pre-review (国自然、学会课题等) | `grant-prescreen` |
| A manuscript, "what would Reviewer 2 say?" | `manuscript-reviewer2` |
| A scale / questionnaire / construct (量表研制与验证) | `measurement-scale` |
| Prediction models, clinical ML, risk scores | `clinical-prediction-model` |
| Registry / EHR / perioperative database research | `real-world-database` |
| A nursing / behavioural / complex intervention | `intervention-implementation` |
| Using AI or LLMs in research or care | `ai-in-research` |
| Ethics, consent, integrity, a dilemma | `research-ethics` |
| What to work on / choosing a direction | `direction-selection` |
| Conflicting results or evidence | `discrepant-results` |
| Qualitative / mixed methods | `qualitative-mixed-methods` |
| Population / policy-level questions | `public-health-policy` |
| Turning findings into a product / pathway | `translation-commercial` |
| Anything else | `general-8` |

If two presets fit, merge them and drop to ≤ 10 lenses.

## 5. Report skeleton (standard mode)

```
# Fusion Report — <topic>
Bottom line (≤ 5 lines)  ·  Confidence: High | Moderate | Low | Unknown
1. Question brief & assumptions
2. Panel (lens — why)
3. Where the panel agrees        [claim · evidence tags · families that converge]
4. Where it splits               [claim · camp A vs camp B · crux type · what resolves it]
5. Blind spots & missing evidence
6. Recommended path              [no-regret moves | conditional moves]
7. What would change this conclusion
8. Next steps (≤ 5; owner · effort · test)
9. Evidence ledger               [E#, G#]
Appendix: per-lens positions · method note (mode, panel, tools, date)
```

## 6. Quality gates (check silently before delivering)

- [ ] Every factual statement is tagged `[E#]`, `[R]` or `[A]`; no invented references.
- [ ] ≥ 3 lens families (or a stated reason) and a red-team lens whose objection appears in the report.
- [ ] Each divergence has a crux type and a resolution path.
- [ ] Confidence is calibrated; "High" is backed by independent evidence, not lens agreement.
- [ ] "What would change this" is present and testable.
- [ ] No impersonation, no fabricated quotes; frameworks are attributed, not voiced.
- [ ] Language and length match the user and the mode.

## 7. Files in this skill

| File | Load when |
|---|---|
| `references/lens-library.md` | choosing lenses; building a lens card (80 lenses + 7 role lenses) |
| `references/panel-presets.md` | picking and tuning a panel for a research task |
| `references/evidence-grounding.md` | building the ledger, grading evidence, citing |
| `references/lens-pass-template.md` | writing or delegating a lens pass |
| `references/fusion-protocol.md` | doing Step 6 |
| `references/report-templates.md` | Step 7, incl. Chinese templates |
| `references/research-checklists.md` | reporting guidelines, causal and measurement checklists |
| `references/platform-notes.md` | Claude Code / Codex / Antigravity specifics, subagents, fallbacks |
| `examples/` | the expected look of a finished report |

## 8. Honest limits (say them when relevant)

A panel of model-generated lenses widens and structures thinking; it does not add independent expertise or new
data. It cannot replace a statistician, an ethics committee, domain experts, or a literature search you verify.
Treat the output as a rigorously organized second opinion to be challenged.
