---
name: setup-apify-insights
description: Install, connect, update or remove apify-insights-mcp, the read-only MCP server that answers an Apify creator's questions about their own actors (earnings, profit, failing or flagged actors, users, acquisition, quality scores, Store rank). Use when the user asks to install or set up apify-insights, connect their Apify account to Claude, Codex, Cursor, Gemini CLI, Grok Build or OpenCode, turn on revenue or money data, fix an apify-insights connection, or update or uninstall it, even if they only say "set up the Apify MCP".
---

# Set up apify-insights

The detailed reference is [docs/install.md](https://github.com/Devansh-365/apify-insights-mcp/blob/main/docs/install.md). Follow these steps, and read that page only when a step points there.

The repository may be private. If a link does not open, read the file with `gh` (`gh api repos/Devansh-365/apify-insights-mcp/contents/<path> --jq .content | base64 -d`) or from a clone.

The server only reads data. Nothing here changes the user's Apify account. Never print, log or paste the user's Apify token, and never write it into a file yourself: the Apify CLI login keeps it out of every config.

## 1. Check the computer

- `node -v` must print v20 or later. If not, ask the user to install Node.js 20+ and stop.
- `git ls-remote https://github.com/Devansh-365/apify-insights-mcp.git HEAD` must print a commit. If it fails, the user's git cannot reach the repository. Tell them to ask the owner for access, or to sign in to GitHub (`gh auth login`), and stop.

## 2. Find the Apify token

The server reads `APIFY_TOKEN`, then the Apify CLI login in `~/.apify/auth.json`. Check only that the file exists (`test -f ~/.apify/auth.json`). Do not read it.

If neither exists, the user runs the login, because it opens a browser:

```bash
npx -y apify-cli login
```

Use the CLI login rather than `APIFY_TOKEN` in a config: Gemini CLI strips variables with `TOKEN` in the name, and Codex passes no environment variables unless told to.

## 3. Register the server with every client

```bash
npx -y github:Devansh-365/apify-insights-mcp setup
```

This copies the server to `~/.apify-insights/app/index.js` and adds it to each client it finds:
- **Claude Code, Codex, Gemini CLI and Grok Build:** through their own `mcp add` command.
- **Cursor and OpenCode:** one entry merged into their JSON config.

Read its output line by line and tell the user what happened for each client:

- `added`: done.
- `could not add (...)`: the line below it is the exact command. Run it if the reason is something you can fix, such as a stale entry. If the reason is an old client version (for example `Unknown arguments`), tell the user to update that client.
- `is not plain JSON, left unchanged`: the config has comments. Add the printed entry to that file by hand, keeping its comments.

For a client that `setup` does not list (Claude Desktop, VS Code, Windsurf, Zed), use the matching section of docs/install.md. In Claude Desktop, the `.mcpb` file from the latest release installs with a double-click.

## 4. Confirm it works

The user restarts the client, or you run `/mcp` if your client supports it. Then call the `auth_status` tool. Expect `Apify API: connected as <username>`. If you are running inside the client you just set up and its tools are not loaded yet, ask the user to restart and say *"Check my apify-insights connection"*.

If something fails, use the "Check it works" table in docs/install.md.

## 5. Offer money data (optional)

Revenue, cost and profit need the bridge, a small Chrome extension that shares the user's Apify Console session. Ask before installing it. If they want it:

```bash
npx -y github:Devansh-365/apify-insights-mcp install
```

You cannot load a browser extension yourself, so give the user these steps:
1. Open `chrome://extensions` (or `brave://`, `edge://`, `arc://`) and turn on Developer mode.
2. Click **Load unpacked** and pick `~/.apify-insights/bridge`.
3. Stay logged in to console.apify.com in that browser.

Then call `auth_status` again: `Console session: ok` means the money tools work. `install` supports macOS and Linux only. On Windows, the public tools still work.

## Update or remove

- **Update:** run step 3 again. If the bridge is installed, run `install` again and ask the user to click reload on the extension.
- **Remove:** follow "Update or remove" in docs/install.md. Ask before deleting `~/.apify-insights`, because it also holds the usage log.

## When it is done

Tell the user which clients now have the server and whether money data is on. Then suggest a first question: *"How did my Apify actors do yesterday?"*
