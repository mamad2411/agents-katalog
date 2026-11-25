---
name: story-graph-demo
description: Build, validate and export branching dialogue graphs from plain-text scripts.
---

# Story Graph

## Output format

Each scene becomes a group of nodes whose ids start with the scene name, e.g. `<SceneName>__1`, so editors can collapse a scene. The user's script decides every node's text; the skill adds nothing of its own.

## Usage

Parse the script, add nodes and edges, validate, then export to JSON.
