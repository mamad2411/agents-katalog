---
name: file-handling
description: Handles uploads, storage, processing and delivery of files safely: type verification by content, size limits enforced before parsing, filename neutralisation, storage outside the served tree, authorised download, signed URLs, image and document processing limits, virus scanning where required, orphan cleanup and retention. Use for any upload, avatar, attachment, import, export or media feature.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, input-validation]
  outputs: [upload-contract, storage-layout, access-policy, processing-limits, retention-rules]
---

# File Handling

A file is untrusted input with a size, a name, a type and content, and every
one of those four lies. Uploads are the shortest path from a stranger to your
storage, your image library and your users' browsers.

The rules below are not paranoia. Each corresponds to a defect class that
ships regularly.

## 1. Upload contract

Decide before implementing:

```
who may upload, and to what
maximum size, per file and per request
accepted types, as a closed list, by content and not by extension
maximum count per operation
where the bytes land, and who can read them afterwards
how long they are kept
what happens to the record if the storage write fails
what happens to the file if the record write fails
```

The last two are the pair that produces rows without files and files without
rows.

## 2. Validation, in this order

```
1 authentication and authorization, before a single byte is accepted
2 declared size against the limit, rejected before the body is read
3 actual size while streaming, enforced with a hard stop
4 content type detected from the bytes, not from the header or the extension
5 the detected type against the closed allow list
6 for structured formats, a parse with limits: dimensions, pages, entries
7 filename neutralised, or discarded entirely in favour of a generated name
8 the storage write, then the database record, in an order that is recoverable
```

Never trust the client's content type header. Never derive a type from an
extension. An executable renamed to end in an image extension is the oldest
trick in this list and it still works against implementations that check the
name.

## 3. Names and paths

```
generate the stored name: an opaque identifier, never the user's name
keep the original name as metadata only, escaped when displayed
never build a path by concatenating user input
reject or strip path separators, parent references, null bytes, control
  characters and leading dots
normalise unicode in names before comparing, since two names can look identical
cap the length of anything derived from a user supplied name
```

## 4. Storage and delivery

```
store outside any directory the web server serves directly
serve through a handler that checks authorization on every request, or
  through a signed URL with a short expiry
signed URLs: short lived, single purpose, and revocable by rotating the key
set the content type from the detected type, never from the stored name
set a content disposition that forces download for anything not displayed
add headers that prevent the browser from sniffing a different type
never serve user uploads from the application's own origin when they can be
  HTML, SVG or anything scriptable
strip metadata that carries location or identity, unless it is the point
```

Serving user content from the main origin is how an uploaded document becomes
a script running with your users' session.

## 5. Processing

```
run conversions and thumbnailing out of the request, in a job
apply limits before decoding: dimensions, pixel count, page count, depth
use a timeout and a memory limit on every conversion
run untrusted formats in an isolated process where the platform allows it
keep the original, or state in writing that it is discarded
handle failure: the record must not claim a derivative that does not exist
never pass a user supplied string into an image or document tool command line
```

Decompression bombs and enormous canvases are denial of service through a
single upload, and the defence is a limit checked before decoding.

## 6. Scanning

Where the product accepts files that are then shared with other people, or
where a regulation requires it:

```
scan before the file becomes reachable by anyone else
quarantine rather than delete, so a false positive is recoverable
record the scan result and the engine version with the file
decide the behaviour when the scanner is unavailable: refuse, or quarantine
```

## 7. Lifecycle

```
orphan cleanup: uploads that never completed, records whose file is gone
retention: how long files live after their record is deleted
deletion: soft delete of a record does not leave the file publicly reachable
export and import: bounded, streamed, and resumable for large sets
storage cost visibility, per tenant where it matters
```

## 8. Prohibitions

- Never accept a file before checking authorization.
- Never trust the extension or the declared content type.
- Never store an upload under a path derived from user input.
- Never serve user uploads from the application origin when they can execute.
- Never decode an image or document before checking its declared dimensions.
- Never interpolate a filename into a shell command.
- Never leave the failure paths undecided: file without a record, record
  without a file.
- Never keep files after the record is gone with no retention rule.

## 9. Protocol

1. Write the upload contract: who, what, how large, how many, how long.
2. Enforce authorization first, then size, then detected type.
3. Generate the stored name and keep the original as metadata.
4. Choose the storage location and the delivery mechanism.
5. Decide the write ordering and the compensation for each failure.
6. Move processing to a job, with limits and timeouts before decoding.
7. Add scanning where the product's sharing model requires it.
8. Set headers on delivery: type, disposition, no sniffing.
9. Write the cleanup and retention jobs, and schedule them.
10. Test with the adversarial matrix in `resources/upload-matrix.md`.

## 10. Auto-critique

Score from 0 to 5: authorization first, content based type detection, size
enforced while streaming, name generation, storage isolation, delivery headers
and authorization, processing limits, failure path compensation, retention and
orphan cleanup, adversarial tests run.

Threshold: no axis below 3, average at least 4. An implementation that
determines type from the extension, or serves uploads from the application
origin, is an automatic failure.

## 11. Interfaces

- Upstream: `input-validation` for the boundary rules, `api-design` for the
  upload contract, `architecture-design` for the storage choice.
- Lateral: `backend-engineering` for the handlers, `background-jobs` for
  processing, `data-privacy` for retention and metadata stripping,
  `security-audit` for the exposure review.
- Downstream: `security-testing` for the adversarial pass,
  `testing-quality` for the permanent tests, `reliability-testing` for storage
  outage behaviour.
