---
name: ide-extension-offering
description: "Decides whether a developer platform should ship an official IDE extension (VS Code, JetBrains), and runs it: job versus cheaper surfaces, IDE families and forks, a thin shell over the CLI, shared login, publishing to VS Code Marketplace, Open VSX and JetBrains Marketplace, telemetry obeying the IDE setting, deprecation. Use whenever a vendor mentions building or maintaining a VS Code extension or JetBrains plugin for their product, vsce, ovsx, Open VSX, or \"developers want us in the editor\" - even without saying \"IDE extension\". Not for internal or personal extensions, writing extension or language-server code, or choosing extensions to install. Do NOT use for CLI design - use samber/developer-platform-skills@cli-interface-design; nor agent tools - use samber/developer-platform-skills@mcp-server-offering."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# IDE Extension Offering

You are a developer-platform engineer who owns a vendor's official editor integrations. Decide whether the platform should ship an IDE extension, for which job and which editors, then run it as a product: published, trusted, in sync with the API and CLI, and retired cleanly.

An IDE extension runs with the editor's full permissions on the customer's source code, with no sandbox. Customers install it once and forget it; their security team allowlists it by publisher ID. A broken release reaches every open editor within a day, and a stale one collects low ratings that rank above your docs.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Record the per-job verdict, the IDE families and registries, the publisher IDs, the minimum host and CLI versions and the deprecation schedule, so a later release checks against them instead of re-deciding.

## The extension contract

Audit every plan, pull request and release against this block first.

1. The extension MUST NOT hold business logic or hand-written API calls that the CLI, SDK or language server already owns, because two implementations of one behaviour drift within a few releases and the extension's copy is the one nobody tests.
2. Every VS Code-API extension MUST ship the same packed `.vsix` to both the VS Code Marketplace and Open VSX, because the Marketplace terms restrict use to Microsoft products, so Cursor, VSCodium, Theia and Kiro users install from Open VSX or find a stranger's copy. When it needs an API or extension that fork hosts lack, publish to both anyway and name the limitation on both listings.
3. Credentials MUST live in the host's secret store (VS Code `SecretStorage`, JetBrains `PasswordSafe`) or come from the CLI's own login, never from a settings file, because settings sync, dotfile repos and support screenshots publish them.
4. Telemetry MUST follow the host's telemetry level whatever the extension's own setting says, because VS Code's policy requires it, JetBrains approval requires explicit consent, and an extension that phones home against the user's choice gets uninstalled and written about.
5. A published extension ID, plugin ID or Open VSX namespace MUST NOT change or be removed; deprecate it and point to its successor, because a removed Marketplace name stays reserved forever, a JetBrains `<id>` change strands every upgrade, and allowlists key on the ID.
6. Publishing credentials MUST be short-lived or federated, scoped below owner, and absent from the package, because a leaked publish token lets an attacker push an update to every install.

Rationalizations to reject:

| Rationalization | Why it fails |
| --- | --- |
| "Developers live in the IDE, so we need an extension." | The job decides, not the location. JSON config help is a schema on SchemaStore; agent help is an MCP server. Ship an extension for a job that needs editor UI (step 1). |
| "Calling the API directly from TypeScript is faster than shelling out to the CLI." | Faster for the first release. Then auth, proxies, retries, pagination and errors fork. Wrap the CLI or the language server, or generate from the same SDK. |
| "Cursor users can sideload the `.vsix`." | They search Open VSX and install whatever matches your name. Publish there and claim the namespace. |
| "Our own `telemetry.enabled` setting defaults on and users can turn it off." | The host setting wins. Gate on it first; your setting can only narrow collection further. |
| "Remove the old extension so nobody installs it." | Removal deletes stats, reserves the name forever and breaks allowlists. Deprecate with a migration pointer. |
| "JetBrains is the same as VS Code, ship the hotfix tonight." | Every JetBrains version goes through manual review with no guaranteed time frame; plan for working days. |
| "Sales asked for an IDE integration, that is the demand." | A deal asks for a logo on a checklist. Count it only once it maps to a job in step 1; until then the verdict is Go later. |

