---
name: zhuluyou
description: Use when the user expresses stable preferences, recurring requirements, project habits, UI taste, architecture rules, skill-pack governance opinions, prompt behavior expectations, repeated corrections, or personal workflow patterns that should influence future Codex work without guessing or storing sensitive data.
---

# Zhuluyou

## Purpose

Maintain a durable, auditable user preference profile. This is a user-model governance skill, not a casual memory dump.

The goal is to improve future work by recording stable preferences about how the user wants software projects, UI, prompts, skills, documentation, and collaboration handled.

Use with `context-engineering-pro`, `project-assistant`, `skill-governance`, and `skill-distillation-pro`.

## Core Principle

Only record preferences that are:

- Explicit or repeatedly demonstrated.
- Stable across tasks.
- Useful for future work.
- Non-sensitive.
- Separable from project-specific facts.

Do not record guesses.

## Profile Files

- `references/profile.md`: durable user profile.
- `references/update-policy.md`: detailed update policy, evidence levels, and conflict rules.
- `user-skills/INDEX.md`: index of evolved user skills.
- `user-skills/*.md`: executable user preference skills that evolve over time.
- `user-skills/memory-reliability-style.md`: single managed memory gateway and macOS/project-root reliability rules.
- `user-skills/memory-stack-style.md`: L0-L3 memory read stack and context budget rules.
- `user-skills/memory-evidence-style.md`: evidence, source hash, invalidation, and superseding rules.
- `user-skills/global-memory-capture-style.md`: active/passive global memory capture rules.
- `user-skills/knowledge-graph-memory-style.md`: optional normalized project knowledge graph activation and schema rules.
- `user-skills/skill-lifecycle-governance-style.md`: skill install/delete/route/audit lifecycle and poisoning checks.
- `templates/user-skill-template.md`: template for new user skills.
- `scripts/update-preference.ps1`: append structured entries.
- `scripts/capture-global-memory.mjs`: macOS-first global profile capture helper.
- `scripts/resolve-memory-context.mjs`: read-only memory context decision helper.
- `scripts/audit-project-memory.mjs`: project memory structure audit and optional initialization helper.
- `scripts/init-project-memory.mjs`: conversational project memory initialization entry for "初始化本项目"; self-checks, initializes, summarizes, and re-audits.
- `scripts/audit-memory-system.mjs`: full v2.2 memory system audit helper.
- `scripts/summarize-project-memory.mjs`: compact project memory summary helper.
- `scripts/maintain-memory.mjs`: scheduled/manual memory maintenance runner for global and project checks.
- `scripts/setup-project-maintenance.mjs`: idempotent project setup for `docs/memory/maintenance.json` and Git pre-push audit hook.
- `scripts/audit-skill-lifecycle.mjs`: snapshot and audit active skill inventory changes.
- `scripts/skill-safety-scan.mjs`: shared static safety and local antivirus scan helper for staged skills.
- `scripts/install-skill-staged.mjs`: mandatory staged skill install gate; scans first, classifies as explicit-only by default, then validates.

## What To Record

### Communication

- Language and tone.
- Role header requirements.
- Desired answer length.
- Formatting requirements.
- Phrases or rituals explicitly required by the user.

### Product And Project Focus

- Primary software categories.
- Preferred platforms.
- Common architecture style.
- Product quality expectations.
- Preferred development workflows.

### UI And Design Taste

- Preferred UI style.
- Rejected UI patterns.
- Density, layout, color, motion, accessibility expectations.
- Product categories needing special design treatment.

### Engineering Standards

- File/module structure.
- Documentation expectations.
- Testing and verification expectations.
- Production readiness gates.
- Security, performance, deployment preferences.

### Skill And Prompt Governance

- Preferred external skill sources.
- Rules for importing, deleting, merging, or adapting skills.
- Prompt versioning expectations.
- Requirements for resource-backed skills.

### Automation And Memory

- When to update `.ai_project.md`.
- When to update `docs/`.
- When to update user profile.
- How project evolution should be recorded.
- How `docs/INDEX.md`, `docs/project-structure.md`, roadmap, maintenance docs, and ADRs should be maintained.
- When to activate project knowledge graph memory for relationship lookup and impact analysis.

## What Not To Record

- API keys, secrets, tokens, passwords.
- Account identifiers, private personal data, payment data.
- One-off task instructions.
- Temporary emotions or frustration unless converted into a stable work rule.
- Private information about third parties.
- Unverified assumptions.

## Evidence Levels

| Level | Meaning | Action |
|---|---|---|
| E1 Explicit | User directly states a lasting preference | Record as Active |
| E2 Repeated | Same preference appears in 2+ separate corrections/requests | Record as Active |
| E3 Inferred | Strong pattern but not directly stated | Add to Candidate Preferences |
| E4 Project-local | Applies only to current project | Route to `.ai_project.md` / `docs/` |
| E5 One-off | Applies only to current turn | Do not record |

## Update Decision

Before updating, classify:

```text
Stable user preference -> zhuluyou
Project-specific rule -> AGENTS.md / .ai_project.md / docs/
Skill-pack rule -> MANIFEST.md + zhuluyou if user-level
Temporary task detail -> no memory
Unclear but possibly recurring -> Candidate Preferences
Sensitive/private -> do not record
```

