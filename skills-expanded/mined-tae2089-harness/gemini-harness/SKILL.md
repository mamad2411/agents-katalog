---
name: gemini-harness
description: "Configures a harness. A Gemini CLI meta-framework for designing specialized subagent teams and collaboration skills. **This skill MUST be invoked first** when: (1) requests such as 'set up a harness', 'build/design/engineer a harness', (2) building an automation system for a new domain/project, (3) reconfiguring or extending an existing harness, (4) requests for maintenance/operations of an existing harness such as 'inspect harness', 'audit harness', 'harness status', 'agent/skill sync', (5) requests to revise/supplement/re-run previous results. Designed around 7 core architecture patterns and strict tool control."
---

# Harness — Subagent Orchestration & Skill Architect

A meta-skill that configures a harness suited to the domain/project, defines each subagent's role and tool permissions, and creates procedure skills and an orchestrator for agents to use in common.

**Core Principles:**

1. **Apply 7 Core Architecture Patterns:** Select the optimal collaboration structure for the problem characteristics (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical, Handoff). Details: `references/agent-design-patterns.md`.
2. **Strict Tool Permission Control:** Assign only tools optimized for each agent's role; `tools: ["*"]` is prohibited. However, **all agents must include the following tools**:
   - `ask_user`: Used to ask the user for clarification instead of guessing when instructions are ambiguous or data conflicts arise.
   - `activate_skill`: Essential for agents to load and execute procedure skills (methodologies, checklists, protocols) under `.gemini/skills/` at runtime.
   - `invoke_agent` is only permitted for orchestrators, Supervisors, and Hierarchical team leads (Mid-level) — prohibited for regular worker agents. Both sequential (`wait_for_previous: true`) and parallel (`wait_for_previous: false`) use is supported.
3. **Main Agent Orchestration and Persistence:** Since Gemini CLI has no direct inter-subagent communication (`SendMessage`) API, the main agent acts as the sole data broker (`_workspace/findings.md`), state manager (`_workspace/checkpoint.json`), and task board (`_workspace/tasks.md`) manager.
4. **Generate the 3 elements: `.gemini/agents/` + `.gemini/skills/` + `GEMINI.md`.** Do not create slash commands (`.gemini/commands/`).
5. **A harness is not a fixed artifact but an evolving system.** Reflect feedback after each execution and continuously update agents, skills, and GEMINI.md.
6. **Plan Mode Required (Critical):** Before starting any harness design, creation, or extension work, `enter_plan_mode` must be called. Isolate the research and design phases to ensure stability of complex orchestration logic, and only implement in code the plan that has received final user approval. However, in yolo mode, proceed directly.
7. **Zero-Tolerance Failure Protocol:** Arbitrarily skipping test failures or rejected agent outputs is strictly prohibited. The main agent and supervisors must always seek a solution (maximum 2 retries, 3 total); if unresolved, do not autonomously proceed to the next step — immediately halt and request user intervention.

---

## Workflow

### Phase 0: Status Audit and Mode Branching

When the harness skill is triggered, first check the current harness status.

1. Read `{project}/.gemini/agents/`, `{project}/.gemini/skills/`, `{project}/GEMINI.md`.
2. Branch execution mode based on current status:
   - **New Build:** Agent/skill directories do not exist or are empty → Execute all phases starting from Phase 1.
   - **Existing Extension:** An existing harness exists and new agents/skills are requested → Execute only the necessary phases according to the phase selection matrix in `references/expansion-matrix.md`.
   - **Operations/Maintenance:** Audit, modification, or sync request for an existing harness → Move to the operations/maintenance workflow in `references/evolution-protocol.md`.
3. Compare the existing agent/skill list against GEMINI.md records to detect drift.
4. Report the audit results to the user and confirm the execution plan.

---

### Phase 1: Domain Analysis and Pattern Matching

> **Required before starting:** Match the 8 scenarios in `references/usage-examples.md` (SSO build, migration, content loop, parallel research, incident analysis, full-stack development, adding a Stage, partial re-run) with the user's request. If a close scenario exists, use its outputs, patterns, and Stage structure as a starting point (no copy-paste — substitute only domain variables).

