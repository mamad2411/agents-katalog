---
name: spclib
description: |
  This skill should be used when the user asks to "write C code with sp.h", "use spclib", "sp.h API", "single-header C library",
  "modern C programming", "sp_str_t usage", "sp_alloc memory", "sp_log formatting", "dynamic array in C", "hash table in C",
  "cross-platform C code", or when working with the sp.h single-header C standard library replacement.
license: MIT
---

# spclib - sp.h Programming Guide

sp.h is a single-header C standard library replacement providing modern, type-safe APIs for memory management, strings, containers, IO, and cross-platform system operations.

## Core Principles

**Always follow these rules when using sp.h:**

| Never Use | Use Instead |
|-----------|-------------|
| `malloc`/`calloc`/`realloc` | `sp_alloc(mem, size)` |
| `const char*` | `sp_str_t` (ptr+len string) |
| `strcmp`/`strlen` | `sp_str_equal()` / `sp_str_empty()` |
| `printf` | `sp_log()` / `sp_print()` |
| `memset(&obj, 0, sizeof(obj))` | `sp_mem_zero(&obj, sizeof(obj))` |
| `for(i=0; i<n; i++)` on C arrays | `sp_carr_for()` / `sp_da_for()` |

## Quick Reference

### Setup
```c
// In ONE C file only:
#define SP_IMPLEMENTATION
#include "sp.h"
```

### Types
- `s8/s16/s32/s64` - signed integers
- `u8/u16/u32/u64` - unsigned integers
- `f32/f64` - floats
- `c8` - char (UTF-8)
- `sp_str_t` - {const c8* data, u32 len} string (no null terminator required)

### Memory Allocator
```c
sp_mem_t mem = sp_mem_os_new();         // OS-backed allocator
void* ptr = sp_alloc(mem, 1024);        // Allocate 1024 bytes
sp_free(mem, ptr);                      // Free allocation

// Scratch arena (temporary allocations):
sp_mem_arena_marker_t mark = sp_mem_begin_scratch();
sp_str_t msg = sp_fmt(sp_mem_get_scratch(), "hello {}", sp_fmt_str(name)).value;
sp_mem_end_scratch(mark);               // All scratch memory freed
```

### Zero Initialization
```c
my_struct_t obj = sp_zero;              // {0} — use for local variables
my_struct_t* p = sp_alloc(mem, sizeof(my_struct_t));
sp_mem_zero(p, sizeof(my_struct_t));    // Zero heap-allocated memory
// sp_zero_s(T) gives (T){0} for passing to functions
```

### String Operations
```c
sp_str_t s = sp_str_lit("hello");       // Compile-time literal (no alloc)
sp_str_t v = sp_str_view(cstr);         // Zero-allocation view from C string
bool eq = sp_str_equal(a, b);           // Compare
bool empty = sp_str_empty(s);           // Check empty
sp_str_t copy = sp_str_copy(mem, s);    // Allocated copy
```

### Formatting & Logging
```c
// Type-safe format strings use {} placeholders — args MUST be wrapped in sp_fmt_* macros:
sp_log("Value = {}", sp_fmt_int(x));                    // log to stdout (appends newline)
sp_print("Hello {}", sp_fmt_str(name));                 // print to stdout (no newline)
sp_str_t s = sp_fmt(mem, "x={}, y={}", sp_fmt_int(x), sp_fmt_int(y)).value;  // format to string
sp_fatal("unrecoverable: {}", sp_fmt_int(err_code));    // log + abort

// Argument wrappers: sp_fmt_int / sp_fmt_uint / sp_fmt_float / sp_fmt_str / sp_fmt_cstr / sp_fmt_char / sp_fmt_ptr
// Style directives inside {}: {.red} {.cyan} {.bold} {.italic} — plus sp_fmt_red() etc. as args
// Spec grammar: [fill/align] [width] [.precision] [renderer]  e.g. {:>10} {:.3} {:x} {.cyan}
// sp_fmt() returns sp_str_r (a Result) — access the string via .value
```

### Dynamic Arrays
```c
sp_da(int) arr = SP_NULLPTR;            // Type is sp_da(T), NOT sp_dyn_array(T)
sp_da_push(arr, 42);                    // Append element
sp_da_push(arr, 99);
sp_da_for(arr, i) {                     // Iterate
  sp_log("arr[{}] = {}", sp_fmt_uint(i), sp_fmt_int(arr[i]));
}
u64 n = sp_da_size(arr);
sp_da_free(arr);                        // Free the entire array
```

