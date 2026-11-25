---
name: unity-performance
description: >
  Unity 6000.3 LTS performance optimization patterns. Covers Profiler usage,
  memory management, GPU instancing, SRP Batcher, and script optimization.
  Trigger: When optimizing performance, profiling, reducing memory usage,
  or improving frame rate in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Profiling game performance or finding bottlenecks
- Reducing memory usage or fixing allocations
- Optimizing rendering (GPU instancing, SRP Batcher, draw calls)
- Improving CPU performance (physics, scripts, garbage collection)
- Setting up performance-critical code patterns
- Using Unity Profiler, Memory Profiler, or Frame Debugger
- Working with Scriptable Render Pipeline (URP/HDRP) optimization

## Critical Rules

### Always Profile Before Optimizing

```csharp
// ❌ WRONG — Optimize blindly without measurement
void Update()
{
    for (int i = 0; i < 1000; i++)
    {
        Instantiate(prefab, Vector3.zero, Quaternion.identity);
    }
}

// ✅ CORRECT — Use Profiler to identify the actual bottleneck first
void Update()
{
    // Wrap critical sections to see exact cost in Profiler
    Profiler.BeginSample("MyCriticalSection");
    // ... code to measure ...
    Profiler.EndSample();
}
```

**Why:** Premature optimization wastes time on code that isn't the bottleneck. Always measure first.

### Memory Allocation is Not Free

```csharp
// ❌ WRONG — Allocating every frame (GC pressure)
void Update()
{
    var name = $"Player_{playerId}";  // String allocation
    var vector = new Vector3(x, y, z); // Class allocation
    var list = new List<int>();        // Collection allocation
}

// ✅ CORRECT — Reuse buffers, avoid per-frame allocations
private StringBuilder _sb = new();
private Vector3 _velocity;              // Struct on stack, no allocation
private List<int> _cache = new();      // Reuse list, clear when needed

void Update()
{
    _sb.Clear();
    _sb.Append("Player_");
    _sb.Append(playerId);
    string name = _sb.ToString();      // Reuses StringBuilder buffer

    _velocity.Set(x, y, z);            // No allocation, mutates existing
    // Use ObjectPool for per-frame spawn/despawn
}
```

**Why:** GC allocations trigger garbage collection, causing frame hitches. Every allocation has a cost.

### Don't Optimize What Users Can't See

```csharp
// ❌ WRONG — Over-optimize distant objects
void Update()
{
    foreach (var obj in allObjects)
    {
        float dist = Vector3.Distance(obj.transform.position, Camera.main.transform.position);
        if (dist < 1000f)
        {
            // Do complex LOD calculation every frame
        }
    }
}

// ✅ CORRECT — Let the engine handle culling naturally
void Update()
{
    // Objects outside camera frustum are already culled
    // Use LOD system instead of manual distance checks
}
```

**Why:** User perceives 60fps differently than 120fps. Focus optimization budget on what affects perceived quality.

## Profiler Usage

### Profiler window Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+P | Open Profiler |
| Ctrl+Shift+C | Clear frames |
| Ctrl+Shift+H | Deep profile (samples everything) |
| Home/End | Navigate timeline |
| Click+drag | Zoom timeline |

### CPU Profiler Sections

```
CPU:
├── Main Thread
│   ├── PlayerLoop (fixed and dynamic update)
│   ├── Rendering (DrawCalls, DynamicResolution)
│   └── Scripts (Your MonoBehaviour code)
├── Render Thread
│   └── GPU work submission
└── job system (Worker threads)
```

### Sampling and Marking Code

```csharp
// Mark sections in Profiler for clarity
public class PerformanceExample : MonoBehaviour
{
    private void Update()
    {
        Profiler.BeginSample("Physics Calculations");
        PerformPhysics();
        Profiler.EndSample();

        Profiler.BeginSample("AI Logic");
        PerformAI();
        Profiler.EndSample();

        Profiler.BeginSample("VFX Spawning");
        SpawnEffects();
        Profiler.EndSample();
    }

    void PerformPhysics() { /* ... */ }
    void PerformAI() { /* ... */ }
    void SpawnEffects() { /* ... */ }
}
```

