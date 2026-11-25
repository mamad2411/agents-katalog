---
name: agent-workflow-video
description: Build a Remotion video that turns an agent workflow or "day-in-the-life" pipeline narrative into a social-ready cut for X / LinkedIn / Reels / Shorts / TikTok. Dark terminal aesthetic, color-coded agent badges, tool-call transcripts, act-based pacing, dual vertical (9:16) + square (1:1) outputs from one codebase. Use whenever the user wants to turn an agent demo, multi-agent pipeline, workflow HTML page, internal walkthrough, or "watch what our system does" story into a shareable short — even if they don't say "Remotion" or "video." Triggers on phrases like "make a video for this workflow," "turn this HTML into a LinkedIn clip," "social cut for this agent demo," "visualize this pipeline as a reel," "render this story as a short," or any time the user has a story about agents, tools, and outcomes that would land better as motion than a static page.
---

# Agent Workflow Video

Turn an agent / workflow narrative into a polished, dual-format Remotion social cut.

## When this is the right tool

This skill is built for one specific kind of video: a **30–60 second narrative** about an agentic system doing work. Tool calls. Agents talking to agents. Results landing. Stats. A tagline.

Reach for it when the user gives you any of:

- An HTML walkthrough page (e.g. an internal "day in the life" or "how it works" page)
- A markdown spec / blog draft describing an agent pipeline
- A bulleted outline of "user asks → agent A does X → agent B does Y → outcome"
- A verbal description of a multi-agent demo

Skip it for: generic explainer videos, talking-head footage, marketing montages, anything that needs camera work or stock footage. This is a code-first, terminal-aesthetic, scene-driven cut.

## What you produce

A complete, runnable Remotion 4.x project with:

- **`DonjonVertical`** — 1080×1920 @ 30fps for X mobile, LinkedIn mobile, Reels, Shorts, TikTok
- **`DonjonSquare`** — 1080×1080 @ 30fps for LinkedIn desktop feed, X desktop, IG feed
- One narrative composition (`<ProjectName>Video.tsx`) used by both
- Reusable components: agent badges, terminal lines, act labels, mesh backdrop, progress bar
- README with install / preview / render commands
- `.gitignore` and Remotion config

Default runtime is **50s (1500 frames)**. Adjust `TOTAL_FRAMES` in `theme.ts` if the user wants 30s or 60s.

## Workflow

### 1. Read the source narrative

If the user pointed at an HTML file, a markdown doc, a Notion page, or anything else, **read it in full first**. Don't skim. The whole point of this skill is content-faithful — if you miss a tool call or an agent name from the source, the output won't match the user's expectations.

For HTML walkthroughs especially, look for:

- **Agents / actors** — names, colors if shown, roles
- **Tool calls** — what each agent invokes (web_search, http_get, execute_python, deploy commands, etc.)
- **Results / artifacts** — what comes out (URLs, files, stats)
- **Act structure** — receive → plan → dispatch → execute → report
- **Stats / numbers** — agents involved, tool calls made, runtime, lines of code, etc.
- **Closing tagline** — the punchy one-liner the page ends on

### 2. Decompose into scenes

Use the standard arc (see `references/scene-patterns.md` for full templates):

| # | Scene | Duration | Purpose |
|---|-------|----------|---------|
| 1 | Intro | 3s | Title reveal + hook |
| 2 | Mission | 3s | The user's ask, in plain text |
| 3 | Receive | 4s | Top-level agent loads context / memory |
| 4 | Plan | 4s | Top-level agent creates tasks |
| 5 | Dispatch | 4s | Tasks routed to specialized agents |
| 6–9 | Execute (×N) | 3s each | One scene per specialized agent + their tool calls |
| 10 | Results | 3s | Aggregated artifacts |
| 11 | Council | 3s | Reflection / meta layer (skip if not in source) |
| 12 | Stats | 6s | Numbers reveal |
| 13 | Outro | 8s | Tagline + brand mark |

Total ≈ 50s. Trim Council or shorten Stats for 30s. Add a second Mission beat or a longer Outro for 60s.

### 3. Scaffold the project

Copy `assets/project-scaffold/` into the user's chosen output folder. Rename:

- `project-scaffold/` → user's chosen folder name (e.g. `donjon-remotion-video`)
- `package.json` `name` field → kebab-case version of the project
- The two composition `id`s in `Root.tsx` if the brand/project name should differ

Everything in `src/components/` and `src/theme.ts` is reusable as-is. The only file you write per-project is `src/<ProjectName>Video.tsx` (the narrative composition).

### 4. Tune the theme

Open `src/theme.ts` and adjust:

- **`COLORS`** — palette derived from the source. If the source HTML uses `#a855f7` for purple, mirror it.
- **`AGENT_COLORS`** — one color per agent. Keep them distinct enough to read in motion.
- **`AgentKey`** type — union of all agent identifiers in the source.
- **`TOTAL_FRAMES`** — adjust if not 50s.

