# Oryntra review in Cursor (current UI)

## What you need (no custom mode)

1. Open **Cursor Settings** (gear tab).
2. Left sidebar → **Plugins** (plug icon) — the page that shows **Agents** / “Meet the new Agents Window”.
3. Scroll to **MCP** (or **Installed MCP Servers**) and enable **oryntra**.  
   - Comes from `.cursor/mcp.json` in this repo.  
   - Run `npm run build` once if oryntra doesn’t appear; then reload the window.
4. In the **Agents** chat (normal **Agent** mode), say: **“Start Oryntra review”**.

That opens Review Studio in the browser. No npm. No custom dropdown mode.

---

## About “Chat” / “Custom modes” in settings

Older docs said **Settings → Features → Chat → Custom modes**.  
In Cursor 3.x that path is often **gone**. Your sidebar may show:

- General · Models · **Features** (star) · **Plugins** (plug) · Beta · …

There may be **no Chat icon**. Custom modes (if your build still has them) are sometimes under:

- **Features** (star icon) — search on that page for “custom”, or  
- **Beta** (flask icon), or  
- The mode dropdown in the agent panel → **Add custom mode** (only if the feature is already on)

**If you can’t find Custom modes anywhere, ignore it.** Use **Agent** + **“Start Oryntra review”** above.

---

## Optional custom mode (only if “Add custom mode” exists in the dropdown)

Name: `Oryntra Review` · Tools: MCP on · Instructions:

```
You are the Oryntra Review agent. When the user wants to review, call MCP collaborate_now. Never tell them to run npm. Read apps/demo-app/.oryntra/review-history.md and implement approved changes.
```
