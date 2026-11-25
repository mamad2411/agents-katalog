---
name: thick-client-testing
description: Methodology for assessing thick / desktop client applications (native, .NET, Java, Electron) — surface mapping, proxy-aware and non-HTTP traffic interception, local storage and secrets, memory and binary analysis, DLL hijacking, IPC, and client-side trust. Use when the target is an installed desktop client rather than a web or mobile app.
metadata:
  domain: offensive-security
  standards: "OWASP Top 10:2025, WSTG (adapted), CWE"
  tier: spine
---

# thick client testing

thick clients split logic between the client and one or more backends. the
recurring flaw is *client-side trust*: controls enforced only in the client are
bypassable. there is no single OWASP list here — adapt WSTG/Top 10 to a desktop
surface. work these axes:

## 1. identify & map

- platform/framework: native (c/c++), **.NET** (decompile with ilspy/dnSpy),
  **Java** (jar/jd), **Electron** (asar → js), or packed. note language, arch,
  and installer artifacts.
- transports: http/https, soap/wcf, grpc, raw tcp/udp, websockets, message
  queues, database-direct. list every channel and endpoint.
- entry points: config files, cli args, registry, env, files it reads/writes.

## 2. traffic interception

- **proxy-aware (http/soap/grpc):** route through an intercepting proxy; handle
  pinning by patching or system trust. capture and replay like a web api → apply
  `owasp-api-top-10`.
- **non-http / raw sockets:** use a transparent/tcp proxy or a network hook;
  many thick clients speak custom binary protocols — capture, understand the
  framing, then tamper.

## 3. local storage & secrets

config files, registry keys, sqlite/embedded db, cached credentials, tokens,
license data. check for cleartext secrets, weak DPAPI/keychain usage, and
world-readable install paths. (→ A04 crypto, M9-style storage.)

## 4. binary & memory

- static: decompile managed binaries; look for hardcoded keys/urls, feature
  flags, and client-side authz checks to bypass.
- dynamic: attach a debugger / frida; read secrets from memory, patch checks
  (license, role, "is-admin"), and observe crypto in use.

## 5. dll hijacking & side-loading

enumerate the app's dll search order and missing/relative-path loads; a
writable directory in the search path enables code execution and persistence.

## 6. ipc & privilege

named pipes, com/dcom, local services, shared memory, custom local sockets. test
for unauthenticated or spoofable ipc and for a low-priv client driving a
high-priv service (privilege escalation → A01).

## 7. server-side trust

replay every client action directly against the backend with a low-privilege or
other-user identity — the differential-across-identities test. controls the
client "enforces" often are not enforced server-side (A01 broken access control,
API1/API5).

## driving it in farai

- do binary triage and decompilation in the container/shell; use the `command_*`
  tools and search for the right cli (`kali_search`) — delegate the static pass
  as a subagent.
- treat captured backend traffic as an api engagement (`owasp-api-top-10`).
- classify findings against OWASP Top 10:2025 (A01 trust/authz, A02 config, A04
  crypto, A08 integrity) and cite CWE ids; keep exact evidence (decompiled
  snippet, captured frame, memory dump excerpt) and a reproduction.
