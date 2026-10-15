---
name: committing-to-git
description: Use when asked to draft, write, or revise a git commit message, or when asked to commit current uncommitted workspace changes. Make sure to use this skill whenever the user asks you to "commit", "draft a commit", "make a commit", or mentions saving their work to git. Also use when pushing a commit that was created by this workflow.
category: development
allowed-tools: [run_command, write_to_file, view_file]
compatibility: Requires Git and Node.js.
---

# Committing To Git

When asked to draft a commit message or commit current workspace changes, follow Sections 1–4. Execute Section 5 only when the user has explicitly requested creation of the commit. Execute `git push` only when the user has explicitly requested pushing. A request to push existing commits MUST NOT implicitly authorize staging or committing uncommitted workspace changes.

## 1. Pre-Commit Verification Workflow
* **Mandatory Execution Order**: To inspect the complete set of current uncommitted changes, you MUST:
  1. Execute `git status --untracked-files=all`.
  2. Execute `git diff HEAD` to inspect all staged and unstaged changes to tracked files.
  3. Inspect the complete contents of every untracked text file reported by `git status` by explicitly executing a file-reading tool (e.g. `view_file`). **CRITICAL**: Do NOT rely on your memory of what you wrote. Inspect the type and relevant metadata of untracked binary files sufficiently to determine their purpose.

## 2. Commit Message Composition
1. **Strict Scope Enforcement**: Base the commit message's technical scope and file modifications EXCLUSIVELY on the current uncommitted changes identified by the Pre-Commit Verification Workflow.
   - DO NOT fabricate file changes or list features drawn from conversation history, memory of earlier edits, or past prompts.
   - YOU MAY use conversation history solely to explain the rationale or context behind the changes (the "why"), provided it strictly aligns with the verified uncommitted changes.
   - DO NOT list files, features, or fixes that are already committed in previous commits, even if they were part of the same task session.
   - DO NOT mention fixes for intermediate regressions or syntax errors introduced during your own uncommitted edits.
