---
name: reading-assembly
description: Read and translate RISC OS ObjAsm/ARM assembly into another language, PyModule, tests, or interface documentation. Use when converting `s/*` assembler modules, reconstructing SWI behaviour, validating comments against generated tables/disassembly, or proving binary-compatible data layout and boundary behaviour.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-dumpi:*)
---

# Reading Assembly For Conversion

## Core Workflow

1. Start from the public module surface, not the algorithm comments.
   Read the module header, exported headers, SWI names table, command table,
   service table, and error blocks before translating implementation code.

2. Record the calling contract before writing code:
   input registers, output registers, preserved/corrupted registers, V flag
   behaviour, processor mode, IRQ state, and error block numbers/messages.

3. Treat comments as hypotheses.
   Verify them against instructions, generated lookup tables, and the built
   binary. Old assembler comments often describe the intended maths but not
   the exact boundary behaviour or packing order.

4. Validate external interfaces against documentation before translating
   calls that cross a module, vector, SWI, or service boundary. If the
   register contract cannot be found in local docs, PRM-in-XML, source
   comments, or an authoritative external reference, report that uncertainty
   to the user instead of filling in registers from guesswork.

5. Translate the observed behaviour, not the apparent structure.
   It is acceptable for the target language to use clear loops where the
   assembler uses lookup tables, register reuse, or carry tricks, but outputs
   and errors must match exactly.

6. Write independent behavioural tests.
   Use a second implementation in BASIC, C, or a small host script to generate
   expected results. Run the same tests against the original module and the
   converted implementation.

## What To Read

Use this order when source is available:

- `docs/*` and `prminxml/*` to provide development and implementation details.
- `hdr/*` or exported interface files: SWI base, names, "internal use" notes.
- any equivalent C reference implementation
- Module header in `s/*`: title, help string, SWI chunk, handler offsets,
  feature flags, command table, message file.
- SWI dispatch code: how R11 or reason registers are decoded, and how
  unknown SWIs branch to errors.
- Entry comments near labels: useful for register contracts, but verify.
- Parameter checks: bit masks, signed comparisons, null cases, and special
  exits.
- Main loops: pointer increments, loop counters, alignment assumptions, and
  final-iteration paths.
- Generated tables: table shape and indexing direction may reveal the true
  algorithm better than prose comments.
- Built binary with `riscos-dumpi`: final code after conditional assembly,
  macro expansion, version conditionals, and linker layout.

## Assembly Patterns To Prove

### Bit And Nibble Order

Do not infer source pixel order from words like "leftmost" in comments. Check
the actual shifts and masks:

- `AND ..., word, LSR shift` with `shift += 4` reads from low bits upward.
- `ORR outword, pixel, outword, LSR #4` packs each new high-nibble pixel while
  shifting earlier pixels downward; the stored word may have the first output
  pixel in the least significant nibble after finalisation.
- A final `MOV outword, outword, LSR #4` before `STR` changes the apparent
  packing order.
- Cross-word cases using `oldword LSR #n` and `newword LSL #(32-n)` may start
  at a different source bit than the regular loop.

Create a tiny data test that prints raw output words. Compare the first word
against candidate interpretations before committing to a data layout.

### Lookup Tables

For generated `DCB` tables:

- Reconstruct the formula by testing table entries, not by trusting nearby
  comments.
- Check whether index 0 is omitted because code avoids zero lookups.
- Check negative indexing such as `LDRB ..., [table, -index]`; the label may
  point to the middle or end of a combined table.
- Check whether version conditionals select a different table layout.

If a direct mathematical translation disagrees with the native module, inspect
the table bytes and derive the weights or values from them.

### Boundary Paths

Read the path after the main inner loop separately. It often handles the last
pixel or the word boundary and may not be equivalent to the regular loop.

Watch for:

- Column counters based on byte stride rather than pixel count.
- "Do not do last pixel" branches that leave the final nibble unused.
- Cross-word reads that intentionally use bits from the next source word.
- Reads which assume spare storage or an unused end bit.
- Null operations such as `SUBS rowcount, rowcount, #3` followed by an
  immediate return on equality.

### Included helper sources

Some RISC OS sources mix assembler dispatch code with included helper
implementations. In the SpriteOp sources, for example, `SprExtend` pulls in the
tiling implementation from `s_c.tile` after `gettile_renderfunc`. If you only
read the entrypoint and stop there, you will miss the real algorithm.

When a routine appears to hand work off to a symbol that is not defined nearby:

* scan the bottom of the file for `GET` includes
* treat those helper sources as part of the same implementation unit
* if code is not provided, ask the user for implementation details or example code

## Error handling

Translate exact error behaviour:

- V set returns R0 as an error block pointer.
- V clear may still corrupt R0 if the contract says so.
- Standard-looking errors may use module-local tokens with standard error
  numbers.
- Parameter checks such as `AND rowcount,#&80000003` also reject negative
  values; preserve that, rather than checking only `value MOD 4`.

For PyModules, raise `RISCOSSyntheticError(ro, number, message)` when matching
an existing module error that is not naturally defined by `error_base`.

## Conversion Strategy

Prefer a clear reference implementation first:

1. Implement a direct version in the target language.
2. Build BASIC tests that calculate expected values independently.
3. Run the tests against the original module.
4. Fix the reference if the original proves different from the comments.
5. Run the same tests against the conversion.
6. Add edge cases for validation failures, empty/null inputs, and final-word
   boundaries.

When converting to a PyModule:

- Define `swi_base`, `swi_prefix`, and `swi_names` from the assembler header.
- Dispatch by SWI offset.
- Use `self.ro.memory[address].byte`, `.word`, `read_bytes`, and `write_bytes`
  for guest memory. Do not use host file or byte objects as substitutes for
  RISC OS memory.
- Preserve guest-visible side effects: output size, untouched padding, error
  flags, and which registers are intentionally left alone.
- Keep the Python code readable; performance optimisations can wait until
  behavioural tests are green.

## Validation Checklist

Before declaring a conversion correct:

- Run tests against the original assembled module and the converted module.
- Include tests for both normal and error paths.
- Include at least one case that crosses an input word boundary.
- Check raw output words, not only rendered images or high-level summaries.
- Re-run documentation lint/build if interface documentation was corrected.
- Note any case where source comments were corrected because the binary proved
  different behaviour.
