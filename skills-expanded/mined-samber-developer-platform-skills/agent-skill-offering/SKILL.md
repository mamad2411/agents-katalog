---
name: agent-skill-offering
description: Ships an Agent Skill (SKILL.md) inside the GitHub repo of the library, CLI or SDK it documents, versioned with the code - repo placement, metadata.version bumped every release, CI that fails a release on a stale skill, tag-pinned installs (skills.sh, gh skill, ClawHub, plugin marketplaces), plugin manifests, OpenClaw gating, skill vs MCP vs CLI. Use whenever a tool maintainer mentions shipping a skill with their tool, a SKILL.md for their library, keeping a skill in sync with releases, or plugin.json versions for a skill beside code - even if they never say "agent skill". Not for standalone skill collections. Do NOT use for CLI command or --json design - use samber/developer-platform-skills@cli-interface-design; nor for MCP servers - use samber/developer-platform-skills@mcp-server-offering.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Agent Skill Offering

You are a release engineer for agent-facing tooling. Make a library, CLI, SDK or tool ship its own Agent Skill, in its own repo, so the skill an agent loads always matches the code version it runs.

The problem this solves: coding agents misuse tools from stale training data - removed flags, renamed functions, old defaults. A shipped skill fixes that only while it matches the installed version. A skill that drifts from the code teaches the same wrong calls, now with the maintainer's authority. Everything below exists to keep the two in lockstep.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. The file is an advisory reference, not a mandatory requirement. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.

## The lockstep rule

The hard rule of this skill. Audit every plan against it before anything else.

1. The skill MUST live in the same repository as the code it documents, because a separate skills repo has its own release cadence and drifts by construction.
2. The skill's `metadata.version` MUST equal the code version, bumped in the same commit or release job that bumps the code, because an installer or agent can only detect a mismatch it can read.
3. Every release tag MUST contain a skill matching that tag's code, because a tag-pinned install is the only reproducible install most channels offer.
4. A release MUST fail before its tag exists when the skill is stale - version mismatch, or a command, flag or symbol it names no longer exists - because a warning in a release log gets read after users installed the wrong skill.
5. A rename or removal of a skill MUST be treated as a breaking change of the tool, because installs, routing tables and other skills point at the skill by name.

Rationalizations to reject:

| Rationalization | Why it fails |
| --- | --- |
| "Patch release, the skill didn't change, skip the bump." | The version is the lookup key. A skill still saying 1.3.0 on the 1.3.1 tag reads as stale to every check and every user. Bump it by script; content can stay identical. |
| "We'll keep skills for all our tools in one `org/skills` repo." | That repo releases on its own clock. Its HEAD documents some mix of versions. The rule is per tool repo. |
| "Users install from the default branch anyway." | Then the default branch documents unreleased features to users on the last release. Pin installs to tags (step 6), or the gap is guaranteed. |
| "The version check is enough." | Equal versions prove only that someone bumped a string. Rule 4 also needs the content check (step 5). |

## Interview

Ask before designing; each answer changes a later step. Batch them - this is a tactical build, not a strategy interview.

1. What ships: a CLI binary, a library/SDK, or both? Which language, and how do users install it (language registry, Homebrew or another binary-only package manager, release download, container image)? (binary-only channels change step 6)
2. How is a release cut today: manual tag, release-please/changesets, goreleaser, a CI job on tag push? Where does the version live (tag only, `package.json`, `pyproject.toml`, a version constant)? Are tags prefixed (monorepo components), and are there maintenance branches or prereleases? What is the repo's license? (the skill's `license` matches it)
3. Which agents should use it: coding agents with a shell and the tool installed locally, chat assistants with no shell, or unattended agent fleets? (decides step 1)
4. What do agents get wrong today: invented flags, deprecated APIs, wrong auth flow, unsafe defaults? Collect three real failures - they become the skill's first content and its tests.
5. Does a skill, plugin manifest or AGENTS.md already exist anywhere for this tool, including community-written ones?
6. By when must the first skill ship, is this a one-off fix or a standing release practice, and what is the effort ceiling (one afternoon, or a maintained release-pipeline change)? May the tool's own binary gain a subcommand (step 6, bundled rung)? A near deadline keeps the default rungs; a standing practice promotes the starved ones.

## Workflow

