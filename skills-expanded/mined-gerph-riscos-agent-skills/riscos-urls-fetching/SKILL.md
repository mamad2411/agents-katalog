---
name: riscos-urls-fetching
description: Fetch URL or URI contents on RISC OS using the Acorn URL_Fetcher module, URL_Register, URL_GetURL, URL_Status, URL_ReadData, URL_Stop, URL_Deregister, URL_ParseURL, proxy setup, protocol enumeration, or URL fetcher protocol modules.
metadata:
  author: gerph@gerph.org
license: MIT
---

# Fetching URLs on RISC OS

Use this skill when code needs to retrieve the contents of a URL/URI on RISC OS. In RISC OS practice, `URL` and `URI` are often used interchangeably, but this API is named `URL`.

The Acorn URL Fetcher module provides a uniform client interface to protocol fetcher modules such as HTTP, HTTPS, FTP, Gopher, File, and similar schemes. It fetches data; it is not the same as launching a URL in the desktop. For desktop launching, use the `riscos-urls-launching` skill.

Public reference: <https://gerph.github.io/riscos-prminxml-staging/prm/html/acorn/url_fetcher/url_fetcher.html>

## Client fetch workflow

A client fetch is performed in a URL session. A session is valid until deregistered and must not be reused for another object fetch.

The usual sequence is:

1. Call `URL_Register` to obtain a session identifier.
2. Optionally call `URL_SetProxy` for session-specific proxy or no-proxy rules.
3. Call `URL_GetURL` to start the transfer.
4. In a desktop task, keep multitasking while repeatedly calling `URL_ReadData` and processing returned blocks.
5. Use `URL_Status` when progress or response information is needed.
6. Call `URL_Deregister` when finished. If the user aborts, call `URL_Stop` first, then `URL_Deregister`.

`URL_ReadData` returns a complete HTTP-compatible response stream: status line, headers, blank line, then body data. Protocol modules should use HTTP/1.0 style responses where possible; clients that only want the body must parse and skip the response headers.

For simple stream-style wrappers, such as a `FILE *` replacement, a useful minimal pattern is:

- Treat a local prefix such as `URL:` as an application convention, strip it, and pass the real URL including its scheme to `URL_GetURL`.
- Call `URL_Register`, save the returned `R1` session identifier, and explicitly provide it as `R1` to every later URL SWI for clarity.
- For a plain read-only fetch, use `URL_GetURL` with `R0` bit 0 set only when providing a User-Agent in `R6`, `R2 = 1` for GET, `R3` pointing at the URL, and no request body in `R4`.
- If `URL_ReadData` returns no bytes and the status has neither the completed bit nor the error bit set, yield while waiting. Desktop tasks should poll from their normal event loop; old command-style examples may use `OS_UpCall` reason 6 to sleep briefly.
- When presenting only the entity body, discard the returned status line and headers on the first read by scanning for the blank line. HTTP-style line endings are normally CRLF; robust code should handle either CRLF or LF.
- On read completion, consume any bytes reported in `R4` before treating the transfer as EOF; completion status and available data should not cause the final copied bytes to be discarded.
- On open/start errors after `URL_Register`, call `URL_Deregister` before freeing local state. On normal close, `URL_Deregister` is sufficient.

When wrapping the API with callbacks, it is useful to remember the last status word and call the data callback when either data is returned or the status changes. Some wrapper clients expect to receive zero-length callbacks for status-only changes. If a callback asks to cancel, mark the transfer aborted and defer freeing the handle until after the callback has returned; otherwise callback re-entrancy can leave the poll loop holding a freed pointer.

For throughput, a wrapper may coalesce small `URL_ReadData` chunks before delivering them to its caller, but it must flush accumulated data when the status changes, the buffer fills, or the transfer completes. Data returned with a status transition still belongs to the stream and must not be dropped.

For buffered wrappers that retain the whole response before handing it off, a useful general pattern is:

- Grow the accumulation buffer in chunks before it becomes completely full, so the next `URL_ReadData` call can continue appending without copying partial state into a temporary buffer.
- Treat header detection as a streaming state machine. Append bytes first, then scan the accumulated prefix for the first blank line; only fire any "headers available" hook once.
- Cache the final status, response code, and extent before deregistering the session, so callers can still inspect completion state after transport cleanup.
- If `URL_Status` has not yet produced a usable response code when the header block is complete, parse the numeric code directly from the leading `HTTP/x.y nnn` status line as a fallback.
- When saving or exposing only the entity body from a buffered response, compute and retain the body offset once the header terminator is known instead of reparsing the whole buffer repeatedly.

## Client SWIs

Define the client SWIs as:

```c
#define URL_Register          0x83e00
#define URL_GetURL            0x83e01
#define URL_Status            0x83e02
#define URL_ReadData          0x83e03
#define URL_SetProxy          0x83e04
#define URL_Stop              0x83e05
#define URL_Deregister        0x83e06
#define URL_ParseURL          0x83e07
#define URL_EnumerateSchemes  0x83e08
#define URL_EnumerateProxies  0x83e09
```

In C code, prefer the exported header when it is available:

```c
#include "URL/URLFetcher.h"
```

It defines the SWIs, method values such as `urlmethod_getobject`, status helpers such as `URL_Status_Complete`, proxy constants, protocol flags, and the `url_parseurl_components_t` parsing structures.

### `URL_Register` `&83E00`

Initialises a client session.

- Entry: `R0 = 0`.
- Exit: `R1 = session identifier`.

Multiple sessions per application are permitted. The module has no fixed session limit beyond available memory.

### `URL_GetURL` `&83E01`

Starts a transfer.

- Entry `R0`: flags.
- Entry `R0` bit 0: `R6` contains a User-Agent string pointer.
- Entry `R0` bit 1: `R4` points to a data block of length `R5`; if clear, `R4` points to a zero-terminated string and `R5` must be `2`.
- Entry `R1`: session identifier.
- Entry `R2`: method word. Bits 0-7 are the protocol-dependent method number; bits 8-15 are method-dependent; bits 16-31 are reserved.
- Entry `R3`: zero-terminated URL string including its scheme.
- Entry `R4`: request data block, usually HTTP-style headers, a blank line, then optional entity body.
- Entry `R5`: length of `R4` data block if `R0` bit 1 is set, otherwise `2`.
- Entry `R6`: User-Agent string if `R0` bit 0 is set; `NULL` or an empty string means use the default.
- Exit `R0`: protocol status word.

For a plain GET, the most common client shape is:

- `R2 = 1`
- `R3 = pointer to zero-terminated URL`
- `R4 = 0`
- `R5 = 2`
- `R6 = 0` unless passing a User-Agent

If the caller is supplying extra request headers or request data, treat `R4`
and `R5` according to the flags rather than assuming a zero-terminated string.

For HTTP POST-style requests, put the extra request headers and entity body in `R4`; do not include the HTTP request line. For simple authenticated GET requests, the data block can just contain extra header lines, for example `Authorization: Basic ...` followed by CRLF; set `R0` bit 1 and pass the exact byte length in `R5`.

Method numbers in `R2` bits 0-7:

- `1`: FTP `RETR`/`LIST`, HTTP `GET`, "get this object".
- `2`: HTTP `HEAD`, "get entity headers".
- `3`: HTTP `OPTIONS`, "get server options".
- `4`: HTTP `POST`.
- `5`: HTTP `TRACE`.
- `6`: reserved to Acorn; do not use.
- `7`: reserved to Acorn; do not use.
- `8`: FTP `STOR`, HTTP `PUT`, "store this object".
- `9`: FTP `MKD`, "create directory".
- `10`: FTP `RMD`, "remove directory".
- `11`: FTP `RNFR`/`RNTO`, "rename object".
- `12`: FTP `DELE`, HTTP `DELETE`, "delete object".
- `13`: FTP `STOU`, "store object unique".

