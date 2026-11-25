---
name: riscos-throwback
description: Use when adding, reviewing, or debugging RISC OS Throwback support through LibThrowback, DDEUtils_ThrowbackStart/Send/End, DDEUtils_ThrowbackRegister, or desktop editor error reporting from compilers, taskwindows, tools, and build processors.
metadata:
  author: gerph@gerph.org
license: MIT
---
# riscos-throwback

Throwback is the DDEUtils protocol used by command-line tools and taskwindow
programs to report warnings, errors, and informational diagnostics to a desktop
editor or other registered receiver. It lets the receiver present messages that
can usually be clicked to open the affected source file and line.

## When to use it

Use Throwback when a RISC OS tool processes files and can report diagnostics
with a filename, line number, message, and severity. Common examples are
compilers, assemblers, converters, validators, or application build front-ends.

Do not use Throwback for normal logging, progress output, or diagnostics that
cannot be tied to a useful file location. Continue to print human-readable
messages to stdout/stderr as well, because Throwback is only available when a
desktop task has registered to receive it.

## Preferred sender API

If the project can link against the Throwback library, prefer its public header:

```c
#include "Throwback.h"
```

The library exposes:

```c
typedef enum {
    s_warning = 0,
    s_error,
    s_seriouserror,
    s_information
} seriousness_t;

void Throwback(seriousness_t seriousness,
               const char *file,
               int line,
               const char *message);

void vThrowbackf(seriousness_t seriousness,
                 const char *file,
                 int line,
                 const char *format,
                 va_list args);
```

`Throwback()` lazily starts a DDEUtils throwback session on the first call,
registers an `atexit()` shutdown handler, clamps line numbers below 1 to 0, and
sends either an error-detail or informational-detail record. Passing `NULL` for
`file` is ignored.

Use the severity that matches how the desktop should present the message:

* `s_warning`: a warning.
* `s_error`: an error.
* `s_seriouserror`: a serious error.
* `s_information`: an informational note, not an error.

Example:

```c
if (missing_field)
{
    Throwback(s_error, source_path, line_number, "Missing field name");
}

if (deprecated_form)
{
    Throwback(s_warning, source_path, line_number, "Deprecated form used");
}
```

When writing a printf-style helper, format into a bounded buffer with
`vsnprintf()` where the target compiler/library supports it. Some older code
uses `vsprintf()`; do not copy that pattern into new code if a bounded
alternative is available.

## Direct DDEUtils protocol

Use direct SWIs when the project cannot use LibThrowback, needs a precise
protocol sequence, or is implementing a Throwback receiver.

Sender SWIs are:

* `DDEUtils_ThrowbackStart` (`&42587`): start a throwback session.
* `DDEUtils_ThrowbackSend` (`&42588`): send processing, error, or info records.
* `DDEUtils_ThrowbackEnd` (`&42589`): end the session.

Call `DDEUtils_ThrowbackStart` before sending records and
`DDEUtils_ThrowbackEnd` before exiting or when processing is complete. Treat
errors such as "No task registered for throwback" and "Throwback not available
outside the desktop" as non-fatal; the tool should still continue with normal
text output. If Start reports that Throwback is unavailable, suppress further
Throwback SWIs for that processing run and rely on the normal textual
diagnostics.

`DDEUtils_ThrowbackSend` takes the reason code in R0 and reason-specific values
in R2-R5:

* `R0 = 0` (`Throwback_ReasonProcessing`): `R2` points to the zero-terminated
  full pathname of the file being processed.
* `R0 = 1` (`Throwback_ReasonErrorDetails`): `R2` points to the file pathname,
  `R3` is the line number, `R4` is severity (`0` warning, `1` error, `2` serious
  error), and `R5` points to the zero-terminated message.
* `R0 = 2` (`Throwback_ReasonInfoDetails`): `R2` points to the file pathname,
  `R3` is the line number, `R4` must be 0, and `R5` points to the
  zero-terminated informational message.

For direct senders, use this sequence:

1. Start the session with `DDEUtils_ThrowbackStart`.
2. For each file that has diagnostics, send `Throwback_ReasonProcessing` once.
3. Send one `Throwback_ReasonErrorDetails` or `Throwback_ReasonInfoDetails` for
   each diagnostic.
4. End the session with `DDEUtils_ThrowbackEnd`.

Always pass full RISC OS pathnames when possible. Relative filenames may be
harder for a desktop receiver to resolve, especially when diagnostics come from
a build tool with a different prefix or current directory.

## Receivers and editors

A desktop task that wants to receive throwback messages registers with:

* `DDEUtils_ThrowbackRegister` (`&42585`): R0 is the caller's Wimp task handle.
* `DDEUtils_ThrowbackUnRegister` (`&42586`): unregister before the task exits.

Only one task can be registered. Registration fails outside the desktop and can
fail if another task is already registered.

DDEUtils translates sender SWIs into Wimp messages for the registered task. The
message action code is at byte offset `+16`; message-specific payload starts at
`+20` unless noted. These are Wimp message action codes, not SWI numbers:

* `DDEUtils_ThrowbackStart` (`&42580`): start of a dialogue.
* `DDEUtils_ProcessingFile` (`&42581`): `+20` zero-terminated filename.
* `DDEUtils_ErrorsIn` (`&42582`): `+20` zero-terminated filename.
* `DDEUtils_ErrorDetails` (`&42583`): `+20` line number, `+28` severity,
  `+32` zero-terminated description.
* `DDEUtils_ThrowbackEnd` (`&42584`): end of the dialogue.
* `DDEUtils_InfoforFile` (`&42585`): `+20` zero-terminated filename.
* `DDEUtils_InfoDetails` (`&42586`): `+20` line number, `+28` must be 0,
  `+32` zero-terminated informational message.

The documented message grammar is:

```text
ErrorDialogue ::=         <DDEUtils_ThrowbackStart>
                          ErrorsWhileProcessing{ErrorsWhileProcessing}
                          <DDEUtils_ThrowbackEnd>

ErrorsWhileProcessing ::= <DDEUtils_ProcessingFile>
                          ErrorFoundIn{ErrorFoundIn}

ErrorFoundIn ::=          <DDEUtils_ErrorIn>
                          <DDEUtils_ErrorDetails>

InfoDialogue ::=          <DDEUtils_ThrowbackStart>
                          InfoDetails{InfoDetails}
                          <DDEUtils_ThrowbackEnd>

InfoDetails ::=           <DDEUtils_InfoforFile>
                          <DDEUtils_InfoDetails>
```

When implementing a receiver, be lenient. Real tools may omit explicit
processing records, may send multiple files in one session, or may continue
after a recoverable protocol error.

## Implementation checks

When adding Throwback support:

* Keep existing command-line diagnostics; Throwback is an additional desktop
  reporting path.
* Verify that the project links the Throwback library or includes the DDEUtils
  SWI definitions it uses.
* Make session shutdown reliable. If using direct SWIs, pair Start and End on
  all normal exit paths. If using LibThrowback, the library handles this after
  the first diagnostic.
* Avoid sending diagnostics without a filename. The LibThrowback wrapper ignores
  `NULL` filenames.
* Use line 0 for whole-file or unknown-line diagnostics.
* Keep messages concise and user-facing; the receiver may display them in a
  compact list.
* Test both desktop and non-desktop cases. Missing throwback support must not
  make the build or processing operation fail.
