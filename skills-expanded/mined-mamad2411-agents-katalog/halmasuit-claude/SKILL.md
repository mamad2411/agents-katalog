# halmasuit — Claude instructions

Project-specific guidance. The global `~/.claude/CLAUDE.md` preferences
still apply (terse, no `_v2` suffixes, fix all lints in one pass, etc.).

## What this project is

A Linux **system compositor**: one long-lived display-server process owning
the GPU from `graphical.target` to shutdown, hosting the greeter and the
user session as nested Wayland clients of itself. Replaces greetd entirely.
Eliminates the visible black flash that exists today between greeter and
session on every greetd-based Linux desktop.

Read **`ARCHITECTURE.md`** for the design, threat model, and roadmap.
Read **`RESEARCH.md`** for the empirically validated architectural
foundations (drm-master-probe Phase 0 + Phase 1).

The terms `v1`, `v2`, `v3`, `v4`, `v5+` in this repo always refer to the
roadmap milestones in `ARCHITECTURE.md`, not crate versions.

## Where the project is

The compositor exists and is the live system. The privileged
`halmasuit-session` broker is the live auth/session path; the compositor
is an unprivileged sans-IO relay to it; the in-compositor `halmasuit-pam`
and the setuid `halmasuit-spawn` helper are deleted (single libpam
surface = `halmasuit-session`; no setuid inode in the closure).
`login-flash` passes through the broker-launched session — PID and frame
continuity hold across the real greeter→session transition. The
assertion is never modified to pass; the system under test changes, the
assertion does not.

## Hard rules

These are anti-patterns codified as Claude rules. Do not relax them
without explicit user direction.

- **`login-flash` is a GREEN hard gate.** It proves halmasuit's PID
  and `assert_no_flash_stream` hold across the real greeter→session
  transition through the broker-launched session — no compositor
  restart, no flash. Never weaken, skip, invert, or conditionalize the
  assertion to keep it green; an unexpected FAIL means the flash
  invariant regressed (the thing this project exists to prevent). The
  CI gate runs it as a normal pass/fail check, never inverted.
- **The privileged surface is the `halmasuit-session` broker.** Every
  change to its privileged boundary is a security-review event —
  surface diffs prominently.
- **`halmasuit-pam` and the setuid `halmasuit-spawn` are DELETED.**
  There is exactly one libpam surface (`halmasuit-session`) and NO
  setuid inode in the closure. Do NOT re-introduce an in-compositor
  PAM path, a setuid spawn helper, a `security.wrappers` setuid entry,
  a second libpam consumer, or `halmasuit-greetd`'s
  `MAX_SESSION_BUILDS_PER_CONNECTION`. Privilege-drop+exec exists ONLY
  in the broker's non-setuid session-leader child (fork-then-drop from
  already-root).
- **The compositor retains zero escalation capability.** After its
  in-process privilege drop the bounding set is emptied entirely; it
  keeps only `CAP_KILL` (to signal its greeter child). Do NOT re-add
  `{CAP_SETUID,CAP_SETGID}` (or anything) to the compositor bounding
  set — it execs no setuid helper, so any retained cap is a
  least-authority regression.
- **UID floor is load-bearing — enforced by the broker's
  session-leader child.** Refuse any `uid`/`gid < UID_MIN` (typically
  1000); reject `(uid_t)-1`/overflow. The broker independently
  re-derives identity from PAM (`pam_get_user` → pwent) and never
  trusts a compositor-asserted identity. This is what makes a
  compromised halmasuit *not* a root compromise. Removing it is
  security theater.
- **Broker SO_PEERCRED authorizes the relay peer, not the greeter.**
  The env var is `HALMASUIT_BROKER_PEER_UID` / `relay_peer_uid`; do
  not rename it back to "greeter" or point the broker gate at the
  greeter uid in the live path.
