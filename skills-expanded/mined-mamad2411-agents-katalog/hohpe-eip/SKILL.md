---
name: hohpe-eip
description: "Knowledge base from \"Enterprise Integration Patterns\" by Gregor Hohpe & Bobby Woolf. Use when applying the authors' messaging patterns for enterprise/application integration, asynchronous messaging, message routing/transformation, channels, endpoints, and messaging-system design, studying the book, or referencing its 65 patterns."
---

<!-- argument-hint: [pattern name, topic, or chapter number e.g. ch07] -->

# Enterprise Integration Patterns
**Authors**: Gregor Hohpe & Bobby Woolf | **Pages**: ~574 | **Chapters**: 14 (65 patterns) | **Generated**: 2026-07-04

## How to Use This Skill

- **Without arguments** — load the core pattern language below.
- **With a pattern/topic** — ask about `Aggregator`, `Content-Based Router`, `idempotency`, `pub-sub`; I find and read the relevant chapter.
- **With a chapter** — ask for `ch07`; I load that file.
- **Browse** — ask "what chapters do you have?" or open [patterns.md](patterns.md) for all 65 in one place.

When you ask about a pattern not fully covered below, I read its chapter file before answering.

---

## Core Pattern Language

EIP is a **pattern language for asynchronous messaging**. Everything refines six root patterns from Ch 3.

### The 6 root patterns (ch03) — the vocabulary
- **Message Channel** — a logical pipe two apps agree on without knowing each other. → family: ch04.
- **Message** — a self-contained header+body data unit (copied, not shared). → family: ch05.
- **Pipes and Filters** — chain single-responsibility filters via channels; the architectural backbone of every flow.
- **Message Router** — consumes then republishes a message *unchanged* to a chosen channel (changes destination, not content). → family: ch07.
- **Message Translator** — converts a message's *format* without touching routing. → family: ch08.
- **Message Endpoint** — client code bridging an app to the messaging API. → family: ch10.

> **Router changes destination; Translator changes format; Endpoint connects the app.** Never blur these.

### The 4 integration styles (ch02) — pick before you pattern
File Transfer · Shared Database · Remote Procedure Invocation · **Messaging**. Choose Messaging when you need frequent, reliable, async exchange while staying loosely coupled. Everything after Ch 3 assumes you chose Messaging.

### Foundational decisions (use these constantly)
- **Loose coupling** is the whole point: minimize the assumptions each app makes about another, accepting added complexity for tolerance to change.
- **Canonical Data Model** (ch08) — with N apps, translate each to one shared model (2N translators, not N²). Reach for it once several apps integrate; skip only if double-translation latency is unacceptable.
- **Intent → type → channel** (ch05): invoke behavior = Command; hand over data = Document; announce change = Event. Commands/Documents → Point-to-Point; Events → Publish-Subscribe.
- **Request-Reply = two one-way messages** (ch05): **Return Address** says where to reply, **Correlation Identifier** says which request it answers. Correlate by an application field, not the system message ID.
- **Stateless vs stateful routers** (ch07): stateless (Content-Based Router, Filter, Recipient List, Splitter) parallelize freely; stateful (Aggregator, Resequencer, Process Manager) need correlation + state cleanup.
- **Key compositions**: Composed Message Processor = Splitter + Aggregator · Scatter-Gather = (Recipient List or Pub-Sub) + Aggregator · Message Broker = routing patterns in hub-and-spoke + Canonical Data Model.
- **Endpoints combine patterns** (ch10): wrap every endpoint in a **Messaging Gateway**; assume duplicates and use an **Idempotent Receiver**; Polling throttles + is transaction-safe, Event-Driven is immediate but transaction-hostile.
- **Invalid vs Dead Letter** (ch04): receiver can't *process* it → Invalid Message Channel (receiver moves it); system can't *deliver* it → Dead Letter Channel (system moves it).
- **Manage on a separate Control Bus** (ch11); observe with Wire Tap / Message History / Message Store; test correctness (not just liveness) with Test Messages + Smart Proxy.

The 65 patterns with when/how/trade-off are in **[patterns.md](patterns.md)**. Decision rules are in **[cheatsheet.md](cheatsheet.md)**.

---

## Chapter Index

