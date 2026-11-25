---
name: focus-group
description: Synthetic audience pretesting (Justin Brooke "predictive wear" method). Run ANY outbound content — ads, emails, sales pages, newsletters, social posts, offers — through a per-business panel of AI persona dossiers BEFORE it ships. Panel critiques → copywriter rewrites 3 variants → prediction engine scores 0-100 → iterate until 85+. Intended as a hard gate: no outbound content ships without a run. Also use to build a new business panel ("focus-group setup <business>").
---

# Focus Group — Synthetic Audience Pretesting

Pretest content against a panel of deeply-researched AI persona dossiers before a dollar or a send goes out the door. Based on Justin Brooke's predictive-wear framework; Brooke reports ~85-92% correlation with human focus groups when personas are high quality.

**The iron law: personas > prompts.** The accuracy comes from the 1,400-word dossiers, not the panel prompt. Never run a panel with thin personas.

## Panel location

Keep one panel per business in your knowledge base, e.g. `{KNOWLEDGE_BASE}/{business}/focus-group/`. Each panel dir contains: an index note (roster, business context, scoring-weight overrides), `personas/*.md` (the dossiers), and `runs/` (run logs). Record your panel locations in your CLAUDE.md so sessions can find them without asking.

## Mode 1: RUN (default) — pretest content

Input needed: **the content** (pasted text, a file path, or a PDF — extract PDF text first with your PDF tooling) and **which business** it belongs to. If the business is obvious from context, don't ask. Identify the content type: `ad` (ads, social posts, emails, headlines) or `offer` (sales pages, launch emails, webinar scripts, anything asking for money) — offer mode adds the yes/no buy question. Separately, flag **social mode** when the content's primary goal is shares/forwards/organic reach rather than direct response — social mode adds the yes/no share question, the sharing-motivation requirement in the copywriter pass, and the social-mode scoring notes in the prediction engine (see [references/sharing-psychology.md](references/sharing-psychology.md)).

**Social-mode decision rule (don't guess):**
- Asset asks for money or a signup NOW (paid ad, sales email, landing page, launch email with a buy CTA) → conversion is primary. Social mode OFF unless the operator says the goal is reach.
- Organic and unpaid (social post, newsletter, video script for organic channels, lead magnet meant to be forwarded) → social mode ON by default.
- Both goals genuinely present (e.g., launch email you also want forwarded) → run BOTH modes; the copywriter splits the asset (share-worthy body, conversion close) rather than softening the money CTA.

### Pipeline

1. **Load the panel.** Read the business's index note (roster + context + any scoring-weight overrides). List `personas/*.md`.
2. **Fire the panel in parallel.** Spawn one subagent per persona (all in ONE message so they run concurrently; batch in groups if the panel exceeds ~8). Each subagent gets: the full text of its ONE persona dossier file (tell it the path to read), the content under review, and the panel prompt from [references/panel-prompt.md](references/panel-prompt.md). Each returns the structured feedback block. Personas critique from their OWN life — never as marketing experts. **Failure protocol:** if a persona subagent errors, rerun it once; proceed only if ≥75% of the panel reported (e.g., 6 of 8) — otherwise abort and restart the round. Record actual responders vs. roster size in the run log.
3. **Copywriter pass.** Using [references/copywriter-prompt.md](references/copywriter-prompt.md): embody a world-class copywriter ("embody", never "pretend"), digest ALL panel feedback + the original, write **3 optimized variants** in the business's voice (per the index note), formatted as an internal team email quoting key feedback.
4. **Prediction engine.** Scoring is done by a **fresh subagent that did not write the variants** (independence keeps the 85 gate honest). Give it: [references/prediction-engine.md](references/prediction-engine.md), all panel feedback, the business context + any weight overrides from the index note, and the variants. Default weights: Relatability 25 / Clarity 20 / Emotional 20 / Credibility 15 / CTA 20. Scores must anchor in panel data (see the "Who scores & anchoring" section of prediction-engine.md), not vibes. Verdicts: 85+ run, 75-84 test vs control, 65-74 revise, <65 reject.
5. **Iterate.** If no variant hits 85, feed the scores + weakest categories back through step 3 — and before round 2's copywriter pass, consult a persuasion-advisor layer if you run one (classic direct-response frameworks work well here: Eugene Schwartz's awareness/sophistication diagnosis for angle mismatches, Alex Hormozi's value equation for offer problems, and — in social mode — the NFX sharing motivations in [references/sharing-psychology.md](references/sharing-psychology.md) to diagnose why personas won't share). The panel says *what* missed; the advisor layer says *why* and *how to fix it*. Each round scores that round's 3 new variants, carrying the best prior variant forward as a comparison control. **Max 2 rewrite rounds.** After round 2, deliver the best variant with the engine's verdict as the ruling: **85+** ship; **75-84** offer it to the operator as a measured test against an existing control (their call); **65-74** stop — more wordsmithing is unlikely to close the gap, surface the weakest categories; **<65** report that the offer/angle itself (not the wording) is the problem and route the offer redesign through your advisor layer before any further copy work.
6. **Write the run log** to `focus-group/runs/YYYY-MM-DD-HH_MM-{slug}.md` — see template below. This is non-optional; run history is how the engine gets calibrated against real results.
7. **Report to the operator:** panel highlights (2-3 verbatim persona quotes), the BUY tally for offers and the SHARE tally for social mode (note which personas SHOULD say no — wrong-fit "no"s are a feature; for shares, report WHO each yes-persona would send it to), the 3 variants, scores, and the recommendation.

### Run log template

```markdown
---
type: focus-group-run
project: {business-slug}
date: YYYY-MM-DD
---
# Run: {slug}
**Content type:** ad | offer  **Rounds:** N
**Panel:** {responded} of {roster} personas — BUY {X yes / Y no} (offer mode) · SHARE {X yes / Y no} (social mode)
## Key feedback
- {persona}: "{verbatim}"
## Scores
| Variant | Rel /25 | Clar /20 | Emo /20 | Cred /15 | CTA /20 | Total | Verdict |
## Shipped
{Which variant shipped, where, and — filled in later — how it actually performed}
```

## Mode 2: SETUP — build a panel for a new business

Trigger: "focus-group setup {business}" or running against a business with no panel. Follow [references/setup-mode.md](references/setup-mode.md): research the business from your knowledge base + web, then draft ~8 dossiers using [references/persona-template.md](references/persona-template.md) (mix of struggling/successful, 1-2 deliberate wrong-fits), write the index note, and hand the panel to the operator for review — drafts are v1 until they've been sharpened with real customer knowledge.

## Rules (hard-won, from our first panel build)

1. **Personas > prompts.** A lazy "pretend to be a parent" gets garbage. 1,400-word dossiers get the accuracy Brooke reports.
2. **"Embody" beats "pretend you are"** in every agent prompt.
3. **Parallel over sequential** — the panel has no cross-dependencies.
4. **85+ before running unmonitored; 75-84 only as a measured test against a control.** Below 75 after two rounds = stop and be honest about why.
5. **Wrong-fit "no"s are signal, not failure.** Beginner offers should repel advanced personas and vice versa. Always report WHO said yes.
6. **Never skip the run log.** Prediction without calibration is astrology.
7. Proof/testimonials must match the audience segment (pro-athlete proof doesn't move a high-school parent).
