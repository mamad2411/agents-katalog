---
name: create-3d-asset
description: Creates 3D or 2D game-ready assets from reference images. Use when the user provides an image (concept art, sketch, photo, screenshot) and wants to generate a 3D model description, Blender Python script, or 2D sprite specification for their game.
---

# Create 3D/2D Asset from Image

Analyze a reference image and produce game-ready asset specifications, Blender generation scripts, or 2D sprite definitions. This skill bridges concept art to implementation.

## Process

### Step 1: Analyze the Image

When the user provides an image path, read it and analyze:

1. **Subject identification** — What is this? (character, prop, environment, vehicle, creature, UI element)
2. **Art style** — Realistic, stylized, low-poly, pixel art, cartoon, anime, voxel
3. **Complexity assessment** — Simple (< 500 tris), medium (500-5K), complex (5K-50K), high-detail (50K+)
4. **Color palette** — Extract 4-6 dominant colors as hex values
5. **Proportions** — Relative dimensions, notable features, silhouette shape

Present the analysis and ask the user to confirm or correct before proceeding.

### Step 2: Determine Output Type

Ask the user what they need:

**3D Options:**
- **Blender Python script** — Generates the model procedurally using `bpy` (best for geometric/architectural objects, props, primitives)
- **Blender modeling guide** — Step-by-step instructions for manual modeling in Blender with exact measurements
- **Three.js code** — Direct Three.js geometry code for simple shapes (boxes, spheres, combined primitives)
- **GLTF spec** — Detailed specification for commissioning or AI model generation

**2D Options:**
- **Sprite specification** — Dimensions, animation frames, color palette for pixel art or vector sprites
- **CSS/SVG code** — Direct code for simple 2D assets (icons, UI elements, particles)
- **Spritesheet layout** — Frame-by-frame animation spec with timing

### Step 3: Generate the Asset

#### For Blender Python Script (3D)

Generate a complete `bpy` script that:

```python
import bpy
import bmesh
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- MODEL GENERATION ---
# Build the asset using mesh primitives, modifiers, and materials
# ...

# --- MATERIALS ---
# Create PBR materials matching the reference image colors
# Use Principled BSDF with correct base color, roughness, metallic
# ...

# --- EXPORT ---
# Export as GLB for web use
bpy.ops.export_scene.gltf(
    filepath='//asset_name.glb',
    export_format='GLB',
    export_apply=True,
    export_yup=True,
)
```

Script requirements:
- Use `bmesh` for complex geometry, primitives for simple shapes
- Apply Subdivision Surface modifier for organic shapes
- Create proper UV unwrapping (`bpy.ops.uv.smart_project`)
- Set up PBR materials using Principled BSDF node
- Match colors from the reference image analysis
- Add edge loops and proper topology for animation if the asset is a character
- Include mirror modifier where symmetry applies
- Export as GLB at the end
- Comment every section clearly

The user can run this via: `python scripts/blender_batch.py convert` or directly in Blender.

#### For Three.js Code (Simple 3D)

Generate TypeScript code using Three.js primitives:

```typescript
import * as THREE from 'three';

export function createAsset(): THREE.Group {
  const group = new THREE.Group();

  // Build from primitives
  const bodyGeo = new THREE.CylinderGeometry(0.5, 0.5, 1.5, 16);
  const bodyMat = new THREE.MeshStandardMaterial({
    color: 0x...,      // from palette
    roughness: 0.7,
    metalness: 0.1,
  });
  const body = new THREE.Mesh(bodyGeo, bodyMat);
  group.add(body);

  // ... more parts

  return group;
}
```

#### For 2D Sprite Specification

Generate a detailed spec:

```markdown
## Sprite: [Asset Name]

### Dimensions
- Frame size: 64x64 px (or appropriate)
- Scale: 1 unit = 16px

### Animation Frames
| Animation | Frames | FPS | Loop |
|-----------|--------|-----|------|
| Idle      | 4      | 8   | yes  |
| Walk      | 6      | 12  | yes  |
| Attack    | 4      | 16  | no   |
| Death     | 5      | 10  | no   |

### Color Palette
| Name    | Hex     | Usage          |
|---------|---------|----------------|
| Primary | #...... | Body           |
| ...     | ...     | ...            |

### Spritesheet Layout
- Columns: 8
- Rows: 4 (one per animation)
- Total: 64x64 * 8cols * 4rows = 512x256 px
```

#### For Modeling Guide (Manual Blender)

Generate step-by-step instructions:

```markdown
## Modeling Guide: [Asset Name]

### Reference Setup
1. Import reference image as background in front + side view
2. Set dimensions: X=..., Y=..., Z=...

### Base Mesh
1. Start with [cube/cylinder/sphere/plane]
2. Enter Edit Mode (Tab)
3. [Specific modeling steps with exact operations]

### Details
1. Add loop cuts at [locations]
2. Extrude [faces] by [amount]
3. Apply [modifier] with settings [...]

### Materials
1. Create material "Body": Base Color #..., Roughness ..., Metallic ...
2. Create material "Detail": ...
3. Assign faces to materials

### UV Unwrapping
1. Mark seams at [edges]
2. Unwrap with [method]

### Export
1. Apply all modifiers
2. Export as GLB: File > Export > glTF 2.0
3. Settings: Format=GLB, Apply Modifiers=Yes, +Y Up=Yes
```

### Step 4: Optimization Notes

Always include optimization guidance based on target platform:

**For Web/Mobile:**
- Target poly count: [based on asset type]
- Texture size: max 1024x1024 for props, 2048x2048 for characters
- Use Draco compression: `python scripts/asset_pipeline.py compress asset.glb --draco`
- Use KTX2 for textures if > 512KB

**For Desktop:**
- Higher poly budgets allowed
- Can use 4096x4096 textures
- Still compress for load time

### Step 5: Integration Code

Provide a code snippet showing how to load the asset in the user's engine:

**Three.js / R3F:**
```typescript
import { useGLTF } from '@react-three/drei';

function Asset() {
  const { scene } = useGLTF('/models/asset_name.glb');
  return <primitive object={scene} scale={1} />;
}

useGLTF.preload('/models/asset_name.glb');
```

**Phaser (2D):**
```typescript
this.load.spritesheet('asset', 'sprites/asset.png', {
  frameWidth: 64,
  frameHeight: 64,
});

this.anims.create({
  key: 'idle',
  frames: this.anims.generateFrameNumbers('asset', { start: 0, end: 3 }),
  frameRate: 8,
  repeat: -1,
});
```

## Rules

- **Always view the image first.** Use the Read tool to analyze the reference image before generating anything.
- **Match the art style.** If the image is low-poly, generate low-poly. If pixel art, generate pixel specs.
- **Provide runnable code.** Blender scripts must work when pasted into Blender's scripting tab or run via CLI.
- **Include materials.** Never generate a model without PBR materials matching the reference colors.
- **Reference the 3d-game-design skill** for compression, optimization, and export workflows.
- **Ask about animation.** If the asset is a character or creature, ask if they need it rigged/animated.
- If the image is too complex for procedural generation, recommend a modeling guide + AI mesh generation tools (Meshy, Tripo3D, Rodin) as alternatives, and offer to write the optimization/import pipeline.
