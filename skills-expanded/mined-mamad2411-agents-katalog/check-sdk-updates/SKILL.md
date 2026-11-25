---
name: check-sdk-updates
description: Check whether Claude Code, Claude Agent SDK, and Codex SDK have new versions on npm. Use when the user asks to check for SDK/CLI updates, e.g. "check sdk updates", "check claude code update", "有沒有更新", "檢查 SDK 版本".
---

# Check SDK Updates

Compare the versions of `@anthropic-ai/claude-code`, `@anthropic-ai/claude-agent-sdk`, and `@openai/codex-sdk` declared in `package.json` against the latest published version on npm.

## Steps

1. Read the `dependencies` block of `package.json` and extract the current declared range for each of:
   - `@anthropic-ai/claude-code`
   - `@anthropic-ai/claude-agent-sdk`
   - `@openai/codex-sdk`

2. Run the following command (single Bash call) to fetch latest versions in parallel:
   ```bash
   npm view @anthropic-ai/claude-code version & \
   npm view @anthropic-ai/claude-agent-sdk version & \
   npm view @openai/codex-sdk version & \
   wait
   ```
   Map the three lines of output back to the three packages in the order requested.

3. For each package, compare the declared version (strip leading `^`/`~`) with the latest. Report a compact table:

   ```
   Package                              Current    Latest     Status
   @anthropic-ai/claude-code            2.1.119    2.1.120    ⬆ update
   @anthropic-ai/claude-agent-sdk       0.2.119    0.2.119    ✓ up to date
   @openai/codex-sdk                    0.125.0    0.126.0    ⬆ update
   ```

4. **For each outdated package, analyze the gap between current and latest** so the user can decide how to implement the update. For each one:

   a. Get the list of versions in between with:
      ```bash
      npm view <pkg> versions --json
      ```
      Filter to versions strictly greater than current and ≤ latest. Note the count and span (patch / minor / major bumps).

   b. Try to fetch release notes / changelog. Try in this order, stop at the first that works:
      - `npm view <pkg> repository.url` → if it points to a GitHub repo, use `gh release list -R <owner/repo> --limit 30` and `gh release view <tag> -R <owner/repo>` for the relevant tags.
      - Look for a `CHANGELOG.md` inside `node_modules/<pkg>/` (already-installed copy reflects the *current* version, but its history section may still cover newer versions if upstream backfills).
      - Fall back to: `npm view <pkg>@<latest> --json` and read the `description` / `homepage` fields, then `WebFetch` the homepage's changelog/releases page.

   c. Summarise per package in 2–4 bullets:
      - Number of versions skipped (e.g. "5 patch releases, 1 minor")
      - Any **breaking changes** or notable API/CLI changes
      - Any items that touch the parts of our codebase that consume this SDK (e.g. `electron/claude-agent-manager.ts`, `electron/codex-agent-manager.ts`, `electron/openai-agent-manager.ts`)
      - Risk assessment: low / medium / high, with one-line justification

5. After the per-package analysis, suggest the exact `npm install` command to bump them, e.g.:
   ```
   npm install @anthropic-ai/claude-code@latest @openai/codex-sdk@latest
   ```
   Group low-risk bumps together; call out any high-risk bump as needing a separate, careful update. Do NOT run the install — only suggest it. Wait for the user's confirmation before installing.

## Notes

- Use `npm view` (not `npm outdated`) so the check works without touching the lockfile or node_modules.
- If `npm view` fails (offline / registry error), report which package failed and stop.
- Keep the output short — table + suggested install line is enough.
