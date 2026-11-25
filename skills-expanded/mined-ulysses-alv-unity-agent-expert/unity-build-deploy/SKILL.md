---
name: unity-build-deploy
description: >
  Unity 6000.3 LTS build and deployment patterns. Covers build profiles,
  platform deployment, IL2CPP, BuildPlayerOptions, and distribution.
  Trigger: When building players, configuring build settings,
  or deploying to platforms in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Building players for PC, mobile, consoles, or WebGL
- Configuring build settings programmatically via `BuildPlayerOptions`
- Using Unity 6000's Build Profiles system for multi-platform pipelines
- Setting up IL2CPP scripting backend for performance or platform requirements
- Building addressable content, bundled assets, or DLC
- Deploying to app stores (Steam, Epic, App Store, Google Play)
- Configuring code stripping, symbol generation, and distribution builds
- Running automated builds via CI/CD pipelines
- Building for PS5, Xbox Series X|S, Nintendo Switch (where applicable)

## Critical Rules

### NEVER Ship Development Builds to Production

```csharp
// ❌ WRONG — Development build has debug symbols, is slow, exposes internals
var options = new BuildPlayerOptions
{
    scenes = scenePaths,
    target = BuildTarget.StandaloneWindows64,
    locationPathName = "Game.exe",
    options = BuildOptions.EnableDebugging | BuildOptions.Development
};

// ✅ CORRECT — Release build with stripping and symbols for crash reports
var options = new BuildPlayerOptions
{
    scenes = scenePaths,
    target = BuildTarget.StandaloneWindows64,
    locationPathName = "Game.exe",
    options = BuildOptions.CompressWithLz4 | BuildOptions.SymbolUpload
};
```

**Why:** Development builds include debug info, disable optimizations, and may expose sensitive APIs. Always verify `BuildOptions.Development` is NOT set for production.

### Always Validate Build Configuration Before Building

```csharp
// ✅ CORRECT — Pre-build validation
public class BuildValidator : MonoBehaviour
{
    [ContextMenu("Validate Build")]
    public void ValidateBuildConfiguration()
    {
#if UNITY_STANDALONE
        if (!PlayerSettings.stripEngineCode)
        {
            Debug.LogWarning("Engine code stripping disabled — consider enabling for smaller builds");
        }
#endif

        var scriptingBackend = PlayerSettings.GetScriptingBackend(EditorUserBuildSettings.selectedBuildTargetGroup);
        if (scriptingBackend != ScriptingImplementation.IL2CPP)
        {
            Debug.LogWarning("IL2CPP recommended for best performance and platform support");
        }
    }
}
```

### BuildPlayerOptions is a Struct — Initialize ALL Fields

```csharp
// ❌ WRONG — Partial initialization leads to random failures
var options = new BuildPlayerOptions
{
    scenes = scenePaths,
    locationPathName = "Game.exe"
};

// ✅ CORRECT — Explicit initialization prevents bugs
var options = new BuildPlayerOptions
{
    scenes = scenePaths,
    target = BuildTarget.StandaloneWindows64,
    locationPathName = "Game.exe",
    options = BuildOptions.None,
    extraScriptingDefines = Array.Empty<string>()
};
```

## Build Profiles

Unity 6000 introduces **Build Profiles** as the primary way to manage platform-specific builds. Each profile contains all settings for a specific platform configuration.

### Creating Build Profiles Programmatically

```csharp
using UnityEditor.Build;
using UnityEditor.Build.Profile;
using UnityEditor.Build.Pipeline;
using UnityEngine;

public class BuildProfileManager
{
    // Create a new build profile
    public static BuildProfile CreatePCProfile()
    {
        var profile = BuildProfile.CreateInstance<BuildProfile>();
        profile.profileName = "PC Windows";
        profile.targetPlatform = BuildTarget.StandaloneWindows64;
        profile.scriptingBackend = ScriptingImplementation.IL2CPP;
        profile.apiCompatibilityLevel = ApiCompatibilityLevel.NET_4_8;

        // Build compression
        profile.buildCompression = BuildCompression.Method.Lz4;

        // Il2Cpp compiler settings
        profile.il2CppCompilerSettings = new Il2CppCompilerInput
        {
            additionalArguments = "--parenthesized-namespaces",
            bytecodeDatabaseGeneration = BytecodeDatabaseGeneration.Generate,
            allowUnsafeCode = false
        };

        return profile;
    }

    public static BuildProfile CreateWebGLProfile()
    {
        var profile = BuildProfile.CreateInstance<BuildProfile>();
        profile.profileName = "WebGL";
        profile.targetPlatform = BuildTarget.WebGL;
        profile.scriptingBackend = ScriptingImplementation.IL2CPP;
        profile.apiCompatibilityLevel = ApiCompatibilityLevel.NET_Standard_2_1;
        profile.buildCompression = BuildCompression.Method.Lz4HC;

        return profile;
    }

    public static BuildProfile CreateAndroidProfile()
    {
        var profile = BuildProfile.CreateInstance<BuildProfile>();
        profile.profileName = "Android";
        profile.targetPlatform = BuildTarget.Android;
        profile.scriptingBackend = ScriptingImplementation.IL2CPP;
        profile.apiCompatibilityLevel = ApiCompatibilityLevel.NET_4_8;
        profile.buildCompression = BuildCompression.Method.Lz4;

        // Android-specific settings
        profile.android.targetDevices = AndroidTargetDevices.ARM64 | AndroidTargetDevices.ARMv7;
        profile.android.minimumSdkVersion = AndroidSdkVersions.AndroidApiLevel24;
        profile.android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevel34;

        return profile;
    }

    public static BuildProfile CreateiOSProfile()
    {
        var profile = BuildProfile.CreateInstance<BuildProfile>();
        profile.profileName = "iOS";
        profile.targetPlatform = BuildTarget.iOS;
        profile.scriptingBackend = ScriptingImplementation.IL2CPP;
        profile.apiCompatibilityLevel = ApiCompatibilityLevel.NET_4_8;
        profile.buildCompression = BuildCompression.Method.Lz4;

        // iOS-specific settings
        profile.iOS.supportedDestinationMask = IPHONEOS.SupportedDestination.iPhoneOnly;
        profile.iOS.deploymentTarget = 14.0f;

        return profile;
    }
}
```

