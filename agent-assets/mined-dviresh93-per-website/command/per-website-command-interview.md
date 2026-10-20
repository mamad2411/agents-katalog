# Interview Coaching Command

Launch the Interview Coach Agent for company-specific interview preparation.

**Usage:** `/interview <company-name> [practice-type]`

**Examples:**
- `/interview casium live-coding`
- `/interview amazon system-design`
- `/interview google behavioral`

**What the agent does:**
- Discovers existing company prep materials OR creates new structure
- Loads company-specific context automatically
- Provides teaching mode (default) or mock interview mode
- Saves practice session notes for future reference
- Maintains progress across multiple sessions

**Company Context:**
- If company folder exists → loads context and continues
- If new company → creates folder structure, gathers context, stores for future

**Implementation:**
Use Task tool with subagent_type="general-purpose" and load the complete agent definition from `.claude/agents/interview-coach-agent.md`.

Pass company name and practice type to the agent.

Agent will discover existing context or create new company folder as needed.