1. Confirm what ships beside the skill.
2. Place the skill in the repo.
3. Write the content contract.
4. Wire the version to the code version.
5. Add the CI gates.
6. Choose install channels and pinning.
7. Publish multi-harness manifests.
8. List and measure.

If your harness has persistent memory, record: the version source of truth, the tag format, the gate list, the chosen channels and the pinned-install command. A later release run then checks the same gates instead of re-deriving them.

## 1. Confirm what ships beside the skill

The skill always ships (lockstep rule). This step decides what it carries and what sits beside it, by who calls the tool and what they need:

- **Agent operates a CLI, shell available** -> skill + the CLI with machine-readable output and non-interactive flags. A skill's description costs about 100 tokens until it loads; an MCP server's tool definitions typically cost one to two orders of magnitude more idle context.
- **Multi-step workflow** (setup, migration, major upgrade) -> a skill with `references/`. This is where skills measurably help most.
- **Knowledge every call needs** (current API names, removed functions) -> docs bundled in the package plus a short pointer the tool writes into the user's project agent-instructions file. On-demand skills can fail to trigger: in one framework's published evals the skill was never invoked in 56% of runs, while an always-loaded docs index scored 100%. Keep the skill for workflows and point it at the bundled docs.
- **No shell (chat assistant, hosted fleet), hosted auth or remote state** -> an MCP server, shipped in the same plugin as the skill. Route its design to `samber/developer-platform-skills@mcp-server-offering`.
- **Agent only reads docs on the web** -> agent-readable docs; see `samber/developer-relations-skills@coding-agent-docs-optimization`.

What to add beside the skill, for a coding-agent audience:

- effort: `MCP server > bundled docs + agent-instructions pointer > JSON output on the CLI > nothing`
- value (correct agent calls): `JSON output on the CLI > bundled docs + agent-instructions pointer > MCP server > nothing`
- efficiency: `JSON output on the CLI > bundled docs + agent-instructions pointer > nothing > MCP server`

Default rung: skill + JSON output on the CLI; hand the CLI's command, `--json` and exit-code design to `samber/developer-platform-skills@cli-interface-design`. Add the bundled-docs pointer when agents keep calling removed APIs even with the skill installed. Promote MCP only for an audience without a shell.

## 2. Place the skill in the repo

- Put each skill at `skills/<skill-name>/SKILL.md` at the repo root. Most installers discover `skills/` without configuration, and plugin manifests point at `./skills/`.
- Name the skill after the tool, qualified by job when there are several: `acme-cli`, `acme-cli-migrations`. The name is public API (rule 5).
- Split by job, not by command group: one skill per thing an agent is asked to do. Start with one; split when `SKILL.md` passes ~250 lines. Keep the set small: focused skills beat exhaustive bundles, and large skill libraries measurably shadow each other.
- Share cross-cutting rules (auth, safety, output parsing) in one skill the others tell the agent to read first, instead of copying them.
- Keep the skill out of the repo's own agent directories (`.claude/skills/`, `.agents/skills/`): those serve agents working on the repo itself, as does the repo's `AGENTS.md`. User-facing skills go in `skills/`.
- In a monorepo with several tools at independent versions, give each tool its own skill, checked against that tool's own version and tag prefix.
- Include the skill in every release artifact the code ships in (package `files` list, archive contents, embedded assets), and check it in CI (gate 3). A skill that exists only in git is invisible to registry users. Go modules carry `skills/` in the module zip automatically.

## 3. Write the content contract

Split ownership so nothing is stated twice:

- **The tool owns WHAT:** flags, arguments, types, defaults. Point the agent at `<tool> --help`, `<tool> <cmd> --help` or the generated reference instead of copying them.
- **The skill owns WHEN and WHY:** which command for which job, ordering, safe defaults, the three failures from interview question 4, how to read errors.
- **`references/` owns the long tail:** per-domain detail loaded only when needed.

Open the body with a two-sided version guard the agent executes. Some harnesses never show the frontmatter to the model, so the body carries one `Skill version:` line outside any code fence; the bump script rewrites it and gate 2 checks it. Name no other version anywhere in the prose.

```
Skill version: 1.4.0
Run `acme --version` first (libraries: read the installed package version).
- Same major.minor: continue. If only the patch differs, mention the matching tag once.
- Major or minor differs, in either direction: trust `acme --help` over this skill's
  command names, and tell the user to install the skill from their version's tag.
- A development build reporting `dev`: continue.
```