Method numbers `0` and `255` are reserved and must not be used. Method numbers `128`-`254` are reserved for private non-distributed modules.

### `URL_Status` `&83E02`

Reports session progress.

- Entry: `R0 = 0`, `R1 = session identifier`.
- Exit `R0`: cumulative status word.
- Exit `R2`: server response code, using HTTP-style response numbers such as `200`, `401`, or `404`.
- Exit `R3`: total body bytes read so far.
- Exit `R4`: approximate total transaction bytes if known, or `-1`.

Status bits are cumulative and must be tested bitwise:

- Bit 0: connected to server.
- Bit 1: request sent.
- Bit 2: request data sent.
- Bit 3: initial response received.
- Bit 4: transfer in progress.
- Bit 5: all data received.
- Bit 6: error occurred.

Do not assume status values progress in a strict sequence.

`URL_Status_Complete` is commonly defined by client headers as bit 5 OR bit 6 (`URL_Status_AllDone | URL_Status_Aborted`). Polling code should stop when either completion bit is set, then inspect the aborted/error bit to distinguish success from failure. The approximate extent in `R4` may be unknown before entity transfer starts; progress wrappers often wait until `URL_Status_Transfer` is set before treating it as the expected body size.

### `URL_ReadData` `&83E03`

Reads pending response data.

- Entry: `R0 = 0`, `R1 = session identifier`.
- Entry `R2`: receive buffer.
- Entry `R3`: receive buffer size.
- Exit `R0`: status word.
- Exit `R4`: bytes copied into `R2`.
- Exit `R5`: bytes still to be read if known, `0` when complete, or `-1` if unknown.

Keep calling while data is available or until the transfer has completed. When `R5` is `0`, all data has been read. `URL_Stop` is not required after a normal completion; `URL_Deregister` will perform final cleanup.

If `URL_ReadData` returns an error, treat the transfer as failed or aborted and still clean up through the usual deregistration path.

When writing wrappers, do not drop the final block merely because completion is
also reported in the returned status word. Consume the bytes in `R4` first.

## Response headers

The response stream starts with a response/status line followed by headers, a blank line, and then the entity body. Code that needs just the body should split this stream itself or use a small state machine while data arrives.

Robust header splitting should recognise all of these blank-line forms:

- CR CR
- LF LF
- CR LF CR LF
- LF CR LF CR

If headers are accumulated for later parsing, include the terminating blank line in the accumulated header block so the parser can terminate the final field safely. Header parsers commonly ignore the first response/status line, split later lines at the first colon, trim whitespace after the colon, and compare field names case-insensitively. Continuation lines begin with space or tab and belong to the preceding header value.

### `URL_Stop` `&83E05`

Aborts an active request.

- Entry: `R0 = 0`, `R1 = session identifier`.
- Exit `R0`: status word.

Use this for premature termination, such as a user cancelling or quitting during a download. It is an error if there is no request associated with the session.

### `URL_Deregister` `&83E06`

Frees the client session and all session-specific state, including proxy settings.

- Entry: `R0 = 0`, `R1 = session identifier`.
- Exit `R0`: status word.

Call this exactly once for each successful `URL_Register`, even on error paths. Deregistration automatically stops any associated protocol transfer that has not already been stopped.

## Proxy handling

Use `URL_SetProxy` (`&83E04`) to configure proxies.

- Entry `R0 = 0`.
- Entry `R1`: session identifier, or `0` for global proxy settings.
- Entry `R2`: proxy base URL string, such as `http://www-cache.example:8080/`; use `0` to clear proxy settings for the session.
- Entry `R3`: URL prefix to proxy, such as `http:` or `ftp:`, when setting a proxy.
- Entry `R4`: `0` for proxy this prefix, `1` for do not proxy.

Proxy selection order is: client no-proxy, client proxy, global no-proxy, global proxy. Session settings therefore override global settings.

