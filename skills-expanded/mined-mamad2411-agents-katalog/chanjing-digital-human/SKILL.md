---
name: chanjing-digital-human
description: Generate Chanjing digital-human videos for FrameVideo projects. Use when creating, listing, polling, or wiring Chanjing public/custom digital humans into a composition; adapts Chanjing OpenAPI auth to FrameVideo's shared credential store, Studio proxy routes, and assets/digital-humans output convention.
---

# Chanjing Digital Human

Create Chanjing digital-human MP4/WebM assets and wire them into FrameVideo compositions. This is the FrameVideo-adapted form of `chanjing-video-compose`: reuse this repo's OpenAPI client and auth store instead of copying standalone Python credential scripts.

## Auth Contract

Use the existing implementation in `packages/cli/src/tts/chanjingOpenapi.ts`.

Credential priority:

1. `CHANJING_OPENAPI_ACCESS_TOKEN`
2. `CHANJING_OPENAPI_APP_ID` plus `CHANJING_OPENAPI_SECRET_KEY`
3. stored `chanjing_openapi` credentials in the shared Chanjing credential store

The store is read through `packages/cli/src/auth/store.ts`, so it honors `CHANJING_CONFIG_DIR` and shares the same `~/.chanjing` credential location used by `framevideo auth` and Studio. Do not create a separate credentials file for this skill.

Useful commands and routes:

```bash
framevideo auth status
```

Studio auth routes, when the Studio server is running:

```text
GET    /api/projects/:id/chanjing/auth/status
POST   /api/projects/:id/chanjing/auth/login
DELETE /api/projects/:id/chanjing/auth
```

`POST /chanjing/auth/login` accepts `app_id` and `secret_key`; the server exchanges them for an access token and persists the result in the shared store.

## API Surface

Prefer `ChanjingOpenApiClient` over hand-written fetch calls:

- `listDigitalPersonTags()` uses `/common/tag_list?business_type=1`
- `listCommonDigitalPersons({ page, size, tagIds, source })` uses `/list_common_dp`
- `listCustomisedPersons({ page, size, source })` uses `/list_customised_person`
- `createDigitalHumanVideo(options)` uses `/create_video`
- `getDigitalHumanVideo(id)` uses `/video`
- `getUserInfo()` uses `/user_info`

OpenAPI base URL defaults to `https://open-api.chanjing.cc/open/v1`. Override with `CHANJING_OPENAPI_BASE_URL`; `CHANJING_API_URL` is also supported and gets `/open/v1` appended.

## Recommended Talking-Head Defaults

For normal spoken-presenter digital-human videos, start from these defaults unless the user asks for a different delivery target.

Default 1080p presenter:

```ts
{
  screenWidth: 1920,
  screenHeight: 1080,
  resolutionRate: 0,
  model: 0,
  speed: 1,
  pitch: 1,
  volume: 100,
  hideSubtitle: true,
  personX: 0,
  personY: 0,
  personWidth: person.width,
  personHeight: person.height,
  bgColor: "#ffffff",
  backway: 1,
}
```

High-quality final delivery:

```ts
{
  screenWidth: 3840,
  screenHeight: 2160,
  resolutionRate: 1,
  model: 1,
  speed: 0.95,
  pitch: 1,
  volume: 100,
  hideSubtitle: true,
  bgColor: "#ffffff",
  backway: 1,
}
```

Transparent presenter overlay for FrameVideo compositing:

```ts
{
  screenWidth: 1920,
  screenHeight: 1080,
  resolutionRate: 0,
  model: 1,
  speed: 1,
  pitch: 1,
  hideSubtitle: true,
  isRgbaMode: true,
  personX: 0,
  personY: 0,
  backway: 1,
}
```

Parameter guidance:

- `hideSubtitle: true` is the preferred default because FrameVideo captions are easier to style, animate, and edit. Use `false` only when the user explicitly wants Chanjing platform subtitles burned into the generated video.
- `model: 0` is good for iteration and ordinary 1080p output; use `model: 1` for final delivery, close-up presenters, 4K, or transparent overlay assets.
- Keep `speed` between `0.9` and `1.05` for most talking-head videos. Use `0.95` for serious explainers and `1.05` for upbeat short-form delivery.
- Keep `pitch: 1` unless the selected voice sounds obviously too low or too sharp.
- `resolutionRate: 0` means 1080p; `resolutionRate: 1` means 4K.
- Avoid `driveMode: "random"` for formal spoken presenter videos; normal sequential driving is steadier.
- Use `isRgbaMode: true` only for custom digital humans that support four-channel WebM output. RGBA mode normally omits subtitles and background, which is ideal for compositing into FrameVideo.

## Standard Workflow

