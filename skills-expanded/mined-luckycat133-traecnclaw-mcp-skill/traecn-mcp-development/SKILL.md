---
name: traecn-mcp-development
description: Develop, review, refactor, and verify Luckycat133/traecn-mcp. Use for the traecnclaw-to-traecn-mcp naming migration, CLI/CDP/MCP changes, gateway task lifecycle, version adapters, packaging, or repository development guidance. Preserve the frozen MCP surface and compatibility boundaries; do not use this Skill merely to operate TraeCN.
compatibility: Repository development uses Node.js 22+ and CommonJS. Live desktop verification requires macOS and an authorized TraeCN/CDP session; mock tests do not establish live compatibility.
metadata:
  author: Luckycat133
---

# TraeCN MCP Development

Develop one local runtime, not a new agent framework or several independent
controllers. Read root `AGENTS.md` first. Use the public `skills/traecn-mcp`
Skill for operating the installed runtime, not as a development plan.

This Skill's canonical directory is `.agents/skills/traecn-mcp-development`.
The `.codex` and `.claude` development entries are symlinks to it. Keep it
repository-local and separate from the generated public runtime Skill.

## Start from evidence

Record the checked-out commit, branch, working-tree changes, requested scope,
and available environment. Do not overwrite user work. Treat a reported local
test pass as owner-provided evidence until its commit, command, and result are
available; do not claim to have rerun it. Do not repeatedly run unchanged gates
merely to reproduce an already adequate result.

Read only the owning implementation and its tests, then select the applicable
reference:

- [Naming and architecture](references/naming-and-architecture.md) for any
  rename, ownership change, protocol change, or compatibility-sensitive work.
- [Roadmap and acceptance](references/roadmap.md) for prioritization, migration
  closure, and the next concrete deliverable. Its review baseline is historical,
  not a claim about a future checkout or a public channel's current status.

Write a small plan: affected contract, implementation owner, regression test,
verification tier, and rollback when relevant. Implement the requested slice;
do not turn a docs change into a runtime rewrite or a release.

## Product and naming invariants

The current display name is **TraeCN MCP**. Use `traecn-mcp` for the public
repository, source package, executable, and runtime Skill, and
`traecn-mcp-development` for this development Skill. Never introduce a new
`traecnclaw-*` development package or product-facing command.

Brand labels, compatibility identifiers, and historical evidence are different
classes. Do not bulk-replace `traecnclaw`, rename persisted state, republish an
npm package, change Registry identity, or rewrite old release evidence merely
to obtain a zero-match search. The reference identifies current exceptions and
the evidence required to migrate each. Keep the source package's publication
safety and do not infer that an unscoped `traecn-mcp` npm package is published.

## Ownership before implementation

Production task execution follows adapters -> shared gateway -> CDP -> TraeCN.
The gateway owns durable task identity, preparation, serialized desktop access,
queues, cancellation, recovery, review/approval checkpoints, and completion.
Clients adapt intent and results; they do not implement a second task engine.

`src/client` owns the HTTP client and command catalog. The OpenClaw `lib`
re-exports remain shims. `src/mcp` owns schemas, authorization adaptation,
protocol/Tasks translation, framing, and stdio. `src/cdp` owns desktop I/O;
`src/trae-adapters` owns version-specific selectors/capabilities/fixtures.
`src/config` owns configuration; `src/shared` holds reusable primitives.
`src/skill` is the JavaScript compatibility API, not this development Skill.

The Web Control Console remains the human control surface; CLI remains setup,
diagnostics, service operations, scripting, and recovery. Existing diagnostic
CDP probes are not permission to bypass gateway ownership for task execution.
OpenClaw and install directories are adapters/channels, not alternate runtimes.

## Preserve the observable contract

Read `src/mcp/contract.js`: product contract v5 contains exactly 20 tools in a
frozen order. Do not add polling, waiting, recovery, proof, process, event-ack,
or generic execution tools. A new gateway capability need not become an MCP
tool. A tool-set change requires an explicit migration, not a version bump alone.