## Interview

Ask before designing; each answer changes a later step. Batch questions. When nobody can answer, write the assumption in the plan's Assumptions table and set the plan status to provisional.

1. Which developer job should the editor do: author a config or schema file, browse or edit product resources, call the API from the editor, run a local emulator, tunnel or listener, log in, see product findings inline (scan results, errors, traces), set up the MCP server? (step 1)
2. What exists already: a CLI with a `--json` contract and a token or session-status command, a language server, a JSON schema, an MCP server, an official or community extension? Who maintains each, and what do its installs and issues show? (steps 1, 3, 4)
3. Which editors do paying customers use, by share, including VS Code forks (Cursor, Windsurf, VSCodium), JetBrains IDEs (open-source or commercial editions), Visual Studio, Neovim, Zed? How many work remotely (Remote-SSH, WSL, dev containers, Codespaces) or in the browser? (steps 2, 3, 4)
4. How do customers authenticate the CLI today, and does the product offer OAuth for desktop clients? (step 4)
5. Who owns the extension after launch: team, languages (TypeScript, Kotlin or Java), on-call, a test account? (steps 1, 2, 8)
6. Do customers run restricted fleets: allowlists, proxies with custom CAs, air-gapped machines, private marketplaces? (step 7)
7. By when must it ship, is it a one-off launch or a maintained surface, and what is the effort ceiling? A near deadline keeps the default rungs; a maintained surface with a staffed owner promotes the starved ones. Write which answer moved which rung in the plan.

## Workflow

1. Decide go/no-go per job.
2. Choose IDE families and registries.
3. Choose the architecture.
4. Wire auth, secrets and workspace trust.
5. Sync with the API and CLI.
6. Claim identity and publish.
7. Design telemetry, trust and fleet support.
8. Release, support and measure.
9. Deprecate and sunset.

Write the deliverable with [references/plan-templates.md](references/plan-templates.md): per-job verdicts, ranking and promotion slots, first-release sequence, compatibility matrix and deprecation notice.

## 1. Decide go/no-go per job

Map each job from interview Q1 to the cheapest surface that does it fully:

| Job | Surface that does it | Extension needed? |
| --- | --- | --- |
| Validate and complete a JSON config file | JSON Schema on SchemaStore, distinctive file name or `$schema` key | No: VS Code, JetBrains, Neovim and others read the catalog |
| Validate and complete a YAML or TOML config file | Same schema | No, but VS Code users need a YAML or TOML extension (Red Hat YAML, Even Better TOML); say so in docs |
| Language features for a vendor file format or DSL | Language server | Thin per-editor client |
| Let a coding agent operate the product | MCP server (`samber/developer-platform-skills@mcp-server-offering`) | No; optional one-click MCP setup through an extension's MCP server definition |
| Run a long-lived local process (emulator, tunnel, webhook listener) | CLI command | Optional launch or run configuration over the CLI |
| Browse or edit product resources, see findings inline, one-click login | Extension | Yes |

Catalog matching fires only on a distinctive file name (`acme.yaml`, `.acmerc.json`). A generic name (`config.yaml`, `flags.yaml`) needs a `$schema` key, a YAML modeline, or the extension's own schema contribution.

Options when an extension is needed:

- **Thin shell:** commands, tree views, diagnostics and a walkthrough over the CLI or language server.
- **Shell plus launch configurations:** adds Debug Adapter Protocol or run configurations for local processes.
- **Rich extension:** adds webview panels (dashboards, editors, forms).

- effort: `rich extension > shell plus launch configurations > thin shell > language server only > JSON schema`
- value (jobs done in-editor): `rich extension > shell plus launch configurations > thin shell > language server only > JSON schema`
- efficiency: `JSON schema > thin shell > language server only > shell plus launch configurations > rich extension`

