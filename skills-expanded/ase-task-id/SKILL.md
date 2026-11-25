---
name: ase-task-id
argument-hint: "[--help|-h] [<id>]"
description: >
    Get or set unique task id <id>.
    Use when user requests to work on a certain task
    or wants to know what the current task is.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-id">
Configure Task Id
</purpose>

<expand name="getopt" arg1="ase-task-id">
    $ARGUMENTS
</expand>

<objective>
*Get* or *set* the unique *task id* of the current session.
</objective>

Procedure
---------

1.  Determine request:
    <request><getopt-arguments/></request>
    Inherit the always existing <ase-session-id/> and the current
    <ase-task-id/> from the current context.

2.  <if condition="<request/> is NOT empty AND <request/> does NOT match the regexp `^[a-zA-Z0-9#][a-zA-Z0-9#_-]*$`">
    Only output the following <template/> and then immediately
    *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ☻ skill: **ase-task-id**, ▶ ERROR: given task id `<request/>` is not a valid id
    </template>
    </if>

3.  <if condition="<request/> is empty">
    -   Call the `ase_task_id(session: "<ase-session-id/>")`
        tool from the `ase` MCP server and set <text/> to its
        `text` output. Only on a clean response set
        <ase-task-id><text/></ase-task-id>. On an `ERROR:`/`WARNING:`
        response, silently ignore the MCP error (deviating from the
        generic MCP error rule) and keep the <ase-task-id/>
        inherited from the current context as the fallback.

    -   Output:
        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**
        </template>
    </if>

4.  <if condition="<request/> is NOT empty">
    -   Call the `ase_task_id(id: "<request/>", session: "<ase-session-id/>")`
        tool from the `ase` MCP server and set <text/> to its `text`
        output. On an `ERROR:`/`WARNING:` response, silently ignore the
        MCP error (deviating from the generic MCP error rule), keep the
        <ase-task-id/> inherited from the current context, and only
        output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-id**, ▶ ERROR: failed to switch to task `<request/>`
        </template>

    -   Only on a clean response set <ase-task-id><request/></ase-task-id>.

    -   Output:
        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>** (*updated*)
        </template>

    -   If <text/> carries a line `NOTICE: <info/>` (the id does not
        conform to the task id scheme of the project), additionally
        output:
        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ NOTICE: <info/>
        </template>
    </if>

