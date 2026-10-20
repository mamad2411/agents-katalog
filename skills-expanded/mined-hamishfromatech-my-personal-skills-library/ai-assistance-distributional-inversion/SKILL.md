---
name: ai-assistance-distributional-inversion
description: Applies the first field-experimental evidence on AI tax assistance (Holz, Perez-Truglia, Simon & Zentner, NBER WP 35632, Aug 2026; 645 Dallas County households, preregistered RCT, Claude-powered chatbot on a property-tax-appeal website) — where an AI chatbot raised direct appeal filing by 9.1pp (41.4%→50.5%) with high 78% take-up, yet effects were smaller for less-advantaged households, inverting the established AI-literature pattern of AI disproportionately benefiting the disadvantaged — as the design framework for AI assistance programs and the distributional-audit rule for any AI-powered guidance product. Use when [evaluating whether an AI assistant narrows or widens user disparities, designing AI help for complex paperwork or financial decisions, auditing take-up vs outcome gaps in AI-assisted workflows, or advising on government/enterprise AI-assistance rollouts]. NOT for [productivity effects of AI on workers, nudge disclosure mechanics, or chatbot UX patterns].
---

# AI Assistance Widens Gaps (Sometimes): The Distributional Inversion

**Source:** Holz, Perez-Truglia, Simon & Zentner, "Taxpayer Behavior in the Age of AI: A Field Experiment on Property Tax Appeals," NBER Working Paper 35632, Aug 2026 (preregistered AEARCTR-0018430; University of Michigan IRB; replication code/data promised on publication). Setting: property-tax appeals in Dallas County, Texas — a setting with documented inequality (2025 appeal rates: 41.7% top-quartile-value homes vs 9.9% bottom-quartile).

## The Experiment

45,200 households received postcards inviting them to a research website with personalized property info, filing instructions, and a Comparable Properties Report. 645 visitors form the analysis sample. Half were randomly assigned a version with an **AI chatbot (Claude)** answering questions with property-specific guidance; a secondary randomization split it into **TaxBot** (machine-like name, factual tone) vs **Marina** (human name, warm tone).

**Results:**
- **Take-up was high:** 78% of chatbot-assigned households initiated a conversation (mean 5.2 messages); time-on-site rose 12.1 → 17.3 minutes.
- **Behavior changed:** direct-appeal filing rose **9.1pp (41.4% → 50.5%; p=0.021; adjusted 10.5pp, p=0.006)**; event-study falsification across 2021–2025 shows no pre-trend. No crowd-out of human agents (−0.2pp, ns).
- **Magnitude benchmark:** equivalent to a ~$425 increase in expected tax savings (per Nathan et al. 2025's 2.14pp per $100), and nearly 2× the 4.98pp effect of a mailed step-by-step guide + tailored argument — delivered on top of a control site that already included substantial assistance.
- **Mechanism:** transcripts show households using the chatbot to *exercise judgment* — 91.5% asked whether to file, 50.8% which comparables best support the case, 44.6% what opinion-of-value to report; the bot recommended filing with rationale in 98.1% of conversations. It also *reshaped* feature use: evidence-document creation (PDF Creator) jumped 7% → 18.4% while Comparable-Report downloads fell 76% → 54%.
- **Persona (secondary):** TaxBot slightly beat Marina on take-up (82.1% vs 74.0%, p≈0.07) — machine-like presentation marginally outperformed the friendly persona; filing differences were not significant.

## The Inversion (the headline mechanism)

In the existing AI literature, AI tools disproportionately benefit **less-skilled, less-experienced, less-educated** workers (Noy & Zhang; Brynjolfsson; Cui et al.). Here the opposite: **effects on filing were smaller among less-advantaged households** — no-bachelor's +5.8pp vs bachelor's +25.0pp (marginally significant difference, p=0.069); lower-value homes +5.5pp vs +13.5pp; minority +7.2pp vs +14.8pp (imprecise but consistent across all three splits). Crucially, **take-up gaps were much smaller than outcome gaps** — the divergence arises *after* take-up, in how effectively households translate guidance into action. Universal access may **widen** rather than narrow existing disparities.

**Plausible mechanisms (authors' reading):** differences in how households use the chatbot and act on it — less-advantaged households extract less value from conversational judgment-support, not less access. Context: 40% of self-filing Texas homeowners already used AI tools (ChatGPT et al.) for appeals — meaning outside AI use may attenuate the measured effect and the real access gap is partly *quality of use*.

## Design Rules

1. **Audit the outcome distribution, not just the average.** Pre-register subgroup analysis on the dimensions your service is meant to equalize (education, wealth, language, prior experience). An AI feature can pass a positive-average review while widening gaps.
2. **Measure take-up AND conversion-to-action separately.** High take-up with flat downstream action for a subgroup = a usage-quality problem (prompting skill, confidence, follow-through), not an access problem — and requires a different fix (structured guidance, human support pairing) than outreach.
3. **Pair universal AI access with scaffolding for the least-advantaged slice** — guided flows, document templates, optional human review — rather than assuming conversational fluency is universal.
4. **For government/enterprise assistance programs:** AI guidance is cheap at the margin (the authors argue tax agencies should consider offering it free) — but the equity assessment must ship with the rollout.
5. **Expect the inversion in "judgment-heavy, consequence-heavy" domains** (tax, legal, benefits, investing): where the task requires translating information into an assertive action, conversational AI benefits the already-confident more. The productivity-literature inversion does not automatically transfer.

## Honest Caveats

- Working paper; single county; sample overrepresents appeal-prone households (22.6% of visitors had filed the prior year vs 10.5% of recipients); subgroup effects are large in magnitude but imprecisely estimated (only the education split is marginally significant); "less-advantaged" proxies via education/home value/BISG-imputed race on the primary owner.
- The chatbot was Claude with a suggested opinion-of-value guardrail — behavior may differ with other models or without anchoring.

## A-Tech Alignment

- **Financial freedom:** the sharp version of the AI-and-wealth question — AI assistance raises everyone's filing (everyone got richer from savings) but raises the advantaged *more*; any A-Tech "AI for financial freedom" content must carry this caveat.
- **Practical:** the take-up-vs-outcome gap table is directly reusable for product analytics and program design.
- **Open source:** replicable preregistered design; the website/chatbot pattern is buildable on open models.
- **Privacy:** conversation transcripts of financial questions are sensitive — flag retention/governance for any similar deployment.

## Related Skills

- `agentic-coding-returns-to-expertise` — the productivity-side moderation literature this inverts (domain expertise helps; here advantage compounds).
- `digital-addiction-economics-2026` — revealed-WTP and behavior-change economics family.
- `kiyosaki-ai-wealth-transfer` — the wealth-transfer frame this study complicates.
- `belief-profile-targeting-rct` — friction diagnosis before choosing the intervention.