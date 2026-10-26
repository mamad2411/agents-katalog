---
name: research-refresh
description: Use this skill when the user asks to "refresh research", "update the catalog", "re-run the framework research", "check for new methodologies", "update mck-scaffold", or when /mck-scaffold:init Step 0 detects a stale `research/last-run.json` and the user opts in. Orchestrates 4 parallel research subagents (GitHub / Reddit / YouTube / web-blogs), diffs new findings against the current catalog in `research/streams/*.md`, surfaces the diff for user-confirmed application to `interview/routing.md` and methodology preset templates, then updates `research/last-run.json` + `research/changelog.md`.
argument-hint: [--auto-apply] [--streams=<csv>]
allowed-tools: [Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash, Agent, TaskCreate, TaskUpdate]
version: 0.11.0
---

# /mck-scaffold:refresh-research

> **Status:** v0.11.0 — runs 4 parallel research streams, produces a structured diff against current catalog, presents per-section confirm prompts, applies confirmed changes. Auto-apply (`--auto-apply`) is a v0.11.1 feature that pre-confirms all sections (use with caution).

## When this skill is invoked

- Auto-triggered when user phrases match: "refresh research", "update the catalog", "re-run framework research", "check for new methodologies", "update mck-scaffold", etc.
- Chained from `/mck-scaffold:init` Step 0 when the user opts in to a refresh.
- Manually via `/mck-scaffold:refresh-research`.

## Pipeline

```
Step 1: read current state (last-run.json + all streams/*.md)
Step 2: confirm refresh with user (cost is real — 4 parallel agents, ~5-10 min)
Step 3: launch 4 parallel research subagents
Step 4: wait for all 4 to complete; consolidate findings
Step 5: diff new findings against current streams/*.md
Step 6: present diff to user; per-section confirm
Step 7: apply confirmed changes to streams/*.md + routing.md + preset templates
Step 8: update research/last-run.json + append to research/changelog.md + write new research/findings.md
Step 9: surface summary; offer to commit to git
```

---

## Step 1 — read current state

Read the plugin root's `research/last-run.json`. Extract:

- `timestamp_iso`, `timestamp_human`
- `mck_scaffold_version_at_run`
- `streams_completed`
- `summary` (short description of last run)
- `catalog_frameworks_count`
- `known_drifts_since_last_run` (if any drift was logged but not yet applied)

Compute `days_since_last_run` from `timestamp_iso` against today.

Read all `research/streams/*.md` files into memory — these are the **baseline** that the diff will compare against.

---

## Step 2 — confirm refresh with user

Print a context block:

```
mck-scaffold research-refresh

Last run: {timestamp_human} ({days_since} days ago)
Streams covered: {streams_completed}
mck-scaffold version at last run: {mck_scaffold_version_at_run}

A refresh runs 4 parallel research subagents:
  - github-landscape  (~2-3 min)
  - reddit-signal      (~2-3 min — may be degraded if Reddit MCP is down)
  - youtube-tutorials  (~2-3 min — may be degraded without transcript MCP)
  - web-blogs          (~2-3 min)

Total expected wallclock: 5-10 minutes (parallel).
Token cost: ~equivalent to 4 medium research conversations.

Proceed?
```

Use `AskUserQuestion` with options:
- **Yes — run all 4 streams** (full refresh)
- **Yes — but only specific streams** (then ask which via second AskUserQuestion; useful when only github/blog drift is suspected)
- **No — abort** (do nothing; return to caller)

If user opts to subset streams, set the `streams_to_run` variable accordingly. Default = all 4.

---

## Step 3 — launch parallel research subagents

For each stream in `streams_to_run`, launch an `Agent` call (`subagent_type: general-purpose`, run in background) with the appropriate brief:

### github-landscape brief