1. Identify the domain/project from the user's request.
2. Identify core task types (generation, analysis, validation, editing, deployment, etc.).
3. Analyze conflicts and duplications with existing agents/skills based on Phase 0 audit results.
4. Explore the project codebase — identify the tech stack, data models, and key modules.
5. **User proficiency detection:** Gauge technical level from contextual cues in the conversation (terminology used, question level), and adjust the communication tone accordingly. Do not use terms like "assertion", "JSON schema", or "brokering" without explanation for users with little coding experience.
6. **Architecture pattern matching:** Select the optimal structure from the 7 patterns (`references/agent-design-patterns.md` + `references/usage-examples.md` scenario comparison).

---

### Phase 2: Virtual Team and Tool Design

#### 2-0. Separation Principle: agents vs skills

- **`.gemini/agents/{name}.md` (Persona — "Who"):** Role-based subagents. Define behavioral boundaries with tool permissions and system prompts. (e.g., `@backend-coder`, `@qa-inspector`)
- **`.gemini/skills/{name}/SKILL.md` (Procedure — "How"):** Methodologies, checklists, and protocols that agents follow in common. Reused by multiple agents. (e.g., `tdd-workflow`, `integration-coherence-check`)
- **Decision criteria:** If there is a fixed responsibility and tool set → agent; if it's a procedure or principle → skill. When in doubt, create a skill first and have agents call it via `activate_skill`.

#### 2-1. Architecture Pattern Selection

Decompose the work into specialized domains, then decide on the coordination structure.

- **Pipeline:** Sequentially dependent tasks (design → implementation → validation).
- **Fan-out/Fan-in:** Parallel independent tasks followed by integration.
- **Expert Pool:** Selective invocation based on context.
- **Producer-Reviewer:** Generation followed by a quality review loop.
- **Supervisor:** Main agent monitors state and dynamically distributes tasks.
- **Hierarchical Delegation:** Team lead agent recursively delegates to sub-agents (recommended within 2 levels).
- **Handoff:** An agent directly recommends and delegates to the next specialist after completing its task.

**workflow.md (mandatory for all harnesses):** Every harness declares a Stage-Step structure in `_workspace/workflow.md`. **Stage = high-level issue (Jira Issue/Story, deliverable)**, **Step = sub-issue (Jira Sub-issue) = a single work item within a Stage** (1 Step = 1 pattern). User approval gates are at the Stage (high-level issue) level. Details: `references/stage-step-guide.md`.

> **[MANDATORY] Naming Convention — Jira Title Convention Enforced.** Stage and Step names must be **noun phrases that convey the deliverable meaning**. Same standard as Jira issue titles — the name alone must identify what is being built.
>
> | Prohibited (placeholder/generic)       | Allowed (deliverable-identifying)                      |
> | -------------------------------------- | ------------------------------------------------------ |
> | `main`·`step1`·`task`·`work`·`default` | `sso-integration`·`payment-flow`·`onboarding-redesign` |
> | `phase1`·`stage1`·`generic`            | `requirements-gathering`·`api-design`·`load-test`      |
>
> **Single Stage / Single Step cases follow the same rule** — placeholders like `main` are prohibited. Use domain deliverable names. Example: writing a single blog post → `Stage 1: blog-post` / `Step 1: draft-and-review` (≠ `main/main`).
> Format: `^[a-z][a-z0-9-]*$` (lowercase kebab-case, numbers and hyphens allowed, must start with a lowercase letter).

> **[MANDATORY] workflow.md Schema Enforcement — Omission triggers Zero-Tolerance Failure.** When writing an orchestrator skill, never fall back to a flat "Step 1~N" listing. Every Step block must include all 6 fields below **without exception**.
>
> | Required Field              | Format                                                                                    | Natural Language Prohibited                                                              |
> | --------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
> | `pattern`                   | One of the 7 patterns (`pipeline`·`fan_out_fan_in`, etc.)                                 | Arbitrary notation like "sequential progression" is prohibited                           |
> | `active_agents`             | `[@name1, @name2]` format                                                                 | Missing agent names or free text is prohibited                                           |
> | `exit_condition`            | **Verifiable predicate** (file existence · `task_*.json` status=done · JSON field value · iteration ≥ N) | Expressions like "QA approved", "enough gathered", "when complete" that allow LLM interpretation are **blocked** |
> | `next_step`                 | Step name within the same Stage or `done`                                                 | Omission prohibited                                                                      |
> | `max_iterations`            | Integer (non-loop=1, loop ≤3)                                                             | Omission prohibited                                                                      |
> | Stage `user_approval_gate`  | `required` or `none (last stage)`                                                         | Explicit omission prohibited                                                             |
>
> If a natural language exit condition is written, **reject it immediately** and rewrite as a verifiable predicate. Drift handling: refer to the "drift handling guide" in `references/expansion-matrix.md`.

