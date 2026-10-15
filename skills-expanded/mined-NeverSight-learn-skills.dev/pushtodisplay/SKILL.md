---
name: pushtodisplay
description: "Send real-time display updates to boards, manage boards, and query devices using the PushToDisplay CLI or MCP server. Use when: the user wants to send content to a display board, create/manage boards, check device connections, or integrate PushToDisplay into a workflow. Trigger on: 'send to display', 'display board', 'pushtodisplay', 'push to display', 'board update', 'display update', 'dashboard display', 'signage', 'send update to board', 'panel update', 'multi-panel', 'display blocks'."
---

# PushToDisplay

Send real-time content to display boards from the terminal or AI agents. Boards show styled text blocks on connected devices — phones, tablets, TVs, or any screen running the PushToDisplay app.

Install from npm — run directly with `npx` or install globally:

```bash
npx pushtodisplay --help
# or
npm install -g pushtodisplay
```

Requires Node.js 18+. See the [PushToDisplay documentation](https://pushtodisplay.com/docs) for guides, use cases, and API details.

**Two interfaces, same capabilities:**

- **CLI** — `pushtodisplay <command>` in any terminal. Every agent can shell out.
- **MCP server** — structured tool calls for agents that support the Model Context Protocol.

---

## 1. Authentication

Authentication is required before any command works. There are two credential types.

### Interactive login (full access)

Opens a browser. Works for all commands — send, boards, devices, config.

```bash
pushtodisplay auth login
```

For headless environments (SSH, containers, CI):

```bash
pushtodisplay auth login --device-code
```

Prints a URL and one-time code. Open the URL on any device, enter the code, approve.

Credentials are stored in the OS keychain (macOS Keychain, Linux libsecret, Windows Credential Manager). Falls back to `~/.config/pushtodisplay/` if the keychain is unavailable.

### API key (send-only)

API keys start with `pt_`. Create one from the mobile app or web portal.

```bash
# Environment variable
export PTD_API_KEY=pt_your_key_here
pushtodisplay send "Hello"

# Or store in keychain
pushtodisplay auth login --api-key pt_your_key_here
```

> **API key auth only supports the `send` command.** Use interactive login for boards, devices, and config management.

### Check and clear

```bash
pushtodisplay auth status    # Show current auth state
pushtodisplay auth logout    # Remove stored credentials
```

### MCP server auth

The MCP server inherits the CLI session. Run `pushtodisplay auth login` once, and the MCP server authenticates automatically.

---

## 2. Core Concepts

| Concept    | Description                                                                        |
| ---------- | ---------------------------------------------------------------------------------- |
| **Board**  | A named display destination. Not a physical device — any device can tune in        |
| **Panel**  | A targetable region within a board (1–4 depending on layout)                       |
| **Block**  | A text content entry in the `blocks` array. Each block can be styled independently |
| **Layout** | A board-level preset that determines panel arrangement                             |
| **Device** | A physical screen running the PushToDisplay app                                    |
| **Stream** | An active connection between a device and a board                                  |

### Layouts

Layouts are set when creating or updating a board, not per-message.

| Layout       | ID  | Panels | Description             |
| ------------ | --- | ------ | ----------------------- |
| Full Screen  | `0` | 1      | Single panel, full area |
| Stacked      | `1` | 2      | Top + Bottom            |
| Side by Side | `2` | 2      | Left + Right            |
| 2×2 Grid     | `3` | 4      | Four equal quadrants    |

---

## 3. CLI Commands

### Send updates

```bash
# Simple text (uses default board)
pushtodisplay send "Deploy succeeded"

# Target a specific board
pushtodisplay send -b <board-id> "Build passed"

# Styled text
pushtodisplay send -b <board-id> "ALERT" --size large --weight bold --color "#FF0000"

# Multiple text blocks (style flags apply to all blocks)
pushtodisplay send -b <board-id> "Build:" "passing" --color "#22C55E"

# Panel targeting
pushtodisplay send -b <board-id> --panel 2 "Right panel content"

# Full panel with layout options
pushtodisplay send -b <board-id> --panel 1 --full-panel --density compact --align-x center "Status OK"

# Per-block styling with JSON (repeatable)
pushtodisplay send -b <board-id> \
  --block '{"text": "API Health", "size": "large", "weight": "bold"}' \
  --block '{"text": "Uptime: 99.97%", "color": "#22C55E"}'

# Pipe full JSON from stdin
echo '{"boardId":"my-board","blocks":[{"text":"From pipe"}]}' | pushtodisplay send --stdin
```

If no `-b` flag is provided, the server uses the user's default board.

The three input modes — positional text arguments, `--block` JSON flags, and `--stdin` — are mutually exclusive. Do not combine them. When style flags are used with multiple positional text arguments, they apply to **all** generated blocks. For per-block styling, use `--block` JSON syntax instead.

**Style flags:** `--size` (small/medium/large), `--weight` (regular/semibold/bold), `--color` (#RRGGBB), `--background` (#RRGGBB)

**Panel flags:** `--panel` (1–4), `--full-panel`, `--density` (compact/standard/spacious), `--align-x` (start/center/end), `--align-y` (start/center/end)

### Manage boards

```bash
pushtodisplay boards list                          # List all boards
pushtodisplay boards get <board-id>                # Get board details
pushtodisplay boards create -n "My Board"          # Create a board
pushtodisplay boards create -n "Dashboard" -l 3    # Create with 2×2 grid layout
pushtodisplay boards delete <board-id>             # Delete a board
```

### Query devices

```bash
pushtodisplay devices list    # List active device-board streams
```

### JSON output

Add `--json` to any command for machine-readable output:

```bash
pushtodisplay boards list --json
pushtodisplay send -b <board-id> "test" --json
```

---

## 4. MCP Tools

The MCP server exposes 8 tools. Start it with:

```bash
npx pushtodisplay mcp
```

### `pushtodisplay_send_update`

Send content to a board. Returns `{ messageId, enqueuedAtUtc, userId }`.

| Parameter    | Type            | Required | Description                         |
| ------------ | --------------- | -------- | ----------------------------------- |
| `boardId`    | `string`        | No       | Board ID. Omit to use default board |
| `blocks`     | `array` (min 1) | Yes      | Text blocks to display              |
| `panelId`    | `int` (1–4)     | No       | Target panel number                 |
| `fullPanel`  | `boolean`       | No       | Use full panel mode                 |
| `density`    | `string`        | No       | `compact`, `standard`, `spacious`   |
| `alignX`     | `string`        | No       | `start`, `center`, `end`            |
| `alignY`     | `string`        | No       | `start`, `center`, `end`            |
| `background` | `string`        | No       | Background color `#RRGGBB`          |

Each block in `blocks`:

| Field        | Type     | Required | Description                   |
| ------------ | -------- | -------- | ----------------------------- |
| `text`       | `string` | Yes      | Text content                  |
| `size`       | `string` | No       | `small`, `medium`, `large`    |
| `weight`     | `string` | No       | `regular`, `semibold`, `bold` |
| `color`      | `string` | No       | Text color `#RRGGBB`          |
| `background` | `string` | No       | Block background `#RRGGBB`    |

### `pushtodisplay_list_boards`

List all boards owned by the authenticated user. No parameters.

### `pushtodisplay_get_board`

Get details of a specific board.

| Parameter | Type     | Required | Description |
| --------- | -------- | -------- | ----------- |
| `boardId` | `string` | Yes      | Board ID    |

Returns: `{ boardId, name, description, layoutId, createdAt, updatedAt, isDefault }`

### `pushtodisplay_create_board`

Create a new board.

| Parameter     | Type     | Required | Description       |
| ------------- | -------- | -------- | ----------------- |
| `name`        | `string` | Yes      | Board name        |
| `description` | `string` | No       | Board description |
| `layoutId`    | `int`    | No       | Layout ID         |

### `pushtodisplay_update_board`

Update an existing board's name, description, or layout.

| Parameter     | Type     | Required | Description     |
| ------------- | -------- | -------- | --------------- |
| `boardId`     | `string` | Yes      | Board ID        |
| `name`        | `string` | No       | New name        |
| `description` | `string` | No       | New description |
| `layoutId`    | `int`    | No       | New layout ID   |

### `pushtodisplay_set_default_board`

Set a board as the user's default. The default board is used when no board ID is specified in `send_update`.

| Parameter | Type     | Required | Description                |
| --------- | -------- | -------- | -------------------------- |
| `boardId` | `string` | Yes      | Board ID to set as default |

### `pushtodisplay_delete_board`

Permanently delete a board and all its data. Cannot be undone.

| Parameter | Type     | Required | Description     |
| --------- | -------- | -------- | --------------- |
| `boardId` | `string` | Yes      | Board to delete |

### `pushtodisplay_list_devices`

List active device-board stream connections. No parameters.

Returns array of `{ boardId, deviceId }`.

---

## 5. Styling Guide

### Block-level styling

Each block in the `blocks` array can have its own `size`, `weight`, `color`, and `background`. These apply only to that block.

### Top-level (entry-level) styling

Top-level fields apply to the entire update entry for the target panel:

- `fullPanel` — expand content to fill the panel area
- `density` — line spacing (`compact` = tight, `standard` = normal, `spacious` = loose)
- `alignX` / `alignY` — content alignment within the panel
- `background` — background color for the entire entry

### Background scope

Top-level `background` and `blocks[].background` are **independent**. Block background does not inherit from or override the entry background.

### Color format

All colors must be hex `#RRGGBB`. They are validated and normalized to uppercase before display.

---

## 6. Recipes

### Multi-panel dashboard

Send to different panels of a 2×2 grid board:

```bash
# Panel 1 — top left
pushtodisplay send -b <board-id> --panel 1 \
  --block '{"text":"API","size":"large","weight":"bold"}' \
  --block '{"text":"200 OK","color":"#22C55E"}'

# Panel 2 — top right
pushtodisplay send -b <board-id> --panel 2 \
  --block '{"text":"Database","size":"large","weight":"bold"}' \
  --block '{"text":"Connected","color":"#22C55E"}'

# Panel 3 — bottom left
pushtodisplay send -b <board-id> --panel 3 \
  --block '{"text":"Queue","size":"large","weight":"bold"}' \
  --block '{"text":"12 pending","color":"#F59E0B"}'

# Panel 4 — bottom right
pushtodisplay send -b <board-id> --panel 4 \
  --block '{"text":"Errors","size":"large","weight":"bold"}' \
  --block '{"text":"0","color":"#22C55E"}'
```

### Styled alert with background

```bash
pushtodisplay send -b <board-id> --full-panel --density compact \
  --align-x center --align-y center --background "#7F1D1D" \
  --block '{"text":"🚨 INCIDENT","size":"large","weight":"bold","color":"#FECACA"}' \
  --block '{"text":"Payment gateway timeout — P1","color":"#FCA5A5"}'
```

### CI/CD pipeline status

```bash
pushtodisplay send -b <board-id> \
  --block '{"text":"deploy/prod #847","size":"large","weight":"bold"}' \
  --block '{"text":"✅ Build passed","color":"#22C55E"}' \
  --block '{"text":"✅ Tests passed (142/142)","color":"#22C55E"}' \
  --block '{"text":"🚀 Deployed to production","color":"#3B82F6"}'
```

### MCP — create a board and send to it

Using MCP tools in sequence:

1. `pushtodisplay_create_board` → `{ name: "Deploy Status", layoutId: 2 }` (Side by Side)
2. `pushtodisplay_set_default_board` → `{ boardId: "<id from step 1>" }`
3. `pushtodisplay_send_update` → `{ blocks: [{ text: "Ready", size: "large" }] }`

---

## 7. Errors and Limits

### Error responses

| Status | Meaning                                      |
| ------ | -------------------------------------------- |
| `400`  | Invalid request (bad fields, malformed JSON) |
| `401`  | Missing or invalid authentication            |
| `403`  | No active subscription                       |
| `404`  | Board not found or no active devices         |
| `409`  | Quota exceeded (boards or monthly messages)  |
| `429`  | Rate limit exceeded                          |

### Subscription tiers

| Quota            | Sandbox (free) | Go ($9.99/mo) | Pro ($19.99/mo) | Business ($49.99/mo) |
| ---------------- | -------------- | ------------- | --------------- | -------------------- |
| Boards           | 1              | 10            | 50              | 100                  |
| Active streams   | 2              | 3             | 10              | 50                   |
| Max message size | 4 KB           | 8 KB          | 32 KB           | 128 KB               |
| Monthly messages | 1,000          | 50,000        | 200,000         | 1,000,000            |
| Rate (msg/s)     | 1              | 1             | 1               | 2                    |
| Burst            | 2              | 3             | 5               | 20                   |

Devices are unlimited across all tiers. A board is a named display destination — not a physical device.

Rate limiting is per-user, token-bucket based. Monthly message count resets on the billing cycle.
