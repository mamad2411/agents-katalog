---
name: mmkv-guidance
description: Definitive reference and enforcement spec for react-native-mmkv V4 and react-native-nitro-modules.
---

# react-native-mmkv V4 — Definitive Reference & Enforcement Spec
# Version: 4.3.2 | Last Updated: 2026-07-17
# Status: MANDATORY READ for any code touching MMKV

---

## 1. PHILOSOPHY & INTENT

MMKV V4 is NOT an upgrade — it's a **rewrite as a Nitro Module**.
- The JS `MMKV` class no longer exists. It's a native HybridObject.
- All native code is consumed via CocoaPods (iOS) and Gradle Prefabs (Android).
- This means: no more duplicate symbol errors when using MMKV from your own native code.
- This also means: **Chrome remote debugging is impossible**. JSI is synchronous.

---

## 2. V3 → V4 BREAKING CHANGES (MIGRATION BIBLE)

| Category | V3 (FORBIDDEN) | V4 (REQUIRED) | Severity |
|---|---|---|---|
| **Import** | `import { MMKV } from 'react-native-mmkv'` | `import { createMMKV } from 'react-native-mmkv'` | 🔴 CRITICAL |
| **Instantiation** | `new MMKV()` | `createMMKV()` | 🔴 CRITICAL |
| **Instantiation** | `new MMKV({ id: 'x' })` | `createMMKV({ id: 'x' })` | 🔴 CRITICAL |
| **Delete key** | `storage.delete('key')` | `storage.remove('key')` | 🔴 CRITICAL |
| **Recrypt** | `storage.recrypt('key')` | Constructor-only: `createMMKV({ encryptionKey: 'key' })` | 🔴 CRITICAL |
| **Listener removal** | `listener.remove()` (returns void) | `listener.remove()` (still works, but verify return) | 🟡 CHECK |
| **App Group (iOS)** | `AppGroup` key in Info.plist | `AppGroupIdentifier` key in Info.plist | 🔴 CRITICAL |
| **Native MMKV import** | `#import <MMKV/MMKV.h>` (manual) | Automatic via CocoaPods/Gradle Prefabs | 🟡 AWARENESS |
| **Debugging** | Chrome DevTools | Flipper / React DevTools / Rozenite | 🟡 AWARENESS |
| **Testing mock** | Manual `jest.mock('react-native-mmkv', ...)` | Auto-mocked in Jest/Vitest | 🟡 CLEANUP |

---

## 3. V4 VERSION-BY-VERSION CHANGELOG

### 4.0.0 (2025-10-20) — THE BIG BANG
- Full rewrite to Nitro Module
- `new MMKV()` → `createMMKV()`
- `.delete()` → `.remove()`
- `AppGroup` → `AppGroupIdentifier`
- `set()` now **throws** if value couldn't be saved (previously silent fail)
- `remove()` and `clearAll()` now properly invoke value change listeners
- `set()` now **throws** if key is empty
- Adds `useMMKVKeys()` hook
- Works on old architecture again (RN 0.75+)
- MMKVCore consumed from CocoaPods/Gradle (no bundled source)
- Requires `react-native-nitro-modules >= 0.30.0`

### 4.0.1 (2025-11-18)
- Adds `MMKV.id` property on instances
- Fixes incorrect return of `remove` on Web
- Upgrades to Nitro 0.31.7
- Docs: Replaces Flipper with Rozenite for debugging

### 4.1.0 (2025-12-04)
- **NEW:** `existsMMKV(id)` — check if instance exists
- **NEW:** `deleteMMKV(id)` — delete an instance entirely
- **NEW:** `importAllFrom(otherStorage)` — migrate all keys/values
- Fixes duplicate `libNitroModules.so` libs on Android
- Removes z and c++ libraries from podspec

### 4.1.1 (2025-12-??)
- Minor fixes

### 4.1.2 (2026-01-28)
- Fix duplicate `libNitroModules.so` libs (Android)