- **Default:** a JSON schema for every config file, plus a thin shell when at least one job in the last two table rows has demand (interview Q1-Q2).
- **Starved:** the rich extension. Promote a webview only for a job that a tree view, quick pick or diagnostic cannot show, and only with a staffed owner: webviews are re-themed, re-tested and rewritten per editor family.
- **Go later:** demand exists only as a sales or checklist ask with no job behind it. Ship the schema and the MCP server, publish the extension ID plan, revisit when a job is named.
- **No-go:** no job has demand, or no owner exists (interview Q5).

When a community extension exists:

- **Maintainer reachable:** adopt it (listing transfer, or the maintainer deprecates theirs pointing at yours).
- **Maintainer unreachable:** publish yours under your verified publisher with a clearly distinct name, link it from your docs as the official one, and report trademark misuse through the registry only if the listing impersonates you.
- **It breaks contract rule 3** (keys in settings, direct API calls): publish a docs notice telling its users to rotate their keys and move to the official extension.

For vendor examples of each pattern, read [references/vendor-patterns.md](references/vendor-patterns.md).

## 2. Choose IDE families and registries

Rank editor families by interview Q3, the share of your own paying users, never by global surveys alone.

- effort: `native JetBrains language plugin > JetBrains plugin over CLI or LSP > VS Code-API extension on both registries > language server documented for other editors`
- value: `VS Code-API extension on both registries > JetBrains plugin > language server documented for other editors`; JetBrains first when customers are Java, Kotlin or Android-heavy.
- efficiency: `VS Code-API extension on both registries > language server documented for other editors > JetBrains plugin over CLI or LSP > native JetBrains language plugin`

- **Default:** one VS Code-API extension published to the VS Code Marketplace and Open VSX. It reaches VS Code and its forks with one codebase.
- **Starved:** the JetBrains plugin, high value and high effort: a second codebase plus three platform majors a year to verify. Promote it when JetBrains users are your second-largest group and a second owner who knows Kotlin or Java fits inside the effort ceiling (Q5, Q7). A half-time owner already on VS Code is not that owner.
- **Other editors** (Neovim, Zed, Emacs, Sublime): reach them through the language server and the schema; document the client config instead of writing plugins.
- **JetBrains LSP caveat:** the platform's LSP API runs only in commercial JetBrains IDEs (and the free tier of unified PyCharm since 2025.1), not open-source IntelliJ builds or Android Studio. Excluding those users or writing a native language plugin is a decision; write it in the plan.

## 3. Choose the architecture

- Put product logic in one shared core: the CLI, a language server, or a generated SDK. The extension renders, routes commands and holds no rules of its own.
- Prefer a language server for diagnostics, completion or hover in a vendor file format: one server serves every LSP editor.
- Detect the CLI on `PATH` (and a configurable path); offer to install a pinned version, never `curl | sh`.
- Call the CLI with `--json` and its exit codes; treat a missing field as a version mismatch (step 5).
- Activate on specific events (a command, a file type, a view), never `*`; measure activation time and lazy-load the CLI check.
- Run heavy analysis out of the editor process, never on the extension host thread.
- Bundle the extension (esbuild or webpack). Ship one `.vsix` per `--target` only when it carries native binaries.
- Set `extensionKind` deliberately. In remote workspaces (Remote-SSH, WSL, dev containers, Codespaces) a workspace extension runs on the remote host: find the CLI there, open URLs with `env.openExternal`, and route OAuth callbacks through `env.asExternalUri`.
- Declare where it cannot run: an extension that spawns processes cannot run on vscode.dev; say "desktop only" on the listing.

The CLI's flags, `--json` shape and exit codes belong to `samber/developer-platform-skills@cli-interface-design`; the extension is only as stable as that contract.

## 4. Wire auth, secrets and workspace trust

- effort: `AuthenticationProvider over product OAuth > CLI login reuse > pasted key in secret store`
- value (one sign-in, revocable, works remotely): `AuthenticationProvider over product OAuth > CLI login reuse > pasted key in secret store`
- efficiency: `CLI login reuse > AuthenticationProvider over product OAuth > pasted key in secret store`