- **One `pam_handle_t`, never split, owner never `execve`s between
  auth and session.** No two-handle / cross-process-handle design
  (pam_mount/keyring/krb5 silently break — locked `$HOME`, no error).
  The session leader's supplementary groups are
  `getgrouplist(PAM-resolved user, primary gid)` ONLY, derived from
  the PAM-resolved identity — NEVER the privileged broker's own
  `getgroups()` (sourcing the handle-owner's set leaks `shadow` into
  every session: CVE-2021-41617 / sddm#1159). Its `execve` env is
  `pam_getenvlist()` MERGED with the fixed allowlist, never a blind
  env-replace (clobbers pam_env/pam_systemd/pam_mount).
- **No `start_session` path that bypasses PAM success.** The greetd
  state machine in `halmasuit-greetd` enforces this; never add a code
  path that side-steps it.
- **No PAM in the compositor's address space.** libpam links in
  exactly one crate (`halmasuit-session`); the compositor relays only
  length-bounded conversation frames.
- **The compositor never blocks the render/calloop thread on broker
  IPC.** greetd's PAM boundary is fully sans-IO (emit/suspend/resume);
  the broker fd is a per-connection NON-blocking calloop source. No
  blocking `recv`/`send`-then-`recv`, with or without a timeout; no
  synchronous `PamSession::step`.
- **One per-greeter-episode object owns the broker socket the whole
  episode.** It is the sole `OwnedFd`; the calloop source is a
  `Generic` over a NON-owning borrowed-fd newtype; the source token is
  removed before the episode drops. No `dup`/`Rc`/`Arc` of the broker
  socket, ever (premature-EOF / least-authority;
  CVE-2015-6563/6564).
- **Session lifecycle is one-way broker→compositor.** No
  compositor-emitted lifecycle frame (no such `CompositorToBroker`
  variant — keep it type-impossible). The visible greeter→session swap
  is gated on AND(`SessionOpened`, the compositor's own
  first-non-empty session frame) — never `SessionOpened` alone (that
  reintroduces the flash). The broker is the sole reaper; any
  SCM_RIGHTS leader pidfd the compositor holds is poll-only (never
  waitid/reap/signal); no raw leader pid in any frame.
- **No mocking PAM in VM / integration tests.** Real PAM, real users.
  Unit tests inside `halmasuit-greetd` may mock individual modules.
- **No running the compositor as root.** halmasuit runs as the
  `compositor` system user and holds no handle. The broker is the
  privileged process; it idle-exits (no standing root daemon).
- **No trusting Wayland client PIDs from message contents.** Always
  `SO_PEERCRED` on the socket.
- **No credential material kept past PAM completion.** `zeroize`
  challenge/response buffers immediately.
- **No `--no-verify`, `--no-gpg-sign`, or skipping hooks.** Quality
  gates are non-negotiable.

## Working conventions

- **Entry point: `just`.** `just check` = `lint test` (rustfmt + clippy
  `-D warnings` + cargo-deny + cargo-machete + typos + nextest). Run
  this before reporting success, per the user's global workflow rule.
- **VM tests: `just test-vm`** runs the full headless gate.
  `just test-vm-drive <name>` opens an interactive QEMU window driven
  via a FIFO command file — use this when debugging a VM test, not
  bare `nix build`. The drive shape is documented inline in the
  `Justfile`.
- **Test cost discipline.** `just check` (fast, ~30s, covers lints +
  every unit test) is the iteration loop; `just test-vm` (slow, ~3-4
  min per single test on a warm cache, longer for the full sweep) is
  the comprehensive sweep and is run ONLY at task boundaries — never
  as the inner loop for "does this change still work." The full
  `just test-vm` sweep must keep covering as much of halmasuit's
  surface as possible (every observable behavior worth a regression
  gate gets a VM test), AND no individual change should trigger more
  than one sweep — if you need to iterate, iterate on `just check` /
  `cargo build` / a single targeted VM test, then run the full sweep
  once when the change is settled. New per-protocol / per-contract
  tests belong as targeted VM tests on the existing
  `tests/visual-*.nix` pattern; new pure-Rust invariants belong as
  unit tests in the relevant crate.
- **TDD loop for compositor changes.** RED via the targeted VM test
  is the right shape when the contract is protocol-observable
  (xdg-shell configure timing, wl_surface.frame callbacks, etc.) —
  drive it with a focused raw-protocol test client and assert via
  introspection events / journal markers. Avoid using the full
  `just test-vm` sweep as the RED-GREEN-loop signal; reserve it for
  the regression sweep after the targeted test is green.
- **Workspace lints live in `[workspace.lints]`.** Add per-crate
  `#![allow]` only with a `// reason: …` comment justifying it; do not
  add per-crate lint overrides in `Cargo.toml` to silence noise. The
  bar for an allow is "this lint flags a genuine false positive on
  this exact code, and the cost of restructuring exceeds the value of
  the rule" — convenience under deadline doesn't clear it. Default is
  to restructure; `try_from` over `as`, dedicated unit-state patterns
  over `_`, extracted helpers over `too_many_lines` allows. If
  reaching for an `#![allow]`, ask the user first — they're a
  judgment call that survives the immediate task.
- **Edition 2024, Rust 1.95 pin** (see `rust-toolchain.toml`). Don't
  bump the channel without coordinating; CI caches key on it.
- **Cargo workspace, monorepo, atomic commits.** A change touching the
  greetd protocol + the CLI + the IPC types lands in one commit.
- **Test user is `tests/lib/test-user.nix`.** New VM tests import it;
  do not copy-paste the insecure user config.

## Ecosystem caveats

These are the easy traps to fall into when adding real deps:

- **`halmasuit-greetd` owns its wire types locally.** The upstream
  `greetd_ipc` crate is GPL-3.0-only; linking it would force
  halmasuit's binary to GPL, conflicting with the workspace's dual
  MIT-OR-Apache posture (which matches the Rust-Wayland infrastructure
  tier: smithay, wlroots, Weston). The wire types in
  `crates/halmasuit-greetd/src/lib.rs` are a clean-room
  reimplementation derived from the public protocol spec at
  <https://man.sr.ht/~kennylevinsen/greetd/protocol.md>, NOT from
  `greetd_ipc`'s source. Drift mitigation is the
  `wire_format_*` canonical-payload roundtrip tests in that crate —
  they pin the JSON shape against payloads from the spec, so if
  upstream ever changes the format we notice. Reusing
  greetd-the-daemon as a library is also not feasible (incompatible
  privilege model: greetd runs as root and `execve`s; halmasuit is
  unprivileged and never execs).
- **smithay** — pin to a `git` revision matching niri's or
  cosmic-comp's current pin, never crates.io 0.7.0 (June 2024,
  pre-DnD-refactor, pre-`delegate_dispatch2!`). Standard
  smithay-downstream pattern.
