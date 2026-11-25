---
tags: [backend, stack, tag, filter, mongo, criteria]
name: stack-parse-tag-filter-to-mongo-criteria
description: Parse a tokenized boolean filter expression (key=value, AND, OR, parens) into a MongoDB Criteria tree using a shunting-yard/stack algorithm, with elemMatch for array-of-tag subdocs.
trigger: UI emits filter expressions as token arrays and the backend needs to translate them into MongoDB Criteria for dynamic "smart group" / saved-search queries
source_project: lucida-cm
version: 1.0.0
category: backend
---

See `content.md`.
