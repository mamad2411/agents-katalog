---
name: knock-in-app-ui
description: Guidance for implementing Knock in-app UI in a web app, with a focus on setting up, rendering, and debugging Knock guides in React.
---

# Knock in-app UI skill

This skill helps you build in-app UI with Knock. It covers the two in-app products — **feeds** and **guides** — at a high level, then goes deep on guides: provider setup, rendering with hooks, and debugging.

Reference: https://docs.knock.app/in-app-ui/overview

## Overview

The skill is organized into four focused rule files. Client-framework guidance is scoped per framework via a `-<framework>` suffix (currently only React). Cross-framework concepts live in unsuffixed files.

1. **Feeds vs. guides** (framework-agnostic) — which product to pick for a given surface and why
2. **Setting up the guide providers in React** — `KnockProvider` and `KnockGuideProvider` props, where each value comes from, and how to sequence them
3. **Rendering guides in React** — building a guide component with `useGuide` / `useGuides`, typed content, and engagement tracking
4. **Debugging guides** (framework-agnostic) — the guides toolbar, the triage checklist, and testing workflow

> **Framework scope:** right now this skill only covers React (`@knocklabs/react`). If the user is building with Vue, Svelte, plain JS, React Native, iOS, or Android, stop and ask how they'd like to proceed — do not adapt the React rules to another client SDK on your own.

## How to use this skill

### When deciding what to build

Start with `rules/feeds-vs-guides.md`:

- Confirm the surface you're building is actually a guide, not a feed
- Check the decision table before picking a direction
- If the answer is "both," wrap the app in `KnockProvider` once and render each product's provider where it's needed

### When adding guides to a React app for the first time

