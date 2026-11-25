---
name: jira
description: Use this skill for Jira work items with Atlassian CLI (`acli`). Trigger it whenever the user mentions Jira, JQL, issue or ticket keys like `ABC-123`, assignees, status changes, comments, rich-text Jira descriptions, or Markdown that needs to become Jira ADF. Resolve the project from an explicit issue key or project key first, then `.jira-skill.json` (searching up to repo root), then `~/.config/jira-skill/config.json`, then STOP and ask the user — never auto-select. Do not use it for GitHub PR edits, repo/codebase searches (even if "jira" appears as a package or library name), git branch naming, Confluence, auth setup, REST API scripting, or non-Jira trackers.
compatibility: Requires `acli` and `mdadf` CLI. Uses `zsh` or `bash` process substitution for piping ADF into acli flags. On Windows PowerShell, uses temp files instead.
---

# Jira Work Item Management

Uses Atlassian CLI (`acli`) to view, search, filter, create, and update work items in Jira projects.

## Prerequisites

Check that both dependencies are available before running any commands. Do this once at the start of the session, not before every command.

1. **acli** — run `acli --version`. If missing, read [references/prerequisites.md](references/prerequisites.md) for install instructions.
2. **mdadf** — run `mdadf --version`. If missing, read [references/prerequisites.md](references/prerequisites.md) for install instructions.

If either tool is missing and cannot be installed (e.g. no network access), tell the user exactly what commands to run and stop.

## Operating Constraints

- **READ-ONLY for Projects**: Never modify Jira projects themselves. Only create, update, or delete work items within projects.
- **Mutation Intent**: For create, edit, transition, assign, comment, or delete operations, only mutate Jira when the user explicitly asks for that change. If the request is ambiguous, clarify before mutating.
- **Key-First Targeting**: If the user provides a work item key such as `MYPROJECT-1455`, use it directly rather than writing JQL. The exact CLI syntax varies per subcommand (`view` uses a positional argument; `edit`, `transition`, `assign`, and `comment` use a `--key` flag) — see [references/commands.md](references/commands.md).
- **JQL**: Use `--jql` for selecting, searching, or filtering work items when applicable.
- **Configured Default Project**: If the user does not specify a project, resolve via the Project Resolution chain below (workspace `.jira-skill.json` → user-global `~/.config/jira-skill/config.json` → ask user).
- **Work Item Types**: `Bug`, `Task`, `Story`, `Epic`
- **Rich Text**: Draft Jira descriptions and comment bodies in Markdown first, then convert to ADF with `mdadf --compact` before calling `acli`:

  ```bash
  acli jira workitem create \
    --summary "Fix the login page" \
    --project "MYPROJECT" \
    --type "Bug" \
    --description-file <(mdadf --compact <<'MD'
  **Short Description**
  The login page returns a 500 on empty email.
  MD
  )
  ```

  For Windows PowerShell or other platform-specific patterns, read [references/mdadf-usage.md](references/mdadf-usage.md).

## Project Resolution

Resolve the project key on every request — do not cache it across requests, because the user may switch repos.

1. If the user gives a Jira issue key such as `MYPROJECT-1455`, use its prefix as the project key.
2. If the user explicitly names a project key such as `MYPROJECT`, use that.
3. Otherwise, search for `.jira-skill.json` starting from the current working directory and walking up parent directories until the repo root (the directory containing `.git`) is reached. If found and it has a valid `defaultProject`, use it.
4. Otherwise, read `~/.config/jira-skill/config.json`. This is the user-global fallback, shared across all repos.
5. If no config is found, you MUST stop and ask the user two things before proceeding:
   - **Which project?** List the available projects (via `acli jira project list --recent`) and ask the user to confirm. Do NOT guess or auto-select a project, even if only one project is returned.
   - **Where to save?** Ask whether to save the default as a **global** config (`~/.config/jira-skill/config.json`, shared across all repos) or a **project-level** config (`.jira-skill.json` in the repo root). Default recommendation is **global**, since most users work on one project at a time. Only write the config after the user answers both questions. If the user just confirms the project without specifying a storage location, use global.

`.jira-skill.json` is workspace-local — different repos get different defaults. Add it to `.gitignore` if it should not be shared. `~/.config/jira-skill/config.json` is user-global and survives skill updates.

Config schema:

```json
{
  "defaultProject": "YOUR_PROJECT_KEY"
}
```

## Safety Rules

These rules prevent common Jira mishaps. Follow them without exception.

1. **NEVER transition without fetching current status first.** Jira workflows may require intermediate states (e.g. To Do → In Progress → In Review → Done). Skipping a step fails silently or throws a confusing error. Always run `acli jira workitem view <KEY> --fields "status"` before any transition.

2. **NEVER bulk-modify without explicit user approval.** Each edit notifies watchers. Editing 10 tickets means 10 notification storms. Always confirm with the user before operating on multiple work items.

3. **NEVER edit a description without showing the original.** Jira has no undo. Before replacing a description, display the current content so the user can verify nothing is lost.

4. **NEVER assume transition names are universal.** "Done", "Closed", "Complete", "Resolved" vary by project and workflow scheme. When in doubt, check the current status with `acli jira workitem view <KEY> --fields "status"` and ask the user which target status to use.

5. **NEVER set Priority, Technical Impact, or Business Urgency on new tickets.** These fields are for triage by leads or product. Creating a "Critical" ticket without authorization undermines the triage process. If the user explicitly requests a priority level, acknowledge it and explain that priority is typically set during triage.

## Execution Steps

1. If the request is mutating, review the Safety Rules above. Identify which rules apply before running any command.
2. Resolve the project key using the project resolution rules above.
3. If the request targets a specific work item key, use it directly rather than JQL. Consult [references/commands.md](references/commands.md) for whether the subcommand takes the key as a positional argument or a `--key` flag. Use JQL only when searching or targeting multiple work items.
4. If the request needs rich text, write the content in Markdown and convert it to ADF with `mdadf --compact` before running `acli`. Read [references/mdadf-usage.md](references/mdadf-usage.md) if you need platform-specific syntax.
5. If creating or rewriting a work item, follow the drafting format in [references/ticket-drafting.md](references/ticket-drafting.md).
6. Run the appropriate `acli` command. Read [references/commands.md](references/commands.md) for the full flag reference.
7. Read and analyze the output. If errors occur, run `acli --help` or the relevant subcommand help for guidance.

## Output Format

- **Always include the direct Jira URL** after any create, edit, transition, comment, or assign operation. Parse the URL from the `acli` output (e.g. `✓ Work item MYPROJECT-100 created: https://…/browse/MYPROJECT-100`) and present it as a clickable link. Never report just the issue key without its URL.
- When reporting search results or findings, use table format with links to the work items.