### Timeline vs Hierarchy View

**Timeline:** Shows WHEN things happen (threading, overlapping work)
**Hierarchy:** Shows WHO消耗最多 (aggregated time per function)

```csharp
// Use Timeline view to find:
// - Long GCs causing spikes
// - Unnecessary syncs (WaitForJobHandle)
// - Thread load imbalance

// Use Hierarchy view to find:
// - Expensive specific functions
// - Hidden allocations (Hidden = GC.Alloc)
```

### Memory Profiler Integration

```csharp
// Take Memory Profiler snapshot
// Use Memory Profiler window: Window > Analysis > Memory Profiler

// Key views:
// - Allocated: What's currently in memory
// - Reserved: What's reserved (may be more than allocated)
// - No GC Alloc: Memory that doesn't trigger GC
```

### Custom Profiler Counters

```csharp
// Register custom counter for runtime analysis
using Unity.Profiling;

private static readonly ProfilerCounterValue<int> ActiveBullets =
    new ProfilerCounterValue<int>(ProfilerCategory.Internal, "Active Bullets",
        ProfilerMarkerDataUnit.Count);

void Update()
{
    ActiveBullets.Value = _activeBulletCount;
}
```

### GPU Profiler Reading

```csharp
// GPU Profiler shows:
// - MSAA cost (if enabled)
// - Render pass timing
// - Bandwidth usage
// - Shader complexity

// Check "Recursive rendering" in Frame Debugger
// Disable it by ensuring no object renders itself as a reflection
```

## Memory Management

### Stack vs Heap Allocation

```csharp
// STRUCTS (stack, no GC) — use for temporary data
struct WeaponStats
{
    public int Damage;
    public float Range;
    public string Name; // Reference type, still heap
}

// CLASSES (heap, GC pressure) — use for persistent objects
class Weapon
{
    public int Damage;
    public float Range;
    public string Name;
}

// ✅ CORRECT — Struct for per-frame calculations
Vector3 CalculateDirection(Vector3 from, Vector3 to)
{
    Vector3 dir = to - from; // No allocation, stack
    dir.Normalize();
    return dir;
}

// ❌ WRONG — Class for frequent temporary creation
Vector3 CalculateDirection(Vector3 from, Vector3 to)
{
    return new Vector3(to.x - from.x, to.y - from.y, to.z - from.z);
}
```

### Object Pool Pattern

```csharp
// Essential for frequently spawned objects (projectiles, particles, VFX)
public class ObjectPool<T> where T : MonoBehaviour
{
    private readonly Queue<T> _pool = new();
    private readonly T _prefab;
    private readonly int _initialSize;

    public ObjectPool(T prefab, int initialSize = 20)
    {
        _prefab = prefab;
        _initialSize = initialSize;

        // Pre-warm pool
        for (int i = 0; i < initialSize; i++)
        {
            var obj = Object.Instantiate(prefab);
            obj.gameObject.SetActive(false);
            _pool.Enqueue(obj);
        }
    }

    public T Get(Vector3 position, Quaternion rotation)
    {
        T obj;
        if (_pool.Count > 0)
        {
            obj = _pool.Dequeue();
        }
        else
        {
            obj = Object.Instantiate(_prefab);
        }

        obj.transform.SetPositionAndRotation(position, rotation);
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }
}

// Usage
public class ProjectilePool : MonoBehaviour
{
    private ObjectPool<Projectile> _pool;

    private void Start()
    {
        var prefab = Resources.Load<Projectile>("Prefabs/Projectile");
        _pool = new ObjectPool<Projectile>(prefab, 50);
    }

    public void Fire(Vector3 position, Quaternion rotation)
    {
        var proj = _pool.Get(position, rotation);
        proj.OnHit += HandleHit; // Subscribe before firing
    }

    private void HandleHit(Projectile p)
    {
        _pool.Return(p); // Return to pool on hit
    }
}
```

