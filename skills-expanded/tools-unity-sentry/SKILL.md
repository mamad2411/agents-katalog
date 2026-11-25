---
name: tools-unity-sentry
description: Sentry Unity SDK integration patterns for error tracking, performance monitoring, transactions, spans, and custom instrumentation.
---

# Sentry Unity SDK

## Overview

Sentry provides error tracking and performance monitoring for Unity games. This skill covers SDK configuration, custom instrumentation, and best practices for mobile games.

## When to Use

- Setting up error tracking in Unity
- Adding performance monitoring (transactions/spans)
- Creating custom breadcrumbs and context
- Debugging production crashes
- Monitoring release health

## Installation

```json
// Via Unity Package Manager
// Add to manifest.json:
"io.sentry.unity": "1.5.0"
```

## SDK Configuration

### SentryOptionsConfiguration (ScriptableObject)

```csharp
[CreateAssetMenu(fileName = "SentryOptions", menuName = "Sentry/Options")]
public class SentryOptionConfiguration : SentryOptionsConfiguration
{
    [SerializeField] private string _dsn;
    [SerializeField] private string _environment;
    [SerializeField] private float _tracesSampleRate = 0.2f;
    [SerializeField] private bool _enableLogDebouncing = true;
    
    public override void Configure(SentryUnityOptions options)
    {
        options.Dsn = _dsn;
        options.Environment = _environment;
        options.Release = $"{Application.version}+{BuildNumber}";
        
        // Performance monitoring
        options.TracesSampleRate = _tracesSampleRate;
        options.AutoStartupTraces = true;
        
        // Log debouncing (prevent spam)
        options.EnableLogDebouncing = _enableLogDebouncing;
        options.DebounceTimeError = TimeSpan.FromSeconds(1);
        
        // Deduplication
        options.DeduplicateMode = DeduplicateMode.All;
        
        // Callbacks
        options.SetBeforeSend(ModifyEvent);
        options.SetBeforeSendTransaction(ModifyTransaction);
        options.SetBeforeBreadcrumb(ModifyBreadcrumb);
        
        // Native crash handling
#if UNITY_ANDROID
        options.AndroidNativeInitializationType = NativeInitializationType.BuildTime;
#elif UNITY_IOS
        options.IosNativeInitializationType = NativeInitializationType.BuildTime;
#endif
    }
    
    private SentryEvent ModifyEvent(SentryEvent sentryEvent)
    {
        // Add custom context to all events
        sentryEvent.SetTag("quality_level", QualitySettings.GetQualityLevel().ToString());
        sentryEvent.SetTag("wifi", Application.internetReachability == 
            NetworkReachability.ReachableViaLocalAreaNetwork ? "true" : "false");
        return sentryEvent;
    }
    
    private SentryTransaction ModifyTransaction(SentryTransaction transaction)
    {
        // Add measurements to all transactions
        transaction.SetMeasurement("memory.used", GetUsedMemoryMB(), MeasurementUnit.Information.Megabyte);
        return transaction;
    }
    
    private Breadcrumb ModifyBreadcrumb(Breadcrumb breadcrumb)
    {
        // Filter unwanted breadcrumbs
        if (breadcrumb.Type == "http")
            return null; // Drop HTTP breadcrumbs
        return breadcrumb;
    }
}
```

## User Context

### Setting User Identity

```csharp
public class SentryController
{
    public void SetUser(string userId, string email = null)
    {
        SentrySdk.ConfigureScope(scope =>
        {
            scope.User = new SentryUser
            {
                Id = userId,
                Email = email,
                Username = username
            };
        });
    }
    
    public void ClearUser()
    {
        SentrySdk.ConfigureScope(scope =>
        {
            scope.User = new SentryUser();
        });
    }
}
```

### Setting Tags (Indexed, Searchable)

