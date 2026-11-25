# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build

```sh
# First-time setup
meson setup build

# Compile
meson compile -C build

# Run all tests
meson test -C build --print-errorlogs

# Run a single test
meson test -C build --print-errorlogs config   # or path / validate / ops
```

Docker convenience wrapper (runs build + tests inside Ubuntu 26.04):

```sh
./docker-build.sh           # glibc
./docker-build.sh musl      # musl via musl-gcc
./docker-build.sh all       # both
```

## Architecture

`populate-volatile` reads declarative config files from `/etc/default/volatiles/` (one entry per line: `TYPE USER GROUP MODE NAME LTARGET`) and creates the described files, directories, symlinks, or bind-mounts on a tmpfs/ramfs at boot, or stages them into a rootfs image at build time (via `-r <rootdir>`, run under [pseudo](https://git.yoctoproject.org/pseudo)).

### Runtime flags

- `-v` - verbose: log each action to stdout
- `-n` - dry-run: implies `-v`; no filesystem changes made
- `-T` - trace: emit detailed per-syscall diagnostics to stderr (unbuffered); useful for diagnosing failed operations. Controlled by global `int pv_trace` (defined in `lib/path.c`, declared in `include/pv/trace.h`).

### Processing order

1. `00_core` is applied first, unconditionally and without user/group validation, matching the upstream shell script's ordering; later config files may rely on the core directories it creates. (The script needed `/var/volatile/tmp` for its requirement checker's temp files; the `getpwnam_r`-based checks here do not.)
2. All remaining config files apply entries individually; entries whose user/group don't exist are skipped.

### Library (`libpv`, static)

| File | Responsibility |
|---|---|
| `lib/config.c` | Line parser (`pv_parse_line`) and file reader (`pv_parse_config`) using a callback |
| `lib/ops.c` | Filesystem operations: `pv_create_file`, `pv_mkdir`, `pv_link_file`, `pv_bind_mount`, `pv_apply_entry` dispatcher |
| `lib/validate.c` | `pv_check_requirements` - resolves users/groups via `getpwnam`/`getgrnam` |
| `lib/path.c` | Path utilities used by ops |

All ops receive a `pv_ctx_t` (rootfd, rootdir, verbose, dry_run, rootfs_mode).

### Key types (`include/pv/`)

- `pv_entry_t` - one parsed config record (type, user, group, mode, name, ltarget)
- `pv_ctx_t` - operation context threaded through all ops functions
- `pv_entry_cb` - callback signature used by `pv_parse_config`

### Tests

Unity 2.6.1 is vendored in `tests/unity/` under the MIT license (see `tests/unity/unity.h`). Five test executables (`test_config`, `test_path`, `test_validate`, `test_ops`, `test_bind_mount`) are built and registered with `meson test`. The bind-mount tests require `CAP_SYS_ADMIN` and exit 77 (meson SKIP) without it; they can be run unprivileged via `unshare -rm build/test_bind_mount`.

## Licensing

This project is **GPL-2.0-only** (`LICENSE.txt`). The vendored Unity test framework (`tests/unity/`) is licensed separately under the **MIT license** - see the header in `tests/unity/unity.h`.
