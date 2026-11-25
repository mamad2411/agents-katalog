---
name: unity-2d
description: >
  Unity 6000.3 LTS 2D graphics patterns. Covers sprites, sprite atlas,
  tilemaps, 2D lighting, sorting, 9-slice scaling, and URP 2D renderer.
  Trigger: When working with 2D sprites, tilemaps, 2D lighting,
  or any 2D game development task in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Working with 2D sprites, sprite sheets, or sprite atlases
- Creating tilemap-based 2D levels (rectangular, hexagonal, isometric)
- Implementing 2D lighting with URP (Light 2D, shadow Caster 2D)
- Setting up sprite sorting, layers, and render order
- Using 9-slice scaling for UI or reusable sprite assets
- Configuring Sprite Masks for reveal/hide effects
- Creating custom tiles, brushes, or scriptable tiles
- Working with 2D physics (see `unity-physics` skill for Rigidbody2D, Collider2D, joints, effectors)

## Critical Rules

### NEVER Modify Transform for Physics Objects

```csharp
// ❌ WRONG — Breaks physics, bypasses collision detection
transform.position = new Vector3(x, y, 0);
transform.rotation = Quaternion.identity;

// ✅ CORRECT — Use Rigidbody2D for physics-driven movement
rb2d.MovePosition(new Vector2(x, y));
rb2d.MoveRotation(angle);

// ✅ OK — Instant teleport for kinematic objects
rb2d.isKinematic = true;
transform.position = new Vector3(x, y, 0);
rb2d.isKinematic = false;
```

**Why:** In 2D physics, Rigidbody2D controls the Transform. Direct Transform manipulation teleports the collider, missing collisions and pushing other bodies incorrectly.

### FixedUpdate for Physics, Update for Rendering

```csharp
public class PlayerController : MonoBehaviour
{
    private Rigidbody2D _rb;
    private Vector2 _input;

    private void Update()
    {
        // Read input in Update — runs every frame
        _input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
    }

    private void FixedUpdate()
    {
        // Apply physics in FixedUpdate — runs at fixed timestep (50Hz default)
        _rb.MovePosition(_rb.position + _input * speed * Time.fixedDeltaTime);
    }
}
```

### Sprite Atlas for Performance

```csharp
// ❌ WRONG — Separate draw call per sprite
spriteRenderer.sprite = sprites[i];

// ✅ CORRECT — All sprites in one atlas = single draw call
// Pack sprites into a Sprite Atlas (Edit > Project Settings > Sprite Atlas)
// Sprites automatically use atlas texture at runtime
```

**Why:** Each unique texture = separate draw call. Sprite Atlas combines multiple textures into one, reducing GPU batches dramatically.

## Sprite System

### Sprite Import Settings

```csharp
// Texture import settings for sprites (Edit > Project Settings > Texture Import)
// Key properties:
// - Texture Type: Sprite (2D and UI)
// - Sprite Mode: Single (one sprite) or Multiple (sprite sheet)
// - Pixels Per Unit: Determines world size (e.g., 100 = 100 pixels = 1 world unit)
// - Mesh Type: Tight (custom outline) or Full Rect (rectangular boundary)
```

### Slicing Sprite Sheets

```csharp
// In Sprite Editor > Slice dropdown:
// - Automatic: Slice by transparent pixels
// - Grid By Cell Size: Fixed pixel size per sprite
// - Grid By Cell Count: Specific rows x columns
// - Isometric Grid: Diamond-shaped isometric sprites

// Example: Slice 4x4 sprite sheet (128x128 pixels, 32x32 per sprite)
TextureImporter importer = AssetImporter.GetAtPath("Assets/Sprites/player_sheet.png") as TextureImporter;
importer.spriteMode = SpriteMode.Multiple;
importer.spriteImportMode = SpriteImportMode.Multiple;

// Configure slicing
var texSettings = new TextureImporterSettings();
texSettings.spriteMode = (int)SpriteImportMode.Multiple;
texSettings.spriteMeshType = SpriteMeshType.Tight;
texSettings.spriteAlignment = (int)SpriteAlignment.Center;
importer.SetTextureSettings(texSettings);

// Slice as grid
 importer.spritesheet = new Sprite[16];
```

