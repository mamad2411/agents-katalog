---
name: symfony-yoandev-storage
description: >-
  Decide what happens to an uploaded file once the controller has it: public under
  public/ or protected behind a controller, Flysystem so local development and S3 in
  production run the same code, a generated storage key with the original filename kept
  in the database, deletion that leaves no orphan file, and validation that actually
  inspects the bytes. Use this skill whenever someone asks to let users upload a
  document, add a profile picture or a book cover, attach a PDF or an invoice to a
  record, asks "where do the files go", wants to serve or download a stored file, wants
  only the owner to see a file, wants to add S3 or object storage or install Flysystem
  — and whenever a file is not found after deploying, an upload fails with an empty
  422, files pile up after their record is deleted, or the URL of a private file turns
  out to be guessable.
---

# File storage

> **Tier: on demand** — applies the moment the application accepts a file. From then on, the public-versus-protected decision is core; Flysystem and object storage are the price of the suite's container deployment.

Where an uploaded file goes, how it comes back out, and what the database holds.

`symfony-yoandev-http` covers receiving the upload — `#[MapUploadedFile]`, files inside a
payload DTO, the constraints that run at the boundary. This skill starts one line
later, at the point where a controller holds a valid `UploadedFile` and something has
to decide what to do with it.

## Start here: a file under `public/` has no access control

```php
// Every authorisation rule in the project is now irrelevant for this file.
$file->move($this->getParameter('kernel.project_dir').'/public/uploads', $file->getClientOriginalName());
```

`public/` is the web server's document root. FrankenPHP, nginx and Apache serve what
they find there without ever entering PHP, so `access_control`, `#[IsGranted]` and
every Voter in the project are bypassed — not defeated, simply never invoked. One line
walks around the whole security chapter.

Keeping the original filename makes it worse: `/uploads/contrat-durand-2026.pdf` is a
URL an attacker guesses rather than finds. And `move()` preserves whatever extension
the client sent, so `evil.php` lands in the document root of a machine configured to
execute PHP.

Two details verified in `vendor/`, because they change *which* precaution matters:

- **`UploadedFile::move()` does defend against path traversal.**
  `File::getName()` normalises `\` to `/` and keeps only what follows the last slash,
  so a client filename of `../../public/evil.php` is written as `evil.php`. Traversal
  is not the hole. The surviving *extension* is.
- **Flysystem also rejects traversal**, throwing `League\Flysystem\PathTraversalDetected`
  for a key containing `../`. So a storage key read back from the database cannot escape
  its root either.

## The decision that comes before everything else

| | Public | Protected |
|---|---|---|
| Examples | Book cover, avatar, public catalogue image | Invoice, contract, a reader's export, anything belonging to one user |
| Where | `public/uploads/…` in dev, an object-storage bucket with a CDN in production | Never under `public/`. A private bucket, or a directory outside the document root |
| Served by | The web server or the CDN, no PHP | A controller that checks authorisation, then streams the file |
| URL | Stable, may be cached publicly | Route with an id, or a short-lived signed URL |

Anything you cannot confidently put in the left column belongs in the right one.
Moving a file from public to protected later means changing its URL everywhere and
accepting that the old URL was already crawled; the reverse costs nothing.

## Local disk breaks on this suite's deployment target

`symfony-yoandev-deployment` ships Docker containers. A file written to a container's
filesystem is gone on the next deploy and invisible to every other replica — which
produces the symptom people report as "the file is not found after deploying" or "it
works, but only sometimes". A volume fixes the first half and not the second.

So: **object storage (S3 or a compatible service) is the default for anything that
must survive a deploy, and local disk is a development convenience.** The way to have
both without two code paths is Flysystem.

```bash
composer require league/flysystem-bundle              # 3.7.x, pulls league/flysystem 3.x
composer require league/flysystem-async-aws-s3 async-aws/s3   # production adapter
composer require --dev league/flysystem-memory        # in-memory adapter for tests
```

Verified: none of these are installed in the reference project — the recipe writes
`config/packages/flysystem.yaml` with a single local storage, which is a starting point
and not the final configuration. Configuration, autowiring and the traps:
`references/storing-files.md`.

Rejected: `vich/uploader-bundle`. It works, but it drives uploads from Doctrine
lifecycle events on the entity, which is exactly the behaviour-on-an-entity this
standard keeps out (see below). Also rejected: writing to `%kernel.project_dir%` by
hand — it is the same code as Flysystem's local adapter with none of the escape route
to S3.

## What the entity holds, and who deletes the file

The entity holds a **storage key** and the display metadata. Never the bytes, never an
absolute path — an absolute path stops being true the moment the file moves to S3.

```php
#[ORM\Column(length: 255, unique: true)]
private string $storageKey;          // 2026/08/rapport-de-lecture-bbf84f80546c6e68.pdf

#[ORM\Column(length: 255)]
private string $originalName;        // Rapport de lecture (final).pdf

#[ORM\Column(length: 100)]
private string $mimeType;