### Native Collections (No GC)

```csharp
// Use NativeArray, NativeList for data that persists across frames
using Unity.Collections;

public class SpatialHashGrid : MonoBehaviour
{
    private NativeParallelMultiHashMap<int, int> _grid;
    private NativeArray<RaycastCommand> _raycasts;

    private void Awake()
    {
        // Allocate native collections (no GC, must dispose)
        _grid = new NativeParallelMultiHashMap<int, int>(1000, Allocator.Persistent);
        _raycasts = new NativeArray<RaycastCommand>(256, Allocator.Persistent);
    }

    private void OnDestroy()
    {
        // CRITICAL: Dispose native collections to prevent leaks
        _grid.Dispose();
        _raycasts.Dispose();
    }

    // Access via Jobs for multithreading
}

// Using Jobs with NativeArray
public struct RaycastJob : IJobParallelFor
{
    public NativeArray<RaycastCommand> Commands;
    public NativeArray<RaycastHit> Results;

    public void Execute(int index)
    {
        RaycastCommand command = Commands[index];
        // Execute raycast at index - runs on worker threads
    }
}
```

### Memory Profiling Tips

```csharp
// Check for hidden allocations in Hot Path profiling
// Look for: gc Alloc in Hierarchy view (red marks allocations)

// Common hidden allocators:
// - LINQ (where, select, tolist)
// - String concatenation in loops
// - foreach on arrays (uses enumerator struct, but captures)
// - Box operation

// ❌ Hidden allocation: LINQ
var enemies = GameObject.FindGameObjectsWithTag("Enemy")
    .Where(e => e.activeSelf)
    .Select(e => e.GetComponent<Health>())
    .ToList();

// ✅ No allocation: Manual loop
List<Health> enemies = new List<Health>();
foreach (var go in GameObject.FindGameObjectsWithTag("Enemy"))
{
    if (go.activeSelf)
        enemies.Add(go.GetComponent<Health>());
}
```

### Texture Memory

```csharp
// Check texture memory in Profiler > Memory > Texture Memory
// Use appropriate compression per platform

public class TextureSettings : MonoBehaviour
{
    [SerializeField] private TextureImporterCompression _compression =
        TextureImporterCompression.Compressed;

    [ContextMenu("Optimize All Textures")]
    void OptimizeAllTextures()
    {
        string[] guids = AssetDatabase.FindAssets("t:Texture", new[] { "Assets" });
        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            var importer = AssetImporter.GetAtPath(path) as TextureImporter;

            importer.textureCompression = TextureImporterCompression.Compressed;
            importer.maxTextureSize = 2048; // Cap maximum size
            importer.mipmapEnabled = true;  // Use mipmaps for GPU
            importer.sRGBTexture = true;    // Color texture flag

            AssetDatabase.ImportAsset(path);
        }
    }
}

// Unity 6000: Check texture streaming budget
void ConfigureTextureStreaming()
{
    QualitySettings.streamingMipmapsActive = true;
    QualitySettings.streamingMipmapsMemoryBudget = 512; // MB
    TextureStreamingManager.enabled = true;
}
```

## GPU Optimization

### GPU Instancing

