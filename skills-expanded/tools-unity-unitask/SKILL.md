---
name: tools-unity-unitask
description: UniTask async/await patterns for Unity including cancellation, lifecycle binding, and coroutine interop.
---

# UniTask Async/Await for Unity

## Overview

UniTask provides efficient async/await support for Unity with zero allocation, proper cancellation, and Unity lifecycle integration.

## When to Use

- Async operations in Unity (loading, networking, delays)
- Replacing coroutines with async/await
- Managing cancellation in MonoBehaviours
- Async initialization patterns
- Parallel async operations

## Installation

```json
// manifest.json
"com.cysharp.unitask": "https://github.com/Cysharp/UniTask.git?path=src/UniTask/Assets/Plugins/UniTask"
```

## Basic Patterns

### Simple Async Method

```csharp
public async UniTask LoadGameAsync()
{
    await UniTask.Delay(1000); // 1 second delay
    await LoadAssetsAsync();
    await InitializeSystemsAsync();
}
```

### Async with Return Value

```csharp
public async UniTask<PlayerData> LoadPlayerAsync()
{
    var json = await File.ReadAllTextAsync(path);
    return JsonUtility.FromJson<PlayerData>(json);
}
```

### Fire-and-Forget (Use Carefully!)

```csharp
// ForgetTask() suppresses warnings but loses error handling
LoadGameAsync().Forget();

// Better: Use UniTaskVoid for true fire-and-forget
public async UniTaskVoid StartBackgroundTask()
{
    try
    {
        await DoWorkAsync();
    }
    catch (Exception ex)
    {
        Debug.LogException(ex);
    }
}
```

## Cancellation Patterns

### Basic CancellationToken

```csharp
public class GameLoader : MonoBehaviour
{
    private CancellationTokenSource _cts;
    
    private void OnEnable()
    {
        _cts = new CancellationTokenSource();
        LoadAsync(_cts.Token).Forget();
    }
    
    private void OnDisable()
    {
        _cts?.Cancel();
        _cts?.Dispose();
        _cts = null;
    }
    
    private async UniTask LoadAsync(CancellationToken ct)
    {
        await UniTask.Delay(1000, cancellationToken: ct);
        // Work here...
    }
}
```

### Destroy CancellationToken (Preferred for MonoBehaviour)

```csharp
public class Enemy : MonoBehaviour
{
    private async UniTaskVoid Start()
    {
        // Automatically cancelled when GameObject destroyed
        var ct = this.GetCancellationTokenOnDestroy();
        
        while (!ct.IsCancellationRequested)
        {
            await UniTask.Delay(1000, cancellationToken: ct);
            Patrol();
        }
    }
}
```

### Linked Cancellation

```csharp
public async UniTask DoWorkAsync(CancellationToken externalCt)
{
    // Link external token with destroy token
    var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
        externalCt,
        this.GetCancellationTokenOnDestroy()
    );
    
    try
    {
        await LongRunningTask(linkedCts.Token);
    }
    finally
    {
        linkedCts.Dispose();
    }
}
```

### Timeout

```csharp
// Timeout with exception
await task.Timeout(TimeSpan.FromSeconds(5));

// Timeout without exception
var (hasValue, result) = await task.TimeoutWithoutException(TimeSpan.FromSeconds(5));
if (!hasValue)
{
    Debug.Log("Operation timed out");
}

// Timeout with CancellationTokenSource
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
await task.AttachExternalCancellation(cts.Token);
```

## Unity Lifecycle Integration

### Waiting for Frames

```csharp
// Wait one frame
await UniTask.Yield();

// Wait for end of frame
await UniTask.WaitForEndOfFrame();

// Wait for fixed update
await UniTask.WaitForFixedUpdate();

// Wait multiple frames
await UniTask.DelayFrame(10);

// Wait for specific player loop
await UniTask.Yield(PlayerLoopTiming.PreUpdate);
```

### Player Loop Timing Options

```csharp
// Available timings:
PlayerLoopTiming.Initialization
PlayerLoopTiming.EarlyUpdate
PlayerLoopTiming.FixedUpdate
PlayerLoopTiming.PreUpdate
PlayerLoopTiming.Update
PlayerLoopTiming.PreLateUpdate
PlayerLoopTiming.PostLateUpdate
PlayerLoopTiming.TimeUpdate
```

### Waiting for Conditions

