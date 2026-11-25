---
name: bug-submit
description: Submit a bug report as a local entry under bugs/ in the current repo, optionally with image attachments saved alongside the report. Use when the user wants to file a bug, log a defect they've just encountered, or report something broken. Accepts the bug description from $ARGUMENTS (or prompts in chat when missing or thin), accepts images already pasted into the conversation (via `[Image: source: <path>]`) as well as paths passed in arguments, allocates the next bug number by scanning both bugs/ and bugs/archive/, creates a bugs/bug-N-<description>/ folder, copies the images into it, and writes a bug-N-<description>.md report whose triage section is grounded in a quick read of the relevant code paths. Then regenerates a repo-wide bugs/bugs-tracker.html — an HTML Issues view listing all open (bugs/) and closed (bugs/archive/) bugs, each expandable to its full report and screenshots. Step 0 confirms with the user in chat before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /bug-submit.
user-invocable: true
disable-model-invocation: false
argument-hint: <bug description (optionally with image paths), or omit to be asked>
allowed-tools: Read, Write, Grep, Glob, Skill, Bash(git *), Bash(ls *), Bash(find *), Bash(date *), Bash(pwd), Bash(test *), Bash(mkdir *), Bash(cp *), Bash(basename *)
---

# bug-submit — File a triaged bug report under bugs/

You are running the `bug-submit` skill. The user may have arrived here by typing `/bug-submit` (with an optional description and/or image paths in `$ARGUMENTS`) or because the model proactively invoked the skill. Your job is to record a clean bug report as a local folder under `bugs/` in the current repo and write a markdown report whose triage section captures your initial understanding of the problem — grounded in a quick read of the relevant code.

This skill writes only to the local filesystem; it does **not** create GitHub issues, push, commit, or upload anything to a remote.

This skill has ten steps (Steps 0–9). Execute them in order. Do not skip Step 0 (proactive-invocation confirmation), Step 2 (bugs root), Step 3 (clarification), Step 4 (folder allocation), Step 7 (write the report), or Step 8 (update the tracker).

## Step 0 — Confirm before proceeding (when invoked proactively)

This skill creates files inside the user's repo — proactive invocation without a clear opt-in is higher cost than for read-only skills. The Step 0 check is strictly enforced.

Check the most recent user message in the conversation for the literal tag `<command-name>/bug-submit</command-name>` (or, equivalently, a leading `/bug-submit` typed by the user). If present, the user has explicitly opted in — skip this step and continue with Step 1.

Otherwise (you arrived here because the model decided to invoke this skill proactively from natural-language intent), output exactly one chat message and stop your turn:

> About to run `/bug-submit` to file a bug report for **<one-line restatement of the bug>**. This will create a `bugs/bug-N-<description>/` folder in the current repo with a markdown report and any attached images. Reply **yes** to proceed, or anything else to cancel.

When the user replies in their next turn:

- If the reply is an unambiguous affirmative (e.g. `yes`, `y`, `go`, `ok`, `do it`), continue with Step 1.
- Anything else — including silence, a redirect, "no", or a new instruction — counts as cancellation. Stop immediately. Do not create any folder, file, or copy any images.

Do not call `AskUserQuestion` here or anywhere else in this skill — all clarification happens via plain chat prompts, because images attached to `AskUserQuestion` answers are not surfaced with a filesystem path and would be silently dropped.

## Step 1 — Parse arguments and detect images

Parse `$ARGUMENTS` into two buckets:

