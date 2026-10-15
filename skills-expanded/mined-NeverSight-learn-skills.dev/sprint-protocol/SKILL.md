---
name: sprint-protocol
description: Use when turning founder requirements, research packets, plans, specs, and system designs into one or more independently executable Claude/Cloud Code implementation sprints with story writing, review, execution, optional verification, and sprint-level commits.
---

# AgentX Sprint Protocol

Use this skill when the user wants to turn a product or engineering goal into a controlled sprint delivery process. The user may arrive with a raw brain dump, or they may already have a `Research.md`, `Plan.md`, `Spec.md`, `System-Design.md`, `Requirements.md`, PRD, architecture packet, or prior chat summary. The protocol must handle both paths.

The goal is not to create busywork. The goal is to decide what should be built, whether it fits in one sprint, how to divide it if it does not, how to write executable stories, how to run multiple workers safely, when to run a dedicated verification pass, and how to preserve traceability through sprint artifacts and commits.

## Core Invariants

1. **Founder intent is the source of truth.** The protocol starts by understanding what the founder wants shipped and why. Existing research or design docs must be reviewed for gaps, inconsistencies, missing decisions, and scope risk before sprint folders are created.
2. **Plan before execution.** Every phase starts with a task list. The lead keeps an explicit queue, dependency map, blocker list, and approval status.
3. **One canonical memory surface.** Sprint state lives in files under the sprint folder, not in chat memory. Long-running work must be resumable from artifacts alone.
4. **Lead orchestrates, workers implement.** The lead does not absorb the whole codebase. The lead reads sprint artifacts, high-level diffs, reports, and status. Codebase research, implementation, code review, and verification are delegated to teammates.
5. **Feature-driven sprinting.** A sprint must deliver one or more concrete features, fixes, or quality checkpoints. Sprints are ordered so each one creates usable foundation for the next.
6. **Story count is earned, not fixed.** Do not force a sprint into an artificial number of stories. Create as many stories as the feature requires, then challenge the set for over-splitting, missing work, dependency problems, and testability.
7. **Every story declares required skills and tests.** Each story must tell the worker which domain skills/tools to load and which feature-specific tests prove completion.
8. **Execution concurrency is configurable.** Before Phase 4 execution, ask the user how many stories to run at once: 1, 2, 3, or 4. Respect dependency and conflict risk even if the user chooses a higher number.
9. **One sprint, one delivery commit.** Workers normally do not create final commits per story. The lead verifies, reviews, stages intentionally, and creates one clean sprint commit unless the user asks for a different commit strategy.
10. **Verification is an explicit QA mode.** Every executed sprint produces `progress.md`, `verification-checklist.md`, and `sprint-completion.md`. `verification-report.md` and browser/video evidence are created when the user runs Phase 5 verification or when a checkpoint sprint explicitly performs QA work.

## Sprint Versus Epic

A **sprint** is an executable delivery unit. It has a folder, stories, a progress ledger, a verification checklist, a completion report, and normally one sprint-level commit. A sprint should deliver one or more concrete features, fixes, foundations, or quality checkpoints that can be reviewed and carried forward.

An **epic** is only a scope signal. It means the founder's input is too large, risky, or sequentially dependent to execute as one sprint. The protocol should not create a separate epic operating system by default. Instead, Phase 1 distributes the scope into independently executable sprint folders, each with its own `research.md` and `plan.md`.

Use the word epic only when explaining size: "this is epic-sized, so I recommend five sprints." Do not require a separate intake-review, roadmap, checkpoint-plan, decisions bundle, or parent planning folder unless the user explicitly asks for a portfolio-level planning artifact.

## Two Intake Modes

### Mode A: Raw Founder Brain Dump

Use when the user arrives with ideas, goals, complaints, screenshots, or loose requirements.

The research phase performs real discovery:

- interview the user only where missing context would make the sprint unsafe or untestable
- identify research shards
- delegate codebase and product research
- synthesize `research.md`
- create `plan.md`
- recommend whether the work fits one sprint or needs a multi-sprint distribution

### Mode B: Baked Research Or Plan Packet

Use when the user already has substantial planning material: `Research.md`, `Plan.md`, `Spec.md`, `System-Design.md`, `Requirements.md`, PRD, architecture notes, or prior chat summaries.

The research phase becomes a planning review and sprint distribution phase:

- read the supplied packet fully
- identify contradictions, missing decisions, hidden dependencies, and untestable acceptance criteria
- ask the user targeted questions only where the plan cannot be safely converted into sprints
- decide whether the scope fits in one sprint
- if it fits, create the sprint `research.md` and `plan.md`
- if it does not fit, create a multi-sprint distribution first, then create named sprint folders after user approval

## Phase Map

| Phase | Name | Main question | Output |
| --- | --- | --- | --- |
| 1 | Research And Planning | What is being built, and does it fit in one sprint? | `research.md`, `plan.md`, or a multi-sprint distribution with independent sprint folders |
| 2 | Story Writing | What exact implementation stories should workers execute? | `README.md`, `stories/STORY-NNN.md` |
| 3 | Review And Audit | Are stories complete, testable, correctly sized, and aligned with founder intent? | updated stories, `verification-checklist.md` |
| 4 | Execution | Which stories can safely run now, with what concurrency and branch strategy? | code changes, `progress.md`, `sprint-completion.md`, one sprint commit |
| 5 | Verification | Did the sprint actually work, and what evidence proves it? | fixes, `verification-report.md`, evidence, PR handoff when explicitly requested |
| C | Checkpoint Sprint | After several implementation sprints, does the integrated product still hold together? | code review, browser verification, integration fixes, `sprint-completion.md`, optional `verification-report.md` |

