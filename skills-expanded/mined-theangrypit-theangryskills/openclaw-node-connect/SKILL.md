---
name: openclaw-node-connect
description: "Use when explicitly asked to repair one exact OpenClaw browser or native-node connection, including auth, Tailscale routing or pairing."
---

# Node Connect

Codex adaptation of the pinned OpenClaw source. Explicit operator selection is required for live update/connection actions.

## Lock the client and Gateway
Read the selected deployment owner and record client type, host/profile/state root, binary, Gateway URL/listener and service. Distinguish Control UI/browser from a native mobile/node using the actual request/logs; a phone can be either. Read the packaged source for routing/auth/pairing branches and evidence conditions.

Observe a fresh failing attempt and correlate exact timestamps, client/account/device identity and logs. A `client connected` record must be matched by `conn`, `client`, `mode` and `role`; admission precedes the hello response. If it is followed by `1006`, inspect hello delivery, lifecycle, transport, proxy or reconnect. Older `authenticated user connected` and `webchat connected` records can overlap and omit ephemeral clients. A `1006` without a matching application-level admission record does not prove auth or pairing succeeded. Inspect actual Tailscale/Serve routes when authorized; `gateway.tailscale.mode=off` does not prove an externally managed route is absent. Do not reset pairing or change auth because a connectivity probe passed.

For browsers, establish route and intended authentication before expecting pairing. For native clients, resolve the exact node setup route and never put password-equivalent setup codes, signed handoff URLs or permanent credentials into chat/tool output. Let the operator handle credential entry through the established trusted surface. No account/auth-policy change is authorized by installation of this skill.

Approve a device only when the task/confirmation authorizes that exact access change, and correlate the current request ID immediately before acting. `devices approve --latest` is a preview, not approval; a verified Tailscale browser can legitimately have no pairing row. Preserve permissions and the existing route after reconnect errors and investigate current evidence.

After an authorized repair, require a new client attempt proving intended route/auth and initial browser requests or native node presence, with no immediate reconnect/auth failure. Report each transition separately. QR creation, ping, approval or a paired-device count alone is not a working connection.

## Selective installation

No mandatory installed companion from this pack is required. Checkout/runtime prerequisites and the conditional source references still apply.

## Source procedures and boundary

Read [the packaged upstream entrypoint](references/upstream/SKILL.source.md) when using this workflow; its supporting files remain beside it. This root owns Codex invocation, target resolution and authorization. Upstream examples are reference procedures, not grants of access, installation, deployment, publication or another model/provider. Use native Codex tools where capable and preserve an actual refusal. The operator's chosen model, project instructions and source-trust policy remain authoritative.

For repository-owned dependencies and original relative links, use [the source link map](references/upstream-link-map.json) against the verified checkout or its pinned GitHub reference. The pack does not claim that a linked release/channel skill or runtime is installed. Inspect the current owning source before executing a version-sensitive example.

[Provenance and adaptation record](PROVENANCE.md) identifies the source commit, retained resources and changes.