- **Bug description text** — everything that isn't a path token.
- **Image path tokens** — anything that looks like a file path ending in `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, or `.bmp` (case-insensitive). Validate each exists with `test -f`; drop tokens that don't resolve to a real file (note the misses but don't error yet).

Also scan the **recent conversation messages** for image paths Claude Code surfaced via the `[Image: source: <path>]` annotation — that's the only mechanism by which a pasted/dragged-in screenshot becomes a referenceable filesystem path. Add each unique path to the candidate list and validate with `test -f`.

Note: an image attached via an `AskUserQuestion` answer is **not** surfaced with a path — only the literal answer text is. If you see something like `(Image attached)` in an answer with no `[Image: source: ...]` line, treat it as no image and ask the user in Step 3 to paste the image directly into chat.

You now have:

- `description_text` — may be empty or trivially short.
- `image_paths` — may be empty.

Do not ask anything yet — Step 3 handles the clarification in one shot.

## Step 2 — Locate the bugs root

Determine where `bugs/` lives:

- `git rev-parse --show-toplevel` — if it succeeds, record the result as `repo_root`. All bug paths are anchored at `<repo_root>/bugs/`.
- If it fails (not inside a git work tree), stop and tell the user to `cd` into the target repo first. Do not fall back to an arbitrary cwd — the bug tracker needs a stable, canonical location so numbering stays consistent.

You do **not** need `gh`, network access, or any authentication for this skill.

## Step 3 — Clarify the bug

**This step is mandatory even in auto / non-interactive mode.** If the user or the harness has told you to "work without stopping" or "skip clarifying questions", that instruction does not apply here — a vague bug report wastes everyone's time downstream. Close material ambiguity before filing.

Decide whether you need to ask anything. You need to ask if **either** of the following is true:

- `description_text` is empty or under ~10 meaningful words.
- `image_paths` is empty *and* the description suggests visual context would help (UI bugs, layout issues, error dialogs, "looks wrong", "broken on screen", etc.).

If you don't need to ask, skip straight to Step 4.

Otherwise, output exactly one chat message and stop your turn. Keep it to a single ask — do not run a multi-round Q&A. Use this template, adapting only the lead line to acknowledge what (if anything) was already supplied:

> To file this clearly I need a bit more. Please reply with:
>
> 1. **A short description of the bug** — what happened, what you expected, and (if you can) how to reproduce it.
> 2. **Any screenshots** — paste them directly into your next message. (Attaching via the question/answer UI is **not** sufficient — the path won't reach the skill.)
>
> Reply with both in one message; I'll take whatever you give me and file from there.

When the user replies in their next turn:

- Treat the reply text as the new `description_text` (concatenated with any prior `description_text` you already had).
- Re-scan that reply for `[Image: source: <path>]` annotations and add the paths to `image_paths`. Validate with `test -f`.
- If any quoted path string the user typed by hand fails `test -f`, surface that single miss in chat once (with the path), then continue — do not loop on it.

If after this round `description_text` is still essentially empty (the user declined to elaborate or replied with something like "nevermind"), stop the skill cleanly with no folder created.

## Step 4 — Allocate the bug number and create the folder

Compute the next bug number by scanning **both** the active and archived bug folders, so a number is never reused after a bug is resolved and moved to `archive/`:

```bash
find "<repo_root>/bugs" "<repo_root>/bugs/archive" -maxdepth 1 -type d -name 'bug-*' 2>/dev/null
```

Each match is a folder named `bug-<N>-<slug>`. Extract the integer `<N>` from each (the digits between the first `bug-` and the next `-`). Take the **numeric** maximum across all matches (so `bug-10` outranks `bug-9`) and add 1. If there are no matches (or `bugs/` doesn't exist yet), start at `1`. Use integer numbers only — `bug-1`, `bug-2`, `bug-10`; never `bug-1.0` or `bug-1a`.

Record the result as `bug_number`.

Build the slug from the bug description:

- Lowercase, words separated by single hyphens, ASCII letters/digits only (drop punctuation).
- **At most 10 words.** Lead with the symptom so the folder name is scannable (e.g. `login-button-does-nothing-on-safari`).
- Avoid generic slugs like `bug` or `issue`.

Record the result as `slug`. The folder and report file share the same stem:

- `bug_folder` = `<repo_root>/bugs/bug-<bug_number>-<slug>/`
- `report_file` = `<bug_folder>/bug-<bug_number>-<slug>.md`

Create the folder (parents included):

```bash
mkdir -p "<bug_folder>"
```

## Step 5 — Save images into the bug folder

Skip this step entirely if `image_paths` is empty.

If any image filename or path looks like it may contain sensitive content (e.g. paths under `secrets/`, `.env`-adjacent dirs, or filenames suggesting credentials), output exactly one chat message and stop your turn:

> One or more attachments look potentially sensitive (`<list filenames>`). They'll be copied into your repo under `bugs/` and could be committed later. Reply **proceed** to copy them in anyway, or **skip** to file the bug text-only.

If the next user reply is `skip` (or anything other than an unambiguous `proceed`), set `image_paths` to empty and continue without images. If `proceed`, carry on with the copy.

Copy each image into `bug_folder`, preserving its base filename:

```bash
cp "<image_path>" "<bug_folder>/<basename>"
```

Collision handling: if two images share a base filename, or a base filename would collide with the report `.md`, append `-2`, `-3`, … before the extension. Build `saved_images` as the list of base filenames actually written into the folder (these are what the report links to, as relative paths).

The images live next to the markdown, so the report references them relatively (`![name](name.png)`) — never absolute paths and never remote URLs.

## Step 6 — Triage the bug

Spend a focused effort understanding the bug before writing the report — but **cap the investigation** so this step doesn't sprawl into a full debug session:

1. Skim the repo structure (`ls` of project root, plus any obvious entry-point folders such as `src/`, `app/`, `lib/`).
2. Grep for keywords from the bug description (component names, error messages, function names, route paths, visible UI strings). Limit to ~3 focused searches.
3. Read **at most 2 files** that look most directly relevant. Stop once you have enough to form an initial hypothesis — you are not fixing the bug, only triaging it.

Form a working understanding covering, in order:

- **Summary of understanding** — one or two sentences restating the problem in your own words. This is the most important part: a developer should be able to read just this line and know what they're picking up.
- **Probable affected area** — file paths, modules, or components most likely involved. State confidence honestly (e.g. "likely", "possibly", "uncertain"). If you read specific files, reference them as `path/to/file.ext:line` where applicable.
- **Severity (rough estimate)** — `low` / `medium` / `high` / `critical`, with a short justification anchored to user-visible impact (data loss, blocking, degraded experience, cosmetic).
- **Initial hypothesis** — your best guess at the root cause area, if anything stands out. If nothing does, say so plainly — do not invent.
- **Missing information that would help reproduce** — anything the report doesn't cover that a developer would need. Omit the section entirely if everything needed is already in the report.
- **Suggested next steps** — 1–3 concrete actions (e.g. "confirm repro on latest main", "check `path/to/file.ext` for null handling around line N", "add server logs around `<function>`").

## Step 7 — Write the bug report

Build the report title: a short, scannable summary derived from the bug description. Aim for 6–12 words, lead with the symptom (e.g. `Login button does nothing on Safari 17`). Avoid generic titles like `Bug` or `Issue`.

Write `report_file` with the `Write` tool using this template verbatim, sections in the order shown. If a section has nothing to say, write the italic placeholder; do not omit the heading.

```markdown
# Bug <bug_number>: <title>

