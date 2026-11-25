---
name: ase-task-list
argument-hint: "[--help|-h] [--verbose|-v] [--include|-i=<state>[,...]] [--exclude|-e=<state>[,...]]"
description: >
    List all available task ids.
    Use when user wants to see all tasks.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-list">
List Task Plans
</purpose>

<expand name="getopt"
    arg1="ase-task-list"
    arg2="--verbose|-v --include|-i=none --exclude|-e=finished">
    $ARGUMENTS
</expand>

<objective>
*List* all available *task plans* of the current project.
</objective>

Procedure
---------

1.  Determine the *effective state set* <states/>, i.e., the lifecycle
    states a task plan has to be in to be listed at all. For this, first
    determine the *all states* set <all-states/> and the *finished
    states* set <finished-states/> of the task lifecycle model
    <ase-project-task-lifecycle/> of the current project:

    -   If <ase-project-task-lifecycle/> is `solo` (or absent):
        <all-states/> is `OPEN`, `SHELVED`, `CLOSED`, and `CANCELLED`,
        and <finished-states/> is `CLOSED` and `CANCELLED`.

    -   If <ase-project-task-lifecycle/> is `team`:
        <all-states/> is `PLANNING`, `SHELVED`, `IMPLEMENTING`,
        `STALLED`, `IMPLEMENTED`, and `CANCELLED`, and
        <finished-states/> is `IMPLEMENTED` and `CANCELLED`.

    -   If <ase-project-task-lifecycle/> is `enterprise`:
        <all-states/> is `DRAFTED`, `SHELVED`, `PLANNING`, `PLANNED`,
        `STALLED`, `IMPLEMENTING`, `IMPLEMENTED`, `DECLINED`,
        `QUALIFYING`, `QUALIFIED`, `DEFERRED`, `INTEGRATING`, `INTEGRATED`,
        and `CANCELLED`, and <finished-states/> is `INTEGRATED` and
        `CANCELLED`.

    Then parse <getopt-option-include/> and <getopt-option-exclude/> as
    comma-separated token lists, silently dropping the `none` sentinel
    and any empty token, and replacing the `finished` sentinel with
    <finished-states/>. If a token <token/> is *not* one of the
    `Status:` values in <all-states/>, only output the following
    <template/> and then *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-task-list**, ▶ ERROR: invalid state: **<token/>**
    </template>

    Otherwise set <states/> to <all-states/> if both lists are
    empty, to the *include* list if only it is non-empty, to <all-states/>
    *minus* the *exclude* list if only it is non-empty, and to the
    *include* list *minus* the *exclude* list if both are non-empty. If
    the resulting <states/> is *empty*, only output the following
    <template/> and then *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-task-list**, ▶ ERROR: options `--include` and `--exclude` cancel out to an empty state set
    </template>

    Directly *after* this error <template/>, and *before* stopping, give
    the corrective hint by expanding the following (which, depending on
    the configured <ase-guidance-level/>, may expand into nothing and
    hence emit no output at all):

    <ase-tpl-hint level="minimal">
    The `--exclude` default `finished` (the finished states of the task lifecycle model) still applies -- add `--exclude none` to reach finished states via `--include`.
    </ase-tpl-hint>

2.  Call the `ase_task_list(verbose: <getopt-option-verbose/>)` tool from
    the `ase` MCP server. The result is a structured object with a
    `tasks` array where each entry has an `id` and a `status` field, and
    -- if <getopt-option-verbose/> is `true` -- additionally an `mtime`
    field (formatted as `YYYY-MM-DD HH:MM`) and an `effort` field (the
    T-shirt size `XS`, `S`, `M`, `L`, or `XL` of the task, empty if not
    estimated). *Drop* from the `tasks`
    array every entry whose `status` is contained in <all-states/> but
    *not* in <states/>. *Keep* every entry whose `status` is *not*
    contained in <all-states/> at all, regardless of <states/>, and
    remember it as an *unknown-status entry*. Do not output anything.

3.  For each *unknown-status entry* of step 2, output the following
    <template/>, where <id/> and <status/> correspond to the entry and
    <all-states/> is rendered as a comma-separated list:

    <template>
    ⧉ **ASE**: ◉ task: **<id/>**, ▶ WARNING: unknown status **<status/>** (expected one of: <all-states/>)
    </template>

    Then, if the `tasks` array is empty, output the following <template/>:

    <template>
    ⧉ **ASE**: ◉ tasks: *(none)*
    </template>

    Else, dispatch on <getopt-option-verbose/>:

    -   If <getopt-option-verbose/> is `true`, output the list of tasks
        with the following <template/>, where each <id/>, <status/>,
        <effort/>, and <mtime/> correspond to an entry in the task list,
        with an empty <effort/> rendered as `-`:

        <template>
        ⧉ **ASE**: ◉ tasks:

        | *Task Id* | *Status*    | *Effort*    | *Last Modified*    |
        |-----------|-------------|-------------|--------------------|
        | **<id/>** | `<status/>` | `<effort/>` | `<mtime/>`         |
        | [...]     | [...]       | [...]       | [...]              |

        </template>

    -   If <getopt-option-verbose/> is `false`, output the list of tasks
        with the following <template/>, where each <id/> corresponds to
        an entry in the task list:

        <template>
        ⧉ **ASE**: ◉ tasks:

        | *Task Id* |
        |-----------|
        | **<id/>** |
        | [...]     |

        </template>

4.  Finally, give the closing hints by expanding the following (which,
    depending on the configured <ase-guidance-level/>, may each expand
    into nothing and hence emit no output at all):

    <if condition="the `tasks` array is NOT empty">
    <ase-tpl-hint level="normal">
    Use `/ase-task-id <id>` to switch to one of the listed tasks and `/ase-task-view` to inspect its plan.
    </ase-tpl-hint>
    </if>
    <elseif condition="entries were dropped by the state filtering of step 2">
    <ase-tpl-hint level="normal">
    All task plans were filtered out by the effective state set -- use `/ase-task-list --exclude none` to list them regardless of their status.
    </ase-tpl-hint>
    </elseif>
    <else>
    <ase-tpl-hint level="normal">
    No task plan exists yet -- use `/ase-task-edit` to create one through a conversational loop.
    </ase-tpl-hint>
    </else>

    <if condition="<getopt-option-verbose/> is not equal `true`">
    <ase-tpl-hint level="verbose">
    Use `/ase-task-list --verbose` to additionally show the status, the effort size, and the last-modified timestamp of each task plan.
    </ase-tpl-hint>
    </if>

    <ase-tpl-hint level="verbose">
    Use `/ase-task-list --include`/`--exclude` to narrow the listing to certain lifecycle states, e.g. `--include IMPLEMENTING,STALLED`.
    </ase-tpl-hint>

