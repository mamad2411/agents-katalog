---
name: ask-science
description: "Step back from a science study: bring it and the shared .science/ shape up to the current format, then look back over its probes and conversation to judge whether it is on track, drifting or lost, find where STUDY.md, the notebook and the probes disagree, resolve each ambiguity with the user, and say how to resume."
license: MIT
disable-model-invocation: true
---

The user wants to step back from a study: unsure where it stands, sensing that the work, the notebook or the question have wandered, or after the science skills changed. This is a **retrospective** on one study: bring its records up to the current format, look back over what was done, judge whether it still serves the question, settle every place where the records disagree, and hand the user the command that resumes the work.

Change nothing until the user approves it. Call the Skill tool with `lab-notebook` for the tree, the formats and the probe states; the checks below compare the study against them.

## 1. The map

Show this map, then mark where the user is once step 2 knows.

```
/setup-science         once per repo: git, .science/SETUP.md, the library, the data folder,
      │                the conventions in AGENTS.md
      │
/experiment <study>    loads a study and focuses the session on it;
      │                opens it first when the folder does not exist (short grilling, first probe)
      │
      ├── probes        chosen one at a time; recorded results become evidence when the next starts
      │                 (pending work stays open; dropped only on the user's word)
      ├── fix a probe   a probe run wrong: fixed in place, rev +1, a lesson
      ├── desk-research a question answered once, into .science/library/, shared by every study
      ├── spin-off      a different question: /experiment <new-study> in a new session
      └── /promote      approved organization, reuse and preservation cycle; then return to probes

/ask-science           this: a step back on one study, bringing it to the current format first
```

Answer the user's direct questions about the flow from this map and the skills it names. Read a skill's `SKILL.md` before stating what it does.

## 2. Find the study

No `.science/SETUP.md`: the repo is not set up; recommend `/setup-science` and skip to step 7. Otherwise the study is the one this session loaded, the one the user names, or ask, listing every study in one line (open or closed, the question, its open probes).

## 3. Bring it to the current format

The skills change; a study written under an older version keeps its old shape until this step brings it up to date. Compare the study, and the shared `.science/` parts it uses, with the formats in `lab-notebook`:

- Stable probe IDs/names and globally continuing numbers across notebook/history, all cycles and current batch. Resolve records by current notebook href; approved physical cycle moves are legitimate, not missing probes. No automatic renaming, relocation, duplication, numbering reset or restoration into `probes/`.
- `STUDY.md` sections. A later correction written into it moves to the notebook's **Current direction** and **Drift log**, and `STUDY.md` goes back to its starting text.
- `NOTEBOOK.md`, rebuilt in the current sections: the map (threads and probe blocks) and the log built from the old notebook, the probe READMEs and `git log --grep '^<study>:'`.
- Probe README formats at their actual physical homes, preserving frozen statements and captured receipts when adding current metadata.
- Library/data indexes, provenance/checksums, current homes, notebook ideas, cycle manifests and physical dispositions with relative links. Check the current `probes/` batch is empty immediately after rollover; later new questions belong there. Cycle `active/` can physically hold continuing open probes; notebook state is current authority.

`.science/SETUP.md` and the `## Science skills` section of `AGENTS.md` belong to `/setup-science`: when they are out of date, say so and recommend rerunning it; do not edit them here.

