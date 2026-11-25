---
name: unity-scripting
description: >
  Unity 6000.3 LTS C# scripting patterns. Covers MonoBehaviour lifecycle,
  serialization, coroutines, jobs, Burst, API usage, and Unity 6000
  scripting features.
  Trigger: When writing C# scripts, MonoBehaviour, coroutines, Jobs,
  or any Unity scripting task in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Writing C# scripts that inherit from `MonoBehaviour`
- Implementing game object behavior with lifecycle callbacks
- Serializing custom data types to/from the Inspector
- Spreading work across multiple frames with coroutines
- Writing multithreaded code with the Unity Job system
- Optimizing code with Burst compilation
- Working with async/await patterns in Unity
- Implementing `ScriptableObject` assets
- Handling Editor-time vs runtime code differences

## Critical Rules

### Never Call Unity API From Serialization Callbacks or Field Initializers

```csharp
// ❌ WRONG — These run on a loading thread, not main thread
[Serializable]
public class MyData
{
    // DO NOT call Unity APIs here (Debug.Log is safe, but not recommended)
    public Vector3 position = Camera.main.transform.position; // Unsafe!
    public GameObject reference = GameObject.Find("Player"); // Unsafe!
}

// ✅ CORRECT — Initialize with simple values or defaults
[Serializable]
public class MyData
{
    public Vector3 position = Vector3.zero;
    public string playerName = "Default";
}

// ✅ CORRECT — Use ISerializationCallbackReceiver for complex initialization
public class MyBehaviour : MonoBehaviour, ISerializationCallbackReceiver
{
    [SerializeField] private Vector3 _position;
    
    public void OnAfterDeserialize()
    {
        // Safe to use Unity APIs here (main thread)
        _position = Vector3.zero;
    }
}
```

**Why:** Unity's serializer runs on a separate loading thread. Calling main-thread-only APIs (like `GameObject.Find`, accessing `Camera.main`) can crash or produce undefined behavior in development builds.

### Update for Input, FixedUpdate for Physics

```csharp
public class PlayerController : MonoBehaviour
{
    private Vector2 _input;
    private Rigidbody _rb;
    private const float SPEED = 10f;
    private const float JUMP_FORCE = 5f;

    private void Update()
    {
        // Read input — can vary per frame, safe in Update
        _input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
        
        // Jump on key press (detected per-frame)
        if (Input.GetButtonDown("Jump") && IsGrounded())
        {
            _rb.AddForce(Vector2.up * JUMP_FORCE, ForceMode.Impulse);
        }
    }

    private void FixedUpdate()
    {
        // Apply physics — uses fixed timestep for consistency
        Vector3 movement = new Vector3(_input.x, 0, _input.y) * SPEED;
        _rb.MovePosition(_rb.position + movement * Time.fixedDeltaTime);
    }
    
    private bool IsGrounded()
    {
        return Physics.CheckSphere(transform.position + Vector3.down * 0.5f, 0.2f);
    }
}
```

### Never Modify transform.position on Physics Objects

```csharp
// ❌ WRONG — Teleports, bypasses physics
transform.position = new Vector3(10, 0, 0);

// ✅ CORRECT — Use Rigidbody for movement
rb.MovePosition(new Vector3(10, 0, 0));

// ✅ CORRECT — Only if kinematic
rb.isKinematic = true;
transform.position = new Vector3(10, 0, 0);
rb.isKinematic = false;
```

**Why:** Setting `transform.position` directly teleports the object, bypassing collision detection and physics simulation.

## MonoBehaviour Lifecycle

### Event Function Order

```
Awake()         → Called when instance is created (before Start)
OnEnable()      → Called when component enabled (every enable)
Reset()         → Called when component added or reset (Editor only)
Start()         → Called before first frame update (if enabled)
FixedUpdate()   → Physics update (fixed timestep)
OnTriggerXXX()  → Physics callbacks
OnCollisionXXX()→ Collision callbacks
Update()        → Frame update
LateUpdate()    → After all Updates
OnDisable()     → When component disabled
OnDestroy()     → When destroyed or scene unloads
```

### Complete Lifecycle Example

```csharp
public class LifecycleExample : MonoBehaviour
{
    [Header("Settings")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private int health = 100;
    
    // Internal state (not serialized)
    private Vector3 _velocity;
    private bool _isInitialized;
    
    // Called when script instance is loaded (before Start)
    // Called even if component is disabled (but game object must be active)
    private void Awake()
    {
        Debug.Log("Awake called");
        Initialize();
    }
    
    // Called before first frame update, only if enabled
    // Use for initialization that depends on other components
    private void Start()
    {
        Debug.Log("Start called");
        if (!_isInitialized)
        {
            Initialize();
        }
    }
    
    // Physics updates (fixed timestep: 50Hz default)
    // Use for physics calculations, forces, movement
    private void FixedUpdate()
    {
        ApplyPhysics();
    }
    
    // Called every frame
    // Use for input, non-physics movement, timers
    private void Update()
    {
        ProcessInput();
        UpdateTimers();
    }
    
    // Called after all Update() calls
    // Use for camera following, final position updates
    private void LateUpdate()
    {
        ApplyCameraFollow();
    }
    
    // Called when object becomes enabled and active
    private void OnEnable()
    {
        Debug.Log("OnEnable called");
    }
    
    // Called when object becomes disabled
    // Save state here (static vars lost on domain reload)
    private void OnDisable()
    {
        Debug.Log("OnDisable called");
        SaveState();
    }
    
    // Called when component or game object is destroyed
    // Last chance to clean up, unsubscribe events
    private void OnDestroy()
    {
        Debug.Log("OnDestroy called");
        Cleanup();
    }
    
    // Editor-only: called when component reset
    private void Reset()
    {
        Debug.Log("Reset called");
        moveSpeed = 5f;
        health = 100;
    }
    
    // Called when game object becomes visible/invisible to any camera
    private void OnBecameVisible()
    {
        Debug.Log("Became visible");
    }
    
    private void OnBecameInvisible()
    {
        Debug.Log("Became invisible");
    }
    
    private void Initialize()
    {
        _isInitialized = true;
        _velocity = Vector3.zero;
    }
    
    private void ApplyPhysics()
    {
        // Physics movement here
    }
    
    private void ProcessInput()
    {
        // Input handling here
    }
    
    private void UpdateTimers()
    {
        // Timer logic here
    }
    
    private void ApplyCameraFollow()
    {
        // Camera code here
    }
    
    private void SaveState()
    {
        // Save to static fields if needed
    }
    
    private void Cleanup()
    {
        // Unsubscribe from events, stop coroutines
        StopAllCoroutines();
    }
}
```

