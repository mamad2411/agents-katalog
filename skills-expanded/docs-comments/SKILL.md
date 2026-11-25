---
name: docs-comments
description: "Comments, doc comments, commit messages and pull request descriptions: comments that explain why, invariants and surprising decisions rather than narrating code, doc comments on public interfaces, TODOs with an owner and a ticket, keeping comments true when code changes, commit subjects and bodies that explain intent, and PR descriptions that let a reviewer review. Read before writing comments, commit messages or pull request descriptions."
---

# Comments, commits and pull requests that explain intent

The generated version comments every line with what it does
(`// increment the counter`), puts a banner over each section, keeps
commented-out code "just in case", writes `TODO: fix this` with no owner,
documents `@param id the id`, and leaves comments describing code that
changed two versions ago. Its commits say "fix", "update" or "address
review comments", and its pull request description is the template with
empty headings. This skill covers the text around code: what only a
comment can say, how to keep it true, and the commit messages and pull
requests a reviewer can work from. The short rules are in `code` (section
8); this goes further.

## 1. What a comment is for

The code says what and how. A comment says what the code cannot:

- **Why this way**: the requirement, constraint or trade-off. "Sorted by
  id as well as time: two rows can share a timestamp, and the cursor must
  be stable."
- **Invariants and preconditions** the types do not enforce: "`items` is
  never empty here: `validate` rejected that."
- **Units and ranges** when the type does not carry them: "timeout in
  milliseconds", "0 to 1, not a percentage".
- **Surprising decisions**: "Not awaited on purpose: the receipt email must
  not hold up checkout; failures go to the retry queue."
- **Workarounds**, with what they work around and when they can go: the
  upstream issue's link and the version or condition that ends them.
- **References**: the spec section, RFC, ticket or decision record
  (`// See docs/adr/0007-use-postgresql-for-the-job-queue.md`).
- **Concurrency**: which lock guards what, what may run in parallel, what
  order is assumed.
- **Performance or security reasons**, with what was measured or the
  threat guarded against. A number only if someone measured it.

```ts
// Bad: repeats the code
// Loop over the users and send each one a reminder
for (const user of users) await sendReminder(user);

// Good: says why it is sequential
// One at a time: the provider allows 10 requests a second and has no
// batch endpoint.
for (const user of users) await sendReminder(user);
```

Before writing a comment, try a better name or a smaller function. A
comment explaining what a block does is often a function name waiting to
be extracted.

## 2. What not to write

- Narration ("Step 1: validate the input"), names restated
  (`// get the user` above `getUser()`), section banners, end-of-block
  markers (`} // end if`).
- History: "changed by Ana in March", "old version below". Git keeps it,
  with the reason in the commit.
- Commented-out code: delete it, git has it. If it must stay, the comment
  says why and links the issue that will decide.
- Jokes, apologies, emoji, capitals for emphasis.
- Comments that contradict the code: fix whichever one is wrong.
- Boilerplate docblocks on private helpers that say nothing the signature
  does not.

## 3. Doc comments

- Every public item of a library, and every exported function at a module
  boundary, gets one: a first sentence that summarises, then what the
  signature does not say (meaning, units, errors, panics, an example). The
  syntax per language, and the tests that run the examples, are in
  `docs-api`.
- A private helper gets one only when its name and signature are not
  enough.
- Never restate types (`@param {string} name the name`); give what the
  type cannot: format, limits, what `null` means.

## 4. Markers and suppressions

- A TODO names an owner or an issue, and the condition that ends it. A
  TODO with neither becomes an issue, or is deleted.

```ts
// TODO(#1234): drop the v1 fallback once no client sends X-Api-Version: 1.
```

- FIXME marks known wrong behaviour that ships, with its issue. Use the
  markers the project already uses; do not bring new ones.
