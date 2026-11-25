---
name: writing-cmodules
description: Development notes and procedures for working with RISC OS modules. Describes the layout of the project, how to build and tests, common patterns with SWIs and Vectors. Use when creating RISC OS modules, creating SWI implementations, claiming vectors, or writing service handlers.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-project:*) Bash(riscos-cmunge:*) Bash(riscos-amu:*) Bash(riscos-build-run:*)
---
# C modules

## Agent guidance

Always use the `writing-c` skill when using this skill, as it includes fundamentals
which are not stated here.

When the user or the existing code structure points at a specific layer for the
work, start there and exhaust that path before changing outer plumbing. For
example, if the request is to implement logic in a helper such as
`c/conversion`, do that first and keep `c/module`, CMHG veneers, SWI claiming,
and registration code unchanged unless the target layer clearly cannot satisfy
the request.

Do not let a runtime symptom in a test environment pull you into unrelated
module scaffolding too early. A missing feature result from a test should first
be checked against the intended implementation layer, not assumed to require
changes to SWI registration, claiming, or veneer wiring.

## Module Structure

### New modules

* If the user requests that a module be built and does not provide a definition of the interfaces, ask if they would like you design the module before launching into implementation.
* When asked to design a new module, use the `designing-modules` skill to aid in getting the interfaces correct, *before* beginning the implementation.

**Creating a template project**:

* To create the base files, use `riscos-project create --name <project> --type cmodule --skeleton`
  This will create the files in the current directory.
* Then build the project to confirm that it works before making changes.



### Core Files

A RISC OS module requires three essential components:

1. **CMHG file** (`cmhg/*`) - Module definition describing:
   - Module title and help string (which should start with a capital letter, using Pascal Case).
   - SWI chunk base number
   - Entry points (initialisation, finalisation, SWI handler, veneers and others)
   - SWI decoding table (names of exported SWIs)
   - Error blocks
   - Command definitions

2. **Module interface** (`c/module`) - C code implementing:
   - `Mod_Init()` - Called when module is loaded
   - `Mod_Final()` - Called when module is unloaded
   - `Mod_SWI()` - Dispatches SWI calls to appropriate functions
   - `Mod_Service()` - Dispatches Services to appropriate functions

If the service handler or SWI handler is not required, it can be omitted, and the CMHG entry commented out.

CMHG service handlers have this C signature:

```c
void Mod_Service(int service, _kernel_swi_regs *r, void *pw);
```

Declare the service list in `cmhg/modhead` with `service-call-handler:`. For cache invalidation based on display or palette state, common services include `Service_ModeChanging`, `Service_SwitchingOutputToSprite`, and `Service_DisplayChanged`.
When porting an assembler module, preserve the original service-call register contract explicitly. If the original service path consumes values from `R0`-`R7`, thread those values through the C interface deliberately instead of discarding them in a simplified wrapper.

3. **Makefile** (`Makefile,fe1`) - Build configuration using AMU (RISC OS make)
   - See the `using-makefiles` skill if you need more information on this.

For more information about the CMHG file format, a blank template can be generated for reference with `riscos-cmunge -blank blank`. Do not commit the template file read in this way - always change the module header. See the `using-cmhg` skill for more information.

When editing the CMHG file or Makefiles, retain the commented lines to help guide future authors.


## Module finalisation

`Mod_Final()` must release resources in reverse order of creation, clear global
state, and only report an error when shutdown genuinely has to be prevented.
If finalisation returns an error, the kernel may call it again, so it must be
repeatable and safe after partial cleanup.

Read `references/finalisation-and-errors.md` for detailed finaliser patterns,
error-block examples, and the `o.modhead` linker pitfall.

## SWI interface

* SWIs are numbered relative to the chunk base declared in `cmhg/modhead`.
* Read the generated `h/modhead` header before changing a handler signature.
* Decode register values into typed locals in `c/module`; do not pass raw
  `_kernel_swi_regs` deeper into the implementation.
* Prefer dedicated SWI handlers over one central dispatcher unless every SWI
  genuinely shares the same register contract.
* Unknown SWIs returned from `Mod_SWI()` must return `error_BAD_SWI`.
* Use XSWIs internally so errors are returned explicitly instead of raising.

Read `references/swi-interface.md` for `swi-decoding-table` syntax, naming
pitfalls, handler signatures, and the XSWI convention.

## Module restrictions

* Floating point should not be used in modules - if it is *required*, then refer to the `using-libasm` skill for details of the `fpsvc` functions.
* `exit()`, `assert()` and `about()` must never be used in modules.


## Memory and private word

Use ordinary C globals and heap allocation for module state. Pass `pw` back to
interfaces that require a private word, but never dereference it or overwrite
it when using the Shared C Library.

If the original source used conditional assembly switches, preserve them as
named `#if` or `#ifdef` options instead of collapsing the behaviour into one
path.

Read `references/finalisation-and-errors.md` for the private-word trap,
CMHG-generated error blocks, and time-format notes.


## Build System

### AMU Makefiles

The build uses AMU (RISC OS make) with `,fe1` filetype:

```makefile
OBJS = o.modhead \
       o.module \
       o.hardware

include CModule
```

If a new header is added, the makefile should be updated to add a dependency in the form `h.header`.
For example, if the file `c/hardware` was created and included the module header with `#include "modhead.h"`, a line should be added
beside the additional dependencies like:

```makefile
${OZDIR}.hardware: h.modhead
```

If a new header file like `h/os` is created, it would be included with `#include "os.h"` and the dependency in the makefile is `h.os`:

