---
name: game-dev-pro
description: "Unity, Unreal, Godot: game architecture, ECS, multiplayer, optimization, CI/CD. Use when building or optimizing game projects."
---

# Game Dev Pro

## Purpose

Build production-quality games. Covers Unity, Unreal Engine, and Godot patterns: architecture, ECS, multiplayer, rendering optimization, asset pipeline, and CI/CD.

## When to Use

**Use this when:**
- Building or reviewing a Unity, Unreal Engine, or Godot project at any stage
- Designing game architecture decisions: ECS layout, state machines, scene management, or asset pipelines
- Optimizing draw calls, physics budget, or memory allocations for a specific target platform

**Use this ESPECIALLY when:**
- A game ships to console, mobile, or WebGL where runtime constraints are strict and GC pauses are visible
- Adding multiplayer (Photon, Fish-Net, Netcode for GameObjects) where tick-rate, lag compensation, and authority models matter
- Debugging frame-rate drops or hitches in a shipped build, where profiler data exists

**Don't skip when:**
- Any Unity script touches `Update()` with allocations — GC spikes are silent until they are not
- Adding a new manager-style singleton that could create hidden coupling across scenes
- Shipping to a new platform (iOS, Android, console) where platform-specific store and certification requirements apply

## Core Patterns

### 1. Architecture (Unity)

```
Assets/
  Scripts/
    Core/              ← Singletons, GameManager, EventBus
    Systems/           ← ECS systems, custom update loops
    Behaviors/         ← MonoBehaviour components
    UI/                ← Canvas controllers
    Audio/             ← FMOD/Wwise integration
    Networking/        ← Photon/Mirror/Fish-Net
    StateMachines/     ← Animator states, game states
  Art/                 ← Models, textures, materials
  Audio/               ← SFX, music, ambience
  Prefabs/             ← Reusable game objects
  Scenes/              ← Levels, menus, UI scenes
  ScriptableObjects/   ← Data containers, configs
  Resources/           ← Runtime-loaded assets (sparingly)
  Shaders/             ← Custom HLSL/ShaderLab
  Plugins/             ← Native SDKs
  StreamingAssets/     ← Bundled external data
```

### 2. Game Loop & State Machine

```csharp
// Finite State Machine for game states
public enum GameState { MainMenu, Playing, Paused, GameOver, Loading }

public class GameStateManager : MonoBehaviour
{
    public static GameStateManager Instance { get; private set; }
    public GameState CurrentState { get; private set; } = GameState.MainMenu;

    private readonly Dictionary<GameState, IState> states = new();

    void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        // Register states
        states.Add(GameState.MainMenu, new MainMenuState());
        states.Add(GameState.Playing, new PlayingState());
        states.Add(GameState.Paused, new PausedState());
        states.Add(GameState.GameOver, new GameOverState());
    }

    public void TransitionTo(GameState newState)
    {
        states[CurrentState].Exit();
        CurrentState = newState;
        states[CurrentState].Enter();
    }
}
```

### 3. Object Pooling

```csharp
// Pool instead of Instantiate/Destroy (GC-friendly)
public class ObjectPool<T> where T : Component
{
    private readonly Queue<T> pool = new();
    private readonly T prefab;
    private readonly Transform parent;

    public ObjectPool(T prefab, int initialSize, Transform parent = null)
    {
        this.prefab = prefab;
        this.parent = parent;

        for (int i = 0; i < initialSize; i++)
        {
            var obj = CreateNew();
            obj.gameObject.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public T Get()
    {
        if (pool.Count == 0)
        {
            var obj = CreateNew();
            obj.gameObject.SetActive(true);
            return obj;
        }

        var pooled = pool.Dequeue();
        pooled.gameObject.SetActive(true);
        return pooled;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        pool.Enqueue(obj);
    }

    private T CreateNew()
    {
        var obj = Object.Instantiate(prefab, parent);
        obj.gameObject.name = $"{prefab.name}_Pooled";
        return obj;
    }
}
```

### 4. Event-Driven Architecture

```csharp
// Type-safe event bus (avoids coupling)
public static class EventBus
{
    private static readonly Dictionary<Type, Delegate> events = new();

    public static void Subscribe<T>(Action<T> handler) where T : struct
    {
        if (events.TryGetValue(typeof(T), out var existing))
            events[typeof(T)] = Delegate.Combine(existing, handler);
        else
            events[typeof(T)] = handler;
    }

    public static void Publish<T>(T eventData) where T : struct
    {
        if (events.TryGetValue(typeof(T), out var handler))
            (handler as Action<T>)?.Invoke(eventData);
    }
}

// Usage
public struct ProjectileHitEvent { public GameObject target; public int damage; }

// Subscribe
EventBus.Subscribe<ProjectileHitEvent>(OnProjectileHit);

// Publish
EventBus.Publish(new ProjectileHitEvent { target = enemy, damage = 10 });
```

### 5. Performance Optimization

| Area | Target | Tech |
|------|--------|------|
| Draw calls | < 200 | Batching, GPU instancing, LODs |
| Poly count | < 100K visible | LOD groups, occlusion culling |
| UI rebuilds | < 5/frame | Canvas pooling, manual rebuild |
| Memory | < 1.5GB | Addressables, asset bundles |
| GC allocations | 0 in Update() | Object pools, structs |
| Physics | < 10ms/frame | Collision layers, simplified meshes |

```csharp
// ✅ Profile before optimizing
// Use Unity Profiler, Xcode Instruments, RenderDoc

// ✅ Addressables for streaming (not Resources folder)
AsyncOperationHandle<GameObject> handle = Addressables.LoadAssetAsync<GameObject>("Enemy_Prefab");
handle.Completed += (op) => Instantiate(op.Result);

// ✅ LOD Group
[RequireComponent(typeof(LODGroup))]
public class LODSetup : MonoBehaviour { /* Set up 3 LOD levels */ }
```

### Checklist

- [ ] Object pools for frequently spawned/despawned objects
- [ ] Event-driven communication (no MonoBehaviour.Find/GetComponent)
- [ ] Addressables for asset management (not Resources folder)
- [ ] LOD groups on all complex meshes
- [ ] GPU instancing for repeated objects
- [ ] Profiling on target device before optimization
- [ ] Fixed Timestep for physics (not tied to frame rate)
- [ ] State machine for game states (no spaghetti bools)
- [ ] Save system with versioning (backward compatible)
- [ ] Audio: spatial blend, occlusion, dynamic mixing

## Related Skills

- **architecture-planner** — use before game-dev-pro when the high-level system boundaries (client/server split, game services topology) are still undecided
- **performance-engineer** — pair when profiler data reveals CPU/GPU hotspots that need deeper analysis beyond Unity-specific patterns
- **backend-senior-engineer** — reach for when the multiplayer authoritative server or game-backend API lives outside the game engine
- **devops-release-engineer** — for setting up Unity CI/CD pipelines, build automation, and platform-specific signing for iOS/Android/console
- **security-reviewer** — when the game handles real-money transactions, anti-cheat systems, or stores user account credentials
- **test-engineer** — for writing PlayMode and EditMode tests in Unity's Test Framework, or Godot's GUT, alongside ECS unit tests