### 4.2.0 (2026-03-04) — NITRO 0.35 BREAKING POINT
- **‼️ REQUIRES `react-native-nitro-modules >= 0.35.0`**
- This is where `JHybridObject::CxxPart` was introduced
- If your Nitro is < 0.35, MMKV 4.2.0+ will C++ compile-fail

### 4.3.0 (2026-03-20)
- **NEW:** `compareBeforeSet` option — skips disk write if value unchanged
- Upgrades MMKV Core to 2.4.0 on Android and iOS
- Makes default MMKV log level configurable at build time
- Android: `MMKV_logLevel` in `gradle.properties`
- iOS: `$MMKVLogLevel` in `Podfile`

### 4.3.1 (2026-04-07)
- Fix `set(ArrayBuffer)` on Web

### 4.3.2 (2026-06-22) — LATEST STABLE
- **NEW:** `checkContentChanged()` — detect external storage modifications
- **NEW:** `recoveryStrategy` config option
- **NEW:** Support for Harness web testing
- **NEW:** Reactively listen to `checkContentChanged()` in hooks
- Bumps MMKV Core fork for RN 0.87 support
- Performance: Reports MMKV external memory size
- Fix `length` being incorrect in MMKV Web
- Docs fix: README object example comment and deprecated `size` usage

---

## 4. NITRO MODULES COMPATIBILITY MATRIX

| MMKV Version | Minimum Nitro | Recommended Nitro | RN Support | Notes |
|---|---|---|---|---|
| 4.0.x | 0.30.0 | 0.31.7 | 0.75 - 0.81 | Initial Nitro rewrite |
| 4.1.x | 0.31.x | 0.33.x | 0.75 - 0.81 | `existsMMKV`, `deleteMMKV` |
| 4.2.0+ | **0.35.0** | 0.36.1 | 0.76 - 0.86 | **Breaking Nitro API change** |
| 4.3.0+ | 0.35.0 | 0.36.1 | 0.76 - 0.87 | `compareBeforeSet`, log level config |
| 4.3.2 | 0.35.0 | **0.36.1** | 0.76 - 0.87 | Latest stable |

**CRITICAL RULE:** `react-native-nitro-modules` uses `*` as peer dep in some MMKV versions. Package managers may install incompatible versions. **Always pin both explicitly.**

---

## 5. COMPLETE V4 API REFERENCE

### 5.1 Factory Function
```ts
import { createMMKV } from 'react-native-mmkv'

const storage = createMMKV(options?: MMKVConfiguration)
```

### 5.2 Configuration Options
```ts
interface MMKVConfiguration {
  id?: string;                    // Required if path or encryptionKey used. Default: 'mmkv.default'
  path?: string;                  // ⚠️ CUSTOM PATH BUG — SEE GOTCHAS
  encryptionKey?: string;         // Encryption key
  encryptionType?: 'AES-128' | 'AES-256';  // Default: 'AES-128'
  mode?: 'single-process' | 'multi-process'; // Default: 'single-process'
  readOnly?: boolean;             // Default: false. Throws on set() if true.
  compareBeforeSet?: boolean;     // Default: false. Skip write if value unchanged (4.3.0+)
  recoveryStrategy?: ...;         // (4.3.2+)
}
```

### 5.3 Instance Methods
```ts
// Core CRUD
storage.set(key: string, value: string | number | boolean | ArrayBuffer): boolean
storage.getString(key: string): string | null
storage.getNumber(key: string): number | null
storage.getBoolean(key: string): boolean | null
storage.getBuffer(key: string): ArrayBuffer | null

// Key management
storage.remove(key: string): boolean        // ⚠️ Was .delete() in V3
storage.contains(key: string): boolean
storage.getAllKeys(): string[]
storage.clearAll(): void

// Instance metadata
storage.id: string                          // (4.0.1+)
storage.byteSize: number                    // Size in bytes

// Maintenance
storage.trim(): void                        // Clean unused keys + clear memory cache
storage.importAllFrom(otherStorage): number // Returns count of imported keys (4.1.0+)
storage.checkContentChanged(): boolean      // (4.3.2+)

// Listeners
storage.addOnValueChangedListener((changedKey: string) => void): { remove: () => void }
// ⚠️ V3's .removeOnValueChangedListener() is gone. Use the returned object's .remove()
```

