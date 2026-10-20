---
name: encoding-realignment
description: Solve CTF challenges where a custom alphabet or unusual string-to-bytes
  encoding yields partially readable output that must be recovered through UTF-16/word
  interpretation, bit-shift realignment, offset scanning, and layered decoding. Use
  when decoded text is half-readable, source code leaks exact transform symbols, or
  nested encodings appear after a custom Base64-like stage.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- encoding
- bit-alignment
- utf16
- custom-base64
- triage
related_skills:
- ctf-technique-atlas
---

# CTF Encoding Realignment

## Overview

Use this skill for CTF puzzles that are not "broken crypto" so much as **misleading encoding pipelines**: custom alphabets, Java/UTF-16 string byte layouts, partial corruption, framing bytes, bit-offset mistakes, or nested encodings revealed only after realignment.

The key mindset is: **partially readable output is evidence, not failure**. If a custom decode yields a few plausible characters and a lot of junk, the route may still be correct; the remaining work is often alignment, offset, framing, or a second decode layer.

## When to Use

- A challenge provides source code or symbol names that imply a specific encode/decode path
- A Base64-like alphabet is clearly nonstandard
- Direct decode gives a mix of readable prefix/body plus junk
- Decoded bytes look structured but not yet human-readable
- You suspect UTF-16/UTF-32, endianness, framing bytes, or word-level shifts
- You see nested encoding artifacts like `V2V...`, PEM-like blocks, hex-looking tails, or obvious flag substrings after a first decode

Do **not** start here when the task is clearly classical crypto, RSA/ECC, or a web/pwn challenge.

## Core Principles

1. **Exact symbols beat broad guessing**
   - If the prompt leaks function names, library names, or upstream source references, reconstruct that exact pipeline first.
   - Example clues: `dirName()`, `byteArrayToAltBase64()`, `UTF_16BE`, custom serializer helpers.

2. **Readable fragments are directional clues**
   - A short readable prefix does not prove the whole decode is correct.
   - But it strongly suggests the alphabet and overall transform family are right.

3. **Keep layers separate**
   - Track:
     - raw ciphertext / encoded string
     - first-stage decoded bytes
     - interpreted words/code units
     - realigned candidate plaintext
     - nested second-layer decodes
     - final flag wrapper hypothesis
   - Do not merge these too early.

## Standard Workflow

### 1. Reconstruct the upstream transform

Before brute forcing anything, write down the exact implied pipeline:

```text
input string
→ optional prefix/suffix framing
→ custom alphabet decode
→ bytes
→ string-byte interpretation (UTF-16BE/LE? UTF-32? raw bytes?)
→ alignment/offset repair
→ nested decode if present
→ flag extraction
```

Questions:
- Was a prefix added mechanically (`_`, version byte, marker)?
- Is the alphabet fully known?
- Did the source convert characters to bytes using UTF-16BE/LE or platform-default encoding?
- Is there padding suppression or truncation?

### 2. Decode with the custom alphabet exactly

Do not substitute a "close enough" alphabet. Build the exact translation table. Log:
- input length
- decoded byte length
- remainder / padding situation
- whether any characters are out-of-alphabet

### 3. Try structured byte interpretations

Inspect the same bytes as multiple candidate views:
- raw hex
- 8-bit ASCII/Latin-1
- UTF-16BE
- UTF-16LE
- 16-bit words
- 32-bit words if source suggests it

Quick signals:
- alternating zero/high-byte patterns → UTF-16 candidate
- many words with low 6 bits zero → possible bit-shift issue
- readable text every N bytes → framing or interleaving

### 4. Scan alignment, not just encodings

If the direction looks right but output is garbled, systematically try:
- whole-bitstream shifts `0..15`
- byte offsets `0..7` where reasonable
- word-level transforms such as `word >> k`, `word << k` with masked carry awareness
- skipping an initial framing segment of a few words/bytes

Score candidates by:
- printable ASCII ratio
- presence of flag syntax / leetspeak / English fragments
- Base64/hex/URL-safe subpatterns
- known challenge prefix/suffix

### 5. Hunt for nested encodings

Once the candidate plaintext becomes partly readable, look for substrings matching:
- standard Base64: `[A-Za-z0-9+/=]{8,}`
- hex runs
- URL encoding
- gzip/zlib magic
- PEM/ASN.1 headers
- obvious wrapper text around an embedded payload

Decode these **as a separate stage**, not by rewriting the whole recovered plaintext.

### 6. Verify each layer independently

Keep a table like:

| Layer | Status | Evidence |
|---|---|---|
| Custom alphabet identified | verified / hypothesis | source symbol, exact alphabet |
| Prefix removal | verified / hypothesis | upstream function behavior |
| UTF-16BE interpretation | verified / hypothesis | source or byte pattern |
| Bit-shift value | verified / hypothesis | scoring / recovered text |
| Nested Base64 | verified / hypothesis | regex + successful decode |
| Final wrapper | verified / hypothesis | platform rule or observed format |

This prevents "looks right" from becoming false certainty.

## OpenJDK altBase64 Pattern

A common pattern validated in practice:

1. Challenge references `java.util.prefs.FileSystemPreferences.dirName()`
2. Leading `_` is added before encoding
3. Payload uses Java Preferences **alternate Base64 alphabet**
4. Underlying string bytes are **UTF-16BE**
5. Output may still require **bit realignment** or skipping framing words
6. Recovered plaintext may contain a **nested standard Base64 tail**

Practical heuristic: if decoded UTF-16 words look like large non-ASCII code points but share suspicious structure, test bitstream shifts before abandoning the path.

## Common Pitfalls

1. **Brute-forcing generic decoders before reading the source clue**
   - Exact upstream behavior usually narrows the search far faster.

2. **Trusting the first readable prefix too much**
   - A prefix can be real, junk, or a wrapper while the main message still needs alignment.

3. **Normalizing to "better English" too early**
   - Preserve literal recovered payload first; human interpretation is a later layer.

4. **Confusing payload with final flag**
   - The decoded message may still need wrapper extraction or submission-format confirmation.

5. **Ignoring truncation**
   - Missing padding or shortened tails can create misleading near-miss decodes.

## Quick Triage Checklist

- [ ] Wrote down the exact source-implied transform
- [ ] Removed only prefixes/suffixes justified by source behavior
- [ ] Implemented the exact custom alphabet
- [ ] Inspected bytes as UTF-16BE/LE and raw words
- [ ] Tried systematic bit/byte/word offset scans
- [ ] Scored candidates instead of eyeballing one output
- [ ] Separated recovered payload from final flag hypothesis
- [ ] Checked for nested Base64/hex/other encodings
- [ ] Marked each layer as verified vs hypothesis

## Minimal Solver Strategy

For reproducible solves, build a script that:
1. decodes the exact alphabet
2. prints multiple interpretations
3. scans bit offsets / word shifts
4. ranks candidates by printability + pattern hits
5. extracts nested encodings for separate testing
6. prints all final candidates with provenance

## Verification Checklist

- [ ] Can explain why the chosen alphabet is exact
- [ ] Can point to evidence for the selected string-byte encoding
- [ ] Can reproduce the realignment numerically (not just visually)
- [ ] Can show the nested decode separately from the main recovery
- [ ] Can distinguish verified facts from guessed wrapper/flag formatting
