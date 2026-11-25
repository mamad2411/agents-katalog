---
name: github-loop-engineering-skill
description: Run an evidence-gated Loop Engineering control loop for GitHub Issues and GitHub Projects through the GitHub CLI (gh), keeping every issue cold-startable for a new collaborator or a fresh agent session. Use when an agent needs to discover work state; create, triage, prioritize, assign, split, block, start, finish, close, or verify work items; plan a parent issue's sub-issues and dependencies so agents can work in parallel, or fan out a parent's ready work to parallel agents; update project fields; maintain acceptance criteria and implementation notes; classify pull requests for human or agent review, walk a human reviewer through a pull request with multiple-choice questions, and merge clearly mergeable ones after an evidence gate; persist handoff state; initialize labels and a project board on first use; install or update issue templates; or route the next bounded task without cached IDs.
---

# GitHub Loop Engineering

Use GitHub Issues and Projects as the durable control plane and memory for Loop Engineering. Move each work item through one bounded, evidence-gated pass, using the GitHub CLI, `gh`, for every GitHub read and write.

Four ideas carry the skill:

- **The issue is the unit of handoff.** Every issue stays cold-startable: someone with no prior context, including a fresh agent session, can read it and act on it without asking anyone or reading chat history.
- **A parent issue is the unit of parallel work.** Its sub-issues and the blocked-by dependencies between them form a work graph. Any agent can take the parent, find the children that can start now, and run them in parallel, each starting cold from its own issue.
- **Evidence is recorded once and reused.** Each check, review, and decision is written to the issue or the pull request together with the commit it covers. Whoever comes next reads that record and repeats only what it doesn't cover.
- **Code is reviewed locally, pull requests for their content.** Each commit and each high-risk change is reviewed locally, under the team's AI controls, before the pull request opens. Reviewing a pull request never means reviewing its code: it checks only that the pull request's content meets what this skill requires. A pull request opens complete, every check and piece of evidence already recorded, because it asks for review and merge and is not where verification is finished.
- **Agents merge what evidence can settle.** An agent merges a pull request that passes the merge gate. A human confirms what evidence can't settle, above all how an interface looks and feels.

## Contents