### 5.4 Static Utilities
```ts
import { existsMMKV, deleteMMKV } from 'react-native-mmkv'

existsMMKV(id: string): boolean        // (4.1.0+)
deleteMMKV(id: string): boolean        // (4.1.0+)
```

### 5.5 React Hooks
```ts
import {
  useMMKVString,
  useMMKVNumber,
  useMMKVBoolean,
  useMMKVBuffer,
  useMMKVKeys,        // (4.0.0+)
} from 'react-native-mmkv'

// Signature: (key: string, instance?: MMKVInstance) => [value, setValue]
const [name, setName] = useMMKVString('user.name', storage)
const [age, setAge] = useMMKVNumber('user.age', storage)
const [active, setActive] = useMMKVBoolean('user.active', storage)
const [token, setToken] = useMMKVBuffer('auth.token', storage)

// useMMKVKeys: Returns all keys as reactive state
const keys = useMMKVKeys(storage)  // string[]
```

### 5.6 Buffer API
```ts
const buffer = new ArrayBuffer(3)
const writer = new Uint8Array(buffer)
writer[0] = 1
writer[1] = 100
writer[2] = 255

storage.set('token', buffer)
const retrieved = storage.getBuffer('token')  // ArrayBuffer
```

---

## 6. LIMITATIONS & GOTCHAS (READ BEFORE USING)

### 6.1 🔴 CUSTOM PATH BUG (#911)
**DO NOT USE `path` UNLESS ABSOLUTELY NECESSARY.**
```ts
// ❌ BROKEN — Data will NOT persist
createMMKV({ id: 'x', path: 'app/data' })

// ✅ SAFE — Use default paths
createMMKV({ id: 'x' })
```
Custom paths fail silently on some platforms. Data appears to write but disappears on app restart. This is a confirmed bug in V4.

### 6.2 🔴 NO CHROME REMOTE DEBUGGING
MMKV V4 uses JSI synchronously. Chrome DevTools (which runs JS in a separate V8 instance) cannot access JSI.
- **Use:** Flipper, React DevTools, Rozenite (`@rozenite/mmkv-plugin`)
- **Error you'll see:** `Failed to create a new MMKV instance: React Native is not running on-device`

### 6.3 🔴 NO `recrypt()` AT RUNTIME
V3 allowed `storage.recrypt('new-key')` to change encryption on the fly.
V4 requires encryption key at construction time only. Plan migration accordingly.

### 6.4 🟡 `remove()` vs `delete()`
- V3: `storage.delete('key')`
- V4: `storage.remove('key')`
`delete` is a C++ reserved keyword. The method was renamed. Old code will get `TypeError: storage.delete is not a function`.

### 6.5 🟡 `set()` THROWS ON FAILURE
V3: `set()` returned `false` or silently failed.
V4: `set()` throws a proper Error if the value couldn't be saved. Wrap in try/catch if you need graceful handling.

### 6.6 🟡 `set()` THROWS ON EMPTY KEY
V4 throws if you call `set('', 'value')`. V3 may have allowed this.

### 6.7 🟡 LISTENERS NOW FIRE ON `remove()` AND `clearAll()`
V3 did NOT fire value change listeners when keys were removed.
V4 DOES fire listeners. If your code assumes listeners only fire on `set()`, you may have bugs.

### 6.8 🟡 INSTANCE ID PROPERTY
```ts
const storage = createMMKV({ id: 'my-store' })
console.log(storage.id)  // 'my-store' (added in 4.0.1)
```

### 6.9 🟡 WEB FALLBACK
If LocalStorage is disabled in the browser, MMKV Web falls back to in-memory storage. Data will NOT persist across refreshes.

