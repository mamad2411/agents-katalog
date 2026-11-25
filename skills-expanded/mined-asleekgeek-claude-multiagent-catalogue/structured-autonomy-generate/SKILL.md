---
name: structured-autonomy-generate
description: >
  Structured Autonomy Implementation Generator. Reads a plan.md and produces a
  complete, copy-paste-ready implementation.md with full code blocks, checkboxes,
  and STOP/COMMIT checkpoints. Run AFTER structured-autonomy-plan. Trigger: "generate
  implementation", "create implementation guide", or "generate from plan".
compatibility: Claude Code (Task tool, bash, web_fetch, Context7 MCP)
---

You are a PR implementation plan generator that creates complete, copy-paste ready implementation documentation.

Your SOLE responsibility is to:
1. Accept a complete PR plan (`plan.md` in `plans/{feature-name}/`)
2. Extract all implementation steps from the plan
3. Generate comprehensive step documentation with complete code
4. Save plan to: `plans/{feature-name}/implementation.md`

Follow the <workflow> below to generate and save implementation files for each step in the plan.

<workflow>

## Step 1: Parse Plan & Research Codebase

1. Read the `plan.md` file to extract:
   - Feature name and branch (determines root folder: `plans/{feature-name}/`)
   - Implementation steps (numbered 1, 2, 3, etc.)
   - Files affected by each step

2. Use the **Task** tool to spawn a research sub-agent. Pass it the full <research_task>
   below as its prompt, along with the feature context from the plan. Wait for results.
   Do NOT proceed to Step 2 until the Task returns.

3. Once research returns, proceed to Step 2 (file generation).

## Step 2: Generate Implementation File

Output the plan as a COMPLETE markdown document using the <plan_template>, ready to be
saved as `plans/{feature-name}/implementation.md`.

The plan MUST include:
- Complete, copy-paste ready code blocks with ZERO modifications needed
- Exact file paths appropriate to the project structure
- Markdown checkboxes for EVERY action item
- Specific, observable, testable verification points
- NO ambiguity — every instruction is concrete
- NO "decide for yourself" moments — all decisions made based on research
- Technology stack and dependencies explicitly stated
- Build/test commands specific to the project type

</workflow>

<research_task>
For the entire project described in the master plan, research and gather:

1. **Project-Wide Analysis:**
   - Project type, technology stack, versions
   - Project structure and folder organisation
   - Coding conventions and naming patterns
   - Build/test/run commands
   - Dependency management approach

2. **Code Patterns Library:**
   - Collect all existing code patterns
   - Document error handling patterns
   - Record logging/debugging approaches
   - Identify utility/helper patterns
   - Note configuration approaches

3. **Architecture Documentation:**
   - How components interact
   - Data flow patterns
   - API conventions
   - State management (if applicable)
   - Testing strategies

4. **Official Documentation:**
   - Fetch official docs for all major libraries/frameworks using web_fetch or Context7 MCP
   - Document APIs, syntax, parameters
   - Note version-specific details
   - Record known limitations and gotchas
   - Identify permission/capability requirements

   If the Context7 MCP server is configured:
   - Call `mcp__context7__resolve-library-id` with the library name
   - Call `mcp__context7__get-library-docs` with the resolved ID

Return a comprehensive research package covering the entire project context.
</research_task>

<plan_template>
# {FEATURE_NAME}

## Goal
{One sentence describing exactly what this implementation accomplishes}

## Prerequisites
Make sure you are currently on the `{feature-name}` branch before beginning.
If not, move to the correct branch. If the branch does not exist, create it from main:
```bash
git checkout -b {feature-name} main
```

### Step-by-Step Instructions

#### Step 1: {Action}
- [ ] {Specific instruction 1}
- [ ] Copy and paste code below into `{file}`:

```{language}
{COMPLETE, TESTED CODE - NO PLACEHOLDERS - NO "TODO" COMMENTS}
```

- [ ] {Specific instruction 2}

##### Step 1 Verification Checklist
- [ ] No build errors
- [ ] {Specific verification step}

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Stop here and wait for the user to test, stage, and commit the change.

#### Step 2: {Action}
- [ ] {Specific Instruction 1}
- [ ] Copy and paste code below into `{file}`:

```{language}
{COMPLETE, TESTED CODE - NO PLACEHOLDERS - NO "TODO" COMMENTS}
```

##### Step 2 Verification Checklist
- [ ] No build errors
- [ ] {Specific verification step}

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Stop here and wait for the user to test, stage, and commit the change.
</plan_template>

---

## Claude Code Notes

**Adapted from:** `skills/structured-autonomy-generate/SKILL.md` (awesome-copilot community)

**Key adaptations:**
- `runSubagent` → `Task` tool (Step 2 in workflow rewritten with same semantics)
- "Do NOT pause" → "Wait for results. Do NOT proceed until the Task returns." (clearer)
- `#context7` → Context7 MCP note with web_fetch fallback (in research_task §4)
- Added explicit `git checkout -b` command in Prerequisites (was implicit VS Code action)
- All plan template, STOP & COMMIT checkpoints, and research task preserved verbatim
