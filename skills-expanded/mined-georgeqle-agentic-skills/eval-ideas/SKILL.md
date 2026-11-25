---
name: eval-ideas
description: Loop feature-interviews over a brainstorm idea set and consolidate survivors into the roadmap
type: planning
invocation: orchestrator
version: v0.0
required_conventions: [alignment-page]
argument-hint: "[optional brainstorm topic or tasks/ideas.md ref] [--override-gate]"
context_intake: scoped
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Codex users to start a fresh Codex CLI session if the skill remains unavailable. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Eval Ideas — Orchestrator

Invoke as `$eval-ideas`.

This is a **self-advancing Pattern A orchestrator** (see `docs/research-session-loop-convention.md`). It bridges `$brainstorm` and the `$feature-interview` prompts that brainstorm proposes: it consumes an existing brainstorm idea set, loops one `$feature-interview` per fresh-context session over the ideas the user selects, then consolidates the survivors into a single prioritized handoff to `$roadmap`.

It is a **thin loop/manifest/gate/consolidation shell only**. The interview itself is `$feature-interview` followed **inline** within the loop session — `eval-ideas` must not re-implement interview logic, write specs directly, or phase the roadmap. It routes through `$feature-interview` (the writer) and `$roadmap` (the phaser).

**Scope: bridge only.** `eval-ideas` does not generate ideas. `$brainstorm` stays the separate upstream generator; run it first if no idea set exists.

Why this loop exists (three gaps it closes):

1. **Context bloat.** `$feature-interview` is `context_intake: deep`. Running several in one session degrades quality — exactly what the Research Session Loop convention prevents. The loop isolates one interview per fresh-context session.
2. **No progress tracking.** A run manifest plus `pending = selected − completed` detection makes the loop resumable across fresh sessions.
3. **No consolidation.** Each `feature-interview` independently picks its own destination and priority. The consolidation step rolls the survivors into one prioritized roadmap handoff.

## Entry Soft Gate — Maturity Check (warn-and-override)

On a cold start (state E), before presenting the multi-select idea gate, check whether the product is mature enough to be adding features. This is a **soft gate**: surface a warning manifest when any condition is unmet and require an explicit override to proceed. It never blocks early exploration with `$brainstorm`; it only warns before committing interview effort.

Check three conditions:

- **(a) Spec exists** — at least one product spec under `specs/` (or `specs/{slug}/`), or `spec.md` / `docs/specifications/`.
- **(b) No open todos** — `tasks/todo.md` (and `tasks/manual-todo.md`) have no outstanding unchecked items.
- **(c) Evidence backing** — at least one of: `research/customer-feedback.md` with findings, `research/icp.md`, `research/mvp-gap.md`, `research/competitive-analysis.md` (or their `{slug}/` equivalents), or public-research notes that back the ideas.

If all three are met, proceed silently to the multi-select gate. If any are unmet, render a **Maturity Warning Manifest** inline as the final message text of its own turn (Manifest Visibility Rule, `docs/interview-convention.md`): list each unmet condition, what is missing, and why it matters (open todos suggest unfinished current work; no spec suggests the product is pre-specification; no evidence suggests the ideas are unvalidated). Then ask the user to confirm the override or stop and address the gap first. `--override-gate` in `$ARGUMENTS` pre-confirms the override but the warning manifest is still shown. Do not present the multi-select idea gate in the same turn as the warning — wait for the override confirmation.

## Execution Model — Research Session Loop

Each invocation starts cold, resolves its state from **pasted YAML + filesystem**, runs **exactly one heavy phase** (one `$feature-interview`, or the consolidation), emits the next gate, and stops. The user advances the loop by clearing context and re-invoking `$eval-ideas`. The user never invokes `$feature-interview` directly — the orchestrator follows it inline.

When an idea is pending, the only user-facing continuation route is re-invoking `$eval-ideas` (with the same brainstorm topic / product-path argument when present). The parent resolves the next pending idea from the run manifest and filesystem.

State lives in **two places only**:

1. **Run manifest** — `tasks/_working/eval-ideas-run.yaml` (flat) or `tasks/{slug}/_working/eval-ideas-run.yaml` when a product-path scope is active. Records the **selected** idea ids, topics, and each idea's expected interview-log path. Written when the multi-select YAML is approved. Selection only, **not** per-idea status. Shape:

   ```yaml
   orchestrator: eval-ideas
   slug: skills-showcase            # omit in flat mode
   source: alignment/brainstorm-{topic}.html   # or tasks/ideas.md
   selected_ideas:
     - id: idea-1
       topic: inline-pr-comments
       interview_log: specs/inline-pr-comments-feature-interview.md
     - id: idea-2
       topic: batch-export
       interview_log: specs/batch-export-feature-interview.md
   ```

2. **Progress = artifact existence.** A selected idea is *done* when its `feature-interview` interview log (`specs/{topic}-feature-interview.md`, or the `docs/specifications/` equivalent) or a spec it produced exists. `pending = selected_ideas − ideas-with-a-written-log/spec`. The manifest stores selection only; status is derived.

`tasks/roadmap.md` / `tasks/todo.md` are **not** the state store for this loop — those belong to the implementation exec loop. This orchestrator keeps its state in the run manifest plus artifact existence.

### State resolution (resolve the first match; YAML first, then most-progressed A→G)

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **0 — pasted YAML** | a compiled alignment YAML is pasted | branch on `approval_status`: an approved multi-select YAML records the run manifest (light) then falls through to state C; an approved consolidation YAML writes the survivor list and roadmap handoff (state B finalize); `not-approved` → amend the named page (refinement session) and stop | manifest written + proceeds ↓, written consolidation, or amended page |
| **A — done** | run manifest exists, all selected ideas have an interview log/spec, **and** a consolidation survivor doc exists | — | done; emit `## Recommended Next Command: $roadmap` |
| **B — consolidate** | run manifest exists, all selected ideas interviewed, no consolidation written | **build the consolidation `review` page** — prioritized survivor list + roadmap handoff | consolidation `review` page |
| **C — run interview** | run manifest exists, ≥1 selected idea pending | **run next pending `$feature-interview` inline** (one heavy phase) | that interview's own checkpoint/handoff, then stop |
| **D — selection in review** | multi-select idea page in `review`, selection not yet recorded | — (waiting) | points the user to the page |
| **E — build selection** | no run manifest, no multi-select page (cold) | resolve idea set → run **entry soft gate** → build multi-select idea `review` page | warning manifest (if gate unmet), else multi-select `review` page |

Resolution order is **YAML first, then most-progressed backward (A→E)**. There is no state F/G: `eval-ideas` is `context_intake: scoped` with no deep interview and no interrogation page — it cold-starts at state E. "Pending idea" = a selected idea whose interview log/spec does not yet exist.

**Light vs heavy.** Recording the approved selection into the run manifest (state 0→C head) and archiving a consumed source are *light* — they fold into the head of the next heavy session. The heavy phase (one `$feature-interview`, or the consolidation) is the only thing isolated per session. If the run is small (1–2 ideas) and a phase is trivially cheap, fold rather than spend a near-empty round-trip.

### Terminal Handoff Contract

Every terminal response for this loop must end with `## Next Work` and one command section:

- `## Invoke With YAML` — only while a `review` page (multi-select or consolidation) is waiting for compiled YAML. It names `$eval-ideas` (with the same argument when present) as the invocation to use with the compiled YAML. Keep review/compile/paste instructions in `## Next Work`.
- `## Recommended Next Command` — only after approved YAML has been consumed and the artifact written/updated. While ideas remain pending or consolidation is unwritten, it names `$eval-ideas`. After the consolidation is written, it names `$roadmap` — the one place cross-skill routing is allowed.

Do not place any other section after the applicable command section. While running a `$feature-interview` inline (state C), the interview's own terminal checkpoints govern that session; when the interview's interview log is written and the loop stops, recalculate pending ideas from the manifest and filesystem, then end with the parent-owned `## Next Work` + the appropriate command section naming `$eval-ideas` (or `$eval-ideas --consolidate` when no ideas remain and consolidation is unwritten).

### Self-Routing Continuation Payload

Every `review` alignment page this parent creates must include `agent_routing` in the bottom compiled YAML, routing a fresh agent back to this parent. Use this shape (preserve the current argument when present):

