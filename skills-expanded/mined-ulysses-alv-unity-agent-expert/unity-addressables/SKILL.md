---
name: unity-addressables
description: >
  Unity 6000.3 LTS Addressables and asset loading patterns. Covers Addressables
  system, AssetBundles, async loading, memory management.
  Trigger: When loading assets at runtime, using Addressables,
  or managing asset bundles in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Load this skill when working with:
- Runtime asset loading from any source (local or remote)
- Dynamic content delivery, DLC, or downloadable assets
- Reducing initial application build size
- Platform-specific optimized assets (iOS, Android, PC)
- Async asset loading patterns
- Memory-sensitive asset management
- CDN-hosted content delivery

Common triggers:
- User mentions "Addressables", "AssetBundle", "load asset at runtime"
- Questions about `Resources.Load` alternatives
- Asset loading performance issues
- Memory management for large assets
- Prefab or scene streaming

---

## Critical Rules

### NEVER do these:

1. **Never load AssetBundle dependencies manually** — Use Addressables which auto-manages dependency chains. Manual dependency tracking leads to missing assets, null references, or crashes.

2. **Never use `Resources` folder for production assets** — Everything in Resources is bundled into the Player build, increasing startup time and build size. Use for prototyping ONLY.

3. **Never forget to unload AssetBundles** — Forgetting `Unload(false)` causes memory leaks. Always pair load operations with unload.

4. **Never assume AssetBundle compatibility across Unity versions** — AssetBundles built with older Unity can't load in newer versions without rebuilding. The serialization format changes between versions.

5. **Never load assets synchronously in large quantities** — This blocks the main thread and causes frame drops. ALWAYS use async APIs.

6. **Never hardcode asset paths with Addressables** — Use the address string, not the physical path. This allows relocating assets without code changes.

---

## Addressables System

### Overview

The Addressable Asset System provides a simple way to load assets by address rather than by direct reference. Once an asset is marked "addressable", it generates an address that can be called from anywhere. The system handles location (local or remote), dependency resolution, and async loading automatically.

**Key benefits:**
- Asynchronous loading from any location
- Automatic dependency management
- No need to track physical asset locations
- Simplified AssetBundle management
- Unity Editor GUI for asset organization

**Version compatibility:** Package version 2.9.1 is released for Unity Editor 6000.3. Available versions include 2.10.0 (released) and 2.9.1.

### Setting Up Addressables

```csharp
// Mark asset as addressable via Unity Editor:
// Window -> Asset Management -> Addressables
// Drag assets to groups in the Addressables Groups window

// Load by address — works for local AND remote assets
public async UniTask<GameObject> LoadPrefabAsync(string address)
{
    var handle = Addressables.LoadAssetAsync<GameObject>(address);
    var prefab = await handle.Task;
    return prefab;
}

// Instantiate after loading
public async UniTask InstantiatePrefab(string address, Vector3 position, Quaternion rotation)
{
    var handle = Addressables.LoadAssetAsync<GameObject>(address);
    var prefab = await handle.Task;
    var instance = UnityEngine.Object.Instantiate(prefab, position, rotation);
}
```

### Addressables vs AssetBundle API

| Feature | Addressables | AssetBundle API |
|---------|--------------|-----------------|
| Dependency tracking | Automatic | Manual |
| Remote hosting | Built-in | Manual (UnityWebRequest) |
| Editor interface | Yes | No |
| Memory management | Automatic | Manual |
| Reference counting | Built-in | Custom implementation needed |
| Catalog system | Yes | No |

### Loading Assets

```csharp
// Basic async loading
Addressables.LoadAssetAsync<T>(address);

// Multiple assets in parallel
public async UniTask<List<T>> LoadMultiple<T>(List<string> addresses)
{
    var tasks = addresses.Select(addr =>
        Addressables.LoadAssetAsync<T>(addr).Task
    );
    var results = await UniTask.WhenAll(tasks);
    return results.ToList();
}

// Release when done
Addressables.Release(handle);
```

