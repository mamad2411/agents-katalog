---
name: research-roadmap
description: Scan research and documentation health, then maintain a priority documentation queue
type: planning
version: v0.9
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Research Roadmap - Documentation Queue Manager

Invoke as `$research-roadmap`.

Use this skill to make the project documentation contract complete before build work continues. It scans research, specs, and task docs, then updates `tasks/todo.md` with immediately actionable documentation work and uses `tasks/record-todo.md` or `tasks/recurring-todo.md` for non-blocking future documentation records.

Do not run the queued research skills from this skill. The job here is to maintain the documentation queue so the user can complete research and planning artifacts in the right order.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 0. Parse Mode Arguments

Parse `$ARGUMENTS` for mode flags:

- `--post-prototype`: Post-prototype research refresh mode
- `--post-spec`: Post-spec research refresh mode
- No flags: default documentation queue mode (existing behavior)

If `--post-prototype` is present, skip to the Post-Prototype Process below.
If `--post-spec` is present, skip to the Post-Spec Process below.
Otherwise, continue with the standard process starting at step 1.

### 1. Resolve Project Pack

1. Read `.agents/project.json` if it exists.
2. Use `project_type` and `enabled_packs` to decide which project-pack research skills apply.
3. If `.agents/project.json` is missing, infer the project type from repository signals:
   - game: game engine files, Steam/store assets, playable prototypes, or game-specific README/spec language
   - devtool: SDK, CLI, API, library, infra, docs, examples, or package-first developer workflow
   - business-app: SaaS, marketplace, productivity, workflow, enterprise, or user-facing app
4. If the project type cannot be inferred, default to `business-app`.
5. If an expected pack is not installed, add a priority todo for `$pack install <pack>` before pack-specific research todos.

### 2. Resolve Documentation Roots

Treat top-level `research/`, `specs/`, and `tasks/` as canonical.

1. If a canonical root exists, use it directly.
2. If a canonical root is missing, search shallowly near the repo root for likely aliases such as `docs/`, `planning/`, `notes/`, or `work/`.
3. Prefer roots that contain multiple expected documentation files over isolated matches.
4. If no credible task root exists, create/update top-level `tasks/todo.md`; create `tasks/record-todo.md` or `tasks/recurring-todo.md` only when advisory items exist.
5. If a fallback root is used for research or specs, mention it in the generated todo item reasons.

For writing the priority queue, prefer `tasks/todo.md`. Use a fallback task root only when the project already has a clear existing task contract and no top-level `tasks/` directory. Do not put condition-gated records or recurring obligations into `tasks/todo.md` unless they are immediately actionable execution work.

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Interpret `active_paths` as the current product/app/ICP focuses and `product_paths[]` as the product-path manifest. Valid statuses include `active`, `deferred`, `archived`, `promoted`, and `revisit_candidate`; these are research product-path states, not git branches.

### 3. Discover Research-Producing Skills

Build the research queue from enabled project packs. Include every enabled research-producing skill whose output is missing or stale, even if its prerequisites are not yet present. When prerequisites are missing, keep the item in the queue but note that it is blocked by earlier documentation items.

Prefer dynamic discovery when skill files are available:

1. Inspect enabled pack skill files under `.codex/skills/*/SKILL.md` or `packs/<pack>/codex/*/SKILL.md`.
2. Include skills with `type: research`.
3. Also include skills whose `## Output` section writes `research/*.md`, `research/{slug}/*.md`, `research/experiments/*.md`, or dated research files.

If dynamic discovery is unavailable, use these fallback maps.

Business-app research outputs:

| Skill | Output |
| --- | --- |
| `$icp` | `research/icp.md` |
| `$competitive-analysis` | `research/competitive-analysis.md` |
| `$journey-map` | `research/journey-map.md` |
| `$positioning` | `research/positioning.md` |
| `$metrics` | `research/metrics.md` |
| `$gtm` | `research/gtm.md` |
| `$monetization` | `research/monetization.md` |
| `$landing-copy` | `research/landing-copy.md` |
| `$customer-feedback` | `research/customer-feedback.md` |
| `$assumption-tracker` | `research/assumption-tracker.md` |
| `$experiment` | `research/experiments/<experiment>.md` |
| `$enterprise-icp` | `research/enterprise-icp.md` |
| `$risk-register` | `research/risk-register.md` |
| `$burn-rate` | `research/burn-rate.md` |
| `$runway-model` | `research/runway-model.md` |
| `$cohort-review` | `research/cohort-review-YYYY-MM-DD.md` |
| `$retro` | `research/retro-YYYY-MM-DD.md` |
| `$investor-update` | `research/investor-update-YYYY-MM.md` |
| `$platform-strategy` | `research/platform-strategy.md` |
| `$product-line review` | `research/.progress.yaml` |
| `$mvp-gap` | `research/mvp-gap.md` |

