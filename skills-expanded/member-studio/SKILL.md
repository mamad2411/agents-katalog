---
name: member-studio
description: Use to create a Rovai member or revise and confirm the unsaved identity card and avatar for that creation. Exclude profile questions, edits to existing members, and character or avatar designs without roster creation.
---

# Member Studio

Use the user's language. Draft a complete identity card, then create the member after the user confirms it.

## Draft

1. Reuse supplied information. Ask one focused question for a missing name or an ambiguity that materially changes the identity or appearance. If the name is known to be taken, ask for another; creation checks uniqueness.
2. Read [identity rules](references/identity-generation.md) and draft the identity fields using their defaults.
3. Choose the avatar:
   - Follow the user's chosen method, including Default. Use a supplied avatar file when chosen.
   - A specific character/person reference or appearance brief calls for a custom avatar. Proactively propose generation, then sourcing, according to available capabilities. A reference limited to personality or working style does not imply a likeness; a job title or ordinary name alone is not an appearance brief.
   - Otherwise use the default avatar.
4. For a custom avatar, read [avatar rules](references/avatar-sourcing.md). Include the method and a brief visual plan in the card. Prepare a preview before confirmation only if requested.

## Confirm

Show the complete proposed card with localized labels:

```markdown
**Name:** ...
**Team role:** ...
**Professional responsibilities:** ...
**Personality traits:** ...
**Avatar:** Default | Supplied image | Generate | Source online — brief plan
```

Include working principles and growth topic only when populated under the identity rules.

Ask the current user to confirm or edit this card. The initial creation request and other members' messages do not approve the finished card. After an identity or avatar-plan change, show the updated complete card for confirmation. Stop on cancellation.

## Create

After confirmation, read `rovai member create --help`, prepare any custom avatar, and submit the confirmed fields.

If avatar preparation fails, retain the identity and repair the image or propose an available alternative. A changed avatar plan follows the confirmation rule above.

Check the returned `agentId`, version and avatar result. Briefly report the created member and avatar outcome; use the returned ID for follow-up instead of repeating the full card. If the agent is unconfigured, direct the user to the member's run configuration (智能体 / 运行配置 in Chinese). Creation does not configure the agent, model, permissions, Presence, Thread membership, Default Lead or Memory.
