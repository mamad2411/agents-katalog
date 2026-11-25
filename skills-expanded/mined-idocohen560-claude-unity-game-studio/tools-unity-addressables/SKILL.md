---
name: tools-unity-addressables
description: Unity Addressables patterns for asset loading, memory management, reference counting, and remote content delivery.
---

# Unity Addressables

## Overview

Addressables provides a system for loading assets by address, with automatic dependency management, memory tracking, and remote content delivery support.

## When to Use

- Loading assets dynamically at runtime
- Managing asset memory lifecycle
- Implementing remote asset downloads
- Reducing build size with asset bundles
- Loading scenes asynchronously

## Core Concepts

### Asset References

```csharp
// In inspector - reference to addressable asset
[SerializeField] private AssetReference _prefabReference;
[SerializeField] private AssetReferenceT<AudioClip> _audioReference;
[SerializeField] private AssetReferenceSprite _spriteReference;
[SerializeField] private AssetReferenceGameObject _gameObjectReference;
```

### Loading by Address (String)

```csharp
// Load by address string
var handle = Addressables.LoadAssetAsync<GameObject>("Prefabs/Enemy");
var prefab = await handle.Task;

// Or with UniTask
var prefab = await Addressables.LoadAssetAsync<GameObject>("Prefabs/Enemy").ToUniTask();
```

### Loading by AssetReference

```csharp
// Load from serialized reference
var handle = _prefabReference.LoadAssetAsync<GameObject>();
var prefab = await handle.ToUniTask();
```

## Loading Patterns

### Basic Asset Loading

```csharp
public class AssetLoader
{
    private AsyncOperationHandle<GameObject> _handle;
    
    public async UniTask<GameObject> LoadAsync(string address, CancellationToken ct)
    {
        _handle = Addressables.LoadAssetAsync<GameObject>(address);
        
        try
        {
            return await _handle.ToUniTask(cancellationToken: ct);
        }
        catch (OperationCanceledException)
        {
            // Release on cancellation
            if (_handle.IsValid())
                Addressables.Release(_handle);
            throw;
        }
    }
    
    public void Unload()
    {
        if (_handle.IsValid())
        {
            Addressables.Release(_handle);
            _handle = default;
        }
    }
}
```

### Instantiate with Auto-Release

```csharp
// Instantiate and track for automatic release
var handle = Addressables.InstantiateAsync(address, parent);
var instance = await handle.ToUniTask();

// Later: Release when done (also destroys GameObject)
Addressables.ReleaseInstance(instance);

// OR release handle directly
Addressables.Release(handle);
```

### Load Multiple Assets

```csharp
public async UniTask<IList<T>> LoadAllAsync<T>(string label, CancellationToken ct)
{
    var handle = Addressables.LoadAssetsAsync<T>(
        label,
        obj => Debug.Log($"Loaded: {obj}") // Per-asset callback
    );
    
    return await handle.ToUniTask(cancellationToken: ct);
}

// Usage
var allEnemies = await LoadAllAsync<GameObject>("Enemies", ct);
```

### Load with Dependencies

```csharp
public async UniTask<T> LoadWithDependenciesAsync<T>(string address, CancellationToken ct)
{
    // Get download size first
    var sizeHandle = Addressables.GetDownloadSizeAsync(address);
    var size = await sizeHandle.ToUniTask();
    
    if (size > 0)
    {
        // Download dependencies
        var downloadHandle = Addressables.DownloadDependenciesAsync(address);
        await downloadHandle.ToUniTask(cancellationToken: ct);
        Addressables.Release(downloadHandle);
    }
    
    // Load asset
    var loadHandle = Addressables.LoadAssetAsync<T>(address);
    return await loadHandle.ToUniTask(cancellationToken: ct);
}
```

## Reference Counting

### Understanding Reference Counts

```csharp
// Each Load increments ref count
var handle1 = Addressables.LoadAssetAsync<T>(address); // RefCount = 1
var handle2 = Addressables.LoadAssetAsync<T>(address); // RefCount = 2 (same asset)

// Each Release decrements
Addressables.Release(handle1); // RefCount = 1
Addressables.Release(handle2); // RefCount = 0 (asset unloaded)
```

### Safe Resource Loader Pattern

