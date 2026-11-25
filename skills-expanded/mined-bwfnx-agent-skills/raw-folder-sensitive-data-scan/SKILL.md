---
name: raw-folder-sensitive-data-scan
description: Weekly scan of the SBDC raw/ Google Drive folder for newly added client PII/tax/financial data (UMD Level 3/4), with a digest report for {{USER}}. Runs on Annie (OpenMausBot) through Composio.
---

> **Schedule:** Weekly scan
> **Needs:** Gmail, workspace files, Drive
> **Helper scripts (yours, not included):** learnings.py

You are running a recurring data-security scan for {{USER}} ({{YOUR_EMAIL}}), a UMD Small Business Development Center (SBDC) advisor. This is a fresh session with no memory of prior runs, so follow these self-contained instructions exactly. Runs as Annie (Wiki Librarian) in OpenMausBot; follow `openmausbot/souls/_common.md` first (git pull, handoff entry, commit as Claude-umd with `Bot: Annie`).

STEP 0 - CHECK LEARNINGS FIRST (do this before anything else). From the Playground root run:

  cd "{{WORKSPACE_ROOT}}"
  py {{WORKSPACE_ROOT}}/learnings.py list --full umd-data-classification-levels umd-level34-real-vs-template-test pdf-acroform-ocr-fallback drive-sharing-inherits-from-parent-folder drive-search-files-pagesize-token-limit drive-folder-ids delete-folder-human-in-the-loop-protocol composio-drive-sbdc-raw-scan-verified-h-drive-log-missing openmausbot-composio-default-account-is-fnx-name-the-alias
  py {{WORKSPACE_ROOT}}/learnings.py list --skill raw-folder-sensitive-data-scan

Never read `memory/learnings/_views/*.jsonl` whole. If any entry contradicts an instruction below (folder ID changed, tool slug renamed, new preference from {{USER}}), the learnings entry wins.

BACKGROUND: On 2026-07-10 a full audit found that real client PII/tax/financial data (completed 1040s and 1120-S returns, Social Security Numbers, EINs, bank account numbers, bank statements) had been mixed into the "raw/" Google Drive folder, which is supposed to hold only generic, non-client-specific advising resources. {{USER}} has since restricted raw/'s sharing to owner-only (verified 2026-09-14: `shared=false`, sole permission is owner {{YOUR_EMAIL}}). This scheduled task exists to catch new instances going forward.

TOOLS (Composio, shared installation-wide). Every Drive and Gmail call MUST pass `account: "SBDC"`; the installation default is the FNX account and an unnamed call reads the wrong Drive. Slugs verified 2026-09-14:
- `GOOGLEDRIVE_FIND_FILE` - list/search. Use `folder_id`, `orderBy: "modifiedTime desc"`, `pageSize` 25-40, `fields: "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,size)"`, and a `q` such as `trashed = false and modifiedTime > '<CUTOFF RFC3339>'`. `files=[]` is a real no-change result when the same folder lists fine without the date filter; if it is empty without the filter too, treat as a scoping failure and stop.
- `GOOGLEDRIVE_GET_FILE_METADATA` (`fileId`, `fields`) - confirm type/parents/shared.
- `GOOGLEDRIVE_LIST_PERMISSIONS` (`fileId`) - sharing exposure check.
- `GOOGLEDRIVE_DOWNLOAD_FILE` - non-native files (PDF, DOCX, XLSX, images). Returns a temporary `downloaded_file_content.s3url`, not bytes; `curl -sL -o <tmp>` it immediately, then inspect locally (pdftotext/py, OCR fallback per the pdf-acroform-ocr-fallback learning). Delete the local temp copy when done; never save client files into the Playground.
- `GOOGLEDOCS_GET_DOCUMENT_PLAINTEXT` - native Google Docs only (400 on anything else).
- `GOOGLEDRIVE_COPY_FILE_ADVANCED` (`fileId`, `parents: ["<delete-folder-id>"]`, `name`) - the ONLY write this task makes. There is no delete or move in scope for this task; "removing" a file always means copying it into {{USER}}'s delete/ folder and leaving the original in place.
- `GMAIL_CREATE_EMAIL_DRAFT` (`recipient_email`, `subject`, `body`) - draft only, never `GMAIL_SEND_EMAIL`.
Discover with `COMPOSIO_SEARCH_TOOLS`, read arguments with `COMPOSIO_GET_TOOL_SCHEMAS`, run with `COMPOSIO_MULTI_EXECUTE_TOOL`. If a slug has been renamed, re-search rather than guess.

