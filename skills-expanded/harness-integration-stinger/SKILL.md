---
name: "harness-integration-stinger"
description: "Wire Wasp Nest capabilities across Claude Code, Cursor, Codex, and Cowork. Use for skill, agent, hook, MCP, or plugin portability. Read README.md for the guide map."

license: AGPL-3.0-or-later
compatibility: Claude Code, Cursor, ChatGPT Codex, Claude Cowork.
metadata:
  hive-tier: stinger
  hive-drone: harness-integration-wasp-drone
  research-window: 2026-08-14 (broadening pass; reuses queen-wasp-stinger 2026-08-14 research plus six new sources)
  case-study: Hivemind six-host installer (examples/case-study-hivemind-six-host-installer.md)
---

# harness-integration-stinger

Start with [README.md](README.md) for the workflow map and detailed references.

The integration playbook for `harness-integration-wasp-drone`. Encodes how to wire one capability (a skill, an agent, a hook-driven behavior, an MCP-backed tool) across The Wasp Nest's four harnesses - Claude Code, Cursor, ChatGPT Codex, Claude Cowork - from the first decision (which component type, which wiring mechanism) through capability detection, graceful degradation, portability, and distribution. Includes a full worked case study of a real six-host integration (Hivemind, a prior product this stinger originally documented) as a concrete example of every decision point answered end to end.

## Quick navigation

For current availability, fallback, release claims and personal action boundaries, load the focused procedures below before relying on dated host tables. Native loading, account access and independent review require separate observed receipts.

| Task | Guide |
|---|---|
| Select task-required packs and active prerequisite branches | `guides/12-select-task-packs.md` |
| Prove event/payload/trust/deadline behavior on actual host version | `guides/13-prove-hook-contract.md` |
| Audit selected owner command carriers and retained resources | `guides/14-audit-selected-command-coverage.md` |
| Separate source coverage, explicit selection and native availability | `guides/08-prove-selected-availability.md` |
| Retain skill procedure without a native agent, with explicit review/isolation losses | `guides/09-use-skill-fallback.md` |
| Bind release claims to installed-host discovery and execution receipts | `guides/10-qualify-installed-host-release.md` |
| Prepare personal work with scoped sources and no hidden sends | `guides/11-prepare-personal-work.md` |
| Coordinate parallel AI workers with exclusive ownership, actual capacity and stop/handoff proof | `guides/07-coordinate-parallel-workers.md` |
| Start here: what integration means, the four harnesses, the wiring-mechanism decision matrix | `guides/00-decision-framework.md` |
| Where does each component type (rules, commands, agents, skills, plugins) live, per harness | `guides/01-component-placement.md` |
| Wire hooks/lifecycle events, per harness, and know the real shared-event floor | `guides/02-hook-lifecycle.md` |
| Register an MCP server, per harness (JSON vs. TOML, cloud reachability) | `guides/03-mcp-registration.md` |
| Detect what a harness supports and degrade gracefully when it doesn't | `guides/04-capability-detection-and-degradation.md` |
| Keep a skill, rule, or tool contract portable (spec-six frontmatter, AGENTS.md, plugin manifests) | `guides/05-portability-and-contracts.md` |
| Ship through each harness's marketplace/install flow and its distribution gate | `guides/06-distribution-and-audit.md` |
| Worked example: a real six-host integration end to end | `examples/case-study-hivemind-six-host-installer.md` |

## Critical directives

Apply portable constraints to the capability being built, and case-specific mechanics only when its inspected source matches that case. Read the target host's actual capability list, selected-plugin registry and carrier before designing integration. A path, API or hook event from a dated example is not present-host proof.

1. **Preserve the capability's actual contract across supported hosts.** Record its real names, inputs, outputs and effects. Hivemind's named tools in the case study illustrate this practice; they are not mandatory tools for a different integration.
2. **Give hooks explicit failure and timing semantics.** Observational hooks may fail open; authorization or integrity gates must retain their intended refusal behavior. Confirm supported events, asynchronous execution and timeouts in the current host before wiring them. Never claim a hook or watchdog is active without observed configuration and execution.
3. **Keep capability detection cheap and side-effect free.** A directory or cache proves files exist, not that a plugin is selected. For Wasp Nest installed work, use the explicit selected-plugin registry and Core resolver, then verify prerequisites. Source-checkout paths cannot stand in for enabled installed components.
4. **Resolve resources against the actual carrier root.** Native plugins, home copies and cloud uploads have different available surfaces. Use the host's verified root/resolver and load resource paths from the returned component root rather than importing a previous product's bundle layout.
5. **Qualify the target distribution.** Validate the actual carrier, retained resources, notices and supported commands/hooks. Hivemind's ClawHub scan and pi raw-TypeScript rules remain case-specific examples; do not apply them to Wasp Nest or another project without that target surface.
6. **Register MCP only through a supported host transport.** Claude Code and Cursor can support MCP as well as hooks; one does not replace the other. Follow [MCP registration](guides/03-mcp-registration.md) and verify the current local/cloud execution surface before deciding connectivity. Do not infer public reachability or localhost support merely from a product name.
7. **Degrade explicitly when a surface is absent.** Keep the contract and report the missing capability. Do not invent a command, infer enabled availability from a cache, or silently change the requested architecture.