Preserve frozen statements and captured receipts in their physical records. Add current metadata or corrections separately rather than rewriting those sources. Where the format needs missing history (an old probe's **asked**, its thread), reconstruct from original READMEs/commits, mark it `[reconstructed]` and ask in step 5. Preserve unmatched old text with its provenance; do not fabricate or silently discard it.

Show one plan table (path, change, evidence for reconstruction) and wait for approval. Migrate current metadata and sections without rewriting original captured receipts or approved cycle trees. Physical reorganization belongs to `/promote` and its exact-tree gate, not automatic format repair. With checkpoint authorization, commit only the approved study paths as `<study>: migrate to current format`, and approved shared parts separately as `science: migrate to current format`. Keep tags and history unchanged. If already current, say so and continue.

## 4. Look back

Read where the study started (`STUDY.md`), where it says it is (the notebook's **Current direction**, **Map**, **Log** and **Drift log**), what was actually done (`git log --grep '^<study>:'`, the probe READMEs, especially **Asked** against **Reading**), and this session's conversation. Then answer, with the evidence for each:

- What is the question now, and is it still the one in `STUDY.md`, or a change the drift log explains?
- What have the last few probes been trying to find out, and does that work bring the answer closer?
- Where did the direction start to shift, and did the user agree to the shift when it happened?
- Is the study still one question, or has it grown a second that belongs to another study?

Give a **verdict** in a few lines: **on track**, **drifting** (and since when, and why), or **lost**. Then the evidence, most telling first.

## 5. Settle the ambiguities

Compare the records with each other and with the format in `lab-notebook`. Every place where they disagree, or where the right reading is unclear, is an **ambiguity**, and the user resolves it. Look at least for:

- `STUDY.md` and the notebook telling different stories: a current direction with no drift log entry to explain it, a question restated differently.
- The **Map** and actual record locations: follow notebook hrefs across every cycle and current batch before calling a folder missing. Check ID uniqueness, manifest moves/dispositions, necessary live consumers and absence of duplicate copies/compatibility aliases in `probes/`. An approved archived record is not misplaced.
- State against remaining work: recorded results with unresolved jobs/analysis/discussion or partial components may legitimately stay open. Evidence with unfinished work, dropped with no **Dead ends**, or stale inference labels need clarification; physical `active/` placement does not override current notebook state.
- Work recorded in git but not in the notebook: probe commits with no log line, results the map does not show.
- Everything the migration marked `[reconstructed]`: confirm or correct it, then drop the mark.
- A story told twice in different words.
- **Ideas** that were already run, and probes run that the study never agreed to. Follow `lab-notebook` **Ideas** for same-question alternatives. If older records put them in separate approach directories, propose moving their unique content into notebook ideas or the ordinary probes that executed them, updating current links and removing obsolete scaffolding only with approval. Preserve captured history and frozen receipts.
- Work in the wrong place: this study's work in another study's folder or none, uncommitted changes, commits whose `<study>:` prefix does not match the paths they touch.
- Library/data indexes and dataset authority: distinguish explicitly approved shared source/prepared/reference data from unapproved fetched probe data, and workflow databases/outputs from general datasets.
- Ideas and cycles: proposals treated as executed, dropped probes or inconclusive evidence hidden, partial promotion incorrectly closing an open probe, archive mistaken for scientific invalidity, stale consumers or map links, and missing preservation digests.

Ask about them in rounds, the way `grilling` does: numbered questions, each naming the ambiguity, quoting the records that disagree, and giving your recommended reading, worded so "yes" accepts it. Most serious first. Wait for the answers before the next round.

When the **question itself has drifted**, offer three readings:

1. **The drift is legitimate.** The study now asks the new question: rewrite **Current direction** and add a drift log entry. `STUDY.md` stays frozen.
2. **Spin off.** The new question is a different study: it starts with `/experiment <new-study>` in a new session, naming the probes where the drift began under **Builds on**. Record it under **Spin-offs**.
3. **Back to the question.** Set the off-axis probes to `dropped`, record what they taught under **Dead ends**, and pick the next probe from the last on-axis one.

## 6. Repair and prevent

Apply each answer as a new commit, limited to the paths it fixes and prefixed with the study it belongs to; history stays as it is, because the checkout is shared.

Then name what let the drift happen, from step 4, and suggest one guard, written once the user agrees:

- **A Lesson** in the notebook, when it is about this study.
- **A convention in `.science/SETUP.md`**, when it holds for the whole repo.
- **A change to a science skill**, when a skill told the agent to do the wrong thing or left a gap: report it as a proposal naming the skill and the change; the skills are edited where they are maintained, outside the study.

## 7. Back on track

End with the resumption command and why: `/experiment <study>` to continue open work, choose from notebook Ideas and keep global numbering, `/experiment <new-study>` for a different question, `/promote` for approved organization or reuse, or `/setup-science` for missing setup. If repaired records make the existing map stale, offer `/scientific-map <study>` to refresh the shared map and select this study. Say when a new session is needed.

Done when the study is in the current format, the user has the verdict, every ambiguity is resolved or deliberately left, and they have that command.
