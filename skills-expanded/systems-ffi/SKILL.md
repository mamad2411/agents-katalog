---
name: systems-ffi
description: "Foreign function interfaces: the C ABI as the boundary, repr(C) layouts, who allocates and who frees, strings and UTF-8 across the boundary, errors without unwinding, panics caught at the edge, callbacks and user data, thread safety, bindgen, cbindgen and cxx, bindings for Python, Node and WebAssembly, ABI versioning, and testing both sides. Read before calling across languages or exposing a library to another language."
---

# Across the language boundary

FFI written by default: a Rust `String` handed to C as a pointer that is
freed when the function returns, a struct passed by value without
`#[repr(C)]`, `long` in the header, a panic unwinding into C, a callback
holding a closure nobody knows how long to keep, and `free()` called on
memory Rust allocated. Each works in the demo and corrupts memory later.
The rules: the boundary is the C ABI, every function states who owns
what, nothing unwinds across it, and both sides are tested. Rust idioms in
`systems-rust`, C and C++ in `systems-c-cpp`.

## 1. The C ABI is the boundary

- Only C crosses: `extern "C"` functions, `#[repr(C)]` types, fixed-width
  integers, pointers and lengths. Never C++ classes, exceptions, Rust
  generics, trait objects, `String`, `Vec` or `std::string`.
- Opaque handles over shared structs: the header declares
  `typedef struct mylib_parser mylib_parser;` and functions take
  `mylib_parser *`, so the layout can change without breaking callers.
  Share a struct only when it is plain data, and then pin its layout
  (`const _: () = assert!(size_of::<Header>() == 16);`).

| C | Rust | Note |
|---|---|---|
| `int32_t`, `uint64_t`, `uint8_t` | `i32`, `u64`, `u8` | prefer these in the API |
| `size_t` | `usize` | |
| `int`, `long`, `char` | `c_int`, `c_long`, `c_char` (`std::ffi`) | `long` is 32 bits on Windows; `char` signedness varies |
| `bool` | `bool` | only against a real C `bool` |
| `const char *` (NUL-terminated) | `*const c_char`, read with `CStr` | |
| `const uint8_t *data, size_t len` | `*const u8, usize` | |
| function pointer, may be null | `Option<unsafe extern "C" fn(...)>` | Rust fn pointers are never null |
| enum value from C | `c_int` or `u32`, converted with a `match` | a Rust enum holding an unknown value is UB |

## 2. Who allocates, who frees

- The side that allocates frees, with its own allocator: Rust memory comes
  back through a Rust function (`mylib_parser_free`), C memory through C.
  Never `free()` a Rust pointer or `Box::from_raw` a `malloc` one; on
  Windows even two C runtimes have separate heaps.
- Each function's doc says which pointers are borrowed for the call only,
  which are taken over, which returned pointers the caller must free and
  with what, and whether null is allowed. Free functions accept null.

```rust
use std::ffi::{c_char, c_int, CStr};
use std::panic::{catch_unwind, AssertUnwindSafe};

pub const MYLIB_OK: c_int = 0;
pub const MYLIB_ERR_NULL: c_int = 1;
pub const MYLIB_ERR_UTF8: c_int = 2;
pub const MYLIB_ERR_PARSE: c_int = 3;
pub const MYLIB_ERR_PANIC: c_int = 99;

/// Returns a parser, or null on failure. Free it with `mylib_parser_free`.
#[unsafe(no_mangle)]
pub extern "C" fn mylib_parser_new(strict: bool) -> *mut Parser {
    catch_unwind(|| Box::into_raw(Box::new(Parser::new(strict)))).unwrap_or(std::ptr::null_mut())
}

/// # Safety
/// `parser` is null or came from `mylib_parser_new` and is not used again.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mylib_parser_free(parser: *mut Parser) {
    if !parser.is_null() {
        // SAFETY: made by Box::into_raw in mylib_parser_new; freed once (contract).
        drop(unsafe { Box::from_raw(parser) });
    }
}

/// Counts the records in `input` and writes the count to `*out`.
///
/// # Safety
/// `parser` is live, `input` is NUL-terminated and valid for the call,
/// `out` is valid for one write.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mylib_count(parser: *const Parser, input: *const c_char, out: *mut u64) -> c_int {
    if parser.is_null() || input.is_null() || out.is_null() {
        return MYLIB_ERR_NULL;
    }
    catch_unwind(AssertUnwindSafe(|| {
        // SAFETY: both non-null (checked above); valid for the call (contract).
        let (parser, input) = unsafe { (&*parser, CStr::from_ptr(input)) };
        let Ok(text) = input.to_str() else { return MYLIB_ERR_UTF8 };
        match parser.count(text) {
            Ok(n) => {
                // SAFETY: non-null (checked above) and valid for a write (contract).
                unsafe { out.write(n) };
                MYLIB_OK
            }
            Err(_) => MYLIB_ERR_PARSE,
        }
    }))
    .unwrap_or(MYLIB_ERR_PANIC)
}
```