**Interaction Style Selection (Interaction Styles — Required):** In addition to structural patterns, define the style of interaction with agents.

- **Delegation:** Direct the agent to create/modify output files itself (`invoke_agent`).
- **Consultative:** The main agent receives only analysis opinions or checklists from experts before making a decision (`invoke_agent`).
- **Manual:** The user intervenes directly from the terminal to inspect (`@agent_name`).

> **Core Guide:** When selecting patterns and writing orchestrator agent call prompts, refer to the **"Interaction Styles"** and **"Usage Examples"** sections of `references/agent-design-patterns.md` to construct specific instructions. Defining the style first clarifies whether to give agents `write_file` permissions (delegation) or not (consultative).

---

#### 2-2. Agent Separation Criteria

Evaluate using 4 axes: specialization, parallelism, context, and reusability.

| Criteria       | Separate                          | Merge             |
| -------------- | --------------------------------- | ----------------- |
| Specialization | If domains differ                 | If domains overlap |
| Parallelism    | If independent execution possible | If sequentially dependent |
| Context        | If burden is high (each with small scope) | If lightweight and fast |
| Reusability    | If used by other teams            | If only used by this team |

**Gemini CLI-specific consideration:** Each separation increases the main agent's brokering burden (updating `findings.md`, injecting prompts). Separate only when the benefits of separation outweigh the brokering overhead.

#### 2-3. Tool Set Mapping

Assign standard tools + relevant MCP tools suited to each agent type (Analyst / Architect / Coder / Reviewer / Operator). See the "Standard Tool Sets by Agent Type" table in `references/agent-design-patterns.md` for the full table.

#### 2-4. Orchestration and Persistence Protocol Design

- **Data Flow:** Design file-based data exchange paths within `_workspace/`.
- **Persistence Protocol:** Define the `checkpoint.json` schema and update timing for resuming after interruption.
- **Data Brokering:** Define the path through which the main agent brokers insights between agents via `findings.md` and `tasks.md`.
- **Conflict Mediation:** Pre-designate which agent the main agent will ask for final judgment when agent outputs conflict.

---

### Phase 3: Subagent Definition Generation (.md)

**Generate `{project}/.gemini/agents/{name}.md` files in compliance with the official Gemini CLI subagent format.** Inlining roles into the agent tool prompt is prohibited (to ensure reusability and collaboration protocol).

**How to create agent files:** Read `_workspace/_schemas/agent-worker.template.md` (or `agent-orchestrator.template.md`) synchronized in Step 1.3 using `read_file`, substitute variables, then `write_file` to `.gemini/agents/{name}.md`. Model IDs must be verified in `_workspace/_schemas/models.md` before use.

1. **Required YAML Frontmatter Fields:**
   - `name`: Unique name in slug format.
   - `description`: Written pushily. Include trigger situations and follow-up task keywords.
   - `kind: local`
   - `model`: **Verify in `_workspace/_schemas/models.md` and use the ID appropriate for the role.** Worker → flash tier, Orchestrator/Architect → pro tier. Arbitrary guessing is prohibited — incorrect IDs will cause runtime errors.
   - `tools`: **Restricted list** (`ask_user` and `activate_skill` are mandatory for all agents; `invoke_agent` is permitted for orchestrators, Supervisors, and Hierarchical team leads (Mid-level) only — prohibited for regular worker agents).

2. **Optional Fields (recommended by role):**

   | Role                            | temperature | max_turns |
   | ------------------------------- | ----------- | --------- |
   | Reviewer/QA (deterministic output) | 0.2      | 5 ~ 10    |
   | Analyst/Architect (exploration/design) | 0.3 ~ 0.5 | 10 ~ 15 |
   | Coder                           | 0.2         | 15 ~ 20   |
   | Operator (infrastructure/deployment) | 0.1 ~ 0.2 | 6 ~ 8   |
   | Creative/Brainstorming          | 0.7+        | 10 ~ 15   |

3. **Required System Prompt Sections:** Core role, task principles, I/O protocol (Data Broker-based), error handling, relationships with other agents.