```
You are refreshing the github-landscape stream of the mck-scaffold catalog.

Goal: produce an updated structured snapshot of agentic-coding SDD frameworks
on GitHub. Focus on what affects routing decisions: framework existence, install
commands, star counts (approximate), deprecation status, and breaking changes
to the install command surface.

Current baseline lives in: {plugin_root}/research/streams/github-landscape.md

Read that first to know what frameworks are already tracked. Then for each:
1. Visit the GitHub repo (WebFetch or gh CLI)
2. Confirm install command is still current (any deprecations? new flags?)
3. Update approximate star count
4. Note any breaking changes since the baseline was written
5. Add any NEW frameworks that have emerged in the same space

Also re-survey for newly-prominent L1/L2/L3 frameworks that weren't in the
baseline. Search "spec-driven development claude code" / "SDD framework claude"
on github with stars:>500.

Return: a markdown document in the SAME structure as the current
streams/github-landscape.md, with the Framework facts table updated and a new
"Drift since prior run" column populated for each row. Note specifically:
- Frameworks unchanged (status quo)
- Frameworks with changed install commands
- Frameworks with significant star-count shifts (>30% change)
- New frameworks added
- Frameworks abandoned or deprecated (no commits in 6+ months)

Cap output at ~1500 words. Structured table > narrative.
```

### reddit-signal brief

```
You are refreshing the reddit-signal stream of the mck-scaffold catalog.

Goal: capture practitioner sentiment from Reddit on Claude Code agentic workflows
and SDD framework choices. CRITICAL: try primary Reddit access first (mcp__reddit
tools if available, or WebFetch against reddit.com). The last baseline run was
degraded — primary Reddit was unreachable and synthesis came from aggregators.
If primary access is still down, fall back to aggregators but FLAG it clearly.

Read current baseline: {plugin_root}/research/streams/reddit-signal.md

Search r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding for posts since {timestamp_human}
mentioning the frameworks in the catalog. Focus on:
- "Marketed but doesn't work" patterns (these are gold)
- New frameworks gaining adoption mentioned in 3+ threads
- Specific tooling combinations that recur
- Critical/skeptical posts about hyped methodologies

Return: a markdown document with same structure as current reddit-signal.md.
Note primary-vs-aggregator source status prominently at the top.

Cap output at ~1500 words.
```

### youtube-tutorials brief

```
You are refreshing the youtube-tutorials stream of the mck-scaffold catalog.

Goal: identify which creators/channels are publishing high-signal Claude Code
methodology content. Focus on tactics that affect routing decisions (e.g., new
HARD-GATE-style enforcement patterns, new subagent orchestration tools).

Read current baseline: {plugin_root}/research/streams/youtube-tutorials.md

Try mcp__youtube__get_transcripts on the URLs in the baseline first — verify
they still resolve and re-confirm tactics. Then search for new high-signal
videos since {timestamp_human}.

Channels to check first:
- Anthropic (official channel)
- Boris Cherny appearances
- IndyDevDan, Cole Medin, Net Ninja, alexop.dev, AI Jason, AI LABS
- BMad creator Brian
- Any new creators who emerge with 100k+ views on a Claude Code methodology video

Return: markdown with same structure as current youtube-tutorials.md.
Flag if transcript MCP was unavailable.

Cap output at ~1500 words.
```

### web-blogs brief

```
You are refreshing the web-blogs stream of the mck-scaffold catalog.

Goal: capture new authoritative engineering writeups on agentic coding, SDD,
and methodology choice. Focus on Anthropic's own engineering articles + the
named practitioner essayists in the baseline.

Read current baseline: {plugin_root}/research/streams/web-blogs.md

Check for:
- New Anthropic engineering articles since {timestamp_human}
- New essays from Ronacher, Willison, Litt, Husain
- New empirical studies (arXiv) on AI coding bugs / methodology effectiveness
- New production case studies (Shopify, Vercel, Sourcegraph, Stripe)
- New critical/skeptical pieces

Use WebSearch + WebFetch. For Microsoft/.NET-adjacent content, use the
microsoft-learn MCP if available.

Return: markdown with same structure as current web-blogs.md, updated tables
and citations.

Cap output at ~1500 words.
```

Launch all `Agent` calls in **a single message** (parallel). Track returned `agentId`s. Wait passively for completion notifications — do NOT poll the output files.

---

## Step 4 — consolidate findings

Once all 4 (or chosen subset) agents have returned:

1. Read each agent's output
2. Build a combined "new state" of the catalog
3. Note any agent that failed or produced degraded output

---

## Step 5 — diff against current

For each stream, compute a structured diff against the current `streams/*.md`:

- **Added:** new frameworks, new sources, new tactics that 3+ creators independently mention
- **Changed:** updated install commands, updated star counts (>30% shift), updated maturity status, deprecation flags
- **Removed:** frameworks abandoned or deprecated, sources that no longer resolve
- **Verified-unchanged:** items confirmed still current (no change needed, but worth noting)

