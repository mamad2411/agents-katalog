---
name: smoke
description: Run the full stack smoke test (31 checks — pods, HTTP, Kafka, Debezium, admin)
disable-model-invocation: true
allowed-tools: Bash
---

Run the comprehensive smoke test suite.

## Notes
- All gateway endpoint checks use `curl -sk` (self-signed TLS cert on port 30000)
- Port 30080 serves HTTP→HTTPS redirect (301 → https://:30000)
- Tool NodePorts (31111, 32000, 32100, etc.) remain plain HTTP
- Cert Dashboard at `http://localhost:32600` (HTTP, NodePort)
- TLS certificates managed by cert-manager with 30-day auto-rotation

## Steps

1. Run:
```bash
cd /Volumes/Other/rand/llm/microservice && bash scripts/smoke-test.sh 2>&1
```

2. If any tests fail, investigate by:
   - Checking pod status: `kubectl get pods -n <namespace>`
   - Checking pod logs: `kubectl logs -n <namespace> deploy/<name> --tail=50`
   - Suggest fixes based on the failure pattern

3. Report results summary (X passed, Y failed).
