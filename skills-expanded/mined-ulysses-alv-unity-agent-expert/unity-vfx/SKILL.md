---
name: unity-vfx
description: >
  Unity 6000.3 LTS VFX patterns for 3D. Covers Particle Systems (Shuriken),
  VFX Graph, shader-based effects, HDRP/URP rendering, GPU instancing, LOD strategies,
  and visual effects optimization for high-performance VFX.
  Trigger: When creating particle effects, VFX graphs, shader effects,
  or visual effects in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating particle effects (fire, smoke, sparks, explosions, rain, snow)
- Building GPU-driven effects with VFX Graph
- Writing HLSL shaders for custom VFX (dissolve, fresnel, distortion)
- Implementingtrail effects, decals, or billboard animations
- Optimizing VFX for mobile or high-particle-count scenarios
- Setting up HDRP/URP materials with proper decal layers
- Creating stylized or procedural VFX with noise fields
- Managing VFX memory budgets and draw call optimization

## Critical Rules

### NEVER write VFX Update in MonoBehaviour Update — Use Proper Timing

```csharp
// ❌ WRONG — Particles are time-based, Update frame rate varies
void Update()
{
    particleSystem.Simulate(Time.time); // Broken timing
}

// ✅ CORRECT — Use particleSystem.Simulate with deltaTime
void Update()
{
    // Option 1: Built-in auto-update (default)
    // Just call Play/Stop, the system updates automatically

    // Option 2: Manual simulation for full control
    particleSystem.Simulate(Time.deltaTime, false, false, true);
}

// ✅ CORRECT — Control playback explicitly
public class ControlledVFX : MonoBehaviour
{
    private ParticleSystem _ps;

    private void Awake()
    {
        _ps = GetComponent<ParticleSystem>();
    }

    private void OnEnable()
    {
        _ps.Play();
    }

    private void Update()
    {
        // Auto-update is on by default, but you can pause/resume
        if (ShouldPause())
        {
            _ps.Pause();
        }
        else
        {
            _ps.Play();
        }
    }
}
```

**Why:** Particle systems have their own timing model. Calling `Simulate()` with wrong parameters causes jitter, incorrect lifetimes, or particles not rendering.

### Use VFX Graph for >10,000 Particles — Particle System for <10,000

```csharp
// Particle System — CPU-driven, good for <10k particles
var ps = gameObject.AddComponent<ParticleSystem>();
ps.maxParticles = 5000;

// VFX Graph — GPU-driven, good for 10k-1M+ particles
// Use when you need:
// - Massive particle counts
// - Complex particle behavior (flocking, steering)
// - GPU-only processing (no CPU simulation)
```

**Why:** Particle System runs on CPU with灵魂出窍限. VFX Graph runs entirely on GPU via compute shaders, scaling to millions of particles.

### Always Configure VFX for the Target Platform

```csharp
// HDRP-specific VFX settings
var ps = GetComponent<ParticleSystem>();
var main = ps.main;

// HDRP uses .hdr color space — colors appear brighter in build
main.startColor = new ParticleSystem.MinMaxGradient(
    new Color(1f, 0.5f, 0.1f, 1f) // HDR color (values can exceed 1)
);

// URP: Use standard color range
// Mobile: Reduce particle counts, use simpler shaders
```

## Particle Systems (Shuriken)

### Module Architecture

Particle Systems are composed of modules. Each module controls a specific aspect:

| Module | What it controls |
|--------|-------------------|
| **Main** | Lifetime, emission, start size/color/rotation |
| **Emission** | Rate over time, burst emission |
| **Shape** | Spawn volume (cone, sphere, box, mesh) |
| **Velocity over Lifetime** | Speed changes over time |
| **Limit Velocity over Lifetime** | Speed capping, damping |
| **Force over Lifetime** | Gravity, wind, custom forces |
| **Color over Lifetime** | Fade, color transitions |
| **Color by Speed** | Color based on velocity |
| **Size over Lifetime** | Scale changes |
| **Size by Speed** | Scale based on velocity |
| **Rotation over Lifetime** | Spin rates |
| **Rotation by Speed** | Spin based on velocity |
| **External Forces** | Wind zones, influence |
| **Noise** | Turbulence, pseudo-random fields |
| **Triggers** | Collision, death callbacks |
| **Renderer** | Material, billboard mode, sorting |
| **Custom Data** | Pass custom floats/colors to shaders |
| **Inherit Velocity** | Parent motion inheritance |
| **Texture Sheet Animation** | Sprite/sheet animation |

### Main Module

