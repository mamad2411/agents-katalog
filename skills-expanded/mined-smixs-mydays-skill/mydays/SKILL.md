---
name: mydays-skill
description: >
  Audit local app-usage tracking and create a private standalone interactive HTML report from macOS or Windows foreground-time data. Use when a user asks what apps consume their day, requests a Screen Time or ActivityWatch preflight, wants app usage by month, day, and hour, or wants Computer Use to verify permissions and test the report. Do not use for website analytics, employee surveillance, mobile-only parental controls, or generic dashboard styling without local usage data.
---

# MyDays Skill

Build an honest, local report of time spent in desktop apps. Verify collection first, collect one non-overlapping source, render one offline HTML file, and test it through Computer Use.

## Truth contract

- Define app usage as foreground time while the user is not AFK.
- Report measured intervals only. Never invent or extrapolate missing history.
- Show requested coverage and measured coverage separately.
- Label uncovered months as «Нет данных», not zero.
- Use one source for any overlapping period. Never add Screen Time, macOS Knowledge, and ActivityWatch totals together.
- Keep window titles, URLs, document names, and raw events out of the report.
- Treat all collected data as private. Keep it on the machine unless the user explicitly requests a transfer or publication.
- Support macOS and Windows in v1. On Windows, exact collection requires ActivityWatch with the window and AFK watchers.
- On macOS, report the current Mac by default. Claim «all Apple devices» only after Computer Use visibly verifies Share Across Devices and the selected source includes them.

## Required tools

- Use the installed Computer Use skill for System Settings, Windows Settings, tray apps, and browser QA. Read its `SKILL.md` before the first UI action.
- Run the deterministic scripts with `uv run`. They use the standard library and do not install packages.
- Use the included HTML template. Do not add a build step, CDN, font request, analytics script, or external chart library.
- Treat the included CSS and layout as the finished theme. Report generation only injects normalized data; do not redesign or regenerate styles for each run.
- If `humanizer-ru` is installed, read it before editing Russian public text. The hard rules below remain mandatory even when it is unavailable.

## Workflow

### 1. Fix the scope

Confirm or infer the requested dates, device scope, output location, and whether the user accepts an accurate partial report when history is missing. State the success criterion before collecting: one standalone HTML file with source, coverage, totals, app ranking, month/day/hour views, and working filters.

When the user names a range ending in the current month without an end day, use today as the inclusive end. Future days are outside the request, not «Нет данных». If the user explicitly includes future dates, label them «Ещё не наступило» and keep them separate from missing history.

Use inclusive dates in the UI and CLI. Example:

```bash
uv run scripts/preflight.py \
  --start 2026-01-01 \
  --end 2026-07-31 \
  --output-dir ./mydays-output \
  --json
```

Add `--all-devices` only when the user asks for all Apple devices.

### 2. Run the read-only preflight

Run `scripts/preflight.py` before opening settings. It checks the operating system, output path, local data sources, ActivityWatch, and which UI checks remain.

Then follow the relevant checklist:

- macOS: read `references/preflight-macos.md`.
- Windows: read `references/preflight-windows.md`.

Use Computer Use to verify every required item. A required item is either ready, blocked, or awaiting the user's action. Do not call it ready from memory or from an old screenshot.

When a setting is off:

1. Navigate to the exact control with Computer Use.
2. Explain the change and why collection needs it.
3. Ask for confirmation immediately before the toggle, install, login, or restart.
4. After confirmation, perform only that action.
5. Observe the fresh UI state and rerun the relevant check.

Never toggle a privacy setting, install ActivityWatch, enable autostart, or restart an app before confirmation. Hand off passwords, Touch ID, Windows Hello, CAPTCHA, and account selection to the user.

### 3. Apply the coverage gate

Read `references/data-contract.md`. Compare the first and last measured events with the requested dates.

If coverage is incomplete, present the real options:

- build an accurate partial report now - recommended;
- stop, enable future collection, and return after enough data exists.