Game research outputs:

| Skill | Output |
| --- | --- |
| `$game-audience` | `research/game-audience.md` |
| `$game-fantasy` | `research/game-fantasy.md` |
| `$game-genre-map` | `research/game-genre-map.md` |
| `$game-comparables` | `research/game-comparables.md` |
| `$game-core-loop` | `research/game-core-loop.md` |
| `$game-prototype-test` | `research/game-prototype-test.md` |
| `$game-playtest-metrics` | `research/game-playtest-metrics.md` |
| `$game-store-page-test` | `research/game-store-page-test.md` |
| `$game-launch` | `research/game-launch.md` |

Devtool research outputs:

| Skill | Output |
| --- | --- |
| `$devtool-user-map` | `research/devtool-user-map.md` |
| `$devtool-integration-map` | `research/devtool-integration-map.md` |
| `$devtool-dx-journey` | `research/devtool-dx-journey.md` |
| `$devtool-adoption` | `research/devtool-adoption.md` |
| `$devtool-positioning` | `research/devtool-positioning.md` |
| `$devtool-monetization` | `research/devtool-monetization.md` |
| `$devtool-docs-audit` | `research/devtool-docs-audit.md` |

Also include documentation-producing non-research skills when their outputs are missing or stale:

| Skill | Output |
| --- | --- |
| `$idea-scope-brief` | `research/concept-brief.md` or `research/{slug}/concept-brief.md` |
| `$spec-interview` | `specs/*.md` |
| `$ux-variations` | `specs/ux-variations-*.md` |
| `$ui-interview` | `specs/ui-*.md` |
| `$scale-audit` | `specs/scale-audit.md` |
| `$roadmap` | `tasks/roadmap.md`, `tasks/todo.md` |
| `$game-roadmap` | `tasks/roadmap.md`, `tasks/todo.md` |
| `$reconcile-research fix all` | `research/reconciliation-report.md` |
| `$reconcile-dev-docs fix all` | reconciled `tasks/`, `specs/`, and phase archives |
| `$youtube-audit` | `research/youtube-audit-YYYY-MM-DD.md` |

### 4. Scan Documentation State

Record existence and last-modified timestamps for:

- all discovered research outputs
- `research/concept-brief.md` and product-path-scoped `research/{slug}/concept-brief.md` when present
- `research/*-search-log.md` and `research/*-interview.md` only as supporting context, not primary completion artifacts
- `specs/*.md` and product-path-scoped `specs/{slug}/*.md`
- `specs/ux-variations-*.md` and product-path-scoped `specs/{slug}/ux-variations-*.md`
- `specs/ui-*.md` and product-path-scoped `specs/{slug}/ui-*.md`
- `tasks/roadmap.md`
- `tasks/todo.md`
- `tasks/history.md`
- `tasks/ideas.md`
- `tasks/manual-todo.md`
- `tasks/record-todo.md`
- `tasks/recurring-todo.md`

When `research/` contains product-path subdirectories, treat it as product-path mode. Build a separate documentation queue per product path and include product-path arguments in commands, such as `$icp web`.

### 5. Classify Missing And Stale Items

An item is missing when its expected output file does not exist.

An item is stale when a newer upstream document should invalidate or refresh it. Include the exact timestamps in the todo reason. Use these default rules:

