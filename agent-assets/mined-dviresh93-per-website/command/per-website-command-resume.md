# Resume Generation Command

Launch the Resume Generation Agent to handle complete job application workflow.

**Usage:** `/resume [paste job description]`

**What the agent does:**
- Analyzes job requirements and assesses your fit
- Generates customized resume scratchpad for review
- Waits for your approval (human-in-the-loop checkpoint)
- Generates professional PDF after approval
- Provides application strategy and next steps

**Implementation:**
Use Task tool with subagent_type="general-purpose" and load the complete agent definition from `.claude/agents/resume-agent.md`.

Pass the user's job description to the agent.
