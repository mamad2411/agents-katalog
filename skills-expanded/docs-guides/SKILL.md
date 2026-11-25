---
name: docs-guides
description: "Tutorials and how-to guides: a tutorial that takes a beginner to a working result with every step succeeding, how-to guides that solve one task for someone who knows the basics, prerequisites stated, numbered steps with expected results, troubleshooting for the known failures, tested code, current screenshots, and the right length. Read before writing a tutorial, a getting-started page or a how-to guide."
---

# Tutorials and how-to guides that work

The generated guide opens with "In this tutorial, we will learn how to",
assumes three tools nobody installed, says "simply run" without showing
what should happen, offers a choice of three databases at step 2, shows a
screenshot of last year's interface, and ends by summarising what the
reader just did. On a clean machine it fails at step 4. This skill: the
tutorial that succeeds every time, the how-to that finishes one task, and
troubleshooting drawn from real failures. Choosing the kind of page, and
the accuracy rules, are in `docs`.

## 1. Tutorial or how-to

| | Tutorial | How-to guide |
|---|---|---|
| Reader | A beginner, learning | Someone with a task, who knows the basics |
| Promise | You will build a working X | You will have done Y |
| Path | One, with every choice made for them | Conditions allowed: "If you deploy with Docker, ..." |
| Explanation | The least that keeps them going, linked | None beyond what a step needs |
| Title | "Build a ..." or "Get started with ..." | The task: "Rotate an API key" |
| Ends with | A working result, and what to learn next | The task done, and related tasks |

A getting-started page is a tutorial: from nothing to the first success.

## 2. Tutorial rules

- Choose a small result that shows what the product is for: an endpoint
  returning real data, a deployed page, a working form. Not a toy that
  could belong to any product.
- One path. The tool, database, options and names are chosen for the
  reader; alternatives are mentioned at the end, never inside the steps.
- Every step produces a result the reader can see and check: "Refresh the
  page: the list shows two tasks." A step with nothing to see merges with
  the next one.
- Explain only what the next step needs, in a sentence, and link the
  explanation page.
- It works on a clean machine with only the stated prerequisites,
  followed in order. Test it that way before publishing and after each
  release.
- Start from nothing: create the project, show each file whole the first
  time, then only the changed lines with enough context to find them (or
  the whole file again when it is short).
- Checkpoints: at the end of each part, the full state of the files, or a
  tag in a companion repository (`part-2-done`) to compare against.
- 10 to 20 steps. Longer becomes parts, each ending in something that
  runs.
- End with two to four links: the next tutorial, the how-to guides for the
  usual next tasks, the concepts page. Not a recap of what they just did.

## 3. How-to rules

- The title is the task, in the reader's words, as they would search for
  it: "Rotate an API key", "Deploy with Docker Compose", "Import users from
  a CSV file" (or "How to rotate an API key", if the site's titles use that
  form).
- The first lines say what this achieves and when you need it, in one or
  two sentences; then the prerequisites.
- Prerequisites: versions, access (the role or permission needed), what
  must already exist, each with a link.
- Numbered steps, one action each, the command in a code block, the
  expected result after it.
- Variations as separate sections, or as conditions at the step they
  change. A variation that changes most of the steps is its own guide.
- Link the reference for options instead of listing them.
- A destructive or irreversible step has its warning before its command,
  never after: what it destroys, how to back up first, whether it can be
  undone.
- End with how to confirm it worked, then related tasks.

## 4. A how-to, whole

An illustration; every fact in a real guide comes from the product.

````markdown
# Rotate an API key

Replace a key without downtime by running the old and the new key side by
side. Do this when a key may have leaked, or on your rotation schedule.

## Before you start

- The **Admin** or **Developer** role.
- The `acme` CLI 2.4 or later: check with `acme --version`.

## Steps

1. Create the new key:

   ```sh
   acme keys create --name billing-worker-2026-09
   ```

   The key is printed once. Store it in your secret manager now.

2. Deploy the new key to every service that uses the old one.

3. Confirm that nothing still uses the old key: its **Last used** time
   stops changing.

   ```sh
   acme keys show key_8Jd2Qw
   ```

4. Revoke the old key. This cannot be undone: requests that still send it
   fail with `401`.

   ```sh
   acme keys revoke key_8Jd2Qw
   ```

## Check that it worked

