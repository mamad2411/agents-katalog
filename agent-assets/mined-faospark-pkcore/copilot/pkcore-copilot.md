# PKextended - AI Agent Instructions

## Project Overview
BepInEx 6.0 IL2CPP plugin for Suikoden I & II HD Remaster (Unity 2022.3.28f1). Uses Harmony to patch Unity engine calls for texture filtering, controller prompt swapping, and custom texture replacement.

## Architecture

### Harmony Patching Pattern
All features use Harmony prefix/postfix patches to intercept Unity setters:
```csharp
[HarmonyPatch(typeof(Image), nameof(Image.sprite), MethodType.Setter)]
[HarmonyPrefix]
public static void Image_set_sprite_Prefix(Image __instance, ref Sprite value)
```

Patches live in `Patches/` folder. Each has static `Initialize()` called from `Plugin.ApplyPatches()`.

### Configuration-Driven Features
- Each feature has dedicated `ConfigEntry<T>` in `ModConfiguration.cs`
- Features conditionally patched in `Plugin.Load()` based on config values
- Access config/logging globally via static `Plugin.Config` and `Plugin.Log`

### Game-Specific Classes
- **`GRSpriteRenderer`**: Game's custom sprite renderer (not standard Unity)
- Patches must target both standard Unity classes (`Image`, `SpriteRenderer`) and game classes

## Key Conventions

1. **Static Access Pattern**: `Plugin.Log.LogInfo()` and `Plugin.Config.FeatureName.Value` used throughout patches
2. **Caching for IL2CPP**: Dictionaries cache sprites/textures (`customSpriteCache`, `texturePathIndex`) - essential for performance in IL2CPP
3. **Modular Patching**: Each feature independently applied - check config before patching in `ApplyPatches()`
4. **Logging Levels**: `LogInfo` for user-facing actions, `LogDebug` for development details, `LogWarning` for failures

## Build & Deploy

- **Always use `dotnet build` to build the project.**
- **Auto-deploy**: Release builds output directly to game's `BepInEx\plugins\` (via registry lookup in `.csproj`)
- **Debug builds**: Go to `bin\Debug` for testing without game installation
- **Excluded folders**: `reserve/`, `build/`, `forlater/` - documentation and experimental code

## Git Commit Policy

- **ONLY THE USER decides what gets committed to GitHub.**
- AI agents do NOT commit changes without explicit user request.
- Always ask the user for approval before `git commit` and `git push`.
- Present changes for review and wait for explicit user command to commit.

## Adding New Features

1. Create patch class in `Patches/` with `[HarmonyPatch]` attributes
2. Add config entries to `ModConfiguration.cs`
3. Add static `Initialize()` method to set up state from config
4. Call `harmony.PatchAll(typeof(YourPatch))` in `Plugin.ApplyPatches()` with config check
5. Update README.md configuration section and CHANGELOG.md

## Critical Implementation Details

- **IL2CPP Limitations**: No reflection, must use direct type references
- **Sprite Suffix Convention**: Xbox=`_00`, PS4=`_01`, PS5=`_02` for controller prompts
- **Texture Replacement**: Partial coverage only - intercepts setters, not all texture loads
- **Scene-based detection**: Custom textures discovered per scene load, not globally
- **Mipmap bias**: Negative values prevent white outlines on filtered sprites

## Debugging & Development Tools

- **DNSSpy  and Unity Asset Explorer**: Required for full debugging. Use to inspect game assets, scene hierarchy, and component values at runtime
- **Game Focus**: This project targets **Suikoden I & II HD Remaster** (Unity 2022.3.28f1) exclusively. All patches, textures, and configurations must be tailored to these games
- **Dependency Repository**: [d3xMachina/Suikoden-Fix](https://github.com/d3xMachina/Suikoden-Fix) is a major source for patches. Reference this repo for game-specific implementation patterns and compatibility considerations

## Reference Files

- [Plugin.cs](Plugin.cs) - Entry point, patch orchestration
- [ModConfiguration.cs](ModConfiguration.cs) - All config definitions
- [GlobalControllerPromptPatch.cs](Patches/GlobalControllerPromptPatch.cs) - Example of global Image.sprite interception
- [reserve/UNITY_CLASSES_EXPLAINED.md](reserve/UNITY_CLASSES_EXPLAINED.md) - Unity API technical details