### 6.10 🟡 MINIMUM RN VERSION
V4 requires React Native **0.76 or higher**. (Nitro itself requires 0.75+)

---

## 7. TESTING & MOCKING

### 7.1 Auto-Mock (Jest/Vitest)
MMKV V4 is **automatically mocked** in test environments. You do NOT need a manual mock.
```ts
// ✅ This works in tests without any setup
import { createMMKV } from 'react-native-mmkv'
const storage = createMMKV()
storage.set('key', 'value')
```

### 7.2 If You Need a Custom Mock
```ts
jest.mock('react-native-mmkv', () => {
  const actual = jest.requireActual('react-native-mmkv')
  return {
    ...actual,
    createMMKV: jest.fn((opts = {}) => {
      const store = new Map()
      return {
        id: opts.id ?? 'mmkv.default',
        set: jest.fn((k, v) => store.set(k, v)),
        getString: jest.fn((k) => store.get(k) ?? null),
        getNumber: jest.fn((k) => store.get(k) ?? null),
        getBoolean: jest.fn((k) => store.get(k) ?? false),
        getBuffer: jest.fn((k) => store.get(k) ?? null),
        contains: jest.fn((k) => store.has(k)),
        remove: jest.fn((k) => store.delete(k)),
        getAllKeys: jest.fn(() => Array.from(store.keys())),
        clearAll: jest.fn(() => store.clear()),
        addOnValueChangedListener: jest.fn(() => ({ remove: jest.fn() })),
        trim: jest.fn(),
        byteSize: 0,
        checkContentChanged: jest.fn(() => false),
        importAllFrom: jest.fn(() => 0),
      }
    }),
    existsMMKV: jest.fn(() => true),
    deleteMMKV: jest.fn(() => true),
    useMMKVString: jest.fn(),
    useMMKVNumber: jest.fn(),
    useMMKVBoolean: jest.fn(),
    useMMKVBuffer: jest.fn(),
    useMMKVKeys: jest.fn(() => []),
  }
})
```

### 7.3 Web Shim for Testing/Bundling
If you have a web shim (`mmkv-web.js`), it MUST export `createMMKV` as a factory function, NOT a class:
```js
// ✅ CORRECT WEB SHIM
export function createMMKV(options = {}) {
  // ... return object matching V4 API
}
export function useMMKVString(key, instance) { /* ... */ }
// etc
```

---

## 8. ENFORCEMENT RULES FOR AGENTS & TEAM

### ABSOLUTE PROHIBITIONS
1. **NEVER** use `new MMKV()` — it does not exist in V4.
2. **NEVER** import `{ MMKV }` from `'react-native-mmkv'` — export is `createMMKV`.
3. **NEVER** use `storage.delete('key')` — use `storage.remove('key')`.
4. **NEVER** use `storage.recrypt('key')` — encryption is constructor-only.
5. **NEVER** use custom `path` in `createMMKV()` without explicit approval and testing.
6. **NEVER** rely on Chrome DevTools for MMKV debugging.
7. **NEVER** write manual Jest mocks unless auto-mock fails.

### REQUIRED PATTERNS
1. **ALWAYS** import: `import { createMMKV } from 'react-native-mmkv'`
2. **ALWAYS** instantiate: `const storage = createMMKV({ id: '...' })`
3. **ALWAYS** pin both packages in package.json:
   ```json
   {
     "react-native-mmkv": "^4.3.2",
     "react-native-nitro-modules": "^0.36.1"
   }
   ```
4. **ALWAYS** handle `set()` throws in critical paths:
   ```ts
   try {
     storage.set('critical-key', data)
   } catch (e) {
     // Handle persistence failure
   }
   ```
5. **ALWAYS** use `storage.remove()` not `.delete()`.

