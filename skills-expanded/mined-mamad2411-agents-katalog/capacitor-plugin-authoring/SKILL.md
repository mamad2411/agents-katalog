---
name: capacitor-plugin-authoring
description: Use when designing or implementing custom CapacitorJS plugins including TypeScript interface definition, iOS Swift bridge, Android Kotlin bridge, and plugin registration with safety and permission controls.
---

# Capacitor Plugin Authoring

## Specialization

Design and implement custom CapacitorJS plugins that bridge native iOS Swift and Android Kotlin capabilities to a web layer through a typed TypeScript interface, with deterministic safety, permission, and error-handling patterns.

## Scope Boundaries

In scope:

- TypeScript plugin interface and implementation definition.
- iOS Swift plugin class authoring and Capacitor bridge registration.
- Android Kotlin plugin class authoring and Capacitor bridge registration.
- Permission declaration and runtime request patterns for both platforms.
- Bridge-safe data serialization and error propagation.
- Plugin packaging for local use or npm publication.

Out of scope:

- Using existing official or community plugins (see `capacitor-native-apis`).
- App-level setup and platform registration (see `capacitor-setup`).
- Plugin CI publishing pipelines beyond local validation.

## Trigger Conditions

- A native capability is needed that no official or community plugin covers.
- An existing custom plugin has bridge safety, permission, or compatibility issues.
- A plugin must wrap a proprietary native SDK.
- A plugin implementation must be reviewed for correctness against the current Capacitor bridge contract.

## Inputs

- Plugin name and capability description.
- Target platforms: iOS, Android, or both.
- Required native SDK or system API references.
- Permission requirements for each platform.
- TypeScript method signatures and data shapes expected by the web layer.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- TypeScript plugin interface and `registerPlugin` call.
- iOS Swift implementation class with Capacitor `CAPPlugin` subclass and method decorators.
- Android Kotlin implementation class with `@PluginMethod` annotations.
- Permission declarations for both `Info.plist` (iOS) and `AndroidManifest.xml` (Android).
- Error propagation pattern from native to web layer.
- Local registration instructions and smoke-test checklist.

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand the plugin contract | One method bridges native to web correctly |
| L2 Practical Plugin | Ship one safe custom plugin | TypeScript, iOS, and Android implementations exist and sync |
| L3 Hardened Plugin | Production-safe plugin | Permissions, errors, threading, and edge cases are handled |
| L4 Expert Plugin | Reusable plugin standard | Plugin is packageable, versioned, and has documented contracts |

## Deterministic Workflow

1. Define the TypeScript interface: method names, parameter types, return types, and error shapes.
2. Create the plugin directory following `@capacitor/plugin-generator` output conventions.
3. Implement `registerPlugin<MyPlugin>('MyPlugin', { web: () => new MyPluginWeb() })` in `index.ts`.
4. Author the iOS Swift class: subclass `CAPPlugin`, annotate methods with `@objc`, call `call.resolve()` or `call.reject()`.
5. Register the iOS plugin in the native project's `AppDelegate` or via auto-discovery with `+load`.
6. Author the Android Kotlin class: extend `Plugin`, annotate methods with `@PluginMethod(returnType = PluginMethod.RETURN_PROMISE)`.
7. Register the Android plugin in `MainActivity` via `registerPlugin(MyPlugin::class.java)`.
8. Declare all required permissions in `Info.plist` (iOS) and `AndroidManifest.xml` (Android).
9. Implement runtime permission requests using `checkPermissions` and `requestPermissions` bridge methods.
10. Validate bridge-safe serialization: all data crossing the bridge must be JSON-serializable primitives or `JSObject`.
11. Run `npx cap sync` and smoke-test all methods on a physical or emulated device.

## Bridge Safety Rules

- Never pass non-serializable native objects (UIImage, Bitmap, etc.) directly across the bridge; convert to base64 strings or file URIs.
- Always call `call.resolve()` or `call.reject()` exactly once per method invocation; never both.
- Never block the main thread in a plugin method; dispatch to a background thread for blocking work.
- Use `notifyListeners()` only for events that may fire multiple times; do not use it for single-call responses.
- Validate all input from `call.getString()` / `call.getObject()` before use; treat bridge input as untrusted.

## Permission Patterns

- Declare usage descriptions in `Info.plist` for every permission type used on iOS.
- Request runtime permissions before accessing restricted APIs on both platforms.
- Implement the `checkPermissions` and `requestPermissions` Capacitor standard methods when the plugin accesses protected resources.
- Return explicit permission state strings (`granted`, `denied`, `prompt`) from `checkPermissions`.

## Error Propagation Pattern

```typescript
// TypeScript
export interface MyPlugin {
  doWork(options: { input: string }): Promise<{ result: string }>;
}

// Native — always reject with a code and message
call.reject("INPUT_INVALID", "Input must not be empty", null);
// Or resolve
call.resolve(JSObject().apply { put("result", value) });
```

## Quality Gates

- All bridge methods return `Promise`; no synchronous bridge calls exist.
- No main-thread blocking in native implementations.
- All native-to-web data is JSON-serializable.
- Permissions are declared before first use and runtime requests are handled gracefully.
- `call.resolve()` and `call.reject()` are mutually exclusive in all code paths.

## Done Criteria

- TypeScript interface, iOS, and Android implementations are complete.
- All methods are smoke-tested on physical or emulated iOS and Android targets.
- Permissions are declared and runtime requests are verified.
- Error paths are tested and produce correct `reject` behavior.
- Bridge safety checklist passes without exceptions.
