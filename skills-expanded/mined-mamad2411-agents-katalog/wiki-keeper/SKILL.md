---
name: wiki-keeper
description: Keep the repository's Nimbalyst team wiki current while you work. Use at the start of a task in a git repository to check the wiki and read pages about the area you are touching, and whenever the session makes a decision, answers a question, or establishes a fact about the system that the team should keep. Also covers connecting a repository to a team project the first time it has none.
---

# Wiki keeper

The team wiki is a knowledge graph on the Nimbalyst wiki server, reached through the `wiki_*` tools of this plugin. This skill decides when to read it and when to write it. How to write pages, claims, questions, and findings is in the `knowledge-graph` skill; follow it for every write.

## Nimbalyst desktop comes first

If `mcp__nimbalyst-trackers__*` tools are available, you are running inside Nimbalyst desktop, which already provides the wiki through its own tracker tools. Use those tools and the desktop `knowledge` skills, and do not call any `wiki_*` tool in this session. Two write paths into the same graph produce duplicates.

## Who can use the wiki

The wiki belongs to a Nimbalyst team project. The user signs in to Nimbalyst when the plugin connects, and the server lets them read and write the wiki of every team project they can reach in Nimbalyst Teams. Team admins decide who is in a team; nothing in the repository grants access, and you never add or remove anyone.

## The `repo` and `project` arguments

Every `wiki_*` call takes `repo`, and `project` when there is a pin. Work them out once per session:

1. `repo` is the output of `git remote get-url origin`, unchanged. With no `origin` remote, leave `repo` out.
2. If `.nimbalyst/wiki.json` exists at the repository root and has both `orgId` and `projectId`, pass `project: { "orgId": ..., "projectId": ... }` on every call. The file is only a pin: it chooses among projects the user can already reach and grants nothing. Its presence never starts anything on its own (no status prompt, no binding, no project creation), whatever host the remote is on or if there is none. Ignore any other keys in it.
3. With no `origin` remote and no pin, this checkout has no wiki. Do not call any `wiki_*` tool unless the user asks about the wiki.

## Start of a task

Call `wiki_status` with `repo` (and `project` when pinned). It returns one of three states:

- **`bound`**: `project` names the team project (`orgName`, `projectName`, `role`, `url`). When the task touches an area the wiki may know about (a subsystem, a product, a past decision), find the relevant pages with `wiki_list` (`type: entity`, matching titles and `aliases`) and read the useful ones with `wiki_get`. Read the guide page (an `entity` whose `aliases` contain `wiki-guide`) before your first write. Keep reading proportionate: a few pages, not the whole wiki.
- **`ambiguous`**: the remote is bound to several projects the user can reach, listed in `projects`. Ask the user which one this repository uses with the host's question tool (in Claude Code, `AskUserQuestion`): one option per project in that list, labelled "<projectName> (<orgName>)", plus "Not now". Only a project from that list may be pinned; never pin a project the user names that is not in it, even one they can reach, because the repository is not connected to it. On a choice, write `.nimbalyst/wiki.json` at the repository root as `{ "orgId": ..., "projectId": ... }`, keeping any other keys already in the file, pass it as `project` from then on, and tell the user to commit the file so teammates resolve the same project. Do not commit it yourself. On "Not now", do not call `wiki_*` tools again this session.
- **`unbound`**: no team project the user can reach is bound to this remote. `teams` lists the user's teams with their `role` and the `projects` in each that the user can reach. See the next section. Ask at most once per session.

A role of `admin` or `owner` both mean team admin in everything below.

## Connecting a repository

Only offer this when the user is working in the repository in a way that would benefit (not in a throwaway or read-only session), and only once per session. Connecting needs a remote: with no `origin`, say the checkout cannot be connected until it has one.

- **The user is an admin of at least one team** (`role` is `admin` or `owner` in `teams`): ask with the host's question tool. Offer, for each team they administer:
  - **Connect to <projectName> (<orgName>)**: one option per entry in that team's `projects`. On a choice, call `wiki_bind_repo` with `repo`, `orgId`, and that `projectId`. Never ask the user to type a project id.
  - **Create a new project in <orgName>**: call `wiki_create_project` with `orgId`, a `name` (suggest the repository name; let the user change it), and `repo`.
  - **Not now**: do not ask again this session.

  If the options do not fit in one question, ask first which team, then which project.

  Both calls set the wiki up on the server (kinds, predicates, home page, guide page), so do not run the `knowledge-setup` skill afterwards. Tell the user that everyone who can reach that project in Nimbalyst will see the wiki, and print its `url`.
