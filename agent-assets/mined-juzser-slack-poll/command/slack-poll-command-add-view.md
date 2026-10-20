Add a new Slack Block Kit view (modal or message) to the poll bot.

The user will describe the view to create. Use $ARGUMENTS as the description.

Steps:
1. Read `src/views/poll-modal.ts` and `src/views/poll-message.ts` to understand the existing view builder conventions and how Block Kit blocks are assembled.
2. Read `src/types/slack.ts` for available type definitions.
3. Create a new file in `src/views/` named after the view (e.g. `src/views/confirm-modal.ts`).
4. Export a builder function that accepts the necessary data parameters and returns a typed Block Kit payload:
   - For modals: return `ModalView` compatible with `client.views.open()` / `client.views.update()`
   - For messages: return `{ blocks: Block[], text: string }` compatible with `client.chat.postMessage()` / `client.chat.update()`
5. Import and call the new builder from the appropriate handler in `src/index.ts` or `src/handlers/`.
6. If the view includes interactive elements (buttons, menus, inputs), define their `action_id` / `block_id` constants at the top of the view file so callers can reference them.

Constraints:
- All user-facing strings must be in Vietnamese (Tiếng Việt)
- Use `@slack/types` for type safety on all Block Kit objects
- Keep view builder functions pure — no side effects, no API calls
- Use tabs for indentation, 140 char line width (Prettier config)

The view to create: $ARGUMENTS
