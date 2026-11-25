---
name: plugin-authoring
description: Make a new evo-agents plugin from the template maycuatroi1/evo-plugin-template once a member approves its proposal, or change a plugin in its repository - the manifest evo-plugin.json, the backend of plugin/1, pages on the hub's UI kit, agent packs, tests - and the CI that signs and releases it. You never publish, install, list or set a secret yourself.
---

# Writing an evo-agents plugin

Two kinds of work reach you:

- **A new plugin for an industry.** A member describes a need. You propose it first, with `builder__propose` of kind
  `plugin` (skill `hub-settings`), and make nothing before an admin of the project approves it. Approving hands you
  the task in the thread: the steps below, from the template.
- **A change of a plugin that exists.** The run checks out the plugin's repository on its branch. You change it there,
  test it, commit and push; the hub opens the draft pull request.

You never publish, install, upgrade or list a plugin, and you never set a secret: the repository's CI publishes, the
hub installs once a hub admin approves, and the member sets the secrets the CI needs when you tell them which.

## A new plugin, from the template

The proposal of kind `plugin` names the plugin's id (`name`), the `industry`, the `need`, the GitHub `owner`, the
`visibility` (public or private) and the `price` (`free`, or USD per hub per month), with an optional `repo` name and
`categories`. Once it is approved, and only then:

1. Create the repository from the template and clone it:

   ```
   gh repo create OWNER/NAME --template maycuatroi1/evo-plugin-template --public --clone
   ```

   with `--private` for a private plugin.
2. Rename the template's plugin as its `docs/rename.md` says: the id `lumen-hello` becomes the plugin's id in
   `evo-plugin.json`, the pages and the tests; the publisher becomes the owner's; the signer becomes
   `sigstore:OWNER/NAME/.github/workflows/ci.yml`, in `evo-plugin.json` and `market-entry.json`.
3. Write the plugin for the need: the manifest, the backend, the pages and their tests (see The repository).
4. Run the checks of Before you push until they pass, then push `main`.
5. Tag the first version and push the tag: `git tag v0.1.0 && git push origin v0.1.0`. The CI signs the bundle and
   makes the GitHub Release (see Signing and releasing).
6. Add the repository to the project, so the runs after this one open it: add it to the harness's `harness.yaml`
   (its `repos`), then register the harness again with `evo-agents hub project register ROOT`.
7. Propose, each with its own call of `builder__propose`, for the member to approve:
   - kind `plugin_install`: set `repo` OWNER/NAME and `tag` v0.1.0. In a self-managed project (the hub admin turned
     it on and listed the GitHub owners they trust; `evo-agents hub admin project show PROJECT --json` prints
     `self_managed` and `trusted_owners`) and an owner on that list, the admin of the project approves it and the
     plugin installs for that project alone. Any other owner, or a project that is not self-managed, waits for a hub
     admin, who trusts the signer for the publisher and installs the release, as `evo-agents hub plugin install
     --github OWNER/NAME@v0.1.0 --trust` would.
   - kind `plugin_listing`: set `repo`, `tag`, `price`, `industries` and `categories`. Approving it hands you the
     listing: for a free plugin, a pull request that adds its entry to the market's index; for a paid one, the
     listing and the bundle on the seller's hub (see Listing).

Say in the thread what you made, the repository's link, what `evo-agents plugin test` printed, and which proposals
wait for whom.

## The repository

```
evo-plugin.json                 the manifest: id, version, publisher, tier isolated, engines, plugin_api 1,
                                permissions, config (a JSON Schema of its config), contributes
backend/main.py                 the backend: a process speaking plugin/1 on stdio
pages/<page>/index.html         each page the manifest contributes, on the hub's UI kit
pages/i18n/en.json, vi.json     the strings of the pages
packs/<name>/                   each agent pack: INSTRUCTIONS.md, skills/<skill>/SKILL.md
tests/test_plugin.py            the plugin's tests, run with `evo-agents plugin test`
market-entry.json               the plugin's entry for a market's market.json (plugin-market-v1)
docs/rename.md                  how to rename the template's id, publisher and signer
.github/workflows/ci.yml        test, pack and sign on main; release on a tag v*; publish-seller, optional
```

- **Manifest.** Raise `version` (semver) on every change that ships, and tag it `v<version>`. `permissions` asks for
  what the plugin reads or writes on the hub; a project's admin grants them when they enable it, so ask for no more
  than the need takes. A new config field with a default keeps the projects that set none working.
- **plugin/1.** The backend answers JSON-RPC lines on stdin and stdout: `initialize` naming plugin/1 and listing the
  MCP tools the manifest contributes, `ping`, one method per point it serves (`tool`, `event`, `route`, `channel`,
  `job`) and `shutdown`. Nothing else goes to stdout; logs go to stderr. A tool's result is
  `{"content": [{"type": "text", "text": "..."}], "is_error": false}`.
