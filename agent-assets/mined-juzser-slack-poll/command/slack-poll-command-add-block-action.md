Add a new block action handler for the Slack poll bot.

The user will describe what the new action should do. Use $ARGUMENTS as the description.

Steps:
1. Read `src/index.ts` to understand the existing `handleBlockAction()` function and how actions are routed by `action.action_id`.
2. Read `src/durable-objects/poll-object.ts` if the action needs to persist state.
3. Read `src/views/poll-message.ts` and/or `src/views/poll-modal.ts` if the action needs to update a message or open a modal.
4. Add a new `action_id` constant (snake_case) for the action button/menu item in the appropriate view builder.
5. Add a new `case` branch in `handleBlockAction()` that:
   - Extracts relevant values from the action payload (user id/name, channel, message_ts, poll_id from metadata)
   - Calls the Durable Object if needed
   - Updates the Slack message via `client.chat.update()` or opens a modal via `client.views.open()`
6. If a new Durable Object endpoint is needed, add it to `PollObject.fetch()` in `poll-object.ts`.

Constraints:
- Keep all user-facing strings in Vietnamese (Tiếng Việt)
- Use `@slack/types` for Block Kit type safety
- The handler must return `new Response("", { status: 200 })` — Slack requires HTTP 200 for block actions
- Use tabs for indentation, 140 char line width (Prettier config)

The action to add: $ARGUMENTS