```csharp
// Use instancing for many identical objects (trees, rocks, debris)
// Automatically batched by SRP Batcher if materials match

public class InstancedRenderer : MonoBehaviour
{
    [SerializeField] private Mesh _mesh;
    [SerializeField] private Material _material;
    private const int MAX_INSTANCES = 500;

    private Matrix4x4[] _matrices = new Matrix4x4[MAX_INSTANCES];
    private Vector4[] _colors = new Vector4[MAX_INSTANCES];

    private ComputeBuffer _matrixBuffer;
    private ComputeBuffer _colorBuffer;

    private void Start()
    {
        // Create GPU buffers (avoid per-frame allocation)
        _matrixBuffer = new ComputeBuffer(MAX_INSTANCES, sizeof(float) * 16);
        _colorBuffer = new ComputeBuffer(MAX_INSTANCES, sizeof(float) * 4);
    }

    private void OnDestroy()
    {
        _matrixBuffer?.Release();
        _colorBuffer?.Release();
    }

    private void Update()
    {
        // Update instance data
        for (int i = 0; i < _instanceCount; i++)
        {
            _matrices[i] = Matrix4x4.TRS(_positions[i], _rotations[i], _scales[i]);
            _colors[i] = _instanceColors[i].ToVector4();
        }

        _matrixBuffer.SetData(_matrices, 0, 0, _instanceCount);
        _colorBuffer.SetData(_colors, 0, 0, _instanceCount);

        // Set shader properties
        _material.SetBuffer("_InstanceMatrix", _matrixBuffer);
        _material.SetBuffer("_InstanceColor", _colorBuffer);
        _material.SetVector("_Color", Color.white);
    }

    private void OnRenderObject()
    {
        Graphics.DrawMeshInstanced(_mesh, 0, _material, _matrices, _instanceCount);
    }
}

// Shader side (HLSL)
Shader "Custom/Instanced"
{
    Properties { _Color ("Color", Color) = (1,1,1,1) }
    SubShader
    {
        Pass
        {
            HLSLPROGRAM
            #pragma instancing_optionsMarerial: _Color
            #pragma multi_compile_instancing

            StructuredBuffer<float4x4> _InstanceMatrix;
            StructuredBuffer<float4> _InstanceColor;

            struct appdata
            {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float3 normal : NORMAL;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            void vert(appdata v, uint instanceID : SV_InstanceID)
            {
                v2f o;
                float4x4 instanceMatrix = _InstanceMatrix[instanceID];
                v.vertex = mul(instanceMatrix, v.vertex);
                v.normal = UnityObjectToWorldNormal(mul(instanceMatrix, v.normal));
                o.pos = UnityWorldViewProj(v.vertex);
                UNITY_TRANSFER_INSTANCE_ID(v, o);
                o.normal = v.normal;
                return o;
            }
            ENDHLSL
        }
    }
}
```

### SRP Batcher Requirements

```csharp
// SRP Batcher automatically batches objects with same shader variant
// Requirements for SRP Batcher compatibility:

// ✅ GOOD: Constant buffer content changes slowly
// - Per-frame: camera position, time
// - Per-object: transform, color

// ❌ BAD: Per-object material properties that change every frame
// - MaterialPropertyBlock with varying values
// - Multiple materials on same GameObject

// Ensure shader uses CBUFFER properly
// Unity auto-generates CBUFFER for shader properties declared in Properties

// Check "SRP Batcher compatible" in Material inspector
// Frame Debugger shows "SRP Batcher" when batching is working
```

### Draw Call Reduction

```csharp
// 1. Static batching for non-moving objects
// MeshRenderer.lightmapIndex != -1 automatically static batched
// Or: GameObjectUtility.SetStaticEditorFlags(gameObject, StaticEditorFlags.BatchingStatic)

// 2. Dynamic batching for small objects (< 900 vertices, same material)
// Automatic in URP/HDRP when vertex count is low

// 3. GPU Instancing for many identical objects
// Graphics.DrawMeshInstanced() or shader instancing

// 4. Combine meshes at runtime for static scenery
public class MeshCombiner : MonoBehaviour
{
    [ContextMenu("Combine Meshes")]
    void CombineMeshes()
    {
        MeshFilter[] meshFilters = GetComponentsInChildren<MeshFilter>();
        CombineInstance[] combines = new CombineInstance[meshFilters.Length];

        for (int i = 0; i < meshFilters.Length; i++)
        {
            combines[i].mesh = meshFilters[i].sharedMesh;
            combines[i].transform = meshFilters[i].transform.localToWorldMatrix;
            meshFilters[i].gameObject.SetActive(false);
        }

        var combinedMesh = new Mesh();
        combinedMesh.indexFormat = IndexFormat.UInt32; // > 65k vertices
        combinedMesh.CombineMeshes(combines, true, true, true);

        var mf = gameObject.AddComponent<MeshFilter>();
        mf.sharedMesh = combinedMesh;

        var mr = gameObject.AddComponent<MeshRenderer>();
        mr.sharedMaterial = meshFilters[0].GetComponent<MeshRenderer>().sharedMaterial;
        gameObject.SetActive(true);
    }
}
```

