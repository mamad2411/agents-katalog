---
name: alpacawork
description: Read before operating alpacawork, a tool for handing tasks to AI agents and managing their progress and the acceptance of results. Use it when asking for a task, checking status, or answering a question or accepting a result in alpacawork; when installing, updating, configuring or repairing alpacawork; and when you receive a request that begins with "[alpacawork] Request for task T…".
---

# alpacawork

alpacawork records a tree of tasks and the owner and members of each task, and launches the agent that receives a request.

## Open the skills for your next action

Before your next action, select the matching rows. For each row, start with the skill specified by project policy for that purpose. When policy leaves the choice open, use the matching skill from your available skills list. Call the agent's skill tool or read the skill's `SKILL.md` before proceeding.

When you are the owner of a new request for a result, load the planning and reporting skills at the start: you will plan a result and give a progress estimate even for a small change. A request to offer the user choices is a decision about what to ask. Use the decision and question skills before preparing the choices.

- **Plan a result or prepare its review:** load the available skill for planning and independent review.
- **Decide what to ask the user or make a consequential choice:** load the available skill for deciding which judgments belong to the user.
- **Draft a question or report for the user, including a progress estimate:** load the available skill for writing questions and reports.

Apply this check again when another row becomes relevant. Reuse a skill already read in this conversation. If policy excludes the skill or the chosen skill is unavailable, continue using alpacawork and the request.

## Decide your role

If you were launched through the conversation's own subagent call (such as `spawn_agent`) as the delegate for a one-off job, do the actual work within the scope the caller stated explicitly, and return the result and what you verified to the caller. Do not decide from the presence or absence of the Run mark (`ALPACAWORK_RUN`) to act as a coordinator or an owner; hand task state changes, questions and agent placements back to the caller. This is a distinction in how work is divided; it grants no CLI or API permissions.

Otherwise, if you have the Run mark, read the file for the role that alpacawork's launch prompt names: [references/owner.md](references/owner.md) for an owner, [references/member.md](references/member.md) for a member. If you have no mark, you are the coordinator; read [references/coordinator.md](references/coordinator.md). Do not infer your role from the wording of the request text; decide it from the Run mark and the launch prompt.

| Name on the screen | CLI value | What it does |
|---|---|---|
| Coordinator | — | The user's point of contact. Is launched in a conversation on the screen (alpacawork's UI), or uses the CLI from an outside conversation (Claude Code, Codex and others). Does short lookups itself and hands long work to agents. Assigns an owner to a top task and requests the work, and writes acceptances, answers and holds by quoting the user's words. Is not woken automatically |
| Owner | `responsible` | Is responsible for the result of one task. Is launched by alpacawork. Chooses whether to do the work itself, assign members, or split the task into child tasks, and reports with `task report --state done` when finished |
| Member | `member` | Is assigned by an owner to the owner's own task. Works on the owner's instructions and returns the result to the owner in its final reply. Does not change states and does not ask questions |

Besides the file for your role, read the following according to the situation.

