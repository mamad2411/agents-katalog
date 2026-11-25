---
name: ui-part-uploads
description: "File uploads: the chooser and drop zone, accepted types and limits said up front, validation, progress per file with cancel and retry, previews, many files, direct uploads to storage, large and resumable uploads, and accessible markup. Read before building any file upload."
---

# File uploads

The generated upload is a large dashed box saying "Drag and drop files
here", with no button, no word on which files or how large, one spinner for
everything, and "Upload failed" for the whole batch when one file is too
big. This skill gives a chooser anyone can use, the rules said before
choosing, progress and recovery per file, and uploads that survive large
files and weak networks. The field's look is in `ui-part-forms`, its logic
in `frontend-forms`, the server's checks and storage in `backend-files`.

## 1. The chooser first, the drop zone second

- A real `input type="file"` behind a visible button ("Choose files",
  "Upload photo"): a `label` styled as a button with the input visually
  hidden but focusable, or a `button` that calls `input.click()`. It works
  with the keyboard, with screen readers and on every phone.
- A drop zone around it as an enhancement for pointer devices: never
  drop-only, never a focus stop of its own.
- `accept` lists what the chooser offers (`.pdf,image/png,image/jpeg`); it
  only filters the picker, so check again.
- `multiple` when several files make sense; `webkitdirectory` when people
  upload whole folders on desktop.
- Paste for images where people work with screenshots (chat, comments,
  editors): read `clipboardData.files` on `paste`.

```html
<div class="upload" data-dropzone>
  <input id="files" type="file" name="files" multiple class="sr-only"
         accept=".pdf,image/png,image/jpeg" aria-describedby="files-rules">
  <label for="files" class="button">Choose files</label>
  <span class="upload-or">or drop them here</span>
  <p id="files-rules">PDF, PNG or JPG, up to 10 MB each, 20 files at most.</p>
</div>
<ul class="upload-list" aria-label="Files"></ul>
<p class="sr-only" role="status" id="upload-status"></p>
```

The input is hidden, so its focus ring goes on the label
(`input:focus-visible + label`).

## 2. Anatomy and measures

- A page-level drop zone 120 to 200px tall with a 1 to 2px dashed border
  from the tokens, the button and the rules centred in it; in a form, a
  compact field 44 to 56px tall with the button and the rules on one line.
- The rules visible before choosing: types in words (PDF, PNG, JPG, not
  MIME types), the size limit per file and in total, the count, and image
  dimensions when they matter ("at least 400 by 400px").
- While files are dragged over it: the border solid in the accent, the text
  "Drop to upload". Where dropping anywhere uploads (chat, a file manager),
  a full-window overlay appears only while files are dragged
  (`event.dataTransfer.types.includes("Files")`).
- The file list below: one row per file, 48 to 64px, with a 40 to 48px
  thumbnail or type icon, the name truncated in the middle so the extension
  stays ("quarterly-rep...ort.pdf"), the size ("2.4 MB", in the same unit
  as the stated limit), a progress bar with its percentage, the status in
  words, and the actions.

## 3. States of a file

| State | The row shows | Actions |
|---|---|---|
| Waiting | "Waiting" | Remove |
| Uploading | The bar and "45%" | Cancel |
| Processing | "Processing" (scan, thumbnails, transcoding) | None, or Cancel if the server can stop |
| Done | A check and the size | Remove, or Replace for a single file |
| Refused | The reason in words | Remove, choose another |
| Failed | The reason and what to do | Retry, Remove |

- One file failing never fails the batch: the others finish, and the failed
  ones say why.
- A bar that reaches 100% while the server still works says "Processing",
  rather than sitting full with nothing happening.