`#[unsafe(no_mangle)]` is the edition 2024 spelling (`#[no_mangle]`
before 1.82). cbindgen declares `Parser` as an opaque struct;
`[export.rename]` in `cbindgen.toml` names it `mylib_parser`.

## 3. Strings and buffers

- Prefer pointer and length (`const uint8_t *data, size_t len`) to
  NUL-terminated strings: no scan, embedded zeros allowed. C often passes
  null with length 0, which `slice::from_raw_parts` does not accept:
  branch on `len == 0` first (the trampoline in section 5 shows it).
- C strings into Rust: `CStr::from_ptr` (valid, NUL-terminated, alive for
  the call), then `to_str()` to validate UTF-8 and return an error code,
  or `to_string_lossy()` where replacement characters are acceptable.
- Rust strings out: `CString::new(s)` fails on an interior NUL (handle
  it); `into_raw()` hands it over and a Rust free function takes it back
  with `CString::from_raw`. Or the caller passes a buffer and gets the
  length needed back, `snprintf`-style, and nothing needs freeing.
- A returned borrowed pointer points at static or handle-owned memory,
  lifetime documented (`mylib_version()` returns `c"1.4.0".as_ptr()`).
- Windows APIs are UTF-16: `encode_wide()` from `OsStrExt` in Rust,
  `MultiByteToWideChar` in C, the `W` functions, never the `A` ones.

## 4. Errors without unwinding

- Return a status (`int`, 0 for success) and write results through
  out-parameters, or return a handle and null on failure. For messages, a
  thread-local `mylib_last_error_message()` valid until the next call on
  that thread, or a caller-provided buffer.
- Nothing unwinds across the boundary: every exported Rust function wraps
  its body in `catch_unwind` and maps a panic to an error code. Since Rust
  1.81 a panic escaping `extern "C"` aborts the process: defined, but it
  takes the host down. `extern "C-unwind"` only when unwinding through is
  meant and both sides are built for it. `panic = "abort"` makes
  `catch_unwind` useless, so a loadable library keeps unwinding.
- C++ exporting C: each function `noexcept`, ending in `catch (const
  std::exception& e) { set_error(e.what()); return -1; } catch (...) {
  return -1; }`.
- Calling C from Rust: check every return code and `errno`
  (`io::Error::last_os_error()` right after the call) and convert into
  the crate's error type in the safe wrapper.

## 5. Callbacks and user data

- A C callback is a function pointer plus a `void *user_data` passed back
  on each call. Registration documents when calls happen (which thread,
  re-entrant or not) and how long `user_data` lives (until unregistered).
- A Rust closure given to a C library: box it, pass the box pointer as
  `user_data`, and a generic trampoline that restores it:

```rust
unsafe extern "C" fn trampoline<F: FnMut(&[u8])>(user: *mut c_void, data: *const u8, len: usize) {
    let _ = catch_unwind(AssertUnwindSafe(|| {
        // SAFETY: `user` is the Box<F> registered with the library, alive until unregistered.
        let f = unsafe { &mut *user.cast::<F>() };
        let bytes = if len == 0 {
            &[][..]
        } else {
            // SAFETY: the library passes `len` bytes, valid during the callback.
            unsafe { std::slice::from_raw_parts(data, len) }
        };
        f(bytes);
    }));
}
// Register: lib_on_data(h, Some(trampoline::<F>), Box::into_raw(Box::new(f)).cast());
// After unregistering: drop(unsafe { Box::from_raw(user.cast::<F>()) });
```

- The trampoline catches panics (record them for the wrapper to report).

## 6. Thread safety

- Find out what the foreign library promises: fully thread-safe, one
  thread per handle at a time, or global state needing one thread (many
  older C libraries, most GUI toolkits).
- Encode it in types: a wrapper holding a raw pointer is `!Send` and
  `!Sync` automatically; add `unsafe impl Send` or `Sync` only with a
  `SAFETY` comment citing the library's documentation. Serialise an unsafe
  library behind one `Mutex`, or one owning thread fed by a channel.
  Thread-local error state (`errno`) is read on the same thread, at once.

## 7. Generating bindings