### Using Build Profiles in Automation

```csharp
using UnityEditor;
using UnityEditor.Build.Profile;
using UnityEditor.Build.Pipeline;
using UnityEngine;

public class AutomatedBuildPipeline
{
    public static void BuildWithProfile(BuildProfile profile, string outputPath)
    {
        // Activate the profile
        BuildProfileContext.SetActiveProfile(profile);

        // Gather scenes
        var sceneAssets = EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();

        // Build content
        var buildContent = ContentBuilder.BuildAssemblyFromSource(
            new[] { "Assets/Scenes/MainScene.unity", "Assets/Scenes/GameplayScene.unity" }
        );

        // Execute build
        var result = BuildPipeline.BuildProject(
            EditorUserBuildSettings.activeBuildTarget,
            buildContent,
            new BuildParameters
            {
                OutputPath = outputPath,
                TargetGroup = BuildPipeline.GetBuildTargetGroup(profile.targetPlatform),
                Type = BuildType.Production
            }
        );

        if (result.status != BuildStatus.Succeeded)
        {
            throw new BuildFailedException($"Build failed: {result.summary}");
        }

        Debug.Log($"Build completed: {result.summary.outputPath}");
    }

    [MenuItem("Build/Build All Platforms")]
    public static void BuildAllPlatforms()
    {
        var profiles = new[]
        {
            BuildProfileManager.CreatePCProfile(),
            BuildProfileManager.CreateWebGLProfile(),
            BuildProfileManager.CreateAndroidProfile()
        };

        foreach (var profile in profiles)
        {
            string outputDir = $"Builds/{profile.profileName}";
            string outputPath = $"{outputDir}/{PlayerSettings.productName}";

            switch (profile.targetPlatform)
            {
                case BuildTarget.StandaloneWindows64:
                    outputPath += ".exe";
                    break;
                case BuildTarget.WebGL:
                    outputPath += ".data";
                    break;
                case BuildTarget.Android:
                    outputPath += ".apk";
                    break;
            }

            BuildWithProfile(profile, outputPath);
        }
    }
}
```

### Build Profile Context

```csharp
// Set active profile for subsequent builds
BuildProfileContext.SetActiveProfile(myProfile);

// Get currently active profile
BuildProfile activeProfile = BuildProfileContext.ActiveProfile;

// Clone and modify an existing profile
BuildProfile clonedProfile = BuildProfile.CloneProfile(sourceProfile);
clonedProfile.profileName = "Modified Clone";
```

### Legacy Build Settings vs Build Profiles

| Aspect | Legacy Build Settings | Build Profiles |
|--------|----------------------|----------------|
| Scope | Global per-target | Per-profile |
| Switch platform | Changes all settings | Just switches active profile |
| Platform variants | Manual configuration | Each profile is independent |
| CI/CD integration | Scripted via `PlayerSettings` | Profile-based with full fidelity |
| Unity 6000 recommendation | Deprecated for new features | Primary approach |

## Platform Deployment

### Standalone (Windows, macOS, Linux)

```csharp
public static void BuildStandaloneWindows()
{
    var options = new BuildPlayerOptions
    {
        scenes = GetEnabledScenePaths(),
        target = BuildTarget.StandaloneWindows64,
        locationPathName = "Builds/Windows/MyGame.exe",
        options = BuildOptions.CompressWithLz4
    };

    // IL2CPP with .NET 4.8
    PlayerSettings.SetScriptingBackend(EditorUserBuildSettings.selectedBuildTargetGroup, 
        ScriptingImplementation.IL2CPP);
    PlayerSettings.SetApiCompatibilityLevel(EditorUserBuildSettings.selectedBuildTargetGroup, 
        ApiCompatibilityLevel.NET_4_8);

    // GPU emulation for headless builds
    PlayerSettings.forceNativeGraphicsJobs = true;

    BuildPipeline.BuildPlayer(options);
}

private static string[] GetEnabledScenePaths()
{
    return EditorBuildSettings.scenes
        .Where(s => s.enabled)
        .Select(s => s.path)
        .ToArray();
}
```

