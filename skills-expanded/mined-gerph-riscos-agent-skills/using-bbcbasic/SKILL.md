---
name: using-bbcbasic
description: Syntax and usage for BASIC on RISC OS. Use this whenever you are creating, editing or reviewing BASIC code (files which end in `,fd1`).
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-build-run:*) Bash(host-open:*)
---
# BBC BASIC

## Summary

* BASIC programs in textual format have a filename which ends with `,fd1` and does not have an extension. Prefer creating textual format files.
* BASIC programs in tokenised format have a filename which ends with `,ffb` and does not have an extension. Never edit tokenised files. Tokenised files can be decoded with:

    riscos-basicdetokenise -i PROGRAM,ffb -o OUTPUT,fd1
    riscos-basicdetokenise -i PROGRAM,ffb

  Always use the `-i` form. Do not call `riscos-basicdetokenise PROGRAM,ffb`
  without `-i`; that only prints the syntax message.

* Line numbers should not be used.

* Start programs with:

    REM >filename
    REM purpose
    ON ERROR ERROR EXT ERR, REPORT$ + " at line " + STR$(ERL/10)

* To run a program run the command:

    riscos-build-run PROGRAM,fd1 --command "run PROGRAM"

    * `INPUT` will not work within programs executed this way (the system will reset).

* To save a screenshot as a PNG use:

    *ScreenSave -native <riscos-filename>

* To run the program and return a screenshot, use a command like:

    riscos-build-run PROGRAM,fd1 --command "run PROGRAM" --command "screensave -native screen" --return-file screen --return-to screen.png

* To show the user a screenshot, use the shell command `host-open screen.png`.

## Detokenising for review

When reviewing or porting tokenised BASIC libraries:

* Detokenise the file first with `riscos-basicdetokenise -i <file>` before reasoning about symbol names, menu strings, or record-field use.
* Treat `riscos-basicdetokenise <file>` without `-i` as wrong; it does not detokenise the file.
* Treat the detokenised output as the source of truth for behaviour matching. Token streams can hide the real identifiers and make control flow or string content easy to misread.

## Structure

* Statements may be separated by a `:` character, but this is discouraged.
* Multi-line `IF` statements, `FOR`, `REPEAT` and `WHILE` loops should be indented by 2 characters.
* Procedures are defined with a line starting `DEFPROC<name>` or `DEFPROC<name>(param1,param2,...)`, and are invoked with `PROC<name>`
* Strings are stored in variables that end in a `$`, for example `name$`.
* Integers are stored in variables that end in a `%`, for example `cows%`.
* Variable names, procedure names and function names must not start with BASIC keywords.
* Prefer using variable, proceure and function names in lower case, preferably using snake case when multiple words are used.

## Graphics

Graphics co-ordinates on RISC OS use:

* Y=0 at the bottom, positive up the screen, negative below the screen.
* X=0 at the left, positive right across the screen, negative to the left of the screen.
* Units are (for most modes) double the resolution, so a 640x480 screen has addressable units of 1280x960.

Before you declare anything complete when drawing graphics, check that you've really got the co-ordinates right.

To select a resolution, use:

    MODE "X<xpixels> Y<ypixels> C<colours>"

For tests that require a specific colour depth, prefer an explicit mode string such as `MODE "X640 Y480 C256"` rather than relying on a numeric mode number. Numeric modes vary by environment and may not have the expected depth.

For paletted modes (where you can change the colours) you would usually use a 16 colour mode
like `MODE 27`, which is 640x480 pixels.

If you are using colour, always check that the colours you are using are what comes out - often the red and green components have been confused.

To clear the screen to a paletted colour, set the background colour first:

    GCOL 0,128+colour
    CLG

To plot triangles, use:

    MOVE <x0>,<y0>
    MOVE <x1>,<y1>
    PLOT 85,<x2>,<y2>

To flood fill, use:

    PLOT 133, <x>, <y>

For more information on the graphics system, use the skill `riscos-output` which describes graphics calls, VDU sequences, colour selection, fonts and sprites in much more detail.

### Colours

In 256 colour modes, select colours using the `OS_SetColour` SWI call. This is necessary because the `GCOL` interface require the use of `TINT` in a 256 colour mode, which makes for a much more complex colour selection.

Do not use `GCOL 0, RND(255)` (the colour numbers for 256 colour modes in GCOL are only selectable up to number 63, with the tint providing the remaining 2 bits). Use `SYS "OS_SetColour", 0, RND(255)` instead.

When selecting colours, you can use RGB colour selection by using the call `SYS "ColourTrans_SetGCOL", &BBGGRR00,,,0,0` to set the foreground graphics colour to the closest RGB colour. To set the graphics background colour to a RGB colour, use `SYS "ColourTrans_SetGCOL", &BBGGRR00,,,128,0`, and then `CLG` to clear the whole screen.