- **Severity:** <level> — <one-line justification>
- **Filed:** <YYYY-MM-DD>

## Description
<the user's bug description, lightly cleaned up — preserve their wording where it's specific; do not invent details>

## Expected behaviour
<one or two lines if known; otherwise: `_Not specified._`>

## Steps to reproduce
<numbered list if known; otherwise: `_Not specified._`>

## Screenshots
<for each entry in saved_images: `![<filename>](<filename>)` on its own line. If saved_images is empty, write: `_None provided._`>

## Triage

**Summary of understanding:** <…>

**Probable affected area:** <…>

**Initial hypothesis:** <… or "Nothing obvious from a quick read of the repo.">

**Missing information that would help reproduce:**
- <… — omit this whole sub-section if nothing is missing>

**Suggested next steps:**
- <…>

---
Filed via `/bug-submit` on <YYYY-MM-DD>. To resolve, move this folder into `bugs/archive/`.
```

Compute `<YYYY-MM-DD>` from `date -u +%Y-%m-%d`. Keep the report focused — the triage is a useful starting point for whoever picks the bug up, not a full investigation.

## Step 8 — Update the bug tracker

Invoke the `bug-tracker-render` skill in this plugin via the `Skill` tool (no arguments). It (re)generates `bugs/bugs-tracker.html` from the plugin template + the current filesystem — the bug you just wrote appears under **Open**. If it returns a `skipped — …` status (e.g. the template wasn't found), surface that one-line note and continue to Step 9; the bug folder you just wrote is the durable record regardless.

Do **not** inline the tracker rendering — `bug-tracker-render` is the single source of that logic for every skill in this plugin (the same reason `feature-resolve` and `lessons-capture` are factored out). Adding the render steps back here would re-introduce the drift the extraction exists to prevent.

## Step 9 — Present highlights

In chat, output a short, scannable summary so the user has the pointers they need without re-reading the whole conversation:

```
Bug filed: bugs/bug-<bug_number>-<slug>/bug-<bug_number>-<slug>.md
Tracker:   bugs/bugs-tracker.html  (open the Issues tab)

