---
name: "agent-handoff"
description: "Implement structured handoffs between agents with JSON-based state transfer, conflict detection, and acknowledgment protocols"
---

# Agent Handoff Skill

## When to activate

- Passing work from one agent to another in a multi-agent workflow
- Implementing request/response cycles between agents in a pipeline
- Building agent teams where one agent depends on another's output
- Debugging why an agent receives incorrect or incomplete input from a prior agent
- Ensuring state mutations are correctly propagated between agents

## When NOT to use

- Single-agent loops (no handoff needed)
- Asynchronous event-driven workflows without explicit request/response
- Workflows where agents do not directly depend on each other's outputs

## Instructions

### Handoff Packet Schema

A handoff is a JSON packet passed from one agent to the next:

```json
{
  "handoff_id": "hof_xyz123",
  "from_agent": "researcher",
  "to_agent": "analyst",
  "timestamp": "2026-06-15T14:15:30Z",
  "session_id": "sess_abc789",
  "trace_id": "tr_xyz456",
  
  "phase_name": "research",
  "phase_status": "completed",
  
  "payload": {
    "sources": [
      {"title": "...", "url": "...", "credibility": "high", "summary": "..."},
      {"title": "...", "url": "...", "credibility": "medium", "summary": "..."}
    ],
    "research_summary": "Found 15 credible sources on quantum computing...",
    "research_duration_seconds": 900
  },
  
  "metadata": {
    "tokens_used": {"input": 2400, "output": 1850},
    "model": "claude-opus-4-20250514",
    "output_schema": {
      "type": "object",
      "properties": {
        "sources": {"type": "array"},
        "research_summary": {"type": "string"}
      }
    }
  },
  
  "constraints_for_next_agent": [
    "Do not contradict findings from sources with credibility = 'high'",
    "Budget max 30 minutes for analysis phase"
  ],
  
  "required_tools_for_next_agent": ["web_search", "fetch_url"],
  
  "next_steps": {
    "agent": "analyst",
    "action": "analyze_findings",
    "estimated_latency_seconds": 1800
  }
}
```

### Validation Before Handoff

The sending agent must validate the payload before handoff:

```python
def validate_handoff(handoff_packet, expected_schema):
    """
    Validate that the handoff packet matches the expected schema.
    Raises ValueError if validation fails.
    """
    # Check required fields
    required = ['handoff_id', 'from_agent', 'to_agent', 'payload', 'timestamp']
    for field in required:
        if field not in handoff_packet:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate payload against schema
    import jsonschema
    jsonschema.validate(
        instance=handoff_packet['payload'],
        schema=expected_schema
    )
    
    # Validate timestamp is recent
    from datetime import datetime, timedelta
    ts = datetime.fromisoformat(handoff_packet['timestamp'].replace('Z', '+00:00'))
    if datetime.now(ts.tzinfo) - ts > timedelta(seconds=300):
        raise ValueError("Handoff timestamp is stale (> 5 minutes old)")
    
    return True
```

Do not proceed with handoff if validation fails. Log the error and escalate.

### Sending a Handoff

```python
def send_handoff(handoff_packet, to_agent_inbox='.claude/agent-inboxes/'):
    """
    Write handoff packet to the receiving agent's inbox.
    Return acknowledgment wait handle.
    """
    import json
    from pathlib import Path
    
    # Write to agent inbox
    inbox_dir = Path(to_agent_inbox) / handoff_packet['to_agent']
    inbox_dir.mkdir(parents=True, exist_ok=True)
    
    handoff_file = inbox_dir / f"{handoff_packet['handoff_id']}.json"
    with open(handoff_file, 'w') as f:
        json.dump(handoff_packet, f)
    
    # Return wait handle (wait for acknowledgment)
    return {
        'handoff_id': handoff_packet['handoff_id'],
        'acknowledgment_file': inbox_dir / f"{handoff_packet['handoff_id']}.ack"
    }

def wait_for_acknowledgment(wait_handle, timeout_seconds=30):
    """
    Poll for acknowledgment from the receiving agent.
    Timeout if no acknowledgment received.
    """
    from pathlib import Path
    from time import sleep
    from datetime import datetime, timedelta
    
    ack_file = Path(wait_handle['acknowledgment_file'])
    start = datetime.now()
    
    while datetime.now() - start < timedelta(seconds=timeout_seconds):
        if ack_file.exists():
            with open(ack_file, 'r') as f:
                import json
                ack = json.load(f)
            return ack
        sleep(0.5)
    
    raise TimeoutError(f"No acknowledgment after {timeout_seconds}s for {wait_handle['handoff_id']}")
```