4. **Re-invocation Guidelines:** Specify in each agent definition "behavior when previous outputs exist" (read previous output files and incorporate improvements; if user feedback is given, modify only the relevant parts).

5. **System Registration (required, user manual action):** After agent files (`.md`) are created and modified, prompt the user to run `/agents reload` and `/skills reload`. Reload is only possible from within the Gemini CLI — the user must enter it directly at the Gemini CLI prompt for it to be reflected in the system registry. The main agent notifies as follows:
   ```
   Agent files written: {agent-1}, {agent-2}, ...
   Skill files written: {skill-1}, {skill-2}, ...
   Please type `/agents reload` and `/skills reload` directly at the Gemini CLI prompt to continue.
   Let me know when complete (e.g., "reload done") and I will proceed.
   ```
   Do not call new agents (`invoke_agent`) or skills (`activate_skill`) before receiving reload confirmation — calling before registration will cause failures.

> For templates and full file examples, see "Agent Definition Structure" in `references/agent-design-patterns.md` + `references/examples/team/`.

**Required when including a QA agent:**

- The QA agent's `tools` must include `run_shell_command` (for running tests and linting). Long-running processes (dev server, build watcher) should be started with the **shell background option** and subsequent validation performed in the same turn.
- The core of QA is not "existence checking" but **"boundary cross-comparison"** — simultaneously reading and comparing producer output and consumer input expectations.
- QA should not run once after full completion, but **incrementally immediately after each module is complete** (Incremental QA).
- Details: See `references/qa-agent-guide.md`.

---

### Phase 4: Skill Creation

Create procedure skills for each agent to use at `{project}/.gemini/skills/{name}/SKILL.md`.

**Skill creation decision criteria:**

- Fixed role and tool set → **agent**. Procedure or principle → **skill**.
- 2 or more agents repeat the same methodology → extract as a skill.
- Checklist, protocol, or repeated validation procedure → bundle as a skill.

**What a skill must contain:**

1. `name` + `description` frontmatter — include trigger keywords and follow-up task keywords, written pushily. (pushy criteria and examples: `references/skill-writing-guide.md` § 1-2·1-3)
2. Imperative body — Step sequence, I/O protocol, error handling (`ask_user` path).
3. `references/` pointer — separate infrequently triggered details here (keep under 500 lines).

**Skill-Agent Connection:** `activate_skill` call / prompt inline / `read_file` to load `references/` — 3 methods. See detailed criteria in `references/agent-design-patterns.md` § "Skill ↔ Agent Connection Methods".

Detailed writing patterns, description examples, Progressive Disclosure, and data schemas: `references/skill-writing-guide.md`.

---

### Phase 5: Integration and Orchestration

The orchestrator is a special form of skill that ties individual agents and skills into a single workflow, coordinating the entire team. While Phase 4's individual skills define "what each agent does and how", the orchestrator defines "who collaborates in what order and when". Specific template: `references/orchestrator-template.md`.

**Orchestrator modification for existing extensions:** Do not create a new orchestrator for non-new builds — modify the existing one. When adding agents, reflect the new agent in the team composition, task allocation, and data flow, and add new agent-related trigger keywords to the description.

#### 5-0. Orchestrator Pattern (Gemini CLI Single Mode)

The main agent acts as a data broker while calling subagents sequentially or in batches. Claude Code's `TeamCreate`/`SendMessage`/`TaskCreate` APIs **do not exist in Gemini CLI** and must never be used. Instead:

```
[Main Agent (Orchestrator)]
    ├── Read workflow.md (check current_stage + current_step + active agents + exit condition)
    ├── Manage checkpoint.json (state persistence and resume logic)
    ├── Update findings.md (detailed recording during work)
    ├── Update tasks.md (task board)
    ├── Call @agent-1 (invoke_agent after checking workflow.md step access control)
    ├── Analyze results and dynamic delegation (parse Handoff)
    ├── Read outputs and update findings.md
    ├── Step exit → auto transition, Stage complete → user approval gate → update checkpoint.json
    ├── After all work complete, archive findings.md to _workspace/{plan_name}/findings.md
    └── Central findings.md retains only summary and archive path
```

