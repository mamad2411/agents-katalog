---
name: agentforge-template-author
description: >
  Guides a contributor through adding a new shipped AgentForge template under
  `packages/core/src/templates/<name>/` (or platform). Walks the user through
  scope check, agent set, prompts, schemas, `template.json` metadata, README,
  and tests, then emits the complete template directory ready for PR. Trigger
  when the user asks to "add a new template", "ship a template for X",
  "contribute a template", "create a starter for Y workflow", or wants to
  publish a reusable pipeline shape that other AgentForge users can scaffold
  via `agentforge init --template <name>`. Do NOT trigger for
  end-user `.agentforge/` projects (use `agentforge-workflow` for those).
license: MIT
metadata:
  author: mandarnilange
  version: "0.2.0"
---

# AgentForge Template Author

You are helping a contributor add a new **shipped template** to AgentForge.
Templates live under `packages/core/src/templates/<name>/` (core, no platform
deps) or `packages/platform/src/templates/<name>/` (platform, can use the
multi-provider middleware, Postgres, Docker / SSH executors). They are
auto-discovered by the template registry — no registration step.

End users scaffold a copy into their project with:

```bash
npx @mandarnilange/agentforge init --template <name>
```

A new template is the right contribution shape when a useful pipeline pattern
is missing from the catalog. It is **not** the right shape when a user is
building something for their own project — point them at
`agentforge-workflow` instead.

## When to use this skill

Trigger on any of:
- "Add / contribute / ship a new AgentForge template"
- "Create a starter template for `<domain>`"
- "Modify the existing `<template>` template" (after confirming it should be
  forked or replaced rather than upstreamed in place)
- A contributor asking how the templates registry works.

Do **not** trigger for end-user workflow design (use `agentforge-workflow`).

## Reference material

Read on demand — do not load upfront:

- `references/template-anatomy.md` — full directory layout, `template.json`
  manifest contract, and the registry's discovery rules
- `references/core-vs-platform.md` — how to pick which package the template
  belongs in and what each gives you
- `references/test-and-publish.md` — required tests, lint, and the PR
  checklist before shipping

The shipped templates themselves are the strongest reference. Read at least
one before authoring:
- `packages/core/src/templates/simple-sdlc/` — minimal 3-agent example
- `packages/platform/src/templates/api-builder/` — parallel codegen + tests
- `packages/platform/src/templates/code-review/` — diff-input pipeline

## The flow

### 1. Scope check

Ask: "Could a small modification of an existing template do the job?"

| If the goal is | Modifying the existing template usually wins |
|---|---|
| Different model / provider on one agent | yes |
| Extra script step in one agent's flow | yes |
| Drop or add a single gate | yes |
| Different output schema for the same artifact type | yes |
| Net-new pipeline shape (different agent set, different domain) | no — new template |

If the answer is "yes, modification wins", do NOT ship a new template — ask
the user to PR the change to the existing one (or contribute a doc / cookbook
entry showing how to override).

If "no, new template is justified", continue.

### 2. Package selection

Use `references/core-vs-platform.md`. Quick rule:

- **core** if every agent uses Anthropic, the executor is `pi-ai` or
  `pi-coding-agent` only, no Postgres, no SSH workers, no multi-provider.
  Anyone with `npm install @mandarnilange/agentforge-core` can use it.
- **platform** otherwise. Multi-provider, Docker executor, SSH workers,
  Postgres-only state, ECS — these all push the template to platform.

When in doubt, prefer **core**. Cross-package dependencies are not allowed.

### 3. Domain & inputs

Pin the answers:

- **What does the template *produce*?** Concrete artifacts the user gets at
  the end (code, docs, dashboards, reports).
- **What does it *take in*?** A brief, a URL, a code repo, a dataset, a
  ticket. Define the `pipeline.spec.input` shape.
- **What is the human role?** Where does the user need to approve / revise?
  These become gates.

If the inputs are ambiguous (e.g. "any kind of brief"), narrow before going
further. A vague input begets vague agents and bad templates.

### 4. Agent set

Apply the same rules as `agentforge-workflow`:

- One agent = one well-named human role doing one phase.
- Every output `type` is a contract — pick names you will not regret.
- `pi-coding-agent` only when the agent must touch files / run shell.
- `pi-ai` for everything else.
- Every agent declares a `resources.budget`.

Aim for **3–5 agents** for a typical template. More than 6 is a sign the
template is doing too much; consider splitting or removing optional phases.

### 5. Pipeline shape

- **Phase order** — strict topological order on artifact dependencies.
- **Gates** — between expensive / one-way phases (after architecture, before
  code-gen, before destructive ops). Skip gates for cheap reversible steps.
- **Parallel phases** — when agents share inputs and have no inter-deps.
- **Loops** — for self-correcting flows (test-fix, validate-fix).

Cross-cutting agents (security, compliance) are unusual in templates because
they push complexity onto every adopter. Only include if the template's
domain genuinely demands it (e.g. a `regulated-content` template).

### 6. Prompts

Every agent's `spec.systemPrompt.file` points at `prompts/<agent>.system.md`.
Write each prompt with:

- A clear role statement and one-sentence mission.
- A description of the inputs the agent will receive.
- An explicit output contract referencing the schema file.
- 2–4 quality-bar bullets the agent must satisfy.
- Hard constraints (out-of-scope behaviour to refuse).

