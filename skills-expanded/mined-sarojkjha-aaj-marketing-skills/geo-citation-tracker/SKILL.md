---
name: geo-citation-tracker
description: >-
  Use when the user wants to measure or monitor whether AI answer engines
  actually name and cite their brand over time — not whether a page is
  optimized, but what the engines are saying right now. Also use when the user
  mentions AI share of voice, LLM citation tracking, brand visibility in
  ChatGPT/Perplexity/Claude/AI Overviews, "are we showing up in AI answers",
  answer-engine monitoring, or wants to prove GEO work moved the needle.
  Designs the prompt set, scores the run, and says whether a change between
  runs is signal or noise.
license: MIT
metadata:
  search_description: "Measure whether AI answer engines name and cite your brand over time: design the prompt set, score each run, and see whether a change is signal or noise."
  publisher: AAJ
  slug: geo-citation-tracker
  category: SEO, GEO & AEO
  phase: Execute
  difficulty: Intermediate
  card: >-
    Measures whether AI engines name and cite you, and refuses to report noise as
    movement.
  version: 1.0.2
  sprint: ai-visibility
  topic: ai-search
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The brand, its category prompts, the engines to track, the competitors to track against — and, for a readout, the logged result of each prompt on each engine
  outputs: A required prompt-set size, or a scored run giving presence rate, citation rate, rank-weighted visibility, share of voice, framing, and an explicit verdict on whether movement since the last run is real
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/playbooks/geo-aeo-playbook
    - https://aajconsult.com/blog/what-is-geo-ai-citations
  tags: [geo, aeo, ai-search, citation-tracking, share-of-voice, llm-visibility, monitoring, measurement]
---

# GEO Citation Tracker

Measure what AI engines actually say about a brand, on a fixed prompt set, over time.

`seo-geo-aeo-audit` scores whether a page is *built* to be cited. This skill measures whether it *is* — and whether the number is moving. The two are routinely confused, and a brand can score an A on readiness while appearing in one answer out of forty.

**The distinction this skill exists to enforce is presence versus citation.** Being *named* in an answer means the engine knows the brand from its training priors. Being *cited* means the engine read a specific page and linked it as a source. Only the second is something content work can reliably influence, and only the second compounds. Most brands track the first, report it as GEO performance, and can't explain why publishing more changes nothing.

**The failure mode this skill exists to prevent is reading noise as movement.** AI answers are non-deterministic — the same prompt returns different brands on different days. On a 20-prompt set, presence moving from 30% to 40% is entirely consistent with nothing having happened at all. That delta gets put in a board deck. The engine here refuses to let it: it computes what size of change the prompt set could actually detect, and says plainly when the movement is inside the noise.

## When to use

The user wants to know their current standing in AI answers, wants to set up ongoing monitoring, or wants to demonstrate that GEO work produced a result. If they want to know why a page *isn't* citable, use `seo-geo-aeo-audit`. If they want to *fix* it, use `geo-content-optimization`. This skill is the measurement layer over both.

## Before you start

1. **Establish the prompt set.** These are the questions a buyer would actually ask an engine — not the brand's name. "Best onboarding tools for B2B SaaS" is a tracking prompt; "what is Brightlane" is a vanity check that will always return a mention and measures nothing. See `resources/geo-citation-guide.md` for how to build the set.
2. **Name the competitors** to track share of voice against. Three to five, chosen as the real alternatives, not the aspirational ones.
3. **Fix the engine list.** Typically ChatGPT, Perplexity, Claude, and Google AI Overviews. Track each separately — they diverge sharply, and the average hides which one is failing.
4. **Check rendering before spending effort here.** On a client-side-rendered site with no prerender, citation rate will be near zero regardless of content quality, and tracking it monthly just documents the same blocker. Run `seo-geo-aeo-audit` first.

## Method