2. **Imperative Mood Throughout**: Use the imperative, present-tense mood for the subject line's `<description>` and all commit-message change descriptions and bullet points (e.g., "Fix", "Add", "Update", "Suppress" — NEVER "Fixed", "Added", "Updates", or "Suppressing"). **CRITICAL**: Before asking for review, you MUST isolate the first word of the subject line and the first word of every bullet point, and explicitly confirm that each is a base-form verb.
3. **Body Line Wrapping**: Wrap body prose at 72 characters. Never hard-wrap file paths, URLs, command names, identifiers, or other indivisible tokens.
4. **Structure**:
   - Separate all sections with **exactly one blank line**.
   1. **Subject Line (Header)**:
      - Format: `<type>(<scope>): <description>` or `<type>: <description>`, where `<scope>` is optional (e.g., `fix(ui): Suppress long-press menu on UI controls`). `<type>` MUST be exactly one of `build`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, or `test`.
      - Length: Target **~50 characters**, and **NEVER exceed 72 characters**.
      - Formatting: Capitalize the first word after type/scope; do NOT end with a period (`.`).
   2. **User Experience Changes Section**:
      - Include this section only when the changes have an observable impact on the end user.
      - Format:

      ```
      User Experience Changes:
        - <first change>
        - <second change>
        - <Nth change>
      ```

      - **Content Scope**: Strictly describe only changes that are observable by the end user.
      - Describe each user-visible outcome as an imperative change statement beginning with a base-form verb (e.g., "Enable", "Improve", "Prevent", "Reduce", etc.).
      - Avoid technical jargon, framework details (e.g. "Jest", "Node.js heap", "OOM"), or implementation specifics in this section. Frame it purely around what the end user perceives or experiences differently as a result of these changes (e.g. "Enable the visualisation of a new file type", "Improve rendering performance").
   3. **File Changes Section**:
      - Format:

      ```
      File Changes:
        1. `<first changed file's file path>`
           - <distinct logical change and brief rationale>
           - <Nth distinct logical change and brief rationale>
        2. `<Nth changed file's file path>`
      ```

      - Include every changed file exactly once.
      - Ensure there are exactly two spaces before the file number (e.g., `  1. `).
      - Order file paths **alphabetically** using relative workspace paths (e.g., `src/app/css/toolstyle.css`).

## 3. Deterministic Commit Message Validation

1. **Scratch File**: Write the proposed commit message to `scratch/commit_msg.txt` in your conversation artifacts scratch directory outside the workspace repository. Never create the scratch file inside the repository working tree.

2. **Mandatory Validator**: You MUST validate the proposed commit message using `scripts/validate-commit-message.mjs`. Resolve the script path relative to this skill's directory and execute: `node <skill-path>/scripts/validate-commit-message.mjs <path-to-scratch/commit_msg.txt>`

3. **Validator Authority**: Treat the validator as authoritative for all mechanically testable commit-message requirements, including:
   - subject syntax, type, capitalization, trailing period, and character length;
   - section ordering and blank-line delimiters;
   - structural formatting of `User Experience Changes` and `File Changes`;
   - File Changes numbering, uniqueness, and alphabetical ordering; and
   - correspondence between File Changes paths and the current changed files relative to `HEAD`, including untracked files.

4. **No Ad-Hoc Validation**: DO NOT manually count characters or create ad-hoc Python, JavaScript, PowerShell, shell, or other commands to reproduce checks performed by the validator.

5. **Validation Errors**: If the validator exits with status 1 or returns `"valid": false`, correct every `"error"` issue and re-run the validator until it returns `"valid": true`.

6. **Manual Review Issues**: If `"manualReviewRequired": true`, review each `"review"` issue. An overlong body line is acceptable only when exceeding 72 characters is necessary to preserve an indivisible file path, URL, command name, identifier, or similar token. Otherwise wrap the line and re-run the validator.

7. **Execution Failure**: If the validator exits with status 2, stop and resolve the validator execution failure before proceeding.

## 4. Commit Message Review
1. **Ask For Review**: Present ONLY the exact validated contents of `scratch/commit_msg.txt` followed by a brief prompt asking the user to review and approve or request changes before proceeding. **CRITICAL**: Do NOT include conversational filler, boilerplate text (e.g., "I have completed the verification...", "Here is the proposed message..."), or the results of your programmatic checks. The user expects concise output.
2. **Iterate**: Do not create the commit until the user explicitly approves the proposed commit message. If the user requests changes, revise the message in the scratch file, re-run the validator, and request approval again.

## 5. Execution Commands
* **Local Git CLI Execution**: To ensure local workspace files and `.git` refs remain cleanly synchronized, you MUST run the following local Git CLI commands in order. If any command fails or exits with a non-zero status, stop immediately and DO NOT execute any subsequent command:
   1. `git add -A`
   2. `git diff --cached --name-only` to verify that the staged snapshot exactly matches the verified uncommitted changes on which the approved commit message was based. **CRITICAL**: You MUST explicitly compare this output list against the files you intended to stage. If any unintended files are in this list, you MUST unstage them before committing. If the snapshot is fundamentally incorrect, DO NOT commit; re-run the Pre-Commit Verification Workflow, revise the commit message as necessary, and return to Section 4 for explicit user approval.
   3. `git commit -S -F <path-to-scratch/commit_msg.txt>`
   4. `git verify-commit HEAD`. This command MUST exit with status 0. If verification fails, stop immediately and DO NOT push.
   5. If and only if the user explicitly requested pushing, execute `git push`.

## 6. Examples

* **Input**:
> Commit our changes

* **Output**:
> ```text
> feat(skills): Harden committing-to-git with strict programmatic guards
> 
> File Changes:
>   1. `skills/committing-to-git/SKILL.md`
>      - Enforce programmatic checks for subject and body line
>        length to prevent visual estimation errors
>      - Mandate explicit use of file-reading tools for
>        untracked files
>      - Require explicit staging verification using name-only
>        diffs
>      - Add a strict post-composition grammar check for
>        imperative mood
> ```
> 
> Please review the proposed commit message. Do you approve, or would you like to request any changes before I proceed with creating the commit?
