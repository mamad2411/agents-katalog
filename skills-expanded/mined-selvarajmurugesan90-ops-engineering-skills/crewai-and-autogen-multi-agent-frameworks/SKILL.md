---
name: crewai-and-autogen-multi-agent-frameworks
description: >
  Guides building multi-agent systems with role-based frameworks — CrewAI's
  crew/task/process model and Microsoft AutoGen's conversable-agent model —
  as opinionated implementations of multi-agent orchestration patterns. Use
  when a user asks to "build this with CrewAI," "set up a crew of agents,"
  "use AutoGen for multi-agent," "define agent roles and tasks in CrewAI,"
  "configure a GroupChat in AutoGen," or is deciding between CrewAI, AutoGen,
  and a hand-rolled or LangGraph-based multi-agent implementation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# CrewAI and AutoGen Multi-Agent Frameworks

## Purpose

[multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) describes
the generic topologies (supervisor/worker, pipeline, parallel/aggregation,
critic/debate) that justify splitting a task across multiple agents. CrewAI
and AutoGen are two concrete, higher-level frameworks that implement those
topologies with an opinionated, role-centric abstraction rather than
requiring you to wire message-passing and state by hand. **CrewAI** models a
multi-agent system as a **crew** of role-scoped **agents**, each assigned one
or more **tasks**, executed under a **process** (`sequential` — tasks run in
a fixed order, each consuming prior tasks' output; or `hierarchical` — a
manager agent delegates and reviews) — it is closest to the pipeline and
supervisor/worker topologies, expressed declaratively. **AutoGen** models a
multi-agent system as a set of **conversable agents** that exchange
messages in a shared conversation (a `GroupChat` with a chat manager
choosing the next speaker, or direct two-agent conversations), with a
distinct built-in role for a **UserProxyAgent** that can execute code and
optionally pause for human input — it is closest to the critic/debate and
supervisor/worker topologies, expressed as a conversation rather than a
fixed pipeline. Both frameworks trade some of LangGraph's low-level control
(explicit state typing, arbitrary cyclical graphs, durable checkpointing)
for faster time-to-first-working-crew when the task genuinely fits a
role-based mental model. This skill covers configuring each framework
correctly and choosing between them (and against LangGraph) for a given
task — it does not repeat the underlying "should this be multi-agent at
all" justification, which lives in
[multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).

## When to use

- The task is naturally described as a set of named roles collaborating
  (e.g. "a researcher, a writer, and an editor") and a declarative,
  role-first framework fits better than hand-wiring a graph.
- Building or reviewing a CrewAI crew's `agents.yaml`/`tasks.yaml` (or
  equivalent Python config) and choosing `sequential` vs. `hierarchical`
  process.
- Building or reviewing an AutoGen `GroupChat` — choosing the speaker-
  selection strategy, configuring a `UserProxyAgent`'s code-execution and
  human-input behavior.
- Deciding between CrewAI, AutoGen, LangGraph
  ([langchain-and-langgraph-agent-orchestration](../langchain-and-langgraph-agent-orchestration/SKILL.md)),
  and a hand-rolled orchestrator for a specific multi-agent task.
- An existing CrewAI crew or AutoGen group chat loops, has agents talking
  past each other, or produces redundant work, and needs debugging.
- Migrating a multi-agent prototype built in one of these frameworks toward
  (or away from) a lower-level graph-based implementation as requirements
  outgrow the framework's abstraction.

## Prerequisites & environment

- Python (both frameworks are Python-first; CrewAI has no first-party JS/TS
  SDK as of current releases — verify before assuming parity).
- CrewAI: the `crewai` package plus `crewai-tools` for common tool
  integrations; an LLM provider configured per-agent (CrewAI supports
  per-agent model overrides, so a cheaper model can drive a simple role
  while a stronger model drives a complex one).
- AutoGen: the `autogen`/`pyautogen` (or current successor package —
  Microsoft has re-branded and restructured AutoGen's packaging across
  versions; confirm the current package name and API surface before
  starting a new project) plus an LLM config dict per agent.
- For AutoGen's `UserProxyAgent` with code execution enabled: a sandboxed
  execution environment (Docker container or restricted subprocess) — never
  enable `code_execution_config` against an unsandboxed host process for
  agent-generated code you have not reviewed.
