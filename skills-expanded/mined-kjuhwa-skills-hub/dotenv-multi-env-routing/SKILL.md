---
name: dotenv-multi-env-routing
description: Single ENV variable flips an entire stack (REST base URL, WebSocket base, per-operation transaction IDs) between production and sandbox tiers, loaded via dotenv with OS-env precedence.
category: backend
tags: [dotenv, config, environments, sandbox, production, routing]
triggers: ["KIS_ENV", "prod", "vts", "sandbox", "dotenv", "Dotenv.configure", "multi-environment", "openapi host"]
source_project: kis-java-bundle
version: 0.1.0-draft
---
