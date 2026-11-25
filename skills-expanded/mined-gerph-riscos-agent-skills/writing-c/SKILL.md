---
name: writing-c
description: Coding style and guidance when writing C code. Use whenever C code is being written, read or updated.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-libsearch:*)
---
# Guidance for writing C code.

## Project Structure
* Source file conventions:
    * C source files live in a directory called `c`, and do not have an extension.
    * C header files live in a directory called `h`, and do not have an extension.
    * For example, a C file for writing files might be called `c/file_writer`, and its header would be called `h/file_writer`.
    * Within the source files, the convention is still to use the extension, for example, `#include "file_writer.h"`.
    * The filenames must NEVER be in the form `c/filename.c` or `h/filename.h`.
* Makefile files have names that start with `Makefile` and end with `,fe1`.
    * Makefile include files can be found in the directory `$AMUFILES`.
* Built absolutes: `aif32/<name>,ffa` (32-bit absolute) or `aif64/<name>,ffa` (64-bit absolute)
* Built modules: `rm32/<name>,ffa` (32-bit module) or `rm64/<name>,ffa` (64-bit module)
* BBC BASIC files are named with a suffix of `,fd1`. They do not need line numbers.
* The version number of the project is in `VersionNum`, a C include file which describes values.
* If the project is a module, a `cmhg` directory will exist with a file describing the module definition and entry points.
* If the project name is not otherwise given, the environment variable `$ROBUILD_PROJECT` contains its name.
* RISC OS application names should normally be capitalised and should generally avoid hyphens.
    * For example, prefer `WimpClicks` over `wimp-clicks` for the built application and package name.
* Place separate functionality in separate files. For example, module interfaces should be in `c/module`, and hardware interface would be in `c/hardware`.

In the filesystem:

**Wrong**:
* `c/name.c`
* `h/name.h`

**Correct**:
* `c/name`
* `h/name`


## C Coding style

* Code conforms largely to C89.
    * All variable declarations must appear at the **top of their block**, before any statements. Create new blocks to ensure that variables are scoped in their use. Do not declare variables inline with code.
    * Use `int32_t`, `uint32_t` and friends as appropriate. `int64_t` is not available for 32-bit, but is available in the 64-bit compiler.
    * When representing on-disk or in-memory RISC OS layout fields with a fixed binary size, prefer explicit fixed-width types such as `int32_t` rather than `int`, so the layout remains correct in 64-bit builds.
    * If you get errors from the compiler like `Serious error: <command> expected but found '<type>'`, this probably means that there is a variable declaration in the middle of the function. C89 requires that variable declarations be at the start of the block.
* Braces go at the start of lines (not the ends).
* Indentation is 4 characters.
* Do not leave trailing spaces, even on blank lines.
* Magic numbers and strings (bare numbers and strings in the code) should be avoided.
    * Use `enum` if you need to enumerate a set of values like state values.
    * Use `#define` for values like bit-fields and constant strings.


### No Threading

RISC OS is single-threaded. Do not use threading or assume re-entrancy.



### Includes

* You may use includes `stdint.h` and `stdbool.h` if needed.
* Interfacing with the OS and calling SWIs will usually need `kernel.h` and `swis.h`.
* Include `stdlib.h` for NULL when needed.


### Commenting

* Retain comments where they remain correct.
* Add comments to describe intent.
* Functions should include a prologue comment to describe the function's purpose and arguments, in a similar style to the rest of the project.
* Both C and H files should contain a prologue comment to describe the file's purpose, and its relationship to others in the project, if necessary.

*File prologues*:

```c
/*******************************************************************
 * File:        filename
 * Purpose:     Description
 * Author:      AUTHOR
 ******************************************************************/
```

*Function prologues*:

```c
/*******************************************************************
 Function:      function_name
 Description:   Description of function
 Parameters:    var = value
 Returns:       none
 ******************************************************************/
```

## 64-bit build notes

* Treat the 64-bit build as a stricter compiler pass, even when the 32-bit Norcroft build is happy.
* Do not define a private `static` helper with the same name as a shared helper already declared in a header. The 64-bit toolchain will reject this immediately.
* Code that calls low-level kernel helpers should be checked for 64-bit visibility and availability. If a helper is not available for `__riscos64`, either provide a real 64-bit implementation or return an explicit unsupported/error result rather than relying on implicit declarations.
* Keep 32-bit-only SWI or ABI dependencies behind narrow helper functions so they can be `#ifdef __riscos64` guarded cleanly.

## Porting graphics-dependent code

When porting code that talks to the graphics or pointer system, separate it into:

