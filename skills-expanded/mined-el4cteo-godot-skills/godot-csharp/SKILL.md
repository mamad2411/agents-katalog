---
name: godot-csharp
description: Godot 4.7 C#/.NET done right - csproj/SDK setup, partial classes and source generators, [Export]/[Signal]/[GlobalClass]/[Tool], C# signals and events that must be disconnected (ObjectDisposedException), StringName caching, Variant/collections marshaling, async ToSignal, GDScript interop, culture bugs, no web export, dotnet build errors as JSON. Use for any .cs file.
license: MIT
compatibility: Godot 4.7+ .NET build, .NET SDK 8+ (10 works). Python 3.9+ for scripts.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# C# / .NET in Godot 4.7

**Build after every edit:** `python scripts/cs_build.py` returns errors as `{file, line, code, msg}`. Use `--doctor` to check the setup and `--init` to create the csproj and sln exactly like the 4.7 editor does.
The engine runs the **last built** assembly in `.godot/mono/temp/bin/`, so build before any smoke run.
C# names: `api_lookup.py Node3D.look_at` prints `Node3D.LookAt(Vector3, Vector3?, bool)`. C# names also work as queries.

## Project setup (verified 4.7.2 template)
```xml
<Project Sdk="Godot.NET.Sdk/4.7.2">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <TargetFramework Condition=" '$(GodotTargetPlatform)' == 'android' ">net9.0</TargetFramework>
    <EnableDynamicLoading>true</EnableDynamicLoading>
  </PropertyGroup>
</Project>
```
- The `Godot.NET.Sdk/x.y.z` version **must equal the engine version**. Bump it when you upgrade Godot. net8.0 is the minimum; net9.0+ is allowed. `<Nullable>enable</Nullable>` is recommended.
- `project.godot` needs `"C#"` in `config/features` and `[dotnet] project/assembly_name`. The assembly name must match the csproj name.
- NuGet packages work normally (`dotnet add package`). Assemblies must be pure managed code, or ship native libraries for every target platform.
- **Not supported:** web export of C# projects (still true in 4.7; use GDScript for web builds). Android needs net9.0 (the template handles it). iOS works. Desktop works everywhere.

## Script rules (the source generators depend on them)
- `public partial class Player : CharacterBody3D`. The file name must equal the class name (`Player.cs`). Namespaces are fine. Godot-derived classes must be `partial`.
- `[GlobalClass]` registers the class in the Create dialog and as an exportable Resource type, like GDScript `class_name`. `[Tool]` runs the class in the editor.
- Exports: `[Export] public float Speed { get; set; } = 5f;` plus `[ExportGroup("Movement")]`, `[ExportSubgroup]`, `[ExportCategory]`, `[Export(PropertyHint.Range, "0,100,1")]` and `[ExportToolButton("Bake")] public Callable BakeButton => Callable.From(Bake);`.
- Signals: `[Signal] public delegate void HitEventHandler(int damage);`. The suffix is required. The generator creates event `Hit` and `SignalName.Hit`.
  Emit with `EmitSignal(SignalName.Hit, 5)` and connect with `enemy.Hit += OnHit;`.
- Use `SignalName.*`, `MethodName.*` and `PropertyName.*` (generated `StringName`s) wherever the API wants a name, so you never allocate strings.
- Structs are copied: `Position.X = 5` won't compile (CS1612). Write `Position = Position with { X = 5 };`.

## Signal lifetime (official rules)
Godot disconnects everything when either object is freed, **except**:
1. `+=` to a **custom** `[Signal]`, when the receiver is freed first, and
2. lambdas that **capture** variables. Godot can't tie them to an instance, and `Callable.From` doesn't help.
In both cases, unsubscribe with `-=` in `_ExitTree` (keep the delegate in a field for lambdas). Otherwise, emitting into a freed object throws `ObjectDisposedException`.

## Performance and correctness
- Cache input actions, groups and other names as `static readonly StringName`. Passing `"jump"` every frame allocates.
- Use `System.Collections.Generic` for internal logic. Use `Godot.Collections.Array<T>`/`Dictionary<TK,TV>` only at the Godot boundary (exports, signals, GDScript calls). Each crossing marshals the data.
- Packed arrays (`Vector3[]`, `byte[]`) are **copied** on every API call. Read a mesh array once and work on the copy.
- Avoid LINQ and closures in `_Process`/`_PhysicsProcess` hot loops. Prefer `GetNode<T>()` once in `_Ready` and keep the result in a field.
- **Culture bug:** `$"{1.5f}"`, `float.Parse` and `ToString()` follow the OS locale (`1,5` in Italian, German, …). Use `CultureInfo.InvariantCulture` for saves, network data, JSON and UI number formats. (Observed on a 4.7.2 test machine.)
- Exceptions in callbacks are logged, not fatal. Watch the Output/Debugger panel, or `run_godot.py smoke` errors.
- `GD.Print` allocates. Remove it from hot paths, or put it behind `#if DEBUG` or `OS.IsDebugBuild()`.

## Async
- `await ToSignal(GetTree().CreateTimer(1.0), SceneTreeTimer.SignalName.Timeout);` awaits a signal on the main thread.
- Run CPU work on `Task.Run`/`WorkerThreadPool`, then get back to the main thread with `CallDeferred` or `Callable.From(...).CallDeferred()` before you touch nodes.
- Await anything inside `_Ready`/`_Process` only through an `async void` handler, and keep it short. Check `IsInstanceValid(this)` after awaits.

## GDScript ↔ C#
- From C#: `var gd = GetNode("Inventory"); gd.Call("add_item", "sword", 2); var n = gd.Get("count").AsInt32();`. Connect to its signals with `gd.Connect("changed", Callable.From<int>(OnChanged))`.
- From GDScript: C# public members appear with their **C# names** (`node.Speed`, `node.Damage(5)`). Signals keep their C# names (`node.Hit.connect(...)`).
- Create GDScript objects from C#: `GD.Load<GDScript>("res://x.gd").New().AsGodotObject()`.
- `Variant`: `Variant.From(x)`, `v.As<T>()`, `v.AsInt32()`, `v.VariantType`. Return `Variant` from methods GDScript calls dynamically.

Patterns, interop and editor/hot-reload notes (compiled by the tests): [references/patterns.md](references/patterns.md).
