---
name: research-directory-conventions
description: Reference standard for creator-media research directory layout — platform-scoped nesting, handle-scoped data, dated snapshots, archive-before-replace, and README indexing
type: reference
version: v0.0
---

# Research Directory Conventions

Invoke as `$research-directory-conventions`.

Reference skill that defines the shared directory layout for all creator-media research. Skills in the `creator-foundation`, `youtube-ops`, and `remotion` packs should follow these conventions when writing artifacts.

## Directory Tree

```text
research/
├── <platform>/                              # e.g. youtube/, tiktok/, linkedin/
│   ├── <report-type>-<slug>[-YYYY-MM-DD].md # analysis reports
│   └── data/                                # raw evidence root
│       ├── <handle>/                         # per-channel / per-creator
│       │   ├── videos-YYYY-MM-DD.jsonl       # dated metadata snapshots
│       │   └── transcripts/                  # per-video transcript JSON
│       └── <video-id>/                       # per-video (external research)
│           ├── metadata-YYYY-MM-DD.json
│           └── transcript/<video-id>.json
├── creator-platforms/                        # multi-platform evidence
│   ├── capability-matrix.md
│   ├── evidence-schema.md
│   └── data/<platform>/<slug>/{raw,text,normalized,notes}/
├── creator-presence/                         # cross-platform dossiers
│   └── <slug>.md
specs/
├── <platform>/
│   ├── series-<slug>.md
│   ├── video-script-<slug>.md
│   └── video-build-<slug>.md
docs/
└── history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>
```

## Rules

1. **Platform-scoped nesting** — never write platform research directly to `research/`.
2. **Handle-scoped raw data** — `research/<platform>/data/<handle>/` for channel data, `research/<platform>/data/<video-id>/` for external video research.
3. **Dated snapshots** — never overwrite; create a new file with today's date.
4. **Archive before replace** — copy existing canonical report to `docs/history/archive/YYYY-MM-DD/HHMMSS/<path>` before replacement.
5. **Reports separate from data** — reports at `research/<platform>/`, raw data at `research/<platform>/data/`.
6. **README as index** — each platform directory has a README documenting current audit state.
7. **Specs separate from research** — production artifacts under `specs/<platform>/`, not `research/`.

## Validation

When validating directory structure compliance:
- Check that no report files exist directly in `research/` (must be nested under platform).
- Check that raw data lives under `data/` subdirectories, not alongside reports.
- Check that dated files use `YYYY-MM-DD` format.
- Check that `docs/history/archive/` exists if any canonical reports have been replaced.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Skill Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/research-directory-conventions-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/research-directory-conventions-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

