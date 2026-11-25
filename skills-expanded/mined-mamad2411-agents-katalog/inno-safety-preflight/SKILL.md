---
name: inno-safety-preflight
description: Use when the user wants their app checked before shipping ("run the safety preflight", "is this safe to ship?", "check my app"). Pushes to the default branch, which runs the platform's REAL safety gates and deploys nothing, then narrates the results with realtime guidance, plus a guardrails policy review. A failure or guardrails violation is a hard stop before inno-ship.
---

# inno-safety-preflight

## Version gate: do this first

Before anything else in this skill, do these five steps in order.

1. If no `inno-platform` tools are available at all, the platform address is
   probably unset. Tell the user to open their platform's panel, copy the
   configure command from its Connect Claude Code card, run it in a terminal,
   and restart Claude Code. Then STOP.
2. Read the `version` field of `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
   and call the `get_platform_status` MCP tool with it as `plugin_version`.
3. If the `Plugin:` line says `OUTDATED`, `version not reported`, or
   `reported version is not a MAJOR.MINOR.PATCH triple`, STOP. Tell the user
   to run the commands that line gives, then restart Claude Code and start
   again. Do not continue on a stale plugin: its guidance may describe
   platform behavior that no longer exists. If there is no `Plugin:` line at
   all, the platform sets no minimum version: go on to the next step.
4. If the `Plugin:` line says `current` and adds that a newer version
   `is available`, that is advice, not a block. Mention it once, with the
   commands from the `Update commands:` line, and go on to the next step.
5. If the status has no `Template repo:` line, the platform is older than
   v0.15.8. Say so, ask the user's admin to upgrade it, and STOP before any
   step that needs an instance value. Never fall back to a literal value.

Carry on.

Deploys are release-driven on this platform: **a push to the default branch
runs every safety gate and deploys nothing**. That run, on the platform's
own runners, with the exact pinned tool versions and the admin-configured
gate policy, IS the preflight. Never install or run scanners locally: local
results drift from CI's and know nothing about centrally-configured ignores
or gate toggles.

**Know the policy that applies to THIS app before you narrate anything.** Call
`get_config app=<name>`: the app's owner can read it, no admin needed. It
gives you the actual `safety.gate.*` toggles, the `safety.a11y.mode` in
force, the `safety.min_release_age_days` cooldown in force, and any
`safety.ignore.<semgrep|trivy|deps|a11y>.<id>` suppression written at this
app's own scope, platform-wide ones being withheld by design. Each row gives
the value, where it came from, who set it and why, and the key's meaning on
the line under it, an ignore's expiry rule included. Read it, don't assume
the defaults:

- A gate an admin turned off still runs as a job and reports success,
  logging a loud `SAFETY GATE DISABLED` warning instead of scanning. For
  `gitleaks`, `semgrep` and `deps` that means nothing is scanned at all. The
  `trivy` toggle is narrower, because it skips only the image CVE scan: the
  container job still builds the image, uploads the SBOM, asserts a
  non-root user and `EXPOSE 8080`, and runs the `/healthz` smoke test. So a
  green gate is not proof that a scan actually happened.
- A finding you expect to be ignored may fail because its ignore's date has
  passed, and one you expect to fail may be suppressed until a date still to
  come. Tell the user while there's still time to act: "that CVE is ignored
  until 2026-12-31, after which this deploy stops passing".

Six things are checked here. **The first four are hard requirements before
`inno-ship`**; the last two are advisory:

1. The **safety gates** (CI): eight jobs, all `needs:` prerequisites of
   `deploy`, plus the `policy` job that fetches the admin gate policy:
   `config-integrity`, `secrets` (gitleaks), `sast` (Semgrep), `deps` (the
   dependency audit), `dep-age` (the dependency-release-age cooldown),
   `container` (run for `container` and `mcp-container` apps only; the
   function-shaped `function` and `mcp-function` types skip it),
   `scaffold-check` (suppresses deploy while the `app/.needs-build` template
   marker is still present) and `app-deps` (installs a function-shaped app's
   `app/package.json` from its lockfile, on every push as well as at the
   tag). What each gate enforces is the contract's to state, not this
   skill's: R7 for `config-integrity`, R8 for the scanners and the cooldown,
   R1 and R2 for the `container` job's image checks and its `/healthz` smoke
   test, R9 for the scaffold marker, and §1.1's **Dependencies** bullet for
   `app-deps` (§1 below says which sections to fetch). After its smoke test
   the `container` job also writes the reports item 6 reads; only the
   accessibility report can turn the job red, and only in `enforce` mode.
2. The **guardrails policy** (you): a qualitative read of the app against
   the platform's acceptable-use policy.
3. The **application contract** (you): the app's conformance to the
   platform's runtime requirements that CI can't see.
4. The **app-code security notes** (you): the app-level risk classes the
   perimeter can't close, authorization and IDOR above all.
5. **Declared variables** (you, repo-local; **advisory**): if
   `app/inno-variables.json` exists, whether it's well-formed and whether
   any name it marks `required` still has no value. §1b is the plugin's
   statement of what CI enforces about it, what you check, and what is the
   user's decision.
6. **Accessibility review** (you, plus CI's reports; **advisory**): the app's
   browser pages against `get_app_accessibility`, a keyboard pass, and the
   accessibility, response-header and Dockerfile reports the `container` job
   writes. In the default `report` mode nothing here blocks `inno-ship`.
   When an admin has set the app's `safety.a11y.mode` to `enforce`, a
   blocking accessibility finding fails the `container` job, and that red
   gate is item 1's hard stop. How to run it and read the reports is §1c.

## 1. Guardrails, contract and security review (do this while CI runs, or first)

Call the `get_guardrails` MCP tool and re-read the app against it: name,
stated purpose, what the code actually does, and how it handles data. You
have the whole repo in front of you; this is judgment, not grep.

- **Clean** → say so in one line and move on.
- **Violation** → HARD STOP. Name the specific policy line, explain the
  conflict plainly, and do not proceed to `inno-ship` until the app is
  changed or the user has an explicit admin exception (they arrange that
  with a platform admin; you cannot grant it). This applies even if every
  CI gate is green.

Then call the `get_app_contract` MCP tool with `sections: ["2", "5", "6"]`
(the requirements R1 to R9, the deployment patterns with what is not
supported today, and the enforcement map). Add to that call the app's own
shape section: `"1.1"` for a `function` app, `"1.1"` and `"1.2"` for an
`mcp-function` app, `"1.3"` for an `mcp-container` app (a `container` app
adds none: section 2 is its baseline). Add to it too `"2.1"`, `"2.2"` or
`"2.3"` when the app links data, uses a connection or declares variables.
If `get_app_contract` refuses the arguments, or the platform is older than
v0.16.14, call it with no arguments and read the sections needed from the
whole contract. Judge the app
against the MUSTs, focusing on the ones the enforcement map (§6) leaves to
preflight review because CI cannot judge them: R3 (identity only from the
gateway headers, no home-grown auth), R4 (the sign-out link; not applicable
to `mcp-function` and `mcp-container` apps), R5 and R6 (durable state in the
platform stores, never local disk or memory), and the parts of R2 CI cannot
see (its smoke test only proves `/healthz` answers inside the image, so
still read it for cheap, no side effects, and independent of storage). Check
too that the app relies on nothing §5 lists as not supported today. A
contract violation is the same hard stop as a guardrails one: name the
requirement, fix or guide the fix, re-check.

Finally, call the `get_app_security` MCP tool and review the app's code
against the sections that apply to it. Its closing **How to use this**
section says which sections a given app may skip, and anything rendered in
a browser keeps some of them, so no browser-facing app skips the review.
CI's scanners catch injection patterns and known-vulnerable deps, but the
highest-impact app bug, **authorization and IDOR** (its §1), is invisible to
them; for any app with **per-user data, an admin surface, a state-changing
write, or a call to a paid or external upstream**, verify its §1 to §5
against the code, and for a browser-facing app (`container`, `function`)
with a state-changing request, its §12 (forged requests, from platform
v0.16.19; on an older platform, the CSRF paragraph under its **What the
platform already handles** heading, which names the same two obligations)
too. That `X-Forwarded-User` is an email address, which can
pass to another person (the contract's R3, or on a platform before v0.16.12
`inno-platform-conventions`' **Identity** section), is not a finding on its
own: no header carries the account itself yet. Per-person data or a role
taken from a caller with no user is a finding, and so is an MCP app that
refuses by HTTP status (a MUST of the contract's §1.2 and §1.3 from
contract 32; on an older platform it is a finding to fix, not a contract
violation). A real authorization hole is a hard stop: fix or guide the fix
before `inno-ship`.
A missing response header (its §9) is a recommendation, not a stop: offer
the fix, and for a `container` app item 6's header report shows what the
app sends today.

## 1b. Declared variables (repo-local, advisory)

If the repo carries `app/inno-variables.json`, this is the plugin's rule for
it; `inno-ship`'s **Declared variables** section applies the same one before
the tag. What the platform does with the file is the contract's §2.3, in
its **Secrecy.** and **Declaring what an app wants** paragraphs
(`get_app_contract` with `sections: ["2.3"]`).

- **What CI enforces: nothing that blocks.** No gate reads the file, and no
  push does. Only the tag's `deploy` job reads it, and neither a bad file
  nor a `required` name with no value fails a gate or stops the deploy.
- **What you check:** the file against §2.3's rules (the name rule and the
  reserved names, from **Secrecy.**; the three allowed fields with their
  defaults and their types, and the 32-entry cap, from **Declaring what an app
  wants**: `required` and `secret` must each be a JSON boolean and
  `description` a JSON string, so a value such as `"true"`, `1` or `null` is
  refused, never coerced, and the platform keeps the previous declarations)
  and, for every `required: true` name, whether it already has a value
  (`list_app_variables`, or `app_status`, which names an unset required one
  directly).
- **What is the user's decision:** whether to fix the file or set the value
  before tagging. Report what you found beside the verdict (**Done**,
  below), never as a blocker: it is purely advisory, and it is the only
  warning an author gets before their first deploy leaves a required key
  silently unset.

## 1c. Accessibility review (advisory: start while CI runs, then read its reports)

Who this covers is `get_app_accessibility`'s **Who this applies to**. A
`function` app has no container for CI to run, so this review is its only
check. For an MCP app (`mcp-function`, `mcp-container`), or a `container`
app that serves no HTML at all (an API), say in your summary that the
review does not apply, rather than listing it as a pass. Every
container-shaped app, `mcp-container` included, still gets CI's Dockerfile
report.

**While CI runs:**

1. Call `get_app_accessibility` and review the app's pages against it. Fix
   what you find (or guide the fix), and fold it into the next push.
2. Do a keyboard pass of a couple of minutes on a running copy of the app
   (the live one if it is deployed, or a local run): Tab through every
   page and check that everything can be reached and operated, and that you
   can always see where focus is. If you cannot drive a browser yourself, ask
   the user to do it and tell them what to look for.
3. CI always scans `/`. To cover more of a `container` app, list pages that
   render **without stored data** (the CI run has none) in
   `app/inno-a11y.json`; the served notes give its format and limits. The
   file only adds pages, so it never stands in for `/`.

**After CI** (a container-shaped app), read the reports in the GitHub Actions
run. They live only there, never on the platform, and in `report` mode their
step is green, so neither `get_ci_status`'s job conclusions nor `gh run view
--log-failed` shows them:

- Open the run link `get_ci_status` returns: the run's summary page carries
  in full each report the run wrote (the accessibility counts by impact and
  its per-route table, the response headers, and the Dockerfile findings).
- With `gh`: `gh run view <run-id>` lists the first findings as annotations
  (GitHub shows at most 10 of each kind per step, so the rest are only in
  the summary), and `gh run view <run-id> --log` carries one count line per
  report, beginning `a11y:` and `dockerfile-report:`.

There is no report when the `container` job failed before its smoke test
passed, or when the app's `safety.a11y.mode` is `off` (the run warns
`Accessibility check off` instead). `Accessibility scan did not run` means
no page was scanned, which is never a clean result; read the reason it
gives. Which reasons are the platform's (they never block) and which are the
app's (they block only in `enforce` mode, where the job also fails with
`Accessibility check failed`) is `get_app_accessibility`'s **What CI checks,
and what it cannot**.

Translate them for the user, in plain terms (the plugin README's **House
style** section):

- **Accessibility findings:** fix critical and serious ones first; each
  names its rule and links an explanation of the fix.
- **Not scanned:** a page listed as not scanned was not checked, which is
  never the same as clean. A 5xx there usually means the page needs stored
  data, which CI does not have; it never blocks.
- **Response headers and Dockerfile findings** never block (the header
  report runs inside the accessibility scan, so it is absent when the mode is
  `off`): explain each in one sentence and offer the fix (`get_app_security` §9 for
  the headers, `inno-containerize` for the Dockerfile).
- **In `enforce` mode** a blocking finding fails the `container` job with
  `Accessibility check failed`; §3's table has the row.

Say plainly what a tool checked, what you checked by hand, and what was not
checked. Never call the app "accessible" or "WCAG compliant" because the
report is clean: a tool finds only part of the problems, as the served notes
explain. A rule that is wrong for this app is waived by a platform admin
(`safety.ignore.a11y.<rule-id>`), never worked around in the page.

## 2. Push and watch the gates

Before pushing, look at `.github/workflows/deploy.yml`. If it has a
`secrets: inherit` line (repos made from older copies of the template do), the
`sast` gate will fail on it: tell the user, and with their okay delete that
line as part of this push. Nothing else in the file changes.

**Confirm the branch before pushing.** The `deploy.yml` `register_app` handed
back triggers gates only on pushes to the repository's default branch (a `v*`
tag deploys from any branch). Compare `git branch --show-current` against
`gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`; if they
differ, do not push blind, tell the user the gates only run on the default
branch, and ask whether to switch to it or merge there first.

This branch check, the symlink check below, and the reading of
`get_ci_status` after it are the plugin's one copy; `inno-ship` and
`inno-migrate-app` point here for them.

```bash
git add -A