1. Confirm the digital-human source: `common` for public people, `custom` for user-trained people. If unclear, start with `common`.
2. Check auth with `getChanjingOpenApiAuthStatus()` or the Studio auth status route. If missing, ask for `app_id` and `secret_key` or point the user to the Studio login UI.
3. List candidates before choosing. For common people, include tag filters if the user described style, age, role, or gender. Compare `name`, `cover`, `previewVideoUrl`, `audioManId`, `audioName`, `figureType`, `width`, and `height`; do not blindly pick the first candidate.
4. Select `audioManId`. Public people often include a matching voice; custom people may require the returned or user-selected voice.
5. Ask for subtitle preference before creating the task unless the current workflow already supplied it. Use `hideSubtitle: true` when the user wants no subtitles; use `false` only when they explicitly want platform subtitles.
6. Create the task with `createDigitalHumanVideo`. Keep defaults conservative: 1920x1080, `resolutionRate: 0`, `model: 0`, `hideSubtitle: true`, person at x/y 0 unless a layout requires otherwise.
7. Poll `getDigitalHumanVideo(taskId)` until a terminal status. Treat `video_url` as success; throw or report `msg`, failed status, or timeout.
8. Always download generated digital-human videos into the project's asset library before wiring them into a composition. Use `assets/digital-humans/<slug>.mp4` for normal output and `assets/digital-humans/<slug>.webm` for VP9-alpha/RGBA output; return and store the project-relative asset path.
9. When editing an `.html` composition, add the generated local asset as a normal FrameVideo video element and then run `npx framevideo lint` plus `npx framevideo validate`.

## Studio Route Workflow

When working through Studio or a local server, prefer the existing routes in `packages/cli/src/server/studioServer.ts`:

```text
GET  /api/projects/:id/digital-humans/tags
GET  /api/projects/:id/digital-humans/common?tagIds=1&tagIds=2
POST /api/projects/:id/digital-humans/custom
POST /api/projects/:id/digital-humans/generate
```

`/digital-humans/generate` expects:

```json
{
  "person": { "id": "person-id", "source": "common" },
  "text": "Script to speak",
  "audioManId": "voice-id",
  "outputName": "presenter-intro",
  "duration": 8
}
```

The route creates the Chanjing task, waits for completion, downloads the generated video into `assets/digital-humans/`, and returns `assetPath`, `taskId`, `durationSeconds`, `videoUrl`, and `previewUrl`.

## Direct TypeScript Pattern

Use this pattern from repo code, scripts, or tests:

```ts
import { mkdir } from "node:fs/promises";
import { join } from "node:path";
import { ChanjingOpenApiClient } from "../packages/cli/src/tts/chanjingOpenapi.js";

const client = new ChanjingOpenApiClient();
const { digitalHumans } = await client.listCommonDigitalPersons({ page: 1, size: 30 });
const person = digitalHumans.find((item) => item.audioManId);
if (!person?.audioManId) throw new Error("No suitable digital human with audioManId");

const taskId = await client.createDigitalHumanVideo({
  person,
  text: "欢迎使用 FrameVideo 生成数字人视频。",
  audioManId: person.audioManId,
  screenWidth: 1920,
  screenHeight: 1080,
  hideSubtitle: true,
});

let videoUrl: string | undefined;
for (let i = 0; i < 180; i++) {
  const video = await client.getDigitalHumanVideo(taskId);
  if (video.video_url) {
    videoUrl = video.video_url;
    break;
  }
  if (video.msg && /fail|error|失败/i.test(video.msg)) throw new Error(video.msg);
  await new Promise((resolve) => setTimeout(resolve, 2000));
}
if (!videoUrl) throw new Error(`Timed out waiting for digital-human task ${taskId}`);

await mkdir(join(projectDir, "assets", "digital-humans"), { recursive: true });
```

Reuse existing repo helpers for slugging, polling, or downloading when editing `studioServer.ts`; do not duplicate them unless you are building an isolated test fixture.

## Composition Wiring

Generated digital-human videos must be stored as project assets under `assets/digital-humans/`. Do not reference Chanjing `videoUrl` directly from composition HTML, Studio timeline entries, generated templates, or examples; download first, then reference the project-relative asset path.

```html
<video
  class="clip"
  src="assets/digital-humans/presenter-intro.mp4"
  data-start="0"
  data-duration="8"
  data-track-index="1"
  muted
  playsinline
></video>
```

For talking-head overlays, keep the digital human on a higher track than the background. If the asset has an opaque background and the user wants a transparent presenter, generate the video first, then use the `framevideo-media` background-removal workflow to create a VP9-alpha `.webm`.

## Selection Rules

- Public library request: list common people, optionally with tags.
- User-trained or uploaded person request: list custom people.
- Public people may require `figureType`; use the selected candidate's `figureType`.
- Prefer candidates matching the user's role and tone; if no guidance is given, choose a clear, youthful, presenter-like option with a preview and matching `audioManId`.
- Do not invent ids. Use ids returned by Chanjing or ids explicitly supplied by the user.

## Subtitle Rules

- Ask for `show` or `hide` before task creation unless the surrounding workflow already decided.
- Default to hidden only when operating through the current Studio route or when the user did not request platform subtitles and a non-interactive workflow must continue.
- If the user wants styled captions in the final FrameVideo composition, prefer hiding Chanjing platform subtitles and adding FrameVideo captions separately.

## Safety

- Never print access tokens, app secrets, or the contents of the credential store.
- Do not commit generated credentials or local API keys.
- Do not use render-time network fetches in compositions. Download the generated digital-human video first and reference the local asset.
- Avoid duplicating standalone `chanjing-video-compose` Python auth scripts in this repo; adapt through `ChanjingOpenApiClient` and the existing auth store.