Build a single consolidated diff document with these four sections per stream.

Also compute downstream impacts:
- Does the diff affect `interview/routing.md`? (e.g., changed install command, new framework added to a routing slot)
- Does it affect any `templates/methodologies/*/README.md` or `CLAUDE.append.md`? (e.g., changed slash command names, changed install flag)
- **Does it affect any `templates/methodologies/<id>/upstream.json`?** This is the canonical pin metadata file. Any drift in install commands, env requirements, or upstream version triggers an `scripts/update_upstream.py` invocation in Step 7 (with user confirmation). Identify the affected methodology IDs here so Step 7 can call the script with the right `--methodology` arg.
- Does it affect `reference_sdd_frameworks_2026.md` in user memory? (catalog refresh)

Surface these impact lists explicitly in the diff document.

---

## Step 6 — present diff, per-section confirm

Print the diff in a structured markdown block. For each section (Added / Changed / Removed / Verified) and each downstream impact, ask via `AskUserQuestion`:

> "Apply these changes to {file path}?"
> - **Yes — apply all in this section**
> - **Per-item review** (then walk each change individually with another `AskUserQuestion`)
> - **Skip this section**
> - **Abort entire refresh** (no changes applied; new findings discarded; user can re-run later)

Default per-section behavior: ask, don't apply.

For `--auto-apply` argument: skip the per-section prompts and apply all changes silently. **Print a warning at the start** that auto-apply skips review.

---

## Step 7 — apply confirmed changes

For each confirmed section, edit the affected files:

- `research/streams/{stream}.md` → write the new structured content
- `interview/routing.md` → patch install commands or routing table rows
- `templates/methodologies/{preset}/README.md` and `CLAUDE.append.md` → patch references, command names, install instructions
- **`templates/methodologies/<id>/upstream.json`** → **always invoke `scripts/update_upstream.py` (single bump) or `scripts/apply_research_drift.py` (bulk) rather than editing the JSON directly**. Direct edits bypass the drift_log accounting and should be reserved for fixing typos in past entries.

  **Single methodology, one drift** → `scripts/update_upstream.py`:

  ```
  python scripts/update_upstream.py \
      --methodology L1-spec-kit \
      --pinned-ref v0.6.0 \
      --drift-note "v0.6.0 adds --quiet flag; --force now default" \
      --install-command "windows=uvx --from git+https://github.com/github/spec-kit.git@v0.6.0 specify init . --integration claude --script ps" \
      --install-command "unix=uvx --from git+https://github.com/github/spec-kit.git@v0.6.0 specify init . --integration claude --script sh" \
      --verified-by "manual smoke test on a sandbox project"
  ```

  **Multiple methodologies in one refresh** (typical case) → build a drift document and call `scripts/apply_research_drift.py` once. The drift schema:

  ```json
  {
    "schema_version": 1,
    "research_refresh_timestamp": "2026-05-20T10:00:00Z",
    "drifts": [
      {
        "methodology": "L1-spec-kit",
        "new_pinned_ref": "v0.6.0",
        "drift_note": "v0.6.0 adds --quiet flag; --force now default",
        "install_commands": {
          "windows": "uvx --from git+https://github.com/github/spec-kit.git@v0.6.0 specify init . --integration claude --script ps",
          "unix": "uvx --from git+https://github.com/github/spec-kit.git@v0.6.0 specify init . --integration claude --script sh"
        },
        "verified_by": "manual smoke test"
      },
      {
        "methodology": "L1-bmad",
        "new_pinned_ref": "v6.0.0",
        "drift_note": "v6 stable release",
        "verified_by": "release notes review"
      }
    ]
  }
  ```

  Apply:

  ```
  python scripts/apply_research_drift.py --drift-file <path>/drift.json --dry-run
  # confirm with user, then:
  python scripts/apply_research_drift.py --drift-file <path>/drift.json
  ```

  The bulk script returns a per-entry results array. Unknown methodologies are skipped (not errors); methodologies without an `upstream.json` are skipped; missing required fields are surfaced as per-entry errors without aborting the whole batch.

- (Optional) `reference_sdd_frameworks_2026.md` in user memory — only if the user opts in to memory refresh

