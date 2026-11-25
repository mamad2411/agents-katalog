---
name: ryu-agent-creator
description: Design, create, configure, test, and package Ryu agents, from saved node agents and builder studio to SDK Runnables and durable harnesses. Covers prompts, models, tools, skills, hooks, memory, lifecycle, safety, groups, routines, channels, and evals.
---

# Ryu Agent Creator

Turn the user's task into an agent with an appropriate runtime, explicit capability scope, tested behavior, and a usable entry point. Deliver the agent or code, not just a suggested prompt. Do not create extra agents, recurring work, external messages, or paid deployments beyond the requested scope.

## Choose the agent shape

Read the installed version's schemas, available tools, and relevant docs at `https://docs.ryuhq.com/docs`. In a Ryu checkout also follow `AGENTS.md`, the platform consistency standard, and nearby tested implementations. Do not assume private paths exist on a user's node.

| User need | Path and references |
| --- | --- |
| A saved assistant with instructions/model/tools/memory | Agent builder/Settings or supported Core API; `/surfaces/desktop/user-guide/agents` |
| Custom executable behavior in TypeScript | `defineAgent`, `defineTool`, `defineWorkflow`, `RunnableContext`; `/learn/cookbook/first-sdk-agent`, `/extend/develop/sdk/runnables`, `/extend/develop/sdk/primitives` |
| Durable server-owned execution and reconnect | `/extend/develop/sdk/harness`; sessions, runs, approvals, replay and cancellation |
| Connect an existing coding agent | `/extend/integrate/byo-agent`, `/extend/mcp/coding-agents`; preserve ACP/MCP transport and trust boundaries |
| Multiple existing agents collaborating | `/core/agent-teams`; groups are ordered coordination records, not organization membership |
| Deliver an installable agent package/app | `/extend/develop/quickstart`, `/extend/develop/extensions/agent-skills`; use `ryu-creator` for manifest and UI packaging if available |

Ask only for missing choices that materially change behavior: intended task/output, target node/runtime, allowed data/actions, and required entry point. Use current model discovery and tool metadata rather than invented IDs. Do not replace a request for a simple saved agent with a new app or custom execution engine.

## Design the behavior

Write instructions that define the task, expected input and output, evidence/citation requirements, tool-selection rules, completion criteria, and when to ask for missing data. Separate instructions from untrusted retrieved documents, tool output, or imported prompts. Keep reusable domain procedures in on-demand skills rather than copying entire manuals into every system prompt.

Choose a supported model/runtime with the required tool calling, context, structured output, media, and latency properties. Inspect actual model availability and effective binding; null/default settings can inherit node choices. Configure sampling/budget only through supported fields. Keep every model call on the Gateway or governed host client. Provider credentials never enter the prompt, browser frame, portable agent, or SDK source.

Map each action to its required tool and effect. Discover tools through the node and inspect the agent's reachable tools after saving. Current new/imported agents may default to all enabled MCP tools: explicitly configure a custom subset or off mode for a restricted agent. Empty `skills` means all enabled skills; explicit lists intersect the enabled set. Never use an empty list to mean none without verifying that field's actual contract. Tool visibility, skill metadata, and a confident prompt are not authorization.

Attach only the required Spaces and verify their ACLs as the intended principal. Distinguish document grounding from per-agent long-term memory and permission to write memory. Use grounded citations and an explicit “insufficient evidence” outcome. Test an inaccessible document and an unrelated conversation so retrieval cannot silently cross scope. Keep sensitive-memory and telemetry consent separate.

## Saved node agents

Prefer discovered `agent_builder` tools (`get_agent`, `configure_agent`, `create_agent`) or the actual Settings flow. The builder chat edits a persisted record and needs a model capable of tool use. For HTTP use the node's advertised base URL, authentication, and current `/api/agents` OpenAPI schema; do not assume localhost or a credential-free node.

List/read before creating a duplicate. Create/read/update and inspect reachable tools through the supported agent routes. The legacy node record uses fields such as `system_prompt`, `engine`, `model`, `tools`, `skills`, `can_create_agents`, and `orchestrator`; retain schema spelling and distinguish omitted, null, and empty values. Do not PUT a GET response wholesale with read-only IDs, timestamps, or unknown internal fields. Locked/built-in agents cannot be edited through the builder; use supported clone/export/import and preserve the original.