### Script Execution Order

```csharp
// Use [DefaultExecutionOrder] to control order between scripts
// Lower values execute first

[DefaultExecutionOrder(-100)] // Executes before default (0)
public class EarlyInit : MonoBehaviour
{
    private void Awake()
    {
        Debug.Log("Early Init Awake");
    }
}

[DefaultExecutionOrder(100)] // Executes after default
public class LateInit : MonoBehaviour
{
    private void Awake()
    {
        Debug.Log("Late Init Awake");
    }
}
```

**Note:** `[DefaultExecutionOrder]` values don't appear in the Script Execution Order window. If you set a value in both code and the Editor UI, the Editor UI takes precedence.

### InitializeOnLoad (Editor Scripts)

```csharp
using UnityEngine;
using UnityEditor;

// Runs when Unity Editor launches (including domain reload)
// Must be in Editor folder or wrapped in #if UNITY_EDITOR
[InitializeOnLoad]
public class EditorInitializer
{
    static EditorInitializer()
    {
        Debug.Log("Editor initialized");
        EditorApplication.playModeChanged += OnPlayModeChanged;
    }
    
    private static void OnPlayModeChanged()
    {
        Debug.Log($"Play mode changed: {EditorApplication.isPlaying}");
    }
}

// Alternative: use InitializeOnLoadMethod for single methods
public class EditorInitializerMethod
{
    [InitializeOnLoadMethod]
    private static void Initialize()
    {
        Debug.Log("InitializeOnLoadMethod called");
    }
}
```

### RuntimeInitializeOnLoadMethod

```csharp
public class RuntimeInitializer : MonoBehaviour
{
    // Runs when runtime initializes (scene load, domain reload)
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void OnSceneLoaded()
    {
        Debug.Log("Scene loaded, after scene setup");
    }
    
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void BeforeSceneLoad()
    {
        Debug.Log("Before scene load");
    }
    
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterAssembliesLoaded)]
    private static void AfterAssembliesLoaded()
    {
        Debug.Log("Assemblies loaded");
    }
    
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void SubsystemRegistration()
    {
        Debug.Log("Subsystem registration");
    }
}
```

## Serialization

### Serialization Rules Summary

Unity serializes fields if:
- `public` OR has `[SerializeField]`
- NOT `static`
- NOT `const`
- NOT `readonly`
- Type is serializable (primitives, Unity types, `[Serializable]` classes/structs, `UnityEngine.Object` references)

```csharp
public class SerializationDemo : MonoBehaviour
{
    // ✅ Serialized: public field
    public int publicField = 10;
    
    // ✅ Serialized: private with SerializeField attribute
    [SerializeField] private float privateField = 5f;
    
    // ❌ NOT serialized: private by default
    private bool hiddenField;
    
    // ❌ NOT serialized: static
    public static int staticField;
    
    // ❌ NOT serialized: const
    public const float CONSTANT = 3.14f;
    
    // ❌ NOT serialized: readonly
    public readonly Vector3 readonlyField = Vector3.up;
    
    // ✅ Serialized: Unity built-in types
    public Vector3 position;
    public Color color = Color.white;
    public AnimationCurve curve = new AnimationCurve();
    public LayerMask mask;
    
    // ✅ Serialized: custom serializable struct
    [SerializeField] private CustomData data;
    
    // ✅ Serialized: array or List
    public int[] intArray;
    public List<string> stringList;
    
    // ✅ Serialized: reference to UnityEngine.Object
    public GameObject prefab;
    public Material material;
    public AudioSource audioSource;
}

// Custom serializable struct
[Serializable]
public struct CustomData
{
    public string name;
    public int value;
    public Vector3 offset;
}
```

### SerializeField with Property

```csharp
public class PropertySerialization : MonoBehaviour
{
    // Auto-property with serialized backing field
    [field: SerializeField]
    public int Health { get; private set; }
    
    [field: SerializeField]
    public string PlayerName { get; set; }
    
    // Serialize backing field instead of property
    [SerializeField] private int _maxHealth;
    public int MaxHealth => _maxHealth;
    
    // Don't serialize backing field
    [field: NonSerialized]
    public bool IsDead { get; set; }
    
    // Serialize as reference (polymorphic)
    [field: SerializeReference]
    public IDamageable Damageable { get; set; }
}
```

### Custom Serialization with ISerializationCallbackReceiver

```csharp
// Dictionary serialization
public class SerializableDictionary : MonoBehaviour, ISerializationCallbackReceiver
{
    [SerializeField] private List<int> _keys = new();
    [SerializeField] private List<string> _values = new();
    
    // Runtime dictionary (not serialized directly)
    private Dictionary<int, string> _dict = new();
    
    public void OnBeforeSerialize()
    {
        _keys.Clear();
        _values.Clear();
        
        foreach (var kvp in _dict)
        {
            _keys.Add(kvp.Key);
            _values.Add(kvp.Value);
        }
    }
    
    public void OnAfterDeserialize()
    {
        _dict.Clear();
        
        for (int i = 0; i < Mathf.Min(_keys.Count, _values.Count); i++)
        {
            _dict[_keys[i]] = _values[i];
        }
    }
    
    public void Add(int key, string value) => _dict[key] = value;
    public string Get(int key) => _dict.TryGetValue(key, out var v) ? v : null;
}
```

### Polymorphic Serialization