#[ORM\Column]
private int $sizeInBytes;
```

The original name is kept for display and for the `Content-Disposition` header. It is
never what is written to disk.

**Deleting the entity does not delete the file.** Something has to, and in this
standard that something is the service:

- the service that removes the entity also removes the file, in that order — remove
  and `flush()` first, delete the file last. A file deleted before a `flush()` that
  then fails leaves a row pointing at nothing, which is worse than an orphan file;
- what the order leaves behind — a successful `flush()` followed by a failed delete —
  is swept by a scheduled command that compares stored keys against the database.

**A Doctrine lifecycle callback on the entity is not the answer here**, even though it
is the obvious one. This standard's entities are maker-format data holders with no
behaviour, precisely so that every rule is in a service where it can be unit-tested and
where reading the service tells you the whole flow. A `postRemove` hook fires from
`flush()`, far from the code that asked for the deletion, and cannot be tested without
a database. The scheduled sweep is the safety net, not the mechanism.

Concrete code for both, plus the orphan-sweep query: `references/storing-files.md`.
The command's own mechanics (dry-run by default, locking) belong to `symfony-yoandev-console`;
scheduling it belongs to `symfony-yoandev-async`.

## Validation that inspects the file rather than trusting the client

The extension and the `Content-Type` the browser sends are both attacker-controlled.
Measured on a PHP script renamed `invoice.pdf` and announced as `application/pdf`:

| Constraint | Result |
|---|---|
| `#[Assert\File(maxSize: '1M')]` | **accepted** |
| `#[Assert\File(extensions: ['pdf'])]` | rejected — `The mime type of the file is invalid ("text/x-php")` |
| `#[Assert\File(mimeTypes: ['application/pdf'])]` | rejected — same sniffed type |

`extensions:` is the option to reach for: it checks the extension *and* derives the
matching media types from `symfony/mime`, then verifies the sniffed type against them.
`UploadedFile::getMimeType()` re-reads the file with `finfo`;
`getClientMimeType()` returns what the browser claimed, and returned
`application/pdf` for that script.

**`#[Assert\Image]` accepts SVG by default.** Verified: an SVG containing
`<script>alert(1)</script>` passes `#[Assert\Image(maxWidth: 2000)]`, because `Image`
defaults `mimeTypes` to `image/*` when neither `mimeTypes` nor `extensions` is set, and
`image/svg+xml` matches that wildcard. Served inline from `public/`, that is stored XSS.
Write `#[Assert\Image(extensions: ['jpg', 'png', 'webp'])]` unless SVG is genuinely
wanted, and if it is, serve it as an attachment.

### PHP's own limits cut in before Symfony sees anything

Two different limits with two very different failure modes, both measured:

| Situation | What PHP does | What the user sees |
|---|---|---|
| Larger than `upload_max_filesize` | `$_FILES` entry present with `error = UPLOAD_ERR_INI_SIZE`, `$_POST` intact | A real validation message — `Assert\File` reports `uploadIniSizeErrorMessage` |
| Larger than `post_max_size` | **`$_POST` and `$_FILES` are both empty**, only `CONTENT_LENGTH` survives | A bare 422 with no message, or "the CSRF token is invalid" |

The second one is the bug report that reads "the upload does nothing". A non-nullable
`#[MapUploadedFile]` argument with no file resolves to `null`, and the resolver throws
`HttpException::fromStatusCode(422)` with an empty message — nothing in the response
says a limit was hit. Set `post_max_size` above `upload_max_filesize` above the largest
`maxSize` in the application, and detect the case explicitly when it matters:
`$request->headers->get('Content-Length') > 0 && !$request->request->count() && !$request->files->count()`.

## When something does not work

| Symptom | Cause |
|---|---|
| File 404s after a deploy | Written to a container filesystem. Object storage, not a local directory |
| Works on one request, 404s on the next | Several replicas, local disk on each |
| A private file is reachable without logging in | It is under `public/`. No amount of `access_control` will change that |
| The upload "does nothing", empty 422 or a CSRF error | Body over `post_max_size`; the request arrived empty |
| `The file is too large` but the file is small | `maxSize` is compared to a size PHP already truncated — check `upload_max_filesize` first |
| A `.php` or `.svg` file was accepted | `maxSize` alone, or `Assert\Image` without `extensions:` |
| Files accumulate in the bucket | Nothing deletes them on entity removal, and no sweep exists |
| A download returns the wrong `Content-Type` | `BinaryFileResponse` sniffs the *content*, not the stored MIME type — set the header |
| A protected download is cached by a proxy | `new BinaryFileResponse(...)` defaults to `public: true` |

## Out of scope

- **Receiving the upload** — `#[MapUploadedFile]`, files in a payload DTO, the
  version fallbacks: `symfony-yoandev-http`, `references/input-mapping.md`.
- **Image processing** — resizing, thumbnails, format conversion. Not covered by this
  suite; it needs a library (`intervention/image`, `liip/imagine-bundle`) and a
  decision about doing the work in a Messenger handler. Say so rather than improvising.
- **Voters** — how to write and test one: `symfony-yoandev-security`. This skill only says
  where to call it.
- **The sweep command itself** — dry-run/`--force`, locking, smoke test:
  `symfony-yoandev-console`. Scheduling it: `symfony-yoandev-async`.

## Version handling

Flysystem is not a Symfony component and follows its own versions; the facts here were
checked against `league/flysystem` 3.35 and `league/flysystem-bundle` 3.7, installed
next to Symfony 8.1. `#[IsSignatureValid]` needs Symfony 7.4 and
`Symfony\Component\HttpFoundation\UriSigner` needs 6.4 — the fallbacks are in
`references/serving-files.md`. Everything else here (`Assert\File`, `Assert\Image`,
`BinaryFileResponse`, `UploadedFile`) is available across 6.4 → 8.x.
**`vendor/` is the source of truth over this file.**

## Reference files

| File | When to read it |
|---|---|
| `references/storing-files.md` | Configuring Flysystem, naming the stored file, what the entity holds, deleting without orphans, testing an upload without touching real storage |
| `references/serving-files.md` | Getting the file back out: public URLs, a streaming controller, `X-Sendfile` / `X-Accel-Redirect`, signed URLs and S3 pre-signed URLs, cache headers |