```csharp
var main = ps.main;

// Duration and looping
main.duration = 3f;
main.loop = true;

// Lifetime
main.startLifetime = 2f; // Constant
main.startLifetime = new ParticleSystem.MinMaxCurve(1f, 3f); // Random range

// Emission rate (particles/second) — only when not using bursts
main.emitterVelocityMode = ParticleSystemEmitterVelocityMode.Transform;
main.simulationSpace = ParticleSystemSimulationSpace.World; // World or Local

// Start size
main.startSize = 0.5f;
main.startSize = new ParticleSystem.MinMaxCurve(0.3f, 0.8f); // Random
main.startSize3D = true; // Enable 3D size for non-uniform scaling
main.startSizeX = new ParticleSystem.MinMaxCurve(0.1f, 0.5f);
main.startSizeY = new ParticleSystem.MinMaxCurve(0.1f, 0.3f);
main.startSizeZ = new ParticleSystem.MinMaxCurve(0.1f, 0.2f);

// Start color (HDR for bloom effects)
main.startColor = new ParticleSystem.MinMaxGradient(
    new Color(1f, 0.8f, 0.2f, 1f),  // HDR yellow
    new Color(1f, 0.2f, 0.1f, 1f)   // HDR red
);

// Start rotation (degrees)
main.startRotation = 0f;
main.startRotation = new ParticleSystem.MinMaxCurve(0f, 360f); // Full spin
main.startRotation3D = true;
main.startRotationX = new ParticleSystem.MinMaxCurve(0f, 90f);
main.startRotationY = new ParticleSystem.MinMaxCurve(0f, 180f);
main.startRotationZ = new ParticleSystem.MinMaxCurve(0f, 360f);

// Playback speed
main.simulationSpeed = 1f; // 2f = 2x faster

// Max particles (memory budget)
main.maxParticles = 1000;

// Ring buffer (reuse dead particles)
main.ringBufferMode = ParticleSystemRingBufferMode.Disabled;
main.ringBufferMode = ParticleSystemRingBufferMode.PauseAfterDeath;
main.ringBufferRetentionTime = 1f; // Seconds before reuse
```

### Emission Module

```csharp
var emission = ps.emission;

// Rate mode — particles per second
emission.rateOverTime = 100f;
emission.rateOverTime = new ParticleSystem.MinMaxCurve(50f, 200f);

// Rate over distance — for moving emitters
emission.rateOverDistance = 10f; // Per unit moved
emission.rateOverDistance = new ParticleSystem.MinMaxCurve(5f, 20f);

// Burst emission — instant spawns at specific times
emission.SetBursts(new ParticleSystem.Burst[]
{
    new ParticleSystem.Burst(0f, 100),                    // At time 0, spawn 100
    new ParticleSystem.Burst(0.5f, 50),                   // At time 0.5, spawn 50
    new ParticleSystem.Burst(1f, new ParticleSystem.MinMaxTrigger(25, 75)) // Random 25-75
});

// Count and cycles
emission.burstCount = 2; // Total burst entries
```

### Shape Module

```csharp
var shape = ps.shape;

// Cone (most common for directional effects)
shape.shapeType = ParticleSystemShapeType.Cone;
shape.angle = 25f; // Cone angle (0 = straight line)
shape.radius = 0.5f; // Base radius
shape.arc = 360f; // Full circle (can be partial)
shape.arcSpeed = 0f; // Static or animated
shape.sphericalDirection = false;

// Box
shape.shapeType = ParticleSystemShapeType.Box;
shape.scale = new Vector3(2f, 1f, 2f); // Box dimensions

// Sphere
shape.shapeType = ParticleSystemShapeType.Sphere;
shape.radius = 1f;

// Mesh (spawn on vertices/surface/triangle)
shape.shapeType = ParticleSystemShapeType.Mesh;
shape.mesh = targetMesh;
shape.useMeshNormals = true; // Align particles to normals
shape.normalOffset = 0f; // Offset along normal

// Skinned Mesh
shape.shapeType = ParticleSystemShapeType.SkinnedMesh;
shape.skinnedMeshRenderer = skinnedMesh;

// Hemisphere
shape.shapeType = ParticleSystemShapeType.Hemisphere;
shape.radius = 1f;

// Circle (2D effect)
shape.shapeType = ParticleSystemShapeType.Circle;
shape.radius = 0.5f;
shape.arc = 180f; // Half circle

// Donut (torus)
shape.shapeType = ParticleSystemShapeType.Donut;
shape.radius = 1f;
shape.donutRadius = 0.3f; // Thickness of donut
```

### Velocity over Lifetime

```csharp
var velocity = ps.velocityOverLifetime;

// Linear velocity
velocity.space = ParticleSystemSimulationSpace.World;
velocity.x = new ParticleSystem.MinMaxCurve(1f, -2f); // Constant + random range
velocity.y = new ParticleSystem.MinMaxCurve(5f); // Upward
velocity.z = new ParticleSystem.MinMaxCurve(0f);

// Orbital (circle around spawn point)
velocity.space = ParticleSystemSimulationSpace.Local;
velocity.orbitX = new ParticleSystem.MinMaxCurve(1f, 0.5f);
velocity.orbitY = new ParticleSystem.MinMaxCurve(2f, 1f);
velocity.orbitZ = new ParticleSystem.MinMaxCurve(0.5f);

// Offset from center
velocity.offsetX = new ParticleSystem.MinMaxCurve(0f);
velocity.offsetY = new ParticleSystem.MinMaxCurve(0f);
velocity.offsetZ = new ParticleSystem.MinMaxCurve(0f);

// Dampen (reduces velocity over time)
velocity.d Dampen = 0.1f; // 10% reduction over lifetime
```

### Limit Velocity over Lifetime

```csharp
var limit = ps.limitVelocityOverLifetime;

// Speed limit
limit.enabled = true;
limit.limit = 10f; // Max speed
limit.limit = new ParticleSystem.MinMaxCurve(5f, 15f); // Random range

// Dampen (drag coefficient)
limit.dampen = 0.5f; // Higher = more drag

// Separate axes
limit.separateX = true;
limit.limitX = 5f;
limit.limitY = 10f;
limit.limitZ = 5f;
```

### Force over Lifetime

