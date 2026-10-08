# ScanSnap Bridge

Auto-process paper scans from the Fujitsu ScanSnap iX1500 into Idan's Obsidian vault via a Claude Code subprocess.

## Flow

```
iX1500 (tap touchscreen) → ScanSnap Home profile → ~/scansnap-inbox/*.pdf
                                                         │
                                                         ▼
                                     scansnap_bridge.py (daemon)
                                         │
                                         ├─ wait for file stability (polling)
                                         ├─ archive source → ~/ScanArchive/YYYY/MM/ (immutable)
                                         ├─ OCR derivative → extract text (pdftotext)
                                         ├─ spawn `claude -p` with prompts/classify.md
                                         ├─ parse JSON filing plan
                                         ├─ execute filing actions against vault
                                         └─ Slack DM summary
```

The **source PDF is never modified**. OCR is only used to extract text for classification; the archive copy remains exactly what came out of the scanner.

## Install

```bash
bash ~/.claude/skills/scansnap-bridge/install.sh
```

Installs `ocrmypdf`, `tesseract`, `poppler` via Homebrew; creates `~/scansnap-inbox/` and `~/ScanArchive/`; writes a launchd plist to `~/Library/LaunchAgents/`.

## Run

```bash
# foreground (for debugging)
python3 ~/.claude/skills/scansnap-bridge/scansnap_bridge.py

# as a persistent launchd agent
launchctl load ~/Library/LaunchAgents/com.idanbeck.scansnap-bridge.plist

# stop
launchctl unload ~/Library/LaunchAgents/com.idanbeck.scansnap-bridge.plist

# one-shot test against an arbitrary PDF
python3 ~/.claude/skills/scansnap-bridge/scansnap_bridge.py once /path/to/test.pdf

# status
python3 ~/.claude/skills/scansnap-bridge/scansnap_bridge.py status
```

Logs: `~/.claude/skills/scansnap-bridge/bridge.log`.

## ScanSnap Home profile config

Minimize ScanSnap Home's role to "driver that drops PDFs in a folder":

1. Open ScanSnap Home → Preferences → disable cloud sync, analytics, notifications, auto-launch on scan completion.
2. Create a profile (edit on the touchscreen if preferred):
   - **Name:** `Vault Scan`
   - **Save to folder:** `~/scansnap-inbox`
   - **File format:** PDF
   - **OCR:** OFF (we do our own OCR)
   - **Image quality:** Best or Excellent
   - **Color mode:** Auto
   - **Paper size:** Auto (lets ADF handle mixed sizes)
   - **Feed:** Duplex (catches back sides automatically)
   - **Rotation:** Auto
   - **Blank page removal:** ON
   - **File name:** `{datetime}` — timestamp-based so we never collide
3. Delete every other profile so the touchscreen shows only `Vault Scan`.
4. ScanSnap Home's auto-organize, auto-tagging, cloud upload, business card extraction, etc. — all OFF.

The iX1500 requires a button press (touchscreen tap) to start a scan. There's no hands-off auto-trigger. Accept that.

## Vault destinations by category

| Category | Lands in |
|----------|---------|
| `handwritten_notes` | Today's daily note (`#log` section) + optional `Meetings/...md` |
| `meeting_notes` | `Meetings/YYYY-MM-DD - <topic>.md` |
| `receipt` / `invoice` | `Epoch/Finance/receipts/YYYY-MM.md` or `Epoch/Finance/invoices/YYYY-MM.md` |
| `business_card` | `People/<First Last>.md` stub with frontmatter |
| `research_paper` | `Reading/Research/<Title>.md` stub |
| `contract` / `legal` | `Epoch/Legal/inbox.md` + flag |
| `tax_document` | `Epoch/Admin/<year>/tax.md` |
| `kids_school` | `Personal/Family/kids/<year>/` |
| `correspondence` | `Personal/Correspondence/YYYY.md` |
| `other` / unsure | Flag → `~/scansnap-inbox/_needs_review/` |

Every destination note embeds a `file://` link back to the archive PDF, with page range.

## Files

| File | Role |
|------|------|
| `scansnap_bridge.py` | Main daemon (watch, OCR, spawn Claude, file, notify) |
| `prompts/classify.md` | Classification prompt — defines categories, schema, vault conventions |
| `install.sh` | Dep install + plist install |
| `com.idanbeck.scansnap-bridge.plist` | launchd agent (written by `install.sh`) |
| `bridge.log` | Runtime log |
| `.bridge.state.json` | Per-file stability-check state (transient) |

## Failure modes

- **OCR fails** → text extraction falls back to `pdftotext` on the raw scan. Often still works for printed docs.
- **No OCR text** → classifier is given a marker to flag the scan for review.
- **Claude subprocess returns non-JSON** → the bridge logs the output and moves the scan to `_needs_review/`.
- **Filing action references a missing path** → logged as a flag in the Slack notification; vault unchanged.
- **Daemon crashes mid-process** → pending files stay in the inbox and are retried on next start. Source is only moved to archive _after_ successful read; only fully-filed scans are removed from state.

## Customization

- Change the Slack DM target: edit `SLACK_DM_TARGET` in `scansnap_bridge.py`.
- Adjust stability window: `STABILITY_CHECKS` (consecutive polls) and `POLL_INTERVAL_S`.
- Classification timeout: `CLAUDE_TIMEOUT_S`.
- Edit the classification logic by editing `prompts/classify.md` — no code change required.

## Non-goals

- **Never modify the source PDF.** The archive copy is ground truth.
- **No cloud upload.** Everything stays local.
- **No deletion.** Scans are archived, not deleted, even if classification fails.
