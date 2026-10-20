---
name: compose-spec
description: >-
  Compose specification: write compose.yaml files that define multi-container applications. Covers Compose file. Use when writing a Compose file. Triggers: Compose, docker compose.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Compose specification

The Compose Specification from the compose-spec project: the application model, the services, networks and volumes top-level elements, interpolation and merge rules, read from the numbered Markdown files in the compose-spec/compose-spec repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Compose file author, or a Compose implementation that parses, merges and runs Compose files.
- Target version: Compose file (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **The Compose application model.** "Project names must contain only lowercase letters, decimal digits, dashes, and underscores, and must begin with a lowercase letter or decimal digit."
2. **Compose file.** "The default path for a Compose file is `compose.yaml` (preferred) or `compose.yml` that is placed in the working directory."
3. **Version top-level element (obsolete).** "The top-level `version` property is defined by the Compose Specification for backward compatibility. It is only informative you'll receive a warning message that it is obsolete if used."
4. **Services top-level element.** "A Compose file must declare a `services` top-level element as a map whose keys are string representations of service names, and whose values are service definitions."
5. **image.** "`image` must follow the Open Container Specification [addressable image format](https://github.com/opencontainers/org/blob/master/docs/docs/introduction/digests.md), as `[<registry>/][<project>/]<image>[:<tag>|@<digest>]`."
6. **ports.** "Port mapping must not be used with `network_mode: host`."
7. **secrets.** "Defining a secret in the top-level `secrets` must not imply granting any service access to it."
8. **external.** "All other attributes apart from name are irrelevant. If Compose detects any other attribute, it rejects the Compose file as invalid."
9. **Extension.** "Compose ignores any fields that start with `x-`, this is the sole exception where Compose silently ignores unrecognized fields."
10. **Interpolation.** "If Compose can't resolve a substituted variable and no default value is defined, it displays a warning and substitutes the variable with an empty string."
11. **Sequence.** "A YAML `sequence` is merged by appending values from the overriding Compose file to the previous one."
12. **Include.** "Compose displays a warning if resource names conflict and doesn't try to merge them."

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
- [ ] A service that needs a secret lists it in its own service definition; defining it at the top level grants nothing.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `yaml`, `dockerfile`, `oci`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Compose Specification: application model](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/02-model.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: the Compose file](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/03-compose-file.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: version and name](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/04-version-and-name.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: services](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/05-services.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: networks](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/06-networks.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: volumes](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/07-volumes.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: extensions](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/11-extension.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: interpolation](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/12-interpolation.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: merge and override](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/13-merge.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: include](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/14-include.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
- [Compose Specification: profiles](https://raw.githubusercontent.com/compose-spec/compose-spec/914ec15d1fa498969c0df5c1d672306db3256089/15-profiles.md): Specification, main at commit 914ec15, 2026-09-17, checked 2026-10-06.