### Shader Variants Reduction

```csharp
// Use multi_compile to control variants generated
// Instead of letting Unity generate all combinations

// Shader code
Shader "Custom/MyShader"
{
    // Generate only these keywords
    #pragma multi_compile _ USE_FOG USE_DITHER
    #pragma multi_compile _ LIGHTMAP_ON _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS

    // Don't use #pragma multi_compile_fwdbase (generates too many)
    // Instead use specific keyword groups
}

// In code, control keyword activation
void SetShaderKeywords()
{
    // Enable/disable keywords
    Material mat = GetComponent<Renderer>().material;

    // Only set keywords that shader expects
    mat.SetKeyword("_USE_FOG", _useFog);
    mat.SetKeyword("_USE_DITHER", _useDither);
}
```

## CPU Optimization

### Job System and Burst

```csharp
// Use Unity.Jobs for parallel CPU work
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;

[BurstCompile]
public struct CalculatePositionsJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float3> Velocities;
    [WriteOnly] public NativeArray<float3> Positions;
    public float DeltaTime;

    public void Execute(int index)
    {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

// Schedule from main thread
public class JobScheduler : MonoBehaviour
{
    [SerializeField] private int _elementCount = 10000;

    private NativeArray<float3> _velocities;
    private NativeArray<float3> _positions;

    private void Start()
    {
        _velocities = new NativeArray<float3>(_elementCount, Allocator.Persistent);
        _positions = new NativeArray<float3>(_elementCount, Allocator.Persistent);
    }

    private void OnDestroy()
    {
        _velocities.Dispose();
        _positions.Dispose();
    }

    private void Update()
    {
        var job = new CalculatePositionsJob
        {
            Velocities = _velocities,
            Positions = _positions,
            DeltaTime = Time.deltaTime
        };

        // Schedule for parallel execution on worker threads
        JobHandle handle = job.Schedule(_elementCount, 64); // 64 = batch size

        // Ensure completion before reading results
        handle.Complete();

        // Now safe to read from _positions
    }
}

// Combine multiple jobs
public struct CombinedJob : IJob
{
    public JobHandle Handle;

    public void Execute()
    {
        Handle.Complete();
    }
}

void ScheduleCombined()
{
    var jobA = new JobA();
    var jobB = new JobB();

    JobHandle handleA = jobA.Schedule();
    JobHandle handleB = jobB.Schedule();

    // Combine dependencies
    JobHandle.CombineDependencies(handleA, handleB);

    var combined = new CombinedJob { Handle = handleA };
    combined.Schedule();
}
```

### Physics Optimization

```csharp
// Reduce physics cost with these settings

// Edit > Project Settings > Physics
// Fixed Timestep: 0.02 (50Hz) → 0.033 (30Hz) for less critical games
// Solver Iterations: 6 → 4 for less stable but faster simulation

// Use Layer Collision Matrix to disable unnecessary collisions
// Edit > Project Settings > Physics > Layer Collision Matrix

// Raycast queries - non-allocating versions in hot paths
public class OptimizedRaycast : MonoBehaviour
{
    private RaycastHit[] _hits = new RaycastHit[10];

    private void Update()
    {
        // Non-allocating raycast
        int count = Physics.RaycastNonAlloc(
            transform.position,
            transform.forward,
            _hits,
            100f
        );

        for (int i = 0; i < count; i++)
        {
            ProcessHit(_hits[i]);
        }
    }

    // Sphere cast for character ground check
    bool CheckGround()
    {
        return Physics.SphereCast(
            transform.position + Vector3.up,
            0.5f,
            Vector3.down,
            out _,
            0.2f,
            ~0, // All layers
            QueryTriggerInteraction.Ignore
        );
    }
}
```

