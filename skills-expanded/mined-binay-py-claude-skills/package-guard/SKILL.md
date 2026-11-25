---
name: package-guard
description: Supply-chain check for packages Claude installs. A PreToolUse hook that reads npm/pnpm/yarn/bun/npx and pip/uv/poetry/pipx install commands, looks each package up on the public npm or PyPI registry, blocks names that don't exist (hallucinated packages, "slopsquatting"), and asks the user first when a name looks like a typo of a popular package, was first published under 30 days ago, has under 100 weekly downloads, is deprecated, or is an obscure package with install scripts. Use when the user wants protection from Claude installing made-up or typosquatted packages, asks whether a package is safe or real, or before running an install command copied from an AI answer.
---

# package-guard

`scripts/package-guard.mjs` is zero-dependency Node 22+. LLMs sometimes invent package names that sound right; attackers register those names. This hook checks the name against the registry before the install runs.

## Install (ask the user first, it changes their settings)
If you installed the binay-skills plugin, this hook is already on (it ships in the plugin's `hooks/hooks.json`); turn it off with `"env": { "BINAY_SKILLS_HOOKS_OFF": "package-guard" }`. Otherwise, without the plugin:

Add to `~/.claude/settings.json` (all projects) or `.claude/settings.json` (one project), with the absolute path to the script:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "node \"/ABSOLUTE/PATH/package-guard/scripts/package-guard.mjs\" hook" }] }
    ]
  }
}
```
Merge into existing `hooks` (it runs fine next to `bash-checkpoint`). Restart Claude Code, check with `/hooks`.

## Check by hand
```
node package-guard.mjs check react expresss pypi:reqeusts     # bare names = npm
node package-guard.mjs check --json lodash pypi:numpy
node package-guard.mjs parse "cd web && npm i -D vite@5 && pip install 'httpx>=0.27'"   # what would be checked (offline)
node tests/run.mjs          # 88 offline tests: parsing, decision rules, fail-open
node tests/run.mjs --live   # +21 tests against the real registries and the hook end to end
```

## What it decides
| Finding | Action |
|---|---|
| Name does not exist on npm / PyPI | **Block** (exit 2): "does not exist on npm — possibly a hallucinated name; did you mean X?" |
| npm security placeholder (`0.0.1-security`, the name was taken down as malware/typosquat, e.g. `lodahs`) | **Block** |
| 1 edit (names of 4–7 chars) or 2 edits (8+ chars) from a popular package, and not itself popular (under 50k weekly downloads and not on the list) | **Ask**: "looks like a typo of express" |
| First published under 30 days ago | **Ask** |
| Under 100 downloads last week (npm; PyPI via pypistats.org when it answers) | **Ask** |
| Latest version has `preinstall` / `install` / `postinstall` **and** under 10k weekly downloads or under 90 days old | **Ask**, naming the scripts |
| Deprecated (npm `deprecated`, PyPI yanked latest or "7 - Inactive") | **Ask** with the deprecation message |
| Anything else, or the registry can't be reached | allow silently (network errors print one line to stderr) |

**Why install scripts only count for unpopular packages:** esbuild, sharp, bcrypt, puppeteer, core-js and cypress all have install scripts and hundreds of millions of installs between them. Asking on every one of them trains people to click yes. The attack this guard targets is a new or obscure package whose `postinstall` runs on install, so that is when it asks. The ~210 npm / ~140 PyPI names in the embedded popular list are never flagged for typos or scripts.

**Parsed:** `npm i/install/add`, `npm init|create x` (→ `create-x`), `npm exec`, `npx`, `pnpm add/i/dlx`, `yarn add`, `yarn global add`, `yarn dlx`, `bun add/i/x`, `bunx`, `pip`/`pip3 install`, `python -m pip` / `py -m pip`, `uv add`, `uv pip install`, `uvx`, `uv tool install/run`, `poetry add`, `pipx install/run`. Versions (`pkg@^2`, `@scope/pkg@1`, `pkg==1.0`, `"pkg>=2,<3"`), extras (`pkg[extra]`), npm aliases (`x@npm:real`), flags with values, compound commands (`cd x && npm i y`), `sudo`, `VAR=1 cmd`, and `bash -c '…'` / `powershell -Command` / `cmd /c` wrappers.
**Skipped:** bare `npm install` / `yarn` / `pnpm install`, `-r requirements.txt`, `-e .`, local paths, git URLs, tarballs and wheels, `user/repo` shorthand, `npx` of a bin already in the project's `node_modules/.bin`, and any command or package using a custom registry (`--registry`, `-i/--index-url`, `.npmrc` `registry=` or `@scope:registry=`, `PIP_INDEX_URL`, `UV_INDEX_URL`, `npm_config_registry`).

Results are cached for 24 h in `~/.claude/package-guard-cache.json` (override with `PACKAGE_GUARD_CACHE`). Each request has a 4 s timeout and the whole hook gives up and allows after 12 s. A cached check takes about 0.25 s, mostly Node startup. Set `PACKAGE_GUARD_OFF=1` to turn it off for one session.

## Limits (tell the user)
- It checks that a name is real and established, not that the code is safe. A hijacked popular package (a stolen maintainer token, like the 2025 chalk/debug compromise) passes. Pair it with lockfiles, `npm ci`, and `--ignore-scripts` for untrusted code.
- It looks at the **latest** version's install scripts and deprecation, not the exact version requested.
- Dependencies of the package are not checked, only the names on the command line. `-r requirements.txt` and `package.json` installs are skipped.
- PyPI has no download counts in its own API. pypistats.org fills that in when it answers; when it doesn't, PyPI checks rely on existence, age, deprecation and the typo list only.
- The typo check only knows the embedded popular list; a typo of a mid-popular package is caught only by the age or download rules.
- A name that doesn't exist yet but is about to be published by you will be blocked. Run the install yourself, or set `PACKAGE_GUARD_OFF=1`.
- `check` with dozens of names can hit the npm downloads API rate limit; download counts then show as unknown.
- It runs on what Claude sends to Bash/PowerShell. A script file that installs things, or an install typed by the user, is not seen.
