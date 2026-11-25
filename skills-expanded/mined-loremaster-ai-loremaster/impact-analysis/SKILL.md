---
name: impact-analysis
description: >
  Computes the ripple radius (affected documents and concepts) of a proposed
  planning change via the graphify graph BEFORE the change is made and surfaces
  it for human review — triggers on "what's affected if we change X?" or
  "let's change X to Y" (analysis/finding by default and the human judges the
  direction; if the user explicitly approves applying the change, apply it and
  then always commit and push — never leave it uncommitted); this channel =
  this project only.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [ripple, impact, graphify, conflict, PM]
    related_skills: [conflict-detection]
---

# Change Ripple (Impact Radius) Analysis

Big planning changes are not local (a billing change → GTM, onboarding, a cascade of related features). **Your job is to *find* and surface what will be affected.** Fixing and judging are human work.

## Behavior
1. **Compute the impact radius (graphify):** query the graph for the change topic/node —
   - `graphify explain "<topic>"` : that node's neighbors (directly connected concepts/documents) + their relationships.
   - `graphify path "<A>" "<B>"` : the connection path between two points.
   - Identify wide-area impact via the **god nodes** (heavily connected hubs) and cross-links in GRAPH_REPORT.md.
   → Collect the **list of affected documents/concepts** and *why each is connected*.
2. **Flag ripple points (conflict):** check which points would become contradictions after the change, from the conflict-detection perspective — do the affected docs clash with the change topic? Quote open conflicts as they are.
3. **Organize and present:** lay out the affected items and (if the change goes through) the points that would become contradictions, at a glance, so the human can **decide whether to proceed with the change**. (No meeting feedback loop and no meeting-agenda chaining — this skill is pre-change impact discovery only.)

## Rules (invariants)
- **The human *judges* which way to change.** Never pick the direction yourself. But once the human approves applying it, apply that decision + commit and push (the ⚠️ section below). If only analysis was requested, git stays untouched.
- The graphify radius is not 100% accurate (leaks and false alarms are possible) → present results as **"impact candidates"** and say so when you are not sure.
- Never assert impact without evidence (a graph edge / a source document).
- This channel = this project only. This project's graph and lore vault only.

## ⚠️ If you *apply* a change — commit and push are mandatory (otherwise it is unreflected and the Obsidian pull is blocked)
This skill's default is **analysis (finding)**. But when the user **explicitly requests application** — e.g. *"let's change Google → Naver / change it for me"* — and presses the approval button (= the human has already decided), apply the change and then **always land it in git before finishing.** Applying without committing leaves the change **floating in the working tree only — it never reaches origin or the wiki** — and the pull from a separate clone (Obsidian) is blocked by the dirty tree.
1. Patch raw/PRD.md (+ directly affected docs). **Prefer not to edit the wiki directly** (refine derives it from raw) — patch raw only. If you had no choice but to edit the wiki directly, commit that too.
2. If the user explicitly named specific Jira backlog updates along with the PRD change, update those Jira issues via the REST API within the same approval scope and verify by re-fetching them. If a Jira issue key was mentioned, prefer a Jira lookup over document search. Jira edits are an external write separate from the docs commit — confirm they are inside the approval scope, and if not, get a separate `request_approval`.
3. Immediately after applying, **always run `git add -A <vault> && git commit`** (even a local commit alone leaves the working tree clean, so the Obsidian pull is not blocked).
4. **The origin push goes through a `request_approval` button** (title example: `origin push — <project> (change applied)`). APPROVED → `git push origin main`. DENIED / no response → hold only the push (keep the local commit).
5. If the PRD change makes the current spec in existing `wiki/concepts/*` stale, load the `refine-wiki` skill after landing raw and refresh the affected concept pages, `wiki/index.md`, and the graphify outputs. This refinement is derived from the raw decision, so it needs no fresh content approval — but after its separate commit, the origin push again goes through a `request_approval` button. In particular, for concepts graphify links directly to the changed topic (e.g. a change touching `pricing`, `data model`, `navigation`, or a related recommendation feature), check the wiki for staleness as well.
**Never end with an applied change left uncommitted.** (Analysis-only runs leave git untouched — nothing was changed.)

## Output
- *Change topic* → **impact radius** (documents/concepts + why each is connected) + **points that would become contradictions if changed**. Slack mrkdwn sections, not tables.
