# fsbrowse/

[fsbrowse.ts](../fsbrowse.ts) is the stable facade: it re-exports `listDir`,
`createDir`, and the `DirEntry`, `DirRoot`, and `DirListing` types.

| Module | Responsibility |
| --- | --- |
| [types.ts](./types.ts) | Listing, entry, and root shapes. |
| [roots.ts](./roots.ts) | `rootEntry` canonicalizes root paths and labels; `listRoots` discovers roots. |
| [validation.ts](./validation.ts) | `validateNewFolderName` trims and validates one folder-name segment. |
| [listing.ts](./listing.ts) | `listDir` validates the target and assembles its directory listing. |
| [create.ts](./create.ts) | `createDir` validates the parent/name and containment, creates, then lists the new folder. |

Read-only integration references: [routes/health/browse.ts](../routes/health/browse.ts)
is the HTTP adapter for `GET /api/list-dir` and `POST /api/create-dir`;
it returns failures as HTTP 400 `{ error: message }`. The frontend [folderPicker consumer](../../../frontend/src/components/folderPicker/useFolderPickerState.ts)
owns navigation and creation UI state ([local guide](../../../frontend/src/components/folderPicker/CLAUDE.md)).

## Listing and roots

- `listDir` trims its target, defaulting to `os.homedir()` when omitted or blank.
  It canonicalizes the path and requires `fs.stat` to report a directory.
- The result is `{ path, parent, roots, entries }`: `path` is canonical;
  `parent` is `path.dirname(path)`, or `null` when that equals `path`.
  Roots and entries are `{ name, path }`; entry paths are joined to the canonical directory.
- Visible directories mean `Dirent.isDirectory()` and no leading `.` in the name;
  entries are sorted by `name.localeCompare`. Reading entries and roots runs concurrently.
- Roots have canonical paths. Windows probes A-Z in order, skipping failed stats/non-directories,
  falling back to the home or cwd root if none are found; labels are the first two path characters.
  POSIX returns one home/cwd/`path.sep` root (in that order), labeled by its canonical path.

## Path and creation contracts

- Before canonicalization or filesystem actions, both operations use
  `isRealAbsoluteProjectPath` to reject relative and drive-relative inputs, plus
  Windows root-relative inputs such as `\tmp` and `/c/Users`; `path.isAbsolute` alone is insufficient.
  Canonical identity details live in [projectPath.ts](../projectPath.ts) and [projectIdentity/CLAUDE.md](../projectIdentity/CLAUDE.md).
- `createDir` requires a nonblank parent, canonicalizes it, and stats it as a directory
  before validating the name. Names are trimmed, then reject empty, `.`, `..`, either
  path separator, a basename mismatch, or NUL. Windows also rejects `< > : " | ? *`,
  control characters, and a trailing space/period in the trimmed name.
- Windows device names are case-insensitive and reserved even with extensions:
  `CON`, `PRN`, `AUX`, `NUL`, `CONIN$`, `CONOUT$`, `COM1`-`COM9`, `LPT1`-`LPT9`,
  and superscript ports `COM¹`-`COM³`/`LPT¹`-`LPT³`; `COM10`/`LPT10` remain allowed.
- Containment uses `path.relative(base, canonicalTarget)`: empty, `..`, a leading
  `..` plus separator, or an absolute relative path is rejected; `..cache` is allowed.
- `fs.mkdir(target)` is non-recursive, followed by `listDir(target)`; validation,
  stat, mkdir (including existing targets), and listing failures propagate to callers.

Existing behavior contract: [fsbrowse.test.ts](../__tests__/fsbrowse.test.ts).
