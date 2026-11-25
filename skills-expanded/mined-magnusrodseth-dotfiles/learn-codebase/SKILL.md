---
name: learn-codebase
description: "Understand a codebase by reading its actual source, on GitHub or on disk: how a pattern is really implemented, an org's conventions, how two things are wired. Use for \"how does <repo> do X\". For published API docs prefer find-docs."
---

# Learn a Codebase

A **targeted search for one contextual answer** inside a repo's real source — not an
onboarding. The job is to find the **needle in the haystack**: how to do X in framework
Y, how to share state across X and Y, how self-service security is wired inside
Gjensidige — whatever the surrounding task needs. Read only enough to trust the find.

`find-docs` covers a named library's *published* docs (Context7). Use **this** for the
*source itself*: internal patterns, org conventions, cross-repo how-X-is-really-done,
and private repos with no docs.

## The spine

### 1. Pin the question

State the one question the search must answer, in a sentence — the **north-star
question**. If the surrounding task already implies it, use that. If you were handed a
bare URL with no goal, ask one sharp question first; do not start a generic survey.

This question is your completion criterion: you are done when you can answer **it** with
citations, never when you "understand the repo."

### 2. Locate the code — check local first

Cheapest source wins. In order:

1. **Working tree / open session sources** — already in front of you? Use it.
2. **Already on disk.** Org and work repos usually live at `~/dev/<owner>/<repo>` (e.g.
   `~/dev/gjensidige/<repo>`). Search, then confirm identity (a same-named dir is not the
   same repo):
   ```bash
   fd -t d -d 2 "^<repo>$" ~/dev
   git -C <hit> remote get-url origin   # must match <owner>/<repo>
   ```
3. **Learn cache** at `~/.learn-codebase/<owner>/<repo>`. If present, **freshen before
   trusting it** — fast-forward to the remote default branch; if offline, use it but flag
   staleness in your answer:
   ```bash
   git -C <dir> fetch --quiet --depth 1 origin && git -C <dir> reset --hard FETCH_HEAD
   ```
4. **Absent everywhere → shallow-clone into the cache.** `gh` is authed over SSH for
   public and org repos alike:
   ```bash
   gh repo clone <owner>/<repo> ~/.learn-codebase/<owner>/<repo> -- --depth 1
   ```

The cache lives in `$HOME`, outside every git repo, so it never clutters dotfiles or the
current project. Never clone into the working project or the dotfiles tree.

### 3. Hunt the needle

Do not read the repo into your own context. For anything past a single precise `rg`, fan
out a **read-only subagent** (`Explore`, or `general-purpose` for big sweeps): hand it the
pinned question verbatim plus the repo path, and have it report back **file:line locations
and the surrounding pattern**, not file dumps. Keep the main context clean.

Orient only as much as you need to navigate to the needle — entry points, directory shape,
build/run, naming conventions *around* the target. Skip the rest of the repo.

**What to look for is contextual.** For the menu keyed by intent (use a library's API,
replicate a pattern across X↔Y, org infra / self-service / security, debug an integration,
evaluate a dependency, match house style), read `WHAT-TO-LOOK-FOR.md` — it maps each intent
to where the answer usually hides and the signal that confirms it.

### 4. Verify it's idiomatic

A single hit can be a one-off or a dead legacy path. Confirm it's **the way this repo does
it**: used in more than one place, the current (not deprecated) approach, consistent with
the repo's house style. Done = you can answer the question with concrete `file:line`
citations and a copyable pattern you trust is idiomatic.

### 5. Answer inline

Give the focused answer to the pinned question: the pattern, `file:line` citations, and a
minimal example adapted to our task. No notes file by default — if the user later wants it
kept, hand off to the `vault` skill.
