<!-- agent-notes: { ctx: "kaizen retrospective with GH issues for findings", deps: [docs/methodology/personas.md, CLAUDE.md], state: active, last: "grace@2026-02-14" } -->
Reflect on the work done in this sprint/session. Consider:

1. What went well?
2. What was harder than expected?
3. Were there any recurring patterns or friction points?
4. What would have made the work easier or faster?
5. Are there any new conventions, gotchas, or patterns to document?
6. Which v-team personas (see `docs/methodology/personas.md`) were effectively engaged during this session? Which were missing?
7. Were there moments where a persona's perspective would have caught an issue earlier?
8. Should any persona definitions in `docs/methodology/personas.md` be updated based on this experience?
9. **Were any process issues identified in a previous retro still recurring?** If so, the previous fix was insufficient — escalate.

Then take these actions:

### Document the retro
- Create a retrospective file at `docs/retrospectives/{{date}}-<topic>.md` summarizing the reflection. Add agent-notes frontmatter per `docs/methodology/agent-notes.md`.
- Update `CLAUDE.md` with any new patterns, conventions, or lessons learned.
- Create or update custom commands in `.claude/commands/` if a repeatable workflow emerged during this session.
- If any architectural decisions were made implicitly, capture them as ADRs in `docs/adrs/`.

### Create GitHub issues for every identified problem (MANDATORY)

For **each** problem, friction point, or process failure identified in the retro, create a GitHub issue:

1. Ensure the `process-improvement` label exists: `gh label create "process-improvement" --description "Process issue identified in sprint retro" --color "d93f0b" --force`.
2. For each identified problem, create an issue:
   ```
   gh issue create --title "Process: <concise description>" --body "<details from retro, what went wrong, proposed fix>" --label "process-improvement"
   ```
3. **These issues gate the next sprint.** They must be resolved or explicitly scheduled into the next sprint before new sprint work can begin. This is enforced by `/sprint-boundary` Step 3.

**Why this matters:** Without this step, retro findings become "lessons learned" docs that nobody reads. By turning them into issues, they become tracked work that blocks forward progress until addressed. This prevents the same process failures from recurring sprint after sprint.

### Check for recurring issues

If a problem identified in this retro was **also** identified in a previous retro (check `docs/retrospectives/` for past entries), this is a red flag:
- The previous fix was insufficient. Note this explicitly in the issue body.
- Consider whether the fix needs to be more structural (e.g., adding a checklist, a gate, or a command) rather than just a note in CLAUDE.md.
- Label these issues with both `process-improvement` and `recurring` (`gh label create "recurring" --description "Issue that has recurred across sprints" --color "b60205" --force`).
