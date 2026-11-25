---
name: backlog
description: Picks, adds, starts, closes tickets in docs/backlog/backlog.md; plans releases. Use for what to do next, noting a task or idea, a ticket started or finished, planning versions.
argument-hint: "[<repo>#T-NN | new <what> | start <repo>#T-NN | done <repo>#T-NN | plan]"
---

No `docs/backlog/backlog.md`: say so, offer setup (`ion repo update` brings it, moves old `docs/a-faire/`; elsewhere copy ion-repo's `template/docs/backlog/`).

`backlog.md`: only open-work list, by priority (🔴 critical, 🟠 important, 🟡 normal, ⚪ background), `Next free: <repo>#T-NN` in header. `done.md`, `rejected.md`: open only to write or when asked about past work. "How to use" in `docs/backlog/README.md` wins on conflict; read if unsure. Never read all of `backlog.md`: overview `grep -E '^(## |### ([a-z0-9-]+#)?T-|- \*\*Status)' docs/backlog/backlog.md`, then only involved tickets (`grep -n` heading, `Read` with offset).

IDs: every ticket is written `<repo>#T-NN`, in its own repo too (`acme-shop#T-07`), in headings, text, commits and PR bodies. `<repo>` is the repo's `name` (`.copier-answers.yml`), never its folder; another repo's ticket carries that repo's name. A branch keeps the number alone (`fix/t07`). Numbers never change and are never reused. A renamed repo: `ion repo set name=…` moves its own prefix in its own tracking; other repos' citations of the old name stay, the forge redirects it; git history is never rewritten. A bare `T-NN` is an unconverted one: `ion repo tickets` shows and converts them.

Ticket: `### <repo>#T-NN · Title`, then `- **Type**:`, `- **Status**:`, `- **Opened**: YYYY-MM-DD`, `- **Effort**: … · **Owner**: … · **Due**: …`, `- **Origin**: …`, details (`- [ ]`). Types: `bug`, `improvement`, `idea`, `task`. Statuses: `todo`, `in progress — branch <name>, since YYYY-MM-DD`, `blocked — waiting for <who or what>`, `to verify — <where>`.

**Owner**: `—` (free), `@login`, a first name (reserved, login unknown), `contributor — #NN`; never `Claude`. User: `gh api user --jq .login` (else `git config user.name`). Ticket owned by **anyone else**: never plan, start or code it, even partly; say who to ask. **Write only the user's own login**: if absent from every **Owner** while first names appear, ask once which is theirs, replace that one alone (on a branch). Never write, guess or ask another member's login.

`docs/_archive/`: read when a ticket cites it; old, check against current code; never edit.

**No argument**: next 3 tickets in section order, following the header's north star, skipping `blocked`, other owners, `contributor — #NN` (`/repo:good-first-issues`); each: ID, one sentence, effort, owner. List separately tickets blocked on the user. Check quickly in code that each isn't already done (quoted locations are often stale).

**ID**: other owner: stop, show ticket, say whose (they take it or hand over). Else show full ticket and cited archive lines, find files in current code, propose a short plan, create the branch (`/repo:worktree`), set `in progress — branch …`.

**`new <what>`**: `Next free` ID (then increment), fitting type (`idea` if undecided), `todo`, today as `Opened`, section by priority (⚪ for an idea to explore). If `## 🚀 Releases` exists, place it in the best-fitting release **whatever its position**; new release only if none fits, per `plan`.

**`start <repo>#T-NN`**: refused if other owner; else set `in progress — branch <name>, since YYYY-MM-DD`, free **Owner** becomes the user's `@login`.

**`done <repo>#T-NN`**: remove from its section; add at **top** of `done.md`'s log (under intro) `- **YYYY-MM-DD** · <repo>#T-NN · Title — what was done (branch) · opened YYYY-MM-DD`. Half done stays: tick steps, write what's left. Keep file's style. Remove from `## 🚀 Releases`; an emptied release is ready for its candidate: say so.

**`plan`**: put **every** open ticket in a planned release, written in `## 🚀 Releases` just above 🔴 (create if missing), then show it. Read every open ticket (priority, effort, status, blockers, what it touches) and the versioning rules of `CLAUDE.md`. Living draft: regroup freely within these rules.
- **Every ticket has a release.** Background, debt, ideas join the theme they serve; blocked on user: where it makes sense, marked `(blocked: <who>)`; dependent ticket: same or later release.
- **Real grouping.** One outcome a user notices or a milestone unblocked; name says it (`v0.4.1 · Nothing to trip on for a beginner`), never contents or `misc`. Link across priorities: 🟡 completing 🟠 goes with it.
- **No useless release.** Stray XS or vague theme: merge into a neighbour. Too big for `CLAUDE.md`'s cadence (default about a week): split along a real seam. A 🔴 bug may stand alone. Work known only partly today (one ecosystem after another, rules to write): size from comparable work, stated in the release line, never from its boxes.
- **Order**: blockers, then 🔴, 🟠, rest; within that, closest to the north star first.
- **Numbers planned, not promised.** 0.x: each release bumps patch; a milestone may propose a minor, saying why: user decides (patch until then). Minor goes to the release reaching the milestone, never the one starting it (leading to v0.8.0 is v0.7.x). Inserting or merging renumbers later ones. Candidate tagged: frozen, no ticket in or out.
- **Breaking** (CLI, `copier.yml` questions, generated tree, workflow inputs, skill and hook names, charter rule IDs): flag `⚠ breaking`; opens the release note, needs conversion in `ion repo update`.

Per release, in order:

    ### v0.4.1 · Nothing to trip on for a beginner
    Why these go together, in one sentence. ⚠ breaking: the size question goes away.
    - <repo>#T-39 · Start light, grow with the repo (M)
    - <repo>#T-42 · The git flow grows with the size (M)

Tickets stay in priority sections; this section quotes ID, short title, effort. After writing, show releases (name, tickets, why) and what moved; user reshuffles by asking. Public roadmap repo (`scripts/roadmap.py`, as ion-repo): redraw after every change.

Commit on the work branch, never integration. Never copy to `rejected.md` without the user's explicit decision.