1. Read `rules/setup-guide-providers-react.md`
2. **Before running any CLI commands, confirm the CLI is authenticated and which Knock environment this setup is for.** First run `knock whoami` — if it errors with something like "not authenticated" or "no user session," run `knock login` and ask the user to complete the browser flow before continuing (the CLI persists the session so this is a one-time step per machine). Only after `knock whoami` succeeds, run `knock environment list` and ask the user to pick (the CLI defaults to `development`, but most real integrations target `production`). Remember that slug as `<env-slug>` and pass `--environment <env-slug>` on every subsequent environment-scoped `knock` command.
3. **Before asking the user anything about the channel, discover `channelId` via the Knock CLI:** run `knock channel list --json | jq -r '.[] | select(.key == "knock-guide") | .id'`. Channels are account-scoped, so this command does **not** take `--environment`. If it prints a UUID, use it — do not ask the user to confirm or re-paste. Only ask the user if the CLI returns nothing or errors. See the rule file's "Where to get `channelId`" procedure for the full fallback order.
4. Ask the user only for values that can't be auto-discovered — primarily the public `apiKey` for the chosen environment (and confirm `user.id` is coming from the app's auth context). Do not bundle the `apiKey` ask with `channelId`.
5. Wire `KnockProvider` + `KnockGuideProvider` at the top of the tree.
6. Gate `readyToTarget` on any async data your targeting depends on.
7. **Get a real guide rendering before stopping.** Run `knock guide list --environment <env-slug> --json`, show the user the options (`key`, `name`, each step's `schema_key`), and build the first component against a real guide's actual values. Do not scaffold with placeholder strings like `"changelog-card"`. Fetch the message type schema with `knock message-type get <schema_key> --environment <env-slug> --json` so the content is typed. **If the environment has no guides, offer to scaffold a test one via the Knock CLI** (`knock guide new` → edit the JSON → `knock guide push --environment <env-slug>`) using a built-in message type (`card`, `banner`, or `modal`) with obvious-placeholder content — don't stall waiting for manual dashboard setup. See `rules/rendering-guides-react.md` → "First guide: discover real guides via CLI before writing code" for the full procedure including the empty-environment branch.
8. Flag anything that still needs the user (paste `pk_` key, flip the guide to active in the dashboard, restart dev server) explicitly — don't leave them to discover it by absence.

### When building a new guide component in React

1. Follow the workflow in `rules/rendering-guides-react.md`
2. **Discover the target guide (or message type) via the Knock CLI before picking values.** `knock guide list --environment <env-slug> --json` for the guide's `key` / step `schema_key`; `knock message-type get <schema_key> --environment <env-slug> --json` for the content schema. Avoid placeholder strings.
3. Pick `useGuide` for single-guide surfaces, `useGuides` for lists
4. Define a TypeScript type that mirrors the message type schema you just pulled
5. Wire `markAsSeen`, `markAsInteracted`, and `markAsArchived` — custom components must do this themselves

### When a guide isn't rendering

1. Open `rules/debugging-guides.md` and work the triage checklist top to bottom
2. Turn on the guides toolbar (`?knock_guide_toolbar=true`) first — it answers most questions in seconds
3. Distinguish server-side (targeting/eligibility) from client-side (provider/component) failures before digging deeper

## Rule files reference

- `rules/feeds-vs-guides.md` — product selection between feeds and guides (framework-agnostic)
- `rules/setup-guide-providers-react.md` — configuring `KnockProvider` and `KnockGuideProvider` for guides (React)
- `rules/rendering-guides-react.md` — `useGuide`, `useGuides`, typed content, engagement tracking (React)
- `rules/debugging-guides.md` — toolbar, triage checklist, testing workflow (framework-agnostic)

## Quick reference

The examples below are React. For any other client SDK, see the note at the top of **Overview** before proceeding.

### Providers (minimum viable setup — React)

```tsx
<KnockProvider
  apiKey={process.env.NEXT_PUBLIC_KNOCK_API_KEY}
  user={{ id: currentUser.id }}
>
  <KnockGuideProvider
    channelId={process.env.NEXT_PUBLIC_KNOCK_GUIDE_CHANNEL_ID}
    readyToTarget
    listenForUpdates
  >
    {children}
  </KnockGuideProvider>
</KnockProvider>
```

### Where to source each value

- **Auth first, then environment** — Knock is environment-scoped. Before any CLI command, verify the CLI is authenticated with `knock whoami`; if it errors, run `knock login` and wait for the user to complete the browser flow. Then run `knock environment list` and confirm the target slug (`production`, `development`, …) with the user. Pass `--environment <env-slug>` on every subsequent environment-scoped `knock` command. Don't rely on the CLI's `development` default.
- `apiKey` — Knock dashboard → **Platform → API keys** → public `pk_...` key **from the tab for the chosen environment** (switch envs via the dashboard's environment selector first; remind the user to copy the key for the right env)
- `user.id` — your auth context; must match the id used when identifying the user from your backend
- `channelId` — the **UUID** of the guide channel, not its key. Channels are account-scoped, so `knock channel list` does **not** take `--environment`. **Always attempt CLI discovery before asking the user:**

  ```bash
  knock channel list --json | jq -r '.[] | select(.key == "knock-guide") | .id'
  ```

  If this prints a UUID, use it directly — don't prompt for confirmation. The default guide channel key is `knock-guide` (type `in_app_guide`). Fall back to the dashboard (**Settings → Integrations → Channels**) only if the CLI returns nothing or errors. See `rules/setup-guide-providers-react.md` for the full procedure.

### Hooks at a glance

- `useGuide({ type })` — one guide by message type
- `useGuide({ key })` — one specific guide by key
- `useGuides({ type })` — array of guides by message type
- `useGuideContext()` — low-level client access

### Engagement methods

- `step.markAsSeen()` — impression (call from `useEffect` keyed on `step`)
- `step.markAsInteracted()` — primary action
- `step.markAsArchived()` — dismissal; removes the guide for this user going forward

### First stop when something's wrong

Append `?knock_guide_toolbar=true` to any URL. The toolbar shows all guides, which are active, which this user is eligible for, and why the rest were filtered out.

## Best practices summary

1. **Pick the right product.** Feeds for chronological lists, guides for targeted UI.
2. **Mount providers once, high in the tree.** Inside your auth boundary, above any route that renders guides.
3. **Never pass a placeholder user.** Wait for auth to resolve before mounting `KnockProvider`.
4. **Gate `readyToTarget` on async data** your targeting rules depend on.
5. **Type your content.** `useGuide<T>` should mirror the Knock message type schema.
6. **Always handle engagement.** Custom components must call `markAsSeen`, `markAsInteracted`, and `markAsArchived` themselves.
7. **Use the toolbar first.** Most "the guide isn't showing" questions are answered in seconds.