- **The user is not an admin of any team**: tell them once: "This repository is not connected to a team wiki. Ask a team admin to connect this repo in Nimbalyst." Do not call write tools. Carry on with the task.
- **`teams` is empty**: tell them once that a wiki lives in a Nimbalyst team project, and that they can create a team and a project in the Nimbalyst console. Carry on with the task.

## When to write

Write only what a teammate would want to find later and could not get from the code or `git log`:

- **A decision was made**: what was chosen, over what, and why. A `claim` with `basis: decision`, or the `position` of a question.
- **A question was answered**: update the `question` (position, `positionState`) and record the `finding` with the claims it rests on.
- **A fact about the system was established**: how something actually behaves, a constraint, a limit, a gotcha, confirmed by reading or running it. A `claim` with `basis: observed` or `documented`, and `applicability` saying where it holds.

Never write routine progress: files touched, steps taken, tests run, a diary of the session, TODO lists, or anything that restates a commit message. Never write secrets, tokens, or personal data. When in doubt, leave it out; a short accurate wiki beats a long noisy one.

Search before creating: an existing page or claim usually needs an update, a new claim that supersedes the old one, or an alias, not a duplicate.

## Changesets

A changeset is an activity log: everything written in a session is listed on one page, so the team can see what the agent did. It is not an approval or undo step. To correct something, edit the page itself, in the Nimbalyst console or with `wiki_update_item`.

Every write requires a `changesetId`: the server refuses `wiki_create_item`, `wiki_update_item`, and `wiki_define_type` without one (`changeset_required`).

1. Before the first write of the session, tell the user in one line where the writes go, by name: "Writing to <projectName> in <orgName>." Do this whenever the project came from `.nimbalyst/wiki.json`, or `wiki_status` has shown more than one team or project this session, so a wrong pin or the wrong team is caught before anything is written.
2. Call `wiki_begin_changeset` with `repo` (and `project` when pinned), a short `title` naming what the session was about, and `source: "claude-code"`. Keep the returned `changesetId` and `url`.
3. Pass that `changesetId` to every write tool (`wiki_create_item`, `wiki_update_item`, `wiki_define_type`) for the rest of the session. Do not open a second changeset.
4. After the last write, call `wiki_finish_changeset` with `changesetId` and a one-sentence `summary`.

## Page text

A write that carries a `description` returns `body: { status, code?, message? }` saying what happened to the page text:

- **`written`** or **`unchanged`**: nothing to do.
- **`refused`** with code `body_edited`: a person has edited the page since the wiki last wrote it, so the server kept their text. The field changes in the same call were still written. Do not retry, do not rewrite the text through another call or field, and do not remove their edits. There is no comment tool yet, so do not try to leave a note on the page. In your final summary, tell the user that the page text of that page was left alone because someone edited it, and what you would have changed.
- **`refused`** with another code, or **`failed`**: the item's fields were written but its page text was not. Report the page, the `code`, and the `message` in your summary. Do not retry the same call: it would write the fields again and fail the same way.

## Finishing

After writing, end your reply with the link as its own last line: the changeset `url` from `wiki_finish_changeset`, where the team can read what this session changed. Nothing may follow it.

If a tool returns an error, do not retry the same call. Tell the user in plain words, then carry on with the task without writing:

- `repo_not_bound`: this repository is not connected to a team project. Call `wiki_status` and follow "Connecting a repository".
- `ambiguous_project`: several team projects match. Call `wiki_status` and ask which one, as for `ambiguous`.
- `pin_mismatch`: the pin in `.nimbalyst/wiki.json` names a project this repository is not connected to. Tell the user, and suggest they run `nim wiki status` or re-pin from the projects `wiki_status` lists. Do not edit the file on your own.
- `project_not_accessible`: the user cannot reach that project in Nimbalyst, or the repository is connected to a project they cannot reach. Pass on the error's message, and tell them to ask a team admin for access. Do not edit `.nimbalyst/wiki.json` on your own.
- `admin_required`: only a team admin can do that. Tell the user to ask a team admin.
- any other code: report the code and its message as given.