```csharp
// Base interface
public interface IDamageable
{
    void ApplyDamage(int damage);
}

// Serializable wrapper for polymorphic types
[Serializable]
public class DamageableWrapper : ISerializationCallbackReceiver
{
    public enum Type { Soldier, Vehicle, Structure }
    
    [SerializeField] private Type _type;
    [SerializeField] private int _soldierHealth;
    [SerializeField] private int _vehicleHealth;
    [SerializeField] private int _structureHealth;
    
    // Runtime reference (not serialized)
    private IDamageable _instance;
    
    public void SetInstance(IDamageable instance, Type type)
    {
        _instance = instance;
        _type = type;
    }
    
    public void OnBeforeSerialize()
    {
        switch (_type)
        {
            case Type.Soldier:
                _soldierHealth = (_instance as Soldier)?.Health ?? 0;
                break;
            case Type.Vehicle:
                _vehicleHealth = (_instance as Vehicle)?.Health ?? 0;
                break;
            case Type.Structure:
                _structureHealth = (_instance as Structure)?.Health ?? 0;
                break;
        }
    }
    
    public void OnAfterDeserialize()
    {
        switch (_type)
        {
            case Type.Soldier:
                _instance = new Soldier { Health = _soldierHealth };
                break;
            case Type.Vehicle:
                _instance = new Vehicle { Health = _vehicleHealth };
                break;
            case Type.Structure:
                _instance = new Structure { Health = _structureHealth };
                break;
        }
    }
}

// Usage in MonoBehaviour
public class DamageManager : MonoBehaviour
{
    [SerializeField] private List<DamageableWrapper> _damageables = new();
}
```

### SerializeReference for Polymorphism

```csharp
[Serializable]
public abstract class Unit
{
    public string name;
    public abstract void Execute();
}

[Serializable]
public class Soldier : Unit
{
    public int damage;
    public override void Execute() { /* soldier logic */ }
}

[Serializable]
public class Medic : Unit
{
    public float healRange;
    public int healAmount;
    public override void Execute() { /* medic logic */ }
}

public class UnitManager : MonoBehaviour
{
    // [SerializeReference] enables polymorphism
    [SerializeField] private List<Unit> _units = new();
    
    private void Start()
    {
        _units.Add(new Soldier { name = "Alpha", damage = 10 });
        _units.Add(new Medic { name = "Medic", healAmount = 20 });
    }
}
```

## Coroutines and Async

### Basic Coroutine Pattern

```csharp
public class CoroutineExample : MonoBehaviour
{
    // Start coroutine from any method
    private void Start()
    {
        StartCoroutine(DoSomethingOverTime());
    }
    
    // Coroutine returns IEnumerator and uses yield
    private IEnumerator DoSomethingOverTime()
    {
        Debug.Log("Start");
        yield return null; // Wait one frame
        Debug.Log("After 1 frame");
        yield return new WaitForSeconds(1f); // Wait 1 second (time scale affected)
        Debug.Log("After 1 real second");
        yield return new WaitForEndOfFrame(); // Wait until end of frame
        Debug.Log("End of frame");
    }
    
    // Stop specific coroutine
    private Coroutine _movementCoroutine;
    
    private void StartMovement()
    {
        _movementCoroutine = StartCoroutine(MoveToTarget());
    }
    
    private void StopMovement()
    {
        if (_movementCoroutine != null)
        {
            StopCoroutine(_movementCoroutine);
            _movementCoroutine = null;
        }
    }
    
    // Or stop all coroutines
    private void OnDisable()
    {
        StopAllCoroutines();
    }
}
```

### Yield Instructions Reference

```csharp
public class YieldInstructionsDemo : MonoBehaviour
{
    private IEnumerator Start()
    {
        // Wait for next frame
        yield return null;
        
        // Wait for fixed update (physics)
        yield return new WaitForFixedUpdate();
        
        // Wait until end of frame (for camera work, rendering)
        yield return new WaitForEndOfFrame();
        
        // Wait for seconds (affected by Time.timeScale)
        yield return new WaitForSeconds(1f);
        
        // Wait for seconds (NOT affected by Time.timeScale)
        yield return new WaitForSecondsRealtime(1f);
        
        // Wait until condition is true
        yield return new WaitUntil(() => someCondition);
        
        // Wait while condition is true
        yield return new WaitWhile(() => !someCondition);
        
        // Wait for AsyncOperation (scene loading, Resource.Load)
        var asyncOp = SceneManager.LoadSceneAsync("NextScene");
        yield return asyncOp;
        Debug.Log($"Loaded in {(1 - asyncOp.progress) * 100}% progress");
        
        // WWW requests
        using (var www = new WWW("https://example.com"))
        {
            yield return www;
            Debug.Log($"Downloaded: {www.text}");
        }
    }
}
```

### Async/Await (Unity's Awaitable)

```csharp
using UnityEngine;
using System.Threading.Tasks;

public class AsyncAwaitExample : MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("Starting async operation...");
        
        // Await with no specific context (resumes on main thread after ContinueWith)
        await Task.Delay(1000);
        Debug.Log("After 1 second (not affected by timeScale)");
        
        // Using Awaitable for Unity-aware async
        await Awaitable.EndOfFrameAsync();
        Debug.Log("After EndOfFrame");
        
        // Custom delay affected by timeScale
        await Awaitable.WaitForSecondsAsync(1f);
        Debug.Log("After 1 game second");
        
        // Scene loading
        await SceneManager.LoadSceneAsync("GameScene").ToAwaitable();
        Debug.Log("Scene loaded!");
    }
    
    public async Task<string> FetchDataAsync(string url)
    {
        using var www = new UnityEngine.Networking.UnityWebRequest.Get(url);
        await www.SendWebRequest();
        return www.downloadHandler.text;
    }
}
```

### Editor Coroutines

```csharp
#if UNITY_EDITOR
using Unity.EditorCoroutines;
using Unity.EditorCoroutines.Editor;
using UnityEditor;

public class EditorCoroutineExample
{
    [MenuItem("Tools/Long Operation")]
    public static void LongOperation()
    {
        // Editor coroutines run in Edit mode
        EditorCoroutineUtility.StartCoroutine(EditorLongOperation(), null);
    }
    
    private static IEnumerator EditorLongOperation()
    {
        Debug.Log("Starting long editor operation...");
        for (int i = 0; i < 100; i++)
        {
            if (i % 10 == 0)
            {
                Debug.Log($"Progress: {i}%");
                yield return new EditorWaitForSeconds(0.1f); // Editor-aware wait
            }
        }
        Debug.Log("Complete!");
    }
}
#endif
```

## Jobs and Burst

### IJob - Basic Job

