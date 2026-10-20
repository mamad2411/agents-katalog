---
name: mongodb-analyze-schema
description: Analyze MongoDB document schema and data modeling, including embedding vs references, document growth, arrays, schema validation, access patterns, denormalization, and shard/index implications. Use for application data-model design or performance problems.
---

# Analyze Schema

1. Identify dominant read/write access patterns and document relationships.
2. Inspect document size/growth, arrays, cardinality, update patterns, and validation rules.
3. Evaluate embedding versus references based on atomicity and access locality.
4. Correlate schema choices with indexes, shard keys, and query targeting.
5. Avoid relational normalization rules that conflict with document access patterns.
6. Preserve business consistency requirements.

## Output
- Access Patterns
- Current Data Model
- Growth/Atomicity Findings
- Index/Sharding Impact
- Recommended Model Changes
