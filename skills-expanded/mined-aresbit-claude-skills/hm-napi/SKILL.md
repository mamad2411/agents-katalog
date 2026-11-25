---
name: hm-napi-skill
description: >
  HarmonyOS/OpenHarmony Node-API (NAPI) domain expertise for developing native C/C++
  modules that bridge ArkTS/JS with native code. Use when: (1) Creating or modifying
  NAPI native modules in OpenHarmony projects, (2) Implementing high-performance
  native-codec/image-processing/thumbnail NAPI interfaces, (3) Designing NAPI module
  registration, async work, thread-safe callbacks, or Promise-based native APIs,
  (4) Debugging NAPI lifecycle, memory, or cross-thread issues, (5) Applying NAPI
  performance patterns (ArrayBuffer zero-copy, Sendable types, QoS scheduling),
  (6) Working with multimedia_media_library or any OHOS service-layer NAPI code.
---

# HarmonyOS Node-API (NAPI) Development

Expert knowledge for developing NAPI native modules in HarmonyOS/OpenHarmony,
synthesized from official docs and real patterns in the `multimedia_media_library` repo.

## Architecture

```
ArkTS/JS Layer
     │ import { x } from 'libmodule.so'
     ▼
ModuleManager → loads .so → calls constructor
     │
     ▼
napi_module_register(&g_module) → nm_register_func(env, exports)
     │
     ▼
Init function → napi_define_properties → returns exports
     │
     ▼
Node-API Layer (libace_napi.z.so)
  ├─ ScopeManager    — napi_value lifecycle (handle_scope)
  ├─ ReferenceManager — napi_ref lifecycle
  ├─ NativeEngine    — ArkTS engine abstraction
  └─ ArkCompiler     — ArkTS Runtime
```

Key include: `#include <napi/native_api.h>`, link: `libace_napi.z.so`

## Module Registration

### Standard (no dlopen before import)

```cpp
#include <napi/native_api.h>

static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor props[] = {
        DECLARE_NAPI_FUNCTION("myMethod", MyMethod),
    };
    napi_define_properties(env, exports, sizeof(props) / sizeof(props[0]), props);
    return exports;
}

static napi_module g_module = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,       // must be static
    .nm_modname = "mymodule",       // must match .so filename exactly, case-sensitive
    .nm_priv = nullptr,
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterMyModule(void)
{
    napi_module_register(&g_module);
}
```

**Rules:**
- `nm_register_func` must be `static` — prevents symbol conflicts across .so files
- `nm_modname` must exactly match the `.so` filename (case-sensitive)
- Constructor function name must be unique across all modules in the process
- If the .so may be `dlopen`'d before `import`, use `extern "C" void napi_onLoad()` instead of `__attribute__((constructor))`

### Multi-class module (real repo pattern)

```cpp
// native_module_ohos_medialibrary.cpp
static napi_value Export(napi_env env, napi_value exports)
{
    FileAssetNapi::Init(env, exports);
    FetchFileResultNapi::Init(env, exports);
    AlbumNapi::Init(env, exports);
    MediaLibraryNapi::Init(env, exports);
    return exports;
}
```

## Core NAPI Method Patterns

### Pattern 1: Sync Method

```cpp
static napi_value MySyncMethod(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value argv[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, argv, nullptr, nullptr);
    int32_t val;
    napi_get_value_int32(env, argv[0], &val);
    napi_value result;
    napi_create_int32(env, val * 2, &result);
    return result;
}
```

### Pattern 2: Promise + napi_async_work (standard async)