```csharp
using UnityEngine;
using Unity.Collections;
using Unity.Jobs;

public struct AddFloatJob : IJob
{
    public float a;
    public float b;
    public NativeArray<float> result;
    
    public void Execute()
    {
        result[0] = a + b;
    }
}

public class JobExample : MonoBehaviour
{
    private NativeArray<float> _result;
    private JobHandle _handle;
    
    private void Update()
    {
        // Schedule job (async)
        _result = new NativeArray<float>(1, Allocator.TempJob);
        
        var job = new AddFloatJob
        {
            a = 10f,
            b = 20f,
            result = _result
        };
        
        _handle = job.Schedule();
        
        // Run immediately on main thread (debug only)
        // job.Run();
    }
    
    private void LateUpdate()
    {
        // Ensure job is complete before accessing results
        _handle.Complete();
        
        float sum = _result[0];
        Debug.Log($"Result: {sum}");
        
        // Dispose allocated memory
        _result.Dispose();
    }
    
    private void OnDestroy()
    {
        // Always complete and dispose
        _handle.Complete();
        if (_result.IsCreated) _result.Dispose();
    }
}
```

### IJobParallelFor - Parallel Jobs

```csharp
public struct ProcessItemsJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<int> input;
    public NativeArray<int> output;
    
    public void Execute(int index)
    {
        output[index] = input[index] * 2;
    }
}

public class ParallelJobExample : MonoBehaviour
{
    private void Start()
    {
        var input = new NativeArray<int>(1000, Allocator.TempJob);
        var output = new NativeArray<int>(1000, Allocator.TempJob);
        
        // Initialize input
        for (int i = 0; i < input.Length; i++)
        {
            input[i] = i;
        }
        
        var job = new ProcessItemsJob
        {
            input = input,
            output = output
        };
        
        // Schedule with batch size for parallelism control
        JobHandle handle = job.Schedule(input.Length, 100);
        
        // Can chain more work here
        handle.Complete();
        
        Debug.Log($"First output: {output[0]}, Last: {output[output.Length - 1]}");
        
        input.Dispose();
        output.Dispose();
    }
}
```

### IJobFor - Non-Parallel For Loop

```csharp
public struct SumArrayJob : IJobFor
{
    [ReadOnly] public NativeArray<int> values;
    public NativeArray<int> result;
    
    public void Execute(int index)
    {
        // Runs sequentially, not in parallel
        result[0] += values[index];
    }
}

public class IJobForExample : MonoBehaviour
{
    private void Start()
    {
        var values = new NativeArray<int>(100, Allocator.TempJob);
        var result = new NativeArray<int>(1, Allocator.TempJob);
        
        for (int i = 0; i < values.Length; i++)
        {
            values[i] = i + 1;
        }
        
        var job = new SumArrayJob
        {
            values = values,
            result = result
        };
        
        // IJobFor: not parallel, executes in order
        job.Schedule(values.Length, 1).Complete();
        
        Debug.Log($"Sum: {result[0]}"); // Should be 5050
        
        values.Dispose();
        result.Dispose();
    }
}
```

### Job Dependencies

```csharp
public class JobDependencies : MonoBehaviour
{
    private NativeArray<int> _data;
    private JobHandle _firstHandle;
    private JobHandle _secondHandle;
    
    private void Start()
    {
        _data = new NativeArray<int>(100, Allocator.TempJob);
        
        // First job
        var firstJob = new InitializeJob { data = _data };
        _firstHandle = firstJob.Schedule();
        
        // Second job depends on first
        var secondJob = new ProcessJob { data = _data };
        _secondHandle = secondJob.Schedule(_firstHandle);
        
        // Third job depends on second
        var thirdJob = new FinalizeJob { data = _data };
        thirdJob.Schedule(_secondHandle).Complete();
    }
    
    private void OnDestroy()
    {
        if (_data.IsCreated) _data.Dispose();
    }
}

public struct InitializeJob : IJob
{
    public NativeArray<int> data;
    public void Execute() { /* init logic */ }
}

public struct ProcessJob : IJob
{
    public NativeArray<int> data;
    public void Execute() { /* process logic */ }
}

public struct FinalizeJob : IJob
{
    public NativeArray<int> data;
    public void Execute() { /* finalize logic */ }
}
```

### NativeContainer Safety

```csharp
public class NativeContainerSafety : MonoBehaviour
{
    // Multiple read-only arrays can be read in parallel
    private NativeArray<int> _inputA;
    private NativeArray<int> _inputB;
    private NativeArray<int> _output;
    
    private JobHandle _handle;
    
    private void Start()
    {
        _inputA = new NativeArray<int>(100, Allocator.TempJob);
        _inputB = new NativeArray<int>(100, Allocator.TempJob);
        _output = new NativeArray<int>(100, Allocator.TempJob);
        
        var job = new ParallelAdditionJob
        {
            inputA = _inputA,
            inputB = _inputB,
            output = _output
        };
        
        _handle = job.Schedule(_inputA.Length, 50);
    }
    
    private void LateUpdate()
    {
        _handle.Complete();
        // ... use results ...
    }
    
    private void OnDestroy()
    {
        _handle.Complete();
        if (_inputA.IsCreated) _inputA.Dispose();
        if (_inputB.IsCreated) _inputB.Dispose();
        if (_output.IsCreated) _output.Dispose();
    }
}

public struct ParallelAdditionJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<int> inputA;
    [ReadOnly] public NativeArray<int> inputB;
    public NativeArray<int> output;
    
    public void Execute(int index)
    {
        output[index] = inputA[index] + inputB[index];
    }
}
```

### Allocator Usage

```csharp
public class AllocatorExample : MonoBehaviour
{
    private void DemonstrateAllocators()
    {
        // Allocator.Temp - fastest, frame-lifetime max
        // Use for single-frame work, local variables
        using var tempArray = new NativeArray<int>(10, Allocator.Temp);
        // Don't pass Temp to jobs stored in fields!
        
        // Allocator.TempJob - 4 frame lifetime
        // Use for typical job work
        using var tempJobArray = new NativeArray<int>(10, Allocator.TempJob);
        // Must Dispose within 4 frames or get warning
        
        // Allocator.Persistent - infinite lifetime
        // Use for data that lives across frames
        using var persistentArray = new NativeArray<int>(10, Allocator.Persistent);
        // Slower allocation, but won't leak
    }
}
```

### Burst Compilation

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;

[BurstCompile(FloatMode = FloatMode.Fast, FloatPrecision = FloatPrecision.Low)]
public struct BurstMathJob : IJob
{
    [ReadOnly] public NativeArray<Vector3> positions;
    public NativeArray<float> distances;
    public Vector3 origin;
    
