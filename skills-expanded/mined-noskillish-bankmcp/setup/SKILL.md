---
name: setup
description: Set up BankMCP™ on this machine step by step: check Node, register the local MCP server, walk through the Enable Banking application, finish the setup page and connect the first bank. Use when the user says "set up bankmcp", "install bankmcp", "/setup", "connect my bank for the first time", or has BankMCP tools that report "not set up yet".
---

# Set up BankMCP™ locally

You are guiding one person through running BankMCP™ on their own machine. Do the steps in order, one at a time, and confirm each before the next. Run commands yourself where you can; ask the user to do the parts that need their browser or their bank login. Do not guess values; read them from command output.

## 1. Node

Run `node --version`. BankMCP needs 24 or newer. If it is older or missing, tell the user to install the current LTS from https://nodejs.org and stop until it is done.

## 2. Register the server with Claude Code

Run:

```
claude mcp add --scope user bankmcp -- npx -y bankmcp
```

Then tell the user to restart Claude Code (or run `/mcp`) so the `bankmcp` tools appear. Wait for them to confirm the tools are listed.

## 3. Find the setup page

Call any BankMCP tool, for example `list_accounts`. On a fresh install it answers with a localhost address such as `https://localhost:8080`. Give the user that exact address and tell them:

- their browser will warn about a self-signed certificate on localhost; they should continue past it, it is the server they just started;
- the page lists four values for Enable Banking's form, each with a Copy button.

## 4. Enable Banking application

Tell the user to open https://enablebanking.com/cp/applications in another tab, create an account if needed, and add an application:

- Environment: **Production** for real accounts, **Sandbox** to try with test data.
- Paste the redirect URL, description, privacy URL and terms URL from the setup page.
- Keep "generate private key" selected. On Save a `.pem` file downloads once; the application id (a UUID) is shown after saving.

For Production, mention that the application starts Inactive and that clicking **Activate by linking accounts** and logging in at their bank is what activates it for their own accounts.

## 5. Finish the setup page

Back on the localhost page: paste the application id, choose the downloaded `.pem`, set the country, click Finish setup. The page turns into a status page. Confirm with the user.

## 6. Connect the first bank

Call `list_banks` with the user's country and let them pick. Call `start_consent` with the exact bank name and give them the URL. They log in at the bank and land on a "Bank connected" page. Then call `list_accounts` and show what got linked. Offer labels with `set_account_label`.

## If something fails

- Tool says "not set up yet" after setup: the server may need a restart; run `/mcp` and reconnect `bankmcp`.
- "redirect_uri" errors from Enable Banking: the redirect URL on the application must be exactly the one the setup page showed, including `https://` and the port.
- Port in use: set `PORT` for the server (for example `claude mcp add --scope user -e PORT=8085 bankmcp -- npx -y bankmcp`) and register the matching redirect URL.
