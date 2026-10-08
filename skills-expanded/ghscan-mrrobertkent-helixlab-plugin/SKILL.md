<objective>
Fix the record-browser skill to resolve the AskUserQuestion auto-resolve bug, align the question templates with the confirmed AskUserQuestion schema, add timeout/error handling instructions, create a self-healing examples file, and ensure the SKILL.md is under 500 lines with proper XML structure.

This skill is part of the HelixLab Claude Code plugin. It launches a headed Chrome browser with recording and annotation tools. The skill must work standalone or chained with vision-replay.
</objective>

<context>
Read these files to understand the current state:
- `CLAUDE.md` for project conventions
- `skills/record-browser/SKILL.md` — the skill definition to fix
- `skills/record-browser/references/question-templates.md` — AskUserQuestion templates
- `skills/record-browser/scripts/recorder.js` — the Node.js recorder (read-only, do not modify)
- `skills/record-browser/scripts/launch-recorder.sh` — launch script (read-only, do not modify)

Key research findings that inform this work:

**AskUserQuestion auto-resolve bug (root cause):**
The SKILL.md frontmatter currently lists `AskUserQuestion` in `allowed-tools`. When a tool is in `allowed-tools`, it gets added to the `alwaysAllowRules` permission set. The permission evaluator has an early-return path that bypasses the `requiresUserInteraction()` check, causing the tool to auto-complete with empty answers. The user never sees the prompt. This is confirmed Claude Code bug (Issue #29547). The fix: remove `AskUserQuestion` from `allowed-tools`.

**AskUserQuestion confirmed schema:**
```
questions: array (1-4 questions, required)
  question: string (the question text, required)
  header: string (max 12 characters, required)
  multiSelect: boolean (must be explicit true/false, required)
  options: array (2-4 options, required)
    label: string (1-5 words, required)
    description: string (required)
```
- "Other" option is added automatically by the system — do NOT include it manually
- There are NO `annotations`, `notes`, or `markdown` fields in the schema
- Recommended options should be listed first with "(Recommended)" appended to the label
- 60-second timeout: if user doesn't respond, tool returns empty/default answers

**SKILL.md conventions (from Anthropic docs):**
- Keep SKILL.md under 500 lines
- YAML frontmatter with `name` and `description` (description should include when to use the skill)
- Body should contain the workflow and procedures
- References, templates, examples in subdirectories — loaded as needed by the agent
- XML tags in the body are the project convention — retain all XML structure
</context>

<requirements>

1. **Fix `allowed-tools` in SKILL.md frontmatter:**
   - Remove `AskUserQuestion` from the `allowed-tools` list
   - Keep all other tools: Bash, Read, Glob, Grep

2. **Remove the Step 4 "load templates" workaround:**
   - The current SKILL.md has an artificial "Step 4: Load question templates" step that was added as a workaround for the bug. Remove it entirely.
   - Restore the original step numbering: Steps should be 1 (launch), 2 (user records), 3 (save dialog), 4 (ask user what to do next), 5 (ask preparation method), 6 (ask analysis mode), 7 (post-analysis cleanup)
   - Each step that uses AskUserQuestion should reference the template by name from `references/question-templates.md` (e.g., "Call AskUserQuestion using Template 1 from `references/question-templates.md`")

3. **Update `references/question-templates.md` to match confirmed schema:**
   - Remove any `markdown` fields from options (they don't exist in the schema)
   - Remove any references to `annotations` or `notes` fields
   - Ensure all `header` values are max 12 characters
   - Ensure all option arrays have 2-4 options
   - Ensure `multiSelect` is explicitly set on every question
   - Keep the "(Recommended)" convention on recommended options
   - Remove any instructions about pressing 'n' for notes (that feature doesn't exist)

4. **Add timeout and empty-response handling to SKILL.md:**
   - At each AskUserQuestion step, add a brief instruction: "If AskUserQuestion returns empty or no response (60-second timeout), inform the user the question timed out and re-ask. Do NOT auto-proceed or assume a default."
   - This should be concise — one sentence per step, not a full paragraph

5. **Create `examples/error-handling.md`:**
   - Create a new file at `skills/record-browser/examples/error-handling.md`
   - Include examples of common error scenarios and how the agent should handle them:
     a. Chrome fails to launch (binary not found, permissions, display server missing)
     b. Recording fails to start (getDisplayMedia error, no capture stream)
     c. Browser closes unexpectedly mid-recording (process exits, WebSocket drops)
     d. Save fails (disk full, permission denied, invalid path)
     e. AskUserQuestion times out or returns empty
     f. Vision-replay scripts fail (ffmpeg missing, invalid video format)
   - For each scenario: describe the error, what the agent should tell the user, and the recovery action
   - Reference this file in SKILL.md with a brief note like: "For error recovery patterns, consult `examples/error-handling.md`"

6. **Add known issue note about Chrome closure crash:**
   - In SKILL.md, add a brief `<known_issues>` section noting: "Chrome for Testing v146 may show a 'quit unexpectedly' dialog when the browser is closed. This is cosmetic — it does not affect recording, video saving, or the workflow. A fix is planned."

7. **Verify SKILL.md is under 500 lines:**
   - After all changes, count lines. If over 500, move detailed content to references/
   - The recording_controls, annotation_tools, keyboard_shortcuts, and recording_modes sections are candidates for extraction to references/ if line count is too high
</requirements>

<constraints>
- Do NOT modify any scripts (recorder.js, cdp.js, launch-recorder.sh, stop-recorder.sh, install-browser.sh)
- Do NOT modify welcome.html or playground.html
- Do NOT modify any files outside the `skills/record-browser/` directory
- Do NOT remove XML tags from the SKILL.md body — retain all existing XML structure
- Do NOT change the core workflow logic — only fix the AskUserQuestion integration and add error handling
- Do NOT add AI attribution or co-authored-by lines to any commits
- Keep the `references/question-templates.md` file in its current location — do not move or rename it
</constraints>

<verification>
After all changes:
1. Confirm `AskUserQuestion` is NOT in `allowed-tools` in the SKILL.md frontmatter
2. Confirm SKILL.md has 7 steps (not 8) with correct numbering
3. Confirm `references/question-templates.md` has no `markdown`, `annotations`, or `notes` fields
4. Confirm all `header` values in templates are max 12 chars
5. Confirm `examples/error-handling.md` exists and covers all 6 scenarios listed
6. Confirm SKILL.md is under 500 lines (run `wc -l`)
7. Confirm SKILL.md retains XML tag structure in the body
8. Confirm each AskUserQuestion step has the timeout handling instruction
9. Confirm the `<known_issues>` section exists with the Chrome closure note
</verification>

<success_criteria>
- AskUserQuestion will no longer auto-resolve (removed from allowed-tools)
- Question templates match the confirmed AskUserQuestion schema exactly
- Agent knows how to handle timeouts and empty responses gracefully
- Agent has error-handling examples to consult for self-healing
- SKILL.md is clean, under 500 lines, with XML structure intact
- Chrome closure known issue is documented
</success_criteria>