**Parallelism:** Although Claude Code's `run_in_background` flag does not exist, in Gemini CLI **use `wait_for_previous: false`** when calling `invoke_agent` to achieve parallel execution. Batch-call independent agents within a single response turn to reduce time. (Shell commands can separately be run in parallel using the background option of `run_shell_command`.)

#### 5-1. Data Transfer Protocol

Specify the inter-agent data transfer method within the orchestrator. **Since Gemini CLI has no direct inter-subagent communication API**, all inter-agent information flow is brokered by the main agent through the following 5 file types.

| Strategy                        | Method                                                                                                         | Best For                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **File-based artifacts (default)** | Workers write artifacts directly to `_workspace/{plan_name}/`                                               | Large data, structured artifacts, audit trails                        |
| **findings.md brokering**       | Main reads artifacts, summarizes into `findings.md`, injects into next agent's prompt                          | Sharing insights between agents, mediating conflicts                  |
| **task\_\*.json (worker reporting)** | Worker writes **only its own** `_workspace/tasks/task_{agent}_{id}.json` → main GLOB-collects and atomically integrates into tasks.md | **Avoiding race conditions with parallel agents** (workers must not write to tasks.md directly) |
| **tasks.md task board**         | Updated by main only. Todo / In-Progress / Done / Blocked states                                               | Progress tracking, dynamic allocation in supervisor pattern           |
| **checkpoint.json**             | Updated by main only. Last successful point, shared variables, current_stage, current_step                     | Durable Execution (resume after interruption)                         |
| **Return message**              | Subagent returns final answer                                                                                   | Short results, one-time queries                                       |

**Recommended combination:** Use all 5: file-based artifacts + findings.md (insight brokering) + task\_\*.json (worker reporting) + tasks.md (progress board) + checkpoint.json (persistence).

##### Artifact Management Hierarchy (Read/Write Permission Matrix)

```
_workspace/
├── _schemas/                    [WRITE: main (Step 1 only)]  [READ: all agents (validating own artifacts)]
│   ├── task.schema.json         (JSON Schema — task_*.json validation)
│   ├── checkpoint.schema.json   (JSON Schema — checkpoint.json validation)
│   ├── findings.template.md     (section skeleton — section guide by pattern)
│   ├── tasks.template.md        (table skeleton — for main integration)
│   └── workflow.template.md     (Stage-Step block skeleton + field rules)
├── workflow.md             [WRITE: main (Step 1 only)] [READ: main (every cycle)]
├── findings.md             [WRITE: main only]          [READ: all agents (prompt injection)]
├── tasks.md                [WRITE: main only]          [READ: main]
├── checkpoint.json         [WRITE: main only]          [READ: main]
├── tasks/
│   └── task_{agent}_{id}.json   [WRITE: worker own only] [READ: main (GLOB collection)]
└── {plan_name}/
    └── {step}_{agent}_*.md      [WRITE: worker]          [READ: main → findings summary]
```

**`_schemas/` self-validation workspace:** In Step 1.3, read the 5 files from `references/schemas/` (`task.schema.json`·`checkpoint.schema.json`·`workflow.template.md`·`findings.template.md`·`tasks.template.md`) using `read_file` and write them to `_workspace/_schemas/` using `write_file` pairs (**shell `cp` is prohibited** — skill reference paths are not shell-reachable from the runtime working directory; agent tools must be used). Workers read `_workspace/_schemas/task.schema.json` before writing their `task_*.json` to match the format. Main validates against the schema every time it updates `task_*.json` and `checkpoint.json`. Skill updates apply from the next init — in-progress workspace snapshots are preserved. SoT: `references/schemas/`.

**Core Rules:**

- **Workers must never directly modify `tasks.md`·`findings.md`·`checkpoint.json`** — data loss from race conditions during parallel invocation.
- **Main must not directly write `task_*.json`** — workers write only their own file after completing their task.
- **Main integration flow:** `GLOB("_workspace/tasks/task_*.json")` → read all → ATOMIC_WRITE update of tasks.md + findings.md summary + checkpoint.json.

##### task\_\*.json Schema (Worker → Main Reporting Standard)

```json
{
  "id": "task_{agent}_{seq}",
  "agent": "@agent-name",
  "stage": "{current_stage}",
  "step": "{current_step}",
  "status": "todo | in-progress | done | blocked",
  "evidence": "Verifiable predicate (e.g., '_workspace/sso/research.md exists', 'go test ./... PASS')",
  "artifact": "_workspace/{plan_name}/{filename}",
  "blocked_reason": "(only when status=blocked) reason for blockage",
  "timestamp": "YYYYMMDD_HHMMSS"
}
```

