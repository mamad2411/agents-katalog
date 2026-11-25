---
name: esp32-lwip-network-diagnostics
description: Use when an ESP32 connects to Wi-Fi or Ethernet but DNS, DHCP, TCP sockets or long-running network sessions fail; especially when reconnects leak resources or packet loss appears only under load.
license: MIT
---

# lwIP and network lifecycle diagnostics

A connected Wi-Fi station is not proof that the IP layer or application socket is healthy.
Diagnose link, address configuration, DNS, route, TCP and application protocol as separate layers.

## Capture the environment

- Record SoC, ESP-IDF or Arduino core version, lwIP configuration and Wi-Fi/Ethernet driver.
- Record AP/router model, DHCP lease behavior, DNS server, VLAN and IPv4/IPv6 assumptions.
- Capture timestamps for link-up, DHCP completion, DNS lookup, connect, TLS handshake and first payload.
- Distinguish a Wi-Fi association event from an IP-ready event.
- Avoid assuming that a private LAN uses one fixed gateway or DNS address.

## DHCP and address lifecycle

- Treat DHCP lease acquisition, renewal and address loss as explicit state transitions.
- Clear stale application connections when the local address changes.
- Do not start cloud clients before the network stack reports a usable IP configuration.
- For static addresses, validate subnet, gateway and DNS independently; an IP address alone does not provide a route.
- Log the assigned address, netmask, gateway and DNS servers without exposing credentials.
- Test router restart, lease renewal, AP roam and Ethernet cable removal.

## DNS diagnosis

- Separate hostname resolution failures from TCP connect timeouts.
- Record the queried hostname, resolver result and elapsed time; do not log secrets embedded in URLs.
- Test multiple DNS servers only as a controlled diagnostic, not as an unexplained hardcoded fallback.
- Respect DNS TTL and avoid caching an address forever.
- Validate IPv4/IPv6 assumptions and the address family returned by the resolver.
- A successful ping to an IP does not prove DNS works.

## Socket lifecycle and resource bounds

- Give every socket a single clear owner and close it on every success and error path.
- Bound connect, send and receive timeouts; a blocking socket must not monopolize a control task.
- Handle partial sends and receives; TCP is a byte stream, not a message protocol.
- Define reconnect backoff with jitter to avoid synchronized reconnect storms.
- Limit concurrent sockets and queued payload bytes; report backpressure instead of allocating indefinitely.
- Distinguish application heap loss from TCP states such as TIME_WAIT and from driver-owned buffers.

## Observability

- Track counts for DNS failures, connect failures, resets, timeouts, bytes and active sockets.
- Log state transitions, not every packet; high-volume logs can change timing and hide the fault.
- Capture lwIP statistics only when the relevant build configuration enables them.
- Use packet capture at the AP/router or Ethernet switch to separate device behavior from network behavior.
- Redact tokens, passwords, session cookies and private payloads before sharing traces.

## Verification

1. Test DNS success, NXDOMAIN, timeout and resolver loss.
2. Restart the AP/router while requests are active.
3. Drop the Ethernet link or force Wi-Fi roam during a TCP transfer.
4. Send payloads larger than one TCP segment and verify framing handles partial reads.
5. Run a long-duration reconnect soak and track heap, largest free block and socket count.
6. Verify backoff remains bounded and the control loop continues to meet its deadline.

## Acceptance criteria

- Host tests cover TCP stream reassembly, retry backoff and connection-state transitions.
- Hardware tests name the AP/router, DHCP/DNS setup, framework version and test duration.
- Resource graphs distinguish free heap, largest block and socket lifecycle.
- No issue is called a memory leak until socket and TCP-state evidence is checked.

## References

- ESP-IDF lwIP: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/lwip.html
- ESP-IDF Wi-Fi: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html
- lwIP documentation: https://www.nongnu.org/lwip/2_1_x/
