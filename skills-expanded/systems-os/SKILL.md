---
name: systems-os
description: "Working with the operating system: files and buffered IO, fsync and durable writes, atomic replace by rename, file locking, processes and exit codes, signals and graceful shutdown, pipes and stdio, environment and permissions, paths and encodings across platforms, monotonic versus wall-clock time, sockets with timeouts, resource limits, and command-line tool conventions. Read before writing code that touches files, processes, signals or the terminal."
---

# Working with the operating system

Default OS code works on the developer's laptop: `fs::write` straight over
the config (a crash leaves half a file), `sh -c` with a formatted string,
a child's stdout read to the end before its stderr (a deadlock once 64 KiB
of errors pile up), no SIGTERM handler (the container is killed after 10
seconds with work lost), colour codes written into a pipe, `SystemTime`
used to time a request, and `/` glued into paths by hand. This skill is
how files, processes, signals, the terminal, time and sockets really
behave, and the conventions a command-line tool follows.

## 1. Files and buffered IO

- Each unbuffered `read` or `write` is a syscall: wrap files and sockets
  in `BufReader`/`BufWriter` (8 KiB default; 64 KiB or more for large
  sequential files via `with_capacity`).
- Stream large files (`lines()`, `read_until`, chunks); read a whole file
  only when it is small and bounded (check `metadata()?.len()` first).
- `BufWriter` flushes on drop and discards the error: `flush()?` before
  reporting success. In C, check `fclose` and `close` (delayed errors).
- `read` and `write` may move fewer bytes than asked: `read_exact` and
  `write_all` loop; in C, loop and retry on `EINTR`.

## 2. Durable writes

- A successful `write` only reached the page cache. `sync_all()` (fsync)
  or `sync_data()` (fdatasync) before telling anyone the data is saved; a
  created or renamed file also needs its directory fsynced, or the entry
  may vanish after a crash (POSIX; not on Windows).
- macOS `fsync` does not flush the drive's cache: Rust's `sync_all` and
  `sync_data` use `F_FULLFSYNC` there; in C call `fcntl(fd, F_FULLFSYNC)`.
- A failed fsync is not retryable (Linux may already have marked the pages
  clean): treat it as fatal for that file and rewrite from a good state.
- fsync costs milliseconds: sync per batch or interval, and write down
  what a crash may lose.

## 3. Atomic replace

Readers see the old file or the new one, never half of either:

```rust
use std::io::Write;
use std::path::Path;

pub fn write_atomic(path: &Path, bytes: &[u8]) -> std::io::Result<()> {
    let dir = match path.parent() {
        Some(p) if !p.as_os_str().is_empty() => p,
        _ => Path::new("."),
    };
    let mut tmp = tempfile::NamedTempFile::new_in(dir)?; // same file system as `path`
    tmp.write_all(bytes)?;
    tmp.as_file().sync_all()?;
    tmp.persist(path)?; // rename(2) over the old file
    #[cfg(unix)]
    std::fs::File::open(dir)?.sync_all()?; // make the rename itself durable
    Ok(())
}
```

- The temp file lives in the target's directory: `rename` across file
  systems fails with `EXDEV`, so never `/tmp`.
- In C: `open(tmp, O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644)`, write
  all, `fsync`, `close`, `rename(tmp, path)`, then fsync the directory.
- `NamedTempFile` is created 0600: copy the old file's mode first when it
  matters. On Windows, replacing a file another process holds open fails:
  retry briefly. Clean up leftover temp files (known prefix) at startup.

## 4. File locks

- `File::lock`, `lock_shared` and `try_lock` (std since Rust 1.89) are
  `flock` on Unix and `LockFileEx` on Windows; open the file for writing.
- Unix locks are advisory (they stop only processes that also lock);
  Windows locks are mandatory. POSIX `fcntl` locks vanish when the process
  closes any descriptor of the file; avoid them for whole-file locking.
- Lock a `.lock` file and keep the handle for the process's life: the OS
  releases it on exit or crash, while a file's mere existence goes stale.
  Locks over NFS or SMB are unreliable: keep lock files on local disk.

```rust
let lock = OpenOptions::new().create(true).truncate(false).write(true).open(dir.join("app.lock"))?;
match lock.try_lock() {
    Ok(()) => {} // keep `lock` alive until exit
    Err(std::fs::TryLockError::WouldBlock) => anyhow::bail!("another instance is running"),
    Err(std::fs::TryLockError::Error(e)) => return Err(e.into()),
}
```

## 5. Processes