```makefile
${OZDIR}.hardware: h.os
```

More information about the use of makefiles can be obtained with the `using-makefiles`

### Build Targets

- `riscos-amu` or `riscos-amu ram` - Build absolutes or RAM module
- `riscos-amu rom` - Build ROM module
- `riscos-amu BUILD26=1` - Build 26-bit compatible version
- `riscos-amu BUILD64=1` - Build 64-bit version
- `riscos-amu export` - Export headers/libraries
- `riscos-amu clean` - Remove build artifacts

### Output Directories

Suffix `z` means 'for modules'; no `z` means 'for application'.
Suffix `32` for 32-bit.
Suffix `64` for 64-bit.
No number suffix for 26-bit (obsolescent).

- `o` - object directory.
- `aif` - AIF, application executable.
- `rm` - modules (RAM).
- `aof` - AOF files (ROM).

## Testing

Use a small BASIC smoke test first, then make it repeatable through a project
`test` target. Keep the host filename and the guest leaf name distinct so the
module and the BASIC file cannot collide inside `riscos-build-run`.

Read `references/testing.md` for example `SYS` calls, `riscos-build-run`
invocations, 64-bit limitations, and the leaf-name collision pitfall.

## Debugging

### Debug Output

Use conditional compilation for debug output:

```c
#define DEBUG

#ifdef DEBUG
#define dprintf if (1) printf
#else
#define dprintf if (0) printf
#endif

dprintf("Debug: value=%d\n", value);
```

Note: `printf` output goes to the debug stream, visible in build logs.

When debug is no longer required, comment out the `#define DEBUG` line. Uncomment if it is needed again. NEVER remove the `dprintf(...)` function calls.

### Build Verification

Always verify builds:

```bash
riscos-amu
riscos-build-run rm32 --command "*RMLoad rm32.<module>"
```

Only clean the build if there are problems with the invocation that are not expected (`riscos-amu clean`).

64-bit builds can be tested with a load, but cannot use BBC BASIC:

```bash
riscos-amu BUILD64=1
riscos-build-run --arch aarch64 rm64 --command "*RMLoad rm64.<module>"
```

## CI/CD

CI files can be created automatically and will generate `.robuild.yaml` which contains RISC OS commands to run.
Use `riscos-project create-ci` to create these files for the current project.


## Common features

### Claiming vectors

Vector claims are usually done in the module initialisation code. They must be released on module finalisation. See the skill `using-cmhg` for details on claiming vectors.


### Generic veneers

For non-claimable entry points, like driver registrations, the CMHG `generic-veneer` should be used.
Many modules (CDFSDriver, SCSI, etc.) require passing entry point addresses to the OS or other drivers via a Driver Information Block.
Other interfaces, like timed events (`OS_CallAfter`, `OS_CallEvery`) have a similar entry point.

**Implementation**: Use the addresses of CMHG-generated generic veneers, not the raw C functions.

```c
/* In Mod_Register */
CDFS_DIB *dib = (CDFS_DIB *)r->r[0];
dib->msf_to_lba_fn = (int)Entry_MSFToLBA_Veneer; // Address of the veneer
```

or

```c
_swix(OS_CallAfter, _INR(0,2), 10, Entry_Tick_Veneer, pw); // Veneer address.
```

This ensures the C environment (relocation, static base) is correctly initialized when the function is called from external assembly or the OS. More information on the
patterns used for generic geneers can be found in the skill `using-cmhg`.



## Module Testing Strategies

### Verifying SWIs in BASIC
A simple BASIC script is the most effective way to test a new module. Use the skill `using-bbcbasic` if you need to work with BASIC.

**Example: Testing a complex SWI (CD_DriveStatus)**

```bbcbasic
REM Passing a pointer in R7
DIM control_block% 20
control_block%!0 = device%
control_block%!4 = card%
...
SYS "CD_DriveStatus", 0, 0, 0, 0, 0, 0, 0, control_block% TO status%
PRINT "Status is: "; status%
```
**Key Tip**: Always pass explicit 0s for intermediate registers (R0-R6) to ensure your target register (R7) is correctly populated.

### Verifying Version Blocks
If your SWI returns a pointer to a block of data:

```bbcbasic
SYS "CD_Version" TO v%
PRINT "Version word: "; v%!0
PRINT "Version string: "; FNstring0(v%+4)

DEFFNstring0(p%):LOCAL s$:SYS "OS_IntOn",p% TO s$:=s$
```

## Build and Linker Pitfalls

*   **Missing COMPONENT**: If `COMPONENT` is not defined in the `Makefile`, the build may fail or produce oddly named binaries.
*   **RAM vs ROM**: Ensure you are building the `ram` target for testing.
*   **File Suffixes**: Always ensure your `Makefile` handles dependencies on generated headers:
    `${OZDIR}.module: h.modhead`


## Resources

- [RISC OS PRM - Introduction to SWIs](https://www.riscos.com/support/developers/prm/swis.html)
- [CMHG Documentation](https://www.riscos.com/support/developers/c/writerm.html)

- Manager modules may need to announce that they are starting up and shutting down. Usually services are issued for these events. The module announcements pattern can be found here [references/module-announcements.md](references/module-announcements.md).

- Licenses and authorship may be announced with the module acknowledgements service. Adding this service can be achieved by following the [module acknowledgements pattern](references/module-acknowledgements.md).

- Modules which need to replace OS functionality may claim those `OS_*` SWI calls through `OS_ClaimOSSWI`. More information on this can be found at [claiming-os-swis](references/claiming-os-swis.md).