```csharp
// Global tags (apply to all events)
SentrySdk.ConfigureScope(scope =>
{
    scope.SetTag("zone.id", currentZoneId);
    scope.SetTag("legend.id", activeLegendId);
    scope.SetTag("build.type", Debug.isDebugBuild ? "debug" : "release");
});

// Event-specific tags
SentrySdk.CaptureMessage("Custom event", scope =>
{
    scope.SetTag("feature", "combat");
});
```

### Setting Extra Data (Non-indexed Context)

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.SetExtra("player_level", 42);
    scope.SetExtra("inventory_count", 150);
    scope.SetExtra("party_composition", new[] { "warrior", "mage", "healer" });
});
```

## Transactions and Spans

### Creating a Transaction

```csharp
public async UniTask LoadZoneAsync(string zoneId)
{
    // Start transaction
    var transaction = SentrySdk.StartTransaction(
        name: $"Zone:Load:{zoneId}",
        operation: "zone.load"
    );
    
    // Set as current transaction for automatic span parenting
    SentrySdk.ConfigureScope(scope => scope.Transaction = transaction);
    
    try
    {
        // Add context
        transaction.SetTag("zone.id", zoneId);
        
        // Create child spans
        using (var span = transaction.StartChild("addressables.load"))
        {
            await LoadAddressablesAsync();
            span.SetMeasurement("asset.count", assetCount);
            span.Status = SpanStatus.Ok;
        }
        
        using (var span = transaction.StartChild("scene.load"))
        {
            await LoadSceneAsync();
            span.Status = SpanStatus.Ok;
        }
        
        transaction.Status = SpanStatus.Ok;
    }
    catch (Exception ex)
    {
        transaction.Status = SpanStatus.InternalError;
        SentrySdk.CaptureException(ex);
        throw;
    }
    finally
    {
        transaction.Finish();
    }
}
```

### Nested Spans

```csharp
public async UniTask ExecuteAbilityAsync(ISpan parentSpan)
{
    using var abilitySpan = parentSpan.StartChild("ability.execute");
    abilitySpan.SetTag("ability.id", _abilityId);
    
    try
    {
        using (var targetSpan = abilitySpan.StartChild("targeting.resolve"))
        {
            var targets = await ResolveTargets();
            targetSpan.SetMeasurement("target.count", targets.Count);
        }
        
        using (var effectSpan = abilitySpan.StartChild("effects.apply"))
        {
            foreach (var effect in _effects)
            {
                using var singleEffect = effectSpan.StartChild($"effect:{effect.Id}");
                await ApplyEffect(effect);
            }
        }
        
        abilitySpan.Status = SpanStatus.Ok;
    }
    catch
    {
        abilitySpan.Status = SpanStatus.InternalError;
        throw;
    }
}
```

### Manual Span Timing

```csharp
var span = transaction.StartChild("custom.operation");
span.SetTag("custom.tag", "value");

// Do work...

span.SetMeasurement("items.processed", itemCount);
span.Status = SpanStatus.Ok;
span.Finish(); // Must call if not using 'using'
```

## Measurements

### Adding Measurements to Transactions

```csharp
// Numeric measurements with units
transaction.SetMeasurement("load.time", loadTimeMs, MeasurementUnit.Duration.Millisecond);
transaction.SetMeasurement("memory.used", usedMb, MeasurementUnit.Information.Megabyte);
transaction.SetMeasurement("fps.average", avgFps, MeasurementUnit.None);
transaction.SetMeasurement("asset.count", count, MeasurementUnit.None);

// Available units
MeasurementUnit.None
MeasurementUnit.Duration.Millisecond
MeasurementUnit.Duration.Second
MeasurementUnit.Information.Byte
MeasurementUnit.Information.Kilobyte
MeasurementUnit.Information.Megabyte
MeasurementUnit.Fraction.Percent
```

## Breadcrumbs

### Adding Breadcrumbs

```csharp
// Simple message
SentrySdk.AddBreadcrumb("Player entered combat zone");

// With category and level
SentrySdk.AddBreadcrumb(
    message: "Zone loaded: Dunmiir",
    category: "navigation",
    level: BreadcrumbLevel.Info
);

