---
name: buda-video-studio
description: "Manage Buda video production from a Google Drive-backed library: scan ideas/raw footage/transcripts, launch a local review app, approve post-production readiness, cover copy, output formats, and distribution checklists."
---

# Buda Video Studio

Use this skill when the user wants to manage Buda video production work: video topic directions, raw footage readiness, post-production handoff, cover copy, output formats, and distribution channels.

This skill follows the App-in-Skill pattern:

- The skill reads the configured online Google Drive video library and prepares a local review batch.
- The local app is a quiet operator surface for review, notes, approvals, cover copy, channel decisions, and published-link records.
- The app reads and writes local handoff files and may sync video decision state to a single Google Drive JSON file.
- External or irreversible actions require the skill to re-read approvals before executing.

## Default Workflow

When the user asks to review video production status, post-production readiness, cover copy, output formats, or distribution channels:

1. Run `node scripts/generate_batch.mjs` from this skill directory.
2. If onboarding says OAuth client exists but no token is configured, run `node scripts/auth_google_drive.mjs`, have the user approve the browser prompt, then run `node scripts/generate_batch.mjs` again.
3. Start or reuse the local app with `app/start.sh`.
4. Report the local URL printed by the launcher.
5. Tell the user the app stores local cache files and, when Drive write scope is authorized, syncs decisions to `buda-video-status.json`.

When the user asks to execute approved decisions:

1. Run `node scripts/validate_ui_schema.mjs`.
2. Run `node scripts/execute_decisions.mjs`.
3. Summarize the execution report.

If the user says "chat only", "no UI", "纯聊天", or similar, do not launch the app. Summarize the batch in numbered items and collect approvals in chat.

## Data Sources

The primary source is online Google Drive through the Drive API. Do not rely on a user's local Drive sync path for the normal workflow.

```yaml
data_reader: "google_drive_api"

google_drive:
  mode: "api"
  root_folder_id: "Google Drive folder id for Buda Videos"
  auth_mode: "device"
  client_secret_path: "~/.config/buda-video-studio/google-oauth-client.json"
  token_path: "~/.config/buda-video-studio/google-oauth-token.json"
  access_token_env: "BUDA_VIDEO_GOOGLE_ACCESS_TOKEN"
  status_file_name: "buda-video-status.json"
```

`local_drive` may exist as an explicit development fallback only. It is not the default and should not be used for team-facing workflows.

The expected online Drive shape is project-folder based:

```text
Buda Videos/
├── use-case-whisper/
│   ├── Raw/
│   │   └── 成品样片/
│   ├── Covers/
│   ├── Youtube/
│   ├── Shorts/
│   ├── 原视频/
│   └── 视频号/
└── intro-workbench-ui/
    ├── Raw/
    │   └── 成品样片/
    ├── Covers/
    ├── Youtube/
    ├── Shorts/
    └── 视频号/
```

`Raw/成品样片/`, `封面素材/`, or configured cover-source folders are treated as cover source/material for production readiness. `Covers/` contains final generated cover outputs; if a final cover already exists in `Covers/`, the cover-material check is also treated as satisfied.

Configuration lookup order:

1. `BUDA_VIDEO_STUDIO_CONFIG=/absolute/path/to/config.yml`
2. `config.local.yml` in this skill directory
3. `~/.config/buda-video-studio/config.yml`
4. `config.example.yml`

`config.example.yml` is a template only. If no private config exists, if the root folder id is missing, or if OAuth is not ready, show onboarding instead of pretending the video library is available.

## Safety Rules

- Do not publish videos, upload to social platforms, delete Drive files, or move large file sets from the local app.
- The skill may call Google Drive API for listing, reading configured video assets, and creating/updating the configured status JSON file.
- Treat publication, deletion, account access, paid promotion, customer data, and brand/legal claims as approval-required.
- Keep Drive credentials, private folder IDs, and tokens out of batch files, UI state, logs, reports, and screenshots.
- Do not write video assets, move folders, delete files, or publish content from the app; the only Drive mutation allowed by default is the status JSON file.
- The app may show only safe config summaries: source mode, configured root path readiness, folder names, channel names, and style settings.
- Before executing, re-read `app/.cache/decisions.json` and refuse to act on missing approvals.

