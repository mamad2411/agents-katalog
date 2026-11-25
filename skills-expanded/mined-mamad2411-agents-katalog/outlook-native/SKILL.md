---
name: outlook-native
description: Query, search, and extract Outlook email content, compose rich HTML Outlook drafts with inline images, and organize a mailbox with folders and server-side rules. Use this skill whenever the user wants to search their Outlook mailbox, extract or export emails (查邮件/提取邮件/导出邮件), parse .ost or .pst files, summarize email threads, draft/backfill an Outlook email (回填邮件/生成草稿/写邮件到Outlook), or tidy up their inbox (整理邮箱/建文件夹/建规则/归档邮件). Trigger even if the user only mentions "my Outlook", "mailbox", an .ost/.pst file path, or pasting HTML into an email that broke its formatting.
---

# Outlook Mail: Query, Compose & Organize

Three capabilities, each with environment-appropriate backends:

1. **Query** — search/extract email content (subject, body, sender, recipients, dates, attachments)
2. **Compose** — create an Outlook draft with Word-engine-safe HTML and inline images (never auto-send)
3. **Organize** — create Inbox subfolders + server-side rules, and file the existing backlog

## Step 0: Route by environment

Detect first — do not assume:

```powershell
powershell -Command "(New-Object -ComObject Outlook.Application).Name"   # succeeds => live COM
```
On a Linux/macOS shell, skip the probe and go straight to the offline path.

| Environment | Query | Compose | Organize |
|---|---|---|---|
| **Windows PC, classic Outlook installed** (Claude Code, Codex, any local agent) | `scripts/query_com.ps1` — live, fast, complete | `scripts/create_draft.ps1` — draft opens in Outlook | `scripts/organize_mailbox.ps1` |
| **Linux/macOS sandbox** (Cowork, remote) — no Outlook process | `scripts/query_ost.py` against a mounted .ost/.pst | emit HTML + images + `create_draft.ps1` to a user-visible folder; user right-clicks → "Run with PowerShell" | **not possible** — OST parsing is read-only; hand the user the config + script to run locally |
| **New Outlook only, no classic** | no OST exists to parse — ask the user to install/enable classic Outlook, or drive OWA | paste-via-Word (references/outlook-html.md) | user does it in the New Outlook UI |

PowerShell here is Windows PowerShell 5.1, not 7 — see the BOM and stream-pollution traps in
references/troubleshooting.md before writing any .ps1 with non-ASCII in it.

### Finding the data files — never hardcode the path

`%LOCALAPPDATA%\Microsoft\Outlook\*.ost` is only the *default*. Enterprises routinely relocate the
whole store with group policy — e.g. onto a `D:\` data drive.
Resolve it in this order:

```powershell
# 1. Authoritative, when Outlook is reachable: ask it.
$ns.Stores | ForEach-Object { "{0} | type={1} | {2}" -f $_.DisplayName, [int]$_.ExchangeStoreType, $_.FilePath }
#    ExchangeStoreType 0 = Exchange mailbox (syncs to cloud); 2 = local .pst (never syncs)

# 2. Offline / Outlook not running: the relocation policy.
Get-ItemProperty "HKCU:\Software\Policies\Microsoft\Office\16.0\Outlook" |
  Select-Object forceostpath, forcepstpath          # e.g. forceostpath = D:\OutlookData

