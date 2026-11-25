---
description: This document provides guidances for your development process
globs:
alwaysApply: true
---

# Developemnt tools
### Mockery
- Used for generating mock implementations.
- All generated mocks are stored in `mocks/`.
- Configuration is defined in `.mockery.yml`
- Example configuration:
```yaml
packages:
  this/is/the/firstpackage: # The package path
    config:
      dir: "mocks/firstpackage" # The mock directory
      filename: "mock_{{.InterfaceName}}.go" # Filename format
    interfaces:
      IDatabase: # Your Interface name here
        config:
      IHttpClient:
        config: # Your Interface name here
  this/is/the/secondpackage: # The package path
    config:
      dir: "mocks/secondpackage"
      filename: "mock_{{.InterfaceName}}.go"
    interfaces:
      IUsecase:
        config:
```

### Golang Linter
- We use `golangci-lint` to ensure coding standards and eliminate code smells.
- Configuration is stored in `.golangci.yaml`.

### Buf build for protobuf generation
- We use Buf for generating gRPC code from `.proto` files.
- Generated file structure:
  - Proto files are stored in `proto/` folder
  - Generated golang code packages are stored in `pkg/` folder
  - Generated swagger json files are stored in `swagger/` folder
- Buf configuration files: `buf.gen.yaml`, `buf.lock`, `buf.yaml`
- Required protoc plugins:
  - protoc-gen-go
  - protoc-gen-go-grpc
  - protoc-gen-grpc-gateway (v2)
  - protoc-gen-openapiv2 (v2)

# Docker usage for development
- `Dockerfile.dev`: the development environment, containerized into a Docker image.
- `Dockerfile`: the runtime environment, serving for runtime deployments.

# Development operations
- The `Makefile` contains all essential commands.
- gvm (https://github.com/moovweb/gvm) is recommended for switching between go environments
- `Makefile` usage:
  - Install development environment:  `make install-dev-env`
  - Clean up the build: `make clean`
  - Acquire go vendor: `make vendor`
  - Run linter: `make lint`
  - Generate golang code from proto files: `make gen-proto`
  - Build code: `make build`
  - Generate mocks: `make gen-mock`
  - Run unit tests: `make test`
  - Run unit tests with coverage reports: `make test-coverage`
  - Run unit tests with HTML coverage reports: `test-coverage-html`

# Development rules
The following rules must be followed **STRICTLY** in the development process:
- After completing a code change (a new function or a modification):
  - Write unit tests to cover the new code.
  - Run the test and fix **ALL** bugs before starting a new implementation.
  - Run linter and check for code smells.
- If you modify an interface with a mock config, re-generate its mock.
- If you modify `.proto` files, regenerate the corresponding Go code.
- If any tools are missing, run `make install-dev-env`.
