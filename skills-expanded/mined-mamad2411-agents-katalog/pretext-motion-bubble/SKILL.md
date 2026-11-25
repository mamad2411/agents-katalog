---
name: pretext-motion-bubble
description: Use when generating or refining a standalone preview page that shows Pretext-driven animated text reflow around a moving video subject inside a chat-style bubble, especially when the effect should be easy to run and share locally.
---

# Pretext Motion Bubble

This skill is for standalone preview demos where text must re-layout around an animated subject, instead of being converted into ASCII art or injected into a live app. Favor a focused preview shell that foregrounds the moving subject and the live text reflow itself.

## When to Use

- The user wants a moving person, clip, or silhouette to push paragraph text around in real time.
- The user wants the output presented like a model response bubble, but as a standalone preview page.
- The user wants `@chenglou/pretext` used as the layout engine, especially `prepareWithSegments()` and `layoutNextLine()`.
- The user wants something that can be launched locally and shared without adapting a target app first.

## First Pass Workflow

1. Put demo-wide knobs in [`src/core/demoConfig.ts`](src/core/demoConfig.ts).
2. Compute blocked horizontal intervals per line band with [`src/core/textFlow.ts`](src/core/textFlow.ts).
3. Extract a per-frame subject mask with [`src/core/videoMask.ts`](src/core/videoMask.ts).
4. Feed each remaining slot into `layoutNextLine()` from [`src/app.ts`](src/app.ts).
5. Render the positioned lines inside a focused preview shell and start the local preview server.

## Extension Rules

- Do not switch to video-to-ASCII unless the user explicitly wants character art.
- Prefer using the actual video subject as the obstacle if the user names a real person, meme, or clip.
- If a user wants richer shapes later, keep the same contract: every frame should resolve to blocked horizontal intervals per line.
- Preserve the chat-bubble presentation unless the user asks for a full-screen editorial layout instead.
- Prefer removing explanatory chrome over adding more panels when the effect itself is the main point of the page.
- Treat real app integration as a separate future adapter layer, not part of the default preview workflow.

## Local Run

```bash
npm install
npm run dev
```

Then open the local URL printed by Vite.

For LAN preview:

```bash
npm run dev:lan
```
