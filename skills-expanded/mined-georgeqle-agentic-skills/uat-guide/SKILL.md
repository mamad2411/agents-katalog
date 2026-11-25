---
name: uat-guide
description: Expand a UAT journey into click-by-click tester instructions, then update the result log on completion
type: analysis
version: v0.5
required_conventions: [alignment-page]
argument-hint: "[optional: journey number, journey name, or 'next']"
visual_tier: prototype
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, before the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# UAT Guide

Invoke as `$uat-guide`.

Expand a single UAT journey from `research/uat-plan.md` into detailed, step-by-step tester instructions. UAT planning (`$uat`) produces high-level task sequences ("sign up", "navigate to dashboard"); this skill turns each step into click-by-click, command-by-command, or request-by-request guidance that a tester unfamiliar with the product can follow without ambiguity.

Do not generate UAT journeys. If no UAT plan exists, stop and recommend `$uat` from the product-testing pack.

## Process

1. **Locate UAT plan**
   - Read `research/uat-plan.md`.
   - If the file does not exist, stop and tell the user: "No UAT plan found. Run `$uat` first to generate acceptance journeys."

2. **Select journey**
   - Parse all `### Journey N:` headings and their `#### UAT result log` status fields.
   - If `$ARGUMENTS` is non-empty, match by journey number or name (case-insensitive substring match).
   - If `$ARGUMENTS` is `next` or empty, pick the first journey whose status is `Not run`.
   - If all journeys have status `Pass`, `Fail`, or `Blocked`, tell the user all journeys are complete and offer to re-run a specific one.

3. **Gather project context**
   - Read `.agents/project.json`, `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `specs/`, `docs/`, and `tasks/` files when present.
   - Search the codebase for routes, UI components, CLI entry points, API endpoints, environment variables, configuration files, and navigation structure relevant to the selected journey's task sequence.

4. **Detect product interface type**
   - Classify the product surface the journey touches:
     - **Web app** -> click-by-click instructions (buttons, links, forms, pages).
     - **CLI** -> command-by-command instructions (exact commands, flags, expected output).
     - **API** -> request-by-request instructions (method, URL, headers, body, expected response).
     - **Hybrid** -> mixed instructions matching each step's surface.
   - Use the detected type to shape the instruction style for step 6.

5. **Research current instructions**
   - Use web search to find up-to-date documentation for any external services or platforms referenced in the journey (OAuth providers, third-party dashboards, payment processors, DNS registrars, etc.).
   - Prioritize official documentation over blog posts.
   - Service UIs change frequently -- never rely solely on prior knowledge; always search.
   - If current web research is unavailable in the active environment, state that limitation clearly and keep external-service steps scoped to what local project evidence proves.

6. **Expand task sequence**
   - For each step in the journey's task sequence, produce:
     - **Numbered sub-steps** with exact UI elements to click, commands to run, or requests to make. Use project-specific values (URLs, routes, field names, env vars) drawn from codebase context.
     - **Checkpoint** tied to the journey's acceptance criteria -- what the tester should observe to confirm the step succeeded.
     - **Evidence capture point** -- what to screenshot, copy, or record at this step.
     - **Gotchas** -- common mistakes, timing issues, or easy-to-miss details.
   - Begin the guide with a **Preparation** section drawn from the journey's Setup field (accounts, data, environment, permissions needed before starting).
   - End the guide with a **Final verification** section drawn from the journey's acceptance criteria and expected success state.

7. **Present guide**
   - Output the guide directly in the conversation. Do not write it to a file.

8. **Collect results**
   - After presenting the guide, tell the user: "When you've completed this journey, let me know the result (Pass / Fail / Blocked) and any notes, and I'll update the result log."
   - When the user reports completion:
     - Update the `#### UAT result log` section for this journey inline in `research/uat-plan.md` with the reported status, evidence, tester notes, and any follow-up tasks promoted.
     - Check off the corresponding item in `tasks/manual-todo.md`.
     - If the result is `Fail` or `Blocked`, suggest follow-up routing: `$debug` for reproducible failures, `$guide` for external blockers, `$user-flow-map` from the product-design pack when acceptance criteria are unclear because journey flow, states, or recovery paths are underspecified, `$ux-variations --layout-mode` when the unresolved issue is layout alternatives, or `$uat-guide next` for the next journey. Apply the Pack Availability Guard before recommending a skill from another pack.

## Output

```markdown
## UAT Guide: Journey N -- [Journey Name]

**Target user**: [persona or role]
**User goal**: [what the user is trying to accomplish]
**Product surface**: [Web app | CLI | API | Hybrid]

### Preparation

- [Account, data, environment, or permission setup needed before starting]
- [Pre-existing state or sample data to have ready]

### Steps

#### Step 1: [Task sequence step name]

1. [Exact action -- click, type, run, send]
2. [Next action with specific UI element / command / request detail]
3. ...

**Checkpoint**: [What the tester should see or verify]
**Evidence**: [What to capture -- screenshot, output, response]
**Gotchas**: [Common mistake or easy-to-miss detail, if any]

#### Step 2: [Task sequence step name]

1. ...

...

### Final Verification

- [ ] [Acceptance criterion from the journey]
- [ ] [Another acceptance criterion]
- [ ] Expected success state: [observable user-visible result]

### Non-Acceptance Signals

- [Confusion, delay, missing affordance, incorrect result, trust issue, or blocker to watch for]

### Tester Notes Prompt

> [Question from the journey that captures whether the target user would accept this]

---

When you've completed this journey, let me know the result (Pass / Fail / Blocked) and any notes, and I'll update the result log.
```

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/uat-guide-{topic}.html`.

## Constraints

- **Always web search** for external services and platforms referenced in the journey when the active environment permits web access. Service UIs change; stale steps are worse than none.
- **Project-specific values** -- never give generic placeholders when the codebase contains the actual values to use (URLs, routes, env vars, field names, commands).
- **Read-only except result log** -- this skill does not modify code. The only files it may edit are `research/uat-plan.md` (result log section) and `tasks/manual-todo.md` (to check off a completed item), and only after the user reports completion.
- **No shipping contract** -- updating a result log and checking off a manual-todo item is minor bookkeeping, not a code change. Do not auto-commit just for that. If other tracked changes are present, leave them for a proper shipping skill.
- **One journey at a time** -- guide the user through one journey per invocation. They can run `$uat-guide next` for the next one.
- **Don't execute the product** -- produce instructions for the user to follow. Do not start dev servers, launch browsers, call APIs, create accounts, or perform CLI workflows.
- **Don't mark complete unprompted** -- only update the result log after the user explicitly reports the outcome.
- **Don't invent acceptance criteria** -- use only the criteria defined in the UAT plan. If criteria are missing or unclear because flow, states, recovery, or handoff structure is underspecified, recommend `$user-flow-map` from the product-design pack; use `$ux-variations --layout-mode` only when the missing decision is layout alternatives.
- **Handle all product surface types** -- web apps get click-by-click, CLIs get command-by-command, APIs get request-by-request, hybrids get mixed. Detect from codebase context; don't assume web.
- **Prerequisite: UAT plan must exist** -- if `research/uat-plan.md` is missing, stop immediately and recommend `$uat` from the product-testing pack.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, prepend `npx skillpacks install <pack-name>` from the project shell, to the recommendation.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
