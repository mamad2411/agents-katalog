---
name: strawberry-reach
description: >
  Reach a Gorshok-v4 board on the LAN and establish an authenticated session: discover
  candidates by WS probe (firmware has NO mDNS), confirm the target by MAC (DHCP drifts),
  perform the HMAC challenge-response login, and persist the returned token to a
  0600 FileTokenStore so the session resumes across reboots. The mandatory first step every
  other board skill depends on. Use when asked to find/reach/connect to a board, log in,
  authenticate, or establish a session before any other board operation.
---

# strawberry-reach — find a board, log in, keep the session

The mandatory first step for every other board skill. It produces two things the rest of the
flow consumes:

- **`$HOST`** — the `ws://<ip>/ws` of the confirmed target board.
- **a 0600 token file** — a HMAC session token that later steps replay with `auth resume`
  to ride out the reboots that OTA and flag changes cause.

Everything below drives `strawberry-cli`, the thin front end over the shared
`@avatarsd-llc/strawberry-client` library (the one WS+protobuf core). Do not hand-roll the
wire protocol or the HMAC — the CLI already is that code.

## Contract

- **Input:**
  - how to reach the board: a known IP, **and/or** a `--cidr` to scan, **and/or** a `--mac` to
    confirm the right one (e.g. `aa:bb:cc:dd:ee:ff`);
  - the board's password, supplied as a `--password-file <f>` or via `$STRAWBERRY_PASSWORD`
    (never inline on the command line — it lands in shell history).
- **Output:** a confirmed `$HOST` and a token file written mode **0600**, with `auth resume`
  proven to work against it.
- **Non-negotiables:**
  - Locate the board **by MAC** — DHCP leases drift, and a stale IP looks like a crash but isn't.
  - The firmware ships **no mDNS** — discovery is WS-probing candidate IPs, not a name lookup.
  - **HMAC only** — the plaintext password never crosses the wire. The CLI sends
    `HMAC-SHA256(password, server-nonce)` (pure-JS, because `crypto.subtle` is undefined over
    plain http).
  - Token file mode **0600** — it is a bearer credential.
  - Keep WS clients **<= 2** at a time (the C6 httpd wedges with more); this skill uses one.

## Step 0 — learn the vocabulary, do not guess it

The CLI command tree is generated from the library's live protobuf enums, so it is the board's
*provable* vocabulary. Read it before anything else and take flag/verb names from it, not from
memory:

```bash
strawberry help --json
```

If a command or flag named below is absent from `help --json`, trust `help --json` — the CLI is
the source of truth, this document is a playbook over it.

## Step 1 — discover the board on the LAN

The firmware has no mDNS, so discovery means WS-probing candidate IPs. Each reachable candidate is
opened, queried for `WHAT_CAPABILITIES` (-> `Capabilities`) and `WHAT_WIFI` (-> `WifiState`), and
reported as `ip / mac / board_rev`.

```bash
# Scan a subnet and confirm the one board you want by MAC:
strawberry discover --cidr 192.0.2.0/24 --mac aa:bb:cc:dd:ee:ff --json
```

Variations:

```bash
strawberry discover --cidr 192.0.2.0/24 --json     # enumerate every reachable board on the subnet
strawberry discover --mac aa:bb:cc:dd:ee:ff --json # confirm a board whose IP you already think you know
```

**Disambiguate by MAC, always.** If the scan returns several rows, the target is the one whose
`mac` equals the label/known MAC — its `ip` may have moved since last session. Capture that row's
`ip` into `$HOST`:

```bash
# Pin the confirmed target for every later command. Example value:
HOST=ws://192.0.2.177/ws
```

`--host` accepts a bare host (`192.0.2.177`), `host:port`, or a full `ws(s)://.../ws` URL; the CLI
normalizes it (`DeviceClient.forWsHost`). Using the full `ws://<ip>/ws` form is the least
ambiguous.

**Fresh board only in SoftAP?** A factory board with no Wi-Fi creds brings up its own AP. Join that
AP from the host machine first, then `discover` on the SoftAP subnet (commonly `192.168.4.0/24`).
The QR claim handshake is **design-only** — there is no claim wire surface on the firmware
yet, so today this is just "join the AP, then proceed as normal".

**Gate to clear:** exactly one candidate whose `mac` matches the target; `$HOST` set to its
`ws://<ip>/ws`.

## Step 2 — HMAC login (plaintext never crosses the wire)

Log in with the challenge-response handshake and persist the returned token. The CLI performs the
full HMAC exchange for you:

1. `AuthChallengeReq` -> `AuthChallenge{nonce}` (a single-use server nonce),
2. compute `HMAC-SHA256(password, nonce)` locally (pure-JS), send only the digest in
   `AuthLogin{hmac, desiredTtlMs}` with `password: ''`,
3. `AuthOk{token, ttl_ms, server_now_ms}` — adopt the token; the CLI also records
   `bootOffsetMs = Date.now() - server_now_ms` so monotonic `ts_ms` push timestamps map to
   wall-clock.