```yaml
command: "$eval-ideas"                  # include the brainstorm topic / product-path arg when present
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: eval-ideas
  command: "$eval-ideas"
  product_path: tasks/{slug}            # omit in flat mode
  gate_owner: parent-orchestrator
  gate_type: idea-selection             # or consolidation
  run_manifest: tasks/_working/eval-ideas-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

`agent_routing` is routing metadata, not execution authority. The parent validates `approval_status`, identifies the gate, derives progress from the run manifest plus interview-log existence, writes/amends the artifact, archives consumed sources, and decides whether to load `$feature-interview` inline. Never put `$feature-interview`, `$roadmap`, `$exec`, or `/exec` in this mapping while a gate is pending.

## Process

### 0. Product-Path Scope Resolution

Resolve scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` (or legacy `abandoned`), stop and warn that the path is archived.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths`; treat legacy `abandoned` as `archived`; exclude `archived`, `deferred`, `revisit_candidate`, `promoted`, and `research/_archive/` scopes from active target selection.
4. If active product paths exist, use them. If multiple exist, ask which one to target.
5. If no active manifest target exists, list non-archived product directories under `research/` (excluding `research/_archive/` and dot dirs). Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint.

When product path `{slug}` is active, scope the run manifest to `tasks/{slug}/_working/eval-ideas-run.yaml` and pass the `{slug}` argument through to each inline `$feature-interview`.

### 1. State E — Resolve the Idea Set (cold start)

Resolve the brainstorm idea set to loop over, in this order:

1. If `$ARGUMENTS` names a brainstorm alignment page (`alignment/brainstorm-{topic}.html`) or a topic that resolves to one, read its **approved/curated** idea cards (title, motivating signal, the per-idea `$feature-interview <topic>` handoff).
2. Else if `tasks/ideas.md` exists, read its entries.
3. Else if a brainstorm alignment page exists for the active scope, use the most recent approved one.
4. If no idea set is found, stop and tell the user to run `$brainstorm` first (honor the Pack Availability Guard — `$brainstorm` is in this same `product-design` pack, so no cross-pack install is needed; if the pack is somehow not enabled, recommend `npx skillpacks install product-design`).

Carry forward each idea's topic slug and the motivating context so it can seed the inline `$feature-interview`.

### 2. State E — Entry Soft Gate

Run the **Entry Soft Gate — Maturity Check** above. If conditions are unmet, render the warning manifest inline and stop for the override confirmation. Do not build the multi-select page until the gate passes or the user overrides.

### 3. State E — Build the Multi-Select Idea Page

Build the multi-select idea `review` alignment page (`alignment/eval-ideas-{topic}.html`) with:

1. **Source summary**: which brainstorm idea set this loop draws from, and the maturity-gate result (met, or overridden with which conditions unmet).
2. **Multi-select idea section**: a checkbox per idea with its title, motivating codebase/research signal, and one-line description. No pre-checks beyond what the brainstorm page already marked approved — the user curates which ideas reach an interview.
3. **Loop explanation**: the selected set is the scope gate; each selected idea is then run through `$feature-interview` inline (one interview per session), the run advances by re-invoking `$eval-ideas`, and survivors are consolidated into a `$roadmap` handoff.
4. **Approval gate**: idea-selection confirmation.

This multi-select approval **is** the scope approval for the whole selected set. Stop for compiled YAML. Do **not** write the run manifest or run any interview in this session — that is state C.

### 4. State C — Run Next Pending Interview (inline)

This session consumes the approved multi-select YAML (state 0→C) or advances after a prior interview completed. At the **head** of the session, do the light bookkeeping first:

1. **Write the run manifest** if it does not yet exist (`tasks/_working/eval-ideas-run.yaml` or the product-path equivalent), recording `selected_ideas` with each idea's `id`, `topic`, and expected `interview_log` path. Include only ideas the user selected.
2. **Archive the consumed multi-select page / brainstorm source** only at this selection-commit point, per the alignment-page archive-first rule.

Then run the **one heavy phase**:

3. **Determine the next pending idea** = the first idea in `selected_ideas` whose interview log/spec does not yet exist.
4. **Load and follow `$feature-interview`'s `SKILL.md` inline**, seeding it with that idea's topic and motivating context (equivalent to `$feature-interview <topic>`). Follow the full feature-interview flow — its evidence brief, assumptions manifest, Planning Destination + Priority Checkpoint, and its interview-log write — within this session. `eval-ideas` adds no interview logic of its own.
5. When the interview's interview log is written, **recalculate pending ideas** from the manifest and filesystem, then stop with the parent-owned handoff.

**Advance the loop by self-re-invocation.** If pending ideas remain, end with `## Next Work` reporting progress as "k of N ideas interviewed" and saying the next run interviews the next pending idea, followed by `## Recommended Next Command` naming `$eval-ideas`. If no ideas remain pending and no consolidation exists, end with `## Next Work` saying the next run builds the consolidation survivor page, followed by `## Recommended Next Command` naming `$eval-ideas --consolidate`. Do not emit `$roadmap` here — that happens only after consolidation.

