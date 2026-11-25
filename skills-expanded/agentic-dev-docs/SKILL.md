---
name: agentic-dev-docs
description: Strict manual-trigger skill for docs-first agentic software development planning. Use only when the user explicitly names `agentic-dev-docs`, says `use agentic-dev-docs skill`, invokes `$agentic-dev-docs`, or directly asks to run this exact skill.
---

# Agentic Dev Docs

Version: 0.7.0

## Manual Trigger Only

Use this skill only when the user explicitly names `agentic-dev-docs`, `use agentic-dev-docs skill`, `$agentic-dev-docs`, or asks to run this exact skill. Do not auto-trigger for ordinary planning, coding, docs, or multi-agent discussion.

## Purpose

Turn a project idea or task spec into a docs-first development control pack. The pack lets a new main-control development session read startup docs, confirm it is the single A main controller, create or reuse workstreams from the project shape, coordinate implementation, testing, Review, progress audit, and handoff.

## Phase Boundary

Planning and documentation generation are not product implementation.

During requirements, collaboration design, plan, and documentation generation:
- Do not create product code, scaffolds, dependencies, codegen outputs, migrations, or dev servers.
- Do not modify product code directories.
- Generate or edit development docs only after the user confirms the plan or explicitly asks to implement the documentation plan.

Main-control development execution is a separate phase. It starts only when the user opens a new session with `00_新窗口启动提示词.md` or explicitly asks to start from `总控开发入口.md`. In that phase, implementation workstreams may write only within their authorized scopes.

## Hard Rules

1. Exactly one `A-main-control`.
2. A main control coordinates, decides conflicts, maintains progress, schedules Review, audits, and reports. It does not implement product-code work in multi-agent execution.
3. Product code, schema, OpenAPI, typed client, tests, and deployment-script changes must be assigned to an authorized workstream or logical workstream.
4. Human labels such as Developer A, Developer B, QA, and Tech Lead are responsibility or Review labels, not agent identities. Convert them to project-shaped workstreams or Review owners.
5. `A-main-control` must not appear as implementer, writable owner, or primary assignee for product implementation tasks. If it does, the generated docs are wrong and must be fixed.
6. Workstreams come from the project shape, not fixed frontend/backend/SDK templates.
7. Every writable role must be in the permission matrix before assignment.
8. Contract, Review, audit, and explorer roles are read-only unless the docs explicitly authorize narrow writes.
9. Real subagents are created only when the user asks for multi-agent, subagent, delegation, or parallel development. Otherwise use logical workstream records.
10. Final closeout is serial: environment check -> implementation evidence -> Review pass -> audit pass -> A reports to user.

## A Main Control Must Not "Just Do It"

If a task has been assigned to a workstream, A main control must not do it directly because it is small, convenient, or already open.

To move a workstream task to A direct execution, all three must happen first:
- User explicitly authorizes the change.
- Permission matrix is updated.
- Progress docs record the responsibility change.

If no real subagent exists, A still must create a logical workstream record and execute under that workstream's scope, log, evidence, and Review rules. Do not mix A-control identity with worker identity.

## Project Shape First

Before creating workstreams, document the project shape:
- Project type: CLI, Web, desktop, mobile, AI app, data app, multi-service system, docs/paper project, or other.
- Deliverables: code, config, scripts, docs, tests, deployment, data, model.
- Tech stack and runtime: language, framework, package manager, database, browser, container, OS.
- Parallel boundaries: independent directories, modules, services, pages, commands, data domains, doc chapters.
- Shared risks: API, DTO, schema, migration, typed client, shared components, config, deployment scripts, permissions, security.

## Workstream Rules

Each writable workstream must have:
- instance name;
- type: implementation-workstream, docs-workstream, contract-review, test-review, security-review, progress-audit, one-shot-investigation;
- lifecycle: persistent, workstream, or one-shot;
- whether multiple instances are allowed;
- reuse scope;
- writable scope;
- forbidden scope;
- required evidence;
- default model;
- recommended reasoning effort: low, medium, high, xhigh, or max;
- Review owner;
- creation condition;
- close condition.

Typical generated names should match the project, such as `sdk-cli-workstream`, `admin-ui-workstream`, `storage-executor-workstream`, `data-schema-workstream`, or `docs-revision-workstream`.

## Subagent Model Policy