## Commands

Claude Code slash commands remain the primary command surface:

- `/sprint-research <topic-or-folder>` — Phase 1: research, planning review, sprint sizing, or multi-sprint distribution
- `/sprint-stories <sprint-folder>` — Phase 2: write implementation stories
- `/sprint-review <sprint-folder>` — Phase 3: founder review, story audit, verification checklist
- `/sprint-execute <sprint-folder>` — Phase 4: configurable multi-worker implementation
- `/sprint-verify <sprint-folder>` — Phase 5: optional QA verification, evidence capture, fixes, and PR handoff

When the user gives a folder path, use that folder directly. Do not assume a parent planning layout. Multi-sprint work should normally be represented by multiple independent sprint folders, usually with a shared initiative prefix.

## Artifact Layout

### Sprint Folder

```text
sprints/<sprint-name>/
  research.md
  plan.md
  README.md
  stories/
    STORY-001.md
  verification-checklist.md
  progress.md
  sprint-completion.md
```

### Verification Mode Adds

```text
sprints/<sprint-name>/
  verification-report.md
  evidence/                  # only when screenshots, recordings, logs, or other QA proof are produced
```

### Multi-Sprint Distribution

Use independent sprint folders. Each folder must be self-contained enough to plan, write, execute, and verify later without needing the original chat.

```text
sprints/
  <initiative>-01-<feature-name>/
    research.md
    plan.md
  <initiative>-02-<feature-name>/
    research.md
    plan.md
  <initiative>-checkpoint-03-<theme>/
    research.md
    plan.md
```

Checkpoint sprints are first-class sprints. They are not filler. Their job is to inspect what previous sprints actually delivered, run code review, run browser/integration testing, repair integration problems, and realign the implementation with the overall initiative goal.

## Required References

Read only the references needed for the current phase:

- Phase 1: `references/phase-1-research.md`
- Phase 2: `references/phase-2-stories.md`
- Phase 3: `references/phase-3-review.md`
- Phase 4: `references/phase-4-execution.md`
- Phase 5: `references/phase-5-verification.md`
- Workers: `references/worker-guide.md`
- Story format: `references/story-template.md`
- Artifact formats: `references/templates.md`

## Difficulty And Model Routing

Every sprint and story must carry a difficulty level:

| Difficulty | Use when | Model routing |
| --- | --- | --- |
| Hard | architecture, cross-system changes, security, complex state, AI agents, migrations, high ambiguity | best available model, highest reasoning effort |
| Medium | multi-file implementation with known patterns and moderate integration risk | strong model, moderate reasoning effort |
| Simple | mechanical, localized, well-specified changes with low blast radius | smaller/cheaper model is acceptable |

The lead chooses worker model strength from difficulty, risk, and dependency position. Do not under-route a story because it looks small if it sits on a critical foundation.

## Skill Routing Rules

Every story must include a mandatory **Required Skills And Tools** section. The story writer must choose skills based on the work, not on habit.

Common routing examples:

- Frontend/UI: frontend design skill, React best practices, Next.js best practices, shadcn/ui skill, accessibility or visual verification skills, and any project-specific design system skill.
- Backend/API/data: stack-specific skills such as Supabase, Convex, Laravel, FastAPI, database/migration, auth, permissions, queue, or API testing skills.
- AI product work: AI SDK, AI Elements, LiveKit agents, LangGraph/Deep Agents, memory, orchestration, tool-calling, evals, or observability skills as applicable.
- Verification: Agent Browser CLI in Claude/Cloud Code, Browser Use in Codex, code review skills, framework test tooling, security review, and any project verification plugin available.

If a required skill is missing, the story should say how the worker should discover it with skill/tool search and what fallback standard applies.

## Branch And Commit Policy

Phase 1 may recommend a branch named `sprint/<sprint-name>` or a shared initiative branch, but execution must confirm the branch strategy with the user before changing branches.

In Phase 4, ask:

1. Should we stay on the current branch or create/switch to a sprint branch?
2. How many stories should run at once: 1, 2, 3, or 4?

Default commit policy:

- workers implement and update `progress.md`
- workers do not create final story commits unless explicitly instructed
- lead performs final review and testing
- lead creates one sprint commit with a clear message and detailed body
- verification fixes may be included in the sprint commit if discovered before commit, or in one follow-up verification commit if discovered during explicit Phase 5 QA

## Stop Conditions

Stop and ask the user when:

- the provided research/spec packet contradicts itself in a way that changes scope
- acceptance criteria are not testable
- sprint sizing shows the work cannot fit one sprint and a multi-sprint distribution needs approval
- branch strategy is unclear and changing branches would risk user work
- credentials, seed data, or services are required for verification but unavailable
- three or more workers hit the same blocker
- continuing would overwrite unrelated user changes

Otherwise, document assumptions in the relevant sprint artifact and continue.
