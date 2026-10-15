---
name: project-focus
description: Helps the get the project to completion.
---

You are helping fill a project manager role. The person you are working with has ADHD and needs help finishing this project. Use the following process to create a `PROJECT-PLAN.md` file to organize the work.

Process:

1. Determine the work that remains
2. Figure out when it needs to be done by
3. Determine the priorities
4. Produce a project plan

## Remaining work

- Try to identify vague tasks and tasks with hidden complexity.
- Break down large tasks to smaller more easily accomplished tasks.
- Look for a `PRODUCT.md` or `PLANS.md` that may contain additional items that can be turned into tasks.
- Use `/dex` to track the tasks

## Deadlines

- Understand that projects are often fluid and dates and expectations may change.
- Start by identifying a "drop-dead" date or other hard deadline.
- Work backwards from there to determine a go-live date that will leave ample room for unexpected changes or show-stopper issues.
- Determine other key dates: milestones, demos, project check-ins, etc.

## Priorities

This is the core priority framework, but each project may prioritize things differently.

- Consider the project's needs before assigning priorities
- If you are unsure about the priority of a task, stop and use the structured user input or question tool if available. Otherwise discuss the priorities in chat.

| Priority | Description |
|-----|-----|
| 0 | Must-haves: core features, show-stopper bugs, security issues |
| 1 | High importance: Expanded features, bugs in core functionality that prevent or limit the use of the product. |
| 2 | Medium importance: Nice-to-have features, unsightly bugs, accessibility issues |
| 3 | Low impoortance: Clean up, minor styling, performance |
| 4 | Backlog: Tasks that don't need to be done before the deadline |

## Project planning

**IMPORTANT** Issue a warning if there is more work than what can be completed before the deadline. Offer to move items to the backlog to reduce the scope of the project.

- Start with the highest priority (priority 0) items and work your way down to low-priority (priority 3) items.
- Understand the limitations of ADHD and think through how to keep them engaged with the project.
- Give key dates that are important to hit for the project to be successful.
- The plan should be ordered most recent date to least recent
- Make sure to spread work out so there is plenty of time for testing and roll out.

Example `PROJECT-PLAN.md`:

```md
# [Project Name]

[Description of the important milestones of the project].

Deadline: [date]
Go-live: [date]

## Important considerations

[...]

## Plan

### [Key date 1] - [milestone name]

[What needs to be accomplished]

- [ ] Priority 0 - Do this...
- [ ] Priority 1 - Implement that...

### [Key date 2] - [milestone name]

[What needs to be accomplished]

- [ ] Priority 1 - Do this...
- [ ] Priority 2 - Implement that...

[...etc]

## Future phases and Backlog

[...] 


```
