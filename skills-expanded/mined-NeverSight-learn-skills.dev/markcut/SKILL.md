---
name: markcut
description: use markdown to describe stream trees, provide CLI to render stream trees to video via `npx @lalalic/markcut`. use it to structure video scenes, and generate TTS, TTI, TTV, STT media automatically.
---

## Stream Tree Specs

Everything video is a **stream tree** described with markdown. see [docs/markdown-descriptive.md](docs/markdown-descriptive.md) for full details.


## Video Design Utilities

### Vision — understand video and images
- `npx @lalalic/markcut vision <folder>` provides tool to understand video and images in a folder, and generate a `metadata.json` file with with text description, duration, and other metadata for each media file.
- `npx @lalalic/markcut vision <folder> --label`, interactive mode, provides tool to label video and images with text, and above metadata.

### Storyboard — plan video structure with scene nodes

- Use `scene` nodes to organize your video. Scenes can nest inside other scenes.
- Use `description`, `scene.instruction`, `script`, `image|video.prompt` to structure your video content.

see [docs/markdown-descriptive.md](docs/markdown-descriptive.md) for full details.

### `--storyboard` — fast structure preview
```bash
npx @lalalic/markcut preview video.md --storyboard
```

Skips slow TTI/TTV/STT generation and renders a fast preview where:
- `image`/`video` nodes with `prompt` but no `src` → `<StoryboardSlot>` placeholder showing the prompt text
- `audio`/`script` nodes → `<StoryboardCaption>` overlays showing narration text
- A `<StoryboardInfo>` card with root metadata (title, dimensions, fps) appears at the first frame

Implies `--edit` so you can chat to reshape the story and see live reloads.

### Video Variants
- define variants for different video configurations, such as different languages, aspects, platforms

### Viral Story requires
- **Hooks** : why should the viewer watch this?
- **Conflict** : what challenges or obstacles do the characters face?
- **Resolution** : how are the conflicts resolved?
- **Emotion** : what feelings are evoked in the viewer?
- **Call to action** : what should the viewer do next?
- **Open ending** : does the story leave room for interpretation or continuation?

### TTS, TTI, TTV, STT media generation
markcut implements a **media generation pipeline** to generate TTS, TTI, TTV, STT media automatically. 
- `npx @lalalic/markcut --show-clis` to see the default CLIs for TTS, TTI, TTV, STT media generation.
- `orchestrator` agent DONT generate media directly

## 3. CLI

```bash
npx @lalalic/markcut <command> [options]
npx @lalalic/markcut --help # get overall information
npx @lalalic/markcut --show-clis # get command specific information
npx @lalalic/markcut preview <file> # assemble and preview the video with a local server, and chat to edit the video and auto refresh
npx @lalalic/markcut preview <file> --storyboard # fast structure preview: replaces TTI/TTV prompts with placeholder components, skips slow generation
npx @lalalic/markcut render <file> # render the video to mp4
npx @lalalic/markcut vision <folder> # vision understanding medias in folder
npx @lalalic/markcut vision <folder> --label # an extra step to provide UI to label the medias with text, time ranges

```

---

## self verification
some common issues (photo or video can't be displayed, audio missing), take below actions to verify
### preview
- take screenshot for some key frames in player, and understand image to verify intent

### final video
- screenshot some key frames, and understand image to verify intent
- stt the final video audio, and verify if vtt result is correct


## Reference

| Topic | File |
|-------|------|
| Markdown descriptive format (primary authoring format) | [docs/markdown-descriptive.md](docs/markdown-descriptive.md) |
| Built-in components & common npm packages | [docs/components.md](docs/components.md) |
| Sound effects | [docs/sound-effects.md](docs/sound-effects.md) |



## Built-in Components

Built-in components available via `@lalalic/markcut/components`. See [docs/components.md](docs/components.md) for full reference.


## Golden rule
- always check stream start and duration to avoid
  - audio cut off
  - video cut off
  - subtitle mismatch
  - sync issues between audio, video, and subtitles
according to the content change. rm `.markcut` will cause all content to be regenerated, which is time consuming and wasteful.
- put all manual assets in `assets` folder, such as bgm, logo, watermark, etc. don't put them in `.markcut` folder, which is auto generated and will be deleted when `markcut clean` command is run.

### Don'ts
- **don't** set duration for script or stream's duration depending on audio script
  - markcut resolver will automatically calculate the duration based on the audio script length
- **don't** rm `.markcut` directory, which served as cache for all generated content. cache will auto update 
- **don't** set timeout for `preview`, `vision`, `render` markcut commands, which may take long time to generate medias.
- **don't** use skill to understand vision media. use `npx @lalalic/markcut vision <folder>`.