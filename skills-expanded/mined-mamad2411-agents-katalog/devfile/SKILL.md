---
name: devfile
description: >-
  Devfile 2.3: describe cloud development environments with components, commands and events in a devfile.yaml. Covers Devfile 2.3. Use when writing a devfile. Triggers: devfile.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Devfile

The Devfile 2.3.0 schema from the Devfile project (CNCF), read from the devfile/api repository at the v2.3.0 tag, together with the Devfile 2.3.0 authoring guides published on devfile.io, read from their Markdown source in the devfile/devfile-web repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Devfile author, or a tool that reads devfiles to build development environments (for example a devworkspace operator or an IDE integration).
- Target version: Devfile 2.3 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Creating devfiles, Procedure.** "`schemaVersion` is the only required root element"
2. **Adding components.** "Each component in a single devfile must have a unique name and use one of the objects: `container`, `kubernetes`, `openshift`, `image` or `volume`."
3. **commands[].id.** "Mandatory identifier that allows referencing this command in composite commands, from a parent, or in events."
4. **components[].container.endpoints[].targetPort.** "The same port cannot be used by two different container components."
5. **components[].container.endpoints[].secure.** "Describes whether the endpoint should be secured and protected by some authentication process. This requires a protocol of `https` or `wss`."
6. **Creating devfiles, Procedure.** "If a `container` entity is defined, an `image` property must be specified"
7. **Creating devfiles, Procedure.** "An `exec` entity must be defined with a `commandLine` string and a reference to a `component`"
8. **Adding a command group, Procedure.** "At most, there can only be one default command for each group kind."
9. **Adding an exec command.** "The `component` attribute value must correspond to an existing container component name."
10. **Adding projects, Procedure.** "The path must be relative to the `/projects/` directory, and it cannot leave the `/projects/` directory."

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

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `yaml`, `json-schema`, `dockerfile`, `kubernetes-api-conventions`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Devfile schema 2.3.0](https://raw.githubusercontent.com/devfile/api/c088cf36a78ddadb8a45b951a2e7214a2ef2da26/schemas/latest/devfile.json): Specification, Devfile schema 2.3.0 (devfile/api v2.3.0, commit c088cf3), checked 2026-10-06.
- [Devfile 2.3.0 docs: Adding components](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/adding-components.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Creating devfiles](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/create-devfiles.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Adding a command group](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/adding-a-command-group.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Adding an exec command](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/adding-an-exec-command.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Adding a container component](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/adding-a-container-component.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Adding projects](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/adding-projects.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Defining starter projects](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/defining-starter-projects.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Defining endpoints](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/defining-endpoints.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
- [Devfile 2.3.0 docs: Referring to a parent devfile](https://raw.githubusercontent.com/devfile/devfile-web/5e4115c7cb868fc52e9898268dd0c93e6292c445/libs/docs/src/docs/2.3.0/referring-to-a-parent-devfile.md): Documentation, 2.3.0 docs (devfile-web main at commit 5e4115c, 2026-09-27), checked 2026-10-06.
