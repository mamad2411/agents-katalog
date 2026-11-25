---
name: mac-preview
description: Open a running local website from a devbox session in the browser on the mac. Use when the user says "show it on the mac", "open it in the browser on the mac", "preview on the mac", "show/open the web on my mac" — typically after starting a dev server (npm run dev, Vite, Next…).
---

# mac-preview

Opens a website running in the devbox container in the browser on the user's mac.

## When to use

The user wants to see a running local website (dev server) on their mac — e.g. after
`npm run dev`. Phrases: "show it on the mac", "open it in the browser on the mac",
"preview on the mac", "show it on my mac".

## How

Run in the container session:

```
preview [port] [/path]
```

- `preview` without a port → autodetects the running server (exactly one → opens it;
  several → prints a list and wants a port; none → help).
- `preview 3000` → a specific port. `preview 3000 /admin` → with a path too.

It prints `▸ preview: http://…` and opens it in the browser on the mac.

## Mental model (why it works)

- The session publishes container ports **3000–3009** to the tailnet; the mac is in the same
  tailnet, so it opens the URL directly.
- `preview` handles two footguns automatically via a **relay**: when the server listens only
  on `127.0.0.1` (Docker does not let that out) or runs on a port outside 3000–3009
  (e.g. Vite 5173), `preview` starts a lightweight relay on a free published port. There is no
  need to configure anything or to start the server with `--host`.

## Limitations

- Works only **inside a devbox session** (the `DEVD_SESSION_ID` variable). On the mac itself,
  `preview` does not exist — do not run it there.
- Several running servers → specify the port explicitly.
- When the mac is offline / outside the tailnet, `preview` prints the URL to open manually.
