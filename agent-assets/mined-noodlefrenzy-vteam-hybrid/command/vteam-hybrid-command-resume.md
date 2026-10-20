<!-- agent-notes: { ctx: "resume from previous session handoff", deps: [.claude/handoff.md, CLAUDE.md, docs/plans/], state: active, last: "grace@2026-02-12" } -->
Resume from a previous session's handoff.

## Steps

1. **Read the handoff file.** Read `.claude/handoff.md`. If it doesn't exist, tell the user there's no handoff to resume from and ask what they'd like to do.

2. **Read project context.** In parallel, read:
   - `CLAUDE.md` (already loaded, but review for any recent changes)
   - `docs/product-context.md` (if it exists — the human's product philosophy)
   - The current plan in `docs/plans/` (if referenced in the handoff)
   - The auto-memory file at the path shown in your system prompt (if it exists)

3. **Verify state.** Run these checks:
   - `git log --oneline -5` — does the last commit match what the handoff says?
   - `git status` — is the working tree clean? If not, investigate before proceeding.
   - **GitHub Board Pre-Flight (Blocking):** If `CLAUDE.md` has a `project-number` and `project-owner` configured (not commented out / not blank), run the full pre-flight:
     1. `gh auth status` — if this fails, STOP: "GitHub CLI is not authenticated. Please run `gh auth login` and try again."
     2. `gh project field-list <NUMBER> --owner <OWNER> --format json` — if this fails, STOP: "Cannot access project board #<NUMBER>. Check your auth scopes (you may need `gh auth refresh -s project`) and that the project exists."
     3. Verify the Status field has all 5 required options (Backlog, Ready, In Progress, In Review, Done). If any are missing, STOP and report.

     **Do not proceed to step 4 if board access fails.** A sprint running without board access causes silent tracking failures — every status transition is skipped, and the sprint boundary will find a broken board. Fix it now, not after a full sprint of lost state.

4. **Summarize to the user.** Give a brief (5-10 line) summary:
   - What the previous session accomplished
   - Current state of the project
   - What you're about to do next

5. **Check for proxy decisions.** If the handoff contains a `## Proxy Decisions (Review Required)` section with entries, surface them to the human **immediately** before continuing any other work. Ask: "Pat made these decisions while you were away. Do you want to review or override any of them?" Do not proceed until the human acknowledges the proxy decisions.

6. **Ask for confirmation.** Before executing, ask: "Ready to pick up from here? Or would you like to adjust the plan?"

7. **Execute.** Proceed with the "What To Do Next" items from the handoff. Follow all CLAUDE.md conventions (TDD, conventional commits, agent-notes, etc.).

## If the user provides $ARGUMENTS

Treat the arguments as an override or addition to the handoff's "What To Do Next" section. For example:
- `/resume focus on issue #14` — prioritize that issue over the handoff's suggested order
- `/resume skip to deployment` — jump ahead in the plan

## Important

- Do NOT blindly trust the handoff. Verify against actual repo/board state. If there's a discrepancy, flag it.
- The handoff is a starting point, not a straitjacket. If the user wants to change direction, that's fine.
- After resuming and completing a significant chunk of work, consider running `/handoff` again to update the state for the next potential session break.
