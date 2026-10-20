---
name: cosmosdb-analyze-sdk
description: Analyze Azure Cosmos DB SDK usage in application code, including client lifecycle, connection mode, retries, diagnostics, preferred regions, serialization, partition-key usage, concurrency, and resilience. Use for Java, Python, Node.js, or .NET application integration reviews and runtime issues.
---

# Analyze SDK

1. Identify language, SDK version, client creation pattern, and affected code path.
2. Inspect:
   - client reuse/lifecycle
   - connection mode
   - preferred regions
   - partition-key use
   - retry behavior
   - diagnostics capture
   - concurrency patterns
   - serialization/item IDs
3. Correlate SDK behavior with runtime errors and Cosmos DB metrics.
4. Distinguish SDK misuse from service-side capacity or availability issues.
5. Do not expose keys, connection strings, tokens, or credentials.

## Output
- SDK Configuration
- Code Findings
- Runtime Correlation
- Resilience/Performance Risks
- Recommended Changes