### Sprite Pivots

```csharp
// Pivot affects rotation origin and sorting position
// Options: Center, Top, Bottom, Left, Right, TopLeft, TopRight, BottomLeft, BottomRight, Custom

// Custom pivot in pixels (from bottom-left)
var spriteData = new SpriteMetaData
{
    pivot = new Vector2(0.5f, 0f), // Bottom-center (good for characters standing on ground)
    alignment = (int)SpriteAlignment.Custom
};
```

### Secondary Textures (Normal Maps, Mask Maps)

```csharp
// Add secondary textures via Sprite Editor > Secondary Textures tab
// Common names:
// - _NormalMap: Normal map for lighting
// - _MaskTex: Mask for light reception (R=Metalness, G=Emission, B=Smoothness, A=Occlusion)

// Configure in URP Material with Sprite Atlas
// The material must support secondary textures
```

## Sprite Renderer

### Core Properties

```csharp
SpriteRenderer sr = GetComponent<SpriteRenderer>();

// Sprite reference
sr.sprite = mySprite;

// Color tint (multiplies with sprite colors)
sr.color = Color.white;        // No tint
sr.color = new Color(1f, 0.5f, 0.5f); // Red tint

// Flip sprite (doesn't move transform)
sr.flipX = false;
sr.flipY = false;

// Draw Mode for 9-slice (see 9-Slicing section)
sr.drawMode = SpriteDrawMode.Simple;  // Normal scaling
sr.drawMode = SpriteDrawMode.Sliced;  // 9-slice
sr.drawMode = SpriteDrawMode.Tiled;   // 9-slice with tiling

// Mask interaction (see Masking section)
sr.maskInteraction = SpriteMaskInteraction.None;
sr.maskInteraction = SpriteMaskInteraction.VisibleInsideMask;
sr.maskInteraction = SpriteMaskInteraction.VisibleOutsideMask;

// Sort point for camera distance calculation
sr.spriteSortPoint = SpriteSortPoint.Center;  // Use sprite center
sr.spriteSortPoint = SpriteSortPoint.Pivot;   // Use sprite pivot
```

### Sorting and Layering

```csharp
// Sorting Layer controls render priority between sprites
sr.sortingLayerName = "Default";          // Layer name
sr.sortingLayerID = 0;                    // Layer ID (faster)

// Order in Layer within same Sorting Layer
sr.sortingOrder = 0;                      // Lower = rendered first (behind)

// Rendering Layer Mask (URP)
sr.renderingLayerMask = 1u << 0;          // Default rendering layer
```

### Transparency Sort Mode (Y-sorting)

```csharp
// Configure in: Edit > Project Settings > Graphics > Transparency Sort Mode
// Or via script:

GraphicsSettings.transparencySortMode = TransparencySortMode.CustomAxis;
GraphicsSettings.transparencySortAxis = new Vector3(0, 1, 0); // Sort by Y axis

// Common 2D setup: Higher Y = rendered behind
// This makes sprites lower on screen appear in front (platformer perspective)
```

### Change Sprite at Runtime

```csharp
// Simple sprite swap
sr.sprite = sprites[frameIndex];

// Animated sprite (frame-by-frame)
public class SpriteAnimator : MonoBehaviour
{
    [SerializeField] private Sprite[] frames;
    [SerializeField] private float frameRate = 12f;
    private SpriteRenderer _sr;
    private float _timer;

    private void Awake() => _sr = GetComponent<SpriteRenderer>();

    private void Update()
    {
        _timer += Time.deltaTime;
        int frame = Mathf.FloorToInt(_timer * frameRate) % frames.Length;
        _sr.sprite = frames[frame];
    }
}
```

## Sprite Atlas

### Creating a Sprite Atlas

