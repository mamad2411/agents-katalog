---
name: esp32-lwip-dns-cache-multi-address-bounds
description: Use when auditing ESP-IDF lwIP DNS cache behavior when CONFIG_LWIP_DNS_MAX_HOST_IP is greater than one or multiple A/AAAA records are returned.
license: MIT
version: "1.0.0"
---

# ESP-IDF LWIP DNS CACHE MULTI-ADDRESS BOUNDS

## Purpose and decision boundary

Audit the boundary between lwIP DNS cache entries and APIs that return one address through a single ip_addr_t output object. This skill is specifically about the cached lookup path and does not replace general DNS reliability, resolver failover or TLS/SNI diagnosis.

The reported condition requires CONFIG_LWIP_DNS_MAX_HOST_IP greater than one, a cached hostname with multiple A or AAAA records, and a subsequent lookup through a single-address API. The ESP-IDF default is one. Do not label every ESP32 DNS client vulnerable without checking all three conditions.

## Required inputs

- Exact SoC, module, board and ESP-IDF release, branch and commit.
- Resolved lwIP component revision and generated sdkconfig.
- CONFIG_LWIP_DNS_MAX_HOST_IP and CONFIG_COMPILER_STACK_CHECK_MODE values.
- DNS APIs used by the application and components, including SNTP and custom resolver wrappers.
- Whether callers supply one ip_addr_t or an explicit-capacity address array.
- DNS response captures, cache state, hostname, record count and timing of first and subsequent lookups.
- Arduino-ESP32 or PlatformIO framework package and the actual ESP-IDF commit it resolves.

Mark unknown values explicitly. Platform package version alone is not proof of the embedded ESP-IDF revision.

## Engineering model

### Cached lookup contract

The vulnerable path reported in lwIP dns_lookup() iterated over every address in a cache entry and copied each address into a caller-provided single ip_addr_t output buffer. The legacy dns_gethostbyname() and dns_gethostbyname_addrtype() APIs do not provide an output capacity. With multiple cached addresses, the loop can write past the single-element destination into adjacent stack memory.

The first DNS resolution goes to the network and is not the reported overflow path. The failure occurs on a later lookup served from the cache. A hostname with multiple A or AAAA records can be legitimate; an attacker who can influence DNS responses can also choose the address bytes that are copied.

### Advisory evidence and version scope

Espressif advisory GHSA-ch63-jxm5-vmvf, CVE-2026-113783, was published 2026-10-30 with High severity (CVSS 7.4). The reporter's condition and affected ranges are:

| ESP-IDF line | Affected range | Fixed release / branch commit |
|---|---|---|
| v5.2 | v5.2.3 through v5.2.8 | No fix; branch is EOL |
| v5.3 | v5.3.2 through v5.3.6 | v5.3.7 / 7ab85eb |
| v5.4 | v5.4.0 through v5.4.4 | v5.4.5 / 882843d |
| v5.5 | v5.5.0 through v5.5.5 | v5.5.6 / af7543d |
| v6.0 | v6.0.0 through v6.0.2 | v6.0.3 / defaa2f |
| v6.1 branch | Check exact tag and ancestry | 98e6e7a |

As of 2026-11-11, v5.5.6 and v6.0.3 are released; v5.3.7 and v5.4.5 were listed as not yet released. The v5.2 branch has reached end of life and has no fixed release. Verify the current release feed before deployment.
## Design and investigation sequence

1. Freeze the IDF commit, lwIP component, board and generated configuration.
2. Search the full call graph for dns_gethostbyname() and dns_gethostbyname_addrtype(), including SNTP and third-party components.
3. Confirm whether CONFIG_LWIP_DNS_MAX_HOST_IP exceeds one. Record the source of the setting; do not assume the example or project default.
4. Reproduce the sequence with a deterministic hostname returning multiple addresses: initial network resolution, then a cache-hit lookup through the single-address API.
5. Inspect whether the exact branch bounds the legacy copy to one address and exposes explicit-count APIs for callers needing multiple addresses.
6. Prefer a fixed release or verified branch commit. If an upgrade is temporarily impossible, keep the maximum at one and document the loss of multi-address behavior.
7. Rebuild all affected components and retain sdkconfig, dependency lock, ELF, map and firmware hash.
8. Verify the actual target and resolver behavior before closing the issue.
## Constraints and invariants

