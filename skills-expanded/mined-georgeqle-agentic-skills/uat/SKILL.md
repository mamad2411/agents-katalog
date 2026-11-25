---
name: uat
description: Create user acceptance test journeys from a target user's perspective, with role-based scenarios, acceptance criteria, and evidence capture
type: analysis
version: v0.9
argument-hint: "[--variant-evaluation] [optional: persona, feature, release, journey, app, or variation spec]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# UAT

Invoke as `$uat`.

Create a user acceptance testing plan from the perspective of a potential or target user. Read the product surface, specs, journeys, stories, roadmap, and relevant research, then produces realistic end-to-end user journeys that validate whether the product satisfies user goals.

UAT is not dogfooding. Dogfood asks how the app owner can adopt the product into their own workflow to understand and evaluate it. UAT asks whether a target user can complete meaningful real-world journeys and would accept the product as fit for use.

This is a human-run acceptance plan, not automated testing. Do not start servers, drive browsers, call APIs, create accounts, or perform the scenarios yourself.

When invoked with `--variant-evaluation` (or when the user asks to test/review UI variants), create a hands-on evaluation plan for built UX/UI variants before `$consolidate-variations`. This mode helps the user try each variant in a comparable way and capture enough evidence to form a defensible consolidation opinion.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

1. **Resolve project context**
   - Read `.agents/project.json` if it exists.
   - Use `project_type` and `enabled_packs` when present.
   - If project metadata is missing, infer the project type from repo signals:
     - business-app: SaaS, marketplace, productivity, workflow, enterprise, or user-facing app
     - devtool: SDK, CLI, API, library, infrastructure, docs, examples, or package-first developer workflow
     - game: game engine files, playable prototypes, store assets, or game-specific README/spec language
     - generic: no strong domain signal
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `spec.md`, and `tasks/` files when present.

2. **Load user evidence**
   - Business app: read `research/icp.md`, `research/journey-map.md`, `research/customer-feedback.md`, `research/metrics.md`, and `research/mvp-gap.md` when present.
   - Devtool: read `research/devtool-user-map.md`, `research/devtool-dx-journey.md`, `research/devtool-integration-map.md`, docs, examples, and package manifests when present.
   - Game: read `research/game-audience.md`, `research/game-fantasy.md`, `research/game-core-loop.md`, `research/game-prototype-test.md`, and `research/game-playtest-metrics.md` when present.
   - Generic: use specs, README, routes, tests, examples, issue descriptions, and task acceptance criteria.
   - In product-path workspaces with `research/{slug}/` or `specs/{slug}/`, produce product-path-scoped UAT journeys for the requested app. If no app is specified and multiple apps are plausible, ask the user to choose.

2b. **Variant evaluation mode**
   - Trigger this branch when invoked with `--variant-evaluation`, when `specs/ui-layout-variations-*.md` exists for the requested topic, or when the user asks how to test/review built variants.
   - Read `specs/ui-layout-variations-[topic].md`, `specs/ux-variations-[topic].md`, `specs/ui-requirements-[topic].md`, built variant routes/components, and any existing `research/uat-variant-evaluation-[topic].md`.
   - Identify each variant, its intended thesis, implementation location, and the target user task it should support.
   - Create comparable journeys that make the user perform the same core task in every variant, then capture variant-specific strengths, friction, confidence, and rejection signals.
   - Include a side-by-side comparison matrix and a "Ready for `$consolidate-variations`?" checklist.
   - Human execution still belongs in `tasks/manual-todo.md`; this skill writes the plan and manual tasks, but does not run the variants.
   - After writing files, recommend `$consolidate-variations` only as the next step after the manual evaluation tasks are completed or when the user explicitly says they have already evaluated the variants.
   - Stop after this branch. Do not generate generic target-user acceptance journeys unless the user also requested them.

3. **Define acceptance perspective**
   - Identify 1-3 target user personas or roles from the evidence.
   - For each selected persona, define the job-to-be-done, context, goal, constraints, and acceptance threshold.
   - Prefer external target users, buyers, evaluators, administrators, developers, or players over the product owner unless the owner is also the target user.
   - If the target user is unclear, stop and recommend `$customer-discovery`, `$journey-map`, or the relevant pack research skill. For `$customer-discovery`, `$journey-map`, and other pack-based skills, apply the Pack Availability Guard — if the target skill's pack is not in `.agents/project.json` `enabled_packs`, recommend `$pack install <pack>` before the skill.

4. **Create UAT journeys**
   - Generate 3-7 journeys unless the user requested a narrower focus.
   - Cover at least one critical happy path, one realistic obstacle or recovery path, and one return-use or handoff path when supported by the product evidence.
   - Each journey must include:
     - target user
     - user goal
     - real-world trigger
     - setup and preconditions
     - end-to-end task sequence
     - expected user-visible success state
     - acceptance criteria
     - non-acceptance signals
     - evidence to capture
     - tester notes prompt
     - follow-up routing
   - Use concrete product language from specs and journeys. Avoid vague instructions such as "verify the feature works."

