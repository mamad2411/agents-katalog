Agent Guidelines for This Repository

Scope: This file applies to the entire repository. It instructs agents (e.g., Codex CLI) how to work here to avoid breakages.

Always Verify Tests and Build After Any Change
- After you modify or add files, you MUST validate both tests and the build before finishing.
- Preferred commands:
  - Local: `make check` (runs `go mod tidy`, `go vet`, `go test ./...`)
  - Local build: `make build` (produces `bin/whatsmeow-adapter`)
  - Docker build: `make docker-build` (equivalent to `docker build -t provider-whatsmeow:local .`)
- If Makefile targets are unavailable in your environment, run:
  - `go mod tidy`
  - `go test ./...`
  - `go build -o bin/whatsmeow-adapter ./cmd/whatsmeow-adapter`

Environment Notes
- Building locally may require CGO deps for Opus. If unavailable, use:
  - `go test -tags nopkgconfig ./...`
  - `go build -tags nopkgconfig -o bin/whatsmeow-adapter ./cmd/whatsmeow-adapter`
- The Dockerfile’s builder stage already installs required packages and runs `go test ./...`.

Logging
- Default log level is `error`. To increase verbosity during debugging:
  - Set `LOG_LEVEL=info` or `LOG_LEVEL=debug`.

Style & Scope
- Keep changes minimal and focused on the task.
- Do not introduce unrelated refactors in the same patch.
- Prefer adding tests when changing logic that affects routing, normalization, or message composition.

