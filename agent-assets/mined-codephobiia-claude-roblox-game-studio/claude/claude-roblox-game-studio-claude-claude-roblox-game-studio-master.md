# FoG Roblox Studio Command — Roblox Game Studio Agent Architecture

Roblox game development managed through coordinated Claude Code subagents.
Each agent owns a specific domain within the Roblox ecosystem, enforcing
separation of concerns and quality.

## Technology Stack

- **Engine**: Roblox Studio
- **Language**: Luau
- **Runtime**: Roblox Engine (client-server architecture)
- **Version Control**: Git with trunk-based development (synced via Rojo/Argon)
- **Sync Tool**: Configured via /start (default: Rojo)
- **Data Layer**: DataStoreService + MemoryStoreService
- **Networking**: RemoteEvents, RemoteFunctions, UnreliableRemoteEvents
- **UI Framework**: Configured via /start (default: Native ScreenGui)

## Project Structure

@.claude/docs/directory-structure.md

## Roblox Architecture Guide

@.claude/docs/roblox-architecture-guide.md

## Luau Style Guide

@.claude/docs/luau-style-guide.md

## Technical Preferences

@.claude/docs/coding-standards.md

## Coordination Rules

@.claude/docs/coordination-rules.md

## Roblox/Luau Wiki (Persistent Knowledge Base)

This project maintains a persistent, LLM-curated wiki at `wiki/` following
[Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
It is the source of truth for deep Roblox/Luau knowledge — services, concepts,
Luau features, anti-patterns, exploits, performance, monetization, studio
workflows, and game patterns. Rules in `.claude/rules/` stay prescriptive;
the wiki provides the descriptive backing.

@wiki/SCHEMA.md

**Operations:**
- `/wiki-seed` — one-time bootstrap from existing repo content
- `/wiki-ingest <source>` — integrate a new raw source
- `/wiki-query <question>` — answer from the wiki
- `/wiki-lint` — health check
- `/wiki-update <page>` — targeted page edit

**Owner:** `wiki-curator` agent coordinates; domain specialists own their pages.
**Raw sources:** `wiki/raw/` (immutable, captured from external sources).

## Roblox Studio MCP (Live Testing)

The official Roblox Studio MCP server is connected. Use `studio-mcp-operator`
agent to execute Luau in Studio, capture screenshots, inspect instances, run
play tests, read console output, and generate meshes/materials via AI.
Skills: `/studio-test`, `/studio-inspect`, `/studio-screenshot`.

## Blender MCP (3D Asset Creation)

Blender MCP is connected for 3D asset generation. Use `blender-mcp-operator`
agent to create models from text/image prompts (Hyper3D, Hunyuan3D), download
from PolyHaven/Sketchfab, optimize for Roblox (10K tris, 1024 textures),
and export FBX. Skills: `/generate-asset`, `/asset-from-image`.

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question → Options → Decision → Draft → Approval**

- Agents MUST ask "May I write this to [filepath]?" before using Write/Edit tools
- Agents MUST show drafts or summaries before requesting approval
- Multi-file changes require explicit approval for the full changeset
- No commits without user instruction

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for full protocol and examples.

> **First session?** If the project has no game concept or existing code,
> run `/start` to begin the guided onboarding flow.

## Coding Standards

@.claude/docs/coding-standards.md

## Context Management

@.claude/docs/context-management.md
