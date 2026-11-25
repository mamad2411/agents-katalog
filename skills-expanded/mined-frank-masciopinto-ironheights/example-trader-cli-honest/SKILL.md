---
name: example-trader-cli-honest
description: Example honest trading helper. Fixture only.
---
# Example trader CLI (honest)
The helper `trader-tool` is built from the source in `src/` (see BUILD.md) and keeps its normal executable name; its checksum is listed in CHECKSUMS.
Keys are read from the user's own environment at run time and are never written by the skill (use FAKE_KEY in tests).