- Rust: a `// SAFETY:` comment above every `unsafe` block says why its
  invariants hold (clippy's `undocumented_unsafe_blocks` checks for it).
- Every lint or type-check suppression carries its reason, in the form the
  tool reads:

```ts
// eslint-disable-next-line no-await-in-loop -- the provider has no batch endpoint
// @ts-expect-error: the published types omit the two-argument overload (fixed in 3.2)
```

```rust
#[expect(clippy::too_many_arguments, reason = "mirrors the C API one to one")]
```

- Prefer `@ts-expect-error` to `@ts-ignore`, and `#[expect]` to
  `#[allow]`: both complain when the problem they silence goes away, so
  the suppression cannot outlive its reason.

## 5. Keeping comments true

- When you change code, read the comments around it and update or delete
  them in the same change. A false comment costs more than a missing one,
  because it is believed.
- Do not copy a value into a comment ("retries 3 times"); name the
  constant (`MAX_RETRIES`), so the comment cannot drift from it.
- In review, a comment that no longer matches its code is a bug.
- Licence headers only when the project requires them, in its form, for
  example `// SPDX-License-Identifier: Apache-2.0`. Never add or change one
  on your own.
- Match the density and tone of the neighbouring files.

## 6. Commit messages

- First, the project's convention: its recent history, `CONTRIBUTING.md`,
  a commitlint config (`commitlint.config.*`, `.commitlintrc*`), a commit
  template.
- **Subject**: the imperative mood, what applying the commit does ("Add",
  "Fix", "Remove", "Rename"); about 50 characters, 72 at most; no full
  stop; capitalised unless the convention is lowercase (Conventional
  Commits descriptions usually are).
- **Body**, after a blank line, wrapped at 72: why the change was needed,
  what it changes at a level above the diff, trade-offs, what it does not
  do, and how it was checked when that is not obvious. Not how it works,
  which the diff shows, unless the approach is surprising.
- **Trailers** at the end: `Fixes #123` or `Closes #123` (the issue closes
  when the commit reaches the default branch), `Refs: #123`,
  `Co-authored-by: Name <email>`, `Signed-off-by:` where the project asks
  for a DCO sign-off (`git commit -s`), `BREAKING CHANGE:` under
  Conventional Commits.
- One logical change per commit: a refactor and a behaviour change are two
  commits; formatting on its own is a third.
- Conventional Commits when the project uses them:
  `feat(api): add cursor pagination to GET /orders`,
  `fix(cli)!: exit non-zero when a table is skipped`.
- With squash merging, the pull request title becomes the subject and its
  description often the body: write both to these rules.
- Never a secret, a customer's data or a private hostname in a message:
  history is hard to rewrite and is often public.

```text
Retry webhook deliveries on 429 and 503

Partners throttle bursts after their own deploys, and we dropped those
deliveries after one attempt. Retry up to 5 times with exponential
backoff (1, 2, 4, 8, 16 seconds), and wait for Retry-After when it is
longer.

Deliveries that still fail go to the dead-letter table, as before.

Fixes #482
```

Subjects that say nothing: "fix bug", "update", "changes", "WIP", "misc",
"address review comments", "final fix".

## 7. Pull request descriptions

- **Title**: like a commit subject, and specific: "Add cursor pagination to
  GET /orders".
- **What and why**: the problem and the change in two to five sentences,
  with the issue linked.
- **How to review**: where to start, what deserves attention, what is
  mechanical (renames, generated files, a regenerated spec).
- **Testing**: the commands you ran and their results, the manual checks,
  and what was not tested. A plain "Not tested: the Windows path" beats a
  ticked box.
- **Screenshots or a short recording** for interface changes, before and
  after, at the widths that changed.
- **Risk and rollout**: migrations and their order, feature flags,
  compatibility, upgrade notes for anything breaking, how to roll back,
  what to watch after the deploy.
- **Follow-ups**: what was left out on purpose, with issues.
- Use the project's template (`.github/pull_request_template.md`): fill it
  in, and delete the sections that do not apply rather than writing "N/A"
  under each. A checklist only when the template has one.
- Small pull requests get real reviews. Split a large change into a
  sequence: the refactor first, the behaviour change second.

```markdown
## What and why

`GET /orders` returned every order, and large accounts timed out (#471).
It now pages with `limit` (default 25, maximum 100) and `cursor`.

## How to review

Start with `orders/list.ts`. `openapi.yaml` is regenerated.

## Testing

- `pnpm test orders`: passing, with 6 new cases for cursors.
- Paged through the staging account with the most orders: no gaps, no
  repeats.
- Not tested: the admin CSV export, which uses the old helper (#475).

## Rollout

Breaking for clients that expect the whole list in one response. The web
app is updated here; the mobile app ships its change first (#476).
```

## Check it

- Each comment you wrote says something the code cannot. For each one,
  ask whether the next engineer would lose anything if it were deleted.
- No commented-out code, no TODO without an owner or issue and an end
  condition, no stale comment beside the lines you changed, no
  suppression without a reason.
- The commit subject is imperative and under 72 characters, the body is
  wrapped at 72, and the trailers are right.
- The pull request's testing section lists real commands and results, and
  claims nothing that was not run.

## Avoid

Comments that narrate the next line; banners and end-of-block markers;
commented-out code; TODOs without an owner; `@param id the id`; comments
left false after a change; suppressions without a reason; "fix", "update"
and "WIP" as commit subjects; bodies that retell the diff; a pull request
description that is an empty template; test claims nobody ran.
