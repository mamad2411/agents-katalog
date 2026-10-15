---
name: pyqgis-api-reference
description: Use when writing QGIS 4 plugins or scripts and need exact PyQGIS API signatures, parameters, enums, return types, or deprecation status for a specific QGIS version (resolved by probing the machine's existing env vars / installed QGIS, default 4.2); when the QGIS-Documentation cookbook (4.4-dev) may drift from the target version; or when checking whether an API changed between QGIS 3 and QGIS 4. Do NOT use for user-manual behavior questions (use the docs.qgis.org user manual instead).
version: 1.2.0
---

# PyQGIS API Reference (qgis.org/pyqgis)

## Overview

The authoritative, version-pinned reference for the PyQGIS API is the Sphinx-generated site at `https://qgis.org/pyqgis/{version}/` — built from Doxygen comments in the QGIS C++ source, so signatures there are exact. The QGIS-Documentation cookbook tracks the dev branch (4.4) — **it may drift from any released version**. When precision matters, verify against the resolved pyqgis version.

## Version Selection — resolve `{version}` FIRST, before fetching anything

Prefer probing the machine over guessing. In order:

1. **Existing QGIS env vars** (never invent new ones): `OSGEO4W_ROOT` or `QGIS_PREFIX_PATH` (pwsh: `echo $env:OSGEO4W_ROOT`). They point at the install dir:
   - Standalone installs encode the version in the path (e.g. `C:\Program Files\QGIS 4.2.0`) → parse `QGIS (\d+\.\d+)`.
   - OSGeo4W paths carry no version (e.g. `D:\OSGeo4W`) → run `& "$env:OSGEO4W_ROOT\bin\qgis-bin.exe" --version` (or `qgis --version`); it prints e.g. `QGIS 4.2.0-Belém do Pará`.
2. **CLI on PATH** if those env vars are absent: `qgis --version` or `qgis-bin --version` (standalone installs ship only `qgis-bin.exe`, which may not be on PATH — check both, ignore failures).
3. **QGIS MCP probe** (only when MCP tools are available): `qgis_list_qgis_instances` reports each reachable instance's `qgis_version` (e.g. `4.2.0-Belém do Pará`).
4. **Default `4.2`** (current stable at skill creation). If in doubt whether a newer stable exists, check the version selector at the bottom of any `https://qgis.org/pyqgis/{v}/` page.

Normalize to major.minor (`4.2.0-Belém do Pará` → `4.2`, `3.44.2` → `3.44`). Never silently substitute a different version; if the resolved version differs from what the user asked about, say so.

## URL Patterns (no trial-and-error needed)

```
https://qgis.org/pyqgis/{version}/{module}/QgsClassName.html     # class page
https://qgis.org/pyqgis/{version}/{module}/index.html             # module class list
https://qgis.org/pyqgis/{version}/genindex.html                   # full class index
```

Modules: `core`, `gui`, `analysis`, `processing`, `server`, `_3d`. Class pages exist for functions too (e.g. `core/qgsfunction.html`).

**Mistakes to avoid:**
- NO `qgis.core.` prefix: `qgis.core.QgsVectorLayer.html` → 404. Use `core/QgsVectorLayer.html`.
- Version-pin explicitly — `master` = dev API, `3.44` = LTR, `4.2` = current stable.
- Correct URL returns 200 and contains the signature; a 404 usually means wrong module or version.

## Workflow

1. **Cookbook first**: consult the QGIS-Documentation cookbook (https://docs.qgis.org) for usage patterns, then this reference for exact signatures.
2. **Fetch the class page** (webfetch). Pages are HUGE (100KB+, e.g. QgsVectorLayer) — the fetch is auto-truncated and the full output saved to a tool-output file.
3. **Search the saved file** with `rg`/Grep instead of reading it whole. Or dispatch an `explore` subagent: "grep `__init__|writeAsVectorFormatV3|Deprecated` in <tool-output file>" to keep context clean.
4. **Cross-check deprecation**: `Deprecated since` markers can render misaligned next to signatures. When ambiguous, consult the C++ header on the matching release branch of `github.com/qgis/QGIS` (e.g. `release-4_2` → `src/core/vector/qgsvectorlayer.h`) — the `\deprecated` / `\since` comments adjacent to the declaration are the ground truth.

## QGIS 4 vs 3 Pitfalls (verified against 4.2 — re-verify if your resolved version differs)

- `QgsVectorLayer(path, name, provider, options)` — `encoding` arg REMOVED in 4.0; use `setProviderEncoding()`.
- Save vector files via `QgsVectorFileWriter.writeAsVectorFormatV3(layer, fileName, transformContext, SaveVectorOptions)` — V2 deprecated since 3.20, V1 since 3.40.
- Python-bound signatures differ from C++: defaults (e.g. `providerLib=''` in Python vs `"ogr"` in C++), `abstract` markers on pure-virtuals, SIP annotations (SIP_HOLDGIL etc.) are irrelevant to Python callers.
- Bindings are PyQt6-based (`from qgis.PyQt import ...` shim works on both Qt5/Qt6 builds).

## Common Mistakes

- Quoting a signature from memory instead of fetching — always fetch and cite the URL.
- Using the cookbook (4.4 dev) signature for released-version code without cross-checking.
- Reading a truncated fetch and missing the method you need — grep the full saved file.
- Forgetting to probe the machine (env vars / `qgis --version` / MCP) and silently answering for the default version.
