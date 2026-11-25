---
name: feature-walkthrough
description: Writes a walkthrough of a feature branch for a reader who did not build it. It follows the real code path end to end with file:line stops verified at one commit, draws the structure with ASCII trees and validated Mermaid diagrams (plain-visual-docs), uses the feature's domain terms, and stays short. The writing can go to a read-only subagent when the environment has one; the citations and diagrams are checked before delivery. Use it whenever the user asks for a walkthrough, a code tour, "explain the feature", "how does what we built work", "show me the code of the branch", an onboarding explanation of a branch or pull request, or wants to understand a feature before a review or a merge.
---

# Feature walkthrough

A walkthrough answers one question: "if I follow one run of this feature (a request, a command, a job), what runs, in which order, and why?" It is not a spec summary and not a PR description. It follows the code.

## 1. Fix the target

Collect these before you delegate. They go into the brief.

- **Commit**: the exact hash under review. The writer reads files at that commit, so every citation stays valid.
- **Diff range**: the commits of the feature only. If the branch contains a merge of other work, name the merge commit and exclude it, or the tour drifts into unrelated code.
- **Spec and decisions**: `docs/<slug>-spec.md` and the ADRs the feature added. If the spec has a "Domain language" section (`domain-language`), the walkthrough uses only those terms.
- **Reader and language**: the user's language, or the document language for a pull request (`simplified-technical-language`).

## 2. Write it, or delegate it

The writing reads many files. When the environment has subagents, brief one read-only subagent with the template below, so the main context stays small. Name the convention skills in the brief. A subagent does not load them by itself, and without `plain-visual-docs` the walkthrough comes back without diagrams. Without subagents, follow the same brief yourself.

```text
Write a walkthrough of <feature> for <reader>. Repository <path>, branch <branch>,
commit <hash>. Feature diff: <range> (exclude <merge commit, skills folder>).

Load and follow these project skills (read <skills folder>/<name>/SKILL.md):
plain-visual-docs, no-slop-code, scratchpad-working-files, simplified-technical-language.

Read first: <spec> (use only the terms of its "Domain language" table), <ADRs>, the
files of the diff, and the tests of the diff.

Structure, in <language>:
1. What it does: one paragraph, no jargon (plain-visual-docs §1).
2. File tree of the feature: ASCII, + new, ~ changed, one short comment per entry.
3. The main path, stop by stop in the real execution order (for example middleware and
   handler, or command and service), with file:line at each stop. One ASCII or Mermaid flowchart of the order.
4. If there is a second actor or path (for example review, admin, background job):
   a Mermaid sequenceDiagram.
5. If data changes: a Mermaid erDiagram of new or changed tables, a stateDiagram-v2
   for records with a lifecycle, and what happens to existing data.
6. How it is tested: which test file covers which part, and one test that fails
   if a protection is removed.
7. How to try it locally: exact commands and URLs.
8. Up to three things that surprise a reader of the code, each with the reason.

Rules:
- Verify every claim against the code at <hash>. Cite with the full path every time
  (`src/app.ts:42`, never `:42` alone). Mark "not run" any
  claim you only inferred. Use the project's test harness (for example its test
  client with a scratch database), or no server at all.
- Validate every Mermaid block with the plain-visual-docs validator.
- Keep it shorter than the code it explains, about 150-300 lines. Do not repeat
  spec tables; link to the spec instead.
- Read-only on the repository. Write only .scratchpad/<slug>/walkthrough.md and scratch
  scripts under .scratchpad/<slug>/walkthrough/. No /tmp.
- Put the full text in your final message and list the files you leave.
```

Fill every `<…>` and drop the sections that do not apply.

## 3. Check before you deliver

The writer can be wrong about the code it cites. Check these after the writing:

1. Run `python3 <base directory of this skill>/scripts/check_walkthrough.py .scratchpad/<slug>/walkthrough.md <hash>`. It reports citations that point past the end of a file, point to files that do not exist at the commit, or have no file path. It also reports the Mermaid block count by type and the length.
2. Render every Mermaid block with the `plain-visual-docs` validator.
3. Run every claim that the writer marked "not run" (for example with a mutation that should make a named test fail). Restore the file after each mutation.
4. Grep the walkthrough for the words in the "Avoid" column of the domain language.

Fix the walkthrough when a check fails, or send the list to the subagent that wrote it.

## 4. Deliver

- In the chat: the path, what each section covers in one line, and the results of step 3.
- Offer to post it as a pull request comment, in the document language (`simplified-technical-language`). Do not commit it unless the user asks.
