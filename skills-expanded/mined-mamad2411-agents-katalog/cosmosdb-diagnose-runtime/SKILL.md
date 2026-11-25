---
name: cosmosdb-diagnose-runtime
description: Diagnose Azure Cosmos DB runtime incidents end-to-end across account configuration, partitions, queries, indexing, RU/throttling, SDK behavior, consistency, regions, change feed, security, and application evidence. Use as the primary Cosmos DB incident skill when the failure domain is not yet known.
---

# Diagnose Runtime

1. Read `.digital-platform-ai/cosmosdb.yaml`, service metadata, dependencies, environment metadata, and relevant service instructions.
2. Resolve account, database, containers, region, and application path.
3. Gather independent evidence in parallel where possible:
   - account/region state
   - RU/throttling metrics
   - partition metrics
   - query diagnostics
   - application/SDK diagnostics
   - DataDog traces/logs
4. Route to focused Cosmos DB skills based on evidence.
5. Correlate the first confirmed failure rather than the loudest downstream symptom.
6. Separate:
   - application misuse
   - data model/partitioning issue
   - query/index issue
   - capacity/throttling
   - regional/consistency issue
   - platform/access issue
7. Do not mutate production resources unless explicitly authorized.

## Output
- Incident Scope
- First Confirmed Failure
- Supporting Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