### Directory Iteration
```c
// Note: mem is the first parameter
sp_fs_for(mem, dir, it) {
  sp_log("Entry: {}", sp_fmt_str(it.entry.name));
}

// Recursive directory traversal
sp_fs_for_recursive(mem, dir, it) {
  sp_log("Path: {}", sp_fmt_str(it.entry.path));
}
```

### Hash Tables

```c
// String-keyed hash table (recommended convenience macros):
sp_str_ht(s32) map = SP_NULLPTR;
sp_str_ht_init(mem, map);
sp_str_ht_insert(map, sp_str_lit("key"), 100);
s32* val = sp_str_ht_get(map, sp_str_lit("key"));

// C-string-keyed hash table:
sp_cstr_ht(s32) cmap = SP_NULLPTR;
sp_cstr_ht_init(mem, cmap);
sp_cstr_ht_insert(cmap, "hello", 42);

// Generic hash table (for non-string key types):
sp_ht(u64, f32) ht = SP_NULLPTR;
sp_ht_init(mem, ht);
sp_ht_insert(ht, 100, 3.14f);
f32* v = sp_ht_getp(ht, 100);
```

### File IO
```c
// Read entire file:
sp_str_t content;
sp_err_t err = sp_io_read_file(mem, sp_str_lit("path/to/file"), &content);

// Write to file:
sp_io_file_writer_t w;
sp_io_file_writer_from_path(&w, sp_str_lit("output.txt"));
sp_io_write_str((sp_io_writer_t*)&w, sp_str_lit("hello"), SP_NULLPTR);
sp_io_file_writer_close(&w);
```

### Error Handling
```c
sp_try(expr);                    // Return if expr fails (returns sp_err_t)
sp_try_goto(expr, err, label);   // goto label on failure
sp_require(ptr != SP_NULLPTR);   // Return if condition false
SP_ASSERT(condition);            // Assert (calls sp_assert)
sp_fatal("msg {}", sp_fmt_int(detail));  // Log and abort
```

### Switch Statements
```c
switch (val) {
  case A: { break; }
  case B: { break; }
  default: { SP_UNREACHABLE_CASE(); }
}
```

## Module Namespaces

Search `references/index.md` for detailed API signatures:

| Namespace | Purpose | Key Functions |
|-----------|---------|---------------|
| `sp_str_*` | String operations | `sp_str_lit`, `sp_str_view`, `sp_str_equal`, `sp_str_empty` |
| `sp_cstr_*` | C string operations | `sp_cstr_len`, `sp_cstr_equal` |
| `sp_da` / `sp_da_*` | Dynamic arrays | `sp_da(T)`, `sp_da_push`, `sp_da_for`, `sp_da_size` |
| `sp_arr` | Fixed-capacity array | `sp_arr(T, N)`, `sp_arr_init` |
| `sp_ht` / `sp_str_ht` / `sp_cstr_ht` | Hash tables | `sp_ht_insert`, `sp_ht_getp`, `sp_str_ht_init` |
| `sp_alloc` / `sp_free` | Memory allocation | `sp_alloc`, `sp_alloc_n`, `sp_free`, `sp_mem_zero` |
| `sp_io_*` | File IO | `sp_io_read_file`, `sp_io_write_str`, `sp_io_get_std_out` |
| `sp_fs_*` | Filesystem | `sp_fs_exists`, `sp_fs_for`, `sp_fs_collect` |
| `sp_ps_*` | Processes | `sp_ps_run`, `sp_ps_create` |
| `sp_tm_*` | Time | `sp_tm_now_epoch`, `sp_tm_now_point` |
| `sp_thread_*` | Threads | `sp_thread_init`, `sp_thread_join` |
| `sp_mutex_*` | Mutexes | `sp_mutex_init`, `sp_mutex_lock` |
| `sp_env_*` | Environment | `sp_env_capture`, `sp_env_get`, `sp_env_insert` |
| `sp_tty_*` / `sp_sys_*` | TTY / low-level sys | `sp_tty_set_mode`, `sp_tty_restore`, `sp_sys_socket_*` |
| `sp_os_*` | Platform | `sp_os_get_kind`, `sp_os_sleep_ms` |
| `sp_log` / `sp_print` / `sp_fmt` | Logging/formatting | `sp_log`, `sp_print`, `sp_fmt` (args wrapped in `sp_fmt_*`) |

