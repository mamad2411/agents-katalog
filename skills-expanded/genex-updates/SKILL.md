# Genex updates in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's updates card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Studio ships and pins the Genex CLI, so ignore its update nudges and skills-refresh lines: never
  run `npm i -D @genex-ai/cli-demo`. Skill cards are never written into the game.
- Studio also pins `@genex-ai/multiplayer` and `@genex-ai/embed-sdk`: add them only with
  `genex__package`, which installs Studio's version. Never run `npm i …@latest` for them.
- If a Genex tool reports that the CLI is below the minimum supported version (HTTP 426,
  `cli_update_required`), tell the user Studio needs an update; there is nothing to run.
- The email-verification row applies as the card says.

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-updates/SKILL.md v1.40.0 sha256 cc42560960ff97138249019116d348c105ccca23cc93606540df53e5bbbc2251 -->
---
name: genex-updates
description: What Genex's update lines and refusals mean. Use when a genex command prints an update nudge ("⬆ Genex … available — run: …"), a skills-refresh line ("🔄 Genex skills updated"), or an update-required refusal (HTTP 426, cli_update_required), or when the user asks about updating Genex packages.
---

# Genex Updates

Genex ships improvements continuously, and the `genex` CLI says when something
is stale.

## The signals in `genex` output

| Line | Meaning | What you do |
| -- | -- | -- |
| `✗ … below the minimum supported version … Update now — run: <command>` | The API refuses this CLI version (HTTP 426, `cli_update_required`). | Nothing runs until Studio is updated: tell the user Studio needs an update. |
| `✗ Out of credits — … costs N credits; your balance is M.` | The account can't cover this generation (HTTP 402, `insufficient_credits`). | Studio keeps the generation's card, which says so and offers Get credits. Never relay the balance, cost or refill date, and don't retry. |
| `✗ Email not verified — …` | Generation credits are locked until the email is verified (HTTP 403, `email_verification_required`). | Give the user the printed verify link, wait for them to confirm, then re-run the command. |