Offer a partial report only when measured events exist. A third-party export needs a separate conversion into `references/data-contract.md`; v1 has no generic import command, so do not promise one.

Do not offer an estimate as if it were history. If the user explicitly asks for a projection, keep it visually separate and label it «Оценка».

### 4. Collect one source

Run:

```bash
uv run scripts/collect_usage.py \
  --start 2026-01-01 \
  --end 2026-07-31 \
  --source auto \
  --output ./mydays-output/usage-data.json
```

Source rules:

- Windows: use ActivityWatch. If it is missing or lacks either watcher, stop at the preflight.
- macOS: `auto` compares readable macOS Knowledge data with ActivityWatch, chooses the source with more active days, and prefers AFK-filtered ActivityWatch on a tie.
- Never merge overlapping candidates. The collector records which source won.

### 5. Render and check the text

Read `references/report-quality.md`. Render the report and run the text gate:

```bash
uv run scripts/render_report.py \
  ./mydays-output/usage-data.json \
  ./mydays-output/mydays-report.html

uv run scripts/text_lint.py ./mydays-output/mydays-report.html
```

Public Russian text must pass these rules:

- Name the thing directly: «Сутки», «По дням», «Приложения», «Покрытие».
- Do not turn chart geometry into copy. Never write «Сутки как орбита», «ландшафт внимания», «пульс продуктивности», or similar metaphors.
- Prefer a fact or instruction over mood: «Выберите приложение. Графики покажут часы и дни использования.»
- Remove канцелярит, advertising adjectives, vague significance, rhetorical questions, and chatbot closings.
- Ban «не просто», «не только», abstract «ключевой», «уникальный», «яркий», and long em dashes.
- Keep headings short. A chart title says what is measured, not how clever the visual is.
- Read every label aloud once. If it sounds like a product pitch or could fit any dashboard, rewrite it.

The linter catches common failures. It does not replace an editorial read.

### 6. Test the artifact

Run deterministic tests first:

```bash
uv run scripts/self_test.py
```

Open the generated file in a browser through Computer Use and verify:

1. the source, requested period, measured coverage, missing months, and partially covered months are visible;
2. month selection changes all charts;
3. app selection changes all charts;
4. an app and month can be selected together;
5. keyboard focus is visible and controls have useful accessible names;
6. the page works at a narrow mobile-sized viewport;
7. `prefers-reduced-motion` removes nonessential motion;
8. the report makes no external network requests.

Fix the cause of any failure and repeat the affected check.

### 7. Hand off the result

Give the user:

- the exact path to the HTML file;
- the measured source and device scope;
- requested and measured dates;
- missing coverage or other limitations;
- whether future collection is now ready.

Do not bury missing data below the file link.

## Failure rules

- No historical data: do not reconstruct it from Battery, Task Manager App history, browser history, or guesses.
- ActivityWatch reachable but empty: verify both default watchers and the requested date range.
- macOS database exists but is unreadable: verify Full Disk Access through Computer Use; request confirmation before changing it.
- Source totals disagree: choose the source with the clearest foreground and AFK semantics; disclose the choice.
- UI state is ambiguous: observe again or ask the user. Do not click speculatively.
- Report has data but no useful story: improve ordering and annotations with facts already present. Do not add metaphors.

## Included resources

- `scripts/preflight.py` - read-only machine and source checks.
- `scripts/collect_usage.py` - normalized interval collection.
- `scripts/render_report.py` - standalone HTML renderer.
- `scripts/text_lint.py` - Russian public-copy gate.
- `scripts/self_test.py` - interval, aggregation, rendering, and copy tests.
- `references/data-contract.md` - source semantics and normalized schema.
- `references/preflight-macos.md` - macOS Computer Use checklist.
- `references/preflight-windows.md` - Windows Computer Use checklist.
- `references/report-quality.md` - report acceptance criteria.
- `assets/report-template.html` - offline responsive report template.
