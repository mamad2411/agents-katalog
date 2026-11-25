---
name: local-knowledge-integration
description: Safely integrate private local knowledge systems using explicit data classification, sanitized fixtures, compatibility checks, and reversible writes. Use before indexing, syncing, retrieving from, migrating, exporting, or changing a personal vault, memory runtime, note template, or knowledge connector.
---

# Local Knowledge Integration

Use this skill before connecting tools to a private vault or changing how personal knowledge is read, indexed, synchronized, or stored.

## Purpose

Protect private notes while allowing safe integration work. Separate the live personal vault, sanitized test fixtures, reusable templates, and derived indexes. This skill is an integration-safety gate; use specialized vault or memory skills for approved day-to-day operations.

## Classify the Data Surface

1. Identify whether the request touches a live personal vault, sanitized fixture, reusable template, derived index/cache, or external connector.
2. Keep live personal vault content outside GitHub, public examples, prompts, attachments, logs, and reusable skills.
3. Treat sanitized fixtures as the default test surface. A fixture must be fictional, minimal, and free of personal names, private notes, credentials, embeddings, and copied vault content.
4. Treat indexes, caches, and runtime memory as derived data unless a contract says otherwise; document how they are regenerated rather than assuming they are authoritative.

## Safe Integration Workflow

1. **State the integration contract.** Name the source of truth, allowed inputs, output location, privacy boundary, and expected degraded behavior when a dependency is unavailable.
2. **Test on a fixture first.** Validate sync, indexing, retrieval, configuration change, and failure behavior with the sanitized fixture before proposing any live-vault action.
3. **Preview all writes.** For migrations, bulk updates, renames, exports, or connector writes, produce a plan, manifest, or diff. Preserve an append-only or restorable path where practical.
4. **Confirm recovery.** Establish what is backed up, how the runtime restarts, and how indexes regenerate before a consequential live change.
5. **Request exact approval.** Name the live-vault paths, transformation, external recipients, retention effect, and rollback method. Do not treat permission to test a fixture as permission to access personal notes.
6. **Record non-secret evidence.** Record contract decisions and pass/fail results without copying note content, retrieval output, credentials, or raw embeddings.

## Hard Stops

Stop and request clarification when an operation would export or commit live notes, send personal content to an unapproved external service, delete or overwrite vault files without recovery evidence, merge a fixture with live content, or rely on a memory cache as the only source of truth.

## Representative Scenario

**Request:** “Connect a new retrieval tool to my second brain.”

**Route:** Define the permitted data path and failure behavior; create or use a fictional fixture; test indexing and a representative query; document rebuild and index-regeneration steps; then request a separate approval before any live-vault connector, sync, or export is configured.

## Companion Skills

- Use `memory-layer-bridge` to route recall and durable decision logging to the correct layer.
- Use `obsidian-vault-manager` for approved day-to-day note operations.
- Use `obsidian-vault-architect` for approved structural redesigns.
- Use `portfolio-governance` to keep reusable behavior, declared configuration, and live personal content in separate owners.
