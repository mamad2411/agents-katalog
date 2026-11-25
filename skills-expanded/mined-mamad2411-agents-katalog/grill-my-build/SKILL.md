---
name: grill-my-build
description: Turn a participant's vague project idea into a scoped, build-ready master prompt through a one-question-at-a-time challenge interview. Use in any file-capable AI coding workspace when participants need to choose a use case, clarify users, inputs, workflow, outputs, constraints, and success criteria before building. Creates a project-local master prompt and, when terminal access is available, opens an automatically updating localhost flow visualisation.
---

# Grill My Build

Use this skill before building a participant's project. It is agent-neutral: work in the participant's current project folder and never rely on a vendor-specific feature. Keep the conversation business-first: the participant answers in plain language; handle file and terminal work yourself.

## Start the local flow

If terminal execution is available, resolve the installed skill folder relative to this `SKILL.md`, then run its launcher from the participant project root. It creates `.build-flow/state.json`, starts a zero-dependency local server, and opens the browser automatically.

```bash
node "<installed-skill-path>/scripts/launch-flow.mjs" --background
```

Read `.build-flow/url.txt` and confirm the page is open. Do not make the participant run a second command unless the browser is blocked.

If terminal execution or localhost access is unavailable, create `.build-flow/state.json` yourself using the state shape below. Continue the workflow normally; the prompt and flow state remain valid outputs and can be opened later in the same folder.

## Grill workflow

Ask one question at a time. Update `.build-flow/state.json` after every answer so the visualisation changes while the participant speaks.

1. **Outcome** — What decision, action, or deliverable should this project improve?
2. **User** — Who will use it, and what do they need to do differently?
3. **Inputs** — What approved, synthetic, or public information will it use? Flag confidential or unavailable data immediately.
4. **Core flow** — What are the 3–5 essential steps from input to outcome?
5. **Output** — What should a good first version produce or show?
6. **Guardrails** — What must it not do? Include privacy, accuracy, approval, and tool-access limits.
7. **Success** — What observable test proves the smallest useful version works in today's session?

After the seven answers, challenge the plan before drafting anything:

- Identify one scope risk, one data/access risk, and one adoption risk.
- Ask the participant to choose the smallest useful version if the idea cannot be built and tested in the session.
- State any defaults as assumptions; never silently invent business rules, sources, or permissions.
- Mark a node `ready` only when its content is specific enough to build.

## Required project files

Create or update only these project-local files:

- `.build-flow/state.json` — flow state used by the local visualisation.
- `MASTER_PROMPT.md` — final build brief and copy-paste master prompt.
- `.build-flow/progress.md` � only after the first build step, with what works, what is next, and what is blocked. Never overwrite a project's existing `progress.md`.

Use this state shape. Keep values short and business-readable.

```json
{
  "projectName": "Account Radar",
  "currentStage": "Guardrails",
  "nodes": [
    { "id": "outcome", "label": "Outcome", "value": "Prioritise account signals for weekly action", "status": "ready" }
  ],
  "risks": ["Use synthetic data only"],
  "masterPrompt": ""
}
```

## Master prompt gate

Do not start building until the participant has seen and accepted the concise master prompt. Write it in `MASTER_PROMPT.md` with these sections:

1. Objective and user
2. Inputs and data boundaries
3. Required workflow
4. Output and acceptance criteria
5. Guardrails and explicit non-goals

Then ask the active AI coding agent to read `MASTER_PROMPT.md`, explain its understanding, and wait for confirmation before changing project files.

## Workshop fallback

If setup, browser launch, or a tool fails, keep the interview going. The finished `MASTER_PROMPT.md` and flow state are valid Lab 1 outputs; the participant can build from them later.
