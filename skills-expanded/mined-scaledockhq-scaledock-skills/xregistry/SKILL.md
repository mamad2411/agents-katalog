---
name: xregistry
description: >-
  xRegistry: manage and discover metadata for message, schema and endpoint registries. Covers xRegistry 1.0-rc4 (build). Use when managing metadata with xRegistry. Triggers: xRegistry.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# xRegistry

The xRegistry core specification from the xRegistry project (a CNCF sandbox project that grew out of the CloudEvents Discovery work), read from `core/spec.md` in the xregistry/spec repository at the v1.0-rc4 release candidate.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Registry server implementer, client or tool that reads, writes or exports xRegistry entities, or author of a domain-specific registry model.
- Target version: xRegistry 1.0-rc4 (current, posture: build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Notational Conventions.** "Server-unknown extension attributes MUST be silently stored in the backing datastore."
2. **Version.** "Each Resource MUST have at least one Version associated with it."
3. **Registry Model.** "Unless otherwise stated in a protocol binding specification, if the processing of a request fails (even during the generation of the response) then an error MUST be generated and the entire request MUST be undone."
4. **`<SINGULAR>id` (`id`) Attribute.** "This attribute MUST be named `registryid` for the Registry itself, and MUST be named `versionid` for all Version entities."
5. **`xid` Attribute.** "Unlike `<SINGULAR>id`, which is unique within the scope of its parent, `xid` MUST be unique across the entire Registry, and as such is defined to be a relative URL from the root of the Registry."
6. **`epoch` Attribute.** "Each time the associated entity is updated, this value MUST be set to a new value that is greater than the current one."
7. **Registry Capabilities.** "When serializing their supported capabilities, servers MUST include all capabilities (including extensions) since the absence of a capability indicates lack of support for that feature."
8. **Updating Nested Registry Collections.** "Any error while processing a nested collection entity MUST result in the entire request being rejected."
9. **Meta Entity.** "Each Resource MUST have a Meta entity, and when the Resource is deleted then the Meta entity MUST also be deleted."
10. **`defaultversionsticky` Attribute.** "A value of `true` means that `defaultversionid` has been explicitly set and its value MUST NOT automatically change if other Versions are added or removed."
11. **`ancestorid` Attribute.** "The `ancestorid` attribute MUST be set to the case-sensitive `versionid` of this Version's ancestor."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cloudevents`, `asyncapi`, `json-schema`, `openapi`, `uri`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [xRegistry Service - Version 1.0-rc4](https://raw.githubusercontent.com/xregistry/spec/508cd2760a3c5b74adf61acac1e94654f9852f34/core/spec.md): Release candidate, 1.0-rc4 (tagged v1.0-rc4, 2026-08-19), main at commit 508cd27, checked 2026-10-06.
