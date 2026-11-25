---
name: intel-analysis-threat-hunt
description: "Intel Analysis Threat Hunt."
domain: cybersecurity
---

--|
| **Campaign** | STIX object representing a grouping of adversarial behaviors with common objectives over a defined time period |
| **Intrusion Set** | STIX object grouping related intrusion activity by common objectives, even when actor identity is uncertain |
| **Pivot** | Using a single data point (IOC, infrastructure, TTP) to discover related events or adversary artifacts |
| **Clustering** | Machine learning or manual grouping of incidents based on feature similarity to identify campaign boundaries |
| **False Correlation** | Incorrect linking of unrelated incidents due to shared infrastructure (CDNs, shared hosting) or common tools |

## Tools & Systems

- **MISP Correlation Engine**: Automatic correlation of events sharing attribute values across the MISP instance and federated instances
- **OpenCTI Graph**: Interactive relationship graph for visualizing campaign linkages with STIX object types
- **Maltego**: Link analysis for infrastructure and capability pivoting across multiple data sources
- **Neo4j**: Graph database with Cypher queries for large-scale campaign correlation (millions of events)

## Common Pitfalls

- **CDN/Shared hosting false positives**: Cloudflare, AWS CloudFront, and bulletproof hosters serve multiple threat actors. Shared IP alone does not establish campaign linkage.
- **Common malware conflation**: Multiple threat actors use Cobalt Strike. Shared capability does not indicate same actor without additional corroboration.
- **Premature attribution**: Forcing campaign-to-actor attribution before evidence threshold is reached produces incorrect intelligence that persists in reports.
- **Missing temporal analysis**: Events from different years may share infrastructure that was recycled by a different actor, not the same campaign.
