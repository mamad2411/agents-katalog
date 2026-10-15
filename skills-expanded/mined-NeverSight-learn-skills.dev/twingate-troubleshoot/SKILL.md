---
name: twingate-troubleshoot
description: >
  Use when the user reports connectivity issues, access failures, DNS resolution problems, or any
  error with Twingate. Activate for: "can't connect", "not working", "resource not found", "access
  denied", DEAD connector, DNS not resolving, device-trust blocks, security policy issues, P2P
  failure, or any Twingate diagnostics. Also activate for symptom-shaped queries: exact client error
  text ("unknown network name", "too many open files", "setup wizard ended prematurely", "unable to
  join network"), OS-specific client bugs on Windows, macOS, Linux (Fedora, Ubuntu, NixOS),
  ChromeOS, or Android Auto; client crashes, freezes, or unresponsiveness; version-specific
  regressions (a specific build misbehaving); TAP/virtual network adapter issues; device posture,
  screen-lock, or disk-encryption failures; third-party AV/EDR/VPN/DNS-filtering conflicts
  (CrowdStrike, Zscaler, Elastic AV, Avast, consumer VPNs); packet capture, system reports,
  client/connector logs; and engaging or escalating to Twingate technical support.
---

## Role

Twingate diagnostics specialist. Owns the six-step decision tree for isolating failures
across the full connection chain: Client → DNS → Controller Auth → Connector → Resource.
When a user reports that something isn't working, this skill finds the broken link
systematically.

## Decisions & Guidelines

Walk the decision tree in order. Stop at the first step that reveals the failure.

**Step 1 — Is the Twingate Client running and authenticated?**
The client must be installed, running, and the user signed in via the IdP. Installation
alone is insufficient. If the client is installed but not signed in, resources will not
appear and DNS will not be intercepted.

**Step 2 — Is the resource visible in the user's resource list?**
If absent: check group membership and device trust policy.
**Device trust failures are silent — the resource disappears with no error message.**

**Step 3 — Is DNS resolving correctly?**
Managed FQDNs should resolve to a Twingate-internal address (the Client uses a
CGNAT-style range — current address space documented in
`references/troubleshooting-overview.md` and `references/dns-failures.md`).
If the response is the real backend IP, the client is not intercepting. If
the response is the Twingate-internal address but the connection still times
out, the DNS layer is healthy — the problem is downstream (Connector or policy).

**Step 4 — Is the Connector ALIVE?**
Check admin console → Remote Networks → Connectors. `DEAD_NO_RELAYS` always
means the connector cannot reach Twingate's control/relay infrastructure —
typically DPI/SSL inspection on `*.twingate.com`, or one of the required
outbound ports being blocked. Read
`skills/twingate-connectors/references/connector-best-practices.md` for the
full network requirements before declaring a root cause.

**Step 5 — Can the Connector reach the Resource?**
Test from the Connector host, not the user's machine. The user's machine cannot directly
reach the backend resource — that is the point of ZTNA.

**Step 6 — Is the Security Policy satisfied?**
Check: device trust enrollment, MFA completion, session expiry, geoblocking, and JIT
approval status.

---

Additional guidelines:

- **Both Connectors DEAD emergency:** Deploy a new Connector from any machine
  with outbound internet access that meets the connector network requirements
  in `skills/twingate-connectors/references/connector-best-practices.md`. You
  do not need an existing working Connector to deploy a replacement.
- **Platform-specific first steps:** Each OS has its own first-line check
  (network extension approval on macOS, virtual adapter on Windows, service
  status on Linux). Current per-platform diagnostic steps and component names
  are in `references/troubleshooting-overview.md` — open that file before
  walking a user through OS-specific commands.
- **Always test Connector → Resource connectivity from the Connector host.** Never from the
  user's machine.
- **Never probe inbound ports on a Connector.** Connectors have no inbound ports. Check
  outbound connectivity instead.
- **Check Connector logs before running network diagnostics.** Logs contain the exact
  failure reason — expired token, relay unreachable, TLS handshake failure.
- **`DEAD_NO_RELAYS` often means DPI, not just a blocked port.** If outbound 443 is
  nominally permitted but the Connector cannot reach Twingate Relays, check for a DPI
  appliance terminating TLS. Add a bypass rule for `*.twingate.com`.
- **Relay fallback is a latency concern, not a security concern.** Both P2P and Relay paths
  are encrypted. Never treat Relay fallback as a security incident.
- **Match the user's exact error string against the help-center corpus before theorizing.**
  The 70+ help-center articles in `references/` document known client bugs, exact log
  lines, and version-specific regressions — many symptoms that look like a network or
  policy problem are actually a documented client bug with a specific fix version.
  Check there before reasoning from first principles.
- **A symptom that "only started after an update" is a version-regression question, not
  a network question.** Ask for the exact client version before troubleshooting further —
  several documented regressions are scoped to a narrow version range with a specific fix
  release.

## Search References First

**Grep `references/` for the user's exact error text before answering.** This corpus is
overwhelmingly symptom-shaped support content — exact error strings, per-OS client bugs,
and version-specific regressions — and filenames hide almost all of that detail: the
literal error message, the affected OS, and the client version range live in the file
body, not the filename.

```
grep -ril "too many open files" references/          # -> connector-failures.md
grep -ril "unknown network name" references/         # -> 3992697531-client-connection-fails-with-unknown-network-name.md
grep -ril "libhydra" references/                     # -> 9756496886-windows-client-v2026-7-...md
```

If the user reports an exact error message, **grep for it before theorizing about
causes.** Never answer from training-data memory for: exact client error text or log
lines, platform-specific diagnostic commands, connector log signatures, version-scoped
client bugs, or third-party software incompatibilities — the help-center corpus changes
weekly and documents bugs that did not exist when this model was trained.

## Routing

**Co-activate, don't either/or.** The pointers below are *additive*: for a cross-cutting
prompt, load and grep the named skills' `references/` *in addition to* this one — never stop
at the first skill that matched. Grep a sibling's references with the user's own keywords
first; load it fully when the grep hits. Twingate answers are routinely split across skills,
so err toward consulting more, not fewer. Common cross-cutting clusters here: any
connectivity diagnosis → **connectors + architect**; access-denied / policy / device trust →
**identity**; DNS or exit-network symptom → **dns-security**; gateway / SSH cert / kubectl
failures → **idfw**.

- **→ twingate-connectors**: for Connector deployment, upgrade, or token questions
- **→ twingate-identity**: for security policy configuration, device trust setup, or SCIM
  provisioning questions
- **→ twingate-architect**: when the failure suggests an architectural problem (wrong Remote
  Network topology, Resource defined incorrectly)
- **→ twingate-dns-security**: when the symptom is DNS filtering, exit-network egress, or a
  third-party DNS-provider conflict rather than a private-resource connectivity failure
- **→ twingate-idfw**: for SSH certificate validation failures, PAM module errors, or
  any Twingate Gateway failure (TLS handshake errors, CONNECT 401/407, kubectl through
  the gateway, session recording) — that skill has a hand-authored field guide at
  `skills/twingate-idfw/references/gateway-troubleshooting.md`

## References

See [`references/`](./references/) for the current corpus, refreshed weekly. Three kinds
of file live there:

- **`{slug}.md`** — summaries of `twingate.com/docs` pages (product documentation and
  the six-step decision tree's supporting facts).
- **`{numeric-id}-{slug}.md`** — Twingate help-center articles: symptom-shaped support
  content, exact error strings, per-OS client bugs, and version-specific regressions.
  This is the largest and most valuable part of the corpus for this skill.
- **`gh-{org}-{repo}.md`** — summaries of public Twingate GitHub repos: community
  diagnostic tooling.

**Decision-tree documentation:**

| If the user asks about… | Read first |
|---|---|
| General diagnostic walkthrough, platform-specific first steps, error messages | `troubleshooting-overview.md`, `how-to-troubleshoot.md`, `troubleshooting.md` |
| DNS resolution failures, internal-IP responses, split-DNS misbehaviour | `dns-failures.md` |
| `DEAD` Connector states, Connector reachability, error-code reference table | `connector-failures.md` (also `skills/twingate-connectors/references/connector-best-practices.md` for network requirements) |
| Firewall rules, egress policy, DPI / SSL inspection issues | `firewalls-and-twingate.md`, `firewall-failures.md` |
| P2P establishment failures, NAT traversal, Relay fallback | `troubleshooting-p2p.md` |
| Split-tunnel routing, traffic not flowing through Twingate | `split-tunnel-failures.md` |
| **Community diagnostic scripts** — shell/Python utilities for DNS lookups, connectivity checks, and traceroute-style analysis in Twingate environments (read-only, no unified CLI) | `gh-twingate-solutions-network-utilities.md` |

**Help-center corpus, by symptom cluster** (72 articles — filenames listed in full so
every one is reachable; a row groups several files under one theme):

| Symptom cluster | Files |
|---|---|
| **Windows client** — service not running, freezes on join, TAP adapter, network-interface checks, nslookup failures, Intune/Jamf upgrade regressions, setup-wizard failures, two version-scoped crash bugs (v2025.138–232 `AccessViolationException` on wake; v2026.7 DNS-detection freeze on boot/sleep), AWS WorkSpaces pool termination, event-log export | `1111227325-windows-troubleshooting-the-twingate-tap-adaptor.md`, `1639815268-windows-client-aws-workspaces-pools-terminates-20-minutes-after-starting-twingate.md`, `1666262145-windows-how-to-generate-a-windows-system-report.md`, `2020664128-windows-client-system-service-is-not-running.md`, `2110427262-windows-checking-network-interfaces.md`, `3973356701-windows-client-freezes-after-clicking-join-network.md`, `4982245028-using-nslookup-with-manually-defined-nameserver-fails-on-windows-with-twingate-client-running.md`, `5666924507-device-security-windows-screen-lock-is-activated-but-not-detected-by-the-posture-check.md`, `5986942828-windows-client-v2025-138-232-unexpected-re-authentication-prompts-or-windows-twingate-service-stopped.md`, `6334957429-windows-how-to-export-windows-event-logs.md`, `8044397985-windows-client-upgrades-via-intune-from-2024-63-and-older-to-2024-142-fail-to-honor-network-param.md`, `9261433921-installation-of-the-windows-twingate-client-fails-with-setup-wizard-ended-prematurely.md`, `9546556496-vpn-clients-with-installed-tap-adapter.md`, `9756496886-windows-client-v2026-7-client-fails-connect-unexpected-disconnections-or-client-unresponsive.md`, `9784439823-windows-checking-the-client-service.md` |
| **macOS client** — menu bar icon missing, no resources after update, DNS resolution to twingate.com, Docker host access, screen-lock posture check false negatives/positives, CrowdStrike verification, Jamf VPN profile deployment, notification prompts, uninstall steps, IP-resource access | `2009351280-macos-crowdstrike-device-verification-not-working-even-though-data-zta-is-present.md`, `2024206011-crowdstrike-is-not-detected.md`, `2367000005-unable-to-access-local-service-on-macos-docker-host.md`, `3181164424-macos-client-no-resources-available-after-client-update.md`, `3201241878-vpn-profile-fails-to-deploy-for-macos-using-jamf-pro.md`, `4209242719-macos-client-enabling-notifications-for-additional-authentication-prompts.md`, `7690090540-macos-client-unable-to-resolve-twingate-com.md`, `8531799362-macos-client-uninstalling-twingate.md`, `8616217757-troubleshooting-access-issues-to-twingate-ip-resources-on-macos.md`, `8933604231-access-being-denied-to-macos-users-due-to-screen-lock-posture-check.md`, `9450787885-macos-client-twingate-menu-bar-icon-not-visible.md` |
| **Linux client** — distro-specific crashes and auth failures | `2349456124-linux-client-crashes-on-fedora-40-if-the-disk-is-encrypted.md`, `8310367817-linux-nixos-twingate-not-detecting-firewall-on-nixos.md`, `8503680533-linux-client-unable-to-authenticate-on-ubuntu-24-04.md` |
| **Mobile / other platforms** — ChromeOS device-security gate, Android Auto refusing to start | `6848754023-login-to-chromebook-fails-with-device-security-not-met.md`, `9474557518-android-auto-refuses-to-start-when-twingate-is-connected-error-21.md` |
| **Device posture edge case** — attached USB storage falsely tripping the disk-encryption check | `1384415743-when-hard-disk-encryption-is-activated-in-device-posture-attached-usb-storage-devices-may-cause-the-check-to-fail.md` |
| **Network interfaces, CGNAT & port/scan issues** — outbound allowlist requirements, blocked-port checks, passive FTP timeouts, port-scan false readings, unsupported regions, consumer router (Netgear) interference, ping-fails-but-other-ports-work | `1198271128-allowlist-for-outbound-connections-to-twingate-infrastructure.md`, `3353935754-connectivity-timeout-issues-when-using-passive-pasv-ftp-mode.md`, `3646943674-checking-for-blocked-outbound-ports.md`, `4186450837-tcp-ip-port-tests-or-scans-produce-inaccurate-results.md`, `4838955865-netgear-router-blocking-twingate-connectivity.md`, `6310565542-unable-to-ping-a-twingate-resource-though-it-is-accessible-on-other-ports.md`, `8648750331-checking-network-interfaces.md`, `9841905042-unsupported-regions.md` |
| **Third-party software conflicts & known incompatibilities** — Zscaler, embedded-browser/IDE certificate warnings, browser DoH, browser Local Network Access (LNA) blocking, consumer VPN clients, and the master known-incompatibility list (Zscaler, Umbrella, DNSFilter, AdGuard, Avast — CGNAT range `100.96/12`) | `1139605544-zscaler.md`, `1782897307-untrusted-certificate-warning-when-accessing-websites-through-embedded-browsers-in-ides.md`, `1933606039-disabling-browser-doh.md`, `4097879304-browser-local-network-access-lna-blocking-twingate-resources.md`, `5946128544-known-incompatibility-overview.md`, `6706399509-consumer-vpns.md` |
| **Access denied / resource ambiguity / unable-to-access** | `1268656324-self-service-resources.md`, `2783921459-checking-resource-definitions.md`, `5098803549-checking-for-resource-ambiguity.md`, `5974826840-unable-to-access-a-resource.md` |
| **Network join, P2P, auth & connection-event diagnostics** — "unable to join network", P2P internal-as-draft-then-public flow, TOTP reset, "unknown network name", connection-event log reading, AD/ADUC slowness over Twingate, `.local` domain handling | `2009013512-joining-a-twingate-network-fails-with-unable-to-join-network.md`, `2740543226-internal-as-draft-then-public-peer-to-peer-connection-troubleshooting.md`, `3391673762-reset-totp-two-factor-authentication-2fa.md`, `3992697531-client-connection-fails-with-unknown-network-name.md`, `6183198873-checking-connection-events.md`, `8595638268-active-directory-users-and-computer-aduc-is-slow-over-twingate.md`, `7071403289-handling-internal-domains-ending-in-local.md` |
| **Diagnostics & log collection** — packet capture, client log locations, admin-console reporting bugs | `1834259102-admin-console-network-events-report-is-blank-when-using-safari.md`, `8458642629-twingate-client-logs.md`, `9900337970-collecting-and-exporting-a-packet-capture.md` |
| **Support process & account/tenant administration** — entitlement, coverage hours, priority levels, escalation, help-center sign-in, client version downloads, system requirements, deleting a tenant, updating a user's email | `1239565250-technical-support-entitlement.md`, `2672568245-engaging-technical-support.md`, `3657481671-technical-support-coverage-hours.md`, `6581096205-signing-into-the-twingate-help-center.md`, `7488571404-technical-support-priority-levels.md`, `9287595551-self-serve-troubleshooting-guide.md`, `6847496306-where-can-i-download-a-previous-version-of-the-twingate-client.md`, `1900346829-twingate-client-system-requirements-and-supported-operating-systems.md`, `5428888738-updating-an-existing-user-s-email-address.md`, `5856392229-how-do-i-delete-my-twingate-network-tenant.md`, `2331236562-security-information-for-the-twingate-network.md` |

This table is a fast path, not the whole corpus — when a question doesn't match a row,
or names an error string not shown above, grep `references/` before answering.
