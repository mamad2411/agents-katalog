---
name: update-jira-ticket
version: 1.2.0
description: Compare the JIRA ticket description to changes made in the current branch and propose description edits and/or comments to keep the ticket accurate and well-documented.
argument-hint: ""
---

Compare the JIRA ticket associated with the current branch against the actual changes made, and propose updates to keep the ticket accurate. Edits the description for missing information, adds comments for unrelated changes or implementation decisions, or both.

**Usage:**
- `/update-jira-ticket` - Analyze branch changes and propose JIRA ticket updates

**Instructions:**

1. **Check prerequisites:**
   - **Atlassian CLI (`acli`):** Run `acli auth status` to check if the CLI is installed and authenticated.
     - If the command is not found, display the following message and **STOP**:
       ```
       ## Missing Prerequisite: Atlassian CLI

       The `acli` command is not installed. This skill requires the Atlassian CLI to fetch and update JIRA issue details.

       Install it with: brew tap atlassian/acli && brew install acli
       ```
     - If the command fails with an authentication error, display the following message and **STOP**:
       ```
       ## Missing Prerequisite: Atlassian CLI Authentication

       The Atlassian CLI is not authenticated. Please run `acli auth login` to authenticate before using this skill.
       ```

2. **Extract the JIRA ID from the current branch name:**
   - Run `git branch --show-current` to get the current branch name
   - Extract the JIRA ID by matching the pattern `[A-Z][A-Z0-9]+-[0-9]+` (e.g., `PROJ-123`, `AB-1`, `MYAPP-4567`)
   - The JIRA ID can appear anywhere in the branch name (e.g., `fix/PROJ-123`, `feat/PROJ-123`, `PROJ-123-some-description`)
   - The match should be case-insensitive — normalize the extracted ID to uppercase for the JIRA API lookup
   - If no JIRA ID is found, display the following message and **STOP**:
     ```
     No JIRA ID found in branch name: "<current-branch>"
     Expected a branch name containing a JIRA ID (e.g., fix/proj-123, feat/MYAPP-456).
     ```

3. **Fetch the JIRA ticket:**
   - Use the Atlassian CLI to retrieve the issue by its JIRA ID:
     ```bash
     acli jira workitem view <JIRA-ID> --fields '*all' --json
     ```
   - Parse **all available fields**: summary, description, issue type, priority, comments, acceptance criteria, custom fields, etc.
   - Store the **original description** for comparison — this is the baseline
   - If the fetch fails, display the error and **STOP**

4. **Determine the base branch:**
   - Check if a `.agent` file exists in the current directory
   - If it exists, read it and look for a `baseBranch=<value>` line to extract the base branch
   - If no `.agent` file or no `baseBranch` key, default to `main`

5. **Analyze the branch changes:**
   - Run `git log <base-branch>..HEAD --oneline` to get the commit history on this branch
   - Run `git diff <base-branch>...HEAD --stat` to get a summary of files changed
   - Run `git diff <base-branch>...HEAD` to get the full diff
   - Read key modified files to understand the nature of the changes
   - Build a comprehensive understanding of:
     - **What was implemented** — new features, bug fixes, refactors, etc.
     - **How it was implemented** — technical approach, patterns used, key decisions
     - **What was changed beyond the original scope** — any additions, adjustments, or deviations from the ticket description

6. **Compare changes to the ticket description:**

   For each significant change or aspect of the implementation, categorize it into one of three types:

   **a) Missing from description — EDIT the description:**
   - Information that should have been in the ticket but wasn't (e.g., missing acceptance criteria that were implemented, undocumented requirements discovered during implementation, scope that was implicit but should be explicit)
   - The description should be edited to include this information for documentation and tracking

   **b) Unrelated to the ticket — ADD a comment:**
   - Changes that were made alongside the ticket work but aren't part of the ticket's scope (e.g., opportunistic refactors, small fixes in adjacent code, dependency updates)
   - These should be documented as comments so the ticket history captures what happened, without polluting the description

   **c) Implementation decision — EDIT the description AND ADD a comment:**
   - Changes where a deliberate technical or product decision was made that affects the ticket (e.g., choosing approach A over approach B, adjusting acceptance criteria based on technical constraints, scope adjustments agreed during implementation)
   - The description should be updated to reflect the final state, and a comment should explain the reasoning behind the decision

   **Skip silently** any changes that are:
   - Already accurately reflected in the current description
   - Trivial implementation details that don't affect the ticket's documentation value (e.g., variable names, minor formatting)

7. **Prepare the list of proposed edits:**

   Present all proposed changes as a numbered list, grouped by action type:

   ```
   ## Proposed JIRA Ticket Updates for <JIRA-ID>

   ### Description Edits
   These changes update the ticket description to reflect the actual implementation.

   **#1** — <Brief title of the edit>
   - **Reason:** <Why this edit is needed>
   - **Change:** <What will be added/modified in the description>

   **#2** — <Brief title>
   - **Reason:** <Why>
   - **Change:** <What>

   ### Comments to Add
   These document changes that don't belong in the description.

   **#3** — <Brief title of the comment>
   - **Reason:** <Why a comment is appropriate here>
   - **Content:** <The comment text to be added>

   ### Description Edits + Comments
   These require both a description update and a comment explaining the decision.

   **#4** — <Brief title>
   - **Reason:** <Why both are needed>
   - **Description change:** <What will be updated>
   - **Comment:** <The comment explaining the reasoning>

   ### Summary
   - **Description edits:** <N>
   - **Comments:** <N>
   - **Description edits + comments:** <N>
   - **Total updates:** <N>
   ```

   If there are no proposed changes (the ticket is already accurate), display:
   ```
   ✅ The JIRA ticket description for <JIRA-ID> is already in sync with the branch changes. No updates needed.
   ```
   And **STOP**.

