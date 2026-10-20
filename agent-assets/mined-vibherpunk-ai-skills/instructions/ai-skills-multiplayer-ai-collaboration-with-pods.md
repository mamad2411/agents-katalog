# Copilot Instructions: Multiplayer Ai Collaboration With Pods
Description: Implement flocking algorithm principles (local separation, distant attraction, alignment) to coordinate AI agents and humans in collaborative workflows using shared state pods.

# Multiplayer AI Collaboration with Pods

## Overview

This skill implements collaborative workflows between multiple AI agents and humans using Dust's pod architecture and flocking algorithm principles. Key concepts are explained in [Flocking Algorithm](references/flocking_algorithm.md) and [Pod Architecture](references/pod_architecture.md).

## Workflow

1. **Initialize Pod**
   ```python
   # Create new collaborative pod
   pod = create_pod(
       name="Team Weekly",
       participants=["pm", "designer", "engineer"],
       shared_fs="gcs://team-weekly-123"
   )
   ```

2. **Spawn Sub-Agents**
   ```python
   # Create specialized agents for each task
   slides_agent = pod.add_agent(
       role="slide_creator",
       skills=["data_analysis", "presentation_design"]
   )
   ```

3. **Implement Flocking Rules**
   - **Local Separation**: Trust-based task ownership
     ```python
     assign_task(agent, task, authority_level="full")
     ```
   - **Distant Attraction**: Cross-reference related work
     ```python
     related_work = find_related_conversations(pod, current_topic)
     ```
   - **Alignment**: Enforce vision constraints
     ```python
     validate_output(task, constraints=["on_brand", "technical_accuracy"])
     ```

4. **Coordinate Work**
   ```python
   # Agent workflow for weekly prep
   def prepare_weekly(pod):
       for slide in weekly_slides:
           session = pod.create_session(owner=slide.owner)
           session.run_task(
               "prepare_slide",
               inputs={"data_sources": slide.sources}
           )
       pod.monitor_completion(deadline="2h_before_meeting")
   ```

5. **Consolidate Outputs**
   ```python
   # Combine all slide frames into final presentation
   final_deck = combine_frames(
       pod.get_files("/pod/slides/*.frame"),
       template="company_standard"
   )
   ```

## Best Practices

1. **Bidirectional Design**: Follow principles in [Bidirectional Design](references/bidirectional_design.md)
2. **State Management**:
   - Keep session-specific files in /session
   - Move shared artifacts to /pod
3. **Error Recovery**:
   ```python
   try:
       agent.execute_task()
   except UncertaintyError:
       request_human_input(agent.current_context)
   ```

## Common Pitfalls

1. **Over-Management**: 
   - Bad: Humans micromanaging agent file movements
   - Good: Trust agents to handle /session space

2. **Isolated Work**:
   - Bad: Agents working in private chats
   - Good: All collaboration happens in pod-visible sessions

3. **Vision Drift**:
   - Bad: No alignment checks on outputs
   - Good: Regular validation against core constraints

## Validation

1. **Flocking Verification**:
   - Confirm 3 rules are active in all workflows
   - Check for emergent coordination patterns

2. **Pod Integrity**:
   - Verify file system permissions
   - Test version recovery scenarios

3. **Bidirectional Testing**:
   - Have humans complete agent-created tasks
   - Have agents continue human-started work

## Reference Guides

### Bidirectional Design

# Bidirectional Design Principle

## Core Concept

Any feature must be equally accessible to both humans and agents. This creates symmetry in collaborative workflows and prevents artificial barriers between human and AI work.

## Implementation Guidelines

1. **API Parity**: 
   - All UI actions must have equivalent API endpoints
   - All API features must have UI representations
2. **State Visibility**:
   - Agents and humans see the same data structures
   - No hidden state or privileged interfaces
3. **Interaction Patterns**:
   - Humans can interrupt/take over agent workflows
   - Agents can request human input when stuck

## Example: Task Management

- **Human Actions**:
  - Create task via UI
  - Assign to agent
  - Mark complete
- **Agent Actions**:
  - Create task via API
  - Self-assign work
  - Update status
  - Spawn sub-tasks

## Pitfalls to Avoid

- Creating "agent-only" features that humans can't understand
- Building "human-only" workflows that agents can't participate in
- Assuming certain actions will always be human-driven or agent-driven

## Testing Approach

For every new feature:
1. Implement human interface
2. Simultaneously build agent API
3. Verify round-trip:
   - Human creates → agent modifies
   - Agent creates → human modifies

### Flocking Algorithm

# Flocking Algorithm for AI Coordination

## Core Principles

The flocking algorithm provides a framework for autonomous coordination between multiple agents (or between agents and humans) through three simple rules:

1. **Local Separation**: Small repulsive forces that prevent crowding (e.g., trust-based delegation where humans don't micromanage)
2. **Distant Attraction**: Pulling forces toward shared objectives (e.g., writing culture that surfaces related work)
3. **Alignment**: Common direction/orientation (e.g., clear company vision)

## Implementation in AI Systems

- **Writing Culture as Attraction**: At Stripe, mailing lists served as the 'distant attraction' mechanism by exposing related work across teams
- **Trust as Separation**: When an agent/human claims responsibility for a task, others stop worrying about it
- **Vision as Alignment**: Clear, simple mission statements ("Dev API for payments") create natural alignment

## Technical Considerations

- Requires shared state visibility (like Dust's pod file system)
- Needs mechanisms for discovering related work (automated or manual)
- Must maintain bidirectional accessibility (all features available to both humans and agents)

## Example Patterns

- Weekly team meeting automation where agents:
  1. Create individual slide sessions
  2. Ping responsible humans
  3. Consolidate outputs
- Project pods with shared tasks that both humans and agents can create/edit/complete

### Pod Architecture

# Pod Architecture for Multiplayer AI

## Core Components

A pod is a collaborative unit containing:

- **Humans**: Team members participating in the workflow
- **Agents**: AI workers assisting with tasks
- **Sessions**: Individual interaction threads between humans and agents
- **Shared State**: Common file system and data store

## Technical Implementation

- **File Systems**: 
  - Session-local storage (GCS-backed via FUSE)
  - Pod-wide shared storage (/pod directory)
- **Access Patterns**:
  - Agents can move files between session and pod storage
  - Humans interact through UI that mirrors the pod structure
- **Versioning**:
  - All changes versioned through GCS
  - Agents track edits in context for easy rollback

## Workflow Example: Team Weekly

1. Trigger agent creates pod
2. Sub-agents spawn per slide:
   - Pull data from metabase/GitHub
   - Pre-build slide content
3. Human collaborators review/refine in parallel
4. Consolidation agent:
   - Checks completion status
   - Follows up with laggards
   - Assembles final presentation

## Security Considerations

- Access controls for pod participants
- Versioning for recovery from bad edits
- Approval workflows for high-stakes actions

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Agents & the $40M Bet on Multiplayer AI](https://www.youtube.com/watch?v=NsLPju6TZVc)** by MLOps.community