| Newer input | Stale target |
| --- | --- |
| `research/concept-brief.md` or `research/{slug}/concept-brief.md` | matching `research/icp.md` or `research/{slug}/icp.md` |
| `research/customer-feedback.md` | `research/icp.md`, `research/journey-map.md`, `research/monetization.md`, `research/landing-copy.md` |
| `research/icp.md` | `research/competitive-analysis.md`, `research/positioning.md`, `research/gtm.md`, `research/monetization.md`, `research/landing-copy.md` |
| `research/competitive-analysis.md` | `research/positioning.md`, `research/gtm.md`, `research/monetization.md`, `research/landing-copy.md` |
| `research/positioning.md` | `research/gtm.md`, `research/landing-copy.md` |
| `research/journey-map.md` | `research/metrics.md`, `research/gtm.md`, `research/monetization.md`, `research/landing-copy.md` |
| `research/metrics.md` | `research/cohort-review-*.md`, `research/runway-model.md`, `research/investor-update-*.md` |
| `research/gtm.md` | `research/monetization.md`, `research/runway-model.md`, `research/investor-update-*.md` |
| `research/monetization.md` | `research/burn-rate.md`, `research/runway-model.md`, `research/investor-update-*.md` |
| `research/experiments/*.md` with results | `research/assumption-tracker.md` |
| `research/cohort-review-*.md` latest | `research/metrics.md`, `research/gtm.md`, `research/monetization.md`, `research/investor-update-*.md` |
| `research/enterprise-icp.md` | `specs/scale-audit.md` |
| `research/journey-map.md` | `specs/*.md`, `specs/ux-variations-*.md`, `specs/ui-*.md`, `research/metrics.md`, `research/gtm.md`, `research/monetization.md`, `research/landing-copy.md` |
| any non-UX/UI `specs/*.md` | `specs/ux-variations-*.md`, `specs/ui-*.md`, `tasks/roadmap.md` |
| `specs/ux-variations-*.md` | `specs/ui-*.md`, `tasks/roadmap.md` |
| `specs/ui-*.md` | `tasks/roadmap.md` |
| `research/runway-model.md` | `tasks/roadmap.md` |

Also flag potentially stale specs when source code has commits newer than the spec files. Add `$spec-drift fix all` as a priority documentation item when specs are probably behind implementation.

Do not queue a missing `$idea-scope-brief` item for established projects that already have `research/icp.md`, `research/competitive-analysis.md`, `research/journey-map.md`, or `specs/`. Queue it only for idea-only projects where no concept brief or downstream research/spec artifact exists.

### 6. Order The Priority Queue

Order immediately actionable todo items so the user can complete documentation without guessing:

1. Pack installation needed for the selected project type.
2. Stale foundational research.
3. Missing foundational research.
4. Stale downstream research.
5. Missing downstream research.
6. Missing or stale specs.
7. Missing or stale UX/UI planning artifacts for user-facing work.
8. Missing or stale roadmap/task docs.
9. Reconciliation items when conflicting docs are detected.

Within research items, use this dependency order when relevant. When emitting queued commands for pack-based skills, apply the Pack Availability Guard — if the target skill's pack is not in `.agents/project.json` `enabled_packs`, queue `$pack install <pack>` before the skill:

When `research/.progress.yaml` exists, show per-path pipeline progress alongside the priority queue. For each path in `active_paths`, show its `pipeline_stage` and queue the next missing research step. For `deferred` or `revisit_candidate` paths, add a concise record or queue note with the `revisit_trigger` and `next_skill` rather than scheduling full downstream research. When 3+ deferred paths accumulate with no recent activation, add `$product-line review` as a priority queue item to prompt portfolio review.

```
$idea-scope-brief
  -> $icp
  -> $competitive-analysis
  -> $journey-map
  -> $positioning
    -> $ux-variations
      -> $ui-interview
        -> $prototype
          -> $uat --variant-evaluation
            -> $consolidate-variations
              -> $research-roadmap --post-prototype
                -> $spec-interview
                  -> $roadmap
    -> $metrics
  -> $gtm
  -> $monetization
  -> $landing-copy
3+ research docs -> $assumption-tracker -> $experiment -> $customer-feedback
$enterprise-icp -> $scale-audit
$metrics + launch data -> $cohort-review
$monetization -> $burn-rate -> $runway-model
quarterly/outcome data -> $retro
stakeholder reporting -> $investor-update
multi-product expansion -> $platform-strategy
3+ deferred product paths -> $product-line review
```

For game and devtool projects, follow the default pack flow from `docs/skills-reference.md` when available. Add review or planning skills such as `$devtool-docs-audit` and `$game-roadmap` only when their documented output is missing from the documentation contract.

Default devtool order:

```
$devtool-user-map
  -> $devtool-integration-map
    -> $devtool-dx-journey
      -> $devtool-adoption
        -> $devtool-positioning
          -> $devtool-monetization
            -> $devtool-docs-audit
              -> $research-roadmap
```

### 6b. Classify Advisory Documentation Work

Before writing any queue, choose the correct task surface:

- `tasks/todo.md`: missing/stale documentation work that can be performed now with available repo context and normal skill inputs.
- `tasks/record-todo.md`: one-time documentation records or measurements that are blocked on future conditions, production aggregate access, external reports, user-provided data, or launch data, and are not launch gates.
- `tasks/recurring-todo.md`: cohort reviews, retros, investor updates, playtest/adoption checks, docs-health checks, or other documentation jobs that recur on a cadence.

Record items must include task, source, condition, non-blocking reason, required data/access, measurement/query, target/acceptance note, revisit cadence/date, completion evidence, and promotion rule. Recurring items must include task, cadence, owner/agent, scope, trigger, last run, next due, command/skill, evidence/output path, and escalation conditions.

### 7. Update `tasks/todo.md`

Write a single top-level section named exactly:

```md
## Priority Documentation Todo
```

Rules:

1. If `tasks/todo.md` does not exist, create it.
2. If a previous `## Priority Documentation Todo` section exists, replace only that section.
3. Put the section before existing implementation work. If the file starts with a title or status block, keep that orientation text at the top and insert the priority section immediately after it.
4. Preserve all other todo content exactly unless it is inside the old priority section.
5. Do not mark existing implementation tasks complete.
6. Do not remove unrelated todo sections.
7. Use unchecked boxes only for missing/stale documentation work that is immediately actionable.
8. Use checked boxes only when an item is already current.

Todo item format:

```md
- [ ] `$skill [optional-app-or-argument]` - create/update `path/to/output.md` because [missing/stale reason with evidence].
```

If prerequisites are missing:

```md
- [ ] `$metrics` - create/update `research/metrics.md` after `$journey-map`; currently blocked because `research/journey-map.md` is missing.
```

Do not write unavailable-data or cadence-gated items here. Write those to `tasks/record-todo.md` or `tasks/recurring-todo.md` instead.

### 7b. Update `tasks/record-todo.md`

When non-blocking condition-gated documentation records exist, append or replace a `## Documentation Records` section in `tasks/record-todo.md`. Preserve all other sections exactly.

Use this item format:

```md
- [ ] [record task]
  - Source: [skill/spec/phase/criterion]
  - Condition: [future condition or required access]
  - Non-blocking reason: [why this does not block launch or current execution]
  - Required data/access: [data, aggregate, portal, credential, or user-provided output]
  - Measurement/query: [how to produce the record]
  - Target/acceptance note: [threshold or expected note]
  - Revisit: [date or cadence]
  - Completion evidence: [research path, history entry, or report path]
  - Promotion rule: [when to move into `tasks/todo.md`]
```

### 7c. Update `tasks/recurring-todo.md`

When recurring documentation work exists, append or replace a `## Documentation Recurring Work` section in `tasks/recurring-todo.md`. Preserve all other sections exactly.

Use this item format:

```md
- [ ] [recurring task]
  - Cadence: [daily/weekly/monthly/quarterly/on release/etc.]
  - Owner/agent: [$skill or responsible role]
  - Scope: [project/app/area]
  - Trigger: [time, release, data threshold, user request]
  - Last run: [date or never]
  - Next due: [date or rule]
  - Command/skill: [$skill args]
  - Evidence/output path: [research/report path]
  - Escalation conditions: [when this becomes executable or blocking]
```

If all documentation is current:

```md
- [x] Documentation is current; no missing or stale research, spec, roadmap, or task artifacts found.
```

### 8. Output To User

After editing, summarize:

```
## Research Roadmap Updated

- Wrote/updated `tasks/todo.md` and any needed advisory task files
- Priority documentation items: N
- Stale items: N
- Missing items: N
- Blocked-by-prerequisite items: N
- Record items: N
- Recurring items: N

Next: start at the first unchecked item in `tasks/todo.md`; review advisory task files separately. If there are no unchecked priority documentation items and no promotable advisory items, route to `$brainstorm` for candidate next-phase discovery unless the latest user request explicitly asks to pause, park, archive, or wait.
```