Follow the Agent Skills spec with keys `name`, `description`, `license` (the repo's own license), `compatibility`, `metadata`. Omit the spec's experimental `allowed-tools`: it pre-approves tools without a prompt. Put the version in `metadata.version` as a quoted string; the spec has no top-level `version`. Declare the binary in `compatibility` without a version number ("Requires acme-cli on PATH"), so no second version string goes stale. Write the description as what + when, with the tool's name and the tasks users type. For general skill-writing quality, use your preferred skill-authoring guidance; this skill covers shipping, not prose.

Good and bad bodies for CLI and library skills: [references/skill-content-examples.md](references/skill-content-examples.md).

## 4. Wire the version to the code version

- Pick one source of truth: the release tag, or the file the release tool already bumps.
- Generate every other version field from it: each `SKILL.md` `metadata.version`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`. Leave `version` out of the marketplace file's `plugins[]` entry: the plugin's own manifest silently wins when both are set.
- Bump them in the commit the release tag points at. A bump made after tagging never reaches the tag. Never by hand across five files:
  - Release-PR tool (release-please, changesets): add every file to its extra-files or version step, including the `Skill version:` body line (step 3), so the bump lands in the release PR.
  - Tag-only version (goreleaser, plain tags): a `make release VERSION=x.y.z` target that runs `scripts/check-skill-version.py x.y.z --write --manifest ...`, then the gates, commits, tags and pushes. Goreleaser itself runs after the tag and cannot bump.
- Between releases, each release branch carries its last released version; only a release commit changes it. Run the same bump and gates on maintenance branches (`release/1.3`) as on the default branch.
- Bump on every release, prereleases included (`1.5.0-rc.1`). Version equality is the contract. Some plugin installers key their cache on the manifest `version`: a set but unbumped version reports "already latest" and users keep the stale copy.
- Treat `metadata.version` and its `Skill version:` body copy as provenance for humans, guards and checks. No installer reads them; installers resolve a git tag, a commit or a manifest `version`.

## 5. Add the CI gates

Run on every pull request that touches code or skills, and again before the tag is created. Ranked:

- effort: `golden agent tasks > content check > changed-surface check > version equality == spec validation == security scan`
- value: `content check > golden agent tasks > version equality > changed-surface check > security scan > spec validation`
- efficiency: `version equality == spec validation > content check > security scan > changed-surface check > golden agent tasks`

The version-equality / spec-validation tie is real: both are one offline command, and each catches a failure the other cannot.

1. **Spec validation** - the reference validator from the spec (pin its version) or an equivalent frontmatter check. Fails on a missing field, a name not matching its directory, a description over 1,024 characters.
2. **Version equality** - copy this skill's `scripts/check-skill-version.py` (Python 3.8+ standard library; `--help` lists the options) into the tool's repo. Run it on every pull request against the version source of truth (for tag-only repos, the last tag: `git describe --tags --abbrev=0`), on the release PR or in `make release` before tagging, and once more on the tag as a backstop (a tag-time failure means deleting the tag). It checks `metadata.version`, the `Skill version:` body line and every manifest; it rejects a top-level `version:`, unquoted, duplicate, flow-style or nested `metadata` keys (`--allow-nested openclaw` admits OpenClaw's block), and strips monorepo tag prefixes with `--tag-prefix`.
3. **Content check** - on the artifact the release will publish (built with the release version stamping, before any publish step), compare the skill against a machine-readable surface (`<tool> help --json`, nested `--help`, the exported API). Stale direction: every command, flag and identifier the skill names must exist. New-surface direction: every public command added since the last release must be mentioned or allowlisted. For libraries, compile or type-check every code block. Also assert the packaged artifact contains `skills/`. Projects whose version checks stayed green have shipped skills naming APIs removed a major version earlier; this gate is what catches that.
4. **Changed-surface check** (pull requests) - when the public surface changes and no file under `skills/` changed, fail or require an explicit "skill unaffected" label.
5. **Golden agent tasks** (starved) - a handful of real tasks an agent runs against the built tool with the skill installed, scored on two numbers: trigger rate (did the agent load the skill) and pass rate. Highest effort, so it is always deferred. Promote it once agents are a main user channel, or after the first issue traced to a wrong skill.
6. **Security scan** - an agent-skill security scanner over `skills/` (see step 8).

Default rung: gates 1-3 and 6 before tagging, gates 1-4 and 6 on pull requests. Workflow snippets, the `--help` extraction pattern, the library variant and release-tool hooks: [references/ci-release-gates.md](references/ci-release-gates.md).

## 6. Choose install channels and pinning

No installer resolves "the skill matching the code I installed" by itself. Most can pin a git tag or commit; one resolves the latest tagged release when unpinned; others follow the default branch. A tag-pinned install matches only at install time: the binary can upgrade silently (package manager, auto-update) while the pinned skill stays put, which is why the guard in step 3 checks both directions. Ranked:

- effort: `bundled with the code > plugin marketplace pinned to a tag > tag-pinned git install > default-branch install`
- value (version match guaranteed): `bundled with the code > plugin marketplace pinned to a tag > tag-pinned git install > default-branch install`
- efficiency: `tag-pinned git install > bundled with the code > plugin marketplace pinned to a tag > default-branch install`

- **Default rung: tag-pinned git install.** Generate the exact tag-pinned command per channel into every release note. In the README, print the commands with a `v<your-installed-version>` placeholder and the tool's version command, so the README never goes stale. Near-zero effort once tags carry matching skills (rule 3).
- **Binary-only package managers** (Homebrew, apt, a release download): users get the binary and no skill, so a git install is a second manual step they skip. Print the matching install command in the tool's own `--help` or first-run output, and treat this as the promotion condition for the bundled rung below.
- **Starved option: bundled with the code** - the skill ships inside the package or binary and a subcommand installs or syncs it (`<tool> install --skills`, `<tool> update`), or the skills installer links it from the installed package. Version match by construction, highest effort. Promote it when most users install through a package manager, or when stale-skill issues keep arriving.
- Add a runtime drift notice when the tool can know: compare the installed skill's recorded version with its own version and print one agent-parseable line, e.g. `skill acme-cli 1.3.0 differs from acme 1.4.0; run: acme skills update`.
- Self-hosted plugin marketplace (`source: "./"`): users who add it from the default branch get merged-but-unreleased skill text under the last released `version`, and the cache may never refresh. Tell them to add the marketplace at a release tag, or keep a `stable` branch moved only at release.
- Keep the default branch releasable, or tell users that a default-branch install may document unreleased features.
- Prereleases: keep them off every default install. Cut them from a `next` branch (or tag a commit off the default branch), mark the GitHub release as a prerelease so latest-release resolution skips it, and move the `stable` branch or recommended marketplace tag only on final releases.

Per-channel commands, ref syntax, lockfiles, update behaviour and manifest fields: [references/distribution-channels.md](references/distribution-channels.md).

## 7. Publish multi-harness manifests

- Ship at repo root, each pointing at `./skills/`: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (self-hosting the plugin, `source: "./"`, no `version` in the entry), `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`.
- Every manifest's `version` comes from step 4's source of truth and is checked by gate 2.
- Copy author, homepage, repository and license from the repo's existing package metadata; never publish placeholder owners.
- Keep the skill itself harness-neutral: no harness-only frontmatter, no harness paths, capabilities described rather than tool names.
- OpenClaw needs no extra manifest: it installs the repo as a bundle at a git tag (from any of the manifests above) or a ClawHub publish. Add a `metadata.openclaw` block map whose `requires.bins` block list names the tool's binary, so OpenClaw offers the skill only where the tool is installed. It is a spec deviation; allow it in gate 2 only for that key. Keys, ClawHub publishing and the MIT-0 catch: [references/distribution-channels.md](references/distribution-channels.md) § OpenClaw and ClawHub.
- Every `plugin.json` and `marketplace.json` field, source form and directory check: [references/plugin-manifest-fields.md](references/plugin-manifest-fields.md).

## 8. List and measure

- Install-ranked directories (skills.sh) index a repo's `SKILL.md` folders and rank them by installs reported by the installer's telemetry. The README install section is the listing's real driver.
- Add repository topics that directory crawlers index (`agent-skills`, `gemini-cli-extension`), and link the install command from the tool's official docs.
- Submit the plugin to Anthropic's Claude plugin directory from `https://claude.ai/directory/manage` (paid claude.ai plan): **Submit new**, **Plugin bundle**, the repository, then **Validate**. Set **Branch or tag** to the `stable` branch moved only at release (step 6): left empty it follows the default branch, so every merge becomes a candidate version that goes live once auto-publish is on or someone selects **Publish**. A tracked tag must be re-pointed each release. A README under 40 words or a missing license blocks the listing.
- Publish under the organization's own namespace and claim obvious name variants: agents hallucinate skill names, and attackers register them.
- Expect public security audits of listed skills, and pass them before launch:
  - Keep `scripts/` few, readable, offline and dependency-pinned; call the tool's own published CLI instead of bundling binaries.
  - Never tell the agent to fetch and follow remote content: the most common audit finding on benign skills is exactly that indirect-injection exposure.
  - Run an agent-skill security scanner such as Snyk Agent Scan (`snyk-agent-scan`) in CI next to the spec validator, and sign release tags. Workflow step, token and flag cautions: [references/ci-release-gates.md](references/ci-release-gates.md) § Gate 6.
- Measure correctness, not reach. Install counts measure interest and can be inflated. The signals that matter: trigger and pass rate per release (gate 5), issues tagged "agent misuse", and how often the drift notice fires.

## Failure modes

- Skill in a separate repo, versioned on its own clock -> lockstep rule 1.
- `version: 1.4.0` at frontmatter top level -> non-spec; move under `metadata` as a quoted string.
- Version guard that checks only "older than" -> a silently upgraded binary passes it; check both directions (step 3).
- Guard that reads only `metadata.version` -> invisible to the agent in harnesses that strip frontmatter; keep the `Skill version:` body line.
- Install docs say `owner/repo` with no ref -> users get the default branch, not their version.
- SKILL.md is a pasted flag reference -> stale on the next release; defer WHAT to `--help`.
- Version bumped by hand in five manifests -> one drifts; generate them (step 4).
- `version` set in both the plugin manifest and its marketplace entry -> one silently wins; keep it in the plugin manifest.
- ClawHub publish without `--version` -> the registry picks its own next patch; pass the release version.
- `metadata.openclaw` copied in flow form (`{...}` or `[...]`) -> strict YAML validators reject the file; convert to block style.
- Directory submission tracking the default branch -> every merge becomes a candidate listing version; track the `stable` branch.
- CI checks only version strings -> a removed flag ships in a "matching" skill; add gate 3.
- Version gate run only on the tag -> the stale tag already exists; run it before tagging.
- Skill script downloads and runs remote code -> fails audits and opens an injection path.
- Silent skill rename -> broken installs and routes. Rename in a major release, and keep a stub skill under the old name for one major that points at the new one.
- The repo's own contributor-facing `AGENTS.md` mistaken for the user-facing skill -> different audience, different file.
- Always-needed API facts only in an on-demand skill -> the skill may never load; bundle the docs and point at them (step 1).

## Invocation examples

- "I maintain a Go CLI. Coding agents keep inventing flags. Ship a skill with it and keep it in sync across releases."
- "Our npm SDK has a SKILL.md in a separate repo that's two majors behind - fix the setup."
- "Add a CI check that fails the release if the skill's version doesn't match the tag."
- "Should we ship an MCP server, a skill, or both for our CLI?"

Expected output: the repo layout, the version-wiring change, the CI gate list with commands, the install commands per channel, and the manifests - each checked against the lockstep rule.

## Measurement

The setup passes when all hold:

- A release with a deliberately stale `metadata.version` fails before its tag exists.
- A release where the skill names a removed flag or symbol fails CI.
- Every manifest's `version` equals the tag on the last three releases.
- Every release note prints a tag-pinned install command.

## References

- `samber/developer-platform-skills@api-integration-surface-strategy` - for a SaaS platform choosing among all its integration surfaces; this skill starts once an agent skill is chosen.
- `samber/developer-platform-skills@sdk-package-publishing` - registry publishing mechanics for the package the skill rides in.
- `samber/developer-platform-skills@github-action-offering` - the same release discipline (frozen contract, immutable tags, CI gates) for the tool's official GitHub Action.
- `samber/developer-platform-skills@agent-integration-surfaces` - the platform-wide agent plan the skill sits in: access policy, agent identity, signup, measurement.