### CODE REVIEW CHECKLIST
- [ ] No `new MMKV()` in diff
- [ ] No `import { MMKV } from 'react-native-mmkv'` in diff
- [ ] No `.delete(` calls on MMKV instances in diff
- [ ] No `.recrypt(` calls in diff
- [ ] No custom `path:` in `createMMKV()` in diff
- [ ] `react-native-nitro-modules` is in `dependencies`, not `devDependencies`
- [ ] Version specs match the compatibility matrix

---

## 9. TROUBLESHOOTING COMMON ERRORS

### `error: no member named 'CxxPart' in 'margelo::nitro::JHybridObject'`
**Cause:** `react-native-nitro-modules` version is too old for your MMKV version.
**Fix:** Upgrade Nitro to match the compatibility matrix (e.g., 0.36.1 for MMKV 4.3.2).

### `TypeError: storage.delete is not a function`
**Cause:** V3 code calling `.delete()` on V4 instance.
**Fix:** Replace with `.remove()`.

### `Error: Failed to create a new MMKV instance: React Native is not running on-device`
**Cause:** Using Chrome Remote Debugger.
**Fix:** Use Flipper, React DevTools, or on-device debugging.

### `Error: Exception in HostFunction: Failed to create MMKV instance!`
**Cause:** Custom `path` is invalid or inaccessible.
**Fix:** Remove `path` option and use default paths.

### `The following Swift pods cannot yet be integrated as static libraries`
**Cause:** Old MMKVCore version without module maps.
**Fix:** Ensure MMKVCore >= 2.2.4, or add `pod 'MMKVCore', :modular_headers => true` to Podfile.

### `react-native-nitro-modules 0.32 as peer dep may be causing crashes on Android`
**Cause:** Peer dependency `*` allowed incompatible Nitro version.
**Fix:** Pin `react-native-nitro-modules` explicitly in your package.json.

---

## 10. MIGRATION CHECKLIST (V3 → V4)

- [ ] Install `react-native-nitro-modules` if not already present
- [ ] Update `react-native-mmkv` to `^4.3.2`
- [ ] Update `react-native-nitro-modules` to `^0.36.1`
- [ ] Replace all `import { MMKV }` with `import { createMMKV }`
- [ ] Replace all `new MMKV(...)` with `createMMKV(...)`
- [ ] Replace all `storage.delete(...)` with `storage.remove(...)`
- [ ] Remove all `storage.recrypt(...)` calls — move encryption to constructor
- [ ] Update iOS `Info.plist`: `AppGroup` → `AppGroupIdentifier` (if using App Groups)
- [ ] Update web shim to export `createMMKV` factory function
- [ ] Remove or simplify manual Jest mocks
- [ ] Verify no custom `path` usages
- [ ] Run `npx tsc --noEmit`
- [ ] Run `eas build --platform android --local` (or full CI build)
- [ ] Test on real device (not just simulator)

---

## 11. QUICK REFERENCE CARD

```
IMPORT:     import { createMMKV } from 'react-native-mmkv'
CREATE:     const storage = createMMKV({ id: 'my-store' })
READ:       storage.getString('key') | .getNumber('key') | .getBoolean('key') | .getBuffer('key')
WRITE:      storage.set('key', value)     ← THROWS on failure
DELETE:     storage.remove('key')          ← NOT .delete()
CLEAR:      storage.clearAll()
CHECK:      storage.contains('key')
KEYS:       storage.getAllKeys()
SIZE:       storage.byteSize
TRIM:       storage.trim()
LISTEN:     storage.addOnValueChangedListener(cb)
IMPORT:     storage.importAllFrom(otherStorage)
CHECK EXT:  storage.checkContentChanged()  ← 4.3.2+
EXISTS:     existsMMKV('id')               ← static, 4.1.0+
DELETE INST: deleteMMKV('id')              ← static, 4.1.0+

HOOKS:      useMMKVString(key, storage?)
            useMMKVNumber(key, storage?)
            useMMKVBoolean(key, storage?)
            useMMKVBuffer(key, storage?)
            useMMKVKeys(storage?)
```
