---
name: feedcontext
description: Provides first-party FeedContext workflows for authentication, Feed Item reading, RSS/Atom Subscription management, and traceable local artifacts. Use when the user asks to connect FeedContext, inspect feeds, read Feed Items, manage Subscriptions, or create feed-backed briefings or audio briefs.
---

# FeedContext Skill

FeedContext is skill-first. Use this root skill to route to the action docs and
the `feedcontext` CLI. Read only the action doc needed for the user's current
workflow; do not load every action doc by default.

## CLI Invocation

Prefer the local `feedcontext` binary when it exists on `PATH`. If it is not
available, use `npx -y feedcontext@latest` as a best-effort fallback for the
same command:

```bash
feedcontext version || npx -y feedcontext@latest version
```

Apply the same fallback to other FeedContext CLI commands documented by this
skill. For example, `feedcontext item list` becomes
`npx -y feedcontext@latest item list` when the local binary is unavailable.
This fallback is a convenience path, not a guaranteed runtime contract: it
depends on npm registry access, a working Node/npm/npx installation, and sandbox
permission to write npm cache and temporary files. If both the local CLI and the
`npx` fallback fail, report that FeedContext CLI execution is unavailable in the
current environment and ask the user to install the CLI with
`npm install -g feedcontext`.

Before any other FeedContext action in an agent session, run the version check:

```bash
feedcontext version || npx -y feedcontext@latest version
```

The version action prints JSON with CLI package metadata. Use it as the first
tool check before authenticated FeedContext CLI actions.

When the host prompt provides an explicit local helper path for validation or
rendering, use that exact path for local-only helper commands. The first helper
command in a local artifact workflow should still be `version`, for example:

```bash
node /path/to/skills/feedcontext/scripts/helper.mjs version
```

Then run `feedcontext auth status` before auth-sensitive workflows. If there is
no local Skill Session, do not ask the user to log in by default; run
`feedcontext auth anonymous` to create an anonymous Skill Session for local
Skill + CLI use. Ask the user to run formal login only when they want durable
storage, cross-device sync, account switching, or an integration that requires a
formal account.

Use `feedcontext auth login` for formal login. Use `feedcontext auth logout`
when the user asks to sign out, switch accounts, or clear a stale local session.

## Action Router

- `actions/auth.md`: CLI Session status, anonymous auth, formal login, pair
  code completion, logout, and account switching.
- `actions/feed-items.md`: Feed Item discovery, pagination, reading, and
  `get-many` for selected items.
- `actions/subscriptions.md`: Subscription list, approved add, and approved
  delete.
- `actions/integrations.md`: Telegram binding status and final artifact
  delivery readiness.
- `actions/api.md`: public `/v1` boundary and raw calls when high-level CLI
  commands are not enough.
- `actions/artifact/README.md`: shared artifact workflow for briefings,
  pages, audio briefs, and full Feed Item streams.
- `actions/migration.md`: RSS reader migration and OPML import routing.
- `actions/troubleshooting.md`: recovery paths after auth, write, or API
  boundary failures.

When the user asks to import or migrate existing subscriptions, follow
`actions/migration.md` first. If the user did not name the source platform and
did not provide an OPML or export file, ask which RSS reader they are migrating
from before choosing a platform playbook. Use `actions/migration/opml.md` when
an OPML or export file is already available.

When reading Feed Items, remember that `item list` is paginated and returns one
page by default. Use `item list --all` when the user asks for all matching Feed
Items.

When composing summaries, roundups, insights, briefings, briefing pages, or
audio briefs, follow `actions/artifact/README.md`. Artifact workflows are
file-backed: use one per-session system temporary directory workspace, create a
Structured Synthesis JSON sidecar before final prose or rendering, and preserve
review notes beside the output. For audio briefs, create and validate a Show
Script before generating audio.

For organized page or audio artifacts, do not default the Artifact Topic count.
After candidate discovery, estimate the semantic topic count from the actual
Feed Items, recommend a count with evidence, and wait for user confirmation
unless the user already specified capacity or the request is a full Feed Item
stream/listing/export.

When the user asks to generate a page, briefing page, digest page, roundup page,
or HTML-like FeedContext artifact from live Feed Items, the default output is a
server-rendered Artifact submitted through `feedcontext artifact
submit-definition`. Do not stop after local helper rendering unless the user
explicitly asks for a local-only HTML file, the prompt supplies an offline
fixture/export, or live FeedContext API access is unavailable. Local helper
rendering is a validation and offline-output path, not a substitute for the
server DSL submission path.

When the user asks to send a generated page or audio brief to Telegram, follow
`actions/integrations.md` to confirm Telegram is linked, then follow
`actions/artifact/README.md` to upload and deliver the final artifact with its
Structured Synthesis sidecar.

This repository publishes the installable skill from `skills/feedcontext`.
Service interaction uses the published `feedcontext` CLI. Local helpers are for
deterministic local-only mechanics, such as schema validation, offline fixture
outputs, and explicit local-only artifact rendering from reviewed structured
sidecars.