- **Default:** reuse the CLI's login through a CLI command that prints the session or token as JSON (`acme auth token --json`), never by reading the CLI's credential file, so one sign-in serves terminal, CI and editor. Hold that token in memory only; never write it to settings, logs or output channels.
- **Starved:** a VS Code `AuthenticationProvider` (sessions in the Accounts menu, per-extension consent). Promote it when the product already issues OAuth to desktop clients or remote workspaces are common (Q3), since a remote CLI cannot see the laptop's login. For the OAuth side, see `samber/developer-platform-skills@oauth2-provider-design`. In JetBrains, store tokens in `PasswordSafe`.
- **Fallback:** a pasted API key, written straight to the secret store and masked in every log and output channel.
- Declare `capabilities.untrustedWorkspaces` honestly: an extension that runs the CLI or project files ships `"limited"` or `false`. Guard the code paths with `workspace.isTrusted` and re-enable on `onDidGrantWorkspaceTrust`, because hidden UI stays reachable by API. In JetBrains, respect trusted projects.
- Never read `.env` files or credentials from the workspace without an explicit user action.

## 5. Sync with the API and CLI

- Publish a compatibility matrix: extension version, minimum CLI or language-server version, minimum host version (`engines.vscode`, `since-build`), API version.
- Check the CLI version at activation; below the minimum, show one message with the upgrade command, never a stack trace.
- Gate new features on capabilities the CLI or API reports, not on the extension's own version.
- Release in the same train as the CLI when a feature spans both; the extension never ships ahead of the CLI it calls.
- Set the `engines.vscode` floor at or below the Code-OSS base of the oldest fork your users run (Q3), and feature-detect APIs forks lack (proposed APIs, language-model and chat APIs). Raise it only in a minor with a changelog line.
- Keep JetBrains `until-build` open-ended unless you publish one build per IDE release.
- Follow the API's own deprecation windows; see `samber/developer-platform-skills@api-versioning-policy`.

## 6. Claim identity and publish

1. Claim every name before launch: VS Code Marketplace publisher ID, Open VSX namespace (then file the ownership claim, or the listing shows an unverified warning), JetBrains vendor and plugin `<id>`. All are permanent.
2. Start the VS Code verified-publisher clock early: the badge needs an extension listed for 6+ months and a 6-month-old domain, so publish an early public version. Until it lands, publish the publisher ID and extension ID on your own domain's docs for buyers and allowlists.
3. Package once: `vsce package` (with `--pre-release` or `--target` at this step), inspect the file list, scan the packed `.vsix` for secrets.
4. Publish that file: `vsce publish --packagePath <file>.vsix --azure-credential` or `--oidc` (after registering a trusted-publishing policy on the Marketplace), and `ovsx publish <file>.vsix --trusted-publishing` from GitHub Actions or GitLab CI; fallback, a namespace-scoped Open VSX token on a Contributor account, rotated before expiry.
5. On the VS Code Marketplace, version as `major.minor.patch` only, with an odd minor for pre-releases and an even minor for releases. On JetBrains, publish pre-releases to an `eap` channel.
6. Plan JetBrains releases around manual review of every version: ship fixes on a schedule. Roll back on VS Code and Open VSX by republishing the last good code as a higher patch; a version number never republishes.

For per-registry requirements, auth, signing, review and removal rules, read [references/registry-publishing.md](references/registry-publishing.md). For npm or other package registries the extension depends on, see `samber/developer-platform-skills@sdk-package-publishing`.

## 7. Design telemetry, trust and fleet support

- Send VS Code events through `env.createTelemetryLogger` or `@vscode/extension-telemetry`, which honour each `telemetry.telemetryLevel` value (all, error, crash, off); never hand-roll the gate. Your own setting can only narrow collection.
- In JetBrains, ask explicit consent before any statistics, and send nothing while the plugin is idle: both are approval rules, and the IDE's data-sharing consent covers JetBrains' collection, not yours.
- Collect no source code, file paths, usernames or tokens. Ship `telemetry.json` (VS Code) and publish the event list beside the README.
- Prefer server-side metrics: a versioned `User-Agent` on every CLI and API call (`acme-vscode/2.4.0 (vscode 1.104; darwin-arm64)`). Keep it to product, version and platform, document that it is sent, and never add user or workspace identifiers.
- Publish the extension ID and publisher ID so IT can add them to allowlists (VS Code `extensions.allowed`).
- Support restricted fleets (Q6): honour `http.proxy` and custom CAs in the extension and in the CLI it spawns, document offline `.vsix` install, and test with the VS Code private marketplace or a JetBrains custom plugin repository when customers use one.
- Keep `SECURITY.md` and a vulnerability contact on the repository; review every `extensionDependencies` and `extensionPack` entry, since each installs with yours.
- Keep a compromised-token runbook per registry before you need it; read [references/registry-publishing.md](references/registry-publishing.md).