### Android

```csharp
public static class AndroidBuild configuration
{
    public static void ConfigureAndroidSettings()
    {
        PlayerSettings.Android.targetDevices = AndroidTargetDevices.ARM64 | AndroidTargetDevices.ARMv7;
        PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel24;
        PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevel34;

        // Keystore for release signing
        PlayerSettings.Android.keystoreName = "user.keystore";
        PlayerSettings.Android.keystorePass = getKeystorePassword();
        PlayerSettings.Android.keyaliasName = "mykey";
        PlayerSettings.Android.keyaliasPass = getKeyPassword();

        // Splits for APK size optimization
        PlayerSettings.Android.split APKByArchitecture = true;
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64 | AndroidArchitecture.ARMv7;
    }

    public static void BuildAndroidAPK(string outputPath)
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenePaths(),
            target = BuildTarget.Android,
            locationPathName = outputPath, // e.g., "Builds/Android/mygame.apk"
            options = BuildOptions.CompressWithLz4 | BuildOptions.PatchPackage
        };

        BuildPipeline.BuildPlayer(options);
    }

    // Build Android App Bundle for Play Store
    public static void BuildAndroidAAB(string outputPath)
    {
        EditorUserBuildSettings.buildAppBundle = true;
        PlayerSettings.Android.splitSourceArchive = true;

        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenePaths(),
            target = BuildTarget.Android,
            locationPathName = outputPath, // e.g., "Builds/Android/mygame.aab"
            options = BuildOptions.CompressWithLz4
        };

        BuildPipeline.BuildPlayer(options);
    }
}
```

### iOS

```csharp
public static class iOSBuildConfiguration
{
    public static void ConfigureiOSSettings()
    {
        PlayerSettings.iOS.targetDevice = IPHONEOS.SupportedDestination.iPhoneOnly;
        PlayerSettings.iOS.deploymentTarget = 14.0f;
        PlayerSettings.SetScriptingBackend(EditorUserBuildSettings.selectedBuildTargetGroup,
            ScriptingImplementation.IL2CPP);

        // Enable bitcode for App Store submission
        PlayerSettings.iOS.enableBitcode = true;

        // Build configuration
        PlayerSettings.iOS.appleEnableManualSigningCertificate = AppleManualSigningCertificate.ManualProvisioning;
    }

    public static void BuildiOS(string outputPath)
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenePaths(),
            target = BuildTarget.iOS,
            locationPathName = outputPath, // e.g., "Builds/iOS/"
            options = BuildOptions.None
        };

        BuildPipeline.BuildPlayer(options);
    }
}
```

### WebGL

```csharp
public static class WebGLBuildConfiguration
{
    public static void ConfigureWebGLSettings()
    {
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Brotli;
        PlayerSettings.WebGL.decompressionFallback = true;
        PlayerSettings.WebGL.memorySize = 512; // MB

        // IL2CPP required for WebGL
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.WebGL,
            ScriptingImplementation.IL2CPP);

        // Template for PlayerSettings
        PlayerSettings.WebGL.playerTemplate = "my-custom-webgl-template";
    }

    public static void BuildWebGL(string outputPath)
    {
        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenePaths(),
            target = BuildTarget.WebGL,
            locationPathName = outputPath,
            options = BuildOptions.CompressWithLz4HC
        };

        BuildPipeline.BuildPlayer(options);
    }
}
```

### Xbox Series X|S / PS5

```csharp
public static class ConsoleBuildConfiguration
{
    public static void ConfigurePS5Settings()
    {
        PlayerSettings.PS5.playerSettingsMaxSpikes = 4;
        PlayerSettings.PS5.playerSettingsSpikeType = PS5PlayerSettingsSpikeType.UseAverage;
        PlayerSettings.PS5.playerSettingsSpikeThresholdTime = 1.0f;
        PlayerSettings.PS5.playerSettingsSpikeThresholdCount = 4;
    }

    public static void ConfigureXboxSettings()
    {
        PlayerSettings.XboxOne.identificationMethod = XboxOneIdentificationMethod.AutoEnforcedPlatform;
        PlayerSettings.XboxOne.splashScreenBackgroundColor = Color.black;
    }
}
```

## IL2CPP

IL2CPP (Intermediate Language To C++) converts CIL bytecode to C++ source code, then compiles with a platform-specific C++ compiler. This provides better performance, AOT compilation, and access to native features.

### IL2CPP Configuration