### Transform Operations

```csharp
// Transform operations are expensive when called frequently

// ❌ SLOW - Using transform.position in loops
void Update()
{
    for (int i = 0; i < 1000; i++)
    {
        enemies[i].transform.position += enemies[i].transform.forward * speed * Time.deltaTime;
    }
}

// ✅ FASTER - Cache transforms or use Component array
void Update()
{
    for (int i = 0; i < 1000; i++)
    {
        var enemy = enemies[i];
        var pos = enemy.transform.position;
        pos += enemy.transform.forward * speed * Time.deltaTime;
        enemy.transform.position = pos;
    }
}

// ✅ EVEN FASTER - Use position directly on TransformAccessArray (Jobs)
private TransformAccessArray _transformAccess;

void Start()
{
    _transformAccess = new TransformAccessArray(1000);
    // Add transforms to array
}

void Update()
{
    var job = new MoveEnemiesJob
    {
        Speed = speed,
        DeltaTime = Time.deltaTime
    };
    job.Schedule(_transformAccess);
}

[BurstCompile]
public struct MoveEnemiesJob : IJobParallelFor
{
    public float Speed;
    public float DeltaTime;

    [NativeDisableParallelForRestriction]
    public NativeArray<Float3> Positions;

    public void Execute(int index)
    {
        // Direct position access, no Transform component overhead
        Positions[index] += Positions[index] * Speed * DeltaTime; // Just example
    }
}
```

## Script Optimization

### Avoiding Boxed Collections

```csharp
// Array vs List vs LinkedList vs Dictionary - know when to use each

// Array (T[]): Best for sequential access, fixed size known
// - Fast iteration, no boxing, cache-friendly
// - Size must be known or resized (expensive)

// List<T>: Best for dynamic size with random access
// - Generic, no boxing
// - Slight overhead per operation vs Array

// Dictionary<TKey, TValue>: Best for lookups
// - O(1) average lookup
// - More memory overhead than array/list

// LinkedList<T>: Worst for most cases
// - O(n) lookup
// - Only good for constant insert/delete at known position

// ❌ WORST - Boxing with non-generic collections
ArrayList list = new ArrayList();
list.Add(5);        // Boxes int to object
int val = (int)list[0]; // Unboxes, causes GC

// ✅ GOOD - Generic collections
List<int> list = new List<int>();
list.Add(5);        // No boxing
int val = list[0];  // No unboxing
```

### Update Frequency Control

```csharp
// Not everything needs to update every frame

public class SlowUpdate : MonoBehaviour
{
    private float _updateInterval = 0.5f; // Every 500ms
    private float _timer;

    private void Update()
    {
        _timer += Time.deltaTime;
        if (_timer >= _updateInterval)
        {
            _timer = 0f;
            OnSlowUpdate();
        }
    }

    void OnSlowUpdate()
    {
        // AI behavior, environmental checks, etc.
    }
}

// Unity's built-in update culling
void Update()
{
    // Only update when visible (requires CullingGroup API)
}

// For particles/effects that don't need consistent timing:
// Use LateUpdate for visual-only components (runs after all Updates)
private void LateUpdate()
{
    // Camera follow, particle systems that don't affect gameplay
}
```

### Caching Component References

```csharp
// ❌ WRONG - GetComponent called repeatedly
void Update()
{
    var rb = GetComponent<Rigidbody>();           // Every frame
    var mesh = GetComponent<MeshRenderer>();       // Every frame
    var anim = GetComponent<Animator>();          // Every frame
}

// ✅ CORRECT - Cache on Start/Awake
public class PlayerController : MonoBehaviour
{
    private Rigidbody _rb;
    private MeshRenderer _mesh;
    private Animator _anim;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _mesh = GetComponent<MeshRenderer>();
        _anim = GetComponent<Animator>();
    }
}

// ✅ ALSO GOOD - SerializeField for editor assignment
[SerializeField] private Rigidbody _rb;
[SerializeField] private MeshRenderer _mesh;
```

