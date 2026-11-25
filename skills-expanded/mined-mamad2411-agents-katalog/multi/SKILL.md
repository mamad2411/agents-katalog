---
name: multi
description: Parallel subagent orchestration kernel — spawn invariants, model routing, generic prompts and synthesis. Entry skills supply job recipes (explore, research, council review, …). Use when a task splits into independent slices and parallel work improves coverage, speed, or confidence.
---

# Multi

**Source of truth for** parallel subagent orchestration.

<!-- doc-meta: owner=eng | last-reviewed=2026-07-14 -->

Parallel independent subagents via the host **Task** tool (Cursor: **Subagent**). **Orchestration kernel only** — entry skills own job recipes and domain-specific synthesis.

## When to Use

- Task splits into 2+ independent slices (explore, research, gather, council dispatch)
- Parallel work improves coverage, speed, or confidence

Skip when: one agent suffices, work is sequential, or user wants a single pass — see [Fit check](#fit-check).

## Quick reference

| Need                         | Where                                                          |
| ---------------------------- | -------------------------------------------------------------- |
| Must-spawn invariants        | [Non-negotiables](#non-negotiables)                            |
| Model routing (cost + fit)   | [references/model-routing.md](references/model-routing.md)     |
| Generic task prompt          | [references/task-prompt.md](references/task-prompt.md)         |
| Per-member output shape      | [references/member-schema.md](references/member-schema.md)     |
| Generic consolidated report  | [references/output-format.md](references/output-format.md)     |
| Agent discovery (mechanical) | [references/agent-discovery.md](references/agent-discovery.md) |

## Non-negotiables

When this skill applies (user attached `multi`, an entry skill invokes parallel dispatch, or the plan chose `N ≥ 2` members):

1. **Spawn real members** — Use the host **Task** tool once per planned member with chosen `subagent_type` and model per [Model assignment](#model-assignment). Parallel `read_file` / `grep` / other tools are **not** substitutes for member runs.
2. **Synthesis runs after members** — The [synthesis gate](#synthesis-gate) merges member outputs. Writing a consolidated report **without** running those `Task` calls first is a **violation**, not an optimization.
3. **Forbidden rationalizations** — Do not skip spawns because you already read the repo, expect overlapping findings, want lower latency, want to save tokens, or the diff is “docs-only,” “skills/agent-infra,” or “single theme.”
4. **Valid skips** — Omit parallel spawns only when: the user declines or asks for a single pass; the job matches [Fit check](#fit-check) **and no entry skill already invoked parallel dispatch**; the host cannot run `Task`; or only one member was planned.

**Model routing:** Apply [Model assignment](#model-assignment) and [model-routing.md](references/model-routing.md) per member. **Invariant:** `Parent model = Auto` + no user model override ⇒ every Task/Subagent call **omits** the `model` property. Tier labels (Fast/Standard/Premium) never select a slug under an Auto parent. Explicit slugs only for (1) a user-named member model in the host enum, or (2) named-parent tier routing after Auto is ruled out. On usage-limit / credit exhaustion → [Usage-limit retry](#usage-limit-retry).

## Fit check

**Use multi** when members are independent and parallel work improves coverage, speed, or confidence — e.g. multi-source gathering, broad exploration, orthogonal research topics, or mixed gather passes.

**Skip multi** when the task fits one agent, work is sequential, members would duplicate without adding confidence, or the user wants a single authoritative pass.

**Entry-skill carve-out:** When `code-review` (or another entry skill) already invoked parallel dispatch / council, Fit check does **not** apply. Do not re-litigate “one agent suffices.” Follow that skill’s member budget and [Non-negotiables](#non-negotiables).

## Dispatch modes

- **Coverage** — Split by source, subsystem, domain, or artifact. Example: one member maps data flow, another maps call sites.
- **Perspective** — Same material, distinct stance. Model diversity alone is not enough if prompts are identical.

**Hard rule:** Never run parallel members with identical model plus identical prompt. When all members inherit Auto, diversify via distinct prompts and/or stances — shared Auto is expected.

## Workflow

### 1. Classify

Load the entry skill's recipe when one applies; otherwise plan manually:

- Job type: `research` | `explore` | `gather` | `mixed`
- Source of truth: `web` | `repo` | `plan`
- Goal: coverage | perspectives | both
- Independence: if members need each other's output, this is sequential — do not use `multi`

### 2. Plan and spawn

1. **Discover** — [agent-discovery.md](references/agent-discovery.md) when council agents may apply; otherwise pick host built-in `subagent_type` values directly.
2. **Dispatch plan** — write before spawning:

```markdown
Task: [What the user asked]
Classification: [research / explore / gather / mixed]
Source of truth: [web / repo / plan]
Goal: [coverage / perspectives / both]

Parent model: [Auto | <named model>]
User model overrides: [none | member=slug, …]
Auto reachable: [inherit-auto | model=auto | no]
Host supports: [Task model enum values checked]
Billing pool: [first-party | API | mixed]
Explicit model slugs used: [none | slug + slice-fit reason + cost note]
Fast variants used: [none | slug + explicit latency reason]

Selected members:

- [subagent_type] · tier=[Fast|Standard|Premium] · model=[inherit-auto | slug] · stance=[id or n/a]: [sub-task and expected output]
- [subagent_type] · tier=[Fast|Standard|Premium] · model=[inherit-auto | slug] · stance=[id or n/a]: [sub-task and expected output]

Why these members: [brief justification]
Synthesis plan: [how outputs will be merged or adjudicated]
```

`inherit-auto` is a **dispatch-plan sentinel only** — it means omit the Task/Subagent `model` argument. It is not a model slug. Never translate `inherit-auto` into an arbitrary explicit slug. Pass `model=auto` only when the host Task enum explicitly includes `auto`.

3. **Pre-spawn gate** — run [Pre-spawn model-routing gate](#pre-spawn-model-routing-gate) and fail closed on contradictions. Do not issue Task/Subagent calls until every member has a resolved model action that agrees with the plan.
4. **Spawn** — one Task per member in parallel. Compose prompts per [task-prompt.md](references/task-prompt.md). **Plan vs tool syntax:** plan `model=inherit-auto` → omit `model` on the tool call; plan `model=<slug>` → pass `model="<slug>"` only when that slug is in the host enum. On usage/credit failures → [Usage-limit retry](#usage-limit-retry).

Member planning defaults:

- Research → one member per independent topic
- Exploration → one member per area, subsystem, or artifact type
- Gathering → one member per source of truth or coverage lens
- Mixed → combine roles only when slices stay independent

### 3. Synthesize

Apply the [synthesis gate](#synthesis-gate).

## Synthesis gate

**Prerequisite:** At least one completed `Task` per planned member (unless valid skips above apply). If no members ran, do not fabricate a multi report.

After members return:

1. Merge findings that agree; state once with the highest shared confidence.
2. Preserve conflicts — do not flatten disagreements.
3. High-stakes contradiction → single sequential tiebreaker per [model-routing.md](references/model-routing.md) (prefer Auto, else most appropriate stronger model) or escalate to the user.
4. Write one consolidated report per [output-format.md](references/output-format.md).

Domain-specific synthesis (review filing, investigate verdicts, second-opinion sections) → entry skill recipe.

## Fallback matrix

When council agents are unavailable or the job uses host built-ins only:

| Need                    | Prefer                    | Fallback                                                         |
| ----------------------- | ------------------------- | ---------------------------------------------------------------- |
| Repo map                | `explore`                 | `generalPurpose`                                                 |
| Web research            | `docs-researcher`         | `generalPurpose`                                                 |
| Plan structure critique | `generalPurpose` + stance | council agent if in HOST and `dispatch.contexts` includes `plan` |

Log skipped council agents and chosen fallbacks in the [availability log](references/agent-discovery.md#availability-log-required-in-dispatch-plan).

## Model assignment

Use the Task tool's allowed `model` enum from the current host. Never invent slugs. Full cost model, strength cards, and escalation matrix → [model-routing.md](references/model-routing.md).

**Optimize for cheapest good enough** — not most capable by default.

### Routing precedence (canonical order)

Resolve every member’s model action in this order — do **not** run tier→slug mapping before parent-aware routing:

1. **User-requested member model** — if the user named a model for this member and it is in the host enum, pass that exact slug. If unsupported, report the unsupported request; do not invent or substitute a different slug.
2. **Auto parent → inherit Auto** — omit the Task/Subagent `model` argument. Log `model=inherit-auto`. Tier metadata (including Premium) must not select a slug.
3. **Named parent → explicit tier-to-slug routing** — only after confirming the parent is named. Prefer `model=auto` when that enum value exists; otherwise map tier via [model-routing.md](references/model-routing.md) (Cursor cost first, cheapest good enough, most appropriate escalation).
4. **Usage/rate-limit failure → retry once via Auto inheritance** — same member, prompt, type, and stance; omit `model` (or pass `model=auto` if that is how Reach Auto works for a named parent with `auto` in enum).
5. **If the Auto retry fails** — document the missing member; do not invent output.

**Hard invariant:** `Parent model = Auto` + `no user model override` ⇒ the spawned Task/Subagent call has **no** `model` property.

### Parent-aware routing (Auto first)

Detect whether the **parent chat** is on host **Auto** (auto model selection) or a **named** model.

| Parent                          | Initial member `model`                 | Notes                                                                                              |
| ------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Auto**                        | **Omit** `model` (inherit parent Auto) | Default for **all** normal members, including Standard/Premium tiers. User-named model still wins. |
| **Named**, enum includes `auto` | Pass `model=auto` for normal members   | Log `model=auto`. Explicit slugs only for justified named-parent escalation or user override.      |
| **Named**, no `auto` in enum    | **Cannot reach Auto**                  | For cost-controlled `N ≥ 2`, **stop** and ask user to switch parent to Auto — do not silent-spend. |
| User named a model for a member | That slug (must be in enum)            | Overrides Auto inherit and cost routing; record override in dispatch plan.                         |

**How to get Auto on Task:**

| Situation                                          | Member `model`                                                                   |
| -------------------------------------------------- | -------------------------------------------------------------------------------- |
| Parent is **Auto**                                 | **Omit** `model` (inherits parent Auto). Log `model=inherit-auto`.               |
| Parent is **named**, but Task enum includes `auto` | Pass `model=auto` (only when the slug is in the current enum).                   |
| Parent is **named**, and `auto` is **not** in enum | You **cannot** reach Auto via Task. Omit `model` only inherits the named parent. |

Do **not** invent `auto` when it is absent from the enum. Do **not** treat “omit `model`” as Auto when the parent is on a named model — that still bills/uses the parent’s named model.

**Plan vs tool syntax** (repeat at spawn time):

| Dispatch-plan value     | Actual Task/Subagent arguments          |
| ----------------------- | --------------------------------------- |
| `model=inherit-auto`    | **Omit** the `model` property           |
| `model=auto`            | Pass `model="auto"` (enum must list it) |
| `model=<explicit slug>` | Pass `model="<explicit slug>"`          |

Record in the dispatch plan: `Parent model`, `User model overrides`, `Auto reachable`, `Host supports`, `Billing pool`, `Explicit model slugs used`, `Fast variants used`.

**Usage-constrained mode:** If the user says they are out of credits / on usage limits, or the first member fails for that reason, route **all** members (remaining + retries) via [Reach Auto](#reach-auto) below — do not keep assigning paid/API slugs.

### Pre-spawn model-routing gate

**Mandatory before any Task/Subagent call.** If any check fails, do not spawn — correct the plan first.

- [ ] Parent model mode recorded (`Auto` or named)
- [ ] Any user model override recorded (`User model overrides: none | …`)
- [ ] Every member has a resolved model action (`inherit-auto` | `auto` | explicit slug)
- [ ] Auto-parent members without user overrides use `model=inherit-auto` in the plan
- [ ] Their actual spawn calls **omit** `model` (plan `inherit-auto` must not become a tool `model` property)
- [ ] Explicit slugs appear only for named-parent routing or recorded user overrides
- [ ] Every explicit slug exists in the current host Task `model` enum
- [ ] Model diversity never causes tier escalation or an Auto override (diversify prompts/stances instead)
- [ ] Premium / Standard tier metadata did not override an Auto parent
- [ ] Plan text and actual tool arguments agree

### Fail closed (do not spawn)

These contradictions are **hard stops** — correct before any member is spawned; do not rely on informal noticing:

1. Plan says `Parent model: Auto` but any member has an explicit slug without a recorded user override → **do not spawn**. Correct that member to `model=inherit-auto` and omit the tool argument.
2. Plan says `model=inherit-auto` but the generated Task/Subagent call contains a `model` property → **invalid**. Remove `model` before dispatch.
3. Plan says named parent and an explicit slug (or `model=auto`) is required by named-parent rules but absent → resolve per [Routing precedence](#routing-precedence-canonical-order) or fail clearly; do not spawn half-routed.
4. User requested an unsupported slug → report unsupported; do not substitute another model.

### Explicit routing (named parent only)

When the parent is **named** and Auto is unreachable (or a documented escalation under a named parent is justified and the user accepts spend), route per [model-routing.md](references/model-routing.md):

1. **Cursor cost first** — prefer first-party pool over API pool; never use throughput `fast` in `N ≥ 2` unless the user explicitly wants latency for that member.
2. **Cheapest good enough** — lowest-cost enum option still likely to succeed for the slice.
3. **Most appropriate escalation** — if cheaper paths are likely to fail, escalate to the strength card that matches the slice (Sonnet for adjudication, Sol for architecture, Codex for long tool-driven implementation, etc.) — **not** the most expensive enum entry by default.
4. **Effort ≠ fast** — raise reasoning effort for harder single-member work; do not buy `*-fast` for intelligence.

Under an **Auto** parent, do **not** enter this branch for normal members — inherit Auto instead. Host Auto selects the underlying model.

#### Tier labels (planning only — subordinate to parent-aware routing)

Tier labels still appear in dispatch plans and agent `dispatch.model.default` metadata. They describe slice difficulty for **named-parent** routing only. Under an Auto parent, keep the tier label for planning/logging but set `model=inherit-auto` and omit the tool argument.

| Tier         | Slice needs                                                                         | Named-parent routing intent                                         | Escalate when (named parent only)                                     |
| ------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Fast**     | Mechanical search, file discovery, repo mapping, narrow gather                      | Auto / cheapest non-fast good enough                                | Cross-file integration or judgment calls needed                       |
| **Standard** | Moderate reasoning, explore follow-ups, web research                                | Auto first; else cheapest mid fit per strength cards                | Conflicting sources, ambiguous adjudication, or deeper synthesis need |
| **Premium**  | Architecture blast radius, synthesis tiebreakers, explicit deepest-analysis request | Auto first; else **most appropriate** stronger model for that slice | —                                                                     |

**Pick a slug:** follow [Routing precedence](#routing-precedence-canonical-order). Tier→slug mapping runs only on the named-parent branch.

#### By job type

| Job                  | Default tier | Routing intent                      | Escalate when (named parent)                     |
| -------------------- | ------------ | ----------------------------------- | ------------------------------------------------ |
| `explore` / `gather` | Fast         | Auto / cheapest non-fast            | Cross-file integration or architectural judgment |
| `research` (web)     | Standard     | Auto first                          | Conflicting sources or policy/legal ambiguity    |
| `mixed`              | Per slice    | Per slice shape in model-routing.md | —                                                |

Per-agent tier defaults → agent dispatch config + [model-routing.md](references/model-routing.md).

#### Diversity

Never escalate price, choose `fast`, or override Auto just to diversify. Diversify prompts and/or stances first. When the parent is on Auto, shared Auto across members is expected and correct. If `N ≥ 2` share the same `subagent_type` under a named parent with explicit models already justified, prefer distinct models **within the same tier / similar cost** only when the user wants diversity — **do not escalate tier just to diversify.**

### Anti-fast (parallel)

For `N ≥ 2`, do **not** pass `*-fast` or high-fast bundles unless the user explicitly requests lower latency for that member. High-fast slugs are sequential escalations only (named parent or user override). See [model-routing.md](references/model-routing.md).

### Reach Auto

Use this as the **default** model path for normal members, and whenever members must run on host Auto (usage-constrained mode, or a usage-limit retry):

1. If parent is **Auto** → omit `model` (inherit). Log `model=inherit-auto`.
2. Else if Task enum includes `auto` → pass `model=auto`. Log `model=auto` (add `— usage/rate limit` on retries).
3. Else → **stop assigning named/paid slugs** for cost-controlled runs. Tell the user that Auto still works for them only when the **parent chat** is on Auto (or when the host exposes `auto` in the Task enum), and ask them to switch the parent to Auto and re-run failed members. Do not claim a retry “used Auto” if you only omitted `model` under a named parent.

### Usage-limit retry

If a member **could not start**, was **stopped**, or returned an error because of **usage limits**, **rate limits**, **quota exhaustion**, or **credit exhaustion** on the chosen model:

1. Enter **usage-constrained mode** for the rest of this `multi` run.
2. Retry that **same** member once via [Reach Auto](#reach-auto). Keep the same `subagent_type`, prompt, and stance; change only the model action to Auto inheritance.
3. Apply whether the failure came from the Task tool (pre-start) or from the member after start.
4. Re-route any **not-yet-started** members via Reach Auto as well (do not spawn more paid/API slugs after the first usage failure).
5. Log the retry/re-route in the dispatch plan (`retried/routed via Reach Auto — usage/rate limit`).
6. If Reach Auto is blocked (named parent and no `auto` in enum), stop and ask the user to switch the parent chat to Auto; do not burn further named-model attempts.
7. If an Auto retry also fails, document the failure and continue with remaining reachable members — do not invent that member's output.

## Agent count

| Scope  | Count | When                                        |
| ------ | ----- | ------------------------------------------- |
| Small  | 2–3   | Focused feature, explore + verify           |
| Medium | 4–6   | Multiple related areas or mixed gather      |
| Large  | 7–10  | Broad exploration or comprehensive research |

More than 10 members — split into multiple `multi` runs.

## Limitations

- 10 member maximum
- Members work independently; no inter-member communication
- Best for parallel independent work, not sequential workflows
- Startup overhead makes it wasteful for tiny tasks

## Output format

Follow [references/output-schema.md](references/output-schema.md). Consolidated runs use [references/output-format.md](references/output-format.md).

## Consumer bindings

Project recipe index and council agent paths arrive as project-specific injected context on skill read. Do not edit synced copies in place.
