---
name: tosca
description: >-
  TOSCA: The Topology and Orchestration Specification for Cloud Applications (TOSCA) provides a language for describing application components and their relationships by means of a service topology, and for specifying the lifecycle management procedures for creation or modification of services using orchestration processes. Covers TOSCA 2.0. Use when describing a cloud application topology. Triggers: TOSCA.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# TOSCA

The Topology and Orchestration Specification for Cloud Applications (TOSCA) provides a language for describing application components and their relationships by means of a service topology, and for specifying the lifecycle management procedures for creation or modification of services using orchestration processes. The combination of topology and orchestration enables not only the automation of deployment but also the automation of the complete service lifecycle management. The TOSCA specification promotes a model-driven approach, whereby information embedded in the model structure (the dependencies, connections, compositions) drives the automated processes.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when describing a cloud application topology.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: TOSCA 2.0 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Key Words.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [ RFC2119 ] and [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
2. **5.2 Mandatory Keynames.** "If a keyname is marked as mandatory it MUST be defined in that particular definition context."
3. **5.3.1 metadata.** "The following shows an example that uses metadata to track revision status of a TOSCA file: metadata : creation-date : '2025-04-14' date-updated : '2025-05-01' status : developmental Data provided within metadata, wherever it appears, MAY be ignored by TOSCA Orchestrators and SHOULD NOT affect runtime behavior."
4. **6.1 Keynames.** "The following rules apply: The key tosca_definitions_version MUST be the first line of each TOSCA file."
5. **6.1 Keynames.** "However, a TOSCA file that defines a profile MUST NOT define a service_template ."
6. **6.2 TOSCA Definitions Version.** "The mandatory tosca_definitions_version keyname provides a means to specify the TOSCA version used within the TOSCA file as follows: tosca_definitions_version : <tosca_version> It is an indicator for the version of the TOSCA grammar that MUST be used to parse the remainder of the TOSCA file."
7. **6.4.2 Type Derivation.** "For definitions that are not inherited, a new definition MUST be provided (if the keyname is mandatory) or MAY be provided (if the keyname is not mandatory)."
8. **6.7.1 Grammar.** "For example, the following profile statement is used to define Version 2.0 of a set of definitions suitable for describing cloud computing in an example company: profile : com.example.tosca_profiles.cloud_computing:2.0 The following defines a domain-specific profile for Kubernetes: profile : io.kubernetes:1.30 TOSCA parsers MUST process profile definitions according to the following rules: TOSCA…"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [TOSCA 2.0](https://docs.oasis-open.org/tosca/TOSCA/v2.0/os/TOSCA-v2.0-os.html): OASIS Standard, TOSCA 2.0, fetched 2026-10-06 (OASIS Standard, 2026-10-06), checked 2026-10-06.