- A concrete task decomposition already justified via
  [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) —
  both frameworks make it easy to declare more agents than a task needs,
  and neither framework's ergonomics substitute for that justification step.
- Tool functions each agent will call, either defined natively in the
  framework's tool format or proxied from an MCP server; see
  [mcp-server-development](../mcp-server-development/SKILL.md) for building
  the MCP side.

## Step-by-step guidance

1. **In CrewAI, define each agent with a narrow role, goal, and backstory**
   — these three fields are what the underlying LLM call actually
   conditions on, not just documentation:
   ```python
   from crewai import Agent, Task, Crew, Process

   researcher = Agent(
       role="Research Analyst",
       goal="Find and summarize the three most relevant sources for a given topic",
       backstory="You are meticulous about citing sources and never invent facts.",
       tools=[web_search_tool],
       allow_delegation=False,
   )

   writer = Agent(
       role="Technical Writer",
       goal="Turn research findings into a clear, well-structured summary",
       backstory="You write for an engineering audience and avoid marketing language.",
       allow_delegation=False,
   )
   ```
   `allow_delegation=False` on worker agents keeps delegation authority
   concentrated in the process/manager rather than letting every agent
   freely hand off work to any other agent, mirroring the "fixed, testable
   roles over a dynamic pool" guidance in
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).

2. **Define tasks with an explicit expected output and, for sequential
   processes, an explicit context dependency** — CrewAI passes prior tasks'
   output into later tasks automatically when wired via `context`, which is
   the framework's version of the structured hand-off contract:
   ```python
   research_task = Task(
       description="Research recent developments in {topic}",
       expected_output="A bullet list of 3 findings, each with a source URL",
       agent=researcher,
   )

   writing_task = Task(
       description="Write a 200-word summary using the research findings",
       expected_output="A markdown summary citing each source",
       agent=writer,
       context=[research_task],   # explicit hand-off, not free-form
   )
   ```

3. **Choose CrewAI's process deliberately.** `Process.sequential` runs tasks
   in the declared order — the pipeline topology. `Process.hierarchical`
   adds a manager agent (either an LLM you configure or CrewAI's default
   manager) that plans and delegates dynamically — the supervisor/worker
   topology, at the cost of an extra planning LLM call and less
   predictable task ordering:
   ```python
   crew = Crew(
       agents=[researcher, writer],
       tasks=[research_task, writing_task],
       process=Process.sequential,
       verbose=True,
   )
   result = crew.kickoff(inputs={"topic": "vector database sharding"})
   ```

4. **In AutoGen, configure each conversable agent's `system_message` as
   narrowly as a CrewAI role**, and decide up front whether the
   conversation is a direct two-agent exchange or a `GroupChat`:
   ```python
   from autogen import ConversableAgent, GroupChat, GroupChatManager

   researcher = ConversableAgent(
       name="researcher",
       system_message="You research topics and report findings with sources. "
                       "You do not write final summaries.",
       llm_config={"config_list": [{"model": "claude-sonnet-4-5", "api_key": "${ANTHROPIC_API_KEY}"}]},
   )

   writer = ConversableAgent(
       name="writer",
       system_message="You turn research findings into clear summaries. "
                       "You do not do your own research.",
       llm_config={"config_list": [{"model": "claude-sonnet-4-5", "api_key": "${ANTHROPIC_API_KEY}"}]},
   )
   ```

5. **Configure `GroupChat`'s speaker-selection strategy explicitly** rather
   than relying on the default, since the default (LLM-based next-speaker
   selection) can pick an unexpected agent, especially with more than a
   handful of participants:
   ```python
   groupchat = GroupChat(
       agents=[researcher, writer],
       messages=[],
       max_round=6,                      # hard bound, same discipline as any agent loop
       speaker_selection_method="round_robin",  # deterministic; alternatives: "auto" (LLM-chosen), "manual"
   )
   manager = GroupChatManager(groupchat=groupchat, llm_config=researcher.llm_config)
   ```
   `max_round` is AutoGen's equivalent of the hard iteration cap described
   in [agent-architecture-design](../agent-architecture-design/SKILL.md) —
   set it explicitly rather than trusting the conversation to converge on
   its own.

