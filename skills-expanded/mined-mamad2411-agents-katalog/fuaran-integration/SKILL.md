---
name: fuaran-integration
description: Wire Fuaran generative UI into an app — let users describe UI in natural language and have it render. Use when the developer wants to add a "describe a dashboard / form / panel and render it" capability, integrate the Fuaran generation endpoint, or set up the call → render → repair turn-loop. Drives the bundled Fuaran MCP tools (recipe, generate, validate, scaffold).
---

# Add Fuaran generative UI to an app

This skill takes a developer from "I want users to describe UI and have it
render" to a wired, compiling integration in one session. It drives the bundled
Fuaran MCP server tools: `recipe`, `generate`, `validate`, `scaffold`.

## When to reach for this

The developer wants any of: "let users describe a dashboard and render it", "a
prompt→UI panel", "generate a form from a description", "AI-authored UI in my
app". Fuaran is the fit: an LLM emits a **canonical wire-format JSON tree**, a
renderer draws it, and each subsequent prompt is a cheap **repair diff** against
the last tree.

## The integration playbook

Follow these steps in order. Prefer the MCP tools over hand-writing.

1. **Detect the stack + pattern.** Identify the app's stack (React/TS or F#/Fable)
   and how secrets should reach the endpoint:
   - **server-proxied** (default, and required for browser apps): the browser
     calls _your_ same-origin proxy route; the proxy injects the access token +
     BYOK key server-side, so no secret ever reaches the bundle.
   - **browser-BYOK**: only for a trusted/desktop context where the user supplies
     their own key at runtime — never a bundled literal.

2. **Look up a recipe.** Call the `recipe` tool with the intent (e.g. "dashboard
   metric strip", "sign-up form") to get the canonical prompt shapes and the
   target tree. This grounds what "good" output looks like for the pattern.

3. **Scaffold the integration.** Call the `scaffold` tool with
   `target: ts-react | fsharp-fable` and the chosen `pattern`. It emits the
   files that wire the `@fuaran-ui/client` SDK call, the renderer, the turn-loop,
   and the secret handling. Write the emitted files into the app and run the
   listed install command.

4. **Wire the turn-loop.** The integration holds the current tree; the first
   prompt is a fresh generation, each next prompt is a repair against the held
   tree. Use the SDK session helper (`FuaranSession` / `useFuaranGenerate`) so
   this is automatic — do not regenerate from scratch each turn.

5. **Validate emissions.** When debugging a bad render, call the `validate` tool
   on the wire JSON to get canonical schema diagnostics (which node/field is
   malformed) rather than guessing.

6. **Develop offline first.** If no endpoint/token is configured yet, point the
   SDK at the local mock — `npx @fuaran-ui/mock` — and build the whole loop with
   no token and no BYOK spend, then swap the base URL to go live.

## Safe defaults (enforce these)

- **Never commit the BYOK key or the access token.** They come from the plugin's
  user config (OS keychain / credentials store) or the app's server-side env —
  never a literal in the repo or the client bundle.
- **Server-proxy the key for any browser app.** The browser-BYOK pattern is only
  for a trusted runtime where the user supplies their own key.
- **Corpus contribution is opt-in.** Never enable `contributeCorpus` on the
  developer's behalf; leave it off unless they explicitly ask.

## Definition of done

The app compiles and renders a tree produced from a prompt; the turn-loop carries
the tree so follow-up prompts are cheap repairs; secrets live in config/env, not
the repo; and (for a browser app) the key is server-proxied.
