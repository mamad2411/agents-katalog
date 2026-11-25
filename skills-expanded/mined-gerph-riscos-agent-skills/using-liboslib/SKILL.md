---
name: using-liboslib
description: Use when working with the OSLib typed SWI interface library in the RISC OS build environment, especially to identify which headers, functions, and public types exist for Core, Computer, User, or Toolbox APIs and to translate between SWI names and OSLib wrapper names.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Using OSLib

Use this skill when code depends on the OSLib typed SWI interface library.

OSLib in this environment is exported under `/riscos-resources/Export/Lib/OSLib`.
This skill is about the OSLib API surface itself: headers, wrapper naming,
public types, and which function families are provided.

## Default workflow

1. Read `references/overview.md` for the library layout and where to look.
2. Read `references/naming.md` when you need to map between PRM SWI names and
   C wrapper names.
3. Read only the area reference you need: `references/core.md`,
   `references/computer.md`, `references/user.md`, or
   `references/toolbox.md`.
4. For a specific call you are about to use, confirm the exact signature in
   the matching exported header under `/riscos-resources/Export/Lib/OSLib/.../h`.
5. If assembler or DefMod naming matters, inspect the matching `hdr/` file for
   the same component name.

## What the reference files contain

The area reference files are source-derived inventories from the exported OSLib
headers. For each public header they list:

* the public typedef aliases declared there
* the exported wrapper functions declared there

This is intended to answer "what does OSLib provide?" without forcing every
agent to trawl the whole tree.

## Scope notes

* `Core` covers the fundamental OS-facing interfaces such as `os`, `osbyte`,
  `osword`, `osspriteop`, `colourtrans`, `messagetrans`, `territory`, and
  related service and event wrappers.
* `Computer` covers filing systems, `osfile`, `osfind`, `osgbpb`,
  `osfscontrol`, sockets, serial, resourcefs, and machine-level subsystems.
* `User` covers desktop-facing APIs such as `wimp`, `font`, `draw`,
  `drawfile`, `jpeg`, `pdriver`, and task/window helpers.
* `Toolbox` covers the Toolbox core plus object and gadget modules such as
  `window`, `menu`, `iconbar`, `saveas`, `writablefield`, and friends.

## Related environment details

The exported object variants currently present under
`/riscos-resources/Export/Lib/OSLib/o` are:

* `OSLib`
* `OSLib-32`
* `OSLib-64`
* `OSLibzm`
* `OSLibzm-32`
* `OSLibzm-64`

The build-environment documentation also identifies `${OSLIB}` as the OSLib
typed SWI interface library, and the 64-bit toolchain documentation shows
`-loslib` with `-I$RO64EXPORT/Lib/OSLib` as the direct compiler/linker form.

## Limits

This skill inventories OSLib's exported headers. It does not replace the PRMs
for behavioural detail, and it does not describe `RISC_OSLib`, which is a
different library with its own conventions and helper layers.
