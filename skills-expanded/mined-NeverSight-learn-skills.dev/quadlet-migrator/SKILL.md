---
name: quadlet-migrator
description: Convert docker run commands, Docker Compose configurations, or self-hosting deployment assets into reviewable Podman Quadlet output, preserve env/support files, and guide users through planning, review, generation, and validation.
---

# Quadlet Migrator

Use this skill when the user wants to migrate `docker run`, `docker compose`, or repository-based self-hosting deployment assets into Podman Quadlet output.

This skill is for review-first migration work. It is responsible for choosing the right source inputs, preserving required runtime assets, reducing deployment decisions to a small confirmed set, and producing maintainable Quadlet artifacts.

Do not rely on `podlet` as an execution dependency. You may use it only as prior-art knowledge, not as part of the workflow.

## Core Defaults

- Use the lightest mode that satisfies the request.
- Prefer reviewable output in the current working directory unless the user requested another output location or an existing-file conflict requires a decision.
- Prefer runnable and maintainable output over mechanical one-to-one translation.
- Preserve required env files, mounted config, initialization assets, and helper scripts when they are part of the deployment.
- Read docs, comments, and example values yourself; ask the user only about high-impact deployment decisions.
- Do not invent deployment-specific values.
- Keep detailed mapping and validation logic in `references/` instead of restating it in the main skill file.

## Modes

- `advice`: explain mappings, review inputs, or answer focused migration questions without writing final artifacts
- `design`: perform planning and finalize review, then stop before writing runnable artifacts
- `generate`: perform planning, finalize review, and execution, then write the approved artifacts

Do not force `generate` mode when the user only wants explanation, review, or a partial conversion.

## Workflow

The workflow has three phases: `Planning`, `Finalize`, and `Execution`.

- `advice` usually stays in planning or answers a focused question directly
- `design` uses planning and finalize
- `generate` uses all three phases

Do not skip phase boundaries when a full workflow is in play.

### Planning

Goal: understand the source inputs, choose the source of truth, identify required runtime assets, and resolve the decisions that actually need user confirmation.

In planning:

1. Classify the input.
2. Find the canonical deployment entry point.
3. Build a semantic model of services, images/builds, ports, storage, networks, env sources, dependencies, and required support files.
4. Identify unresolved deployment decisions and ask the user about them.
5. Summarize what you learned and state the proposed reviewable output location before moving on.

Planning is where you must ask about unresolved high-impact values. The following must be explicitly confirmed before leaving planning:

- **Deployment mode** (rootless vs rootful) — determines Quadlet target directory, systemctl scope, linger requirement, and helper-script behavior.
- **Volume strategy** (named volume vs bind mount vs `.volume` unit) — determines whether `.volume` files are generated and how mount paths are written.
- Domains, host paths, credentials, optional services, and output-location conflicts.
- **Host port availability** — when `PublishPort=` is used, detect whether the host-side port is already occupied before proceeding.

If the source has many env variables, reduce them to a small decision list instead of dumping raw templates back to the user.

Do not leave planning until the canonical input set and the important unresolved decisions are clear enough for a coherent design review.

### Finalize

Goal: freeze the design that planning established and ask the user to review it in conversation.

Finalize is not a second discovery pass. Do not use it to introduce first-time major choices.

In finalize:

1. Freeze the chosen service set and topology.
2. Freeze storage, image, env, and output-location decisions.
3. Confirm the reviewed artifact set, including support files and env files, not only Quadlet units.
4. Present a concise design snapshot and ask the user to approve it or request edits.

Do not start execution until the user has reviewed and confirmed the finalize snapshot.

### Execution

Goal: write the approved artifacts.

Before writing any file, confirm that the user has explicitly approved the finalize snapshot. If the finalize phase was skipped or the user has not confirmed, stop and ask.

In execution:

1. Generate the approved Quadlet files.
2. Generate env files or env deltas only when needed for the approved output.
3. Generate helper scripts only when they materially help the user apply or operate the result.
4. Include required support files and directories in the reviewed deliverable set.
5. Add deployment notes or validation guidance when they materially help the user operate the result.

If implementation reveals a material conflict with the approved design, stop and return to planning instead of silently diverging.

## Hard Stops

Stop and ask the user before finalizing or generating runnable output when any of these remain unresolved:

- required secrets, external URLs, host paths, or other deployment-specific values
- multiple plausible source inputs with no confident canonical entry point
- image strategy versus local build strategy when the difference materially affects the result
- a lossy mapping that would change runtime behavior in an important way
- output-location conflicts or overwrite strategy for files that already exist
- required support files or directories referenced by mounts, docs, commands, or scripts
- required env values for minimal startup
- likely env-key typos or mismatches
- host port conflicts when `PublishPort=` is used — detect occupied host ports before finalizing
- unresolved deployment mode (rootless vs rootful)
- unresolved volume strategy (named volume vs bind mount vs `.volume` unit)
- a mismatch between deployment mode and the intended operator model or file locations

Do not keep moving forward by guessing through these gaps.

If a structured input tool is unavailable, ask the user directly in conversation before proceeding. Do not substitute defaults for unresolved high-impact decisions.

## Decision Priority

When rules or signals conflict, use this priority order:

1. the user's explicit request
2. the source project's documented canonical deployment path
3. runnable and safe output
4. maintainable output
5. defaults in this skill and its references

If a lower-priority default conflicts with a higher-priority source of truth, follow the higher-priority source and say so briefly.

## Reference Routing

Use the reference files for detailed rules instead of duplicating them here:

- `references/github-repo-intake.md` for repository discovery and source-of-truth selection
- `references/compose-mapping.md` for Compose field mapping, topology, naming, network, storage, and runtime-identity defaults
- `references/env-strategy.md` for `.env`, `env_file`, interpolation, sensitive values, completeness checks, and typo detection
- `references/deployment-notes.md` for rootless/rootful deployment, helper scripts, apply flow, and operational notes
- `references/validation.md` for validation, troubleshooting, and runnable-output checks

When Quadlet option semantics or supported behavior are unclear, treat `references/podman-systemd.unit.5.md` as the authoritative source.

## Collaboration Rules

- Confirm deployment-specific values that materially affect connectivity, credentials, storage, or topology.
- Keep the user's review burden small by summarizing decisions instead of forwarding raw upstream material.
- Distinguish between upstream example values and user-confirmed values.
- Preserve placeholders when the user has not provided final values yet, and do not describe the result as runnable when required values are still unresolved.

## Validation Reminder

When the user wants runnable output, make sure the final artifact set includes the required support files and env sources, and point the user to the deployment and validation references as needed.