```csharp
// Assets > Create > 2D > Sprite Atlas
// Creates .spriteatlasv2 file

// Or via script:
AssetDatabase.CreateAsset(ScriptableObject.CreateInstance<SpriteAtlas>(), "Assets/Atlases/GameAtlas.spriteatlasv2");
```

### Atlas Configuration

```csharp
// In Sprite Atlas Inspector:

// Type
// - Master: Primary atlas (default)
// - Variant: Lower-resolution version of a Master atlas

// Include in Build: Enable to auto-load at runtime
// Disable to manually load via SpriteAtlasManager

// Packing
// - Allow Rotation: Rotate sprites for better packing (disable for UI)
// - Tight Packing: Use sprite outline vs rectangle
// - Alpha Dilation: Expand edge colors into transparent pixels
// - Padding: Pixels between sprites (default 4)

// Texture Settings
// - Read/Write: Enable only if reading pixel data via script
// - Generate Mip Maps: For LOD or minification
// - sRGB: Color space (enable for color textures)
// - Filter Mode: Point (pixelated), Bilinear (blurry), Trilinear (mip blend)
```

### Adding Sprites to Atlas

```csharp
// Via Editor: Drag sprites/textures/folders onto "Objects for Packing" in Inspector

// Via script (Editor only):
SpriteAtlas atlas = AssetDatabase.LoadAssetAtPath<SpriteAtlas>("Assets/Atlases/GameAtlas.spriteatlasv2");
atlas.Add(new[] { mySprite }, typeof(Sprite));
atlas.Remove(new[] { mySprite });
atlas.Compile();

// Call Pack Preview to see the result
```

### Runtime Loading

```csharp
// Automatic (default): Atlas included in build, auto-loaded
// Manual loading via callback:

SpriteAtlasManager.atlasRequested += (tag, callback) =>
{
    var atlas = Resources.Load<SpriteAtlas>(tag);
    callback?.Invoke(atlas);
};

// Tag must match the atlas's "Include in Build" or be in Resources
```

### Variant Atlases

```csharp
// Create variant for different resolutions
// Variant inherits sprites from Master atlas at reduced resolution

// Master Atlas
var master = AssetDatabase.LoadAssetAtPath<SpriteAtlas>("Assets/Atlases/Master.spriteatlasv2");

// Variant Atlas (set Type to Variant in Inspector)
// Scale 0.5 = half resolution of master
// Variant's sprites are auto-generated from master sprites
```

### Atlas Performance Tips

```csharp
// 1. Separate atlases for different scenes (load only what's needed)
atlas.GetDependencies(); // Check what sprites are in atlas

// 2. Match compression to sprite detail level
// High quality for characters, normal for environment

// 3. Disable Read/Write unless needed
// Enabling creates duplicate texture in memory

// 4. Use Tight Packing to reduce waste
// Especially for non-rectangular sprites

// 5. Avoid adding same sprite to multiple atlases
// Unity randomly picks one at runtime
```

## Tilemap System

### Tilemap Types

| Type | Use Case | Grid Layout |
|------|----------|------------|
| Rectangular | Standard 2D games | Rectangle cells |
| Hexagonal Point Top | Strategy, RPG | Diamond, point at top |
| Hexagonal Flat Top | Strategy, RPG | Diamond, flat at top |
| Isometric | RPG, tactics | Rhombus cells |
| Isometric Z as Y | Height simulation | Z converts to Y |

```csharp
// Create via: GameObject > 2D Object > Tilemap
// Or via script:
Grid grid = new GameObject("Grid").AddComponent<Grid>();
Tilemap tilemap = new GameObject("Tilemap").AddComponent<Tilemap>();
tilemap.transform.SetParent(grid.transform);

// Different tilemap types use different Grid Cell Layouts
grid.cellLayout = GridLayout.CellLayout.Rectangle;
grid.cellLayout = GridLayout.CellLayout.Hexagon;       // Point or flat top
grid.cellLayout = GridLayout.CellLayout.Isometric;
grid.cellLayout = GridLayout.CellLayout.IsometricZAsY;
```

### Grid Component

