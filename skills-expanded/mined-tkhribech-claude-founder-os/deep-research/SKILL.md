---
name: deep-research
description: Use when the founder asks for a deep-research briefing ("deep research this", "give me a full read on X"), OR before any research-backed deliverable — a blog post, newsletter, landing-page claim, market read, or strategic bet — where multiple viewpoints and fact-checked claims matter. Runs a 4-phase pipeline — parallel expert lenses → contradiction map → synthesized briefing → adversarial peer review + primary-source verification of every citation. Overkill for a simple factual lookup.
---

# Deep Research — multi-lens, citation-verified briefings

Turns one topic into a verified, multi-perspective briefing. It simulates several expert lenses on the topic, maps where they contradict each other, synthesizes one report, then adversarially peer-reviews its own output and **verifies every citation against its primary source** before delivering. The verification phase is the whole reason this exists — "never assume, always verify" encoded as a pipeline.

Run the full pipeline end to end; do not shortcut a phase. This is deliberately heavier than a quick web lookup — reserve it for multi-angle or claim-heavy work, not for "what's the average price of X" (that's one search).

## Phase 0 — Scope the topic + build the panel

1. State your interpretation of the topic in one line and proceed (ask only if genuinely ambiguous in a way that changes the research).
2. **Build the panel from the business's stakeholders.** 4–5 lenses; the right set is: the demand side, the supply/operator side, the channel or market view, and ALWAYS a Skeptic. For Kiln & Co (the fictional pottery studio used throughout this repo) that's: **the Student** (who takes classes and worries about cost and skill progression), **the Studio Owner** (margins, kiln time, scheduling), **the Local-Market Analyst** (how nearby studios and hobby chains position and price), and **the Skeptic** (who thinks the obvious angle is overstated or could backfire). For broad-trend questions where business framing doesn't fit, use the classic research set: Practitioner, Academic, Skeptic, Economist, Historian.
3. Identify the reader's role so the actionable section can target it (default: the founder as decision-maker).
4. Tell the founder the pipeline is running — which panel, how many lenses — in one line.

## Phase 1 — Expert lenses (parallel agents)

Spawn all lens agents **in a single message** so they run concurrently. Each gets the same one-line topic frame plus its own lens persona, and this contract:

> You are THE {LENS} for: {TOPIC} ({TOPIC_FRAME}). Do real web research from the places this stakeholder actually reads. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE — 3–5 bullets, each with a concrete data point / quote / named source + URL. 3) THE ONE THING only this stakeholder would say. Cite real sources with URLs. Under 400 words.

Example, fully in-fiction: for the topic "should Kiln & Co add a kids' summer camp," the Student lens researches what hobby-class customers actually search and complain about; the Studio Owner lens researches operating economics of youth programs; the Local-Market lens researches how nearby art programs position and price camps; the Skeptic hunts for failed-program post-mortems and liability traps.

When all lenses return, post a 2–3 line note in chat: where they converge, and the sharpest disagreement. Keep the raw briefs out of chat.

## Phase 2 — Map the contradictions (inline, no agents)

Working only from the returned briefs: 1) **direct conflicts** — name the specific clashing claims; 2) **strongest vs weakest evidence** — rank by hierarchy (peer-reviewed causal > official/market data > operator anecdote > analogy), say why; 3) **the resolving question** — the single empirical question that would settle the biggest contradiction; 4) **universal agreement** — what every lens confirms, even opponents (the likely-true load-bearing finding); 5) **the blind spot** — what NO lens addressed (becomes the "missing lens" and the frontier question).

## Phase 3 — Synthesize the briefing

Write one self-contained report (markdown is fine; a styled HTML template if your workspace has one) containing, in order: **60-second summary** (settled fact first, then contested interpretation) · **key findings ranked by reliability**, each with a 1–10 confidence score and supported-by/challenged-by notes from the contradiction map · **the hidden connection** only visible across all lenses · **the missing lens** · **actionable moves** (3–6, concrete, targeted at the reader's role) · **claim-safety guide** (assert / caveat / avoid — filled after Phase 4) · **frontier question** · **references** with verification-status tags. Save to a dated file in the workspace's reports folder.

## Phase 4 — Adversarial peer review + verification (never skip)

This is what separates a deep-research briefing from a normal report.

**4a. Self-review (inline).** Score each finding 1–10 for reliability and justify. Name the weakest link and what would verify it. Bias check: which lens dominated the synthesis, what got underweighted.

**4b. Verify every citation (parallel agents).** One agent per citation cluster (~4–6 agents), each instructed:

> Independently verify a citation against its PRIMARY source. Be skeptical; do not trust secondary summaries. CLAIM: {claim + figure + named source}. Find the actual primary source; confirm or correct title/authors/venue/year/URL, the real figure as published, method and author-stated limits. For contested claims, find the strongest credible counter-source. Return VERDICT = CONFIRMED / PARTIALLY CONFIRMED (with corrections) / UNVERIFIED / FALSE, then the corrected one-line citation, then 2–4 specifics with the primary URL. Under 280 words.

**4c. Apply corrections.** Fix wrong figures and mischaracterizations; downgrade confidence where evidence was thin; re-attribute single-survey stats honestly; fill a truthful verification banner (`N/N checked, X fabricated, Y corrected, Z demoted`) and the claim-safety guide from the verdicts.

## Output

The report file path, the verification tally, the one universal finding, the frontier question, and the claim-safety summary (safe to assert vs. avoid) — tight, in chat. Anything the briefing clears for publication STILL passes the content gates before it ships.

## Guardrails

- **Real research only.** Every citation traces to a real, fetched source. A figure that can't be verified gets demoted or cut, never papered over.
- **The panel is author-built — disclose it in the report.** Convergence across lenses is a strong hypothesis, not field consensus.
- **A report without Phase 4 is not a deliverable of this skill.**
- Cost: ~9–11 agents per run is expected. Don't fan out wider than 5 lenses or one verifier per citation cluster.
