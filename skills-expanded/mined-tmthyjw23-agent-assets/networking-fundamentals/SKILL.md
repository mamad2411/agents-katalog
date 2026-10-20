---
name: networking-fundamentals
description: >
  Understand the network layer under your system. Use for DNS and record types,
  TCP vs UDP, HTTP/1-2-3, TLS handshake, OSI model, IP addressing (IPv4/IPv6),
  ports, NAT, unicast/broadcast/multicast/anycast, proxies, load balancing at
  L4/L7, latency budgeting, and "what happens when I type a URL". Triggers:
  "DNS", "TCP vs UDP", "HTTP/3", "OSI model", "ports", "what happens when...".
---

# Networking Fundamentals

Most production incidents are network-shaped. Know the stack.

## When to use
- Debugging latency, timeouts, connection issues.
- Choosing transport (TCP/UDP/QUIC) or HTTP version.
- Explaining request paths end-to-end.
- Capacity/latency budgeting.

## Core concepts
- **OSI / TCP-IP layers:** physical → link → network (IP) → transport
  (TCP/UDP) → application (HTTP/DNS/...).
- **IP:** IPv4 vs IPv6; subnets; NAT; public vs private; anycast for CDN/DNS.
- **Transport:** TCP (reliable, ordered, handshake, head-of-line) vs UDP
  (unreliable, low-latency, gaming/streaming/DNS/QUIC).
- **DNS:** resolution path (resolver → root → TLD → authoritative), caching/TTL,
  record types (A/AAAA/CNAME/MX/TXT/NS/SOA/SRV), geo/weighted routing.
- **HTTP evolution:** HTTP/1.1 (sequential, HOL) → HTTP/2 (multiplexing,
  header compression, one TCP) → HTTP/3 (QUIC over UDP, no HOL blocking).
- **TLS:** handshake, certificates, SNI, session resumption.
- **Ports:** common well-known ports.

## Traffic & latency
- Latency numbers every engineer should know (L1/L2/SSD/DC round trip/...).
- Latency budget: client → DNS → TLS → LB → service → DB → back. Sum it.
- Reduce round trips: keep-alive, connection pooling, multiplexing, edge.
- Anycast + CDN to shorten the physical path.

## Proxies & load balancing
- Forward proxy vs reverse proxy; API gateway vs LB.
- L4 (TCP) vs L7 (HTTP) load balancing; TLS termination point.

## Checklist
- [ ] Transport protocol chosen (TCP vs UDP/QUIC) with rationale.
- [ ] HTTP version and connection strategy defined.
- [ ] DNS TTL + routing policy (geo/weighted/failover) set.
- [ ] TLS termination location decided; cert rotation automated.
- [ ] Latency budget written and measured end-to-end.
- [ ] Timeouts/retries aligned across layers.
- [ ] Port/address plan documented.

## Common pitfalls
- Long DNS TTLs blocking failover.
- TCP head-of-line blocking on multiplexed HTTP/2 connections.
- Retries at multiple layers → retry storms.
- Assuming IPv4-only.
- Ignoring connection setup cost per request.

## References
- `...\what-is-osi-model.md`, `...\explaining-8-popular-network-protocols-in-1-diagram.md`
- `...\how-does-the-domain-name-system-dns-lookup-work.md`, `...\dns-record-types-you-should-know.md`
- `...\ipv4-vs-ipv6.md`, `...\18-common-ports-worth-knowing.md`, `...\how-nat-made-the-growth-of-the-internet-possible.md`
- `...\http1-http2-http3.md`, `...\what-makes-http2-faster-than-http1.md`, `...\important-things-about-http-headers-you-may-not-know.md`
- `...\http-status-code-you-should-know.md`, `...\5-http-status-codes-that-should-never-have-been-created.md`
- `...\what-protocol-does-online-gaming-use-to-transmit-data.md`, `...\top-4-most-popular-use-cases-for-udp.md`
- `...\unicast-vs-broadcast-vs-multicast-vs-anycast.md`, `...\internet-traffic-routing-policies.md`, `...\proxy-vs-reverse-proxy.md`
- `...\what-happens-when-you-type-a-url-into-your-browser.md`, `...\which-latency-numbers-should-you-know.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`api-design`, `security-and-auth`, `scalability-and-performance`,
`computer-fundamentals`.
