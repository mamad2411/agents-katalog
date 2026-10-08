---
name: research-publish
description: Publish standalone HTML research reports to Nir Pechuk’s password-protected website at nirpechuk.github.io/research from a local or headless remote machine, without a Git checkout.
---

Publish a user-requested HTML report using the bundled `scripts/upload.mjs`.
Requires Node.js 20+ and network access to GitHub and the website.

## Credentials

Use existing `GH_TOKEN` / `GITHUB_TOKEN` or the machine’s `gh auth` login.
The GitHub credential needs Contents read/write access to
`nirpechuk/nirpechuk.github.io`. Read the research password from
`RESEARCH_PASSWORD`, `~/.config/nir-research/password`, or `--password-file PATH`.
If either credential is missing, ask the user to configure it on the machine;
do not ask them to paste tokens into chat or print credentials in tool output.

## Publish

1. Prepare one self-contained HTML file, up to 50 MiB. Embed images, styles, and scripts, or
   use absolute HTTPS assets. External assets remain public. Reports run in a
   sandboxed iframe: scripts work, but same-origin storage and backend services
   are not available. Do not upload raw sensitive images separately.
2. Choose a descriptive lowercase hyphenated slug. Slugs and commit messages
   are public, so avoid sensitive information in the slug. Reuse an existing
   slug only when the user intends to update that report.
3. Validate without changing GitHub:

   ```sh
   node /path/to/this/skill/scripts/upload.mjs /path/to/report.html --slug experiment-notes --dry-run
   ```

4. If the user has requested publication, publish and wait for the exact uploaded
   payload to appear online:

   ```sh
   node /path/to/this/skill/scripts/upload.mjs /path/to/report.html --slug experiment-notes --title "Experiment notes" --wait
   ```

   Add `--replace` to both commands for an intended update of an existing page.
   Resolve `/path/to/this/skill/` relative to this SKILL.md. If installed, the
   `nir-research` command is an equivalent shortcut. Use `--list` to find pages.

5. Return the URL and whether the JSON result says `live` or `queued`.
   A commit is not proof that deployment finished. If the wait times out,
   check GitHub Actions or fetch the live page; do not upload again just to wait.

The uploader encrypts before sending data, updates only the four relevant
research files, and uses a non-forced branch update. On a concurrent-change
error, inspect the latest directory before retrying once. If another upload
created the same slug, do not add `--replace` unless that update was intended.
Stop and report repeated conflicts, branch permission errors, or an ambiguous
network result after a commit was created. Do not force-update main or bypass
branch rules. No browser, Git checkout, npm packages, or Ruby build is needed.
