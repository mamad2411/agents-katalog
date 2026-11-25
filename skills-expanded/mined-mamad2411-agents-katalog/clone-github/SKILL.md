---
name: clone-github
description: Clone a GitHub (or any git) repository into the sandbox so you can explore its real files, instead of guessing or relying only on web search. Use whenever the user gives a repo URL or asks you to look at / analyze / explain a GitHub project.
---

# Clone a GitHub repo, then explore it

When the user points you at a repository (a GitHub URL, "owner/repo", or "look at
project X"), DO NOT try to answer from memory or from web snippets. Bring the
real code into the sandbox and read it.

## Procedure

1. **Clone it.** Use the `clone_repo` tool with the repository URL (preferred — it
   does a shallow clone into this conversation's sandbox and returns the top-level
   file tree). It accepts `https://github.com/owner/repo`, `owner/repo`, or any
   git URL.

   If you only have `run_code`, clone with bash instead:
   ```bash
   git clone --depth 1 https://github.com/owner/repo repo && ls -la repo
   ```

2. **Explore with the `explore-codebase` skill.** Once cloned, switch into the
   repo dir and use tree-structured search (ripgrep/grep), never sequential reads:
   ```bash
   cd repo
   sed -n '1,60p' README* 2>/dev/null                       # what is this project?
   find . -path ./.git -prune -o -type f -print | head -200  # the file tree
   git grep -n "the thing you care about"                    # find it (or: grep -rn)
   ```

3. **Answer from what you actually read**, citing concrete files and line numbers
   (e.g. `src/index.ts:42`). If something isn't in the repo, say so.

## Rules

- Always shallow-clone (`--depth 1`) unless history is genuinely needed — it's far
  faster and smaller.
- The sandbox is per-conversation and auto-deletes; re-clone if you return later.
- For a specific branch: `clone_repo` with the URL, or `git clone --depth 1 -b <branch> <url>`.
- After cloning, immediately fall back to the **explore-codebase** workflow — the
  point of cloning is efficient local search, not reading everything.
