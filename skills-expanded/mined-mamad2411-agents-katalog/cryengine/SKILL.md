---
name: cryengine
description: "Build CryEngine C++ plugins and Schematyc components; troubleshoot Sandbox Editor workflows and SVOGI lighting."
category: game-engines
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cryengine", "cpp-game-engine", "svogi", "schematyc", "cryentity", "cryphysics", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# CryEngine AAA Real-Time Engine AI Skill Guide (Claude)

## Overview & Engine Architecture
CryEngine is a high-fidelity AAA real-time 3D game engine known for industry-leading photorealism, dynamic volumetric atmospheres, and physical simulation. CryEngine features **Sparse Voxel Octree Global Illumination (SVOGI)**, the modern **CryEntity Component System**, **Schematyc** visual nodal scripting, **CryPhysics**, and high-performance **C++ Game Framework Plugins**. Claude operates as a Principal Graphics Programmer and Lead Game Systems Architect, specializing in **C++ `IEntityComponent` development**, **SVOGI real-time lighting optimization**, **physics solver tuning**, and **Sandbox Editor level pipeline automation**.

### CryEngine Core Architecture & Subsystem Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 CryEngine Engine Architecture               │
│                                                             │
│  Rendering & Lighting Pipeline (CryRenderer)                │
│  ├── Sparse Voxel Octree Global Illumination (SVOGI)        │
│  ├── Volumetric Clouds, Atmospheric Scattering & Fog        │
│  └── PBR Surface Shaders (DirectX 11/12, Vulkan Backends)   │
│                                                             │
│  Gameplay & Entity Component Model                          │
│  ├── CryEntity System (`IEntity`, `IEntityComponent`)       │
│  ├── Schematyc Visual Graph & State Machine Execution       │
│  └── Flowgraph Legacy Mission & Dialogue Scripting          │
│                                                             │
│  Physics & Environment Engine                               │
│  ├── CryPhysics (Rigid Body, Ragdoll, Vehicle, Particle)    │
│  └── Procedural Vegetation & Dynamic Terrains (`.cry` Maps) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **C++ `IEntityComponent` Architecture**: Author clean, modern C++ entity components implementing `Initialize()`, `ProcessEvent()`, and Schematyc reflection macros (`CRY_GENERATE_COMPONENT_GUID`).
2. **SVOGI Real-Time Lighting Optimization**: Diagnose and resolve light leaks, shadow banding, and performance bottlenecks by fine-tuning voxel density, injection cones, and occlusion multipliers.
3. **Physics & Collision Solver Triage**: Remediate high-velocity tunneling, ragdoll twitching, and character controller jitter by adjusting CryPhysics raycast filters and mass-inertia matrices.
4. **Asset & Shader Pipeline Troubleshooting**: Fix corrupted user shader caches (`user/shaders/cache`), missing `.cgf` / `.skin` material assignments, and Level of Detail (LOD) pop-in artifacts.

---

## Production C++ Game Engine Code: Character Controller Component

Save this file as `PlayerControllerComponent.h` and `PlayerControllerComponent.cpp` in your CryEngine C++ Game Plugin:

