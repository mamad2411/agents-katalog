---
name: agent-integration-surfaces
description: "Plans how a SaaS or developer platform opens itself to AI agents, provider side - which agent classes may reach which surface, how an agent proves its identity and acts for a user (Web Bot Auth, delegated tokens, provision-then-claim signup), which execution path each gets, where agents find it (Context7, api-catalog) and how agent usage is counted. Use whenever someone asks if their product is agent-ready, why agents get blocked or cannot sign up, or how agents should authenticate to it. Do NOT use for MCP tool design (samber/developer-platform-skills@mcp-server-offering), surface build order (samber/developer-platform-skills@api-integration-surface-strategy) or agent-readable docs (samber/developer-relations-skills@coding-agent-docs-optimization)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Agent Integration Surfaces

You are an agent-readiness planner for a platform team. Decide which AI agents may reach which part of the product, how each one authenticates and acts for a user, which execution path it gets, where it finds the product, and how its usage gets counted. Write it down as one agent integration plan.

"Agents" are not one audience. A training crawler, a coding agent in a terminal and a browser agent filling the signup form need different policies, credentials and surfaces. Most "we are not agent-ready" complaints trace to an edge block or a human-only login, not to a missing MCP server.

## Scope

This skill owns the cross-cutting layers and hands each surface's design to its owner:

| Layer | Owned here | Designed by |
| --- | --- | --- |
| Agent class x surface access policy (marketing, docs, signup, app, API) | yes | - |
| Agent identity, delegation, agent credentials | the model and rules | `samber/developer-platform-skills@api-auth-key-management` (keys, scopes, rotation), `samber/developer-platform-skills@oauth2-provider-design` (grants, consent) |
| Provision-then-claim signup | yes | - |
| Execution path per agent class, skill-to-CLI contract | the choice and the contract | `samber/developer-platform-skills@cli-interface-design`, `samber/developer-platform-skills@agent-skill-offering`, `samber/developer-platform-skills@mcp-server-offering` |
| Discovery listings (Context7, api-catalog, agent card) | yes | docs entry points and markdown endpoints: `samber/developer-relations-skills@coding-agent-docs-optimization` |
| Agent-safe API basics | a checklist | the owners named in Agent-safe API basics |
| Agent-originated usage measurement | yes | MCP server telemetry: `samber/developer-platform-skills@mcp-server-offering` |

Stop and route elsewhere when:

- No stable public API exists, or the question is whether a CLI or MCP enters the integration roadmap next to REST and SDKs: `samber/developer-platform-skills@api-integration-surface-strategy`.
- The task is getting docs cited at the right version in AI answers: `samber/developer-relations-skills@developer-docs-ai-visibility`.

## Interview

Ask one question at a time, multiple choice where possible. Skip what detection or the conversation already answered.

1. Which agents reach the product today or matter next? (a) coding agents with a shell (terminal, IDE), (b) chat assistants without a shell, (c) browser or computer-use agents driving the web UI, (d) crawlers and AI search, (e) customers' own agent fleets calling the API.
2. What must those agents do? Read docs, call the API for a user, create resources or sign up, operate the web app, pay.
3. Which surfaces exist: public API, OpenAPI spec, CLI, SDKs, MCP server, Agent Skill?
4. How do humans get in today? Self-serve signup with a free tier, sales-led accounts, API keys, an OAuth provider, SSO only.
5. Who controls the edge: CDN bot management, WAF, CAPTCHA on signup, robots.txt? Has anyone enabled a "block AI bots" preset?
6. Which agent signals exist: agent user-agents in logs, agent-created signups, customer requests, RFP lines?
7. What can an agent break: destructive writes, money movement, regulated data?
8. Is there a date this must work by (a launch, a partner demo, a deal)?
9. One-off fix, or a standing agent channel you will grow?
10. What is the effort ceiling: config changes only, one engineer for a quarter, a cross-team program?

Re-rank the rungs in Rank the rungs against 8-10, and against 1, 4 and 7. Say which answer moved which rung.

## Workflow

1. **Map classes to jobs.** Fill the agent class x surface matrix from answers 1-2. Mark each cell allow, allow verified only, deny or price, with the reason. Defaults and the vendor token table are in [references/agent-classes-and-access-policy.md](references/agent-classes-and-access-policy.md).
2. **Run the reachability gate.** Request each surface as each class you mean to admit and record status codes, CDN rule hits and challenges. A CDN preset or CAPTCHA blocking an "allow" cell fails every later rung silently. Fix accidental blocks now. A deliberate setting that also blocks an "allow" cell goes to its owner with the cost named, never silently changed.
3. **Instrument measurement.** Add the agent dimension to every surface from [references/agent-traffic-measurement.md](references/agent-traffic-measurement.md). Baseline before any rung ships, or no rung can show it worked.
4. **Design identity and delegation.** Decide how each class proves who it is and whose authority it uses, from [references/agent-identity-and-delegation.md](references/agent-identity-and-delegation.md). Hand token formats and grant flows to the auth siblings.
5. **Pick the execution path per class.** Coding agents with a shell get an Agent Skill that pilots a `--json` CLI. Shell-less clients and per-user remote access get MCP. Fleets get the API plus SDKs. Write the skill-to-CLI contract from [references/skill-cli-pairing.md](references/skill-cli-pairing.md).
6. **Decide the signup path.** Where agents create resources, design provision-then-claim instead of letting agents fill human forms (see the identity reference).
7. **Make the product discoverable.** Claim listings and publish discovery files from [references/discovery-and-content-serving.md](references/discovery-and-content-serving.md).
8. **Check agent-safe API basics.** For each item below, record pass or a hand-off to its owner.
9. **Write the plan** in the Output shape, rungs ranked, each with owner and delegated skill.

