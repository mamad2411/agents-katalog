---
name: recalibrate-dash-p
description: >
  Recalibrate dash-p's recognition profile when a new Claude Code version ships.
  Drives the new TUI through a diverse SCENARIO BATTERY (short/long input, long
  output, code, markdown, tables, unicode, tool use), cross-checks every result
  against the session JSONL (ground truth), then fixes the profile/recognizer and
  validates before promotion. TRIGGER when `claude --version` is newer than the
  highest profiles/claude-*.json, or when dash-p returns degraded / low-confidence
  results, or startup hangs ("timed out waiting for the input box").
---

# Recalibrate dash-p

dash-p reads the Claude TUI by matching **literals** (markers, glyphs, anchors)
in `profiles/claude-<version>.json`, plus a small amount of structural logic in
`src/recognize/`. When the TUI changes, those drift and extraction degrades —
or, worse, a new startup gate hangs the engine. This skill regenerates and
re-validates from **evidence captured against the real TUI**, never by guessing.

The split that makes it reliable:
- a **deterministic harness** (`npm run recalibrate`) drives the real TUI through
  many scenarios and **auto-grades** each against the on-disk session transcript;
- **you (the agent)** read the report, separate real bugs from known ceilings,
  fix the profile (data) or `src/recognize/` (structure), and re-run;
- a **validation gate** (`npm test` + a clean re-run) proves it before promotion.

## When to run

- A scheduled check finds `claude --version` is newer than the highest
  `profiles/claude-*.json`.
- Users report `degraded: true` / confidence < 0.5, or a startup timeout.

## Procedure

### 1. Detect the version

```bash
claude --version          # e.g. "2.1.183 (Claude Code)"
ls profiles/              # highest characterised version
```

dash-p already does **nearest-version selection** (`selectProfile`): an unknown
patch reuses the highest profile ≤ installed. So a new patch usually *works*
already — recalibration is about catching the cases where it doesn't, and minting
a dedicated profile so the package can advertise support (the package `version`
tracks the newest profile).

### 2. Run the scenario battery (the core step)

```bash
CLAUDE_PATH=$(which claude) npm run recalibrate
#   → fixtures/recalibrate-report.{md,json} + a PASS/CEILING/REVIEW table
```

It runs ONE session through these scenarios and diffs each scraped result against
the session JSONL (exact model output):

| scenario | exercises |
|---|---|
| `short` | baseline prose extraction |
| `long-paragraph` | paragraph **reflow** (TUI hard-wraps; we rejoin) |
| `long-output` | long response: scrollback, numbered-list reflow |
| `code-block` | fenced code (markdown ceiling) |
| `markdown-mix` | heading/bold/italic/inline-code/list/quote (ceiling) |
| `table` | box-drawn table extraction |
| `unicode` | wide CJK / emoji / combining chars |
| `long-input` | ~2.6k-char paste (collapse + ingestion) |
| `tool` | tool_use / tool_result / permission handling |

Run a subset while iterating: `npm run recalibrate -- short,table,tool`.

### 3. Read the report — real bug vs. known ceiling

Each row gets a verdict:

- **PASS** (prose, sim ≥ 0.9 / exact) — extraction matches ground truth. Good.
- **CEILING** (markdown/tool, some loss) — **expected**. The TUI renders
  ```code```/**bold**/tables as styled output, so scraped text loses literal
  syntax; tool blocks summarise. Not a regression. `--enrich-from-session` gives
  the exact form when a caller needs it.
- **REVIEW** — investigate. The harness flags REVIEW for:
  - **chrome leak** (`❯`, `⏺`, `⎿`, an interrupt hint, a footer fragment, banner
    corners in the answer) → a real recognizer/profile bug. Fix it.
  - **prose below 0.9 similarity** → real extraction drift, *unless* it's a
    one-token wide-char artifact (see Known ceilings).
  - **send-error** (a turn threw) → a liveness bug (a stuck state, an unhandled
    gate). Fix it; these are the highest priority.

Per-scenario `scraped` vs `ground truth (JSONL)` blocks are in the `.md` report —
diff them to see exactly what drifted.

### 4. Capture a single frame for structure/marker calibration

When the report shows drift, dump real frames to find the new literals:

```bash
CLAUDE_PATH=$(which claude) npm run probe -- "Reply with exactly: hello"
#   → fixtures/spike-frames.txt (tagged with state/conf/matched), spike-final-buffer.txt
```

Then confirm/fix each profile field against the frames:

| Profile field | What to look for (and the traps hit so far) |
|---|---|
| `inputBox.promptMarkers` | The prompt glyph. **Trim-aware**: an empty prompt is just `❯` (trailing space trimmed) — use the bare glyph. |
| `idleMarkers` | Footer text when idle. Footer hints **drift** (`? for shortcuts` → `← for agents` / `bypass permissions`); add new anchors. The input box itself (not the footer) is the ground truth for readiness. |
| `busyMarkers` | **Interrupt hints only** (`esc to interrupt`). NEVER add `tokens` — newer footers show a persistent `N tokens` counter while idle, which would hang the engine. A token count is treated as activity only alongside an animated spinner. |
| `spinnerGlyphs` | Animation frames for masking only (braille + `✻✽✶…`). Exclude `·` — it's also a footer separator. |
| `assistantMarkers` / `userMarkers` | `⏺` / `❯`. |
| `startup.trustTriggers` | Workspace-trust dialog (Enter accepts). |
| `startup.gates` | **Other one-time onboarding prompts** with the keys that dismiss them. The "fullscreen renderer?" gate (2.1.183) MUST be **declined** (`["escape"]`) — its alt-screen/mouse renderer breaks screen-scraping. Add new gates here, not in the engine. |
| `chromePatterns` | Lines to strip from content: `─` rules, bare prompt, done-status (`^\s*[✻✽…]`), pure box-grid (`^[\s┌┐└┘├┤┬┴┼─━]+$`). Do **not** strip a lone `│` (that eats table content rows). |

Record *why* in the profile's `_note`.

### 5. Validate (gate before promotion)

```bash
npm run typecheck
npm test                                   # recognizer regression suite (must pass)
CLAUDE_PATH=$(which claude) npm run recalibrate   # re-run: no REVIEW except known ceilings
npx tsx src/cli/index.ts -o json "What is 6 times 7? Reply with just the number."
#   → result "42", degraded:false, confidence ≥ 0.5
```

Add a recognizer test in `test/recognizer.test.ts` for any new structural fix
(feed the captured snapshot, assert the state/extraction). This is how the
token-footer, fullscreen-gate, and table regressions are now locked in.

### 6. Promote

- Mint `profiles/claude-<version>.json` (calibrated), refresh `default.json`, and
  bump the package `version` to match the newest profile.
- If a field is uncertain or a REVIEW is unresolved, do **not** promote — leave
  the old profile, write up the unresolved scenario, and attach the report. A
  wrong profile that silently mis-extracts is worse than "needs human review".

## Edge cases this battery has surfaced (and how they're handled)

- **New startup gate** ("fullscreen renderer?") → generalized `startup.gates` in
  the profile; the engine dismisses each with its declared keys (decline = Esc).
- **Session pollution** → when dash-p runs *inside* Claude Code, the child
  inherited `CLAUDE_CODE_SESSION_ID` and wrote into the user's real conversation.
  The transport now scrubs the whole `CLAUDE_CODE_*` env family by prefix.
- **Multi-turn stuck state** → a turn that finished without the engine observing
  generation states left `submitting` set, hanging the next turn. The engine now
  clears it at every turn's end.
- **Box-drawn tables** → render as grid art; the `│`-row chrome strip used to eat
  the data. Now grid borders are stripped and content rows kept (still a ceiling:
  it's `│ … │`, not `| … |` — enrich for exact markdown).
- **Wide chars** → CJK/emoji extract correctly, but an occasional emoji can leave
  a one-cell artifact (e.g. a stray `)` after 🚀). A known ceiling; enrich for
  byte-exact.
- **Large output (big single Write / long answer)** → the render scrolls the
  input box off-screen, so viewport-only completion never fires and the turn used
  to hang to `turnTimeoutMs`. The engine now drives completion + content from the
  session JSONL (`turnCompletedAfter`, viewport-independent) and drains the PTY
  through a non-blocking buffer so a big burst can't backpressure `claude`.
  `completedBy === 'timeout'` is a failure signal. Covered offline by
  `npm run test:integration` against `test/fixtures/fake-claude.mjs` (small/large
  Write, long text, burst) — no live model needed.

## Guardrails

- Prefer changing **data (the profile)** over `src/recognize/`. Touch the engine
  only for genuinely new *structure* (a new gate type, a new layout) — and add a
  unit test when you do.
- Parse **text and structure, never colour or motion.** Cosmetic changes (new
  spinner art, new gradient) should only add glyphs to `spinnerGlyphs` /
  `chromePatterns` for masking.
- Keep `default.json` = the newest validated profile.