    public void Execute()
    {
        for (int i = 0; i < positions.Length; i++)
        {
            distances[i] = Vector3.Distance(positions[i], origin);
        }
    }
}

// Burst-compiled static method
[BurstCompile]
public static class BurstMath
{
    [BurstCompile]
    public static float CalculateDamage(float baseDamage, float multiplier, float armor)
    {
        float effectiveDamage = baseDamage * multiplier;
        return effectiveDamage * (1f - armor / 100f);
    }
}

// Using BurstCompile attribute in code (can also enable in inspector)
// Methods marked with [BurstCompile] or called from [BurstCompile] code get compiled
```

### IJobParallelForTransform

```csharp
using Unity.Transforms;
using Unity.Mathematics;

public class MoveTransformsJob : MonoBehaviour
{
    public Transform[] transforms;
    
    private void Start()
    {
        var positions = new NativeArray<float3>(transforms.Length, Allocator.TempJob);
        var velocities = new NativeArray<float3>(transforms.Length, Allocator.TempJob);
        
        // Initialize positions from current transform positions
        for (int i = 0; i < transforms.Length; i++)
        {
            positions[i] = transforms[i].position;
            velocities[i] = new float3(0, 0, 1);
        }
        
        var job = new TransformMovementJob
        {
            positions = positions,
            velocities = velocities,
            deltaTime = Time.deltaTime
        };
        
        JobHandle handle = job.Schedule(transforms.Length, 1);
        
        // For transform jobs, must complete before main thread can safely access transforms
        handle.Complete();
        
        positions.Dispose();
        velocities.Dispose();
    }
}

[BurstCompile]
public struct TransformMovementJob : IJobParallelForTransform
{
    public NativeArray<float3> positions;
    public NativeArray<float3> velocities;
    public float deltaTime;
    
    public void Execute(int index, TransformAccess transform)
    {
        positions[index] += velocities[index] * deltaTime;
        transform.position = positions[index];
    }
}
```

## Scripting API

### GameObject and Component

```csharp
public class GameObjectAPI : MonoBehaviour
{
    private void Demo()
    {
        // Create new GameObject
        var go = new GameObject("MyObject", typeof(MeshFilter), typeof(MeshRenderer));
        
        // Get component (returns null if not found)
        var meshFilter = go.GetComponent<MeshFilter>();
        
        // Get or add component
        var collider = go.GetComponent<BoxCollider>();
        if (collider == null)
        {
            collider = go.AddComponent<BoxCollider>();
        }
        
        // Get all components
        var allColliders = go.GetComponents<Collider>();
        
        // Get components in children
        var childColliders = go.GetComponentsInChildren<Collider>();
        
        // Find objects
        var player = GameObject.FindGameObjectWithTag("Player");
        var allEnemies = GameObject.FindGameObjectsWithTag("Enemy");
        
        // Instantiate prefab
        var instance = Instantiate(prefab, transform.position, Quaternion.identity);
        
        // Destroy
        Destroy(instance, 5f); // Delay destruction
        DestroyImmediate(instance); // Immediate (editor only)
    }
    
    [SerializeField] private GameObject prefab;
}
```

### Transform Operations

```csharp
public class TransformAPI : MonoBehaviour
{
    private void Demo()
    {
        var t = transform;
        
        // Position
        Vector3 pos = t.position;
        t.position = new Vector3(0, 1, 0);
        
        // Local position
        Vector3 localPos = t.localPosition;
        t.localPosition = Vector3.zero;
        
        // Rotation
        Quaternion rot = t.rotation;
        t.rotation = Quaternion.Euler(0, 90, 0);
        
        // Local rotation
        Quaternion localRot = t.localRotation;
        
        // Scale
        Vector3 scale = t.localScale;
        t.localScale = Vector3.one * 2f;
        
        // Hierarchy
        Transform parent = t.parent;
        t.SetParent(someParent);
        t.SetParent(someParent, false); // worldPositionStays = false
        t.SetParent(null); // detach
        
        // Children
        int childCount = t.childCount;
        Transform firstChild = t.GetChild(0);
        
        // Find child by name
        Transform namedChild = t.Find("ChildName");
        
        // Iterate children
        foreach (Transform child in t)
        {
            Debug.Log(child.name);
        }
        
        // World transforms
        Vector3 worldForward = t.forward;
        Vector3 worldUp = t.up;
        Vector3 worldRight = t.right;
        
        // Transform points
        Vector3 localPoint = t.InverseTransformPoint(worldPos);
        Vector3 worldPoint = t.TransformPoint(localPoint);
        
        // Transform directions (ignore position)
        Vector3 localDir = t.InverseTransformDirection(worldDir);
        Vector3 worldDir = t.TransformDirection(localDir);
        
        // Look at
        t.LookAt(target);
        t.LookAt(target, Vector3.up);
        
        // Translate (relative to self or world)
        t.Translate(Vector3.forward * 10);
        t.Translate(Vector3.forward * 10, Space.World);
        
        // Rotate (local space by default)
        t.Rotate(Vector3.up * 90);
        t.Rotate(Vector3.up * 90, Space.World);
        
        // Rotate around point
        t.RotateAround(point, axis, angle);
        
        // Set global rotation (bypassing local rotation)
        t.SetPositionAndRotation(newPos, newRot);
    }
    
