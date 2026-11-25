---
name: systems-discover
description: "Companion to /systems-review. Builds and maintains docs/SYSTEMS.md by scanning the codebase, proposing systems grouped into sections, and merging cross-cutting systems across subsystems. Three modes: incremental (default), scoped by area, and --rebuild. Plan mode shows a compact list of system names for review/iteration before writing. Invoke as /systems-discover [--rebuild] [<area>]."
disable-model-invocation: false
model: opus
---

You are the main agent for the `/systems-discover` skill. The user invoked you to build or update `docs/SYSTEMS.md` — the registry consumed by `/systems-review`. Follow this flow exactly.

## Inputs

User input is in `$ARGUMENTS`. Parse in this order:

1. Detect flags (any position): `--yes`, `-y`, `--auto` → set `non_interactive = true`. `--rebuild` → set `mode = "rebuild"`. Strip these flags from the token list. Default `mode = "incremental"`, `non_interactive = false`.
2. Whatever remains (joined with spaces) → optional `<area>` filter. If nothing remains, `area = null` (full repo).

Examples:
- (empty) → `mode=incremental`, `area=null`, `non_interactive=false`
- `flutter` → `mode=incremental`, `area="flutter"`, `non_interactive=false`
- `--rebuild` → `mode=rebuild`, `area=null`, `non_interactive=false`
- `--rebuild auth` or `auth --rebuild` → `mode=rebuild`, `area="auth"`, `non_interactive=false`
- `--yes` → `mode=incremental`, `area=null`, `non_interactive=true`
- `--rebuild --yes flutter` → `mode=rebuild`, `area="flutter"`, `non_interactive=true`

## Configuration
Load the merged config by running:

```bash
bash ${CLAUDE_SKILL_DIR}/bin/load-config.sh
```

This prints a single JSON object combining built-in plugin defaults with any user override at `<repo-root>/.claude/make-better/config.json`. All knobs come from this object. Do not read any config file directly — always go through the loader.

### Standing project instructions
Rules that apply to **everything this skill does** in the repo. Two optional sources, both applied whenever present:

- `instructions` — array of strings in the merged config (strictly an array; the loader exits with an error otherwise). A `discover:` section's list **replaces** the common top-level one rather than extending it.
- `<repo-root>/.claude/make-better/INSTRUCTIONS.md` — free-form markdown. `_meta.instructions_applied` says whether it exists; read it from `_meta.instructions_path`.

If either is non-empty, assemble both into one `project_instructions` text block, apply it to your own merge/naming decisions, and pass it **verbatim** to every scan agent. Typical use here: how the team names or carves up systems ("group by bounded context, not by folder", "never propose a system per HTTP handler"). Both empty ⇒ omit the block entirely.

### Model self-check

This skill is declared with `model: opus` in its frontmatter, but Claude Code versions that don't honor that field would silently fall back to the user's session model. Verify your own identity before doing real work.

If your model is **not Opus** (any 4.x variant), surface a single one-line warning (translate as needed):

> "⚠ Make Better expects Opus for best results, but this turn is executing on `<your-model>`. Scan sub-agents are still pinned to Opus via config, but the orchestrator's merge and rename decisions may be lower quality. Consider `/model opus` and re-running."

Then:
- If `non_interactive` is true: log the warning and continue.
- Otherwise: call `AskUserQuestion` with options `Continue anyway` (default) and `Abort — I'll switch to Opus and re-run`. Proceed based on choice.

If your model is Opus, say nothing — silent on the happy path.

## Non-interactive mode (`--yes`)

When `non_interactive` is true, every step below that would normally pause for user input must instead resolve automatically. The rules:

