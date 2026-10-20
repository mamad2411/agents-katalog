---
name: dns-aid
description: >-
  DNS-AID (DNS for AI Discovery): publish and discover AI agents in DNS with SVCB records, following
  draft-mozleywilliams-dnsop-dnsaid-02 (individual Internet-Draft for dnsop, name posture): an
  agent SVCB RRset at its primary owner name, one record per agent protocol, the
  _index._agents.<domain> organization index, AliasMode for _agents and DNS-SD names, DANE TLSA
  at _443._tcp, DNSSEC, mandatory= downgrade rules, and the proposed cap, cap-sha256, bap, policy,
  realm and well-known SvcParamKeys, kept as private-use keyNNNNN until IANA assigns them. Covers
  consumer rules (try the agent name first, treat records as transport not trust, refuse cap-sha256
  mismatches, DoT or DoH), and upgrading -00/-01 records from _name._proto._agents leaves. Use when
  making an agent, MCP server or A2A agent discoverable through DNS, building a resolver-side
  discovery client, or reviewing an agent zone. Triggers: DNS-AID, DNS for AI Discovery,
  _agents, _index._agents, agent SVCB record, dns-aid-core.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DNS-AID (DNS for AI Discovery)

DNS-AID publishes AI agents in the DNS so other agents can find them without a central registry. It defines no new record types: an agent is an SVCB RRset (RFC 9460) at its own name, carrying the endpoint, transport and agent protocol, optionally with a DANE TLSA record and DNSSEC signatures. An organization index at `_index._agents.<domain>` points to the organization's list of agents. With this skill the agent publishes agent records or writes a client that discovers them.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. "§" alone refers to `draft-mozleywilliams-dnsop-dnsaid-02`; "-01 §" to the legacy revision; "RFC 9460 §" to SVCB. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Draft posture: **name**. Reserve the identifiers -02 defines (the agent primary owner names and `_index._agents`) and publish them using only registered SVCB keys plus TLSA, so the records are useful to any RFC 9460 client today. The DNS-AID SvcParamKeys have no IANA numbers, the ALPN ids `mcp` and `a2a` are placeholders, and the draft has changed its naming between revisions, so nothing should depend on those parts until they are assigned.

## Inputs (fill in, or ask before starting)

- Role: publisher (zone operator for agents), consumer (discovery client), or both.
- Agents: name, primary owner FQDN, endpoint (TargetName, port, addresses), agent protocols (MCP, A2A, other) and the descriptor each protocol uses, such as an A2A agent card.
- Hosting: in your zone or at a service provider (a different TargetName).
- Index: whether the organization publishes `_index._agents.<domain>`, and where its index document lives (format out of scope for DNS-AID).
- DNSSEC and DANE: whether the zone is signed, and whether endpoints publish TLSA.
- Private-use keys: whether a closed group of consumers has agreed on `keyNNNNN` numbers for the DNS-AID keys.
- Target version: draft-mozleywilliams-dnsop-dnsaid-02 (default, posture name: reserve names, use registered keys). draft-mozleywilliams-dnsop-dnsaid-01 is legacy: read and upgrade from, never publish. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the datatracker page for a newer revision, dnsop adoption, expiry or replacement, check the IANA SvcParamKeys registry for assigned DNS-AID keys, and update the pins.

## Invariants

1. **No new record types.** Agent records are SVCB; TLSA is optional; DNS-SD is optional (§ 1.1).
2. **The agent's name is the primary entry point.** Publishers SHOULD put a ServiceMode SVCB RRset at the agent's own name, for example `agent-name.example.com`, and requestors MUST try that query first (§ 3.1).
3. **Other names alias to it.** An `_agents` inventory leaf or a DNS-SD name for the same agent MUST be SVCB AliasMode pointing at the primary owner (§ 3.1).
4. **One agent protocol per record.** Each agent protocol is a separate SVCB record in the RRset; never list two agent protocols in one `alpn` (§ 3.1.1; RFC 9460 § 7.1).
5. **The index uses a real TargetName.** `_index._agents.<domain>` is an SVCB record whose TargetName MUST be present and MUST NOT contain underscores, so the index can be served with a public X.509 certificate; TLSA is queried at that TargetName. The index document's format is out of scope (§ 3.2).
6. **Records are transport, not trust.** Consumers MUST NOT treat a DNS-AID record as a trust signal: an authentic record can point at a hostile agent or a descriptor carrying prompt injection. Trust is decided out of band (§ 1.2, § 6.1).
7. **Integrity checks are binding.** A capability descriptor whose SHA-256 does not match `cap-sha256` MUST be refused (§ 6.1).
8. **DNSSEC.** Records SHOULD be signed, and MUST be when TLSA is used. Consumers SHOULD validate, SHOULD refuse bogus data, and MUST NOT relax validation because `mandatory=` keys appear absent (§ 1.1, § 6.4).
9. **Mandatory keys gate records.** A key the consumer must honor goes in `mandatory=`, and a consumer that does not implement a mandatory key MUST skip the record (§ 6.3; RFC 9460 § 8).
10. **Unassigned keys stay private-use.** Until IANA assigns numbers, DNS-AID keys can only appear as `keyNNNNN` in the private-use range 65280 to 65534, with meaning agreed out of band (§ 7.1; RFC 9460 § 2.1, § 14.3.2; -01 § 4.4.3).
11. **Privacy.** Use DNS over TLS or HTTPS for discovery queries, and do not send EDNS Client Subnet on queries that reveal user-identifying agent names (§ 6.6).