Use `URL_EnumerateProxies` (`&83E09`) to inspect proxy and no-proxy lists:

- Entry `R0` bit 0 clear: enumerate proxy entries.
- Entry `R0` bit 0 set: enumerate no-proxy entries.
- Entry `R1`: session identifier, or `0` for global settings.
- Entry `R2`: context, initially `0`.
- Exit `R2`: next context, or `-1` when finished.
- Exit `R3`: read-only URL or no-proxy prefix.
- Exit `R4`: read-only proxy URL for proxy enumeration; meaningless for no-proxy enumeration.

Do not update proxy lists while enumerating; the module may duplicate or miss entries.

## URL parsing and resolving

Use `URL_ParseURL` (`&83E07`) instead of hand-parsing URLs.

Common entry registers:

- `R0` bit 0: `R5` gives the number of words in the data block; if clear, 10 words are assumed.
- `R0` bit 1: escape character codes 0-31 and 127 using hex encoding. Avoid this unless required.
- `R1`: reason code.
- `R2`: base URL string.
- `R3`: relative URL string, or `NULL`.
- `R4`: data block or output buffer.
- `R5`: block size in words when `R0` bit 0 is set, or buffer size for quick resolve.

The classic parser block has 10 component slots:

1. Fully canonicalised URL.
2. Scheme/protocol, lower-case.
3. Hostname, lower-case.
4. Port.
5. Username.
6. Password.
7. FTP account.
8. Path.
9. Query.
10. Fragment.

The exported `URL/URLFetcher.h` header also defines `url_parseurl_components_t` and `url_parseurl_componentsizes_t` with an 11th `minimal` component after `fragment`. When using those structures, set `URL_ParseURL_WordLengthGiven` and pass `sizeof(url_parseurl_components_t) / sizeof(char *)` or `sizeof(url_parseurl_componentsizes_t) / sizeof(size_t)` in `R5`, otherwise the default 10-word block will not cover the extra field.

Reason codes:

- `0`: return required component buffer lengths in the `R4` word block. Lengths include the zero terminator; absent fields are zero.
- `1`: copy component strings into buffers whose pointers are supplied in the `R4` word block; unused component pointers may be zero.
- `2`: compose a canonical URL from component strings supplied in the `R4` word block.
- `3`: quick-resolve a full URL into the buffer at `R4`, with buffer length in `R5`.

For simple relative URL resolution, prefer reason `3`. Size the buffer as `strlen(base) + strlen(relative) + 4`; if hex escaping is requested, multiply that estimate by three. On exit from reason `3`, `R5` is the remaining buffer space, or negative if the buffer was too small.

The path component does not start with `/` unless the parsed URL explicitly included one. In `http://example/path`, the slash after the hostname is a separator, not part of the path.

A safe full decomposition pattern is:

1. Call reason `0` with `URL_ParseURL_WordLengthGiven` to fill a size structure. Set `URL_ParseURL_EscapeCharacters` if the caller wants control characters escaped in the returned strings.
2. Sum the returned component sizes. Lengths already include terminators, and absent fields have length zero.
3. Allocate one block containing the pointer structure followed by string storage.
4. Set each pointer to the next string slot, or `NULL` for zero-length components.
5. Call reason `1` with the pointer structure and the same word count.

Free the single allocated block when finished. This pattern avoids guessing output lengths and keeps all component strings in one allocation.

## Scheme enumeration

Use `URL_EnumerateSchemes` (`&83E08`) to discover available fetch schemes.

- Entry: `R0 = 0`, `R1 = context`, initially `0`.
- Exit `R1`: next context, or `-1` when finished.
- Exit `R2`: read-only scheme string, if not finished.
- Exit `R3`: read-only help string.
- Exit `R4`: protocol module SWI base.
- Exit `R5`: protocol module version multiplied by 100.

