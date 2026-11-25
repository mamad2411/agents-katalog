---
name: miui-mobile-forensics
description: Use when solving Android or MIUI phone forensic CTF tasks, especially Xiaomi MIUI backup zip or .bak evidence, app databases, SharedPreferences, MMKV, browser history, wallet apps, social apps, alarm, smart-home, AI chat, or recording artifacts. Helps extract selected app data safely, triage SQLite/XML/JSON/MMKV/LevelDB files, preserve evidence paths, and write Chinese WP answers.
---

# MIUI Mobile Forensics

## Purpose

Use this skill to solve phone-forensics questions from a MIUI/Xiaomi Android backup or extracted Android app data. The goal is to move fast without guessing: identify the app package, extract only lightweight artifacts, query structured stores first, and produce answers with file/table/key evidence.

## Initial Triage

1. Identify the evidence container:
   - MIUI backup zip: list entries first, then locate `MIUI/backup/AllBackup/<yyyyMMdd_HHmmss>/`.
   - Android backup `.bak`: inspect header before extraction.
   - Already extracted app data: start from `apps/<package>/db`, `shared_prefs`, `sp`, `f`, `files`, `databases`, `no_backup`.
2. Preserve the original evidence. Work in `_work/` or another scratch directory. Do not overwrite or recursively extract large backups unless needed.
3. If there is a document or note near the evidence, inspect it for passwords. MIUI zips in CTF tasks often use a password hidden in a `.docx`, `.txt`, chat, or case note.
4. Record evidence as you go:
   - container path
   - app package
   - artifact file
   - table/key/field
   - decoded timestamp and timezone

## MIUI Backup Workflow

For a password-protected MIUI zip:

```bash
python C:/Users/27516/.agents/skills/miui-mobile-forensics/scripts/extract_miui_backup.py MIUI.zip --password Qwer0714 --out _work/app_extracts --include im.token.app cn.soulapp.android com.mmbox.xbrowser.pro
```

If the backup is large, always filter by app package or display name. Avoid full extraction unless the user explicitly needs it and disk space is known to be sufficient.

The backup timestamp is usually encoded in the directory name:

```text
MIUI/MIUI/backup/AllBackup/20250801_104823/
```

Interpret this as `2025-08-01 10:48:23` unless other metadata proves a different timezone or clock setting.

## Artifact Priority

Search in this order:

1. SQLite databases: `db`, `databases`, named files without extension that start with `SQLite format 3`.
2. SharedPreferences/XML: `shared_prefs`, `sp`, `*.xml`.
3. JSON/local storage: `*.json`, React Native `RKStorage`, `AsyncStorage`, `LocalStorage`.
4. MMKV: `*.mmkv` and adjacent `.crc` files. Use strings first; decode only if needed.
5. LevelDB/RocksDB: `CURRENT`, `MANIFEST-*`, `*.ldb`, `*.sst`, `LOG`.
6. Media metadata: app databases first, then EXIF/file mtime only as corroboration.

Use `rg` for broad text search, but prefer structured queries once the right DB is found.

## Common Queries

List SQLite tables:

```bash
sqlite3 artifact.db ".tables"
sqlite3 artifact.db "SELECT name, sql FROM sqlite_master WHERE type='table';"
```

Find likely text columns:

```bash
sqlite3 artifact.db "PRAGMA table_info(table_name);"
sqlite3 artifact.db "SELECT * FROM table_name LIMIT 5;"
```

Search extracted artifacts:

```bash
rg -a -n "wallet|imToken|download|search|group|alarm|room|model|nickname|三唑仑|快递" _work/app_extracts
```

Scan SQLite and small text artifacts:

```bash
python C:/Users/27516/.agents/skills/miui-mobile-forensics/scripts/scan_android_artifacts.py _work/app_extracts --pattern "三唑仑|快递|imToken|room|nickname"
```

## App Cookbook

### Browser

Look for:
 - history tables: `history`, `urls`, `keyword_search_terms`, `search_his`
 - downloads: `download`, `downloads`, `DownloadManager`
 - WebView storage: `app_webview`, `Local Storage`, IndexedDB

For XBrowser `com.mmbox.xbrowser.pro`, check `db/mbrowser`, especially `history`, `search_his`, and `download`.

### Wallet

For imToken `im.token.app`, check:
 - `db/RKStorage`, table `catalystLocalStorage`
 - `f/walletsV2/*.json`
 - keys such as `reduxPersist:db`, `AccountModel`, `WalletModel`, `identifier`, `address`, `chainType`

Count accounts from account model arrays or account IDs, not only from visible addresses. Preserve case for addresses when reporting suffixes.

### Soul

For Soul `cn.soulapp.android`, check:
 - chat DBs named like `chat_*`
 - group tables such as `im_group_bean`
 - message tables for group chat activity
 - MMKV/strings for `group_nick_name`

To identify the most active group user, first filter to current joined groups, then count group messages by sender account/user ID. Map sender ID to nickname only after the account is established.

### AI Chat Apps

Find installed AI Q&A packages first from backup names and manifests. Candidate artifacts include:
 - SQLite chat/message/history DBs
 - SharedPreferences/XML login profile
 - React Native or Flutter local storage
 - request/response cache containing model names, prompts, conversation titles, and user profile

For model questions, look for explicit fields like `model`, `modelName`, `bot`, `llm`, `provider`, `assistant`, `agentId`. Do not infer the option from the app brand unless no artifact exists and the answer is marked tentative.

### Xiaomi Smart Home

For `com.xiaomi.smarthome`, search DB/XML/JSON for camera names, room names, `roomId`, `homeId`, `did`, `deviceId`, and location labels such as `后院`. Room IDs are usually in device/home relationship tables or cached home JSON.

### Alarm

For `com.android.deskclock` or MIUI Clock, inspect alarm databases and XML. Convert stored minutes or milliseconds into local time. If a label says flight/赶飞机, use that row as primary evidence.

### Recording Apps

For recording apps, use the app database over filesystem mtime. Search for file-password clues first, then identify the recording row and report the app's recorded creation time.

## Timestamps

Handle these formats explicitly:
 - Unix seconds: 10 digits
 - Unix milliseconds: 13 digits
 - Unix microseconds: 16 digits
 - Chrome/WebKit timestamp: microseconds since `1601-01-01 UTC`
 - Android alarm minutes: minutes since midnight
 - MIUI backup folder: `yyyyMMdd_HHmmss`

Default reporting for Chinese CTF mobile evidence is local device time if the artifact is local-app UI data. State the timezone if conversion was required.

## Answer Discipline

For each question, output:

```text
题号. 简短题名
答案：...
分析：在 <artifact path> 中，<table/key/field> 记录为 ...；因此答案为 ...
```

If an answer is not proven, say `未确认` and list the next artifact to inspect. Do not fill a CTF blank with a plausible guess unless the user explicitly asks for tentative answers.

## When Blocked

If a URL or public writeup is unavailable, continue from local evidence and known Android artifact patterns. Make the limitation explicit in the final note so the user knows which parts came from evidence and which came from reusable methodology.