Your services respond normally, and `acme keys list` shows the old key as
**Revoked**.

## Troubleshooting

### `401 invalid_api_key` after the deploy

A service still sends the old key, often a worker that was not restarted.
Restart it, then check the key's **Last used** time again.

## Related

- [API keys reference](../reference/api-keys.md)
- [Restrict a key to IP addresses](./restrict-key-ips.md)
````

## 5. Steps that work

- One action per step, and the action first: "Run", "Open **Settings**,
  then **API keys**", "Add this line to `config.toml`".
- Commands in code blocks without prompts; output in a separate block
  marked `text`, trimmed with `...`.
- Where it runs, when that matters: which directory, which machine, which
  shell.
- The expected result after each step: the output, what appears on the
  screen, the file that now exists.
- Interface steps: labels in bold, exactly as the screen shows them, with
  `>` between menu levels: **Settings > Billing > Invoices**.
- Where platforms differ, show each one, in tabs where the site has them:

```sh
export ACME_TOKEN=<your-token>        # macOS and Linux
```

```powershell
$env:ACME_TOKEN = "<your-token>"      # Windows PowerShell
```

- Placeholders in angle brackets, explained under the block: "Replace
  `<project-id>` with the id under **Settings > General**." Never a real
  key or a real customer's data.
- A file's path above its block (or as the block's title where the site
  supports it), and the whole file the first time.
- A step that takes a while says what shows it is done ("the status turns
  **Live**"); a duration only if you measured it.

## 6. Troubleshooting

- From real failures: issues, support tickets, chat questions, and what
  went wrong when you tested the guide. Never imagined ones.
- Each entry: the symptom as the reader sees it, with the exact error text
  as the heading so search finds it; then the cause; then the fix.

```markdown
### `Error: listen EADDRINUSE: address already in use :::3000`

Another process holds port 3000, often a dev server from an earlier run.
Stop it, or start this one on another port: `PORT=3001 npm run dev`.
```

- At the end of the guide, or on a troubleshooting page linked from the
  step where the failure happens.
- The usual families to look for: the wrong version of a tool, a missing
  environment variable, a port in use, file or cloud permissions, a proxy
  or firewall, a stale cache or lockfile.

## 7. Screenshots, video and time

- A screenshot when the reader must find something visual, not to repeat
  text the step already gives.
- Crop to the region that matters plus enough to locate it; 2x
  resolution; one highlight at most (a box or an arrow); no browser
  chrome; a demo account, never real personal data; the same window size
  and theme throughout.
- Alt text says what the image shows for this step.
- Retake them with every interface change. Where the interface changes
  often, capture them in CI (Playwright's `page.screenshot` with a
  `clip`), or use fewer.
- A video sits beside the written steps, never in place of them: it cannot
  be searched, copied or skimmed.
- "This takes 15 minutes" only when measured with real readers; otherwise
  leave time out.

## 8. Keeping guides working

- Follow the guide on a clean environment (a fresh container, a new
  account) before publishing and after each release. Better still, a CI
  job runs its commands, and its code lives in files CI builds, included
  into the page rather than pasted (`docs-sites`).
- Pin the versions a guide depends on in its install commands, and update
  them on purpose.
- Stamp it: "Tested with acme 2.4 on 2026-09-29."
- Every support question a guide should have answered becomes an edit to
  it.
- As short as the task allows. A how-to that runs past two screens is
  usually two tasks, or one task and an explanation that belongs on its
  own page.

## Check it

- Follow the guide literally, from step 1, in a clean environment.
  Without `bash`, trace each step to the code, script or screen it depends
  on, and list in your report the steps that were not run.
- Every tool the steps call is in the prerequisites: search the steps for
  command names and tick each one off.
- Each step has one action and a result to check; each placeholder is
  explained; each block has a language and no prompt.
- Every link resolves; screenshots match the current interface, or are
  listed in your report as needing a retake.
- No "simply" or "just", no recap at the end, no time estimate nobody
  measured.

## Avoid

"In this tutorial, we will"; choices inside a tutorial; steps with no
visible result; prerequisites discovered at step 5; commands with prompts
that break when pasted; "simply run"; troubleshooting for failures nobody
has had; screenshots of an old interface or of real customer data; a
closing summary of what the reader just did; a guide nobody has followed
on a clean machine.
