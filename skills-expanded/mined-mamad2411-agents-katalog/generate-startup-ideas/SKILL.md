---
name: generate-startup-ideas
description: Generate, refine, research, and validate startup ideas through an interactive founder-specific idea machine. Use when Codex needs to ask a few focused questions, search current public web signals, rapidly brainstorm startup or SaaS ideas, learn from love/maybe/no reactions, produce additional idea rounds, compare finalists, investigate competitors and existing workarounds, select a promising opportunity, or create an evidence-linked Markdown startup-idea report.
---

# Startup Idea Machine

Turn a blank prompt into a multi-round idea hunt. Ask three focused questions, search current public signals, generate concise idea bursts, learn from the founder's reactions, and validate only the finalists.

Respond in English even when the user's request is written in another language, unless the user explicitly requests a different output language.

## Load the right references

- Read [references/intake-and-rounds.md](references/intake-and-rounds.md) before starting or continuing an interactive hunt.
- Read [references/research-lenses.md](references/research-lenses.md) before searching the web or selecting source types.
- Read [references/evidence-rules.md](references/evidence-rules.md) before citing signals, competitors, spending, or timing.
- Read [references/idea-session-schema.md](references/idea-session-schema.md) before writing session, round, feedback, or validation JSON.
- Read [references/originality.md](references/originality.md) before generating a second round or checking diversity.
- Read [references/scoring.md](references/scoring.md) before ranking finalists.
- Read [references/report-schema.md](references/report-schema.md) before producing the final report.

## Core workflow

### 1. Start with three questions

For an open-ended request, ask the following three questions together and wait:

1. What are you unusually good at, curious about, or experienced in?
2. What customers, markets, or business styles attract you, and what should be avoided?
3. What constraints matter: time, budget, technical ability, team, geography, and ambition?

Keep the questions easy to answer. Let the user say "surprise me" or "no preference." If the user already supplied an answer, do not ask for it again. Ask at most one compact follow-up only when a missing constraint would materially change the hunt.

### 2. Create the idea session

Save the normalized answers as JSON in the workspace `outputs/` directory. Run:

```bash
node <skill-dir>/scripts/create_session.mjs <intake.json> <startup-idea-session.json>
```

Keep using the same session file throughout the hunt. Do not discard rejected ideas; they teach the machine what to avoid.

### 3. Run a fast public-signal scan

Browse the current public web after receiving the answers. Use at least four query angles and at least three source types from [references/research-lenses.md](references/research-lenses.md).

Collect enough evidence to inspire and constrain the first burst without turning the opening into a long market report. Prefer original sources and capture URLs, dates when visible, actors, workflows, workarounds, and spending proxies.

### 4. Fire the first idea burst

Generate 12 distinct ideas. Keep each idea compact enough to scan quickly.

For every idea include:

- **Name**
- **Customer**
- **Pain**
- **Product**
- **Signal** — one source-backed reason or a clearly labeled hypothesis
- **Why you** — connection to the founder's answers

Cover multiple idea shapes and business models. At least eight ideas must connect to recorded public signals. Label the remaining ideas "exploratory" rather than fabricating evidence.

Do not create a large scoring table in the first burst. End by asking the user to react using:

```text
Love: [numbers]
Maybe: [numbers]
No: [numbers]
```

Save the round JSON and run `append_round.mjs`.

### 5. Learn from reactions

Record the user's reactions with `record_feedback.mjs`. Extract positive and negative patterns from idea tags, customers, business models, and reasons.

Do not interpret rejection as proof that an opportunity is bad. It only indicates founder preference. Preserve an explicit distinction between market evidence and personal taste.

### 6. Fire the refinement burst

Generate eight new ideas:

- four direct descendants of loved ideas;
- two adjacent ideas that preserve the attractive mechanism but change the customer or market;
- two wildcards that challenge the emerging pattern without repeating rejected traits.

Do not rename old ideas and present them as new. Use the originality checks in [references/originality.md](references/originality.md). Keep the cards concise and ask the user to select one to three finalists.

Repeat the feedback and refinement loop when the user wants more ideas. A session can contain any number of rounds.

### 7. Validate the finalists

For each selected finalist, research:

- repeated problem evidence;
- current workaround and switching friction;
- spending, hiring, or purchase proxies;
- direct and adjacent competitors;
- underserved wedge;
- reachable first customers;
- why now;
- fatal assumption;
- disconfirming evidence;
- smallest useful MVP;
- a seven-day validation test.

Use current sources and original pages. Do not claim market size, willingness to pay, customer interest, or competitive absence without evidence.

### 8. Score and select

Score finalists using [references/scoring.md](references/scoring.md). Show criterion-level scores and the reason behind each score.

The highest score is not automatically the winner. Choose the winner by balancing evidence, founder fit, reachability, buildability, and fatal risk. It is acceptable to conclude that none should be built yet.

Save the validation JSON and run `complete_session.mjs`.

### 9. Create the native Codex report

Run:

```bash
node <skill-dir>/scripts/generate_report.mjs <startup-idea-session.json> <startup-idea-machine-report.md>
```

Save the report in the workspace `outputs/` directory. Verify that source links, reaction history, scores, risks, unknowns, and the seven-day plan render correctly.

Return clickable links to both the Markdown report and session JSON.

## Hunt modes

- **open-web**: Search across markets and idea shapes. Default when no niche is supplied.
- **niche**: Stay within one industry, audience, or workflow.
- **boring-business**: Prioritize recurring operational work, legacy tools, and clear budgets.
- **manual-work**: Look for spreadsheets, copy-paste work, assistants, agencies, and repeated services.
- **unbundle**: Look for valuable pieces of expensive or bloated software.
- **new-tech**: Combine newly available technology with an old, expensive workflow.
- **github-demand**: Prioritize feature requests, issues, scripts, and open-source commercialization gaps.
- **local-opportunity**: Prioritize location-bound businesses and workflows.

Use `open-web` by default. The user can mix modes.

## Bundled scripts

- `create_session.mjs` — normalize founder answers and initialize session state.
- `append_round.mjs` — validate and append a source-backed idea round.
- `record_feedback.mjs` — persist love/maybe/no reactions and derive taste signals.
- `complete_session.mjs` — attach finalist research, scoring, winner, and validation plan.
- `generate_report.mjs` — render the session as native Markdown.

## Quality rules

- Start ideating after the questions; do not bury the user in methodology.
- Prefer concrete customers and workflows over broad categories.
- Keep the first two rounds varied and fast.
- Link material validation claims to sources.
- Separate observed evidence, inference, and speculation.
- Search for counterevidence before recommending a winner.
- Never present generated people, quotes, revenue, market size, or customer interest as factual.
- Do not bypass logins, paywalls, access controls, rate limits, or private communities.
- Do not use leaked, private, or sensitive personal data.
- Never contact prospects, submit forms, or publish anything without separate user authorization.

## Default output

`Three Questions → 12-Idea Burst → Founder Reactions → 8-Idea Refinement → 1–3 Validated Finalists → Winner or No-Go → Native Markdown Report`