**Filename convention (for artifacts):** `{step}_{agent}_{artifact}_v{version}.{ext}` (e.g., `01_analyst_requirements_v1.md`). Output only final artifacts to user-specified paths; intermediate files are preserved in `_workspace/{plan_name}/`.

#### 5-2. Error Handling and Self-Healing

Include error handling policy within the orchestrator. Core principles: **checkpoint-based automatic resumption**, maximum 2 retries (3 total), then if unresolved, transition task to `Blocked` and request user intervention via `ask_user` (arbitrary skipping is absolutely prohibited), and conflicting data must not be deleted — record with source attribution.

> For error-type strategy table and implementation details, see "Error Handling and Self-Healing" in `references/orchestrator-procedures.md`.

#### 5-3. Team Size Guidelines

| Task Scale                    | Recommended Agents | Tasks per Agent |
| ----------------------------- | ------------------ | --------------- |
| Small (5~10 tasks)            | 2~3                | 3~5             |
| Medium (10~20 tasks)          | 3~5                | 4~6             |
| Large (20+ tasks)             | 5~7                | 4~5             |

> The more agents, the greater the main agent's brokering overhead. 3 focused agents are better than a team of 5 scattered ones.

#### 5-4. GEMINI.md Harness Pointer Registration

After harness configuration is complete, register minimal pointers in the project's `GEMINI.md`. Since GEMINI.md is loaded at every new session, recording only the harness existence and trigger rules is sufficient — the orchestrator skill handles the rest.

> **Parallel use of AGENTS.md:** For projects used alongside Claude Code, Codex, Aider, etc., additionally write an `AGENTS.md` following the Agent Rules initiative standard, and register `{ "context": { "fileName": ["AGENTS.md", "GEMINI.md"] } }` in `settings.json` to load both files.

**GEMINI.md Template:**

```markdown
## Harness: {domain name}

**Goal:** {one-line core goal of the harness}

**Trigger:** Use the `{orchestrator-skill-name}` skill for {domain}-related task requests. Simple questions can be answered directly.

**Change History:**
| Date | Change | Target | Reason |
|---|---|---|---|
| {YYYY-MM-DD} | Initial setup | Entire harness | - |
```

**What NOT to put in GEMINI.md:** Agent list, skill list, directory structure, detailed execution rules. Reason: these are managed in `.gemini/agents/`, `.gemini/skills/`, and the orchestrator skill — duplicating them here is redundant. GEMINI.md should only contain **pointers (trigger rules) + change history**.

#### 5-5. Follow-up Task Support

The orchestrator must handle not only the initial run but also follow-up tasks. Ensure the following three things.

**1. Include follow-up keywords in the orchestrator description:**
Initial creation keywords alone will not trigger follow-up requests. The following expressions must be included:

- "re-run", "run again", "update", "modify", "supplement"
- "redo only {partial task} of {domain}"
- "based on previous results", "improve results"

**2. Add a context check step to Orchestrator Step 0:**
At the start of the workflow, check for existing artifacts and checkpoint existence to determine execution mode.

- **`checkpoint.json` exists + `status: "in_progress"`** → **Resume from interruption point** (execute from the point of failure).
- **`checkpoint.json` exists + `status: "completed"`** → Previous completion state. If partial modification, branch to partial re-run; if new input, branch to new run. Resume prohibited.
- `_workspace/` exists + user requests partial modification → **Partial re-run** (re-invoke only the relevant agents).
- `_workspace/` exists + user provides new input → **New run** (move existing to `_workspace_{timestamp}/` for preservation before starting fresh).
- `_workspace/` does not exist → **Initial run**.

**3. Include re-invocation guidelines in agent definitions:** See Phase 3-4.

> See the "Step 0: Re-run Detection" section of the orchestrator template: `references/orchestrator-template.md`.

---

### Phase 6: Validation and Testing

Validate the generated harness. Detailed testing methodology: `references/skill-testing-guide.md`.

#### 6-1. Structure Validation

