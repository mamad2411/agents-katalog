---
name: productize-dogfood
description: >-
  Browser-driven exploratory QA for web apps. Use when a local app, staging URL, or production
  URL needs real-user dogfooding with sitemap coverage, flows, console checks, screenshots,
  issue severity, blockers, and release evidence.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Dogfood

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `dogfood`
- **Lifecycle**: Launch & Learn
- **Category**: Delivery
- **Primary artifact**: Dogfood QA report with pages tested, flows tested, console errors, screenshots, severity table, blockers, and release decision

Dogfood is a routed QA skill for testing a web product like a real user. It is
not a fourth Productize playbook and not a replacement for the QA gate. QA calls
Dogfood when the target is a web UI and browser evidence is needed.

Use this skill for local apps, staging URLs, production smoke checks, release
candidates with a web UI, and "test this URL end-to-end" requests.

## Inputs

Capture these before testing:

- **Target**: URL, localhost route, deployed app, or app launch command.
- **Scope**: full site, changed flows, smoke test, regression pass, or named features.
- **Mode**: quick, standard, exhaustive, regression, or report-only.
- **Access**: credentials, seed data, feature flags, device/viewport requirements, and any unsafe actions to avoid.
- **Output directory**: default to `dogfood-output` when the host can save screenshots and a report.

If authentication, a running server, seed data, or browser tooling is missing,
state the blocker and run the safest fallback coverage instead of inventing
results.

## Tool Posture

Use the host's browser tooling when available. Prefer tools that can:

- navigate to URLs and local web apps
- inspect DOM or accessibility snapshots
- click, type, scroll, go back, and use keyboard navigation
- read browser console messages, JavaScript errors, and failed network requests
- capture screenshots or vision snapshots, with annotations when useful

Check the console after every navigation and every significant interaction.
Silent JavaScript errors on core pages are reportable findings even when the UI
appears to work.

## Workflow

### Phase 1: Plan

1. Create the output structure when file writes are appropriate:

   ```text
   dogfood-output/
   screenshots/
   report.md
   ```

2. Define the scope, test mode, assumptions, excluded surfaces, and known blockers.
3. Build a rough sitemap from visible navigation, route files, links, or app docs.
4. Identify primary user flows, including first-run, happy path, invalid input,
   interrupted flow, empty state, and recovery paths.

### Phase 2: Explore Pages

For each page in scope:

1. Navigate to the page.
2. Record URL, page purpose, visible state, and whether it loaded successfully.
3. Capture a screenshot or visual evidence.
4. Inspect DOM/accessibility text for missing labels, broken content, or hidden state.
5. Check browser console output and failed requests.
6. Scroll through the page and repeat visual/console checks when new content loads.

### Phase 3: Exercise Flows

Test the product like the intended user:

- navigation between key routes
- signup, login, onboarding, dashboard, search, checkout, import/export, or other core flows
- valid and invalid form submissions
- empty submissions, duplicate submissions, rapid clicks, cancellation, and back navigation
- loading, error, empty, and permission states
- mobile or narrow viewport when the UI is responsive
- keyboard navigation, focus visibility, labels, and basic contrast/accessibility cues

After each significant interaction, record expected behavior, actual behavior,
console output, and screenshot evidence when something changes or fails.

### Phase 4: Classify Issues

For every issue, capture:

- severity: P0, P1, P2, or P3
- category: functional, visual, accessibility, console, UX, content, performance, or data
- affected URL/page
- repro steps
- expected behavior
- actual behavior
- console errors or failed requests
- screenshot/evidence path
- likely owner/gate
- release impact and retest instruction

Use `references/issue-taxonomy.md` for severity and category definitions.
De-duplicate issues before final reporting.

### Phase 5: Report

Use `templates/dogfood-report-template.md` unless the user asked for another
format. The report must be evidence-first and include:

1. **Quality Scope**: target, mode, assumptions, and exclusions.
2. **Pages Tested**: URLs/pages visited and page-level results.
3. **Flows Tested**: user flows exercised, expected behavior, actual behavior, and result.
4. **Console Errors**: console messages, JavaScript errors, failed requests, or an explicit "none observed" with caveats.
5. **Screenshots/Evidence**: screenshots, traces, logs, DOM snapshots, command output, and paths.
6. **Severity Table**: counts by severity and category, sorted by release impact.
7. **Issues**: reproducible findings with owner, release impact, and retest steps.
8. **Blockers**: anything that prevented coverage or blocks release.
9. **Decision**: pass, conditional pass, retest, block, or escalate.
10. **Next Gate**: QA, release, docs, design, eng, operate, or product review.

Do not report vague findings without repro steps and evidence. Do not claim a
surface was tested unless you navigated or inspected it in the current run.

## Route Internally

- `$qa` when the dogfood report needs broader acceptance, regression, or release-risk judgment.
- `$test-scenarios` when the team needs a reusable scenario matrix before dogfooding.
- `$acceptance-criteria-for-ui` when the UI expectations are ambiguous.
- `$accessibility-review` when accessibility defects need deeper review.
- `$systematic-debugging` when a confirmed issue needs root-cause analysis and a fix loop.
- `$release` when the dogfood result is release evidence.
- `$operate` when the result is a production smoke check or live-product health signal.

## Required Output

Return:

1. **Quality Scope**: target, mode, assumptions, excluded surfaces, and blockers.
2. **Pages Tested**: each page/URL, evidence, console status, and result.
3. **Flows Tested**: each flow, expected behavior, actual behavior, evidence, and result.
4. **Console Errors**: errors/warnings/failed requests, or explicit none observed with caveats.
5. **Screenshots/Evidence**: screenshot paths, traces, logs, snapshots, and command outputs.
6. **Severity Table**: issue counts by severity and category.
7. **Issues**: severity, category, repro, expected, actual, evidence, owner, release impact, and retest step.
8. **Blockers**: missing access, missing data, unavailable tools, unsafe actions, or release blockers.
9. **Decision**: pass, conditional pass, retest, block, or escalate.
10. **Next Gate**: the next Productize gate or routed skill and why.
