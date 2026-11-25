---
name: call-atlas
description: "Call Atlas subagent directly to execute tasks. Trigger when the user mentions Atlas, asks to send a message to Atlas, or requests Atlas. Triggers: call-atlas, atlas, 呼叫 atlas, 傳送給 atlas, atlas subagent."
---

# Call Atlas

This skill automates the packaging of your message and forwards it directly to the Atlas subagent.

## Instructions

When this skill is loaded, do the following:
1. Extract the core task or message provided by the user.
2. Formulate a call to the `invoke_subagent` tool with the following configurations:
   - **TypeName**: `atlas`
   - **Role**: `Atlas - Master Orchestrator`
   - **Prompt**:
     ```text
     [User's Message]
     ```
3. Do NOT execute any other operations (such as file edits, command execution, or other tool calls) that are not explicitly specified by the Subagent or the User.
4. Execute the `invoke_subagent` tool immediately.
5. If the Subagent asks the user any questions, the main Agent must forward the questions directly to the user and is strictly forbidden from answering them on the user's behalf.
