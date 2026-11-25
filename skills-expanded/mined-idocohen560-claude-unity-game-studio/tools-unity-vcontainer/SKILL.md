---
name: tools-unity-vcontainer
description: VContainer dependency injection patterns for Unity including lifecycle management, scoped registrations, and common pitfalls.
---

# VContainer Dependency Injection

## Overview

VContainer is a lightweight, fast DI container for Unity. This skill covers registration patterns, lifecycle management, and common pitfalls that cause crashes.

## When to Use

- Setting up dependency injection in Unity
- Creating scoped containers for features/states
- Debugging VContainerException crashes
- Writing testable Unity code
- Managing service lifetimes

## Installation

```csharp
// Package Manager
// Add to manifest.json:
"jp.hadashikick.vcontainer": "https://github.com/hadashiA/VContainer.git?path=VContainer/Assets/VContainer#1.15.4"
```

## Core Concepts

### Lifetime Types

| Lifetime | Description | Use Case |
|----------|-------------|----------|
| `Singleton` | One instance per container | Global services, managers |
| `Scoped` | One instance per scope | Feature-specific services |
| `Transient` | New instance every resolve | Factories, short-lived objects |

**Critical:** `Singleton` in a child scope is actually **scoped to that child**, not truly global!

## Registration Patterns

### Basic Registration

```csharp
public class GameInstaller : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        // Interface to implementation
        builder.Register<IPlayerService, PlayerService>(Lifetime.Singleton);
        
        // Concrete type
        builder.Register<GameManager>(Lifetime.Singleton);
        
        // With interfaces
        builder.Register<AudioSystem>(Lifetime.Singleton)
            .AsImplementedInterfaces()
            .AsSelf();
    }
}
```

### Instance Registration

```csharp
protected override void Configure(IContainerBuilder builder)
{
    // Pre-existing instance
    builder.RegisterInstance(existingService);
    
    // ScriptableObject from Resources
    var config = Resources.Load<GameConfig>("GameConfig");
    builder.RegisterInstance(config);
    
    // Component on same GameObject
    builder.RegisterComponent(GetComponent<AudioSource>());
}
```

### Factory Registration

```csharp
protected override void Configure(IContainerBuilder builder)
{
    // Simple factory
    builder.RegisterFactory<Enemy>(() => new Enemy(), Lifetime.Scoped);
    
    // Factory with parameters
    builder.RegisterFactory<string, IWeapon>(name => 
        new Weapon(name), Lifetime.Transient);
    
    // Async factory
    builder.Register<IEnemyFactory, EnemyFactory>(Lifetime.Singleton);
}

public class EnemyFactory : IEnemyFactory
{
    private readonly IObjectResolver _resolver;
    
    public EnemyFactory(IObjectResolver resolver)
    {
        _resolver = resolver;
    }
    
    public Enemy Create(EnemyConfig config)
    {
        var enemy = new Enemy(config);
        _resolver.Inject(enemy);
        return enemy;
    }
}
```

### EntryPoint Registration

```csharp
protected override void Configure(IContainerBuilder builder)
{
    // IStartable - called once after container built
    builder.RegisterEntryPoint<GameInitializer>();
    
    // ITickable - called every frame
    builder.RegisterEntryPoint<GameLoop>();
    
    // IAsyncStartable - async initialization
    builder.RegisterEntryPoint<AsyncGameInitializer>();
    
    // Multiple interfaces
    builder.Register<GameManager>(Lifetime.Singleton)
        .AsImplementedInterfaces();
}

public class GameInitializer : IStartable
{
    public void Start()
    {
        // Called after container is built
    }
}

public class AsyncGameInitializer : IAsyncStartable
{
    public async UniTask StartAsync(CancellationToken ct)
    {
        await LoadGameDataAsync(ct);
    }
}
```

## Injection Patterns

### Constructor Injection (Preferred)

```csharp
public class PlayerController
{
    private readonly IInputService _input;
    private readonly IPlayerService _player;
    
    // Dependencies injected via constructor
    public PlayerController(IInputService input, IPlayerService player)
    {
        _input = input;
        _player = player;
    }
}
```