```csharp
Grid grid = GetComponent<Grid>();

// Cell Size (world units per cell)
grid.cellSize = new Vector3(1f, 1f, 0f);  // 1x1 unit cells

// Cell Gap (spacing between cells)
grid.cellGap = Vector3.zero;

// Cell Swizzle (axis reordering for coordinate conversion)
// Default: XYZ - standard Unity coordinates
// For isometric games, you might use XZY or YXZ
grid.cellSwizzle = GridLayout.CellSwizzle.XYZ;
```

### Tile Assets

```csharp
// Tile = Sprite + Color + Collider Type
// Create via: Assets > Create > 2D > Tiles

// Tile properties:
// - Sprite: The image to render
// - Color: Tint color (white = no tint)
// - Collider Type: None, Sprite (custom outline), Grid (cell shape)

// Tile usage:
Tilemap tilemap = GetComponent<Tilemap>();
tilemap.SetTile(new Vector3Int(x, y, 0), myTile);      // Place tile
tilemap.GetTile<Tile>(new Vector3Int(x, y, 0));        // Get tile
tilemap.DeleteTile(new Vector3Int(x, y, 0));            // Remove tile

// Batch operations for performance
tilemap.SetTilesBlock(bounds, tiles);                   // Set many tiles
tilemap.GetTilesBlock(bounds);                          // Get tiles in area
```

### Tile Palette

```csharp
// Window > 2D > Tile Palette
// Tools:
// - Paint: Draw tiles
// - Select: Select placed tiles
// - Move: Move tiles between tilemaps
// - Fill: Fill area with tile
// - Eraser: Remove tiles
// - Flood Fill: Replace all tiles of same type

// Brush types (2D Tilemap Extras):
// - Default Brush: Standard painting
// - Random Brush: Random tile from set
// - Line Brush: Draw tile lines
// - Group Brush: Paint groups of tiles
// - GameObject Brush: Place GameObjects
```

### Scriptable Tiles

```csharp
// Custom tile behavior by extending TileBase
public class AnimatedTile : TileBase
{
    public Sprite[] sprites;
    public float speed = 1f;

    public override void GetTileData(Vector3Int position, ITilemap tilemap, ref TileData tileData)
    {
        tileData.sprite = sprites[Mathf.FloorToInt(Time.time * speed) % sprites.Length];
        tileData.color = Color.white;
        tileData.transform = Matrix4x4.identity;
        tileData.flags = TileFlags.LockTransform;
        tileData.colliderType = Tile.ColliderType.Sprite;
    }

    public override bool GetTileAnimationData(Vector3Int position, ITilemap tilemap, ref TileAnimationData data)
    {
        if (sprites.Length > 1)
        {
            data.animatedSprites = sprites;
            data.animationSpeed = speed;
            return true;
        }
        return false;
    }
}
```

### Scriptable Brushes

```csharp
// Custom brush behavior by extending GridBrushBase
public class LineBrush : GridBrush
{
    public bool lineStartActive = false;
    public Vector3Int lineStart = Vector3Int.zero;

    public override void Paint(GridLayout grid, GameObject brushTarget, Vector3Int position)
    {
        if (lineStartActive)
        {
            // Draw line from start to position
            Vector2Int start = new Vector2Int(lineStart.x, lineStart.y);
            Vector2Int end = new Vector2Int(position.x, position.y);
            foreach (var point in GetPointsOnLine(start, end))
            {
                Vector3Int paintPos = new Vector3Int(point.x, point.y, position.z);
                base.Paint(grid, brushTarget, paintPos);
            }
            lineStartActive = false;
        }
        else
        {
            lineStart = position;
            lineStartActive = true;
        }
    }
}

// Register with attribute for Editor integration
[CustomGridBrush(true, false, false, "Line Brush")]
public class LineBrush : GridBrush { ... }
```

### Tilemap Renderer

