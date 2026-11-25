# Official brush repository layout

This audit covers `mypaint/mypaint-brushes` commit `08da4a48a4b63f2e0f3303942d7c21da8479ea9f` on 2026-07-12. Re-run the audit when changing the submodule revision.

## Contents

```text
mypaint-brushes/
├── Licenses.dep5       authoritative per-path licensing
├── Licenses.md         human-readable license summary
├── COPYING             GPL text for repository tooling
└── brushes/
    ├── order.conf      groups and presentation order
    ├── <group>/
    │   ├── <name>.myb
    │   └── <name>_prev.png
    └── ...
```

The audited tree contains seven preset directories, 196 `.myb` files, and 197 PNG files. All inspected preview images are 128×128, but they use several PNG color types: RGB, RGBA, and indexed color. Do not specialize the loader to one PNG representation.

`order.conf` defines Dieterle, Classic, Deevad, Favorites, Ramon, Experimental, Tanda, and Kaerhon groups. Favorites is intentionally empty in the distributed catalog. An extensionless entry such as `classic/pencil` maps to `classic/pencil.myb` and `classic/pencil_prev.png`.

## License boundary at this revision

`Licenses.dep5` says:

- `brushes/*`: CC0-1.0
- repository files not covered by a more specific rule: GPL-2+

This makes the brush settings and their shipped preview icons suitable Rasterra assets at this pin. It does not make the build scripts or every future revision CC0. Retain the submodule's license records and make packaged-asset provenance visible even though CC0 does not require attribution.

## Submodule placement

Use a clearly external path such as `vendor/mypaint-brushes`. Keep the upstream checkout intact instead of moving files out of it. Application packaging should deliberately copy only the required `brushes/` tree plus appropriate provenance/license records.

Document `git submodule update --init` in the setup path once the submodule is added. CI and release jobs must initialize the pinned submodule explicitly; Cargo must not mutate or update it.

## Update audit

Before advancing the pin:

1. Read the upstream changelog and compatibility notes.
2. Diff `Licenses.dep5`, `order.conf`, and file types against the current pin.
3. Run every `.myb` file through Rasterra's parser and compatibility tests.
4. Decode every referenced preview.
5. Review added, removed, and renamed stable brush IDs.
6. Commit the new submodule pointer and any required compatibility changes atomically.
