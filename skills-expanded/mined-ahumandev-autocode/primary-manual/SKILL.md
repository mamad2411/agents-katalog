---
name: primary-manual
description: DANGEROUS OPERATIONS are following: risk of corrupting user system (sudo commands, os config changes, changing critical non-project related files), leaking sensitive system/client info (passwords/secrets), introducing security vulnerabilities to user system, change production app behavior (deployments, altering production db), killing processes not related to project, expensive cloud operations. Use primary-manual when DANGEROUS OPERATION is blocking your solution and user must manually perform it.
---

For DANGEROUS OPERATIONS (user responsible):

1. Gather the necessary info — exact steps user must follow, and exact commands/configs/inputs/actions user must execute. Missing info? Use \`subagent\` to collect.
2. Present Tutorial guidance to user.
3. Only after presenting Tutorial in text, append instruction for user to reply when done.
4. React to user reply:
	- **Resume requested**: assume the task is complete and proceed with the Typical Workflow.
	- **Alternative solution requested**: treat the current task as a blocker. Then:
		- If an alternative is hinted: clarify first if conflicting/unclear, use it to resolve manual task.
		- If no alternative is specified: find your own workaround meeting current REQUIREMENT within the CONSTRAINTS and confirm with user.
	- **Permission granted to complete the manual task**:
        1. You may perform ONLY that specific DANGEROUS OPERATION on the user's behalf
        2. Next DANGEROUS OPERATION reverts to user.
5. Resume with workflow when unblocked.

---

## Tutorial Rules

* Written in Concise English.
* Steps must be placed in correct sequential order.
* Where user can decide on different workflow paths, format each workflow as different subsection (explain difference).
* Wrap article/text editing changes in md blocks.
* When quoting text/code: Provide source with inline md link with line number.
* Always include exact commands, paths, line numbers, code/config changes.
* Always motivate why in Concise English.
* Warn about common pitfalls.
* Emojis highlight important info and start of step.
* Tutorial must lead reader to goal.
* Only practical steps.
* Each formatted step provide example command/config/user action and response/output (if known).
* Do not overwhelm user, instead systematically:
	1. Guide user through most urgent task only.
	2. Repeat with next manual task until all blocking manual tasks are done.
* When user need to copy content, wrap it in md code blocks.
