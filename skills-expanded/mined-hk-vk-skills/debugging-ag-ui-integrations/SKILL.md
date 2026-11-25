---
name: debugging-ag-ui-integrations
description: The `encryptedContent` field enables privacy-preserving workflows where
sensitive content (such as reasoning chains) can be passed across turns
without exposing the raw content. This is particularly useful for zero data
retention (ZDR) compliance and `store:false` scenarios.
metadata:
  source: llms.txt
  source_url: https://docs.ag-ui.com/llms-full.txt
  generated: 2026-06-09T14:52:49.106Z
---

# Debugging AG-UI Integrations

> The `encryptedContent` field enables privacy-preserving workflows where
sensitive content (such as reasoning chains) can be passed across turns
without exposing the raw content. This is particularly useful for zero data
retention (ZDR) compliance and `store:false` scenarios.

The `encryptedContent` field enables privacy-preserving workflows where
sensitive content (such as reasoning chains) can be passed across turns
without exposing the raw content. This is particularly useful for zero data
retention (ZDR) compliance and `store:false` scenarios.

## Available Resources

### Agentic Protocols

### AG-UI Handshakes with MCP and A2A

### Generative UI Specs

### What is an Agent?

### Agent Architecture

### Agent Types

### Implementing Agents

### Agent Capabilities

### Using Agents

### Agent Configuration

### Agent State Management

### Conclusion

### Design Principles

### Architectural Overview

### Core components

### Running Agents

### State Management

### Tools and Handoff

### Events

### How It Works

### The AgentCapabilities Interface

### Capability Categories

### Implementing getCapabilities()

### Client Usage Patterns

### Event Types Overview

### Base Event Properties

### Lifecycle Events

### Text Message Events

### Tool Call Events

### State Management Events

### Activity Events

### Special Events

### Reasoning Events

### Deprecated Events

### Draft Events

### Event Flow Patterns

### Implementation Considerations

### **AG-UI and Generative UI Specs**

### Lifecycle

### Run outcomes

### The Interrupt type

### Resuming a run

### Contract rules

### State at the interrupt boundary

### Error handling

### Reason taxonomy

### Tool-bound interrupts

### Examples

### Related

- **Events**
  - URL: /concepts/events

- **Capabilities**
  - URL: /concepts/capabilities

### Message Structure

### Message Types

### Vendor Neutrality

### Message Synchronization

### Tool Integration in Messages

### Streaming Tool Calls

### Practical Example

### Conclusion

### What is Middleware?

### How Middleware Works

### Function-Based Middleware

### Class-Based Middleware

### Built-in Middleware

### Middleware Patterns

### Combining Middleware

### Execution Order

### Best Practices

### Advanced Use Cases

### Conclusion

### Overview

### ReasoningMessage

### Reasoning Events

### Privacy and Compliance

### Example Implementations

### Client Integration

### Migration from Thinking Events

### Best Practices

### Related Documentation

- **Events**
  - URL: /concepts/events#reasoning-events

- **Messages**
  - URL: /concepts/messages#reasoning-messages

- **Serialization**
  - URL: /concepts/serialization

### Core Concepts

### Updated Event Fields

### Event Compaction

### Branching and Time Travel

### Examples

### Implementation Notes

### See Also

- **Events**
  - URL: /concepts/events

### Shared State Architecture

### State Synchronization Methods

### JSON Patch Format

### State Processing in AG-UI

### Human-in-the-Loop Collaboration

### CopilotKit Implementation

### Best Practices

### Conclusion

### What Are Tools?

### Tool Structure

### Frontend-Defined Tools

### Tool Call Lifecycle

### Tool Results

### Human-in-the-Loop Workflows

### CopilotKit Integration

### Tool Examples

### Best Practices

### Conclusion

### Get Involved

### Summary

### Status

- **mail@mme.xyz**
  - URL: mailto:mail@mme.xyz

### Challenges and Limitations

### Detailed Specification

### Implementation Examples

### Implementation Considerations

### Use Cases

### Testing Strategy

### References