    private Transform target;
}
```

### Time and DeltaTime

```csharp
public class TimeAPI : MonoBehaviour
{
    private void Demo()
    {
        // Delta time (frame time)
        float dt = Time.deltaTime;
        float fixedDt = Time.fixedDeltaTime;
        
        // Unscaled time (ignores timeScale)
        float unscaledTime = Time.unscaledTime;
        float unscaledDt = Time.unscaledDeltaTime;
        
        // Time scale
        float timeScale = Time.timeScale;
        Time.timeScale = 0.5f; // Slow motion
        Time.timeScale = 0f; // Pause
        
        // Frame count
        int frame = Time.frameCount;
        
        // Time since start
        float time = Time.time;
        
        // Smooth delta (adjusts for frame rate variation)
        float smoothDt = Time.smoothDeltaTime;
        
        // Capture time (for benchmarking)
        var sw = System.Diagnostics.Stopwatch.StartNew();
        // ... work ...
        sw.Stop();
        double ms = sw.ElapsedTicks / (double)System.Diagnostics.Stopwatch.Frequency * 1000;
    }
}
```

### Input System

```csharp
public class InputAPI : MonoBehaviour
{
    private void Update()
    {
        // Keyboard axes (-1 to 1)
        float h = Input.GetAxis("Horizontal"); // A/D, Left/Right arrows
        float v = Input.GetAxis("Vertical");   // W/S, Up/Down arrows
        
        // Raw axes (no smoothing, -1, 0, or 1)
        float rawH = Input.GetAxisRaw("Horizontal");
        
        // Button states
        if (Input.GetButtonDown("Fire1"))     { /* first frame */ }
        if (Input.GetButton("Fire1"))        { /* held */ }
        if (Input.GetButtonUp("Fire1"))      { /* released */ }
        
        // Mouse
        Vector3 mousePos = Input.mousePosition;
        Vector3 mouseDelta = Input.GetAxis("Mouse X") * Vector3.right 
                           + Input.GetAxis("Mouse Y") * Vector3.up;
        bool mouseButton0 = Input.GetMouseButton(0);
        bool mouseButton0Down = Input.GetMouseButtonDown(0);
        bool mouseButton0Up = Input.GetMouseButtonUp(0);
        
        // Touch (mobile)
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            Vector2 pos = touch.position;
            Vector2 delta = touch.deltaPosition;
            
            TouchPhase phase = touch.phase;
            // Began, Moved, Stationary, Ended, Canceled
        }
        
        // Key codes (scan for specific keys)
        if (Input.GetKeyDown(KeyCode.Space)) { Jump(); }
        if (Input.GetKey(KeyCode.LeftShift)) { Sprint(); }
        
        // Any key/button
        if (Input.anyKeyDown) { /* start game */ }
    }
    
    private void Jump() { }
    private void Sprint() { }
}
```

### Physics Queries

```csharp
public class PhysicsQueries : MonoBehaviour
{
    [SerializeField] private LayerMask _groundLayers;
    
    private void Demo()
    {
        // Raycast
        if (Physics.Raycast(transform.position, Vector3.down, out RaycastHit hit, 10f))
        {
            Debug.Log($"Hit: {hit.collider.name} at {hit.point}");
        }
        
        // Raycast with layer mask
        if (Physics.Raycast(transform.position, Vector3.down, out hit, 10f, _groundLayers))
        {
            Debug.Log($"Hit ground!");
        }
        
        // Non-allocating raycast
        RaycastHit[] hits = new RaycastHit[10];
        int count = Physics.RaycastNonAlloc(transform.position, Vector3.down, hits, 10f);
        for (int i = 0; i < count; i++)
        {
            ProcessHit(hits[i]);
        }
        
        // Sphere cast (swept sphere for fast-moving objects)
        if (Physics.SphereCast(origin, radius, direction, out hit, distance))
        {
            // ...
        }
        
        // Box cast
        if (Physics.BoxCast(origin, halfExtents, direction, out hit, rotation, distance))
        {
            // ...
        }
        
        // Capsule cast
        if (Physics.CapsuleCast(point1, point2, radius, direction, out hit, distance))
        {
            // ...
        }
        
        // Overlap sphere (no raycast, just check colliders)
        Collider[] colliders = Physics.OverlapSphere(position, radius, _groundLayers);
        foreach (var col in colliders)
        {
            Debug.Log(col.name);
        }
        
        // Non-allocating overlap
        Collider[] results = new Collider[20];
        int overlapCount = Physics.OverlapSphereNonAlloc(position, radius, results, _groundLayers);
        
        // Check if collider is on specific layer
        bool isOnGround = Physics.CheckSphere(groundCheck.position, 0.1f, _groundLayers);
    }
    
    private void ProcessHit(RaycastHit hit)
    {
        Debug.Log($"Hit: {hit.collider.name}");
    }
    
    private Vector3 origin, direction;
    private float radius, distance;
    private Quaternion rotation;
    private Transform groundCheck;
}
```

### Scene Management

```csharp
using UnityEngine.SceneManagement;

public class SceneManagementExample : MonoBehaviour
{
    private void Demo()
    {
        // Load scene (additive or single)
        SceneManager.LoadScene("GameScene");
        SceneManager.LoadScene("GameScene", LoadSceneMode.Additive);
        
        // Async load
        AsyncOperation asyncOp = SceneManager.LoadSceneAsync("GameScene");
        asyncOp.completed += OnSceneLoaded;
        
        // Unload scene
        SceneManager.UnloadSceneAsync("OldScene");
        
        // Get active scene
        Scene activeScene = SceneManager.GetActiveScene();
        Debug.Log($"Active scene: {activeScene.name}");
        
        // Get scene by name or index
        Scene scene = SceneManager.GetSceneByName("GameScene");
        
        // Get all loaded scenes
        for (int i = 0; i < SceneManager.sceneCount; i++)
        {
            Scene s = SceneManager.GetSceneAt(i);
            Debug.Log($"Scene {i}: {s.name}");
        }
        
        // Scene is loaded check
        if (scene.isLoaded)
        {
            // ...
        }
        
        // Get build index
        int buildIndex = scene.buildIndex;
        
        // Check if scene is valid
        if (scene.IsValid())
        {
            // ...
        }
    }
    
    private void OnSceneLoaded(AsyncOperation op)
    {
        Debug.Log("Scene load complete!");
    }
}
```

### ScriptableObject

```csharp
// Define a ScriptableObject asset
public class EnemyData : ScriptableObject
{
    public string enemyName;
    public int health;
    public float moveSpeed;
    public GameObject prefab;
    public AudioClip attackSound;
}

// Create asset programmatically
public class CreateAssetExample : MonoBehaviour
{
    [ContextMenu("Create Enemy Data")]
    private void CreateEnemyData()
    {
        var data = ScriptableObject.CreateInstance<EnemyData>();
        data.enemyName = "Goblin";
        data.health = 50;
        data.moveSpeed = 3f;
        
        // Save to project (requires UnityEditor if using AssetDatabase)
#if UNITY_EDITOR
        string path = "Assets/Data/EnemyData.asset";
        UnityEditor.AssetDatabase.CreateAsset(data, path);
#endif
    }
}

// Load ScriptableObject from code
public class LoadAssetExample : MonoBehaviour
{
    [SerializeField] private EnemyData _enemyData;
    
