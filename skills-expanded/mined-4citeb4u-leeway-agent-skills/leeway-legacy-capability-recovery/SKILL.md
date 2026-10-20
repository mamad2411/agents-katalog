---
name: leeway-legacy-capability-recovery
description: Recovers useful Agent Lee skills, MCPs, adapters, models, contracts, and verified patterns from historical LeeWay repositories without bulk-copying duplicates, stale paths, secrets, simulated success, or unverified claims into the canonical system.
license: MIT
metadata:
  authority: Creator/Human Authority > canonical LeeWay repository authority
  mode: capability-recovery-governance
  factory: skills/leeway-skill-factory/SKILL.md
  lifecycle: skills/leeway-skill-lifecycle-governance/SKILL.md
---

# LeeWay Legacy Capability Recovery

## Purpose

Turn old Agent Lee work into current portable capabilities while keeping provenance and execution truth intact.

`discover → classify → deduplicate → normalize → qualify → promote → register → re-enumerate`

## Required classification

Classify every recovered artifact as one of:

- `SKILL`
- `MCP_SERVER`
- `MCP_TOOL`
- `ADAPTER`
- `CONTRACT`
- `MODEL_OR_MODEL_CACHE`
- `TEST_OR_RECEIPT`
- `GENERATED_STUB`
- `PLACEHOLDER_OR_SIMULATION`
- `HISTORICAL_DECLARATION`

Also record its evidence state:

- `SOURCE_IMPLEMENTED`
- `DEPENDENCIES_PRESENT`
- `ADAPTER_CONFIGURED`
- `RUNTIME_RESPONDED`
- `EXECUTED_UNVERIFIED`
- `VERIFIED`
- `BLOCKED`
- `FAILED`

## Recovery law

Do not bulk-copy a repository because it contains a large skill count or a production-ready label. For each candidate:

1. bind repository, branch, commit and source path;
2. inspect imports, dependencies, credentials and provider assumptions;
3. compare semantic ownership with the canonical skill graph;
4. preserve one canonical owner and register subordinate adapters/tools;
5. replace absolute roots with logical configuration;
6. retain security and approval boundaries;
7. run negative tests as well as the success path;
8. record the qualified platform and remaining dependencies;
9. update the capability universe and provider graph;
10. resume the original user acceptance gate.

## Rejection rules

Do not promote:

- scripts that only write their own PASS record;
- mock or simulated provider success;
- generated agents with empty tool bodies;
- registries without corresponding implementation;
- unsafe shell interpolation;
- copied credentials or secrets;
- host-path identity;
- voice adapters that bypass canonical Voice Fabric;
- device control that bypasses Device Bridge authority;
- Formula values manufactured outside canonical Formula authority.

## Promotion choices

Choose one:

- `REUSE_CANONICAL`
- `EXTEND_CANONICAL`
- `PROMOTE_PORTABLE_CONTRACT`
- `CREATE_PROVIDER_ADAPTER`
- `REGISTER_MCP_TOOL`
- `KEEP_HISTORICAL_EVIDENCE`
- `QUARANTINE`
- `RETIRE_DUPLICATE`

Skill Factory and Lifecycle Governance remain the promotion authorities. This skill supplies the recovery procedure and evidence discipline.
