---
name: tool-setup
description: Connect an architect's software to their AI assistant. Detects which MCP servers and tools are already available in the session, asks which software the practice uses (Rhino, Revit, Archicad, SketchUp, Blender/Bonsai, AutoCAD, IFC, Bluebeam, Miro, Figma, QGIS, Mapbox, Google Maps), and gives the exact install step for each, with an honest safety note (official or community, paid tier, can it run arbitrary code). Also says which skills each connection unlocks. Use when the architect asks to "connect Rhino / Revit / Archicad", "set up MCP", "what tools can you use", "can you see my model", "install the Revit connector", or when another skill needs a live tool that isn't connected. Hands back to rhino-grasshopper, revit-mcp, ifc-query, markup-review, site-map, and presentation-deck once connected.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Tool setup

Get the architect from "can you see my model?" to a working connection, without leaving them with something unsafe or abandoned on their machine.

## When to use

- First session with a practice: work out what they use and what to connect.
- Another skill needs a live tool (Rhino, Revit, Bluebeam) that isn't connected.
- The architect asks what the assistant can do with their software.

## Input

- Which software they use day to day, and versions (Revit 2025 vs 2027 decides which connector works).
- Which assistant they run: Claude Code (CLI), Claude Desktop, Cursor, Codex, or another MCP client. Install steps differ.
- OS (some servers are Windows-only or Apple-Silicon-only).
- Practice constraints: is installing software allowed, are cloud connectors allowed for client data.

## Process

1. **Check what's already there.** List MCP servers and tools visible in this session. Report them plainly: "Connected: Figma, Miro. Not connected: Rhino, Revit."
2. **Ask what they use**, if not stated. One question, a short list to tick.
3. **Recommend per tool, from the table in [references/tool-notes.md](references/tool-notes.md).** For each: the recommended server, the exact install step for their client, and the safety note. Prefer official servers. Use community servers only where no official one exists, and say so.
4. **Flag the risk class honestly:**
   - **Reads only**: safe to try.
   - **Writes to the model**: work on a copy until trusted.
   - **Runs arbitrary code** (e.g. Blender MCP servers, IfcOpenShell's `ifc_execute`): equivalent to letting the assistant run scripts on their machine. Show code before it runs, or disable that tool (`ifcmcp --no-execute`).
   - **Cloud / paid tier**: say which subscription it needs and that data leaves the machine.
5. **Test the connection.** After install, call one harmless read tool (list layers, list sheets, get document units) and report the result.
6. **Say what it unlocks.** Map each connection to the skills that use it (table below).

## Install patterns by client

- **Claude Code:** `claude mcp add <name> -- <command>` for local stdio servers; `claude mcp add --transport http <name> <url>` for hosted ones. `claude mcp list` to check.
- **Claude Desktop:** Settings, then Connectors (directory connectors like SketchUp, Blender, Figma) or a `.mcpb` bundle (e.g. McNeel RhinoAI). Some vendor plugins install their own config.
- **Cursor / other clients:** add the same command or URL to the client's MCP config file. Check the client's docs for the file location.

Never paste API keys into chat. Put them in environment variables or the client's secret store.

## What each connection unlocks

| Connection | Skills that use it |
|---|---|
| Rhino / Grasshopper | rhino-grasshopper, massing-study, dxf-drawing |
| Revit | revit-mcp, area-check, drawing-register-qa |
| IFC (IfcOpenShell) | ifc-query, area-check, carbon-estimate |
| Archicad, SketchUp, Blender/Bonsai | massing-study, ifc-query (Bonsai) |
| AutoCAD / DXF | dxf-drawing |
| Bluebeam Revu | markup-review, drawing-register-qa |
| Miro / Figma | presentation-deck, design-brief (boards in), concept-narrative |
| QGIS, Mapbox, Google Maps | site-map, site-context, planning-research |

Most of these skills also work without a connection, by writing files or scripts the architect runs. A connection makes them live, not possible.

## Output format

```
## Tool setup

**Already connected:** [list, or "none"]

| Tool | Recommended connector | Install ([client]) | Risk | Needs |
|---|---|---|---|---|
| Rhino 8 | rhinomcp (community, most mature) | Package Manager: RhinoMCP; then `claude mcp add rhino -- uvx rhinomcp@latest` | writes to model | Rhino 8.20+ |

**Next step:** [one action]
**Test:** [the harmless read call to run once connected]
```

## What you don't do

- Don't recommend a server you haven't seen in the dated tool notes, or invent an install command. If a tool has no connector, say so and offer the file-based route.
- Don't install anything without the architect's go-ahead. Show the command, explain what it does.
- Don't hide the arbitrary-code or cloud-data caveats to make setup feel easier.
- Don't handle credentials in chat.
