---
name: model-signing
description: >-
  Model signing: sign and verify machine-learning models with Sigstore and in-toto statements. Covers Model signing. Use when signing machine-learning models. Triggers: model signing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Model signing

The OpenSSF Model Signing (OMS) specification 1.0: a Sigstore bundle wrapping a DSSE envelope whose payload is an in-toto Statement listing every model file and its digest. Read from the specification's Markdown at a pinned commit, with the CLI rules of the sigstore/model-transparency reference implementation at release v1.1.1.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Model signer (producer of OMS bundles) or model verifier (consumer that checks a model directory against its bundle).
- Target version: Model signing (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 5.1.** "Implementations MUST set `predicateType` to exactly this URI."
2. **§ 6.1.2.** "A path MUST NOT start with `/` (absolute path) or contain `../` components (parent traversal)."
3. **§ 6.2.** "Implementations MUST also exclude the signature output file (e.g., the path passed via `--signature`) from the file enumeration during both signing and verification."
4. **§ 8.5.** "By default, files present in the model directory but absent from `resources` (after applying exclusions) MUST cause verification to fail."
5. **§ 11.2.** "Producers MUST always generate bundles conforming to the current version."

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
- [ ] Verification of the signed model directory fails after adding an unlisted file or changing one byte of a listed file.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `sigstore`, `in-toto`, `slsa`, `owasp-ml-top-10`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenSSF Model Signing (OMS) Specification](https://raw.githubusercontent.com/ossf/model-signing-spec/91bf841e8ccf97a3ed97309387e9298d1ac18ba2/spec/v1.0.md): OpenSSF specification, Version 1.0, commit 91bf841e8ccf (2026-09-18), checked 2026-10-06.
- [sigstore/model-transparency README](https://raw.githubusercontent.com/sigstore/model-transparency/v1.1.1/README.md): Reference implementation, Release v1.1.1 (2025-10-10), checked 2026-10-06.
- [sigstore/model-transparency: Model Signing Format](https://raw.githubusercontent.com/sigstore/model-transparency/v1.1.1/docs/model_signing_format.md): Reference implementation, Release v1.1.1 (2025-10-10), checked 2026-10-06.