Treat prompts as the public surface of the template — they are what
end-users will read and edit when adapting it. Prefer clear over clever.

### 7. Schemas

Every output `type` needs a schema file under `schemas/<type>.schema.yaml`.
Reuse the 45 shipped schemas in `packages/core/src/schemas/` whenever
possible — `frd`, `architecture`, `test-suite`, etc. — so end-users get
familiar artifact types across templates.

For new artifact types, follow the structure shown in
`references/template-anatomy.md`. Don't over-specify; the agent fills it in.

### 8. Manifest, README, and tests

Required files at the top of the template directory:

- `template.json` — manifest with `name`, `displayName`, `description`,
  `tags[]`, `agents` (number), `executor`. Schema in
  `references/template-anatomy.md`.
- `README.md` — one-page user-facing doc showing the pipeline shape, what to
  pass in, what comes out, and how to extend. Mirror the structure of
  `packages/core/src/templates/simple-sdlc/README.md`.
- A test that asserts the template's pipeline + agents + nodes parse against
  the Zod schemas in `packages/core/src/definitions/parser.ts`. See
  `references/test-and-publish.md` for the test pattern.

### 9. Wire-up & documentation

- The template registry **auto-discovers** anything with a valid
  `template.json` — no code change needed for `agentforge templates list` to
  pick it up.
- Add an entry to `docs/templates.md` (table at the top + dedicated section
  with pipeline diagram and example run command).
- For platform templates, also update
  `packages/platform/src/templates/registry.ts` only if it does anything
  beyond auto-discovery (most don't).
- Run the full test suite locally: `npm test` from the repo root.

### 10. Emit and stop

Write the directory tree per `references/template-anatomy.md`. **Default
to creating new files** — see the *Modification policy* below before
touching any existing template, registry, or doc. After writing, show the
contributor:

1. The exact file tree you wrote.
2. The validate command:
   ```bash
   npm test -- packages/core/tests/templates  # or platform/
   ```
3. The local-scaffold command they can run to dogfood the template:
   ```bash
   npx tsx packages/core/src/cli/index.ts init --template <name>
   ```
4. The PR checklist from `references/test-and-publish.md`.

Do **not** open the PR. Do **not** push. Stop here unless the contributor
explicitly asks for the next step.

## Modification policy

This skill ships changes into the repo, not into a user's project — every
edit becomes a PR that other people will live with. Be conservative.

**Default behaviour: create a new template directory. Never touch an
existing shipped template, registry file, doc, or test unless the user
explicitly says "update", "edit", "modify", or names the file.**

Three cases:

1. **New template (greenfield).** Create a brand-new directory under
   `packages/{core,platform}/src/templates/<new-name>/` and a brand-new
   test file. The registry auto-discovers — no registry edit needed.
   `docs/templates.md` is the only existing file you need to *append* to;
   confirm the addition before writing.

2. **The user explicitly asks to edit an existing template** (e.g.
   *"update `simple-sdlc` to add a security agent"*). Before each file
   edit, ask explicit confirmation. Use `AskUserQuestion` (Claude Code)
   or the host agent's interactive-prompt tool when available. Otherwise,
   state the proposed change in chat and wait for a yes/no:

   > *"`packages/core/src/templates/simple-sdlc/pipelines/simple-sdlc.pipeline.yaml`
   > currently has 3 phases. Adding a `security` phase between
   > `architecture` and `implementation` requires renumbering. Apply
   > this edit? (y/n)"*

   One question per file. Modifying a shipped template can break end
   users on `agentforge init --template <name>`; warn the contributor
   that this is a **major** version bump and a breaking change.

3. **The user has NOT signalled an edit intent** but the work overlaps
   with an existing template. Default to forking: create a new template
   directory (e.g. `simple-sdlc-secure/`) instead of modifying the
   existing one. Confirm naming with the contributor.

**Never silently overwrite a shipped template, the registry file, an
existing test, or `docs/templates.md`.** Every edit to existing files in
this repo needs an explicit go-ahead.

## Hard rules

- **Do not invent registry fields.** `template.json` must match the schema in
  `packages/core/src/templates/registry.ts` (`isValidManifest`).
- **One package only.** A template lives in core OR platform, never both.
  Cross-package imports are forbidden.
- **No platform-only features in core templates.** No multi-provider models,
  no Postgres, no Docker executor, no SSH affinity. The CI build will fail.
- **Every output `type` has a schema.** Either reuse a shipped one from
  `packages/core/src/schemas/` or add a new one under the template's
  `schemas/` directory.
- **System prompts go in files**, never inline `text:`. End-users will edit
  these.
- **Tests required.** A template without a parse test should not merge. See
  `references/test-and-publish.md`.
- **Default to creating a new template. Confirm before editing existing
  ones.** See *Modification policy* above. Use `AskUserQuestion` or the
  host agent's interactive-prompt tool. Editing a shipped template is a
  breaking change — warn the contributor.

## What success looks like

- A new directory under `packages/{core,platform}/src/templates/<name>/`
  with `agents/`, `pipelines/`, `nodes/`, `prompts/`, `schemas/`,
  `template.json`, and `README.md`.
- `npm test` passes — including the new template's parse test.
- `npx tsx packages/core/src/cli/index.ts templates list` shows the new
  template (or the platform CLI for platform templates).
- `docs/templates.md` updated with the catalog entry.
- The contributor knows the exact PR checklist and can ship.