The ColourTrans calls are preferred over the `GCOL` calls as they allow the code to be safe for use in any screen mode.

## Text on the graphics screen

Text co-ordinates on RISC OS use:

* Y=0 at the top, positive down the screen.
* X=0 at the left, positive right across the screen.

To write text on the screen at the text cursor, use `VDU 31, <xchar>, <ychar>`. Text characters are
8 pixels by 8 pixels.

To write text on the screen at the graphics cursor, use `VDU 5` to enable writing to the graphics
cursor, then `PRINT` the text, and finally `VDU 4` to return to the text cursor.

## System calls (SWIs)

System calls can be made with the `SYS` keyword, which can be given a string or a number for the
SWI to call, followed by values for the input registers. For example, to call `OS_ReadModeVariable`
with R0=-1 and R1=3, and return R2 into `ncols` you would use
`SYS "OS_ReadModeVariable",-1,3 TO ,,ncols`.

If you want to check for errors, use the X-prefixed version of the SWI name, and return the flags,
in the form `SYS "Xswiname", r0,r1,r2,... TO r0,r1,r2 ;flags%`. Bit 0 of `flags%` will be set if an error (V flag) was returned.
If the error was returned, the error number will be in the memory at r0+0, which you can read with `r0!0`.
Up to 10 registers can be passed into the SWI and returned.

Example usage of non-erroring SWI call:

```basic
REM BBC BASIC - use X-SWIs for error handling
SYS "XTimer_ReturnNumber", 0 TO r0%,r1%,r2%;flags%
IF flags% AND 1 THEN
  error_num% = r0%!0 : REM Error number at R0+0
  PRINT "Error returned: &";~error_num%
ELSE
  PRINT "Timers count: ";r0%
ENDIF
```

It is redundant to use X-SWIs and raise errors if nothing is being handled.

**Wrong**:
```basic
SYS "XModule_Parse", file$ TO h%; flags%
IF (flags% AND 1) THEN SYS "OS_GenerateError", h%
```

**Correct**:
```basic
SYS "Module_Parse", file$ TO h%
```

This implicitly raises the error.

### Converting C code

C calls can be translated to BASIC SYS calls. A C call using `_swix` takes a SWI number (which is always called as an X-SWI), input registers (`_IN(reg)`) or a range of input registers (`_INR(low, high)`), and output registesr (`_OUT(reg)`) or a range of output registesr (`_OUTR(low, high)`). For example a C call like:

    _kernel_oserror *err;
    err = _swix(OS_Plot, _INR(0, 2), inr0, inr1, inr2);

Might be represented in BASIC as:

    SYS "XOS_Plot", inr0%, inr1%, inr2% TO err% ;flags%
    IF flags% AND 1 THEN
        REM error pointer is in err%
    ENDIF

A C call using `_swi` will raise an error if it fails. It is therefore equivalent to the non-X version of a SWI. A C call like:

    _swi(DrawFile_Render, _INR(0, 5), flags%, drawdata%, size%, matrix%, rect%);

Would be directly equivalent to:

    SYS "DrawFile_Render", flags%, drawdata%, size%, matrix%, rect%

The `_kernel_swi` convention passes 10 registers in a `_kernel_swi_regs` structure,
and returns them into a second structure. Usually the output registers are the same.
The SWIs are always called as X-SWIs, even it they are not specified as such.
For example:

    _kernel_oserror *err;
    _kernel_swi_regs regs;
    regs.r[0] = inr0;
    regs.r[1] = inr1;
    regs.r[2] = inr2;
    err = _kernel_swi(OS_Plot, &regs, &regs);

Is equivalent to:

    SYS "XOS_Plot", inr0%, inr1%, inr2% TO err% ;flags%
    IF flags% AND 1 THEN
        REM error pointer is in err%
    ENDIF

## Accessing memory

### Reading
* Read a byte at an address: `byte% = ?ptr%`
* Read a byte at offset 4: `byte% = ?(ptr% + 4)` or `byte% = ptr%?4` (*never* `byte% = 4?ptr%`)
* Read a word (32-bits) at an address: `word% = !ptr%`
* Read a word (32-bits) at offset 4: `word% = !(ptr% + 4)` or `word% = ptr%!4` (*never* `word% = 4!ptr%`)
* Read a CR-terminated string at an address: `str$ = $ptr%`
* Read a CR-terminated string at offset 4: `str$ = $(ptr% + 4)` (*never* `str$ = $ptr%+4`)

0-terminated strings are not easily readable with operators, and are usually implemented by a helper function at the end of the file:

    DEFFNstring0(ptr%)
    LOCAL s$
    SYS "OS_IntOn",ptr% TO s$
    = s$

