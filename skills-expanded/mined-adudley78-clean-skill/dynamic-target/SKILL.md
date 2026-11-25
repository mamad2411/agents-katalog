---
name: dynamic-target
version: 0.0.1
description: Integration-test fixture; writes a file and exits.
entrypoint: main.py
tools: []
allowed_hosts: []
---

Fixture for the dynamic-analysis integration test. The real entrypoint is
`main.py`, picked up automatically by `docker/runner.sh`.
