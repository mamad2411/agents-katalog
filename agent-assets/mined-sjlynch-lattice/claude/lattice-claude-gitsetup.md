# frontend/src/components/gitSetup

- [GitSetupProvider.tsx](./GitSetupProvider.tsx) owns the `ensureGitRepo` promise
  gate shared by task create, run and navbar callers. Concurrent calls with the
  same project-path string share one in-flight promise, removed on settlement.
  A superseding dialog resolves the prior awaiter `false`; `settle` clears the
  resolver before invoking it, making settlement idempotent. Keep the API
  context memoized and the success nonce separate: `useGitSetupNonce()` refreshes
  git observers (including the navbar probe and branch subscription) without
  changing the API value for every consumer.
- Each provider request gets a fresh `key={request.id}` so
  [GitSetupDialog.tsx](./GitSetupDialog.tsx) remounts and resets preview/draft
  state. Only `initable` + `none`, or `initable` + unborn `repo`, reaches
  `InitDialog`; nested and other blocked states get explanation-only UI.
  A committed repo passes the gate immediately. An absent old-server `git`
  probe also deliberately passes, leaving failures to the pre-existing backend
  error path instead of opening an unpopulatable dialog.
- [useInitPreview.ts](./useInitPreview.ts) sends the initial preview without a
  draft; `.gitignore` stays `null` until that response loads its text. Only user
  edits enable the 400 ms re-preview debounce. Each started request advances
  `previewSeq`; stale responses cannot update preview, error or loading flags.
  Cleanup clears the pending timer, not an in-flight request: there is no
  request abort or unmount fence, and typing alone does not advance the sequence.
  The hook's `error`/`setError` is shared with the init action.
- Init submits the current shown draft via
  `initProjectGit(project, gitignore ?? undefined)`; preserve deliberate empty
  strings. Re-preview does not gate submission, so counts may still be refreshing.
  `busy` blocks dismissal and repeat submission during mutation; success calls
  `onDone(true)` to settle/unmount. For missing-identity `HttpError` 422s, preserve
  raw git stderr from `detail` (currently trimmed, falling back to `message`)
  in the dedicated help block: it carries git's fix commands. Mutation guards,
  unborn-repo recovery and the prohibition on probing/setting git identity belong
  to [backend projectInit guidance](../../../../backend/src/projectInit/CLAUDE.md).
- Keep chip states, blocker copy and formatting in
  [gitSetupDerive.ts](./gitSetupDerive.ts). Existing
  [gitSetupDerive.test.ts](../../__tests__/gitSetupDerive.test.ts) covers chip
  fallbacks/unborn/nested states, blocker copy, path basenames, byte/count
  formatting (including truncated lower bounds), and the large-entry threshold.
  This is pure-helper coverage, not coverage of the asynchronous dialog lifecycle.

Ownership outside this directory: [api/pushRuns.ts](../../api/pushRuns.ts) owns
`checkGit`; [api/projectInit.ts](../../api/projectInit.ts) owns preview/init POSTs;
[api/types/git.ts](../../api/types/git.ts) owns their wire types and
[api/http.ts](../../api/http.ts) preserves `HttpError.detail`.
[styles/git-setup.css](../../styles/git-setup.css) owns dialog/picker styles
(imported after `modal.css` in `frontend/src/index.css`); navbar chip styles stay
in [styles/appbar.css](../../styles/appbar.css). The newly created empty-folder
path in [folderPicker/useFolderPickerState.ts](../folderPicker/useFolderPickerState.ts)
intentionally calls init directly, bypassing this dialog and preview.

Command references only, all with `frontend/` as cwd: `npm run build` (build),
`npm test` (tests), `npx tsc -b` (type-check). These are not task execution
instructions; task agents leave verification to the separate Run tests step.