- An argument array, never a shell string:
  `Command::new("git").args(["log", "--format=%H", "--"]).arg(&path)`.
  User input in `sh -c` is command injection, and a value starting with
  `-` becomes an option: put `--` before operands. `env_clear()` plus the
  variables needed when a child must not inherit secrets.
- `output()` reads stdout and stderr concurrently. Streaming with
  `spawn()`, drain both pipes at once (a thread each, or async): reading
  one to the end while the other fills its 64 KiB buffer hangs both sides.
- Always `wait()`, or the child stays a zombie; on timeout `kill()` then
  `wait()` (tokio: `kill_on_drop(true)` with `tokio::time::timeout`).
- `code()` is `None` when a signal killed the child (`ExitStatusExt::signal()`
  on Unix). A failure names the command, the code and the tail of stderr.

| Exit code | Meaning |
|---|---|
| 0 | success |
| 1 | general failure |
| 2 | usage error (bad flags or arguments) |
| 126, 127 | found but not executable; not found (shell) |
| 128 + N | killed by signal N: 130 SIGINT, 137 SIGKILL (often the OOM killer), 143 SIGTERM |

## 6. Signals and graceful shutdown

| Signal | Sent by | Do |
|---|---|---|
| SIGINT | Ctrl-C | stop gracefully; a second one exits at once |
| SIGTERM | `kill`, systemd, `docker stop`, Kubernetes | stop within the grace period (10s Docker, 30s Kubernetes), then SIGKILL comes |
| SIGHUP | a closed terminal; by convention to daemons | reload configuration, or exit in interactive tools |
| SIGPIPE | writing to a closed pipe | Rust ignores it, so writes fail with `BrokenPipe`: exit quietly |

- Graceful: stop accepting work, finish or hand back in-flight work within
  a deadline shorter than the grace period, flush buffers and logs, fsync
  state, exit 0; past the deadline, exit non-zero. SIGKILL cannot be
  caught, so nothing important may depend on a clean exit.
- Handlers call only async-signal-safe functions (`write`, `_exit`, a
  `volatile sig_atomic_t` or atomic store): no `malloc`, `printf`, locks
  or logging. Set a flag or write to a self-pipe and act in normal code,
  or use `signalfd` (Linux) or `sigwait` on a dedicated thread. Rust:
  `tokio::signal`, or `signal-hook` and `ctrlc` in sync code.

```rust
async fn shutdown_signal() {
    let ctrl_c = async { tokio::signal::ctrl_c().await.expect("install Ctrl-C handler") };
    #[cfg(unix)]
    let terminate = async {
        use tokio::signal::unix::{signal, SignalKind};
        signal(SignalKind::terminate()).expect("install SIGTERM handler").recv().await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();
    tokio::select! { () = ctrl_c => {}, () = terminate => {} }
}
```

PID 1 in a container has no default signal actions: unhandled SIGTERM is
ignored until SIGKILL. Handle it, or run under `tini` (`docker run --init`).

## 7. stdio and the terminal

- stdout carries the output a pipe or script consumes; logs, progress,
  warnings and errors go to stderr. `--json` gives machine-readable output
  with a stable shape.
- Rust's stdout is line-buffered even into a pipe: for bulk output use
  `BufWriter::new(io::stdout().lock())` and flush at the end.
- `std::io::IsTerminal` (`isatty` in C) gates colours, progress bars and
  prompts. Honour `NO_COLOR` (set and non-empty: no colour),
  `--color=auto|always|never` and `TERM=dumb`. `-` as a file argument
  means stdin or stdout.
- `app | head` closes the pipe early: `println!` panics on it, so bulk
  writers use `writeln!`, treat `ErrorKind::BrokenPipe` as the end, and
  exit 0.

## 8. Environment and permissions

- Read environment variables once at startup into a typed config,
  validate, fail fast naming the variable; never print a secret's value or
  log the environment. `env::var` fails on non-UTF-8: `var_os` for paths.
- Precedence: flags over environment over config file over defaults; a
  `config show` command (secrets masked) saves hours.
- `std::env::set_var` is `unsafe` in edition 2024 (other threads may read
  the environment): pass a child its variables with `Command::env`.
- Files get the requested mode minus the umask (usually 022). Secrets:
  `0o600` files in a `0o700` directory, set at creation
  (`OpenOptionsExt::mode(0o600)`), not by `chmod` afterwards. Nothing
  world-writable; refuse a secrets file others can read, as ssh does.
- In shared directories create with `create_new(true)` (`O_EXCL`) so a
  planted symlink cannot redirect the write. Rust opens descriptors
  close-on-exec; in C pass `O_CLOEXEC` and `SOCK_CLOEXEC`.

