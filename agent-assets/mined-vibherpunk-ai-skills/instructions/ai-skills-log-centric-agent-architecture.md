# Copilot Instructions: Log Centric Agent Architecture
Description: Implement and manage AI agents where the log is the primary source of truth, enabling durability, scalability, and ownership.

# Log-Centric Agent Implementation Guide

## Overview
This skill teaches you to build AI agents where the event log is the source of truth, not the runtime or model. Key benefits include:
- **Reliability**: Survives process crashes
- **Scalability**: Parallel processing of agents
- **Ownership**: Avoid vendor lock-in

Learn the core principles in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Initialize Log Storage**
   ```python
   # Using AWS S3 for durable storage
   import boto3
   s3 = boto3.client('s3')
   
   def append_log(session_id: str, entry: dict):
       """Atomically append to log"""
       key = f"agents/{session_id}/log.jsonl"
       s3.put_object(
           Bucket='my-agent-logs',
           Key=key,
           Body=json.dumps(entry) + '\n',
           ACL='private'
       )
   ```

2. **Worker Loop**
   ```python
   def process_agent_step(session_id: str):
       # 1. Acquire distributed lock
       with redis.lock(f"agent:{session_id}"):
           # 2. Read full log
           log = s3.get_object(Bucket='my-agent-logs', Key=f"agents/{session_id}/log.jsonl")
           
           # 3. Reconstruct state
           state = reconstruct_state(log)
           
           # 4. Get model response
           prompt = create_prompt(state)
           response = model.generate(prompt)
           
           # 5. Append new event
           append_log(session_id, {
               'timestamp': datetime.utcnow().isoformat(),
               'eventType': 'model_output',
               'content': response,
               'sequenceId': len(log.splitlines()) + 1
           })
   ```

3. **State Reconstruction**
   ```python
   def reconstruct_state(log_entries: list) -> dict:
       """Project log into current state"""
       state = {'history': [], 'pending_actions': []}
       
       for entry in log_entries:
           if entry['eventType'] == 'user_input':
               state['history'].append(f"User: {entry['content']}")
           elif entry['eventType'] == 'model_output':
               state['history'].append(f"Agent: {entry['content']}")
               
               # Parse tool calls
               if 'tool_call' in entry['content']:
                   state['pending_actions'].append(parse_tool_call(entry['content']))
       
       return state
   ```

## Best Practices
1. **Log Design**:
   - Use immutable, append-only writes
   - Include sequence IDs for ordering
   - Store in durable, centralized storage

2. **Worker Implementation**:
   - Keep workers stateless
   - Implement heartbeat checks
   - Use exponential backoff for contention

3. **Error Handling**:
   ```python
   try:
       process_agent_step(session_id)
   except ToolTimeoutError:
       append_log(session_id, {
           'eventType': 'failure',
           'content': {'error': 'Tool timeout', 'step': 'email_send'}
       })
   ```

## Validation Steps
1. **Crash Recovery Test**:
   - Kill worker mid-process
   - Verify new worker resumes correctly

2. **Log Consistency Check**:
   ```bash
   # Verify no gaps in sequence IDs
   awk '{print $2}' log.jsonl | sort -n | awk 'BEGIN{prev=0} {if ($1 != prev+1) print "Gap at " prev+1; prev=$1}'
   ```

3. **Projection Validation**:
   - Generate multiple summaries from same log
   - Verify key decisions remain consistent

For complete implementation guidance, see [Practical Guide](references/practical_guide.md). To avoid common mistakes, review [Common Pitfalls](references/common_pitfalls.md).

## Reference Guides

### Common Pitfalls

# Common Pitfalls and Solutions

## 1. Treating Logs as Secondary
**Anti-pattern**: Storing logs as afterthought (e.g., local JSONL files without durability guarantees)
**Consequence**: Data loss when processes crash
**Solution**: Make log storage your primary architectural concern

## 2. Over-Compaction
**Anti-pattern**: Discarding raw logs after summarization
**Consequence**: Irreversible loss of agent history
**Solution**: Always retain raw logs; treat summaries as derived views

## 3. Provider Lock-in
**Anti-pattern**: Using proprietary log formats tied to specific platforms
**Consequence**: Inability to migrate agents
**Solution**: Use open formats (JSON Schema, Protocol Buffers)

## 4. State Leakage
**Anti-pattern**: Assuming tool calls are deterministic
**Example**: Agent sends email, then log is rewound - email remains sent
**Solution**: Clearly separate:
- Agent's view (log)
- World state (external systems)

## 5. Scaling Mistakes
**Anti-pattern**: Sticky sessions tying agents to specific workers
**Consequence**: Bottlenecks and difficult failover
**Solution**: Stateless workers + centralized log storage

## Debugging Tips
1. **Replay Testing**: Reconstruct agent state from log at any point
2. **Diff Analysis**: Compare projections from same log
3. **Failure Injection**: Kill workers mid-process to verify durability

### Core Concepts

# Core Concepts: Log-Centric Agent Architecture

## The Log as the Agent
At its core, this architecture posits that an agent's identity and state are not defined by its runtime environment or model, but rather by its immutable, append-only event log. This log contains every significant state transition:
- User inputs
- Model outputs
- Tool calls and their results
- Permission requests
- Failures

## Key Properties
1. **Durability**: The agent survives process failures because its state is reconstructed from the log.
2. **Scalability**: Workers can process any agent's state by reading its log, enabling horizontal scaling.
3. **Ownership**: The log becomes the valuable asset, not the runtime or model.

## Projections
Various components interact with projections (derived views) of the log:
- **Model Context**: A compacted summary fitting within context windows
- **UI State**: A rendered view of current status
- **Debugging**: Full trace of all events

## Compaction
While logs grow indefinitely, models require finite context. Compaction creates lossy summaries that:
- Preserve essential agent state
- Allow continuation of work
- Don't replace the raw log (which remains the source of truth)

### Practical Guide

# Practical Guide: Implementing Log-Centric Agents

## Log Structure
Design your log with these required fields:
```typescript
interface LogEntry {
  timestamp: string; // ISO-8601
  eventType: 'user_input' | 'model_output' | 'tool_call' | 'tool_result' | 'permission' | 'failure';
  content: string; // JSON string of event details
  sequenceId: number; // Strictly increasing
  sessionId: string; // Unique agent identifier
}

## Storage Requirements
1. **Durability**: Use write-ahead logging with fsync or equivalent cloud storage guarantees
2. **Atomicity**: Each append must be atomic (consider WAL or transaction logs)
3. **Access Control**: Implement fine-grained permissions for multiplayer scenarios

## Worker Implementation
Workers should:
1. Claim a session via distributed lock
2. Read the full log
3. Reconstruct state
4. Advance one step
5. Append new events
6. Release lock

Critical considerations:
- Workers must be stateless
- Never modify existing log entries
- Handle partial writes (use checksums)

## Compaction Strategies
1. **Windowed**: Keep last N entries + summary
2. **Semantic**: Identify and preserve key events
3. **Hybrid**: Combine recency with importance

Example compaction rule:
"If log exceeds 100 entries, summarize first 50 into 5 key points, keep last 50 verbatim"

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[The Log Is The Agent - Ishaan Sehgal, Omnara](https://www.youtube.com/watch?v=UPwGaM2MKHY)** by AI Engineer