// With custom data
SentrySdk.AddBreadcrumb(
    message: "Purchase completed",
    category: "monetization",
    level: BreadcrumbLevel.Info,
    data: new Dictionary<string, string>
    {
        { "product_id", productId },
        { "price", price.ToString() },
        { "currency", currency }
    }
);

// Different levels
BreadcrumbLevel.Debug
BreadcrumbLevel.Info
BreadcrumbLevel.Warning
BreadcrumbLevel.Error
BreadcrumbLevel.Critical
```

### Automatic Breadcrumb Categories

```csharp
// Recommended categories for games:
"navigation"    // Zone changes, scene loads
"combat"        // Combat events
"ui"            // UI state changes
"monetization"  // Purchase events
"quest"         // Quest progress
"performance"   // Performance events
"network"       // Network operations
"state"         // State machine transitions
```

## Error Capture

### Capture Exception

```csharp
try
{
    RiskyOperation();
}
catch (Exception ex)
{
    SentrySdk.CaptureException(ex);
    // or with extra context
    SentrySdk.CaptureException(ex, scope =>
    {
        scope.SetTag("operation", "risky_operation");
        scope.SetExtra("input_data", inputData);
    });
}
```

### Capture Message

```csharp
// Simple message
SentrySdk.CaptureMessage("Unexpected state reached");

// With level
SentrySdk.CaptureMessage("Memory warning triggered", SentryLevel.Warning);

// With context
SentrySdk.CaptureMessage("Combat desync detected", scope =>
{
    scope.SetTag("combat.id", combatId);
    scope.SetExtra("player_state", playerState);
    scope.Level = SentryLevel.Error;
});
```

### Custom Exception Context

```csharp
public class GameplayException : Exception
{
    public string ZoneId { get; }
    public string AbilityId { get; }
    
    public GameplayException(string message, string zoneId, string abilityId) 
        : base(message)
    {
        ZoneId = zoneId;
        AbilityId = abilityId;
    }
}

// Capture with context
try
{
    ExecuteAbility();
}
catch (GameplayException ex)
{
    SentrySdk.CaptureException(ex, scope =>
    {
        scope.SetTag("zone.id", ex.ZoneId);
        scope.SetTag("ability.id", ex.AbilityId);
    });
}
```

## Performance Monitoring Patterns

### Continuous Profiling

```csharp
public class PerformanceMonitor
{
    private readonly FrameTiming[] _frameTimings = new FrameTiming[1];
    
    public void CaptureFrame()
    {
        var transaction = SentrySdk.StartTransaction("Gather Metrics", "performance.metrics");
        
        // Frame timing
        if (FrameTimingManager.IsFeatureEnabled())
        {
            FrameTimingManager.CaptureFrameTimings();
            var count = FrameTimingManager.GetLatestTimings(1, _frameTimings);
            
            if (count > 0)
            {
                transaction.SetMeasurement("frame.cpu", _frameTimings[0].cpuFrameTime, 
                    MeasurementUnit.Duration.Millisecond);
                transaction.SetMeasurement("frame.gpu", _frameTimings[0].gpuFrameTime,
                    MeasurementUnit.Duration.Millisecond);
            }
        }
        
        // Memory
        var usedMemory = Profiler.GetTotalAllocatedMemoryLong() / 1_000_000f;
        transaction.SetMeasurement("memory.used", usedMemory, MeasurementUnit.Information.Megabyte);
        
        // FPS
        transaction.SetMeasurement("fps", 1f / Time.deltaTime, MeasurementUnit.None);
        
        // Context
        transaction.SetTag("zone.id", CurrentZone);
        transaction.SetTag("in_combat", InCombat.ToString());
        
        transaction.Finish();
    }
}
```

### Hitch Detection

```csharp
public void DetectHitch(float frameTimeMs)
{
    if (frameTimeMs > 100f) // Severe hitch
    {
        SentrySdk.AddBreadcrumb(
            message: $"Severe hitch: {frameTimeMs:F1}ms",
            category: "performance",
            level: BreadcrumbLevel.Error,
            data: new Dictionary<string, string>
            {
                { "zone", _currentZone },
                { "in_combat", _inCombat.ToString() },
                { "activity", _currentActivity }
            }
        );
    }
    else if (frameTimeMs > 50f) // Major hitch
    {
        SentrySdk.AddBreadcrumb(
            message: $"Major hitch: {frameTimeMs:F1}ms",
            category: "performance",
            level: BreadcrumbLevel.Warning
        );
    }
}
```

## Release Health

### Release Configuration

```csharp
// In SentryOptionsConfiguration
options.Release = $"{Application.version}+{Changelist}";
options.Environment = "production"; // or "staging", "development"
```

### Session Tracking

```csharp
// Sessions are tracked automatically, but you can add context
public void OnSessionStart()
{
    SentrySdk.ConfigureScope(scope =>
    {
        scope.SetTag("session.type", isFirstSession ? "new" : "returning");
        scope.SetTag("install.age", installAgeDays.ToString());
    });
}
```

## Mobile-Specific Considerations

### Memory Warnings

```csharp
private void OnEnable()
{
    Application.lowMemory += OnLowMemory;
}

