# Progressive Memory Helper

Helper tool for managing Progressive Memory files (index + detail blocks).

## Usage

Use this tool to add new entries to the daily memory file without worrying about markdown formatting or ID conflicts.

### Command

```bash
node skills/progressive-memory-helper/index.js add --type <TYPE> --summary "<SUMMARY>" --details "<DETAILS>"
```

### Parameters

- `type`: The type of memory entry. Choose from:
  - `rule` (🚨): Critical rules.
  - `gotcha` (🔴): Mistakes to avoid.
  - `fix` (🟡): Fixes/Workarounds.
  - `how` (🔵): How-to/Explanations.
  - `change` (🟢): Changes made.
  - `discovery` (🟣): Insights/Learnings.
  - `decision` (🟤): Decisions made.
- `summary`: Short summary for the index table (max 10 words).
- `details`: Full text of the memory entry.

### Example

```bash
node skills/progressive-memory-helper/index.js add \
  --type decision \
  --summary "Switched to Progressive Memory" \
  --details "Decided to use progressive memory format to save tokens. Created helper script."
```

## Benefits

- **Auto-Formatting**: Automatically updates the index table and appends details.
- **ID Management**: Auto-increments IDs (e.g., #1, #2).
- **Token Estimation**: Automatically calculates token counts for the index.
- **File Init**: Creates the daily file if it doesn't exist.