## Workflow

1. **Pick the version.** Publish -02 names; treat `_<name>._<proto>._agents` leaves as -01 input to upgrade.
   -> [`references/versions.md`](references/versions.md)
   ✓ No new record is published under a -01-only name pattern except as an AliasMode pointer.
2. **Design the agent RRset** (publisher). One ServiceMode record per agent protocol at the primary owner, with TargetName, `port`, `ipv4hint` and `ipv6hint`, and an `alpn` holding the agent protocol id plus real transport ids such as `h2` and `h3` (§ 3.1, § 3.1.1; RFC 9460 § 7.1.2).
   -> [`references/records.md`](references/records.md)
   ✓ Every record parses as plain RFC 9460 SVCB, no record lists two agent protocols, and a client that knows none of the agent ids still finds a transport it supports.
3. **Decide the DNS-AID keys** (publisher). Under the name posture, omit `cap`, `cap-sha256`, `bap`, `well-known`, `policy` and `realm` from public records, or publish them as agreed private-use `keyNNNNN` values outside `mandatory=` (§ 3.1, § 5.1, § 5.6, § 7.1).
   -> [`references/records.md`](references/records.md)
   ✓ A consumer that knows none of the private-use keys still gets a usable record.
4. **Add aliases and the index** (publisher). AliasMode for `_agents` and DNS-SD names; `_index._agents.<domain>` ServiceMode to an index host without underscores (§ 3.1, § 3.2).
   -> [`references/records.md`](references/records.md)
   ✓ Every alias resolves to a primary owner, and the index TargetName can hold a WebPKI certificate.
5. **Secure the zone** (publisher). Sign with DNSSEC; publish TLSA at `_443._tcp.<TargetName>` if DANE is used, and then signing is mandatory (§ 1.1, § 6.2).
   -> [`references/records.md`](references/records.md)
   ✓ A validating resolver returns the SVCB and TLSA RRsets with the AD bit set.
6. **Discover** (consumer). Query the agent name first, then the index; filter records to supported ALPN and mandatory keys; authenticate TLS with TLSA or WebPKI under a chosen posture (§ 3.1, § 3.2, § 6.2, § 6.3).
   -> [`references/consumer.md`](references/consumer.md)
   ✓ Unknown mandatory keys skip the record, and the TLS posture is explicit (permissive, preferred or strict).
7. **Fetch descriptors safely** (consumer). Verify `cap-sha256` if present, treat the descriptor as untrusted input, and make the trust decision from reputation, attestation or policy (§ 6.1).
   -> [`references/consumer.md`](references/consumer.md)
   ✓ Descriptor text never reaches a model as instructions without an out-of-band trust decision.
8. **Review privacy and operations.** DoT or DoH, no ECS, TTLs per volatility, no algorithm choices validators ignore (§ 6.4, § 6.6).
   -> [`references/consumer.md`](references/consumer.md)
   ✓ Discovery queries do not leak over plaintext DNS where an encrypted resolver is available.

## Verify before done

- [ ] Each agent has one ServiceMode SVCB RRset at its primary owner, one record per agent protocol (§ 3.1, § 3.1.1).
- [ ] `_agents` and DNS-SD names for an agent are AliasMode to the primary owner (§ 3.1).
- [ ] `_index._agents.<domain>` has a TargetName without underscores (§ 3.2).
- [ ] No unassigned DNS-AID key appears by name in a zone file; private-use `keyNNNNN` values are documented and outside `mandatory=` for public consumers (§ 7.1; RFC 9460 § 2.1, § 8).
- [ ] The zone is DNSSEC-signed whenever TLSA is published (§ 1.1).
- [ ] The consumer tries the agent name first, skips records with unknown mandatory keys, and refuses `cap-sha256` mismatches (§ 3.1, § 6.1, § 6.3).
- [ ] Nothing in the consumer treats a DNS-AID record as authorization or trust (§ 6.1).