```csharp
// Wait until condition is true
await UniTask.WaitUntil(() => player.IsReady);

// Wait while condition is true
await UniTask.WaitWhile(() => isLoading);

// Wait until with cancellation
await UniTask.WaitUntil(
    () => player.IsReady,
    cancellationToken: ct
);

// Wait until with timeout
await UniTask.WaitUntil(() => player.IsReady)
    .Timeout(TimeSpan.FromSeconds(10));
```

### Waiting for Unity Events

```csharp
// Wait for button click
await button.OnClickAsync();

// Wait for trigger enter
var other = await gameObject.OnTriggerEnterAsync();

// Wait for collision
var collision = await gameObject.OnCollisionEnterAsync();

// Wait for animation event
await animator.WaitForAnimationEvent("AttackHit");
```

## Parallel Operations

### WhenAll (Wait for All)

```csharp
// Wait for all tasks to complete
var results = await UniTask.WhenAll(
    LoadTexturesAsync(),
    LoadAudioAsync(),
    LoadConfigAsync()
);

// With different return types
var (textures, audio, config) = await UniTask.WhenAll(
    LoadTexturesAsync(),
    LoadAudioAsync(),
    LoadConfigAsync()
);
```

### WhenAny (Wait for First)

```csharp
// Wait for first to complete
var (winIndex, result1, result2) = await UniTask.WhenAny(
    TryServerAAsync(),
    TryServerBAsync()
);

// Use winner
if (winIndex == 0)
{
    UseResult(result1);
}
```

### Throttling Parallel Operations

```csharp
// Process with limited concurrency
var semaphore = new SemaphoreSlim(3); // Max 3 concurrent

await UniTask.WhenAll(items.Select(async item =>
{
    await semaphore.WaitAsync();
    try
    {
        await ProcessItemAsync(item);
    }
    finally
    {
        semaphore.Release();
    }
}));
```

## Coroutine Interop

### Convert Coroutine to UniTask

```csharp
// Wrap existing coroutine
await MyCoroutine().ToUniTask();

// With cancellation
await MyCoroutine().ToUniTask(cancellationToken: ct);

// From IEnumerator
IEnumerator LegacyCoroutine()
{
    yield return new WaitForSeconds(1);
}

await LegacyCoroutine().ToUniTask();
```

### Convert UniTask to Coroutine

```csharp
// For APIs that require coroutines
StartCoroutine(MyUniTask().ToCoroutine());
```

### Async Trigger Components

```csharp
// Add async triggers to GameObjects
var trigger = gameObject.GetAsyncTriggerEnterTrigger();

// Wait for trigger
var other = await trigger.OnTriggerEnterAsync();
```

## Resource Loading

### Addressables Integration

```csharp
public async UniTask<T> LoadAssetAsync<T>(string address, CancellationToken ct)
{
    var handle = Addressables.LoadAssetAsync<T>(address);
    
    try
    {
        return await handle.ToUniTask(cancellationToken: ct);
    }
    catch (OperationCanceledException)
    {
        Addressables.Release(handle);
        throw;
    }
}
```

### Scene Loading

```csharp
public async UniTask LoadSceneAsync(string sceneName, CancellationToken ct)
{
    await SceneManager.LoadSceneAsync(sceneName)
        .ToUniTask(cancellationToken: ct);
}

// With progress
public async UniTask LoadSceneWithProgressAsync(string sceneName, IProgress<float> progress)
{
    await SceneManager.LoadSceneAsync(sceneName)
        .ToUniTask(progress: progress);
}
```

### Asset Bundle Loading

```csharp
public async UniTask<AssetBundle> LoadBundleAsync(string url, CancellationToken ct)
{
    var request = UnityWebRequestAssetBundle.GetAssetBundle(url);
    
    await request.SendWebRequest().ToUniTask(cancellationToken: ct);
    
    if (request.result != UnityWebRequest.Result.Success)
    {
        throw new Exception(request.error);
    }
    
    return DownloadHandlerAssetBundle.GetContent(request);
}
```

## Error Handling

### Try-Catch Pattern

```csharp
public async UniTask SafeLoadAsync()
{
    try
    {
        await LoadDataAsync();
    }
    catch (OperationCanceledException)
    {
        // Expected when cancelled - don't log as error
        Debug.Log("Load cancelled");
    }
    catch (Exception ex)
    {
        Debug.LogException(ex);
        ShowErrorUI();
    }
}
```

### SuppressCancellationThrow

