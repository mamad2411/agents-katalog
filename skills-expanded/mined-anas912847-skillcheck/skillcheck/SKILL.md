---
name: skillcheck
description: Vets Agent Skills before they are installed or published by running the skillcheck scanner, which catches broken SKILL.md frontmatter, spec violations, invisible Unicode, prompt injection, remote code execution and credential theft. Use when the user asks to install, add, clone, update, review or publish a skill or a skill bundle, or shares a link to one.
license: MIT
compatibility: Requires Node.js 20+, and git to scan remote repositories.
---

# skillcheck

A skill runs with the agent's permissions: its scripts execute on the user's machine and its text becomes the agent's instructions. Check a skill before it lands in a skills folder.

## Before installing a skill

1. Scan the source, before copying anything:

   ```bash
   npx -y skillcheck-cli <owner/repo | github-url | local-path>
   ```

2. Go through the report with the user:
   - **Security errors** (`hidden-unicode`, `prompt-injection`, `remote-exec`, `obfuscated-exec`): stop. Show each finding with its `file:line` and snippet, and install only if the user confirms after reading them.
   - **Security warnings** (`concealment`, `exfil-endpoint`, `secret-access`, `persistence`, `agent-config`, `destructive-command`, `binary-file`, `symlink`): explain in one sentence what the code does and whether it fits the skill's stated purpose. A Slack skill calling a Slack webhook is expected; a PDF skill reading SSH keys is not.
   - **Spec errors** (`frontmatter-*`, `name-*`, `description-*`): the skill may fail to load. Say so.
3. Install only once the user agrees.

## Before publishing a skill

1. Run `npx -y skillcheck-cli . --strict` at the root of the repository.
2. Fix every finding, then run it again until it reports no problems.
3. Offer to add the GitHub Action so every pull request gets checked:

   ```yaml
   - uses: Anas912847/skillcheck@v1
     with:
       strict: true
   ```

## Limits

skillcheck matches known patterns. A clean report lowers the risk, it does not prove a skill is safe: still skim `scripts/` before running anything from an unknown author.