### String Operations

```csharp
// String operations allocate heavily

// ❌ WRONG - Concatenation in loops
void Update()
{
    for (int i = 0; i < 100; i++)
    {
        var name = "Enemy_" + i; // New string each iteration
        Debug.Log(name);
    }
}

// ✅ CORRECT - StringBuilder or pre-formatting
private StringBuilder _sb = new StringBuilder(256);

void Update()
{
    for (int i = 0; i < 100; i++)
    {
        _sb.Clear();
        _sb.Append("Enemy_");
        _sb.Append(i);
        var name = _sb.ToString(); // Reuses buffer
    }
}

// For constants and debug tags - use static readonly
private static readonly string[] EnemyNames = new[]
{
    "Grunt", "Elite", "Boss", "Swarm"
};

// For formatted debug - use nameof and interpolation sparingly
string message = $"Player {playerId} took {damage} damage"; // Allocates on every call
```

### Virtual / Interface Calls

```csharp
// Virtual and interface calls have overhead vs direct calls

// ❌ POTENTIALLY SLOW - Virtual in tight loops
public interface IDamageable
{
    void TakeDamage(float amount);
}

public class DamageDealer : MonoBehaviour
{
    [SerializeField] private IDamageable[] _targets;

    private void Update()
    {
        for (int i = 0; i < _targets.Length; i++)
        {
            _targets[i].TakeDamage(_damage); // Virtual call each iteration
        }
    }
}

// ✅ FASTER - Struct interface with managed blurittable
// Or use direct concrete types when possible

// ✅ ALSO GOOD - Cache virtual call results
void Update()
{
    for (int i = 0; i < _targets.Length; i++)
    {
        var target = _targets[i];
        if (target != null)
        {
            target.TakeDamage(_damage); // Group virtual calls
        }
    }
}
```

## Common Mistakes to Prevent

### 1. Over-using FindObjectsOfType

```csharp
// ❌ WRONG - Expensive, runs on main thread
var enemies = FindObjectsOfType<Enemy>();

// ✅ CORRECT - Use events, interfaces, or registry
public class EnemyRegistry : MonoBehaviour
{
    private static List<Enemy> _enemies = new();
    public static IReadOnlyList<Enemy> Enemies => _enemies;

    public static void Register(Enemy enemy) => _enemies.Add(enemy);
    public static void Unregister(Enemy enemy) => _enemies.Remove(enemy);
}

// Or use tags/layers
int enemyLayer = LayerMask.NameToLayer("Enemy");
var enemies = FindObjectsOfType<Transform>()
    .Where(t => t.gameObject.layer == enemyLayer);
```

### 2. Not Disposing Native Collections

```csharp
// ❌ WRONG - Memory leak
void Start()
{
    _data = new NativeArray<int>(1000, Allocator.Persistent);
    // Never disposed!
}

void OnDestroy()
{
    // Forgot to call Dispose
}

// ✅ CORRECT - Always dispose
void OnDestroy()
{
    if (_data.IsCreated)
        _data.Dispose();
}

// ✅ SAFER - Use try/finally or using statement patterns
void Start()
{
    _data = new NativeArray<int>(1000, Allocator.Persistent);
}

void OnDestroy()
{
    if (_data.IsCreated)
        _data.Dispose();
}

// If using in Play mode only - verify in Edit Mode too
```

### 3. Ignoring Memory Layout for Jobs

```csharp
// ❌ WRONG - Cache line false sharing
struct Victim
{
    public float Value1;
    public float Value2; // Adjacent, causes cache ping-pong
}

// ✅ CORRECT - Padding to avoid false sharing
struct Optimized
{
    public float Value1;
    private float _padding; // Forces separate cache lines
    public float Value2;
}

// Or pack data into struct tightly when no sharing needed
struct PackedData
{
    public float3 Position;
    public float3 Velocity; // Cache-friendly for sequential access
}
```