- **AG-UI Tools Documentation**
  - URL: /concepts/tools

- **JSON Schema**
  - URL: https://json-schema.org/

- **React Hook Form**
  - URL: https://react-hook-form.com/

- **JSON Forms**
  - URL: https://jsonforms.io/

### Summary

### Status

- **mail@mme.xyz**
  - URL: mailto:mail@mme.xyz

### Detailed Specification

### New Type: MetaEvent

### Implementation Examples

### Common Meta Event Types

### Use Cases

### Implementation Considerations

### Testing Strategy

### References

- **AG-UI Events Documentation**
  - URL: /concepts/events

- **Event Sourcing**
  - URL: https://martinfowler.com/eaaDev/EventSourcing.html

- **CQRS Pattern**
  - URL: https://martinfowler.com/bliki/CQRS.html

### Current Drafts

### Status Definitions

### Agentic Protocols

### Building blocks (today & upcoming)

### Why Agentic Apps need AG-UI

### AG-UI in Action

### Supported Integrations

### Quick Start

### Explore AG-UI

### Resources

### Contributing

### Support and Feedback

- **create a GitHub issue**
  - URL: https://github.com/ag-ui-protocol/ag-ui/issues

- **Discord community**
  - URL: https://discord.gg/Jd3FzfdJa8

### When to use a client implementation

### What you'll build

### Prerequisites

- **Node.js**
  - URL: https://nodejs.org/

- **pnpm**
  - URL: https://pnpm.io/

### Step 1 – Initialize your project

### Step 2 – Install AG-UI and dependencies

### Step 3 – Create your agent

### Step 4 – Create the CLI interface

### Step 5 – Test your assistant

### Step 6 – Understanding the AG-UI event flow

### Step 7 – Add tool functionality

### Step 8 – Add more functionality

### Step 9 – Deploy your client

### Extending your client

### Share your client

- **AG-UI GitHub Discussions**
  - URL: https://github.com/orgs/ag-ui-protocol/discussions

### Conclusion

- **here**
  - URL: /concepts/events

### When to use a middleware implementation

### What you'll build

### Prerequisites

- **Node.js**
  - URL: https://nodejs.org/

### Step 1 – Scaffold your integration

### Step 2 – Add package to dojo dependencies

### Step 3 – Start the dojo

### Step 4 – Bridge OpenAI with AG-UI

### Step 4 – Chat with your agent

### Bridging AG-UI to any protocol

### Connect your agent to a frontend

### Share your integration

- **AG-UI repository**
  - URL: https://github.com/ag-ui-protocol/ag-ui

- **Contributing**
  - URL: ../development/contributing

### Conclusion

### When to use a server implementation

### What you'll build

### Prerequisites

- **Python**
  - URL: https://www.python.org/downloads/

- **Poetry**
  - URL: https://python-poetry.org/docs/#installation

### Step 1 – Scaffold your server

### Step 2 – Add package to dojo dependencies

### Step 3 – Start the dojo and server

### Implementing Basic Chat

### Step 4 – Bridge OpenAI with AG-UI

### Step 5 – Chat with your server

### Share your integration

- **AG-UI repository**
  - URL: https://github.com/ag-ui-protocol/ag-ui

- **Contributing**
  - URL: ../development/contributing

### Conclusion

### Configuration

### Core Methods

### Observable Properties

### Properties

### Protected Methods

### API

### What it does

### Example

### When to use

### Notes & limitations

- **Serialization**
  - URL: /concepts/serialization

### Configuration

### Creating an HttpAgent

### Methods

### Protected Methods

### Properties

### Types

### Function-Based Middleware

### Class-Based Middleware

### Accumulator Helpers (Class Middleware)

### Built-in Middleware

### Middleware Patterns

### Chaining Middleware

### Advanced Usage

### Lifecycle Notes

### Best Practices

### TypeScript Support

### AbstractAgent

- **Configuration**
  - URL: /sdk/js/client/abstract-agent#configuration

- **Core Methods**
  - URL: /sdk/js/client/abstract-agent#core-methods

