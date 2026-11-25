---
name: reverse-engineer-anything
description: Reverse engineer applications, Electron apps, JavaScript bundles, network protocols, and native binaries with REA inspection tools.
---

# REA: Reverse Engineer Anything for Muse AI Agent

Integrates the 200,000+ star [morluto/rea](https://github.com/morluto/rea) reverse-engineering skill and toolchain directly into Muse AI Agent.

## Overview
See a feature you like in any desktop application or mobile service? Ask Muse Agent to investigate it with REA. It can inspect applications, trace runtime crypto protocols, and explain internal behaviors down to the binary and network layer.

## Key Capabilities
- **Static App Inspection**: Inspect JavaScript bundles, Electron apps, unpacked assets, and config schemas.
- **Crypto & Protocol Tracing**: Validates AES-256-GCM, SHA-256 integrity hashes, and WebSocket RPC handshakes.
- **Binary Doctor**: Run system diagnostics via `rea-inspector/lib/doctor.js`.
- **CUA Cross-Pairing**: Pair reverse-engineered insights directly with Muse Computer-Use Agent to automate discovered workflows.

## Execution
```bash
# Run REA diagnostic suite
node -e "console.log(require('./rea-inspector/lib/doctor').runDoctor())"
```