| Reader | Situation | What to read |
|---|---|---|
| Coordinator and owner | Before creating a task or sending a request or an answer | [Tasks and requests: the common procedure](references/request.md) |
| Coordinator and owner | When woken; when asking or answering a question; when reporting the end or accepting; when handling a hold or a failure; when stopping a Run or stopping a task | The relevant section of [Delivery and completion](references/lifecycle.md) |
| Coordinator | When installing or updating alpacawork itself, or connecting from another device or conversation; when preparing a project for the first time | [Setup](references/setup.md) |
| Owner | When given the job of updating alpacawork itself | ["Update" in Setup](references/setup.md#update) |
| Coordinator | When changing the configuration or the AI to use | [Configuration](references/config.md) |
| Coordinator | When a task does not move, the server does not start, or an update stopped | [Troubleshooting](references/troubleshoot.md) |

## Terms and relationships

- In this skill, "parent" means the owner of the parent task, and "child" means a child task. A member is not a child. For a top task (a task directly under a project), the coordinator or a person holds the parent's role (assigning an owner, handing over to another, releasing one, requesting work, and stopping Runs).
- When this skill says only "accept" or "acceptance", it means that the user accepts a result that is awaiting review.
- The requester is the user for a top task the user asked for, and the parent for a child. Even for a child, the requester is the user while a request the user made directly to that child is still open. The requester is where returns, urgent notes and failures go, and the server decides who it is. The recipient of a question is separate from the requester: it is fixed by the explicit choice made when the question is asked.
- Instructions to a member (`member`) placed on a task in alpacawork always go through the owner, so that exactly one party receives the member's result and the member does not get conflicting instructions. This is separate from the conversation's own subagent call; a one-off delegation from the coordinator follows [the coordinator's procedure](references/coordinator.md#delegating-a-one-off-job).

## Commands

- Operate alpacawork with commands. `alpacawork -h` shows how to use them. Before running a command, read "Access" (who may run it) and the argument rules in `alpacawork <group> <verb> -h`. In Access, check the role, the relationship to the target task, and the conditions on the options you use. Access states who may run the command; whether the user's approval is needed follows "Approval defaults" below. If a command is refused, read the reason and go back to what this skill prescribes. The table below maps what you do to the command (each command's `-h` has the description).

| What you do | Command |
|---|---|
| Create a task | `task new` |
| Read a task | `task get` |
| Change a title or field values | `task update` |
| See the tree or search for tasks | `task list` |
| Set or clear dependencies (tasks that must finish first) | `dependency set --task X --after Y,Z`, `dependency clear --task X` |
| Move a task | `task move` |
| Request work or answer | `task request` |
| Report a state, ask a question, accept, stop a task, or put a task on hold | `task report` |
| Record (including urgent notes) | `task comment` |
| Read the returns and notices that arrived | `task returns` |
| Assign, hand over or release an agent | `agent assign`, `agent handover`, `agent release` |
| Read a Run's result or stop a Run | `run get`, `run stop` |
| Read or change personal settings (such as the language for the user) | `settings get`, `settings set` |
| Read the fields a task writes (ID, maximum length, how to write) before writing values | `field get` |
| Read, create, change or delete field definitions; choose the fields a project uses | `field list`, `field set`, `field delete`, `field use` |

## Projects and fields

- A project is a task of kind project (with a P number), and projects can be nested. A task's parent is either a task in the same project or that project itself. An agent (a Run) reads and writes only inside the project it belongs to.
- In this skill, "field" is the CLI's field, "value" is its content, and "snapshot" is the whole set of a task's values at one point in time.

## When you start or resume

- The launch prompt of a new conversation contains the top task's "User instructions" (background; your scope is the part the request gives you), the full text of the request that arrived, the snapshot of your own task, the snapshot of the parent if the parent is a task, the project's policy chain, and a list of read commands (one-line commands that read records, such as `alpacawork task get …`). An owner also gets open work (open requests and returns not yet handled), carried-over items (things that arrived earlier and are not yet handled), and estimate examples.
- The launch prompt of a continued conversation does not contain the parent's snapshot or the list of read commands, and it carries the policy chain and "User instructions" only when they have changed. Large parts are shortened to read commands. Do not take a part that is missing from the prompt to mean "there is none" or "nothing changed"; read it with `task get`.
- The snapshot is the task record as of the moment the server accepted the request, before the agent has applied what this request means. In a new conversation, check it against the original request and the goal currently in effect, then update your judgment to reflect the new instruction.
- Read the latest values and questions with `task get` when you start, when you resume, when you replace another agent, before you rewrite values, and after the conversation has been compacted. The alpacawork record, not your memory of the conversation, is the source of truth.

## Reading and writing

- Always fetch alpacawork records (values, log, Run results, reports) with alpacawork commands. Do not build paths and read directly under the workspace's `.alpacawork/` (the database or the Run folders), because you would get the location or the shape of the contents wrong.
- A read result is partial when it contains `errors`, or when it has omissions (`omitted`) or is cut off at a limit. Do not read missing information (for example an empty list of Runs) as "none" or "not running"; treat it as unverified.
- The Run list of `task get --runs <count>` is `runs` at the top level of the response, not `task.runs`. The count you give covers only the latest Runs of that task itself, so also check the tasks below it and any read errors.
- Other conversations can also read the latest version and write. With a write, pass the hash you read (and the revision when required). It is the mark that you "read the latest and decided on it". If the write is refused for a conflict (`conflict`), read again and decide again. Do not just attach a new hash without reading again.

## When a save is uncertain

- When you do not know the result of a save, check it with the ID and the check command in the failure's `error.detail.operation`. Even when you have to resend, use the same Run, the same ID and the same original input (text, hash, file bytes, credentials). Do not swap in the latest hash or text, and do not blindly retry with a new ID. A committed result from `operation get` does not by itself tell you whether the original input matched.
- For a creation or another write that you may need to check later, specify `--op-id` from the start. When you do not know the ID, look in the task, the tree, History, files and config for whether the intended result exists; if that is unclear, report that the save is uncertain.

## Recording work

- History is where the user follows the course of the work afterwards. Record only milestones: a result became usable (it was merged into main, or a sample is ready); a decision is needed or was made; the direction or the estimate changed substantially; a problem occurred; an action with outside effects was taken (a push, a production swap and the like). Do not record what is only a step along the way (running tests, reading something back, tidying up, asking for a review). At a milestone that makes an earlier record out of date, whoever caused it writes the new record.
- Make each record a short title and a few lines of description. Write, in words the user would use, what changed, how it was verified and what remains, and point to the versions and grounds needed for a decision by saying how to get them. Do not list SHAs, Run numbers or counts, and do not narrate the steps you took to verify.
- A member's result stays in the Run as its final reply (`run get`), and History shows it under the Request that asked for it, so do not copy it into a record. A member records only changes that cannot wait for the owner's reply (a merge into main, an action with outside effects, an incident that may lose data); the owner sums up the rest at milestones.
- Record a milestone that changes the state in the title and description of `task report --state`. Record a milestone that does not change the state (a push after a merge, a production swap and the like) with `task comment` (who may write, and on which tasks, is in Access in `task comment -h`). A record wakes no one. Only a record that the task's owner marks `--urgent` wakes the parent at once, and only when the requester is the parent (when the requester is the user, it is refused).

## Checking a result against the request

- Before treating a result as acceptable, asking a question or submitting, check the user's original words and what was agreed afterwards against the task's values, the Run results (`run get`), the report for each condition and "Running processes", and verify that the outcome the user wanted has come about in the original situation. Do not count having found part of the cause, or the build approach having worked, as meeting the requirement, and do not turn a shortfall into a question of whether to adopt some other result. Distinguish the result statuses (`present`, `pending`, `missing`, `too_large`, `unreadable`), and do not treat something that is not there as an empty result. Check that nothing temporary remains, and that anything permanent is what was intended as a result.
- For each done condition, separate met, not met and unchecked. Present deliverables and evidence separately. Do not report an unchecked condition as met.

## Guardrails

- Do not operate alpacawork with the Run mark (environment variables such as `ALPACAWORK_RUN`) removed or rewritten. alpacawork decides who performed an operation from this mark. Remove it for a test only when pointing at a test workspace.
- Do not reopen, in the desktop app or the agent's CLI, a conversation that alpacawork manages.
- When the user asks you to open the screen, run `alpacawork open`. It opens the screen in this PC's browser for the user, or prints the URL and what to do where no browser can be opened; tell the user the URL, and the printed instruction when there is one.
- When the user asks you to stop, start or restart alpacawork on this PC, run `alpacawork stop`, `alpacawork start` or `alpacawork restart`. Inside a Run (the screen's coordinator included) they are refused; there, tell the user to type the command in a terminal or to ask Claude Code or Codex opened outside alpacawork.
- When you open the alpacawork screen yourself to check something, add `?agent=1` to the URL. Without it, the task you open is marked as read for the person, who then misses what is new.
- Do not put files, worktrees or temporary files in the workspace root. The root is where alpacawork keeps its records, and it is also the launch directory of a Run started without `--cwd` in a project that has no code location. A relative path resolves against the Run's launch directory, so use an absolute path in your work location for writes.
- Before you return, stop anything long-running that you started temporarily for the work (a server for checking or showing something, a watcher, a check running in the background, a temporary environment and the like), using the PID you recorded yourself. You do not wake by yourself after returning, so if you leave it, no one stops it. Finding it by name and stopping it catches other Runs as well.
- When you start something temporary, decide when it ends and start it in a form that stops by itself at that time, so that it does not remain even if you forget to stop it.
- Stop temporary things even when you want to keep them to show a person or to use later. Write the steps to start them again (command and location) in a file in the task folder and link to it from the deliverables. For a sample to show the user, ask that task's owner with `task request` to start it with a set end time, and to stop it once the user has finished looking (the coordinator does not start one).
- Do not stop permanent things that keep running as the task's result (when the job is to start a production server or an always-on service). Distinguish them from temporary things and state, as a deliverable, what is running, where, and how to stop it: the owner writes this in the "Running processes" field (or, if the task has no such field, in the "Notes" field), and a member writes it in its final reply and returns it to the owner.
- If you are an owner or a member, do not end your reply while something that takes time (tests, a build and the like) is still running in the background. Ending the reply ends the Run, and you do not wake by yourself. Wait until it finishes, then return.

## Policy

- Write preferences that differ from user to user (the scope of delegation, the skills for each purpose, the scope of approval and the like) in the project policy. Do not use memory as the place for settings. The request text defines the scope of its task.
- Owners and members get the project policy in their launch prompt as the policy chain; the coordinator reads it with `task get --task <project>` (["Authority" in Coordinator](references/coordinator.md#authority)). The only things the coordinator may quote on the user's behalf are the user's current message and this chain (["Relaying the user's words" in Coordinator](references/coordinator.md#relaying-the-users-words)). When projects conflict, the ancestor project's policy wins.
- When instructions conflict, follow the user's own words first, then the project policy, then instruction files such as AGENTS.md, then the instructions of the AI that asked you for the work, then alpacawork's defaults. An instruction applies only to what it addresses.
- In a launch prompt, the user's own words are under "User instructions" (the whole job; the request says which part is yours), the policy is under "Project policy" (each project's summary, the one sentence on what it is for, comes first under its name), and the first line of "Request" says who wrote it. The user's words quoted in an AI's instructions count as the user's words.
- For how project policy selects skills and what to do with an empty policy, see [Open the skills for your next action](#open-the-skills-for-your-next-action).

## Approval defaults

For the scope of approval, every role (including the coordinator for its own operations) follows what the user's own words, the project policy or an instruction file such as AGENTS.md specifies for the operation; an AI's instruction can narrow it but not widen it. Where none of them specifies it, get the user's approval for actions with outside effects, for weakening done conditions, and for deletion. The agent decides everything else within the scope of the request text. The only approval of completion is the user accepting a user-requested task that is awaiting review; a task an agent created is done when its owner reports `done`. The rules in "Guardrails" that follow from how alpacawork works, and the roles and permissions the CLI requires for an operation, cannot be changed.