- Confirm all agent files are in the correct location under `.gemini/agents/`.
- Validate skill frontmatter (`name`, `description`).
- Validate agent frontmatter (`name`, `description`, `kind: local`, `model`, `tools`).
- Confirm the `tools` array is not `["*"]` and includes `ask_user` and `activate_skill`.
- Confirm reference consistency between agents.
- Confirm slash commands (`.gemini/commands/`) were **not created**.

#### 6-2. Execution Mode Validation

- Confirm each agent's I/O path (`_workspace/`) matches the next agent's input.
- Confirm the orchestrator contains logic to actually update `findings.md`, `tasks.md`, and `checkpoint.json`.
- Confirm no Claude Code-only APIs (`TeamCreate`/`SendMessage`/`TaskCreate`/subagent `run_in_background`) remain in the orchestrator.
- **When using expert_pool pattern:** Confirm `CLASSIFY()` results are recorded in the `[routing rationale]` section of `findings.md`, and that ambiguous classification delegates to `ask_user`.
- **When using handoff pattern:** Confirm both paths with and without `[NEXT_AGENT]` (ELSE branch) record task files and findings. Confirm `handle_handoff` cycle detection call is included.

#### 6-3. Skill Execution Testing

Perform actual execution tests for each generated skill.

1. **Write test prompts** — Write 2~3 realistic test prompts for each skill. Specific and natural sentences that actual users would likely input.
2. **With-skill vs Without-skill comparison** — Where possible, run with-skill and without-skill executions in parallel to verify the skill's added value.
   - **With-skill:** Perform the task with the skill activated.
   - **Without-skill (baseline):** Perform the same prompt without the skill.
3. **Evaluate results** — Evaluate output quality both qualitatively (user review) and quantitatively (assertion-based). Define assertions for objectively verifiable cases (file creation, data extraction); use user feedback for subjective cases (writing style, design).
4. **Iterative improvement loop** — When issues are found, **generalize** the feedback and modify the skill (do not make fixes specific to a particular example) → re-test → repeat until satisfied.
5. **Bundle repeated patterns** — When code commonly written by agents is discovered, pre-bundle it in `scripts/`.

Record evaluation results in `_workspace/evals/{timestamp}/grading.json` following the `grading.json` schema in `references/skill-writing-guide.md`.

> **Path distinction:** `_workspace/evals/{timestamp}/grading.json` is for **one-time validation of skills created during harness construction**. For long-term iterative skill improvement, use the `_workspace/{skill-name}/iteration-N/eval-{id}/{variant}/grading.json` structure from `references/skill-testing-guide.md`.

#### 6-4. Trigger Validation

Validate that each skill's description triggers correctly.

1. **Should-trigger queries (10)** — Various expressions that should trigger the skill (formal/casual, explicit/implicit, including follow-up task keywords).
2. **Should-NOT-trigger queries (10)** — "Near-miss" queries where the keyword is similar but a different tool/skill is more appropriate.

**Key to writing near-misses:** Queries obviously unrelated like "write a Fibonacci function" have no test value. Good test cases are **queries with ambiguous boundaries** like "extract the chart from this Excel file as PNG" (xlsx skill vs. image conversion).

Also check for trigger conflicts with existing skills at this stage (full scan of `.gemini/skills/*/SKILL.md`).

#### 6-5. Dry-Run Test

- Review whether the orchestrator skill's Step sequence is logical.
- Confirm there are no dead links in the data transfer path.
- Confirm all agent inputs match the outputs of the previous Step.
- Confirm fallback paths for each error scenario are executable.

#### 6-6. Write Test Scenarios

- Add a `## Test Scenarios` section to the orchestrator skill.
- Describe at least 1 normal flow + 1 error flow + **1 resume flow**.

---

### Phase 7: Harness Evolution

A harness is not a fixed artifact but an evolving system. New feature additions, existing agent modifications, skill updates, deprecations/consolidations, and regular operations/maintenance workflows are defined in `references/evolution-protocol.md`. When the user requests "harness inspection", "harness audit", "agent sync", "feature addition", etc., load that file first.

---

## Output Checklist

Confirm after generation is complete:

- [ ] `{project}/.gemini/agents/{name}.md` — **Agent definition file must be created**. Generate by substituting variables in `_workspace/_schemas/agent-worker.template.md` (or orchestrator). `model` ID must be verified in `_workspace/_schemas/models.md` — arbitrary guessing is prohibited.
- [ ] `{project}/.gemini/skills/{name}/SKILL.md` — Skill files (SKILL.md + `references/`·`scripts/`·`assets/` as needed).
- [ ] **New orchestrator skill must bundle 5 `references/schemas/` files** — `task.schema.json`·`checkpoint.schema.json`·`workflow.template.md`·`findings.template.md`·`tasks.template.md`. Copy as-is from SoT (`gemini-harness/references/schemas/`). Runtime Step 1.3 reads `references/schemas/{file}` via `read_file` — missing files cause immediate failure. (gemini-harness is a meta-skill and is not runtime-activated.)
- [ ] 1 orchestrator skill (includes Step 0 re-run detection + data flow + error handling + test scenarios).
- [ ] `_workspace/` standard path definitions — `_schemas/` (Step 1.3 synchronizes 5 `references/schemas/` files using `read_file`+`write_file` pairs), `workflow.md` (Stage-Step structure declaration), `findings.md`, `tasks.md`, `checkpoint.json`, `{plan_name}/` (execution artifacts), `tasks/task_{agent}_{id}.json` (per-agent status files), `evals/{timestamp}/grading.json`.
- [ ] `{project}/GEMINI.md` — Harness pointer (trigger rules + change history) registered.
- [ ] `.gemini/commands/` — **Nothing created**.
- [ ] No conflicts with existing agents/skills (including trigger conflicts).
- [ ] Skill descriptions are written assertively ("pushy") — **including follow-up task keywords**.
- [ ] SKILL.md body is within 500 lines; if exceeded, split into `references/`.
- [ ] Execution validation completed with 2~3 test prompts.
- [ ] Trigger validation (Should-trigger + Should-NOT-trigger, 10 each, 20 total) completed.
- [ ] **grading.json path distinction** — one-time harness build validation: `_workspace/evals/{timestamp}/grading.json` / long-term iterative improvement: `_workspace/{skill-name}/iteration-N/eval-{id}/{variant}/grading.json` (mixing paths prohibited).
- [ ] **Context and checkpoint check step in Orchestrator Step 0** (distinguishing initial / follow-up / partial / resume) exists.
- [ ] **GEMINI.md change history** records additions, deletions, and modifications of agents/skills.
- [ ] No Claude Code-only APIs (`TeamCreate`/`SendMessage`/`TaskCreate`/subagent `run_in_background`) in use — since Gemini CLI has no such team APIs, inter-agent communication is replaced with file-based brokering via `_workspace/tasks/task_{agent}_{id}.json`.

---

## References

- **Usage Case Catalog (8 trigger utterances + mode mapping + non-trigger utterances):** `references/usage-examples.md` — read first when receiving a new domain and match the scenario.
- **7 Architecture Patterns + Agent Definition Structure + Tool Mapping:** `references/agent-design-patterns.md`
- **Advanced Orchestrator Template** (Step 0~5 pseudocode, checkpoint.json schema, Split Task Schema): `references/orchestrator-template.md`
- **Orchestrator Procedures & Principles** (error handling decision tree, blocked_protocol, handle_handoff, description keywords, writing principles): `references/orchestrator-procedures.md`
- **Real-world Collaboration Examples** (pattern index + pattern selection guide + artifact pattern summary): `references/team-examples.md` / Example details: `references/examples/team/01~05-*.md`
- **Skill Writing Guide** (writing patterns, examples, data schema standards, orchestrator writing rules §7-5, **flat Step → Stage-Step migration §7-6**): `references/skill-writing-guide.md`
- **Skill Testing Guide** (testing/evaluation/trigger validation/iterative improvement): `references/skill-testing-guide.md`
- **QA Agent Guide** (integration coherence validation, boundary bug patterns, shell background usage, 7 real bug case studies): `references/qa-agent-guide.md`
- **Harness Evolution Protocol** (feedback incorporation, change history, operations/maintenance workflow): `references/evolution-protocol.md`
- **Existing Extension Phase Selection Matrix** (determining execution phase by change type): `references/expansion-matrix.md`
- **Stage-Step Workflow Guide** (workflow.md spec, checkpoint.json schema, Step/Stage transition protocol): `references/stage-step-guide.md` / 5 examples: `references/examples/step/01~05-*.md` / 6 test scenarios: `references/examples/step/test-scenarios.md`
- **workflow.md Writing Template** (write to `_workspace/workflow.md` after variable substitution): `references/schemas/workflow.template.md`
