---
name: create-game-plan
description: Creates a complete game development plan from an existing game story. Use when the user has a game story document and wants to turn it into a technical implementation plan covering architecture, milestones, asset lists, engine configuration, and task breakdown.
---

# Create Game Plan

Transform a game story into an actionable development plan. This skill reads the game story document (from `/create-game-story` or user-provided) and produces a full technical blueprint.

## Prerequisites

Before starting, gather:

1. **Game story document** — Ask the user for the path, or check `docs/game-story.md` in the current project
2. **Team size** — Solo dev, small team (2-5), or larger team?
3. **Target platforms** — Web (browser), Desktop (Electron), Mobile (PWA/Capacitor), or multiple?
4. **Timeline** — Game jam (48h-1week), prototype (1-4 weeks), full project (1-6 months)?
5. **Skill level** — Beginner, intermediate, advanced?

## Process

### Phase 1: Engine & Tech Stack Selection

Based on the story's requirements (3D/2D, complexity, multiplayer), recommend:

1. **Engine** — Use the `3d-game-design` skill's decision tree:
   - 3D complex → Three.js or R3F
   - 3D with heavy UI → Babylon.js
   - 2D platformer/RPG → Phaser 3
   - 2D casual/UI → PixiJS
   - Present the recommendation with reasoning

2. **Tech stack** — Recommend specific packages:
   - Rendering: engine + helpers (drei, etc.)
   - Physics: Rapier / Cannon / none
   - State management: Zustand / custom ECS
   - Audio: Howler.js / Web Audio API
   - Networking: Socket.io / Colyseus / none
   - UI: HTML overlay / React / Phaser UI scenes
   - Build: Vite + TypeScript

3. **Architecture pattern** — Based on game complexity:
   - Simple: Scene-based (Phaser scenes or Three.js scene swapping)
   - Medium: Component pattern with game loop
   - Complex: Full ECS with event bus

Present the stack as a table and ask for approval before proceeding.

### Phase 2: Feature Breakdown

Parse the story document and extract every feature needed:

**Core Systems** (must have for MVP):
- [ ] Player controller (movement, actions)
- [ ] Camera system (type based on game)
- [ ] Core game loop
- [ ] Scene/level loading
- [ ] Basic UI (HUD, menus)

**Story-Driven Features** (from the narrative):
- Extract from quests: combat, dialogue, inventory, crafting, etc.
- Extract from world: terrain, weather, day/night, procedural elements
- Extract from characters: AI behaviors, pathfinding, dialogue trees

**Polish Features** (nice to have):
- Particles, post-processing
- Sound design, music
- Save/load system
- Settings menu
- Achievements

Present as a categorized checklist. Let the user mark what's in scope for MVP vs later.

### Phase 3: Asset List

From the story, generate a complete asset manifest:

```markdown
## Asset List

### 3D Models / 2D Sprites
| Asset | Type | Priority | Notes |
|-------|------|----------|-------|
| Player character | 3D model / spritesheet | P0 | Needs animations: idle, walk, run, attack |
| [Environment] | Tilemap / 3D scene | P0 | Based on [setting] |
| [Enemy types] | Model / sprite | P1 | From story antagonist + minions |
| [NPCs] | Model / sprite | P1 | [Supporting cast names] |
| [Items/Props] | Model / sprite | P2 | [Key objects from story] |

### Audio
| Asset | Type | Priority |
|-------|------|----------|
| Background music | Loop per scene | P1 |
| SFX: footsteps, attacks, UI | One-shot | P1 |
| Ambient: environment | Loop | P2 |
| Dialogue VO | Per character | P3 |

### UI Assets
| Asset | Type | Priority |
|-------|------|----------|
| HUD elements | PNG/SVG | P0 |
| Menu screens | Layout | P0 |
| Font | TTF/WOFF2 | P0 |
| Icons | Spritesheet | P1 |

### Textures & Materials
| Asset | Type | Size | Priority |
|-------|------|------|----------|
| [Per environment] | Diffuse+Normal+ORM | 1024x1024 | P0 |
| Skybox / Environment map | HDR / Cubemap | 2048 | P1 |
```