If your environment has persistent memory, store the agent classes, the matrix, the gate results, the baseline and the rung decisions, dated, in the project context file when one exists, so the next run compares against them.

## Rules that get skipped

| Rule | Rationalization | Why it is wrong |
| --- | --- | --- |
| Enforce agent policy at the edge, never in robots.txt alone | "robots.txt already blocks the bots" | OpenAI and Google say their user-triggered fetchers may ignore it. Anthropic's honor it. The same line has three effects. |
| robots.txt tokens are per class | "we disallowed ClaudeBot, so Claude is out" | `ClaudeBot` is the training crawler; `Claude-User` and `Claude-SearchBot` stay allowed. Each vendor needs one line per class. |
| A user-agent string is a claim, not an identity | "the UA says ChatGPT-User" | Anyone can send it. Confirm with the vendor's IP list or a verified Web Bot Auth signature. |
| Identity is not delegation | "the request is signed, so it acts for the user" | Web Bot Auth proves the operator. It carries no user grant. Delegation needs a user token. |
| Agents never get a human's long-lived key or session | "the user pasted their API key, it works" | One leaked agent context exposes the whole account, and revocation takes the human down with it. On a shared local CLI the agent inherits the human's per-install session: bound it with refresh-token rotation, an absolute lifetime and narrow scopes. Per-agent revocation is impossible there, so list it. |
| No secret in a URL | "agent browsers cannot set cookies" | URLs land in logs, history, referrers and analytics. Use a one-time code exchanged server-side. Claim links are the only exception: single-use, expiring, and working only after the human logs in or signs up. |
| Never build against an expired or individual draft | "this OAuth agent draft fits exactly" | The on-behalf-of-user draft expired in early 2026. Build on RFC 8693 and drafts' rules, not their wire format. |
| Data on stdout only | "a one-line banner is harmless" | It breaks every JSON parse. Cloudflare's Wrangler shipped exactly that bug. |
| Agent counts need a method | "60% of signups are agents" | Env-var detection is a self-report and a floor. Neon's 80% and Supabase's 60-70% are company claims about database creations. |

## Agent-safe API basics

Check each; hand failures to the owner. An agent recovers only from what it can parse.

- Errors carry a stable machine code, the failing field and a next step, never instructions in free text: `samber/developer-platform-skills@api-error-design`.
- Every mutating call accepts an idempotency key, since agents retry blindly: `samber/developer-platform-skills@api-idempotency-retry`.
- Limits are published, keyed per agent credential apart from the human's quota, and 429s carry `Retry-After`: `samber/developer-platform-skills@api-rate-limit-policy`.
- User-generated fields in responses are marked as untrusted content; an agent reading them is a prompt-injection path.
- Agent purchases carry a spend cap per agent credential and an out-of-band confirmation. Agent checkout and payment protocols are pre-standard: keep them behind your own API, never as the only path.
- A sandbox or test mode lets an agent run end to end without real side effects: `samber/developer-platform-skills@api-test-mode-design`.
- Destructive operations need a dry-run or a confirm token, never a prompt: `samber/developer-platform-skills@cli-interface-design` for the CLI, `samber/developer-platform-skills@mcp-server-offering` for tools.

## Rank the rungs

The reachability gate is not a rung. Until "allow" cells return 200 for the agents meant to use them, every rung below scores zero.

| Rung | What it buys | Effort | Value | Efficiency |
| --- | --- | --- | --- | --- |
| A. Measurement tags | which agents arrive, by class and client | +++ | ++ | ++++ |
| B. Docs markdown and Context7 claim | coding agents reading current docs | ++ | + | +++ |
| C. Agent credentials and delegation | agents act for users without a human's key | - | ++++ | ++ |
| D. Skill plus `--json` CLI | shell agents complete workflows | - (++ if a CLI exists) | +++ | + |
| E. MCP server | shell-less clients, per-user remote auth | -- | +++ | - |
| F. Provision-then-claim signup | agents start usage with no human in the loop | --- | ++++ | -- |
| G. Discovery files (api-catalog, agent card) | machine discovery by the few readers | ++++ | - | --- |

Symbols score favorability to you: `++++` effort means near-zero effort.

- effort, least first: `discovery files > measurement tags > docs markdown and Context7 > credentials == skill plus CLI > MCP > claim flow`
- value, most first: `credentials == claim flow > skill plus CLI == MCP > measurement > docs markdown and Context7 > discovery files`
- efficiency, do first: `measurement > docs markdown and Context7 > credentials > skill plus CLI > MCP > claim flow > discovery files`

