---
name: idea-launcher
description: "Use when Codex needs to turn a rough app, tool, game, automation, or product idea into a ready-to-build project plan, scaffold direction, implementation task breakdown, verification checklist, deployment workflow, or first build prompt. Trigger for idea shaping, MVP narrowing, project specification, starter structure generation, planning docs, pre-build interviews, product and technical tradeoff analysis, factory mode, sharpen-the-axe mode, and ship mode."
---

# Idea Launcher

Turn vague ideas into practical project plans, starter folders, and execution prompts for a one-person software factory. Optimize for fast learning, narrow scope, good taste, verification, and deployability.

## Operating Rules

- Prefer a concrete proposal with explicit assumptions over a long questionnaire.
- Ask at most 1-3 clarifying questions per pass. Ask only questions that change the plan materially.
- Always include both the good side and bad side before recommending a direction.
- Treat the first useful shipped version as the default target. Push nice-to-haves into later milestones.
- If the user asks to brainstorm, explore options, tradeoffs, and failure modes before converging.
- If the user asks to build, run the prompt-readiness triage first, shape only enough to prevent rework, then move into implementation.
- Respect local `AGENTS.md` and `MEMORY.md` instructions. If a durable preference or project fact is discovered, update the relevant memory file and mention the change.
- Commit and push after major tasks when the active workspace instructions say to do so.

## Prompt-Readiness Triage

Classify the user's idea before choosing brainstorm, planning, or build behavior.

**Detailed-enough prompt:** the prompt names the product or workflow, gives a target user or context, implies a platform or output, and has enough constraints to choose a first build without inventing the core product. Do not skip straight into code. First give a serious pass:

- Summary of what will be built.
- Assumptions you will use unless corrected.
- Pushbacks, risks, and likely scope traps.
- Suggestions that would improve the build without bloating v1.
- The smallest credible v1 and what is explicitly not in v1.

After that pass, proceed when the user already asked to build and no answer is needed to avoid wrong work.

**Basic, half-formed, or unclear prompt:** the prompt is mostly a theme, name, vibe, feature pile, or unclear request. Use brainstorm mode or the clarifying pattern from `references/interview-workflow.md`. Ask only the 1-3 questions that change direction, and offer a default assumption path so the user can say "go".

**Explicit brainstorm prompt:** expand options first, compare tradeoffs, then recommend one direction and one smaller version.

## Core Workflow

1. **Capture the idea:** Restate the concept in one sentence, name the target user, and infer the likely project type: app, tool, game, automation, integration, content workflow, data product, or experiment.
2. **Triage readiness:** Decide whether the prompt is detailed enough, basic/unclear, or explicitly brainstorm-oriented.
3. **Interview lightly:** Use `references/interview-workflow.md` to collect only the missing information needed to shape scope, risk, stack, and output.
4. **Run the tradeoff pass:** List the good side, bad side, hidden complexity, and the smallest credible version.
5. **Shape the project:** Use `references/project-shaping-rubric.md` across usefulness, scope, stack, data model, UI, workflows, automation, risks, verification, and deployment.
6. **Select a mode:** Use `references/modes.md` for default launch, factory mode, sharpen-the-axe mode, brainstorm mode, or ship mode.
7. **Produce artifacts:** Create or update the needed planning files using `assets/templates/`.
8. **Prepare execution:** Convert decisions into atomic tasks, verification gates, subagent splits where allowed, and a first build prompt.
9. **Generate a starter when useful:** In factory mode, use `scripts/launch_project.py` with a matching starter pack to create a project folder, then run `scripts/validate_placeholders.py` against the result.
10. **Build the actual product:** In full-build mode, generate the starter, inspect the generated docs and source, then implement the project-specific behavior, UI/design, tests, and deploy config directly in the generated project.
11. **Reinforce frontend quality:** For web apps, tools, dashboards, and games, apply `references/frontend-design.md` before coding UI. Favor fast static starters and only add heavier frontend stacks when the workflow justifies them.

## Output Contract

For a planning response, provide:

- Idea summary
- Good side
- Bad side
- Key assumptions
- Recommended MVP
- Project shape
- Open questions, capped at 3
- Next artifact or build step

For file generation, write only the artifacts that are useful for the current request. Start with:

- `SPEC.md` from `assets/templates/SPEC.md`
- `TASKS.md` from `assets/templates/TASKS.md`
- `AGENTS.md` additions from `assets/templates/AGENTS-additions.md`
- Implementation checklist from `assets/templates/IMPLEMENTATION-CHECKLIST.md`
- Test plan from `assets/templates/TEST-PLAN.md`
- Deploy plan from `assets/templates/DEPLOY-PLAN.md`
- First build prompt from `assets/templates/FIRST-BUILD-PROMPT.md`
- Starter structure from `assets/templates/STARTER-STRUCTURE.md`

When copying templates, replace placeholders, delete irrelevant sections, and keep open questions explicit instead of hiding uncertainty.

## Factory Script

Use the factory script when the user wants a reusable starter structure or a generated project folder:

```bash
python scripts/launch_project.py --name "Project Name" --idea "One-line idea" --type web-app --out ./output
python scripts/validate_placeholders.py ./output/project-name
```

Starter pack choices:

- `web-app`
- `automation`
- `game`
- `data-tool`

Use `--force` only when intentionally regenerating files. Do not overwrite a user's existing project files without explicit approval.

## Full-Build Mode

Use full-build mode when the user wants the actual app, game, automation, or data tool, not just specs. The factory script creates a runnable baseline; Codex must then edit the generated project until it matches the idea.

Full-build sequence:

1. Generate the closest starter pack.
2. Read the generated `docs/SPEC.md`, `docs/TASKS.md`, and source files.
3. Replace demo behavior with the real core workflow.
4. Shape the interface or output format to the domain. For web apps and games, load `references/frontend-design.md` and treat design as part of implementation, not a later polish task.
5. Add or update focused tests for the real behavior.
6. Run local verification commands from `AGENTS.md`.
7. Start the dev server or provide the runnable command/path.

Do not stop at generated docs when the user asked to build. The generated starter is the starting point, not the deliverable.

## Subagents

Use subagents only when the current session and user instructions allow it, and when the split will materially save time. Prefer independent sidecar work: repo discovery, UI surface planning, data model review, risk review, test planning, deployment research, or isolated implementation slices. Do not delegate the immediate blocking decision.

For detailed split patterns and prompt shapes, use `references/subagents.md`.

## Quality Gates

Before finishing a launch plan, confirm:

- The MVP is narrow enough for one person to build.
- Every major feature maps to a user workflow or explicit learning goal.
- The data model is named even if it is intentionally simple.
- Risks have mitigation or scope cuts.
- The test plan verifies the highest-risk behavior first.
- The deploy plan names the target environment, secrets, migration needs, and rollback path.
- The first build prompt is self-contained enough for a fresh Codex thread to execute.
- Generated starters have no unresolved double-brace template placeholders.
- Full-build outputs run locally and demonstrate the real core workflow.
- Frontend outputs are fast to run, domain-specific, responsive, and free of generic placeholder UI.

## References

- `references/interview-workflow.md`: Clarifying without over-questioning.
- `references/project-shaping-rubric.md`: Good/bad tradeoff and project shaping rubric.
- `references/modes.md`: Factory mode, sharpen-the-axe mode, ship mode, and default launch mode.
- `references/full-build-workflow.md`: How to turn a generated starter into a real runnable project.
- `references/frontend-design.md`: Fast, practical frontend design rules for generated apps and games.
- `references/subagents.md`: When and how to split work across agents.
- `references/examples.md`: Short examples for web apps, automations, and games.
- `assets/templates/`: Copy-ready planning and execution templates.
- `assets/blueprints/`: Runnable baseline projects copied by the factory script.
- `assets/starter-packs/`: JSON defaults for generated project starters.
- `scripts/launch_project.py`: Generate a starter project from templates and a starter pack.
- `scripts/validate_placeholders.py`: Check generated artifacts for unresolved placeholders.
