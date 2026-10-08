---
name: fit-ride-studio
description: Analyze one or more cycling, running, or hiking FIT/KML activity tracks, generate evidence-based single or aggregate reports, open the bundled local Ride Relief report page when the environment supports it, enrich results with user-confirmed public location context, and create shareable PNG or H.264 MP4 route stories on request. Use whenever a user wants to analyze, compare, visualize, or export .fit or .kml activities, including requests that mention a workout but do not yet include track files.
---

# FIT & KML Activity Studio

Turn local cycling, running, and hiking tracks into an evidence-based report and local visual experience. Follow this sequence:

1. Ask for FIT/KML files when none were provided, or use the bundled synthetic demo when requested.
2. Check the installation, install missing locked dependencies automatically, and analyze every valid file.
3. Present the result, stage private runtime files, and open the bundled Ride Relief report page when local browser access is available.

Enter the export composer only when the user asks for a shareable image, animation, or video. Ride Relief is the web app bundled inside this Skill, not a separate product to install.

## Workflow

### 1. Get the track files

- When the user explicitly asks for a demo, use `<skill-root>/samples/demo.kml`. State that it is fictional data.
- Otherwise, if no readable `.fit` or `.kml` was supplied, ask in the user's language for either an attachment or a local path. Example in Chinese: “请把 `.fit` 或 `.kml` 拖进对话，或告诉我文件路径（例如 `~/Downloads/ride.fit`）；可以一次给多个。”
- Stop after requesting missing input. Do not invent activity data and do not ask the user to configure the project.
- Proceed immediately when at least one file is accessible. Infer single versus aggregate mode from valid files.
- Accept a directory only when the user placed it in scope; expand only top-level FIT/KML files.
- Process tracks locally. Do not upload exact GPS tracks or expose coordinates in the response.
- Continue a batch when one file is corrupt, provided another track is valid. Report skipped basenames.
- Detect likely duplicates by start time, distance, and duration. Exclude them from totals and identify them.

### 2. Check readiness and analyze

Resolve `<skill-root>` as the directory containing this `SKILL.md`. Run from that directory:

```bash
node scripts/check-install.mjs
```

Handle its single-line status deterministically:

- `OK` — continue.
- `NEED_INSTALL` — run `npm ci`, rerun the check, then continue. Use the lock file; do not substitute `npm install`.
- `UNSUPPORTED_NODE` — explain the reported Node requirement and stop before running the app.
- `ERROR` — report the missing/broken Skill files and reinstall or update the Skill before continuing.

Treat `npm ci` as internal preparation, not a routine user step. If a sandbox blocks network access, request network permission when the environment supports approvals. If permission is unavailable, tell the user to run `npm ci` once from `<skill-root>`. If the Skill directory is read-only, explain that a writable installation or checkout is required; do not loop on installation or claim success.

Run the deterministic analyzer:

```bash
node scripts/analyze-fit.mjs --format json <fit-or-kml-path> [more-track-paths...]
```

Use `--format markdown` when a ready-to-read local report is sufficient. Use `--keep-duplicates` only after the user confirms matching activities are distinct. Read [references/report-contract.md](references/report-contract.md) when interpreting fields, checking weighting rules, or changing report behavior.

### 3. Present the result

Start with the result, not dependency or parser details.

For one activity, present:

1. A compact terrain/route verdict and the most important observation.
2. Distance and ascent when available; show duration, speed/pace, calories, and pauses only when supported.
3. Sport-appropriate recorded metrics: cycling speed/cadence, running pace/step cadence, hiking elevation/ascent, plus heart rate, power, temperature, and grade when present.
4. Data-quality coverage, especially cadence, heart rate, power, and grade.
5. Two to eight concrete suggestions ordered by impact.

For multiple activities, present:

1. Overall totals and date range.
2. A per-activity table with sport and source format.
3. Longest, most climbing, and fastest only within comparable activities with time data.
4. Earliest-to-latest deltas as observations, not proof of fitness improvement.
5. Sensor consistency, duplicates, and skipped files.
6. Aggregate suggestions plus important activity-specific exceptions.

Keep absent data distinct from zero. Say “未记录” / “not recorded” or “覆盖不足” / “insufficient coverage,” never zero when a sensor was unavailable. Do not invent FTP, power zones, heart-rate zones, VO₂max, training load, recovery status, or medical conclusions unless the user supplies the necessary thresholds and explicitly requests that analysis.

Apply these rules:

- Compute aggregate average speed as total distance divided by total moving time.
- Never infer duration, speed, pace, pauses, or photo-time matching from geometry-only KML.
- Prefer KML document metadata for declared sport, distance, ascent, and descent. Use the longest `LineString` or `gx:Track` and retain the source basename.
- Weight cadence, heart rate, power, and temperature by valid sample counts.
- Treat calories as device estimates and temperature as ambient/device temperature.
- Describe cadence as an activity-pattern observation, not a universal prescription. Confirm the running-cadence convention before interpreting spm.
- When grade coverage is adequate, report distance-weighted grade bands, smoothed P99 representative grade, and up to three continuous climbs; label the device maximum as raw.
- Match heat/hydration suggestions to recorded moving duration.
- Warn before sharing a highly closed route; recommend hiding the first and last 300–500 m.

Choose two to six evidence-backed deep dives. Omit empty or speculative dimensions.

When place-aware advice would materially improve the result, read [references/location-enrichment.md](references/location-enrichment.md). Confirm ambiguous public place names, search by the confirmed name rather than coordinates, and time-stamp live conditions. Do not treat an old activity as evidence that a route is currently open.

### 4. Stage and open the report page

Attempt this automatically after successful analysis, but adapt to the environment.

1. Read [references/ui-report-contract.md](references/ui-report-contract.md).
2. Write the model-authored report contract to a writable temporary JSON file. Do not store per-user analysis in `public/skill-analysis.json`.
3. For a batch, select the user's requested activity; otherwise use the longest non-duplicate as the representative route while keeping the text response aggregate.
4. Stage the selected track and analysis in the private OS temporary directory:

```bash
node scripts/prepare-report.mjs --track <selected-track> --analysis <temporary-report-json>
```

5. Read the returned JSON object. Keep its `url` and `session`; the URL expires after 24 hours, stale files are cleaned on the next staging run, and nothing is stored in the repository.
6. Fetch `http://127.0.0.1:5174/` and treat it as this project only when the returned HTML contains both `<title>Route Relief` and `id="fit-input"`. Otherwise start `npm run dev` from `<skill-root>`. The server uses port 5174 with `strictPort`; if another application owns the port, report the conflict instead of silently switching ports.
7. Use any available browser-opening or browser-automation capability to open the returned URL. The URL auto-loads the track and analysis; do not rely on setting a file input.
8. With screenshot/visual capability, verify the loaded source, the `Fit Ride Studio Skill` analysis badge, recommendation layout, and clipping. Without visual capability, skip visual claims and ask the user to inspect the opened page.

Apply these fallbacks honestly:

- If the Agent can open URLs but cannot automate page controls, open the URL; no further interaction is required for the report.
- If no browser tool exists but the user shares the same machine, provide the returned URL and say to open it manually.
- If running remotely or in a cloud container where the user's browser cannot reach that loopback address, deliver the text report and temporary analysis JSON instead. Do not claim the page opened.
- If staging is impossible because every writable temporary location is blocked, fall back to the existing file-input workflow and give concise manual steps.

Track the terminal/process handle used to start Vite. Before finishing, state whether the local server remains running and how to stop that exact process (for example, `Ctrl+C` in its terminal). Do not use a broad kill command. Clean a staged report after the user is finished when practical:

```bash
node scripts/prepare-report.mjs --cleanup <session-id>
```

Opening the report page does not authorize export or switching to **导出创作**.

### 5. Handle export requests

Read [references/export-workflow.md](references/export-workflow.md) before operating the export UI.

- Follow the user's activity selection; otherwise use a clear preference such as latest, longest, or most climbing.
- Prefer user media. Disclose when a built-in abstract background will be used.
- Default to 9:16, H.264 MP4 for motion, whole-activity summary card, watermark enabled, and safe placement. Use a 10-second single-background rotation or 2.5 seconds per route photo.
- Before rendering, tell the user that Chromium may open a native save picker that requires their own click; otherwise the browser downloads folder is used.
- Inspect the preview when visual capability exists. Without it, do not claim bounds were verified; ask the user to check the preview before the expensive render.
- Choose PNG for a still and MP4 for animation/video.
- Never claim success until rendering finishes and save/download is confirmed.

## Usability defaults

- Use basenames in reports and watermarks; omit absolute paths.
- Explain missing sensors once in the data-quality section.
- Preserve the current export layout when revisiting the composer.
- Avoid one “average activity” conclusion for mixed sports.
- Keep user files and generated reports out of the repository. Runtime copies live in the OS temporary directory; npm packages live in the Skill directory and may be replaced by updates.

## Examples

- “帮我分析一次运动。” with no file → Ask in Chinese for a dragged file or local path.
- “Show me the demo.” → Use `samples/demo.kml`, state that it is synthetic, analyze it, and open the local report when reachable.
- The user provides one FIT → Check/install, analyze, present, stage, and open the URL-loaded report.
- “把这 8 次骑行综合分析一下。” → Analyze valid non-duplicates and open the longest ride as the representative report unless another is named.
- “只看看数据，先别导出。” → Analyze and open the report page, but do not enter the export composer.
- A remote Agent cannot expose loopback → Deliver the text report and JSON, explain why the local page is unavailable, and do not pretend it opened.
