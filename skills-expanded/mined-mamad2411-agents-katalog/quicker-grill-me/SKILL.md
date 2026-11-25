---
name: quicker-grill-me
description: Stress-test a software design or proposal with a short, material-decision questionnaire, then produce a reconciled design and decision ledger. Use before implementing a feature, system, migration, or other consequential technical change.
compatibility: Requires Node.js 20+ and a local browser for the bundled UI; includes a chat fallback.
---

# QuickerGrillMe

Turn an incomplete proposal into shared design understanding without exhaustive interrogation. Ask only when plausible answers materially change behavior, architecture, cost, risk, or scope.

## Operating workflow

### 1. Establish factual context

Read the user's proposal first, then inspect only the code, configuration, and documentation needed to resolve facts that could change a material question. Prefer high-signal entry points and batch independent lookups when the host supports it. Stop exploring once the material decision boundaries are clear. Do not ask the user for file contents, framework versions, existing conventions, or other facts available through the host's tools.

Separate:

- **Facts** established from the proposal or environment.
- **Material decisions** that require user intent.
- **Defaults** the Agent can choose safely.
- **Unknowns** that need later evidence rather than preference.

Do not begin implementing the resulting design during this skill. The final step is explicit confirmation of shared understanding.

### 2. Select only material questions

For every candidate question, apply the counterfactual materiality test:

1. Identify at least two realistic answers.
2. State the concrete design delta caused by each answer.
3. Reject the question if the delta is merely wording, personal preference, or a cheap reversible detail.
4. Keep it only if answers change a boundary, hard-to-reverse architecture, core behavior, interface, failure mode, security posture, operating cost, scope, or material delivery risk.
5. When a reasonable default is safe, reversible, and cheap to validate, choose it and put it in the default ledger instead of asking.

Choose a depth and enforce its hard cap:

| Depth | Target | Hard cap |
| --- | --- | --- |
| Essential | 5-7 | 7 |
| Standard | 10-15 | 15 |
| Deep | 20-25 | 25 |

Standard is the default. Use Essential for narrow or low-risk work. Use Deep only for high-risk, cross-system, security-sensitive, or hard-to-reverse designs. Do not add filler to reach a target.

### 3. Generate questionnaire JSON

Create a working-artifact directory in the user's project or host temp area, never inside the installed skill. Start from `assets/questionnaire.template.json` and conform to `references/questionnaire.schema.json`.

Each question must include:

- dependency and stage metadata;
- impact and complexity;
- realistic options;
- one preselected recommendation with rationale and confidence;
- explicit defer behavior with a temporary default, confidence, and observable validation trigger;
- affected design decisions.

Order prerequisites before dependents. Prefer high-impact unresolved decisions. Use conditional visibility when a downstream decision is relevant only for a particular upstream answer.

Resolve `SKILL_DIR` as the absolute directory containing this `SKILL.md`; do not assume the current working directory or a particular installer location. Quote every path because installed paths may contain spaces.

Do not launch a separate validation process before serving. The `serve` command performs the same strict questionnaire validation before binding a port. If it reports validation issues, fix every issue and rerun it; do not weaken or bypass validation.

### 4. Run the bundled local questionnaire

Start the browser runtime in a terminal/background process that can remain alive while the user answers:

```text
node "<SKILL_DIR>/scripts/runtime/cli.js" serve "<questionnaire-path>" --output "<answers-path>" --round 1
```

The runtime chooses a loopback port, opens the browser, persists the answer artifact atomically, and exits after successful submission. It also exits when the user closes the questionnaire page; a page refresh reconnects during a short grace period instead of cancelling the questionnaire. It uses only bundled JavaScript and browser assets; do not run `npm install`, `npm run build`, or code from the source tree.

Tell the user briefly that the questionnaire opened and wait for submission. If automatic opening fails, provide the printed `http://127.0.0.1:<port>` URL. If the process reports that the questionnaire closed before submission, stop this skill immediately, tell the user the questionnaire was cancelled, and do not wait, reopen it, or look for an answer artifact. Otherwise, after the process exits, read and validate the resulting answers artifact against `references/answers.schema.json`. Reconcile the answers with the factual context; do not merely restate questionnaire labels.

If a browser cannot be used, present the ordered questions in the host UI or chat. Preserve recommendations, depth caps, dependency/visibility rules, defer metadata, changed-answer review, and the answer contract. Ask primarily for changes from recommendations.

### 5. Decide whether round two is warranted

Do not create a second round merely because the user changed recommendations. Round two is allowed only when round-one answers reveal:

1. answers that cannot both be satisfied;
2. an answer that invalidates a key premise used to generate round one; or
3. an unresolved high-risk unknown whose plausible outcomes require materially different designs.

When triggered, generate exactly one final questionnaire with 3-5 material follow-ups, use a distinct questionnaire and answer path, and run:

```text
node "<SKILL_DIR>/scripts/runtime/cli.js" serve "<round-2-questionnaire-path>" --output "<round-2-answers-path>" --round 2
```

Never exceed two rounds. Prefer a temporary default and validation plan when another question would not resolve the uncertainty.

### 6. Produce the final design

Stop questioning when every high-impact decision is answered or has an explicit temporary default, remaining unknowns are reversible or have validation plans, no contradiction remains, and round two is complete or was not triggered.

Produce one coherent design containing:

1. goals, scope, and non-goals;
2. architecture, interfaces, data flow, and core behavior;
3. failure handling, security, operations, rollout, and validation strategy as applicable;
4. a decision summary with selected options and material consequences;
5. **Defaults and assumptions** containing only defaults that materially affect behavior, cost, or risk;
6. **Deferred validation items**, each with temporary default, confidence, owner if known, and trigger;
7. a **Default ledger appendix** containing every chosen default, including reversible low-impact choices.

Call out unresolved risk plainly. Keep the design proportionate to the proposal; this workflow is not a new framework, approval system, or hosted service.

Persist that complete design as `final-design.md` in the working-artifact directory; this is the canonical plan Markdown for subsequent edits and implementation, so do not leave the only copy in chat. Then generate a self-contained, read-only review page containing both the final design and the complete questionnaire decision record:

```text
node "<SKILL_DIR>/scripts/runtime/cli.js" render-review "<questionnaire-path>" "<answers-path>" "<final-design.md-path>" --output "<design-review.html-path>"
```

The HTML makes no external requests and is ready to upload to a static host. It does not implement authentication. Because the intended access is organization members or invited reviewers, publish it only through a host that enforces those permissions. If no approved host or publisher integration is available, provide the local `file://` URL printed as `Final HTML` and do not upload it to a public service. The command also prints the canonical plan document as `Plan Markdown`.

After the questionnaire submission has been reconciled and the review page has been generated, the Agent's final response must include both exact clickable URLs emitted by `render-review`:

- `Final HTML`: the read-only review page.
- `Plan Markdown`: the editable source of truth for later design changes or implementation.

Also state the plan file name and explain that the user can start a later task by asking the Agent to modify or implement from that Markdown file. Then ask the user to confirm that the design captures the shared understanding. Do not finish with only an answer JSON path, and do not implement until that confirmation is received.
