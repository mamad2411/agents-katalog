---
name: mypaint-brush-assets
description: Add, update, parse, test, package, or display the official MyPaint brush presets and preview icons in Rasterra. Use for the mypaint-brushes submodule, order.conf catalogs, .myb discovery, preview PNGs, brush groups, asset licensing, or brush-picker data models.
---

# Work with MyPaint brush assets

Read `CONTRIBUTING.md` and `docs/plan.md`. Keep brush catalog and format logic independent of Bevy; translate catalog entries into Bevy asset handles at the application boundary.

## Source policy

1. Prefer the official [`mypaint/mypaint-brushes`](https://github.com/mypaint/mypaint-brushes) repository, pinned to a reviewed revision as a Git submodule, over copying ad hoc presets from the MyPaint application.
2. Consume the submodule's `brushes/` data tree. Do not build or integrate its Autotools/SCons packaging machinery.
3. Treat the pinned revision's `Licenses.dep5` as the authoritative license inventory. Preserve upstream license and provenance files in source distributions.
4. Do not infer a file's license solely from the repository's GitHub license badge. At the audited revision, `brushes/*` is CC0 while repository tooling defaults to GPL-2+; recheck this boundary when updating the pin.
5. Do not fetch brushes during a normal build or application launch. A missing submodule should produce an actionable build/package message or a deliberate asset-free mode, never an implicit network operation.

The current upstream policy requires raw `.myb` settings to be public domain/CC0 and permits other brush-pack artwork to use CC0, CC BY, or CC BY-SA. The audited repository revision declares its full `brushes/*` tree CC0, including previews. Audit future revisions rather than assuming that will remain true.

## Catalog model

Parse `brushes/order.conf` as the authoritative group and display order. Each non-comment `Group: Name` begins a group; following extensionless relative paths identify brushes until the next group. Resolve a brush entry as:

```text
<entry>.myb          required preset
<entry>_prev.png     optional 128x128 preview icon
```

Use a stable relative-path ID, not a display label or array index. Preserve upstream spelling and ordering. Paths contain characters such as spaces, `#`, `+`, `%`, and parentheses, so use path APIs and never shell-concatenate them.

Model missing previews explicitly. Do not assume a perfect one-to-one file pairing: the audited tree contains 196 `.myb` files and 197 PNG files, including a standalone preview.

Read [repository-layout.md](references/repository-layout.md) before adding the submodule, catalog loader, packaging rules, or brush-picker assets.

## Loading boundary

- The format layer parses `.myb` contents.
- The catalog layer owns groups, stable IDs, preset paths, preview paths, and diagnostics.
- The Bevy application layer turns preview paths into image handles and selection into Rasterra actions.
- The brush engine consumes typed brush settings and has no knowledge of submodules, PNGs, or UI groups.

Keep user-installed brushes as a later source implementing the same catalog model. Do not make an absolute developer checkout path part of production behavior.

## Validation

- Test comments, blank lines, empty groups, ordering, unusual valid filenames, missing presets, and missing previews.
- Reject absolute paths and `..` traversal if catalogs outside the pinned tree are accepted later.
- Snapshot the parsed group/ID structure for the pinned corpus; avoid snapshotting absolute paths.
- Decode representative RGB, RGBA, and indexed-color previews through the same image path used by the application.
- Run the existing `.myb` parser tests against every catalog entry and report all failures in one pass.

## Primary references

- [Official mypaint-brushes repository](https://github.com/mypaint/mypaint-brushes)
- [MyPaint licensing policy](https://www.mypaint.app/en/docs/contributing/licenses/)
