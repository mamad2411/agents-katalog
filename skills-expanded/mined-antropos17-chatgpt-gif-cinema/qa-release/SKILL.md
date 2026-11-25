---
name: qa-release
description: Run offline checks, prevent secrets from shipping, and distinguish mocked API tests from actual renders.
---
# QA Release
Run `python -m unittest discover -s tests -v` and `python -m compileall -q gif_cinema`. Review for leaked API keys, .env, private/ and outputs. Check README claims and live access. Only label API rendering passed after real authenticated output has been verified.

Require FFmpeg and ffprobe for render integration tests; report skipped tests. Run the
offline script with `--execute --max-api-calls 0`, then rerun to verify zero-call reuse.
Read the receipt and inspect the contact sheet and full movie. Technical decode checks
do not establish identity, aligned motion or coherent storytelling.
