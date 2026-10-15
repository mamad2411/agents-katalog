---
name: Truto Link SDK
description: Embed the Truto connection flow in your frontend using @truto/truto-link-sdk. Covers account connection, RapidForm, file pickers, display modes, and error handling.
---

# Truto Link SDK

Use this skill when embedding the Truto connection UI in a frontend application. This covers installing and using the `@truto/truto-link-sdk` npm package to let end-users connect their third-party accounts.

## What is Truto Link SDK?

The [`@truto/truto-link-sdk`](https://www.npmjs.com/package/@truto/truto-link-sdk) is a **browser-only** JavaScript library that opens the Truto connection UI. It works with any frontend framework (React, Vue, Svelte, vanilla JS) — it's a plain ES module, not framework-specific.

It provides three capabilities:

- **`authenticate`** — Open the connection flow so end-users can link their third-party accounts
- **`rapidForm`** — Open post-connect forms for additional configuration after connection
- **`showFilePicker`** — Open native cloud file pickers (Google Drive, SharePoint, OneDrive, Box, Dropbox)

## Installation

```bash
npm install @truto/truto-link-sdk
```

## Prerequisites

Before using the SDK in the frontend, your **backend** must generate a link token. The Truto API token is secret and must never be exposed to the browser.

```typescript
// Backend route
app.post("/api/truto/link-token", async (req, res) => {
  const response = await fetch("https://api.truto.one/link-token", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.TRUTO_API_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tenant_id: req.body.tenantId }),
  });
  const { link_token } = await response.json();
  res.json({ linkToken: link_token });
});
```

## Quick Start

```typescript
import authenticate from "@truto/truto-link-sdk";

async function connectAccount(tenantId: string) {
  const res = await fetch("/api/truto/link-token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tenantId }),
  });
  const { linkToken } = await res.json();

  try {
    const result = await authenticate(linkToken);
    console.log("Connected:", result.integrated_account_id);
  } catch (err) {
    if (err === "closed") {
      console.log("User closed the dialog");
    } else {
      console.error("Connection failed:", err);
    }
  }
}
```

## API Reference

### authenticate(linkToken, options?)

Opens the Truto Link UI so the end-user can select an integration and authenticate.

**Returns:** `Promise<{ integrated_account_id: string; integration: string }>` — or `undefined` if `sameWindow` is true.

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `integration` | string | — | Pre-select a specific integration (skips the picker) |
| `integrations` | string[] | — | Restrict the picker to these integrations only |
| `iframe` | boolean | `true` | Use a full-screen iframe overlay. Set `false` for a popup window. |
| `sameWindow` | boolean | `false` | Navigate the current page instead of iframe/popup. Use with `redirect_uri` on the link token. No Promise is returned. |
| `noBack` | boolean | `false` | Hide the back button on the integration auth screen |
| `authFormat` | string | — | Force a specific auth flow: `api_key`, `oauth2`, `oauth2_client_credentials`, `keka_oauth` |
| `skipRapidForm` | boolean | `false` | Skip the post-connect form (RapidForm) even if one is configured |
| `baseUrl` | string | `https://app.truto.one` | Override the Truto app URL |
| `width` | number | 700 | Popup window width (only when `iframe: false`) |
| `height` | number | 800 | Popup window height (only when `iframe: false`) |

#### Display Modes

| Mode | Option | Behavior |
|------|--------|----------|
| **Iframe** (default) | `iframe: true` | Full-screen overlay on `document.body`. User connects inline. |
| **Popup** | `iframe: false` | New browser window. Useful when iframes are restricted. |
| **Same-window** | `sameWindow: true` | Navigates the current page. No Promise returned. Set `redirect_uri` on the link token. |

#### Error Handling

| Rejection Value | Type | Meaning |
|----------------|------|---------|
| `"closed"` | string | User closed the dialog without connecting |
| `"blocked"` | string | Browser blocked the popup window |
| Error with `error_type` | Error | Connection error from Truto (see error types below) |

**Error types** (on `err.error_type`): `invalid_token`, `invalid_integration`, `connection_error`, `post_install_error`, `validation_error`

Additional properties on the Error object: `err.integration` (integration name), `err.integrated_account_id` (if the account was created before the error).

### Pre-selecting Integrations

```typescript
// Skip the picker — go directly to HubSpot auth
const result = await authenticate(linkToken, { integration: "hubspot" });

// Restrict the picker to specific integrations
const result = await authenticate(linkToken, {
  integrations: ["hubspot", "salesforce", "pipedrive"],
});
```

## Framework Recipes

The SDK is a plain ES module — these are thin wrappers, not separate packages. Pick the one that matches your stack.

### React — `useTrutoLink` hook

```typescript
import { useState, useCallback } from "react";
import authenticate from "@truto/truto-link-sdk";

type ConnectArgs = { tenantId?: string; integratedAccountId?: string };

export function useTrutoLink() {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const connect = useCallback(async (args: ConnectArgs) => {
    setPending(true); setError(null);
    try {
      const res = await fetch("/api/truto/link-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(args),
      });
      const { linkToken } = await res.json();
      return await authenticate(linkToken);
    } catch (err) {
      if (err !== "closed") setError(err);
      throw err;
    } finally {
      setPending(false);
    }
  }, []);

  return { connect, pending, error };
}
```

Usage:

```tsx
function ConnectButton({ tenantId }: { tenantId: string }) {
  const { connect, pending } = useTrutoLink();
  return (
    <button onClick={() => connect({ tenantId })} disabled={pending}>
      {pending ? "Connecting…" : "Connect an account"}
    </button>
  );
}
```

### Vue 3 — composable

```typescript
import { ref } from "vue";
import authenticate from "@truto/truto-link-sdk";

type ConnectArgs = { tenantId?: string; integratedAccountId?: string };

export function useTrutoLink() {
  const pending = ref(false);
  const error = ref<unknown>(null);

  async function connect(args: ConnectArgs) {
    pending.value = true; error.value = null;
    try {
      const res = await fetch("/api/truto/link-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(args),
      });
      const { linkToken } = await res.json();
      return await authenticate(linkToken);
    } catch (err) {
      if (err !== "closed") error.value = err;
      throw err;
    } finally {
      pending.value = false;
    }
  }

  return { connect, pending, error };
}
```

### Svelte — action

```typescript
import authenticate from "@truto/truto-link-sdk";

type Args = { tenantId?: string; integratedAccountId?: string };

export function trutoLink(node: HTMLElement, args: Args) {
  const handler = async () => {
    const res = await fetch("/api/truto/link-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(args),
    });
    const { linkToken } = await res.json();
    try {
      const result = await authenticate(linkToken);
      node.dispatchEvent(new CustomEvent("trutoConnected", { detail: result }));
    } catch (err) {
      if (err !== "closed") {
        node.dispatchEvent(new CustomEvent("trutoError", { detail: err }));
      }
    }
  };
  node.addEventListener("click", handler);
  return { destroy: () => node.removeEventListener("click", handler) };
}
```

Usage:

```svelte
<button
  use:trutoLink={{ tenantId }}
  on:trutoConnected={(e) => console.log(e.detail.integrated_account_id)}
>
  Connect an account
</button>
```

### Backend link-token routes

The frontend recipes above all call the same backend route. For Express, Next.js Route Handlers, and Hono / Cloudflare Workers variants of that route, see [Getting Started — Step 5](../truto/references/getting-started.md#step-5--write-the-link-token-route-in-your-app) in the Truto skill.

## References

| Reference | Content |
|-----------|---------|
| [RapidForm & File Pickers](references/rapidform-and-file-pickers.md) | Post-connect forms, native cloud file pickers, advanced options |

## Related Skills

- **Truto** skill — For writing backend API calls, handling webhooks, and the overall integration architecture
- **Truto CLI** skill — For admin setup and debugging in the terminal