8. **Author portable skills against the six-field Agent Skills spec only.** Outside Claude Code proper, only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are legal `SKILL.md` frontmatter. Any Claude-Code-only field (`context: fork`, `disable-model-invocation`, `paths`, `hooks`, etc.) throws a hard packaging error on claude.ai uploads, the Skills API, and Cowork's "Save skill" pipeline. Source: `research/external/2026-08-14-agentskills-spec-six-fields.md` (source-repository research, not shipped with the plugin); queen-wasp-stinger distilled-research-articles.md, Claude Code §SUPPLEMENT.

9. **Use the current host's MCP config format.** Local Codex configuration uses TOML `mcp_servers`; Claude Code and Cursor use their supported JSON forms. Read [MCP registration](guides/03-mcp-registration.md) and validate the intended configuration through the actual host. Do not assume a pasted incompatible shape will be silently ignored or successfully registered.

10. **Distinguish local plugin runtimes from cloud connectors.** A cloud connector needs an endpoint reachable from its actual execution environment. A local desktop plugin may have a separate local MCP surface. Verify both carrier and runtime; do not assert that every Cowork connection runs through the cloud or can reach localhost.

11. **Compute the supported hook-event intersection before design.** Use currently verified host capabilities and the target carrier's registration surface. Record unsupported events and any approximated behavior. The dated case study's event counts and timeouts are historical evidence, not a guaranteed floor for a new native installation.

12. **Qualify worker coordination before fanout.** Read [worker coordination](guides/07-coordinate-parallel-workers.md); reuse selected AppPrimer Zero handoff resources, count actual slots including the coordinator, and preserve exclusive ownership and ordered candidate review. A prepared plan or worker status is not final integration proof.

13. **Keep proof layers separate.** Source coverage, selected registry, native discovery, actual execution and account permissions each need their own receipt. A direct skill read does not create an independent worker or reviewer. Personal-work preparation remains draft-only unless the specific external action is authorized. Use guides 08 through 11 and preserve unknowns.

14. **Select and qualify actual task coverage.** Use guides 12 through 14 for O287, O292 and O299. Close each active branch and preserve missing selected owners, resources and native event/invocation evidence as distinct gaps. Never invent a command or agent to fill a carrier gap.

## Scope note

This stinger covers the **integration surface** for The Wasp Nest's four harnesses (Claude Code, Cursor, ChatGPT Codex, Claude Cowork): per-harness component placement, the wiring-mechanism decision (hooks, native extensions, MCP, AGENTS.md/instruction files), capability detection and graceful degradation, cross-harness portability, and distribution. It also retains, as a labeled case study, the original Hivemind six-host adapter work (Claude Code, Codex, Cursor, Hermes, pi, OpenClaw) this stinger was first built around. It does **not** cover vector-store schema/write-path internals, the embeddings runtime, retrieval ranking internals, or MCP wire-protocol details beyond registration - route those to the relevant stinger (`vector-store-stinger`, `embeddings-runtime-stinger`, `retrieval-stinger`, `mcp-protocol-stinger`).

## Handoff map

- Vector-store schema and the capture/write-path internals behind an MCP-backed memory tool: route to `vector-store-stinger`.
- Embeddings model selection, batching, runtime cost: route to `embeddings-runtime-stinger`.
- MCP protocol internals (tool schemas, transport framing) beyond per-harness registration: route to `mcp-protocol-stinger`.
- Bundling pipeline topology and release CI: route to `ci-release-stinger`.
- Login/auth device flow and token vault security audit: route to `security-stinger`.

---

*Part of The Wasp Nest, curated by [Mario Aldayuz a.k.a @thenotoriousllama](https://github.com/thenotoriousllama).*