```cpp
struct AsyncContext {
    napi_async_work work = nullptr;
    napi_deferred deferred = nullptr;
    int32_t input = 0;
    std::string output;
    bool status = false;
};

static void Execute(napi_env env, void *data) {
    auto *ctx = static_cast<AsyncContext *>(data);
    ctx->output = std::to_string(ctx->input * 2); // heavy work here
    ctx->status = true;
}

static void Complete(napi_env env, napi_status status, void *data) {
    napi_handle_scope scope;
    napi_open_handle_scope(env, &scope);
    auto *ctx = static_cast<AsyncContext *>(data);
    napi_value result;
    napi_create_string_utf8(env, ctx->output.c_str(), NAPI_AUTO_LENGTH, &result);
    if (ctx->status) {
        napi_resolve_deferred(env, ctx->deferred, result);
    } else {
        napi_reject_deferred(env, ctx->deferred, result);
    }
    napi_close_handle_scope(env, scope);
    napi_delete_async_work(env, ctx->work);
    delete ctx;
}

static napi_value MyAsyncMethod(napi_env env, napi_callback_info info)
{
    auto *ctx = new AsyncContext;
    // ... parse args into ctx->input ...
    napi_value promise;
    napi_create_promise(env, &ctx->deferred, &promise);
    napi_value resource;
    napi_create_string_utf8(env, "MyAsyncWork", NAPI_AUTO_LENGTH, &resource);
    napi_create_async_work(env, nullptr, resource, Execute, Complete, ctx, &ctx->work);
    napi_queue_async_work_with_qos(env, ctx->work, napi_qos_default);
    return promise;
}
```

**QoS levels:**
- `napi_qos_background` — sync/backup, invisible to user
- `napi_qos_utility` — download, import
- `napi_qos_default` — default
- `napi_qos_user_initiated` — user-triggered, visible progress (e.g. open doc)

### Pattern 3: uv_queue_work (libuv dispatch)

Used in `medialibrary_backup_napi.cpp` for backup/restore — handles scope manually:

```cpp
uv_loop_s *loop;
napi_get_uv_event_loop(env, &loop);
uv_work_t *work = new uv_work_t;
work->data = block;

uv_queue_work_internal(loop, work,
    [](uv_work_t *work) {
        // Worker thread — do heavy computation
    },
    [](uv_work_t *work, int) {
        // JS main thread — MUST open handle_scope
        napi_handle_scope scope;
        napi_open_handle_scope(block->env, &scope);
        // ... resolve/reject promise or call JS callback ...
        napi_close_handle_scope(block->env, scope);
        delete block; delete work;
    }, "ResourceName");
```

**Key rule:** When using `uv_queue_work`, always open `napi_handle_scope` in the JS-thread callback — the NAPI framework does not manage scope for you here.

### Pattern 4: napi_threadsafe_function (cross-thread JS callback)

For calling JS callbacks from any native thread (e.g., thumbnail generation progress):

```cpp
// Create on JS main thread:
napi_value resource;
napi_create_string_utf8(env, "TSFN", NAPI_AUTO_LENGTH, &resource);
napi_threadsafe_function tsfn;
napi_create_threadsafe_function(env, jsCallback, nullptr, resource,
    0,        // max queue size (0 = unlimited)
    1,        // initial thread count
    nullptr, nullptr, nullptr, nullptr, &tsfn);

// Call from any native thread:
napi_call_threadsafe_function(tsfn, data, napi_tsfn_blocking);

// Release when done:
napi_release_threadsafe_function(tsfn, napi_tsfn_release);
```

**Constraints:** `initial_thread_count` max 128. Env and func must be from same ArkTS thread. Use `napi_call_threadsafe_function_with_priority` (API 12+) for prioritised enqueue.

### Pattern 5: Permission / Bundle Check (auth)

```cpp
static int32_t CheckPermission(void)
{
    auto context = AbilityRuntime::Context::GetApplicationContext();
    if (context == nullptr) return E_FAIL;
    std::string bundleName = context->GetBundleName();
    if (bundleName.compare(EXPECTED_BUNDLE_NAME) != 0) return E_FAIL;
    return E_OK;
}
```

## Performance Patterns

### ArrayBuffer over JSArray for bulk numeric data

| Container    | 1000 writes (us) |
|-------------|-------------------|
| JSArray     | ~1566             |
| ArrayBuffer | ~3.6              |

