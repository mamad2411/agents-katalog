---
name: mouseketool
description: "Use FIRST, before you start writing a new reusable tool, app, service or library for the user, whenever they want one to exist that they have not built yet: a product idea, a wish (\"I want something that...\", \"a way to...\") or a requirements list. Searches GitHub for existing projects that already do it, checks them for real and gives a verdict - reuse, adapt, use as a base, or build from scratch. Do NOT use for a one-off script that performs an immediate action on the user's own files (\"write a script that renames the photos in this folder\" is an action, not a tool to research), nor when the user asks to change, fix or extend code that already exists in their project."
---

# mouseketool

Before building something new, find out whether it already exists. The tools `search_repositories`, `inspect_repository` and `read_repository_file` (MCP server `mouseketool`) gather facts and make no judgments. You judge. Your final answer starts with its verdict line (section 7), with nothing before it.

## 1. Gate

Run the method when the user wants a new reusable tool, app, service or library to exist (an idea, a wish, a requirements list), even when phrased as a wish: that is exactly when people build what already exists. Do it before writing any file. Stop silently (no mention of this skill, no questions, no search) when the request is a one-off script that performs an immediate action, or asks to change, fix or extend code already in their project. A request that points at the user's own files or folder to act on ("this folder", "these files", "my photos here") is an immediate action even when it says "write a script". When in doubt between those, do not trigger: noise on a small task is the failure to avoid.

## 2. Read the input

Split the idea into must-haves and nice-to-haves, and note the stated use (commercial, internal, open source) and stack constraints. Ask at most two questions, and only if the answer would change the verdict; otherwise state your assumption in one line and go on. Calibrate depth to the input: a vague one-liner gets a wide map of what exists in that space; a defined requirements document gets a requirement-by-requirement analysis.

## 3. Expand

Write 15 to 30 varied queries: synonyms, the names the community would use, category terms, `topic:` qualifiers, different angles on the same need. Not 30 rewordings of the user's sentence. GitHub matches whole words, so a project turns up only for the words it uses itself: write the forms a community would, such as an abbreviation and its spelled-out form (`dnd`, `d&d`, `dungeons dragons`), or the singular and the plural. A project a query misses is rarely further down its results; another wording finds it. GitHub matches every word of a query, so keep each to 2 to 4 keywords; long queries return nothing. Add `stars:>50` to at least half of them, so mature projects are not buried under one-person experiments.

## 4. Search and shortlist

Call `search_repositories` once with all queries. Call it a second time when the first gave nothing useful, only tiny projects (under 50 stars), or no candidate that covers every must-have: aim the new queries at the must-haves still uncovered, from a different angle, with `stars:>100` on most of them. A project that covers what the first search missed is often there under another name. Drop candidates that are archived, stale (last push over 18 months ago), or clearly off target. Judge "off target" by what the project does, not by whether its description repeats the user's words: a mature framework or library for the same domain is on target, because it can be the base. Keep a handful, and always keep the most-starred on-target candidates. When the idea has several parts (for example "convert images" and "generate from an idea"), keep the strongest candidate for each part. A project you already know, or found through a link in a README, is not checked yet: call `search_repositories` with its name before you inspect it. The search shows it still exists under that exact `owner/name`; a project no search returns is not a candidate.

## 5. Inspect

Call `inspect_repository` on 3 to 6 candidates (fewer only when fewer survive the shortlist), starting with the most adopted ones. Drop any with `health.archived` or `health.stale`, or whose license blocks the user's stated use. `licenseKind` `none` blocks all use. `copyleft` blocks closed-source use only when the license really does: LGPL and MPL do not block all of it, so drop only after checking what the specific license requires. For `other`, read the license (the `LICENSE` file via `read_repository_file`) and decide. Then read code with `read_repository_file`, at least one source file of each candidate the verdict names or rules out on a capability: confirm each capability the verdict relies on, and confirm each gap that rules a candidate out. `tree` lists only the top level; give a directory as `path` to list its entries and reach the source file you need. A listing is not a read: open at least one file of every candidate the verdict names, the base included. This applies to a `build` verdict too, since "nothing covers X" is also a claim. A README claim alone is not confirmation, and an answer that says the code was not read is not finished: read it first.

## 6. Judge

For each candidate: coverage per must-have, health (`maintenance`, recent activity, open issues), adoption (stars, contributors, releases), license fit, and the rough effort of adapting it versus building from scratch. Between candidates that cover the must-haves, prefer the one people actually use: a mature project beats a weeks-old repo with a handful of stars. Never recommend `reuse` or `adapt` for a candidate that misses a must-have. When a mature project would be the foundation the new tool sits on (an engine, framework, library or app that covers part of the idea), the verdict is `base` with that project, not `build`. The test is size: when the project already does at least one must-have end to end (for example it reads the live data and shows it in the terminal), it is a base, even if you would replace or extend part of it. Build and borrow a piece only when what you would reuse is smaller than a must-have, such as one parser or one function. Pick the base by maturity before closeness to the idea: the most adopted project that does a must-have end to end beats a young one with few stars or a single contributor, even one that looks more like the idea, because the base is what the new tool will depend on. Name a young, closer project as a reference in the answer, not as the base.

## 7. Answer

The first line of the answer is exactly one of these, nothing before it: no sentence about what you did ("I searched...", "Here is the result"), no heading, no blank line.

- `Verdict: reuse foo/bar` : use it as is.
- `Verdict: adapt foo/bar` : fork or modify it to fit.
- `Verdict: base foo/bar` : build on top of it as a foundation.
- `Verdict: build` : nothing fits, build from scratch.

Here `foo/bar` stands for the repository's real name. For `reuse`, `adapt` and `base`, list it after the word, comma-separated when there are several (`Verdict: adapt foo/bar, baz/qux`). Copy each name from the `name` field of a tool result, never from memory, a package name or a README: a project can live under another owner than its name suggests. The line holds nothing else: no other words or punctuation, and it stays in English even when the rest of the answer is in the user's language. Examples:

```
Verdict: reuse foo/bar
Verdict: adapt foo/bar
Verdict: base foo/bar, baz/qux
Verdict: build
```

Then at most three lines of summary: what you found and why that verdict. Then, per candidate, pros and cons against the user's goal, saying which claims you confirmed in the code. Stop there: do not design the new tool or ask about its design. The user decides what to build with the verdict.

If nothing fits, say so plainly: `Verdict: build`, and why. A forced candidate is a failure. Recommending a poor match to have something to show is worse than saying "build it". You may add "build it, and borrow this piece from owner/name" when that is true.
