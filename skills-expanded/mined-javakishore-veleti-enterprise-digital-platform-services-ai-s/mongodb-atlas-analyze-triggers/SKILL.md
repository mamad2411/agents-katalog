---
name: mongodb-atlas-analyze-triggers
description: Analyze MongoDB Atlas Triggers and related event workflows where available, including lifecycle, retries, idempotency, and modernization risk. Use for MongoDB Atlas-specific engineering and operational tasks where the managed Atlas platform is material to the answer.
---

# Analyze Triggers

1. Read `.digital-platform-ai/mongodb-atlas.yaml`, service metadata, environments, and relevant instructions.
2. Resolve the MongoDB Atlas organization/project, deployment, cloud provider, region, environment, and consuming application context.
3. Gather the Atlas configuration and runtime evidence relevant to this task before drawing conclusions.
4. Distinguish MongoDB database behavior from Atlas-managed platform behavior, cloud-provider networking, and application behavior.
5. Verify feature availability, tier/provider/region support, engine version, and current product lifecycle before recommending Atlas-specific capabilities.
6. Route related investigations to other `mongodb-atlas-*` skills, `datadog-*`, or application/framework skills when evidence crosses boundaries.
7. Do not mutate production resources unless explicitly authorized. Never expose credentials, API keys, tokens, or sensitive connection strings.

## Output
- Scope
- Observed Evidence
- Findings
- Platform vs Application Assessment
- Recommended Action
- Remaining Unknowns
