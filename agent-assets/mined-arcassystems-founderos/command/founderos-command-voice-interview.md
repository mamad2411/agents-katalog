---
description: Set up your voice profile. Say "set up my voice profile" (or run /founder-os:voice-interview). Captures how you write into core/voice-profile.yml. Activates the voice-coupled writing skills (linkedin-post, client-update, proposal-writer, email-drafter, content-repurposer, sop-writer, your-voice). Takes about 10 minutes.
allowed-tools: ["Read", "Write", "Edit"]
---

# Founder OS voice interview

Entry point for the voice interview. Triggers the `voice-interview` skill, which captures the user's writing voice and writes it to `core/voice-profile.yml`.

## Procedure (in order)

1. Check whether `core/identity.md` exists at the repo root.

2. If `core/identity.md` does NOT exist, reply: `Founder OS not set up here yet. Say "set up Founder OS" first.` and stop. The voice interview depends on identity being filled.

3. Check whether `core/voice-profile.yml` exists.

   - If it does NOT exist, copy the template from `templates/voice-profile.yml.template` to `core/voice-profile.yml` (placeholders intact) before invoking the skill, so the skill can fill it in place.
   - If it exists, scan its content for placeholder markers: `[CHOOSE:`, `[YOUR `, `[example:`, `[NOT SET]`. If ALL voice fields still contain these markers (no field has been replaced with a real value), the profile is placeholder-only - proceed directly into the interview without asking for confirmation.
   - If at least one field has been filled with a real value (no longer a placeholder), ask the founder, as a single message:

     ```
     Voice profile already filled. Re-run the interview and overwrite? (yes / no)
     ```

     Wait for the reply. If the reply is a clear `no`, reply: `Voice interview dismissed. Existing profile left untouched.` and stop. If the reply is a clear `yes`, proceed.

4. Read the voice-interview skill at `skills/voice-interview/SKILL.md` and execute it end to end. The skill owns the interview flow: welcome, samples, shaping questions, confirmation, write. Follow its phases IN ORDER. Do not shortcut.

## Rules

- This command is a thin trigger. All logic lives in the skill. Do not duplicate interview steps here.
- If the skill file is missing, reply: `Voice interview skill not found at skills/voice-interview/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
- No em dashes or en dashes. Hyphens only with spaces.
- Never overwrite an existing populated profile without the explicit re-run confirmation above.