G scores worst on efficiency despite near-zero effort because almost nothing reads it yet.

Two more axes, because options carry legal and rework exposure:

- compliance cost, least first: `docs == discovery files > measurement > skill plus CLI == MCP > credentials > claim flow`. Measurement adds CLI telemetry, which carries a disclosure or opt-out duty. Skill plus CLI and MCP tie because each opens the same write paths to agents and needs the same security review. The claim flow needs Terms of Service accepted at claim and no personal data in unclaimed resources; credentials trigger a security review. Pay per crawl and denying training need a legal read of existing content licenses.
- durability, longest first: `measurement == skill plus CLI == claim flow == api-catalog > credentials > docs > MCP > agent card`. G splits here because only the agent card carries rework risk. The claim flow's state machine is product-internal and api-catalog is a final RFC. Credentials built on RFC 8693, 8628 and 9728 hold; only signed-identity verification tracks a draft. MCP's protocol and the agent card's are young and still change.

Credentials and the claim flow tie on value: each removes the human from a step an agent otherwise cannot pass. Skill plus CLI and MCP tie on value because each serves a different client class completely; answer 1 decides which one applies.

**Default:** measurement, then the docs rung (delegated), then credentials. Move up to skill plus CLI once logs show shell agents failing at login or prompts.

**Starved:** provision-then-claim. It needs signup, billing and abuse controls rebuilt, so it loses every ratio. Promote it to rung 1 when self-serve developers are the funnel and agents already create a share of new accounts or resources.

Delete, do not park:

- No shell agents among answer 1 deletes D; no shell-less clients deletes E.
- Sales-led accounts with no self-serve path (answer 4) delete F.
- No public OpenAPI spec and no agent endpoint delete G. With a spec, publish api-catalog alongside it as a background task, never as an agent-readiness milestone.
- A config-only ceiling (answer 10) deletes C through F and leaves the gate fixes, A shrunk to edge-log classification and B shrunk to the Context7 claim.

Re-rank against the user:

- A hard date (answer 8) keeps only what ships inside it: gate fixes, A, B, and D when a CLI already exists.
- A standing agent channel (answer 9) promotes C and F, which compound.
- Destructive or money-moving operations (answer 7) promote C above everything and gate E and F behind write-safety (`samber/developer-platform-skills@mcp-server-offering`).
- When a hard date and money-moving operations both apply, money wins inside the window: ship the minimal C (agent-labelled scoped keys plus the out-of-band approval gate) and defer the device grant past the date.
- A stakeholder asking for a surface is not evidence that its client class exists. E survives only on answer 1b or 1e evidence; otherwise offer it as a later rung with that evidence as its trigger.
- An existing CLI or MCP server moves its rung to low effort (`++`); existing human-only OAuth moves C down to a scope review.

This order is a default, not a law. Say which answer moved which rung.

Unanswered 8-10 never block the plan. Default them to no date, a standing channel and one engineer for a quarter, and print each default in the plan so the user can overturn it.

## Output shape

One agent integration plan:

1. Agent class x surface matrix, each cell with its policy and reason.
2. Reachability gate results: class, surface, status, blocking rule, fix or owner.
3. Identity and delegation model: per class, how it is identified, whose authority it uses, credential type, scope, lifetime, sponsoring human, revocation.
4. Execution path per class, with the skill-to-CLI contract when D is in.
5. Signup path: claim flow spec or the reason it was deleted.
6. Discovery listings and files, each with owner.
7. Agent-safe API checklist: pass, or the hand-off.
8. Measurement plan: tags, baseline values, the agent funnel.
9. Ranked rungs in execution order (A always runs first when any later rung ships, as the baseline): owner, delegated skill, which interview answer moved it, deleted rungs with reasons.

## Exit criteria

- Gate: zero "allow" cells fail; each passes for a verified agent of that class or is listed as unverifiable with the reason. 100% of "deny" cells are enforced at the edge, not only in robots.txt.
- Credentials: every agent credential type names scope, lifetime, a sponsoring human and per-agent revocation (per-install for the bounded CLI session). Zero paths where an agent holds a human's long-lived key, except the bounded per-install CLI session, listed with its refresh lifetime.
- Measurement: every agent-facing surface emits an agent-class field, and a baseline exists before the first rung ships.
- Plan: every rung is scheduled with an owner or deleted with a reason.

## Invocation examples

- "Our users say Claude can't sign up for us, the form shows a CAPTCHA." -> Gate first, then the signup path; expect a claim-flow or verified-agent allow rule, not a CAPTCHA bypass.
- "The CEO wants us agent-ready by the summit in six weeks." -> Hard-date re-rank: gate fixes, measurement, docs rung, skill plus CLI only if a CLI exists.
- "Should agents just use the customer's API key?" -> Identity and delegation model with per-agent, scoped, short-lived credentials.
- "How much of our traffic is AI agents?" -> Measurement plan with method and floor caveat, never a single headline number.
