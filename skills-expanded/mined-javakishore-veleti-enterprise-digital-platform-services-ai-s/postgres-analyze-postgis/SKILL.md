---
name: postgres-analyze-postgis
description: Analyze PostGIS on Azure Database for PostgreSQL Flexible Server, including spatial types, SRIDs, GiST/SP-GiST indexes, spatial queries, transformations, performance, and extension compatibility. Use for geospatial PostgreSQL workloads.
---

# Analyze PostGIS

1. Verify PostGIS version/support for the target server.
2. Identify geometry/geography types, SRIDs, query patterns, and spatial predicates.
3. Inspect spatial index usage and coordinate transformations.
4. Correlate query performance with selectivity and geometry complexity.
5. Validate data-quality and SRID assumptions before tuning.
6. Do not enable/change production extensions without authorization.

## Output
- Spatial Model
- Index/Query Findings
- SRID/Data Quality
- Performance Findings
- Recommended Action
