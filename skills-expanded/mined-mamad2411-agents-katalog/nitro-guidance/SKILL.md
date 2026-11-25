---
name: nitro-guidance
description: Definitive reference and enforcement spec for react-native-nitro-modules.
---

# react-native-nitro-modules — Definitive Reference & Enforcement Spec
# Version: 0.36.1 | Last Updated: 2026-07-17
# Status: MANDATORY READ for any code touching Nitro, MMKV V4, or custom HybridObjects

---

## 1. WHAT IS NITRO?

Nitro is a framework for building native modules that uses **JSI (JavaScript Interface)** for synchronous, zero-overhead communication between JS and native code (C++, Swift, Kotlin).

- **Core library**: `react-native-nitro-modules` — the runtime that powers all Nitro modules
- **Nitrogen**: Code generator CLI (`npx nitrogen`) that generates native bindings from TypeScript interfaces
- **Hybrid Object**: A native object exposed to JS. Can have methods, properties, and callbacks.
- **Nitro Module**: A library (like MMKV V4) that contains one or more Hybrid Objects.

**Performance benchmark** (100,000 method calls):
- ExpoModules: ~435ms
- TurboModules: ~116ms
- **NitroModules: ~7ms** 

---

## 2. VERSION HISTORY & BREAKING CHANGES

### 0.30.0 — Initial Stable
- First stable release with Nitrogen code generation
- Requires React Native >= 0.75

### 0.31.x — Stability
- Various bug fixes
- Used by MMKV 4.0.x - 4.1.x

### 0.32.x — ⚠️ KNOWN CRASH ON ANDROID
- **DO NOT USE 0.32** if you have other Nitro modules.
- Known crash: `libNitroModules.so` segfault during initialization on Android 
- MMKV's peer dep `*` would pull this in automatically — **pin your version!**

### 0.33.x — Stability
- Fixes for 0.32 crash
- Used by MMKV 4.1.x

### 0.34.x — (Internal/Skipped)
- No widely documented public changes

### 0.35.0 — 🔴 MAJOR BREAKING CHANGE FOR LIBRARY AUTHORS
Released: ~March 2026

**This is the version that introduced `JHybridObject::CxxPart` — the exact cause of your C++ compile error.**

Breaking changes for library authors:
- **Android C++ generated code structure changed** — `JHybridObject::CxxPart` introduced
- **Libraries compiled against < 0.35 will fail to build** with Nitro >= 0.35
- **iOS minimum deployment target raised to 15.1** (aligns with Expo SDK 52+, New Architecture) 
- **`nitro.json` schema changed** — new `autolinking` syntax
- **`updateNative` reference changed** in generated Kotlin code 
- **`[super invalidate]` behavior changed** — broken in RN 0.82 or below (fixed in 0.35.2)

