---
name: google-aip
description: >-
  Google AIPs: design resource-oriented APIs by the Google API Improvement Proposals. Covers AIPs. Use when designing an API with Google AIP guidance. Triggers: AIP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# AIP

The general API Improvement Proposals (AIPs) published by Google at google.aip.dev, read from the Markdown sources in the aip-dev/google.aip.dev repository: AIP-121 resource-oriented design, AIP-122 resource names, AIP-131 to AIP-135 standard methods, AIP-158 pagination, AIP-180 backwards compatibility and AIP-193 errors.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: API designer or reviewer of a gRPC or HTTP API that follows the AIPs, or author of a linter or client library that enforces them.
- Target version: AIPs (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **AIP-121 § Methods.** "A resource **must** support at minimum [Get][]: clients must be able to validate the state of resources after performing a mutation such as [Create][], [Update][], or [Delete][]."
2. **AIP-122 § Guidance.** "All resource names defined by an API **must** be unique within that API."
3. **AIP-122 § Resource ID aliases.** "However, all data returned from the API **must** use the canonical resource name."
4. **AIP-131 § Guidance.** "APIs **must** provide a get method for resources."
5. **AIP-132 § Guidance.** "APIs **must** provide a `List` method for resources unless the resource is a [singleton][]."
6. **AIP-133 § User-specified IDs.** "An API **must** allow a user to specify the ID component of a resource (the last segment of the resource name) on creation if the API is operating on the [management plane][]."
7. **AIP-134 § Request message.** "If partial resource update is supported, a field mask **must** be included."
8. **AIP-135 § Errors.** "Permission **must** be checked prior to checking if the resource exists."
9. **AIP-158 § Opacity.** "Page tokens provided by APIs **must** be opaque (but URL-safe) strings, and **must not** be user-parseable."
10. **AIP-180 § Adding components.** "New required fields **must not** be added to existing request messages or resources."
11. **AIP-193 § Status.details.** "All error responses **must** include an `ErrorInfo` within `details`."

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

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `protobuf`, `grpc`, `http-semantics`, `kubernetes-api-conventions`, `microsoft-rest-api-guidelines`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [AIP-121: Resource-oriented design](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0121.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-122: Resource names](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0122.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-131: Standard methods: Get](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0131.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-132: Standard methods: List](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0132.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-133: Standard methods: Create](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0133.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-134: Standard methods: Update](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0134.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-135: Standard methods: Delete](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0135.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-158: Pagination](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0158.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-180: Backwards compatibility](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0180.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
- [AIP-193: Errors](https://raw.githubusercontent.com/aip-dev/google.aip.dev/23e176e7333ea3bc6b085f9950a5da03d2bbfc72/aip/general/0193.md): Approved AIP, master at commit 23e176e, 2026-08-17, checked 2026-10-06.
