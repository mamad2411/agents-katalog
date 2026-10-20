---
name: kubernetes-api-conventions
description: >-
  Kubernetes API conventions: design Kubernetes resources with spec, status, metadata and conditions. Covers Kubernetes API conventions. Use when designing a Kubernetes API. Triggers: Kubernetes API conventions.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Kubernetes API conventions

The Kubernetes API conventions from the Kubernetes project (SIG Architecture), read from `contributors/devel/sig-architecture/api-conventions.md` in the kubernetes/community repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: API author designing a built-in or custom resource, controller author writing status and conditions, or reviewer of a Kubernetes API change.
- Target version: Kubernetes API conventions (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **API Conventions (introduction).** "Group names must be lower case and be valid DNS subdomains."
2. **Metadata.** "Every object kind MUST have the following metadata in a nested object field called "metadata":"
3. **Spec and Status.** "The PUT and POST verbs on objects MUST ignore the `status` values, to avoid accidentally overwriting the `status` in read-modify-write scenarios."
4. **Spec and Status.** "A `/status` subresource MUST be provided to enable system components to update statuses of resources they manage."
5. **Typical status properties.** "Condition types should be named in PascalCase."
6. **Idempotency.** "All compatible Kubernetes APIs MUST support "name idempotency" and respond with an HTTP status code 409 when a request is made to POST an object that has the same name as an existing object in the system."
7. **Optional vs. Required.** "Fields must be either optional or required."
8. **Serialization Format.** "APIs may return alternative representations of any resource in response to an Accept header or under alternative endpoints, but the default serialization for input and output of API responses MUST be JSON."
9. **Units.** "Duration fields must be represented as integer fields with units being part of the field name (e.g. `leaseDurationSeconds`)."
10. **Naming conventions.** "Go field names must be PascalCase. JSON field names must be camelCase."
11. **Label, selector, and annotation conventions.** "Key prefixes under the "kubernetes.io" and "k8s.io" domains are reserved for use by the kubernetes project and must not be used by third-parties."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] The resource has `spec` and `status`, and writes to `status` go through the `/status` subresource (Spec and Status).
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `json`, `yaml`, `json-patch`, `openapi`, `google-aip`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Kubernetes API conventions](https://raw.githubusercontent.com/kubernetes/community/3bc2da62f72a7a05b8838014be60566668edc3e3/contributors/devel/sig-architecture/api-conventions.md): SIG Architecture convention, main at commit 3bc2da6, 2026-10-06, checked 2026-10-06.
