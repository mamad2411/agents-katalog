---
tags: [backend, elasticsearch, xpack, ssl, transport]
name: elasticsearch-xpack-ssl-transport
description: Gate `PreBuiltXPackTransportClient` vs `PreBuiltTransportClient` on auth flag (not SSL flag) and configure keystore/truststore as independent ES X-Pack settings
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - connect Java client to X-Pack-secured Elasticsearch cluster
  - production ES requires auth and optional transport TLS
linked_knowledge:
  - es-xpack-transport-vs-rest-ssl
---

# Elasticsearch X-Pack SSL Transport Client

See `content.md`.
