# CS Build

An AI-first website builder for small businesses in West Africa (Ghana first). ASP.NET Core 9,
Blazor Server for the builder UI and Razor Pages for the published tenant sites, in one process,
against Postgres. Deployed to Railway from `main`.

## Read these first

- **`docs/HANDOFF.md`** — what is live, decided, or pending right now, and the things a fresh
  session gets wrong without being told. Start here.
- **`docs/PROJECT.md`** — the whole codebase: architecture, multi-tenancy, the site model,
  generation, the shop, configuration reference.

Both are kept current. If you change something they describe, update them in the same pass.

## Working agreements

- **Explain the reasoning behind a change, not just the change.** Why it is the right fix matters
  more than what the diff says.
- **Verify rather than assert.** Run it, read the output, and say plainly what you did *not* check.
  Being told what is unverified is as useful as being told what passed.
- **No AI-attribution trailer in commit messages.** A commit has been rejected purely for carrying
  one. Commit messages are explanatory and multi-paragraph.
- **Don't push deploys or transition shared Jira issues without asking.** The Jira board is shared
  with a collaborator, and its epic statuses drift — derive state from children, not the parent.
- Kofi commits frequently. A clean working tree is normal; check `git log` before assuming
  anything is unpushed.

## Things that will cost you an hour if you don't know them

- **`ui.pen` is encrypted.** Never open it with Read, Grep, or Edit — only the Pencil MCP tools.
- **A Claude subscription is not Anthropic API credit.** Pro, Max and Claude Code fund nothing in
  this app and issue no `sk-ant-` key. This has caused real confusion twice.
- **Railway variables use `__`, not `:`** — `Gemini__ApiKey`, not `Gemini:ApiKey`. A wrongly named
  variable is silent: the startup banner just says the provider is unconfigured.
- **Integration tests need Docker running** (Testcontainers, real Postgres). They are free — the
  test host blanks every provider API key, and `TestHostGenerationTests` guards that. Add any new
  provider's key name to the blanked list in `TenantAppFactory`.
- **Scoped CSS does not reach `MarkupString` content.** Blazor stamps its `b-…` attribute at
  compile time, so a selector written against runtime-injected markup silently matches nothing.
  This shipped twice as oversized icons. Inline SVGs carry their own `width`/`height`.
- **`.mcp.json` configures `chrome-devtools-mcp`.** Use it to look at the running app rather than
  reasoning about what should render — appearance bugs are invisible in the source. The app needs
  to be running (`dotnet run --project src/WebsiteBuilder.Web`).

## Commands

```bash
dotnet build
dotnet test                                    # 441 tests, ~20s, needs Docker
dotnet run --project src/WebsiteBuilder.Web
```