```csharp
public static class IL2CPPConfiguration
{
    public static void ConfigureIL2CPP(BuildTargetGroup target)
    {
        PlayerSettings.SetScriptingBackend(target, ScriptingImplementation.IL2CPP);
    }

    public static void ConfigureIL2CPPCompilerSettings()
    {
        var compilerSettings = new Il2CppCompilerInput
        {
            // Additional C++ compiler arguments
            additionalArguments = "--no-centralized-threads " +
                                 "--parenthesized-namespaces",

            // Bytecode database for faster startup
            bytecodeDatabaseGeneration = BytecodeDatabaseGeneration.Generate,

            // Allow unsafe code blocks
            allowUnsafeCode = false,

            // Symbol generation
            emitDataComments = true,
            dumpPseudocode = false,
            enableReversedCleanupMethod = false
        };

        // Note: In Unity 6000, compiler settings are typically set via BuildProfile
        // This is shown for understanding the structure
    }

    // IL2CPP method inlining configuration
    public static void ConfigureIL2CPPRuntime()
    {
        // Configure via PlayerSettings for IL2CPP specific options
        PlayerSettings.SetIl2CppCompilerConfiguration(
            EditorUserBuildSettings.selectedBuildTargetGroup,
            Il2CppCompilerConfiguration.Release
        );
    }
}
```

### IL2CPP vs Mono — When to Use IL2CPP

| Scenario | Recommended Backend |
|----------|-------------------|
| Mobile (iOS, Android) | IL2CPP (required for iOS AOT) |
| Performance-critical game | IL2CPP |
| Platform requires it (Consoles) | IL2CPP |
| Quick iteration, small project | Mono acceptable |
| WebGL | IL2CPP (required) |
| .NET features needed | IL2CPP (better .NET support) |

### Code Stripping with IL2CPP

```csharp
public static class CodeStrippingConfiguration
{
    public static void ConfigureStripping()
    {
        var target = EditorUserBuildSettings.selectedBuildTargetGroup;

        // Link.xml to preserve types used via reflection
        // Place in Assets/ folder

        // Strip engine code (significant size savings)
        PlayerSettings.stripEngineCode = true;

        // Managed stripping level
        PlayerSettings managedStrippingLevel = ManagedStrippingLevel.High;

        // For projects with heavy reflection
        PlayerSettings.managedStrippingLevel = ManagedStrippingLevel.Extreme;
    }
}
```

### Link.xml for Reflection-Heavy Code

```xml
<!-- Assets/link.xml -->
<linker>
    <!-- Preserve entire assemblies -->
    <assembly fullname="MyGame.Core" preserve="all"/>
    <assembly fullname="MyGame.Data" preserve="all"/>

    <!-- Preserve specific types -->
    <type fullname="MyGame.SaveSystem.SaveData" preserve="all"/>
    <type fullname="MyGame.ReflectionExample" preserve="all"/>

    <!-- Preserve serialization-related types -->
    <type fullname="UnityEngine.GameObject" preserve="all"/>
    <type fullname="UnityEngine.Component" preserve="all"/>

    <!-- Preserve generic types -->
    <type fullname="System.Collections.Generic.List*" preserve="all"/>
</linker>
```

### AOT Safe Code Patterns

```csharp
// ❌ UNSAFE — Reflection at runtime may fail with IL2CPP
public class UnsafeSerialization : MonoBehaviour
{
    [SerializeField] private string _typeName;

    public void Load()
    {
        var type = Type.GetType(_typeName); // May return null
        var obj = Activator.CreateInstance(type); // May fail
    }
}

// ✅ SAFE — Use link.xml or explicit type registration
public class SafeSerialization : MonoBehaviour
{
    // Pre-register types for AOT
    private static readonly Type[] _registeredTypes = new[]
    {
        typeof(MyCustomClass),
        typeof(AnotherClass)
    };

    public void Load<T>() where T : new()
    {
        var obj = new T(); // AOT-safe
    }

    // Use System.Reflection for known types
    public static Type GetRegisteredType(string name)
    {
        foreach (var type in _registeredTypes)
        {
            if (type.Name == name) return type;
        }
        return null;
    }
}
```

## Build Player Options

The `BuildPlayerOptions` struct is the primary API for programmatic builds.

### Complete BuildPlayerOptions Structure

```csharp
public class BuildPlayerOptionsExamples
{
    public static void BasicBuild()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            // Required fields
            scenes = new[] { "Assets/Scenes/MainScene.unity" },
            target = BuildTarget.StandaloneWindows64,
            locationPathName = "Builds/Windows/MyGame.exe",

            // Optional fields
            options = BuildOptions.None,

            // Unity 6000 additional fields
            extraScriptingDefines = Array.Empty<string>()
        };

        BuildPipeline.BuildPlayer(options);
    }

    public static void DevelopmentBuild()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetAllEnabledScenePaths(),
            target = BuildTarget.StandaloneWindows64,
            locationPathName = "Builds/Windows/MyGame_Dev.exe",
            options = BuildOptions.Development |
                      BuildOptions.EnableDebugging |
                      BuildOptions.AllowDebugging
        };

        BuildPipeline.BuildPlayer(options);
    }

    public static void ReleaseBuildWithSymbols()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetAllEnabledScenePaths(),
            target = BuildTarget.StandaloneWindows64,
            locationPathName = "Builds/Windows/MyGame.exe",
            options = BuildOptions.CompressWithLz4 |
                      BuildOptions.SymbolUpload
        };

        BuildPipeline.BuildPlayer(options);
    }

    public static void HeadlessServerBuild()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = GetAllEnabledScenePaths(),
            target = BuildTarget.StandaloneWindows64,
            locationPathName = "Builds/Windows/MyGame_Server.exe",
            options = BuildOptions.CompressWithLz4 |
                      BuildOptions.EnableHeadlessMode
        };

        BuildPipeline.BuildPlayer(options);
    }

    private static string[] GetAllEnabledScenePaths()
    {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }
}
```

