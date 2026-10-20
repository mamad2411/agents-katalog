---
name: public-link
version: 1.0.0
description: Put something running on this machine (a prototype, a dev server, a rendered preview, a video or a static folder) on a public HTTPS link through a Cloudflare tunnel, only after the user says yes, and report the URL with how to stop it. Load when the work produced something a person views in a browser and they may want to open it on a phone or send it to someone. Not a deploy. Do NOT use for production hosting, for anything holding real credentials or unapproved real data, or to expose a database, admin port or API without its own auth.
---

# Public link (Cloudflare tunnel)

A public link lets a person open what you built on their phone, or forward it to a stakeholder, without a deploy. Anyone with the URL can open it while it runs. That makes it a publish action: it happens only after the user says yes.

## 1. Ask first, once, after it works

- **Timing.** Offer the link only after the thing runs and your own check passed. A link to a broken page teaches nothing.
- **An earlier answer counts.** If the request already says yes or no ("share it", "give me a link", "local only"), act on that and don't ask again.
- **Otherwise, ask once:**
  - Use a direct question tool if you have one.
  - If not, make the question the last item of your report, with the commands from §3 already prepared: "Do you want this on a public link through a Cloudflare tunnel? (temporary trycloudflare.com URL; anyone with the link can open it)".
  - A yes that arrives later as a continuation is the go-ahead.
- **No yes, no tunnel.** Silence, "maybe" and a request for "a link to the files" are not a yes.
- **Unattended run.** Treat the link as a publish gate. Open it only if `autonomy.json` pre-authorizes it (see `autonomy-policy`). Otherwise, record it as a blocked gate with the commands prepared.

## 2. Check before exposing — even with a yes

Refuse, and say why, when the thing to be exposed contains any of these:

- **Real secrets:** credentials, an API key in client code, or a `.env` file inside the served folder.
- **Real data without approval:** customer or personal data that the caller has not confirmed, by name, may go on a public link.
- **Raw services without auth:** a database, admin console, debugger port or internal API that has no auth of its own. Mocked auth is not protection.
- **Media still waiting on review:** footage or audio whose publication approval is still open (people in frame, consent, rights). The owning agent's own gates still apply.

Serve only the project folder, never a home directory or the repository root with its `.git/`.

## 3. Open it

**Serve it locally on 127.0.0.1** and check it before tunnelling:

- **Static folder** (a prototype `index.html`, a rendered preview, a video): `python3 -m http.server <port> --bind 127.0.0.1 --directory <folder>`
- **App with a start command:** run that command, bound to localhost.
- **Vite:** it rejects unknown hosts, so add `.trycloudflare.com` (or the stable hostname) to `server.allowedHosts`.
- **Check:** `curl -sI http://127.0.0.1:<port>` must return 200 before you start the tunnel.

**Quick tunnel (the default).** It needs `cloudflared`, on `PATH` or at `~/.local/bin/cloudflared`.

- If it is missing, say so and give https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/ instead of installing it globally.
- Start the tunnel in the background, then read its URL from the log:

```bash
cloudflared tunnel --no-autoupdate --url http://127.0.0.1:<port> > .tunnel.log 2>&1 &
grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' .tunnel.log | head -1
```

- Poll the log for a few seconds before giving up; the URL appears once the tunnel connects.
- Verify the public URL with `curl -sI <url>`. A new hostname can take a few seconds to resolve.
- Keep `.tunnel.log` out of git.

**Stable hostname.** Use one only when the user asks for it and already has a named tunnel.

- Follow their documented setup, for example a `guide.md` beside their tunnel config.
- **Ask first, for each of these changes:**
  - creating a tunnel;
  - adding a DNS record;
  - editing a shared tunnel's ingress config.
- **Shared tunnels:** restarting one takes every hostname on it offline briefly, so say so before restarting.

**Credentials.** Never read, copy, print or commit anything in `~/.cloudflared/` except a config `.yml` you were told to edit. The `cert.pem` and `<tunnel-id>.json` files are credentials.

## 4. Report it

One line in the report:

`Public link: <url> — server PID <n>, tunnel PID <n>; stop with: kill <n> <n>`

or `Public link: not requested | declined | refused — <reason> | blocked gate — <reason> | asked, awaiting answer`.

- **Say it is temporary.** A quick-tunnel URL dies when the process stops and changes on every restart.
- **Prefer stopping it.** When your session ends, stop the processes unless the user asked you to keep the link up. A forgotten tunnel is a public endpoint nobody watches.
- **Document it.** When the project has a run document (`PROTOTYPE.md`, a README section), add a *Share it* line with the two commands.
