---
name: device-session-management
description: Manage sessions across devices. Use when handling login sessions on
  multiple devices.
metadata:
  tags: device, session, management
---

# Device Session Management

## Use this skill when
- Listing and revoking devices
- Handling password changes across devices
- Session invalidation on compromise

## Do not use this skill when
- Session storage primitives (use session-management)

## Instructions
1. Track sessions with device metadata: id, agent, created, last seen.
2. Let users view and revoke their own devices.
3. Invalidate all sessions on password change and on suspected compromise.
4. Alert on new-device logins where appropriate.
5. Store session records server-side for revocation.
6. Handle logout-all and force logout remotely.

## Checklist
- Password change kills old sessions
- Revoke-one and revoke-all work
- New-device detection exists

## Output Format
- Device model | revocation endpoints | notification strategy

## Common Mistakes
- No way to revoke a stolen device
- Password change leaving sessions alive
- No metadata on sessions
