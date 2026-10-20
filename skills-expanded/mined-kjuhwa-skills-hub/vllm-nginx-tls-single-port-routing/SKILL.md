---
tags: [vllm, nginx, tls, single, port, routing]
name: vllm-nginx-tls-single-port-routing
description: Serve multiple vLLM OpenAI-API backends behind one Nginx TLS proxy on 443 using path-based routing
category: ai
version: 1.0.0
source_project: lucida-for-docker
trigger: Running multiple vLLM models (generation + embedding) on a single GPU host where only port 443 can be exposed and TLS termination must happen at the edge
---

See `content.md`.
