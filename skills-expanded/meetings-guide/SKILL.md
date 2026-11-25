---
name: meetings-guide
description: Reference for the meetings-mcp tools — how a meeting runs turn by turn, who may call which tool, moderator and participant practice, and an example flow. Load before starting or joining a multi-agent meeting.
---

# Multi-agent meetings — the guide

The `meetings` card in your instructions carries the rules (when a meeting
is right, who you can meet, the start_meeting rule, the do-nots). This
guide is the reference behind them.

## How meetings work

1. Call `start_meeting(topic, agents)` — you become the **moderator**
2. Use `direct_to(agents=[...])` to address specific agents — they respond next (in parallel if multiple)
3. If you don't call `direct_to`, your response broadcasts to all participants
4. All responses are visible to everyone in the transcript, regardless of routing
5. As moderator, call `end_meeting` to conclude — your response becomes the summary
6. Any agent can call `propose_conclude` to suggest ending — you (moderator) decide

Turns are strictly sequential. The platform routes your message only when your
turn ENDS: the agents you addressed start speaking after your response is
complete, and what they say reaches you as transcript in your next turn. So a
turn is always the same shape — gather what you need with tools, write your
message as response text, call the routing tool once, stop. Nothing you do
after the routing call can hear a reply; the platform denies later tool calls
in that turn (memory writes are the one exception, so you can still save
what the meeting taught you on the way out).

## Tool guide

| Tool | Who | What it does |
|------|-----|-------------|
| `start_meeting` | You (becomes moderator) | Start a meeting with specified agents |
| `direct_to(agents)` | Any participant | Address specific agents — they speak next |
| `end_meeting` | Moderator only | End the meeting. Your response = final summary |
| `propose_conclude` | Any non-moderator | Pause meeting, moderator decides to end or continue |
| `leave_meeting` | Any participant | Leave if topic is outside your expertise |

## Best practices

- **Starting a meeting — CRITICAL**: When you call `start_meeting`, the meeting session starts AFTER your current response completes. You will then receive a separate, dedicated prompt as the moderator to open the discussion inside the meeting. Therefore: your response that calls `start_meeting` must ONLY contain a brief acknowledgment + the tool call. Do NOT call `direct_to`, do NOT discuss the topic, do NOT address other agents, do NOT share opinions. Any text or tool calls after `start_meeting` in the same response happen OUTSIDE the meeting and are wasted — the other agents will never see them. Correct: "Sure, let me set up that meeting." → `start_meeting(...)`.
- **As moderator**: Open with a clear agenda. Use `direct_to` to address specific agents for their input, then stop — their answers arrive in your next turn. When done, write the summary, call `end_meeting`, stop.
- **As participant**: Be concise (1-3 paragraphs). Address other agents by name. Disagree constructively. Call `propose_conclude` when you have nothing more to add.
- **Do NOT** use the Agent tool, background subagents, or `delegate` during meetings.
- **Do NOT** respond with just acknowledgments — if you have nothing to add, call `propose_conclude`.

## Example flow

```
Turn 1 — Moderator: "Let's check store and systems health."
  → direct_to(["home-assistant", "system-admin"])   → turn ends

Turn 2 — Home Assistant + System Admin respond IN PARALLEL with their reports
  → both direct_to(["personal-assistant"])  (report back)   → turns end

Turn 3 — Moderator (both reports now in the transcript): "Here's the summary. [action items]"
  → end_meeting   → turn ends, meeting concluded
```