## Common Patterns

### Allocator Setup
```c
// At program start:
sp_mem_t mem = sp_mem_os_new();

// For most allocations, use this mem handle.
// For temporary scratch allocations:
sp_mem_arena_marker_t mark = sp_mem_begin_scratch();
// ... allocations using sp_mem_get_scratch() ...
sp_mem_end_scratch(mark);
```

### Error Propagation
```c
sp_err_t do_work(sp_mem_t mem) {
  sp_str_t content;
  sp_try(sp_io_read_file(mem, sp_str_lit("data.txt"), &content));
  // content is now valid
  return SP_OK;
}
```

### String Building
```c
sp_io_dyn_mem_writer_t w;
sp_io_dyn_mem_writer_init(mem, &w);
sp_io_write_cstr((sp_io_writer_t*)&w, "Hello ", SP_NULLPTR);
sp_io_write_str((sp_io_writer_t*)&w, name, SP_NULLPTR);
sp_str_t result = sp_io_dyn_mem_writer_as_str(&w);
```

## Reference Files

For complete API documentation with full function signatures:
- **`references/index.md`** - Comprehensive API reference (auto-generated from sp.h upstream)
- **`include/sp.h`** - The actual single-header library source (authoritative)
- **`include/sp/*.h`** - Extra module headers (`sp_math`, `sp_elf`, `sp_msvc`, `sp_prompt`, `sp_cli`, `sp_glob`, `sp_http`, `sp_macho`, `sp_asset`, `sp_test`); include them with their own `SP_*_IMPLEMENTATION` macro

## Examples

Example code demonstrating sp.h usage:

| File | Description |
|------|-------------|
| `references/example/msvc.c` | MSVC compiler specific examples |
| `references/example/cli/palette.c` | Terminal color palette demo |
| `references/example/cli/prompt.c` | Interactive CLI prompt example |
| `references/example/freestanding/embed.c` | Embedded usage example |

## Practical Tips & Pitfalls

### SP_IMPLEMENTATION 的正确使用
sp.h 是单头文件库，需要在**一个且仅一个** C 文件中定义 `SP_IMPLEMENTATION` 宏：
```c
// 在 main.c 中：
#define SP_IMPLEMENTATION
#include "sp.h"

// 在其他文件中只需包含头文件：
#include "sp.h"
```
**错误现象**：多个 .o 文件中出现重复定义的链接错误。

### Android/Termux 平台适配
在 Android/Termux 环境中，某些 POSIX 函数不可用：
- `posix_spawn_file_actions_addchdir_np` 在 Android 上缺失
**解决方案**：在编译时添加 `-DSP_PS_DISABLE` 禁用进程支持模块：
```makefile
CFLAGS += -DSP_PS_DISABLE
```

### API 名称的常见错误
- `sp_str_eq` → 正确：`sp_str_equal`
- `sp_os_read_entire_file` → 正确：`sp_io_read_file`
- `sp_dyn_array(T)` / `sp_dyn_array_push` / `sp_dyn_array_for` → 正确：`sp_da(T)` / `sp_da_push` / `sp_da_for`
- `sp_atomic_s32_get/set` / `sp_atomic_ptr_get/set` → 正确：`sp_atomic_s32_load/store` / `sp_atomic_ptr_load/store`（需传内存序 `SP_ATOMIC_RELAXED` 等）
- `sp_os_tty_enter_raw` / `sp_os_tty_restore` / `sp_os_print` → 正确：`sp_tty_set_mode` / `sp_tty_restore` / `sp_io_write_str(sp_io_get_std_out(), ...)`
- `sp_env_set(name, value)` → 正确：`sp_env_insert(&env, name, value)`（先 `sp_env_capture` 获取 env）
- `sp_str_map` / `sp_str_reduce` → 已移除（"str: kill fake functional shit"）

### 字符串结构成员
`sp_str_t` 结构使用 `.data` 成员，而不是 `.ptr`：
```c
// ❌ 错误
c8 ch = str.ptr[i];

// ✅ 正确
c8 ch = str.data[i];
```

### 零初始化注意事项
`sp_zero` 不能用于全局变量赋值（它不是编译时常量表达式）：
```c
// ❌ 错误（可能在某些编译器上不通过）
editor_t E = sp_zero;

// ✅ 正确方式：显式初始化或使用 sp_mem_zero
editor_t E;
sp_mem_zero(&E, sizeof(E));
```
注意：`sp_zero` 在局部变量和 `sp_alloc` + `sp_mem_zero` 组合使用是安全的。

