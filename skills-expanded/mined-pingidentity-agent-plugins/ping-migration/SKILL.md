---
name: ping-migration
description: "Use when migrating identity applications from PingFederate or PingOne for Enterprise (P14E) to PingOne — running a migration, assessing readiness, planning waves, classifying apps as direct/redesign/out-of-scope, mapping grant types and entities to PingOne equivalents, post-migration secrets, rollback and cutover, or extending the bundled orchestrator's adapters."
compatibility: "Requires Node.js 18+ and pingcli on PATH, authenticated at least once so ~/.pingcli/config.yaml exists. Runs against live source admin APIs (requires a valid PingCLI profile defined and authenticated for the source - more detail on profiles at: https://developer.pingidentity.com/pingcli/using_pingcli/managing-configuration-profiles.md) or a pre-exported source file. Mutates the destination PingOne environment, using a PingCLI profile defined and authenticated for the destination, except under --dry-run. Fetch live documentation for current product details — live documentation overrides local reference files."
metadata:
  publisher: Ping Identity
  version: "2.1.0"
  product_family: cross-platform
---

# Ping Migration

Application-level migration from a source system (PingFederate, PingOne for Enterprise) to a destination (PingOne). Bundles a migration orchestrator that extracts, classifies, applies, and validates applications in one command, plus the classification rules, assessment and wave-planning method, and rollback design for everything the orchestrator does not automate.

## When to use this skill

- Migrating OAuth clients, SAML SP connections, or IdP connections off PingFederate or P14E into PingOne
- Assessing migration readiness, or previewing what would be migrated without changing anything
- Planning migration waves, sequencing, acceptance criteria, or validation gates
- Deciding whether a specific app can migrate directly, needs redesign, or is out of scope
- Mapping PingFederate grant types, entities, or auth policy topology to PingOne equivalents
- Designing rollback or cutover, or rolling back a completed migration run
- Understanding what the bundled orchestrator does, or extending a source/destination adapter

## When NOT to use this skill

- Choosing which migration track applies at all (SDK code vs. server/SaaS vs. PingFederate → PingOne)
- Migrating SDK code from ForgeRock SDKs to Ping Orchestration SDKs → https://developer.pingidentity.com/orchsdks/journey/migration.md
- Routine platform setup unrelated to a migration (create an environment, register an app) → the PingOne admin console and https://docs.pingidentity.com/
- Re-creating a journey or DaVinci flow in the destination → the destination platform's flow-design documentation

## Execution rules (unattended)

This skill is agent-first: no user is expected to be present. Resolve missing values from the task prompt, the environment (existing `pingcli` profiles, a pre-exported source file), and the reference files — not by waiting for an answer.

- Always run `--dry-run` first. It classifies and writes the assessment report without applying anything, and with `--import-file` it needs no credentials at all.
- Never pause for optional detail. Derive sensible values (work directory, environment name, wave counts) from context and state them in the output.
- Stop and report only when a required value has no derivable source — name the missing value and the command that needs it, then stop.
- Secrets are supplied out-of-band: `PINGONE_CLIENT_SECRET` for the secret script, never a command-line flag.
- Tool order: `pingcli` (check with `which pingcli`) → bundled orchestrator in `scripts/` → general guidance.

## Bundled scripts

| Script                             | Purpose                                                     |
| ---------------------------------- | ----------------------------------------------------------- |
| `scripts/ping-migration.js`        | Migration orchestrator — extract, classify, apply, validate |
| `scripts/rollback.js`              | Delete every resource recorded in a migration report        |
| `scripts/pingone-client-secret.js` | Read or set PingOne application and resource client secrets |
| `scripts/classifier.js`            | Classification logic — the single source/destination seam   |
| `scripts/reports.js`               | Assessment and migration report generation                  |
| `scripts/adapters/sources/`        | `pf-adapter.js`, `p14e-adapter.js`                          |
| `scripts/adapters/destinations/`   | `pingone-adapter.js`                                        |

## Routing by agent intent

References are layered by intent so a task loads only what it needs: `playbooks/` for step-by-step execution, `blueprints/` for architecture and topology, `catalogs/` for lookup tables, `examples/` for evaluation prompts.

| Task | Reference |
|---|---|
| Run a migration — flags, invocation, run sequence, outputs, exit codes | `references/playbooks/run-migration.md` |
| Assess readiness, plan waves, build a risk register, define validation gates, design cutover | `references/playbooks/assessment-and-wave-planning.md` |
| Roll back a run, rotate secrets, or work the manual follow-up list | `references/playbooks/post-migration-and-rollback.md` |
| Understand the pipeline, canonical item model, or adapter interfaces | `references/blueprints/migration-architecture.md` |
| Scope which PingFederate entities are in or out of an automated run; auth policy topology | `references/blueprints/pingfederate-migration-inventory.md` |
| Understand why an item was classified direct / redesign / out-of-scope; grant-type mapping | `references/catalogs/classification-rules.md` |
| A P14E-sourced field came out empty or null; extend the P14E adapter | `references/catalogs/p14e-admin-api-mapping.md` |
| Evaluate routing or playbook behavior against known-good prompts | `references/examples/sample-prompts.md` |

Sources are `pingfederate`, and `p14e`; destinations are `pingone`. Each source extracts either live from its own admin API or from a pre-exported native file via `--import-file`.

Per-source extraction mechanisms, native file formats, apply mechanisms, and the full flag reference: `references/playbooks/run-migration.md`.
