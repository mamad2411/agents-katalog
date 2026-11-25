---
name: api-mitmproxy
description: Interactive HTTPS proxy for API security testing with traffic interception, modification, and replay capabilities.
metadata:
  version: 0.2.0
  category: appsec
---
# mitmproxy API Security Testing

## Quick Start
```bash
# Start the interactive console proxy
mitmproxy

# Start the web-based interface (default http://127.0.0.1:8081)
mitmweb
```

## Workflow
1. **Setup**: Start `mitmproxy` or `mitmweb` and configure the target client to use the proxy (default: localhost:8080).
2. **CA Trust**: Visit `http://mitm.it` on the client and install the mitmproxy CA certificate to intercept HTTPS traffic.
3. **Traffic Analysis**: Exercise the target application and observe API requests and responses in the proxy interface.
4. **Interception**: Use intercept filters (e.g., `~u <regex>`) to pause requests and modify parameters or headers on-the-fly.
5. **Replay & Test**: Replay captured requests with modified payloads to test for vulnerabilities like IDOR, SQL injection, or authorization bypass.
6. **Automation**: Use `mitmdump` and Python scripts to automate complex testing scenarios or export traffic.

## Rules & Constraints
- **RULE-1**: Always secure the proxy interface with authentication (e.g., `--web-user`, `--web-password`) when running in accessible environments.
- **RULE-2**: Encrypt and secure stored flow files, as they contain sensitive credentials, tokens, and PII.
- **RULE-3**: Do not use the proxy for production traffic interception without explicit authorization and proper data handling controls.

## When to Use
- Intercepting and analyzing API traffic for security testing.
- Debugging mobile app or thick client communications with backend APIs.
- Automating API security tests with Python scripts and replaying traffic.

## When NOT to Use
- Real-time intrusion detection or prevention in production environments.
- High-volume traffic logging (use dedicated logging infrastructure).

## References
- [Skill Manual](references/api-mitmproxy-manual.md)
- [mitmproxy Official Site](https://mitmproxy.org/)
