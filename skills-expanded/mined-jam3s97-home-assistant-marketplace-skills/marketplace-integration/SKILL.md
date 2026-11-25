---
name: marketplace-integration
description: Write, build and review Home Assistant custom integrations (custom_components) to the standard Home Assistant core holds its own integrations to, and publish them through the Home Assistant Marketplace (formerly HACS). Use when the user wants to scaffold a new custom integration; write, fix or refactor integration code (config, options, reauth and reconfigure flows, coordinators, entities, devices, actions, diagnostics, repairs, translations, tests, manifest.json, hacs.json, brand images); review an integration for bugs and Home Assistant best practice, or grade it against the integration quality scale (Bronze, Silver, Gold, Platinum); fix a failing hassfest or HACS check; or prepare for, or work through review feedback on, a pull request to hacs/default (the Marketplace catalog, also known as the HACS default store). Not for dashboards, cards, themes, templates or blueprints.
---

# Marketplace integration skill

Helps write a Home Assistant custom integration that is as good as one in
core: **create** (scaffold from the blueprint), **build** (write code the
Home Assistant way, checked against the live developer docs) and **review**
(find bugs, best-practice gaps and quality-scale rules not yet met). Getting
listed in the Marketplace catalog follows from that: an integration built
this way passes the checks and gives reviewers little to ask for, and
**publish** and **respond** cover the steps that are specific to the
catalog. Scope is the `integration` category only.

**Naming.** From Home Assistant 2026.11, HACS is built in as the
**Marketplace**. It is the same system: the catalog is still the
`hacs/default` repository, the manifest is still `hacs.json`, and the check is
still the HACS action. Users may say "HACS", "the HACS default store" or "the
Marketplace catalog" and mean the same thing. Use "Marketplace" when talking
to the user, and keep the HACS names for the things still called that.

