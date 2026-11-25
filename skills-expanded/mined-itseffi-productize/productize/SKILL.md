---
name: productize
description: >-
  Productize root skill for building, shipping, operating, and growing AI products inside a
  coding harness. Routes work across thesis framing, discovery, research, positioning,
  finance, decision making, requirements, design, metrics, AI-builder execution, code
  implementation, verification, stakeholder narratives, growth, launch, operation, and
  learning workflows. Use when the user wants to build a product from zero, improve an
  existing product, or needs product work that spans multiple lifecycle stages before code,
  launch, operation, or growth execution.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Productize

Productize is the root routing skill for the Productize system. It helps a coding
harness decide which playbook, gate, or routed skill owns the current product job,
produce the product artifacts, convert them into agent-ready implementation work,
write or modify code through the host agent, verify the result, and set up the next
learning loop.

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

- **Skill**: `productize`
- **Lifecycle**: Think
- **Category**: Operations
- **Primary artifact**: Routed Productize workflow

## Access Surface

Use the smallest entry point that owns the cadence:

**Playbooks**

- `/productize build <request>`: main operator entry point. Inspect project
  knowledge and workflow artifacts, choose the next lifecycle route, and return
  a concrete route plan with approval/edit options. Tactical skills are internal
  implementation details behind this route.
- `/productize adopt`: existing repository onboarding. Run `productize onboard existing`, review generated `.productize/project/` coverage, then recommend the next workflow route. Use `productize init existing` only for an intentional knowledge-only refresh without setup or workspace registration.
  - Select one agent target by default. Use repeated `--agent <name>` flags only when the user explicitly requests multiple targets, and reserve `--all-agents` for an explicit all-target install.
  - If targeted setup reports an older Productize-managed target, preview `productize setup cleanup --keep-agent <name> --dry-run` and request approval before applying it. Cleanup must preserve drifted, unknown, and user-owned files.
- `/productize-0-1`: new bet or new capability; closes at ship gate, pivot, pause, or kill.
- `/productize-operate`: production deploy; continuous operating loop that does not close.
- `/productize-grow`: stable product with activation evidence; closes when the growth target is hit or the strategy pivots.

**Gates**

- `thesis-review`
- `product-review`
- `design-review`
- `eng-review`
- `qa`
- `release`
- `docs`
- `dx-review`
- `comms-review`

**Meta-runner**

- `/productize-autoplan`: detects the current gate and runs the relevant gates.

**Routed Skills**

- 239 Productize routed skills called internally by the three playbooks and nine gates.

## Routing Map

| User intent | Route | Signals |
|---|---|---|
| I have an idea | Think | thesis framing, opportunity, wedge |
| I want to build a feature or change | Operator Build Route | `/productize build`, build, implement, add, improve, ship |
| I need to use Productize on an existing repo | Adopt Existing Project | adopt, existing project, mature repo, repo context, project memory |
| I need positioning/growth | Strategize / Growth | positioning, brand, PMF, AARRR, CAC/LTV |
| I need a PRD/spec | Plan / Build With AI | PRDs, requirements, technical handoff, implementation plan |
| I need research | Discover | JTBD, interviews, assumptions, ICP, insight synthesis |
| I need metrics/PMF | Measure | PMF, dashboards, funnels, experiments, churn |
| I need valuation/deal pricing | Finance | DCF, WACC, CAPM, EV/equity bridge, cap tables, VC deals |
| I need to make a better decision | Think / Align | decision quality, heuristics, group process, role identity, visual bias |
| I need to build with AI | Build With AI | agent-ready specs, code implementation, verification, architecture |
| I need stakeholder material | Align | updates, narratives, decks, stakeholder plans |

## Lifecycle Index

- **Think**: 25 skills
- **Discover**: 37 skills
- **Strategize**: 46 skills
- **Design**: 39 skills
- **Plan**: 21 skills
- **Measure**: 17 skills
- **Growth**: 12 skills
- **Align**: 31 skills
- **Build With AI**: 13 skills
- **Launch & Learn**: 11 skills

## Workflow

