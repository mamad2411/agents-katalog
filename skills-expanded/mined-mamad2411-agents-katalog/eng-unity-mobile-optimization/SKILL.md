---
name: eng-unity-mobile-optimization
description: Mobile-specific Unity optimization patterns for memory, battery, thermal, and performance.
---

# Unity Mobile Optimization

## Overview

Mobile platforms have unique constraints: limited memory, battery life, thermal throttling, and variable hardware. This skill covers mobile-specific optimization techniques.

## When to Use

- iOS and Android development
- Battery-sensitive applications
- Memory-constrained devices
- Thermal management
- Variable quality settings

## Memory Management

### Memory Budget System

```csharp
public class MobileMemoryManager : MonoBehaviour
{
    [SerializeField] private long _warningThresholdMB = 800;
    [SerializeField] private long _criticalThresholdMB = 1000;
    
    public event Action OnMemoryWarning;
    public event Action OnMemoryCritical;
    
    private void Awake()
    {
        // iOS memory warning callback
        Application.lowMemory += OnLowMemory;
    }
    
    private void OnDestroy()
    {
        Application.lowMemory -= OnLowMemory;
    }
    
    private void OnLowMemory()
    {
        Debug.LogWarning("Low memory warning received");
        OnMemoryCritical?.Invoke();
        
        // Emergency cleanup
        Resources.UnloadUnusedAssets();
        GC.Collect();
    }
    
    public MemoryStatus GetMemoryStatus()
    {
        long usedMB = Profiler.GetTotalAllocatedMemoryLong() / 1_000_000;
        
        if (usedMB >= _criticalThresholdMB)
            return MemoryStatus.Critical;
        if (usedMB >= _warningThresholdMB)
            return MemoryStatus.Warning;
        return MemoryStatus.Normal;
    }
    
    public void RequestCleanup()
    {
        // Aggressive cleanup
        StartCoroutine(CleanupRoutine());
    }
    
    private IEnumerator CleanupRoutine()
    {
        // Unload unused assets
        var operation = Resources.UnloadUnusedAssets();
        yield return operation;
        
        // GC with minimal pause
        GC.Collect(0, GCCollectionMode.Optimized);
        yield return null;
        
        GC.Collect(1, GCCollectionMode.Optimized);
    }
}

public enum MemoryStatus { Normal, Warning, Critical }
```

### Texture Memory Control

```csharp
public class TextureMemoryController
{
    public static void SetQualityForDevice(DeviceTier tier)
    {
        switch (tier)
        {
            case DeviceTier.Low:
                QualitySettings.globalTextureMipmapLimit = 2; // 1/4 resolution
                QualitySettings.anisotropicFiltering = AnisotropicFiltering.Disable;
                break;
                
            case DeviceTier.Medium:
                QualitySettings.globalTextureMipmapLimit = 1; // 1/2 resolution
                QualitySettings.anisotropicFiltering = AnisotropicFiltering.Enable;
                break;
                
            case DeviceTier.High:
                QualitySettings.globalTextureMipmapLimit = 0; // Full resolution
                QualitySettings.anisotropicFiltering = AnisotropicFiltering.ForceEnable;
                break;
        }
    }
    
    public static void ForceReduceTextureMemory()
    {
        // Increase mipmap limit temporarily
        QualitySettings.globalTextureMipmapLimit++;
        
        // Force GPU to release memory
        Resources.UnloadUnusedAssets();
    }
}
```

## Battery Optimization

### Frame Rate Control

```csharp
public class BatteryOptimizer : MonoBehaviour
{
    [SerializeField] private int _highPerformanceFps = 60;
    [SerializeField] private int _balancedFps = 30;
    [SerializeField] private int _batterySaverFps = 24;
    
    private PerformanceMode _currentMode = PerformanceMode.Balanced;
    
    public void SetPerformanceMode(PerformanceMode mode)
    {
        _currentMode = mode;
        
        switch (mode)
        {
            case PerformanceMode.HighPerformance:
                Application.targetFrameRate = _highPerformanceFps;
                QualitySettings.vSyncCount = 0;
                break;
                
            case PerformanceMode.Balanced:
                Application.targetFrameRate = _balancedFps;
                QualitySettings.vSyncCount = 1;
                break;
                
            case PerformanceMode.BatterySaver:
                Application.targetFrameRate = _batterySaverFps;
                QualitySettings.vSyncCount = 2;
                // Additional battery saving
                Screen.brightness = 0.5f;
                break;
        }
    }
    
    public void SetAdaptiveFrameRate(bool inCombat)
    {
        // Dynamic frame rate based on gameplay
        if (inCombat)
        {
            Application.targetFrameRate = _highPerformanceFps;
        }
        else
        {
            Application.targetFrameRate = _balancedFps;
        }
    }
}

public enum PerformanceMode { HighPerformance, Balanced, BatterySaver }
```

### Background Behavior

