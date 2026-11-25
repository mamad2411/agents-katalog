---
name: cxone-agent-management
description: Manage and interact with NICE CXone Agent SDK and APIs for agent status, login, and logout.
---

# NICE CXone Agent Management Skill

This skill provides guidelines for working with the NICE CXone Agent APIs and SDKs to handle agent sessions, statuses, and capabilities.

## Key Concepts

- **Agent Sessions**: Agents must log in to establish a session, which allows them to interact with the ACD (Automatic Call Distributor).
- **Agent Status**: Agents have states (e.g., Available, Unavailable, Routing, Logged Out) which dictate whether they can receive interactions.
- **CXone Agent SDK**: A powerful toolkit available via NPM or GitHub (`NICE-DEVone`) to simplify agent-side integrations in client applications.

## Authentication
Client-side apps often use OpenID Connect. Agents must authenticate properly, generating the required ID and tokens for the session.

## Agent API Capabilities
- **Login/Logout**: Establish or terminate an agent's session securely.
- **State Management**: Update agent availability states (e.g., changing from 'Available' to an 'Unavailable' code like 'Break' or 'Lunch').
- **Agent Configuration**: Retrieve assigned skills and profile details.

## Best Practices
- Always clean up agent sessions gracefully to avoid stuck interactions.
- Use WebSockets where appropriate to subscribe to real-time agent state changes, reducing polling overhead.
- Handle authentication token expiration and refresh securely within your application logic.