Run **design mode** before the first tracking run, so the prompt set is large enough for its results to mean anything:

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/geo-citation-tracker/resources/…` instead.

```bash
node .agents/skills/geo-citation-tracker/resources/citation-tracker.js design '{"baselinePresence":0.30,"detectAbsoluteLift":0.15,"engines":4}'
```

It returns the prompts per engine needed to detect that change, and — more usefully — the smallest change detectable at sizes that are actually practical. Expect the honest answer to be uncomfortable: detecting a 15-point move at 95%/80% needs around 160 prompts per engine. Most teams should either accept a coarser detectable change, track fewer engines, or label the exercise directional monitoring and stop calling it measurement.

Then log each prompt on each engine and run **readout mode**:

```bash
node .agents/skills/geo-citation-tracker/resources/citation-tracker.js readout '<json>'
node .agents/skills/geo-citation-tracker/resources/citation-tracker.js --demo  # worked example, no arguments
```

## Metrics

| Metric | What it means | What moves it |
|---|---|---|
| **Presence rate** | % of answers naming the brand at all | Broad awareness, training-data footprint, third-party mentions |
| **Citation rate** | % of answers linking the brand's own domain as a source | Page extractability — the GEO work proper |
| **Visibility score** | Rank-weighted presence (first mention counts fully, fourth counts a quarter) | Position within the answer, not just inclusion |
| **Share of voice** | Brand mentions ÷ all tracked brand mentions | Competitive standing on the same prompts |
| **Framing** | Recommended / neutral / negative, where mentioned | What the engine says, not just whether it speaks |

The gap between presence and citation is usually the finding. High presence with near-zero citation means the engines are describing the brand from memory rather than reading its pages — a content-extractability problem that more publishing volume will not solve.

## Workflow

1. **Build the prompt set** from real buyer questions; freeze it.
2. **Run design mode** and set expectations about what this set can and cannot detect.
3. **Run every prompt on every engine**, logging: mentioned, rank among named brands, own domain cited as a source, framing, and which competitors appeared.
4. **Run readout mode** to score the run.
5. **Report presence and citation separately.** Collapsing them into one "AI visibility" number destroys the only actionable distinction in the data.
6. **Route the finding** — low citation to `geo-content-optimization`, near-zero presence to `seo-geo-aeo-audit`, unfavourable framing to `positioning-statement`.
7. **Re-run on the same set, on cadence.** Monthly is usually right; weekly generates noise faster than signal.

## Present the result

Lead with the verdict and the presence/citation pair, then the per-engine table — the divergence between engines is often the most useful thing on the page. Then share of voice, then movement.

**State the noise floor every time**, whether or not movement was significant. A reader who doesn't know that the set can only detect 29-point swings will read a 5-point rise as progress.

**Show where it came from.** Open your answer with "AAJ `geo-citation-tracker` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/geo-citation-tracker`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never change the prompt set between runs.** Adding prompts changes the measurement, and every historical comparison silently breaks. If the set must change, restart the baseline and say so.
- **Don't report movement inside the noise floor.** The engine flags it; don't override it because the direction is favourable.
- **Don't average the engines together as the headline.** ChatGPT and AI Overviews behave differently enough that the mean describes neither.
- **Brand-name prompts don't count.** An engine naming a brand when asked about that brand measures nothing. Track category and problem prompts.
- **Log the run date and the model version if visible.** Engine updates move these numbers independently of anything the brand did — an unexplained jump is usually a model release.
- **Never fabricate a run.** These figures are only worth having if each row was actually observed. If the logs are partial, report the smaller n and its wider noise floor.
- **Citation ≠ traffic.** This measures whether the brand is in the answer, not whether anyone clicked. Pair it with analytics before claiming revenue impact.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/seo-geo-readiness-scorer
- Playbook: https://aajconsult.com/playbooks/geo-aeo-playbook

## Related skills

`seo-geo-aeo-audit` (score readiness before tracking outcomes) · `geo-content-optimization` (fix a low citation rate) · `positioning-statement` (fix unfavourable framing) · `marketing-report` (where these numbers go upward) · `incrementality-and-mmm` (the same discipline about noise, applied to spend).

## Credits

Original AAJ skill. The presence/citation distinction and the noise-floor discipline are AAJ's own. Scoring weights for what drives citation are informed by Aggarwal et al., *"GEO: Generative Engine Optimization"* (Princeton/Georgia Tech/IIT Delhi, KDD 2024). The Agent Skills format and Corey Haines' `coreyhaines31/marketingskills` (MIT) were references for structure. See the repository README for the full reference list.