### Build Options Reference

| Option | What it does | Use when |
|--------|--------------|----------|
| `None` | Default build | Production builds |
| `Development` | Debug symbols, logging enabled | Testing, QA |
| `EnableDebugging` | Attach debugger | Development |
| `AllowDebugging` | Allow script debugging | Development |
| `CompressWithLz4` | LZ4 compression | Release builds (faster) |
| `CompressWithLz4HC` | LZ4HC compression | Release builds (smaller) |
| `EnableHeadlessMode` | No display output | Server builds |
| `InstallInBuildFolder` | Install in build folder | Development |
| `ForceEnableOptimization` | Force optimizations on | Release builds |
| `ForceDisableOptimization` | Disable optimizations | Development only |
| `SymbolUpload` | Upload symbols for crash reports | Production |
| `PatchPackage` | Incremental patch | Updates |
| `BuildScriptsOnly` | Only compile scripts | Fast iteration |
| `AutoRunPlayer` | Run after build | Quick testing |

### BuildPlayerOptions in CI/CD

```csharp
public class CIBuildPipeline
{
    private const string BUILD_BASE_PATH = "Builds";

    public static void Main(string[] args)
    {
        string platformArg = args.Length > 0 ? args[0] : "Windows";
        string configArg = args.Length > 1 ? args[1] : "Release";

        BuildTarget target = ParseTarget(platformArg);
        BuildOptions options = ParseOptions(configArg);

        var buildPlayerOptions = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            target = target,
            locationPathName = GetOutputPath(target, configArg),
            options = options,
            extraScriptingDefines = GetDefines(configArg)
        };

        // Set scripting backend
        PlayerSettings.SetScriptingBackend(
            BuildPipeline.GetBuildTargetGroup(target),
            ScriptingImplementation.IL2CPP
        );

        var result = BuildPipeline.BuildPlayer(buildPlayerOptions);

        if (result.summary.result != UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            Console.WriteLine($"Build FAILED: {result.summary.result}");
            Environment.Exit(1);
        }

        Console.WriteLine($"Build succeeded: {result.summary.totalSize} bytes");
    }

    private static BuildTarget ParseTarget(string platform)
    {
        return platform.ToLowerInvariant() switch
        {
            "windows" or "win" or "pc" => BuildTarget.StandaloneWindows64,
            "mac" or "osx" => BuildTarget.StandaloneOSX,
            "linux" => BuildTarget.StandaloneLinux64,
            "android" => BuildTarget.Android,
            "ios" => BuildTarget.iOS,
            "webgl" => BuildTarget.WebGL,
            _ => throw new ArgumentException($"Unknown platform: {platform}")
        };
    }

    private static BuildOptions ParseOptions(string config)
    {
        return config.ToLowerInvariant() switch
        {
            "release" => BuildOptions.CompressWithLz4 | BuildOptions.SymbolUpload,
            "development" or "dev" => BuildOptions.Development |
                                     BuildOptions.EnableDebugging |
                                     BuildOptions.AllowDebugging,
            "server" => BuildOptions.CompressWithLz4 | BuildOptions.EnableHeadlessMode,
            _ => BuildOptions.CompressWithLz4
        };
    }

    private static string GetOutputPath(BuildTarget target, string config)
    {
        string extension = target switch
        {
            BuildTarget.StandaloneWindows64 => ".exe",
            BuildTarget.Android => ".apk",
            _ => ""
        };

        return $"{BUILD_BASE_PATH}/{target}/{config}/MyGame{extension}";
    }

    private static string[] GetScenePaths()
    {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }

    private static string[] GetDefines(string config)
    {
        return config.ToLowerInvariant() switch
        {
            "release" => new[] { "PRODUCTION", "FINAL_BUILD" },
            "development" => new[] { "DEVELOPMENT", "DEBUG" },
            _ => Array.Empty<string>()
        };
    }
}
```

## Distribution

### Versioning

