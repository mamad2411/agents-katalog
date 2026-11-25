---
name: resolve-conflicts
description: >
  Use when team members have posted prose verdicts on open conflicts (via /resolve, a
  "resolve conflicts" request, or a direct spec-change request) to draft a PRD revision
  plus diff, apply it only after human button approval, and align downstream docs to the
  updated PRD (PRD = SoT); acts in the PM/SM role; verdict = human, edit = Loremaster proposal, apply = approval
  gate; never auto-overwrite; this channel = this project only.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [conflict, resolution, PRD, SoT, write-gate, PM]
    related_skills: [conflict-detection, refine-wiki, impact-analysis]
---

# Conflict Resolution — Prose Verdicts → PRD Draft → Approval → Alignment (PRD = SoT)

When humans edit the PRD by hand, internal text dependencies break and consistency falls apart. So **humans provide judgment only (prose); Loremaster drafts a consistency-aware PRD revision** and a human approves it.

## Flow
1. **Collect:** Read the open conflicts in `conflicts/` plus the team's **prose verdicts** (this thread / provided text). Read them directly with `read_file`/`search_files` (no `execute_code`).
   - **Slack thread replies count as verdicts/instructions even without a mention.** In particular, when a user replies to my conflict-sweep message with things like "decided: 3 variants", "go with A", "go with B", treat that as the human verdict for that conflict — no separate @mention or re-confirmation required. If the thread context contains earlier replies, incorporate them first; never stall with "I couldn't read it because I wasn't tagged."
   - When the user replies to the conflict-detection result with bare numbered verdicts like `1. ... 2. ...`, map them in order to the existing `CONFLICT-001`, `CONFLICT-002`, ... as the team verdicts and proceed straight to resolution proposals. Do not ask "shall I resolve the conflicts?" separately.
   - When the user directly provides a `[spec change request]`, a specific PRD section, current/proposed text, and a supporting decision file, **run it through this skill's PRD-change flow even if no CONFLICT file exists.** Still follow the order: write PROPOSAL file → PRD approval button → apply → downstream alignment check → refine/push.
2. **Draft the PRD revision:** Produce a revision of `raw/PRD.md` that reflects the verdicts.
   - Account for **internal PRD dependencies and consistency** (changing one place means updating related statements too). Never invent blanks or missing content (if something is unclear, ask, as-is).
   - **Integrate resolution results into the PRD** (no separate decisions.md — it would collide with the existing DECISIONS.md).