```csharp
TilemapRenderer renderer = GetComponent<TilemapRenderer>();

// Render Mode
renderer.mode = TilemapRenderer.Mode.Chunk;    // Batch by location/texture (best perf)
renderer.mode = TilemapRenderer.Mode.Individual; // Each tile sorted individually
renderer.mode = TilemapRenderer.Mode.SRPBatch;   // For SRP Batcher compatibility

// Sort Order (direction tiles are sorted)
renderer.sortOrder = TilemapRenderer.SortOrder.TopRight;   // etc.

// Chunk Culling
renderer.chunkCullingBounds = new Vector3(5, 5, 5); // Extend culling bounds

// Mask Interaction
renderer.maskInteraction = SpriteMaskInteraction.None;
renderer.maskInteraction = SpriteMaskInteraction.VisibleInsideMask;
renderer.maskInteraction = SpriteMaskInteraction.VisibleOutsideMask;

// Materials
renderer.material = myMaterial;  // Default: Sprite-Lit-Default (URP)
```

### Tilemap Collider 2D

```csharp
// Add to tilemap GameObject for collision detection
TilemapCollider2D collider = tilemapGameObject.AddComponent<TilemapCollider2D>();

// Performance: Add Composite Collider to merge neighboring colliders
CompositeCollider2D composite = tilemapGameObject.AddComponent<CompositeCollider2D>();
composite.geometryType = CompositeCollider2D.GeometryType.Polygons;
composite.generationType = CompositeCollider2D.GenerationType.Manual;

// Must add Rigidbody2D (Static) to parent Grid for proper physics
Rigidbody2D rb = gridGameObject.AddComponent<Rigidbody2D>();
rb.bodyType = RigidbodyType2D.Static;

// Update collider shapes manually (for runtime tile changes)
if (collider.hasTilemapChanges)
{
    collider.ProcessTilemapChanges();
}
```

### Collider Type per Tile

```csharp
// Tile asset's Collider Type determines collision shape:

// None: No collider for this tile
// Sprite: Uses sprite's Custom Physics Shape
// Grid: Uses cell shape (rectangle, hexagon, etc.)

// Set in Tile asset Inspector, or via script:
Tile tile = ScriptableObject.CreateInstance<Tile>();
tile.sprite = mySprite;
tile.colliderType = Tile.ColliderType.Sprite;  // Use custom outline
tile.colliderType = Tile.ColliderType.Grid;    // Use cell shape
tile.colliderType = Tile.ColliderType.None;    // No collision
```

### Hexagonal Tilemap Coordinates

```csharp
// Hexagonal grids use offset coordinate system
// Point Top: Odd rows offset right by half cell width
// Flat Top: Odd columns offset up by half cell height

// Convert world position to hex coordinates
Vector3 worldPos = transform.position;
Vector3Int hexPos = tilemap.WorldToCell(worldPos);

// For offset systems, adjust:
// Point Top odd row offset:
if (hexPos.y % 2 == 1) hexPos.x += 1;  // Adjust for odd row

// Hex distance calculation
int HexDistance(Vector3Int a, Vector3Int b)
{
    return (Mathf.Abs(a.x - b.x) + Mathf.Abs(a.y - b.y) + Mathf.Abs(a.x + a.y - b.x - b.y)) / 2;
}
```

### Isometric Tilemap

```csharp
// Isometric: X+Y+Z = constant for each height level
// Z as Y: Z position converts to local Y (for height simulation)

// Cell to world conversion
Vector3 worldPos = grid.CellToWorld(new Vector3Int(x, y, z));

// For Z as Y isometric:
Vector3 isoPos = grid.CellToWorld(new Vector3Int(x, y, 0));
isoPos.y = z;  // Use Z as height

// Custom sorting axis for proper depth
renderer.sortOrder = TilemapRenderer.SortOrder.Custom;
GraphicsSettings.transparencySortMode = TransparencySortMode.CustomAxis;
GraphicsSettings.transparencySortAxis = new Vector3(0, 1, 1); // Diagonal for isometric
```

## 2D Lighting (URP)

### Light 2D Component

