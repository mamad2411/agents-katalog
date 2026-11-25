---
name: darktide-extract-resources
description: "Extract Warhammer 40,000: Darktide resources from bundles, inspect resource dependencies, and obtain usable images and audio."
license: MIT
metadata:
  author: deluxghost
  version: "1.0.0"
  repository: https://github.com/deluxghost/darktide-skills
---

# Darktide Resource Extraction

Use limn for extraction. Its DDS, OGG, and JSON outputs can be final results; convert further only when the requested format or downstream use requires it.

Use existing extracted files directly for conversion. When bundle extraction is needed, use the supplied input or resolve the game installation from context; ask for the game path only if needed and unknown. Do not scan entire drives.

limn accepts a bundle directory (normally `<game>/bundle`) or a single bundle. It resolves external `data/...` paths relative to the input directory, or the parent directory of a single input bundle. Keep the matching `data/` at that location for textures, materials, and audio that reference it.

Use [Workspace And Tools](references/tools.md) for the shared path convention and tool dependencies.

## Selecting Resources

A resource has a name and a type. Game paths use `/` and omit the type extension. The same name can have several types; a bundle's filename identifies its container, not necessarily an individual resource.

limn filters by type, such as `texture`, not by a resource-path argument or `*.texture` glob. Multiple type arguments are accepted. For known paths, a UTF-8 dictionary containing one resource name per line narrows extraction:

```powershell
& '<limn-executable>' -i '<game>/bundle' -o '<output>' --dict '<selection.txt>' texture
```

Dictionary behavior matters:

- Names omit the extension. A known hash can instead use `@<16-hex-hash>=<relative-output-name>`; the output label is not a recovered original name.
- With a dictionary, limn skips unknown names. `--dict-no-skip` retains them with hash filenames.
- Without an explicit `--dict`, limn reads `dictionary.txt` from its working directory if present.
- For broader name coverage, use the [Darktide dictionary from Bitsquid Blender Tools](https://gitlab.com/qasikfwn/bitsquid-blender-tools/-/raw/dev/bitsquid/murmur/dictionaries/dictionary_hashcat_dt.txt). Known-path extraction needs only the relevant names, not a full dictionary.

For a hash inventory, `--dump-hashes` writes `hashes.bin` in the working directory, ignoring `-o`; run it in the task's temporary directory. Each record is two little-endian unsigned 64-bit values: type hash, then name hash.

## Extraction And Conversion

limn extracts bundle resources across types. It automatically converts types with a built-in converter; other types are written as raw resources, retaining limn's resource header, variant metadata, and data. `--dump-raw` selects this raw representation even for types with converters. Raw output is different from a standalone DDS, WEM, or a resource's payload alone.

The following are selected common conversion outputs, not a complete list of extractable types:

- `texture` → `.dds`: reconstructs the highest available mip level, including external texture data.
- `wwise_stream` → `.ogg`: converts supported Wwise Vorbis streams. `--config force-wem` instead resolves and writes the original Wwise media as WEM.
- `package` → `.package.json`: resource dependencies, with type and name hash, plus names when known. A unit often has a same-named package; these entries identify associated resources, but extracting the list does not extract those resources.

limn can skip data or encounter individual extraction errors without a failing exit code. Its reported count alone does not establish that the requested files were produced.

For PNG, WAV, or embedded event audio, read [Resource Conversions](references/conversions.md).