Use `Edit` for surgical patches when possible (preserves diff history). Use `Write` only for full-file replacements (the streams/*.md files specifically). Always invoke `scripts/update_upstream.py` for upstream.json changes.

---

## Step 8 — update timestamps + changelog

1. Read current `research/last-run.json`
2. Build a new version:
   - `timestamp_iso` = now
   - `timestamp_human` = today
   - `mck_scaffold_version_at_run` = read from `.claude-plugin/plugin.json`
   - `run_kind` = "refresh" (not "baseline" — only the first run is baseline)
   - `streams_completed` = list of streams that ran successfully
   - `summary` = 1-2 sentence summary of what changed
   - `known_drifts_since_last_run` = items flagged for next time
3. Write the updated `research/last-run.json`

4. Append an entry to `research/changelog.md` at the TOP:

```markdown
## {today} — Refresh — {short title}

**Refresh kind:** refresh

### Frameworks tracked (delta from prior run)

{added / changed / removed counts}

### Files updated in this delta

- {file path} — {what changed}
- ...

### Validated via

{how findings were verified — direct GitHub access, working MCP, etc.}

### Notable findings preserved for future diffs

{free-text notes that don't fit the structured tables but matter}
```

5. Update `research/findings.md` — re-synthesize the consolidated narrative from the new streams/*.md content.

---

## Step 9 — summary + offer commit

Print a closing block:

```markdown
✅ mck-scaffold research-refresh complete.

## What changed

- {N} frameworks added
- {N} frameworks changed (install commands, star counts, maturity)
- {N} frameworks removed
- {N} verified unchanged

## Files updated

{list of file paths edited}

## Manual review recommended

{any items that flagged for human eyes — e.g., new framework that doesn't cleanly map to a routing slot yet}

## Next

This is a shared-repo refresh. To make it available to other users / your other machines:

1. Review the diff: `git -C "{mck_scaffold_path}" diff`
2. Stage and commit: `git -C "{path}" add research/ interview/routing.md templates/ && git commit -m "chore(research): refresh catalog {today}"`
3. Push: `git -C "{path}" push`

Want me to run those for you? (Yes / I'll do it manually)
```

If user says yes, run the git commands via `Bash`. If user opts to do manually, end here.

---

## Argument handling

- `--auto-apply` — skip per-section confirm prompts at Step 6. Print warning at Step 2. Apply all confirmed-by-default sections silently. Useful for CI / scheduled refreshes; risky for first runs.
- `--streams=github-landscape,web-blogs` — comma-separated list of which streams to run. Default = all 4.

---

## Acceptance criteria (Phase 12 / v0.11.0)

- [ ] Skill auto-triggers on relevant user phrases
- [ ] Step 1 reads `research/last-run.json` and reports staleness in days
- [ ] Step 3 launches 4 parallel `Agent` calls (or subset per `--streams`)
- [ ] Step 5 produces a STRUCTURED diff (Added / Changed / Removed / Verified per stream + downstream impact list)
- [ ] Step 6 prompts per-section before applying anything
- [ ] Step 8 writes a new `last-run.json` and appends to `changelog.md`
- [ ] `--auto-apply` works as documented (warning + apply-all behavior)
- [ ] If primary Reddit access is still degraded, the reddit-signal output flags it explicitly (epistemic-discipline carry-through)

---

## Implementation notes for Claude (not user-facing)

- `Agent` tool calls in Step 3 must be in a **single message** for true parallelism. Multiple sequential messages = sequential execution.
- Background-mode agents (run_in_background: true) is appropriate — wait passively for completion notifications, do NOT poll output files.
- Use `TaskCreate` at Step 2 to make this run trackable; mark in_progress / completed as steps execute.
- For the diff at Step 5: use a structured representation (Python-dict-style or YAML-style) that's both human-readable and machine-parseable. Phase 12.1 will auto-apply confirmed sections; the parser depends on consistent diff format.
- For `routing.md` patches in Step 7: prefer `Edit` with surgical old_string/new_string. Avoid full-file rewrites — they nuke git blame.
- Re: epistemic rigor — the agents should flag confidence per finding. "Updated by direct GitHub view" = Verified; "from aggregator without primary source" = Moderate; "single source claim" = Low. Carry these confidence tiers into the diff so the user can weight per-section.