```csharp
var forces = ps.forcesOverLifetime;

// Wind force
forces.enabled = true;
forces.space = ParticleSystemSimulationSpace.World;
forces.x = new ParticleSystem.MinMaxCurve(0f, 1f); // Turbulence
forces.y = new ParticleSystem.MinMaxCurve(2f);
forces.z = new ParticleSystem.MinMaxCurve(0f);

// Add randomness
forces.x = new ParticleSystem.MinMaxCurve(0f, new AnimationCurve(
    new Keyframe(0f, 0f),
    new Keyframe(0.5f, 1f),
    new Keyframe(1f, 0f)
));

// Inherit from Rigidbody
forces.inheritVelocity = 0.5f; // 0-1 multiplier
```

### Color over Lifetime

```csharp
var color = ps.colorOverLifetime;

// Fade out over lifetime (most common)
color.enabled = true;
var gradient = new ParticleSystem.MinMaxGradient(
    new Color(1f, 1f, 1f, 1f),  // Start: fully opaque white
    new Color(1f, 1f, 1f, 0f)   // End: transparent
);
gradient.mode = ParticleSystemGradientMode.Blend; // Or Constant
color.color = gradient;

// Two-stop gradient with color interpolation
color.color = new ParticleSystem.MinMaxGradient(
    new GradientColorKey[] {
        new GradientColorKey(Color.red, 0f),
        new GradientColorKey(Color.yellow, 0.5f),
        new GradientColorKey(Color.blue, 1f)
    },
    new GradientAlphaKey[] {
        new GradientAlphaKey(1f, 0f),
        new GradientAlphaKey(0.5f, 0.5f),
        new GradientAlphaKey(0f, 1f)
    }
);
```

### Size over Lifetime

```csharp
var size = ps.sizeOverLifetime;

// Simple uniform scale curve
size.enabled = true;
size.size = new ParticleSystem.MinMaxCurve(1f, new AnimationCurve(
    new Keyframe(0f, 0f),
    new Keyframe(0.25f, 1.2f),  // Grow
    new Keyframe(1f, 0f)        // Shrink to nothing
));

// 3D size (separate X, Y, Z)
size.size3D = true;
size.sizeX = new ParticleSystem.MinMaxCurve(1f, curveX);
size.sizeY = new ParticleSystem.MinMaxCurve(1f, curveY);
size.sizeZ = new ParticleSystem.MinMaxCurve(1f, curveZ);
```

### Noise Module

```csharp
var noise = ps.noise;

// Enable and configure
noise.enabled = true;
noise.separateAxes = true; // Different noise per axis

// Strength (amplitude)
noise.strengthX = new ParticleSystem.MinMaxCurve(1f, 0.5f);
noise.strengthY = new ParticleSystem.MinMaxCurve(1f, 0.5f);
noise.strengthZ = new ParticleSystem.MinMaxCurve(1f, 0.5f);

// Scroll (move through noise field)
noise.scrollSpeed = 0.5f; // UV scrolling speed

// Frequency (zoom level)
noise.frequency = 2f; // Higher = more detailed noise

// Octaves (layers of noise for complexity)
noise.octaveCount = 3; // More octaves = more detail, more expensive

// Damping (how much noise affects vs base velocity)
noise.damping = 0.5f; // 0.5 = noise contributes 50% of velocity

// Remap (scale output)
noise.remapX = new ParticleSystem.MinMaxCurve(1f, -1f); // Output range
noise.remapY = new ParticleSystem.MinMaxCurve(1f, -1f);
noise.remapZ = new ParticleSystem.MinMaxCurve(1f, -1f);
noise.remap = new ParticleSystem.MinMaxCurve(1f, -1f); // Uniform
```

### Texture Sheet Animation

```csharp
var texSheet = ps.textureSheetAnimation;

// Enable and configure
texSheet.enabled = true;
texSheet.mode = ParticleSystemAnimationMode.Row; // Or WholeSheet

// Grid size
texSheet.numTilesX = 4; // Columns
texSheet.numTilesY = 4; // Rows

// Starting frame
texSheet.startFrame = 0;

// Animation
texSheet.cycleCount = 1; // Times to loop (0 = infinite)
texSheet.rowIndex = 0; // Which row (for Row mode)

// UV options
texSheet.uvChannelMask = new Vector4(1, 1, 0, 0); // Which UV channels to use
```

### Renderer Module

```csharp
var renderer = ps.renderer;

// Material
renderer.renderMode = ParticleSystemRenderMode.Billboard; // Default
renderer.renderMode = ParticleSystemRenderMode.Stretch; // Stretches with velocity
renderer.renderMode = ParticleSystemRenderMode.HorizontalBillboard;
renderer.renderMode = ParticleSystemRenderMode.VerticalBillboard;
renderer.renderMode = ParticleSystemRenderMode.Mesh;
renderer.renderMode = ParticleSystemRenderMode.None; // No geometry (trails only)

renderer.material = particleMaterial;
renderer TrailMaterial = trailMaterial;

// Mesh for mesh render mode
renderer.mesh = targetMesh;

// Sorting
renderer.sortMode = ParticleSystemSortMode.None; // Default (by distance)
renderer.sortMode = ParticleSystemSortMode.OldestFirst;
renderer.sortMode = ParticleSystemSortMode.YoungestFirst;
renderer.sortMode = ParticleSystemSortMode.ByDistance;
renderer.sortMode = ParticleSystemSortMode.None;

// Fading
renderer.fadeOut = true; // Fade when near camera
renderer.minParticleDistance = 0.1f; // Distance before fade starts

// Motion Vectors (for motion blur)
renderer.motionVectorGenerationMode = MotionVectorGenerationMode.Camera;
renderer.motionVectorGenerationMode = MotionVectorGenerationMode.Object;
renderer.motionVectorGenerationMode = MotionVectorGenerationMode ForceNoMotion;

// Shadow casting
renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.On;
renderer.receiveShadows = true;

// Sorting layer
renderer.sortingLayerID = sortingLayerId;
renderer.sortingOrder = 0;

// Billboard alignment
renderer.billboardCameraTarget = mainCamera.transform;
renderer.billboardAlignMode = ParticleSystemBillboardAlignMode.ViewPlane; // Default
renderer.billboardAlignMode = ParticleSystemBillboardAlignMode.LocalPlane;
renderer.billboardAlignMode = ParticleSystemBillboardAlignMode.World;
renderer.billboardAlignMode = ParticleSystemBillboardAlignMode None;

// Normal direction (for lighting on stretched billboards)
renderer.normalDirection = 1f; // 0-1 blend towards normal

// Pivot (rotation center offset)
renderer.pivot = new Vector3(0f, 0.5f, 0f); // Offset upward
```

