---
name: cloud-migration
description: "Cloud migration strategy: 6 Rs (Rehost, Replatform, Refactor, Repurchase, Retain, Retire), AWS/GCP landing zones, and cutover execution"
category: migration
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/migration/cloud-migration/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Cloud Migration Architecture

## Scope
Planning and executing enterprise workload migrations from on-premises data centers to public cloud environments (AWS, Azure, GCP).

## The 6 Rs Migration Strategies (Gartner / AWS)
1. **Rehost (Lift and Shift)**: Moving applications without architectural changes.
2. **Replatform (Lift, Tinker, and Shift)**: Making minor optimizations (e.g., migrating database to managed RDS).
3. **Refactor / Re-architect**: Redesigning application using cloud-native microservices and serverless architectures.
4. **Repurchase (Drop and Shop)**: Replacing custom legacy systems with SaaS solutions.
5. **Retain**: Keeping critical or unmovable applications in on-premises data centers.
6. **Retire**: Decommissioning redundant or obsolete applications.

## Cutover Planning & Zero Downtime
- Continuous data synchronization using replication agents; phased cutover using DNS weighting (Route 53) and rollback plans.

## Standards & Tools
- **Tools**: AWS Application Migration Service (MGN), Azure Migrate, GCP Migrate to Containers.
