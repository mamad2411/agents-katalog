---
name: second-look-code-review
description: Turn the current branch or PR into an interactive review guide, with changes grouped into feature chapters, ranked by risk, checked against an AI-code checklist, opened as a browser view. On later runs, shows only what changed since the last review. Use when the user asks to review a PR, review a branch, review changes before merging, re-review, or runs /second-look-code-review. Also use when the user pastes a block starting with <!-- second-look-comments -->.
---

# Second Look Code Review

You produce a **review guide** for a set of changes, and a bundled script renders it as an interactive page. You never write the UI yourself: you write `guide.json`, the script does the rest. Keep it that way, so the view looks the same every run and costs no tokens to draw.

Files in this skill (paths are relative to the folder containing this SKILL.md):
- `schema.json`: the exact shape of `guide.json`
- `checklist.md`: the checks to run on risky chapters
- `scripts/render.mjs`: renders the guide (Node 18+, no dependencies)

## 0. First review or re-review?

If `.second-look/last-review.json` exists, this is a **re-review**. Run:

```bash
node <this-skill-folder>/scripts/render.mjs --status --previous .second-look/last-review.json --base <base>
```

It prints JSON: every changed file marked `updated` (reviewed before, changed since, with the exact `git diff` command for just those changes), `new` (never reviewed), or `unchanged` (reviewed, same content). If nothing is `updated` or `new`, tell the user nothing changed since their last review and stop, unless they ask for the full view. Otherwise follow **Re-review** below instead of steps 1-5.

## 1. Find the changes

- Base branch: use the one the user names. Otherwise try `gh pr view --json baseRefName -q .baseRefName`, then `git symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`), then `main`, then `master`.
- Intent: try `gh pr view --json title,body,url`. If there's no PR, use `git log --format='%s%n%b' <base>..HEAD` and any issue the user mentions.
- Files: the view covers everything on the branch since it left the base, **including uncommitted and untracked files**. Get the list with `git diff --numstat $(git merge-base <base> HEAD)` plus `git ls-files --others --exclude-standard`, and read each with `git diff $(git merge-base <base> HEAD) -- <path>` (or the file itself if untracked). For files over ~400 changed lines, read the risky regions and skim the rest.
- To review only uncommitted work, pass `--working-tree` to the render script and use `git diff HEAD`. To review a specific ref instead of the working tree, pass `--head <ref>`.

## 2. State the intent

Write one sentence: what this PR is supposed to do, in behavior terms ("Users can attach Word templates in chat and the workflow fills them"), not file terms. If the description and the diff disagree, or you can't tell what the PR is for, set `intent_clear: false` and say what's unclear in `intent_note`. That is the first thing the reviewer sees, and often the most useful.

## 3. Group files into chapters

This is the part that makes the view worth opening. Rules:

- **Group by behavior, not by folder.** A chapter is one thing the PR does: "Resolve chat uploads", "Fill uploaded templates", "Rename run → job". Files from five folders can belong to one chapter.
- **Tests go in the chapter of the code they test**, after that code.
- **Every changed file appears in exactly one chapter.** The renderer will flag any file you miss or repeat.
- Usually 2-8 chapters. One chapter for a tiny PR is fine.
- Lockfiles, generated code, snapshots, pure renames and formatting go in one final chapter titled "Mechanical changes", risk `low`.
- Order files within a chapter so a reader can follow them: entry point first, then what it calls, then tests.
- **Order chapters for reading**: what the rest depends on first (schemas, types, shared helpers), then features, then mechanical changes. Don't sort by risk; the view shows risk badges and lets the reader jump.

Chapter titles: 2-5 words, verb first where it reads naturally, sentence case.

Chapter summary: 1-3 short sentences on what changes in behavior and how it works. Link the specific code you mention with markdown links to a file path, optionally with a line: `[copies those files into the run workspace](packages/backend/workflows/launch.ts#L42)`. Line numbers are on the new side of the diff. These links are how the reader jumps into the code, so link the two or three places that matter, not every noun.

### Tour, checks and test steps

For every chapter except "Mechanical changes", also write:

- **`tour`**: 2-6 stops that walk the reader through the chapter in the order they'd explain it to a colleague. Start where the behavior begins (the entry point), follow the call into the code that matters, and end on the tricky part. Each stop is a `file`, a `line` (new side, an added or context line in the diff), an optional `end_line` to highlight a short range (keep it under ~15 lines), and a `note`: one or two sentences saying what this code does and what to notice. Say *why it matters*, not what the syntax says. Bad: "This function takes a userId." Good: "Ownership is only checked here, so every caller has to go through this function."
- **`checks`**: 1-3 questions a sharp reviewer would ask about this chapter, specific to this code. "What happens if the upload is still processing when the run starts?", not "Is error handling correct?"
- **`test`**: how to try the chapter by hand, in one or two sentences, with the command or steps. `inline code` is fine. Omit it if there's genuinely nothing to try.

