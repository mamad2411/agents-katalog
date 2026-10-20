<!-- agent-notes: { ctx: "session handoff for wave-based sprint execution", deps: [CLAUDE.md, docs/sprints/, docs/code-map.md], state: active, last: "coordinator@2026-02-15" } -->
Create a session handoff document so the next session can pick up where this one left off.

## Steps

1. **Assess current state.** In parallel, run:
   - `git log --oneline -10` — recent commits
   - `git status` — working tree state
   - `git diff --stat` — uncommitted changes summary
   - **Board check (if configured):** If `CLAUDE.md` has `project-number` and `project-owner` set, verify access first with `gh auth status` and then `gh project item-list <NUMBER> --owner @me --format json`. If board access fails, warn the user: "Board access failed — handoff will be written without board status. Fix GitHub access before the next session resumes." Continue writing the handoff (it's still useful), but note the board gap in the handoff's Current State section.

2. **Summarize what was done.** Review the work completed in this session:
   - What features/fixes were implemented
   - What tests were written/updated
   - What docs were created/updated
   - What ADRs were created
   - What's committed vs. uncommitted

3. **Sprint wave context.** Check `docs/sprints/` for the current sprint wave plan:
   - Which wave was this session executing?
   - Which issues in the wave are Done vs. in-progress vs. not started?
   - What's the next wave? List the issues with their titles and sizes.

4. **Identify what's next.** Based on the wave plan and any in-flight work:
   - What's the immediate next task (or next wave)?
   - What's blocked and on what?
   - What decisions are pending human input?
   - What open questions remain?

5. **Check tracking artifacts.** Read `docs/tracking/` for any active tracking artifacts from this session. Include the latest artifacts in the handoff so the next session can pick up phase context without re-discovering it. Also check if `docs/product-context.md` exists and note its last-updated date in the handoff.

6. **Write the handoff file.** Create or update `.claude/handoff.md` with this structure:

```markdown
# Session Handoff

**Created:** <today's date>
**Sprint:** <sprint number>
**Wave:** <wave number/name> of <total waves>
**Session summary:** <1-2 sentence summary>

## What Was Done
- <bulleted list of accomplishments>

## Current State
- **Branch:** <current branch>
- **Last commit:** <hash + message>
- **Uncommitted changes:** <description or "none">
- **Tests:** <total passing> across <N> test files
- **Board status:** <summary>

## Sprint Progress
- **Wave plan:** `docs/sprints/sprint-<N>-plan.md`
- **Current wave:** <wave number> — <status>
- **Issues completed this session:** #X, #Y, #Z
- **Issues remaining in wave:** #A, #B (with brief status)
- **Next wave:** <wave number> — <issues and sizes>

## What To Do Next (in order)
1. Read `docs/code-map.md` to orient
2. Read `docs/product-context.md` for human's product philosophy
3. Read `docs/sprints/sprint-<N>-plan.md` for wave context
4. <specific next task with file paths and enough context to execute>
5. ...

## Tracking Artifacts
- <list any active tracking artifacts from `docs/tracking/` relevant to in-flight work>
- <include the artifact file names so the next session can read them for phase context>

## Proxy Decisions (Review Required)
<!-- If Pat made proxy decisions while the human was unavailable, list them here -->
<!-- Each entry: question asked, Pat's decision, rationale, reversibility -->

## Key Context
- <any non-obvious context the next session needs>
- <files that were being actively worked on>
- <gotchas discovered during this session>
```

7. **Update MEMORY.md.** Ensure the session memory file has current sprint status and any new patterns discovered.

8. **Commit the handoff.** If there are uncommitted changes, ask the user if they want to commit before creating the handoff. Then commit the handoff file itself.

## Important

- Be specific in "What To Do Next" — include file paths, function names, and enough detail that the next session doesn't need to re-discover context.
- The handoff's job is to make the next session's first 2 minutes productive, not its first 10 minutes.
- "Read code-map.md" should always be step 1 in "What To Do Next" — it replaces codebase exploration.
- Don't include sensitive information (tokens, credentials, personal data) in the handoff.
- If the session discovered patterns or gotchas, update `docs/process/gotchas.md` (durable) not just the handoff (ephemeral).
- Add agent-notes frontmatter to the handoff file per `docs/methodology/agent-notes.md`.