- A single-address API must never write more than one ip_addr_t to the caller's output.
- Multi-address APIs must receive and enforce an explicit caller capacity.
- Never infer output capacity from CONFIG_LWIP_DNS_MAX_HOST_IP alone.
- Keep CONFIG_LWIP_DNS_MAX_HOST_IP at one on affected releases unless the fixed implementation is present and verified.
- Stack smashing protection detects some corruptions but does not prevent the out-of-bounds write; it is not a fix.
- Do not weaken DNS authentication, TLS verification, stack protection or watchdogs to hide the symptom.
- Preserve DNS failure and timeout semantics; do not silently return a partial or stale address list as complete.
- Treat the v5.2 EOL line as unpatched unless the product carries a reviewed downstream fix.
## Failure analysis

| Observation | Likely investigation path | Evidence limit |
|---|---|---|
| First lookup succeeds, later lookup crashes | Check cache-hit path and multiple cached records | Timing correlation alone is not proof |
| Crash follows DNS or SNTP refresh | Inspect single-address consumers and response record count | A reboot does not identify the exact overwrite |
| CONFIG_LWIP_DNS_MAX_HOST_IP is one | This specific multi-address precondition is not met | Other DNS parser bugs may still exist |
| Stack canary aborts | Treat as detection of corruption, not prevention | Canary does not prove the only possible impact |
| PlatformIO or Arduino build is affected | Resolve the actual IDF/lwIP package and sdkconfig | Platform version alone is insufficient |
## Verification plan

- Host/unit: model cache entries with one and multiple addresses; verify single-address calls write one slot and explicit-capacity APIs never exceed the supplied count.
- Boundary: test zero, one, maximum configured and excess cached addresses; include IPv4, IPv6 and mixed-family records.
- Cache lifecycle: test first network lookup separately from subsequent cache hits, expiry and cache replacement.
- Build: compile the exact target and confirm the fixed lwIP source is in the resolved dependency graph.
- Hardware/system: run repeated lookups with controlled DNS responses and retain stack, reset and packet evidence.

A host model cannot prove the actual lwIP stack frame, cache implementation or target behavior. Never use a production device or untrusted live DNS environment as a destructive fuzz target.
## Deliverables

1. Exact affected/not-affected/unknown matrix for IDF, lwIP, configuration and API usage.
2. Call graph of all single-address and multi-address DNS consumers.
3. Minimal cache-hit reproducer with DNS response and sdkconfig evidence.
4. Fixed release/commit or documented temporary configuration restriction.
5. Host, build and target validation results plus residual risk.

## Review checklist

- [ ] Exact SoC, IDF commit, lwIP revision and generated sdkconfig are recorded.
- [ ] CONFIG_LWIP_DNS_MAX_HOST_IP is explicitly checked.
- [ ] The first lookup and subsequent cache-hit lookup are tested separately.
- [ ] Single-address APIs cannot write beyond one ip_addr_t.
- [ ] Multi-address APIs use an explicit output capacity.
- [ ] Stack protection is not misrepresented as a repair.
- [ ] PlatformIO/Arduino dependency resolution is verified rather than inferred.
- [ ] EOL v5.2 exposure and downstream patch status are explicit.
- [ ] Hardware results identify board revision, firmware hash and DNS test fixture.

## References and source policy

- Espressif advisory GHSA-ch63-jxm5-vmvf: https://github.com/espressif/esp-idf/security/advisories/GHSA-ch63-jxm5-vmvf
- ESP-IDF fix on master: https://github.com/espressif/esp-idf/commit/75f2ff7e0c2d19e113293ec122b701c83d2f6665
- ESP-IDF fix on release/v6.1: https://github.com/espressif/esp-idf/commit/98e6e7a
- ESP-IDF fix on release/v6.0: https://github.com/espressif/esp-idf/commit/defaa2f
- ESP-IDF fix on release/v5.5: https://github.com/espressif/esp-idf/commit/af7543d
- ESP-IDF fix on release/v5.4: https://github.com/espressif/esp-idf/commit/882843d
- ESP-IDF fix on release/v5.3: https://github.com/espressif/esp-idf/commit/7ab85eb
- ESP-IDF DNS API reference: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/lwip.html

Treat the advisory as the primary version-scope source. Recheck release notes, commit ancestry and the exact dependency graph before deployment.
