---
name: annoying-customer-en
description: Let vision-capable AI act like demanding real customers—including technical users, non-technical customers, leaders, business stakeholders, and system operators—by experiencing a deployed product through browser screenshots, visible text, clicks, typing, scrolling, and waiting. Use before launch for synthetic-user research, exploratory UX testing, customer journey evaluation, first-use testing, role-based usability reviews, and evidence-backed product feedback when real users are scarce. Produce candidate problems and improvements; never treat simulated preferences as market validation.
---

# Annoying Customer — English

Operate the product as bounded synthetic users. Discover usability friction through visible UI behavior, then separate observations, reproduced defects, hypotheses, and recommendations.

## Preconditions

1. Identify the target URL, allowed environment, credentials source, and mutation boundary.
2. Prefer staging or seeded test data. Do not run destructive journeys in production without explicit authorization.
3. Confirm that a browser-capable tool is available. Use the product's real browser surface, not source-code inspection, as the Actor.
4. Read [references/role-catalog.md](references/role-catalog.md) when selecting roles.
5. Read [references/actor-policy.md](references/actor-policy.md) before running journeys.
6. Read [references/evaluator-policy.md](references/evaluator-policy.md) before judging results.

If no browser tool is available, stop before claiming a simulated-user run. Offer a scenario/persona design pass only.

## Workflow

### 1. Establish the study

Record:

- product and environment;
- study question;
- allowed and forbidden actions;
- starting state and reset method;
- core tasks;
- roles and run count;
- deterministic success evidence;
- privacy and credential constraints.

Use at least one role from each user group relevant to the product. Do not invent a role that has no plausible relationship to the product.

### 2. Prepare personas and scenarios

Start from the five role presets under `assets/personas/`, or copy [assets/persona.example.yaml](assets/persona.example.yaml) and [assets/scenario.example.yaml](assets/scenario.example.yaml). Validate them with:

```bash
python scripts/validate_config.py persona path/to/persona.yaml
python scripts/validate_config.py scenario path/to/scenario.yaml
```

Keep role, knowledge, goal, patience, risk tolerance, reading depth, exploration tendency, device, and action budget explicit. Give the Actor only the knowledge a real person in that role would possess.

### 3. Run the Actor

Create a fresh browser context per run unless the scenario explicitly tests returning-user state.

For every step:

1. Capture a screenshot and the visible/accessible page state.
2. Update the Actor state: current belief, confidence, frustration, trust, goal progress, and remaining budget.
3. Choose exactly one visible user action: click, type, select, scroll, navigate back, wait, refresh, or abandon.
4. Execute the action through the browser.
5. Record the action, reason, observed feedback, duration, and errors.

Do not use repository search, implementation knowledge, direct database queries, hidden APIs, DOM mutation, JavaScript injection, or developer-only tools to help the Actor navigate. Diagnostic evidence may be collected separately after the Actor run.

Allow realistic failure. Abandon when the persona's patience, time, or action budget is exhausted. Never force task completion to make a run look successful.

### 4. Apply realistic behavior

Translate persona traits into behavior:

- Low patience: wait once, retry once, then abandon or seek another visible path.
- Low reading depth: scan headings, labels, primary buttons, and the first visible paragraph.
- Low product knowledge: interpret terminology literally and permit plausible confusion.
- Low risk tolerance: hesitate or refuse when impact, scope, or rollback is unclear.
- High time pressure: prefer prominent shortcuts and summaries over exhaustive exploration.
- High technical skill: inspect visible detail and terminology, but still forbid code and hidden APIs.
- Low technical skill: prefer plain-language labels, onboarding, and recognizable navigation.

Do not add random mistakes merely for theater. Every mistake must follow from the persona, visible UI, or prior belief.

### 5. Evaluate independently

Keep the Actor's self-assessment separate from the Judge.

Judge in this order:

1. deterministic API/database/business-state evidence when authorized;
2. visible confirmation and resulting UI state;
3. trace consistency;
4. model-based UX judgment only for ambiguity, clarity, trust, and perceived effort.

Classify every finding as one of:

- `confirmed_bug`: reproduced functional or state defect with objective evidence;
- `high_confidence_friction`: repeated blockage across runs or roles;
- `ux_hypothesis`: plausible but not repeated or objectively verified;
- `preference`: subjective reaction, never a defect by itself;
- `test_artifact`: browser, model, seed-data, or harness failure.

### 6. Repeat and aggregate

Run each persona/scenario combination at least three times when cost permits. Do not promote a one-off model behavior into a high-confidence finding.

Store one JSON result per run using the shape in [references/result-schema.md](references/result-schema.md), then aggregate:

```bash
python scripts/aggregate_runs.py runs/*.json --output synthetic-user-report.md
```

Prioritize findings by reproducibility, affected roles, task impact, severity, recovery difficulty, and evidence quality. Avoid ranking by how strongly the Actor complained.

### 7. Report and hand off

Use [assets/report-template.md](assets/report-template.md). Include:

- environment and study limitations;
- role/task/run matrix;
- completion, abandonment, median steps, and median duration;
- repeated confusion and failure points;
- evidence links or artifact paths;
- confirmed bugs separated from UX hypotheses;
- smallest useful improvement for each high-confidence finding;
- risks and what still requires real-user validation.

Create Issues or modify the product only when explicitly authorized. Keep investigation, prioritization, and implementation as separate phases.

## Integrity Rules

- Never claim that synthetic users prove product-market fit, desirability, willingness to pay, or real-user preference.
- Never expose credentials, tokens, personal data, or sensitive screenshots in reports.
- Never let the Actor see the expected click path or success oracle.
- Never let the same model narrative be the sole Actor and sole Judge evidence.
- Never call an HTTP 200, service status, or model self-report a completed user journey.
- Mark blocked browser tooling, stale authentication, bad seed data, and environment outages as test artifacts until proven otherwise.

## Resources

- [references/role-catalog.md](references/role-catalog.md): default role families and behavioral distinctions.
- [references/actor-policy.md](references/actor-policy.md): browser-only simulation and state-transition rules.
- [references/evaluator-policy.md](references/evaluator-policy.md): evidence hierarchy and finding classification.
- [references/result-schema.md](references/result-schema.md): run artifact format.
- [assets/persona.example.yaml](assets/persona.example.yaml): persona template.
- `assets/personas/`: technical, non-technical, leader, business, and system-operator presets.
- [assets/scenario.example.yaml](assets/scenario.example.yaml): scenario template.
- [assets/report-template.md](assets/report-template.md): final report template.
- `scripts/validate_config.py`: deterministic persona/scenario validation.
- `scripts/aggregate_runs.py`: aggregate run JSON into a Markdown report.