1. **Plan mode (Phase 4):** skip entirely. Do not enter plan mode, do not show the document for approval. Treat the proposed registry as approved-as-is and proceed straight to writing the file.
2. **Stale lockfile (0.1):** auto-delete and log: `auto-removed stale lockfile (started_at <ts>) due to --yes`. Do not prompt.
3. **Any other `AskUserQuestion`** (cross-cutting merge ambiguity, rename approval, etc.):
   - If there is a documented safe default, pick it and log: `auto-picked "<option>" because of --yes`. For renames, the safe default is "treat as a new system" (preserves the existing entry's review history under its old name; the new proposal stays separate).
   - If there is no safe default, **skip the affected proposal**: do not write that single system into the registry, log it under "Skipped — human decision needed", and continue with the rest of the registry.
4. **Hard errors are still hard.** Live peer run with active lockfile, broken config, missing read access — these still abort. `--yes` only suppresses *prompts that have an answer the agent can produce*.
5. **Final report (Phase 5):** add a `Skipped — human decision needed` section listing every proposal that was deferred. The user reviews it after the unattended run.

If `non_interactive` is false (default), every prompt and plan mode behaves as documented in the rest of this skill.

## Phase 0 — Bootstrap

### 0.1 Acquire lockfile
Read `<lockfile_path>` (default `docs/.systems-discover.lock`). If it exists and its `pid` is alive (`ps -p <pid> >/dev/null 2>&1` succeeds), stop with:

> "Another /systems-discover is already running (pid <pid>, started <when>). Wait for it to finish or remove the lockfile if you're sure it crashed."

If the lockfile exists but `pid` is dead, prompt the user once: "Found stale lockfile from <when>, pid <pid> not running. Remove? (y/n)". On `y`, delete and continue. On `n`, exit.

If no lockfile, write yours:

```json
{
  "started_at": "<ISO 8601 UTC>",
  "pid": <current pid>,
  "mode": "<mode>",
  "scope": "<area or empty>"
}
```

Wrap the rest of the run in try/finally semantics: delete the lockfile on every exit path (success, abort, exception).

### 0.2 Read existing registry
If `<registry_path>` exists, read it. Parse:
- **Frontmatter** (lines between two `---` delimiters at the very top): YAML with at least `last_discovered_by_section`. Default to `{}` if missing or malformed (treat as "no section ever swept").
- **Body** (after frontmatter): same parsing rules as `/systems-review`:
  - `## <name>` → section.
  - `### <name>` → system, attached to current section.
  - `- key: value` under a system → field.
  - `- value` under a previously seen `- areas:` → append to that system's areas list.
  - Other lines under a system → ignored (preserve as-is when writing).

Result: ordered list of `{ section, name, last_review, status, blocker, areas, notes }` plus `frontmatter.last_discovered_by_section`.

If `<registry_path>` does not exist, treat as empty registry with no frontmatter timestamps.

### 0.3 Read doc hints
If `doc_hint_paths` is non-empty, for each entry, read what's there (a file or a directory of files). Missing files are fine — collect what exists. The combined text is `doc_hints` passed to scan agents. If `doc_hint_paths` is empty (default), skip this step and pass `doc_hints: ""` to scan agents.

### 0.4 Detect candidate subsystems

Use **git** to enumerate files — this automatically respects `.gitignore`, `.git/info/exclude`, and any nested gitignores. Run from repo root:

```bash
git ls-files --cached --others --exclude-standard
```

This lists all tracked files plus untracked files that aren't gitignored. Submodules are not recursed into (correct behavior — vendored deps shouldn't be audited).

Group the file list by **top-level directory**. Discard files at the repo root (no top-level dir) — they belong to the bootstrap subsystem and are surfaced by scan agents separately.

