---
name: houdini-20-5-python-scripting
description: "Houdini 20.5 Python scripting and HOM (Houdini Object Model) reference. Use automatically for any Houdini Python programming question, including writing plugins, shelf tools, Python SOPs/COPs, viewer states, handles, digital assets (HDA), HDAs, Solaris, dynamics, geometry processing, parameter scripting, rendering, VEX interop, importing the hou module, or looking up hou API classes, methods, functions, and examples."
---

# Houdini 20.5 Python Scripting

This skill covers the SideFX Houdini 20.5 Python scripting documentation (`hou` module / HOM).

## Core Frameworks & Mental Models

- **HOM is the Houdini Object Model**: Python API replacing the legacy HScript language.
- **The `hou` module is the root**: All classes, functions, and sub-modules live under `hou` (e.g., `hou.node()`, `hou.Geometry`, `hou.Parm`).
- **Python is available in multiple contexts**: parameter expressions, shelf tools, Python SOPs/COPs, hython, external Python sessions, and viewer states/handles.
- **Geometry access is context-sensitive**: Modify geometry only from inside a Python SOP; read from elsewhere.
- **hou license behavior**: Importing `hou` outside of hython checks out a Houdini license (batch or FX by default).

## Chapter Index

- `ch01-overview.md` — Overview: Python scripting overview and subtopics
- `ch02-getting-started.md` — Getting Started: HOM introduction
- `ch03-python-expressions.md` — Python Expressions: Writing parameter expressions in Python
- `ch04-script-locations.md` — Script Locations: Where Python scripts can live in Houdini
- `ch05-tool-scripts.md` — Tool Scripts: Writing Python scripts for shelf/asset tools
- `ch06-cookbook.md` — Cookbook: HOM cookbook examples
- `ch07-node-user-data.md` — Node User Data: Storing and retrieving data on nodes
- `ch08-python-sop.md` — Python SOP: Defining geometry nodes with Python
- `ch09-python-cop.md` — Python COP: Defining compositing nodes with Python
- `ch10-command-line-scripting.md` — Command-Line Scripting: Importing hou and hython usage
- `ch11-node-search.md` — Node Search: Programmatically finding nodes
- `ch12-browser-python.md` — Browser Python: Scripting Houdini from web pages
- `ch13-rpc.md` — RPC: Remote Houdini control via Python
- `ch14-python-viewer-states.md` — Python Viewer States: Custom viewer states in Python
- `ch15-python-viewer-handles.md` — Python Viewer Handles: Custom viewer handles in Python
- `ch16-hou-api-overview.md` — hou API Overview: Module/class/function index and navigation
- `ch17-api-animation.md` — Animation
- `ch18-api-apex.md` — apex
- `ch19-api-digital-assets.md` — Digital assets
- `ch20-api-channels.md` — Channels
- `ch21-api-cooking.md` — Cooking
- `ch22-api-crowds.md` — Crowds
- `ch23-api-dynamics.md` — Dynamics
- `ch24-api-exceptions.md` — Exceptions
- `ch25-api-file-io.md` — File I/O
- `ch26-api-general.md` — General
- `ch27-api-geometry.md` — Geometry
- `ch28-api-images.md` — Images
- `ch29-api-nodes.md` — Nodes
- `ch30-api-node-types.md` — Node types
- `ch31-api-objects.md` — Objects
- `ch32-api-organization.md` — Organization
- `ch33-api-parameters.md` — Parameters
- `ch34-api-parameter-templates.md` — Parameter templates
- `ch35-api-performance.md` — Performance
- `ch36-api-playbar.md` — Playbar
- `ch37-api-preferences.md` — Preferences
- `ch38-api-radial-menus.md` — Radial menus
- `ch39-api-rendering.md` — Rendering
- `ch40-api-scripting.md` — Scripting
- `ch41-api-shading.md` — Shading
- `ch42-api-shelf.md` — Shelf
- `ch43-api-solaris.md` — Solaris
- `ch44-api-takes.md` — Takes
- `ch45-api-ui.md` — UI
- `ch46-api-utility.md` — Utility
- `ch47-api-vex.md` — VEX
- `ch48-api-views.md` — Views
- `ch49-api-viewer.md` — viewer
- `ch50-api-webserver.md` — webServer
- `ch51-api-getting-started.md` — Getting started
- `ch52-api-next-steps.md` — Next steps
- `ch53-api-reference.md` — Reference
- `ch54-api-guru-level.md` — Guru level
- `ch55-api-python-viewer-states.md` — Python viewer states
- `ch56-api-python-viewer-handles.md` — Python viewer handles
- `ch57-api-plugin-types.md` — Plugin types

## How to Use This Skill

- Ask for a specific `hou` class, method, or function (e.g., "how does hou.Geometry.createPoint work?").
- Load a module chapter (e.g., `/houdini-20-5-python-scripting ch17-api-geometry`) to browse all geometry-related classes and functions.
- Use `cheatsheet.md` for common snippets and `glossary.md` for terms.

## Glossary / Quick Reference

See `glossary.md` for key terms and `cheatsheet.md` for common code snippets.