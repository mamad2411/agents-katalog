<!-- agent-notes: { ctx: "implementation planning workflow", deps: [docs/methodology/personas.md, docs/methodology/phases.md], state: active, last: "pat@2026-02-12" } -->
I need to plan the implementation of: $ARGUMENTS

Before writing the plan, ensure the goal is well-understood. If the request is vague, first run through Coach Cam elicitation (see `docs/methodology/personas.md`) or use `/kickoff` for full discovery.

## Architecture Decision Scan (Mandatory Pre-Step)

Before writing the plan, scan the work items for architectural decisions:

1. **For each item, ask:** Does this involve a new pattern, new integration, technology choice, data model change, or package boundary?
2. **If yes:** The item requires the Architecture Gate (see CLAUDE.md § Architecture Gate). Flag it in the plan as "**Requires Architecture Gate:** ADR + Wei debate before implementation."
3. **If any items require the gate:** The plan must schedule Phase 2 (Architecture) before Phase 3 (Implementation) for those items. They cannot enter the TDD pipeline until the ADR exists, Wei has challenged it, and the debate is tracked.
4. **List gated items** in a dedicated section of the plan document.

## Plan Document

Create or update a plan document in `docs/plans/`. The plan should include:

1. **Goal** — What we're trying to achieve and why.
2. **Constraints** — Any relevant ADRs, conventions, or technical limitations.
3. **Architecture Gate Items** — Items requiring ADR + Wei debate before implementation. For each: what decision needs an ADR, and why it's architectural (not just implementation detail).
4. **Approach** — Step-by-step implementation plan following TDD. Gated items must show Architecture phase before Implementation phase.
5. **Personas involved** — Which v-team personas should be consulted during implementation? (See `docs/methodology/personas.md`.) Include Wei for any gated items.
6. **Open Questions** — Anything that needs clarification before starting.
7. **Acceptance Criteria** — How we'll know the work is done.

Check existing ADRs and plans for context before writing. Add agent-notes frontmatter per `docs/methodology/agent-notes.md`.

## Tracking Artifact

After the plan document is written, produce `docs/tracking/YYYY-MM-DD-<topic>-plan.md` summarizing the plan's goals, approach, key constraints, and acceptance criteria. Use the standard tracking format from `docs/process/tracking-protocol.md`. Set **Prior Phase** to the most recent tracking artifact for this topic (if any), or "None" if this is a standalone plan.

## Development Environment Check

After the plan is written, check whether a devcontainer is set up:

1. Check if `.devcontainer/devcontainer.json` exists.
2. **If it does not exist:** Ask the user: "No devcontainer is configured for this project. Would you like me to set one up before we start implementation? This ensures a consistent development environment. I can run `/devcontainer` to create one."
   - If yes: run `/devcontainer` with the project's tech stack as context.
   - If no: note the decision and proceed.
3. **If it already exists:** No action needed — proceed to implementation.