### Asset References (Lazy Loading)

```csharp
// Use AssetReference for deferred loading
public class MyComponent : MonoBehaviour
{
    public AssetReference cubeReference;

    public async void LoadAndInstantiate()
    {
        if (cubeReference != null && cubeReference.RuntimeKeyIsValid())
        {
            var handle = cubeReference.LoadAssetAsync<GameObject>();
            await handle.Task;
            var cube = Instantiate(handle.Result);
        }
    }

    public void ReleaseAsset()
    {
        if (cubeReference != null)
        {
            cubeReference.ReleaseAsset();
        }
    }
}
```

---

## AssetBundles

### What is an AssetBundle?

An AssetBundle is an archive file containing grouped assets. Use it to:
- Create downloadable content (DLC)
- Reduce initial installation size
- Load optimized platform-specific assets
- Lower memory usage at runtime

AssetBundles are **platform-specific** — a bundle built for iOS won't work on Android. Each platform requires separate builds.

### AssetBundle Structure

The AssetBundle file format contains:
1. **Serialized files** — Unity objects in binary format (same as Player builds)
   - Single serialized file for assets-only bundles
   - Two serialized files per scene (hierarchy + referenced objects)
2. **Resource files** — Binary data for textures/audio, loaded via multithreaded code

The bundle includes an `AssetBundle` object that acts as a directory for contents.

### Manual AssetBundle Workflow

```csharp
// Build AssetBundles (low-level API)
var buildMap = new AssetBundleBuild[1];
buildMap[0] = new AssetBundleBuild
{
    assetBundleName = "mybundle",
    assetNames = new[] { "Assets/Prefabs/Cube.prefab" }
};

BuildPipeline.BuildAssetBundles(
    outputPath,
    buildMap,
    BuildAssetBundleOptions.None,
    BuildTarget.StandaloneWindows64
);

// Load AssetBundle
public AssetBundle LoadBundle(string path)
{
    return AssetBundle.LoadFromFile(path);
}

// Load asset from bundle
public T LoadAsset<T>(AssetBundle bundle, string assetName) where T : UnityEngine.Object
{
    return bundle.LoadAsset<T>(assetName);
}

// Unload when done
public void UnloadBundle(AssetBundle bundle, bool complete)
{
    bundle.Unload(complete);
}
```

### AssetBundle Dependencies

When AssetBundle A depends on AssetBundle B, you MUST load B before loading assets from A.

```csharp
public class AssetBundleManager
{
    private Dictionary<string, AssetBundle> loadedBundles = new();

    public async Task<T> LoadAssetWithDependencies<T>(string assetBundleName, string assetName)
    {
        // Load dependent bundles first
        string[] dependencies = GetDependencies(assetBundleName);
        foreach (var dep in dependencies)
        {
            if (!loadedBundles.ContainsKey(dep))
            {
                loadedBundles[dep] = await LoadBundleAsync(dep);
            }
        }

        // Now load the main bundle
        if (!loadedBundles.ContainsKey(assetBundleName))
        {
            loadedBundles[assetBundleName] = await LoadBundleAsync(assetBundleName);
        }

        return loadedBundles[assetBundleName].LoadAsset<T>(assetName);
    }

    private async Task<AssetBundle> LoadBundleAsync(string bundleName)
    {
        var request = AssetBundle.LoadFromFileAsync(Path.Combine(Application.streamingAssetsPath, bundleName));
        await request.task;
        return request.assetBundle;
    }
}
```

### Streaming Scene AssetBundles

AssetBundles containing scenes are special:
- Cannot mix scenes with other assets in same bundle
- Accessible via `AssetBundle.isStreamedSceneAssetBundle`
- Two serialized files per scene (hierarchy + references)