```csharp
// Add via: GameObject > Light > 2D > Freeform Light 2D
// Or: GameObject > Light > 2D > Sprite Light 2D

Light2D light = GetComponent<Light2D>();

// Light type
light.lightType = Light2D.LightType.Freeform;
light.lightType = Light2D.LightType.Sprite;
light.lightType = Light2D.LightType.Parametric;  // Shape: Hexagon, Diamond, Circle
light.lightType = Light2D.LightType.Point;

// Blending
light.blendingMode = Light2D.BlendingMode.Additive;     // Brighten
light.blendingMode = Light2D.BlendingMode.Mix;           // Soft light

// Color and intensity
light.color = Color.white;
light.intensity = 1f;

// Volume shadow settings
light.shadowVolumeIntensity = 0f;  // 0-1, how dark shadows are inside volume
light.shadowVolumeIntensity = 0.5f;
```

### Shadow Caster 2D

```csharp
// Add ShadowCaster2D to sprites that should cast shadows

ShadowCaster2D shadow = spriteGameObject.AddComponent<ShadowCExtension>();
shadow.shadowVolumeIntensity = 1f;  // Fully opaque shadow

// Use "Self" shadows (shadows from own shape)
// Or use "World" shadows (projected based on light position)

// For tilemap shadows:
// Add ShadowCaster2D to tilemap renderer GameObject
// It automatically casts shadows based on sprites
```

### Configuring Sprites for 2D Lighting

```csharp
// Sprites need Secondary Textures for proper lighting:
// 1. Open Sprite Editor > Secondary Textures
// 2. Add _NormalMap (normal map) and/or _MaskTex (mask)

// Or via script:
TextureImporter importer = AssetImporter.GetAtPath("Assets/Sprites/player.png") as TextureImporter;
var secondaryTextures = new SecondaryTexture[] {
    new SecondaryTexture { name = "_NormalMap", texture = normalMap }
};
importer.secondaryTextures = secondaryTextures;

// URP Material must have "Include Input" enabled for each secondary texture
```

### Light 2D with Sprite Masks

```csharp
// Light only affects sprites inside certain layers
light.cullingLayers = LayerMask.GetMask("Player", "Environment");

// Or use sorting layer ranges
light.volumeOpacity = 0.5f;  // Affects how shadows fade

// Combine with Sprite Mask for visibility control
// Sprites can only receive light if they interact with the mask
sr.maskInteraction = SpriteMaskInteraction.VisibleInsideMask;
// Now this sprite is only lit when inside the mask
```

### Practical 2D Lighting Setup

```csharp
// 1. Set up URP with 2D rendering:
// - Install 2D Renderer (URP asset > Renderer List > Add 2D Renderer)

// 2. Create lights per "layer" of your scene:
// - Background layer lights
// - Character layer lights
// - Foreground effects lights

// 3. Configure shadow casters:
// - Add ShadowCaster2D to all light-blocking objects
// - Use self-shadows for simple setups
// - Use world-shadows for projected shadows

// 4. Light optimization:
// - Limit number of lights affecting each sprite
// - Use culling layers to isolate light groups
```

## 9-Slicing

### When to Use 9-Slicing

- UI panels, windows, buttons with borders
- Ground/platform tiles that stretch but keep corners
- Speech bubbles, tooltips, inventory slots
- Any sprite that needs to resize without distortion

### Sprite Setup for 9-Slice

```csharp
// In Sprite Editor, set Border values (L, R, T, B in pixels):
// L=10, R=10, T=10, B=10 means:
// - Corners stay 10x10 pixels
// - Edges stretch in one direction
// - Center stretches in both

// Or via script when importing:
TextureImporter importer = AssetImporter.GetPath("Assets/Sprites/panel.png");
var spriteData = new SpriteMetaData
{
    border = new Vector4(10f, 10f, 10f, 10f),  // L, R, T, B
};
```

### Sprite Renderer Draw Mode

