---
tags: [backend, avro, event, change, flags]
name: avro-event-with-change-flags
description: Design Kafka Avro event schemas that carry an actionType enum plus boolean "changed" flags per mutable section so consumers can branch cheaply without diffing payloads.
trigger: designing Kafka/Avro event payloads for entity CRUD where consumers only care about which sub-sections changed (e.g. parent vs tag filters vs child membership)
source_project: lucida-cm
version: 1.0.0
category: backend
---

See `content.md`.
