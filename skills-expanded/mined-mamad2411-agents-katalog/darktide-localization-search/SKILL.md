---
name: darktide-localization-search
description: "Acquire and query Warhammer 40,000: Darktide localization data. Use to resolve localization keys, search translated text, compare languages, or trace displayed text back to candidate keys."
license: MIT
compatibility: "For indexing and queries: Python 3.10+ with sqlite3, or Windows with Windows PowerShell 5.1 or PowerShell 7 and the SQLite CLI."
metadata:
  author: deluxghost
  version: "1.0.0"
  repository: https://github.com/deluxghost/darktide-skills
---

# Darktide Localization Search

## Select The Data

Reuse a localization index created by this skill, or build one from existing readable `.strings` files. If extraction is needed, read [Data Acquisition](references/acquisition.md). Resolve data, tool and output locations from context and project conventions; ask only for missing choices.

The database is generated locally, not bundled with the skill. Reuse suitable workspace locations; otherwise keep readable `.strings` under `<workspace>/game-data/localization/`, the reusable database at `<workspace>/game-data/index/localization.sqlite`, and newly installed tools under `<workspace>/tools/<tool>/<release-or-commit>/`. These are persistent files, not temporary output. An existing database from another tool is not automatically this schema; build a separate index rather than replacing it.

Keep tools acquired for this workflow, extracted localization data, and generated indexes inside the active workspace, separate from the skill and game installation. Resolve these write destinations, including directory links, before use. Existing tools and input data elsewhere can be used in place.

Use `<workspace>/.tmp/<task-id>/` for intermediates from tool unpacking, extraction, and index building. Create these directories only when needed; clean this run's intermediates on success or failure, then remove `.tmp` non-recursively if empty. Retain failed-step intermediates only when needed to diagnose or resume that step, reporting where and why; leave other runs' files untouched.

Use [Build And Query](references/querying.md) for script arguments and dependencies. Prefer Python 3.10 or later when `import sqlite3` succeeds, regardless of the operating system. On Windows without suitable Python, use the independent PowerShell implementation with the SQLite command-line executable.

Index only the selected dataset, not a mixture of extraction generations. Rebuild when that data changes; rebuild with the optional Lua source or known-key file when updating reverse-lookup candidates. `query --info` reports input files, SHA-256 fingerprints and the supplied game version. A timestamp or successful build alone does not establish a match with the installed game.

## Localization Conventions

- **Keys and hashes:** Lua generally refers to a key such as `loc_<identifier>`. Extracted records often expose only an eight-digit hexadecimal hash. This is the high 32 bits of seed-zero MurmurHash64A over the key's UTF-8 bytes, not ordinary MurmurHash32. Both script implementations calculate it without an external tool.
- **Reverse lookup:** Hashing cannot recover the original key. Names come from named extracted records, optional Lua scanning, or a supplied known-key list. Static `loc_...` tokens are candidates: dynamically assembled keys and backend-only names can be absent. Return every candidate for a hash; an empty `keys` array means no known name, not no translation. A hash match alone cannot disambiguate a collision.
- **Resource identity:** A hash may occur in several `.strings` resources. Results retain the relative resource path, so differing records are not silently merged. A translated display name may also be shared by several unrelated keys or internal templates.
- **Text representation:** Readable `.strings` files use SJSON, not JSON. The bundled converters produce this format from raw DTMT output. Quoting and escapes must be decoded before comparing displayed text. The helpers do this; `null` in query results denotes a missing language, while `""` is a present empty translation.
- **Languages:** Supported codes are `en`, `pl`, `ja`, `es`, `zh-tw`, `pt-br`, `de`, `ko`, `ru`, `it`, `zh-cn`, and `fr`. `lang_8` is `comment`, a separate annotation rather than a player language. The numeric mapping is bundled in `scripts/languages.json`. Choose output languages from the request or context; the script default returns all of them.
- **Runtime wording:** Static translations can contain macros and interpolation placeholders. `scripts/managers/localization/localization_manager.lua` and its consumers explain how `Localize` formats them; backend data can also add entries. A static string is not necessarily the final on-screen text.

For Lua references or formatting logic, use the separately available `darktide-source-search` skill. When initialized runtime values are actually needed, use `dt-cli`. It is optional and not included with this skill or the game: [Darktide CLI on Nexus Mods](https://www.nexusmods.com/warhammer40kdarktide/mods/1016) supplies LuaExec and `<game>/mods/LuaExec/bin/dt-cli.exe`. LuaExec must be loaded in the relevant running game. Use the `darktide-dt-cli` skill for invocation and PID selection, or the installed client's `--help` if that skill is unavailable.