### Receiving a Handoff

```python
def receive_handoff(from_agent, inbox_dir='.claude/agent-inboxes/'):
    """
    Poll for incoming handoffs from a specific agent.
    Return the first available handoff.
    """
    from pathlib import Path
    import json
    
    inbox = Path(inbox_dir) / from_agent
    
    # Find first unacknowledged handoff
    for handoff_file in sorted(inbox.glob('*.json')):
        ack_file = handoff_file.with_suffix('.ack')
        if not ack_file.exists():
            with open(handoff_file, 'r') as f:
                handoff = json.load(f)
            return handoff
    
    return None

def acknowledge_handoff(handoff_packet):
    """
    Send acknowledgment back to the sending agent.
    """
    import json
    from pathlib import Path
    
    ack = {
        'handoff_id': handoff_packet['handoff_id'],
        'acknowledged_by': 'analyst',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'ready_to_proceed': True
    }
    
    ack_file = Path('.claude/agent-inboxes') / handoff_packet['from_agent'] / f"{handoff_packet['handoff_id']}.ack"
    with open(ack_file, 'w') as f:
        json.dump(ack, f)
```

### Conflict Detection

When a handoff arrives, check for conflicts with previously received state:

```python
def detect_handoff_conflict(new_handoff, previous_state):
    """
    Detect if the new handoff conflicts with previous state.
    Returns conflict details or None if no conflict.
    """
    if not previous_state:
        return None
    
    # Check if from_agent is the same (linear handoff)
    if new_handoff['from_agent'] != previous_state.get('last_handoff_from'):
        return {
            'type': 'source_mismatch',
            'last_agent': previous_state.get('last_handoff_from'),
            'new_agent': new_handoff['from_agent']
        }
    
    # Check for version mismatch (has data been modified since I received it?)
    if new_handoff.get('version', 1) < previous_state.get('last_handoff_version', 1):
        return {
            'type': 'version_downgrade',
            'previous_version': previous_state.get('last_handoff_version'),
            'new_version': new_handoff.get('version', 1)
        }
    
    return None
```

If a conflict is detected, escalate to supervisor before proceeding.

## Example

```python
# Researcher agent (sender)
def researcher_finalize():
    handoff = {
        'handoff_id': 'hof_r2a_001',
        'from_agent': 'researcher',
        'to_agent': 'analyst',
        'timestamp': '2026-06-15T14:15:30Z',
        'phase_name': 'research',
        'phase_status': 'completed',
        'payload': {
            'sources': [...],  # 15 sources
            'research_summary': '...'
        },
        'output_schema': {
            'type': 'object',
            'properties': {'sources': {'type': 'array'}, 'research_summary': {'type': 'string'}}
        },
        'constraints_for_next_agent': [
            'Do not ignore high-credibility sources',
            'Budget 30 min for analysis'
        ]
    }
    
    validate_handoff(handoff, handoff['output_schema'])
    wait_handle = send_handoff(handoff)
    ack = wait_for_acknowledgment(wait_handle)
    print(f"Handoff {handoff['handoff_id']} acknowledged at {ack['timestamp']}")

# Analyst agent (receiver)
def analyst_receive():
    handoff = receive_handoff('researcher')
    if handoff:
        print(f"Received handoff {handoff['handoff_id']} from {handoff['from_agent']}")
        print(f"Sources: {len(handoff['payload']['sources'])}")
        acknowledge_handoff(handoff)
        
        # Now proceed with analysis
        analyze(handoff['payload'])
```

---