private void OnLowMemory()
{
    SentrySdk.AddBreadcrumb(
        message: "Low memory warning",
        category: "performance",
        level: BreadcrumbLevel.Warning,
        data: new Dictionary<string, string>
        {
            { "used_mb", GetUsedMemoryMB().ToString() },
            { "zone", _currentZone }
        }
    );
}
```

### Background/Foreground

```csharp
private void OnApplicationPause(bool paused)
{
    if (paused)
    {
        SentrySdk.AddBreadcrumb("App backgrounded", "lifecycle");
        SentrySdk.FlushAsync(TimeSpan.FromSeconds(2)).Forget();
    }
    else
    {
        SentrySdk.AddBreadcrumb("App foregrounded", "lifecycle");
    }
}
```

### Network Connectivity

```csharp
SentrySdk.ConfigureScope(scope =>
{
    var reachability = Application.internetReachability;
    scope.SetTag("network.type", reachability switch
    {
        NetworkReachability.NotReachable => "none",
        NetworkReachability.ReachableViaLocalAreaNetwork => "wifi",
        NetworkReachability.ReachableViaCarrierDataNetwork => "cellular",
        _ => "unknown"
    });
});
```

## Debug Symbol Upload

### Unity Cloud Build / CI

```bash
# Upload debug symbols after build
sentry-cli debug-files upload \
  --org your-org \
  --project your-project \
  ./Library/Bee/artifacts/

# For iOS
sentry-cli debug-files upload \
  --org your-org \
  --project your-project \
  ./Builds/iOS/
```

### IL2CPP Symbols

```bash
# Upload IL2CPP line number mappings
sentry-cli debug-files upload \
  --include-sources \
  ./Library/Bee/artifacts/il2cpp/
```

## Best Practices

1. **Set user context early** - As soon as authentication completes
2. **Use transactions for key flows** - Zone loads, combat, purchases
3. **Add breadcrumbs liberally** - Help debug crash context
4. **Sample transactions** - 0.1-0.2 for production, 1.0 for debugging
5. **Use meaningful operation names** - `zone.load`, `combat.ability`, `ui.navigate`
6. **Add measurements** - Memory, FPS, timing data on transactions
7. **Filter noisy breadcrumbs** - HTTP spam, frequent events
8. **Upload debug symbols** - Critical for native crash symbolication
9. **Test in Editor** - Enable `CaptureInEditor` during development

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Check DSN, network, sample rate |
| Missing stack traces | Upload debug symbols |
| Too many events | Increase debounce time, filter |
| Performance impact | Reduce sample rate, async flush |
| Native crashes unsymbolicated | Upload dSYM/symbols |
