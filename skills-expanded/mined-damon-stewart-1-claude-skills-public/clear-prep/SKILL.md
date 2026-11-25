---
name: clear-prep
description: This skill should be used when the user says "/clear-prep", "prep for context clear", "prepare to clear", "handover prompt", "I'm going to clear the context", "relay context to a new instance", "snapshot my session", "session is getting full", "give me a handover", or "context is running out". Generates a self-contained handover prompt the user pastes into a cleared Claude Code instance so work continues seamlessly with zero re-explanation.
user_invocable: true
---

# clear-prep

Generate a self-contained handover prompt for a cleared Claude Code instance. No logging, no Productive, no sync-context, no `git diff`. Pure relay.

---

## Step 0: Check for Viable Session

If the conversation has fewer than ~3 substantive turns AND no files were mentioned/edited AND no commands were run, output: "No active session to relay. Describe the project or task first, then run /clear-prep." Stop. A planning-only or research-only session with substantive decisions IS viable.

## Step 1: Read MEMORY.md

Read `~/.claude/projects/$(basename $HOME)/memory/MEMORY.md` (adjust path to match your setup). Store its contents for the delta check in Step 6. If unreadable: skip the delta check and add a high-priority entry to `## Warnings`.

## Step 2: Session Analysis

Scan conversation history to populate: **Decision Log** (explicit decisions and rejections with reasons), **Session State** (goal, completed vs. in progress, working directory), **Blocked On** (unresolved blockers/dependencies), **Warnings** (gotchas, tool failures, session-specific instructions), **Environment State** (`export`, `source`, `alias`, `conda activate`, `nvm use`, or similar ephemeral shell commands).

## Step 3: Identify Active Scope

Check for `/scope` invocations, agent file references, or the working directory of most recently referenced files. List all projects/directories touched. If undeterminable, note "No active scope detected."

## Step 4: File Snapshot Fingerprinting

Read `references/fingerprint-patterns.md` for the exact commands, output format, caps, and edge case handling. Fingerprint all relevant files.

## Step 5: Dispatch Job Ingestion

```bash
ls -t ~/.claude/jobs/*.md 2>/dev/null
```

Filter to files modified within the last 2 hours (`stat -f %m` vs `date -v-2H +%s`). For complete jobs: extract results (up to 10 lines). For running jobs: note ID, task, status, and add a warning not to modify affected files.

## Step 6: Memory Delta Check

Compare session context against MEMORY.md from Step 1. Include anything that meets ALL criteria: falls into a concrete category (user preference, project constraint, architectural decision, deployment target, API credential location, team/people context, or non-obvious workflow), is NOT already in MEMORY.md, and would be useful weeks from now. If nothing qualifies, omit the section.

## Step 6b: Plugin Debrief

Scan this session for gaps in the plugin system. Look for three things only:
1. A hook that should exist or a current hook that didn't catch something it should have
2. A workflow that repeated enough to warrant a new skill or an addition to an existing one
3. Something learned about a client that isn't in their agent `.md` file

For each gap found, propose a specific diff: which plugin file (hooks/, skills/, agents/), what to add or change, and why. If nothing qualifies, say "No plugin gaps found." Do not propose CLAUDE.md edits or memory file writes here -- that's Step 6.

## Step 7: Sanitization Pass

Read `references/section-rules.md` for the complete list of secret patterns to scan for. Replace any match with `[REDACTED -- see Keychain or passwords app]`. Never output a real secret.

## Step 8: Assemble Output

Read `references/handover-template.md` for the exact output structure. Do not ask for approval. Output a single fenced code block. Read `references/section-rules.md` for which sections are required vs. optional.

## Step 9: Copy to Clipboard

After outputting the fenced handover block, immediately copy its contents (the text inside the fences, not the fences themselves) to the macOS clipboard:

```bash
cat <<'CLEAR_PREP_EOF' | pbcopy
<the full handover content here, exactly as it appeared in the fenced block>
CLEAR_PREP_EOF
```

Use a heredoc with a unique sentinel (`CLEAR_PREP_EOF`) so embedded backticks, dollar signs, and quotes pass through untouched. Do not use `echo` or `printf` (they mangle special chars). After running, output one final line confirming: `Handover copied to clipboard. Paste with Cmd+V into the cleared instance.`

If `pbcopy` fails (e.g., no display, headless), say so and skip silently rather than blocking.
