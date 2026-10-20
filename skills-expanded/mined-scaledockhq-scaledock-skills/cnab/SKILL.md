---
name: cnab
description: >-
  CNAB: The Cloud Native Application Bundle (CNAB) is a _standard packaging format_ for multi-component distributed applications. Covers CNAB 1.2.0. Use when packaging a cloud native application bundle. Triggers: CNAB.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# CNAB

Cloud Native Application Bundle Core 1.2.0 (CNAB1) from the CNAB project: the overview, the bundle.json file and the invocation image chapters, read from the cnabio/cnab-spec repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Bundle author, or CNAB runtime or tooling that reads bundle.json and runs invocation images.
- Target version: CNAB 1.2.0 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Summary.** "However, as a signed bundle definition represents an immutable bundle, all invocation images and images references must have a content digest."
2. **Approach.** "Credentials are injected into the invocation image, but they MUST NOT be stored."
3. **Key Terms.** "A runtime MUST support the 'install', 'upgrade', and 'uninstall' actions, while bundle tooling MAY choose not to implement 'upgrade'."
4. **Schema Version.** "Every `bundle.json` MUST have a `schemaVersion` element."
5. **Invocation Images.** "A CNAB bundle MUST have at least one invocation image."
6. **Definitions.** "Indicates that the value of the parameter is sensitive and MUST NOT be written to insecure locations such as log files or user-facing output."
7. **Custom Actions.** "The built-in actions (`install`, `upgrade`, `uninstall`) MUST NOT appear in the `actions` section, and an implementation MUST NOT allow custom actions named `install`, `upgrade`, or `uninstall`."
8. **Custom Extensions.** "Tools MUST NOT define additional fields anywhere else in the bundle descriptor."
9. **The `/cnab` Directory.** "An invocation image MUST have a directory named `cnab` placed directly under the root of the file system hierarchy inside of an image."
10. **The Run Tool.** "The run tool MUST be located at the path `/cnab/app/run`."
11. **The Run Tool.** "It MUST react to the `CNAB_ACTION` provided to it."

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

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `oci`, `json-schema`, `semver`, `json-canonicalization`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CNAB Core 1.2.0: overview](https://raw.githubusercontent.com/cnabio/cnab-spec/5771c874bedce48f5762a40becc984d55116b8b7/100-CNAB.md): Specification, CNAB Core 1.2.0 (main at commit 5771c87, 2021-09-15), checked 2026-10-06.
- [CNAB Core 1.2.0: the bundle.json file](https://raw.githubusercontent.com/cnabio/cnab-spec/5771c874bedce48f5762a40becc984d55116b8b7/101-bundle-json.md): Specification, CNAB Core 1.2.0 (main at commit 5771c87, 2021-09-15), checked 2026-10-06.
- [CNAB Core 1.2.0: the invocation images](https://raw.githubusercontent.com/cnabio/cnab-spec/5771c874bedce48f5762a40becc984d55116b8b7/102-invocation-image.md): Specification, CNAB Core 1.2.0 (main at commit 5771c87, 2021-09-15), checked 2026-10-06.