- Default real-subagent assignment: `model: gpt-5.6-luna`, `reasoning_effort: max`.
- Every real-subagent assignment must explicitly include both `model` and `reasoning_effort`.
- Precedence: task declaration -> workstream permission-matrix declaration -> global default.
- If only one field is declared, the other field falls back independently to the global default.
- Explicit model values are passed through without a skill-level allowlist.
- If the runtime cannot accept the requested model or reasoning effort, record `BLOCKED-HUMAN` with the exact error and do not silently downgrade.
- Logical workstreams record requested model and effort as metadata; real subagents receive them at creation or assignment.

## Reasoning Effort Policy

Use reasoning effort as a task-risk control. When real subagents or APIs support it, `A-main-control` must set or request the selected level during assignment. When direct setting is unavailable, record the recommended level in the task assignment, workstream registry, or permission matrix.

- Real subagents must not silently inherit the parent session reasoning level by default.
- Each time `A-main-control` creates or assigns a real subagent, it must explicitly pass or request `reasoning_effort` from the task declaration, permission matrix, or global default.
- Precedence is: task declaration -> permission matrix declaration -> global default `max`.
- If a workstream has no declared effort, use `max` and record the global-default source in task progress.
- If cost, speed, or tool limits require a different level, record the reason first and get `A-main-control` confirmation before assigning the task.
- `A-main-control` coordination may use high.
- Final decisions, cross-workstream conflicts, permission defects, and final audits may use xhigh.
- Ordinary implementation workstreams may explicitly declare medium.
- Simple lookup, formatting, organization, and low-risk docs cleanup may explicitly declare low or medium.
- Contract review, security review, progress audit, and high-risk Review may explicitly declare high; final closeout audit may explicitly declare xhigh.
- These role-based values override global `max` only when explicitly recorded in the task or permission matrix.
- `max` is a valid explicit global or task-level effort.

## Explicit Skill Routing

Use explicit skill routing only when the user specifies skills. If the user does not specify skills, do not invent, infer, or add default skill requirements.

Before plan generation, parse user-provided skill routing lines into two layers:

- Global skill baseline: applies to `A-main-control` and every real or logical workstream. Recognize inputs such as `all agents use skill`, `所有智能体使用skill`, `所有智能体（包括主子）使用skill`, and `A主控和所有子智能体使用skill`.
- Task or workstream skill routing: applies only to a task type, named workstream, Review, audit, or one-shot assignment. Recognize inputs such as `执行<任务类型>任务的子智能体使用skill`, `<workstream>使用skill`, and `<任务>交给<workstream>，使用skill`.

Skill names may be separated by `+`, `,`, `，`, `/`, or whitespace. Preserve the user-specified names as written, normalize only obvious spacing, and do not replace them with unrelated skills.

When skill routing exists, the generated plan and docs must record:
- global skills, if any;
- task/workstream-specific required skills, if any;
- optional or forbidden skills, only if the user explicitly states them;
- exact trigger wording for task assignment, such as `use playwright skill`;
- fallback behavior when a required skill is unavailable.

`A-main-control` must merge global skills with task/workstream-specific skills before assigning work, record the resulting required skills in task progress, and include the exact trigger wording in the assignment. If a required skill is unavailable, pause or follow the documented fallback instead of pretending the skill was used.

## Reuse Rules

Only one effective instance may exist for the same lifecycle and reuse scope.

- `persistent`: one global primary instance, such as the single A main control.
- `workstream`: reuse for the same module, directory, deliverable, or context chain.
- `one-shot`: use only for isolated investigation, validation, or Review. If later tasks need the same context, upgrade to `workstream`.
- Record every reuse: task, instance name, reason, latest output location.
- If duplicates exist, A pauses assignment, chooses the most complete instance as primary, merges other outputs into the registry/progress docs, then closes duplicates.
- Do not create a duplicate workstream because there are many tasks, a window is long, or switching seems convenient.

## Permission Matrix

Every output pack must include a permission matrix. Minimum columns:

| Column | Required content |
|---|---|
| Role / instance | exact name |
| Type | A main control, implementation-workstream, review, audit, docs, one-shot |
| Default agent | current session, worker, explorer, logical instance |
| Default model | requested model; defaults to `gpt-5.6-luna` |
| Product-code write | yes, no, or restricted |
| Writable scope | directories, file types, module, or docs |
| Forbidden scope | shared contracts, other modules, secrets, build outputs, unrelated docs |
| Required evidence | tests, build, screenshot, log summary, Review, audit |
| Recommended reasoning effort | low, medium, high, xhigh, or max |
| Skill routing | global inherited skills and task/workstream-specific required skills, or blank when the user specified none |
| Review owner | exact role |
| Close condition | objective proof |

Roles outside the matrix cannot modify product code.

## Phase Workflow