| # | Title | Key Patterns |
|---|-------|--------------|
| [ch01](chapters/ch01-solving-integration-problems.md) | Solving Integration Problems using Patterns | loose coupling, Canonical Data Model, middleware anatomy |
| [ch02](chapters/ch02-integration-styles.md) | Integration Styles | File Transfer, Shared Database, RPC, Messaging |
| [ch03](chapters/ch03-messaging-systems.md) | Messaging Systems (roots) | Message Channel, Message, Pipes and Filters, Router, Translator, Endpoint |
| [ch04](chapters/ch04-messaging-channels.md) | Messaging Channels | Point-to-Point, Publish-Subscribe, Dead Letter, Guaranteed Delivery, Channel Adapter, Message Bus |
| [ch05](chapters/ch05-message-construction.md) | Message Construction | Command/Document/Event, Request-Reply, Return Address, Correlation Identifier |
| [ch06](chapters/ch06-interlude-simple-messaging.md) | Interlude: Simple Messaging (code) | JMS/.NET Request-Reply, JMS Pub-Sub |
| [ch07](chapters/ch07-message-routing.md) | Message Routing | Content-Based Router, Filter, Splitter, Aggregator, Scatter-Gather, Routing Slip, Process Manager |
| [ch08](chapters/ch08-message-transformation.md) | Message Transformation | Envelope Wrapper, Content Enricher, Content Filter, Claim Check, Normalizer, Canonical Data Model |
| [ch09](chapters/ch09-interlude-composed-messaging.md) | Interlude: Composed Messaging (Loan Broker) | Scatter-Gather + Aggregator; sync vs async |
| [ch10](chapters/ch10-messaging-endpoints.md) | Messaging Endpoints | Gateway, Polling/Event-Driven Consumer, Competing Consumers, Idempotent Receiver, Service Activator |
| [ch11](chapters/ch11-system-management.md) | System Management | Control Bus, Wire Tap, Message History, Message Store, Smart Proxy, Test Message |
| [ch12](chapters/ch12-interlude-system-management-example.md) | Interlude: System Management Example | Loan Broker instrumented |
| [ch13](chapters/ch13-integration-patterns-in-practice.md) | Integration Patterns in Practice | Bond Trading case study |
| [ch14](chapters/ch14-concluding-remarks.md) | Concluding Remarks | emerging standards & futures (2003) |

## Topic Index

- **Aggregator / completeness condition** → ch07, ch09
- **Asynchronous messaging / async vs sync** → ch02, ch05, ch09
- **Canonical Data Model** → ch01, ch08
- **Channel Adapter / Messaging Bridge / Message Bus** → ch04
- **Command / Document / Event Message** → ch05
- **Competing Consumers / Message Dispatcher** → ch10
- **Content-Based Router / Message Filter** → ch07
- **Content Enricher / Content Filter / Claim Check** → ch08
- **Control Bus / Wire Tap / Smart Proxy** → ch11, ch12
- **Correlation Identifier / Return Address** → ch05, ch09, ch11
- **Dead Letter / Invalid Message Channel** → ch04
- **Guaranteed Delivery** → ch04
- **Idempotent Receiver / de-duplication** → ch10
- **Integration styles (File Transfer, Shared DB, RPC, Messaging)** → ch02
- **JMS / MSMQ / .NET code** → ch06, ch09
- **Loan Broker case study** → ch09, ch12
- **Loose coupling** → ch01, ch02
- **Message Broker / hub-and-spoke** → ch03, ch07
- **Message Router / Translator / Endpoint (roots)** → ch03
- **Message Sequence / Expiration / Format Indicator** → ch05
- **Pipes and Filters** → ch03
- **Point-to-Point / Publish-Subscribe Channel** → ch04
- **Polling vs Event-Driven Consumer** → ch10
- **Process Manager / Routing Slip** → ch07
- **Real-world architecture (Bond Trading)** → ch13
- **Recipient List / Scatter-Gather / Splitter / Resequencer** → ch07
- **Request-Reply** → ch05, ch06
- **Selective Consumer / Durable Subscriber** → ch04, ch10
- **Service Activator / Messaging Gateway / Mapper** → ch10
- **Transactional Client / XA** → ch10
- **Web Services / WS-* / BPEL / SOA** → ch14, ch09

## Supporting Files
- [patterns.md](patterns.md) — all 65 patterns + 4 styles, when/how/trade-off
- [glossary.md](glossary.md) — key terms with definitions
- [cheatsheet.md](cheatsheet.md) — decision rules and tells

---

## Scope & Limits
Covers the book (2003) only. Excludes (by the authors' choice) security, complex data mapping, workflow/rule engines, scalability/robustness, and distributed (XA) transaction internals. Standards in Ch 14 are 2003-era — REST/JSON, event-driven microservices, and Kafka-style logs later reshaped the landscape, but the patterns themselves remain the vocabulary. For implementation, pair with project-specific tooling.
