---
name: SpecDriven
description: Spec-driven development — capture intent, interview for gaps, produce verifiable specs before any code gets written. USE WHEN spec, write a spec, spec-driven, brain dump, spec interview, requirements document, what am I building, define requirements, scope this project, plan this feature, spec this out, /spec, /brain-dump, /spec-interview.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/SpecDriven/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the SpecDriven skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **SpecDriven** skill to ACTION...
   ```


# SpecDriven

Structured alignment before action. Capture intent, interview for gaps, produce a verifiable spec — so the Algorithm builds the right thing the first time.

## Core Principles

1. **Alignment before action** — Never build until "done" is defined. Vague requests produce wrong outputs.
2. **The user knows the WHAT, the AI finds the gaps** — Brain dumps capture intent. The interview extracts what was forgotten.
3. **Verifiable over vague** — Every requirement must have a way to check it. "Make it good" fails. "Tests pass" succeeds.
4. **The spec is the contract** — Once agreed, the spec is the single source of truth for all downstream work.
5. **Spec before Algorithm** — This skill runs BEFORE the PAI Algorithm. The spec becomes the Algorithm's input, making OBSERVE sharper and ISC criteria pre-defined.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **BrainDump** | User wants to capture raw thoughts, start a new spec, or says "brain dump" / "spec" / "scope this" | `Workflows/BrainDump.md` |
| **SpecInterview** | User has a brain dump or draft spec and wants gaps filled, or says "interview me" / "refine the spec" | `Workflows/SpecInterview.md` |
| **GenerateSpec** | User confirms interview is complete and wants the final spec written, or says "generate spec" / "write the spec" | `Workflows/GenerateSpec.md` |

## Mode Detection

| User Input | Route |
|------------|-------|
| "I want to build X" / "scope this project" / "brain dump" / "/spec" | → BrainDump workflow |
| Pastes raw notes + "spec this out" | → BrainDump workflow |
| "interview me" / "what am I missing" / "refine the spec" / "/spec-interview" | → SpecInterview workflow |
| "that covers it" / "generate the spec" / "write it up" / "/generate-spec" | → GenerateSpec workflow |
| Pastes a complete spec + "review this spec" | → SpecInterview workflow (review mode) |

## The Three Phases

```
Phase 1: BRAIN DUMP          Phase 2: SPEC INTERVIEW         Phase 3: GENERATE SPEC
┌─────────────────┐          ┌─────────────────────┐         ┌──────────────────┐
│ Raw thoughts     │          │ AI reads brain dump  │         │ Structured spec   │
│ Constraints      │  ──────▶ │ Asks 5-8 questions   │ ──────▶│ Verification cmds │
│ "Done" criteria  │          │ Fills gaps           │         │ Success criteria  │
│ Unknowns         │          │ Pushes back on vague │         │ Ready for work    │
└─────────────────┘          └─────────────────────┘         └──────────────────┘
```

## Output Location

All specs are written to the project's working directory:
- Default: `./spec.md` (or `./specs/{name}.md` for multiple specs)
- The user can override the path.

## Integration

### Feeds Into
- **The Algorithm** — The generated spec becomes the input for OBSERVE. ISC criteria are pre-defined by the spec's Success Criteria section.
- **MEMORY/WORK/** — Specs are stored as work artifacts for session continuity.

### Uses
- **AskUserQuestionTool** — For the interactive interview in Phase 2.
- **Research** — Optionally spawns researchers if the spec involves unfamiliar domains.

### Complements
- **Fabric `create_prd`** — For product-level requirements. SpecDriven is for task/feature-level specs.
- **Fabric `create_recursive_outline`** — For breaking large specs into phases.

## Examples

**Example 1: New feature from scratch**
```
User: "I want to build a CLI tool that converts markdown to PDF"
→ Invokes BrainDump workflow
→ Captures intent, constraints, unknowns
→ Produces draft spec.md with open questions
→ User says "interview me" → SpecInterview fills gaps
→ User says "generate spec" → Final spec.md ready for Algorithm
```

**Example 2: Scoping an existing project task**
```
User: "spec this out — I need to add OAuth to our API"
→ Invokes BrainDump workflow
→ Extracts: OAuth provider, scopes, token storage, redirect flow
→ Flags gaps: which providers? refresh token rotation? rate limits?
→ Interview resolves gaps → generates phased spec
```

**Example 3: Quick bug fix spec**
```
User: "brain dump: the upload endpoint crashes on files over 10MB"
→ Invokes BrainDump workflow (Mode A — raw text provided)
→ Produces micro-scale spec: reproduce, fix, verify
→ Short interview: "Is there a max file size? Should we return 413?"
→ Generates 15-line spec ready for execution
```

## Anti-Patterns (NEVER DO)

1. **Never skip the interview.** The brain dump is never detailed enough. Always ask questions.
2. **Never start building during the spec phase.** This skill produces a DOCUMENT, not code.
3. **Never accept vague success criteria.** Push back. "Works correctly" is not verifiable. "Returns 200 on GET /tasks" is.
4. **Never assume tech stack.** If the user didn't specify, ASK. Don't default silently.
5. **Never generate a 20-section enterprise PRD for a small task.** Scale the spec to the task. A bug fix needs 5 lines, not 5 pages.
