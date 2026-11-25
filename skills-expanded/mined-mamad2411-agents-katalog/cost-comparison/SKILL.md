# Cost Comparison — Multi-Cloud Network Pricing Analysis

## Overview

Network costs — particularly egress charges — are often the most underestimated component of multi-cloud architectures. Treat any numeric examples as illustrative only: pricing varies by region, tier, commitment, currency, and date. For production estimates, use the official calculators and export assumptions with the design review.

## Current Pricing Sources

| Cloud | Primary calculators / pricing pages | What to verify |
|---|---|---|
| Azure | Azure Pricing Calculator; Bandwidth, ExpressRoute, VPN Gateway, Azure Firewall, Front Door pricing pages | Zone/region pair, meter name, ExpressRoute data plan, gateway SKU |
| AWS | AWS Pricing Calculator; Data Transfer, Direct Connect, Site-to-Site VPN, Transit Gateway, VPC Endpoint pricing pages | Cross-AZ, inter-region, public internet, TGW processing, PrivateLink hourly/data charges |
| GCP | Google Cloud Pricing Calculator; Network Data Transfer, Cloud VPN, Cloud Interconnect, Private Service Connect pricing pages | Premium vs Standard tier, inter-region pair, Cloud NAT/LB processing, Interconnect egress class |

## Pricing Model Guidance

| Cost area | Model to compare | Design implication |
|---|---|---|
| Ingress | Usually free, but confirm service-specific processing charges | Do not assume the receiving service has no per-request or processing fee |
| Same-zone / same-AZ | Often free or cheapest path | Co-locate chatty tiers where resilience requirements allow |
| Cross-zone / cross-AZ | Frequently charged per GB, sometimes each direction | Avoid unnecessary east-west replication and topology-unaware scheduling |
| Inter-region | Region-pair dependent and materially higher than intra-region | Keep stateful dependencies regional; replicate asynchronously where possible |
| Internet egress | Tiered by volume and destination | Model blended rates at expected monthly volume, not a single list price |
| Private circuits | Fixed port/circuit/gateway fees plus metered or included transfer | Usually wins only at sustained volume or for deterministic latency/compliance |
| Transit services | Hourly attachment plus per-GB processing in many clouds | Centralized transit simplifies operations but can add a data-processing tax |
| Private endpoints | Hourly endpoint/service charges plus per-GB processing | Include both producer and consumer side charges in multi-account designs |

## Cost Comparison for Common Scenarios

Use scenario models instead of fixed tables that age quickly:

1. **Low volume (<5 TB/month):** VPN or public egress is often cheaper because private circuits add fixed monthly port, circuit, and gateway costs.
2. **Moderate volume (5–50 TB/month):** Compare internet egress against private circuit metered egress plus fixed costs; break-even is cloud-pair and region dependent.
3. **High volume (50+ TB/month):** Private connectivity, CDN offload, committed bandwidth, or data-locality redesign usually provides material savings.
4. **Chatty east-west systems:** Cross-zone and transit processing fees can exceed internet egress; model packet path and both directions.

**Break-even analysis:** Calculate `monthly fixed connectivity cost + metered private transfer` versus `standard egress + VPN/transit processing`. Re-run the calculation whenever regions, providers, or traffic mix change.

## Cross-Cloud Data Transfer Optimization Strategies

**CDN Offload:** Serve cacheable content (static assets, API responses with appropriate cache headers) through Azure Front Door, CloudFront, or Cloud CDN. CDN egress rates are typically lower than standard compute egress, and cache hits eliminate origin egress entirely.

**Compression:** Enable gzip or Brotli compression on all cross-cloud API traffic. For typical JSON/XML payloads, compression reduces transfer volume by 60–80%, directly reducing egress costs.

**Caching at Boundary:** Deploy Redis or Memcached at the receiving cloud boundary to cache frequently accessed data from the source cloud. This reduces repetitive cross-cloud fetches. Example: cache database query results from Azure SQL in an AWS ElastiCache cluster co-located with the consuming application.

**Data Locality:** Place data stores in the same cloud as their primary consumers. Avoid architectures where the database is in one cloud and the application tier is in another — this generates continuous cross-cloud egress. Use event-driven replication (Change Data Capture, event streams) to synchronize data across clouds asynchronously rather than synchronous cross-cloud reads.

**Committed Use Discounts:** AWS offers Data Transfer bundles with CloudFront for reduced egress rates. GCP offers committed use discounts for Interconnect bandwidth. Azure offers unlimited data ExpressRoute circuits that cap egress costs regardless of volume. Evaluate committed pricing against on-demand rates for predictable workloads.

**Minimize Inter-AZ Transfer on AWS:** AWS charges $0.01/GB per direction for inter-AZ traffic. For high-throughput distributed systems (Kafka, Cassandra, Elasticsearch), prefer single-AZ placement for non-critical workloads or use topology-aware scheduling (e.g., Kubernetes topology spread constraints) to minimize cross-AZ traffic.

**Analysis only — verify against vendor documentation before applying.**
