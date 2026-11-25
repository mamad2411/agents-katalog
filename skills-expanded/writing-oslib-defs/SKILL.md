---
name: writing-oslib-defs
description: Use when writing, reading, or reviewing OSLib Def interface description files, or when generating C headers, ObjAsm veneers, assembler/C SWI headers, SrcEdit help, or StrongHelp content from them with riscos-defmod.
metadata:
  author: gerph@gerph.org
license: MIT
---

# Writing OSLib Def files

A Def file is a compact, declarative description of an OSLib-style RISC OS
interface: module metadata, types, constants, and SWI signatures. One
reviewed Def file is processed by `riscos-defmod` to derive C headers, ObjAsm
veneers, assembler headers, SrcEdit help, and StrongHelp content, so the Def
file is the source of truth and the generated files are build artefacts.

Read only the reference files needed for the task:

* Full grammar (types, structs, SWI entry/exit conditions, literals): `references/grammar.md`
* `riscos-defmod` command-line flags and output-format selectors: `references/command-line.md`

## The one rule that will trip you up

**The semicolon between declarations is a separator, not a terminator.** A
trailing semicolon after the *last* top-level declaration in the file is a
syntax error reported at end of file, even though every other pair of
declarations must be separated by one. Verified directly against the real
`defmod` binary and against `oslibsrc/Core/def/portable`, a genuine
production Def file, which itself ends on a bare closing parenthesis with no
trailing semicolon.

```
TITLE Example "Example OSLib interface";
AUTHOR "Example Author";
NEEDS os;
CONST ExampleReason = .int: 1 "Primary reason code";
TYPE ExampleBlock = .struct (.int: value, .bool: enabled);
SWI Example_DoThing = (NUMBER &54321 "DoThing",
                       ENTRY (R0 -> ExampleBlock: block,
                              R1 # ExampleReason),
                       EXIT (R0! = .int: result, R1 ?))
```

Note there is no semicolon after the closing `))` of the `SWI` declaration,
because it is the last declaration in the file. If another declaration
followed it, that `SWI` declaration would need a trailing semicolon to
separate it from the next one.

## Minimal worked example

This is the smallest realistic file: metadata, one constant, and one SWI.

```
TITLE Example;
AUTHOR "Test Author";
NEEDS OS;

CONST
   ReasonCode = .Int: 5 "Reason code for the SWI";

SWI
   Example_Call =
   (  NUMBER &12345 "Example call",
      ENTRY
      (  R0 = .Int: value,
         R1 # ReasonCode
      ),
      EXIT
      (  R0! = .Int: result
   )  )
```

Type and keyword names are matched case-insensitively by the lexer, so
`.Int`/`.int`, `TITLE`/`title`, and similar pairs are equivalent; pick one
style and stay consistent within a file.

## Running riscos-defmod

`riscos-defmod` reads the Def file from standard input; most output forms
write to standard output, so redirect them yourself:

```sh
mkdir -p h s
riscos-defmod -h   < InterfaceDef > h/interface       # C header
riscos-defmod -hdr < InterfaceDef > h/interface_asm    # ObjAsm header
riscos-defmod -s -byte_wide bytewide.txt < InterfaceDef > s/interface  # ObjAsm veneers
```

Directory-producing modes (`-l`, `-cstrong`) take `-o <dir>` and create that
directory themselves; everything else relies on the shell redirection, so the
destination directory for those must already exist:

```sh
riscos-defmod -l -o LibraryOut -26bit -32bit < InterfaceDef
```

See `references/command-line.md` for the full flag list, including which
historical flags (`-p` for Pascal, `-asmstrong`) are accepted by the parser
but do not actually produce output.

## Workflow

1. Write or edit the `.Def` source describing the interface (types,
   constants, SWI signatures).
2. Generate the header(s) and veneer(s) you need with `riscos-defmod`.
3. Build the generated `.s`/`.o` veneer alongside your C source in the normal
   way; see `using-makefiles` for wiring this into a project's build.
4. Keep the Def file under source control as the reviewed artefact; treat
   generated output as disposable and regenerate it on each build.

## Style guidelines

* Keep one `Def` file per logical interface (module or shared header), named
  to match its `TITLE`.
* Use `NEEDS` to declare cross-interface dependencies explicitly rather than
  relying on include order in generated headers.
* Prefer named `TYPE` declarations over inline `.struct`/`.union` expressions
  when a structure is used by more than one SWI, so the generated header
  gives it a stable name.
* Use the starred-description form (`NUMBER &12345 "description"` or a bare
  `*`) on SWI numbers and constant reason codes you want exposed as named
  manifest constants in generated headers; omit it for values that are
  implementation detail only.
* Do not hand-edit generated headers, veneers, or help output — re-run
  `riscos-defmod` after editing the Def file instead.
