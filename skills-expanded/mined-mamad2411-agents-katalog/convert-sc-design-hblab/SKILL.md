---
name: convert-sc-design-hblab
description: >
  Use when a Google Sheets URL (docs.google.com/spreadsheets/d/) or raw spreadsheet ID is present, or when
  the user says "read the sheet", "fetch spreadsheet", "convert sheet", "doc sheet", "import from Google Sheet",
  "get data from sheet", "đọc sheet", "doc sheet", "lay du lieu tu sheet", "lay data tu google sheet", or wants
  to export, document, or convert Google Sheet data into markdown, a table, a report, or documentation.
  Do NOT trigger for: Excel (.xlsx), CSV, Google Docs (docs.google.com/document), databases, or how-to questions about Google Sheets.
---

# convert-sc-design-hblab

Read a Google Sheet by `SPREADSHEET_ID` and turn the result into usable markdown.

## Requirements

- OAuth credentials at `~/.config/google-sheets/oauth-token.json` with:
  - `client_id`
  - `client_secret`
  - `refresh_token`
- Google Sheets API enabled for that OAuth app

## Output Policy

- Use the installed script from the skill directory, but write any authored markdown into `./docs` of the current workspace.
- If `./docs` does not exist, create it before writing files.
- Do not save generated documents into the installed skill directory.

## Usage

### Step 1: Resolve the installed script path

`SKILL_DIR` is the directory containing this skill — the directory from which this `SKILL.md` was loaded. It contains `scripts/read_sheet.py`. Each agent resolves this from its own skill registry; no hardcoded path is needed.

### Step 1.5: Extract the spreadsheet ID

If the user gave a URL like:
`https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0`

The spreadsheet ID is the segment between `/d/` and the next `/`:
`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

```bash
# Extract from URL (bash)
SPREADSHEET_ID=$(echo "$URL" | sed 's|.*/d/\([^/]*\).*|\1|')
```

If the user gave a raw alphanumeric ID with no slashes, use it directly.

### Step 2: Fetch sheet data

```bash
python3 "$SKILL_DIR/scripts/read_sheet.py" --spreadsheet-id "$SPREADSHEET_ID" --sheet-name <SHEET_NAME>
```

If the caller already has a Google Sheets tab id from the URL, they can target it directly:

```bash
python3 "$SKILL_DIR/scripts/read_sheet.py" --spreadsheet-id "$SPREADSHEET_ID" --gid <GID>
```

### Step 2.5: Discover the sheet name

If the user did not specify a sheet name, omit `--sheet-name` — the script reads the first sheet by default.
If the user provides both `--sheet-name` and `--gid`, `--gid` overrides `--sheet-name`.

To inspect headers and data shape before committing to a format, always run json first:

```bash
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "$SPREADSHEET_ID" \
  --format json
```

Ask the user whether they want to read additional sheets if the spreadsheet has multiple tabs.
Always preserve the full sheet content unless the user explicitly asks for summarization.

### Step 3: Classify data shape and format accordingly

After inspecting the JSON output, classify the data:

| Shape              | Signs                                     | Recommended approach                                      |
| ------------------ | ----------------------------------------- | --------------------------------------------------------- |
| Tabular            | Row 0 = headers, rows 1+ = records        | `--format table`, add heading + 1-sentence description    |
| Key-value / config | Two columns (key, value)                  | Don't use a table — render as `## Key` / value prose      |
| Pivot / cross-tab  | First col = label, remaining = categories | `--format table`, note pivot structure above table        |
| Free text / notes  | Irregular rows, no clear header           | `--format text`, render each row as a paragraph or bullet |

### Step 4: Write the markdown document

Structure:

```
# <Spreadsheet Title or User-Provided Name>

> Source: Google Sheet — <Sheet Name> (ID: <SPREADSHEET_ID>)

## <Section heading derived from content>

<Formatted content>
```

- Derive the title from context or ask the user.
- Always include the source line.
- Save to `./docs/<sheet-name-kebab-case>.md`. Create `./docs` first: `mkdir -p ./docs`

## Parameters

| Parameter          | Required | Description                                                                     |
| ------------------ | -------- | ------------------------------------------------------------------------------- |
| `--spreadsheet-id` | Yes      | The Google Spreadsheet ID                                                       |
| `--sheet-name`     | No       | Sheet name to read. Defaults to the first sheet.                                |
| `--gid`            | No       | Google Sheets tab id / `sheetId`. Overrides `--sheet-name` when both are set.   |
| `--credentials`    | No       | OAuth credentials path. Defaults to `~/.config/google-sheets/oauth-token.json`. |
| `--output`         | No       | Output file path. Defaults to stdout.                                           |
| `--format`         | No       | Output format: `json` (default), `table`, or `text`.                            |
| `--raw`            | No       | Keep empty columns instead of cleaning them.                                    |

## Example

```bash
# Fetch as JSON
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --gid "0"

# Fetch as markdown table
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --sheet-name "Sheet1" \
  --format table

# Save raw output directly into the current workspace docs folder
mkdir -p ./docs
python3 "$SKILL_DIR/scripts/read_sheet.py" \
  --spreadsheet-id "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" \
  --gid "0" \
  --format table \
  --output ./docs/sheet1.md
```

## OAuth Credentials Format

```json
{
  "type": "oauth",
  "client_id": "your-client-id.apps.googleusercontent.com",
  "client_secret": "your-client-secret",
  "refresh_token": "your-refresh-token"
}
```

## First-Run Setup

If credentials don't exist at `~/.config/google-sheets/oauth-token.json`:

1. Create a Google Cloud project, enable the **Google Sheets API**
2. Create an **OAuth 2.0 Desktop app** credential → download JSON
3. Get a refresh token via https://developers.google.com/oauthplayground/
   - Use scope: `https://www.googleapis.com/auth/spreadsheets.readonly`
4. Create the credentials file:
   ```bash
   mkdir -p ~/.config/google-sheets
   # Write the JSON with client_id, client_secret, refresh_token
   ```

For detailed steps, see `docs/troubleshooting.md` in the source repo.
