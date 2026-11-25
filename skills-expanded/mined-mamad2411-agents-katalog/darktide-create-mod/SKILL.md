---
name: darktide-create-mod
description: "Create a Warhammer 40,000: Darktide mod from bundled templates. Use when scaffolding or initializing a new mod with its Lua entrypoints, .mod file, and info.json metadata."
license: MIT
compatibility: "Python 3.10+, or Windows with Windows PowerShell 5.1 or PowerShell 7."
metadata:
  author: deluxghost
  version: "1.0.0"
  repository: https://github.com/deluxghost/darktide-skills
---

# Create a Darktide Mod

Select exactly one generator in this order:

1. If the user requests a specific implementation, use it.
2. Otherwise, use `scripts/create_mod.py` when an available command successfully runs Python 3.10 or later. A Windows Store command alias that cannot run Python does not count.
3. If Python 3.10 or later is unavailable on Windows, use `scripts/create_mod.ps1`, which supports Windows PowerShell 5.1 and has no external dependencies.

Report a missing requested or supported runtime instead of installing one or silently changing an explicit user choice.

## Scaffold Boundary

Create the bundled scaffold without asking the user to configure its file names, paths, `.mod` structure, or Lua entrypoint structure. Modify the generated main Lua body only when the request also includes implementing mod behavior.

## Resolve Inputs

The generator requires concrete values for:

- `output-root`: Existing directory that will contain the new mod folder.
- `name`: Internal mod ID and folder name. It must match `[A-Za-z0-9][A-Za-z0-9_-]*`.
- `author`: Non-empty author name.
- `description`: Non-empty English description.

Resolve them from the full request, conversation context, and target workspace. If the user delegates a choice, select a reasonable, non-misleading value. Ask only when no valid choice can be made without risking the user's intent. Never infer the author from an operating-system username or assume a machine-specific output path.

Apply these defaults without asking unless the user supplied a value:

- `title`: Derive a readable display name from `name`. For example, `MyExampleMod` becomes `My Example Mod`, `example_overlay` becomes `Example Overlay`, and `UIExample` becomes `UI Example`.
- `version`: Use `1.0.0`.

Optional public metadata includes `homepage`, `source`, funding links, dependencies, and localized names or descriptions. Use relevant values already available from the request or context and otherwise omit them. Ask only when an unresolved optional choice materially affects the requested result. Do not fabricate public URLs, identities, dependencies, or translations.

When localized names or descriptions are requested, read `references/languages.json`. Use only the canonical codes in its `languages` object. The `primary` language is already populated by the base title and description and cannot be supplied again as an optional localization. Platform locale aliases such as `de-de` or `zh-hk` are not localization keys.

## Run the PowerShell Generator

Use this Windows fallback when Python 3.10 or later is unavailable, or when the user requests PowerShell. Pass arguments with hashtable splatting. The following variables are examples rather than environment defaults:

~~~powershell
$skillRoot = '<path-to-darktide-create-mod-skill>'
$outputRoot = '<existing-output-directory>'
$modName = 'ExampleMod'
$author = 'Author Name'
$description = 'A concise description of the mod.'

$createScript = Join-Path $skillRoot 'scripts\create_mod.ps1'
$createParams = @{
	OutputRoot = $outputRoot
	Name = $modName
	Author = $author
	Description = $description
}

& $createScript @createParams
~~~

The PowerShell generator also accepts:

- `-Title <text>` and `-Version <version>`.
- `-Homepage <https-url>` and `-Source <https-url>`.
- `-Funding <provider=https-url[]>`.
- `-RequiredDependency <mod-id[]>`, `-LoadAfter <mod-id[]>`, and `-LoadBefore <mod-id[]>`.
- `-LocalizedName <language=text[]>` and `-LocalizedDescription <language=text[]>`.

Pass multiple values as a PowerShell array, such as `-Funding @('provider-a=https://example.invalid/a', 'provider-b=https://example.invalid/b')`.

## Run the Python Generator

Use this generator whenever Python 3.10 or later is available unless the user requests PowerShell. Pass native arguments as separate array elements. It accepts:

- `--title <text>`: Override the derived display name.
- `--version <version>`: Override `1.0.0`.
- `--homepage <https-url>` and `--source <https-url>`.
- `--funding <provider=https-url>`: Add a funding entry; repeat for multiple providers.
- `--required-dependency <mod-id>`: Add a required dependency; repeat as needed.
- `--load-after <mod-id>` and `--load-before <mod-id>`: Add optional load-order relationships; repeat as needed.
- `--localized-name <language=text>` and `--localized-description <language=text>`: Add a real translation to both `info.json` and the Lua localization table; repeat for each language.

Both generators fail if `<output-root>/<name>` already exists. They never overwrite or merge an existing mod.

## Generated Files

~~~text
<name>/
├── <name>.mod
├── info.json
└── scripts/mods/<name>/
    ├── <name>.lua
    ├── <name>_data.lua
    └── <name>_localization.lua
~~~

- `<name>.mod` checks for DMF with `fassert`, then calls `new_mod` with the main script, data, and localization paths.
- `info.json` always contains `name`, `description`, `version`, and `author`. It contains optional public metadata only when supplied.
- `<name>.lua` obtains the mod instance and provides the main logic entrypoint.
- `<name>_data.lua` exposes the localized display name and description and sets `is_togglable = true`.
- `<name>_localization.lua` contains initial English values. Add real translations only when they are available.

After generation, verify that all five files exist, parse `info.json` as JSON, and confirm that no unresolved template placeholders remain.

## Scope

The generator renders only the five files listed above. It does not edit `mod_load_order.txt`, initialize Git, build or deploy the mod, or launch the game.
