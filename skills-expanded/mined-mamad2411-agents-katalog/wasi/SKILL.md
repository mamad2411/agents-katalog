---
name: wasi
description: >-
  WASI: target the WebAssembly System Interface and Component Model with WIT interfaces. Covers WASI 0.2.12, WASI 0.3.1 (track preview), WebAssembly Component Model. Use when targeting the WebAssembly System Interface. Triggers: WASI, Component Model.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# WASI

The WebAssembly System Interface from the WASI Subgroup of the WebAssembly Community Group, read from the WASI 0.2.12 and 0.3.1 specification overviews in the WebAssembly/WASI repository, and the Component Model it builds on, read from `design/mvp/Explainer.md` and `design/mvp/WIT.md` in the WebAssembly/component-model repository.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Component author or toolchain targeting a WASI world, host runtime implementing WASI interfaces, or author of WIT packages.
- Target version: WASI 0.2.12 (current); WASI 0.3.1 (preview, posture: track); WebAssembly Component Model (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **WASI 0.2.12 § WASI Specification v0.2.12.** "This is version 0.2.12 of the WASI specification, based on the [WebAssembly Component Model][cm]."
2. **WASI 0.3.1 § Component Model features.** "Implementing this version of the specification requires the default (ungated) [Component Model][cm] features, plus the [gated features][gates] adopted by the WASI Subgroup up to and including this version:"
3. **WASI 0.3.1 § Component Model features.** "These are required whether or not an API in this version uses them."
4. **Explainer § Gated Features.** "All other features are in various stages of implementation, are not enabled by default, may have breaking changes, and, after a suitable [WASI] SG vote, may be shipped as part of a future WASI Developer Preview release:"
5. **Explainer § Component Invariants.** "Component validation rules only allow a component to import and export component-level functions, not Core WebAssembly functions."
6. **Explainer § Import and Export Definitions.** "The `label` production used inside `plainname` as well as the labels of `record` and `variant` types must be [kebab case]."
7. **Explainer § 🔀 `task.return`.** "One of `task.return` or `task.cancel` must be called exactly once from any of a task's threads."
8. **WIT § WIT Worlds.** "Each name must be case-insensitively unique in the scope in which it is declared."
9. **WIT § Interfaces, worlds, and `use`.** "Interfaces linked with `use` must be acyclic."
10. **WIT § Lexical structure.** "Additionally, wit files must not contain any bidirectional override scalar values, control codes other than newline, carriage return, and horizontal tab, or codepoints that Unicode officially deprecates or strongly discourages."
11. **WIT § Rules for feature gate usage.** "As part of WIT validation, any item that refers to another gated item must also be compatibly gated."
12. **WIT § Rules for feature gate usage.** "If a package contains a feature gate, it's version must be specified (i.e. `namespace:package@x.y.z`)"

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

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `webassembly`, `oci`, `semver`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [WASI Specification v0.2.12](https://raw.githubusercontent.com/WebAssembly/WASI/90105ffc2a4eed594909f9df2f473596500b49d2/specifications/wasi-0.2.12/Overview.md): Released WASI version, v0.2.12 (released 2026-06-02), main at commit 90105ff, checked 2026-10-06.
- [WASI Specification v0.3.1](https://raw.githubusercontent.com/WebAssembly/WASI/90105ffc2a4eed594909f9df2f473596500b49d2/specifications/wasi-0.3.1/Overview.md): WASI preview release, v0.3.1 (released 2026-08-11), main at commit 90105ff, checked 2026-10-06.
- [Component Model explainer](https://raw.githubusercontent.com/WebAssembly/component-model/a25fc0b372dd21f07f0242c46e98bd0f1ea0c0e1/design/mvp/Explainer.md): Component Model design (explainer), main at commit a25fc0b, 2026-09-28, checked 2026-10-06.
- [The `wit` format](https://raw.githubusercontent.com/WebAssembly/component-model/a25fc0b372dd21f07f0242c46e98bd0f1ea0c0e1/design/mvp/WIT.md): Component Model design (WIT), main at commit a25fc0b, 2026-09-28, checked 2026-10-06.