The view turns the tour into a step-by-step walkthrough (press `t`), so a good tour is the fastest way for someone to understand the chapter.

## 4. Rate risk

Per chapter, `high`, `medium` or `low`, plus one short `risk_reason`.

- **high**: data migrations or schema changes, auth/permissions, anything trusting user input, money, deletes, concurrency, retries/timeouts, LLM calls in a loop, prompt or model changes, public API changes.
- **medium**: new behavior with tests, changed control flow, config defaults, error handling.
- **low**: tests only, renames, copy, types, logging, mechanical changes.

When unsure between two levels, pick the higher one.

## 5. Run the checklist

Read `checklist.md`. Apply every check to `high` and `medium` chapters; skim `low` ones for anything obvious.

Report a finding only when you can point at a line and explain the actual problem in this code. No "consider adding tests" or style opinions. A review with three real findings is far better than one with fifteen guesses.

Each finding needs: the file, the line on the **new** side of the diff (it must be an added or context line in the diff, or the renderer will pin it to the top of the file), a severity, the check id from `checklist.md` (or `other`), a message, and a concrete suggestion when there is one.

Severity:
- `blocker`: will break, corrupt data, leak, or cost real money in production.
- `warn`: likely bug or a real risk worth fixing before merge.
- `nit`: small, optional. Use sparingly.

## 6. Write and render

Write the guide to `.second-look/guide.json` in the repo root, matching `schema.json`. Then run:

```bash
node <this-skill-folder>/scripts/render.mjs --guide .second-look/guide.json --base <base> --open
```

Add `--previous .second-look/last-review.json` on a re-review. The script reads the real diff from git, checks the guide against it, writes `.second-look/review.html` and opens it. If it prints warnings (missing files, findings on lines not in the diff), fix `guide.json` and run it again. Suggest adding `.second-look/` to `.gitignore` the first time.

## 7. Reply

Keep it short: the intent sentence, how many chapters, and the blockers if any, one line each. The view has everything else. Don't repeat the guide in chat.

## Re-review

The goal is to show the reviewer only what changed since they last looked, and to spend tokens only on that.

1. **Reuse `.second-look/guide.json`.** Keep the intent, chapter ids, titles and order.
2. **Read only what changed.** For `updated` files, run the `diff_since_review` command from the status output. For `new` files, read the full diff. Don't re-read `unchanged` files.
3. **Place new files** in the chapter they belong to, or a new chapter. Drop files that are no longer in the diff.
4. **Update summaries** only for chapters with `updated` or `new` files: keep the summary and add one sentence starting "Since your review:" describing what changed. Rewrite those chapters' `tour` to walk through what changed (line numbers have moved), and update `checks` and `test` if they no longer apply.
5. **Findings:** keep findings on `unchanged` files as they are. Remove findings on `updated` files, and run the checklist again on their since-review diff and on `new` files. Line numbers are the file's current line numbers.
6. Render with `--previous .second-look/last-review.json`. The view hides unchanged files you already reviewed, shows updated files as "since your review" diffs (with a toggle to the full PR diff), and shows earlier comments with how you resolved them.
7. Reply in two or three lines: how many files changed since the last review, and any earlier comment marked `question` that needs the reviewer's answer.

## Addressing review comments

The view's **Export for AI** button copies a block that starts with `<!-- second-look-comments -->`: the reviewer's comments, then a `<!-- second-look-state … -->` block recording which version of each file they reviewed. When the user pastes it:

1. **Save the state first, before changing any code.** Copy the JSON between `<!-- second-look-state` and `-->` exactly into `.second-look/last-review.json`, replacing any earlier one. It records the versions the reviewer saw, so it must be saved as is.
2. Treat each comment as a review request on its file and line. Lines are the file's line numbers at the time of the review (`side: "old"` means a deleted line).
3. Fix each one, or explain why not if a fix would be wrong.
4. **Record what you did** by adding a `resolution` to each comment in `.second-look/last-review.json`:
   ```json
   "resolution": { "status": "fixed", "note": "Removed fileIds; ownership now checked in listReadyFiles (launch.ts:9)" }
   ```
   `status` is `fixed`, `wont_fix`, or `question` (you need the reviewer's answer). Keep `note` to one line. Don't change anything else in the file.
5. Finish with a list: comment → what you changed (file:line), or why you didn't. Then offer to run the re-review.

Don't commit unless the user asks; the re-review includes uncommitted changes. Don't make changes nobody asked for while you're in there.