5. **Classify follow-up work**
   - Human-run UAT journeys go in `tasks/manual-todo.md` under `## UAT Journeys`.
   - Use `_(after: research/uat-plan.md)_` unless the journey blocks or follows a known roadmap step. If tied to a known step, use `_(blocks: Step N.X)_` or `_(after: Step N.X)_`.
   - Do not put human-run UAT journeys in `tasks/todo.md`.
   - Implementation or documentation fixes discovered after a completed UAT run belong in `tasks/todo.md`, but do not invent fixes before the user journey has been attempted.
   - One-time evidence collection belongs in `tasks/record-todo.md`.
   - Recurring release acceptance checks belong in `tasks/recurring-todo.md` only when there is a clear release cadence.
   - If a journey needs click-by-click help for a human-only external blocker, recommend `$guide`.

6. **Present findings before writing when risk is high**
   - If source material is thin, contradictory, or missing target-user evidence, summarize the gap and ask whether to proceed with assumptions.
   - If source material is sufficient, write the plan and task sections directly.

## Deliverables

- `research/uat-plan.md` - persona assumptions, journey matrix, source evidence, acceptance checklist, result log template, and follow-up guidance.
- In variant evaluation mode: `research/uat-variant-evaluation-[topic].md` - variant inventory, task script, comparison matrix, result logs, and consolidation readiness checklist.
- `tasks/manual-todo.md` - append or replace only the `## UAT Journeys` section.
- `tasks/recurring-todo.md` - optional, only when recurring UAT is useful and not already tracked.

If `tasks/manual-todo.md` does not exist, create it with a `# Manual Tasks - [Project Name]` title, a short note that these items require human-only action, and the UAT section. Preserve all non-UAT sections when updating an existing file.

Use this journey format in `research/uat-plan.md`:

```markdown
### Journey N: [Name]

- Target user: [persona or role]
- User goal: [what the user is trying to accomplish]
- Trigger: [real-world reason the user starts]
- Setup: [accounts, data, environment, permissions, or sample state needed]
- Task sequence:
  - [step the human tester performs as the target user]
- Expected success state: [observable user-visible result]
- Acceptance criteria:
  - [ ] [specific criterion]
- Non-acceptance signals: [confusion, delay, missing affordance, incorrect result, trust issue, or blocker]
- Evidence to capture: [screenshots, recordings, notes, timestamps, records, command output, or artifacts]
- Tester notes prompt: [question that captures whether the target user would accept this]
- Follow-up routing: [manual note, $customer-discovery, $journey-map, $guide, or task promotion guidance]

#### UAT result log

- Status: Not run | Pass | Fail | Blocked
- Evidence captured:
- Tester notes:
- Follow-up tasks promoted:
```

Use this variant evaluation format in `research/uat-variant-evaluation-[topic].md`:

```markdown
## Variant Evaluation Plan

### Variant Inventory

| Variant | Implementation location | Thesis | Primary task |
|---|---|---|---|

### Shared Evaluation Script

- Target user:
- Scenario:
- Setup:
- Core task sequence:
- Success criteria:
- Non-acceptance signals:
- Evidence to capture:

### Per-Variant Result Log

#### [Variant name]

- Status: Not run | Pass | Fail | Blocked
- Evidence captured:
- What worked:
- What felt wrong:
- Time/friction notes:
- Keep for consolidation:
- Reject for consolidation:
- Confidence: Low | Medium | High

### Side-by-Side Comparison Matrix

| Dimension | Variant A | Variant B | Variant C | Current preference | Evidence |
|---|---|---|---|---|---|

### Ready for `$consolidate-variations`?

- [ ] Every built variant has been tried or explicitly skipped.
- [ ] Evidence exists for each kept/rejected design element.
- [ ] Open blockers are documented.
- [ ] The user has enough confidence to converge.
```

Use this item format in `tasks/manual-todo.md`:

```markdown
## UAT Journeys

- [ ] Run UAT journey: [Journey name] as [target user] _(after: research/uat-plan.md)_ - capture evidence in `research/uat-plan.md`.
```

## Task Classification

- Human UAT journey execution goes in `tasks/manual-todo.md`.
- Variant evaluation tasks go in `tasks/manual-todo.md` under `## UAT Journeys` and should reference `research/uat-variant-evaluation-[topic].md`.
- Immediate implementation or documentation fixes confirmed by completed UAT go in `tasks/todo.md`.
- One-time condition-gated evidence collection goes in `tasks/record-todo.md`.
- Release-cadence UAT checks go in `tasks/recurring-todo.md`.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Do not run or operate the product in this skill.
- Do not start dev servers, launch browsers, use Playwright, call APIs, create accounts, or perform CLI workflows.
- Do not mark journeys complete; only a human tester can do that after performing them.
- Do not recommend `$consolidate-variations` before variant evaluation evidence exists, unless the user explicitly confirms they have already reviewed the variants and are ready to converge.
- Do not duplicate existing unchecked UAT or manual tasks. Reference existing items when they already cover the same journey.
- Prefer evidence-backed target-user journeys over exhaustive feature coverage.
- Keep dogfood and UAT separate: use `$dogfood` for owner/operator adoption into the builder's workflow; use `$uat` for target-user acceptance journeys.
- If no credible user journey, story, spec, or product surface can be found, stop and recommend `$customer-discovery`, `$journey-map`, or the relevant pack research skill. Apply the Pack Availability Guard for pack-based skills.