### 4. Premature Optimization

```csharp
// ❌ WRONG - Optimize something that doesn't matter
void Update()
{
    // Micro-optimizing a function that runs once per frame
    // when there's a query in the same loop that takes 10ms
}

// ✅ CORRECT - Measure first, optimize where it counts
void Update()
{
    // Use Profiler to find actual bottleneck
    // Focus optimization on hot paths
}
```

### 5. Not Using Appropriate Data Structures

```csharp
// ❌ WRONG - Using List for frequent random access by index
List<int> list = new List<int>();
for (int i = 0; i < list.Count; i += 2) // Random access on List is fine
{
    Process(list[i]); // But this is not random, just sequential
}

// Sequential access - use array (faster iteration, less memory)
int[] array = new int[count];
for (int i = 0; i < array.Length; i++) // Array is fastest
{
    Process(array[i]);
}

// Lookup by key - use Dictionary
Dictionary<int, Enemy> enemiesById = new();
if (enemiesById.TryGetValue(id, out var enemy))
{
    enemy.TakeDamage();
}
```

## Common Issues / Gotchas

| Issue | Cause | Solution |
|-------|-------|----------|
| GC spikes | Per-frame allocations | Use ObjectPool, NativeArray, cache strings |
| Low FPS on mobile | Too many draw calls, overdraw | Use batching, LOD, reduce shadow quality |
| Physics jitter | Fixed timestep too high | Lower Time.fixedDeltaTime to 0.01 |
| Texture streaming pop | Budget too low | Increase streamingMipmapsMemoryBudget |
| SRP Batcher not working | Different materials per object | Share materials, use MaterialPropertyBlock |
| GPU instancing no effect | Shader not instancing-compatible | Add `#pragma multi_compile_instancing` |
| Job completion stutter | main thread sync in job | Avoid calling Unity API in jobs |
| Burst not accelerating | Managed references in struct | Use blittable types only (float3, NativeArray) |
| Memory growing | Native collections not disposed | Always dispose in OnDestroy |
| Low fillrate | Overdraw, transparency | Reduce particle count, optimize shader |

## Response Format

When answering Unity performance questions:

1. **Identify the bottleneck** (CPU/GPU/Memory)
2. **Show working code** with `#if UNITY_EDITOR` guards if helpful
3. **Explain tradeoffs** (memory vs speed, complexity vs readability)
4. **Provide profiling guidance** (where to measure, what to look for)
5. **Mention alternatives** (Jobs vs regular scripts, managed vs native)

## Performance Checklist

### Per-Frame Budget (60fps = 16.67ms frame time)

```
✅ Target < 10ms for main thread (leaves headroom for engine)
✅ Target < 4ms for render thread
✅ Target < 8ms for GPU
✅ GC < 2ms per frame (ideally < 1ms)
✅ No allocation in hot paths
```

### Memory Budget (varies by platform)

```
✅ Desktop: < 1GB total, < 512MB texture
✅ Mobile: < 512MB total, < 256MB texture
✅ Streaming: Keep mipmap budget 2x visible requirements
✅ Native arrays: Always dispose on OnDestroy
```

### Draw Call Budget

```
✅ Desktop: < 2000 draw calls per frame
✅ Mobile: < 500 draw calls per frame
✅ Use SRP Batcher for same-shader objects
✅ Use GPU Instancing for many identical objects
✅ Combine static meshes where possible
```

### Profiling Flow

1. Run Game view, open Profiler (Ctrl+Shift+P)
2. Check GPU Usage - is it the bottleneck?
3. Check CPU Usage - which section is highest?
4. Look at Hierarchy for specific expensive calls
5. Use Timeline to find threading opportunities
6. Use Memory Profiler to check for leaks
7. Use Frame Debugger to verify batching works
8. Use Memory Profiler to track texture/memory growth