```csharp
public class ResourceLoader : IDisposable
{
    private readonly Dictionary<string, AsyncOperationHandle> _loadedAssets = new();
    private readonly object _lock = new();
    
    public async UniTask<T> LoadAssetAsync<T>(string key, CancellationToken ct = default)
    {
        lock (_lock)
        {
            if (_loadedAssets.TryGetValue(key, out var existingHandle))
            {
                return (T)existingHandle.Result;
            }
        }
        
        var handle = Addressables.LoadAssetAsync<T>(key);
        
        try
        {
            var result = await handle.ToUniTask(cancellationToken: ct);
            
            lock (_lock)
            {
                _loadedAssets[key] = handle;
            }
            
            return result;
        }
        catch
        {
            if (handle.IsValid())
                Addressables.Release(handle);
            throw;
        }
    }
    
    public async UniTask ReleaseAll(bool immediate = false)
    {
        List<AsyncOperationHandle> handles;
        
        lock (_lock)
        {
            handles = _loadedAssets.Values.ToList();
            _loadedAssets.Clear();
        }
        
        foreach (var handle in handles)
        {
            if (handle.IsValid())
                Addressables.Release(handle);
        }
        
        if (!immediate)
            await UniTask.Yield(); // Allow cleanup
    }
    
    public void Dispose()
    {
        ReleaseAll(true).Forget();
    }
}
```

## Scene Loading

### Load Scene Additively

```csharp
public async UniTask<SceneInstance> LoadSceneAsync(
    string sceneAddress,
    LoadSceneMode mode = LoadSceneMode.Additive,
    CancellationToken ct = default)
{
    var handle = Addressables.LoadSceneAsync(sceneAddress, mode);
    return await handle.ToUniTask(cancellationToken: ct);
}

// Unload scene
public async UniTask UnloadSceneAsync(SceneInstance scene)
{
    var handle = Addressables.UnloadSceneAsync(scene);
    await handle.ToUniTask();
}
```

### Scene with Activation Control

```csharp
public async UniTask<SceneInstance> LoadSceneWithDelayedActivation(string address)
{
    var handle = Addressables.LoadSceneAsync(
        address,
        LoadSceneMode.Additive,
        activateOnLoad: false // Don't activate immediately
    );
    
    var scene = await handle.ToUniTask();
    
    // Do preparation work...
    await PrepareSceneAsync();
    
    // Now activate
    await scene.ActivateAsync().ToUniTask();
    
    return scene;
}
```

## Remote Content Delivery

### Check for Updates

```csharp
public async UniTask<bool> CheckForUpdatesAsync()
{
    var checkHandle = Addressables.CheckForCatalogUpdates();
    var catalogs = await checkHandle.ToUniTask();
    Addressables.Release(checkHandle);
    
    return catalogs != null && catalogs.Count > 0;
}
```

### Update Catalogs

```csharp
public async UniTask UpdateCatalogsAsync(IProgress<float> progress = null)
{
    var checkHandle = Addressables.CheckForCatalogUpdates();
    var catalogs = await checkHandle.ToUniTask();
    
    if (catalogs != null && catalogs.Count > 0)
    {
        var updateHandle = Addressables.UpdateCatalogs(catalogs);
        await updateHandle.ToUniTask();
        Addressables.Release(updateHandle);
    }
    
    Addressables.Release(checkHandle);
}
```

### Download Content

```csharp
public async UniTask DownloadContentAsync(
    string label,
    IProgress<float> progress,
    CancellationToken ct)
{
    // Get download size
    var sizeHandle = Addressables.GetDownloadSizeAsync(label);
    var totalSize = await sizeHandle.ToUniTask();
    Addressables.Release(sizeHandle);
    
    if (totalSize <= 0)
    {
        Debug.Log("All content already downloaded");
        return;
    }
    
    Debug.Log($"Downloading {totalSize / 1_000_000f:F2} MB");
    
    // Download
    var downloadHandle = Addressables.DownloadDependenciesAsync(label);
    
    // Report progress
    while (!downloadHandle.IsDone)
    {
        progress?.Report(downloadHandle.PercentComplete);
        
        if (ct.IsCancellationRequested)
        {
            Addressables.Release(downloadHandle);
            throw new OperationCanceledException(ct);
        }
        
        await UniTask.Yield();
    }
    
    if (downloadHandle.Status != AsyncOperationStatus.Succeeded)
    {
        var error = downloadHandle.OperationException?.Message ?? "Unknown error";
        Addressables.Release(downloadHandle);
        throw new Exception($"Download failed: {error}");
    }
    
    Addressables.Release(downloadHandle);
}
```

### Clear Cache

```csharp
public async UniTask ClearCacheAsync()
{
    // Clear all cached bundles
    Caching.ClearCache();
    
    // Re-initialize Addressables
    await Addressables.InitializeAsync().ToUniTask();
}

public bool ClearCacheForKey(string key)
{
    var locator = Addressables.ResourceLocators.FirstOrDefault();
    if (locator != null && locator.Locate(key, typeof(object), out var locations))
    {
        foreach (var location in locations)
        {
            Caching.ClearAllCachedVersions(location.InternalId);
        }
        return true;
    }
    return false;
}
```

