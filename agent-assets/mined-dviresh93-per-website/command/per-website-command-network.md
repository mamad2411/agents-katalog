# Networking & Communication Command

Launch the Networking Agent to draft human-sounding messages.

**Usage:** `/network <type> [details]`

**Examples:**
- `/network connection "Hiring manager at Amazon"`
- `/network follow-up "After applying 5 days ago"`
- `/network thank-you "After phone screen with Sarah"`

**What the agent does:**
- Drafts 2-3 message variations (casual, professional, brief)
- Uses networking templates and your background
- Keeps messages short and human-sounding
- Iterates based on your feedback

**Implementation:**
Use Task tool with subagent_type="general-purpose" and load the complete agent definition from `.claude/agents/network-agent.md`.

Pass the networking request context (type and details) to the agent.
