---
name: omt-design
description: Design pass in T3 Code. Use when the user asks for designs, mockups, screens, UX, or a design pass, or when an omt-plan or omt-ulw run has a requested design pass before its UI units. Draws variants, lets the owner pick and steer by screenshots until they approve, and writes a design spec that UI units cite.
---

# Design

You get designs drawn, apply the owner's words until the owner approves, and write the design spec. The owner is the design review. No model reviews the design files or the screenshots.

## Steps

### 0. Check your mode

Call `t3_thread_configure` with no arguments ([delegation.md](../omt/references/delegation.md#your-interaction-mode)). A design pass writes files, so in `plan` mode ask the user to switch this thread to default mode.

Pick the drawer by [roles.md](../omt/references/roles.md#main-thread-or-child): run `omt route design --json`. When its `delegateTask.target.model` is your model, you draw. Otherwise one routed `design` child draws.

Done when: you run in `default` mode and you know the drawer, or the user has the question.

### 1. Frame and slug

Write down the goal, the users, the platform, the screens and flows, the constraints, and the existing brand, from the code and assets. Ask the owner only what you cannot find, in one batch, with options and your recommendation.

Pick a slug that matches `^[a-z0-9][a-z0-9-]{0,63}$`. The design files go under `docs/design/<slug>/`, and the spec is `docs/design/<slug>.md`. The ledger plan is the plan slug when `omt-plan` or `omt-ulw` called this skill, else `design-<slug>`.

Done when: the frame and the slug are in your reply.

### 2. Draw the variants

When this skill runs alone, run `omt git start --run <slug>` before the first file. Step 7 builds under the plan `<slug>`, so the same start record covers the design files.

Draw `workflow.design.variants` distinct variants of each screen, or the count that the owner asked for. Each variant has its empty, loading, and error states. Use the tool that `workflow.design.tool` names:

- `paper`: a new Paper file named after the project, when Paper's tools load. Reuse no open file. Without Paper's tools, use HTML mockups.
- `html`: self-contained HTML mockups.

Export a PNG of each frame to `docs/design/<slug>/`, by [roles/design.md](../omt/references/roles/design.md). When Anthropic's optional `frontend-design` skill is installed, load it, and put its path in a child's brief.

A child draws as unit `DS<k>`, dispatched by [Dispatching a child](../omt/references/delegation.md#dispatching-a-child) with `--scope docs/design/<slug>/` and `mode: "wait"`. Its task holds the frame, the variant count, and the tool.

Done when: every variant of each screen has a PNG under `docs/design/<slug>/`, or the owner knows why no drawer can run.

### 3. Owner checkpoint

Show every screenshot as a Markdown image with its absolute path, such as `![Home, variant A](/abs/path/docs/design/<slug>/home-a.png)`, grouped by screen, with one line on each variant. Ask in one batch which variant to keep for each screen and what to change. End the turn.

Done when: the owner has the screenshots and the question.

### 4. Steer

Apply the owner's words verbatim to the chosen variants, in the same Paper file or mockups. When you draw, change the frames and export again. When a child draws, dispatch a new round of the same unit with the owner's words in the task and every earlier round in `--prior-file`. Run one `design` child at a time. Then go back to step 3.

Done when: the owner approved one variant for each screen.

### 5. Write the spec

Write `docs/design/<slug>.md` yourself, also when a child drew. Read exact values from the Paper file or mockup source, not from the screenshots. Use the spec sections of [roles/design.md](../omt/references/roles/design.md). Name the approved variant of each screen, and quote the owner's last words.

Done when: the spec exists, each screenshot path in it exists, and the owner has its path.

### 6. Hand off

Each unit that builds this UI cites `docs/design/<slug>.md` and uses the `ui` role. Its `qa` task gets no `docs/design/` paths and no visual-match checks: QA checks behavior, and the owner compares the result with the design.

Return the spec path to `omt-plan` or `omt-ulw` when one called this skill. Otherwise give the owner the spec path, and offer to build the screens here.

Done when: the caller, or the owner, has the spec path.

### 7. Build in the same thread

Only when the owner asks, write a LIGHT plan with `omt plan new <slug> --light`, with one `ui` unit per screen that cites the spec. Then run [omt-ulw](../omt-ulw/SKILL.md) steps 7 to 12.

Done when: the `omt-ulw` step 12 report is with the owner.
