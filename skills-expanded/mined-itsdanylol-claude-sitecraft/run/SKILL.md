---
name: run
description: Starts a local site or app and looks at it in a real browser. Detects the stack from package.json, config files or a plain index.html, picks a free port, starts the dev server or a static server, waits until it actually answers, screenshots it or opens it, and stops it again with one flag. Use when the user asks to run, serve, launch, preview, start or open a project locally, check a page in the browser, take a screenshot of a site, or when a build needs to be seen before it can be judged.
license: CC-BY-4.0
---

# Run

A site is not finished until it has been seen running. Source tells you what someone intended; the browser tells you what a person gets. This skill is the shortest path between a folder and a rendered page.

## Run it

```
node <skill folder>/scripts/serve.mjs <dir> [--port 4173] [--open] [--shot out.png] [--stop] [--detect]
```

- `--detect` prints what it found and starts nothing. Do this first when the folder is unfamiliar.
- `--port` starts looking there and takes the next free port, so two projects can run at once.
- `--open` opens the default browser.
- `--shot out.png` renders the page at 1440 wide, full height, through Playwright.
- `--stop` kills the process tree from `.run/state.json`.

It writes `.run/state.json` (pid, port, url, command) and `.run/server.log` beside the project. Those two files are the whole handover between the start and the stop.

## What it detects

| Finds | Runs |
| --- | --- |
| `package.json` with `dev`, `start`, `serve` or `preview` | `npm run <that script>` on a free port, with `PORT` set |
| `index.html` in the root | `python -m http.server` on that folder |
| `public/index.html`, `dist/index.html`, `build/index.html` | a static server rooted at the built output |
| A config file but no scripts | reports it and stops: the project needs its own command |
| `go.mod`, `Cargo.toml`, `pubspec.yaml` | reports it and stops: use the project's own run command |

Framework specifics, port defaults and the failure modes worth knowing: [references/stacks.md](references/stacks.md).

## Reading the result

The script proves three things and nothing more: a process started, a port answered, a page rendered. What it cannot tell you:

- whether the layout is right at 375, 768 and 1440 (use `sitecraft/scripts/verify.mjs` for that)
- whether the console is clean (it is not captured here; `verify.mjs` captures it)
- whether the page it screenshotted is the page the user meant (check the URL against the route you asked for)

So the loop is: `serve.mjs --shot`, look at the picture with your own eyes, fix, shoot again. Three renders is the cap for one pass; past that, the problem is the plan, not the CSS.

## Rules

- **Never leave a server running.** Stop it when the check is done, or say plainly that it is still up and on which port. A stray dev server on the user's machine is a mess they have to clean.
- **Do not start what you cannot stop.** If the project needs Docker, a database or a paid API key, say so before spawning anything.
- **Report the real URL.** `localhost:4173`, not "the app". If the port moved because 4173 was taken, say the new one.
- **Read the log before guessing.** A failed start is almost always a missing dependency, a missing env var or a port already bound. `.run/server.log` has the answer, and quoting the actual error beats a theory.
- **No installs without saying so.** If `node_modules` is missing, `npm install` is usually right, and it is also a mutation of their project. Do it, then say it ran, or ask once when the install is large.
- **Static over framework.** When a built output exists and is current, serving `dist/` is faster and truer than the dev server.

## When it will not start

1. Read `.run/server.log` and quote the first real error, not the last line.
2. Missing dependencies: `npm install` in the project, then retry.
3. Missing env: look for `.env.example`, name what is required, and stop if a value is secret and absent.
4. Port already bound: the script already steps to the next free port; a hardcoded port in the framework config is the usual cause when it still fails.
5. Build step required: run `npm run build` first, then serve `dist/`.
6. Native or containerised: hand back the command the project documents. Not every stack is a script.

## Checklist

- [ ] Detected the stack rather than assumed one
- [ ] Started it and saw a real HTTP answer, not just a spawned process
- [ ] Reported the exact URL and port
- [ ] Looked at a screenshot, not only at the log
- [ ] Checked the route matches the page that was meant
- [ ] Stopped it, or said it is still running and where
- [ ] Quoted the real error when it failed