### Method Injection

```csharp
public class EnemyBehavior : MonoBehaviour
{
    private ITargetingService _targeting;
    
    [Inject]
    public void Construct(ITargetingService targeting)
    {
        _targeting = targeting;
    }
}
```

### Property Injection (Use Sparingly)

```csharp
public class DebugManager
{
    // Optional dependency
    [Inject]
    public IAnalyticsService Analytics { get; set; }
}
```

### Field Injection (Avoid in Production)

```csharp
public class LegacyComponent : MonoBehaviour
{
    [Inject] private IService _service; // Avoid - harder to test
}
```

## Scoped Containers (Child Scopes)

### Creating Child Scopes

```csharp
public class StateNavigationController
{
    private readonly LifetimeScope _rootScope;
    private readonly List<LifetimeScope> _stateStack = new();
    
    public async UniTask NavigateTo(IStateTransitionData data)
    {
        // Create child scope for new state
        var stateScope = _rootScope.CreateChild(builder =>
        {
            builder.Register<IState, WorldState>(Lifetime.Singleton);
            builder.Register<WorldController>(Lifetime.Singleton);
        });
        
        _stateStack.Add(stateScope);
        
        var state = stateScope.Container.Resolve<IState>();
        await state.Enter(data);
    }
    
    public async UniTask ExitState()
    {
        var scope = _stateStack[^1];
        _stateStack.RemoveAt(_stateStack.Count - 1);
        
        var state = scope.Container.Resolve<IState>();
        await state.Exit();
        
        // CRITICAL: Dispose scope AFTER exit completes
        await UniTask.Yield(); // Allow pending callbacks
        scope.Dispose();
    }
}
```

### Using IInstaller

```csharp
public class WorldStateInstaller : IInstaller
{
    public void Install(IContainerBuilder builder)
    {
        builder.Register<IState, WorldState>(Lifetime.Singleton);
        builder.Register<WorldController>(Lifetime.Singleton);
        builder.Register<WorldView>(Lifetime.Singleton);
    }
}

// Usage
var scope = parentScope.CreateChild(new WorldStateInstaller());
```

### Enqueue Pattern for Segment Loading

```csharp
using (LifetimeScope.Enqueue(segmentCache))
{
    var stateScope = _rootScope.CreateChild(installer);
    // segmentCache registrations included
}
```

## Common Crash Patterns & Fixes

### Problem 1: Resolving After Disposal

```csharp
// BAD: Scope disposed while async operation pending
await state.Exit();
scope.Dispose(); // Crash if Exit has pending callbacks

// GOOD: Wait for pending operations
await state.Exit();
await UniTask.Yield(); // Allow callbacks to complete
scope.Dispose();
```

### Problem 2: Singleton Referencing Scoped

```csharp
// BAD: Global singleton holds scoped reference
builder.Register<GlobalManager>(Lifetime.Singleton); // Root scope
builder.Register<FeatureService>(Lifetime.Scoped);   // Child scope

public class GlobalManager
{
    // This will break when child scope disposes!
    public GlobalManager(FeatureService feature) { }
}

// GOOD: Use factory or lazy resolution
public class GlobalManager
{
    private readonly IObjectResolver _resolver;
    
    public GlobalManager(IObjectResolver resolver)
    {
        _resolver = resolver;
    }
    
    public FeatureService GetFeature()
    {
        return _resolver.Resolve<FeatureService>();
    }
}
```

### Problem 3: Fire-and-Forget Without Guard

```csharp
// BAD: No cancellation when scope disposes
public async UniTaskVoid DoAsyncWork()
{
    await UniTask.Delay(5000);
    _service.DoSomething(); // May crash if disposed
}

// GOOD: Use CancellationToken
private CancellationTokenSource _cts;

public void Initialize()
{
    _cts = new CancellationTokenSource();
}

public async UniTask DoAsyncWork()
{
    await UniTask.Delay(5000, cancellationToken: _cts.Token);
    _service.DoSomething();
}

public void Dispose()
{
    _cts?.Cancel();
    _cts?.Dispose();
}
```

### Problem 4: Missing Registration

