---
name: gittuf
description: >-
  gittuf: protect Git repositories with signed, verifiable policy for who may change which branches and files. Covers gittuf. Use when verifying Git repository policy. Triggers: gittuf.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# gittuf

gittuf, an OpenSSF security layer for Git: root of trust and rule file policy metadata in `refs/gittuf/policy`, the Reference State Log (RSL) that records every ref change, and the verification and recovery workflows, read from the gittuf design document at release v0.16.0.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Repository owner who writes gittuf policy, developer who pushes through gittuf, or verifier that checks a repository against its policy.
- Target version: gittuf (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Root of Trust.** "This new version must be signed by a threshold of root keys trusted in the previous version."
2. **Rule Files.** "The primary rule file derives its trust directly from the root of trust metadata; it must be signed by a threshold of actors trusted to manage the repository's primary rule file."
3. **RSL Annotation Entries.** "Since the RSL history cannot be overwritten, an annotation entry must be used to communicate to gittuf clients to skip the corresponding entries."
4. **Regular Pushes.** "When an actor pushes a change to a remote repository, this update to the corresponding ref (or refs) must be recorded in the RSL."
5. **Identifying Authorized Signers for Protected Namespaces.** "During this process, a principal must only be counted once even if they sign multiple times using different keys."

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
- [ ] Every change to a protected branch or file has an RSL entry signed by a threshold of principals that the policy in force at that entry authorizes.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `tuf`, `in-toto`, `slsa`, `sigstore`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [gittuf Design Document](https://raw.githubusercontent.com/gittuf/gittuf/v0.16.0/docs/design-document.md): Design document, Release v0.16.0 (2026-09-04), checked 2026-10-06.
