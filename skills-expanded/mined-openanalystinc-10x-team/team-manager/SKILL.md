---
name: team-manager
description: |
  Manage team members and their platform credentials for multi-user outreach.
  Each team member can have their own authenticated accounts for LinkedIn, Twitter, Instagram, and Gmail.
  Use this skill when the user wants to add team members, configure platform accounts, or check team status.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - TodoWrite
  - AskUserQuestion
---

# Team Manager Skill

Manages team members and their platform credentials for the 100X Outreach System.

## When to Use This Skill

Use this skill when the user:
- Wants to add or remove team members
- Needs to configure platform credentials (LinkedIn, Twitter, Instagram, Gmail)
- Asks about team status or who is set up
- Wants to link browser extension credentials to team members
- Needs to check authentication status

## When NOT to Use This Skill

Do NOT use this skill for:
- Sending outreach → use `outreach-manager` or `workflow-engine`
- Finding people → use `discovery-engine`
- Reading emails → use `inbox-reader`

## Capabilities

1. **Add Team Members** - Add new team members with name, email, timezone
2. **Configure Platforms** - Enable/disable platforms per member
3. **Link Browser Extension** - Connect browser extension credentials
4. **View Status** - Show team overview and auth status
5. **Manage Limits** - Set per-user rate limits

## Commands

### Add a Team Member

```bash
python .claude/scripts/team_manager.py add --name "John Doe" --email "john@example.com" --timezone "America/New_York"
```

### List Team Members

```bash
python .claude/scripts/team_manager.py list
```

### Get Team Status

```bash
python .claude/scripts/team_manager.py status
```

### Configure Platform for Member

```bash
python .claude/scripts/team_manager.py configure --id MEMBER_ID --platform linkedin --enable --handle "@johndoe" --profile-url "linkedin.com/in/johndoe"
```

### Link Browser Extension Credentials

After verifying extension connection, link credentials:

```bash
python .claude/scripts/team_manager.py configure --id MEMBER_ID --platform linkedin --browser-profile "CREDENTIALS_ID"
```

### Set Rate Limits

```bash
python .claude/scripts/team_manager.py configure --id MEMBER_ID --platform linkedin --daily-limit 20 --hourly-limit 5
```

### Remove Team Member

```bash
python .claude/scripts/team_manager.py remove --id MEMBER_ID
```

## Browser Extension Integration

To authenticate a team member's platform account:

1. **Check Extension Status:**
   Use `curl http://localhost:3000/api/extension/status` to verify extension is connected.

2. **Verify Authentication:**
   Team member should be logged into platforms (LinkedIn, Twitter, Instagram) in their browser.
   The extension uses the authenticated browser session automatically.

3. **Link Credentials:**
   ```bash
   python .claude/scripts/team_manager.py configure --id MEMBER_ID --platform linkedin --browser-profile "UUID"
   ```

4. **Verify Authentication:**
   ```bash
   python .claude/scripts/team_manager.py get --id MEMBER_ID
   ```

## Workflow: Setting Up a New Team Member

1. **Create the member:**
   ```
   Add team member "Sarah" with email sarah@company.com
   ```

2. **Configure platforms:**
   ```
   Enable LinkedIn for Sarah with handle @sarahsmith
   Enable Twitter for Sarah with handle @sarah_tweets
   ```

3. **Link authenticated browser profiles:**
   - List browser profiles
   - User selects which profile is Sarah's LinkedIn
   - Link the profile UUID to Sarah's LinkedIn

4. **Set rate limits if needed:**
   ```
   Set Sarah's LinkedIn daily limit to 25 connections
   ```

5. **Verify setup:**
   ```
   Show Sarah's configuration
   ```

## Data Storage

Team data is stored in:
- `credentials/team.json` - Team configuration
- `credentials/profiles/{member_id}/` - Per-member credential files

## Security Notes

- Browser profile IDs are stored but not exported
- Rate limit state is tracked per-user in `credentials/rate_limits_state.json`
- All credentials remain local, never transmitted

## Example Conversations

**User:** "Add my colleague Mike to the team"
**Assistant:**
1. Ask for Mike's email and timezone
2. Run: `team_manager.py add --name "Mike" --email "..." --timezone "..."`
3. Show Mike's profile
4. Ask which platforms to enable

**User:** "Set up Mike's LinkedIn"
**Assistant:**
1. Ask for LinkedIn profile URL/handle
2. Run: `team_manager.py configure --id MIKE_ID --platform linkedin --enable --handle "@mike"`
3. List browser profiles
4. Ask user to identify Mike's LinkedIn browser profile
5. Link the browser profile
6. Confirm setup complete