```csharp
public static class VersionManagement
{
    public static void SetVersion(string version)
    {
        // Parse version (e.g., "1.2.3")
        var parts = version.Split('.');
        int major = int.Parse(parts[0]);
        int minor = int.Parse(parts[1]);
        int patch = int.Parse(parts[2]);

        PlayerSettings.bundleVersion = version;
        PlayerSettings.majorVersion = major;
        PlayerSettings.minorVersion = minor;
        PlayerSettings.defaultScreenWidth = Screen.width;
        PlayerSettings.defaultScreenHeight = Screen.height;
    }

    public static void SetAndroidVersionCode(int versionCode)
    {
        PlayerSettings.Android.bundleVersionCode = versionCode;
    }

    public static void SetiOSBuildNumber(int buildNumber)
    {
        PlayerSettings.iOS.buildNumber = buildNumber.ToString();
    }
}
```

### Code Signing

```csharp
public static class CodeSigning
{
    public static void ConfigureiOSSigning()
    {
        PlayerSettings.iOS.appleEnableAutomaticSigning = false;
        PlayerSettings.iOS.appleManualSigningCertificate =
            AppleManualSigningCertificate.ManualProvisioning;
        PlayerSettings.iOS.signInTeam = "XXXXXXXXXX"; // Team ID
        PlayerSettings.iOS.provisioningProfileUUID = "xxxx-xxxx-xxxx";
    }

    public static void ConfigureAndroidSigning()
    {
        PlayerSettings.Android.keystoreName = "${KEYSTORE_PATH}";
        PlayerSettings.Android.keystorePass = "${KEYSTORE_PASSWORD}";
        PlayerSettings.Android.keyaliasName = "${KEY_ALIAS}";
        PlayerSettings.Android.keyaliasPass = "${KEY_PASSWORD}";
    }

    public static void ConfigureStandaloneSigning()
    {
        // For standalone builds that need signing
        PlayerSettings.productName = "MyGame";
        PlayerSettings.companyName = "MyCompany";
    }
}
```

### Application Identifiers

```csharp
public static class AppIdentifiers
{
    public static void ConfigureAllIdentifiers()
    {
        ConfigureStandaloneIdentifier();
        ConfigureAndroidIdentifier();
        ConfigureiOSIdentifier();
        ConfigureWebGLIdentifier();
    }

    public static void ConfigureStandaloneIdentifier()
    {
        PlayerSettings.productName = "MyGame";
        PlayerSettings.companyName = "MyCompany";
        PlayerSettings.productGUID = Guid.NewGuid().ToString();
    }

    public static void ConfigureAndroidIdentifier()
    {
        PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.mycompany.mygame");
    }

    public static void ConfigureiOSIdentifier()
    {
        PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.iOS, "com.mycompany.mygame");
    }

    public static void ConfigureWebGLIdentifier()
    {
        PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.WebGL, "com.mycompany.mygame");
    }
}
```

### Distribution Builds

```csharp
public class DistributionBuilder
{
    public struct DistributionConfig
    {
        public string Platform;
        public string OutputDir;
        public BuildOptions Options;
        public bool GenerateSymbols;
        public bool CompressOutput;
    }

    public static readonly DistributionConfig[] DefaultDistributions = new[]
    {
        new DistributionConfig
        {
            Platform = "Windows",
            OutputDir = "dist/Windows",
            Options = BuildOptions.CompressWithLz4 | BuildOptions.SymbolUpload,
            GenerateSymbols = true,
            CompressOutput = true
        },
        new DistributionConfig
        {
            Platform = "Android",
            OutputDir = "dist/Android",
            Options = BuildOptions.CompressWithLz4,
            GenerateSymbols = true,
            CompressOutput = false // AAB/APK already compressed
        },
        new DistributionConfig
        {
            Platform = "iOS",
            OutputDir = "dist/iOS",
            Options = BuildOptions.None,
            GenerateSymbols = false,
            CompressOutput = false // Xcode project structure
        },
        new DistributionConfig
        {
            Platform = "WebGL",
            OutputDir = "dist/WebGL",
            Options = BuildOptions.CompressWithLz4HC,
            GenerateSymbols = false,
            CompressOutput = true
        }
    };

    public static void BuildAllDistributions()
    {
        foreach (var config in DefaultDistributions)
        {
            BuildDistribution(config);
        }
    }

    private static void BuildDistribution(DistributionConfig config)
    {
        var target = config.Platform.ToLowerInvariant() switch
        {
            "windows" => BuildTarget.StandaloneWindows64,
            "android" => BuildTarget.Android,
            "ios" => BuildTarget.iOS,
            "webgl" => BuildTarget.WebGL,
            _ => throw new ArgumentException($"Unknown platform: {config.Platform}")
        };

        var options = new BuildPlayerOptions
        {
            scenes = GetScenePaths(),
            target = target,
            locationPathName = $"{config.OutputDir}/game",
            options = config.Options,
            extraScriptingDefines = new[] { "DISTRIBUTION_BUILD" }
        };

        Directory.CreateDirectory(config.OutputDir);

        var result = BuildPipeline.BuildPlayer(options);
        if (result.summary.result != UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            throw new Exception($"Build failed for {config.Platform}: {result.summary}");
        }
    }

    private static string[] GetScenePaths()
    {
        return EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();
    }
}
```

