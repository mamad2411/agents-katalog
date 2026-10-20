---
name: embed-connectivity
description: Wireless and networked connectivity for embedded devices — Wi-Fi, BLE, Thread / Matter, cellular, LoRaWAN, MQTT/CoAP. Auto-invoked when designing connectivity stacks, debugging pairing/provisioning, or optimizing power/cost trade-offs for fleet comms.
---

# Embedded Connectivity

A field-deployed device that can't reconnect is a brick. Provisioning, credential
storage, retry behavior, and protocol choice shape both field reliability and
fleet economics — and most of those decisions are expensive to change after launch.

## When to reach for this

- Choosing a radio / protocol stack for a new device class
- Designing or debugging pairing, provisioning, or reconnect flows
- Sizing cellular data plans or cutting per-device data cost
- Planning RF certification (FCC/CE/IC, BT SIG, WFA, Matter/CSA, carrier approval)

## Principles

1. **Pick the radio by duty cycle and payload shape first.** LoRaWAN for
   tiny-and-rare, BLE for paired-and-close, Thread/Matter for ecosystem-first,
   LTE-M/NB-IoT for field-deployed without a gateway, Wi-Fi for mains-powered.
   Cost and power diverge fast when you pick wrong.
2. **Design for reconnect, not connect.** First-time pairing is easy;
   week-three-in-a-basement reconnects are where fleets die. Exponential backoff
   with jitter, persistent connection state across reboots, captive-portal
   detection, and a physical "reset to pairing" control.
3. **Store credentials in hardware.** Secure element (ATECC608, SE050, NXP
   EdgeLock) or TrustZone-backed key storage — never flash-resident cleartext.
   Provision per-device keys at manufacturing, not at first boot.
4. **Compact payloads aggressively on cellular.** CBOR over JSON, delta encoding,
   batching. A 200-byte payload can bloat to 600+ bytes once TLS record and IP
   overhead are counted; use DTLS/TLS session resumption and PSM/eDRX, and size
   the data plan from measured bytes/day, not the application payload.
5. **Instrument the comms thread.** Counters for connect attempts,
   failures-by-reason, bytes up/down, and latency — emitted periodically even on
   success. Reconnect flakes are undebuggable without field telemetry.
6. **Plan the cert path from day zero.** BLE → BT SIG listing, Wi-Fi logo → WFA,
   Matter → CSA, cellular → PTCRB/GCF plus carrier approval. These are
   months-long pipelines; retrofitting certification is painful and expensive.

## Radio selection — first cut

| Radio | Best fit | Power profile | Watch out for |
|---|---|---|---|
| LoRaWAN | bytes, minutes–hours apart, km range | years on primary cells | regional duty-cycle limits; downlink is scarce |
| BLE | phone-paired, short range | coin-cell viable | needs a mediator (phone/gateway) for cloud reach |
| Thread / Matter | smart-home ecosystem play | low; mesh extends range | commissioning UX + CSA cert effort |
| Wi-Fi | mains-powered, high throughput | worst of the set | provisioning UX; 2.4 GHz congestion |
| LTE-M / NB-IoT | field-deployed, no gateway | battery-viable only with PSM/eDRX | carrier cert, roaming policy, per-MB cost |
| LTE Cat-1 / 4G | bandwidth-heavy field devices | mains or large battery | module + plan cost dominates BOM |

## Connection state machine — minimum states

`PROVISIONING → CONNECTING → CONNECTED → BACKOFF (jittered exponential, capped)
→ OFFLINE_BUFFERING → FACTORY_RESET_PENDING`. Persist the current state and
backoff counter across reboots; on MQTT use LWT so the fleet sees ungraceful
drops, and pick QoS per topic (telemetry QoS 0/1, commands QoS 1) rather than
globally.

## Pitfalls

- Retry loops without jitter — a fleet-wide outage recovery becomes a thundering
  herd against your broker
- Credentials provisioned at first boot over an unauthenticated channel
- Trusting "connected to AP" as "has internet" — no captive-portal/DNS check
- JSON-over-TLS telemetry on NB-IoT plans sized from payload bytes only
- Certification discovered at EVT — module pre-certs help but don't cover the
  end product's intentional-radiator testing

---
*Related: `embed-driver` (radio-module bus driver), `embed-rtos` (comms task
design), `embed-ota` (update transport), `embed-power` (radio duty-cycle vs
sleep) · domain agent: `embed-architect` · output/ADR format:
`playbook-conventions`*