```csharp
// VContainerException: Unable to resolve IService

// Check 1: Is it registered?
builder.Register<IService, ServiceImpl>(Lifetime.Singleton);

// Check 2: Is the assembly referenced?
// Add to asmdef references

// Check 3: Is the scope correct?
// Child scope can't resolve from parent without proper hierarchy
```

### Problem 5: Circular Dependency

```csharp
// VContainerException: Circular dependency detected

// BAD
public class ServiceA
{
    public ServiceA(ServiceB b) { }
}
public class ServiceB
{
    public ServiceB(ServiceA a) { }
}

// GOOD: Break with Lazy<T> or factory
public class ServiceA
{
    private readonly Lazy<ServiceB> _b;
    public ServiceA(Lazy<ServiceB> b) => _b = b;
}
```

## Safe Resolution Patterns

### TryResolve Extension

```csharp
public static class VContainerExtensions
{
    public static bool TryResolve<T>(this IObjectResolver resolver, out T result)
    {
        result = default;
        try
        {
            if (resolver == null) return false;
            result = resolver.Resolve<T>();
            return true;
        }
        catch (VContainerException)
        {
            return false;
        }
    }
    
    public static T ResolveOrDefault<T>(this IObjectResolver resolver, T defaultValue = default)
    {
        return resolver.TryResolve<T>(out var result) ? result : defaultValue;
    }
}

// Usage
if (scope.Container.TryResolve<IState>(out var state))
{
    await state.Exit();
}
```

### Scope Alive Check

```csharp
public static bool IsAlive(this LifetimeScope scope)
{
    try
    {
        return scope != null && scope.Container != null;
    }
    catch
    {
        return false;
    }
}
```

## Testing with VContainer

### Mocking Dependencies

```csharp
[TestFixture]
public class PlayerControllerTests
{
    private LifetimeScope _testScope;
    
    [SetUp]
    public void SetUp()
    {
        _testScope = LifetimeScope.Create(builder =>
        {
            // Register mocks
            var mockInput = Substitute.For<IInputService>();
            builder.RegisterInstance(mockInput);
            
            // Register real implementation under test
            builder.Register<PlayerController>(Lifetime.Singleton);
        });
    }
    
    [TearDown]
    public void TearDown()
    {
        _testScope?.Dispose();
    }
    
    [Test]
    public void PlayerController_Move_UpdatesPosition()
    {
        var controller = _testScope.Container.Resolve<PlayerController>();
        // Test...
    }
}
```

### Testing Installers

```csharp
[Test]
public void Installer_RegistersAllDependencies()
{
    using var scope = LifetimeScope.Create(new GameInstaller());
    
    Assert.DoesNotThrow(() => scope.Container.Resolve<IPlayerService>());
    Assert.DoesNotThrow(() => scope.Container.Resolve<IInputService>());
}
```

## Editor Cleanup (Critical for Unity Editor)

```csharp
// Prevent VContainerException when exiting Play Mode
public static class EditorLifetimeScopeCleanup
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void ClearGlobalInstallers()
    {
        var type = typeof(LifetimeScope);
        var field = type.GetField("GlobalExtraInstallers", 
            BindingFlags.NonPublic | BindingFlags.Static);
        
        if (field?.GetValue(null) is IList list)
        {
            list.Clear();
        }
    }
}
```

## Best Practices

1. **Prefer constructor injection** - Explicit dependencies, easier testing
2. **Use interfaces** - Enables mocking and swapping implementations
3. **Scope appropriately** - Don't make everything Singleton
4. **Dispose child scopes** - Prevent memory leaks
5. **Use CancellationToken** - Graceful async cleanup
6. **Avoid property/field injection** - Except for optional dependencies
7. **Test your installers** - Catch missing registrations early
8. **Guard against disposed scopes** - Use TryResolve in edge cases

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Unable to resolve` | Not registered | Add registration |
| `Circular dependency` | A→B→A | Use Lazy<T> or factory |
| `Object disposed` | Scope disposed | Check lifecycle, add guards |
| `Multiple registrations` | Duplicate registration | Remove duplicate |
| `Invalid cast` | Wrong type registered | Check As<T>() calls |