### 5. Write the narrative composition

Create `src/<ProjectName>Video.tsx`. Structure it as:

```tsx
import { AbsoluteFill, Sequence } from "remotion";
import { MeshBackdrop } from "./components/MeshBackdrop";
import { ProgressBar } from "./components/ProgressBar";
import { COLORS, FONT_MONO, TOTAL_FRAMES } from "./theme";

export const ProjectVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: COLORS.bg, fontFamily: FONT_MONO }}>
    <MeshBackdrop />
    <ProgressBar totalFrames={TOTAL_FRAMES} />

    <Sequence from={0} durationInFrames={90}><Intro /></Sequence>
    <Sequence from={90} durationInFrames={90}><Mission /></Sequence>
    {/* ...one Sequence per scene... */}
  </AbsoluteFill>
);

// Then define each scene component inline below.
```

Inline scene components keeps the narrative readable as one file. See `references/scene-patterns.md` for ready-to-paste scene templates (Intro, Mission, AgentTurn, Gremlin, Stats, Outro).

For each agent execution scene, prefer the reusable `Gremlin` pattern (one component, props for agent name + tool calls + result) over copy-pasting per-agent JSX. Saves ~200 lines on a 4-agent demo.

### 6. Update the README

The scaffold ships a generic README. Update:

- The scene breakdown table (use your actual frame ranges)
- Project name in the heading
- The "Customize the mission" snippet to match your hard-coded mission text

### 7. Deliver

Hand the user the absolute path and the three commands they need:

```sh
cd <project-folder>
npm install
npm run dev      # Remotion Studio at localhost:3000 for scrubbing
npm run render   # Vertical MP4 → out/<name>-vertical.mp4
```

## Style invariants — what keeps it on-brand

These are what make the output look like the rest of the family of cuts. Keep them unless the user explicitly asks for a different aesthetic:

- **Dark backdrop** (`#0a0e1a` or similar) with slow-drifting radial gradients via `MeshBackdrop`
- **Monospace everywhere** — `'SF Mono', 'Menlo', 'Monaco', 'Cascadia Code', 'Fira Code', 'Consolas'`
- **Agents are color-coded pills** via `AgentBadge`, never just text
- **Tool calls are typed-in terminal lines** via `TerminalLine` with `›` (tool), `✓` (result), `▸` (dispatch) prefixes
- **Each act starts with a small uppercase `ActLabel`** — gives the viewer a beat to orient
- **Spring-physics entrances** for badges (damping 10–16, stiffness 80–120)
- **Blur-reveal for title text** in the Intro
- **Shimmer-sweep on the closing tagline** in the Outro

## Custom palettes

If the user has brand colors that aren't the default Donjon palette, ask once or infer from the source:

- 1 background (very dark, near-black)
- 1 muted text (mid-gray)
- 1 highlight (white-ish for primary text)
- 5–7 distinct agent colors (purple, green, amber, red, cyan, pink work as a starting set)
- 1 success green and 1 alert red for terminal results

Update `theme.ts` `COLORS` and `AGENT_COLORS` only — components consume the theme, so nothing else needs to change.

## Reference files

Read these when you need detail:

- **`references/scene-patterns.md`** — Ready-to-paste JSX templates for every standard scene (Intro, Mission, Receive, Plan, Dispatch, Gremlin, Results, Council, Stats, Outro). Read this whenever you're writing the narrative composition.
- **`references/component-library.md`** — Full API for `AgentBadge`, `TerminalLine`, `ActLabel`, `MeshBackdrop`, `ProgressBar`. Read this if you need to add a new component or extend an existing one.
- **`references/publishing-notes.md`** — Per-platform sizing, runtime caps, caption strategy, and thumbnail tips for X, LinkedIn, Instagram, TikTok. Read this when the user asks about distribution.

## Common pitfalls

- **Don't use `staticFile()` for fonts.** The scaffold sticks to system monospace stacks so the project runs without bundling assets. Only add `staticFile` if the user wants a custom font and is OK creating `public/`.
- **Don't add audio by default.** Music is highly opinionated. Offer it as a follow-up; don't assume.
- **Don't break the dual format.** Both compositions render the same component — never write CSS that hard-codes 1080×1920. Use `useVideoConfig()` if you need width/height.
- **Don't over-explain in the video.** Viewers read 2–3 lines per scene max. Cut text aggressively if a scene feels dense.
- **Don't skip the Intro hook.** First 1.5 seconds determines whether someone scrolls past on mobile.

## When the user wants something different

If the user explicitly asks for:

- **A pure code demo video** → use the base Remotion skill instead, this one's overkill.
- **A talking-head or screen-recording-driven video** → Remotion can do it but this skill's templates won't help.
- **A different aesthetic (light mode, photo-real, etc.)** → fork the scaffold, but warn the user that the Donjon look-and-feel is what makes the cut feel coherent across posts.

Otherwise, ship it. The scaffold + scene patterns get a polished cut in well under an hour of model time.