## Alignment Page

Build and attempt to open `alignment/uat-{topic}.html` before writing or replacing `research/uat-plan.md`, `research/uat-variant-evaluation-[topic].md`, or manual UAT tasks.

**Page layout contract.** After the page title and short summary, include a top-of-page "Table of Contents" section with anchor links to the major review sections and the bottom compile section. Keep the Table of Contents in normal document flow. Do not use a sidebar, side rail, drawer, split-shell layout, or sticky navigation for the Table of Contents unless the user explicitly asks for that layout. Do not place compile, copy, feedback, or answer controls in a sticky or fixed bottom banner/footer. Bottom compile controls must appear as ordinary content in a bottom compile section, so they scroll with the page and do not cover content at high zoom.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. Include evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and approval gates. Render target-user evidence, scenario inventory, acceptance criteria, evidence-capture prompts, manual task placement, variant comparison matrix when applicable, and every proposed deliverable section with no context loss from source evidence.

**Required inline questions.** Ask whether the evidence is sufficient for the UAT journeys, whether any assumptions or confidence levels are wrong, whether acceptance criteria and non-acceptance signals are acceptable, whether the proposed canonical file changes are approved, and whether any downstream route should remain blocked until manual testing is complete.

**Section feedback controls.** Add lightweight section-feedback controls to every major section of the page: emphasize, reject or flag a concern, and clarification needed. Selecting a control reveals a multi-line section-feedback textarea placed directly under or beside the emphasize/down/clarify controls. This textarea is separate from gate-question text inputs, so it still appears near the feedback controls even when the same section also has required gate questions with their own text boxes. These controls are optional for final approval and do not replace required gate questions. They also power the separate feedback-only YAML path so the user can send emphasis requests, concerns, or clarification requests before answering every required gate question.

**Feedback-only YAML contract.** Provide feedback-only YAML in two places: locally under each selected section-feedback textarea, and globally in the bottom compile section. When a section-feedback control is selected, show local "Compile Feedback YAML" and "Copy YAML" controls plus a read-only YAML textarea directly under that section's feedback textarea. The local feedback compile generates YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `feedback_status: revision-request`, `approval_status: not-approved`, `unanswered_required_questions`, and a `section_feedback` list containing the single selected section-feedback entry for that local control. The bottom "Compile Feedback YAML" control generates the same YAML shape but aggregates every selected section-feedback entry on the page. Enable both local and bottom feedback compile controls as soon as at least one section-feedback control is set, even if required inline gate questions are unanswered. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. Each feedback entry uses `section`, `feedback` (`emphasize`, `down`, or `needs-clarification`), optional `notes` from that section's feedback textarea, and `requested_agent_action` (`add-weight-to-section`, `investigate-and-revise`, or `clarify-before-approval`). For `emphasize` feedback, the YAML must tell the agent to add more weight, prominence, evidence, detail, or recommendation emphasis to that section or to the specific point named in the notes; this is a revision request, not approval of the section as-is. For `down` and `needs-clarification` feedback, the YAML must tell the agent to evaluate the feedback, investigate further when needed, and contextually amend the HTML alignment page before asking again for final approval answers. Copy and display feedback YAML locally or at the bottom with the same clipboard retry and textarea fallback behavior as final gate YAML. Do not render the bottom feedback compile controls as a sticky or fixed banner.

**Gate YAML contract.** At the bottom of the page, include an ordinary in-flow compile section with a "Compile Feedback YAML" button for selected section feedback and a separate "Compile Answers" button for final approval answers. The bottom compile section must not be sticky, fixed, floating, or styled as a persistent banner. The "Compile Answers" button compiles final approval answers into YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `approval_status: ready-for-agent-review`, `section`, `gate_type`, `status`, `decision`, `notes`, and `approved_file_changes` fields. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. The final approval button remains disabled until every required question has a selection. The final YAML may also include any section feedback the user set, using the feedback-only YAML `section_feedback` shape. The page must automatically attempt to copy the YAML to the clipboard, provide an explicit "Copy YAML" button, and fall back to selecting the textarea contents.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page. Ask the user to review the page and provide either local or bottom feedback-only YAML for emphasis requests, concerns, or clarification, or final compiled YAML answers when ready. Do not require the user to answer every gate before sending emphasis requests, negative feedback, or clarification needs. When feedback-only YAML is provided, treat it as a revision request: evaluate the feedback, investigate further when needed, archive and amend the HTML alignment page contextually, highlight the changes, and ask again for review. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML has been provided and the approved artifacts have been written or updated.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