### Steam Deployment

```csharp
public static class SteamDeployment
{
    // Steamworks API integration for builds
    public static string GetSteamBuildArgs()
    {
        // Use with BuildPipeline.BuildPlayer for Steam builds
        return "-reservedSpace 50000"; // Minimum space requirement
    }

    public static void ConfigureSteamBuild()
    {
        // Set build for Steam distribution
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Standalone,
            ScriptingImplementation.IL2CPP);

        // Ensure 64-bit
        if (PlayerSettings.targetPlatforms.Contains(BuildTarget.StandaloneWindows))
        {
            PlayerSettings.targetPlatforms.Remove(BuildTarget.StandaloneWindows);
        }
    }
}
```

### Post-Build Validation

```csharp
public static class PostBuildValidation
{
    [MenuItem("Build/Validate Last Build")]
    public static void ValidateLastBuild()
    {
        var report = BuildPipeline.GetLastBuildReport();
        if (report == null)
        {
            Debug.LogError("No build report available");
            return;
        }

        Debug.Log($"Build duration: {report.summary.totalTime}");
        Debug.Log($"Build size: {report.summary.totalSize / 1024 / 1024} MB");
        Debug.Log($"Files: {report.files.Length}");

        foreach (var file in report.files)
        {
            if (file.role == "Resource")
            {
                Debug.Log($"Resource: {file.path} ({file.size / 1024} KB)");
            }
        }

        // Validate file size
        long maxSizeMB = 50;
        if (report.summary.totalSize > maxSizeMB * 1024 * 1024)
        {
            Debug.LogWarning($"Build exceeds {maxSizeMB}MB target: {report.summary.totalSize / 1024 / 1024} MB");
        }
    }
}
```

## Common Mistakes to Prevent

### Mistake 1: Building with Development Option in Production

```csharp
// ❌ WRONG — Forgot to remove development option
options = BuildOptions.Development | BuildOptions.EnableDebugging;

// ✅ CORRECT — Explicit production options
options = BuildOptions.CompressWithLz4 | BuildOptions.SymbolUpload;
```

**Prevention:** Create a CI environment variable `BUILD_CONFIG` that controls options, or have separate build methods for `BuildType.Release` vs `BuildType.Development`.

### Mistake 2: Wrong Scripting Backend for Platform

```csharp
// ❌ WRONG — WebGL requires IL2CPP
PlayerSettings.SetScriptingBackend(BuildTargetGroup.WebGL,
    ScriptingImplementation.Mono);

// ✅ CORRECT — Always use IL2CPP for WebGL
PlayerSettings.SetScriptingBackend(BuildTargetGroup.WebGL,
    ScriptingImplementation.IL2CPP);

// ❌ WRONG — iOS requires IL2CPP for AOT
PlayerSettings.SetScriptingBackend(BuildTargetGroup.iOS,
    ScriptingImplementation.Mono);

// ✅ CORRECT — IL2CPP required for iOS
PlayerSettings.SetScriptingBackend(BuildTargetGroup.iOS,
    ScriptingImplementation.IL2CPP);
```

**Prevention:** Create a `ValidatePlatformSettings()` function that checks requirements before build.

### Mistake 3: Missing Scene in Build

```csharp
// ❌ WRONG — Hardcoded scene list, easy to forget updates
scenes = new[] { "Assets/Scenes/MainScene.unity" };

// ✅ CORRECT — Always use EditorBuildSettings
scenes = EditorBuildSettings.scenes
    .Where(s => s.enabled)
    .Select(s => s.path)
    .ToArray();
```

**Prevention:** Use `EditorBuildSettings.scenes` query shown above; never hardcode scene arrays.

### Mistake 4: Not Setting API Compatibility Level

```csharp
// ❌ WRONG — Using default which may be wrong for your dependencies
PlayerSettings.SetApiCompatibilityLevel(group, ApiCompatibilityLevel.NET_Standard_2_1);

// ✅ CORRECT — Match your dependencies' requirements
PlayerSettings.SetApiCompatibilityLevel(group, ApiCompatibilityLevel.NET_4_8);
```

**Prevention:** Document your API compatibility level and validate it in build pre-flight checks.

### Mistake 5: Forgetting to Set Bundle Identifier

```csharp
// ❌ WRONG — Leaving default identifier
PlayerSettings.SetApplicationIdentifier(group, null);

// ✅ CORRECT — Set valid identifier before build
PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.company.game");
PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.iOS, "com.company.game");
```

**Prevention:** Use `AppIdentifiers` class above to set all identifiers in one call.

### Mistake 6: Wrong Compression for Platform

| Platform | Recommended Compression |
|-----------|------------------------|
| Windows/macOS/Linux | `CompressWithLz4` (fast decompression) |
| Android | `CompressWithLz4` (APK/AAB) |
| iOS | `None` (Xcode handles it) |
| WebGL | `CompressWithLz4HC` (Brotli via PlayerSettings) |