```csharp
public class BackgroundHandler : MonoBehaviour
{
    private bool _wasInBackground;
    
    private void OnApplicationPause(bool pauseStatus)
    {
        if (pauseStatus)
        {
            // Going to background
            OnEnterBackground();
        }
        else
        {
            // Returning from background
            OnExitBackground();
        }
        
        _wasInBackground = pauseStatus;
    }
    
    private void OnEnterBackground()
    {
        // Pause audio
        AudioListener.pause = true;
        
        // Stop expensive updates
        Time.timeScale = 0;
        
        // Release non-essential resources
        Resources.UnloadUnusedAssets();
    }
    
    private void OnExitBackground()
    {
        AudioListener.pause = false;
        Time.timeScale = 1;
        
        // Check if device overheated while backgrounded
        CheckThermalState();
    }
}
```

## Thermal Management

### Thermal State Monitoring

```csharp
public class ThermalManager : MonoBehaviour
{
    public event Action<ThermalState> OnThermalStateChanged;
    
    private ThermalState _currentState = ThermalState.Normal;
    private float _checkInterval = 5f;
    
    private void Start()
    {
        InvokeRepeating(nameof(CheckThermalState), 0, _checkInterval);
    }
    
    private void CheckThermalState()
    {
#if UNITY_IOS
        var newState = GetIOSThermalState();
#elif UNITY_ANDROID
        var newState = GetAndroidThermalState();
#else
        var newState = ThermalState.Normal;
#endif
        
        if (newState != _currentState)
        {
            _currentState = newState;
            OnThermalStateChanged?.Invoke(newState);
            ApplyThermalMitigation(newState);
        }
    }
    
#if UNITY_IOS
    private ThermalState GetIOSThermalState()
    {
        // iOS provides thermal state via native plugin
        // ProcessInfo.ThermalState
        return ThermalState.Normal; // Implement native plugin
    }
#endif
    
#if UNITY_ANDROID
    private ThermalState GetAndroidThermalState()
    {
        // Android thermal API (API 29+)
        // PowerManager.getCurrentThermalStatus()
        return ThermalState.Normal; // Implement native plugin
    }
#endif
    
    private void ApplyThermalMitigation(ThermalState state)
    {
        switch (state)
        {
            case ThermalState.Normal:
                // Full performance
                Application.targetFrameRate = 60;
                QualitySettings.SetQualityLevel(2);
                break;
                
            case ThermalState.Fair:
                // Slight reduction
                Application.targetFrameRate = 45;
                break;
                
            case ThermalState.Serious:
                // Significant reduction
                Application.targetFrameRate = 30;
                QualitySettings.SetQualityLevel(1);
                break;
                
            case ThermalState.Critical:
                // Emergency mode
                Application.targetFrameRate = 24;
                QualitySettings.SetQualityLevel(0);
                ShowThermalWarning();
                break;
        }
    }
    
    private void ShowThermalWarning()
    {
        Debug.LogWarning("Device overheating - reducing performance");
        // Show UI warning to user
    }
}

public enum ThermalState { Normal, Fair, Serious, Critical }
```

## Device Tier Detection

### Hardware Classification

```csharp
public class DeviceClassifier
{
    public static DeviceTier ClassifyDevice()
    {
        int systemMemoryMB = SystemInfo.systemMemorySize;
        int processorCount = SystemInfo.processorCount;
        int graphicsMemoryMB = SystemInfo.graphicsMemorySize;
        
        // Calculate tier based on specs
        int score = 0;
        
        // Memory score
        if (systemMemoryMB >= 6000) score += 3;
        else if (systemMemoryMB >= 4000) score += 2;
        else if (systemMemoryMB >= 2000) score += 1;
        
        // CPU score
        if (processorCount >= 8) score += 3;
        else if (processorCount >= 6) score += 2;
        else if (processorCount >= 4) score += 1;
        
        // GPU score
        if (graphicsMemoryMB >= 4000) score += 3;
        else if (graphicsMemoryMB >= 2000) score += 2;
        else if (graphicsMemoryMB >= 1000) score += 1;
        
        // Classify
        if (score >= 7) return DeviceTier.High;
        if (score >= 4) return DeviceTier.Medium;
        return DeviceTier.Low;
    }
    
    public static void LogDeviceInfo()
    {
        Debug.Log($"Device: {SystemInfo.deviceModel}");
        Debug.Log($"OS: {SystemInfo.operatingSystem}");
        Debug.Log($"RAM: {SystemInfo.systemMemorySize}MB");
        Debug.Log($"CPU: {SystemInfo.processorType} x{SystemInfo.processorCount}");
        Debug.Log($"GPU: {SystemInfo.graphicsDeviceName} ({SystemInfo.graphicsMemorySize}MB)");
        Debug.Log($"Tier: {ClassifyDevice()}");
    }
}

public enum DeviceTier { Low, Medium, High }
```

### Quality Presets