1. Classify the user's persona, product stage, artifact mode, evidence state, and
   decision mode.
   - If the user asks `/productize build <request>`, use the operator build
     route. Read `.productize/project/context.md`, `.productize/project/conventions.md`,
     `.productize/project/architecture.md`, `.productize/project/decisions.md`, and
     `.productize/project/constraints.md` when present. Read
     `.productize/project/manual.md` when present for human-authored additions. Inspect
     `.productize/tasks/` for existing PRD, TechSpec, task, and review artifacts.
     Return the required route-plan contract below and ask whether to approve or
     edit the route before mutating files or running agents.
   - If the user asks to adopt, onboard, or initialize Productize for an existing repository, route to `/productize adopt`: run `productize onboard existing`, inspect the Knowledge Coverage section, read `.productize/project/context.md`, `.productize/project/conventions.md`, `.productize/project/architecture.md`, `.productize/project/decisions.md`, and `.productize/project/constraints.md`, plus `.productize/project/manual.md` when present, then recommend the next workflow route.
2. Route to the narrowest Productize skill that can produce the artifact or build
   step. If the request spans stages, sequence the skills and explain the order.
3. Use existing context first: attached docs, repo files, meeting notes, research,
   metrics, prior Productize artifacts, and explicit user constraints.
4. Choose artifact format deliberately: Markdown for short or diff-sensitive work,
   self-contained HTML for long, visual, shareable, interactive, or explicitly
   requested artifacts.
5. State what is known, assumed, missing, and risky before making recommendations.
6. Produce the artifact, implementation plan, code change, verification evidence,
   or handoff plan the user can act on immediately.

## Intent Routes

- **I have an idea**: use Think skills for thesis framing, opportunity selection,
  wedge design, and early validation.
- **I need positioning/growth**: use Strategize or Growth skills for market structure,
  positioning, brand, GTM, growth loops, retention, and PMF.
- **I need a PRD/spec**: use Plan or Build With AI skills for PRDs, requirements,
  architecture briefs, agent handoffs, and verification.
- **I need research**: use Discover skills for JTBD, interviews, assumptions, ICP,
  research plans, and insight synthesis.
- **I need metrics/PMF**: use Measure skills for dashboards, funnels, experiments,
  churn, retention, PMF, and metric reviews.
- **I need valuation/deal pricing**: use Finance skills for DCF, WACC, CAPM,
  enterprise-value to equity-value bridges, cap tables, dilution, and startup deal terms.
- **I need to make a better decision**: use Decision Making skills for individual,
  group, visual, role/social, heuristic, and decision-record workflows.
- **I need to build with AI**: use Build With AI skills for agent-ready specs,
  technical planning, code implementation, verification, and implementation handoff.
- **I need stakeholder material**: use Align skills for narratives, executive updates,
  decks, meeting plans, and decision rights.

## Output Contract

For `/productize build <request>`, return this operator route plan:

```text
Route selected:
1. ...

Why:
...

Project context read:
...

Missing artifacts:
...

Next command:
...

Approval needed:
...
```

Route rules for `/productize build <request>`:

- If `.productize/project/context.md` is missing, degraded, or reports unresolved
  Knowledge Coverage findings, make `productize onboard existing` the first route step.
- If project context exists but PRD, TechSpec, or tasks are missing, route through
  `/create-prd`, `/create-techspec`, and `/create-tasks` in that order.
- If task files exist, route to `productize tasks run <workflow>`.
- If review artifacts exist, route to review/fix before completion.
- Always name the exact next command or skill.
- Ask for approval before any step that writes files, runs an implementation
  agent, changes git state, or starts a long-running daemon task.

For all other Productize routes:

Return:

1. **Route**: selected skill or skill sequence, with a one-sentence reason.
2. **Context read**: known facts, assumptions, missing inputs, and risky leaps.
3. **Artifact contract**: artifact type, format, audience, fidelity, and decision it supports.
4. **Work product**: the actual artifact, implementation step, code change, or first useful slice of it.
5. **Next action**: owner, validation step, metric, or handoff.

Do not stop at a list of possible frameworks unless the user explicitly asks for a
menu. Recommend a route and proceed with explicit assumptions when possible.
