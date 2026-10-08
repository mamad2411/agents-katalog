---
name: "proxyman-https-capture"
description: "Configure and troubleshoot Proxyman HTTPS capture across desktop systems, Apple and Android devices or simulators, browsers, runtimes, containers, frameworks, and HTTP clients, including Atlantis instrumentation for controlled apps."
---

# Proxyman HTTPS Capture

Choose the least invasive working capture path for the user's exact device, runtime, network, and Proxyman platform. Normal proxy capture has three independent requirements: route traffic through Proxyman, trust the Proxyman CA, and enable SSL Proxying for the target host. Atlantis is an instrumentation alternative that forwards inspected traffic to Proxyman without that proxy/CA/SSL-Proxying path; apply its separate limits and verification.

Use `proxyman-mcp-setup` if tools are absent, `proxyman-traffic-debugging` to inspect captured flows, `proxyman-certificates-recovery` for the host Mac's generated/custom root lifecycle or custom server/client identities, and `proxyman-debugging-tools` when current official documentation is needed beyond the setup flow.

## Gather The Minimum Context

Establish:

- host OS running Proxyman and app version;
- target type, OS/runtime version, physical vs simulator/emulator, and debug vs production build;
- how the target connects to the host and whether a VPN, MDM, firewall, proxy, or certificate pinning is present;
- target hostname and whether HTTP is visible but HTTPS is opaque, or no traffic appears at all;
- whether the user wants GUI steps, MCP-guided automation, or manual commands.

Do not install certificates, root an emulator, alter system proxy, inject a shell/app, or restart a target until the user approves that action.

## Universal Capture Model

Diagnose in this order:

1. **Reachability:** target can reach the host running Proxyman.
2. **Routing:** target sends HTTP/HTTPS to Proxyman's current proxy host and port.
3. **Recording:** Proxyman is recording and the source/client is visible.
4. **Trust:** target trusts the correct Proxyman root CA in the relevant store.
5. **SSL Proxying:** target host is included and not excluded.
6. **Application behavior:** library proxy bypass, localhost special case, VPN, pinning, QUIC/HTTP3, or a custom trust store.

Do not treat certificate installation as proof that routing works, or SSL Proxying as proof that the target trusts the CA.

## Choose A Path

Read [capture paths](references/capture-paths.md) for the decision matrix and official page links. Read [Atlantis capture](references/atlantis.md) when the user asks what Atlantis is, needs capture while a VPN blocks the normal proxy, or wants to integrate Atlantis into an app.

- Desktop browser/app honoring system proxy: use system proxy plus host certificate trust.
- iOS/iPadOS/Vision Pro device: use Wi-Fi manual proxy and device certificate trust; for a supported app that can include an instrumentation library, consider Atlantis when proxy/certificate setup is undesirable or a VPN blocks the normal route.
- Apple simulator: install the CA into the booted simulator and use the simulator proxy path.
- tvOS/watchOS: follow the physical/simulator-specific official path.
- Android physical device: manual Wi-Fi proxy plus user/system CA strategy appropriate to OS and app policy.
- Android emulator: prefer Proxyman's guided automation for an active compatible AVD; read [Android emulator safety](references/android-emulator.md).
- Terminal runtime or browser: prefer Automatic Setup/injection when supported; otherwise use explicit proxy variables/options and the runtime CA bundle/store from [runtime capture](references/runtime-capture.md).
- Localhost: use explicit proxy configuration or Reverse Proxy; many clients intentionally bypass the system proxy.
- Docker/VM/subsystem: use the host address reachable from that network namespace, not blindly `127.0.0.1`.

## MCP-Guided Workflow

1. `get_version` and `get_proxy_status`.
2. `answer_setup_question` with the exact target, platform, runtime, VPN, and symptom.
3. Read the returned citations and use `list_setup_workflows` when the target is ambiguous.
4. For a normal proxy path, check `get_certificate_status` and `get_ssl_proxying_list`. For Atlantis, read `docs://setup/atlantis` and do not force certificate or SSL Proxying setup.
5. Use a relevant built-in resource or prompt. Setup resources are listed in the capture-path reference.
6. Explain the automation's state changes and request consent.
7. Use `run_guided_setup`, `inject_terminal`, `inject_electron`, `set_system_proxy`, `install_certificate`, or SSL tools only when the live server exposes the needed action and the user approved it.
8. Generate one known HTTPS request from the target.
9. Find it with `filter_flows` using host and, when relevant, `client`; inspect it with `get_flow_detail`.
10. Verify HTTPS body visibility, TLS/certificate summary, and target identity.

If the MCP setup index has no exact match, fetch the current official page through `proxyman-debugging-tools` rather than forcing a generic fallback result.

## GUI Workflow

1. Open Proxyman's Setup or Certificate guide for a normal proxy target. For Atlantis, follow the dedicated integration reference instead.
2. Use the proxy host/port shown by the running app; do not hardcode a common port.
3. Follow the target-specific routing and certificate steps from the current official page.
4. Enable SSL Proxying only for the required host or wildcard.
5. Generate a deterministic request and verify it in Proxyman.
6. Document how to restore proxy, trust, emulator boot image, or injected environment.

## Failure Triage

- **Nothing appears:** recording/routing/reachability/client-source problem.
- **HTTP appears, HTTPS does not:** routing works; inspect target trust, SSL Proxying, pinning, HTTP3/QUIC, or custom CA stores.
- **TLS error:** verify the correct CA, full trust, host include/exclude, app pinning, and date/time. Do not disable TLS verification as the default fix.
- **Only some libraries missing:** the library likely bypasses environment/system proxy or uses a separate trust store.
- **Device cannot connect:** verify same network or routable host address, firewall/access control, current port, and VPN/Private Relay behavior.
- **Localhost missing:** use Reverse Proxy or explicit proxy settings with a non-loopback target address.
- **VPN conflict on iOS:** read the Atlantis decision path for a build the user controls instead of repeatedly changing the device proxy.
- **Android app rejects user CA:** use a debug network security configuration or a controlled compatible emulator system-CA path. Do not advise bypassing pinning in a production app.

## Verification Checklist

A setup is complete only when:

- the expected target/client is identifiable;
- the test request and response appear;
- HTTPS headers/body are readable through the intended path: decrypted for normal proxy capture or forwarded by the expected Atlantis source;
- no unrelated hosts were unnecessarily enabled for SSL Proxying when the normal proxy path was used;
- the user knows the rollback path;
- limitations such as pinning, production builds, VPN, root/Magisk, or unsupported automation are stated.