## File Contract

- `app/.cache/current_batch.json`: latest generated video review batch.
- `app/.cache/decisions.json`: user decisions, notes, publication links, and local item edits.
- `app/.cache/execution_report.json`: latest generated briefs/checklists report.
- `app/.cache/agent.lock`: lock while the skill writes batch/report files.
- `buda-video-status.json`: optional Google Drive root-level state file used to remember decisions, completion state, and publication links across environments.

## Video Stages

- `idea`: topic or concept only. The app shows this first in `选题表`; once accepted it moves to `待分配录制`, then to `待补齐素材`.
- `script_ready`: script, outline, or transcript exists but footage is not ready.
- `assets_ready`: raw footage exists.
- `ready_for_edit`: raw footage and supporting notes/transcripts are ready for post-production.
- `editing`: currently in post-production. The app uses this when editing has started but channel export files have not appeared yet.
- `cover_review`: needs cover copy or cover approval.
- `render_ready`: ready to render/export.
- `distribution_ready`: exported asset exists and needs distribution work.
- `published`: already published or archived as done.
- `blocked`: missing critical source material or user direction.

## Rule Definition

Use `references/video-rules.md` as the canonical rule explanation. In short:

1. Treat each direct child folder under the configured Drive root as a video project.
2. Identify raw footage, scripts, transcripts, cover source/material images, final `Covers` outputs, and channel exports from configured folder names and file extensions.
3. For each project, automatically check the three required production items: voiceover/script markdown or subtitle/transcript file, PNG/JPG/JPEG cover source/material image, and raw video. If a final cover already exists in `Covers`, treat the cover-material check as satisfied.
4. Show the human workflow as: `选题表` -> `待分配录制` -> `待录制` -> `待补齐素材` -> `待进入后期` -> `剪辑中` -> `待制作封面` -> `待确认分发`.
5. Apply asset priority: selected YouTube language exports plus 视频号 and final cover -> distribution confirmation. Default projects require YouTube Chinese and English; single-language projects can uncheck the unused YouTube language in `输出渠道`, so one YouTube export can be enough. Shorts is optional and should be shown when present, but missing Shorts must not block `待确认分发`; editing started or channel exports without final cover -> cover production; all three required production items present -> post-production handoff; partial source material -> idea/recording queues.
6. Add human-readable missing-item risks when a required item is absent.
7. Allow a human override from `待补齐素材` to `剪辑中` only when voiceover/script evidence and raw video are present and the only missing required item is the cover source/material.
8. Keep the app read/write only over local handoff files; external actions remain skill-side and approval-gated.

## State and Sync

- Use the app's `重新同步` control, or rerun `node scripts/generate_batch.mjs`, whenever Google Drive files change.
- Google Drive remains the source of truth for assets. The app should not require local Drive sync paths.
- Local human decisions are stored in `app/.cache/decisions.json`.
- If Drive write scope is available, decisions are also merged into `buda-video-status.json` so another environment can remember owners, due dates, recording status, workflow overrides, completion, and publication links.
- Re-sync must preserve the current Google Drive OAuth config/token and merge status JSON back into the local cache.

## App Actions

The app stores decisions locally and syncs them to the Drive status file when available. After a video is marked complete, the app can also record the public URL for each selected distribution channel. The skill performs approved follow-up work.

Supported decision actions:

- `approve`: ready for the next skill-side step.
- `revise`: user requested changes or extra direction.
- `block`: cannot proceed.
- `no_action`: intentionally skip.

Approved first-version execution creates local files only:

- post-production brief markdown files under `app/.cache/briefs/`
- distribution checklist markdown files under `app/.cache/distribution/`
- `app/.cache/execution_report.json`

No external publication is performed.