### 字符处理头文件
使用 `isalpha`、`isdigit` 等函数时需要包含 `<ctype.h>`：
```c
#include <ctype.h>  // 必须包含
```

### 文件读写 API
文件操作应使用 `sp_io_*` 系列函数：
- 读取：`sp_err_t err = sp_io_read_file(mem, path, &content);`（注意第三个参数是输出指针）
- 写入：使用 `sp_io_file_writer_from_path()` + `sp_io_write_str()` + `sp_io_file_writer_close()`

### 格式化参数必须包裹类型宏
sp.h 的格式字符串使用 `{}` 占位，参数**必须**用 `sp_fmt_*` 宏包裹（这是类型安全的核心）：
```c
// ❌ 错误：裸参数，编译器无法推断类型
sp_log("Value: {}", x);

// ✅ 正确：用 sp_fmt_* 宏包裹，明确类型
sp_log("Value: {}", sp_fmt_int(x));
sp_log("Name: {}, Age: {}", sp_fmt_str(name), sp_fmt_uint(age));

// sp_fmt() 返回 sp_str_r（Result 类型），取字符串要用 .value
sp_str_t s = sp_fmt(mem, "{}", sp_fmt_int(x)).value;
```
可用的包裹宏：`sp_fmt_int` / `sp_fmt_uint` / `sp_fmt_float` / `sp_fmt_str` / `sp_fmt_cstr` / `sp_fmt_char` / `sp_fmt_ptr`，以及颜色/样式宏 `sp_fmt_red()` / `sp_fmt_cyan()` / `sp_fmt_bold()` / `sp_fmt_italic()` 等。

## Common Mistakes

```c
// ❌ 错误: 使用C字符串 + printf
const char* name = "Alice";
printf("Hello %s\n", name);

// ✅ 正确: 使用sp_str_t + sp_log（参数用 sp_fmt_str 包裹）
sp_str_t name = sp_str_lit("Alice");
sp_log("Hello {}", sp_fmt_str(name));

// ❌ 错误: 手动计算字符串长度
if (strlen(str) > 0) { ... }

// ✅ 正确: 使用sp.h的API
if (!sp_str_empty(str)) { ... }

// ❌ 错误: 裸malloc
int* arr = malloc(sizeof(int) * 10);

// ✅ 正确: 使用sp_alloc (需要 sp_mem_t 句柄)
int* arr = sp_alloc(mem, sizeof(int) * 10);

// ❌ 错误: 手动for循环遍历动态数组
for (u32 i = 0; i < sp_da_size(arr); i++) { ... }

// ✅ 正确: 使用遍历宏
sp_da_for(arr, i) { ... }

// ❌ 错误: 格式化参数不包裹类型宏（裸参数）
sp_log("Value: {}", name);

// ✅ 正确: 用小写 sp_log，参数用 sp_fmt_* 宏包裹
sp_log("Value: {}", sp_fmt_str(name));
```

## Checklist

在提交代码前，确认：

- [ ] 使用 `sp_zero` 或 `sp_mem_zero()` 初始化结构体
- [ ] 使用 `sp_str_t` 而不是 `const char*`
- [ ] 使用 `sp_alloc(mem, size)` 而不是 `malloc()` — 注意 mem 参数
- [ ] 使用 `sp_log()` / `sp_print()` 而不是 `printf()`
- [ ] 使用 `sp_str_empty()` 而不是检查 `len > 0`
- [ ] Switch 语句处理所有枚举值，default 用 `SP_UNREACHABLE_CASE()`
- [ ] 使用 `sp_da_for()` 或 `sp_carr_for()` 遍历数组
- [ ] 字符串比较使用 `sp_str_equal()` 而不是 `strcmp()`
- [ ] 格式化字符串参数用 `sp_fmt_int` / `sp_fmt_str` 等宏包裹（类型安全，裸参数编译不过）
- [ ] 动态数组类型使用 `sp_da(T)` 而非 `sp_dyn_array(T)`

## Finding APIs

When looking for a specific function:
1. Check the namespace table above
2. Search `references/index.md` for the pattern
3. Search `include/sp.h` for the exact function/macro definition (authoritative)
4. All public APIs are marked with `SP_API` in the source
