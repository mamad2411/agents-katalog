---
name: blueprint-from-collection-import
description: "Build the import that moves the copied records into Firestore and their files into Cloud Storage, and prove it on the emulators."
---

# Move the records in (emulators)

Read `.blueprint/source/source.json` first. If `records` is `false`, only the shape was copied: there is nothing to
move. Add a `yarn import-source` script that says so and exits 0, and stop.

Otherwise the records are in `.blueprint/source/collections/<slug>/records.jsonl` (one JSON object per line), and the
files they point at are under `.blueprint/source/files/`, at the path the record names.

1. Add `yarn import-source --target emulator|prod`, using the Admin SDK (`firebase-admin`, a dev dependency — it
   never ships to the client). `emulator`: the project id `demo-blueprint`; the emulator hosts come from the
   environment `firebase emulators:exec` sets, so no key is needed. `prod`: the production project from
   `.firebaserc`, with the person's Application Default Credentials. Never read a service account key file.
2. Names follow the spec and the pack's `spec/conversion.md` (Firestore): the collection is the slug; the document id
   is the primary key's value; a stored field keeps its key. A boolean stays a boolean, a number a number, a date its
   ISO text, a `ref` the referenced id as text.
3. A record's `image` / `file` value is a path: upload `.blueprint/source/files/<path>` to the default bucket at the
   same path, and keep the path in the field. If any file is uploaded, add the Storage emulator and `storage.rules`
   (deny by default; open only what the spec says), and write the bucket's name to `.blueprint/storage-bucket`.
4. Running it twice leaves the same documents (`set` by id, never `add`).
5. A record that does not fit is not dropped silently: the script stops and names the collection, the record's id and
   the field.
6. The rules are not loosened for the import: the Admin SDK does not go through them.

Done when the check passes: inside the emulators, run twice, every collection has as many documents as it had records,
every stored field reads back equal, and every pointed-at file is in the bucket named in `.blueprint/storage-bucket`.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never enable billing, deploy to production, delete data or handle a credential unless this step's gates say the
  user approved exactly that.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
