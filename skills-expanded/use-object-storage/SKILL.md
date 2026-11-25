---
name: use-object-storage
description: >
  The media store — where uploaded images, video and icons actually live. Load it before adding an
  upload, before showing a picture the owner uploaded rather than one committed to the repository,
  when an image answers 401 or renders blank, and before writing image resizing of your own. Two
  facts decide almost everything and neither is visible from the code you can see: a stored file is
  referenced BY NAME, never by id, because ids differ on every server — and the picture reaches the
  visitor through this app's own route, never from the data host, which is why a secret is involved
  in showing a public image at all.
---

# use-object-storage

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The door and the credential are in `use-data`. This is about files.

---

## 1. 🔒 Reference a stored file BY NAME, not by id

In content and in code you write `media:<file-name>`; `lib/media/by-name.ts` resolves it.

**Why it cannot be the id.** The id is born at upload time and is different on every server. Content
lives in the repository and is the same everywhere — an id inside it points at nothing on the second
machine. The name is chosen by a person and stays.

Anything not starting with `media:` is treated as an ordinary path, so files committed under
`public/` keep working exactly as before.

The lookup is cached (an hour): a prerendered page must not walk to the data layer per reader, and the
store's contents change rarely.

## 2. 🔒 The picture reaches the visitor through THIS app

The path a browser actually takes is `/_next/image?url=/api/media/<id>/file` — the slot's own route,
which adds the secret server-side. The data host is never named in the browser.

Bought with a real defect (2026-08-13): the proxy read the key from a variable name that does not
exist on the server, so the key was empty and it forwarded **the visitor's cookie** instead. An
anonymous visitor has no session, so the image answered 401 and the optimiser above it answered 400 —
**no stored image had ever been visible to the public**, and nobody noticed because the pages showed
files from `public/`.

Two rules follow: the key is the answer, not the visitor's cookie; and a stored image must be checked
**as an anonymous visitor**, because signed in it works either way.

🔒 **The file committed under `public/` does not disappear — it changes role.** A picture referenced
as `media:` still ships in the repository as **seed material**: `npm run seed:media` uploads it to the
store on first run, and until that has happened the resolver falls back to the file. Without this a
fresh server would open the article on an empty database and show a hole.

**Two traps this already fell into.** A **link on a picture is not a source of the picture** — the
figure renderer branched on `href` first and drew the image itself, skipping `media:` resolution, so
the raw string reached the HTML; the defect was visible only on the one block where both conditions
met. And a **video's poster is not an image**: `<video poster="…">` takes neither the blurred
placeholder nor the optimiser, wherever the file lives. That is the element's nature, not a gap here —
say so plainly instead of promising a placeholder for every picture.

**Resizing needs no machinery of yours.** Media is served from the app's own origin, so the optimiser
treats it as local: no `remotePatterns`, no second image service, no resizing code of your own.

## 3. Uploading — multipart, so not through the JSON helper

`dataFetch` sets `Content-Type: application/json`, which destroys a multipart body: `FormData` must
set its own boundary. Follow the route already written here — `app/api/media/upload/route.ts`: a plain
`fetch` with **only** the `X-Data-Secret` header and the `FormData` as body.

The limit is 200 MB per file. Bigger than that is not an upload problem to solve with a retry — it is
a conversation with the owner about what the file is.

## 4. What the store already did for you

On upload it records `width`, `height`, `duration` for video, a **blur** placeholder as a `data:`
string, mime type and size. Read them from the row instead of measuring the file again: a catalogue
page with two dozen products would otherwise make two dozen extra round-trips, and a prerendered page
would become a chain of requests.

| Want | Route |
|---|---|
| the file itself | `GET /media/:id/file` |
| a small preview | `GET /media/:id/thumb` — 200×200, cover, JPEG, **images only** |
| shorten a video | `POST /media/:id/trim` — **video only**, refuses anything else |
| the project's icon set | `/media/icons`, `/media/icons/current`, `/media/generate-icons` |

Do not write resizing of your own: the thumb route exists, and `next/image` handles the rest.

## 5. Cutting and trimming are tools, not code you write

`_tools/image-cropper` (crop before upload) and the video trim tool already exist and are mirrored in
the panel — see `use-tools` before building a second one. The store keeps `crop_mode` so the intent
survives the upload.

## 6. Before you call it done

1. Content references the file by `media:<name>`, and the same content works on a second server.
2. The image was opened **anonymously**, in a private window — signed in proves nothing here.
3. Uploads go through the existing route; you did not force JSON onto a multipart body.
4. Dimensions and the blur come from the row, not from measuring the file on render.