## Reference index

- **`references/versions.md`**: the -02 current line, the -00/-01 legacy line and BANDAID predecessor, what changed, the upgrade steps, and why the posture is name. Load for step 1.
- **`references/records.md`**: zone-file patterns for agent RRsets, multi-protocol agents, hosted agents, aliases, the index, TLSA, and the private-use key question, including the numbers dns-aid-core uses. Load for steps 2 to 5.
- **`references/consumer.md`**: the discovery procedure, ALPN and mandatory-key filtering, TLS postures, descriptor handling, DNSSEC, privacy and the experimental mechanisms not to depend on. Load for steps 6 to 8.

## Related skills

- `dns-over-https` for encrypted discovery queries: `npx skills add ScaleDockHQ/scaledock-skills --skill dns-over-https`.
- `a2a` for the Agent2Agent protocol and its agent card, which DNS-AID records point to: `npx skills add ScaleDockHQ/scaledock-skills --skill a2a`.
- `mcp` for Model Context Protocol servers published as agents: `npx skills add ScaleDockHQ/scaledock-skills --skill mcp`.
- `agntcy-oasf` for the Open Agentic Schema Framework, one candidate format for capability descriptors: `npx skills add ScaleDockHQ/scaledock-skills --skill agntcy-oasf`.
- `well-known-uris` for the `/.well-known/` paths agent descriptors use: `npx skills add ScaleDockHQ/scaledock-skills --skill well-known-uris`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [draft-mozleywilliams-dnsop-dnsaid-02: DNS for AI Discovery](https://www.ietf.org/archive/id/draft-mozleywilliams-dnsop-dnsaid-02.txt): individual Internet-Draft aimed at dnsop (not adopted), intended Standards Track, -02 (27 May 2026), expires 28 November 2026, posture name, checked 2026-10-09.
- [draft-mozleywilliams-dnsop-dnsaid datatracker page](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-dnsaid/): Active, I-D Exists, latest revision -02, checked 2026-10-09.
- [draft-mozleywilliams-dnsop-dnsaid-01](https://www.ietf.org/archive/id/draft-mozleywilliams-dnsop-dnsaid-01.txt): individual Internet-Draft, superseded, -01 (2 March 2026), for the legacy line, checked 2026-10-09.
- [draft-mozleywilliams-dnsop-dnsaid-00](https://www.ietf.org/archive/id/draft-mozleywilliams-dnsop-dnsaid-00.txt): individual Internet-Draft, superseded, -00 (23 February 2026), for the legacy line, checked 2026-10-09.
- [draft-mozleywilliams-dnsop-bandaid-00: Brokered Agent Network for DNS AI Discovery](https://www.ietf.org/archive/id/draft-mozleywilliams-dnsop-bandaid-00.txt): individual Internet-Draft, replaced by dnsaid, -00 (16 October 2025), history only, checked 2026-10-09.
- [DNS-AID project site](https://dns-aid.org/): project site, informative; still shows the -01 naming pattern, checked 2026-10-09.
- [dns-aid/dns-aid-core](https://github.com/dns-aid/dns-aid-core): reference implementation (Apache-2.0), informative, release v0.28.1 (9 August 2026), main at commit c4944f51 (20 September 2026), checked 2026-10-09.
- [RFC 9460: Service Binding and Parameter Specification via the DNS (SVCB and HTTPS RRs)](https://www.rfc-editor.org/rfc/rfc9460): RFC (Proposed Standard), RFC 9460, checked 2026-10-09.
- [RFC 6698: The DNS-Based Authentication of Named Entities (DANE) TLSA protocol](https://www.rfc-editor.org/rfc/rfc6698): RFC (Proposed Standard), RFC 6698, checked 2026-10-09.
- [RFC 7671: The DANE Protocol: Updates and Operational Guidance](https://www.rfc-editor.org/rfc/rfc7671): RFC (Proposed Standard), RFC 7671, checked 2026-10-09.
- [RFC 9364: DNS Security Extensions (DNSSEC)](https://www.rfc-editor.org/rfc/rfc9364): RFC (Best Current Practice), BCP 237, checked 2026-10-09.
- [RFC 8552: Scoped Interpretation of DNS Resource Records through "Underscored" Naming of Attribute Leaves](https://www.rfc-editor.org/rfc/rfc8552): RFC (Best Current Practice), BCP 222, checked 2026-10-09.
- [RFC 8484: DNS Queries over HTTPS (DoH)](https://www.rfc-editor.org/rfc/rfc8484): RFC (Proposed Standard), RFC 8484, checked 2026-10-09.
