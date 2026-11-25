---
name: softgirlnocode-ai-video
description: AI video editing workflow using Codex (AI agent), HyperFrames (code-to-video library), and ElevenLabs (speech transcription). Four techniques — Reference, Context, Catalog, Tools — for directing Codex to produce precisely styled video edits without manual timeline work. Source: @softgirlnocode on TikTok.
---

## What this skill covers

A four-part framework for AI-assisted video editing using Codex as the agent, HyperFrames as the motion graphics library, and ElevenLabs for caption timing. Each technique is a specific way to give Codex the information it needs to produce the edit you want.

---

## The Tool Stack

| Tool | Role |
|------|------|
| **HyperFrames** | Turns code into video edits and motion graphics. Library of ready-made animations, captions, and effects. Install: `npx skills add heygen-com/hyperframes --full-depth` |
| **Codex** | The AI agent that builds the edit. Preferred for strong results + token efficiency |
| **ElevenLabs** | Transcribes speech for precisely timed captions |

---

## Technique 1 — Reference

**Give AI the look you want.**

Drop a screenshot into your project folder. Tell Codex which visual details to carry into the edit.

**Example prompt:**
```
Use this reference for translucent panels, pastel colors, and rounded corners.
```

**How:**
1. Screenshot any UI, video, or design that has the style you want
2. Save it to your project folder (e.g. `reference/style.png`)
3. In your Codex session, point to it and name the specific details

---

## Technique 2 — Context

**Give AI your operating system.**

Keep past projects, reusable assets, and editing rules in one place (your AIOS — AI Operating System) so Codex can find clips and follow your style across sessions.

**AIOS folder structure:**
```
projects/
  past-project-1/
  past-project-2/
assets/          ← reusable clips, B-roll, sound FX
style-rules.md   ← your editing preferences and rules
```

**Example prompt:**
```
Find past clips that show what I'm explaining.
```

Codex searches your AIOS for relevant clips from past projects automatically.

---

## Technique 3 — Catalog

**Let AI choose from the library.**

HyperFrames has ready-made animations, captions, and effects. Ask Codex to pick what fits the video from the catalog.

**Example prompt:**
```
Choose at least 4 relevant catalog assets and apply them where they support the story.
```

**Available catalog assets (examples):**
- Camera Follow Captions — one sentence written across a frame, camera pulls back
- Blend Difference — auto-inverting text using mix-blend-mode: difference
- Char Slam Explode — headline glyphs scatter then reassemble with slam and shake
- Parallax Layers — behind-subject 3D text layering with vertical stretch effect

---

## Technique 4 — Tools

**My AI video-editing stack.**

- **HyperFrames**: Turns code into video edits and motion graphics
- **Codex**: The AI agent building the edit. Pick for strong results + token efficiency
- **ElevenLabs**: Transcribes speech for precisely timed captions

**Install HyperFrames:**
```bash
npx skills add heygen-com/hyperframes --full-depth
```

---

## Full workflow

```
1. Gather reference screenshots → drop in /reference folder
2. Set up AIOS (projects/ + assets/ + style-rules.md)
3. Open Codex session
4. Prompt with reference: "Use this reference for [specific style details]"
5. Prompt with context: "Find past clips that show what I'm explaining"
6. Prompt with catalog: "Choose at least 4 HyperFrames catalog assets and apply them where they support the story"
7. Use ElevenLabs transcript for caption timing
8. Review output, iterate with targeted prompts
```

---

## Related

- HyperFrames docs: linked from heygen-com/hyperframes
- @softgirlnocode on TikTok — "How I edit Videos with AI" carousel