* pure algorithmic control flow
* state queries
* side-effect backends

This makes it possible to implement and test the orchestration logic before the
real plotting or output backend exists. For example, tiled sprite plotting can
be implemented as:

* local tile placement logic
* a support hook to read graphics bounds and eig factors
* repeated calls into the lower-level sprite plotting reason

That keeps partial implementations honest and avoids hard-coding fake graphics
behaviour into otherwise reusable logic.

When part of the implementation drops below the normal graphics interfaces and
touches screen memory directly, isolate that path behind dedicated helpers.
That makes it easier to keep cursor removal, mode checks, and 32-bit/64-bit
differences local to the framebuffer code instead of leaking through the
general rendering logic.

## Porting record-based BASIC code

When porting BBC BASIC code that uses fixed-offset records and ad hoc blocks:

* Convert the record layouts into explicit C structures with descriptive member names before rewriting the higher-level logic.
* Pull narrow behavioural rules into pure helpers where practical, especially for geometry adjustment, selection arithmetic, and message-block construction.
* For Wimp or clipboard protocols, separate block construction from message sending so the protocol details can be regression-tested without a live desktop session.

## Self-test reporting

When tests are skipped because of OS version or environment restrictions, count
and report the skipped cases explicitly. Do not silently reduce the apparent
coverage of the test run.

## Compilation and linking errors

* **"Serious error: <command> expected"**: This is almost always a C89 violation where a variable was declared after a statement. Move all declarations to the top of the `{ }` block, or wrap the logic in a new `{ ... }` block:

```c
void my_function(void)
{
    int i = 0;
    do_something();
    {
        int j = 5; // Valid in C89 because it's at the top of this sub-block
        do_more(j);
    }
}
```

* **Static/non-static declaration mismatch**: Check whether a source file has redefined a helper which is already declared in a shared header or implemented elsewhere.
* **Undefined symbols at link time**: Check if `o.modhead` (the CMHG object) or your assembly objects (e.g., `o.veneer`) are missing from the `OBJS` variable in your makefile.
* **Implicit declaration warnings in 64-bit builds**: Treat these as real porting work, especially for SWI wrappers and kernel helper entry points.


## Standard C files
* The C includes for RISC OS can be found in the directories:
    * `/riscos-built/Export/C/` and `/riscos-built/Export/Lib` - searched first.
    * `/riscos-resources/Export/C/` and `/riscos-resources/Export/Lib` - searched second.
* Use `riscos-libsearch` to find exported headers, libraries, functions and defines:
    * `riscos-libsearch ScreenSave` - find a function or define by name.
    * `riscos-libsearch Sprite.h` - find matching headers and their host filenames.
    * `riscos-libsearch --symbols riscos/Sprite.h` - list symbols from a header.
    * `riscos-libsearch --lib RISC_OSLib` - show a library's headers, objects and symbols.
    * `riscos-libsearch --lib-list` - list known libraries.
* `riscos-libsearch` reads the baked system index from `/riscos-resources/Export/Lib/libraries.db` and, when present, the user-built index from `/riscos-built/Export/libraries.db`. Built results take priority over system results for the same include path.
* If `/riscos-built/Export` has changed and lookup results look stale, run `riscos-libsearch --index` to rebuild the user-built index.
* RISC OS interface values and constants can be found in the following includes (include name `riscos/NAME.h` is held in file `riscos/h/NAME`):
    * `riscos/CMOS.h` - NVRAM values
    * `riscos/DynArea.h` - Dynamic area constants
    * `riscos/EnvNumbers.h` - Program environment registration values
    * `riscos/Events.h` - Event numbers
    * `riscos/FileTypes.h` - RISC OS file type numbers
    * `riscos/Heap.h` - `OS_Heap` constants
    * `riscos/Messages.h` - Wimp message numbers
    * `riscos/ModeVariables.h` - `OS_ReadModeVariable` and `OS_ReadVduVariables` values
    * `riscos/ModHand.h` - RISC OS module area constants
    * `riscos/NewErrors.h` - Error numbers and standard strings
    * `riscos/OSPlatformFeatures.h` - Platform information
    * `riscos/OSReadSysInfo.h` - OS information
    * `riscos/OSScreenMode.h` - Screen mode selection and information
    * `riscos/Oswords.h` - `OS_Word` constants
    * `riscos/Pointer.h` - `OS_Pointer` constants
    * `riscos/Services.h` - Service numbers.
    * `riscos/Sprite.h` - `OS_SpriteOp` constants
    * `riscos/UpCall.h` - `OS_UpCall` constants
    * `riscos/Vectors.h` - Vector numbers