```cpp
// BAD: JSArray — JS interop on every element
napi_value arr;
napi_create_array(env, &arr);
for (int i = 0; i < N; i++) {
    napi_value v;
    napi_create_int32(env, i, &v);
    napi_set_element(env, arr, i, v);
}

// GOOD: ArrayBuffer — direct C++ access
void *data;
napi_value buf;
napi_create_arraybuffer(env, N * sizeof(int32_t), &data, &buf);
int32_t *p = static_cast<int32_t *>(data);
for (int i = 0; i < N; i++) p[i] = i; // zero JS overhead
```

### Minimize data copies
- Use `napi_get_arraybuffer_info` to get raw buffer — read/write directly
- Use `napi_create_external_buffer` to wrap existing C++ memory without copy
- **Never** `delete` buffer pointers from `napi_get_*_info` — engine owns them
- In hot loops, open/close `napi_handle_scope` each iteration to free temp napi_values
- Use `napi_create_external_string_utf16` (API 22+) for zero-copy string creation

## Error Handling

### Standard macro pattern (from `medialibrary_napi_utils.h`):

```cpp
#define CHECK_ARGS(env, cond, err) \
    do { if ((cond) != napi_ok) { NapiError::ThrowError(env, err, __FUNCTION__, __LINE__); return nullptr; } } while (0)

#define NAPI_ASSERT(env, cond, msg) \
    do { if (!(cond)) { NapiError::ThrowError(env, JS_ERR_PARAMETER_INVALID, __FUNCTION__, __LINE__, msg); return nullptr; } } while (0)

#define GET_JS_ARGS(env, info, argc, argv, thisVar) \
    do { void *data; napi_get_cb_info(env, info, &(argc), argv, &(thisVar), &(data)); } while (0)
```

### Error creation APIs:
- `napi_throw_error(env, code, msg)` — throw JS Error
- `napi_throw_type_error(env, code, msg)` — throw JS TypeError
- `napi_throw_range_error(env, code, msg)` — throw JS RangeError
- `napi_throw_business_error(env, code, msg)` — throw with numeric code (API 23+)

## Memory Management Rules

1. **Handle scope**: Open scope in loops creating JS objects; close each iteration
2. **Never cross env**: napi_value from env1 used with env2 → crash
3. **Buffer ownership**: `data` from `napi_get_arraybuffer_info` is engine-owned; do not free
4. **napi_wrap**: If last arg `result` is non-null, must later call `napi_remove_wrap`
5. **napi_env is thread-local**: Do not share across threads without TSFN

## Sendable Types (API 12+)

Cross-thread object passing without serialization:
- `napi_define_sendable_class` — define Sendable class
- `napi_create_sendable_array`, `napi_create_sendable_arraybuffer`
- `napi_wrap_sendable` / `napi_unwrap_sendable` / `napi_remove_wrap_sendable`
- `napi_is_sendable` — check if value is Sendable

## Key HarmonyOS NAPI Extensions

Beyond standard Node-API, HM provides:
- `napi_queue_async_work_with_qos` — QoS-based scheduling
- `napi_coerce_to_native_binding_object` — cross-thread native object binding
- `napi_create_ark_runtime` / `napi_destroy_ark_runtime` — standalone runtime
- `napi_serialize` / `napi_deserialize` — native serialization
- `napi_create_object_with_properties` — batch create from descriptors
- `napi_call_threadsafe_function_with_priority` — prioritized TSFN call
- `napi_create_external_string_utf16` / `napi_create_external_string_ascii` — zero-copy strings (API 22+)
- `napi_create_strong_reference` — strong reference (API 21+)
- `napi_wrap_enhance` — wrap with GC-aware size tracking (API 18)
- `napi_open_critical_scope` — critical scope (API 21)

Full API reference: see `references/napi_api_reference.md`

## CMakeLists.txt

```cmake
target_link_libraries(mymodule PUBLIC
    libace_napi.z.so
    libhilog_ndk.z.so      # for OH_LOG_* macros
)
```

## Repo Navigation

This repo (`multimedia_media_library`) is the reference implementation:
- `frameworks/js/` — NAPI client layer (ArkTS-facing API)
- `services/media_backup_extension/` — NAPI service layer with uv_queue_work
- `services/media_thumbnail/` — thumbnail service (high-performance native processing)
- `interfaces/kits/js/include/` — NAPI header files with macro definitions