KEY IDS (double check against the learnings store's drive-folder-ids entry):
- raw/ folder ID: 19Id8xNciNDo7QFSTOwq1BEjKl2TsiAsX
- {{USER}}'s standing "delete" holding folder (human-in-the-loop removal; copy confirmed-sensitive files here, never delete anything yourself): 1urZxcV70UIKvt8-FoG70_moCd5CxrlJN
- Persistent scan log (read this first to find the last scan date): `{{WORKSPACE_ROOT}}/sbdc-advising/outputs/raw_folder_security_scan_log.md` (git-tracked; the old `{{TEAM_DRIVE}}/...` path is gone, no H: drive is mounted on [hostname]). If it doesn't exist yet, treat this as the first run and use a lookback window of the last 8 days.

UMD DATA CLASSIFICATION (apply this test - also saved in learnings as umd-data-classification-levels and umd-level34-real-vs-template-test): Level 1 = public/generic templates, blank forms, guides - fine, ignore. Level 2 = moderate/internal, low harm - ignore unless clearly a live client financial record. Level 3 = SSNs, driver's license numbers, financial info tied to a real named individual. Level 4 = completed tax forms (1040/W-2/1099/1120-S/Schedule C), bank account/routing numbers, EIN+income data for a real entity. The test is REAL, FILLED-IN data about a real person/business - a blank template of the same form is NOT a concern. Don't flag based on filename alone; open candidate files and confirm actual sensitive content before flagging.

STEPS:
1. Read the scan log to get the last scan's cutoff date. If missing, use (today's date minus 8 days).
2. `GOOGLEDRIVE_FIND_FILE` (account SBDC) on raw/ with `q: "trashed = false and (createdTime > 'CUTOFF' or modifiedTime > 'CUTOFF')"`, pageSize 25-40, paginate with `pageToken` until `nextPageToken` is absent. This only checks the top level - also recurse into subfolders that were themselves newly created/modified, and spot-check subfolders you can't easily filter (anything resembling "[Business Name] SBA Loan", "Banks", "Tax Returns", or a folder named for a person that isn't a generic resource category).
3. For every candidate file, confirm real Level 3/4 content via actual content read (not filename guessing).
4. For every CONFIRMED Level 3/4 file: `GOOGLEDRIVE_COPY_FILE_ADVANCED` it into the delete/ folder (do not attempt to move or delete the original), and `GOOGLEDRIVE_LIST_PERMISSIONS` to note if it's shared beyond UMD ("anyone with the link" or a {{COLLEAGUE_EMAIL}} address).
5. Do NOT delete, move, or modify anything in raw/ itself - copy-to-delete-folder only, per {{USER}}'s standing delete-folder-human-in-the-loop-protocol. Never touch sharing/permissions settings (that requires {{USER}} to do himself).
6. Append a dated entry to the scan log (create it with a top-level heading `# raw/ folder security scan log` if it doesn't exist) recording: scan date, files reviewed count, files newly flagged (names/paths/why - no SSNs, account numbers, or other sensitive values in the log, it is git-tracked), sharing exposure, and the new cutoff date for next time (today's date in RFC3339). Commit the log with the run's handoff entry.
7. If you found ANY new Level 3/4 files, also create a Gmail draft (account SBDC, do not send) addressed to {{YOUR_EMAIL}} summarizing the findings, so {{USER}} sees it even if he misses the session notification.
8. End your final message with a clear, short digest: how many files were reviewed, how many newly flagged (with names + why + sharing exposure + confirmation they were copied into the delete/ folder for {{USER}} to review and clear), and confirmation that originals were left untouched in raw/. If nothing new was found, say so briefly - don't pad the report. Also note briefly whether Step 0's learnings check surfaced anything that changed how this run behaved.

LEARNINGS PASS: {{USER}} has authorized this automation to save non-sensitive durable learnings when confidence and usefulness are both 8 or higher - e.g. a new recurring tool quirk discovered during a run. `py {{WORKSPACE_ROOT}}/learnings.py list --grep <term>` first to avoid duplicates, then `py {{WORKSPACE_ROOT}}/learnings.py add --namespace sbdc --skill raw-folder-sensitive-data-scan --key <kebab> --insight "..."`. Do not save client names, SSNs, account numbers, or other sensitive specifics to the learnings store under any circumstances. For lower-confidence or lower-usefulness observations, just mention them in your final summary instead.
