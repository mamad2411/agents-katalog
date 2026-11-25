---
name: tool-showcase-submit
description: Submit a tool or project to the FE Tool Showcase Google Sheet. Use when the user wants to register, submit, or add a tool/project/demo to the FE showcase spreadsheet. Researches across Glean, JIRA, Slack, and Obsidian vault notes to gather details and fills the required fields.
---

# Tool Showcase Submission

Research and submit FE tools/projects to the [FE Tool Showcase Google Sheet](https://docs.google.com/spreadsheets/d/1KXrOftLakQ6itztbgxNzowhH2mLOyGxFhYWk1HbGBw8/edit?gid=1509921540).

## Capabilities

- Research a tool/project across Glean, JIRA, Slack, and Obsidian vault
- Auto-populate all required fields for the showcase sheet
- Preview the submission for user review before appending
- Append the finalized row to the Google Sheet

## Required Fields

The showcase sheet has these columns (in order):

| # | Column | Description |
|---|--------|-------------|
| 1 | Timestamp | Auto-filled (current date/time) |
| 2 | Email Address | Submitter's email |
| 3 | Region | Submitter's region (e.g., AMER, EMEA, SEMEA, APJ) |
| 4 | Tool Name | Name of the tool/demo |
| 5 | Elevator Pitch | Short description of what the tool does |
| 6 | Powered By | Technologies used (e.g., Databricks, LLMs, Unity Catalog, MLflow) |
| 7 | Persona(s) | Who should use this tool? |
| 8 | Goal | Why use this tool? What problem does it solve? |
| 9 | Metrics | Quantifiable success if available (adoption, productivity gains, time saved) |
| 10 | FE-IP? | Is this tracked as FE IP? Link to FEIP JIRA ticket if yes, or "No" |
| 11 | Contributors | Names of contributors |
| 12 | Link | Link to the tool or documentation |

## Workflow

### Phase 1: Identify the Tool/Project

1. Ask the user which tool or project to submit (or accept from arguments)
2. If the user has Obsidian vault notes, search for relevant notes about the tool:
   - Use the Obsidian MCP tools (`mcp__obsidian__search_notes`) to find notes mentioning the tool name
   - Read matching notes for details

### Phase 2: Research Across Sources

Run research in parallel across multiple sources:

1. **Obsidian Vault**: Search notes in the current vault for any mentions of the tool
   - Use `mcp__obsidian__search_notes` with the tool name
   - Read any matching notes for elevator pitch, tech stack, goals

2. **Glean**: Search internal knowledge base
   - Use the `fe-internal-tools:glean-search` skill or Glean MCP tools
   - Search for the tool name to find documentation, announcements, wiki pages

3. **JIRA**: Search for related tickets
   - Use JIRA MCP tools to search for the tool name
   - Look for FEIP tickets specifically (FE-IP tracking)
   - Extract contributor names, status, goals

4. **Slack**: Search relevant channels
   - Use Slack MCP tools to search messages about the tool
   - Look in channels like #field-engineering, #fe-tools, #fe-ip

### Phase 3: Compile and Preview

1. Merge findings from all sources into the 12 required fields
2. For any field that couldn't be filled, mark as "NEEDS INPUT" 
3. Present a formatted preview table to the user:

```
| Field          | Value                    |
|----------------|--------------------------|
| Timestamp      | [auto]                   |
| Email          | [user's email]           |
| Region         | [from profile or ask]    |
| Tool Name      | [discovered]             |
| Elevator Pitch | [from research]          |
| Powered By     | [from research]          |
| Persona(s)     | [from research]          |
| Goal           | [from research]          |
| Metrics        | [from research or "N/A"] |
| FE-IP?         | [JIRA link or "No"]      |
| Contributors   | [from research]          |
| Link           | [from research]          |
```

4. Ask the user to confirm or edit any fields

### Phase 4: Submit to Google Sheet

1. Ensure Google auth is valid:
   ```bash
   python3 <google-auth-skill-path>/resources/google_auth.py status
   ```

2. Append the row using the Google Sheets API:
   ```bash
   TOKEN=$(python3 <google-auth-skill-path>/resources/google_auth.py token)
   curl -s -X POST \
     "https://sheets.googleapis.com/v4/spreadsheets/1KXrOftLakQ6itztbgxNzowhH2mLOyGxFhYWk1HbGBw8/values/Form%20Responses%201:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng" \
     -H "Content-Type: application/json" \
     -d '{"values":[["<timestamp>","<email>","<region>","<tool_name>","<pitch>","<powered_by>","<personas>","<goal>","<metrics>","<feip>","<contributors>","<link>"]]}'
   ```

3. Confirm success and provide link to the sheet

## Google Auth

This skill requires Google Sheets API access. Before submitting:

1. Run the google-auth skill to check/establish authentication
2. The auth script is at: `fe-google-tools/google-auth/resources/google_auth.py`
3. Required scope: `https://www.googleapis.com/auth/spreadsheets`
4. Quota project: `gcp-sandbox-field-eng`

## Sheet Details

- **Spreadsheet ID**: `1KXrOftLakQ6itztbgxNzowhH2mLOyGxFhYWk1HbGBw8`
- **Sheet name**: `Form Responses 1`
- **Sheet GID**: `1509921540`

## Examples

### Example: Submit a known project
User says: "Submit my FinanceDIP demo to the tool showcase"
1. Searches Obsidian vault for "FinanceDIP" notes
2. Searches Glean for internal docs about FinanceDIP
3. Searches JIRA for FEIP tickets related to FinanceDIP
4. Compiles findings into the 12 fields
5. Presents preview for user review
6. Appends to Google Sheet on confirmation

### Example: Submit from vault notes
User says: "I have notes about my new Lakebase demo, add it to the showcase sheet"
1. Searches Obsidian vault for "Lakebase demo" notes
2. Extracts tool name, tech stack, description from notes
3. Supplements with Glean/JIRA/Slack research
4. Presents preview and submits on approval

### Example: Quick submit with details provided
User says: "Add InspireAI to the showcase - it generates AI use cases for business leaders"
1. Uses provided details as starting point
2. Enriches with research from Glean, JIRA, Slack
3. Presents preview and submits on approval
