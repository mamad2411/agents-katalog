---
name: check-my-app
description: Check an app the user built with AI for security problems, explain the results in plain language, fix them, and record the app in AppLedger. Use when the user says "check my app", "is my app safe", "is this secure", "add this app to AppLedger", asks whether their app is ready to share, wants a security check or review, or is about to deploy or share an app with colleagues.
---

# Check my app

The user built an app, often with an AI tool, and wants to know if it's safe to share. They may not be a developer. Your job: get an honest, independent verdict, explain it in everyday words, and fix what they agree to fix. Checking an app also adds it to their AppLedger dashboard if this computer is connected.

## 1. Ask before uploading

By default the check uploads the project's source files to appledger.net, where they are scanned and deleted right after. The user must agree to that first.

1. Find the app's folder. Use the current project unless the user names another folder. Pass an absolute path.
2. Call `preview_upload` with that path. Summarise it in one or two sentences, for example: "To check it, AppLedger will send 48 source files (1.2 MB) to appledger.net over an encrypted connection; they're deleted right after the scan. Secret files like `.env` and key files stay on your computer (3 left out)."
3. Ask: **"Are you allowed to upload this code?"** If it belongs to an employer or client and they're not sure, suggest local mode (below) or checking with their IT team first. Don't upload until they say yes.
4. If they say yes, call `check_app` with the path and `confirm_upload=True`. It usually takes 10–30 seconds; tell them it's running.
5. If `check_app` returns `needs_confirmation` (for example when you called it without asking), don't retry on your own. Show the user its upload preview, ask as in step 3, and call again with `confirm_upload=True` only after they agree.
6. If it returns `ok: false`, show the error in plain words. Call `scanner_status` if the service seems unreachable. If it says the connection key was revoked, tell them to create a new key in the dashboard.

Only ask once per folder; later checks of the same folder don't need a new preview unless the user wants one. If the user runs AppLedger in local mode, nothing is uploaded, so skip steps 2–3.

**Local mode** (nothing uploaded): the user installs Trivy and Opengrep and sets `APPLEDGER_MODE=local` before starting Claude Code, or runs `python -m appledger PATH --local` in a terminal. Call `scanner_status` to see whether the scanners are found. With a connected dashboard, local mode still saves a summary (app name, score, grade, problem counts, the list of problems found (level and short title, never code or file paths)); pass `save_to_dashboard=false` if they don't want that. Setup steps: https://appledger.net/docs/#local

## If the AppLedger tools aren't available

The plugin starts its tools with `uv`. If `preview_upload` and `check_app` don't exist in this session:

1. Check with `uv --version`. If uv is missing, tell the user the plugin needs it (it also installs Python
   for them) and offer to install it with the official installer: Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`, macOS or Linux
   `curl -LsSf https://astral.sh/uv/install.sh | sh`. Run it only if they agree, then ask them to start a new Claude Code session.
2. Or use the command line instead, which works without the plugin's tools: `python -m pip install appledger`,
   then `python -m appledger PATH --list-files` to show what would be sent, ask as in step 3, and run
   `python -m appledger PATH --yes` once they agree. Read the results from `PATH/.appledger/findings.json`
   (its `save_link`, if present, is the save link described under Dashboard).
   To connect a dashboard this way, the user runs `python -m appledger --connect KEY` themselves.

## 2. Explain the result

Lead with the verdict, then the problems. Keep it short and concrete.

- Start with the grade, the score, and who may use the app right now (from `who_can_use_it`).
- Explain the "Fix before sharing" items first, one line each, using the finding's own plain wording. Say what could happen, not the technical name.
- Summarise "Fix soon" items in a sentence or two. Mention "Good to know" items only if asked.
- Don't paste CVE numbers, rule IDs or file dumps unless the user asks.
- Tell them the full report is in `report.html` (give the path) if they want to read it.
- If a finding says a secret file (such as `.env` or a key file) is committed to Git or not ignored: its content was not uploaded, but anyone who can see the repository can read it. Tell them to **create new keys at each provider and revoke the old ones**, then add the file to `.gitignore` and remove it from Git.

Then ask: "Do you want me to fix these?"

## 3. Fix, then check again

1. Call `get_fix_prompt` with the same path and follow it, most serious first.
2. After each fix, say in one plain sentence what you changed.
3. Never remove a feature to make a warning disappear. If a fix would change how the app behaves, ask first.
4. Never put keys or passwords in code. Move them to environment variables. **Tell the user that any key that was in the code must be treated as leaked and replaced** (for example a new Stripe or Slack key), because you can't do that for them.
5. When done, call `check_app` again (same path, `confirm_upload=True` since they already agreed) and show the old and new score side by side, plus anything still open.

## Dashboard

If `check_app` returns `dashboard` with `recorded: true`, say in one line that the app is saved in their AppLedger dashboard and give the link. If it returns `save_link`, mention it once, in one line at the end, without pushing: "If you want to keep this result, you can save it to a free AppLedger ledger with this link (it works for 24 hours): <save_link>." Don't repeat it after later checks in the same conversation unless asked. Opening the link lets them create an account or log in, and the result is saved; the page then offers a key so later checks are saved by themselves. If it isn't connected and they want a dashboard, point them to https://appledger.net/app/ → "Connect a computer". If the user gives you a connection key (it starts with `al_`), call `connect_dashboard` with it. Never invent a key, and only use one the user gave you in this conversation.

## Scheduled checks

If the user wants the app checked regularly, suggest they install the package once (`python -m pip install appledger`; the plugin alone isn't enough, because scheduled runs happen without Claude Code) and run this once in a terminal (you don't run it for them):

```
python -m appledger PATH --schedule weekly --yes
```

Use the app's real path. `--yes` confirms the upload for unattended runs; `daily` and `off` also work, and `python -m appledger --schedules` lists what's scheduled. It uses Windows Task Scheduler or cron, so it runs even when Claude Code is closed.

## Tone

Be honest and calm. Don't scare, don't reassure falsely. If the scanners found nothing serious, say so plainly, and add that scanners can't catch everything (for example a page with no login that shows private data), so the user should still think about who can reach each page.