```bash
# Password from a file (preferred — keeps the secret out of shell history):
strawberry auth login \
  --host "$HOST" \
  --password-file ./board.pass \
  --token-file ./board.token \
  --ttl-ms 86400000 \
  --json
```

```bash
# Or password from the environment (also kept off the command line):
export STRAWBERRY_PASSWORD='...'   # set without leaving it in history (e.g. read -s)
strawberry auth login --host "$HOST" --token-file ./board.token --json
```

`--ttl-ms` is the desired session lifetime (the server clamps it); a day is a reasonable default
for a bring-up that includes reboots. Omit it to take the firmware default.

**Lock down the token file** — it is a bearer credential. The CLI writes the `FileTokenStore`
0600, but verify it:

```bash
chmod 600 ./board.token
ls -l ./board.token   # expect -rw------- ...
```

**Gate to clear:** `auth login --json` reports an `AuthOk` (a token and a non-zero `ttl_ms`); the
token file exists and is mode `0600`.

## Step 3 — confirm capabilities (scope every later step to real hardware)

With a session up, read what the board actually is, so downstream skills skip hardware the board
lacks:

```bash
strawberry query capabilities --host "$HOST" --json   # board_rev, display_kind, zigbee/modbus/sd/flow/analog presence
strawberry query wifi         --host "$HOST" --json   # current Wi-Fi state + LAN IP (confirms reachability)
```

`query capabilities` -> `Capabilities`; `query wifi` -> `WifiState`. Record both — `strawberry-board`
and `strawberry-config` gate their steps on the capability flags (e.g. don't toggle Zigbee on a board
whose `zigbee_supported` is false).

**Gate to clear:** a `Capabilities` snapshot and a `WifiState` recorded; reachability re-confirmed
over the authenticated socket.

## Step 4 — prove the session resumes (so later reboots are survivable)

OTA and subsystem-flag changes reboot the unit. Resuming a stored token across the reconnect is
how every later skill stays authenticated without re-prompting for the password. Prove it works
**now**, while nothing is broken:

```bash
strawberry auth resume --host "$HOST" --token-file ./board.token --json
```

This replays the token (`AuthResume{token}` -> `AuthOk` on success). If the firmware has rebooted
and the token is still valid, this re-establishes the session and re-records `bootOffsetMs`.

If the token has expired, the firmware answers `error ERR_AUTH_EXPIRED`; the CLI clears the stored
token. In that case fall back to a fresh `auth login` (Step 2).

**Gate to clear:** `auth resume` returns `AuthOk` against the stored token. The session is now
resumable; hand `$HOST` and `./board.token` to the next skill.

## Verifying success (end-to-end)

A one-shot check you have a working, resumable, authenticated session:

```bash
./scripts/verify-session.sh "$HOST" ./board.token
# or inline:
strawberry auth resume --host "$HOST" --token-file ./board.token --json \
  && strawberry query capabilities --host "$HOST" --json
```

Success looks like: `discover` confirmed the target by MAC; `auth login` returned an `AuthOk` and
wrote a 0600 token; `query capabilities` returns a board snapshot; `auth resume` re-authenticates
from the stored token. If `query capabilities` errors with an auth code, the session was not
actually established — go back to Step 2.

## Cleanup / rollback

- **End of a one-off session** (revoke the token server-side so a leaked file is useless):

  ```bash
  strawberry auth revoke --host "$HOST" --token-file ./board.token --json
  rm -f ./board.token
  ```

  `auth revoke` sends `AuthRevoke{token}` -> `Ack`; the firmware invalidates that token. **Do
  this only when you are done** — later skills in the same bring-up need the token to resume.

- **Stale / rejected token** (`ERR_AUTH_EXPIRED` on resume): delete the file and re-`auth login`.

  ```bash
  rm -f ./board.token
  ```

- **Nothing this skill does is destructive to the board** — no reboot, no NVS write, no factory
  state change. It only opens a socket, authenticates, and reads. There is no board-side rollback
  to perform; cleanup is purely local (token file) plus the optional `auth revoke`.

## What this supersedes

The `_login()` / `ws_authenticate()` HMAC handshake helper that was copy-pasted across
`strawberry-fw/tools/ota_check.py`, `verify_grow.py`, `verify_orphans.py`, and `wg_provision.py`.
Those re-login every run and have no token persistence; this skill establishes one resumable
session over the shared library's single HMAC implementation.

## Hand-off to the next skill

Downstream skills (`strawberry-provision`, `strawberry-flash`, `strawberry-config`, `strawberry-unit`,
`strawberry-diagnose`) each take the same two values:

- `--host "$HOST"`
- `--token-file ./board.token`

and call `auth resume` first if they were invoked after a reboot. If Wi-Fi provisioning moves the
board off SoftAP, its DHCP IP changes — **re-run `discover --mac` and update `$HOST`** before the
next command.

## See also

- Orchestrator: `strawberry-board` (sequences this skill first).
- Index + ground rules: `skills/README.md`.
- Library: `@avatarsd-llc/strawberry-client` — the WS+protobuf core the CLI is built on. The HMAC handshake this skill drives is
  `ws.service.ts login()/tryResume()/logout()` ported framework-free.