6. **Scope `UserProxyAgent`'s code execution and autonomy explicitly** —
   this is AutoGen's most operationally sensitive default surface:
   ```python
   from autogen import UserProxyAgent

   user_proxy = UserProxyAgent(
       name="user_proxy",
       human_input_mode="ALWAYS",         # "NEVER" for fully autonomous runs; "TERMINATE" to ask only at the end
       code_execution_config={
           "use_docker": True,             # never run agent-generated code outside a sandbox
           "timeout": 60,
       },
       max_consecutive_auto_reply=5,
   )
   ```
   > **Warning:** setting `human_input_mode="NEVER"` with
   > `code_execution_config` enabled means agent-generated code executes
   > with no human checkpoint at all. Only do this against a fully
   > sandboxed, disposable environment with no access to real credentials
   > or production systems — treat it the same as any irreversible-action
   > tool per
   > [agent-architecture-design](../agent-architecture-design/SKILL.md).

7. **Cap delegation depth in CrewAI's hierarchical process and AutoGen's
   nested chats** — both frameworks support an agent's task spawning
   further sub-delegation, which needs an explicit ceiling
   (`max_iter` on a CrewAI agent, a bounded `max_round` and no nested
   `GroupChat`-within-`GroupChat` without a depth check in AutoGen) to
   avoid the unbounded recursive-delegation pitfall described in
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).

8. **Log the full conversation/task trace**, not just final output — CrewAI
   exposes task outputs and `verbose=True` logging; AutoGen's `GroupChat`
   exposes `groupchat.messages` as the full transcript. Both are what you
   need to debug agents duplicating work or talking past each other, the
   same failure modes described generically in
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).

## Best practices

- Treat CrewAI's `role`/`goal`/`backstory` and AutoGen's `system_message`
  with the same rigor as a production system prompt — vague or overlapping
  role descriptions across agents are the single biggest cause of
  duplicated work or role confusion in both frameworks.
- Default to CrewAI `Process.sequential` or AutoGen `speaker_selection_method="round_robin"`
  for anything that needs predictable, reviewable ordering; reserve
  `Process.hierarchical` or `"auto"` speaker selection for cases where the
  task genuinely needs dynamic delegation and you've accepted the added
  unpredictability and planning-call cost.
- Keep `allow_delegation=False` on CrewAI worker agents by default; enable
  delegation only on an explicit manager/supervisor role, mirroring the
  fixed-role guidance in
  [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).
- Never enable AutoGen code execution against a real filesystem, network,
  or credential set without Docker (or an equivalent) sandbox — this is a
  destructive-action risk, not a convenience trade-off to skip under time
  pressure.
- Use a cheaper/faster model for narrowly-scoped worker roles (a
  researcher summarizing one document) and reserve the strongest available
  model for planning/manager roles, the same cost-optimization principle as
  [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md).
- Re-evaluate whether a CrewAI/AutoGen crew could be replaced by a single
  well-scoped agent periodically — both frameworks make it easy to declare
  agents, which is exactly the failure mode
  [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) warns
  against: splitting because it "felt cleaner," not because of measured
  need.

## Common pitfalls

- **Symptom:** Two CrewAI agents (or two AutoGen conversable agents) both
  produce overlapping output — e.g. both research the same sub-topic — with
  no error, just redundant/contradictory results.
  **Fix:** This is the same task-boundary-overlap pitfall described in
  [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md).
  Tighten each `Task.description`/`ConversableAgent.system_message` to state
  what the role does *not* do, and check for overlapping tool access — two
  agents with the same tool and a vague task boundary will often both use it.

