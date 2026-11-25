---
name: jira-fetch-ticket
description: Fetch a Jira ticket and create a structured analysis document. Use when starting work on a ticket or when you need full context on a Jira issue.
compatibility: Requires Python 3.8+ and network access to your Jira instance. git is optional (used to infer project key from branch name when only a ticket number is provided).
args:
  - name: ticket
    description: "Jira ticket ID (e.g. PROJ-189 or just 189)"
    required: true
---

# Jira Fetch Ticket

Fetch a Jira ticket and produce a structured analysis document in `docs/jira-tickets/`.

## Instructions

### Step 1: Parse Ticket ID

Normalize the `{{ticket}}` argument:
- If it already has a project prefix (e.g. `PROJ-189`), use as-is
- If it's just a number (e.g. `189`), the fetch script will infer the project key from the current git branch
- Store the result as `TICKET_KEY` for use in later steps

### Step 2: Fetch Ticket

Run the fetch command:

```bash
python3 fetch_ticket.py {{ticket}}
```

If the script fails due to missing environment variables, help the user set them up:
1. Ask how they'd like to provide the variables — via `.env` files, their agent's config, or shell environment.
2. If using `.env` files:
   - Check if `.env` exists in the project root — if not, create it and ask the user for their Jira instance URL:
     ```
     JIRA_BASE_URL=https://yourcompany.atlassian.net
     ```
   - Check if `.env.local` exists — if not, create it and ask the user for their email and API token (direct them to https://id.atlassian.com/manage-profile/security/api-tokens to generate one):
     ```
     JIRA_EMAIL=you@yourcompany.com
     JIRA_API_TOKEN=your-api-token
     ```
   - Remind the user to add `.env.local` to `.gitignore` if not already present.
3. Re-run the script once configured.

If the script fails for any other reason, report the error and stop.

After the script runs, read the raw JSON from `docs/jira-tickets/${TICKET_KEY}/raw.json` for the full ticket data.

### Step 3: Check for Parent Epic Context

If the ticket has a `parent` field:
1. Extract the parent key (e.g. `PROJ-175`)
2. Look for `docs/jira-tickets/${PARENT_KEY}/${PARENT_KEY}.md` using Glob
3. If found, read it for additional context about the epic's goals and scope
4. If not found, ask the user if they'd like to fetch the parent epic — if yes, run `python3 fetch_ticket.py ${PARENT_KEY}` and read the resulting document

### Step 4: Check for Linked Issue Context

If the ticket has entries in `issuelinks`:
1. Extract the key of each linked issue
2. For each, look for `docs/jira-tickets/${LINKED_KEY}/${LINKED_KEY}.md` using Glob
3. If found, read it for additional context — note the link type (e.g. "blocks", "is blocked by", "relates to") when using the context
4. If any are not found, list them and ask the user if they'd like to fetch them — if yes, run `python3 fetch_ticket.py ${LINKED_KEY}` for each confirmed and read the resulting documents

### Step 5: Analyze the Ticket

Using the fetched data, any epic context, and any linked issue context:

1. **Classify the work type**: new feature, bug fix, enhancement, refactor, tech debt, etc.
2. **Extract acceptance criteria**: look for patterns like "AC:", "Acceptance Criteria", or checklists in the description
3. **Identify keywords**: extract endpoint names, component names, file references, model names, etc.
4. **Scan the codebase**: use Grep/Glob to find files relevant to the keywords. Focus on:
   - Backend: controllers, services, models, routes mentioned
   - Frontend: pages, components, types mentioned
   - Existing related code that will need modification
5. **Note gaps**: identify missing information, ambiguities, or questions that should be clarified

### Step 6: Create the Ticket Document

Write `docs/jira-tickets/${TICKET_KEY}/${TICKET_KEY}.md` with this structure:

```markdown
# ${TICKET_KEY}: {Summary}

## Jira
- **Type**: {issuetype.name}
- **Status**: {status.name}
- **Priority**: {priority.name}
- **Assignee**: {assignee.displayName or "Unassigned"}
- **Environment**: {environment or "None"}
- **Parent Epic**: {parent.key}: {parent summary} (or "None")
- **Labels**: {labels joined, or "None"}
- **Created**: {created date, YYYY-MM-DD}
- **URL**: {JIRA_BASE_URL}/browse/${TICKET_KEY}

## Description

{Jira description converted from wiki markup to markdown:
 - Convert wiki headings (h1. h2.) to markdown (# ##)
 - Convert wiki links [text|url] to [text](url)
 - Convert {code} blocks to fenced code blocks
 - Strip image macros !image.png|opts! to [image: image.png]
 - Preserve lists, bold, italic}

## Acceptance Criteria

{Extracted from description if present, otherwise "Not specified in Jira — clarify with the team."}

## Linked Issues

{For each link: "- {linkType}: {key} — {summary}" or "None"}

## Subtasks

{For each subtask: "- {key}: {summary} ({status})" or "None"}

## Comments

{For each comment: author, date, body. Or "No comments."}

## Analysis

{Your analysis:
 - What is being asked for (in your own words)
 - Type of work (feature, bug, refactor, etc.)
 - High-level approach considerations
 - Dependencies or blockers you can identify
 - Missing information or ambiguities to clarify before starting}

## Code References

{Files relevant to this ticket, from codebase scanning:
 - Each file with a brief note on why it's relevant
 - Group by backend/frontend if applicable
 - Note existing patterns to follow
 - Limit to ~10-15 most relevant files}
```

### Step 7: Report

1. Confirm the file was created at `docs/jira-tickets/${TICKET_KEY}/${TICKET_KEY}.md`
2. Show a brief summary: ticket title, type, status, and top-level analysis
3. Highlight any **ambiguities or missing info** to clarify before starting work
4. Mention subtasks or linked issues as potential scope considerations

## Rules

- NEVER commit the ticket document — it's a local working file
- NEVER start implementing the ticket — this skill is for analysis only
- Keep the Analysis section concise but actionable
- Limit codebase scan results to the most relevant files (~10-15 max)
