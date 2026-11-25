---
name: inter-agent-communication
description: Protocols and patterns that allow independent agents to exchange messages, negotiate, and collaborate across network boundaries or process isolation. Use when user asks to "make agents communicate", "agent messaging", "inter-agent protocol", or mentions agent coordination, message passing, or shared state.
---

# Inter-Agent Communication

Inter-Agent Communication defines the language and transport layer for agents to talk to each other. In a distributed system, Agent A (Booking) might run on a different server than Agent B (Payment). They need a standard way to find each other (Discovery), send requests (Messaging), and understand the data format (Protocol).

## Use Cases

-   **Agent Marketplace**: An agent searches a registry to find a "Translation Agent" and hires it for a task.
-   **Supply Chain**: A "Retail Agent" sends a restock order to a "Warehouse Agent", which confirms availability.
-   **Delegation**: A "Personal Assistant Agent" delegates a math problem to a specialized "Wolfram Alpha Agent".

## Implementation Pattern

```python
# Conceptual A2A (Agent-to-Agent) Interaction

class AgentA:
    def run(self):
        # Step 1: Discovery
        # Find an agent that supports the 'payment' skill
        payment_agent_url = directory.lookup(skill="process_payment")
        
        # Step 2: Messaging (HTTP/RPC)
        # Send a structured request
        payload = {
            "task": "pay_invoice",
            "amount": 100,
            "currency": "USD"
        }
        
        response = http.post(f"{payment_agent_url}/inbox", json=payload)
        
        # Step 3: Handle Response
        if response.status == "CONFIRMED":
            print("Payment successful")
```


## Examples

**Input**: An orchestrator agent distributing research tasks to specialist agents.

```python
# Orchestrator sends task
orchestrator.send(Message(
    to="researcher-agent-1",
    task="Find all SEC filings for AAPL in 2024",
    context={"output_format": "json", "deadline": "2025-03-01"}
))

# Researcher replies
researcher.send(Message(
    to="orchestrator",
    status="complete",
    result=filings_data,
    metadata={"sources": 14, "latency_ms": 3200}
))
```


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Messages lost | No delivery acknowledgement | Require ACK from receiver; use at-least-once delivery with idempotency keys |
| Agents talk past each other | No shared schema | Define a typed message schema (Pydantic/JSON Schema) for all message types |
| Deadlock between agents | Circular dependency | Design a strict orchestrator hierarchy; no peer-to-peer blocking calls |
| Message queue backs up | Slow consumer agent | Add horizontal scaling or a priority queue for time-sensitive messages |
