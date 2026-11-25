---
name: riscos-urls-launching
description: Launch URLs or URIs from RISC OS code, Obey files, commands, desktop applications, Wimp tasks, or modules using the AcornURI URI handler, URI_Dispatch, *URIdispatch, URI filetype &F91, or the legacy ANT URL broadcast system with wimp_MOPENURL and URLOpen scheme aliases. Treat URI and URL as interchangeable terms in RISC OS contexts.
metadata:
  author: gerph@gerph.org
license: MIT
---

# Launching URLs on RISC OS

Use this skill when code, scripts, desktop applications, Toolbox programs, modules, or documentation need to open a URL/URI in the user's configured RISC OS desktop handler.

In RISC OS practice, the terms `URI` and `URL` are often used interchangeably. Do not spend effort distinguishing them unless a user explicitly asks for standards terminology; the AcornURI APIs are the normal way to launch web URLs and other URI-like strings.

## Preferred mechanisms

Use the AcornURI handler rather than hard-coding a browser application.

- From C or module code, call `URI_Dispatch` (`&4E381`) with a zero-terminated URL string in `R1`.
- From Obey files, command scripts, tests, or manual instructions, use `*URIdispatch <url>`.
- For a desktop file that represents a URL, use filetype `&F91` (`URI`) and the defined URI file format. Do not set `Alias$@RunType` for filetype `&F91`.
- Do not start `Desktop_AcornURI` directly; use `*Desktop` if the desktop needs to be started.

Reference specification: <https://gerph.github.io/riscos-prminxml-staging/prm/html/acorn/uri_handler/uri_handler.html>

## Simple C launch pattern

For fire-and-forget launching from a desktop task:

```c
#include "swis.h"

#define URI_Dispatch            (0x4e381)
#define URIFlags_DispatchFailed (1 << 0)

_kernel_oserror *launch_url(const char *url)
{
    _kernel_oserror *error;
    int flags;

    error = _swix(URI_Dispatch, _INR(0, 2) | _OUT(0), 0, url, 0, &flags);
    if (error != NULL)
    {
        return error;
    }

    if ((flags & URIFlags_DispatchFailed) != 0)
    {
        /* Report a suitable application error here. */
    }

    return NULL;
}
```

This mirrors the local `URILaunch` example: `R0 = 0`, `R1 = url`, `R2 = 0`, and returned `R0` contains the immediate dispatch flags. This does not request an asynchronous success/failure result.

## Requesting a result

`URI_Dispatch` dispatches asynchronously. If a Wimp task needs a result notification:

1. Set `R0` bit 0 on entry to request a result.
2. Put the Wimp task handle in `R2`.
3. Register for `Message_URI_MReturnResult` (`&4E383`).
4. Match the returned URI handle from `R3` if handling multiple launches.
5. Treat bit 0 of the message flags as failure when set.

For module clients that need a service-call result, set `R0` bit 0 and pass `R2 = 0`; handle `Service_URI` reason 3 and match the URI handle.

If `R0` bit 0 is not set, registering for `URI_MReturnResult` is not enough: no return-result message is requested.

## Checking without launching

To check whether a handler may exist without processing the URL, call `URI_Dispatch` with:

- `R0` bit 0 set, because a result is required.
- `R0` bit 1 set, for check-only mode.
- `R2` set as for the requested result path: Wimp task handle for a Wimp message, or `0` for a service call.

## Handling incoming URLs

Applications or modules that process URLs should participate in the URI handler protocol:

- Wimp tasks inspect `Message_URI_MProcess` (`&4E382`) and acknowledge by returning `Message_URI_MProcessAck` (`&4E384`) only when they can handle the URL.
- Modules inspect `Service_URI` reason 2 and claim the service only when they can handle the URL.
- The URI string pointer supplied by the handler is read-only and temporary. If actually processing it, call `URI_RequestURI` (`&4E382`) to copy the string before returning from the handler.
- If the URL cannot be handled, preserve the required registers and pass the message/service on.

## Environment fallback

The URI handler can start an external handler using variables of the form:

```text
Alias$Open_URI_<scheme> <application-or-command>
```

For example:

```text
Alias$Open_URI_http <Browse$Dir>.!Run
```

Handlers should append to these variables rather than overwriting existing values; the format allows comma-separated handlers.

## Useful constants

- `URI_Version`: SWI `&4E380`
- `URI_Dispatch`: SWI `&4E381`
- `URI_RequestURI`: SWI `&4E382`
- `URI_InvalidateURI`: SWI `&4E383`
- `Service_URI`: service call `&A7`
- `Message_URI_MProcess`: Wimp message `&4E382`
- `Message_URI_MReturnResult`: Wimp message `&4E383`
- `Message_URI_MProcessAck`: Wimp message `&4E384`
- URI filetype: `&F91`

## Legacy ANT URL launching

The older ANT URL launch mechanism is less common now, but still appears in historical software and may be needed for compatibility with ANT Internet Suite era applications.

Prefer AcornURI for new work. Use the ANT mechanism only when maintaining old clients, interoperating with software that documents `wimp_MOPENURL`, or deliberately supporting the legacy broadcast protocol.

### Sending an ANT URL request

Broadcast Wimp message `wimp_MOPENURL` (`&4AF80`) using `Wimp_SendMessage` with event code `wimp_ESENDWANTACK` (`18`).

For a short URL, put a zero-terminated string directly in the message data area. The direct payload supports URLs shorter than 236 bytes and is only suitable when no POST body, MIME type, or target frame/window is needed.

For longer or richer requests, use the indirect form:

- `tag` is `0`.
- `url` identifies the URL string.
- `flags` has bit 0 set only when `body_mimetype` is valid; all other bits are reserved and should be zero.
- `body_file` names form data to POST, or is unset.
- `target` names the browser frame/window, or is unset.
- `body_mimetype` gives the MIME content type for posted data.

The indirect string fields may be unset, offsets within the message data area, or pointers to strings in shared memory. For compatibility with older receiving applications, make the indirect URL string point into the RMA or a dynamic area; older receivers may treat the value as a pointer even when the newer offset form was intended.

Receivers should check the message size before reading optional indirect fields. Very old senders may include only `tag` and `url`.

### Receiving an ANT URL request

A receiving application should:

1. Check whether the direct URL string is present; otherwise decode the indirect fields.
2. Decide whether it can handle the URL scheme. Schemes are case-insensitive.
3. Acknowledge the message before the next Wimp poll only when it will handle the request.
4. Ignore and pass on unsupported URLs.

Typical historical scheme ownership was `http`, `https`, `ftp`, and `gopher` for web browsers; `mailto`, `news`, and `nntp` for mail/news clients; and `ftp` for FTP clients.

### Bounced ANT requests

If the original sender receives the message bounced back, it should try a command fallback using `Wimp_StartTask`:

```text
URLOpen_<scheme> <URL>
```

Applications that handle URL schemes should provide a command-line URL option and set appropriate aliases in their `!Boot` files, for example `Alias$URLOpen_HTTP`, so the fallback can start the right application. If this fallback errors, report that the URL could not be opened.

If no bounce is received, assume another application accepted the URL.

### ANT file URLs

The ANT mechanism documents local RISC OS file paths using the `file:/` scheme. The mapping is:

- RISC OS `.` directory separators become URL `/`.
- RISC OS `/` filename characters become URL `.`.
- RISC OS `#` characters become URL `*`.

For example, a RISC OS path like `ADFS::disc.$.test/html` maps to a URL like `file:/ADFS::disc/$/test.html`.
