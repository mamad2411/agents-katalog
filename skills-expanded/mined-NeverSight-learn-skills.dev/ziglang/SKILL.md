---
name: ziglang
description: >-
  Guides correct Zig 0.15.x programming, build system configuration, and
  standard library usage. Covers breaking API changes from prior versions
  (ArrayList, I/O rewrite, build.zig, Ed25519, JSON, HTTP client,
  @typeInfo enum casing, usingnamespace removal). Use when writing Zig code,
  debugging Zig compiler errors, configuring build.zig, or when the user
  mentions Zig, zig build, zig test, or Zig standard library.
---

# Zig 0.15.x Programming

> **Version scope**: Pinned to Zig 0.15.x (specifically 0.15.2). For master/nightly, APIs may differ. Always check official docs for the target version.

Many LLMs have outdated Zig knowledge (0.11-0.14) that causes compilation errors. This skill ensures correct 0.15.x API usage.

## Official Documentation

- Language Reference: <https://ziglang.org/documentation/0.15.2/>
- Standard Library: <https://ziglang.org/documentation/0.15.2/std/>
- Release Notes: <https://ziglang.org/download/0.15.1/release-notes.html>
- Build System: <https://ziglang.org/learn/build-system/>
- Source: <https://codeberg.org/ziglang/zig>

## Critical API Changes in 0.15

### ArrayList -- Allocator Now Required

All mutating methods require an explicit `allocator` parameter. `AssumeCapacity` variants do not.

```zig
var list = try std.ArrayList(T).initCapacity(allocator, 16);
defer list.deinit(allocator);
try list.append(allocator, item);
try list.appendSlice(allocator, items);
_ = try list.addOne(allocator);
_ = try list.toOwnedSlice(allocator);

list.appendAssumeCapacity(item); // no allocator needed
```

### I/O Rewrite (Writergate)

New `std.Io.Writer` and `std.Io.Reader` are non-generic, buffer-in-interface, ring-buffer-based types.

```zig
// stdout (0.15+)
var stdout_buffer: [1024]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
const stdout: *std.Io.Writer = &stdout_writer.interface;
try stdout.print("Hello\n", .{});
try stdout.flush();

// adapter for old-style writers
fn useOldWriter(old_writer: anytype) !void {
    var adapter = old_writer.adaptToNewApi(&.{});
    const w: *std.Io.Writer = &adapter.new_interface;
    try w.print("{s}", .{"example"});
}
```

### @typeInfo Enum Cases -- Lowercase

```zig
// 0.15+ uses lowercase / @"" escaped names
if (@typeInfo(T) == .slice) { ... }
if (@typeInfo(T) == .pointer) { ... }
if (@typeInfo(T) == .@"struct") { ... }
if (@typeInfo(T) == .@"enum") { ... }
if (@typeInfo(T) == .@"union") { ... }
```

### Custom Format Functions -- {f} Specifier

```zig
// 0.15+: use {f}, simplified signature
pub fn format(self: Self, writer: anytype) !void {
    try writer.writeAll("...");
}
// Usage: std.fmt.bufPrint(&buf, "{f}", .{value});
```

### usingnamespace Removed

```zig
// explicit re-exports instead
pub const foo = @import("other.zig").foo;
// or namespace via field
pub const other = @import("other.zig");
```

### async/await Keywords Removed

Async functionality will be provided via the standard library's new I/O interface in a future release.

## Build System (build.zig)

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "hello",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    b.installArtifact(exe);

    const run_exe = b.addRunArtifact(exe);
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_exe.step);

    const unit_tests = b.addTest(.{
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = b.graph.host,
        }),
    });
    const run_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_tests.step);
}
```

Key changes from 0.14:

- `root_source_file` moved inside `b.createModule(...)` via `root_module`
- Use `b.path("src/main.zig")` instead of `.{ .path = "src/main.zig" }`
- Libraries: `b.addLibrary(.{ .linkage = .dynamic, ... })` replaces `addSharedLibrary`
- Module deps: `exe.root_module.addImport("sdk", sdk_module)` replaces `exe.addModule`
- Test target: use `b.graph.host` for native

## Common Patterns

### HashMap

```zig
// Managed (stores allocator)
var map = std.StringHashMap(V).init(allocator);
defer map.deinit();
try map.put(key, value);

// Unmanaged (allocator per call)
var map = std.StringHashMapUnmanaged(V){};
defer map.deinit(allocator);
try map.put(allocator, key, value);
```

### JSON

```zig
// Parse
const parsed = try std.json.parseFromSlice(MyStruct, allocator, json_str, .{});
defer parsed.deinit();
const data = parsed.value;

// Serialize (no stringifyAlloc in 0.15.2)
const formatted = try std.fmt.allocPrint(allocator, "{f}", .{std.json.fmt(data, .{})});
defer allocator.free(formatted);
```

### Testing

```zig
test "no memory leaks" {
    const allocator = std.testing.allocator;
    const data = try allocator.alloc(u8, 100);
    defer allocator.free(data);
}

test "assertions" {
    try std.testing.expect(condition);
    try std.testing.expectEqual(expected, actual);
    try std.testing.expectEqualSlices(u8, expected, actual);
    try std.testing.expectError(error.SomeError, result);
    try std.testing.expectEqualStrings("hello", str);
}
```

### Memory Operations

```zig
@memcpy(dest, src);
@memset(buffer, 0);
const equal = std.mem.eql(u8, slice1, slice2);
const index = std.mem.indexOf(u8, haystack, needle);
```

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| expected 2 argument(s), found 1 | ArrayList method missing allocator | Add allocator as first arg |
| no field named `root_source_file` | Old build.zig API | Use `root_module = b.createModule(...)` |
| enum has no member named 'Slice' | @typeInfo case changed | Use lowercase `.slice` |
| expected error union, found 'Signature' | Ed25519 Signature.fromBytes doesn't return error | Remove `try` |
| no member function named 'open' | Old HTTP API | Use `client.request()` or `client.fetch()` |

## Verification Workflow

1. Run `zig build` to check compilation
2. Match errors against the table above and apply fixes
3. Run `zig build test` to verify functionality
4. Use `zig build -Doptimize=ReleaseFast test` to catch UB

## Additional References

- For stdlib API details (HTTP, Ed25519, Base64): [references/stdlib-api-reference.md](references/stdlib-api-reference.md)
- For build system details: [references/build-system.md](references/build-system.md)
- For migration patterns from 0.13/0.14: [references/migration-patterns.md](references/migration-patterns.md)

## Community Resources

- Zig Cookbook: <https://cookbook.ziglang.cc/>
- awesome-zig: <https://github.com/zigcc/awesome-zig>
- Zigistry (package registry): <https://zigistry.dev/>

## Production Codebases

| Project | URL | Focus |
|---------|-----|-------|
| Bun | <https://github.com/oven-sh/bun> | JS runtime, async I/O, FFI |
| Tigerbeetle | <https://github.com/tigerbeetle/tigerbeetle> | Financial DB, deterministic execution |
| Ghostty | <https://github.com/ghostty-org/ghostty> | Terminal emulator, GPU rendering |
| Mach | <https://github.com/hexops/mach> | Game engine, graphics |
| ZLS | <https://github.com/zigtools/zls> | Language Server |
