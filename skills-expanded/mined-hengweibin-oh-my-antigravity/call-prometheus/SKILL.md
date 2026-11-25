---
name: call-prometheus
description: "Call Prometheus subagent directly to execute tasks. Trigger when the user mentions Prometheus, asks to send a message to Prometheus, or requests Prometheus. Triggers: call-prometheus, prometheus, 呼叫 prometheus, 傳送給 prometheus, prometheus subagent."
---

# Call Prometheus

This skill automates the packaging of your message and forwards it directly to the Prometheus subagent.

## Instructions

When this skill is loaded, do the following:
1. Extract the core task or message provided by the user.
2. Formulate a call to the `invoke_subagent` tool with the following configurations:
   - **TypeName**: `prometheus`
   - **Role**: `Prometheus - Planner`
   - **Prompt**:
     ```text
     [User's Message]
     ```
3. Do NOT execute any other operations (such as file edits, command execution, or other tool calls) that are not explicitly specified by the Subagent or the User.
4. Execute the `invoke_subagent` tool immediately.
5. If the Subagent asks the user any questions, the main Agent must forward the questions directly to the user and is strictly forbidden from answering them on the user's behalf.
6. When the Prometheus Subagent is ready and returns a Plan (e.g., a path to a markdown plan), the main Agent must NOT perform redundant validation, exploration, or regenerate any implementation plans on top of it. Simply report the path of the Plan directly to the user.
