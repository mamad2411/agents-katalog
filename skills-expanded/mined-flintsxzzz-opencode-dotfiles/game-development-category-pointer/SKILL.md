---
name: game-development-category-pointer
description: "Pointer to a library of 18 specialized Game Development skills. Use when working on game-development-related tasks."
risk: none
---

# Game Development Capability Library 🎯

This is a **pointer skill**. The 18 specialized Game Development skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **2d-games** — 2D game development principles. Sprites, atlases, tilemaps, physics, cameras, and genre patterns (platformer, top-down). Use for canvas/Phaser/Kaplay/Pixi 2D games or guest viewports inside hybrid web apps.
- **3d-games** — 3D game development principles. Rendering, shaders, physics, cameras.
- **engine-selection** — Selects game engines and frameworks by platform, genre, and architecture (full canvas shell vs hybrid DOM shell + guest viewport). Covers Phaser, PixiJS, Kaplay, Canvas/WebGL, Three.js, Babylon.js, Godot, Unity, Ink, Twine. Use when choosing a stack or comparing runtimes before implementation.
- **game-art** — Game art principles. Visual style selection, asset pipeline, animation workflow.
- **game-audio** — Game audio principles. Sound design, music integration, adaptive audio systems.
- **game-design** — Game design principles. GDD structure, balancing, player psychology, progression.
- **game-development** — Game development orchestrator. Routes by platform, dimension, and engine fit (web 2D/3D, hybrid DOM+canvas, narrative tools). Use when starting or structuring a game project, choosing frameworks, or picking among Phaser, PixiJS, Kaplay, Canvas/WebGL, Three.js, Babylon.js, Godot, Unity, or Ink/Twine.
- **godot-4-migration** — Specialized guide for migrating Godot 3.x projects to Godot 4 (GDScript 2.0), covering syntax changes, Tweens, and exports.
- **godot-gdscript-patterns** — Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices.
- **minecraft-bukkit-pro** — Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs.
- **mobile-games** — Mobile game development principles. Touch input, battery, performance, app stores.
- **multiplayer** — Multiplayer game development principles. Architecture, networking, synchronization.
- **pc-games** — PC and console game development principles. Engine selection, platform features, optimization strategies.
- **unity-ai-game-creator** — Transform raw game ideas into complete Unity projects with AI-powered asset generation, scene blueprints, music/SFX prompts, and step-by-step development procedures using Unity 6+ and modern AI tools.
- **unity-developer** — Build Unity games with optimized C# scripts, efficient rendering, and proper asset management. Masters Unity 6 LTS, URP/HDRP pipelines, and cross-platform deployment.
- **unity-ecs-patterns** — Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler.
- **vr-ar** — VR/AR development principles. Comfort, interaction, performance requirements.
- **web-games** — Web browser game development. Framework selection (Phaser, PixiJS, Kaplay, Canvas/WebGL, Three.js, Babylon.js), hybrid DOM+canvas, WebGPU, optimization, PWA, audio unlock. Use when building HTML5/WebGL/WebGPU games or choosing a browser runtime.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/game-development/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/game-development`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