- C headers into Rust: bindgen in `build.rs` into `OUT_DIR`; raw bindings
  in a `foo-sys` crate (`links = "foo"` in its `Cargo.toml`) and a safe
  `foo` crate on top. Allowlist what you use:

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    println!("cargo:rustc-link-lib=foo");
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .allowlist_function("foo_.*")
        .allowlist_type("foo_.*")
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        .generate()
        .expect("generate bindings for wrapper.h");
    let out = std::path::PathBuf::from(std::env::var("OUT_DIR").expect("cargo sets OUT_DIR"));
    bindings.write_to_file(out.join("bindings.rs")).expect("write bindings.rs");
}
```

  Then `include!(concat!(env!("OUT_DIR"), "/bindings.rs"));`. `cc` builds
  bundled C, `pkg-config` finds system libraries; bindgen needs libclang,
  so some `-sys` crates commit pre-generated bindings instead.
- Rust into a C header: cbindgen with a committed `cbindgen.toml`
  (`language = "C"`, include guard, prefix), regenerated in CI and diffed
  against the committed header:
  `cbindgen --config cbindgen.toml --crate mylib --output include/mylib.h`.
- C++: `cxx` for a safe bridge both ways (`#[cxx::bridge]` with
  `UniquePtr`, `CxxString`, slices, shared structs); `autocxx` generates
  one from existing headers. Raw bindgen over C++ headers is fragile.

## 8. Other runtimes

| Target | Tool | Build |
|---|---|---|
| Python | PyO3 | `maturin develop`, `maturin build --release` (abi3 wheels with an `abi3-py39` feature) |
| Node.js | napi-rs | `napi build --platform --release` (`@napi-rs/cli`) |
| Browser | wasm-bindgen | `wasm-pack build --target web`, or the `wasm-bindgen` CLI |
| WASI components | `wit-bindgen`, `cargo component` | target `wasm32-wasip2` |
| Swift, Kotlin | UniFFI | bindings generated from the Rust interface |
| Java, Android | the `jni` crate | `System.loadLibrary` on the Java side |

The same rules hold inside these tools: ownership explicit, no panic
escaping (PyO3 and napi-rs turn them into exceptions), long work off the
host's main thread: PyO3's `py.detach(|| ...)` (`allow_threads` before
0.26) releases the interpreter, napi-rs's `AsyncTask` spares the event loop.

## 9. Versioning, visibility, linking

- Prefix every exported symbol (`mylib_`), export `mylib_version()`, and
  never change a published signature or public struct layout: add
  `mylib_parse2`, or take options in a struct whose first field is its own
  size (`uint32_t size`, set to `sizeof`), so it can grow.
- Shared library versions: bump the SONAME (`libmylib.so.1`, CMake
  `SOVERSION`) on an ABI break; Windows exports via `__declspec(dllexport)`
  or a `.def` file.
- Export only the API: `-fvisibility=hidden` in C and C++; a Rust `cdylib`
  exports only its `#[no_mangle]` functions. `crate-type = ["cdylib"]` or
  `["staticlib"]`; a static library needs the system libraries std uses,
  listed by `cargo rustc --lib --release -- --print native-static-libs`.
- Static linking: one file, no version skew, a rebuild for every fix.
  Dynamic: shared updates, plus versions and loader paths to manage.

## 10. Test both sides

- Rust tests call the exported functions directly: null arguments,
  invalid UTF-8, length 0, a panic path, free of null. Miri runs them for
  the Rust side (it does not execute foreign C code).
- A C (or C++) program includes the generated header, links the built
  library, and runs in CI under ASan and UBSan (Valgrind on Linux):
  create, use, free, error codes, and threads if the API promises them.
- The header is regenerated and diffed in CI, so the Rust signature and
  the C declaration cannot drift. Python, Node and wasm bindings get tests
  in that language (pytest, `node --test`, `wasm-bindgen-test`).

## Check it

- Every exported function: `catch_unwind` around the body, null checks, a
  `# Safety` doc naming who owns each pointer, a test that passes null.
- `bash`: `cargo test`, `cargo +nightly miri test`, the C harness under
  ASan, and a clean `git diff` on the regenerated header.
- `nm -gU` (macOS) or `nm -D --defined-only` (Linux) on the library shows
  only prefixed API symbols.
- Say which side could not be run here (no C toolchain, no target runtime).

## Avoid

Rust types without `#[repr(C)]` across the boundary; `long` or `int` for
sizes in the API; freeing with the other side's allocator; pointers to
temporaries (`CString::new(s)?.as_ptr()` dangles at the end of the
statement); panics or C++ exceptions crossing into C; Rust enums or
non-`Option` function pointers taking values from C; `unsafe impl Send`
or `Sync` without the library's word; `user_data` freed while its
callback is still registered; a published signature or struct layout
changed; a hand-written header that drifts from the code.
