---
name: copilot-nuget-manager
display_name: Nuget Manager
skill_id: ACU-SKILL-1949
version: 1.0.0
category: cloud-azure
thread: T13
domain: infrastructure
shard_affinity:
  - Marel
layer_access:
  - L5
  - L6
  - L7
sovereignty_score: 8
governance_level: restricted
source_repo: github/awesome-copilot
triggers:

---

# Nuget Manager

## Description
Manage NuGet packages in .NET projects/solutions. Use this skill when adding, removing, or updating NuGet package versions. It enforces using `dotnet` CLI for package management and provides strict procedures for direct file edits only when updating versions.

## Acuterium Integration
- **Thread:** T13 — ACAI V2
- **Shard:** Marel
- **Layers:** L5, L6, L7
- **Governance:** restricted
- **Sovereignty Score:** 8/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/nuget-manager/SKILL.md
- **Author:** GitHub Copilot Community
