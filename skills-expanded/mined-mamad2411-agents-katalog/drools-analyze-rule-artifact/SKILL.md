---
name: drools-analyze-rule-artifact
description: Analyze Drools KJAR/rule artifacts, Maven coordinates, versions, KieModule packaging, dependencies, compilation, and runtime artifact selection. Use for wrong-rule-version incidents, packaging failures, build issues, or artifact-governance investigations.
---

# Analyze Rule Artifact

1. Identify expected rule artifact, version, source revision, and target environment.
2. Inspect KJAR/KieModule packaging and relevant Maven dependencies.
3. Compare expected artifact/version with what the application actually loads.
4. Check compilation/build failures and dependency conflicts.
5. Correlate artifact changes with deployment and rule-behavior changes.
6. Do not promote or replace production artifacts unless explicitly authorized.

## Output
- Expected Artifact
- Loaded/Deployed Version
- Packaging/Dependency Findings
- Version Drift
- Recommended Action
