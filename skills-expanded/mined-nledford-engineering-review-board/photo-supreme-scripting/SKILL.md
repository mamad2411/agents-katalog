---
name: photo-supreme-scripting
description: Photo Supreme (idimager) embedded Object Pascal scripting guidance. Use when writing, changing, reviewing, or debugging Photo Supreme scripts, .psc quick scripts, Script Studio scripts, search/filter/sort scripts, inline %code scripts, download pre/post scripts, or Photo Supreme API calls (idCatalog, idCore, xom*, OMPublic, UIPublic). Do not use for standard Object Pascal or Delphi application development outside Photo Supreme; use object-pascal-engineering instead.
---

# Photo Supreme Scripting

Use this skill for scripts that run inside Photo Supreme (IDimager Systems), a
digital asset management application whose scripting environment is an embedded
Object Pascal interpreter. Inspect the target Photo Supreme version's Script
Studio and API document before relying on a specific class, function, or language
feature.

## Use When

- Writing, changing, reviewing, or debugging a Photo Supreme script.
- Working with `.psc` quick scripts, Script Studio scripts, search/filter/sort
  scripts, inline `%code` scripts, or downloader pre/post scripts.
- Calling the Photo Supreme API (`idCatalog`, `idCatalogDOM`, `idCore`,
  `idEffectProcessor`, `idMacroBuilder`, `idMacroParser`, `idRecipe`, `OMPublic`,
  `UIPublic`, `xom*` units).

Do not use this skill for standard Object Pascal or Delphi application
development outside Photo Supreme; use
[`object-pascal-engineering`](../object-pascal-engineering/SKILL.md) instead.

## Scope And Routing

Own Photo Supreme's scripting environment, script types, API surface, and
environment-specific constraints. Use
[`object-pascal-engineering`](../object-pascal-engineering/SKILL.md) for the
Object Pascal language and RTL that the interpreter supports, and
[`object-pascal-antipatterns`](../object-pascal-antipatterns/SKILL.md) for
language-level smells. Use
[`digital-asset-management`](../digital-asset-management/SKILL.md) for the
media-catalog domain model (assets, originals, renditions, metadata precedence,
collections) that Photo Supreme implements. Use
[`security-review`](../security-review/SKILL.md) when a script handles untrusted
input, paths, credentials, or destructive catalog operations.

## Environment Model

- All Photo Supreme scripting is Object Pascal, executed by an embedded
  interpreter inside the Photo Supreme process. Scripts are not compiled to a
  standalone executable and do not run outside Photo Supreme.
- Scripts are authored and run through the Script Studio (`Tools > Scripter`) or
  written as plain-text files. The API document is generated per version with
  PasDoc and is the authoritative reference for the exposed units.
- The interpreter exposes a fixed set of application units and globals. It is not
  a general Delphi runtime: do not assume arbitrary RTL units, third-party
  libraries, DLLs, or OS APIs are available.
- The API document is version-specific. Confirm the class, method, property, and
  enum values against the target Photo Supreme version before use.

## Script Types And Entry Points

- **Quick scripts (`.psc`):** plain ASCII text with no embedded UI; commonly
  created in Script Studio or a text editor. Run directly.
- **Normal scripts:** designed in Script Studio and run from it.
- **Search scripts:** Script Studio scripts with specific search-handling
  implementations.
- **Filter scripts:** like search scripts, with filter-handling implementations.
- **Sort scripts:** like search and filter scripts, with sort-handling
  implementations.
- **Inline scripts:** small snippets usable almost anywhere (rename rules, custom
  thumbnail info, custom toolbar text, image caption titles, the web-template
  designer). An inline script starts with `%code` and ends with `%/code`.
- **Download scripts:** pre- and post-scripts used by the Downloader, designed
  inside the Downloader.

Match the script type to the entry point. A search, filter, or sort script must
implement the handlers that entry point requires; an inline script must set the
expected `result` value.

## API Surface

The exposed units include catalog and domain types (`idCatalog`,
`idCatalogDOM`, `idCore`, `idRecipe`, `idEffectProcessor`), macro handling
(`idMacroBuilder`, `idMacroParser`, `xomMacroParser`), public entry points
(`OMPublic`, `UIPublic`), and support units (`xomElements`, `xomException`,
`xomFileSystem`, `xomGPS`, `xomGPSReadWrite`, `xomList`, `xomLogging`,
`xomProgress`, `xomPublicFunctions`, `xomPublicTypes`, `xomSettings`, `xomTif`,
`xomUnicode`, `xomXMP`, `xomDXGraphics`).

Common entry points observed in documented examples and the API:

- `PublicCatalog` / `Catalog` (`TCatalog`) for catalog operations.
- `ImageItem` (`TImageItem`) for the current image in inline and per-image
  scripts.
- `Options` / `PublicOptions` (`TOptions`) for application settings; persist with
  `PublicBroadcast(nil, 'SaveOptions', nil)`.
