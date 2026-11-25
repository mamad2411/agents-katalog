---
description: Deploy the current local project to Hatchable. Use when the user wants to import, migrate, publish, or host an existing repo or working directory on Hatchable.
disable-model-invocation: true
---

# Import this project to Hatchable

Deploy the current working directory (or the path in "$ARGUMENTS", if given) as a Hatchable project.

Use the Hatchable MCP tools (the `hatchable` server bundled with this plugin). If they are unavailable or unauthenticated, tell the user to run `/mcp` and complete the Hatchable OAuth sign-in first.

1. **Survey the local project.** List its files and identify what maps to Hatchable's structure: static assets to `public/`, server endpoints to `api/*.js` handlers, schema to `migrations/*.sql`, shared code to `lib/`. Read https://hatchable.com/docs/developers/project-structure if unsure of the target shape.
2. **Check the fit before writing.** Hatchable runs plain JS with no build step and no npm install. If the project uses a bundler, TypeScript, an ORM, or a server framework, tell the user what needs restructuring and how much work it is BEFORE creating anything. Small static sites and plain-JS apps import cleanly; framework apps need porting.
3. `create_project`, then push the mapped files with `write_files` in batches.
4. `dry_run_deploy` first. Fix every blocker it reports (the errors name the supported alternative), then `deploy`.
5. Verify the live URL works, then hand it to the user. Mention that the project starts private and how to share or publish it from the console.

If the user's repo is on public GitHub and they'd rather not go file-by-file, they can also paste the repo URL into the console's Import page; offer that as the alternative.