Requirements move. Home Assistant's APIs and the Marketplace rules change
several times a year, so the references here are a summary, and the live
docs on <https://contributors.home-assistant.io> are the authority. Each
section of `references/ha-best-practices.md` links its live pages, and
[Reading the live docs](references/ha-best-practices.md#reading-the-live-docs-for-a-custom-integration)
says how to fetch them (with a fallback when the site is blocked) and how to
read core-only details for a custom integration. When a reference here
disagrees with the live docs about how Home Assistant works, the live docs
win; say so and follow them. For the catalog checks, the older
<https://hacs.xyz/docs/publish/include> still applies alongside
<https://contributors.home-assistant.io/marketplace/>.

Home Assistant core ships its own agent guidance for integration code: the
`ha-integration-knowledge` and `ha-review` skills
(<https://github.com/home-assistant/core/tree/dev/.claude/skills>) and
`AGENTS.md` in the repository root. They only load inside a core checkout,
so the rules from them that apply to a custom integration are carried in
`references/ha-best-practices.md`. Core's copy is the newer one: where it is
available and differs on how integration code should be written, prefer it.
What does not carry over is core-only: `homeassistant/components/` paths,
`strings.json`, `quality_scale` in the manifest and core's PR rules. This
skill's own ground is what is different for a custom integration and what
the catalog review asks for.

## The human stays in the loop

Home Assistant and HACS are Open Home Foundation projects, and the
foundation's AI policy (<https://contributors.home-assistant.io/start/ai-policy/>)
applies to what gets submitted to them. AI may be used as a tool; the person
is responsible for the contribution and must understand it. In practice:

- **Explain, don't just patch.** For every non-trivial change, say what was
  wrong, why it matters and what the fix does, so the user can explain their
  own code to a maintainer. Encourage them to read the diff before releasing.
- **Never act as the user on hacs/default.** Do not open the pull request,
  write or post comments, reply to reviews, or tick checklist boxes there.
  The policy bans autonomous agents and says not to use AI to generate
  answers to maintainers' questions; such PRs and comments are closed or
  hidden.
- **The user writes their own words.** The PR description and review replies
  are theirs. Help by listing the facts they need (what changed, which
  release, which links) and by checking a draft they wrote for accuracy,
  missing items or grammar. Do not hand them finished prose to paste.
- **Tested by a person.** Before a release, the user should have run the
  integration against the real device or service. Do not describe untested
  behaviour as working.

If the user asks for something on the wrong side of this, say what the
policy is and offer the allowed form of help.

## Pick the mode

| The user wants to… | Do |
| --- | --- |
| Start a new integration | [Create](#create) |
| Add features or fix code in an existing one | [Build](#build) |
| Know whether it is good / ready, which quality-scale tier it meets, or why a check fails | [Review](#review) |
| Get ready to be listed in the Marketplace catalog | [Publish](#publish) |
| Work through a maintainer's review on their hacs/default PR | [Respond to a review](#respond-to-a-review) |

When invoked as a command, the first word of the argument selects the mode:
`create`, `build`, `review`, `publish` or `respond` (for example
`/marketplace-integration review`). With no argument, or anything else, infer the
mode from the request; if the working directory already holds an integration
and nothing else was asked, default to Review.

## Create

**Every new integration starts from the blueprint**,
<https://github.com/ludeeus/integration_blueprint>. Clone it; do not write the
files by hand, and do not recreate its files from memory. This holds for a
small, simple or throwaway "test" integration too: being quick or small is
not a reason to skip it. Hand-written scaffolds leave out the parts the user
cannot easily add later: the devcontainer and `scripts/develop` (a local Home
Assistant to test in), `scripts/setup` and `scripts/lint`, the ruff config,
the issue templates, and the hassfest and HACS validation workflows.

The only exceptions:

- The user says, in this conversation, that they do not want the blueprint.
- The clone fails (no network, host blocked). Stop and tell the user. Offer
  to retry, or to hand-write the scaffold with their agreement, listing what
  will be missing. Never fall back silently.

Do the steps in order. If you skip or change any step, say so at the time
and why; do not leave it for the user to discover.

1. Check it should exist. Search Home Assistant core
   (<https://www.home-assistant.io/integrations/>) and the Marketplace catalog for the
   same device, brand or API. Duplicates of core or of an existing default,
   and forks of them, are the most common reason maintainers decline a
   submission; contributing to the existing integration is the usual
   advice. A custom repository is still fine for personal use.
2. Ask for (or infer) the display name, the **domain** (lowercase,
   underscores, must not match any Home Assistant core integration), what
   device or service it talks to, and the owner's GitHub handle. Then work
   out the integration's type before writing code, because it decides the
   manifest, the config flow and how data is fetched:

   | Question | Answer decides |
   | --- | --- |
   | Local device or cloud service? | `iot_class` prefix; discovery is possible only for local |
   | Polls, or the source pushes updates (websocket, MQTT, webhook, BLE advertisements)? | `iot_class` suffix; a `DataUpdateCoordinator`, or push callbacks with `should_poll = False` |
   | How does the user sign in: none, host only, API key or password, OAuth 2.0? | config flow steps; OAuth needs application credentials |
   | Bluetooth? | the Bluetooth coordinators and manifest matchers |
   | Found on the network (zeroconf, DHCP, SSDP, USB, Bluetooth)? | discovery steps and manifest matchers |
   | One device, a hub with several devices, or a service with no device? | `integration_type` (`device`, `hub`, `service`) and `DeviceInfo` |
   | Several user-chosen items under one account (locations, rooms)? | config subentries |

   Ask about anything the user has not said and cannot be inferred. Read
   the matching sections of
   [references/ha-best-practices.md](references/ha-best-practices.md)
   (OAuth 2.0 accounts, Config subentries, Bluetooth devices) before step 6.
3. Get the template, according to what the working directory holds:
   - Already contains the blueprint (`custom_components/integration_blueprint`
     exists): skip to the next step.
   - Empty, or the user names a new folder: clone the blueprint into it as
     below. Tell the user they will need to create the GitHub repository and
     add it as `origin` before pushing; do not create one for them unasked.
   - Contains an unrelated project: stop and ask where the integration
     should go. Never scaffold over existing files.

   "Use this template" on GitHub, or
   `git clone --depth 1 https://github.com/ludeeus/integration_blueprint <repo> && rm -rf <repo>/.git && git -C <repo> init`.

   Before going on, confirm the clone landed: `.devcontainer.json`,
   `scripts/develop`, `scripts/lint`, `scripts/setup`, `.ruff.toml`,
   `.github/workflows/validate.yml`, `.github/workflows/lint.yml` and
   `custom_components/integration_blueprint/` must all exist. Keep all of
   them; later steps rename and edit, they do not delete.
4. Rename everything. Directory `custom_components/integration_blueprint` →
   `custom_components/<domain>`; then replace `integration_blueprint`,
   `IntegrationBlueprint`, `Blueprint`, `Integration blueprint` and `ludeeus`
   across the tree (code, `manifest.json`, `hacs.json`, `README.md`,
   `translations/en.json`, `.devcontainer.json`, `scripts/develop`, issue
   templates). Leftover template names are a common reason submissions are
   closed.
5. Fix `manifest.json`: real `documentation` and `issue_tracker` URLs,
   `codeowners`, correct `iot_class`, add `integration_type`, add one to
   three `categories`, add `requirements` (pinned `==`) for the client
   library, leaving out anything Home Assistant already requires. Keys ordered `domain`,
   `name`, then alphabetical.
6. Replace the blueprint's sample API client, entities and the
   `unique_id=slugify(username)` placeholder with real ones (see Build).
   The blueprint's coordinator raises `ConfigEntryAuthFailed` but its config
   flow has no reauth step; add `async_step_reauth` / `reauth_confirm` and
   their strings, or reviewers will ask for it.
7. Add `custom_components/<domain>/brand/icon.png` (and ideally `logo.png`),
   then **delete `ignore: brands`** from `.github/workflows/validate.yml`.
   If the user has no artwork yet, a generated placeholder keeps the check
   green, but say plainly that it is a placeholder and list replacing it
   under what the user still has to do.
8. Replace the README with real install, configuration and entity
   documentation. Keep the LICENSE (MIT) or swap for another OSI licence.
9. Verify, and run each of these rather than assuming:
   - `scripts/setup`, then `scripts/lint` (ruff format and check). Fix what
     it reports.
   - The pre-flight script (see Review). It reports an integration that is
     missing the blueprint's development files.
   - `scripts/develop` starts a local Home Assistant with the integration
     loaded. It is long-running and usually needs the devcontainer, so ask
     the user to run it (in VS Code: "Reopen in Container", then
     `scripts/develop`) and add the integration from Settings → Devices &
     services. Do not claim the integration works until someone has.
10. Finish with a short report: that the blueprint was used (or why not),
    each step above as done, skipped or failed, the pre-flight result, and
    what the user still has to do themselves (create the GitHub repository,
    run `scripts/develop`, add real brand images, test against the device).

## Build

Read [references/ha-best-practices.md](references/ha-best-practices.md) before
writing or changing integration code, and for each area you are about to
touch (config flow, entities, a platform, Bluetooth…) fetch the live pages
its section links. Do this before writing the code, not after: the live
page is where new helpers and changed APIs show up first. Unless the user
sets another target, aim at the Silver rules of the
[quality scale](references/quality-scale.md) for new work, and do not let a
change break a rule the integration already met. The non-negotiables:

- UI setup through a config flow that tests the connection before creating the
  entry and sets a stable unique ID. No YAML configuration for new work.
- Everything on the event loop is async. No `requests`, `time.sleep`, file or
  socket I/O without `hass.async_add_executor_job`. Device/protocol logic
  lives in a PyPI library, not in the integration.
- Use `async_get_clientsession(hass)`; do not create your own session.
- Runtime objects go in `entry.runtime_data` (typed `ConfigEntry` alias), not
  `hass.data[DOMAIN]`.
- One `DataUpdateCoordinator` per polled endpoint, constructed with
  `config_entry=entry`; raise `UpdateFailed` for
  transient errors and `ConfigEntryAuthFailed` for bad credentials.
- Entities: `_attr_has_entity_name = True`, stable `unique_id`, `DeviceInfo`,
  device classes / state classes / units from the enums, names from
  `translation_key`, `available` reflecting reality.
- `async_unload_entry` must cleanly undo setup.
- Set `PARALLEL_UPDATES` in every platform module.
- An integration that only makes sense once (no account, no host) sets
  `"single_config_entry": true` in the manifest rather than using the domain
  as a unique ID.
- User-facing strings live in `translations/en.json` (custom integrations do
  not load `strings.json`).

Follow the blueprint's file split (`api.py`, `coordinator.py`, `data.py`,
`entity.py`, one file per platform) unless the repo already has its own
convention.

**Before calling a change done**, go through this list against the files
you touched and fix or report anything that fails:

- [ ] No blocking I/O on the event loop; nothing new from the "Outdated
      patterns" table in the best-practices reference.
- [ ] Timestamps come from `homeassistant.util.dt` (`dt_util.utcnow()`,
      `dt_util.now()`), not `datetime.now()`, and are timezone-aware.
- [ ] State attributes and service responses are JSON-serialisable: no
      `datetime`, dataclass or library objects.
- [ ] Every new entity has a stable `unique_id`, a `translation_key` (or
      `_attr_name = None`) and is attached to a device.
- [ ] Every new config-flow step, error, abort, entity name, exception and
      service has its string in `translations/en.json`.
- [ ] Credentials and tokens are not logged and are redacted in diagnostics.
- [ ] Anything set up in setup or `async_added_to_hass` is undone on unload
      or removal.
- [ ] Options are read when they are used, or the entry reloads when they
      change; none is captured once at setup and reused later.
- [ ] Code that enables or unhides entities in bulk only touches entries
      whose `disabled_by` / `hidden_by` is `INTEGRATION`, never ones the
      user changed.
- [ ] New dependencies are pinned in `requirements`; new core components
      used are in `dependencies` or `after_dependencies`.
- [ ] The live docs for each area you touched were read (or you said they
      could not be reached), and no quality-scale rule the integration met
      before is now broken.
- [ ] `scripts/lint` (or `ruff check` and `ruff format`) and the tests pass;
      the pre-flight script reports no new errors.
- [ ] You have told the user what still needs testing against the real
      device or service.

## Review

Work in this order and report findings grouped as **Blocking** (a HACS or
hassfest check fails, or the PR would be closed), **Should fix** (Home
Assistant best practice, user-visible bugs, Bronze rules not met) and
**Nice to have**. Give file:line and the concrete fix for each. End the
report with the quality-scale summary from step 3.

1. Run the offline pre-flight:
   `python3 <skill-dir>/scripts/preflight.py <repo-path>`.
   It covers repository layout, `hacs.json`, `manifest.json`, brand icon,
   translations, workflows, and a scan for common code smells. It cannot see
   GitHub-side settings, so check those by hand (step 4).
2. Read the code against
   [references/ha-best-practices.md](references/ha-best-practices.md). The
   script's pattern hits are leads, not verdicts; confirm each by reading the
   code. Where a finding rests on how a Home Assistant API behaves, check
   the live page linked from that section before reporting it.
3. Grade the integration against the quality scale with
   [references/quality-scale.md](references/quality-scale.md): every rule of
   the target tier (Silver unless the user named one) and the tiers below
   it, each Met, Not met, N/A or Unknown with its evidence. Report the
   per-tier summary in the format that file shows, and say plainly that
   custom integrations have no official tier.
4. Check what only GitHub knows, using
   [references/marketplace-requirements.md](references/marketplace-requirements.md):
   description, topics, issues enabled, licence detected, not archived, a
   full **release** (not just a tag) made *after* the last green workflow
   run, and both workflows green with no `ignore`.
5. Go through [references/review-rounds.md](references/review-rounds.md),
   the code-level findings maintainers raised on submissions that were later
   merged (auth and reauth, exceptions, blocking calls, privacy, access
   control, frontend escaping, device safety, minimum-version floor). This is
   the closest thing to the reviewer's own checklist.
6. Compare against
   [references/common-pr-feedback.md](references/common-pr-feedback.md), the
   catalogue of what gets hacs/default submissions closed or drafted.

Review the code as it is in the latest release tag, not only the working
tree: that is what HACS validates and what maintainers read.

If hassfest or the HACS action is failing, map the message to its fix with the
table in `references/marketplace-requirements.md` before changing anything.

## Publish

Only when the Review is clean. The full procedure, the PR template and the
rules that get PRs closed without comment are in
[references/marketplace-requirements.md](references/marketplace-requirements.md#submitting-to-hacsdefault).
In short:

1. HACS action and hassfest both pass on the default branch with no `ignore`.
2. Publish a GitHub release after that passing run.
3. Repository name has no "HACS" in it. Fork `hacs/default` from a
   **personal** account, branch from `master` (not
   on `master`), add `owner/repo` to the `integration` file in alphabetical
   (case-insensitive) position, one repository per PR.
4. Fill in the PR template completely, with working links to the release and
   to the two passing workflow runs. Leave "allow edits by maintainers" on.
   The user does this themselves, in the GitHub web UI, using the template
   as provided.
5. Do not request reviews, ping maintainers or bump the PR. Review takes
   months; a drafted PR means "fix, then mark ready".

The person submitting must be the owner or a major contributor of the
repository, and must open the PR themselves (see
[The human stays in the loop](#the-human-stays-in-the-loop)). Your part is
everything up to that point: getting the checks green, preparing the one-line
change to the `integration` file on their fork if they want, giving them the
three links, and verifying each checklist statement is true before they tick
it. Misrepresenting the checklist gets the PR closed.

## Respond to a review

When the user has change requests on their hacs/default PR, follow
[references/review-rounds.md](references/review-rounds.md#responding-to-a-review).
The rule that saves the most time: fix the whole class of problem, not the
quoted line. Reviews that ran to four or five rounds did so because the same
kind of issue (an unescaped value, a logged secret, a blocking call) was still
present elsewhere. Then bump the version, publish a new non-pre-release
release, and update the PR branch and its three links.

Walk the user through each item so they understand the problem and the fix.
The reply to the maintainer is theirs to write: give them a factual list of
what changed per item and the release that contains it, and review what they
write if they ask. Do not draft the reply for them and never post it.

## Things this skill should refuse to paper over

- Adding `ignore:` to the HACS action, or disabling hassfest, to get green.
- Moving or re-creating a git tag or release to hide a change.
- Opening the hacs/default PR, or writing or posting replies to maintainers,
  on the user's behalf.
- Using a domain that shadows a core integration, or publishing an alpha/beta
  copy of a core integration as a default.
- Copying another project's brand assets or code without a compatible licence.
- Submitting a repository the user does not own or substantially maintain.

Explain why, and fix the underlying problem instead.
