---
name: unix-socket-essentials
description: Use when building local IPC over Unix domain sockets — choosing UDS over TCP, filesystem security, Claude Code sandbox fallback to TCP loopback.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: protocol
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [rest-essentials, websocket-essentials, security]
---

# Unix Socket Essentials

**Iron Law: faster + more secure than TCP for local IPC. But Claude Code sandbox blocks UDS — fall back to TCP loopback.**

## Why UDS beats TCP for local IPC

| Property                           | UDS                                          | TCP loopback (127.0.0.1)             |
| ---------------------------------- | -------------------------------------------- | ------------------------------------ |
| Bytes through kernel network stack | No (skips IP/TCP)                            | Yes                                  |
| Throughput on small messages       | ~2×                                          | baseline                             |
| Latency on small messages          | ~30–50% lower                                | baseline                             |
| Discoverable via `netstat -p`      | No                                           | Yes                                  |
| Routable from off-host             | Never                                        | If 127.0.0.1 binding fails open, yes |
| Auth via filesystem perms          | Yes (`chmod 0660`, dir perms)                | No (anyone on host can connect)      |
| Auth via peer credentials          | `SO_PEERCRED` / `getsockopt(LOCAL_PEERCRED)` | No                                   |
| Survives container boundaries      | Only via shared bind mount                   | Yes (port forward)                   |
| Survives `sudo` / namespaces       | Filesystem rules apply                       | Network namespace rules apply        |

UDS wins on three axes: faster, smaller attack surface (not on the network), and OS-enforced access control via filesystem perms.

## The basic shape

```python
# Server
import socket, os
SOCK = "/run/myapp/api.sock"
os.makedirs(os.path.dirname(SOCK), exist_ok=True)
try: os.unlink(SOCK)             # clean stale file
except FileNotFoundError: pass

srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
srv.bind(SOCK)
os.chmod(SOCK, 0o660)            # owner+group RW only
srv.listen(64)

# Client
cli = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
cli.connect(SOCK)
```

```go
// Server
_ = os.Remove("/run/myapp/api.sock")
l, err := net.Listen("unix", "/run/myapp/api.sock")
_ = os.Chmod("/run/myapp/api.sock", 0o660)
```

**SOCK_STREAM = TCP-like (ordered, reliable). SOCK_DGRAM = UDP-like.** Use STREAM unless you have a specific reason.

## Security model

The socket is a **file**. Treat it like one.

```
drwxrws--- 2 myapp myapp 60 /run/myapp/    # dir perms gate listing
srw-rw---- 1 myapp myapp  0 /run/myapp/api.sock
```

- Directory perms restrict **who can find the socket** (no x → no traversal).
- File perms restrict **who can connect**. `0o660` = owner & group only.
- `chown` to a dedicated service user, add legitimate clients to its group.
- **Don't `chmod 0o666`.** That's `0.0.0.0:80` for your local box — every process on the host can connect.
- Use `SO_PEERCRED` (Linux) / `LOCAL_PEERCRED` (BSD/macOS) to authenticate the calling UID/PID/GID at accept time:

```go
// Linux only
ucred, err := syscall.GetsockoptUcred(int(fd), syscall.SOL_SOCKET, syscall.SO_PEERCRED)
// ucred.Uid is the connecting process's UID — trust nothing else
```

This is **stronger than TCP-loopback auth** because there isn't one — anyone on the box can hit 127.0.0.1.

