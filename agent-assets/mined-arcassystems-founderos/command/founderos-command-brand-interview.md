---
description: Set up your brand profile. Say "set up my brand profile" (or run /founder-os:brand-interview). Captures your visual identity (colors, fonts, logo) into core/brand-profile.yml. Activates branded outputs (your-deliverable-template, branded proposals, branded client updates). Takes about 10 minutes.
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# Founder OS brand interview

Entry point for the brand interview. Triggers the `brand-interview` skill, which captures the user's visual brand and writes it to `core/brand-profile.yml`.

## Procedure (in order)

1. Check whether `core/identity.md` exists at the repo root.

2. If `core/identity.md` does NOT exist, reply: `Founder OS not set up here yet. Say "set up Founder OS" first.` and stop. The brand interview depends on identity being filled.

3. Check whether `core/brand-profile.yml` exists.

   - If it does NOT exist, copy the template from `templates/brand-profile.yml.template` to `core/brand-profile.yml` (placeholders intact) before invoking the skill, so the skill can fill it in place.
   - If it exists and contains real values (not `[CHOOSE: ...]`, `[YOUR ...]`, `[#XXXXXX]`, or `[NOT SET]` on every required field), ask the founder, as a single message:

     ```
     Brand profile already filled. Re-run the interview and overwrite? (yes / no)
     ```

     Wait for the reply. If the reply is a clear `no`, reply: `Brand interview dismissed. Existing profile left untouched.` and stop. If the reply is a clear `yes`, proceed.

4. Read the brand-interview skill at `skills/brand-interview/SKILL.md` and execute it end to end. The skill owns the interview flow: welcome and detect starting point, three branches (have-kit / partial / fresh-start), confirmation, write. Follow its phases IN ORDER. Do not shortcut.

## Rules

- This command is a thin trigger. All logic lives in the skill. Do not duplicate interview steps here.
- If the skill file is missing, reply: `Brand interview skill not found at skills/brand-interview/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
- No em dashes or en dashes. Hyphens only with spaces.
- Never overwrite an existing populated profile without the explicit re-run confirmation above.
