---
name: readme-upgrade
description: Audit a repo's README and check that what it says is true — title and one-line description at the top, Install/Usage/License sections, a LICENSE file that matches the badge and package.json, relative links and images that exist (with GitHub's case-sensitivity and heading-anchor slugs), http(s) links and badges that respond, and shell commands that call package.json scripts or files that don't exist or still contain placeholders. With --run it executes the safe commands (installs, tests, builds) in a temporary copy of the repo and reports which ones actually work. Use before publishing or open-sourcing a repo, when asked to improve or rewrite a README, or after moving files around.
---

# readme-upgrade

`scripts/readme-check.mjs` is zero-dependency Node 22+. It never changes the repo.

```
node readme-check.mjs                    # README in the current folder
node readme-check.mjs path/to/repo       # or path/to/README.md
node readme-check.mjs path/to/repo --offline              # skip http(s) link and badge checks
node readme-check.mjs path/to/repo --run --timeout 120    # also run the safe commands, in a temp copy
```

Output: a one-line inventory, which sections exist, findings sorted high → info with README line numbers, the `--run` results, and a summary. Exit code 1 if there is a high finding or a command failed.

## Checks
| Severity | Finding |
|---|---|
| high | relative link or image to a file that doesn't exist, or exists with different letter case (works on Windows/macOS, broken on GitHub); an http(s) link that returns 404/410; a command running a package.json script that isn't there (`npm run x`, `npm test`, `pnpm x`, `yarn x`, `bun run x`); a command running a file that isn't in the repo (`node scripts/x.mjs`, `python x.py`, `./x.sh`); README names a license but there is no LICENSE file, or it names a different one |
| medium | no `# Title` near the top, no one-line description under it, no Install / Usage / License section, no LICENSE file; `#anchor` links that match no heading (GitHub slug rules, duplicates get `-1`, `<a name>` counts), anchors into other .md files; http(s) links that time out, fail DNS, or return other errors; badges that don't return an image; package.json `license` that disagrees with LICENSE |
| low | placeholders in commands (`<your-api-key>`, `YOUR_TOKEN`, `your-site.com`, `xxx`); a command whose file exists elsewhere in the repo (the README assumes a subfolder: say which); `curl … \| sh` and `sudo npm install` |
| info | 403/429/999 from sites that block scripts (LinkedIn, X, npm, Medium…) and the 404 GitHub gives logged-out requests for `/stargazers` and `/watchers`, reported as unverified; over 300 lines with no table of contents; a UI project (React/Vue/Vite/Electron/index.html/Streamlit…) with no screenshot or GIF |

Commands come from ```` ```bash/sh/shell/console/powershell/cmd ```` blocks and from `$ ` lines in any block. In console blocks only the `$ ` lines count, the rest is output. `cd` is followed within a block, and `git clone …/name.git` + `cd name` is treated as the repo root.

## --run safety
The repo is copied to the system temp folder without `.git`, `node_modules`, venvs and build caches; the copy is deleted afterwards (`--keep` keeps it). Commands run one by one with `CI=1`, a per-command timeout (the whole process tree is killed), and stop at the first failure within a line. Only these run:
- `npm`/`pnpm`/`yarn`/`bun` `install`/`ci` (no package names), `test`, `build`, and `run <script>` for scripts that exist
- `node <file in the repo>`, `npx <bin already in node_modules/.bin>`, `node --version`
- `python <file>.py`, `python -m pytest|unittest`, `pytest`, `pip install -r <file>`. Python runs inside a fresh venv in the copy, never your global environment.
- `go build|test|vet`, `cargo build|test|check`, `make <target>` (not install/deploy/publish/release/clean/run/serve/dev/start/watch)
- `ls`, `cat`, `echo`, `pwd` inside the copy

Everything else is skipped with the reason: sudo, rm, curl/wget/iwr, git (including push), docker, cloud CLIs, global installs (`-g`), pipes, redirects, `$VARS`, env assignments, commands with placeholders, and scripts named `dev`/`start`/`serve`/`watch`/`preview` or whose body runs a dev server or watcher.

## How Claude should use it
1. Run it (add `--run` when the user wants the commands verified and the project has an install/test step). Fix the high findings first: they are what a new user hits.
2. Then improve the README. Keep what is accurate, cut what isn't. A structure that works: title → one sentence on what it is and who it's for → screenshot/GIF for anything with a UI → Install (requirements with versions, exact commands) → Quick start (the smallest example that works, with its real output) → Features → Configuration (env vars, with where to get each value) → Contributing → License.
3. Stay honest: only list features that exist, only show output you got from a real run, don't add badges for CI or coverage that isn't set up, and mark placeholders clearly with a line saying what goes there.
4. Run the check again after editing (with `--run` if commands changed) and show the user the before/after summary.

## Limits
- Commands are checked statically except under `--run`. Runtime success depends on this machine (OS, installed toolchains, network); a command that fails here may work elsewhere, and vice versa. `npm install` still runs dependency install scripts, as it would for any user.
- Only README.md is audited, not other docs (anchors into other .md files are checked).
- Link checks cover `[text](url)`, reference links, HTML `href`/`src`, and bare or `<https://…>` URLs (GitHub autolinks them), not URLs inside code. They send one HEAD (falling back to GET) per unique URL with a 10 s timeout. Some hosts return 403/5xx to scripts; check those in a browser before reporting them as broken.
- Heading slugs follow GitHub's rules; GitLab and other renderers differ slightly. HTML-only READMEs and reStructuredText are not parsed.
- Section detection is by heading words (Install/Setup/Getting started, Usage/Quick start/Examples, License). A README that explains installation under a different heading gets a false "missing section".