```csharp
// ❌ WRONG — Unnecessary compression on iOS
options = BuildOptions.CompressWithLz4; // iOS should use None

// ✅ CORRECT — No compression for iOS
options = BuildOptions.None;
```

### Mistake 7: Building for Wrong Architecture

```csharp
// ❌ WRONG — Only ARM32, missing ARM64
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARMv7;

// ✅ CORRECT — Both architectures for modern devices
PlayerSettings.Android.targetArchitectures =
    AndroidArchitecture.ARM64 | AndroidArchitecture.ARMv7;
```

**Prevention:** Always set both ARM64 and ARMv7 for Android; x86_64 for Windows if needed (though x86 is deprecated).

### Mistake 8: Not Using Build Profiles for Multi-Platform

```csharp
// ❌ WRONG — Trying to share settings across platforms
PlayerSettings.productName = "MyGame"; // Same for all

// ✅ CORRECT — Use Build Profiles for platform-specific settings
var profile = BuildProfile.CreateInstance<BuildProfile>();
profile.profileName = "Android";
profile.productName = "MyGame Android";
```

### Mistake 9: Incremental Build Without Clean

```csharp
// ❌ WRONG — Incremental build with stale data
BuildPipeline.BuildPlayer(options); // May use cached data

// ✅ CORRECT — Clean when needed
if (shouldClean)
{
    BuildPipeline.BuildPlayer(options);
    // Or use:
    // BuildPipeline.BuildPlayer(options with BuildOptions.CleanBuildCache)
}

// Better approach for CI:
EditorUtility.DisplayProgressBar("Building", "Cleaning...", 0.1f);
FileUtil.DeleteFileForRetry(Application.dataPath + "/../Library/cache");
```

### Mistake 10: No Symbol Upload for Crash Reports

```csharp
// ❌ WRONG — No symbols means crashes are unreadable
options = BuildOptions.CompressWithLz4;

// ✅ CORRECT — Upload symbols for production
options = BuildOptions.CompressWithLz4 | BuildOptions.SymbolUpload;
```

**Prevention:** Always use `SymbolUpload` for production builds; symbols are required for crash dump analysis.

## Response Format

When building players or deploying platforms, provide:

1. **Target Platform** — Which platform(s) and architecture(s)
2. **Build Options** — Compression, development vs release, symbol settings
3. **Scripting Backend** — IL2CPP (recommended) or Mono
4. **Distribution Method** — Standalone installer, app store, steam
5. **Key Settings** — Bundle ID, version, signing configuration
6. **CI/CD Integration** — Command line args for automated builds

### Example Response

```
Building for: StandaloneWindows64 (Windows 64-bit)
Compression: LZ4
Scripting Backend: IL2CPP
Options: CompressWithLz4 | SymbolUpload
API Level: .NET 4.8
Output: Builds/Windows/MyGame.exe

For CI:
Unity.exe -buildTarget StandaloneWindows64 -buildOptions CompressWithLz4|SymbolUpload
```

## Unity 6000-Specific Notes

### Build Profile Best Practices

```csharp
// Always use BuildProfiles for new projects
var profile = BuildProfile.CreateInstance<BuildProfile>();

// Profile inherits from ScriptableObject
// Use CloneProfile for variants
var variant = BuildProfile.CloneProfile(baseProfile);
variant.profileName = "Release Variant";

// Serialize profiles for reuse
AssetDatabase.CreateAsset(profile, "Assets/BuildProfiles/PCProfile.asset");
AssetDatabase.CreateAsset(variant, "Assets/BuildProfiles/PCRelease.asset");
```

### Build Pipeline Compatibility

```csharp
// Unity 6000 still supports legacy BuildPlayerOptions
var legacyOptions = new BuildPlayerOptions { /* ... */ };

// But Build Profile context provides more control
using (BuildProfileContext.ActiveProfileScope(myProfile))
{
    BuildPipeline.BuildProject();
}
```

### New Build Settings Locations

| Setting | Location in Unity 6000 |
|---------|----------------------|
| Build Profiles | Edit > Build Profiles |
| Platform settings | Per-profile in Build Profiles window |
| Build Settings | Edit > Build Settings (legacy, shows active profile) |

## Quick Reference

### Build Command Line

```bash
# Basic build
Unity.exe -batchmode -projectPath "C:\MyProject" -executeMethod BuildPipeline.BuildPlayer -quit

# With specific scene
Unity.exe -batchmode -projectPath "C:\MyProject" -executeMethod "MyBuilder.BuildWindows" -quit

# Development build
Unity.exe -batchmode -projectPath "C:\MyProject" -buildOptions Development -quit
```

### Key PlayerSettings

```csharp
PlayerSettings.productName = "MyGame";
PlayerSettings.companyName = "MyCompany";
PlayerSettings.bundleVersion = "1.0.0";
PlayerSettings.stripEngineCode = true;
PlayerSettings.managedStrippingLevel = ManagedStrippingLevel.High;
```
