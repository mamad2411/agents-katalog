---
name: inspect-metadata
description: Use when the embedded metadata of a file matters — extracts EXIF, IPTC, XMP, and container metadata to JSON, then flags anomalies such as timestamp disagreement or editing-software markers as signals worth investigating. Triggers - "read the EXIF on this", "does this photo have GPS", "check this video for editing traces".
allowed-tools: Bash(exiftool *), Bash(mediainfo *), Bash(command *), Bash(file *), Bash(stat *), Bash(mkdir *), Read, Write
---

# Inspect Metadata

Extract embedded metadata to JSON and flag patterns that warrant a closer look.

## When to use

- Establishing what a file claims about its own origin.
- Checking whether an image or document carries location or identity data before it is
  disclosed to anyone.
- Looking for internal inconsistency in an item whose provenance is contested.

## Inputs

- Path to a file or directory. Required.
- `--out <path>` — JSON destination. Defaults to `logs/metadata-<name>-<date>.json`.

## Procedure

### 1. Determine the handler

```bash
file --mime-type -b "$TARGET"
```

Images and documents go to `exiftool`. Audio and video go to both `exiftool` and
`mediainfo`, because they describe different layers — `exiftool` reads tags,
`mediainfo` reads the container and stream structure.

### 2. Extract

```bash
exiftool -json -a -G1 -struct "$TARGET" > exif.json
mediainfo --Output=JSON "$TARGET" > mediainfo.json
```

`-a` keeps duplicate tags rather than collapsing them, and `-G1` records which group
each tag came from. Both matter when tags disagree — collapsing hides the disagreement.

### 3. Merge

Produce one JSON object per input file with `exiftool` and `mediainfo` as separate
keys, plus the filesystem facts the file itself cannot carry:

```bash
stat -f '%z %m' "$TARGET"    # macOS: size, mtime
stat -c '%s %Y' "$TARGET"    # GNU
```

### 4. Flag anomalies

Report these as **signals warranting investigation**, never as findings of tampering.
Ordinary software produces most of them for entirely innocent reasons.

- GPS coordinates present, or conspicuously absent on a device that normally records them.
- Disagreement between EXIF `DateTimeOriginal`, the container creation date, and the
  filesystem timestamp.
- Editing-software markers in `Software`, `ProcessingSoftware`, or XMP history.
- An embedded thumbnail that does not match the full image.
- Container and codec combinations inconsistent with the claimed source device.
- Re-encode indicators such as a bitrate or colour profile atypical for the device.

For each flag, record the tag names and values that produced it so a reader can check
the reasoning rather than trust the label.

### 5. Report

Summarise in prose, then give the JSON path. If a flag was raised, state plainly what
would need to be established to turn the signal into a conclusion.

## Output

- A JSON file at the resolved path.
- A short summary with any flags and the evidence for each.

## Notes

- Never write metadata back. This skill is read-only on its input.
- Absence of metadata is not evidence of stripping. Many platforms remove it on upload
  as a matter of routine.
- Metadata is self-reported by whatever wrote the file. It is a claim, not a fact.