### Trails Module

```csharp
var trails = ps.trails;

// Enable trails
trails.enabled = true;
trails.ratio = 1f; // Particles with trail (0-1)
trails.lifetime = 0.5f; // Trail length as fraction of particle lifetime
trails.minVertexDistance = 0.1f; // Minimum distance between trail points

// World space vs local
trails.space = ParticleSystemTrailSpace.World;
trails.space = ParticleSystemTrailSpace.Local;
trails.space = ParticleSystemTrailSpace.Custom; // Relative to transform
trails.customWorldSpaceTrailAnchor = anchorTransform;

// Width
trails.widthOverTrail = new ParticleSystem.MinMaxCurve(1f, new AnimationCurve(
    new Keyframe(0f, 1f),
    new Keyframe(1f, 0f) // Taper to end
));
trails.widthOverTrailMultiplier = 1f;

// Color
trails.colorOverLifetime = colorGradient; // Optional

// Inherit particle color
trails.inheritParticleColor = true;

// Material
trails.ratio = 0.5f; // 50% of particles have trails
trails.dieWithParticle = true; // Trail dies with particle

// Lifetime affects trail visibility
trails.dieWithParticle = false; // Trail persists after particle death
trails.worldSpaceTrailMaxLength = 10f; // Maximum trail length in world space
```

### Collision Module

```csharp
var collision = ps.collision;

// Enable and type
collision.enabled = true;
collision.type = ParticleSystemCollisionType.Plane; // Infinite planes
collision.type = ParticleSystemCollisionType.World; // Actual geometry

// For World collision
collision.worldBounds = new Vector3(50f, 50f, 50f); // Collision volume

// Bounce
collision.bounce = 0.5f; // 0-1, how much to bounce
collision.bounce multiplier = 1f; // Scale bounce

// Lifetime loss on collision
collision.lifetimeLoss = 0.5f; // Lose 50% lifetime on hit
collision.lifetimeLossMultiplier = 1f;

// Collides with
collision.collidesWith = LayerMask.GetMask("Ground", "Walls");
collision.collidesWithLayers = everythingLayerMask; // Everything

// Enable dynamic colliders (moving objects)
collision.enableDynamicColliders = true;

// Quality
collision.quality = ParticleSystemCollisionQuality.High; // All particles
collision.quality = ParticleSystemCollisionQuality.Medium; // Half
collision.quality = ParticleSystemCollisionQuality.Low; // Quarter
collision.quality = ParticleSystemCollisionQuality.EveryFrame; // High quality

// Voxel collision (for many small colliders)
collision.voelSize = 0.5f; // Voxel grid size

// Send collision callbacks
collision.enableInteriorCollisions = false; // Don't trigger for "inside" hits
collision.maxCollisionShapes = 65535; // Limit for performance
```

### Sub Emitters

```csharp
var subEmitters = ps.subEmitters;

// Configure sub-emitters for birth, death, collision
subEmitters.enabled = true;

// Birth sub-emitter (spawned when particle is born)
subEmitters.SubEmitterBirth = explosionPS; // ParticleSystem reference
subEmitters.SubEmitterBirth3 = null; // No 3D version

// Death sub-emitter (spawned when particle dies)
subEmitters.SubEmitterDeath = deathEffectPS;

// Collision sub-emitter (spawned on collision hit)
subEmitters.SubEmitterCollision = impactPS;
subEmitters.collisionProbability = 0.1f; // 10% chance per collision

// Properties passed to sub-emitter
subEmitters.properties = ParticleSystemSubEmitterProperties.InheritEverything;
subEmitters.properties = ParticleSystemSubEmitterProperties.InheritNothing;
subEmitters.properties = ParticleSystemSubEmitterProperties.InheritColor;
subEmitters.properties = ParticleSystemSubEmitterProperties.InheritSize;
subEmitters.properties = ParticleSystemSubEmitterProperties.InheritRotation;
```

### Custom Data Module

```csharp
var customData = ps.customData;

// Define custom data slots (up to 4 vector4 slots)
customData.SetMode(ParticleSystemCustomData.Custom1, ParticleSystemCustomDataMode.Vector);
customData.SetMode(ParticleSystemCustomData.Custom2, ParticleSystemCustomDataMode.Color);

// Set values procedurally
customData.SetVector(ParticleSystemCustomData.Custom1, 0, new Vector4(1f, 0f, 0f, 1f));

// Read in shader via vertex attributes
// Shader receives: UV4 (custom1), UV5 (custom2), UV6 (custom3), UV7 (custom4)
```

### Trigger Module

