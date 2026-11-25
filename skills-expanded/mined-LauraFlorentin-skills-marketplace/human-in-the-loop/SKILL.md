---
name: human-in-the-loop
description: A hybrid pattern where the system pauses execution to request human approval, input, or disambiguation before proceeding with critical actions. Use when user asks to "add human approval", "require human review", "human-in-the-loop", or mentions approval workflows, human oversight, or escalation.
---

# Human-in-the-Loop

Human-in-the-Loop (HITL) bridges the gap between full automation and manual control. It treats the human user as a "privileged tool" or "approver". This is crucial for high-stakes domains where AI errors are unacceptable, or for ambiguous tasks where human intuition is required to guide the agent.

## Use Cases

-   **Approval Workflow**: Agent drafts a reply -> Human approves/edits -> Agent sends.
-   **Escalation**: Chatbot handles simple queries -> Escalates to human support for complex issues.
-   **Clarification**: Agent: "I found 3 files. Which one do you mean?" -> Human selects.

## Implementation Pattern

```python
def hitl_workflow(user_request):
    # Step 1: Plan/Draft
    plan = agent.create_plan(user_request)
    
    # Step 2: Risk Assessment
    if is_high_risk(plan):
        # Step 3: Pause for Approval
        # Send notification to user UI
        approval = notify_user(
            message="Agent wants to execute the following plan:",
            payload=plan
        )
        
        if approval.status == "REJECTED":
            return "Action cancelled by user."
        elif approval.status == "EDITED":
            plan = approval.new_plan
            
    # Step 4: Execute
    return agent.execute(plan)
```


## Examples

**Input**: "Require human approval before the agent sends any email."

```python
def send_email_with_approval(draft):
    # Present draft to human
    approval = review_queue.submit({
        "type": "email_approval",
        "content": draft,
        "timeout_hours": 4
    })
    if approval.status == "approved":
        email_client.send(draft)
    elif approval.status == "rejected":
        agent.revise(draft, feedback=approval.comment)
    else:  # timeout
        escalate_to_manager(draft)
```

**Output**: Email sent only after explicit human approval, with full audit trail.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Humans are a bottleneck | Too many approval requests | Raise the automation threshold; only require approval above risk score 0.8 |
| Agent waits indefinitely | No timeout configured | Set approval timeout; define auto-escalation path on timeout |
| Reviewer lacks context | UI shows only the action | Include full context: why the agent wants to take this action |
| Feedback loop never closes | No mechanism to learn from rejections | Log rejection reasons; update agent guidelines after 10+ similar rejections |
