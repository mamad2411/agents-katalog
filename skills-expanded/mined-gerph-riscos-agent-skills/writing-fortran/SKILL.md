---
name: writing-fortran
description: Use when writing, reading, updating, building, or reviewing Fortran code in the RISC OS build environment, especially when compiling with riscos64-fortran, linking with C, passing _kernel_swi_regs, handling C/control-terminated strings, or generating Fortran modules from RISC OS header constants.
metadata:
  author: gerph@gerph.org
license: MIT
---

# Writing Fortran for RISC OS

Use this skill for Fortran work in the RISC OS build environment.

Read only the reference files needed for the task:

* Build, source layout, modules, and command lines: `references/building.md`
* C/Fortran interworking, C strings, and `_kernel_swi_regs`: `references/c-interop.md`
* Generated constants and Fortran modules from RISC OS headers: `references/generated-constants.md`
* Common RISC OS build pitfalls and review checks: `references/pitfalls.md`

## Core Rules

Fortran source files live in `f90/` and do not have a `.f90` suffix in the
host filesystem. Use RISC OS-style names with the wrappers, for example:

```sh
riscos64-fortran -c -o o.name f90.name
riscos64-link o.name -lgfortran -o name,ff8
```

Always link `-lgfortran` when any Fortran object is present.

Always use `implicit none` in every `program`, `module`, `function`, and
`subroutine`.

Use modules for shared constants and library code. Fortran module names are
flat; there is no `use riscos/WimpSpace` path syntax. Prefer namespaced module
names such as `riscos_wimpspace`.

For C-facing interfaces, use `iso_c_binding` and `bind(C, name="...")`.

Use `value` in Fortran for scalar arguments passed by value from C.

For `_kernel_swi_regs`, C `regs.r[0]` maps to Fortran `regs(1)`.

Do not read or write generated `.rotransform` files.