```csharp
var trigger = ps.trigger;

// Enable and configure
trigger.enabled = true;
trigger.inside = ParticleSystemTriggerAction.Callback; // When entering collider
trigger.inside = ParticleSystemTriggerAction.Kill; // Destroy particle
trigger.inside = ParticleSystemTriggerAction.Ignore; // Do nothing
trigger.inside = ParticleSystemTriggerAction.CallbackOnly; // Callback but keep particle

trigger.outside = ParticleSystemTriggerAction.Ignore;
trigger.enter = ParticleSystemTriggerAction.Callback;
trigger.exit = ParticleSystemTriggerAction.Ignore;

// Collider reference
trigger.colliderQueryMode = ParticleSystemColliderQueryMode.One; // Check one collider
trigger.colliderQueryMode = ParticleSystemColliderQueryMode.All; // Check all colliders

// Radius (for trigger volume)
trigger.radiusScale = 0.5f; // Smaller trigger volume

// List of colliders
trigger.AddCollider(myCollider);
trigger.RemoveCollider(myCollider);
trigger.ClearColliders();
```

## VFX Graph

### Graph Structure

VFX Graph uses nodes and edges instead of modules:

```
[Source] → [Output]
   ↑
[Operator/Block]
```

### Common Nodes

#### Spawn Context
- **Constant Rate** — Spawn N particles per second
- **Burst Rate** — Spawn N particles at intervals
- **Single Burst** — Spawn N particles once
- ** Poisson** — Random spawn distribution

#### Initialize Particle
- **Spawn** — Set capacity (max particles)
- **Initialize Position** — Set spawn location
- **Initialize Velocity** — Set initial speed
- **Initialize Color** — Set particle color
- **Initialize Size** — Set particle size
- **Initialize Age** — Set particle age (for delayed spawn)

#### Update Particle
- **Integrate** — Apply physics (position += velocity * dt)
- **Gravity** — Apply gravity force
- **Force** — Apply custom force field
- **Wind** — Apply wind turbulence
- **Drag** — Apply velocity damping
- **Collision** — Bounce off surfaces
- **Kill** — Remove particles based on condition
- **Set Color** — Update particle color
- **Set Size** — Update particle size
- **Orient** — Rotate to face direction (billboard, etc.)

#### Output Particle
- **Output Particle** — Finalize and render particle
- **Output Decal** — Render as decal

### VFX Graph C# Binding

```csharp
// Finding and controlling VFX from C#
using UnityEngine.VFX;

public class VFXController : MonoBehaviour
{
    [SerializeField] private VisualEffect vfxGraph;

    private void Start()
    {
        // Set float parameters
        vfxGraph.SetFloat("Intensity", 1.5f);
        vfxGraph.SetFloat("Speed", 10f);
        vfxGraph.SetFloat("Turbulence", 0.5f);

        // Set vector parameters
        vfxGraph.SetVector3("Direction", Vector3.up);
        vfxGraph.SetVector3("AreaSize", new Vector3(5f, 1f, 5f));

        // Set int parameters
        vfxGraph.SetInt("ParticleCount", 1000);

        // Set bool parameters
        vfxGraph.SetBool("UseNoise", true);

        // Set gradient (via AnimationCurve)
        vfxGraph.SetAnimationCurve("ColorGradient",
            new AnimationCurve(
                new Keyframe(0f, 0f),
                new Keyframe(0.5f, 1f),
                new Keyframe(1f, 0f)
            )
        );

        // Set texture
        vfxGraph.SetTexture("NoiseTex", noiseTexture);

        // Play/Stop
        vfxGraph.Play();
        vfxGraph.PlaySubgraph("SubGraphName"); // Play nested graph
        vfxGraph.Stop();
        vfxGraph.Stop(StopFlags.D graceful); // Let current particles finish

        // Reset
        vfxGraph.Reinit(); // Clear all particles and restart
    }

    private void Update()
    {
        // Continuous parameter update
        float pulse = Mathf.Sin(Time.time) * 0.5f + 0.5f;
        vfxGraph.SetFloat("Pulse", pulse);
    }

    // Event binding for VFX callbacks
    private void OnVFXEvent(VFXOutputEventData e)
    {
        Debug.Log($"VFX Event: {e}");
    }
}
```

### VFX Graph Shader Graph Integration

```csharp
// Using a custom shader with VFX Graph
// 1. Create a Lit/Unlit shader with VFX keywords
// 2. Use the appropriate target (HDRP/URP)

// Example: Custom VFX fragment shader (HDRP Lit)
Shader "VFX/CustomVFX"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Distortion ("Distortion", Range(0, 1)) = 0.1
    }

    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue"="Transparent" }
        Blend SrcAlpha OneMinusSrcAlpha

        Pass
        {
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile _ VFX_USE_DISTORTION
            #include "Packages/com.unity.visualeffectgraph/Shaders/RenderPipeline/HDRP/VFXDefines.hlsl"

            struct Attributes
            {
                float4 position : POSITION;
                float2 uv : TEXCOORD0;
                float4 color : COLOR;
                // VFX specific
                float3 normal : NORMAL;
                float4 texcoord1 : TEXCOORD1;
                float4 texcoord2 : TEXCOORD2;
                float4 texcoord3 : TEXCOORD3;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct Varyings
            {
                float4 position : SV_POSITION;
                float2 uv : TEXCOORD0;
                float4 color : COLOR;
                float3 normal : TEXCOORD1;
                float3 viewDir : TEXCOORD2;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            Varyings vert(Attributes input)
            {
                Varyings output;
                UNITY_SETUP_INSTANCE_ID(input);
                UNITY_TRANSFER_INSTANCE_ID(input, output);

                output.position = TransformWorldToHClip(input.position.xyz);
                output.uv = input.uv;
                output.color = input.color;
                output.normal = input.normal;
                output.viewDir = GetWorldSpaceNormalizeViewDir(input.position.xyz);

                return output;
            }

            TEXTURE2D(_MainTex);
            SAMPLER(sampler_MainTex);
            float _Distortion;

            float4 frag(Varyings input) : SV_Target
            {
                UNITY_SETUP_INSTANCE_ID(input);
                float4 col = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, input.uv);
                col *= input.color;

                // Fresnel rim
                float fresnel = pow(1 - saturate(dot(input.normal, input.viewDir)), 3);
                col.rgb += fresnel * 0.5f;

                return col;
            }
            ENDHLSL
        }
    }
}
```