# Committed DIRECTORY symlinks fail config-integrity (check 1c) and there is
# no policy toggle for it. Run this AFTER `git add -A`, so the index covers
# both already-tracked links and ones you are about to commit, and so
# gitignored app/node_modules (which npm fills with directory links) drops
# out on its own. A link to a FILE is legal, so classify rather than reject
# on mode alone: -d and -e follow the link, which is the test the gate makes.
git ls-files -s | awk '$1 == "120000"' | cut -f2 | while IFS= read -r l; do
  if   [ -d "$l" ];   then echo "BLOCKED (directory link): $l -> $(readlink "$l")"
  elif [ ! -e "$l" ]; then echo "BLOCKED (dangling link):  $l -> $(readlink "$l")"
  fi
done

git commit -m "<why-focused message>"   # if uncommitted work
git push origin HEAD
```

Nothing deploys from this push. Watch the run either way:

- **MCP (no gh needed):** call `get_ci_status` with the app name: it returns
  the run status, the run link, and each gate's conclusion. Its first line
  also names the branch and commit the run is for ("... on «<branch>»,
  commit `<sha>`"), with the branch fenced in «» guillemets because anyone
  who can push to the repo chooses it; with no `run_id` it
  returns only the latest `deploy.yml` run, so check that commit (or branch)
  against `git rev-parse --short HEAD` before narrating a green or red
  result as the answer for this push, not a stale one. File:line failure
  annotations normally do not come through (the tool's description says
  why), and a failed job's line points at the run link instead: narrate
  from the job conclusions and that link (or `gh run view --log-failed`).
  Refusals worth recognizing: `app_not_installed` (the user reinstalls the
  App on the repo on GitHub), `repo_not_linked` (registration never
  finished), and a platform-side GitHub App fault (`github_app_not_configured`,
  `github_app_key_invalid` or `installation_token_failed`), which only a
  platform admin can fix: tell the user it is not theirs to fix, and watch
  the run with the `gh` CLI below meanwhile. The refusals any platform tool
  can give are named once, in the platform MCP server's instructions.
  Poll every ~30s while `in_progress`; narrate transitions ("secrets ✓,
  container still building…"). Polling that slowly is well inside the
  platform's call budget, but never poll the same run from several subagents
  at once: the budget is per person, not per agent. The rule is
  `inno-manage-app`'s **Call budget** section.
- **gh CLI (if authenticated):** `gh run watch` from the repo.

## 3. Translate the results: this is the actual product

For each gate, tell the user what happened in THEIR terms. Plain terms, no
provider or product names unless they have shown technical fluency; the full
rule is the plugin README's **House style** section.

| Outcome | What you say / do |
|---|---|
| All green | "All safety gates passed. Run `/inno-ship` when you're ready to release." |
| **Real finding** (SAST/deps/CVE) | Show the file:line if the annotations came through. If they didn't, open the run link yourself (or run `gh run view --log-failed` when the user has `gh` authenticated) and read the failing step. Explain the risk in one sentence, fix it (or guide the fix), re-push. |
| **Likely false positive** | Never work around it in code (renames, string-splitting, suppression comments). Name the exact finding ID and tell the user a platform admin can add a central ignore for it (`safety.ignore.<tool>.<id>`, where the value is the expiry date, or empty for none), which clears it at both the gate and the periodic safety sweep (an `a11y` ignore clears only the deploy check, because accessibility findings never reach the sweep). A `secrets` finding is the exception: gitleaks has no central ignore family, and its supported suppression is a `.gitleaksignore` committed in the app's own repo, an entry there being sanctioned, not an in-code workaround (the contract's R8). Semgrep has no repo-side escape at all: the `sast` gate honors neither a `# nosemgrep` comment nor a `.semgrepignore` (R8), so a semgrep finding is either fixed in the code (when it is real) or ignored centrally by a platform admin (`safety.ignore.semgrep.<rule id>`). |
| `yaml.github-actions.security.secrets-inherit` finding on `.github/workflows/deploy.yml` | A real fix, not a false positive: tell the user and, with their okay, delete the `secrets: inherit` line from `deploy.yml`. The platform's reusable workflow needs no inherited secrets (it uses only the automatic `GITHUB_TOKEN` and OIDC), and repos made from older copies of the template carry that line. Keep the `workflow_dispatch` trigger. |
| `SAFETY GATE DISABLED by platform policy` in the log | Deliberate admin configuration, not a bug. Note it and move on. |
| config-integrity failure | Something in the repo is a file the platform injects at build time, or one it forbids outright; the failure names each path, and the full list with the reason for each is `inno-platform-conventions`' **Files you must not touch** section. Three rules govern how you act on it. **Never move or delete author code unprompted**: files under a root `src/`, and a root `package.json` / `package-lock.json` / `tsconfig.json`, are often the author's real code and manifests in a migrated repo, so show the user every flagged path and, only with their okay, move it under `app/` (for example `app/src/`), updating the Dockerfile `COPY` paths and any imports or build settings that pointed at the old location; delete only what they confirm is not theirs. **Platform-owned files just go**: a root `wrangler.jsonc` or any competing wrangler config, a `.wrangler/` directory, a `scaffold/` that outlived `app/.needs-build`, a root-level `.env*` (its values move into app Variables with `set_app_variable`) and any root package-manager config, plus every `.npmrc` at any depth. **A directory symlink has no policy toggle**: show the user the link, then replace it with the real directory or drop it. If instead `CLAUDE.md`'s required template headers were altered, revert them (the rest of the file is yours). A message that the gate "could not fully inspect the app tree" means a committed directory it could not read; fix or remove that path. Everything else under `app/` (an `app/package.json`, an `app/.yarnrc.yml`, an `app/src/`) is yours and fine. |
| `dep-age` failure | The **inverse** of a CVE finding: do NOT bump to the newest release, that makes it redder. Either a pinned dependency was published more recently than the platform's cooldown allows (`safety.min_release_age_days`; `get_config app=<name>` tells you the value actually in force, and from it how many days you're short by), or the app ships `app/package.json` with no committed, parseable `app/package-lock.json` and there are no exact versions to date at all. Remedies: wait out the cooldown, pin an older vetted version, commit `app/package-lock.json`, or ask a platform admin for an app-scope `safety.min_release_age_days: 0`. Separately from this gate, a function-shaped app that ships `app/package.json` with no committed `app/package-lock.json` fails the `app-deps` job outright, whatever the cooldown says, in this very run rather than at the tag (the contract's §1.1 **Dependencies** bullet). |
| `container` fails with `Accessibility check failed` | Only happens when the app's `safety.a11y.mode` is `enforce`. Read the report (§1c) for what it marks as blocking; the causes and the remedies are the row for it in `inno-ship`'s failure table. Fix, then re-push. |
| container failure | Dockerfile contract problem (the contract's R1), or the built image never answered `GET /healthz` with exactly 200 inside the smoke test's budget (R2 gives its clocks); hand off to `inno-containerize`, whose item 2 covers a non-root failure. |

Diagnose privately (the `get_ci_status` run link and job conclusions, its
annotations when they come through, or `gh run view --log-failed` if the user
has `gh` authenticated); don't paste raw logs at the user. After two failed
fix attempts on the same gate, ask permission to create a
`create_support_bundle` for the app and hand the user the download link to
attach to a support ticket. The caps and refusals are `inno-manage-app`'s
support-bundle section; the one to expect here is `bundle_limit_reached`,
which is not a reason to retry: point the user at a bundle already created.

## Done

End with a clear verdict: **"Safe to ship"** (gates green and guardrails
clean, and, for a `function` or `mcp-function` app that has
`app/package.json`, a committed `app/package-lock.json` in step with it; point
at `/inno-ship`) or **"Not yet"** with the specific blockers listed. This push
proves the lockfile on its own, because `app-deps` runs on every push to the
default branch, so a missing or stale lockfile is a red job in the run you are
narrating, not a surprise at the tag. (The `deps` gate still builds a
throwaway lockfile when none is committed, so its own green never proved
anything here.) One
exception, and it is about what you REPORT rather than about safety:
`app-deps` is `needs: [policy, config-integrity]`, so a red
`config-integrity` skips it. Nothing unsafe follows, because that run skips
`deploy` too and there is no tag to cut, but a skipped `app-deps` proved
nothing. Do not report the lockfile as clear on such a run, and say that it
will be checked for the first time on the re-push, so a lockfile failure
arriving then is not a new regression. Checking the file yourself is
otherwise belt, not the safeguard: it saves a round trip through CI.

Report the declared variables (§1b) beside the verdict too, never inside
it: each `required` name with no value, and any problem in
`app/inno-variables.json`, with the note that the platform still deploys.
They never turn "Safe to ship" into "Not yet"; setting them first is the
user's call.

Report the accessibility review (§1c) beside the verdict, not inside it:
what a tool checked, what you checked by hand, and what was not checked. In
`report` mode its findings never turn "Safe to ship" into "Not yet"; in
`enforce` mode a blocking one already shows as a red `container` job.
