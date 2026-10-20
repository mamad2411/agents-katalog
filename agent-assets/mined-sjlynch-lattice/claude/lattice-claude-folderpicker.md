# frontend/src/components/folderPicker

Folder-picker internals used by the project chooser.

- No fetch lives in this folder: `useFolderPickerState.ts` imports `listDir`
  (`/api/list-dir`), `createDir` (`/api/create-dir`) and `initProjectGit`
  (`/api/project-init`) from the API layer (`api/scan.ts`,
  `api/projectInit.ts`).
- `loadDirectory.ts` makes no request either: it is the latest-navigation-wins
  guard around an *injected* `listDir` — a monotonic `seqRef` stamp so a slower,
  stale listing never lands after a newer navigation (and only the latest
  clears `loading`).
- `useFolderPickerState.ts` owns navigation state, loading, root switching,
  create-folder flow, and selection callbacks, and shapes the create/init errors
  itself (create bumps the same `seqRef` to invalidate in-flight loads; a git
  failure becomes `Git setup failed: <message>` plus the backend's `detail`
  stderr when present). Create runs `createDir` →
  (when the "Initialize a git repo" checkbox is on, default) `initProjectGit` on
  the new path, and reports the outcome through `notice`. A folder that was just
  created is empty by definition, so this is the zero-risk half of the Git Setup
  contract — no preview, no dialog. A git failure sets `error` but keeps the
  `notice`, since the folder itself was created either way.
- Presentational pieces (`DriveSelector`, `PathRow`, `DirectoryList`,
  `CreateFolderRow`) should stay dumb and callback-driven.
- Use `rootKey.ts` when deriving stable React keys for filesystem roots; drive
  letters and POSIX roots need normalization.
- Do not assume Windows-only paths despite Lattice's primary dev environment.