- **Pages.** A page runs in `<iframe sandbox="allow-scripts allow-forms">` with no network of its own: it reaches the
  hub only through the bridge `evo-plugin/1` (`postMessage` to the parent, which calls the plugin's routes and tools
  for it). It loads the hub's UI kit, `/v1/plugin-ui/kit/1/evo-ui.css` and `/v1/plugin-ui/kit/1/evo-ui.js`, so it
  looks like the hub in both themes, and keeps its strings in `pages/i18n`. It injects nothing into the hub's web.
- **Agent packs.** A skill's directory name equals the `name` of its front matter, with a description of 1 to 1024
  characters. INSTRUCTIONS.md stays under 32 KiB.

## Records: a plugin that keeps a company's papers

A plugin that keeps business records (leave requests, expense vouchers, draft entries, a customer's file) keeps them
in the hub's records store, never in `data/<name>/` of its backend: the store lives in the hub's Postgres, in its
backup, and survives a restart or a new host; `data/<name>/` is a cache that may vanish. Do this:

- Ask `records:use` in `permissions`, and nothing else the plugin does not need. The admin of the project grants it,
  and sets `records_level`, the highest level that jobs and events, which have no caller, may touch.
- Read and write through the records API (`/v1/plugin-api/projects/{project}/records/{collection}/{key}`, or the
  bridge's `records.list|get|put|delete` from a page), sending the plugin token and, for a route or tool call, the
  call's `caller.token` as `X-Evo-On-Behalf-Of`. Never invent a token, never send one from another call.
- Before you write the plugin, ask the member two things for each kind of record, and put the answers in the code:
  its `level`, one of the project's ladder (a leave request: `internal`; an expense voucher: `finance`), and its
  `audience`: `everyone` that the level reaches, or `writer`, so that only the person who wrote it sees it (a leave
  request: the writer, with the manager's level reaching it through a role, not through the audience). The level of
  a record may be no higher than the writer reaches.
- Use `revision` on every update, so that two people do not overwrite each other, and generated keys for a new record.
- Expect 404 for a record the call cannot see, 409 for a revision that moved, 403 for a level above the call.
- Test with `evo-agents plugin test .`: a stand-in hub answers the records API, and the check `records` fails when the
  plugin calls it without `records:use` in its manifest, for another project, or with a delegation the call did not
  carry.

## Before you push

```
python -m pytest -q                  # the plugin's own tests
evo-agents plugin test .             # the checks a hub relies on
evo-agents plugin pack .             # <id>-<version>.tar.gz, deterministic
```

Commit with a message that says what changed and why. In your reply, say what changed, what you ran and what it
printed, and what the reviewer should check.

## Signing and releasing

The repository's CI does it, never you.

- **A plugin made from the template.** Its `ci.yml` tests and packs on every push and pull request, and signs keyless
  with Sigstore on `main`. A tag `v*` makes the GitHub Release with `<id>-<version>.tar.gz` and
  `<id>-<version>.tar.gz.sigstore.json`, which a hub installs with `evo-agents hub plugin install --github OWNER/NAME`.
  The job `publish-seller` uploads the bundle to a seller's hub instead, for a paid plugin; it runs only when the
  repository's variable `EVO_SELLER_PUBLISH` is `true` and its environment `seller` holds the seller's token. Ask the
  member to set both: you set neither.
- **A client's plugin published straight to its hub.** `ci.yml` beside this skill is the template: copy it to
  `.github/workflows/ci.yml` when the repository has none, with the plugin's directory in `PLUGIN_DIR`. Its **test**
  job runs on every push and pull request; **sign** runs on the default branch only, is the only job with
  `id-token: write`, runs none of the plugin's code and signs the bundle the test job packed; **publish** runs in the
  GitHub Environment `evo-hub`, whose reviewers and secrets the client's owner sets (`EVO_HUB_URL`, `EVO_HUB_LOGIN`,
  `EVO_HUB_TOKEN`), and publishes the signed bundle to the hub, where the version waits as available. A hub admin
  then upgrades to it (`evo-agents hub plugin upgrade NAME`, or the hub's plugin page).

## Listing

You list a plugin only when the member approved a proposal of kind `plugin_listing`, and the hub hands you its task.

- **Free.** Fork the market's index (`maycuatroi1/evo-agents-market` unless the proposal names another) and open a
  pull request that adds the plugin's entry to `market.json`, from the repository's `market-entry.json`: the id, name
  and description of the release's manifest, the industries and categories, the repo, the publisher and its signer,
  tier `isolated`, price `free`. Run `evo-agents plugin market-check market.json --releases` before you push, follow
  the index's `CONTRIBUTING.md`, and give the member the pull request's link. A maintainer of the index merges it.
- **Paid.** On the seller's hub, with the member's account, add the listing and upload the release's bundle:

  ```
  evo-agents hub market listing add PLUGIN --publisher PUBLISHER --signer SIGNER --usd 49.50
  evo-agents hub market bundle upload PLUGIN FILE --signature FILE
  ```

  When the account holds no seller's grant there, say so to the member and stop.