```csharp
SpriteRenderer sr = GetComponent<SpriteRenderer>();

// Simple: Normal scaling (no 9-slice)
sr.drawMode = SpriteDrawMode.Simple;

// Sliced: 9-slice scaling
sr.drawMode = SpriteDrawMode.Sliced;
sr.size = new Vector2(4f, 2f);  // New dimensions in world units

// Tiled: 9-slice with tiling middle
sr.drawMode = SpriteDrawMode.Tiled;
sr.size = new Vector2(8f, 4f);  // Larger than sprite = tiled middle
```

### Tiled Mode Details

```csharp
// Tiled mode has two tile modes:
sr.tileMode = SpriteTileMode.Continuous;  // Middle tiles evenly
sr.tileMode = SpriteTileMode.Adaptive;    // Stretch until threshold, then tile

// Adaptive mode has stretch value:
sr.adaptiveThresholdThreshold = 0.5f;  // 0-1, when to start tiling
// At scale 2x original, middle begins to tile
```

### 9-Slice with Colliders

```csharp
// Only BoxCollider2D and PolygonCollider2D support 9-slice
// With Auto Tiling enabled, collider updates when sprite size changes

BoxCollider2D col = GetComponent<BoxCollider2D>();
col.autoTiling = true;  // Collider follows sprite size (Sliced/Tiled mode)

// ❌ Can't manually edit collider when Sprite Renderer is Sliced/Tiled
// Inspector shows warning: "Collider is driven by Tile"

PolygonCollider2D polyCol = GetComponent<PolygonCollider2D>();
polyCol.autoTiling = true;
```

### 9-Slice Limitations

| Limitation | Description |
|------------|-------------|
| Collider support | Only BoxCollider2D and PolygonCollider2D |
| Manual editing | Disabled when Draw Mode is Sliced/Tiled |
| Auto Tiling side effects | May add edges within shape during regeneration |

## Sprite Masks

### Mask Concept

Sprite masks hide or reveal parts of sprites based on alpha. Sprites outside the mask are invisible (Visible Inside) or visible (Visible Outside).

### Basic Mask Setup

```csharp
// 1. Create Sprite Mask (GameObject > 2D Object > Sprite Mask)
SpriteMask mask = GetComponent<SpriteMask>();

// Mask uses sprite shape as the mask
mask.sprite = maskSprite;  // Shape of the mask
mask.alphaCutoff = 0.1f;   // Minimum alpha to be considered mask

// 2. Configure sprites to be masked
SpriteRenderer sr = GetComponent<SpriteRenderer>();
sr.maskInteraction = SpriteMaskInteraction.VisibleInsideMask;  // Hide outside mask
sr.maskInteraction = SpriteMaskInteraction.VisibleOutsideMask; // Hide inside mask
```

### Mask Properties

```csharp
SpriteMask mask = GetComponent<SpriteMask>();

// Mask source: Sprite or Renderer
mask.maskSource = SpriteMaskSource.Sprite;         // Use sprite
mask.maskSource = SpriteMaskSource.SupportedRenderer; // Use renderer's sprite

// Alpha cutoff threshold
mask.alphaCutoff = 0.5f;  // Higher = more transparent areas excluded

// Custom range: Only affect certain sorting layers
mask.customRange = true;
mask.frontSortingLayer = 5;   // Highest layer affected
mask.frontSortingOrder = 10; // Highest order affected
mask.backSortingLayer = 3;   // Lowest layer not affected
mask.backSortingOrder = 5;

// Rendering layer mask (URP)
mask.renderingLayers = 1u << 0;  // Affect specific rendering layers
```

### Practical Mask Uses

```csharp
// 1. Reveal character behind walls:
public class WallReveal : MonoBehaviour
{
    [SerializeField] private SpriteMask mask;
    [SerializeField] private Transform player;

    private void Update()
    {
        // Mask follows player position
        mask.transform.position = player.position;
    }
}

// 2. Inventory slot highlight:
public class InventorySlot : MonoBehaviour
{
    [SerializeField] private SpriteMask slotMask;
    [SerializeField] private SpriteRenderer itemRenderer;

    private void Start()
    {
        itemRenderer.maskInteraction = SpriteMaskInteraction.VisibleInsideMask;
    }

    public void Select() { slotMask.gameObject.SetActive(true); }
    public void Deselect() { slotMask.gameObject.SetActive(false); }
}
```