If fallback discovery was used, include a short note naming the inferred roots.

## Next-Step Routing

Before handing back, identify the next concrete documentation, planning, or discovery route from project state.

Output exactly two lines beyond the normal report:

- **Next work:** <specific documentation task, promotable advisory review, discovery task, or explicit parked state>
- **Recommended next command:** <one command or route>

Rules:

- Recommend the first unchecked `## Priority Documentation Todo` item when one exists.
- If a record or recurring item appears promotable to concrete execution work, recommend reviewing or promoting that item rather than discovery.
- Do not emit `Recommended next command: none` unless the latest user request explicitly asks to pause, park, archive, or wait.
- If documentation is current and no advisory item is promotable, route to new-phase discovery: `**Next work:** discover candidate next phase or explicitly park the project` and `**Recommended next command:** $brainstorm`.
- Use `$feature-interview` instead of `$brainstorm` when the project already has a concrete unspecced idea selected but still needs planning-destination triage. Use `$spec-interview` only when full-spec creation is already confirmed.

## Post-Prototype Process (`--post-prototype`)

### Gate

A consolidated prototype must exist at `prototypes/{topic}/consolidated/`. If missing, halt and recommend `$consolidate-variations` first.

### Scan

1. Read the consolidated prototype directory to understand what was built.
2. Read all research docs: `research/concept-brief.md`, `research/icp.md`, `research/competitive-analysis.md`, `research/journey-map.md`, and any other `research/*.md` files.
3. For each research document, compare against the consolidated prototype:
   - **User flows**: Does the prototype's flow match the journey map's discovery -> onboarding -> aha -> conversion -> retention path?
   - **Onboarding**: Does the prototype's first-run experience match ICP expectations for technical sophistication and time-to-value?
   - **Density and copy**: Does the prototype's information density and copy tone match ICP communication preferences?
   - **Interactions**: Do the prototype's interaction patterns match journey-map touchpoints and competitive differentiation?
   - **Differentiation**: Does the prototype demonstrate the competitive advantages identified in competitive analysis?
4. Flag research documents that are contradicted or made stale by prototype decisions.

### Output

Populate `tasks/todo.md` `## Priority Documentation Todo` with research skills that need re-running, using the same format as the standard process. Each item must explain what the prototype revealed that contradicts or supersedes the current research document.

**Next step:** first unchecked queued item in `tasks/todo.md`.

## Post-Spec Process (`--post-spec`)

### Gate

A production spec must exist at `specs/{topic}.md`. If missing, halt and recommend `$spec-interview` first.

### Scan

1. Read the production spec to understand implementation constraints.
2. Read all research docs.
3. For each research document, compare against spec constraints:
   - **Auth model**: Does the research assume an auth model that the spec changed?
   - **Data model**: Does the research assume data structures that the spec redesigned?
   - **Performance**: Does the research assume performance characteristics that the spec's architecture contradicts?
   - **Deployment**: Does the research assume a deployment model that the spec changed?
4. Flag research documents that are invalidated by spec constraints.

### Output

Populate `tasks/todo.md` `## Priority Documentation Todo` with research skills that need re-running. Each item must explain what spec constraint invalidates the current research document.

**Next step:** first unchecked queued item in `tasks/todo.md`.

## Constraints

- This skill updates `tasks/todo.md`, `tasks/record-todo.md`, and `tasks/recurring-todo.md`; it must not run the queued skills.
- Preserve user-authored todo content outside `## Priority Documentation Todo`.
- Preserve user-authored record/recurring content outside `## Documentation Records` and `## Documentation Recurring Work`.
- Every stale item must include timestamp evidence.
- Every enabled research-producing skill must be represented unless its output is present and fresh.
- Prefer canonical `research/`, `specs/`, and `tasks/` paths over aliases.
- In product-path mode, include product-path-scoped commands and output paths.
- Do not put condition-gated measurements, future validation records, or cadence-based research jobs into `tasks/todo.md` unless they are immediately executable.
- Do not create or modify source code.

## Alignment Page