```csharp
public class QualityPresetManager
{
    public static void ApplyPresetForTier(DeviceTier tier)
    {
        var preset = GetPreset(tier);
        
        // Graphics
        QualitySettings.SetQualityLevel(preset.QualityLevel);
        QualitySettings.shadows = preset.Shadows;
        QualitySettings.shadowResolution = preset.ShadowResolution;
        QualitySettings.antiAliasing = preset.AntiAliasing;
        
        // Rendering
        QualitySettings.pixelLightCount = preset.PixelLights;
        QualitySettings.globalTextureMipmapLimit = preset.TextureMipLevel;
        
        // Performance
        Application.targetFrameRate = preset.TargetFps;
        
        // Physics
        Time.fixedDeltaTime = 1f / preset.PhysicsRate;
        
        Debug.Log($"Applied quality preset for {tier}: {preset.QualityLevel}");
    }
    
    private static QualityPreset GetPreset(DeviceTier tier)
    {
        return tier switch
        {
            DeviceTier.Low => new QualityPreset
            {
                QualityLevel = 0,
                Shadows = ShadowQuality.Disable,
                ShadowResolution = ShadowResolution.Low,
                AntiAliasing = 0,
                PixelLights = 1,
                TextureMipLevel = 2,
                TargetFps = 30,
                PhysicsRate = 30
            },
            DeviceTier.Medium => new QualityPreset
            {
                QualityLevel = 2,
                Shadows = ShadowQuality.HardOnly,
                ShadowResolution = ShadowResolution.Medium,
                AntiAliasing = 2,
                PixelLights = 2,
                TextureMipLevel = 1,
                TargetFps = 45,
                PhysicsRate = 45
            },
            _ => new QualityPreset
            {
                QualityLevel = 4,
                Shadows = ShadowQuality.All,
                ShadowResolution = ShadowResolution.High,
                AntiAliasing = 4,
                PixelLights = 4,
                TextureMipLevel = 0,
                TargetFps = 60,
                PhysicsRate = 60
            }
        };
    }
    
    private struct QualityPreset
    {
        public int QualityLevel;
        public ShadowQuality Shadows;
        public ShadowResolution ShadowResolution;
        public int AntiAliasing;
        public int PixelLights;
        public int TextureMipLevel;
        public int TargetFps;
        public int PhysicsRate;
    }
}
```

## Render Pipeline Optimization

### Dynamic Resolution

```csharp
public class DynamicResolutionController : MonoBehaviour
{
    [SerializeField] private float _targetFrameTime = 16.67f; // 60 FPS
    [SerializeField] private float _minScale = 0.5f;
    [SerializeField] private float _maxScale = 1f;
    
    private float _currentScale = 1f;
    private float _smoothedFrameTime;
    
    private void Update()
    {
        // Smooth frame time
        float frameTime = Time.unscaledDeltaTime * 1000f;
        _smoothedFrameTime = Mathf.Lerp(_smoothedFrameTime, frameTime, 0.1f);
        
        // Adjust scale
        if (_smoothedFrameTime > _targetFrameTime * 1.2f)
        {
            // Too slow - reduce resolution
            _currentScale = Mathf.Max(_minScale, _currentScale - 0.05f);
        }
        else if (_smoothedFrameTime < _targetFrameTime * 0.8f)
        {
            // Room for improvement - increase resolution
            _currentScale = Mathf.Min(_maxScale, _currentScale + 0.02f);
        }
        
        ScalableBufferManager.ResizeBuffers(_currentScale, _currentScale);
    }
}
```

### LOD Bias

```csharp
public class LODController
{
    public static void SetLODForTier(DeviceTier tier)
    {
        switch (tier)
        {
            case DeviceTier.Low:
                QualitySettings.lodBias = 0.5f;
                QualitySettings.maximumLODLevel = 1;
                break;
                
            case DeviceTier.Medium:
                QualitySettings.lodBias = 1f;
                QualitySettings.maximumLODLevel = 0;
                break;
                
            case DeviceTier.High:
                QualitySettings.lodBias = 1.5f;
                QualitySettings.maximumLODLevel = 0;
                break;
        }
    }
}
```

## Best Practices

1. **Profile on actual devices** - Not just Editor
2. **Set memory budgets** per device tier
3. **Monitor thermal state** and adapt
4. **Use dynamic frame rate** based on gameplay
5. **Implement quality tiers** automatically
6. **Handle background/foreground** transitions
7. **Pool and reuse** everything
8. **Compress textures** appropriately
9. **Limit draw calls** to <100 on low-end
10. **Test on minimum spec** devices

## Troubleshooting

| Issue | Solution |
|-------|----------|
| App killed by OS | Reduce memory, handle lowMemory |
| Device overheating | Monitor thermal, reduce quality |
| Battery drain | Lower frame rate, disable features |
| Stuttering | Profile GC, use pools |
| Long load times | Stream assets, show progress |
| Crash on low-end | Test minimum spec, reduce quality |