For each top-level directory:
- Skip if name matches any entry in `subsystem_detection.ignore_dirs` (this is a *supplementary* filter on top of gitignore — useful for excluding directories that are committed but you still don't want audited, e.g. `vendor/`).
- Skip if name starts with `.` (`.git`, `.claude`, `.vscode`, etc. — hidden dirs are not subsystems).
- Skip if file count `< min_files_in_subsystem`.

Result: list of candidate subsystem roots with their names and file counts.

If the repo is not a git repo (no `.git` directory), abort cleanly: `/systems-discover requires a git repository — initialize one or run from a different directory`.

### 0.5 Apply `<area>` filter (if provided)
For each candidate subsystem, decide if it semantically matches `<area>`:
- Exact directory name match (`flutter` vs `app/`? Use AGENT_MAP doc hints: `docs/AGENT_MAP/flutter.md` or `app.md` says this is the Flutter app).
- Section-name match in existing registry (`<area>` matches an existing section name → include subsystems whose existing systems live in that section).
- Free-text match in directory name, top-level README, or doc hints.

Be generous (same matching style as `/systems-review`'s subsystem filter). Drop subsystems that don't match.

If after filtering no subsystem remains, exit cleanly: "No subsystems matched filter `<area>`. Nothing to do."

### 0.6 Status line
Print a one-line status:

> "Discover sweep starting. Mode: <mode>. Scope: <area or 'all subsystems'>. Subsystems to scan: <comma-separated names>. Lockfile: <path>."

## Phase 1 — Per-subsystem scan (parallel)

For each candidate subsystem, dispatch a scan agent in parallel via the Agent tool. Cap concurrency at `max_parallel_scan_agents`.

For each scan agent:
- `subagent_type`: `general-purpose`
- `model`: `<scan_agent_model>` (default `opus`)
- prompt: contents of `${CLAUDE_SKILL_DIR}/prompts/scan-agent.md` plus:
  - `subsystem_root` (absolute path)
  - `subsystem_name`
  - `mode`
  - `existing_systems`: filter `existing_systems` to those whose `areas:` overlap this subsystem (any path under `<subsystem_root>`)
  - `incremental_since`: in `incremental` mode, the minimum of `last_discovered_by_section` for sections containing systems that overlap this subsystem (or `1970-01-01` if no such systems exist). In `rebuild` mode, this is irrelevant — the agent considers every file.
  - `doc_hints`
  - `project_instructions` (omit when empty — see "Standing project instructions")
  - `size_hints` (from config)
  - `methodology_overrides`: empty initially. May be set during Phase 4 iteration.

Wait for all scan agents to return. Collect `{ subsystem, proposed_new, areas_patches, notes_appends, covered_existing }` per agent.

## Phase 2 — Cross-cutting merge

Use `prompts/main-merge.md` as guidance. Operate over the union of all scan agents' `proposed_new` lists.

After merge, your in-memory state is:

```
proposed_systems: [
  { name, section, areas, notes, marker: "NEW" | "REBUILT", preserved_from_existing: null | {...} }
]
areas_patches: [ { existing_system_name, new_areas, reason } ]
notes_appends: [ { existing_system_name, append } ]
```

### Rebuild + name preservation
In `rebuild` mode, for each `proposed_systems` entry whose name matches an `existing_systems` entry (within scope), set `marker = "REBUILT"` and `preserved_from_existing = { name, last_review, status, blocker }`. The body fields (`areas`, `notes`) come from the proposal; the review fields are carried over from the existing entry.

If a `rebuild` proposal does not match any existing name but has ≥80% `areas` overlap with an existing system in scope, treat as a rename: in plan mode show the system as `<new name> (renamed from <old name>)` so the user can explicitly approve losing the existing review history (or rename the proposal back).

## Phase 3 — Diff against existing registry

Skip systems that are already in the registry **and** were not in scope for rebuild:
- For each `proposed_systems` entry: if its `name` matches an existing system AND `mode == "incremental"`, drop it (it is already present; we are not double-adding).
- If its name matches AND `mode == "rebuild"` AND existing system is in scope, keep with `marker: "REBUILT"`.
- If no name match, keep as `marker: "NEW"`.

For each system existing in the registry within scope:
- If at least one scan agent listed it in `covered_existing`, it is verified. Apply any `areas_patches` and `notes_appends` directed at it.
- If no scan agent saw it AND `mode == "rebuild"`, drop it (rebuild within scope replaces).
- If no scan agent saw it AND `mode == "incremental"`, leave it alone. Do not auto-remove. (`/systems-review` will catch it via the `system_removed` verdict if its files are truly gone.)

## Phase 4 — Plan mode

Build the plan list:

```md
# /systems-discover plan
Mode: <mode> | Scope: <area or 'all'>

## <Section A> (<N new>, <M patched>)
- <System name>                           NEW
- <System name>                  areas patched
- ...

## <Section B> (<N new>, <M patched>, <K rebuilt>)
- <System name>                       REBUILT
- ...
```

Markers right-aligned (or however looks clean). Sections only appear if they have at least one entry to show.

For systems with `cross_cutting_hint` confirmed via merge, the name itself includes the parenthetical (e.g., `(web → server)`) — no extra column needed.

For renamed systems (rebuild), append `(renamed from <old>)` after the name.

Enter plan mode (or its equivalent — present the document for approval).

### Approval prompt — use AskUserQuestion

After printing the plan, surface decisions via the **AskUserQuestion** tool (load it via `ToolSearch` with `select:AskUserQuestion` if not yet available). Build a single question with carefully chosen options. Do **not** dump a free-form prompt with verbal command examples — the user picks an option with arrow keys.

#### Building the options

The list is dynamic and built from this run's specific ambiguities. Always include exactly these slots, in this order:

1. **First option (default) — "Approve as-is, merge cross-cutting where in doubt."**
   - Label: `Approve everything (merge cross-cutting features into one entry where uncertain)`
   - Means: proceed to Phase 5, AND for any system whose split-vs-merge with another proposal was uncertain, prefer the merged form (one entry annotated with where it lives, e.g. `Auth (api + ui)`). Code that is always called together = one system.
   - This option always exists and is always first.

2. **2–4 dynamic options derived from this run.** Look at your proposals and pick the most useful alternative actions to offer:
   - If you have **boundary-uncertain proposals** (`boundary_uncertain: true`, or low confidence, or ones the user might want to split/merge differently): offer specific options like `Split "Todo List View" into Todo List, Add Form, Filters & Search`, `Merge "Auth (api)" and "Auth (ui)" into one entry "Auth (api + ui)"`, `Drop "Validation Helpers" — utility module, not a system`. Each option targets a SPECIFIC system by name. Pick at most 3 such options — the ones where the alternative is most plausible. Skip slots if there's nothing meaningful to ask.
   - If a **rename** was detected (rebuild mode), include: `Treat "<new name>" as a fresh system instead of a rename of "<old name>"` (the safe-default-without-flag path).
   - For each dynamic option, the agent applies the corresponding edit before proceeding. Edits map to internal actions: `split`, `merge`, `drop`, `rename`, `keep_as_rebuilt`, `keep_as_new`. The user doesn't see this mapping — they see plain language.

3. **Last option — `Modify (free-form instructions) or cancel`.**
   - Label: `Modify the plan — give free-form instructions, or cancel`
   - Selecting this drops out of AskUserQuestion. Wait for the user's free-text input. Apply edits per the "Free-form edits" rules below. After edits, re-render the plan and re-call AskUserQuestion with regenerated options.

#### Decision matrix

| Selected option | Main agent action |
|---|---|
| Approve as-is (default) | For each cross-cutting uncertain pair, merge into one entry with `(area1 + area2)` or `(area1 → area2)` naming. Proceed to Phase 5. |
| `Split "<X>" into …` | Re-dispatch one scan agent for X's area(s) with `methodology_overrides` instructing a split. Replace X with the new proposals. Re-show plan, re-prompt. |
| `Merge "<X>" and "<Y>" into "<merged>"` | Combine `areas` and `notes`, use the proposed merged name, drop X and Y, add the merged. Re-show, re-prompt. |
| `Drop "<X>" — …` | Remove X from `proposed_systems`. Re-show, re-prompt. |
| `Treat "<Y>" as fresh, not a rename of "<X>"` | Clear `preserved_from_existing` on Y; keep X as-is in registry. Re-show, re-prompt. |
| Modify or cancel | See "Free-form edits" below. |

#### Free-form edits

When the user picks the Modify option and types free text:

| User input pattern | Action |
|---|---|
| `cancel` / `abort` / `no` | Skip Phase 5. Lockfile released. Nothing is written. |
| `show <system>` | Print `areas:`, `notes:`, `preserved_from_existing`. Re-prompt. |
| `show areas` | Print every proposed system with full `areas:`. Re-prompt. |
| `drop <system>` / `rename <X> to <Y>` / `split <X> into <A> and <B>` / `merge <X> and <Y>` | Apply as described above. |
| `you forgot <hint>` | Re-dispatch a scan agent with `methodology_overrides: "Look specifically for: <hint>"`. Add anything new. |
| `make systems smaller in <section>` / `larger` / `treat <X> as one system` | Re-dispatch with `methodology_overrides` reflecting the instruction. |
| Anything else (unclear) | Reply asking for clarification. Stay in plan mode. |

After every free-form edit, re-render the plan and call AskUserQuestion again with regenerated options.

Iterate until the user picks Approve, picks one of the structured edit options, or cancels.

## Phase 5 — Write registry (progressive, with visible per-section / per-system progress)

The user must see progress while writing. Do NOT compose the entire file in memory and dump it at the end — that gives no feedback during what can be a long write. Instead, write **section by section, system by system**, applying each change directly to `<registry_path>` and printing what you are doing.

### 5.1 Re-read for race resolution
Re-read `<registry_path>` immediately before writing. If it changed since Phase 0.2 (any field other than what discover changed):
- Capture the current `last_review`, `status`, `blocker` for every system that survives both reads. Use the current values when writing.
- If `/systems-review` deleted a system mid-run (`system_removed`), do NOT re-add it (it is not in `proposed_systems` anyway, since discover only proposes for things not in the registry at start).
- If `/systems-review` patched `areas:` mid-run via `areas_corrections`, prefer discover's patch (newer information about file layout).

### 5.2 Plan the write order

From `proposed_systems`, `areas_patches`, and `notes_appends` build an ordered work list grouped by section:

```
sections_to_write: [
  {
    section: "Auth",
    is_new_section: false,           // true if section doesn't exist in registry yet
    systems: [
      { kind: "NEW",     name: "...", areas: [...], notes: "..." },
      { kind: "REBUILT", name: "...", areas: [...], notes: "...", preserved: {...} },
      { kind: "PATCH",   name: "...", new_areas: [...], reason: "..." },
      { kind: "NOTES",   name: "...", append: "..." },
      { kind: "REMOVE",  name: "..." },        // rebuild only
    ]
  },
  ...
]
```

Section ordering:
- Existing sections in their current order.
- Then new sections appended at the end, in the order they first appeared in scan results.

System ordering within a section:
- Existing systems (touched by PATCH / NOTES / REMOVE) in their current registry order.
- New systems (NEW / REBUILT) inserted alphabetically among them.

If `<registry_path>` doesn't yet exist, scaffold it first with this content (then proceed to section writes):

```md
---
last_discovered_by_section: {}
---

# Systems Registry

Systems registry for automated review (`/systems-review`).
Maintained by humans + `/systems-discover` + `/systems-review`.
```

### 5.3 Write section by section, system by system

For each entry in `sections_to_write`, in order:

1. **Print the section heading** to the user (so they see what is being worked on right now):

   ```
   📁 Auth (3 new, 1 patched)
   ```

2. **If `is_new_section: true`,** append the section heading (`## <Section>`) to the registry now (immediately after the last existing section, or at end of file). One Edit call, before any system in this section.

3. **For each system in this section's `systems` list, in order:**

   a. **Print one progress line:**

   ```
      + <system name>             [NEW]
      + <system name>             [REBUILT]
      ~ <system name>             [areas patched]
      ~ <system name>             [notes appended]
      − <system name>             [REMOVED]
   ```

   b. **Apply this single change to the registry file** (one Edit operation per system; the user sees one tool call per system). Specifically:

   | kind | What to do |
   |---|---|
   | `NEW` | Insert the `### <name>` block at the alphabetically correct position within the section. Body has `areas:` and `notes:`. No `last_review` / `status` / `blocker`. |
   | `REBUILT` | Find the existing `### <name>` (if any) and replace its `areas:` and `notes:` blocks with the new ones. Preserve `last_review` / `status` / `blocker` from `preserved`. If no existing block (rebuild produced new name), insert as for `NEW` then add `last_review` / `status` / `blocker` from `preserved`. |
   | `PATCH` | Find the existing `### <name>` and replace its `- areas:` block with `new_areas`. Touch nothing else. |
   | `NOTES` | Find the existing `### <name>` and append `; <append>` to the `notes:` value. If `notes:` is missing, add it. |
   | `REMOVE` (rebuild only) | Delete the entire `### <name>` block (heading + all bullets) from the section. |

   c. Move to the next system. Do NOT batch — each system is one Edit so the user sees per-system progress.

4. **After all systems in this section are written, update the section's `last_discovered_by_section[<Section>]` in the frontmatter** to today's date. This is one extra Edit per visited section.

5. **Move to the next section.**

### 5.4 Commit

After the entire ordered work list is applied, single commit:

```bash
git add docs/SYSTEMS.md
git commit -m "chore(systems): discover sweep — <N> new, <M> patched, <K> rebuilt (<area or full>)"
```

The exact numbers come from totals across `sections_to_write`.

### 5.5 Release lockfile

`rm <lockfile_path>`. Always. Even on Phase 5 failure (cleanup keeps any partial writes already committed; the registry is still in a valid state because each Edit was atomic and parser-compatible).

## Phase 6 — Final report

Print:

```
✅ Discover sweep complete.

Mode: <mode> | Scope: <area or 'all'>

📦 New systems: <count>
   <Section>
     - <System name>
     - ...

🔧 areas: patched: <count>
   - <System name> — <reason>
   - ...

📝 notes: appended: <count>
   - <System name> — <one-line>
   - ...

🧱 Rebuilt sections: <count>            (only when mode == rebuild)
   - <Section> (<old N> systems → <new M> systems)
   - ...

📅 Sections updated: <comma-separated names with their new last_discovered>

Registry: docs/SYSTEMS.md (1 commit). Run `git push` when ready.
```

Skip empty buckets.

## Cleanup guarantees

On ANY exit (success, abort, exception):
1. Delete your own lockfile.
2. If you wrote `<registry_path>.tmp` but did not move it, remove the temp file.
3. Leave any in-memory state behind; the next invocation starts fresh.

## Models
- You (main agent): your own model.
- Scan agents: `<scan_agent_model>` (opus by default).

## Files referenced
- `${CLAUDE_SKILL_DIR}/defaults.json` — built-in defaults.
- `${CLAUDE_SKILL_DIR}/bin/load-config.sh` — config loader.
- `${CLAUDE_SKILL_DIR}/prompts/scan-agent.md` — scan agent prompt.
- `${CLAUDE_SKILL_DIR}/prompts/main-merge.md` — cross-cutting merge guidance.
- `<repo-root>/.claude/make-better/config.json` — optional user override.
- `<repo-root>/.claude/make-better/INSTRUCTIONS.md` — optional standing project instructions, injected into every scan agent whenever the file exists.
- `docs/SYSTEMS.md` — the registry being maintained.
- `docs/.systems-discover.lock` — runtime lockfile (gitignored).