# 3. Which profile is active.
(Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Office\16.0\Outlook").DefaultProfile

# 4. Last resort: search both the default location and any policy path.
Get-ChildItem "$env:LOCALAPPDATA\Microsoft\Outlook\*.ost", "<policyPath>\*.ost" -ErrorAction SilentlyContinue
```

Reference paths:

| What | Where |
|---|---|
| Classic OST (default) | `%LOCALAPPDATA%\Microsoft\Outlook\*.ost` |
| Classic OST (relocated) | whatever `forceostpath` says |
| Archive PST | `%USERPROFILE%\Documents\Outlook Files\*.pst`, or `forcepstpath` |
| **New Outlook cache** | `%LOCALAPPDATA%\Microsoft\Olk\` — WebView2 IndexedDB, **not** an OST, do not parse |
| Outlook profiles | `HKCU:\SOFTWARE\Microsoft\Office\16.0\Outlook\Profiles\<profile>` |

In a sandbox, tell the user the resolved path to mount rather than guessing — and note the OST is
locked while Outlook runs, so they must close Outlook or copy the file.

### New Outlook (Monarch) — what it actually is

New Outlook is **an Edge WebView2 wrapper around outlook.office.com**, not a mail client with a local store. Verified layout:

```
%LOCALAPPDATA%\Microsoft\Olk\                              process: olk.exe
└─ EBWebView\Default\IndexedDB\
   ├─ https_outlook.office.com_0.indexeddb.leveldb   mail metadata (Chromium LevelDB)
   └─ https_outlook.office.com_0.indexeddb.blob      images only — NO mail bodies
```

Consequences, in priority order:

- **There is no OST/PST.** `libpff`/`pypff` is inapplicable — it parses PST/OST only.
- **Do not try to parse the IndexedDB.** It is a dead end: locked and live-compacting under `olk.exe`, ~1% of the mailbox (a rolling window), and it requires stacking LevelDB + Chromium IndexedDB key encoding + Blink structured-clone + Microsoft's undocumented OWA schema. Any parser built today breaks on the next update.
- **The authoritative mailbox is Exchange Online.** Both the OST and the Olk cache are just caches.
- **Therefore: prefer classic Outlook COM even when the user lives in New Outlook.** Folders and rules are server-side (see Workflow C), so changes made through classic COM appear in New Outlook automatically. Classic and New can both be installed; check with `Get-Process olk, OUTLOOK`.

If classic Outlook is not installed at all: query via OST parsing is impossible (no OST exists), so fall back to asking the user to export, or drive the OWA UI. For compose, deliver the HTML with paste-via-Word instructions (references/outlook-html.md).

**Classic Outlook present but its data looks stale?** A classic profile only syncs while it is actually running with a signed-in session. A profile untouched for weeks reports `Offline=False` yet returns no recent mail, and a COM-launched headless instance is often too short-lived to finish an incremental resync. Check `$ns.ExchangeConnectionMode` — see the enum table in references/troubleshooting.md, and note **400 means disconnected, not connected**. Fix: have the user open Outlook normally and leave it running until the status bar reads "Connected"; a multi-week backfill can take an hour.

## Workflow A: Query emails

### Live (COM)

```powershell
# keyword search across Inbox + Sent, last 90 days, export CSV
powershell -ExecutionPolicy Bypass -File scripts/query_com.ps1 `
  -Keyword "hackathon" -Since "2026-01-01" -Folders Inbox,SentMail `
  -OutCsv results.csv -IncludeBody
```

Run `scripts/query_com.ps1 -?` style inspection (read the param block) for all options. Output CSV is UTF-8 BOM so Excel opens Chinese/Unicode correctly.

### Offline (.ost / .pst)

```bash
pip install libpff-python --break-system-packages   # module imports as pypff
python3 scripts/query_ost.py \
  --files "/path/to/mailbox.ost" \
  --keyword "hackathon|黑客松" \
  --out ./mail_out --budget 30
```

Important behaviors baked into the script (read them, don't re-derive):

- **Checkpoint/resume**: large OSTs (multi-GB) can't be scanned inside one shell-call timeout, and background processes do not survive between calls in sandboxes. The script scans for `--budget` seconds then exits with state saved; simply re-run the identical command until it prints `ALL_DONE`.
- **Sent-items recipient backfill**: sent/draft messages in OST files usually have no transport headers, so To/Cc looks empty. The script reads MAPI properties PR_DISPLAY_TO (0x0E04) / PR_DISPLAY_CC (0x0E03) from the message record set to recover display-name recipients. Without this, any "emails I sent to X" filter silently loses most results.
- Output: `matches.jsonl` (full bodies for later use) + `summary.csv` (UTF-8 BOM, Excel-ready preview).

If the OST is locked by a running Outlook, ask the user to close Outlook or copy the file first.

### Query hygiene (both backends)

- Deduplicate: the same message often exists in multiple folders (Inbox copy + Sent copy + Deleted). Key on (date, sender, subject, folder) when listing; on (date, subject) when the user wants unique conversations.
- Offer to filter automated senders (Microsoft Forms, GitLab, SharePoint, no-reply/noreply, Teams/Yammer notifications) — they typically dominate keyword matches and users almost always want them separated out.
- HTML bodies: strip `<style>/<script>` then tags for previews; keep the raw body in JSONL because the user often wants full content later.

## Workflow B: Compose / backfill a draft

1. Write the email body following **references/outlook-html.md** — Outlook desktop renders with the Word engine, so browser-grade CSS silently breaks. That reference contains the safe-markup rules plus copy-paste snippets (stat cards, ranking tables, image grids, section headers) that survive Word rendering.
2. Put referenced images next to the HTML (e.g. `images/*.png`) using plain relative `src="images/name.png"`.
3. Create the draft with `scripts/create_draft.ps1`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create_draft.ps1 `
  -Html final.html -Subject "My Subject" -To "a@x.com" -Cc "b@x.com"
```

The script attaches every locally-referenced image as a hidden inline attachment, sets its Content-ID, rewrites `src` to `cid:`, sets `HTMLBody`, and calls `.Display()` — so the user reviews and sends manually. Never modify it to send automatically: drafts are the safety boundary of this skill.

If you cannot execute PowerShell (sandbox), place `create_draft.ps1` + HTML + images together in a folder the user can see and tell them: right-click the .ps1 → "使用 PowerShell 运行" / "Run with PowerShell". Warn that classic desktop Outlook is required.

## Workflow C: Organize a mailbox (folders + rules + backlog)

Use `scripts/organize_mailbox.ps1` with a JSON config. Read **references/mailbox-organize.md** first — it covers the server-side model, the client-only-rule trap, and the COM landmines that make rule creation fail with a useless error message.

```powershell
# 1. always dry-run first
powershell -ExecutionPolicy Bypass -File scripts/organize_mailbox.ps1 -Config plan.json -Mode Plan -DoFolders -DoRules -DoBacklog
# 2. folders must exist before rules/backlog can reference them
powershell -ExecutionPolicy Bypass -File scripts/organize_mailbox.ps1 -Config plan.json -Mode Apply -DoFolders
powershell -ExecutionPolicy Bypass -File scripts/organize_mailbox.ps1 -Config plan.json -Mode Apply -DoRules
powershell -ExecutionPolicy Bypass -File scripts/organize_mailbox.ps1 -Config plan.json -Mode Apply -DoBacklog
```

Method that works well:

1. **Profile before designing.** Dump every inbox message's sender + unread flag to CSV, then group by sender. The folder scheme should follow the actual volume distribution, not a generic GTD template. In real mailboxes ~40–60% of the inbox is broadcast/notification noise from <40 distinct senders.
2. **Design folders from that profile**, numbered (`01_`, `10_`, `30_`…) so ordering is stable.
3. **Rules match on sender ADDRESS, never display name.** Display names must resolve in the GAL; system senders (`itnoreply`, `SharePoint Online`, `Workday`…) usually do not, and an unresolved recipient makes the rule silently never match. Get real addresses first via `$msg.Sender.GetExchangeUser().PrimarySmtpAddress`. An alias fragment (`opsalerts`) matches both the SMTP form and the X500 form.
4. **Rule actions: move only.** Anything else demotes the rule to client-only.
5. **File the backlog with explicit per-sender queries, not "Run Rules Now"** — every move is then counted and reportable, and New Outlook has no global Run Rules Now anyway.
6. **Move, never delete.** Everything stays reversible.

Report volumes per folder before applying so the user can sanity-check the split.

## Common failure modes

Read **references/troubleshooting.md** when you hit: COM errors, rules that refuse to save, locked OST files, garbled encodings, emoji in PowerShell strings, pypff install failures, stale classic profiles, or pasted-HTML formatting loss. It documents fixes verified in real sessions.