### Writing
* Write a byte at an address: `?ptr% = byte%`
* Write a byte at offset 4: `?(ptr% + 4) = byte%` or `ptr%?4 = byte%` (*never* `4?ptr% = byte%`)
* Write a word (32-bits) at an address: `!ptr% = word%`
* Write a word (32-bits) at offset 4: `!(ptr% + 4) = word%` or `ptr%!4 = word%` (*never* `4!ptr% = word%`)
* Write a CR-terminated string at an address: `$ptr% = str$`
* Write a CR-terminated string at offset 4: `$(ptr% + 4) = str$` (*never* `$ptr%+4 = str$`)

0-terminated strings are not easily writable with operators, and are usually implemented writing a string with an 0, and then overwriting the CR afterwards (if needed). For example, to write the string `Hi!` to memory, followed by a 0-terminator you might use:

    $ptr% = "Hi!"+CHR$0

## Heap-managed allocation

For programs which need C-like dynamic allocation, especially desktop applications which keep many buffers or variable-sized structures alive for a long time, see [references/heaplib.md](references/heaplib.md).

The skill also includes a reusable plain-text copy of the non-debug library at `assets/HeapLib/HeapLib,fd1`.


## Common pitfalls

**Bad variable names**:
If the program reports a syntax error, for a variable assignment or use, check the variable name.
Variable names must not start with a BASIC keyword, and will report `Syntax error` if they see this.

Do not:

```
ORBIT = 5
PICTURE$ = "filename"
PROCESS =  TRUE
TANGENT = 0
VALUE% = 10
```

Instead use variables in lower case to avoid the problem:

```
orbit = 5
picture$ = "filename"
process =  TRUE
tangent = 0
value% = 10
```

**Unknown location of the problem**:
If an error occurs, but the program does not report ` at line <number>`, this may mean that there is no error handler to help in this process. If the line number is given, but is far too high for the program, this may mean that the error handler is not reporting the right number. BASIC will renumber lines, in increments of 10, so we must divide the error line (`ERL`) by 10.

Early in the file there should be an error handler like:

```
ON ERROR ERROR EXT ERR, REPORT$ + " at line " + STR$(ERL/10)
```

This will cause the program to exit.

**Syntax error on lines with comments**:
It has been common to not use `:` separator for statements and comments.

Do not:

```
name$ = "bob"   REM user's name
circles = 7  REM how many to draw
```

Instead do this:

```
name$ = "bob" : REM user's name
circles = 7 : REM how many to draw
```

**Using a 256 colour mode with GCOL**:

Using `GCOL` to select colours in a 256 colour mode does not work as you expect. Colours are selected in the form `GCOL <base-colour> TINT <tint>` where <base-colour> is a value from 0-63 and <tint> is a value 0, 64, 128, or 192 for each of the lower bits of the colour. The tint adds progressive lightness to the colour.

Instead of this, use `OS_SetColour`, eg `SYS "OS_SetColour",0,<colour>` which allows the full 256 colour range to be used.

**Tilde (`~`) is a PRINT format modifier only**:

The `~` prefix formats a number as hexadecimal, but it is only valid as a format modifier
directly inside a `PRINT` statement (or `PRINT ... ;` chain). It cannot be used inside a
string expression.

```basic
PRINT ~n%             : REM OK - prints n% in hex
PRINT "val: ";~n%     : REM OK - prints "val: " then hex n%
```

To embed a hexadecimal number inside a string, use `STR$~`:

```basic
msg$ = "value is &" + STR$~n%     : REM correct
msg$ = "value is &" + ~n%         : REM WRONG - syntax error
```

**`ON ERROR LOCAL` cannot be used at top level**:

`ON ERROR LOCAL` installs a local error handler that is only valid inside a `PROC` or `FN`.
Using it at the top level of a program (outside any procedure) causes a
"badly nested error handler" error.

Use `ON ERROR` (without `LOCAL`) at top level, or move the guarded code into a `PROC`:

```basic
REM at top level, use the plain form:
ON ERROR ERROR EXT ERR, REPORT$ + " at line " + STR$(ERL/10)
```

For per-call error trapping without a procedure boundary, use X-prefixed SWIs and check
bit 0 of the flags variable instead of relying on `ON ERROR LOCAL`.

## BASIC smoke tests

When BASIC is used for smoke tests or SWI probes:

- `--command` runs OSCLI, not BASIC statements.
- Put `SYS`, `MODE`, loops, and assertion logic in the BASIC file itself.
- Pass the host file on the command line and use the RISC OS filename in the
  `Run` command.
- Use XSWIs in tests when you need to inspect the returned error block or flags.

## References

* For the full BBC BASIC commands list, see [references/commands.md](references/commands.md).
* For dynamic heap allocation patterns, relocatable blocks, and garbage collection hooks, see [references/heaplib.md](references/heaplib.md).