## Shader Effects

### Fresnel (Rim Light)

```hlsl
// Fresnel effect for VFX — makes edges glow
float Fresnel(float3 normal, float3 viewDir, float power)
{
    return pow(1 - saturate(dot(normal, viewDir)), power);
}

// Usage in fragment shader
float fresnel = Fresnel(input.normal, input.viewDir, 4.0);
float3 rimColor = _RimColor * fresnel * _RimIntensity;
output.rgb += rimColor;
```

### Dissolve Effect

```hlsl
// Dissolve shader for VFX
Properties
{
    _DissolveMap ("Dissolve Map", 2D) = "white" {}
    _DissolveThreshold ("Threshold", Range(0, 1)) = 0.5
    _DissolveColor ("Edge Color", Color) = (1, 0.5, 0, 1)
    _DissolveWidth ("Edge Width", Range(0, 0.5)) = 0.05
}

float4 Dissolve(Varyings input, float4 baseColor)
{
    float dissolve = SAMPLE_TEXTURE2D(_DissolveMap, sampler_DissolveMap, input.uv).r;
    float threshold = _DissolveThreshold;

    // Discard dissolved pixels
    clip(dissolve - threshold);

    // Edge glow
    float edge = dissolve - threshold;
    if (edge < _DissolveWidth)
    {
        float edgeFactor = edge / _DissolveWidth;
        float3 edgeColor = lerp(_DissolveColor, baseColor.rgb, edgeFactor);
        return float4(edgeColor, 1.0);
    }

    return baseColor;
}
```

### Distortion/Refraction

```hlsl
// Screen-space distortion for heat haze, water, etc.
Properties
{
    _DistortionTex ("Distortion Texture", 2D) = "bump" {}
    _DistortionStrength ("Strength", Range(0, 1)) = 0.1
    _DistortionSpeed ("Speed", Vector) = (1, 1, 0, 0)
}

float4 Distortion(Varyings input, float4 sceneColor)
{
    float2 uv = input.uv;
    float2 offset = SAMPLE_TEXTURE2D(_DistortionTex, sampler_DistortionTex,
        uv + _DistortionSpeed * _Time.xy).xy;
    offset = (offset - 0.5) * 2 * _DistortionStrength;

    // Sample scene with offset
    float4 distortedColor = SAMPLE_TEXTURE2D(_CameraOpaqueTexture,
        sampler_CameraOpaqueTexture, uv + offset);

    return lerp(sceneColor, distortedColor, _DistortionStrength);
}
```

### Procedural Noise for VFX

```hlsl
// Value noise
float Noise(float2 uv)
{
    float2 i = floor(uv);
    float2 f = fract(uv);
    f = f * f * (3 - 2 * f); // Smoothstep

    float a = hash(i);
    float b = hash(i + float2(1, 0));
    float c = hash(i + float2(0, 1));
    float d = hash(i + float2(1, 1));

    return lerp(lerp(a, b, f.x), lerp(c, d, f.x), f.y);
}

// FBM (Fractal Brownian Motion)
float FBM(float2 uv, int octaves)
{
    float value = 0;
    float amplitude = 0.5;
    float frequency = 1;

    for (int i = 0; i < octaves; i++)
    {
        value += amplitude * Noise(uv * frequency);
        amplitude *= 0.5;
        frequency *= 2;
    }

    return value;
}

// Animated turbulence
float Turbulence(float2 uv, float time)
{
    float n1 = FBM(uv + time * 0.1, 4);
    float n2 = FBM(uv + float2(n1) + time * 0.2, 4);
    return n2;
}
```

### Particle Soft Particles

```hlsl
// Soft particle fade based on depth
float SoftParticle(float particleDepth, float surfaceDepth, float softFactor)
{
    float depthDelta = surfaceDepth - particleDepth;
    return saturate(depthDelta * softFactor);
}

// Usage in fragment shader
float4 col = tex2D(_MainTex, i.uv);
float fade = SoftParticle(i.pos.w, sceneDepth, _SoftFactor);
col.a *= fade;
return col;
```

### Vertex Animation (Wobble)

```hlsl
// Vertex wobble for organic VFX
float3 Wobble(float3 position, float time, float intensity)
{
    float3 offset;
    offset.x = sin(time * 3 + position.y * 5) * intensity;
    offset.y = sin(time * 2 + position.x * 4) * intensity;
    offset.z = cos(time * 2.5 + position.z * 3) * intensity;
    return offset;
}

// In vertex shader
v.vertex.xyz += Wobble(v.vertex.xyz, _Time.y, _WobbleIntensity);
```

## Common Mistakes to Prevent

