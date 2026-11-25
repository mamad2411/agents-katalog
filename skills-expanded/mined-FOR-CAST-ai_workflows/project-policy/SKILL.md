---
name: project-policy
description: Create or update .claude/r-project-policy.json, the per-repo policy file that drives this plugin's guardrails -- pinned R binary, package-install discipline, air opt-out, publish approval, control-node hosts, and long-run process patterns. Use when setting up a repo, or when a guardrail is firing wrongly or not firing at all.
argument-hint: "[optional: repo path]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash(git -C:*), Bash(jq:*), Bash(cat:*), Bash(ls:*), Bash(hostname:*), Grep, Glob
---

# Project policy file

The guardrails in this plugin ship the *mechanism*; each repo declares its own
*policy*. That split exists because these projects genuinely disagree with each
other, deliberately:

- `air format` is mandatory in most repos and **explicitly forbidden** in a few
  whose HEAD is not air-clean;
- R is pinned to different versions, and some repos pin nothing;
- some projects install exclusively through `renv`; others do not;
- only some machines are control nodes.

Hardcoding either side of any of these would be wrong somewhere. An absent policy
file means "no opinion": only the universally-safe guards stay active.

## Write it to `<repo>/.claude/r-project-policy.json`

```json
{
  "rBinary": "Rscript-4.6.1",
  "packageInstall": "renv",
  "noAirFormat": false,
  "publishRequiresApproval": true,
  "controllerHosts": ["control-node-name"],
  "hostPatterns": ["control-node-name", "worker-node-name"],
  "longRunPatterns": ["tar_make", "DEoptim", "spades", "landis"],
  "heavyCommands": ["tar_make", "quarto render", "devtools::check", "docker run"],
  "asciiExtensions": ["R", "qmd", "Rmd", "bib"]
}
```

| Key | Effect when set |
| --- | --- |
| `rBinary` | a bare `Rscript`/`R` call gets a non-blocking note naming the pinned binary |
| `packageInstall: "renv"` | denies `install.packages()`, `devtools::install*`, `remotes::install_*`, `BiocManager::install()`, `pak::pak()`/`pkg_install()`/`local_install()`, `Require::Install()`, `setupProject()`, and bare `renv::snapshot()` |
| `noAirFormat: true` | denies `air format` in this repo |
| `publishRequiresApproval: true` | forces a permission prompt -- even in auto mode -- for `git push`, `gh` writes (pr/issue/release/repo changes, `workflow run`), `gh api` writes including the implicit POST of `-f`/`-F`/`--input` without a method, `gh extension install`, and MCP tools whose names say they write or run code |
| `controllerHosts` | denies heavy compute when `hostname -s` matches one of these, unless the command is an `ssh` dispatch |
| `heavyCommands` | overrides what counts as heavy for `controllerHosts` |
| `hostPatterns` | asks before a machine name reaches a commit message, a PR or issue body, release notes, the staged diff, or a tracked file. Gitignored files and `ssh` destinations are exempt |
| `longRunPatterns` | what the live-run interlock and the SessionStart report look for |
| `asciiExtensions` | which file types the ASCII guard covers (default `R r qmd Rmd rmd bib`) |

## How to fill it in for a repo

1. **`rBinary`** -- read it from the project's own docs, or infer from `renv.lock`:
   ```sh
   jq -r '.R.Version' renv.lock       # e.g. 4.6.1  ->  "Rscript-4.6.1"
   ```
   Only set it if the project actually installs versioned binaries (rig-style).
2. **`packageInstall`** -- set `"renv"` if `renv.lock` is present and the project
   treats it as the source of truth.
3. **`noAirFormat`** -- set `true` only if the repo says so, or if
   `air format --check .` reports a large diff on an untouched tree. Check:
   ```sh
   air format --check . 2>&1 | tail -5
   ```
4. **`controllerHosts`** -- the machine that schedules work and hosts the user's
   interactive session. If the project has an `_hosts.R.example`, the control node
   is the one *not* in the worker list. Ask if unsure; getting this wrong either
   blocks legitimate work or fails to prevent an OOM.
5. **`publishRequiresApproval`** -- default this to `true`. Turning it off should
   be a deliberate decision by the user, not an inference.
6. **`hostPatterns`** -- every machine the user works on, including the controller.
   Set it where infrastructure identity is meant to stay private. Expect prompts if
   a name is also an ordinary word in the domain (a genus, a place, a person); that
   is the guard working, since only a person can tell those apart. Narrow the
   pattern (`"nodename\\."`, or the fully qualified name) if the noise outweighs
   the protection.

## Verifying it works

```sh
jq empty .claude/r-project-policy.json          # valid JSON
```

Then start a new session: the `SessionStart` hook prints the policy it loaded, the
node's role, and any long-running processes already on the host. If a guard fires
when it should not, the fix is almost always a policy value, not a code change --
report which key and why.

## Do not commit machine-specific values by mistake

`controllerHosts` and `hostPatterns` name real machines. If the repo's convention is that
infrastructure identity stays out of version control (`_hosts.R` gitignored, and
comments referring to roles rather than machines), put this file in
`.claude/settings.local.json` territory instead: add
`.claude/r-project-policy.json` to `.gitignore` and keep a
`.claude/r-project-policy.json.example` tracked alongside it.
