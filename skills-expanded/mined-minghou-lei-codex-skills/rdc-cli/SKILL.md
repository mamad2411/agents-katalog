---
name: "rdc-cli"
description: "Use when tasks involve RenderDoc capture files (.rdc), GPU frame analysis, draw call and pipeline inspection, shader debugging, render target export, or CI-style assertions over captures. Prefer this skill when the user mentions RenderDoc, rdc, .rdc files, draw calls, pixel history, shader replay, or GPU capture automation."
---

# rdc-cli Skill

## When to use
- Open or inspect RenderDoc capture files (`.rdc`).
- Capture a frame from a local Windows application with `rdc capture`.
- Analyze draw calls, events, render passes, resources, pipeline state, or bindings.
- Debug a pixel, vertex, or compute thread from a capture.
- Export textures, render targets, buffers, meshes, or thumbnails from a capture.
- Compare captures or run CI-style assertions such as `assert-pixel`, `assert-image`, `assert-count`, and `assert-state`.
- Use remote replay, split mode, or Android capture workflows.

## Preconditions
- Confirm `rdc doctor` passes before assuming local replay works.
- On Windows, prefer quoted `C:\...` paths in user-facing commands.
- If the task needs local replay, ensure the `renderdoc` Python module is available.
- If the task needs remote replay, confirm whether the target machine runs `rdc serve` or `renderdoccmd remoteserver`.

## Core workflow
1. Open or create a capture session.
   - Existing capture: `rdc open "C:\path\to\frame.rdc"`
   - Fresh capture: `rdc capture "C:\path\to\app.exe" -o "C:\Temp\frame.rdc" --auto-open`
2. Inspect frame shape.
   - Start with `rdc info`, `rdc stats`, `rdc passes`, `rdc events --limit 100`
3. Narrow to an event or pass.
   - Use `rdc goto EID`, `rdc pipeline EID`, `rdc bindings EID`, `rdc usage RESOURCE_ID`
4. Debug exact output.
   - Use `rdc pick-pixel X Y`, `rdc pixel X Y`, or `rdc debug pixel X Y`
5. Export evidence.
   - Use `rdc rt EID -o out.png`, `rdc texture EID -o tex.png`, `rdc log`, `rdc snapshot`
6. Close the session when done.
   - `rdc close`

## Output modes
- Default TSV is best for human reading and shell pipelines.
- Use `--json` when the user wants structured output, automation, or downstream parsing.
- Use `-q` or `--no-header` when extracting identifiers for follow-up commands.

## High-value commands
- Session: `open`, `capture`, `status`, `goto`, `close`
- Inspection: `info`, `stats`, `passes`, `pass`, `events`, `draws`, `resources`, `usage`
- Pipeline: `pipeline`, `bindings`, `shader`, `shaders`, `search`
- Pixel and debug: `pick-pixel`, `pixel`, `debug`
- Export: `rt`, `texture`, `buffer`, `mesh`, `thumbnail`, `snapshot`, `log`
- Assertions: `assert-clean`, `assert-count`, `assert-pixel`, `assert-state`, `assert-image`
- Remote: `serve`, `remote connect`, `remote list`, `remote capture`, `open --proxy`, `open --connect`

## Windows command style
- Existing capture:
  - `rdc open "C:\Temp\frame.rdc"`
- Local frame capture:
  - `rdc capture "C:\Games\MyApp.exe" -o "C:\Temp\frame.rdc" --frame 100 --auto-open`
- Query events as JSON:
  - `rdc events --json`
- Export current render target:
  - `rdc rt 12345 -o "C:\Temp\rt.png"`

## Remote and split mode
- Replay host:
  - `rdc serve --port 54321`
- Analyst machine:
  - `rdc remote connect "HOST:54321"`
  - `rdc open "C:\Temp\frame.rdc" --proxy HOST:54321`
- Thin client mode:
  - Server: `rdc open "C:\Temp\frame.rdc" --listen 0.0.0.0:54321`
  - Client: `rdc open --connect HOST:54321 --token TOKEN`

## References
- For high-frequency commands and examples, read [references/quick-ref.md](references/quick-ref.md).
- For the full CLI surface, prefer `rdc --help` and `rdc <command> --help`.