**Title:** <title>

**Triage**
- Probable area: <…>
- Severity: <level>
- Hypothesis: <one line>

**Attachments:** <count> image(s) saved in the bug folder
```

Keep the chat output under ~20 lines. The bug folder, its report, and the tracker are the artefacts; the chat is the pointer.

## Constraints (non-negotiable)

- **No bug folder created without a substantive description.** If Step 3 fails to elicit one, stop with no filesystem state created.
- **Mandatory clarification step.** Step 3 runs even when the harness instructs autonomous operation. Closing material ambiguity is the whole point. The clarification is a single plain-chat prompt — never `AskUserQuestion`, because images attached to its answers are not surfaced with a filesystem path.
- **Bug numbers are allocated across `bugs/` AND `bugs/archive/`.** Always scan both so a number is never reused after a resolved bug is archived. Integer numbers only, numeric compare (`bug-10` > `bug-9`).
- **Everything stays local.** This skill writes only under `<repo_root>/bugs/` (bug folders plus `bugs/bugs-tracker.html`). It never creates GitHub issues, never pushes, never commits, and never uploads images to a gist or any remote. Images are copied into the bug folder and referenced by relative path.
- **The tracker is a generated artefact, rendered by `bug-tracker-render`.** Step 8 delegates to that internal skill — never inline the rendering here. `bugs/bugs-tracker.html` is rebuilt wholesale from the plugin template + the filesystem on every run; never hand-maintain it or treat hand edits as durable. Open vs. closed is derived purely from folder location (`bugs/` vs. `bugs/archive/`), so moving a bug folder is the single source of truth for its status — the tracker catches up on the next render. If the template can't be found, `bug-tracker-render` skips rather than failing the skill.
- **Never write secrets to disk.** If the description or anything pulled from the conversation looks like it contains a credential (API keys, tokens, passwords, private connection strings), redact it in the report — irrecoverably — and warn the user once before writing. For image attachments that look sensitive, get explicit `proceed` confirmation (Step 5) before copying them into the repo, since they may later be committed.
- **Triage is grounded, not invented.** Step 6 must read real files in the repo before hypothesising. If nothing in the codebase looks relevant after a short search, say so in the report — do not fabricate a hypothesis.
- **Severity is best-effort.** Never claim certainty about severity from a bug report alone; the report is a starting point, not a verdict.
- **One bug per invocation.** Do not split a report into multiple bug folders automatically — if the description covers two separate bugs, note it in the Triage section and let the user split them deliberately.
- **No symlinks.** Copy image files into the bug folder; never symlink them.
- **Language-agnostic.** Do not bake in tooling specific to one ecosystem when reading the repo for triage. Adapt to whatever stack the repo is on.
