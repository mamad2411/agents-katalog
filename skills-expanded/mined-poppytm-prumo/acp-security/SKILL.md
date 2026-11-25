---
name: acp-security
description: Verified agent routing, capability delegation limits, mutual authentication, state isolation, and deterministic termination signals
---
# Agent Client Protocol (ACP) Transport & Multi-Agent Security

## 1. Agent Communication Boundaries
Enforce cryptographic routing verification on all inter-agent messages. Deny untrusted or unverified subagents from spoofing sender identities. Maintain an explicit agent registry validating role permissions.

## 2. Capability Delegation Limits
Enforce strict delegation caps: subagents may only inherit a proper subset of their parent agent's capabilities. Mandate a maximum delegation depth (default 1, max 2) to prevent uncontrolled multi-agent recursion.

## 3. Mutual Authentication & Session Handshake
Authenticate agent-to-agent RPC channels using mutual session tokens or cryptographic signatures. Establish unique ephemeral session IDs per task delegation to ensure message provenance.

## 4. Message Integrity & Replay Protection
Include monotonic message sequence numbers, ISO 8601 UTC timestamps, and SHA-256 payload checksums on all agent messages. Reject messages with timestamps skewed beyond 60 seconds or duplicated sequence IDs.

## 5. State & Context Isolation
Isolate context memory between agents. Subagents must receive only a tailored, minimal context capsule (Working Context Capsule) necessary for their immediate task, preventing cross-tenant data leakage.

## 6. Untrusted Subagent Quarantine
When spawning agents to inspect external or untrusted codebases, place them in a quarantined sandbox with read-only filesystem access and zero outbound network or command execution capabilities.

## 7. Token Budget Envelopes
Assign explicit, non-expandable token budget envelopes to each subagent task. Track cumulative input, output, and cached token consumption. Terminate the subagent immediately if the allocated budget is exhausted.

## 8. Deterministic Termination Signals
Implement immediate, unignorable handling for CANCEL, STOP, and KILL signals across all running agent processes and background tasks. Prevent dangling background execution loops.

## 9. Behavioral Monitoring & Drift Detection
Monitor agent reasoning traces for cyclic loops, repetitive tool failures, or unexpected tool call patterns. Trigger an automatic circuit breaker after 3 consecutive failed verification attempts.

## 10. Secure Handoff Contracts
Execute agent-to-agent task handoffs via immutable state artifacts with defined schemas. Validate that all prerequisite acceptance criteria are certified before the receiving agent begins execution.