- Many files: an overall line above the rows ("12 of 40 uploaded, 1
  failed"), and about 3 uploads at a time rather than 40 at once.

## 4. Validate early, and again on the server

- In the browser, for quick feedback: type (MIME type and extension), size
  (`file.size`), count, total size, empty files, and image dimensions (read
  with `createImageBitmap`).
- Messages per file, in plain words: "holiday.mov is 1.2 GB. The limit is
  500 MB." "report.docx is a Word file. Upload a PDF." Refused files are
  listed with their reason, never dropped silently.
- The server checks everything again: the type from the content rather
  than the name, its own size limit, a generated name, and a malware scan
  for files other people will download (`backend-files`).

## 5. Progress, cancel, retry

`fetch` reports no upload progress; `XMLHttpRequest` does, and upload
libraries use it:

```ts
export function put(file: File, url: string, onProgress: (pct: number) => void) {
  const xhr = new XMLHttpRequest();
  const done = new Promise<void>((resolve, reject) => {
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) onProgress(Math.round((e.loaded / e.total) * 100));
    };
    xhr.onload = () => (xhr.status < 300 ? resolve() : reject(new Error(`HTTP ${xhr.status}`)));
    xhr.onerror = () => reject(new Error("network"));
    xhr.onabort = () => reject(new DOMException("Cancelled", "AbortError"));
  });
  xhr.open("PUT", url); // a presigned URL from your server
  xhr.setRequestHeader("Content-Type", file.type); // must match what was signed
  xhr.send(file);
  return { done, cancel: () => xhr.abort() };
}
```

- Cancel stops the request and removes the row, or marks it "Cancelled"
  with Retry. Retry sends the file again, or resumes it (section 7).
- The rest of the form stays usable while files upload; submitting waits
  for them and says so ("Waiting for 2 uploads"); leaving the page while
  uploads run asks first (`beforeunload`).

## 6. Previews and cropping

- Images preview from `URL.createObjectURL(file)`, revoked with
  `URL.revokeObjectURL` when the row is removed or the component unmounts.
- iPhone photos may arrive as HEIC, which most browsers other than Safari
  cannot show: accept them, show a type icon, convert on the server.
- Documents show a type icon and the page count when known; videos show a
  first frame.
- Crop only when the result has a fixed shape (an avatar, a cover): a
  cropper with the ratio locked (react-easy-crop, Cropper.js), zoom and
  move by keyboard as well as by drag, a way to skip it, the original kept.
  Location data in photos is stripped on the server.

## 7. Direct to storage, large and resumable

Files go straight to object storage, not through your app server, which
times out on large files and pays for the bandwidth twice:

1. The browser asks your server for an upload, with the name, type and size.
2. The server checks the user, the type and the size, makes the storage key
   (never the user's file name), and returns a presigned URL (S3, R2, GCS,
   Supabase Storage) that expires in 5 to 15 minutes. Where the storage
   takes presigned POST policies (S3, GCS), a `content-length-range`
   condition enforces the size limit there too.
3. The browser uploads, with progress.
4. The browser tells your server it finished; the server checks the object
   (size, type from its first bytes), records it, and starts processing.

- The bucket's CORS allows PUT or POST from your origin only; files stay
  private and are served through signed URLs or your server.
- Above about 100 MB, or for people on phones: S3 multipart (parts of at
  least 5 MiB except the last, up to 10,000, each presigned and retried on
  its own) or the tus protocol (tus-js-client with tusd, or storage that
  speaks tus: Supabase Storage, Cloudflare Stream). tus-js-client can find
  an unfinished upload after a reload and resume it from where it stopped.
- Libraries: Uppy (dashboard, XHR, tus, S3 multipart, webcam, resuming),
  FilePond (a polished field with previews), react-dropzone (the drop and
  chooser logic only, with your markup), UploadThing (hosted, for Next.js).
  A single avatar field needs none of them.

## 8. Accessibility

- The chooser is a real control reachable by Tab, named by its label, with
  the rules tied to it by `aria-describedby`.
- Each row: the name as text, a `progress` element labelled with the file
  ("Uploading report.pdf"), the status in words, and buttons named with the
  file ("Cancel report.pdf", "Retry report.pdf", "Remove report.pdf").
- The polite status region announces the start, each finish or failure,
  and the end of a batch ("3 files uploaded, 1 failed"), never each percent.
- After a removal, focus goes to the next row's Remove, or to the chooser
  when the list is empty.

## 9. On a phone, themes, motion

- No dragging on phones: the button is the control, full width, and no
  "drop them here" text on touch screens (`(pointer: coarse)`).
- When a photo is the point (a receipt, a damaged parcel), "Take photo"
  with `capture="environment"` opens the camera, beside "Choose from
  library" without it; `capture` alone would take the library away.
- Rows stack the name and size above the bar; actions are 44px buttons.
- The drop highlight and the bar from tokens in both themes (`ui-themes`);
  the bar fills with `transform: scaleX()`, no looping stripes
  (`motion-interface`).

## Check it

- Keyboard only: Tab to the chooser, pick files, cancel one, retry one,
  remove one.
- DevTools throttling (Slow 4G), then Offline in the middle of an upload:
  progress moves, the failure sits on that file, Retry works.
- Files that must be refused: an empty file, one just over the limit, an
  executable renamed `.pdf` (the server refuses it), 50 files at once.
- An iPhone HEIC photo, a portrait photo, a file name with spaces, accents
  and emoji.
- A screen reader hears one message per file, not every percent.
- `preview` at 360px: a full-width button, no drop text, 44px targets.

## Avoid

A drop zone with no button; drag-and-drop text on phones; rules shown only
after a failure; one spinner for the whole batch; "Upload failed" with no
file and no reason; a failed file that sinks the batch; a bar stuck at 100%
while the server works; the user's file name as the storage key; trusting
`accept` or the extension; object URLs never revoked; large files through
the app server; `capture` forcing the camera on people who need their
library.