- **PAM bindings** — hand-rolled FFI in
  `crates/halmasuit-session/src/pam_sys.rs`, following sudo-rs's
  pattern (the most security-audited Rust libpam consumer in
  existence). Production halmasuit-session links `-lpam` directly with
  zero bindgen / clang-sys / libclang at build time. The third-party
  `pam-sys` crate is retained as a `[dev-dependencies]` audit lever
  consumed only by `tests/pam_ffi_parity.rs`, which asserts struct
  layouts + constant values + symbol resolution match bindgen's output
  against the build host's libpam headers (libpam ABI drift fails CI
  before the broker hits it). Do not add a second production PAM
  crate; do not introduce a `build.rs` in halmasuit-session.
- **D-Bus** — `zbus` 5.x. Do not pull in glib.
- **wayland-server** + **calloop** are smithay's, follow smithay's
  pin.

## Test-VM rendering gotcha

Headless NixOS VM tests use `virtio-gpu-pci` (no GBM allocator) — niri
runs but paints nothing, screenshots are solid black. PID-tracking still
works, which is enough for v1's flash assertion. Interactive driver mode
swaps to `virtio-vga-gl` + `-display gtk,gl=on` and pixels actually
render. If you need visual frame capture in CI later, you'll need to
either solve the headless GL backend or shell out to a real GPU runner.
Do not pretend the headless screenshots are valid — they are
deliberately not.

## Open decisions

Listed in `ARCHITECTURE.md` § "Open decisions"; the still-open ones:

1. smithay revision pin (see Ecosystem caveats above).
2. OCR for text-leak detection in frame-capture (tesseract).

The `org.halmasuit.Compositor1` D-Bus surface is RESOLVED (Epic #71):
the as-built surface is read-only observability (`GetPhase`,
`GetUptime`, `GetFrameCounter`, `ListWindows`, `GetBrokerStatus`);
mutating control (`Lock`/`Unlock`/`RestartInnerWM`) is deferred to v2+.

Don't invent answers; flag the decision when the relevant code lands.

## CI

GHA on `ubuntu-24.04`, actions pinned to commit SHAs. Consumes (does
not push to) `joshsymonds.cachix.org`. `login-flash` runs as a normal
pass/fail gate; do not introduce `continue-on-error` or any inversion
that turns FAIL into success.

## Where to look

- `RESEARCH.md` — empirically validated architectural foundations.
- `ARCHITECTURE.md` — full design, threat model, roadmap.
- `Justfile` — every command, local and CI.
- `tests/login-flash.nix` — the canonical no-flash gate; reading it
  end-to-end is the fastest way to understand the testing posture.
- `crates/halmasuit-session/src/broker.rs` — the module doc is the
  authoritative description of the privileged PAM/session lifecycle
  (one handle, killable auth fork, fork-then-drop leader, slot-owned
  reaping, relay-peer SO_PEERCRED gate).
- `crates/halmasuit/src/broker_session.rs` — the compositor's
  per-greeter `BrokerEpisode`: owns the broker `SeqpacketChannel`,
  drives the sans-IO greetd machine, relays to the broker.