```csharp
public async Task LoadSceneBundle(string bundlePath, string sceneName)
{
    var bundleLoadRequest = AssetBundle.LoadFromFileAsync(bundlePath);
    await bundleLoadRequest.task;

    var bundle = bundleLoadRequest.assetBundle;
    if (bundle.isStreamedSceneAssetBundle)
    {
        var sceneLoadRequest = UnityEngine.SceneManagement.SceneManager.LoadSceneAsync(sceneName);
        await sceneLoadRequest;
    }
}
```

---

## Async Loading

### Why Async Matters

Synchronous asset loading blocks the main thread, causing:
- Frame drops and stuttering
- Poor user experience
- Potential timeouts on slow devices

ALWAYS use async APIs for asset loading, especially for:
- Remote assets (download time unpredictable)
- Large assets (textures, audio, models)
- Multiple assets (batch loading)

### Async Patterns for Addressables

```csharp
// Basic async/await pattern
public async UniTask<Sprite> LoadSpriteAsync(string address)
{
    var handle = Addressables.LoadAssetAsync<Sprite>(address);
    return await handle.Task;
}

// With progress tracking
public async UniTask<Sprite> LoadSpriteWithProgress(string address, IProgress<float> progress)
{
    var handle = Addressables.LoadAssetAsync<Sprite>(address);
    while (!handle.IsDone)
    {
        progress.Report(handle.percentComplete);
        await UniTask.Yield();
    }
    return handle.Result;
}

// Loading multiple with progress
public async UniTask<List<T>> LoadAllWithProgress<T>(
    List<string> addresses,
    IProgress<float> progress)
{
    var handles = addresses.Select(addr =>
        Addressables.LoadAssetAsync<T>(addr)).ToList();

    float total = addresses.Count;
    float current = 0;

    while (handles.Any(h => !h.IsDone))
    {
        float completed = handles.Count(h => h.IsDone);
        progress.Report(completed / total);
        await UniTask.Yield();
    }

    progress.Report(1f);
    return handles.Select(h => h.Result).ToList();
}
```

### Async Patterns for AssetBundle

```csharp
// AssetBundle.LoadFromFileAsync
public async Task<AssetBundle> LoadBundleAsync(string path)
{
    var request = AssetBundle.LoadFromFileAsync(path);
    await request.task;
    return request.assetBundle;
}

// AssetBundle.LoadFromMemoryAsync
public async Task<AssetBundle> LoadBundleFromMemoryAsync(byte[] data)
{
    var request = AssetBundle.LoadFromMemoryAsync(data);
    await request.task;
    return request.assetBundle;
}

// DownloadHandler-based loading (for remote)
using (var uwr = UnityWebRequestAssetBundle.GetAssetBundle(url))
{
    var operation = uwr.SendWebRequest();
    await operation;
    var bundle = DownloadHandlerAssetBundle.GetContent(uwr);
}
```

### Task-Based Loading Wrapper

```csharp
public static class AssetLoader
{
    public static async Task<T> LoadAddressable<T>(string address) where T : UnityEngine.Object
    {
        var handle = Addressables.LoadAssetAsync<T>(address);
        var result = await handle.Task;
        return result;
    }

    public static async Task<T> LoadAssetBundleAsset<T>(string bundlePath, string assetName) where T : UnityEngine.Object
    {
        var bundleRequest = AssetBundle.LoadFromFileAsync(bundlePath);
        await bundleRequest.task;
        var bundle = bundleRequest.assetBundle;
        var assetRequest = bundle.LoadAssetAsync<T>(assetName);
        await assetRequest.task;
        return assetRequest.asset as T;
    }

    public static void UnloadBundle(AssetBundle bundle, bool unloadAllObjects = false)
    {
        if (bundle != null)
        {
            bundle.Unload(unloadAllObjects);
        }
    }
}
```

---

## Memory Management

### Critical Memory Rules