- `Say(...)` for user-visible output and `PublicBroadcast(...)` for application
  notifications.
- `WriteToRegistry(...)` for registry-backed settings.
- `WideFileExists`, `WideFileIsReadOnly`, `WideUpperCase`, `iif(...)` and other
  helpers from the public function units.
- Macro tokens such as `%exif:Software` and `%FileExtension` are Photo
  Supreme-specific substitutions, not Object Pascal.

Treat the API document as the source of truth; the names above are examples, not
a complete or version-stable list.

## Differences From Standard Object Pascal

Write Photo Supreme scripts differently from a compiled Delphi/FPC application:

- **Interpreted, not compiled:** there is no compiler or build step. Syntax and
  type errors surface at run time, so test scripts in Script Studio before
  relying on them.
- **Hosted, not standalone:** a script runs inside Photo Supreme and depends on
  its process, catalog, and UI. There is no `program`/`Application` entry point
  of your own.
- **Fixed API, no arbitrary `uses`:** you can call the exposed units and globals,
  not arbitrary RTL units, third-party libraries, or OS APIs. Do not assume a
  Delphi RTL unit exists.
- **No direct OS/registry/network/filesystem access:** use the provided API
  functions (for example `WriteToRegistry`, `WideFileExists`) rather than
  assuming general file, registry, or network access.
- **No threads or parallelism:** scripts run on the application's thread. Long or
  blocking scripts freeze the UI; keep work bounded and avoid sleeps.
- **No unit-test framework:** validate through Script Studio and controlled runs,
  not DUnitX/fpcunit. Back up the catalog before destructive scripts.
- **Inline-script conventions:** inline scripts set `result` and are delimited by
  `%code`/`%/code`; they are not full units.
- **Version-specific language subset:** the interpreter may not support every
  Delphi language feature (for example generics, anonymous methods, attributes,
  or newer RTL types). Verify the feature against the target version before use;
  prefer plain, conservative Object Pascal.

## Writing Scripts

- Prefer small, single-purpose scripts. Keep the logic readable and avoid deep
  nesting.
- Use the documented API types and enum values rather than magic numbers or
  strings.
- For inline scripts, set `result` to the value the host expects and keep the
  snippet short.
- For search/filter/sort scripts, implement exactly the handlers the entry point
  requires and follow the examples importable from Script Studio.
- Handle the "no selection" and "no catalog item" cases explicitly; do not assume
  an image or selection exists.
- Report progress or completion with `Say(...)` where the script type supports
  it, so the user can tell the script ran.
- Keep scripts idempotent where possible; a re-run should not duplicate labels,
  collections, or metadata.

## Limitations And Environment-Specific Considerations

- **Catalog mutation is consequential.** Scripts can change labels, metadata,
  collections, files, and settings. Back up the catalog and test on a copy before
  running a destructive script on a real catalog.
- **Registry and settings writes persist.** `WriteToRegistry(...)` and
  `PublicBroadcast(nil, 'SaveOptions', nil)` change application state; some
  changes require a restart. Document the exact keys and values.
- **No transactional rollback.** A script that fails partway may leave partial
  changes; design for resumability or verify state before re-running.
- **UI thread only.** Do not attempt background work; there is no supported
  threading model in scripts.
- **Version drift.** API classes, methods, and enum values change between Photo
  Supreme versions. Re-check the API document for the target version.
- **Encoding.** The API uses `WideString`/`String` heavily; be explicit about
  conversions and do not assume byte-oriented behavior.

## Testing And Validation

- Develop and run in Script Studio; use its output and error reporting to confirm
  behavior.
- Test on a copy of the catalog or a small selection before a full run.
- For inline scripts, verify the rendered result in the exact host location
  (rename rule, custom thumbnail info, caption title, toolbar text, web template).
- Keep a known-good copy of the script so a failed run can be reverted.
- There is no automated test lane; treat manual, observed runs as the evidence.

## Safety

- Confirm the exact target (catalog, selection, files) before a destructive
  operation, and prefer a preview or dry-run pass where the API allows it.
- Never embed credentials or secrets in a script; scripts are plain text and may
  be shared.
- Treat file paths and metadata read from the catalog as untrusted; validate
  before using them in file operations.
- Load [`security-review`](../security-review/SKILL.md) when a script crosses a
  trust boundary or performs privileged or irreversible operations.

## Anti-Patterns

- Assuming a full Delphi runtime, arbitrary `uses`, or OS/network access.
- Long-running or blocking scripts that freeze the UI.
- Destructive catalog or file operations without a backup or preview.
- Hard-coded enum integers or strings instead of the documented API values.
- Ignoring the "no selection"/"no item" case.
- Relying on a language feature the target interpreter may not support.
- Leaving registry or settings changes undocumented.

## Successful Use

Report the target Photo Supreme version, script type and entry point, API units
and calls used, whether the script mutates the catalog or settings, the backup or
preview taken, and the observed run result.