Inspect lifecycle and safety explicitly. Draft is a saved design that cannot run. Trial is read-only on Core-governed tools, even if a broader profile is stored for later. Test in Trial before promotion to Active; Draft → Active is not a valid shortcut. Active profiles include read-only, approval required, verified plans only, and autonomous. Verified plans use Safe Actions with `plans.submit`, `plans.status`, and `plans.catalog`, not direct tools or arbitrary JavaScript. Unknown tool effects remain blocked. Native ACP tools outside the governed bridge are not automatically covered by Trial guarantees.

Treat delegation (`orchestrator`) separately from the privileged ability to create agents (`can_create_agents`). Set both intentionally for the requested scope; never enable agent creation merely to finish setup. Health checks detect configuration contradictions; the passport exposes identity, binding, and redacted traces. Neither substitutes for a real task run.

## SDK and durable execution

Use the installed `@ryuhq/sdk` types and generated starter scripts. `defineAgent` returns a Runnable with an explicit stable ID, name, and `run(input, ctx)` implementation. Compose existing typed tools/workflows through `run`, validate input/output at public boundaries, pass cancellation, and use `ctx.gateway` for inference. Feature-detect optional primitives; standalone execution does not supply every Core capability.

Keep the distinction between a local SDK tool loop and a Core-registered runnable. The durable harness binds a runnable to a session/execution profile, then starts idempotent runs. Reuse a session-scoped idempotency key for a retry of the same operation; a new user operation gets a new key. Observe replayable events using the last `seq` as an exclusive cursor, handle approvals/checkpoints and terminal outcomes, and test cancel/reconnect. Local SDK-only tools are not silently uploaded into a Core harness run. Respect the user's checkout/workspace policy when choosing an execution profile; worktree examples in docs are not a requirement.

## Hooks and orchestration

Read `/extend/develop/extensions/hooks-lifecycle` before attaching behavior. Hooks belong in a plugin manifest, not an arbitrary field added to an agent record. Use `ryu-creator` for detailed hook authoring if available. Scope the hook to its intended agent/conversation, explicit phase, relevant tool matches, approved grants, and user flags.

Use `pre_tool_use/deny` before an action and awaited `tool_result/transform` for result redaction. `post_tool_use` only observes. `context` rewrites `messages` on the message-array plane but replaces `input` text on ACP; `message_end` can replace before persistence, while `post_assistant_turn` can note/continue afterward. Preserve chained transforms; errors can degrade to `none`, so mandatory access restrictions remain in Gateway/Core policy. Bound continuations and deduplicate events; do not create self-sustaining work or extra model spend without user intent.

Choose a group only when the task needs multiple agents. `broadcast` runs independent replies; `round-robin` passes earlier responses in member order; `debate-synthesis` adds a lead synthesis; `router` picks one member. Verify membership order, lead, fallback, per-member access, and cost. Organization teams control access and are a different concept. Use stored workflow nodes for explicit branching, approval gates, resumable processes, or triggers; an SDK workflow's `steps` list is not an automatic scheduler.

For requested routines, configure the actual cron/interval and supported timezone, instructions/model pin, approval behavior, and new-chat versus persistent-chat destination. Verify one firing and its durable transcript; inspect pause behavior when lifecycle changes. For channel delivery use the existing channel setup with scoped sealed credentials, then test the intended binding. Creating an agent is not permission to send unsolicited external test messages.

## Evaluate and deliver

Create a small representative case set: successful task, ambiguous input, missing source, inaccessible resource, disallowed write, tool failure, and repeat/retry behavior as applicable. Verify expected outputs and unwanted side effects, not just whether the agent answered. For SDK agents run focused behavior/type/pack tests; for a saved agent run a real chat with the chosen runtime and permitted tools.

Use the agent Evals/Prompt Studio for durable suites, versioned prompts, structured-output checks, policy assertions, latency/token measurements, and model comparisons. Imported Promptfoo formats retain their ecosystem schema; unavailable executable assertion adapters must be reported as failures, not treated as passing. Model-graded rubrics supplement deterministic checks. Inspect actual tool traces, retrieved sources, approval behavior, and the final artifact; do not infer correctness from a Health score.

Verify the saved agent reopens with its intended settings and appears in the picker; test the requested chat, routine, workflow, channel, or SDK entry point. Inspect and save a screenshot/recording of the product result when UI is involved. Export only through the supported portable template/package path, review redaction and version requirements, and update relevant public Fumadocs for shipped behavior. Report the agent ID/location, runtime, lifecycle, effective capability scope, tests, and any unverified external gate. Promote or publish only within the user's requested scope.