3. **Proposal = write it to `conflicts/PROPOSAL_<YYYY-MM-DD_HHMM>.md` (team-timezone date+time suffix. Do not paste diffs into Slack — poor readability):**
   - **All timestamps use the team's timezone** — the filename, dates inside PROPOSAL/CONFLICT files, the `status: resolved` date, and the alignment dates in `raw/decisions/*.md`, all of them. Get them with `TZ="$TEAM_TZ" date +'%Y-%m-%d_%H%M'` (filenames) and `TZ="$TEAM_TZ" date +%F` (body). Never use the host/container default clock (UTC) as-is — always pass an explicit timezone so filenames and dates match the team's wall clock (set `TEAM_TZ` to your team's IANA timezone, e.g. `America/New_York`).
   - PROPOSAL.md layout: (1) team verdict summary, (2) the unified PRD diff under `## Stage 1 — PRD changes` (strict format below), (3) to-dos on apply.
   - **Unified diff format (no free-form):** one ```` ```diff ```` code block per file; first line `--- a/raw/PRD.md`, second line `+++ b/raw/PRD.md`, then `@@ section @@`; changed lines as `- old` / `+ proposed`; context lines indented one space with no prefix. Do not mix items — separate per file.
   - **Keep the Slack message short:** `📄 Please review <lore vault>/conflicts/PROPOSAL_<date>.md and let me know whether to approve.` (No diffs, no numbered prompts.)
4. **First approval = `request_approval` button (PRD change):** After presenting the PROPOSAL, get Slack [Allow]/[Deny] approval via **`request_approval`** (`title` = e.g. "Apply PRD revision — <project>"; `detail` = PROPOSAL path/summary). Apply **only on APPROVED**. On DENIED/NO_RESPONSE, no apply and no retry. No clarify/numbered text prompts.
   - (Note: a plain `git commit` is not a dangerous command, so no automatic approval button appears for it. Perform the approval explicitly via `request_approval`.)
5. **Apply stage 1 (PRD, first-approval scope):**
   - Update `raw/PRD.md` (git commit). Never apply unapproved parts.
   - The PROPOSAL's diff is a record for human review. When applying, extracting the diff from markdown code fences and relying on `git apply` can break on long diffs, abbreviated context, and fence counts. Prefer applying the approved changes via `patch` / an exact file rewrite, then verify with `git diff --check` and searches for the key phrases.
   - Mark the matching `conflicts/CONFLICT-*.md` as `status: resolved` (verdict date = **today in the team's timezone**) with evidence `raw/PRD.md (finalized)`.
6. **Second approval = downstream doc alignment (against PRD = SoT, separate button):** The PRD is now updated, so check the **other raw docs that still contradict the finalized PRD** (`raw/decisions/*.md`, gtm, etc. — `raw/**/*.md`; progress files are not there).
   - If contradictions exist (e.g. an old decision in `raw/decisions/` conflicts with the PRD / a reversed decision lacks a superseded marking / the frontmatter of the decision file the user cited is still `draft` while the request and PRD assume `stable`), build an **alignment plan** — mark the item `status: superseded` or draft a fix. **Never delete the decision log's original dates or content (preserve history).** Alignment annotations use **today's date in the team's timezone** — e.g. append to the entry: `> **superseded** 2026-06-23 — replaced by finalized PRD (Google login). (PROPOSAL_2026-06-23_HHMM)`. New decision entries use the format `### <today (YYYY-MM-DD)> #N — ...`. All dates via `TZ="$TEAM_TZ" date +%F`.
   - When a direct spec-change request piggybacks on an existing PRD-update flow (e.g. "fold this into the PROJ-36 update draft"), then after applying the PRD, also **add the current flow as a new decision row** in that decision file; do not delete the earlier interim decision — explain it as superseded.
   - **Append these alignment diffs to the same PROPOSAL file under a `## Stage 2 — Downstream alignment` section** (same unified diff format, separated per file).
   - Raise a **second `request_approval` button** (`title` = e.g. "Apply doc alignment — <project>"; `detail` = files to align + summary). **On APPROVED**, apply the alignment (git commit). **On DENIED/NO_RESPONSE**, hold the alignment — but stage 1 (PRD + resolved) is already applied, so do not roll it back. No retry, no workaround.
   - **If there is nothing to align (other docs already match the PRD), skip this stage and the second button.** Do not force a button when there is nothing.
   - **Guard against missed duplicate PRD sections:** Do not fix one spot in the PRD and stop. The same decision may be described in both the user journey (e.g. §9.1) and the screen/IA details (e.g. §13.1.1). Search all of `raw/PRD.md` — not just the lines quoted in the conflict — for the old canonical phrasing, its synonyms, and evidence IDs (e.g. `single-provider login`, `DECISIONS #44`, `Apple / Google`) and align every current-spec statement together. If the user reacts with "didn't you already update that?", first assume your earlier edit missed something and immediately hunt for leftover phrasing.
   - When the apply is done, mark PROPOSAL.md `status: applied`.
7. **Afterwards — auto-chaining (refine):** After the PRD and alignment are applied, if the open conflicts in `conflicts/` reach 0, **immediately auto-invoke refine-wiki** (no need for the human to call it again). refine-wiki handles graphify + wikilinks.
   - Count open conflicts only from the current status in `conflicts/CONFLICT-*.md`. Do not count old `-**status** open` lines inside `PROPOSAL_*.md` diffs.
   - refine's auto-refinement regenerates derived artifacts (wiki/graphify), so **do not raise another content re-approval button** — content approval finished in stages 1 and 2 above.
8. **origin push approval (automatic after commit):** After git-committing the changes, **do not wait for the human to say "push"** — immediately raise a `request_approval` **"Push to origin?"** button (`title` = `origin push — <project>`, `detail` = commit hashes/messages to push + remote URL). **On APPROVED**, `git push origin main`; **on DENIED/NO_RESPONSE**, do not push (keep the local commits). No retry, no workaround.
   - **Do not substitute text approval for a button timeout.** If `request_approval` returned `NO_RESPONSE` and the user later says "I approved it", the recorded tool result is still unapproved. Summarize the same push/write scope, **raise a new `request_approval`**, and proceed only when that new call returns `APPROVED`.
   - **In the normal flow that chains into refine-wiki, do not push here — batch it at refine-wiki's final push step** (PRD + alignment + wiki commits in one push, avoiding duplicate approvals). This step 8 applies only when the flow ends here without chaining into refine.

## Rules (invariants)
- **Verdicts and decisions belong to humans.** The team's opinion is the verdict; Loremaster is the proposer that turns it into PRD wording.
- Every external write (PRD/conflicts/other docs) goes through the **button approval gate**. Never auto-apply unapproved changes.
- The PRD is the SoT. One-way flow (update raw → derive wiki afterwards). No inventing blanks; keep evidence traceable.
- This channel = this project only. This project's lore vault only.

## Output
- Slack: PRD revision summary + changes + [Approve]/[Cancel]. After approval, report the apply results (commit, resolved markings, alignment proposals).