    private void LoadData()
    {
        // Via direct reference (set in inspector)
        EnemyData data = _enemyData;
        
        // Load from resources
        var fromResources = Resources.Load<EnemyData>("EnemyData");
        
        // Load via AssetDatabase (Editor only)
#if UNITY_EDITOR
        var fromAssetDB = UnityEditor.AssetDatabase.LoadAssetAtPath<EnemyData>(
            "Assets/Data/EnemyData.asset"
        );
#endif
    }
}

// ScriptableObject as data container (similar to MonoBehaviour but no GameObject)
public class GameConfig : ScriptableObject
{
    public static GameConfig Instance { get; private set; }
    
    public int maxPlayers = 4;
    public float gameDuration = 300f;
    public List<string> availableLevels;
    
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Initialize()
    {
        Instance = Resources.Load<GameConfig>("GameConfig");
    }
}
```

### Attributes Reference

```csharp
public class AttributesDemo : MonoBehaviour
{
    // Serialize field (private but shown in Inspector)
    [SerializeField] private int _health;
    
    // Header (group in Inspector)
    [Header("Movement Settings")]
    [SerializeField] private float _speed;
    [SerializeField] private float _jumpForce;
    
    // Range (slider in Inspector)
    [Range(0f, 100f)]
    [SerializeField] private float _stamina;
    
    // Tooltip (hover help in Inspector)
    [Tooltip("How fast the unit moves in meters per second")]
    [SerializeField] private float _moveSpeed;
    
    // Hide in Inspector
    [HideInInspector] public int hiddenValue;
    
    // Require component (auto-add to GameObject)
    [RequireComponent(typeof(Rigidbody))]
    public class Movement : MonoBehaviour { }
    
    // Context menu (right-click in Inspector)
    [ContextMenu("Reset Values")]
    private void ResetValues()
    {
        _health = 100;
        _speed = 5f;
    }
    
    // Context menu item
    [ContextMenuItem("Randomize Health", "RandomizeHealth")]
    [SerializeField] private int _health;
    
    [ContextMenuItem("Randomize Speed", "RandomizeSpeed")]
    [SerializeField] private float _speed;
    
    private void RandomizeHealth() { _health = Random.Range(0, 100); }
    private void RandomizeSpeed() { _speed = Random.Range(1f, 10f); }
    
    // Execute in edit mode
    [ExecuteInEditMode]
    public class EditorBehavior : MonoBehaviour { }
    
    // Always execute (even in prefab mode)
    [ExecuteAlways]
    public class AlwaysBehavior : MonoBehaviour { }
    
    // Add to context menu
    [ContextMenu("Do Something")]
    private void DoSomething()
    {
        Debug.Log("Did something!");
    }
    
    // Disallow multiple components
    [DisallowMultipleComponent]
    public class SingleInstance : MonoBehaviour { }
    
    // Selection base (for hierarchy selection)
    [SelectionBase]
    public class Selectable : MonoBehaviour { }
    
    // Default execution order
    [DefaultExecutionOrder(100)]
    public class OrderedBehavior : MonoBehaviour { }
    
    // Color header (gizmo color)
    [HeaderColor(0.5f, 0.8f, 0.3f)]
    public float someField;
    
    // Space (vertical spacing in Inspector)
    [Space]
    public float beforeSpace;
    public float afterSpace;
    
    // Multiline (for long strings)
    [Multiline(4)]
    [SerializeField] private string _notes;
    
    // Text area (scrollable)
    [TextArea(3, 6)]
    [SerializeField] private string _description;
}
```

## Unity 6000-Specific Features

### Conditional Compilation Symbols

```csharp
public class ConditionalCompilation : MonoBehaviour
{
    private void Demo()
    {
        // Unity version
#if UNITY_6000
        Debug.Log("Running on Unity 6000");
#elif UNITY_2023
        Debug.Log("Running on Unity 2023");
#endif
        
        // Platform
#if UNITY_EDITOR
        Debug.Log("In Editor");
#endif
        
#if UNITY_STANDALONE
        Debug.Log("Standalone build");
#endif

#if UNITY_ANDROID
        Debug.Log("Android build");
#endif

#if UNITY_IOS
        Debug.Log("iOS build");
#endif

#if UNITY_WEBGL
        Debug.Log("WebGL build");
#endif
        
        // Scripting backend
#if ENABLE_IL2CPP
        Debug.Log("IL2CPP backend");
#elif ENABLE_MONO
        Debug.Log("Mono backend");
#endif
        
        // Development build
#if DEVELOPMENT_BUILD
        Debug.Log("Development build");
#endif
        
        // Burst AOT
#if ENABLE_BURST_AOT
        Debug.Log("Burst AOT enabled");
#endif
        
        // Custom symbols (Player Settings > Other Settings > Scripting Define Symbols)
#if MY_CUSTOM_SYMBOL
        Debug.Log("Custom symbol defined");
#endif
    }
}
```

### Conditional Attribute (Inspector-only)

```csharp
public class ConditionalAttributeDemo : MonoBehaviour
{
    public bool showAdvancedSettings;
    
    [Tooltip("Only visible when showAdvancedSettings is true")]
    public float advancedValue;
}

// Note: Unity's [Conditional] attribute only works on method attributes,
// not serialized fields. Use a custom editor or #if UNITY_EDITOR for fields.

// For serialization, consider using ShowIf attribute from Collections package
```

### Custom Player Loop

```csharp
using UnityEngine;
using UnityEngine.LowLevel;
using UnityEngine.PlayerLoop;

public class CustomPlayerLoop : MonoBehaviour
{
    private void Start()
    {
        var loop = PlayerLoop.GetCurrentPlayerLoop();
        
        // Find existing systems
        foreach (var system in loop.subSystemList)
        {
            Debug.Log($"System: {system.type}");
        }
    }
    
    private static PlayerLoopSystem CreateCustomSystem()
    {
        return new PlayerLoopSystem
        {
            type = typeof(MyCustomSystem),
            updateFunction = MyCustomSystem.Update,
            initializeFunc = MyCustomSystem.Initialize,
            cleanupFunc = MyCustomSystem.Cleanup,
            shouldGatherInputs = false
        };
    }
}

public static class MyCustomSystem
{
    public struct CustomUpdate { }
    
    public static void Initialize(ref PlayerLoopSystem system)
    {
        // Add to player loop
    }
    
    public static void Update()
    {
        // Called each frame
    }
    
