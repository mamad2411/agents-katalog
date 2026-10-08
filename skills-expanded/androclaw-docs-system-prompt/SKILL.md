# System Prompt

AndroClaw uses a modular system prompt architecture inspired by OpenClaw's composable prompt system (AGENTS.md, SOUL.md, TOOLS.md, USER.md).

## Prompt Sections

The system prompt is assembled from 6 sections in order:

### 1. Identity (Always Present)
Core agent name and role. Not user-editable.

> You are AndroClaw, a powerful AI agent running on the user's Android device. You can execute real actions on their phone using the tools provided.

### 2. Persona (Customizable)
Controls the agent's tone, personality, and behavioral boundaries.

**Default:**
> Be concise, helpful, and proactive. When the user asks you to do something, use the appropriate tool right away. Be action-oriented — don't ask for confirmation on safe operations. Only confirm before destructive actions.

Users can customize this in Settings > Persona. Examples:
- "Be brief and casual. Use humor."
- "Always respond formally. Be thorough in explanations."
- "Reply in Spanish when I write in Spanish."

A "Reset to default" button is available if customized.

### 3. Tool Guidance (Always Present)
Detailed instructions for how to use each of the 33 tools. Not user-editable. Includes guidance for:
- Contact resolution for calls/messages
- File operations (find/read/tree/grep/glob)
- Memory types and usage
- Web search vs web fetch
- Alarms vs reminders
- Skill management and slash commands
- Schedule automation
- Screenshot analysis

### 4. User Profile (Optional)
Facts about the user that personalize every conversation. Set in Settings > About You.

Example:
> My name is Alex. I work as a designer in NYC. My partner's name is Sam. I prefer metric units.

### 5. Custom Instructions (Optional)
Standing orders the AI always follows. Set in Settings > Custom Instructions.

Example:
> Always check my calendar before suggesting meeting times. Respond in Spanish when I write in Spanish. Never share my location without asking first.

### 6. Memory Context (Auto-Injected)
Saved memories from the database, grouped by type:

```
About the user (from memory):
- user_name: Alex
- user_role: UX Designer

User preferences:
- communication_style: Brief and casual
- favorite_music: Jazz

Standing instructions (always follow):
- morning_routine: Check weather before calendar

Known facts:
- partner_name: Sam
- home_city: New York
```

## Configuration

| Section | Editable | Storage | Reset |
|---------|----------|---------|-------|
| Identity | No | Hardcoded | N/A |
| Persona | Yes | SharedPreferences | Reset to default button |
| Tool Guidance | No | Hardcoded | N/A |
| User Profile | Yes | SharedPreferences | Clear the field |
| Custom Instructions | Yes | SharedPreferences | Clear the field |
| Memory | Auto | Room database | Delete memories |
