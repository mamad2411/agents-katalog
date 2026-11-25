---
name: task-router
description: |
  Route requests to the best-fit skill based on user intent.
  Use when the user asks for routing, workflow selection, or when a request spans multiple capability domains.
---

<skill name="task-router" version="1.0.0">
  <metadata>
    <keywords>
      <keyword>route</keyword>
      <keyword>router</keyword>
      <keyword>dispatch</keyword>
      <keyword>workflow</keyword>
      <keyword>skill-selection</keyword>
    </keywords>
  </metadata>

  <goal>Choose a single best-fit router skill for a request when the user explicitly asks for routing or workflow selection.</goal>

  <core_principles>
    <principle name="Minimal Ceremony">
      <rule>Only activate routing when it reduces confusion or improves execution quality.</rule>
    </principle>
    <principle name="Narrowest Match">
      <rule>Select the single most specific skill that covers the user's primary intent.</rule>
    </principle>
  </core_principles>

  <when_to_use>
    <trigger>User explicitly invokes or asks for task routing.</trigger>
    <trigger>User asks which skill or capability should handle a request.</trigger>
    <trigger>The request spans multiple possible capability domains and a route decision would reduce confusion.</trigger>
  </when_to_use>

  <when_not_to_use>
    <condition>The request is straightforward and can be handled directly.</condition>
    <condition>The user already named the skill to use.</condition>
    <condition>Routing would add ceremony without improving accuracy or execution quality.</condition>
  </when_not_to_use>

  <routing_table>
    <route trigger="Archive, memory, code search, docs index, git history, graph" skill="archive-manager" />
    <route trigger="Planning, architecture, API design, frontend/backend/database design" skill="architect" />
    <route trigger="Build or update skills, workflows, rules, automations, custom MCP tools" skill="agent-builder" />
    <route trigger="Implementation, refactor, tests, commits, PRs, deployment" skill="code" />
    <route trigger="Debugging, fixes, reviews, CI/CD, dependencies, security, performance" skill="quality-repair" />
    <route trigger="Onboarding, morning routine, handoff, explicit teaching mode" skill="project-continuity" />
    <route trigger="Validated research, documentation, tool selection" skill="research-docs" />
    <route trigger="MCP operations, Docker MCP troubleshooting, Serena activation" skill="mcp-ops" />
  </routing_table>

  <workflow>
    <step number="1" name="Classify Request">
      <instruction>Identify the primary outcome the user wants.</instruction>
      <instruction>Use project-continuity for teaching only when the user explicitly asks for learning support.</instruction>
    </step>
    <step number="2" name="Choose Smallest Capability">
      <instruction>Select one primary router skill from the routing table.</instruction>
      <instruction>Choose multiple skills only when the request genuinely crosses responsibilities.</instruction>
    </step>
    <step number="3" name="Return Route Decision">
      <instruction>Return the recommended skill, confidence, rationale, and immediate next action.</instruction>
    </step>
  </workflow>

  <output_format>
    <field>recommended_skill</field>
    <field>confidence</field>
    <field>reason</field>
    <field>next_step_instruction</field>
  </output_format>

  <related_skills>
    <skill>architect</skill>
    <skill>code</skill>
    <skill>quality-repair</skill>
    <skill>research-docs</skill>
    <skill>archive-manager</skill>
    <skill>mcp-ops</skill>
    <skill>agent-builder</skill>
    <skill>project-continuity</skill>
  </related_skills>
</skill>
