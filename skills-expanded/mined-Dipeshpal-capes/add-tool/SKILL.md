---
description: Add a new MCP tool, or a whole new service integration, to Capes following the project conventions
argument-hint: <service> <tool_name> (for example: slack slack_send_message)
disable-model-invocation: true
---

Add the tool described by `$ARGUMENTS` to this repository.

1. Read `.claude/rules/tools.md`, `.claude/rules/dashboard.md`'s database section, and the module closest to the new service (`pulse/discord.py` for REST APIs, `pulse/gmail.py` for blocking libraries needing the `ContextVar` pattern).
2. If the service is new, create `pulse/<service>.py` from `${CLAUDE_SKILL_DIR}/template.py.txt` and import it in **both** `api/index.py` and `scripts/gen_tools_doc.py` (it has its own separate `pulse` import list -- easy to update one and forget the other; `tests/protocol.py` catches it if you do). Register it in `pulse/connectors.py` (a `Connector(...)`, leave `db_backed` at its default `True` unless there's a real reason not to). If the service already exists, add the function to its module.
3. Pick the honest `hint` (`read`, `write`, `destructive`). Write a description a language model can act on, with argument descriptions and enums.
4. Read secrets with `await creds.get("NAME")` inside the function (checks the database, falls back to the env var of the same name) -- not `os.getenv` directly. Raise `ToolError` with a fix-it message when a token or permission is missing.
5. Add the env vars to `.env.example`, `docs/setup/vercel.md`, and the installer prompts in `scripts/capes.mjs` (both `install()` and `addEnv()`) if the service needs credentials.
6. Add tests: offline where possible (see `tests/gmail_offline.py`, which fakes the remote server), otherwise an opt-in end-to-end script that never runs against real user data by default.
7. Documentation: run `python scripts/gen_tools_doc.py` to regenerate `docs/usage/tools.md` (never hand-edit it), then `docs/setup/<service>.md` (how to get the credentials and permissions), a row in the README services table, the tool names in the README tool list, and a line in `docs/usage/troubleshooting.md`.
8. Verify: run `/run-tests`, then `python tests/check_docs.py`, then confirm `tools/list` contains the new tool.
9. Report what you added, what you tested, and anything you could not test.

Do not put real credentials, IDs or personal data anywhere in the repository.
