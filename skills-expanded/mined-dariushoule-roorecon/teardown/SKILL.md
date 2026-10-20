---
name: teardown
description: Cleanly shut down a RooRecon engagement — close the browser, drop the SOCKS proxy and VPN tunnel, tidy runtime scratch out of the working tree, and confirm nothing is left running. Use when the operator says to clean up, shut down, tear down, wrap up, or stop everything at the end of a session. Triggers on "clean up", "shut down", "shut things down", "tear down", "wrap up", "stop everything", "we're done", "end the engagement".
---

# Teardown — clean shutdown of an engagement

Bring everything down in the right order, leave the working tree clean, and keep the
loot. This is the end-of-session counterpart to recon: it stops what's running and
tidies scratch, without throwing away results or the operator's work.

> **Capture lessons before you tear down.** Teardown shuts down infra; it does not
> learn anything. If the engagement surfaced friction worth folding back into the
> skills, run the **retro** skill *first* — while the transcript and `recon-results/`
> are still warm — then tear down.

## Principles

- **Preserve the loot.** Never delete `recon-results/` (recon, vuln-research,
  fingerprints) or `.roo/browser-profile` (the operator's saved login) unless the
  operator explicitly asks for a deep clean. They're git-ignored, so they don't dirty
  the tree — leaving them costs nothing and saves a re-auth / re-scan next time.
- **Leave the BloodHound stack up.** `roo bloodhound` is a *local* analysis platform
  (not on the engagement network) holding the operator's graph — treat it like loot,
  not engagement infra. Tearing down the tunnel does not require stopping it, so
  leave it running by default; stop it only on request (`roo bloodhound down`, or
  `--wipe` to drop the data) or in a deep clean.
- **Don't auto-commit code.** Make the tree *clean to report*, but commit source
  changes only when the operator asks. Commits are solo-authored — no co-author /
  generated-by trailer.
- **Idempotent and quiet.** Only stop what's actually running; a teardown must never
  error because something is already down. Skip steps that don't apply (no browser
  open → nothing to close).
- **Graceful order:** close the browser *before* dropping the tunnel, and drop the
  tunnel **last** — so nothing loses its network out from under it mid-operation.

## Sequence

1. **Close the browser** (if a `roo browser` / CDP session is up). First, if the
   Playwright MCP is attached, call `browser_close` to release the CDP page cleanly.
   Then run **`./roo browser --stop`** — `browser_close` only detaches the page,
   it leaves the host Chrome *process* running, so this is what actually exits it. It
   matches only the dedicated roo profile (`.roo/browser-profile`), never the
   operator's other browsers or the BloodHound stack's browser, and is a no-op if
   nothing is running.
2. **Tidy runtime scratch from the working tree.**
   - The Playwright MCP writes snapshots/console logs/screenshots to `.playwright-mcp/`
     in the cwd. Make sure it's git-ignored (it is, in `.gitignore`), then remove it:
     `rm -rf .playwright-mcp`.
   - `git status --short` — anything left should be intentional. Generated runtime
     dirs (`.roo/`, `recon-results/`) are git-ignored and stay.
3. **Drop the SOCKS proxy:** `./roo proxy down`.
4. **Drop the VPN tunnel (last):** `./roo vpn down` — now off the engagement
   network.
5. **Verify nothing is left:**
   - `docker ps --filter name=roorecon --format '{{.Names}}' | grep -v roorecon-bloodhound`
     → empty (the engagement containers — vpn/proxy/fwd/scanners — are down). The
     `roorecon-bloodhound-*` analysis stack is *expected* to remain unless asked to
     stop; don't flag it as leftover.
   - `git status --short` → clean (or only intentional, operator-approved changes).

## Report back

Tell the operator, plainly, what's down and what was kept:

- Browser closed; SOCKS proxy stopped; VPN tunnel down (off the engagement network);
  no engagement `roorecon-*` containers running.
- Working tree clean.
- **Preserved:** `recon-results/` (loot), `.roo/browser-profile` (saved login), and
  the BloodHound CE stack if it was up (the graph) — note it's still on
  `127.0.0.1:8080` and how to stop it (`roo bloodhound down`).

If the operator asked to commit pending changes, do so (solo author, concise message)
and report the hash. If there are uncommitted source changes you did *not* commit,
list them so nothing is silently dropped.

## Optional deep clean (only if asked)

- Stop + wipe the BloodHound CE stack (graph DB included): `./roo bloodhound
  down --wipe`.
- Remove the saved browser session / generated artifacts: `rm -rf .roo/` (forces
  re-auth and regenerates proxychains/hosts next run).
- Remove engagement results: `rm -rf recon-results/<target>/` — **destructive, confirm
  first.** This is the loot; never do it on your own initiative.