## 9. Paths and encodings

- Paths are OS strings, not text: `PathBuf` and `OsString` (Unix paths are
  bytes, Windows paths possibly ill-formed UTF-16), `std::filesystem::path`
  in C++. Show with `display()`; `to_str()` only where UTF-8 is required.
- Build with `join`, never `format!("{dir}/{name}")`. `join` with an
  absolute path replaces the base (`Path::new("/srv").join("/etc/passwd")`
  is `/etc/passwd`): reject absolute user-supplied names and `..`
  components (`Component::ParentDir`) first.
- Windows: `\` separators, drive letters, `\\?\` and UNC prefixes, a
  260-character limit unless long paths are enabled, reserved names
  (`CON`, `NUL`, `COM1`). macOS and Windows are case-insensitive by
  default: `README.md` and `readme.md` are one file there.
- `fs::canonicalize` resolves symlinks but returns `\\?\C:\` paths on
  Windows that other tools reject: `dunce::canonicalize`. Check
  containment after canonicalising, and open once rather than check then
  open (TOCTOU).
- Temporary files through `tempfile` (deleted on drop), never a fixed name
  in `/tmp`; config and data in the platform's directories (`directories`).

## 10. Time

- Durations, timeouts, rate limits and retries use the monotonic clock
  (`Instant`, `CLOCK_MONOTONIC`, `steady_clock`), which never jumps back.
  Timestamps use the wall clock (`SystemTime`), stored in UTC and zoned
  only for display (`jiff` or `chrono`); NTP and people move it.
- Compute a deadline once (`let deadline = Instant::now() + timeout;`) and
  give each wait the remaining time, so retries cannot stretch it.

## 11. Sockets

- Every connect, read and write has a timeout: resolve with
  `to_socket_addrs()`, then `TcpStream::connect_timeout(&addr,
  Duration::from_secs(5))` per address, `set_read_timeout`,
  `set_write_timeout`; in async code `tokio::time::timeout` on each step.
- `set_nodelay(true)` for request-response protocols (Nagle plus delayed
  ACKs add 40 to 200ms); leave it off for bulk streams.
- std's `TcpListener::bind` sets `SO_REUSEADDR` on Unix and a backlog of
  128; `socket2` for `SO_REUSEPORT`, keepalive and buffer sizes.
- A read of 0 bytes is end of stream; a reset is an error. Frame the
  protocol (`systems-formats`, section 7).

## 12. Resource limits

- Open files: the soft limit is often 1024 on Linux and 256 by default on
  macOS. Servers raise it to the hard limit at startup
  (`setrlimit(RLIMIT_NOFILE)`) or set `LimitNOFILE=` in the systemd unit.
- `EMFILE` under steady load is usually a descriptor leak: watch
  `ls /proc/<pid>/fd | wc -l` or `lsof -p <pid>` over time. Other limits
  that bite: `ulimit -s`, processes per user, inotify watches.

## 13. Command-line conventions

- `--help`/`-h`, `--version`/`-V`, subcommands for distinct actions, `--`
  to end options, kebab-case long flags, `-q` and repeatable `-v`.
- Errors to stderr as `mytool: cannot read config.toml: permission
  denied`, with a hint when there is one; exit codes as in section 5.
- clap derive; `env = "..."` (feature `env`) ties a flag to a variable;
  `clap_complete` generates shell completions:

```rust
#[derive(clap::Parser)]
#[command(version, about)]
struct Cli {
    /// Config file (default: the platform's config directory)
    #[arg(long, env = "MYTOOL_CONFIG")]
    config: Option<PathBuf>,
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
    #[command(subcommand)]
    command: Command,
}
```

## Check it

- Kill the process mid-write (`kill -9` in a loop in a test script): the
  file is always the old or the new version.
- `timeout -s TERM 5 ./app` or `docker stop`: in-flight work finishes,
  exit code 0, inside the deadline.
- `./app | head -1` exits quietly; `./app > out.txt` and `NO_COLOR=1 ./app`
  print no colour codes; a path with spaces and non-ASCII works.
- CI runs the tests on Linux, macOS and Windows (paths, line endings,
  permissions and signals differ); say which could not be tested here.

## Avoid

Writing over a file in place; a temp file on another file system; no
directory fsync; retrying a failed fsync; lock files without a lock; shell
strings for commands; one pipe drained before the other; unwaited
children; no SIGTERM handling; work inside signal handlers; logs on
stdout; colour into pipes; `set_var` at run time; paths as `String` or
glued with `/`; wall-clock time for durations; sockets without timeouts;
secrets in logs or world-readable files.