## Conflict Rules

When new preference conflicts with old:

1. Prefer latest explicit user instruction.
2. Mark old entry as `Superseded`, not deleted.
3. Add evidence for the change.
4. If conflict is ambiguous, add candidate and ask when needed.

User preferences never override:

- System/platform safety.
- Current explicit user instruction.
- Project-local rules when working inside that project.
- Verifiable facts and official documentation.

## Profile Update Workflow

1. Identify preference statement or repeated behavior.
2. Classify evidence level.
3. Decide destination: `profile.md`, `AGENTS.md`, `.ai_project.md`, docs, MANIFEST, or no memory.
4. Use `scripts/update-preference.ps1` for simple appends.
5. For conflicts/superseding, edit `profile.md` directly and preserve history.
6. Mention update briefly in final answer.

## User Skill Evolution

Use user skills when a preference has become an executable workflow, not merely a profile fact.

Read `user-skills/INDEX.md` first when this skill is triggered. Then read the matching user skill files according to their `Read When` rules.

## First-Run Initialization

If the user profile or communication user skill lacks a preferred address, communication preference, primary development focus, or stable workflow habits, run a light initialization.

Ask at most three questions:

1. What should Codex call the user?
2. Should Codex default to concise execution, or propose a plan before executing?
3. Which long-term habits matter most: project docs, UI taste, code quality, verification, skill governance, or something else?

Do not block urgent work. If the user asks for a direct fix, production debugging, or a clear implementation task, do the task first and mention that preference initialization can be completed later.

Save answers to:

- `references/profile.md`
- `user-skills/communication-style.md`
- other matching `user-skills/*.md` when the answer becomes executable workflow guidance

Default read routing in V5.0:

| Task | Read |
|---|---|
| Every turn | `user-skills/INDEX.md`, `user-skills/routing-core.md`, `user-skills/communication-style.md` |
| Memory routing, index repair, project root discovery | `user-skills/memory-reliability-style.md`, `user-skills/memory-stack-style.md`, `user-skills/global-memory-capture-style.md` |
| Tone, persona, user mood | `user-skills/persona-style.md`, `user-skills/emotion-support-style.md` |
| Normal responses, final summaries, progress updates, reviews | `user-skills/communication-style.md` |
| Code/config/test changes | `user-skills/role-coder-style.md`, `user-skills/skill-router-style.md` |
| Debugging | `user-skills/role-debugger-style.md`, `user-skills/debug-reuse-style.md` |
| Project file changes, docs, `.ai_project.md`, `AGENTS.md`, project memory | `user-skills/role-project-assistant-style.md`, `user-skills/project-memory-style.md`, `user-skills/memory-evidence-style.md`, `user-skills/knowledge-graph-memory-style.md` when KG activation may apply |
| UI design, redesign, polish, frontend product screens, visual QA | `user-skills/ui-taste-style.md`, `user-skills/skill-router-style.md` |
| Prompt/skill installation, deletion, merging, versioning, distribution | `user-skills/role-rule-governor-style.md`, `user-skills/skill-lifecycle-governance-style.md`, `user-skills/skill-router-style.md` |
| Long-term preference or user profile growth | `user-skills/user-profile-growth-style.md`, `user-skills/global-memory-capture-style.md` |
| Automation/high-risk boundaries | `user-skills/automation-boundary-style.md` |

`profile.md` records what the user prefers. `user-skills/*.md` records how to act on those preferences.

Evolution stages:

| Stage | Meaning | Storage |
|---|---|---|
| S1 Profile | A stable preference is recorded | `references/profile.md` |
| S2 Candidate | Repeated preference may become a workflow | `user-skills/INDEX.md` |
| S3 Active Skill | Has triggers, rules, forbidden behaviors, and acceptance checks | `user-skills/<skill-name>.md` |
| S4 Evolving | Updated after user corrections or repeated use | user skill change log |
| S5 Deprecated | No longer applies or conflicts with newer preference | mark status, do not delete silently |

Create or update a user skill only when:

- The preference is E1 or E2.
- It applies across projects or many tasks.
- It can be expressed as triggers and behaviors.
- It will improve future work.
- It contains no sensitive or project-private data.

Do not create user skills for one-off requests, project-only facts, secrets, or guesses.

User skill files should include:

- Name
- Status
- Purpose
- Trigger Conditions
- Behavior Rules
- Forbidden Behaviors
- Output / Acceptance Checks
- Related Profile Entries
- Change Log

When a user skill is created or changed, update `user-skills/INDEX.md`.

## Output Contract

When updated:

```markdown
用户画像：
- 更新 `zhuluyou/references/profile.md`
```

When a user skill is created or updated:

```markdown
女助理：
- 更新 `zhuluyou/user-skills/<skill-name>.md`
```

When not updated:

```markdown
用户画像：
- 未更新：本次是临时任务要求，不是长期偏好。
```

Only include this section when user profile was relevant.

## Common Mistakes

- Recording too much.
- Recording project facts as user preferences.
- Recording guesses as rules.
- Letting old preferences silently conflict with new ones.
- Creating a profile so broad it stops being useful.