- **Symptom:** An AutoGen `GroupChat` with `speaker_selection_method="auto"`
  runs many rounds without converging, or the same agent keeps being
  selected to speak.
  **Fix:** Switch to `"round_robin"` or `"manual"` for predictability, or
  add explicit termination conditions to agent system messages (e.g. "reply
  TERMINATE when the summary is complete"); always set `max_round` as a
  hard backstop regardless of selection method.

- **Symptom:** A CrewAI crew using `Process.hierarchical` produces
  inconsistent results run-to-run for the same input.
  **Fix:** The manager agent's delegation plan is itself an LLM call and
  can vary; if reproducibility matters more than dynamic flexibility,
  switch to `Process.sequential` with explicit `context` dependencies
  between tasks instead of relying on the manager to reconstruct the same
  plan every run.

- **Symptom:** An AutoGen agent with `code_execution_config` enabled and
  `human_input_mode="NEVER"` executes a destructive shell command (e.g.
  deleting files) generated in response to a misleading or adversarial
  prompt.
  **Fix:** This is a real incident, not a tooling quirk — code execution
  with no human checkpoint should only ever run inside a disposable,
  network-isolated sandbox (Docker with no mounted credentials or
  production filesystem access); if that constraint can't be met, set
  `human_input_mode="ALWAYS"` or `"TERMINATE"` so a human reviews commands
  before they run.

- **Symptom:** A multi-agent crew/group-chat is noticeably slower and more
  expensive than expected for what turns out to be a fairly linear task.
  **Fix:** Count actual LLM calls per run (each agent turn, each manager
  planning call) — CrewAI's hierarchical process and AutoGen's `"auto"`
  speaker selection both add planning-overhead calls beyond the "useful
  work" calls; if the task is genuinely linear, a sequential process (or a
  single agent) removes that overhead entirely.

## Worked example

**Scenario:** Generate a weekly engineering digest summarizing merged PRs
and open incidents — the same task used as the parallel-aggregation example
in [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md),
built here as a CrewAI sequential crew for a team that wants a declarative,
low-code implementation rather than hand-wiring a graph.

```python
from crewai import Agent, Task, Crew, Process

pr_agent = Agent(
    role="PR Summarizer",
    goal="Summarize merged pull requests from the past week",
    backstory="You report only on merged PRs, with links, in one bullet each.",
    tools=[list_merged_prs_tool],
    allow_delegation=False,
)

incident_agent = Agent(
    role="Incident Reporter",
    goal="Summarize currently open incidents",
    backstory="You report only open incidents with severity and age.",
    tools=[list_open_incidents_tool],
    allow_delegation=False,
)

digest_writer = Agent(
    role="Digest Editor",
    goal="Combine PR and incident summaries into one Markdown digest",
    backstory="You never invent content not present in the inputs you're given.",
    allow_delegation=False,
)

pr_task = Task(description="List merged PRs from the last 7 days", expected_output="Bullet list with links", agent=pr_agent)
incident_task = Task(description="List currently open incidents", expected_output="Bullet list with severity and age", agent=incident_agent)
digest_task = Task(
    description="Combine the PR and incident summaries into one weekly digest",
    expected_output="A Markdown document with a PRs section and an Incidents section",
    agent=digest_writer,
    context=[pr_task, incident_task],
)

crew = Crew(
    agents=[pr_agent, incident_agent, digest_writer],
    tasks=[pr_task, incident_task, digest_task],
    process=Process.sequential,
)
digest = crew.kickoff()
```

Each agent has exactly one tool and a role description stating what it does
*not* cover (PRs vs. incidents), so `digest_writer` receives two clearly
separated, non-overlapping inputs via `context` rather than free-form text —
the same schema-based hand-off discipline recommended in
[multi-agent-orchestration](../multi-agent-orchestration/SKILL.md), here
expressed through CrewAI's `context` mechanism instead of a hand-rolled JSON
contract.

## Cross-references

- [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md) — the vendor-neutral topologies (supervisor/worker, pipeline, parallel/aggregation, critic/debate) and coordination pitfalls that CrewAI and AutoGen each implement in their own opinionated way.
- [langchain-and-langgraph-agent-orchestration](../langchain-and-langgraph-agent-orchestration/SKILL.md) — a lower-level, graph-based alternative when a task outgrows CrewAI/AutoGen's role-based abstraction and needs explicit cyclical control flow or durable checkpointing.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — the single-agent control-loop fundamentals (iteration caps, tool boundaries, human checkpoints) that still apply inside each individual CrewAI/AutoGen agent.
- [mcp-server-development](../mcp-server-development/SKILL.md) — building the tool-serving side that CrewAI/AutoGen agents call into, rather than defining every tool as an in-framework Python function.