## 8. Release, support and measure

- Test with `@vscode/test-cli` on the minimum `engines.vscode`, current stable and Insiders, plus the main fork your users run (point `@vscode/test-electron` at its executable, or run a manual smoke test); for JetBrains, the IntelliJ Platform test framework and Plugin Verifier across the declared range, including EAP.
- Triage issues weekly; answer every listing review below 4 stars with a fix or a workaround.
- Make the first run succeed: a walkthrough (VS Code `walkthroughs`) that checks the CLI, signs in and completes one job.
- Track: weekly active users by version from server-side `User-Agent`, first-run success (CLI found, login done, first job completed), share of users on supported versions, issues and tickets per release.
- Treat marketplace install counts as acquisition only; large vendor extensions often rate well below what their install counts suggest.
- Link the extension from the CLI's help, the quickstart and the dashboard. On the listing, lead with one screenshot or GIF of the main job and the install-to-first-job steps.

## 9. Deprecate and sunset

Deprecate when the host absorbs the job (built-in auth, built-in agent tools), when an MCP server or language server now does it, or when no owner remains.

1. Announce with a date, the replacement and migration steps, in a public issue and the changelog.
2. Ship a last release that shows the notice once at activation, with a link.
3. Mark it deprecated on the VS Code Marketplace (comment on the `microsoft/vscode-discussions` "Deprecated extensions" thread, naming the replacement), deprecate it on Open VSX by pull request naming the replacement (see the publishing reference), and note it on JetBrains.
4. Keep the listing installable through the announced date; never remove it.
5. Archive the repository after the date; keep the security contact live.

## Gates

A release ships only when every gate passes:

- the same `.vsix` hash on both registries, with a clean secret scan of the packed file;
- integration tests green on the minimum and newest host, the pre-release host, the main fork and one remote target, against a real sandbox account;
- JetBrains Plugin Verifier clean across the declared build range;
- compatibility matrix updated, minimum CLI check covered by a test;
- no usage event fires with host telemetry at `error` or `off` (tested);
- untrusted-workspace behaviour tested.

## Failure modes

- **Cursor users install a lookalike** - the extension is not on Open VSX, or the namespace is unclaimed. Publish there and file the ownership claim.
- **Publishing breaks after a token deadline** - CI used a global Azure DevOps PAT or an expiring Open VSX token. Move to federated publishing on both.
- **Extension works for the team, fails for customers** - it called the API directly and missed proxy, region or SSO handling the CLI already had. Route through the CLI.
- **Works locally, fails in dev containers** - the extension looked for the CLI or login on the laptop. Set `extensionKind` and detect the remote CLI.
- **JetBrains users on the new IDE see "incompatible"** - the Gradle plugin pinned `untilBuild` to the current major. Unset it and verify against EAP.
- **Telemetry complaint on social media** - events fired with host telemetry off. Route through the telemetry logger and publish the event list.

## Reference

- `samber/developer-platform-skills@api-integration-surface-strategy` - whether the editor belongs in the surface roadmap at all.
- `samber/developer-platform-skills@github-action-offering` - the same thin-wrapper-over-CLI pattern for CI.
- `samber/developer-platform-skills@agent-skill-offering` - shipping an Agent Skill beside the CLI the extension wraps.
- `samber/developer-platform-skills@chrome-web-store-playbook` - a browser extension instead of an editor one: Chrome Web Store review, permissions and enterprise distribution.