```csharp
// Returns (isCancelled, result) instead of throwing
var (cancelled, result) = await LoadAsync()
    .SuppressCancellationThrow();

if (cancelled)
{
    return; // Graceful exit
}

ProcessResult(result);
```

### Exception Handling in WhenAll

```csharp
// Collect all exceptions
try
{
    await UniTask.WhenAll(tasks);
}
catch (AggregateException ae)
{
    foreach (var ex in ae.InnerExceptions)
    {
        Debug.LogException(ex);
    }
}
```

## Progress Reporting

### IProgress<float>

```csharp
public async UniTask LoadWithProgressAsync(IProgress<float> progress, CancellationToken ct)
{
    var items = await GetItemsAsync();
    
    for (int i = 0; i < items.Count; i++)
    {
        await ProcessItemAsync(items[i], ct);
        progress?.Report((float)(i + 1) / items.Count);
    }
}

// Usage
var progress = new Progress<float>(p => loadingBar.value = p);
await LoadWithProgressAsync(progress, ct);
```

### Custom Progress

```csharp
public struct LoadProgress
{
    public string CurrentItem;
    public int Loaded;
    public int Total;
    public float Percent => (float)Loaded / Total;
}

public async UniTask LoadAsync(IProgress<LoadProgress> progress)
{
    var items = await GetItemsAsync();
    
    for (int i = 0; i < items.Count; i++)
    {
        progress?.Report(new LoadProgress
        {
            CurrentItem = items[i].Name,
            Loaded = i + 1,
            Total = items.Count
        });
        
        await ProcessItemAsync(items[i]);
    }
}
```

## UniTask vs Task

### When to Use UniTask

```csharp
// Unity main thread operations
await UniTask.Delay(1000);              // Use UniTask
await UniTask.Yield();                   // Use UniTask
await SceneManager.LoadSceneAsync(s);    // Use UniTask

// Fire and forget in Unity
DoWorkAsync().Forget();                  // UniTask only
```

### When to Use Task

```csharp
// Pure .NET operations (no Unity API)
await File.ReadAllTextAsync(path);       // Task is fine
await Task.Run(() => HeavyComputation()); // Task for thread pool

// Converting
var result = await task.AsUniTask();     // Task to UniTask
var task = unitask.AsTask();             // UniTask to Task
```

## Common Pitfalls

### Pitfall 1: Missing CancellationToken

```csharp
// BAD: No cancellation, leaks when object destroyed
public async UniTaskVoid Start()
{
    await UniTask.Delay(10000);
    DoSomething(); // May crash if destroyed
}

// GOOD: Use destroy token
public async UniTaskVoid Start()
{
    await UniTask.Delay(10000, cancellationToken: destroyCancellationToken);
    DoSomething();
}
```

### Pitfall 2: Forget Without Error Handling

```csharp
// BAD: Exceptions silently swallowed
DoWorkAsync().Forget();

// GOOD: Handle errors
async UniTaskVoid DoWorkSafe()
{
    try
    {
        await DoWorkAsync();
    }
    catch (Exception ex) when (!(ex is OperationCanceledException))
    {
        Debug.LogException(ex);
    }
}
DoWorkSafe().Forget();
```

### Pitfall 3: Blocking on Main Thread

```csharp
// BAD: Blocks main thread
var result = LoadAsync().GetAwaiter().GetResult();

// GOOD: Await properly
var result = await LoadAsync();
```

### Pitfall 4: Unnecessary Allocations

```csharp
// BAD: Allocates closure
await UniTask.Delay(1000).ContinueWith(_ => DoSomething());

// GOOD: Just await
await UniTask.Delay(1000);
DoSomething();
```

## Best Practices

1. **Always use CancellationToken** for MonoBehaviour async methods
2. **Use GetCancellationTokenOnDestroy()** for automatic cleanup
3. **Handle OperationCanceledException** separately from other exceptions
4. **Prefer UniTask over Task** for Unity operations
5. **Use WhenAll** for parallel operations
6. **Report progress** for long-running operations
7. **Use SuppressCancellationThrow** for optional cancellation handling
8. **Avoid Forget()** without proper error handling

## Performance Tips

- UniTask is struct-based (zero allocation when awaited directly)
- Avoid unnecessary `.AsTask()` conversions
- Use `UniTask.Yield()` instead of `await UniTask.Delay(0)`
- Pool `CancellationTokenSource` for high-frequency operations
- Use `UniTaskCompletionSource` for custom async patterns