    public static void Cleanup()
    {
        // Called on shutdown
    }
}
```

## Common Mistakes to Prevent

### 1. NullReferenceException from GetComponent in Awake

```csharp
// ❌ WRONG — Component might not be ready
void Awake()
{
    var rb = GetComponent<Rigidbody>();
    rb.mass = 10f; // Crashes if no Rigidbody attached
}

// ✅ CORRECT — Check for null
void Awake()
{
    if (TryGetComponent<Rigidbody>(out var rb))
    {
        rb.mass = 10f;
    }
    else
    {
        Debug.LogWarning("No Rigidbody found!");
    }
}
```

### 2. Not Completing Jobs Before Accessing NativeContainer

```csharp
// ❌ WRONG — Access data before job completes
private void Update()
{
    var job = new MyJob { data = _data };
    job.Schedule();
    // Don't access _data here! Job still running!
    Debug.Log(_data[0]); // UNSAFE
}

// ✅ CORRECT — Complete in LateUpdate after all jobs
private JobHandle _handle;

private void Update()
{
    var job = new MyJob { data = _data };
    _handle = job.Schedule();
}

private void LateUpdate()
{
    _handle.Complete(); // Safe to access now
    Debug.Log(_data[0]);
}
```

### 3. Memory Leaks with NativeContainer

```csharp
// ❌ WRONG — Never disposing
void Start()
{
    _array = new NativeArray<int>(100, Allocator.Persistent);
}

void OnDestroy()
{
    // Forgot to dispose!
}

// ✅ CORRECT — Always dispose
void OnDestroy()
{
    if (_array.IsCreated)
    {
        _array.Dispose();
    }
}

// ✅ ALSO CORRECT — Using using statement (C# 8+)
using var array = new NativeArray<int>(100, Allocator.Persistent);
// Automatically disposed at end of scope
```

### 4. Using List as MonoBehaviour Field Without Initialization

```csharp
// ❌ WRONG — Serialization doesn't work on uninitialized List
[SerializeField] private List<int> _ints; // null in Play mode!

void Start()
{
    _ints.Add(5); // NullReferenceException!
}

// ✅ CORRECT — Initialize in Awake or Start
[SerializeField] private List<int> _ints = new();

void Awake()
{
    if (_ints == null) _ints = new List<int>();
}
```

### 5. Modifying Rigidbody in Update Instead of FixedUpdate

```csharp
// ❌ WRONG — Input in Update, physics in FixedUpdate mismatch
void Update()
{
    rb.velocity = new Vector3(Input.GetAxis("Horizontal"), 0, 0) * speed;
}

// ✅ CORRECT — All physics in FixedUpdate
void FixedUpdate()
{
    rb.velocity = new Vector3(Input.GetAxis("Horizontal"), 0, 0) * speed;
}

// ✅ ALTERNATIVE — Read input in Update, apply in FixedUpdate
private Vector3 _input;

void Update()
{
    _input = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
}

void FixedUpdate()
{
    rb.velocity = _input * speed;
}
```

### 6. Coroutine Memory Leaks

```csharp
// ❌ WRONG — Starting coroutine without stopping
void OnEnable()
{
    StartCoroutine(LongRunningOperation());
}

void OnDisable()
{
    // Forgot to stop!
}

// ✅ CORRECT — Track and stop coroutines
private Coroutine _operation;

void OnEnable()
{
    _operation = StartCoroutine(LongRunningOperation());
}

void OnDisable()
{
    if (_operation != null)
    {
        StopCoroutine(_operation);
        _operation = null;
    }
}

// ✅ ALSO CORRECT — Stop all
void OnDisable()
{
    StopAllCoroutines();
}
```

### 7. Ignoring Time.timeScale

```csharp
// ❌ WRONG — Assuming fixed timing
void Update()
{
    healthRegen += 1f * Time.deltaTime; // Affected by timeScale!
    if (healthRegen >= 10f) // Will take 10 real seconds at timeScale=1
    {                      // But different at other timeScale values
        health++;
        healthRegen = 0f;
    }
}

// ✅ CORRECT — Use unscaled time when needed
if (shouldRegenInRealtime)
{
    healthRegen += 1f * Time.unscaledDeltaTime;
}
else
{
    healthRegen += 1f * Time.deltaTime;
}
```

### 8. Checking Tag Without Null Check

```csharp
// ❌ WRONG — Could crash if collider is null
void OnCollisionEnter(Collision collision)
{
    if (collision.gameObject.CompareTag("Enemy")) // Crash if null!
    {
        TakeDamage();
    }
}

// ✅ CORRECT — Check collision.gameObject exists
void OnCollisionEnter(Collision collision)
{
    if (collision.gameObject != null && collision.gameObject.CompareTag("Enemy"))
    {
        TakeDamage();
    }
}

// ✅ EVEN BETTER — Use CompareTag (faster than == operator)
void OnCollisionEnter(Collision collision)
{
    if (collision.CompareTag("Enemy"))
    {
        TakeDamage();
    }
}
```

## Response Format

When answering Unity scripting questions:

1. **Code first** — Provide fully compilable C# examples
2. **Explain WHY** — Don't just show what, explain why this pattern is correct
3. **Mention gotchas** — Common mistakes and how to avoid them
4. **Reference version** — Note Unity 6000-specific behavior
5. **Cross-reference** — Link to related skills (e.g., `skills/unity-physics/` for physics-related scripting)

### Example Response Template

```csharp
// ❌ WRONG - [brief explanation]
// [incorrect code]

// ✅ CORRECT - [brief explanation]  
// [correct code]

// Why: [detailed explanation of the pattern]
// Unity version: [if 6000-specific]
// Related: See skills/unity-physics/ for physics interaction patterns
```

### Quick Reference — Common Operations

```csharp
// Instantiate prefab
var instance = Instantiate(prefab, position, rotation);

// Get component (add if missing)
if (!TryGetComponent<T>(out var component))
    component = gameObject.AddComponent<T>();

// Enable/disable component
component.enabled = true/false;

// Check if component is valid
if (component != null && component.enabled)

// Stop coroutine
StopCoroutine(coroutine);
StopAllCoroutines();

// Schedule job
JobHandle handle = job.Schedule(dependencies);

// Complete job
handle.Complete();

// Dispose NativeContainer
if (container.IsCreated) container.Dispose();

// Check layer mask
bool hit = (1 << hit.collider.gameObject.layer & layerMask) != 0;
```