### 5. State B — Consolidation (auto-detected; also `$eval-ideas --consolidate`)

Enter consolidation when the run manifest exists, **all** selected ideas have an interview log/spec, and no consolidation doc exists yet. `$eval-ideas --consolidate` also forces this state.

Read every selected idea's interview log (and any spec it produced). For each, extract: the confirmed planning destination, the user-confirmed priority hypothesis, the scope to build now vs defer, and the recommended next command recorded in the log. **Do not re-interview and do not re-decide** — consolidation reconciles what the interviews already concluded.

Build the consolidation `review` page with:

1. **Survivor list**: each interviewed idea, its planning destination (new spec / add-on spec / spec update / roadmap-or-task edit / no-action), the artifact path it produced, and its confirmed priority.
2. **Cross-idea prioritization**: a single ordered list of the survivors that reach the roadmap, with dependencies, conflicts, and a recommended build sequence. Drop ideas whose interview concluded `no action` / already-covered; note them as evaluated-and-parked.
3. **Roadmap handoff**: the prioritized survivor set framed for `$roadmap` to phase — which items are spec-backed and ready to sequence, which need further planning first.
4. **Approval gate**: consolidation confirmation.

Stop for compiled YAML. On approval, write the survivor/consolidation doc to `tasks/eval-ideas-survivors.md` (or `tasks/{slug}/eval-ideas-survivors.md`): the ordered survivor list, each item's destination + artifact path + priority, the parked/no-action ideas, and the recommended `$roadmap` handoff. Then **archive the run manifest** under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, convert the consolidation page to `confirmed`, and emit the downstream route (`$roadmap`). Verify `$roadmap` availability per the Pack Availability Guard: it lives in the `agent-work-admin` pack — if that pack is not enabled, recommend `npx skillpacks install agent-work-admin` before `$roadmap`.

## Constraints

- **Bridge only.** Do not generate ideas (that is `$brainstorm`). Do not change `$feature-interview` or `$brainstorm`. Consume an existing idea set and loop to a roadmap handoff.
- **Parent self-advances one phase per invocation** and follows `$feature-interview` inline. The run manifest records the selected idea set; progress is interview-log/spec existence. The loop advances by re-invoking `$eval-ideas` (clear context between sessions).
- **Do not write specs directly.** `eval-ideas` routes through `$feature-interview` (the writer) and `$roadmap` (the phaser). Its only writes are the run manifest and the consolidation survivor doc.
- **Reuse, don't duplicate.** The interview is `$feature-interview` followed inline; the handoff contract is copied from the Research Session Loop convention; the soft-gate manifest renders inline per the Manifest Visibility Rule.
- **The soft gate is a warning, not a block.** Always allow an explicit override. Never silently proceed past an unmet gate, and never present the multi-select gate in the same turn as the warning.
- **Consolidation does not re-decide.** It reconciles the interview conclusions into one prioritized handoff; it does not re-run interviews or override a user-confirmed destination/priority.
- **No cross-skill routing while a gate is pending.** During the multi-select and consolidation review gates, the only user-facing continuation command is `$eval-ideas`. Emit `$roadmap` only after the consolidation is written.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` before the target skill.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/eval-ideas-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