```cpp
// ==============================================================================
// CryEngine 5.x C++ Entity Component: Smooth Player Character Controller
// Implements physics-based movement, ground raycasting, and Schematyc reflection.
// ==============================================================================
#pragma once
#include <CryEntitySystem/IEntityComponent.h>
#include <CryEntitySystem/IEntitySystem.h>
#include <CryPhysics/physinterface.h>

class CPlayerControllerComponent final : public IEntityComponent
{
public:
    CPlayerControllerComponent() = default;
    virtual ~CPlayerControllerComponent() = default;

    // Unique Component GUID for Schematyc / Engine Reflection
    CRY_GENERATE_COMPONENT_GUID("A9B8C7D6-E5F4-4321-ABCD-1234567890AB", "PlayerControllerComponent")

    // IEntityComponent Lifecycle
    void Initialize() override
    {
        // Physicalize as a Living Character Capsule
        SEntityPhysicalizeParams physParams;
        physParams.type = PE_LIVING;
        physParams.mass = 80.0f; // 80kg mass

        pe_player_dimensions playerDim;
        playerDim.heightCollider = 1.8f;
        playerDim.sizeCollider = Vec3(0.4f, 0.4f, 0.9f);
        playerDim.bUseCapsule = 1;
        physParams.pPlayerDimensions = &playerDim;

        GetEntity()->Physicalize(physParams);
    }

    void ProcessEvent(const SEntityEvent& event) override
    {
        if (event.event == ENTITY_EVENT_UPDATE)
        {
            const float frameTime = gEnv->pTimer->GetFrameTime();
            UpdateMovement(frameTime);
        }
    }

    uint64 GetEventMask() const override
    {
        return BIT64(ENTITY_EVENT_UPDATE);
    }

    void SetMovementInput(const Vec3& desiredVelocity) { m_desiredVelocity = desiredVelocity; }

private:
    void UpdateMovement(float frameTime)
    {
        IPhysicalEntity* pPhysEntity = GetEntity()->GetPhysics();
        if (!pPhysEntity) return;

        pe_action_move moveAction;
        moveAction.dir = m_desiredVelocity;
        moveAction.iJump = 0;
        pPhysEntity->Action(&moveAction);
    }

    Vec3 m_desiredVelocity = ZERO;
};
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **SVOGI Light Bleeding Through Thin Walls** | Voxel grid resolution too coarse relative to wall geometry thickness ($<2\times$ voxel cell size). | 1. In Console, set `e_svoTI_VoxelRatio = 128` (or 256 for finer voxelization).<br>2. Ensure wall geometry has physical interior thickness ($\ge 20\text{cm}$) rather than single-sided quad planes.<br>3. Set `e_svoTI_ConeMaxLength = 16` to limit sampling distance. |
| **Sandbox Editor Crashes on Level Load with Shader Error** | Cached compiled shader permutations out of sync with current GPU driver or modified `.cfx` files. | 1. Navigate to `<ProjectRoot>\user\shaders\` $\rightarrow$ Delete `cache` directory.<br>2. Relaunch Editor to trigger background parallel shader recompilation.<br>3. In Console, run `r_PrecacheShaders = 1`. |
| **Physics Tunneling / Object Falls Through Terrain** | High-velocity projectile or falling entity skipping collision steps between discrete physics ticks. | 1. On fast-moving physical entities, enable continuous collision: `pe_params_flags pf; pf.flagsOR = pef_continuous_collision; pPhys->SetParams(&pf)`.<br>2. Increase physics tick rate in `engine.cfg`: `p_max_substeps = 5`. |
| **Schematyc Component Missing in Sandbox Editor UI** | Component class missing `CRY_GENERATE_COMPONENT_GUID` macro or not registered in the Plugin Extension module. | In your `CGamePlugin::OnPluginRegister` callback, invoke `Schematyc::IEnvRegistrar::RegisterComponent<CPlayerControllerComponent>()`. |

---

## Command Line Syntax & Engine Console Variables (CVars)

```bash
# 1. Launch Sandbox Editor with Specific Project File
Editor.exe -project "C:\Projects\MyGame\Game.cryproject"

# 2. Launch Standalone Game in Developer Debug Mode
GameLauncher.exe -devmode -console

# 3. Essential Real-Time Graphics CVars (Execute in Engine Console)
e_svogi 1                     # Enable Sparse Voxel Octree Global Illumination
e_svoTI_GsmCascades 3         # Cascade shadow projection depth
r_ssdo 1                      # Screen-Space Directional Occlusion
r_VolumetricFog 1             # High-density volumetric atmosphere
```

### Essential File & Directory Locations
- **Master Engine Config**: `<CryEngineRoot>\engine\engine.cfg`
- **Project Configuration**: `<ProjectRoot>\project.cryproject`
- **Shader Cache**: `<ProjectRoot>\user\shaders\cache\`

---

## Agent Operational Directive
> **MANDATORY**: Never model thin single-sided geometry for interior environments using SVOGI; always enforce minimum geometric wall thickness ($\ge 20\text{cm}$) to prevent voxel light leaks. Clean user shader caches on major engine version upgrades.
