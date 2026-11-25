---
name: kanvis-studio
description: Open or resume the full project-local Kanvis Studio video workbench in the Codex in-app browser, inspect its status, and apply structured video editing operations. Use whenever the user asks to open the workbench, editing workbench, video workbench, editing project, or says “打开工作台”“打开剪辑工作台”“打开剪辑项目”“用剪辑工作台打开”, and when scenes, text, captions, assets, timing, transforms, or rendered outputs need visual inspection or adjustment.
---

# Kanvis Studio

Use the Kanvis Studio interface and its internal VisualHyper MCP contracts instead of editing generated composition HTML directly. VisualHyper is an implementation detail; the public product name is Kanvis Studio.

## Choose the launch mode

- **Automatic handoff**: when Kanvis Video finishes and the current project already contains `visualhyper.artifact.json`, open that project without replacing its editable artifact.
- **Direct open**: resolve the user's requested project directory, or the most recent Kanvis project when the user does not provide one, then open it in Studio.
- **Flat output handoff**: when only an MP4 exists, register it as a flat video output. State clearly that already composited layers cannot be reconstructed.

## Open inside Codex

1. Resolve the requested video project as an absolute `projectDir`. For an existing-project request, verify that it contains `visualhyper.project.json` or `visualhyper.artifact.json`; do not create a placeholder project in the current workspace merely to open Studio.
2. Call `open_visualhyper_web_panel` with that directory and read the returned loopback URL.
3. Use the Codex in-app Browser (`control-in-app-browser`) to open that URL and make the browser visible. Do not use external Chrome unless the user explicitly requests it.
4. Confirm that the top-level “视频工作台” view is active. If the page opens on “创作中心”, switch to “视频工作台” before handing control to the user.
5. Keep the workbench tab as a deliverable tab and report the resolved project file.

## Work with a project

- Call `create_visualhyper_project` only when no project exists or the user explicitly wants a new project.
- Call `get_visualhyper_project` before proposing edits that depend on current scene or selection state.
- Use `apply_visualhyper_operations` for changes. Include the current `baseRevision`; on a revision conflict, reload and rebase instead of overwriting newer work.
- Use `list_visualhyper_assets` to discover media. Never invent asset paths.
- The embedded UI calls these same tools through the Codex MCP host bridge. Keep `visualhyper.project.json` as the shared source of truth.

## Boundaries for this version

- This version provides the local project shell, declared artifact editor, rendered-output playback, and Codex integration. Do not claim that a flat MP4 recovers original layers or that Jianying/CapCut project export is already complete.
- Keep HyperFrames HTML as generated output. The editable source of truth is `visualhyper.project.json`.
- Do not transmit large local media as Base64 through MCP.