Do not assume enumeration remains stable if protocol modules are loaded or removed between calls. If the URL Fetcher cannot handle a scheme, consider handing it to the URI handler for desktop launching instead.

The module is primed with knowledge of schemes including `mailto:`, `telnet:`, `finger:`, `file:`, `filer_opendir:`, `filer_run:`, `local:`, `gopher:`, `ftp:`, `http:`, `https:`, and `whois:`.

## Implementing protocol fetcher modules

Most applications should not call protocol module SWIs directly. Implement this section only when writing a URL Fetcher protocol module.

Register the protocol module with `URL_ProtocolRegister` (`&83E20`):

- Entry `R0` bit 0: `R5` contains protocol flags.
- Entry `R0` bit 1: `R6` contains default port number.
- Entry `R1`: protocol module SWI base.
- Entry `R2`: supported scheme string, such as `http:`.
- Entry `R3`: version multiplied by 100.
- Entry `R4`: informational string, up to 50 characters, or `0`.
- Entry `R5`: protocol flags if `R0` bit 0 set.
- Entry `R6`: default port if `R0` bit 1 set.

Protocol flags:

- Bit 0: path is not Unix-like.
- Bit 1: no parsing should be performed for this scheme.
- Bit 2: scheme allows `user@` before the hostname.
- Bit 3: hash character is allowed in hostname, for example `file:`.
- Bit 4: no hostname component, for example `mailto:`.
- Bit 5: remove leading `..` path components.

Use `URL_ProtocolDeregister` (`&83E21`) from finalisation code:

- Entry: `R0 = 0`, `R1 = protocol module SWI base`.
- Exit `R1`: number of client sessions that were using the module.

The URL module calls protocol modules through four SWIs starting at the registered SWI base:

- `Protocol_GetData`: SWI base + `0`.
- `Protocol_Status`: SWI base + `1`.
- `Protocol_ReadData`: SWI base + `2`.
- `Protocol_Stop`: SWI base + `3`.

Protocol modules must return standard SWI-not-known error `&1E6` for unsupported SWIs. If a module supports multiple protocols, keep its internal protocol SWI bases at least 16 SWIs apart. Protocol-specific extra SWIs should be allocated from the top of the chunk downwards.

The session identifiers used between the URL module and protocol modules are private to the URL module and are not the same as client session identifiers.

## Service calls and command

Service calls:

- `Service_URLProtocolModule` (`&83E00`), reason `0`: URL module started. Protocol modules should re-register.
- `Service_URLProtocolModule` (`&83E00`), reason `1`: URL module dying. Protocol modules should stop talking to it.
- `Service_URLProtocolModule_ProtocolModule` (`&83E01`), reason `0`: a protocol module registered.
- `Service_URLProtocolModule_ProtocolModule` (`&83E01`), reason `1`: a protocol module deregistered.

These service calls must not be claimed; preserve registers unless the API explicitly says otherwise.

The `*URLProtoShow` command displays registered protocol modules and their SWI bases. Use it for diagnostics.

## Common URL errors

URL module errors occupy `&80DE00` to `&80DE1F`. Common client-facing errors include:

- `&80DE00`: session ID not found.
- `&80DE01`: out of memory.
- `&80DE02`: no matching fetcher for the URL.
- `&80DE04`: session already used for a fetch; sessions cannot be reused.
- `&80DE05`: no fetch in progress because it has already been terminated.
- `&80DE07`: no fetch in progress because `URL_GetURL` has not been called.
- `&80DE0A`: unable to parse URL.

Protocol-specific errors use their own ranges and should be handled as normal `_kernel_oserror` results.

## Practical test coverage

When you implement or review URL fetch support, exercise these behaviours
separately:

- session create and destroy
- simple GET
- GET with explicit headers and User-Agent
- status polling during and after transfer
- repeated `URL_ReadData` until completion
- stop/abort path
- session and global proxy handling
- proxy enumeration
- URL parsing and relative resolution
- scheme enumeration
- protocol register and deregister paths