Read `src/mcp/protocol.js` and conformance tests for supported wire versions;
these are independent of contract v5. Preserve era negotiation, authorization,
error/result semantics, stdout framing, subscription cleanup, and semantic
parity between text and structured results. Never use the server's own decoder
as the only conformance oracle. Preserve terminal idempotency replay and
nullable-error/output-schema cases.

`mcp-server.js` is a thin entry: no arguments mean stdio; arguments mean CLI.
No startup banner, help text, or diagnostic logs may leak into protocol stdout.
Keep stable tool names, client keys, environment aliases, IDs, and exported
compatibility entry points unless their migration is separately authorized.

## Task and desktop correctness

Accepted, queued, running, or input-required is not completed. Preserve task,
conversation, submission, interaction, and parent/child identities across
retries and restarts. An uncertain send must not become another prompt. Reuse
the existing durable identity and reconcile the original attempt.

Cancellation must remain durable; late callbacks must not revive cancelled
work. Storage failure must not turn unconfirmed output into final success.
Keep task cancellation distinct from explicitly stopping visible untracked
work. Bind approvals, questions, reviews, deletion, and stop actions to the
current task/native conversation and exact pending interaction. Preserve all
existing confirmation and audit safeguards in both legacy tools and Tasks.

Place maintained selectors in versioned adapters with sanitized fixtures.
Unknown versions are unverified, not automatically supported. Environment
selector overrides are local diagnosis, not a shipped compatibility fix.
Never infer stable conversation identity from a title or invent an ID for an
empty draft. Assert the postcondition of an interaction, not just a click.

## Implement and validate the smallest relevant slice

Use CommonJS, existing test-runner/assert conventions, and injected drivers,
stores, clocks, and network/process hooks. Characterize existing behavior before
moving ownership; remove superseded paths only after callers and compatibility
requirements are accounted for.

Choose gates by change, using commands actually present in `package.json`:

| Changed surface | Focused gate, then broaden when justified |
| --- | --- |
| Docs/development Skill | Frontmatter/name, links, paths, symlinks, scoped diff; no desktop required |
| Public runtime Skill | `npm run check:skill-contracts`, `npm run check:local-skill`, relevant Skill tests |
| CLI/launcher | `npm run test:cli`, setup/launcher tests, `npm run test:mcp-stdio-smoke` |
| MCP/protocol/Tasks | Relevant `src/mcp/*.test.js`, `npm run test:mcp-conformance`, stdio smoke |
| CDP/version adapters | Relevant driver tests, `npm run test:trae-adapters`; live verification only for real compatibility claims |
| Gateway/task lifecycle | Relevant gateway/store/recovery tests, `npm run test:system` |
| Packaging/distribution | `node scripts/public-mirror.test.js`, `npm run test:release`, actual target-channel install where authorized |

For source changes that affect MCP metadata, run `npm run sync:skill-contracts`.
After any public runtime Skill change, run `npm run sync:local-skill`; its
`.codex/skills/traecn-mcp` mirror must match the complete canonical tree, not
only `SKILL.md`. Do not put developer instructions into that generated package.
Use `npm run verify:static` and the repository-wide `npm run verify` for the
appropriate wider checks. Run `npm ci` when the locked dependency graph is
needed; a docs-only review need not install dependencies or operate the desktop.

For authorized live readiness, use `npm run doctor`, `npm run inspect:verify`,
and `node scripts/live-uat.js --strict --require-ready --require-verified-adapter`.
A missing desktop is a limitation, not a passed live gate. Restarting TraeCN,
changing profiles/accounts/models, `--cleanup-queue-probes`, `--delegate`, and
quota-consuming proof execution require their applicable task authorization;
non-quota does not mean non-mutating. Prefer disposable state and never touch
the installed user's service/profile as a side effect of release validation.

## Deliver and stop

Report changed files and behavior, executed commands/results, evidence tier,
remaining risks, and tests not run. Distinguish static, mock, artifact,
live-desktop, host, and published-channel evidence. Attach the commit/artifact
identity to compatibility claims. Neither this Skill nor a passing mock test
is proof that a release was published or a live model task completed.

Preserve root workflow rules. Do not merge, publish, migrate user state, spend
quota, or change accounts/models outside the current authorization. A review
branch/PR is not a merged or released product. Keep release versions and
historical evidence unchanged in a naming-policy-only change.