1. **Always unload unused AssetBundles** — Failure to do so causes memory leaks
2. **Use `Unload(false)` to keep loaded assets** — Only unload the bundle container
3. **Use `Unload(true)` when done with loaded assets** — Also unloads all assets from that bundle
4. **Track dependency chains** — Don't unload a bundle that another bundle depends on

### Unload Strategies

```csharp
// Unload bundle but keep loaded assets (false)
// Use when you want to keep the GameObject/instances alive
bundle.Unload(false);

// Unload everything including loaded assets (true)
// Use when you're done with both the bundle AND its assets
bundle.Unload(true);
```

### Addressables Release Patterns

```csharp
// Release individual handle
var handle = Addressables.LoadAssetAsync<GameObject>(address);
var obj = await handle.Task;
Addressables.Release(handle);

// Release AssetReference
public void ReleaseReference(AssetReference reference)
{
    if (reference != null && reference.RuntimeKeyIsValid())
    {
        reference.ReleaseAsset();
    }
}

// Automatic cleanup with UniTask
public async UniTask&lt;GameObject&gt; LoadAndRelease(string address)
{
    var handle = Addressables.LoadAssetAsync&lt;GameObject&gt;(address);
    var result = await handle.Task;
    Addressables.Release(handle);
    return result;
}
```

### Memory Monitoring

```csharp
public class MemoryMonitor
{
    public long GetTotalAllocatedMemory()
    {
        return GC.GetTotalMemory(false);
    }

    public async Task UnloadUnusedAssets()
    {
        await Resources.UnloadUnusedAssets();
        System.GC.Collect();
    }

    public bool IsMemoryPressureHigh(float thresholdMB = 500f)
    {
        var allocated = GC.GetTotalMemory(false) / (1024f * 1024f);
        return allocated > thresholdMB;
    }
}
```

### AssetBundle Reference Counting

Implement reference counting for complex dependency graphs:

```csharp
public class AssetBundleRegistry
{
    private Dictionary<string, int> referenceCounts = new();
    private Dictionary<string, AssetBundle> loadedBundles = new();

    public void Increment(string bundleName)
    {
        if (!referenceCounts.ContainsKey(bundleName))
            referenceCounts[bundleName] = 0;
        referenceCounts[bundleName]++;
    }

    public void Decrement(string bundleName)
    {
        if (referenceCounts.ContainsKey(bundleName))
        {
            referenceCounts[bundleName]--;
            if (referenceCounts[bundleName] <= 0)
            {
                UnloadBundle(bundleName);
            }
        }
    }

    private void UnloadBundle(string bundleName)
    {
        if (loadedBundles.ContainsKey(bundleName))
        {
            loadedBundles[bundleName].Unload(true);
            loadedBundles.Remove(bundleName);
            referenceCounts.Remove(bundleName);
        }
    }
}
```

---

## Common Mistakes to Prevent

### 1. Missing Dependencies

**Problem:** Asset loads but dependencies (textures, materials) are missing.

**Solution:** Use Addressables — it auto-loads dependencies. If using AssetBundle API, manually load all dependent bundles first.

```csharp
// WRONG - might have missing materials
var bundle = AssetBundle.LoadFromFile("myprefab");
var prefab = bundle.LoadAsset<GameObject>("MyPrefab");

// CORRECT - load dependencies first
var deps = bundle.GetAllDependencies("MyPrefab");
foreach (var dep in deps)
{
    AssetBundle.LoadFromFile(dep);
}
// Then load the main asset
```

### 2. Forgetting to Unload

**Problem:** Memory leak, game crashes after loading many assets.

**Solution:** Always track and unload bundles.

```csharp
// WRONG
AssetBundle bundle = AssetBundle.LoadFromFile(path);
var prefab = bundle.LoadAsset<GameObject>("MyPrefab");
Instantiate(prefab);
// bundle never unloaded!

// CORRECT
AssetBundle bundle = AssetBundle.LoadFromFile(path);
var prefab = bundle.LoadAsset<GameObject>("MyPrefab");
Instantiate(prefab);
bundle.Unload(false); // Unload bundle but keep prefab
```