## Sorting Groups

### Why Sorting Groups

When using multi-sprite characters (body parts as separate sprites), sorting by individual Order in Layer causes different prefab instances to overlap incorrectly.

```csharp
// ❌ WITHOUT Sorting Group:
// Each prefab instance sorts independently
// Two characters' body parts can interleave incorrectly

// ✅ WITH Sorting Group:
// All parts of one character sort as a unit
// Each character's parts stay together
```

### Sorting Group Component

```csharp
SortingGroup sg = GetComponent<SortingGroup>();

// All child Sprite Renderers now sort together
sg.sortingLayerName = "Characters";
sg.sortingOrder = 0;  // Priority within layer
sg.rendererPriority = 0;  // Queue priority

// Or set via hierarchy:
// Sorting Group on root, all sprite renderers as children
```

### Multi-Sprite Character Setup

```csharp
// Character hierarchy:
// Character (Sorting Group, Order = 0)
//   ├─ Body (SpriteRenderer, Order = 0)
//   ├─ Head (SpriteRenderer, Order = 1)
//   ├─ Weapon (SpriteRenderer, Order = 2)
//   └─ Cape (SpriteRenderer, Order = -1)

// Each character instance needs unique Order in Layer
// Set via script when spawning:
public class Character : MonoBehaviour
{
    [SerializeField] private int instanceId;

    private void Awake()
    {
        GetComponent<SortingGroup>().sortingOrder = instanceId;
    }
}
```

## Common Mistakes to Prevent

| Mistake | Problem | Solution |
|---------|---------|----------|
| Transform.position on physics object | Teleports, misses collisions | Use Rigidbody2D.MovePosition |
| Sprite in multiple atlases | Random atlas selected | Assign to one atlas only |
| No Sprite Atlas | Excessive draw calls | Pack sprites into atlas |
| Wrong Pivot for character | Odd rotation behavior | Set pivot at feet or center |
| Forgetting Static Rigidbody | Tilemap doesn't collide | Add Rigidbody2D Static to Grid |
| Manual collider edit with 9-slice | Can't edit, shows warning | Disable Auto Tiling or don't use Sliced |
| Z-fighting on tilemaps | Flickering tiles | Set different Order in Layer per tilemap |
| Wrong Transparency Sort Mode | Sprites sort incorrectly | Set Custom Axis Y=1 for 2D |
| Missing 2D Tilemap package | No Tilemap menu | Install 2D Tilemap Editor via Package Manager |
| Sprite Mask not affecting sprite | Different sorting layers | Ensure sprite and mask share sorting layers |

## Response Format

When answering Unity 2D questions:

1. **Code-first**: Always provide fully compilable C# examples
2. **Explain the "why"**: Not just what, but why this approach
3. **Show alternatives**: When there's trade-off, mention it
4. **Reference docs**: Link to skill/reference/ source files for deep dives
5. **Cross-reference**: Mention `unity-physics` for 2D physics questions

### Template for Code Answers

```csharp
// Brief explanation of what this does
// Why this approach is correct

// ❌ WRONG approach (and why)
someBrokenCode();

// ✅ CORRECT approach
public class MyComponent : MonoBehaviour
{
    [SerializeField] private int exampleField;

    private void Start()
    {
        // Clear explanation of what happens here
        DoSomething();
    }

    private void DoSomething()
    {
        // Implementation with explanation
    }
}

// Performance note (if applicable)
// "This creates N allocations. For hot paths, consider..."
```

### Template for Architecture Questions

```
Architecture: [Pattern Name]

Problem: [What issue this solves]

Approach:
1. [First step]
2. [Second step]
3. [Third step]

Trade-offs:
- Pro: [Advantage]
- Con: [Disadvantage]

Related: [Cross-references to other skills or docs]
```

(End of file - total 1023 lines)