### 0.35.1 — Hybrid Views + New Autolinking
- **NEW:** `onDropView()` for Hybrid Views
- **NEW:** `autolinking` syntax in `nitro.json` — allows mixed C++ and Swift/Kotlin per platform 
- **FIX:** Stack overflow in nitrogen (#1247)
- **FIX:** Detect duplicate nitro JS installs before install
- **DOCS:** Android `Context` guide (`NitroModules.applicationContext`)

### 0.35.2 — RN 0.82 Compatibility
- **FIX:** `[super invalidate]` broken in RN 0.82 or below 

### 0.35.3 — macOS + RuntimeError
- **NEW:** macOS support (`:osx` podspec target)
- **NEW:** `RuntimeError(...)` constructor
- **FIX:** Xcode 26.4 static linkage build 

### 0.35.4 — Variant Type Helpers
- **NEW:** `.asType<T>()` and `.isType<T>()` on Swift and Kotlin Variants 

### 0.35.5–0.35.7 — Patch releases
- Various fixes, used by downstream libraries

### 0.36.0 — Latest Major
- Latest stable baseline
- Used by MMKV 4.3.2

### 0.36.1 — Latest Stable (as of July 2026)
- Current recommended version

---

## 3. COMPATIBILITY MATRIX

| Nitro Version | MMKV Version | RN Version | iOS Min | Android Compile SDK | Notes |
|---|---|---|---|---|---|
| 0.30.x - 0.31.x | 4.0.x | 0.75 - 0.81 | 13.0 | 34 | Initial stable |
| 0.31.x - 0.33.x | 4.1.x | 0.75 - 0.81 | 13.0 | 34 | `existsMMKV`, `deleteMMKV` |
| **0.35.0+** | **4.2.0+** | **0.76 - 0.86** | **15.1** | **35+** | **CxxPart breaking change** |
| 0.35.0+ | 4.3.x | 0.76 - 0.87 | 15.1 | 35+ | `compareBeforeSet`, log level |
| **0.36.1** | **4.3.2** | **0.76 - 0.87** | **15.1** | **35+** | **Latest stable** |

---

## 4. CORE API REFERENCE

### 4.1 NitroModules (JS Entry Point)

```ts
import { NitroModules } from 'react-native-nitro-modules'

// Create a Hybrid Object by name (must be registered in native)
const obj = NitroModules.createHybridObject<SomeInterface>('ObjectName')

// Create a Nitro View (RN 0.78+ with New Architecture)
const NitroView = NitroModules.createNitroView<SomeView>('ViewName')
```

### 4.2 HybridObject Type (TypeScript Spec)

```ts
import type { HybridObject } from 'react-native-nitro-modules'

export interface Math extends HybridObject<{
  ios: 'swift'      // or 'c++'
  android: 'kotlin' // or 'c++'
}> {
  readonly pi: number
  add(a: number, b: number): number
}
```

### 4.3 Supported JS ↔ Native Types

| JS Type | C++ Type | Swift Type | Kotlin Type |
|---|---|---|---|
| `boolean` | `bool` | `Bool` | `Boolean` |
| `number` | `double` | `Double` | `Double` |
| `bigint` | `int64_t` | `Int64` | `Long` |
| `string` | `std::string` | `String` | `String` |
| `ArrayBuffer` | `std::shared_ptr<ArrayBuffer>` | `ArrayBuffer` | `ArrayBuffer` |
| `Promise<T>` | `std::shared_ptr<Promise<T>>` | `Promise<T>` | `Promise<T>` |
| `Date` | `std::chrono::system_clock::time_point` | `Date` | `java.time.Instant` |
| `AnyMap` | `std::shared_ptr<AnyMap>` | `AnyMap` | `AnyMap` |
| `Error` | `std::exception_ptr` | `Error` | `Throwable` |
| `HybridObject` | `std::shared_ptr<HybridObject>` | `HybridObject` | `HybridObject` |
| `enum` | `enum class` | `enum` | `enum` |
| `union` | `enum class` | `enum` | `enum` |
| `Record<string, T>` | `std::unordered_map` | `[String: T]` | `Map<String, T>` |
| `(T...) => void` | `std::function` | `@escaping` closure | lambda |
| `(T...) => R` | `std::function` | `@escaping` closure | lambda |
| `[A, B, C]` (tuple) | `std::tuple` | tuple | `Pair`/`Triple` |

### 4.4 Nitro View Props (RN 0.78+ New Architecture)

```ts
import type { HybridView } from 'react-native-nitro-modules'

interface VideoPlayerProps {
  url: string
  isPlaying: boolean
  onProgress: { f: (progress: number) => void }  // Callbacks MUST be wrapped in object
}

export interface VideoPlayer extends HybridView<VideoPlayerProps> {}
```

**CRITICAL:** Callbacks in Nitro Views must be wrapped in an object:
```tsx
// ✅ CORRECT
<NitroView onProgress={{ f: (p) => console.log(p) }} />

// ❌ WRONG — will fail
<NitroView onProgress={(p) => console.log(p)} />
```

---

## 5. nitro.json CONFIGURATION

### 5.1 V0.35.0+ Schema (Current)

```json
{
  "name": "MyNitroModule",
  "cxxNamespace": ["my", "module"],
  "ios": {
    "cxxNamespace": ["my", "module"],
    "iosModuleName": "MyModule"
  },
  "android": {
    "cxxNamespace": ["my", "module"],
    "androidPackageName": "com.my.module"
  },
  "autolinking": {
    "Math": {
      "ios": {
        "language": "swift",
        "implementationClassName": "HybridMath"
      },
      "android": {
        "language": "kotlin",
        "implementationClassName": "HybridMath"
      }
    }
  }
}
```

### 5.2 Pre-0.35 Schema (DEPRECATED)

Before 0.35, `autolinking` used a flat structure. The nested platform-specific syntax was introduced in 0.35.1. 

---

## 6. NATIVE IMPLEMENTATION PATTERNS

### 6.1 Swift Implementation

```swift
import Foundation
import NitroModules

class HybridMath : HybridMathSpec {
  var pi: Double {
    return Double.pi
  }
  
  func add(a: Double, b: Double) throws -> Double {
    return a + b
  }
}
```

### 6.2 Kotlin Implementation

```kotlin
package com.margelo.nitro.math
import com.margelo.nitro.core.*

class HybridMath : HybridMathSpec() {
  override fun add(a: Double, b: Double): Double {
    return a + b
  }
}
```

### 6.3 C++ Implementation (Without Nitrogen)

```cpp
#include <NitroModules/HybridObject.hpp>
using namespace margelo::nitro;

class MyHybridObject: public HybridObject {
public:
  explicit MyHybridObject(): HybridObject(TAG) {}
  
  double getNumber() { return 13; }
  void setNumber(double value) { }
  double add(double left, double right) { return left + right; }
  
  void loadHybridMethods() override {
    HybridObject::loadHybridMethods();
    registerHybrids(this, [](Prototype& prototype) {
      prototype.registerHybridGetter("number", &MyHybridObject::getNumber);
      prototype.registerHybridSetter("number", &MyHybridObject::setNumber);
      prototype.registerHybridMethod("add", &MyHybridObject::add);
    });
  }
  
private:
  static constexpr auto TAG = "MyHybrid";
};
```

### 6.4 Registration (Manual C++)

```cpp
#include <NitroModules/HybridObjectRegistry.hpp>

void load() {
  HybridObjectRegistry::registerHybridObjectConstructor(
    "MyHybrid",
    []() -> std::shared_ptr<HybridObject> {
      return std::make_shared<MyHybridObject>();
    }
  );
}
```

---

## 7. COMMON ERRORS & TROUBLESHOOTING

### `error: no member named 'CxxPart' in 'margelo::nitro::JHybridObject'`
**Cause:** Library compiled with Nitro < 0.35, but Nitro >= 0.35 is installed.
**Fix:** Upgrade the library (e.g., MMKV) to a version compatible with your Nitro version.

### `Unresolved reference 'updateNative'`
**Cause:** Library generated with Nitro < 0.35, running with Nitro >= 0.35.
**Fix:** Regenerate the library's Nitro bindings with `npx nitrogen` using Nitro >= 0.35. 

### `[Error: NitroModulesProxy.createHybridObject(...): Cannot create an instance of HybridObject "X" - It has not yet been registered]`
**Cause:** The Hybrid Object wasn't registered at app startup.
**Fix:** 
- If using Nitrogen: Ensure `nitro.json` has the object in `autolinking`
- If using Nitrogen: Ensure `$$PackageName$$OnLoad.initializeNative()` is called at startup
- If manual: Call `HybridObjectRegistry::registerHybridObjectConstructor(...)` 

### Android crash in `libNitroModules.so` at startup
**Cause:** Nitro 0.32 has a known initialization crash on Android. 
**Fix:** Upgrade to Nitro >= 0.33.

### `The following Swift pods cannot yet be integrated as static libraries`
**Cause:** Old MMKVCore without module maps.
**Fix:** Ensure MMKVCore >= 2.2.4, or add `pod 'MMKVCore', :modular_headers => true` to Podfile.

### `unknown argument: '-isystem'` (iOS build failure)
**Cause:** iOS pod header search paths using joined quoted string instead of CocoaPods array values.
**Fix:** Update to Nitro >= 0.35.5 or patch the podspec.

---

## 8. ENFORCEMENT RULES FOR AGENTS & TEAM

### ABSOLUTE PROHIBITIONS
1. **NEVER** declare `react-native-nitro-modules` as `*` or `>= 0.20.0` — always pin to a specific minor range.
2. **NEVER** mix Nitro 0.3x with libraries requiring 0.35+ in the same project.
3. **NEVER** use Nitro 0.32 — known Android crash.
4. **NEVER** write `nitro.json` with the pre-0.35 flat `autolinking` schema.

### REQUIRED PATTERNS
1. **ALWAYS** pin both MMKV and Nitro explicitly:
   ```json
   {
     "react-native-mmkv": "^4.3.2",
     "react-native-nitro-modules": "^0.36.1"
   }
   ```
2. **ALWAYS** run `npx nitrogen` after modifying `.nitro.ts` specs or `nitro.json`.
3. **ALWAYS** ensure `$$PackageName$$OnLoad.initializeNative()` is called for Nitrogen-generated modules.
4. **ALWAYS** wrap callbacks in objects for Nitro Views: `onEvent={{ f: (data) => ... }}`.

---

## 9. COMPARISON WITH OTHER NATIVE MODULE FRAMEWORKS

| Feature | Legacy Native | TurboModules | ExpoModules | Nitro |
|---|---|---|---|---|
| Bridge | JSON | JSI | JSI | JSI |
| Sync calls | ❌ | ✅ | ✅ | ✅ |
| Swift direct | ❌ | ❌ | ❌ (via Obj-C) | ✅ |
| Kotlin direct | ❌ | ❌ | ✅ | ✅ |
| Properties | ❌ | ❌ | ✅ | ✅ |
| Callbacks with return | ❌ | ❌ | ❌ | ✅ |
| Tuples | ❌ | ❌ | ❌ | ✅ |
| Unions | ❌ | ❌ | ✅ | ✅ |
| ArrayBuffer | ❌ | ❌ | ✅ | ✅ |
| Hybrid Objects | ❌ | ❌ | ✅ | ✅ |
| Codegen timing | N/A | Build-time | N/A | Package-build |
| Performance | Slow | Fast | Fast | **Fastest** |

---

## 10. QUICK REFERENCE CARD

```
IMPORT:     import { NitroModules } from 'react-native-nitro-modules'
            import type { HybridObject, HybridView } from 'react-native-nitro-modules'

CREATE:     const obj = NitroModules.createHybridObject<Interface>('Name')
CREATE VIEW: const View = NitroModules.createNitroView<ViewInterface>('ViewName')

NITROGEN:   npx nitrogen          # Regenerate bindings
            npx nitrogen init     # Bootstrap new module

MIN IOS:    15.1 (Nitro >= 0.35)
MIN RN:     0.75 (Nitro 0.30)
            0.76 (Nitro 0.35, MMKV 4.2+)
MIN NODE:   22.13.x

VIEW CALLBACKS:  onEvent={{ f: (data) => ... }}  # MUST wrap in object
```

---

## APPENDIX A: DOWNSTREAM LIBRARY VERSION TRACKING

When upgrading Nitro, verify ALL these libraries in your project are compatible:

| Library | Nitro 0.33 | Nitro 0.35 | Nitro 0.36 |
|---|---|---|---|
| react-native-mmkv | 4.1.x | 4.2.0+ | 4.3.2 |
| react-native-unistyles | Check | Check | Check |
| Any custom Nitro module | Rebuild | Regenerate + rebuild | Regenerate + rebuild |

**Rule:** When you bump Nitro, you MUST rebuild all custom Nitro modules from source (`npx nitrogen` + clean build).