- **Protected Methods**
  - URL: /sdk/js/client/abstract-agent#protected-methods

- **Properties**
  - URL: /sdk/js/client/abstract-agent#properties

### HttpAgent

- **Configuration**
  - URL: /sdk/js/client/http-agent#configuration

- **Methods**
  - URL: /sdk/js/client/http-agent#methods

- **Protected Methods**
  - URL: /sdk/js/client/http-agent#protected-methods

- **Properties**
  - URL: /sdk/js/client/http-agent#properties

### Middleware

- **Function Middleware**
  - URL: /sdk/js/client/middleware#function-based-middleware

- **Class Middleware**
  - URL: /sdk/js/client/middleware#class-based-middleware

- **Built-in Middleware**
  - URL: /sdk/js/client/middleware#built-in-middleware

- **Middleware Patterns**
  - URL: /sdk/js/client/middleware#middleware-patterns

### AgentSubscriber

- **Event Handlers**
  - URL: /sdk/js/client/subscriber#event-handlers

- **State Management**
  - URL: /sdk/js/client/subscriber#state-management

- **Usage Examples**
  - URL: /sdk/js/client/subscriber#usage-examples

- **Integration**
  - URL: /sdk/js/client/subscriber#integration-with-agents

### Overview

### Adding Subscribers to Agents

### Core Interfaces

### Event Handlers

### Async Support

### Multiple Subscribers

### Integration with Agents

### EventType Enum

### BaseEvent

### Lifecycle Events

### Text Message Events

### Tool Call Events

### State Management Events

### Reasoning Events

### Special Events

### Deprecated Events

### Event Schemas

### Source Types

### Common Use Cases

### Types

- **RunAgentInput**
  - URL: /sdk/js/core/types#runagentinput

- **Message**
  - URL: /sdk/js/core/types#message-types

- **Context**
  - URL: /sdk/js/core/types#context

- **Tool**
  - URL: /sdk/js/core/types#tool

- **State**
  - URL: /sdk/js/core/types#state

### Events

- **Lifecycle Events**
  - URL: /sdk/js/core/events#lifecycle-events

- **Text Message Events**
  - URL: /sdk/js/core/events#text-message-events

- **Tool Call Events**
  - URL: /sdk/js/core/events#tool-call-events

- **State Management Events**
  - URL: /sdk/js/core/events#state-management-events

- **Special Events**
  - URL: /sdk/js/core/events#special-events

### RunAgentInput

### Message Types

### Context

### Tool

### State

### AgentCapabilities

### EventType Enum

### BaseEvent

### Lifecycle Events

### Text Message Events

### Tool Call Events

### State Management Events

### Special Events

### Reasoning Events

### Deprecated Events

### Event Discrimination

### Source Types

### Common Use Cases

### Types

- **RunAgentInput**
  - URL: /sdk/python/core/types#runagentinput

- **Message**
  - URL: /sdk/python/core/types#message-types

- **Context**
  - URL: /sdk/python/core/types#context

- **Tool**
  - URL: /sdk/python/core/types#tool

- **State**
  - URL: /sdk/python/core/types#state

### Events

- **Lifecycle Events**
  - URL: /sdk/python/core/events#lifecycle-events

- **Text Message Events**
  - URL: /sdk/python/core/events#text-message-events

- **Tool Call Events**
  - URL: /sdk/python/core/events#tool-call-events

- **State Management Events**
  - URL: /sdk/python/core/events#state-management-events

- **Special Events**
  - URL: /sdk/python/core/events#special-events

### RunAgentInput

### Message Types

### Context

### Tool

### State

### EventEncoder

### Adding the documentation to Cursor

- **https://docs.ag-ui.com/llms-full.txt**
  - URL: https://docs.ag-ui.com/llms-full.txt

### Using the documentation

### Best practices

### The AG-UI Dojo

### Getting Started with the Dojo

- **github.com/ag-ui-protocol/ag-ui**
  - URL: https://github.com/ag-ui-protocol/ag-ui

## How to Use This Skill

Reference these resources when working with Debugging AG-UI Integrations.