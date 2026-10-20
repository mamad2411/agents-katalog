# Portfolio Maintenance Command

Launch the Portfolio Agent to safely update portfolio website content.

**Usage:** `/portfolio <action> [details]`

**Examples:**
- `/portfolio add-project "GridCOP in production"`
- `/portfolio update-skills "Add CrewAI and MCP"`
- `/portfolio review "Check consistency with resume"`

**What the agent does:**
- Proposes changes (shows diff before writing)
- Waits for your approval (safety checkpoint)
- Updates JSON files only (never touches HTML/CSS/JS)
- Verifies consistency with resume
- Confirms success after changes applied

**Safety:**
- READ-ONLY by default (proposes before writing)
- Explicit approval required for modifications
- Never touches production HTML/CSS/JS files
- Only modifies JSON files in `data/` directory

**Implementation:**
Use Task tool with subagent_type="general-purpose" and load the complete agent definition from `.claude/agents/portfolio-agent.md`.

Pass the portfolio action request to the agent.
