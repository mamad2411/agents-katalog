---
name: visual-brief-generator
description: "Turns content into a structured image or video generation brief: shot list, per-scene AI image/video prompts, aspect ratio per platform, and a style and mood guide, and generates the asset if a visual-generation tool is connected. Use when the user asks for a visual brief, video brief, creative brief, shot list, storyboard, or image or video prompts."
allowed-tools: Read, Grep, Glob, Write
---

# Visual Brief Generator

## Purpose

Turn a piece of content or campaign idea into a structured, copy-paste-ready
visual generation brief — a shot list, per-scene prompts, aspect ratios per
platform, and a style/mood guide. If a connected image- or video-generation
MCP tool is available in the current session and the user wants to generate
now, use it. Otherwise the written brief itself is the deliverable.

**Important:** Higgsfield launched an official hosted MCP server in 2026
(Runway and Midjourney still have no known official one as of this
writing), so it's no longer accurate to assume none of the major
image/video-gen tools has one — but having an MCP server available in
general doesn't mean it's connected in any given session. This skill
checks whatever tools are actually available at runtime instead of
hardcoding a tool name, the same as it always has. For short-form vertical
video specifically (YouTube Shorts/Instagram Reels/TikTok), see the more
targeted `short-form-video` skill instead, which checks for the same
connectors and also produces platform-specific captions, hashtags, and
posting-time guidance this skill doesn't.

## Step-by-step process

**Plugin root:** if a path below still shows an unexpanded
`CLAUDE_PLUGIN_ROOT` placeholder (Claude Code fills it in; other agents
such as Codex don't), resolve it before using any of them: take the
output of `printenv CLAUDE_PLUGIN_ROOT` if it prints a path, otherwise
walk up from this file's folder to the first folder that contains
`references/brand-voice.md`, and if neither works, ask the user where
this plugin lives. Use that absolute path in every file path and shell
command below.

1. **Check onboarding status.** Read
   `${CLAUDE_PLUGIN_ROOT}/references/brand-voice.md`. If it doesn't exist,
   or its first line is `<!-- MARKETING-SKILL:UNCONFIGURED -->`, pause and
   ask the user this plugin's 4 setup questions (priority task; content
   types to produce; target audience + tone; default output format — same
   as `/marketing-skill:marketing-setup`) before continuing, then save the
   answers into that file and flip the marker to `CONFIGURED` with today's
   date. Otherwise, read it for mood/tone consistency below.

2. **Confirm scope.**
   - Source content or campaign this brief is for. If the user references
     a project feature/launch without describing it, look for it first —
     Glob for `README*`, `CHANGELOG*`, and `docs/**/*.md` at the project
     root, then Read whichever look relevant — before asking them to
     describe it. Only check documentation-oriented files this way, not
     arbitrary source code. If nothing relevant turns up, ask directly.
   - Deliverable type: video, image, or both.
   - Target platform(s) — this determines aspect ratio (e.g. Reels/TikTok
     9:16, LinkedIn 1:1 or 16:9, YouTube 16:9).
   - Roughly how many scenes/shots, and total duration if video.
   - Any existing brand assets, colors, or style references to match.

3. **Look for a connected visual-generation tool.** Check the tools
   actually available in this session for one whose name or description
   indicates image or video generation (for example, a connected Canva
   connector, or any other connected MCP server for this purpose — do not
   assume any specific one is present).
   - If found: ask the user whether to actually generate the asset(s) now
     using that tool, with the per-scene prompts below as input.
   - If not found: proceed to produce the written brief only.

4. **Draft the brief** using the exact section structure below, applying
   brand voice/tone from `references/brand-voice.md`.

5. **Report status honestly.** Never claim an asset was generated if no
   tool call actually happened. If no visual-gen tool is connected, say so
   plainly and point to this plugin's README section on connecting one.

## When to use this skill

Trigger on requests like:
- "Make a visual brief / video brief for..."
- "I need a shot list for..."
- "Write image/video prompts for..."

## Output structure (required)

Use this exact section order, as Markdown `##` headings:

### Brief Overview
Goal, source reference, target platform(s), total duration or frame count.

### Shot List
A table: `Shot # | Description | Duration/Frames | Camera/Framing notes`.

### Per-Scene Prompts
One block per shot. Each prompt must be self-contained (no dangling
pronouns like "it" referring to a previous scene) and include:
- The generation prompt itself.
- A negative prompt, if relevant to the target tool.
- Aspect ratio for that shot.
- Style/mood keywords.

### Aspect Ratio & Format per Platform
A table: `Platform | Aspect Ratio | File Type`.

### Style & Mood Guide
Color palette, tone, pacing, and sound/music direction (if video).

### Generation Status / Next Steps
State plainly whether a connected tool was used to actually generate
anything. If not, note how to connect a visual-gen MCP tool (see this
plugin's README) or how to paste these prompts into a tool manually.

## Formatting rules

- Keep style/mood keywords consistent across scenes unless variation is
  intentional and called out.
- Respect brand-voice constraints (including any banned words/imagery).
- Never fabricate an asset URL or claim generation succeeded when it
  didn't.

## Example output

> Fictional example: a 3-scene, 15-second product-teaser brief for
> Instagram Reels, brief-only (no visual-gen tool connected).

```markdown
## Brief Overview
Goal: teaser for the "one-click export" feature launch.
Source: content-repurposer LinkedIn post draft.
Platform: Instagram Reels.
Total duration: 15 seconds (3 scenes, 5s each).

## Shot List
| Shot # | Description | Duration | Camera/Framing notes |
|---|---|---|---|
| 1 | Cluttered desktop, multiple export windows open, looking chaotic | 5s | Close-up, slight overhead angle |
| 2 | Cursor clicks a single "Export" button | 5s | Screen-capture style, centered on the button |
| 3 | Clean report appears instantly, checkmark animation | 5s | Full-screen, centered |

## Per-Scene Prompts
**Scene 1:** "A cluttered computer desktop with five overlapping export
dialog boxes, warm office lighting, slightly messy and stressful mood,
overhead close-up angle." Negative prompt: "no readable text, no logos."
Aspect ratio: 9:16. Style/mood: chaotic, warm-toned, slightly comedic.

**Scene 2:** "A cursor clicks a single glowing 'Export' button on a clean
software interface, satisfying tactile motion, centered framing." Negative
prompt: "no readable brand names." Aspect ratio: 9:16. Style/mood: crisp,
minimal, satisfying.

**Scene 3:** "A finished report appears on screen with a green checkmark
animation, bright and clean, full-screen." Negative prompt: "no clutter."
Aspect ratio: 9:16. Style/mood: bright, resolved, confident.

## Aspect Ratio & Format per Platform
| Platform | Aspect Ratio | File Type |
|---|---|---|
| Instagram Reels | 9:16 | MP4 |

## Style & Mood Guide
Color: cool blues and whites, one warm accent in scene 1 for contrast.
Tone: light, a little playful, resolves into confident/clean. Pacing:
quick cuts, no scene longer than 5s. Sound: upbeat, minimal, a single
"ding" sound cue on scene 3's checkmark.

## Generation Status / Next Steps
No connected image/video-generation tool was available in this session, so
no asset was generated — this brief is the deliverable. To generate
directly, connect a visual-gen MCP tool and re-run this skill (see this
plugin's README), or paste the per-scene prompts above into your tool of
choice.
```