1. Requirements clarification: ask only questions that change the plan.
2. Collaboration design: offer 2-3 options, always with one A main control.
3. Plan generation: produce a decision-complete plan.
4. Documentation generation: create docs only after plan confirmation.
5. Main-control handoff: new session uses startup docs to execute.

## Plan Must Include

- Project summary and project shape.
- Frozen decisions and assumptions.
- Documentation set size: minimal, standard, or complete. Prefer references in `references/document-set.md` over repeating long lists.
- Docs to create.
- Workstream registry, reuse strategy, and permission matrix.
- Recommended reasoning effort in workstream registry, permission matrix, and task assignments. For real subagents, task assignment must explicitly pass or request `reasoning_effort` from the task declaration, permission matrix, or global default `max`.
- Default model and explicit `model` value in workstream registry, permission matrix, and task assignments. Use `gpt-5.6-luna` + `max` when no override exists.
- Explicit skill routing only when the user specified skills: global skill baseline, task/workstream skill routing, trigger wording, and fallback.
- Contract-first rule for APIs/data.
- Startup environment checks.
- Code commit/push policy. A verified independent task may create a local commit. `git push`, PR creation, and remote branch operations require explicit plan or user authorization.
- Human-blocking policy. Record `BLOCKED-HUMAN`, skip the blocked point, continue independent work, and retry at phase boundaries or dependency changes.
- Review and audit gates.
- Acceptance criteria.
- Mapping from human responsibility labels to workstreams or Review owners.

Implementation tasks in the plan must be assigned to workstreams, not A main control.

## Documentation Set Guidance

Use existing references and templates instead of copying long content into the skill:
- `references/workflow.md`
- `references/agent-roles.md`
- `references/document-set.md`
- `references/templates.md`
- `references/examples.md`
- `assets/doc-templates/`

The generated pack must include at least:
- startup prompt with a separate copyable `/goal` execution objective;
- startup environment checklist;
- main-control entry;
- requirements/spec;
- user stories;
- collaboration rules;
- A main-control rules;
- workstream rules;
- progress doc;
- human test checklist;
- docs acceptance checklist.

## Self-Check Before Completion

Before claiming docs are complete, verify:
- startup prompt exists and clearly enters main-control execution phase;
- startup prompt includes a separate copyable `/goal` execution objective;
- `/goal` objective states that verified tasks may be committed locally, while push and PR remain forbidden without explicit authorization;
- startup environment checklist exists;
- main-control entry exists;
- progress doc exists;
- there is exactly one A main control;
- project shape is documented before workstreams;
- each role has lifecycle, reuse scope, multi-instance rule, writable scope, forbidden scope, evidence, Review owner, and close condition;
- each real subagent or logical workstream has a recommended reasoning effort;
- each real subagent or logical workstream has a requested model;
- each real subagent assignment explicitly passes or requests both `model` and `reasoning_effort`, or records global-default fallback;
- any reasoning effort override records cost, speed, or tool-limit reason and `A-main-control` confirmation;
- runtime model/effort failures are recorded as `BLOCKED-HUMAN` with exact evidence;
- if the user specified skills, global and task/workstream skill routing are recorded in the plan, startup prompt, main-control entry, collaboration rules, task progress pattern, and docs acceptance checklist;
- if the user did not specify skills, generated docs do not invent skill requirements;
- permission matrix exists;
- product implementation tasks are assigned to workstreams, not A main control;
- human responsibility labels are not converted into A implementation tasks;
- reuse and duplicate-instance handling are explicit;
- A cannot do assigned workstream tasks without explicit user authorization, matrix update, and progress record;
- final audit is a required gate;
- all selected document sets include `用户故事.md` with traceable acceptance criteria;
- verified independent tasks may have local commits, while push and PR require explicit authorization;
- human test checklist exists;
- docs acceptance checklist exists;
- no unfilled placeholder markers remain unless the user requested a blank template.

## Failure Handling

- Requirements too vague: do not generate plan; ask 1-3 material questions.
- User skips plan and asks for docs: give a short plan summary and ask for confirmation unless they explicitly insist.
- User asks for docs and code together: split docs phase first, development phase later.
- User does not want multi-agent: use A-only flow with Review/test checklists; do not create implementation workstreams.
- Tech stack unclear: offer 2-3 options and recommend one.
- Permission matrix missing or writable scope unclear: do not assign development tasks.
- Duplicate workstreams created: pause, select primary, merge outputs, close duplicates.
- Product-code task assigned to A main control: treat as doc defect; rewrite assignment to a workstream.
- A main control already did workstream work: stop, record violation, fix matrix/progress; without explicit user authorization, return work to the workstream.
