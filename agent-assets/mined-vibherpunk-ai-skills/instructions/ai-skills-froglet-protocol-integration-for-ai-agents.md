# Copilot Instructions: Froglet Protocol Integration For Ai Agents
Description: This skill enables AI agents to integrate with the Froglet protocol, facilitating discovery, transaction, and receipt verification across organizational boundaries. It focuses on enabling agents to manage budgets, negotiate terms, and execute tasks while maintaining a verifiable chain of receipts.

# Froglet Protocol Integration for AI Agents

## Overview

The Froglet protocol is designed to enhance AI agent capabilities by enabling them to discover, transact with, and receive verifiable receipts from external data and service providers. This skill focuses on integrating Froglet into your AI agent workflows, allowing for seamless collaboration and transaction verification across organizational boundaries.

For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Install Froglet Locally**: Use Docker to install Froglet on your local machine.
   ```bash
   HBS Froglet Dev Agent
   ```
   This command downloads and installs the Froglet agent on Docker.

2. **Create a Temporary Token**: Generate a temporary token for accessing Froglet services.
   ```bash
   froglet create-token
   ```
   This creates a temporary token valid for 15 minutes.

3. **Define Payload**: Create a payload specifying the service, provider, and input data.
   ```json
   {
     "schema": "add_two_numbers",
     "provider": "example_provider",
     "input": {
       "num1": 7,
       "num2": 5
     }
   }
   ```

4. **Execute Service**: Send the payload to the Froglet node for execution.
   ```bash
   froglet execute --payload payload.json
   ```
   This command sends the payload to the Froglet node and returns a deal ID.

5. **Verify Receipt**: Use the deal ID to verify the receipt of the transaction.
   ```bash
   froglet verify-receipt --deal-id <deal_id>
   ```
   This command verifies the receipt and ensures the transaction is valid.

For detailed code examples and practical guidance, see [Practical Guide](references/practical_guide.md).

## Best Practices

- **Ensure Compatibility**: Verify that your AI agent framework is compatible with Froglet plugins.
- **Monitor Budgets**: Regularly monitor and manage the budgets allocated to your agents.
- **Validate Receipts**: Always validate receipts to ensure transaction integrity.

## Common Pitfalls

- **Token Expiry**: Ensure tokens are renewed before expiry to avoid service interruptions.
- **Payload Errors**: Double-check payload definitions to prevent execution errors.

## Validation and Testing

- **Test Locally**: Run Froglet locally using Docker to test integration before deploying.
- **Verify Transactions**: Use the `verify-receipt` command to ensure all transactions are correctly recorded.

For more information on common pitfalls and validation steps, refer to [Common Pitfalls](references/common_pitfalls.md).


## Reference Guides

### Common Pitfalls

# Common Pitfalls in Froglet Protocol Integration

Integrating the Froglet protocol into AI agent workflows can present several challenges. This document outlines common pitfalls and provides guidance on how to avoid them.

## Token Expiry

One common issue is the expiry of temporary tokens. Ensure tokens are renewed before expiry to avoid service interruptions. Regularly monitor token validity and automate the renewal process if possible.

## Payload Errors

Errors in payload definitions can lead to execution failures. Double-check payload definitions to ensure all required fields are correctly specified. Use schema validation tools to catch errors early.

## Compatibility Issues

Ensure that your AI agent framework is compatible with Froglet plugins. Test integration locally before deploying to production to identify and resolve any compatibility issues.

## Budget Management

Managing budgets effectively is crucial for autonomous agents. Regularly monitor and adjust budgets to ensure agents have the necessary resources to complete their tasks. Implement alerts for low budget levels to prevent service interruptions.

For practical examples and implementation details, refer to [Practical Guide](references/practical_guide.md).


### Core Concepts

# Core Concepts of Froglet Protocol

The Froglet protocol is designed to enhance AI agent capabilities by enabling them to discover, transact with, and receive verifiable receipts from external data and service providers. This document delves into the core concepts that underpin the Froglet protocol.

## Verifiable Chain of Receipts

One of the foundational concepts of Froglet is the verifiable chain of receipts. This ensures that every step in a transaction is recorded and can be verified, providing a transparent and trustworthy record of actions. This is crucial for collaborative environments where multiple agents and organizations interact.

## Budget Management

Froglet allows AI agents to manage their own budgets, enabling them to discover services, request data, negotiate execution terms, and pay for work across organizational boundaries. This transforms agents from mere executors of tasks to autonomous entities capable of making financial decisions.

## Integration with Existing Systems

Froglet is designed to integrate seamlessly with existing systems and protocols. It does not require a complete overhaul of existing infrastructure but rather adds a layer of functionality that enhances interoperability and collaboration.

For practical examples and implementation details, refer to [Practical Guide](references/practical_guide.md).


### Practical Guide

# Practical Guide to Froglet Protocol Integration

This guide provides step-by-step instructions for integrating the Froglet protocol into your AI agent workflows. It includes detailed examples and best practices to ensure a smooth implementation.

## Installation

To install Froglet locally using Docker, run the following command:
```bash
HBS Froglet Dev Agent
```
This command downloads and installs the Froglet agent on Docker.

## Token Creation

Generate a temporary token for accessing Froglet services:
```bash
froglet create-token
```
This creates a temporary token valid for 15 minutes.

## Payload Definition

Define a payload specifying the service, provider, and input data:
```json
{
  "schema": "add_two_numbers",
  "provider": "example_provider",
  "input": {
    "num1": 7,
    "num2": 5
  }
}
```

## Service Execution

Send the payload to the Froglet node for execution:
```bash
froglet execute --payload payload.json
```
This command sends the payload to the Froglet node and returns a deal ID.

## Receipt Verification

Use the deal ID to verify the receipt of the transaction:
```bash
froglet verify-receipt --deal-id <deal_id>
```
This command verifies the receipt and ensures the transaction is valid.

For more information on core concepts and common pitfalls, refer to [Core Concepts](references/core_concepts.md) and [Common Pitfalls](references/common_pitfalls.md).


### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Agents Need Receipts, Not More Tool Calls - Armanas Povilionis, Alithea Bio](https://www.youtube.com/watch?v=Fu45geO3zX8)** by AI Engineer