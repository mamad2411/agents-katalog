---
name: quality-artifact-verify
description: 'Review build and release artifacts, images and versioned deliverables against their actual inputs, packaging and runtime contracts. Use when asked to validate a deliverable or release. RU: проверка артефакта, релиз, сборка.'
disable-model-invocation: true
---

# Artifact packaging acceptance

Use when the task asks to validate a deliverable, build output, image or versioned release. Establish the candidate, required contents, excluded material, producer, supported build interface, authorized reads and intended consumer. Inventory the actual source inputs, generated files and dependencies; avoid treating a manifest or a clean source tree as proof of what was packaged.

Inspect or build the candidate only within the task's permissions, then compare actual packaged contents and metadata with the required manifest and producer identity. Distinguish tracked source, ignored or untracked deliverables, build context, image contents and running artifact. Verify dependency ownership and licenses when material. A matching filename or checksum proves the corresponding identity or bytes, not that the artifact installs, launches or meets a runtime contract.

When source can change during a build, freeze or otherwise protect the complete admitted input context for the entire producer read, not just an initial checksum. Reconcile any frozen context with the actual runtime baseline and approved changes; a clean snapshot can omit already deployed uncommitted behavior. Bind review and acceptance to the exact candidate and consumed dependencies.

When runtime readiness is in scope and authorized, exercise the real consumer and relevant behavior in a controlled environment. Separate source review, packaging checks, local execution, publication and live rollout; each has independent evidence and authority. Record exact failures and limits, preserve pre-existing work and do not upload, publish or deploy merely because packaging passed. See [deployment operations](../deploy-rollout-run/SKILL.md) for an authorized rollout.