Build and attempt to open `alignment/research-roadmap-{topic}.html` before writing or replacing `tasks/todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. Include evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and approval gates. Render documentation-health evidence, missing/stale artifact inventory, blocked prerequisites, priority queue rationale, pack-availability assumptions, proposed task-file changes, and the full proposed queue with no context loss from scan evidence.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.

**Research-roadmap translation.** Separate observed file/path evidence from inferred documentation health conclusions. Include source coverage expectations for web research and repo research: competitors, pricing, user sentiment, positioning, integrations, and recent activity when web evidence is used; file/path evidence and a distinction between observed code facts and inferred product, workflow, or user conclusions when repo evidence is used.

**Research quality contract.** Preserve `claims` (what the report concludes), `evidence`, `inference`, assumptions, confidence, alternatives considered, rejected or lower-confidence findings, source coverage gaps, and downstream implications in the page before approval. Include an evidence matrix, confidence/assumption register, and research completeness gate that asks whether the evidence is sufficient for the recommendation.

**Research completeness gate.** Ask whether the evidence is sufficient for the recommendation, which claims need more support, and what missing context could change the queue.

**No context loss rule.** Preserve every material fact, source, caveat, file/path reference, rationale, and decision impact from the scan evidence and proposed queue.

**Source coverage expectations.** For web research, cover competitors, pricing, user sentiment, positioning, integrations, and recent activity when those categories affect the queue. For repo research, include file/path evidence and distinguish observed code facts from inferred product, workflow, or user conclusions.

**Required inline questions.** Ask whether the evidence is sufficient for the queue, whether any assumptions or confidence levels are wrong, whether the recommended path and blocked prerequisites are acceptable, whether the proposed canonical file changes are approved, and whether any downstream route should remain blocked.

**Section feedback controls.** Add lightweight section-feedback controls to every major section of the page: approve as-is, reject or flag a concern, and clarification needed. Selecting a control reveals a multi-line section-feedback textarea placed directly under or beside the thumbs up/down/clarify controls. This textarea is separate from gate-question text inputs, so it still appears near the feedback controls even when the same section also has required gate questions with their own text boxes. These controls are optional for final approval and do not replace required gate questions. They also power the separate feedback-only YAML path so the user can send concerns or clarification requests before answering every required gate question.

**Feedback-only YAML contract.** Do not place a global feedback-only compile/output banner at the bottom of the page. When a section-feedback control is selected, show local "Compile Feedback YAML" and "Copy YAML" controls plus a read-only YAML textarea directly under that section's feedback textarea. Enable the local feedback compile as soon as that section feedback is set, even if required inline gate questions are unanswered. The local feedback compile generates YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `feedback_status: revision-request`, `approval_status: not-approved`, `unanswered_required_questions`, and a `section_feedback` list containing the single selected section-feedback entry for that local control. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. The feedback entry uses `section`, `feedback` (`up`, `down`, or `needs-clarification`), optional `notes` from that section's feedback textarea, and `requested_agent_action` (`accept-as-is`, `investigate-and-revise`, or `clarify-before-approval`). For `down` and `needs-clarification` feedback, the YAML must tell the agent to evaluate the feedback, investigate further when needed, and contextually amend the HTML alignment page before asking again for final approval answers. Copy and display this feedback YAML locally with the same clipboard retry and textarea fallback behavior as final gate YAML.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that compiles final approval answers into YAML with `alignment_page: alignment/{skill-name}-{topic}.html`, `approval_status: ready-for-agent-review`, `section`, `gate_type`, `status`, `decision`, `notes`, and `approved_file_changes` fields. Keep this bottom compile area for final approval answers; feedback-only YAML output belongs under each selected section feedback textarea, not in the bottom area. Populate `alignment_page` from the known repo-relative output path used to write the HTML page, not from the page title, browser URL, window location, or any display label. The final approval button remains disabled until every required question has a selection. The final YAML may also include any section feedback the user set, using the feedback-only YAML `section_feedback` shape. The page must automatically attempt to copy the YAML to the clipboard, provide an explicit "Copy YAML" button, and fall back to selecting the textarea contents.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page. Ask the user to review the page and provide either feedback-only YAML for concerns/clarification or final compiled YAML answers when ready. Do not require the user to answer every gate before sending negative feedback or clarification needs. When feedback-only YAML is provided, treat it as a revision request: evaluate the feedback, investigate further when needed, archive and amend the HTML page contextually, highlight the changes, and ask again for review. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML has been provided and the approved artifacts have been written or updated.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