- [Read the references](#read-the-references)
- [Rules](#rules)
- [The loop](#the-loop)
- [Verify once](#verify-once)
- [Work-item rules](#work-item-rules)
- [Operations](#operations)
- [Failure handling](#failure-handling)

## Read the references

| Reference | Read it |
|:--|:--|
| [references/gh-cli.md](references/gh-cli.md) | Before the first GitHub operation in a session, and whenever a command, flag, or JSON field is unclear |
| [references/work-item-format.md](references/work-item-format.md) | Before creating an issue or substantially rewriting an issue body. It defines the cold-start contract and check |
| [references/pull-requests.md](references/pull-requests.md) | Before opening, classifying, reviewing, or merging a pull request |
| [references/fan-out.md](references/fan-out.md) | Before handing leaves to parallel agents, and when you resume a fan-out after an interruption |
| [references/initialization.md](references/initialization.md) | When a repository's issues or board are used for the first time |
| [references/issue-templates.md](references/issue-templates.md) | When installing issue templates, or when a repository's templates differ from this skill's in [assets/issue-templates/](assets/issue-templates/) |

## Rules

1. **GitHub through gh.** Use the GitHub CLI for every GitHub read and write: its own commands first, and `gh api` for REST or GraphQL requests they don't cover. Don't use `curl` or any client that needs the raw token, and don't use a GitHub MCP server for this skill's work, so that every agent's commands, records, and briefs stay comparable. Stay inside the [command boundary](references/gh-cli.md#command-boundary): gh can also delete repositories, change settings, and bypass branch rules, and none of that is part of a transition unless the user asks for exactly that.
2. **The installed gh wins.** Flags and JSON fields change between gh releases. When a command in this skill is unclear or rejected, read `gh <command> <subcommand> --help` on the installed version and follow it. Read JSON with `--json` or `--format json`, never the table output, and pass issue and pull request bodies with `--body-file`, never inline through the shell.
3. **Discover at runtime.** Find the repository, project, fields, options, labels, issue types, and item identifiers in the current session. Never copy IDs or option values from another repository, and never cache them in this skill.
4. **One transition at a time.** Frame one authorized state transition, with its evidence and its stop condition, and make the smallest mutation that completes it.
5. **A write's response is a claim.** Re-read the affected resource after each write. The transition is verified only when a fresh read shows the intended state.
6. **Persist for a cold start.** Write verified state, decisions, and remaining work to GitHub so that another agent or a human can resume without you. An issue that fails the cold-start check is not finished being written.
7. **Verify once.** Record each check with the commit it covers, and reuse a recorded check instead of running it again, as described in [Verify once](#verify-once).
8. **Preserve what exists.** Keep repository conventions and existing content unless the user explicitly asks to change them. Repository guidance wins over every default in this skill.
9. **Brief delegated agents.** A delegated agent doesn't inherit this skill. Put the rules in its prompt: GitHub access through gh only and inside the command boundary, the exact commands and inputs, `-R owner/repo` on every command, bodies through `--body-file`, which writes it may make itself, never writing content it hasn't read, and when to stop and report.
10. **Never merge on your own judgment.** Merge a `review:ai` pull request only when it passes the [merge gate](references/pull-requests.md#merge-gate) on its current head commit. Merge a `review:human` pull request only after a human approved its current head commit for merging and the gate's other conditions hold, as described in [Human review](references/pull-requests.md#human-review).
11. **Public means published.** In a public repository, every issue, comment, pull request, commit, and CI log is published the moment it is written, and edit history keeps what a later edit removes. Never write secrets, internal hostnames or addresses, customer names, or personal data there. Read what a delegated agent prepared before it goes out.

## The loop

Run every operation as:

**Discover → Frame → Act → Verify → Persist → Continue or stop**

- **Discover:** rebuild the current state from GitHub, not from memory.
- **Frame:** select one bounded transition, its authorization, and the proof of success.
- **Act:** perform the minimum mutation in dependency order.
- **Verify:** compare freshly read state with the intended state.
- **Persist:** write durable evidence, decisions, blockers, and handoff context.
- **Continue or stop:** route the next authorized step, or stop at done, ambiguity, missing evidence, missing capability, repeated failure, or a human gate.

Do not collapse Act and Verify into one step. A successful write response proves only that GitHub accepted a request, not that automations, linked state, or concurrent edits produced the intended result.

### Discover

Identify the target:

- the repository owner and name;
- the project owner, owner type, and project number;
- the issue, pull request, or project item being changed;
- the requested final state.

Take these from an explicit URL or the repository context when possible. If several repositories or projects remain plausible and a write could land in the wrong place, ask one concise question before mutating anything. Do not guess a project merely because its title resembles the repository name.

Check the GitHub CLI as described in [Set up gh](references/gh-cli.md#set-up-gh): `gh --version` reports 2.97.0 or later, and `gh auth status` shows a login whose token reaches the repository and, for board work, has the `project` scope, or `read:project` for reads only. If gh is missing, too old, or not authenticated, or the token lacks a scope or permission the transition needs, stop before the mutation and report the exact step the user must take, such as running `gh auth refresh -s project`. Get the host's approval before downloading software, and never print or store the token. Then resume from a fresh Discover pass.

Before the first write:

1. Read repository guidance and issue templates when available. When guidance says the templates come from this skill, compare them as described in [Keep issue templates current](#keep-issue-templates-current).
2. List matching projects and verify the selected project's title and number.
3. List the project's fields and their current options.
4. List the existing repository labels.
5. List issue types and custom issue fields only when the repository supports them or the request needs them.
6. When updating existing work, read the current issue, its labels, relevant comments, hierarchy, and project item.

Paginate until uniqueness is established. Prefer human-readable field and option names, which gh resolves by name.

**First-use gate.** If this Discover pass shows that the repository's issues, its board, or its pull request review have never been set up for this workflow, as defined in [references/initialization.md](references/initialization.md#when-to-initialize), stop the original transition. Propose initialization, and run it only after the user authorizes it. Resume the original request from a fresh Discover pass once initialization is verified or explicitly declined. If the user declines, work with the vocabulary that exists and don't invent labels or statuses.

### Frame

Define:

- the current observed state;
- one requested or policy-authorized next state;
- the exact issue and Project mutations needed;
- the evidence that will prove success;
- the conditions that require stopping or human input.

When repository guidance sets no policy, use these defaults:

- Represent actionable work as a real issue, not a draft project card.
- Use the repository's established language and terminology.
- Write the issue body to the cold-start contract in the [work-item format](references/work-item-format.md): why, what, current state, acceptance criteria, and pointers, with absolute dates and no session-only references.
- Use project fields as the source of truth for board state.
- Triage by best judgment, as described under [Status](#status) and [Priority](#priority).
- Add a duplicate priority label only when the repository already requires field-and-label synchronization.
- Reuse existing labels. Create or rename labels only when the user requests it, standing repository policy clearly authorizes it, or an authorized initialization adds them.
- Leave assignees empty on creation unless the user names someone. Assign the authenticated user when work starts, as the claim on the issue.
- Use issue types only when supported. Do not emulate them with new labels unless repository policy says to.
- Treat follow-up work an agent discovers as a proposal. Create it only when the user requested discovery-and-creation or the repository has a standing intake policy. Give a follow-up you create the milestone or parent it belongs to, and don't add it to the current run unless it belongs there. A finished leaf often turns up one or two follow-ups, and a run that takes on all of them doesn't finish.

### Act

Perform related mutations in dependency order. Change only the fields, labels, body sections, relationships, or state the framed transition requires. Keep mutations idempotent when the API supports stable issue locators or read-before-write merging.

### Verify

Re-read the affected issue, hierarchy, pull request, or project item after each mutation, and request every field you need to compare. Verify both sides when one operation can trigger an automation elsewhere, such as closing an issue and moving a Project status.

Whenever the transition created an issue, changed its body, or changed its Status, run the [cold-start check](references/work-item-format.md#cold-start-check) on the body as read back from GitHub. A failed check means the transition is not yet verified.

If an operation partially succeeds, rebuild the involved state and recover only the missing part. Retry only with new evidence or a changed strategy. Do not repeat an unchanged failing call.

### Persist and route

Keep the issue body as the durable current-state snapshot. Put chronological decisions, validation, gotchas, and partial progress in comments. Keep Project fields synchronized with the verified lifecycle state.

Report the final issue URL or number, the Project, the fields changed, the evidence, and the observed result. Route only an authorized next step. Otherwise stop with a precise handoff that describes the state, the blocker, and the condition for the next loop.

## Verify once

Work passes through several hands: the agent that implements it, a coordinator, a reviewer's agent, the agent that merges it, and often another person's agent in a later session. Each check runs once. Its result is recorded, and everyone after that reads the record instead of running the check again.

**Record.** When you run a check, a review, or an audit, write the result where the next reader will look. Anything about a change goes into the pull request's [verification record](references/pull-requests.md#verification-record). Acceptance evidence and decisions go into the issue. Each record names the commit SHA it covers, who ran it (the person, or the agent and its model), what it covered, and the result.

**Reuse.** Before you run a check, a review, or an audit, or delegate one, look for its record. A record is a claim, and you test a claim by reading it against what GitHub and git show: the commit it names is in the pull request, CI ran on that commit, a fix it names exists. You don't test it by doing the work again. Then do only what the record doesn't cover: the commits after the one it names, an area it leaves out, or a check nobody recorded. Add your result to the record, so the next reader doesn't repeat your part either. A pull request is the exception: a reviewer or a merging agent doesn't fill a gap in its record, but returns it to draft for the author's side, as in [Verification record](references/pull-requests.md#verification-record).

A record in any form counts, including one written before this format. One that names no commit covers the commits that existed when it was written.

**Don't reuse** a record when:

- it was written by someone without write access to the repository, as in a pull request from a fork;
- what you observe contradicts it. Then run that check yourself and correct the record;
- the user, a human reviewer, or repository guidance asks for an independent check at that point.

Nothing else is a reason to repeat recorded work. A high-risk change is not one. Neither is a rule that sends some kind of work to a stronger model or a dedicated agent: such a rule decides who runs a check, not whether a finished check runs again.

Reading your own write back, as rule 5 requires, is not a repeated check. It is one cheap read, and it is how the write gets verified in the first place.

## Work-item rules

### Status

Map workflow intent to an existing project option. Never assume exact option names:

- unreviewed intake → `Triage`, `Inbox`, or equivalent;
- accepted but not started, including work that waits on other issues → `Todo`, `Ready`, or equivalent;
- active work → `In Progress`, `Doing`, or equivalent;
- work stopped by something outside the work graph → `Blocked` or equivalent;
- completed work → `Done`, `Complete`, or equivalent.

If no unambiguous option exists, leave the field unchanged and ask for the intended mapping.

Agents triage by best judgment: accepted work moves to the accepted option, and rejected work is closed as not planned. Leave triage to humans when repository guidance or the project's own Status descriptions reserve it, as boards initialized with earlier versions of this skill do.

Waiting on another issue is not a blocked status. Record the prerequisite as a native blocked-by dependency and keep the item in the accepted option. GitHub marks the item blocked until every prerequisite closes, so the Project filter `-is:blocked` separates work that can start now from work that waits. Use the blocked option only for blockers outside the work graph, such as a pending decision, missing hardware or access, or another team.

A parent issue moves to the active option when its first child starts, and it closes through its own completion ritual once every child is closed.

Project automations can change state on their own, so check the documented workflows before acting:

- An **Auto-close issue** workflow closes the issue as soon as Status becomes the completed option. Never set the completed option before the completion ritual. Close the issue and let the automation move Status, then verify.
- When an issue is reopened and no reopen workflow is documented as enabled, move Status back to the correct option explicitly.

### Priority

Use the project's existing priority scheme. Infer meaning only from documented option names or repository guidance. Do not invent `P0`, `P1`, or `P2`, and do not create a Priority field as part of an ordinary issue update. The baseline scheme in the initialization reference applies only after the user authorizes initialization.

Set Priority when you create an issue, by best judgment against those meanings, unless repository guidance reserves it for humans. When the current focus follows milestones, raise the next milestone's issues when it becomes current.

When the repository mirrors priority in labels, read the full current label set, remove only the superseded priority label, add the new one, and preserve every unrelated label. An organization can also define an issue field named Priority. It is separate from the Project's field, so set it only when repository guidance chose it as the mirror.

### Acceptance criteria

Write observable, testable checkbox items. Include commands, user-visible behavior, or concrete artifacts where appropriate. Mark an item complete only when evidence supports it, and record that evidence in an issue comment or in a test report in the repository's docs. Do not close an issue with incomplete criteria unless the user deliberately descopes them and the issue records that decision.

A short answer that skips a criterion, such as "don't test that", can mean "not now", for example because the hardware or access doesn't exist yet, rather than "never". Record the criterion as pending, with the reason and the condition for doing it, unless the user says to drop it. When the answer could mean either, ask in one line.

A claim that something didn't happen, such as a scheduled run that never started, is evidence only once it can no longer happen. Scheduled workflow runs can start hours late.

### Dates and notes

Use absolute ISO dates (`YYYY-MM-DD`) for blockers, decisions, and completion notes. Put durable current-state information in the issue body and chronological implementation notes in comments.

## Operations

### Create an issue

1. Search for likely duplicates.
2. Read labels, optional issue types, repository templates, and the [work-item format](references/work-item-format.md).
3. Create the issue with a complete cold-startable body and only known labels, milestone, and type. Add assignees only when the user names them.
4. Add it to the selected project. If the project's auto-add workflow already attached it, treat an already-present response as success.
5. Set the requested project fields one at a time, by current field and option name.
6. Read back both the issue and the project item, including every field just changed, and run the cold-start check on the returned body.

### Update or reprioritize an issue

1. Read the issue and its current project item.
2. Update the relevant issue metadata or body. Preserve the rest of the body and every unrelated label.
3. Update only the requested project fields.
4. Verify that the issue and the board agree.

When one authorized transition sets the same field value on several items, such as moving a set of accepted children to the ready option, update each item in turn, paced as [Change many items](#change-many-items) describes. Then verify every item, because a run can stop partway.

### Start work

Starting work means claiming the issue, moving it to the existing active-status option, updating `State` in the body, checking the issue for overbuilding, and planning how each acceptance criterion will be proven. Add an implementation note only when it provides durable context.

#### Claim the issue

Nobody is assigned when an issue is created. At the start transition, the assignee is the claim: it tells other people and agents that the issue is taken, so two of them don't pick up the same work. Claim the issue before any other work on it:

1. Read the current assignees.
2. If the authenticated user is already assigned, keep the assignment.
3. If nobody is assigned, assign the authenticated user without asking. `gh issue edit <number> --add-assignee @me` assigns the authenticated user and leaves any other assignee in place. Leave the issue unassigned only when the request or repository policy says so, for example when only a human assigns work.
4. If someone else is assigned, don't start, reassign, or add anyone. Report the current assignee and ask how to proceed.
5. Add your assignment, then re-read the assignees. If the read-back shows another assignee, someone claimed the issue at the same time: remove only your own login and handle it as in step 4.

#### Check the issue for overbuilding

An issue can ask for more than its goal needs, and an agent that executes it faithfully builds all of it. Only the user can descope an acceptance criterion, so give them the chance before the work starts. Right after you claim an issue, and before you write any code, compare its `What` and acceptance criteria with its `Why` and look for items that:

- don't serve the stated `Why`;
- build generality for a need nobody has stated, such as an option, plugin point, or abstraction layer with only one user;
- already exist in the repository, fully or in part;
- require verification beyond what the repository's guidance asks for at this stage.

When none match, continue without saying anything. A check that asks every time slows every loop. When some match, ask the user once, with all the items in one question set, as for a [pending decision](#mark-or-clear-a-blocker): for each item, name the criterion or scope line, say why it looks unneeded, and give the choices, which are drop it, move it to a follow-up issue, or keep it, with your recommendation first. Keep working on the parts the answer doesn't affect while you wait.

Record the answer in the issue as an explicit descoping decision with its date and reason, in `Out of scope` and an implementation note, so that someone who resumes the issue cold knows why the criteria are fewer. A moved item becomes a follow-up issue only under the follow-up rule in [Frame](#frame). In a fan-out, the coordinator runs this check on each leaf before handing it out, and a leaf agent that finds overbuilding during the work reports it rather than descoping on its own.

While you work, build only what the acceptance criteria need. An improvement you notice along the way is a follow-up proposal, not part of the current change.

#### Plan the verification

Verification comes before the pull request, never after it. The merge gate needs evidence for every acceptance criterion, so a pull request whose evidence is still to come passes CI and then can't merge. It waits with green CI while the verification runs, each commit that adds evidence reruns CI, and the base moves on under it.

Right after the overbuilding check, and before you write code, decide for each acceptance criterion what will prove it and where that runs: a test, a command on a build machine, an end-to-end or browser run against the branch's head, a run on lab hardware or a preview environment, or a CI job. Line up what the proof needs, such as hardware, a shared test environment, or a person's time, so the evidence is ready when the code is.

A criterion that only something after the merge can prove, such as a deployment of the base branch, a nightly or release build from it, or a field test scheduled for later, can never pass the merge gate in this issue. Settle it now, not when the pull request is ready: ask the user, as a [pending decision](#mark-or-clear-a-blocker), whether to prove it before the merge instead, for example with the same deployment from the branch's head, or to move it into its own issue that is blocked by this one. Record the answer as for descoping. In a fan-out, the coordinator does this for each leaf before handing it out.

### Plan a work graph

Use sub-issues when parts can be independently assigned, sequenced, or accepted. Keep small implementation steps as acceptance-criteria checkboxes.

When the parts can run in parallel, plan them as a work graph that agents can execute:

- Make the parent a container. Its body states the goal and the done criteria and lists the children, and nobody implements the parent directly. Nest another level only when the grouping helps someone take a slice of the work.
- Size each leaf for one agent pass that ends in one reviewable change, with its own acceptance criteria. A leaf must be startable from its own body, as the [work-item format](references/work-item-format.md#parent-issue) requires. Every criterion of a leaf must be provable before the leaf's pull request merges. A proof that needs the merged result, such as a deployment of the base branch or a test on site, belongs to a later child that depends on the leaf, like the exit child below, never to the leaf that changes the code.
- When the parent's done criteria need end-to-end proof, add a final exit child that proves them, for example with an automated test. It depends on the leaves it covers.
- Add blocked-by dependencies only between leaves, and only for real prerequisites: a leaf can't start, or can't be accepted, without another leaf's result. Keep the graph acyclic. Prefer many independent leaves and a short longest chain to a long sequence of small steps.
- Don't stack leaves. A leaf that needs another open leaf's change starts from the base once that leaf merged. When it has to start sooner, it starts from the prerequisite's head and brings in the base once, after the prerequisite merged. It never merges the prerequisite's branch again while both are open: every later commit on either branch then becomes a conflict on the other, and the two pull requests' records overlap.
- Keep interface changes in leaves of their own where the work allows, apart from the logic behind them. A person confirms every change to what a user sees, so only those leaves' pull requests wait for one. Put the approved design or the exact copy into such a leaf's body, asking the user for it as a [pending decision](#mark-or-clear-a-blocker), so that the review confirms a result rather than starting a redesign.
- Check the leaves for [shared hotspots](#shared-hotspots) before you create them.
- List each leaf's parent and prerequisites in `Pointers`.

#### Shared hotspots

A hotspot is a place in a file that many changes extend at the same spot, such as a central route or permission list, an API document's path list, a changelog section, an index, or a README section that every feature adds to. Two leaves that both add to it conflict, whichever merges second, and the more leaves run in parallel, the more conflicts each pull request meets before it merges. Generated files and sequence numbers are hotspots too: every leaf that adds an endpoint regenerates the same API spec and the client built from it, and two leaves that each add a database migration take the same number.

1. Find the hotspots. The best evidence is the conflicts that recent merges actually resolved. For each merge commit on recent pull request branches, `LC_ALL=C git show --remerge-diff --format= <merge commit>` names every file it resolved on a `remerge CONFLICT` line, so count those files. Set `LC_ALL=C`, because git translates that line in other locales. Add the files that the leaves' scopes name or will change, and the files that the base branch's recent commits change most often, for example `git log -100 --first-parent --name-only --format= <base> | sort | uniq -c | sort -rn`. Then read where in the file the changes land. A file that many commits change in different places is not a hotspot.
2. When a few leaves add an entry or two to the same hotspot, keep them parallel. The conflicts are small. When those leaves are ready together and share a review lane, the coordinator merges them locally into one [batch](references/fan-out.md#batch-leaves-into-one-pull-request) and resolves their conflicts once. Otherwise they merge [in line](references/pull-requests.md#merge), and each one resolves its conflicts once, at its turn.
3. Resolve a conflict in a generated file by running its generator once the rest of the merge is resolved, never by editing its conflict markers. Take a sequence number at the leaf's turn to merge rather than when the leaf starts, unless the repository names such files in a way that can't collide, such as by timestamp. Two leaves that take the same number usually don't conflict in git, so check for a collision at each turn to merge and treat one like a conflict.
4. When the same hotspot conflicted in several pull requests within a few days, or its structure makes most leaves conflict, for example because every new endpoint must be added to several central lists, restructuring it saves more than any merge order can. Propose the restructuring to the user right away, with the conflict counts, rather than as a follow-up note: letting each module register its own entries, generating the list, splitting the file, or naming files so they can't collide. Once the user accepts, create it as its own issue at the priority of the work it slows, and make the leaves that would conflict blocked by it when it can land first.
5. Don't split or reorganize a hotspot inside a feature leaf. Moving content conflicts with every open pull request that touches the file. A restructuring is its own change, made when few open pull requests touch that file.

#### Create the children

1. Create each child as a complete, cold-startable ordinary issue that names its parent in `Pointers`, and pass the parent with `gh issue create --parent`, so that creation and attachment happen in one call.
2. For an issue that already exists, attach it with `gh issue edit <child> --parent <parent>`.
3. Add each child to the project and initialize its fields.
4. Add the dependencies as described in [Mark or clear a blocker](#mark-or-clear-a-blocker).
5. Re-read the parent's sub-issues, each child's project item, and the dependencies.

When bodies must reference issues that don't exist yet, create the issues one at a time in a fixed order. Check each returned number against the number the bodies assume, and stop at the first mismatch.

Do not confuse the issue number, the database ID, the node ID, and the project item ID.

### Split an issue that turns out too large

An issue that is too large blocks other work. Its assignee claims all of it, so nobody else can take a part, and every issue that waits on it waits for all of it. When you find, at the start or during the work, that the issue won't end in one agent pass and one reviewable change, that part of it could be taken by someone else now, or that an issue blocked by it needs only part of it, split it before you continue. Don't ask first, unless repository guidance reserves splitting for humans. In a fan-out, a leaf agent doesn't split its leaf: it stops and proposes the split in its report, and the coordinator splits it.

1. Stop at a clean point, and record the progress so far in an implementation note with its commits and evidence.
2. Plan the parts as a [work graph](#plan-a-work-graph). The part already in progress becomes one leaf, and it stays yours.
3. Turn the original issue into the parent: rewrite its body to the [parent format](references/work-item-format.md#parent-issue). Move every acceptance criterion into the child that will prove it or into the parent's done criteria, so none is lost, and carry each child's finished progress into its `State`.
4. Create the children. Assign yourself only the leaf you continue, and leave the others unassigned in the accepted option so that others can take them now. Keep the parent in the active option and remove your own assignment from it, so your claim covers only your leaf.
5. When another issue is blocked by the original but needs only one part, move its dependency to that child, as in [Mark or clear a blocker](#mark-or-clear-a-blocker).
6. Add an implementation note on the parent that records the split and its date. Re-read the parent, the children, and the dependencies, and run the cold-start check on each body. Then continue with your leaf.

### Fan out from a parent issue

Use this when you are asked to work through a parent issue and the host can run agents in parallel. Without parallel agents, work through the same ready set one leaf at a time. [references/fan-out.md](references/fan-out.md) describes the coordinator's side in full.

1. Read the parent, its sub-issues at every level, and their project items.
2. Find the ready set: open leaves in the accepted status that nothing blocks and nobody else is assigned to. A Project query returns it for each container, for example `parent-issue:owner/repo#40 status:Todo -is:blocked` with the project's own option names. Order the set by Priority.
3. Claim each leaf before handing it out: [assign](#claim-the-issue) the authenticated user, move it to the active option, and re-read it. Skip a leaf that someone else is assigned to or already started. Move the parent to the active option with its first leaf. [Check each leaf for overbuilding](#check-the-issue-for-overbuilding), [plan its verification](#plan-the-verification), and ask about all the leaves' findings in one question set.
4. Give each claimed leaf to its own agent in an isolated workspace, such as a git worktree. The prompt names the repository and the issue number, tells the agent to run this skill's loop on that issue only, and points it at the written [brief](references/fan-out.md#write-one-brief) that repeats the rules it doesn't inherit. The agent asks you whatever its issue and the brief don't answer, and you answer it yourself, as in [Answer the agents' questions](references/fan-out.md#answer-the-agents-questions): you hold the run's context, and you take to the user only what only the user can decide.
5. When an agent reports back, check its report against GitHub, git, and the record of its work, as in [Review before anything goes out](references/fan-out.md#review-before-anything-goes-out), and have a fresh agent on a smaller model run the [acceptance check](references/pull-requests.md#acceptance-check) on every leaf. Have a second agent try to break a leaf with security or design risk before its pull request opens, and write the result into the pull request, as in [Verify risky leaves independently](references/fan-out.md#verify-risky-leaves-independently). Then rerun the ready-set query, because a closed leaf can unblock others, and hand out what became ready.
6. Once a leaf's every criterion has evidence and its acceptance check found nothing left, open a pull request for it, or one for a [batch](references/fan-out.md#batch-leaves-into-one-pull-request) of leaves that change the same files, share a review lane, and are ready together, so CI runs once, their conflicts are resolved locally, and a person reviews one feature once. Merge the pull requests in line, one at a time, as described in [Pull requests](#pull-requests): you merge the `review:ai` ones, and the `review:human` ones only after a human approves them. Leaf agents never merge, because every merge moves the base branch under every other open pull request.
7. Stop when every child is closed, the same leaf fails twice, or a step needs a human. Close the parent through its completion ritual, or leave a handoff comment on the parent that lists each child's state.

After an interruption, such as a usage limit or a context reset, rebuild the state from GitHub before you resume any agent, as described in [Resume after an interruption](references/fan-out.md#resume-after-an-interruption).

### Mark or clear a blocker

A wait on another issue, a blocker outside the work graph, and a decision only the user can make are recorded differently.

**Prerequisite issue.** Add a native blocked-by dependency from the waiting issue to its prerequisite, list the prerequisite in `Pointers`, and leave Status unchanged. The Project's `is:blocked` filter reflects the dependency, and GitHub clears it when the prerequisite closes. Write it with `gh issue edit <waiting> --add-blocked-by <prerequisite>` and read `blockedBy` back, as in [Add a prerequisite](references/gh-cli.md#add-a-prerequisite). If the write fails, keep the prerequisite in `Pointers` and report that the native dependency relation was not changed. Never leave the task looking fully linked when it is not.

**External blocker.** When marking blocked:

1. Record the blocker, the date, and the exact unblock condition in the managed `Blocked by` section.
2. Add an existing blocked label if repository policy uses one.
3. Move the project item to the existing blocked-status option if available.
4. Verify all supported representations.

When unblocking, remove only the resolved blocker entry and the blocked label, restore the appropriate workflow status, add the resolution date, and verify that no other blocker remains.

**Pending decision.** A decision only the user can make is an external blocker on each issue that waits for it. Don't collect decisions in a parent issue's body for the user to find there, because they wait for days, and don't send a pull request to human review to get one decided. Ask the user directly, several at a time, with the host's question tool when it has one. Make each question self-contained: the issues it blocks, what each option does and costs, and your recommendation as the first option. Read a free-text answer literally, and treat a multiple-choice question answered with nothing selected as "change none of these". Record each answer in the issues it affects, with its date, then unblock them.

### Add implementation notes and links

Use `gh issue comment` with `--body-file` for decisions, gotchas, partial progress, validation results, and commit references. Keep comments concise and append-only.

For pull requests, use an auto-closing keyword such as `Closes owner/repo#N` only when the merge should close the issue. Otherwise use a non-closing issue reference. Re-read the issue or pull request after changing linkage-sensitive text.

### Pull requests

Follow [references/pull-requests.md](references/pull-requests.md). In short:

A pull request gets no code review. Code is reviewed locally before the pull request opens: each commit by the pre-commit review gate, and a high-risk change by one security review. Reviewing a pull request checks only that its content meets what this skill requires, including that those local reviews are on record. When something is missing, send the pull request back to the author's side to supply it.

1. **Verify, then open.** A pull request opens only once it could merge as soon as CI is green. Before the first push, prove every acceptance criterion as [planned](#plan-the-verification): run its core behavior at least once and record the evidence. Then have a fresh agent on a smaller model run the [acceptance check](references/pull-requests.md#acceptance-check), which reads the diff and that evidence against each acceptance criterion, and run the repository's checks. Never open a pull request first and verify after it. Write a body that carries the [verification record](references/pull-requests.md#verification-record): the checks, each commit's pre-commit review, the acceptance check, any security review, and the acceptance evidence, each with the commit it covers.
2. **Classify.** Label the pull request `review:ai` or `review:human` as soon as it is open. `review:human` is for a change to what a user sees or how they interact with it, which a person always confirms, a pull request that sets up this skill, such as initialization or an issue template update, a change repository guidance reserves for a person, and a pull request from a fork. A person's part is to understand the feature, not to judge technical choices. An open decision, a failed check, a high-risk change, or a change to how the repository works, such as its agent guidance, CI, or pre-commit gate, is not a reason for human review: ask the user the one question, such as whether to accept a change that loosens a rule, or fix the failure.
3. **Merge gate.** For `review:ai`, check the gate on the head commit: the lane still fits, CI is green, every commit has a local review on record, a high-risk change has a local security review on record, every acceptance criterion has evidence and an acceptance check on record, the checks passed on the head, each issue reads as final, and the body closes its issues. The gate only reads the verification record against GitHub and git. Anything the record lacks fails the gate, and the pull request goes back to draft for the author's side. Don't assume branch protection or required checks exist.
4. **Human review.** For `review:human`, write why it needs a person and what they must confirm, then request review. When the reviewer is in the conversation, run a [review interview](references/pull-requests.md#review-interview): teach each point in plain language, then ask a multiple-choice question about it. For an interface change, run the head and open each affected screen for the reviewer before they confirm it. Screenshots don't replace the screen. Merge only after a human approves the current head commit and the gate's other conditions hold, and record that approval in the pull request first.
5. **Merge.** Never require a pull request to contain the base branch's latest commits. Ready pull requests merge in line, one at a time. Only the one at the front brings in the base, and only when it conflicts with it or a reviewer asks, so it resolves its conflicts once, against every merge before it. A merge commit holds only the merge and its conflict resolutions. Re-read the pull request, its reviews, and its CI right before merging, and merge with the head SHA you checked. Squash a pull request that completes one issue, and use a merge commit for one that integrates several.
6. **After the merge.** Verify that the pull request merged, the merge commit changed the same files, each issue closed, and its Status is the completed option. Add the completion comment. Read the base branch's CI on the merge commit when it finishes. If it fails, stop merging and fix forward or revert first.

### Complete and close

1. Re-read the issue, its acceptance criteria, project fields, sub-issues, linked closing pull requests, and relevant comments.
2. Confirm every acceptance criterion with evidence. Record any explicit descoping. A linked pull request is a pointer to evidence, not evidence itself.
3. Update the issue body's durable state so it reads as the final, cold-startable record, then run the cold-start check.
4. Add a completion comment with the outcome, pull request and commit links, validation, and authorized follow-ups.
5. Close the issue with the appropriate state reason. When a pull request closes it, the merge takes this step, as described in [After the merge](references/pull-requests.md#after-the-merge).
6. Re-read the project item. If an automation did not move it to the completed option, update that field and verify again.
7. Check what the completion unblocks. Native dependencies need no update: GitHub stops treating a dependent as blocked once its last prerequisite closes. When you are fanning out, rerun the ready-set query. Update external blocker entries that pointed at this work only when authorized.

Do not rely on an assumed project automation. Closing an issue and setting a project status are distinct until a read proves otherwise.

### Change many items

Large runs, such as creating a work graph or retriaging a board, meet limits that single transitions don't:

- GitHub's secondary rate limits allow about 80 content-creating requests per minute and 500 per hour for each user, counting the web UI and both APIs. Count every issue create or update, comment, label change, project field update, and dependency write. Include what earlier runs spent in the past hour, and pace the run to stay under both limits.
- Split long runs into chunks. Delegate each chunk with the exact commands and one write per message, and have it report what it changed and any anomaly. When a write carries content the agent must read first, such as a prepared issue body, require the read and the write in separate messages. An agent that sends both at once writes text it hasn't seen.
- Verify with compact reads, such as `gh issue list --json` with only the fields you compare, and with Project filters such as `no:priority`. An empty filter result proves nothing until a filter that must match returns items, so run that control first.
- Audit the writes, not only the end state. Compare every write's inputs with the intended values, using the host's record of delegated tool calls when it keeps one. A wrong write that a later write corrected still leaves a revision in the issue's edit history and a cross-reference on every issue it mentioned, and a read-back of the final state shows neither. Report any such write and what it left behind.

### Initialize issues and board

Run this only through the first-use gate, and only after the user authorizes it. Follow [references/initialization.md](references/initialization.md):

1. Diff the repository and Project against the baseline profile. Build the plan in three lists: changes the agent will apply, UI steps for the user, and items left unchanged.
2. Confirm the open decisions: language, Project, area labels, priority mirror, blank issues, triage authority, merge authority, and what a person must review.
3. Create only the missing labels, views, Priority field, and Project-repository link, plus the Project if the user asked for one.
4. Propose the chosen issue templates from [assets/issue-templates/](assets/issue-templates/), together with the recorded conventions, in a pull request. Never push to the default branch, and never merge it yourself.
5. Hand off the manual steps. Status options, option colors and descriptions, workflows, view filters, and issue types need the GitHub UI.
6. Verify every readable result, record user-confirmed items as confirmed rather than verified, and resume the original request from Discover.

### Keep issue templates current

This skill's issue templates are the source of truth for every repository that installed them. Follow [references/issue-templates.md](references/issue-templates.md): when the repository's templates differ from this skill's, finish the current transition, then propose the update in its own pull request. Never push to the default branch, and never merge it yourself.

## Failure handling

- **Missing field or option:** refresh the project fields once. Do not create, rename, or rewrite project configuration during an ordinary work-item operation. Configuration changes belong to an authorized initialization.
- **Authorization error:** report the resource and the required read or write capability without exposing credentials.
- **Ambiguous or stale item ID:** locate the item again by repository and issue number.
- **Pagination:** continue with the returned cursors before concluding that an item, label, field, or project is absent.
- **Partial failure:** report the confirmed completed steps and the exact remaining mutation.
- **Repeated unchanged failure:** stop, and persist the attempted action, the error, and the new evidence or authority required.
- **Secondary rate limit:** stop writing, wait at least as long as the response asks, and resume from a fresh read of the items still pending.
- **Timeout or dropped connection during a write:** the write may have applied anyway. Read before retrying: look for the issue or pull request by title or head branch, or re-read the field. Retry only what is missing, because a blind retry of a create makes a duplicate.
- **Denied by the host's permission system:** treat the denial as a human gate. Don't retry the action through another tool or another agent. Report it and ask the user.
- **A read returns more than the host accepts,** such as a large diff or a parent's sub-issues with full bodies: narrow it with `--jq` to only the fields you compare, a Project query with `--query`, or the diff from a local fetch of the pull request's head.
- **Concurrent edits:** re-read and merge intentionally. Never overwrite newer user content with an older snapshot.
