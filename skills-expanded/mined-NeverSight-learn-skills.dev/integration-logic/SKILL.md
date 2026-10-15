---
name: integration-logic
description: Identify, interpret, review, or write integration logic in code. Use when an agent needs to decide whether code exists so two independent applications can communicate, or when it must implement, preserve, or refactor protocol handling, message exchange, contract mapping, or communication workflows between separate running systems.
---

# Integration Logic

## Goal

Define integration logic as the code required for two independent applications to communicate.

Use the broadest meaning of application: a browser-based application, web service, database, message broker, worker, daemon, or any program that runs as its own process on the same machine or on a remote one.

Integration logic often exists on both sides of the communication. Each participating application may contain code that prepares, sends, receives, validates, translates, or acknowledges data so the integration works end to end.

Treat integration logic as communication-driven code. The key question is whether the code exists because one independently running application must exchange data or signals with another.

## What Counts as Integration Logic

Classify code as integration logic when it does one or more of these things:

- establishes or manages communication with another application
- implements or abstracts a communication protocol
- builds, parses, serializes, deserializes, encodes, or decodes messages exchanged between applications
- maps internal data to an external contract or maps external data into internal structures
- sends requests, commands, events, queries, or messages to another application
- receives, validates, routes, acknowledges, or interprets requests, responses, events, or messages from another application
- manages transport details such as endpoints, topics, queues, channels, headers, correlation identifiers, acknowledgements, retries, or timeouts
- coordinates handshake or exchange steps required for two applications to communicate successfully

Integration logic often appears in code that answers questions such as:

- how one application reaches another
- how data must be shaped so another application can understand it
- how protocol details are handled or hidden behind an abstraction
- how requests, responses, events, or messages are exchanged reliably
- how an external contract is enforced at the communication boundary

## Detection Workflow

1. Read the code for communication purpose first.
   - Look for external system names, service names, broker names, database names, queue names, endpoint paths, topic names, channel names, protocol names, or contract names.
   - Pay attention to code that only exists because another independently running application participates in the flow.

2. Identify the participating applications.
   - Determine which application sends and which application receives, or whether the code supports both directions.
   - Treat communication with browsers, servers, workers, databases, brokers, and other standalone processes as integration between applications.

3. Trace the exchange.
   - Identify the data or signal being exchanged.
   - Identify how the code prepares, transmits, receives, validates, translates, or acknowledges that exchange.
   - Identify the protocol or contract rules the code must respect.

4. Prefer semantic classification to file or framework conventions.
   - Do not assume code is or is not integration logic only because of its folder, class name, library choice, or framework role.
   - Classify by whether the code exists to make inter-application communication work.

## Writing or Changing Integration Logic

1. Preserve the communication contract before refactoring.
   - Restate which applications communicate, what they exchange, and which protocol or contract rules apply.
   - Keep contract fields, protocol concepts, and transport semantics explicit in names and code structure.

2. Make the exchange legible.
   - Express request and response shapes, message formats, routing keys, acknowledgement behavior, retry rules, and timeout handling clearly.
   - Prefer code shapes that reveal the communication steps instead of hiding them behind incidental detail.

3. Keep contract translation explicit.
   - Make it clear where internal data is transformed into externally exchanged data and where external payloads are translated into internal structures.
   - Preserve field names, required fields, and protocol expectations with care.

4. Protect the integration boundary.
   - Verify that edited code still matches the protocol and contract expected by the other application.
   - Verify that serialization, parsing, routing, and acknowledgement behavior still produce a valid end-to-end exchange.

## Review Questions

When reading or reviewing code, ask:

- Which independent applications are being connected here?
- What request, response, event, message, or signal is being exchanged?
- Which protocol or communication contract does this code implement or abstract?
- Where does this code translate data between internal structures and exchanged payloads?
- Would changing this code alter whether two applications can communicate correctly?

If the answer is yes, treat the code as integration logic.

## Report the Outcome

When finishing the task:

- state which code was identified or treated as integration logic
- state which applications, protocols, or contracts were involved
- state which exchanged payloads, messages, requests, responses, or acknowledgements were implemented or preserved
