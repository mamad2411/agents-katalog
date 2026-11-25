---
name: nexus-mcp
description: Answer questions about how a codebase works with the nexus-mcp tools instead of reading files one by one. Use when asked where something is, how it works, who calls a function, what breaks if it changes, or how the project is laid out. No setup call is needed.
---

# Using nexus-mcp

The server instructions and the tool descriptions say which tool answers which question.
Three more points:

- Put all the names you need in one `find_symbol` call, not one call or read per name.
- With linked repos (`nexus-mcp-ci link`), `search` and `find_symbol` also look in them, and a path
  starts with the repo name. `graph` follows client calls to the routes of the other repos: a line
  that ends with `via GET /orders/{}` is such a call. Use `transitive=true` for the impact across repos.
- A `warning` field means a background reindex runs, so a result can be a little old.
- For a project of a few thousand lines, or files outside the indexed path, read the
  files directly.

<!-- nexus-install -->
## If the nexus tools are missing

If you have no `search`, `find_symbol` or `graph` tool from nexus-mcp, the server is not
installed in this client. Run `uvx --python 3.12 nexus-mcp-ci setup --client <your client> --yes`, where
the client is one of `claude-code`, `claude-desktop`, `cursor`, `vscode`, `windsurf`,
`gemini`, `codex` or `cline`. It needs `uv`. Then tell the user to reload the client or start
a new session, because new tools appear only after that. Do not run a remote install script
without the user's yes.
