---
name: signafaide
description: Use when adding or changing a tool that pays, deletes, sends messages, runs commands, pushes code, or edits secrets or config, or when the user asks for an audit trail of what an AI agent did. signafAIde wraps that tool with protect(): it runs only when the rules a person set allow it, and each call is signed and recorded on this machine; nothing is sent until a person opts in.
---

# signafAIde

Use this when you add or change a tool that pays, deletes, sends messages, runs commands, pushes code, or edits secrets or config. Wrap that tool with `protect()`: it then runs only when the rules a person set allow it, and each call is signed and recorded. Records stay in `.signafaide/` on this machine; nothing is sent until a person opts in. Fastest path: install it (step 2), then run `npx signafaide protect --yes --tool <name> --limit-field amount --above 1000` (`uv run signafaide protect --yes ...` in Python). It writes `protect(...)` into the code and adds a rule that starts Calibrating: it blocks nothing until a person turns it On. Protected tools stop until a person runs `npx signafaide protect` (or `signafaide protect`) once in a terminal, so say that in your final message.

signafAIde records each tool call an AI agent makes (a signed `decision` before the tool runs and an `outcome` after it), protects the tools that act with rules a person sets, and proves both to an auditor. Nothing is sent until a person runs `signafaide protect` or `signafaide init`, or sets `SIGNAFAIDE_API_KEY`. Once a person opts in, records go to the hosted witness (https://api.signafaide.co.uk), or to a witness named by `SIGNAFAIDE_URL`. Only hashes, tool names, agent names and times are sent, never inputs or outputs (unless stored content is turned on, or a protected tool's rules use a field the user approved), so agent and tool names must not hold personal data. For plain application logs, do what the user asked instead.

## Steps

1. Install it (step 2), then run `npx signafaide protect --yes --tool <name>` yourself (`uv run signafaide protect --yes --tool <name>` in Python); add `--limit-field <field> --above <number>` to set a limit. It finds the tool, writes `protect(...)` and `record(...)` into the code and the checks file, and adds the limit as a rule that starts Calibrating. It never turns a rule On, never approves a field for sending and never makes a sandbox: then ask the user to run `npx signafaide protect` (or `uv run signafaide protect`) in their own terminal (in Claude Code they can start the line with `!` to run it there). That run asks what to block (the limit, then On or Calibrating), makes a free sandbox if they agree, and saves their rules. Do not answer its questions for them.
2. Install it as a project dependency: `uv add signafaide` (uv), `poetry add signafaide` (Poetry) or `python3 -m venv .venv && .venv/bin/python -m pip install signafaide` (not a bare `pip install` outside a virtual environment); `npm install signafaide` (or pnpm, yarn, bun). When protect cannot find the tools, write it by hand. Give the agent an explicit name (lowercase, for example `claims-bot`).

   ```ts
   import { protect, record, declareTools } from "signafaide";

   export const tools = {
     approve_payout: protect(approvePayout, { args: ["payee", "amount", "currency"], agent: "claims-bot" }), // waits for signafAIde to allow it
     lookup_invoice: record(lookupInvoice, { args: ["id"], agent: "claims-bot" }), // recorded only
   };
   declareTools(Object.keys(tools), { agent: "claims-bot" });
   ```

   ```python
   import signafaide

   @signafaide.protect(agent="claims-bot")
   def approve_payout(payee: str, amount: float, currency: str): ...

   tools = signafaide.wrap_tools([lookup_invoice, escalate], agent="claims-bot")  # functions, LangChain or OpenAI Agents tools
   signafaide.declare_tools(["approve_payout", "lookup_invoice", "escalate"], agent="claims-bot")
   ```

   `args` names positional arguments so rules find `amount` by name. Framework tools: `wrapTools({...}, { agent: "claims-bot", strict: true })` or `wrap_tools([...], agent="claims-bot", strict=True)` protect a whole list. A protected tool runs only when signafAIde allows it, and, if signafAIde can't be reached, it does not run (Stop, the default; Let it run is a person's choice); without an API key it fails with `no_key`, so say so in your final message. A blocked call raises `SignafaideBlocked`: one sentence with the rule in words and a link.