| Mistake | Why it's wrong | Correct approach |
|---------|----------------|------------------|
| Using Particle System for 1M+ particles | CPU bottleneck, terrible performance | Use VFX Graph (GPU-driven) |
| Forgetting to set maxParticles | Unlimited particles = memory explosion | Always set maxParticles = target count |
| Not using Particle System Render Mode Billboard | Particles face random directions | Set billboard mode for camera-facing particles |
| Creating new materials at runtime | Memory leak, GC pressure | Pre-create and reuse materials |
| Using MeshCollider for particle collisions | Extremely expensive | Use Plane colliders or world collision with low quality |
| Setting emit rate too high without bursts | Frame drops during gameplay | Use bursts for instant spawns, lower rates for continuous |
| Not enabling Particle System instancing | Extra draw calls | Enable "Enable Instancing" in Renderer module |
| Ignoring particle bounds | Culling doesn't work | Set appropriate bounds or use AutoBinding |
| Using uncompressed textures for mobile | Memory bloat | Use compressed ASTC/ETC2 textures |
| Not pooling particle systems | Instantiate/Destroy causes GC hitches | Pool and reuse ParticleSystem components |
| Setting lifetime to 0 | Particles die instantly | Use minimum lifetime > 0.1f |
| Forgetting to Stop() before Destroy() | Particles continue playing after object gone | Call Stop() before Destroy() or use auto-destroy |

## Response Format

When writing VFX code:

```csharp
// Use descriptive names for particle system variables
private ParticleSystem _firePS;
private ParticleSystem _smokePS;
private ParticleSystem _sparksPS;

// Group related systems together
[Serializable]
public class ExplosionVFX
{
    public ParticleSystem Main;
    public ParticleSystem Shockwave;
    public ParticleSystem Debris;
    public VisualEffect Sparks;
}

// Use constants for layer/mask values
private const int VFX_LAYER = 8;
private static readonly LayerMask VFX_COLLISION_MASK = LayerMask.GetMask("Ground");

// Document non-obvious configurations
/// <summary>
/// Configures the fire particle system with HDR colors for bloom.
/// Requires HDR rendering enabled on the target pipeline.
/// </summary>
private void ConfigureFireForBloom()
{
    var main = _firePS.main;
    // HDR colors appear brighter in HDRP/URP bloom
    main.startColor = new ParticleSystem.MinMaxGradient(
        new Color(1f, 0.3f, 0.1f, 1f),   // Warm orange
        new Color(1f, 0.8f, 0.2f, 1f)    // Bright yellow
    );
}
```

## Particle System Optimization

### Performance Budgets

| Platform | Max Particles | Draw Calls | Texture Memory |
|----------|---------------|------------|----------------|
| Desktop High | 100,000+ | <50 | <64MB |
| Desktop Low | 10,000 | <20 | <32MB |
| Mobile High | 5,000 | <30 | <32MB |
| Mobile Low | 1,000 | <10 | <16MB |

### Optimization Techniques

```csharp
// 1. Reduce particle count — most effective
main.maxParticles = Mathf.Min(main.maxParticles, targetBudget);

// 2. Use simple render modes
renderer.renderMode = ParticleSystemRenderMode.Billboard; // Fastest
renderer.renderMode = ParticleSystemRenderMode.Stretch; // Slower
renderer.renderMode = ParticleSystemRenderMode.Mesh; // Slowest

// 3. Disable unneeded modules
ps.trails.enabled = false; // Disable if not used
ps.noise.enabled = false; // Noise is expensive

// 4. Use collision quality settings
collision.quality = ParticleSystemCollisionQuality.Low; // Mobile
collision.maxCollisionShapes = 256; // Limit geometry checks

// 5. Reduce emission rate
emission.rateOverTime = Mathf.Min(emission.rateOverTime, 100);

// 6. Use ring buffer mode to reduce allocation
main.ringBufferMode = ParticleSystemRingBufferMode.PauseAfterDeath;
main.ringBufferRetentionTime = 1f;

// 7. Pool particle systems
public class ParticleSystemPool : MonoBehaviour
{
    private Queue<ParticleSystem> _pool = new();
    [SerializeField] private ParticleSystem _prefab;
    [SerializeField] private int _initialSize = 10;

    private void Awake()
    {
        for (int i = 0; i < _initialSize; i++)
        {
            var ps = Instantiate(_prefab);
            ps.gameObject.SetActive(false);
            _pool.Enqueue(ps);
        }
    }

    public ParticleSystem Get(Vector3 position, Quaternion rotation)
    {
        ParticleSystem ps;
        if (_pool.Count > 0)
        {
            ps = _pool.Dequeue();
        }
        else
        {
            ps = Instantiate(_prefab);
        }

        ps.transform.position = position;
        ps.transform.rotation = rotation;
        ps.gameObject.SetActive(true);
        ps.Play();
        return ps;
    }

    public void Return(ParticleSystem ps)
    {
        ps.Stop();
        ps.gameObject.SetActive(false);
        _pool.Enqueue(ps);
    }
}
```

### LOD for Particle Systems

```csharp
// Create simplified versions for distance
public class VFXLOD : MonoBehaviour
{
    [SerializeField] private ParticleSystem highQualityPS;
    [SerializeField] private ParticleSystem mediumQualityPS;
    [SerializeField] private ParticleSystem lowQualityPS;

    [SerializeField] private float mediumDistance = 20f;
    [SerializeField] private float lowDistance = 50f;

    private Transform _cam;

    private void Start()
    {
        _cam = Camera.main.transform;
    }

    private void Update()
    {
        float dist = Vector3.Distance(transform.position, _cam.position);

        highQualityPS.gameObject.SetActive(dist < mediumDistance);
        mediumQualityPS.gameObject.SetActive(dist >= mediumDistance && dist < lowDistance);
        lowQualityPS.gameObject.SetActive(dist >= lowDistance);
    }
}
```