**TOCTOU on stale-file cleanup**: the `unlink`-then-`bind` sequence has a window. On a world-writable parent (`/tmp`) a competing process can `bind` the path between your `unlink` and `bind` → either you get `EADDRINUSE` and silently fall back to TCP (your server runs on a random port the clients don't know about), or worse, an attacker bound a socket clients connect to instead of yours. The `/run/myapp/` + `0o700` directory permission above is what closes this race — only the owning user can create files there, so the window has no exploitable participant. Never put production sockets in `/tmp`.

## Abstract namespace (Linux)

Prefix the path with `\0`:

```python
srv.bind("\0myapp.api")     # no file on disk
```

Pros: no stale file cleanup, no perm dance, instance-private namespace.
Cons: Linux-only, no filesystem perms (anyone in the same network namespace can connect), invisible to standard tools.

Filesystem sockets are the right default unless you need the abstract namespace's lifecycle.

## Claude Code sandbox — and the loopback fallback

**The Claude Code sandbox blocks `AF_UNIX` `bind()`/`connect()` outside an explicit allowlist.** You'll see `Permission denied` or `Operation not permitted` even though the path is writable. The sandbox's network policy treats UDS as network I/O.

**Fallback pattern:** auto-detect and prefer UDS in production, TCP loopback in development/sandboxed environments.

```python
def listen():
    # Prefer $XDG_RUNTIME_DIR (per-user) over /run/myapp (needs systemd-tmpfiles or root)
    runtime = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
    sock_path = os.environ.get("APP_SOCK", f"{runtime}/myapp.sock")
    try:
        try: os.unlink(sock_path)                            # stale socket from prior crash (race-safe)
    except FileNotFoundError: pass
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(sock_path)
        os.chmod(sock_path, 0o660)
        srv.listen(64)
        return srv, f"unix://{sock_path}"
    except (PermissionError, OSError):                       # sandbox or unsupported FS — fall back
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", 0))                           # 0 = OS-assigned port
        srv.listen(64)                                       # REQUIRED on both paths or accept() fails
        return srv, f"tcp://127.0.0.1:{srv.getsockname()[1]}"
```

Document both modes in a `transport=` env var so it's not magical:

```
APP_TRANSPORT=unix:///run/myapp/api.sock     # prod, container with bind mount
APP_TRANSPORT=tcp://127.0.0.1:9876            # dev, sandbox
```

| Tradeoff                         | UDS                               | TCP loopback                       |
| -------------------------------- | --------------------------------- | ---------------------------------- |
| Sandbox-compatible               | No                                | Yes                                |
| Filesystem-perm auth             | Yes                               | No (any local process can connect) |
| Visible in `lsof -i`             | No                                | Yes                                |
| Survives process restart cleanly | Stale `.sock` file unless removed | Port may be in TIME_WAIT           |
| Performance                      | Faster                            | Slightly slower                    |

When you fall back to TCP, **bind to `127.0.0.1` only** — never `0.0.0.0`. Verify with `ss -lntp` post-bind in dev.

## Anti-patterns

- `chmod 0o666` on the socket file — public local IPC
- Forgetting to `unlink` stale socket files on restart → bind fails with `EADDRINUSE`
- Hard-coding UDS with no fallback → breaks in sandbox/Windows/containers without bind mount
- Binding TCP fallback to `0.0.0.0` instead of `127.0.0.1` → accidentally network-exposed
- Trusting client identity over UDS without `SO_PEERCRED` — anyone in the group can lie about who they are
- Putting the socket in `/tmp` on a multi-tenant host (`/tmp/myapp.sock` is world-writable parent)
- Mixing UDS and TCP listeners on the same connection without a transport prefix in URIs

## Red flags

| Thought                                  | Reality                                                            |
| ---------------------------------------- | ------------------------------------------------------------------ |
| "UDS is too obscure"                     | It's how nginx talks to PHP-FPM, Docker daemon, systemd. Standard. |
| "127.0.0.1 is local-only, that's enough" | Any local process can connect. Adversarial multi-tenant says hi.   |
| "Sandbox should support UDS"             | It doesn't. Build the fallback first; you'll need it.              |
| "We can skip the stale-file cleanup"     | First crash leaves the file; next start `EADDRINUSE`.              |

## Hand-off

For HTTP-over-UDS specifically (nginx → app): the UDS is transport; the protocol on top is still REST — see `Skill(rest-essentials)`. For WS over UDS: `Skill(websocket-essentials)`. For filesystem perm review: `Skill(security)`.