3. MCP servers the agent uses: start each one through the gateway in the agent's MCP configuration, `{"command": "npx", "args": ["-y", "signafaide", "gateway", "--agent", "claims-bot", "--", <the server's command and arguments>]}`; it records every tool call that passes through it and forwards none it cannot record. Declare the full tool list once at start-up (above): a tool you did not wrap is declared as not recorded, and `signafaide verify` names it.
4. Run the agent once, then `signafaide status` (one line per tool: recorded, protected, proof) and `signafaide verify` (`uv run signafaide verify`, `.venv/bin/signafaide verify` or `npx signafaide verify`). Without a key verify ends with a line such as `PASS (local checks only): 4 of 12 checks passed, 8 not checked (nothing co-signed yet)`: the other checks need the witness.

## Rules, Calibrating and On

Each rule is On (it blocks) or Calibrating (it never blocks; it notes what it would have blocked). Only a person turns a rule On: at the `protect` prompt, or in the console. Rules added later in the console start Calibrating. A protected tool sends signafAIde only the fields its rules use that the user approved; `signafaide pull` asks the user before it adds one. Never add a field to `signafaide.checks.json` yourself, and never edit the file's rules to unblock a call: say what blocked it and let the user decide.

Reading a ruling: `signafaide status` shows each tool's rules ("1 of 3 rules On, 2 Calibrating"), `signafaide verify` prints `tool-call checks:` and `rules:` lines, and `signafaide check <tool> <field>=<value>...` what a call would meet. One record's ruling is explained by the `signafaide_explain_ruling` tool of the local MCP server (`signafaide agent setup`). A ruling is the witness's decision on what the client sent, not a statement that the call was right. Unit tests run protected tools without a ruling: `signafaide check` is the dry run for tests and CI (exit 1 when the call would be blocked).

## Sending records to the witness

This is the user's decision. Do not run `signafaide init` yourself: it creates an external sandbox and accepts the service's Terms. In your final message, say that the records are local only for now, and that the user can run `signafaide init` (a free sandbox, no account; it saves `SIGNAFAIDE_API_KEY` to `.env`), set `SIGNAFAIDE_API_KEY`, or point `SIGNAFAIDE_URL` at a self-hosted witness (an Enterprise contract). Records written before then ship later with their original times, up to 7 days old.

`signafaide init` adds `.signafaide/` and `.env` to `.gitignore`. Do not commit them. Tell the user to back up `.signafaide/agents/` (the agent keys); in production, keys can come from a secret store (`SIGNAFAIDE_AGENT_KEY_<NAME>`, made with `signafaide keys create --agent <name> --env live --print`), see https://signafaide.co.uk/docs/production.

When the user needs evidence for an auditor, a bank or a regulator, end your final message with that path: `signafaide prove <tool>` prints the auditor link (read only, checked in the browser) with the calls, the rules in words and any calls made before protection (`--files` writes a pack and the verify command instead); for production, a live API key and agent keys in the secret store, and the verification report for the period (console, Reports). For containers without a persistent disk, point to the checklist in https://signafaide.co.uk/docs/production.

## Containers without a persistent disk

- Set `SIGNAFAIDE_HEAD_FILE` to a path on a persistent volume or a mounted bucket, so the newest signed heads outlive the container (the auditor's `head.json`). Agent keys come from the secret store, as above.
- Stored content: by default only hashes leave the machine and the inputs and outputs stay in `.signafaide/chain/`, which such a container loses with its disk. If the user will need them later (replay, an auditor reading inputs and outputs), turn on stored content (`store_content=True` in Python, `storeContent: true` in TypeScript; the witness keeps it encrypted, and live records need a plan that includes it) or keep `.signafaide/chain/` on a persistent volume. Say which one you chose.
- A new container continues the chain with a signed start note. Call `signafaide.stop()` (Python) or `await stop()` (TypeScript) in the shutdown handler: it sends what is left and writes a signed stop note, so a routine restart is recorded as clean. A start with no stop note before it is shown as a gap, because records the earlier instance had not sent are not known.

## Commands

Run these in the project folder (`npx signafaide <command>` in a TypeScript project, `uv run signafaide <command>` or `.venv/bin/signafaide <command>` in a Python one).

- `protect --yes --tool <name> [--limit-field <field> --above <number>]` is yours to run (step 1); `protect` without `--yes` is the user's, in their terminal.
- `status` shows one line per tool (recorded, protected, proof), then the key, the chains and the quota.
- `check <tool> <field>=<value>...` is a dry run: exit 1 when the call would be blocked.
- `pull` fetches the rules and asks the user before a new field is sent; `prove <tool>` gives the auditor link.
- `verify` runs the checks on the local records and prints PASS or FAIL.
- `replay` shows what an agent saw and did, from the local records.
- `flush` sends the waiting records once an API key exists, and does nothing without one.
- `init` creates the external sandbox and from then on sends record hashes to the witness. It is the user's to run, as above: it accepts the Terms (https://signafaide.co.uk/legal/terms) and the Privacy notice (https://signafaide.co.uk/legal/privacy).
- `claim` prints the link the user opens to claim the sandbox. Show it to the user; do not open it yourself.

## MCP tools

The plugin's `signafaide` MCP server is hosted (https://api.signafaide.co.uk/mcp). It reads nothing on this machine, needs no account and changes nothing. `signafaide_quickstart` gives the install command and code for a language and framework, `signafaide_explain_error` explains an error code, `signafaide_check_auditor_link` checks an auditor link, `signafaide_verify_pack` verifies a verification pack sent to it, and `signafaide_service_keys` gives the service's public keys. Recording and checking the project's own records use the commands above, on this machine.