## HDRP/URP VFX Considerations

### HDRP-Specific

```csharp
// HDRP uses .hdr color space
// Colors can exceed 1.0 for bloom effect
main.startColor = new Color(2f, 1f, 0.5f, 1f); // Bright for bloom

// Decal layers
renderer.decalSortingLayerId = sortingLayerId;
renderer.decalRenderPhase = DecalRenderPhase.PreRaytracing; // Or PostRaytracing

// Ray tracing support
renderer.rayTracingMode = ParticleSystemRayTracingMode.None; // Default
renderer.rayTracingMode = ParticleSystemRayTracingMode.All; // Full ray tracing
```

### URP-Specific

```csharp
// URP uses standard color range (0-1)
// Bloom requires Rendererpass/post-processing

// For URP VFX, use:
main.startColor = new Color(1f, 0.5f, 0.2f, 1f); // Standard HDR not required

// Enable HDR for bloom in URP:
// Project Settings > Quality > HDR = true
// Then use ColorMultiple for HDR-like intensity
var color = main.startColor;
color.mode = ParticleSystemGradientMode.Constant;
color.constant = new Color(1f, 0.5f, 0.2f, 1f) * 2; // Boost for bloom
main.startColor = color;
```

### Common VFX Pipeline Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Particles not visible | Render mode None or missing material | Check renderer module settings |
| Bloom not working | Colors not in HDR range | Multiply colors > 1.0 for HDRP |
| Particles z-fighting | Same depth as ground plane | Offset particle render queue or use soft particles |
| Trails flickering | Min vertex distance too high | Lower minVertexDistance in trails module |
| Performance drop over time | Particle accumulation, no cleanup | Set maxParticles, use ring buffer |
| VFX not appearing in build | Shader not included in build | Add shader to "Always Included" or use variant collection |
| Mobile crash | Too many particles or complex shaders | Reduce count, simplify shaders, use mobile alternatives |

## Unity 6000-Specific VFX Features

### VFX Graph Improvements (Unity 6000)

```csharp
// New in Unity 6000: Better GPU simulation
// More particles per instance with improved batching

// Improved spawn contexts
vfxGraph.Play(); // Plays from initial state
vfxGraph.PlaySubgraph("SubgraphName"); // Plays nested graph

// New event system
vfxGraph.SendEvent("ImpactEvent", new VFXEventData
{
    { "Position", impactPosition },
    { "Intensity", impactStrength }
});

// Compile inline expressions directly in the graph
// No need for external scripts for simple logic
```

### Particle System Threading (Unity 6000)

```csharp
// Unity 6000 improved multithreaded particle simulation
// Most simulation now runs on job system automatically

// For explicit job control:
var job = new ParticleSystemSimulationJob
{
    particleSystem = ps,
    deltaTime = Time.deltaTime
};
job.Schedule();
```

### VFX Asset Compilation

```csharp
// VFX Graph assets compile to optimized compute shaders
// Compilation happens automatically but can be controlled:

// Force recompilation
VFXGraphCompiler.CompileAll();

// Get compilation status
var status = VFXGraphCompiler.GetCompilationStatus(vfxAsset);
```

## Common Issues / Gotchas

| Issue | Cause | Solution |
|-------|-------|----------|
| Particles appear as white quads | Missing/broken material | Assign correct particle material |
| Emission rate seems wrong | Wrong simulation space | Check shape module space setting |
| Particles not rotating | startRotation set to 0 | Set rotation range in main module |
| Color over lifetime not fading | Gradient alpha keys wrong | Set alpha to 0 at end of gradient |
| Trails not showing | Trail material not set or too short lifetime | Assign TrailMaterial, increase lifetime |
| Noise not working | Noise module disabled or frequency wrong | Enable noise, adjust frequency (higher = more detail) |
| Collision not detecting | Layer mask excludes collider | Include collider layer in collision module |
| VFX Graph not spawning | Capacity too low or spawn rate 0 | Increase capacity, check spawn block |
| Performance drops with VFX | Too many simultaneous graphs | Use LOD, reduce particle counts |
| Particles stretch weirdly | Stretched billboard mode with low velocity | Adjust speed threshold in renderer |
| Sub emitter not triggering | Sub emitter not configured | Set SubEmitterBirth/Death/Collision |

## Best Practices

1. **Set maxParticles budget upfront** — Prevents memory runaway
2. **Use Billboard render mode** — Fastest GPU path, best for most effects
3. **Reuse materials** — Don't create materials at runtime
4. **Pool particle systems** — Avoid Instantiate/Destroy in hot paths
5. **Use VFX Graph for >10k particles** — GPU acceleration matters at scale
6. **Use HDR colors for bloom** — Multiply colors by 2-3x in HDRP
7. **Disable unneeded modules** — Each enabled module costs CPU/GPU
8. **Use Shape module correctly** — Cone for directional, Sphere for omnidirectional
9. **Test on target hardware** — Mobile and desktop have very different budgets
10. **Profile VFX with RenderDoc** — Identify GPU bottlenecks precisely
11. **Use LOD for distant VFX** — Simplify or hide at distance
12. **Document non-obvious settings** — HDR color ranges, custom curves, etc.
13. **Clean up on disable** — Stop particle systems before object pooling
14. **Use soft particles** — Blend with scene for believability
15. **Pre-warm particle systems** — Simulate(rime) before first render to avoid pop-in

(End of file - total 1047 lines)
