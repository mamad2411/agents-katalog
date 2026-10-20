---
name: security-core
description: "Shared reference for the security cluster: the trust-boundary model (untrusted input/action → privileged sink), the defend-vs-attack × code/config/runtime surface map, severity & exploitability conventions, and the tooling matrix every security spoke shares. USE WHEN triaging a finding, judging whether something is exploitable, or deciding which control to apply — the interlocking rules behind all six spokes."
cluster: security
version: 1.0.0
---

# Security Core

Shared model for the `security` cluster. The review, hunting, scanning, and guard spokes all
turn on the same one idea — keep it consistent here so no spoke contradicts another.

## 1. The decision this cluster turns on: the trust boundary

Every security question reduces to one thing: **can attacker-controlled input or action reach a
privileged sink, and what contains it?**

```
Untrusted source ──reaches──> Sink (privileged effect) ──contained by──> Control (default-deny)
   user input / network /         filesystem, exec, SQL,           capability, scope, allowlist,
   webview / agent prompt         secrets, deploy, money           gate, freeze
```

- A **finding is real** only when a path connects an untrusted source to a meaningful sink. No reachable path → informational, not exploitable. This is the line `security-bounty-hunter` draws and the lens `security-review` reviews against.
- A **control is sound** when it is **default-deny**: the narrowest grant that still works, with any widening (new host, new path, new permission, a disabled gate) treated as a stated security change — never silent. This is what `security-scan`, `gateguard`, and `safety-guard` enforce.

Everything below is an application of this one model to a different surface.

## 2. The surface map (posture × surface)

|  | **Defend** (prevent) | **Attack** (discover) |
|---|---|---|
| **Code** | `security-review` | `security-bounty-hunter` |
| **Agent config** (`.claude/`) | `security-scan` | — *(audit findings feed back to review)* |
| **Source tree / supply chain** | `repo-scan` | `repo-scan` (embedded-dep CVEs) |
| **Live runtime** (agent actions) | `gateguard`, `safety-guard` | — |

Pick the cell, not just the keyword. "Secure my agent project" spans the config row
(`security-scan`) and the code row (`security-review`); a full-auto run also needs the runtime
row (`safety-guard`).

## 3. Severity & exploitability conventions

Rank every finding the same way, so spokes agree:

- **In-scope, high-signal** — reachable from a real user/network boundary, input genuinely user-controlled, sink meaningful (RCE, auth bypass, SSRF→metadata, SQLi, path traversal, auto-triggered XSS, leaked secret, destructive op). Map to a CWE where possible.
- **Out-of-scope / low-signal** — local-only `pickle`/`torch.load`, `eval` in CLI-only tooling, `shell=True` on hardcoded commands, missing-header-only, generic rate-limit gripes, self-XSS, demo/test/fixture code. Drop unless the program scope says otherwise.
- **Static tooling is triage input, not a verdict.** A scanner hit is a lead; confirm the path end-to-end and the smallest safe PoC before it counts.

## 4. Shared conventions

- **Secrets** live in env / a secret manager, never in source; verify presence at startup; redact in logs and in any schema you display.
- **Validate at the boundary** — never trust the client/webview/prompt; validate on the privileged side.
- **State every grant** — a new permission, scope path, allowed host, or a disabled gate is a decision worth naming in the output.
- **Reachability before refactor** — for `repo-scan`, an outdated *vendored* dependency is only urgent if it sits on a reachable path; classify ownership first.
- **Reports are reproducible** — pin the version/commit tested, give file:line, and a minimal PoC (offensive) or a concrete fix (defensive).

## 5. Tooling matrix

| Surface | Spoke | Primary tooling | Mechanism |
|---|---|---|---|
| Code (defend) | `security-review` | manual checklist + grep/read | review-time |
| Code (attack) | `security-bounty-hunter` | `semgrep --config=auto` (triage) + manual path proof | discovery |
| Agent config | `security-scan` | `ecc-agentshield` (`scan`, `--fix`, `--format json/html`, CI action) | static + optional adversarial pass |
| Source tree | `repo-scan` | cross-stack classifier (`fast`/`standard`/`deep`/`full`) | inventory + verdicts |
| Runtime (investigate) | `gateguard` | PreToolUse hook (deny → force → allow) | fact-forcing gate |
| Runtime (contain) | `safety-guard` | PreToolUse hook (careful / freeze / guard modes) | destructive-op + write lock |

Hooks (`gateguard`, `safety-guard`) are PreToolUse-based and intercept Bash/Write/Edit/MultiEdit;
both expose an off switch and log blocked actions — keep them on for autonomous sessions.

## 6. Shared guardrails

- **Default-deny**: narrowest permission/scope/allowlist that works; per-target over global.
- **Exploitability over theory**: rank by reachable-source → meaningful-sink, not pattern count; drop local-only and out-of-scope noise.
- **Boundary is sacred**: validate all input on the trusted side; the client/webview/prompt is untrusted.
- **No silent weakening**: disabling a gate, widening a scope, or adding a host is a stated change.
- **Contain first in autonomy**: `gateguard` to force investigation, `safety-guard` to cap blast radius, before granting broad write/exec.
- **Reproducible findings**: pin version/commit, give file:line, and a minimal PoC or concrete fix.