## Progress Reporting

### Download Progress

```csharp
public struct DownloadProgress
{
    public long TotalBytes;
    public long DownloadedBytes;
    public float Percent;
    public string CurrentFile;
}

public async UniTask DownloadWithDetailedProgress(
    string label,
    IProgress<DownloadProgress> progress,
    CancellationToken ct)
{
    var sizeHandle = Addressables.GetDownloadSizeAsync(label);
    var totalBytes = await sizeHandle.ToUniTask();
    Addressables.Release(sizeHandle);
    
    var downloadHandle = Addressables.DownloadDependenciesAsync(label);
    
    while (!downloadHandle.IsDone)
    {
        ct.ThrowIfCancellationRequested();
        
        var status = downloadHandle.GetDownloadStatus();
        
        progress?.Report(new DownloadProgress
        {
            TotalBytes = totalBytes,
            DownloadedBytes = status.DownloadedBytes,
            Percent = status.Percent,
            CurrentFile = status.DownloadedBytes.ToString()
        });
        
        await UniTask.Yield();
    }
    
    Addressables.Release(downloadHandle);
}
```

## Memory Management

### Preloading Assets

```csharp
public class AssetPreloader
{
    private readonly List<AsyncOperationHandle> _preloadedHandles = new();
    
    public async UniTask PreloadAsync(IEnumerable<string> addresses, CancellationToken ct)
    {
        var tasks = addresses.Select(async addr =>
        {
            var handle = Addressables.LoadAssetAsync<object>(addr);
            await handle.ToUniTask(cancellationToken: ct);
            _preloadedHandles.Add(handle);
        });
        
        await UniTask.WhenAll(tasks);
    }
    
    public void ReleaseAll()
    {
        foreach (var handle in _preloadedHandles)
        {
            if (handle.IsValid())
                Addressables.Release(handle);
        }
        _preloadedHandles.Clear();
    }
}
```

### Memory Budget Tracking

```csharp
public class AddressableMemoryTracker
{
    public long GetEstimatedMemoryUsage()
    {
        long total = 0;
        
        // This is approximate - actual tracking requires custom implementation
        foreach (var locator in Addressables.ResourceLocators)
        {
            // Track loaded bundles
        }
        
        return total;
    }
    
    public void LogLoadedAssets()
    {
        // Use Addressables Event Viewer in Editor
        // For runtime, implement custom tracking
    }
}
```

## Error Handling

### Robust Loading Pattern

```csharp
public async UniTask<T> LoadWithRetryAsync<T>(
    string address,
    int maxRetries = 3,
    CancellationToken ct = default)
{
    Exception lastException = null;
    
    for (int attempt = 0; attempt < maxRetries; attempt++)
    {
        try
        {
            var handle = Addressables.LoadAssetAsync<T>(address);
            return await handle.ToUniTask(cancellationToken: ct);
        }
        catch (OperationCanceledException)
        {
            throw;
        }
        catch (Exception ex)
        {
            lastException = ex;
            Debug.LogWarning($"Load attempt {attempt + 1} failed: {ex.Message}");
            
            if (attempt < maxRetries - 1)
            {
                await UniTask.Delay(1000 * (attempt + 1), cancellationToken: ct);
            }
        }
    }
    
    throw new Exception($"Failed to load {address} after {maxRetries} attempts", lastException);
}
```

### Handle Invalid Operations

```csharp
public void SafeRelease<T>(ref AsyncOperationHandle<T> handle)
{
    if (handle.IsValid())
    {
        try
        {
            Addressables.Release(handle);
        }
        catch (Exception ex)
        {
            Debug.LogWarning($"Error releasing handle: {ex.Message}");
        }
        finally
        {
            handle = default;
        }
    }
}
```

## Best Practices

1. **Always release loaded assets** when done
2. **Use labels** for grouping related assets
3. **Preload critical assets** during loading screens
4. **Check download size** before downloading
5. **Handle cancellation** properly
6. **Use typed AssetReferences** in inspector
7. **Profile memory** with Addressables Event Viewer
8. **Test remote loading** early in development
9. **Implement retry logic** for network operations
10. **Clear cache** when updating content significantly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Asset not found | Check address spelling, rebuild addressables |
| Memory leak | Ensure all handles are released |
| Slow loading | Use preloading, check bundle sizes |
| Download fails | Check network, implement retry |
| Duplicate loading | Track loaded assets, use singleton loader |
| Cache issues | Clear cache, check catalog version |
