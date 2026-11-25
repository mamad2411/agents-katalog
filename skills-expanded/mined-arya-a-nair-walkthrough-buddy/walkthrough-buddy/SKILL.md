---
name: walkthrough-buddy
description: Turns any pull request, branch, commit, folder, feature or whole repository into one onboarding page a newcomer reads once and then ships a change from - diagrams of what calls what, an ELI5 analogy for every idea, real code excerpts pinned to a commit and machine-checked, file:line links, run and test commands that were actually run, a recipe for the most common change, and a starter task. Has an ADHD mode with short timed parts, progress tracking and one next step. Use whenever someone needs to understand unfamiliar code well enough to change it - "walk me through this PR", "explain this codebase", "onboard me to src/billing", "ELI5 how the retry queue works", "I'm new to this repo", "how does X work end to end", new-hire onboarding, handover notes, or orienting a reviewer - even if they never say "walkthrough".
---

# Walkthrough Buddy

Turn a piece of code into one page a newcomer can read top to bottom and then ship a change. Diagrams show the shape, ELI5 analogies make each idea stick, and real excerpts, pinned to a commit and checked by a script, make sure every claim holds.

**The bar:** after reading, the reader can answer "where would I change X, how do I run it, and which test proves it works" without opening another tab.

## Inputs

- **Target:** PR number or URL, `A..B` range, commit, branch, path, or a concept ("how billing retries work"). If it's missing, ask once.
- **Reader:** default is a competent engineer who is new to this repo. If the user names someone else (non-engineer, designer, new grad), adjust vocabulary and depth, not structure.
- **Mode:** standard (default) or **ADHD mode**. Use ADHD mode when the user asks for it ("ADHD mode", "I have ADHD", "easier to read", "I lose focus on long docs") or when the `i-have-adhd` skill is active in this session. If you turned it on by default, say so in the delivery line and offer a standard page. ADHD mode reshapes the page and covers the same content: read `references/adhd-mode.md` before writing.
- **Format:** self-contained HTML (default). Use Markdown when the user wants it committed or posted as a PR comment, since GitHub renders Mermaid.

Stay read-only on the repo. The only file you write is the output, and it goes outside version control (see Deliver).

## Workflow

1. **Gather.** Run `bash <skill-dir>/scripts/gather.sh <target>` from inside the repo. It resolves the target, then prints the base/head commits, commits, diffstat, PR body, review comments, nearby docs, build/test entry points and nearby tests. Read every doc it lists that sits on the path to the target (README, CONTRIBUTING, AGENTS.md, CONTEXT.md, ...).

2. **Understand before you write.** Read whole files, not just hunks: unchanged code explains what the changed code means. Trace the one main path from where it starts (user action, request, CLI call, cron) to where it ends (response, write, side effect). Find the tests that pin that path and one real input: a fixture, a test case, or a sample request. Keep a scratch fact sheet where every claim carries `path:line`, with the line number taken from `grep -n` or `sed -n 'Np'`, never estimated. Anything you could not confirm is marked *(inferred)* on the page. If gather.sh says the checkout is not at the target, read with `git show <sha>:<path>`.

3. **Verify what you will tell the reader to run.** Each setup, run and test command must come from the repo (manifest scripts, Makefile, CI workflow, docs). If a command is safe and finishes in a couple of minutes (unit tests, typecheck, a single test file), run it in a throwaway worktree, `git worktree add --detach <tmp-dir> <head-sha>`, so installs, caches and build output never touch the user's checkout. Record the result, then run `git worktree remove <tmp-dir>`. Otherwise label it *not run here*. Never present an invented command as fact.

4. **Plan.** Write the answer sentence: what this does for a person, in 20 words or fewer. Pick the 5–9 concepts a contributor must hold, and put them in reading order: the order a person would follow the code, not the folder order. Scale with the target:

   | Target | Diagrams | Code stops | Read time |
   |---|---|---|---|
   | Change under 150 changed lines | 2–3 | 3–5 | 5–8 min |
   | Change of 150+ lines, or a feature | 4–6 | 6–10 | 10–20 min |
   | Folder / service | 4–6 | 6–10 | 15–20 min |
   | Whole repo | 5–7 | 8–12 | 20–30 min |

   These are targets, not caps. If going one over teaches the main path, go over. If going under covers it, stop.

5. **Write.** Copy `assets/template.html` and replace everything between `<!-- BODY START -->` and `<!-- BODY END -->`, or write Markdown. Fill the sections in `references/sections.md`, in that order, and in ADHD mode apply `references/adhd-mode.md` on top of them. That file is the contract: section ids, what each one holds, Mermaid rules, the excerpt markup, and the writing rules. Read it before writing.

   Make every code excerpt with `python3 <skill-dir>/scripts/excerpt.py <path> <A-B[,C-D]> --sha <head> --tag new|changed|context` (add `--base <base>` for a diff, `--old` for pre-change code, `--md` for Markdown). It copies from git, escapes the code and adds a pinned permalink. Hand-copied excerpts are where walkthroughs go wrong.

6. **Check.** Run `python3 <skill-dir>/scripts/check.py <output> --repo <repo> --stamp`. It verifies that every excerpt matches the pinned commit, every `path:line` citation exists, required sections are present, no `{{placeholders}}` remain, and every diagram renders in a headless Chromium-family browser. Fix what it flags and re-run until it exits 0. On a pass, `--stamp` writes its own numbers into the page's trust box, so the reader sees what was verified rather than your claim about it. On exit 3 (could not render), say diagrams are unverified. Never call it verified.

7. **Cold-read test** (for anything bigger than a small PR). If your harness can start a fresh subagent, give it only the output file and ask it to answer the page's "Check yourself" questions and outline the starter task, without opening the repo. Every question it gets wrong or hedges on points to a gap in the page. Fix the page, not the answer key. If you cannot start a subagent, reread the page cold as the named reader and do the same.

8. **Deliver.** Write to `<repo>/.walkthroughs/<slug>.html` and add `.walkthroughs/` to `.git/info/exclude`, which stays local and leaves `.gitignore` untouched. Use another location if the user names one. Open it (`open` on macOS, `xdg-open` on Linux, `start` on Windows) when a desktop is available. If your harness can publish or share pages, offer that. Do not publish private code without asking. Reply with the path, the answer sentence, and the check result, in three lines.

## Common mistakes

| Mistake | Fix |
|---|---|
| Changelog order ("file 1 changed, file 2 changed") | Reading order along the main path |
| Diagram of the folder tree | Diagram of what calls what, or what flows where |
| One giant diagram | One idea per diagram, 12 nodes or fewer, caption says what to notice |
| Analogy replaces the code | Each concept follows the same order: what it does → ELI5 → real excerpt → why it's built this way |
| Excerpts retyped from memory | Copy from `git show <sha>:<path>` with real line numbers; the checker enforces this |
| "Run `npm test`" with no proof | The command comes from the repo, and you ran it or labelled it |
| Ends at "how it works" | Ends at "how you change it": recipe, test, gotchas, starter task |
| Page sounds like it covered everything | The trust box lists what was not read or not run, and "Read these yourself" points at the exact lines the excerpts left out |
| Review becomes the topic | Not a code review. Raise risks as "watch out" notes, and say who raised them |