Provide polygon/texture budget recommendations based on target platform (load `3d-game-design/references/asset_optimization_guide.md`).

### Phase 4: Milestone Plan

Break the project into milestones with deliverables:

```markdown
## Milestones

### M0: Project Setup (Day 1-2)
- [ ] Scaffold project: `python scripts/scaffold_project.py <engine> <name> --features <list>`
- [ ] Configure Vite, TypeScript, linting
- [ ] Set up version control
- [ ] Create folder structure for assets

### M1: Core Prototype (Week 1-2)
- [ ] Player movement + camera
- [ ] Basic level/scene with placeholder art
- [ ] Core game mechanic working (combat/puzzle/etc.)
- [ ] Basic collision / physics
- **Deliverable:** Playable gray-box prototype

### M2: Content Pipeline (Week 2-3)
- [ ] Asset pipeline setup (Draco, KTX2 compression)
- [ ] Import first real assets (character, environment)
- [ ] Implement scene transitions
- [ ] Basic UI (main menu, HUD)
- **Deliverable:** One complete level with real art

### M3: Story Implementation (Week 3-5)
- [ ] Quest/mission system
- [ ] Dialogue system (if applicable)
- [ ] All main quest content
- [ ] NPC interactions
- [ ] Save/load system
- **Deliverable:** Full main story playable

### M4: Polish & Audio (Week 5-6)
- [ ] Post-processing effects
- [ ] Sound effects + music
- [ ] Particle effects
- [ ] Animations refinement
- [ ] Bug fixing
- **Deliverable:** Near-final quality

### M5: Deploy (Week 6-7)
- [ ] Performance optimization (bundle analysis, LODs)
- [ ] Build for target platform(s)
- [ ] Package: `python scripts/build_deploy.py package-itch .`
- [ ] Testing on target devices
- [ ] Publish
- **Deliverable:** Released game
```

Adjust timeline based on user's stated timeframe. For game jams, compress to hours.

### Phase 5: File Structure

Generate the recommended project structure:

```
<game-name>/
├── docs/
│   ├── game-story.md          # From /create-game-story
│   └── game-plan.md           # This document
├── src/
│   ├── main.ts                # Entry point
│   ├── game/
│   │   ├── Game.ts            # Main game class / loop
│   │   ├── scenes/            # Level / scene files
│   │   ├── entities/          # Player, enemies, NPCs
│   │   ├── systems/           # Physics, input, AI, audio
│   │   ├── components/        # ECS components (if applicable)
│   │   └── ui/                # HUD, menus, dialogue
│   ├── assets/
│   │   ├── models/            # GLB/GLTF files
│   │   ├── textures/          # Images, KTX2
│   │   ├── audio/             # MP3/OGG
│   │   ├── sprites/           # Spritesheets
│   │   └── fonts/             # Typography
│   └── utils/                 # Helpers, constants, types
├── public/                    # Static files
├── package.json
├── tsconfig.json
└── vite.config.ts
```

Adapt based on engine choice (e.g., R3F uses React component structure).

### Phase 6: Output Document

Compile into a structured plan and save:

```markdown
# [Game Title] — Development Plan

## Tech Stack
## Feature Scope (MVP)
## Asset Manifest
## Milestones & Timeline
## Project Structure
## Risk Assessment
## Next Steps
```

Save to `<project>/docs/game-plan.md`.

## Rules

- **Read the story first.** Always load and reference the game story document before generating the plan.
- **Be realistic.** Scale recommendations to the user's team size and timeline.
- **Prioritize ruthlessly.** Everything gets P0 (MVP), P1 (important), P2 (nice), or P3 (stretch).
- **Use the 3d-game-design ecosystem.** Reference scripts, templates, configs, and reference docs from the master skill.
- **Ask before assuming.** Confirm engine choice, scope, and timeline before generating milestones.
- If the story doesn't exist yet, suggest running `/create-game-story` first.