### 3. Synchronous Loading on Main Thread

**Problem:** Frame drops, frozen UI, poor performance.

**Solution:** Always use async APIs.

```csharp
// WRONG - blocks main thread
var bundle = AssetBundle.LoadFromFile(path);
var tex = bundle.LoadAsset<Texture2D>("bigtexture");

// CORRECT - async loading
var request = AssetBundle.LoadFromFileAsync(path);
await request.task;
var bundle = request.assetBundle;
var texRequest = bundle.LoadAssetAsync<Texture2D>("bigtexture");
await texRequest.task;
```

### 4. Hardcoding Paths or Asset Names

**Problem:** Code breaks when assets are moved or renamed.

**Solution:** Use Addressables addresses, not file paths.

```csharp
// WRONG
var bundle = AssetBundle.LoadFromFile(Application.dataPath + "/../Bundles/prefabs");
var prefab = bundle.LoadAsset<GameObject>("Assets/Prefabs/Cube.prefab");

// CORRECT
var prefab = await Addressables.LoadAssetAsync<GameObject>("Prefabs/Cube").Task;
```

### 5. Not Handling Load Failures

**Problem:** Null reference crashes when asset doesn't exist.

**Solution:** Always check for null and handle errors gracefully.

```csharp
public async UniTask&lt;T&gt; SafeLoad&lt;T&gt;(string address) where T : UnityEngine.Object
{
    var handle = Addressables.LoadAssetAsync&lt;T&gt;(address);

    try
    {
        var result = await handle.Task;
        if (result == null)
        {
            Debug.LogWarning($"[AssetLoader] Asset at '{address}' is null after loading.");
            return null;
        }
        return result;
    }
    catch (Exception ex)
    {
        Debug.LogError($"[AssetLoader] Failed to load '{address}': {ex.Message}");
        return null;
    }
}
```

### 6. Loading Assets Before Scene Unload

**Problem:** Assets reference scenes that are unloaded, causing errors.

**Solution:** Unload old scenes before loading dependent assets.

```csharp
public async Task TransitionToScene(string newSceneAddress)
{
    // Get current scene dependencies
    var currentScene = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
    var dependencies = UnityEngine.AddressableAssets.Addressables.GetSceneountains(currentScene.name);

    // Unload current scene
    await UnityEngine.SceneManagement.SceneManager.UnloadSceneAsync(currentScene);

    // Load new scene
    await UnityEngine.AddressableAssets.Addressables.LoadSceneAsync(newSceneAddress);
}
```

---

## Response Format

When answering Unity addressables questions, always:

1. **Check context** — Are they using Addressables package or raw AssetBundle API?
2. **Provide working code examples** — Show async patterns, not sync
3. **Mention memory implications** — Unload considerations, dependency chains
4. **Offer alternatives** — When Addressables overkill vs when necessary
5. **Warn about common mistakes** — Based on the "Common Mistakes" section

### Response Template

```
## Quick Answer
[Direct answer to the question]

## Code Example
```csharp
[Working async code example]
```

## Memory Considerations
[What to watch out for regarding memory]

## Common Pitfalls
[How to avoid the most common mistake for this scenario]

## Alternative Approaches
[If applicable, other ways to solve the same problem]
```

### When recommending Addressables:
- Projects with remote/CDN content
- Apps needing dynamic updates/DLC
- Games with large asset catalogs
- Cross-platform asset management

### When NOT recommending Addressables:
- Small prototypes with fixed assets
- Assets that are always needed at startup
- Simple projects with minimal assets
- Cases where Resources folder is acceptable (bootstrapping only)

---

## Source Documentation

Based on Unity 6000.3 LTS documentation:
- `com.unity.addressables@2.10` (released)
- `com.unity.addressables@2.9` (compatible with 6000.3)