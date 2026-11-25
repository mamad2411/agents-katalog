---
name: intel-feeds-stixfeed
description: "Intel Feeds Stixfeed."
domain: cybersecurity
---

--|
| **STIX Bundle** | Top-level STIX container object (type: "bundle") holding any number of STIX Domain Objects (SDOs) and STIX Relationship Objects (SROs) |
| **SDO** | STIX Domain Object — core intelligence types: indicator, threat-actor, malware, campaign, attack-pattern, course-of-action |
| **SRO** | STIX Relationship Object — links two SDOs with a labeled relationship (e.g., "uses", "attributed-to", "indicates") |
| **Pattern Language** | STIX pattern syntax for indicator conditions: `[network-traffic:dst_port = 443 AND ipv4-addr:value = '10.0.0.1']` |
| **Marking Definition** | STIX object encoding TLP or statement restrictions on intelligence sharing |
| **added_after** | TAXII 2.1 filter parameter (RFC 3339 timestamp) for incremental polling of new objects |

## Tools & Systems

- **stix2 (Python)**: Official OASIS Python library for creating, parsing, and validating STIX 2.0/2.1 objects
- **taxii2-client (Python)**: Client library for TAXII 2.0/2.1 server discovery, collection enumeration, and object retrieval
- **MISP**: Open-source TIP with native TAXII 2.1 server and client; MISP-TAXII-Server plugin for publishing MISP events
- **OpenCTI**: CTI platform with built-in TAXII 2.1 connector; supports STIX 2.1 import/export natively
- **Cabby**: Legacy Python TAXII 1.x client for older government feeds still on TAXII 1.1

## Common Pitfalls

- **Ignoring `spec_version` field**: STIX 2.0 and 2.1 have incompatible schemas (2.1 adds `confidence`, `object_marking_refs` at bundle level). Always check `spec_version` before parsing.
- **No pagination handling**: TAXII servers cap responses at 100–1000 objects per request. Missing pagination (via `next` link header) causes silent data loss.
- **Clock skew on `added_after`**: Server and client time misalignment causes missed objects at interval boundaries. Use UTC exclusively and add 5-minute overlap windows.
- **Storing raw STIX blobs without indexing**: Storing bundles as opaque JSON prevents querying by indicator type or campaign. Parse into relational or graph database.
- **Sharing TLP:RED content inadvertently**: Automated pipelines must filter marking definitions before routing to any shared platform or SIEM with broad analyst access.