8. **Get developer confirmation:**

   Use `AskUserQuestion` to ask the developer to review and approve the proposed updates:
   - **"Apply all"** — apply all proposed edits and comments
   - **"Let me choose"** — the developer will specify which items to apply (by number)
   - **"Skip"** — cancel, don't update the ticket

   **If "Let me choose":**
   - Use `AskUserQuestion` to ask which item numbers to apply (e.g., "1, 3, 4")
   - Only apply the selected items

9. **Apply the approved updates:**

   **a) Description edits:**
   - Read the current ticket description
   - Apply all approved description edits, integrating them naturally into the existing description structure
   - Preserve the original description's tone, formatting, and structure — don't rewrite sections that aren't being updated
   - Write the description as an ADF (Atlassian Document Format) JSON payload and use `--from-json` to update:
     ```bash
     acli jira workitem edit --from-json <temp-file.json> --yes
     ```
     The JSON file must contain the full edit payload with the description as an ADF object (see [ADF Format Reference](#adf-format-reference) below).
   - If the update fails, show the error and provide the proposed description as copyable text

   **b) Comments:**
   - For each approved comment, use the Atlassian CLI:
     ```bash
     acli jira workitem comment create --key <JIRA-ID> --body "<comment text>"
     ```
   - Each comment should be self-contained and clearly explain the context
   - Prefix implementation decision comments with "**Implementation note:**" for clarity
   - If a comment fails to post, show the error and provide the comment text as copyable text

10. **Show results:**

    Display a summary of what was applied:

    ```
    ## JIRA Ticket Updated: <JIRA-ID>

    ### ✅ Description Updated
    - #1 — <title>
    - #4 — <title>

    ### ✅ Comments Added
    - #2 — <title>
    - #3 — <title>
    - #4 — <title> (implementation note)

    ### ❌ Skipped
    - #5 — <title> (developer chose to skip)

    Ticket: https://<site>.atlassian.net/browse/<JIRA-ID>
    ```

11. **Handle edge cases:**
    - If the ticket description is empty, all implementation details count as "missing from description" — propose a complete description based on the changes
    - If there are no commits on the branch yet, display "No changes found on this branch compared to <base-branch>." and STOP
    - If the diff is too large to analyze in full, focus on the most significant changes (new files, large modifications) and note that some minor changes were not reviewed
    - If the JIRA update fails partially (e.g., description updated but a comment failed), report what succeeded and what failed
    - If the branch has changes from multiple tickets (e.g., cherry-picks), only propose updates for the ticket matching the branch name

---

## ADF Format Reference

JIRA does **not** render Markdown. Descriptions must use **Atlassian Document Format (ADF)** — a JSON-based document format. The `--description-file` flag treats file content as a plain text string, so it cannot be used for rich descriptions. Use `--from-json` instead.

**Important:** `--from-json` expects a structured JSON file with the full edit payload. The `description` field must be an ADF object, not a string. You can run `acli jira workitem edit --generate-json` to see the expected schema.

**Edit payload format (`--from-json`):**

```json
{
  "issues": ["<JIRA-ID>"],
  "description": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 2 },
        "content": [{ "type": "text", "text": "Description" }]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Regular text. " },
          { "type": "text", "text": "Bold text", "marks": [{ "type": "strong" }] }
        ]
      },
      {
        "type": "bulletList",
        "content": [
          {
            "type": "listItem",
            "content": [
              { "type": "paragraph", "content": [{ "type": "text", "text": "List item" }] }
            ]
          }
        ]
      },
      {
        "type": "orderedList",
        "content": [
          {
            "type": "listItem",
            "content": [
              { "type": "paragraph", "content": [{ "type": "text", "text": "Numbered item" }] }
            ]
          }
        ]
      },
      {
        "type": "taskList",
        "attrs": { "localId": "unique-id" },
        "content": [
          {
            "type": "taskItem",
            "attrs": { "localId": "task-1", "state": "TODO" },
            "content": [{ "type": "text", "text": "Acceptance criterion" }]
          }
        ]
      },
      {
        "type": "codeBlock",
        "attrs": { "language": "typescript" },
        "content": [{ "type": "text", "text": "const x = 1;" }]
      }
    ]
  }
}
```

**Common ADF node types:**

| Markdown | ADF `type` | Notes |
|----------|-----------|-------|
| `## Heading` | `heading` with `attrs.level` | Levels 1–6 |
| Plain text | `paragraph` with `text` children | |
| `**bold**` | `text` with `marks: [{"type": "strong"}]` | |
| `*italic*` | `text` with `marks: [{"type": "em"}]` | |
| `- item` | `bulletList` > `listItem` > `paragraph` | |
| `1. item` | `orderedList` > `listItem` > `paragraph` | |
| `- [ ] task` | `taskList` > `taskItem` (state: `TODO`/`DONE`) | |
| `` `code` `` | `text` with `marks: [{"type": "code"}]` | Inline code |
| Code block | `codeBlock` with `attrs.language` | |
| `---` | `rule` | Horizontal rule |
| `[link](url)` | `text` with `marks: [{"type": "link", "attrs": {"href": "url"}}]` | |
