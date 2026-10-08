# MVEP_SKILL — Mainvec Platform (MVEP) Integration Guide

> **Audience:** AI coding agents and human developers integrating MVEP into their projects.
>
> **What is MVEP?** The Mainvec Platform is a **spec-driven, command-based API framework** that standardizes how applications define their commands and APIs. You write a declarative JSON spec, and the toolchain generates type-safe server code, client code, CLI tools, and API definitions in Go and JavaScript/TypeScript.

---

## Table of Contents

- [Ecosystem Overview](#ecosystem-overview)
- [Architecture](#architecture)
- [The MVEP Spec Format](#the-mvp-spec-format)
- [MVEP CLI Reference](#mvp-cli-reference)
- [Project Integration Guide](#project-integration-guide)
- [Generated Code Structure](#generated-code-structure)
- [Core Generated Patterns](#core-generated-patterns)
- [runtime/go Runtime](#runtime/go-runtime)
- [ugo Utilities](#ugo-utilities)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [For AI Agents — Quick Reference](#for-ai-agents--quick-reference)

---

## Ecosystem Overview

MVEP consists of three core components:

| Component | Module | Purpose |
|-----------|--------|---------|
| **mvp generator** | `github.com/mainvec/mvep/toolkit` | Code generator — transforms MVEP specs into Go, JS/TS, and Protobuf code |
| **runtime/go** | `github.com/mainvec/mvep/runtime/go` | Runtime library — `mvep.Package` and `mvep.CommandRunner` interfaces, HTTP/Unix socket server & client, middleware/interceptor system |
| **ugo** | `github.com/mainvec/ugo` | Go utilities — CLI framework (`cli`), ordered maps (`omap`), encoding registry (`oencoding`), validation, collections |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        MVEP Spec (JSON/JSONC)                     │
│                    (your-service-spec.json)                       │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │      mvp       │  Code Generator
              │  (CLI tool)    │
              └───────┬────────┘
                      │ generates
        ┌─────────────┼─────────────────────────┐
        ▼             ▼                         ▼
   Go Code        JS/TS Code             Proto Definitions
   ├── api/           ├── api/               ├── api/*.proto
   │   ├── *.plain.go │   ├── *.js           └── api/*.pb.go
   │   └── *_package.go   ├── *.d.ts
   ├── *_impl.go      │   └── *_package.js
   ├── *_commands.go   │
   └── cmd/*/main.go   │
        │               │
        ▼               ▼
  ┌──────────────────────────────────────────┐
  │   Implements mvep.Package &               │
  │   mvep.CommandRunner interfaces           │
  │            (from runtime/go)                  │
  └──────────────────┬───────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────┐
  │   PackageHandler                         │
  │   ├── Interceptor chain (auth, logging)  │
  │   ├── ServeCmd / ServeCmdReq             │
  │   └── HTTP / Unix socket transport       │
  └──────────────────────────────────────────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
           Server        Client
       (mvp/server)   (mvp/client)
```

**Foundation layer:** `ugo` provides the CLI framework (used by the descriptor-driven `mvep/cli` builder and generated `cmd/` code), ordered maps (used by the generator for deterministic output), and the encoding registry (used by runtime/go for JSON/Protobuf serialization).

---

## The MVEP Spec Format

MVEP specs are JSON or JSONC files validated against a JSON Schema (`2020-12` draft).

**Schema URL:** `https://spec.mainvec.com/mvepspec/0.2/schema/2026-01-15`

Legacy specs using `https://spec.mainvec.com/mvepspec/0.1/schema/...` remain supported for backward compatibility.

### Spec Structure

```jsonc
{
  "$id": "acmeapp",
  "$schema": "https://spec.mainvec.com/mvepspec/0.2/schema/2026-01-15",
  "name": "acmeapp",
  "namespace": "acmeappns",
  "title": "Acme Application API",
  "desc": "API specification for the Acme application",
  "version": "v0.1",

  "gen_options": {
    "go_package": "github.com/acme/acmeapp/mvepapi/go;acmeapp",
    "go_api_package": "github.com/acme/acmeapp/mvepapi/go/api;api",
    "format": "plain",           // "plain" (Go structs + JSON) or "pb3" (protobuf)
    "cli": "runtime",            // "runtime" (default, descriptor-driven cli.New), "legacy", or "none"
    "edition": "2023",
    "go_default_api_level": "API_OPAQUE"
  },

  "commands": {
    // Commands define the API operations
    "UserRegisterCmd": {
      "title": "Register a new user",
      "alias": "register",
      "desc": "Creates a new user account with email and password",
      "fields": {
        "email":    { "fnum": 1, "type": "string", "title": "User email",    "tags": ["required"] },
        "password": { "fnum": 2, "type": "string", "title": "User password", "tags": ["required"] },
        "name":     { "fnum": 3, "type": "string", "title": "Display name" }
      },
      "resultFields": {
        "userID": { "fnum": 1, "type": "string", "title": "Created user ID" },
        "token":  { "fnum": 2, "type": "string", "title": "Auth token" }
      }
    },

    "UserGetProfileCmd": {
      "title": "Get user profile",
      "alias": "get_profile",
      "fields": {
        "userID": { "fnum": 1, "type": "string", "tags": ["required"] }
      },
      "resultFields": {
        "user": { "fnum": 1, "type": "recRef", "$ref": "#/recordsDefs/User", "title": "User record" }
      }
    },

    "UserUpdateSettingsCmd": {
      "title": "Update user settings",
      "alias": "update_settings",
      "fields": {
        "userID":   { "fnum": 1, "type": "string", "tags": ["required"] },
        "settings": { "fnum": 2, "type": "map", "valueType": "string", "title": "Key-value settings" }
      },
      "resultFields": {
        "updated": { "fnum": 1, "type": "boolean" }
      }
    },

    "OrderCreateCmd": {
      "title": "Create a new order",
      "alias": "create_order",
      "group": "orders",           // optional: place under a CLI command group
      "fields": {
        "customerID": { "fnum": 1, "type": "string", "tags": ["required"] },
        "items":      { "fnum": 2, "type": "recRef", "$ref": "#/recordsDefs/OrderItem", "repeated": true, "title": "Order items" },
        "notes":      { "fnum": 3, "type": "string" }
      },
      "resultFields": {
        "orderID":  { "fnum": 1, "type": "string" },
        "total":    { "fnum": 2, "type": "double" },
        "createdAt": { "fnum": 3, "type": "timestamp" }
      }
    }
  },

  "commandGroups": {
    // Optional metadata for CLI command groups, keyed by full path.
    "orders": { "title": "Orders", "desc": "Create and manage orders" }
  },

  "recordsDefs": {
    // Shared data structures referenced by commands
    "User": {
      "name": "User",
      "title": "User record",
      "fields": {
        "id":        { "fnum": 1, "type": "string" },
        "email":     { "fnum": 2, "type": "string" },
        "name":      { "fnum": 3, "type": "string" },
        "active":    { "fnum": 4, "type": "boolean" },
        "createdAt": { "fnum": 5, "type": "timestamp" },
        "metadata":  { "fnum": 6, "type": "map", "valueType": "string" }
      }
    },
    "OrderItem": {
      "name": "OrderItem",
      "title": "An item in an order",
      "fields": {
        "productID": { "fnum": 1, "type": "string" },
        "quantity":  { "fnum": 2, "type": "int32" },
        "price":     { "fnum": 3, "type": "double" }
      }
    }
  }
}
```

### Required Top-Level Fields

| Field | Description |
|-------|-------------|
| `$id` | Unique identifier for the service |
| `name` | Service name (used for file naming) |
| `namespace` | Service namespace (used for protobuf package) |

### Field Type Reference

| Type | Go Type | JS/TS Type | Description |
|------|---------|------------|-------------|
| `string` | `string` | `string` | UTF-8 string |
| `boolean` | `bool` | `boolean` | True/false |
| `int32` | `int32` | `number` | 32-bit signed integer |
| `int64` | `int64` | `number` | 64-bit signed integer |
| `uint32` | `uint32` | `number` | 32-bit unsigned integer |
| `sint32` | `int32` | `number` | ZigZag-encoded signed integer |
| `float` | `float32` | `number` | 32-bit floating point |
| `double` | `float64` | `number` | 64-bit floating point |
| `bytes` | `[]byte` | `Uint8Array` | Raw bytes |
| `timestamp` | `*timestamppb.Timestamp` / `time.Time` | `Date` | Point in time |
| `duration` | `*durationpb.Duration` | `number` | Time duration |
| `uuid` | `string` | `string` | UUID string |
| `recRef` | Pointer to struct | Object | Reference to a `recordsDefs` entry |
| `map` | `map[string]T` | `Object` | String-keyed map (use `valueType`) |
| `recDef` | Inline struct | Object | Inline record definition |
| `oneOf` | Interface | Union type | One-of discriminated union |

### Special Field Properties

| Property | Description |
|----------|-------------|
| `fnum` | **Required.** Unique field number (maps to protobuf field number). Never reuse. |
| `type` | **Required.** One of the types from the table above. |
| `repeated` | `true` for arrays/slices of the type. |
| `tags` | Array of tags, e.g. `["required"]`. |
| `alias` | CLI flag alias for the field. |
| `$ref` | For `recRef` type: `"#/recordsDefs/RecordName"`. |
| `valueType` | For `map` type: the value type (e.g. `"string"`, `"boolean"`, `"int32"`). |
| `title` | Short human-readable label. |
| `desc` | Longer description. |

### Gen Options

| Option | Values | Description |
|--------|--------|-------------|
| `format` | `plain`, `pb3` | `plain` = Go structs with JSON tags (no protobuf dependency). `pb3` = full protobuf. |
| `go_package` | Module path | Go module path for the generated package |
| `go_api_package` | Module path | Go module path for the `api/` sub-package |
| `edition` | `2023` | Protobuf edition (when using `pb3` format) |
| `go_default_api_level` | `API_OPAQUE`, etc. | Protobuf API level |

---

## MVEP CLI Reference

### Installation

```bash
go install <module>/mvepapi/cmd/mvep@latest
```

### Commands

| Command | Description | Required Flags |
|---------|-------------|----------------|
| `generate` | Generate code from an MVEP spec | `--in`, `--lang` |
| `validate` | Validate a spec against the JSON Schema | `--in` |
| `init` | Initialize a new MVEP spec file | `--name`, `--ns` |

> Commands are driven by the package descriptor. The spec's `alias` field
> becomes the command name (e.g. `generate`, `init`, `validate`); the
> snake_case struct name (`generate_cmd`) is an alias. The `gen` alias from
> the legacy hand-wired CLI is not present by default — add it via
> `App.Root().AddCommand()` if needed.

### Command groups

A command's optional `group` field (a `/`-separated path) places it under a
nested CLI subcommand, so `"group": "orders"` with `"alias": "create_order"`
yields `svc orders create_order`. Group metadata (title, description, aliases,
hidden) lives in the optional top-level `commandGroups` object, keyed by full
path; a group referenced by a command but absent there is auto-created with the
path segment as its name. Groups are a CLI presentation concern only — they do
not affect routes, envelopes or encodings, and a spec with no `group` generates
the same flat tree as before.

### The reserved `mvep` namespace

Every generated CLI reserves a single top-level `mvep` group that provides a
spec-independent, machine-readable surface:

```
cat p.json | svc mvep exec generate            # run a command from a JSON payload
svc mvep exec --input p.json generate          # flags precede the command name
cat reqs.ndjson | svc mvep send                # stream CmdReq -> CmdResp envelopes
svc mvep list                                  # command names
svc mvep describe [command]                    # versioned schema projection
```

- **`mvep exec`** reads a complete payload from `--input <path>`, `--input -`,
  or implicitly from stdin when stdin is not a terminal. Payload keys are
  validated against the descriptor (unknown keys, including nested record
  fields, hard-error), then decoded with the same encoder registry the server
  uses.
- **`mvep send`** reads a stream of `CmdReq` envelopes (NDJSON or concatenated)
  and emits one `CmdResp` per record, flushing immediately for live pipelines.
  `--fail-fast` halts at the first error; the process exits non-zero if any
  record errored. Request headers ride the context, so interceptors behave
  identically under the CLI and over HTTP, and response headers round-trip.
- **`mvep list`** prints command names (a JSON array under `--mvep-output json`).
- **`mvep describe`** emits a versioned JSON projection (name, alias, group,
  description, fields, result).
- **`--mvep-output json|text`** (a persistent flag on every command) renders
  results and errors as machine-readable JSON; errors serialize as
  `{"error":...}` on stdout, shaped like a `send` record's `CmdResp.Error`.

The namespace name is overridable via `cli.New(desc, executor,
cli.WithNamespace("acme"))`, which also renames the output flag to
`--acme-output`. A spec that declares a top-level command or group named `mvep`
fails generation (reserved-name validation). Because ugo inherits stdlib `flag`
parsing, `--input`/`--fail-fast` must precede the command name inside the
namespace verbs. See `runtime/go/mvep/cli/README.md` for the full guide.

### Flags

| Flag | Commands | Description |
|------|----------|-------------|
| `--in` | `generate`, `validate` | Path to the MVEP spec file |
| `--lang` | `generate` | Target language(s): `go`, `js`, or comma-separated `go,js` |
| `--outdir` | `generate` | Output directory for generated code |
| `--format` | `generate` | Output format: `plain` (default) or `pb3` |
| `--name` | `init` | Service name for the new spec |
| `--ns` | `init` | Namespace for the new spec |

### Examples

```bash
# Generate Go code (plain structs mode)
mvep generate --in ./spec/acmeapp-spec.json --lang go --outdir ./go --format=plain

# Generate JavaScript/TypeScript code
mvep generate --in ./spec/acmeapp-spec.json --lang js --outdir ./js --format=plain

# Generate both Go and JS in one invocation
mvep generate --in ./spec/acmeapp-spec.json --lang go,js --outdir ./out

# Generate Go code with protobuf
mvep generate --in ./spec/acmeapp-spec.json --lang go --outdir ./go --format=pb3

# Validate a spec
mvep validate --in ./spec/acmeapp-spec.json

# Initialize a new spec
mvep init --name myservice --ns myservicens
```

---

## Project Integration Guide

### Step 1: Create the Project Structure

```
your-project/
└── mvepapi/
    ├── generate_api.sh          # Code generation script
    └── spec/
        └── acmeapp-spec.json    # Your MVEP specification
```

### Step 2: Write Your MVEP Spec

Create `mvepapi/spec/<name>-spec.json` following the [spec format](#the-mvp-spec-format) above. Start with:

```jsonc
{
  "$id": "acmeapp",
  "$schema": "https://spec.mainvec.com/mvepspec/0.2/schema/2026-01-15",
  "name": "acmeapp",
  "namespace": "acmeappns",
  "title": "Acme Application API",
  "version": "v0.1",
  "gen_options": {
    "go_package": "github.com/acme/acmeapp/mvepapi/go;acmeapp",
    "go_api_package": "github.com/acme/acmeapp/mvepapi/go/api;api",
    "format": "plain"
  },
  "commands": {},
  "recordsDefs": {}
}
```

### Step 3: Create the Generation Script

Create `mvepapi/generate_api.sh`:

```bash
#!/bin/bash

# Generate API code from MVEP spec
# Usage: cd mvepapi && bash generate_api.sh

SPEC="./spec/acmeapp-spec.json"

mvep generate -in "$SPEC" -lang go -outdir ./go -format=plain \
&& \
mvep generate -in "$SPEC" -lang js -outdir ./js -format=plain

if [ $? -eq 0 ]; then
  echo "✓ API generated successfully"
else
  echo "✗ API generation failed"
  exit 1
fi
```

```bash
chmod +x mvepapi/generate_api.sh
```

### Step 4: Generate the Code

```bash
cd mvepapi
bash generate_api.sh
```

### Step 5: Implement Your Commands

Open the generated `*_impl.go` file. Each command has a stub like:

```go
func runUserRegisterCmd(ctx context.Context, cmd *api.UserRegisterCmd) (*api.UserRegisterCmdResult, error) {
    return nil, errors.New("command not implemented")
}
```

Replace the stub with your business logic:

```go
func runUserRegisterCmd(ctx context.Context, cmd *api.UserRegisterCmd) (*api.UserRegisterCmdResult, error) {
    user, err := createUser(ctx, cmd.Email, cmd.Password, cmd.Name)
    if err != nil {
        return nil, fmt.Errorf("registration failed: %w", err)
    }
    token, err := issueToken(ctx, user.ID)
    if err != nil {
        return nil, fmt.Errorf("token generation failed: %w", err)
    }
    return &api.UserRegisterCmdResult{
        UserID: user.ID,
        Token:  token,
    }, nil
}
```

### Step 6: Wire Up the Server (with runtime/go)

```go
package main

import (
    "context"
    "log"
    "os/signal"
    "syscall"
    "time"

    "github.com/acme/acmeapp/mvepapi/go/api"
    acmeapp "github.com/acme/acmeapp/mvepapi/go"
    "github.com/mainvec/mvep/runtime/go/mvep"
    "github.com/mainvec/mvep/runtime/go/mvep/server"
)

func main() {
    srv, err := server.NewServer(&server.ServerConfig{
        Listeners: []server.ListenerConfig{{Address: ":8080"}},
        BasePath:  "/api",
        Interceptor: mvep.Chain(
            mvep.RecoveryInterceptor(),
            mvep.LoggingInterceptor(),
            mvep.RequestIDInterceptor(nil),
        ),
    })
    if err != nil {
        log.Fatal(err)
    }

    if err := srv.RegisterPackage(api.NewPackage(), acmeapp.GetCommandRunner()); err != nil {
        log.Fatal(err)
    }

    if err := srv.StartAsync(); err != nil {
        log.Fatal(err)
    }

    // The application owns signal handling; mvep only owns the HTTP surface.
    signalCtx, stopSignals := signal.NotifyContext(
        context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stopSignals()

    select {
    case <-signalCtx.Done():
        ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
        defer cancel()
        _ = srv.ShutdownContext(ctx)
    case <-srv.Done():
        log.Printf("server stopped: %v", srv.Err())
    }
}
```

---

## Generated Code Structure

After running `mvep generate`, your `mvepapi/` directory will look like:

```
mvepapi/
├── generate_api.sh
├── spec/
│   └── acmeapp-spec.json           # Your MVEP specification (you write this)
├── go/
│   ├── go.mod                      # Generated Go module file
│   ├── acmeapp_impl.go             # ✏️  EDIT THIS — command implementations
│   ├── acmeapp_commands.go         # ⛔ Generated — GetCommandRunner() factory
│   ├── api/
│   │   ├── acmeapp.plain.go        # ⛔ Generated — Go structs (plain mode)
│   │   └── acmeapp_package.go      # ⛔ Generated — Package, CommandRunner, handlers
│   └── cmd/
│       └── acmeapp/
│           └── acmeapp_main_cmd.go # ⛔ Generated (runtime) or ✏️ NOMVEP (custom) — CLI entry point
└── js/
    └── api/
        ├── acmeapp.js              # ⛔ Generated — JS classes with JSDoc
        ├── acmeapp.d.ts            # ⛔ Generated — TypeScript type definitions
        ├── acmeapp_package.js      # ⛔ Generated — Package utilities
        └── client/                 # ✏️  Hand-written — typed client (see JS/TS Client section)
            ├── acmeapp_client.ts
            ├── acmeapp_package.ts
            └── index.ts
```

**With `--format=pb3`** (protobuf mode), the `api/` directory contains instead:

```
api/
├── acmeapp.proto                   # ⛔ Generated — Protobuf definition
├── acmeapp.pb.go                   # ⛔ Generated — Compiled protobuf Go code
└── acmeapp_package.go              # ⛔ Generated — Package, CommandRunner, handlers
```

### File Edit Safety

| File | Safe to Edit? | Notes |
|------|---------------|-------|
| `*_impl.go` | **Yes** | This is where you implement your business logic |
| `*_commands.go` | No | Regenerated — wires handler functions to the runner |
| `api/*_package.go` | No | Regenerated — handler types, PkgCommandRunner, dispatch |
| `api/*.plain.go` / `api/*.pb.go` | No | Regenerated — data structures |
| `api/*.proto` | No | Regenerated — protobuf definitions |
| `cmd/*/main.go` | No (runtime) / Yes (NOMVEP) | Regenerated by default (descriptor-driven `cli.New`); protect with `// NOMVEP` to customize |
| `js/api/*` | No | Regenerated — JavaScript/TypeScript code |

### Protecting Files from Overwrite

Add `// NOMVEP` as the **first line** of any generated file to prevent regeneration from overwriting it (the generator also still honors the legacy `// NOMVGEN` and `// NOWOGEN` markers):

```go
// NOMVEP
package acmeapp

// This file is now protected from regeneration.
// ... your customizations ...
```

---

## Core Generated Patterns

### Handler Types (in `*_package.go`)

For each command, the generator emits a typed handler function signature:

```go
type UserRegisterCmdHandler func(context.Context, *UserRegisterCmd) (*UserRegisterCmdResult, error)
type UserGetProfileCmdHandler func(context.Context, *UserGetProfileCmd) (*UserGetProfileCmdResult, error)
type OrderCreateCmdHandler func(context.Context, *OrderCreateCmd) (*OrderCreateCmdResult, error)
```

### PkgCommandRunner (in `*_package.go`)

A struct holding one handler per command, implementing `mvep.CommandRunner`:

```go
type PkgCommandRunner struct {
    RunUserRegisterCmd      UserRegisterCmdHandler
    RunUserGetProfileCmd    UserGetProfileCmdHandler
    RunUserUpdateSettingsCmd UserUpdateSettingsCmdHandler
    RunOrderCreateCmd       OrderCreateCmdHandler
}

// Implements mvep.CommandRunner — dispatches by type
func (r *PkgCommandRunner) RunCmd(ctx context.Context, cmd any) (any, error) {
    switch cmd := cmd.(type) {
    case *UserRegisterCmd:
        return r.RunUserRegisterCmd(ctx, cmd)
    case *UserGetProfileCmd:
        return r.RunUserGetProfileCmd(ctx, cmd)
    case *OrderCreateCmd:
        return r.RunOrderCreateCmd(ctx, cmd)
    // ...
    }
    return nil, fmt.Errorf("unknown command type: %T", cmd)
}
```

### Package Interface (in `*_package.go`)

The package implements `mvep.Package` via `mvep.NewPackageFromDesc`, which derives
`InstanceOf`/`NameOf`/`CommandNames` from the descriptor rather than emitting hand-
written switch statements. The generated code is:

```go
var pkgDesc = mvep.PackageDesc{
    Name:        "acmeapp",
    // ...
    Commands: []mvep.CommandDesc{ /* ... */ },
    Records:  []mvep.RecordDesc{ /* ... */ },
}

var pkg = mvep.NewPackageFromDesc(&pkgDesc)

func NewPackage() mvep.Package { return pkg }
func Describe() *mvep.PackageDesc { return &pkgDesc }

// InstanceOf constructs a command or result by name, derived from pkgDesc.
func InstanceOf(compName string) (any, bool) { return pkg.InstanceOf(compName) }

// NameOf returns the name of a command or result, derived from pkgDesc.
func NameOf(comp any) string { return pkg.NameOf(comp) }
```

`GetName()` still returns `Name + "Package"` (e.g. `"acmeappPackage"`) to preserve
HTTP routing — the suffix is a legacy compatibility shim.

The descriptor (`PackageDesc`) is emitted by codegen from the same `ExecuteGenerate`
run that produces the command structs, so the two cannot disagree.
`FieldDesc.Ptr` closes over a real struct field; a codegen mistake is a compile
error, not a silent runtime drop. Build-time inputs (`GenOpts`, `ProtocOpts`) are
deliberately excluded — the descriptor describes what a package *is* at runtime,
not how it was *built*.

### GetCommandRunner Factory (in `*_commands.go`)

Wires the impl functions to the runner:

```go
func GetCommandRunner() *api.PkgCommandRunner {
    return &api.PkgCommandRunner{
        RunUserRegisterCmd:       runUserRegisterCmd,
        RunUserGetProfileCmd:     runUserGetProfileCmd,
        RunUserUpdateSettingsCmd: runUserUpdateSettingsCmd,
        RunOrderCreateCmd:        runOrderCreateCmd,
    }
}
```

### Implementation Stubs (in `*_impl.go`)

Each command gets a stub — this is where you write your logic:

```go
func runUserRegisterCmd(ctx context.Context, cmd *api.UserRegisterCmd) (*api.UserRegisterCmdResult, error) {
    return nil, errors.New("command not implemented")
}

func runOrderCreateCmd(ctx context.Context, cmd *api.OrderCreateCmd) (*api.OrderCreateCmdResult, error) {
    return nil, errors.New("command not implemented")
}
```

### CLI Entry Point (in `cmd/*/`*_main_cmd.go`)

The CLI mode is controlled by `gen_options.cli`:

| Mode | Behaviour |
|------|-----------|
| `runtime` (default) | Emits a descriptor-driven `cli.New(api.Describe(), ...)` main |
| `legacy` | Emits the old hand-wired `prepareXxxCmd` pattern |
| `none` | No CLI main generated |

`skipCmd=true` forces `none` regardless of the genopt. The generated
`runtime` main is:

```go
func main() {
    app := cli.New(api.Describe(), &cli.LocalExecutor{Runner: runner})
    app.Root().Version = resolveVersion()
    err := app.Run(context.Background())
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(cli.ExitCode(err))
    }
}
```

Add `// NOMVEP` as the first line to protect a hand-customized entry point.
The `mvep/cli` library provides flag binding (all `FieldType`s via `Ptr`),
required-flag enforcement, pre/post hooks, custom renderers, the reserved
`mvep` namespace (`exec`/`send`/`list`/`describe`), the `--mvep-output` JSON
renderer, per-field `-file` hatches, and exit-code classification. See
`runtime/go/mvep/cli/README.md` for the full guide.

---

## runtime/go Runtime

`github.com/mainvec/mvep/runtime/go` provides the runtime infrastructure for serving and consuming MVEP APIs.

### Core Interfaces

```go
// mvep.Package — component registry for a service
type Package interface {
    GetName() string
    InstanceOf(compName string) (any, bool)  // factory: name → zero-value instance
    NameOf(comp any) string                   // reverse: instance → name
}

// mvep.CommandRunner — command execution
type CommandRunner interface {
    RunCmd(ctx context.Context, cmd any) (any, error)
}
```

### Request/Response Envelope

Commands are wrapped in envelopes with headers for transport:

```go
type CmdReq struct {
    Cmd     any
    Headers map[string]string  // headers use "x-mvep-" prefix in HTTP
    Payload []byte
}

type CmdResp struct {
    Headers map[string]string
    Payload []byte
    Error   *ErrorInfo
}
```

### PackageHandler

The bridge between your package, command runner, and transport layer:

```go
handler := mvep.NewPackageHandler(pkg, transporter, runner, interceptor)

// Server-side: handle incoming commands
handler.ServeCmdReq(ctx, req) *CmdResp

// Client-side: send commands
handler.SendCmdReq(ctx, req) *CmdResp
```

### Interceptor / Middleware System

Interceptors wrap command execution for cross-cutting concerns:

```go
type CmdHandler func(ctx context.Context, req *CmdReq) *CmdResp
type CmdInterceptor func(ctx context.Context, req *CmdReq, next CmdHandler) *CmdResp
```

**Built-in interceptors:**

| Interceptor | Purpose |
|-------------|---------|
| `LoggingInterceptor()` | Logs command timing and structured metadata |
| `AuthInterceptor(validator)` | Token validation via `TokenValidator` interface |
| `RecoveryInterceptor()` | Catches panics and returns error responses |
| `RequestIDInterceptor(generator)` | Adds unique request IDs |

**Composition helpers:**

```go
// Chain multiple interceptors
chain := mvep.Chain(
    mvep.RecoveryInterceptor(),
    mvep.LoggingInterceptor(),
    mvep.AuthInterceptor(myValidator),
)

// Skip auth for specific commands
auth := mvep.SkipCommands(
    mvep.AuthInterceptor(myValidator),
    "UserRegisterCmd", "UserLoginCmd",
)

// Apply only to specific commands
admin := mvep.OnlyCommands(
    adminCheckInterceptor,
    "AdminDeleteUserCmd", "AdminResetCmd",
)
```

### Server

```go
srv, err := server.NewServer(&server.ServerConfig{
    Listeners:         []server.ListenerConfig{{Address: ":8080"}},
    BasePath:          "/api",
    EnableHealthCheck: true,
    EnableCORS:        true,
    AllowedOrigins:    []string{"https://app.example.com"},
    MaxRequestBytes:   4 << 20, // default 4 MiB; oversized bodies get 413
    VerboseErrors:     false,   // true only for local dev — reflects raw errors to callers
})
if err != nil {
    return err
}

if err := srv.RegisterPackage(pkg, runner); err != nil {
    return err
}

// StartAsync returns once every listener is bound and serving.
if err := srv.StartAsync(); err != nil {
    return err
}

// ... own your signal handling, then shut down explicitly:
ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
defer cancel()

serverErr := srv.ShutdownContext(ctx) // drains active requests
cleanupErr := myApp.Close()           // your cleanup, in your order
return errors.Join(serverErr, cleanupErr)
```

The server installs **no signal handlers**. `Start()` still blocks, but it
returns on explicit shutdown or a fatal serve error. `ServerConfig.OnShutdown`
was removed in runtime v0.8.0 — sequence cleanup around `ShutdownContext`
instead. See `runtime/go/mvep/server/SERVER.md` for the full lifecycle contract.

#### HTTP hardening (runtime v0.9.0)

`PackageHandler.ServeHTTP` enforces real HTTP semantics instead of treating
HTTP as a byte pipe:

| Behavior | Detail |
|----------|--------|
| Method enforcement | Non-`POST` requests get `405 method_not_allowed`; the runner is never invoked. |
| Content-Type parsing | Parsed as a media type (`application/json; charset=utf-8` still resolves the JSON encoder); unregistered types get `415`. |
| Status mapping | Exported `mvep.HTTPStatusForErrorCode(code)` maps stable codes to HTTP statuses (`400`/`401`/`403`/`404`/`405`/`413`/`415`/`500`). The machine-readable code is echoed in the `x-mainvec-error-code` response header. |
| Error redaction | **Default now redacts.** Handler error detail is logged server-side with the request id; the client gets a generic message. Set `VerboseErrors: true` to restore raw error reflection (local dev only). |
| Body size limits | `MaxRequestBytes` (default 4 MiB) bounds command bodies; `http.Server.MaxHeaderBytes` is capped at 1 MiB per listener. |

**CORS is an explicit allowlist**, not a wildcard:

- `EnableCORS: true` with empty `AllowedOrigins` emits **no** CORS headers and logs a startup warning (fail closed) — it no longer sends `Access-Control-Allow-Origin: *`.
- An allowed origin is echoed back with `Vary: Origin`.
- Advertised methods no longer include `PUT`/`DELETE` (MVEP only uses `POST`).

**`LocalTrustMiddleware` verifies the peer** before marking a request as
locally trusted (which lets `AuthInterceptor` skip token validation): trusted
only for a Unix-socket peer or a loopback TCP address. Anything else passes
through untrusted and is logged — a listener accidentally exposed to the
network fails closed instead of silently bypassing auth.

```go
handler := mvep.NewPackageHandler(pkg, transporter, runner, interceptor)
mux.Handle("/internal/", mvep.LocalTrustMiddleware(handler))
```

### Go Client

`github.com/mainvec/mvep/runtime/go/mvep/client` provides a full-featured Go client for calling MVEP services.

#### `ClientConfig`

```go
type ClientConfig struct {
    BaseURL     string              // Required. e.g. "http://localhost:8080" or "unix:///tmp/my.sock"
    BasePath    string              // URL path prefix, e.g. "/api"
    Encoder     string              // Content type, default "application/json"
    Timeout     time.Duration       // HTTP timeout, default 30s
    HTTPClient  *http.Client        // Optional custom HTTP client
    Interceptor mvep.ClientInterceptor // Optional interceptor chain
}
```

#### Creating a Client

```go
import (
    "github.com/mainvec/mvep/runtime/go/mvep/client"
    "github.com/mainvec/mvep/runtime/go/mvep"
    "github.com/acme/acmeapp/mvepapi/go/api"
)

mvpClient, err := client.NewClient(client.ClientConfig{
    BaseURL:  "http://localhost:8080",
    BasePath: "/api",
})
if err != nil {
    log.Fatal(err)
}
defer mvpClient.Close()

// Register the generated package
pkg := api.NewPackage()
pkgClient, err := mvpClient.RegisterPackage(pkg)
if err != nil {
    log.Fatal(err)
}
```

#### Sending Commands

```go
// Simple — no headers
result, err := pkgClient.SendCmd(ctx, &api.UserRegisterCmd{
    Email:    "alice@example.com",
    Password: "s3cret",
    Name:     "Alice",
})
if err != nil {
    log.Fatal(err)
}
regResult := result.(*api.UserRegisterCmdResult)
fmt.Println("User ID:", regResult.UserID)
fmt.Println("Token:", regResult.Token)

// With headers — returns typed result + response envelope
result, resp, err := pkgClient.SendCmdReq(ctx, &api.UserGetProfileCmd{
    UserID: regResult.UserID,
}, map[string]string{
    "auth": regResult.Token,
})
if err != nil {
    log.Fatal(err)
}
profileResult := result.(*api.UserGetProfileCmdResult)
fmt.Println("Name:", profileResult.User.Name)
```

#### Client Interceptors

```go
type ClientInvoker func(ctx context.Context, req *CmdReq) (*CmdResp, error)
type ClientInterceptor func(ctx context.Context, req *CmdReq, invoker ClientInvoker) (*CmdResp, error)
```

**Built-in client interceptors:**

| Interceptor | Description |
|-------------|-------------|
| `AuthHeaderInterceptor(tokenProvider)` | Dynamically injects `auth` header. `TokenProvider = func(ctx) (string, error)` |
| `StaticAuthHeaderInterceptor(token)` | Adds a fixed `auth` header to every request |
| `HeaderInterceptor(headers)` | Adds custom static headers |
| `ClientLoggingInterceptor()` | Logs request/response timing via `slog` |
| `RetryInterceptor(maxRetries, delay)` | Retries on transport errors |
| `ClientRequestIDInterceptor(generator)` | Adds `request-id` header |
| `SkipCommandsClient(interceptor, cmds...)` | Skips interceptor for listed commands |

#### Building a Typed Go Client (Full Example)

A common pattern is wrapping `PackageClient` in a typed struct with auth management:

```go
package acmeclient

import (
    "context"
    "fmt"
    "sync"

    "github.com/mainvec/mvep/runtime/go/mvep"
    "github.com/mainvec/mvep/runtime/go/mvep/client"
    "github.com/acme/acmeapp/mvepapi/go/api"
)

type AcmeClient struct {
    mvpClient *client.Client
    pkgClient *client.PackageClient
    mu        sync.RWMutex
    authToken string
}

type AcmeClientConfig struct {
    BaseURL  string
    BasePath string
    Timeout  time.Duration
}

func NewAcmeClient(cfg AcmeClientConfig) (*AcmeClient, error) {
    ac := &AcmeClient{}

    // Auth interceptor reads token from the client struct
    tokenProvider := func(ctx context.Context) (string, error) {
        ac.mu.RLock()
        defer ac.mu.RUnlock()
        return ac.authToken, nil
    }

    mvpClient, err := client.NewClient(client.ClientConfig{
        BaseURL:  cfg.BaseURL,
        BasePath: cfg.BasePath,
        Timeout:  cfg.Timeout,
        Interceptor: mvep.ChainClient(
            mvep.ClientLoggingInterceptor(),
            mvep.AuthHeaderInterceptor(tokenProvider),
            mvep.RetryInterceptor(3, time.Second),
        ),
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create client: %w", err)
    }

    pkg := api.NewPackage()
    pkgClient, err := mvpClient.RegisterPackage(pkg)
    if err != nil {
        mvpClient.Close()
        return nil, fmt.Errorf("failed to register package: %w", err)
    }

    ac.mvpClient = mvpClient
    ac.pkgClient = pkgClient
    return ac, nil
}

func (c *AcmeClient) Close() error {
    return c.mvpClient.Close()
}

func (c *AcmeClient) SetAuthToken(token string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.authToken = token
}

// ── Typed command methods ──────────────────────────────────

func (c *AcmeClient) RegisterUser(ctx context.Context, email, password, name string) (*api.UserRegisterCmdResult, error) {
    result, _, err := c.pkgClient.SendCmdReq(ctx, &api.UserRegisterCmd{
        Email: email, Password: password, Name: name,
    }, nil)
    if err != nil {
        return nil, err
    }
    regResult := result.(*api.UserRegisterCmdResult)
    // Auto-set token on successful registration
    if regResult.Token != "" {
        c.SetAuthToken(regResult.Token)
    }
    return regResult, nil
}

func (c *AcmeClient) GetUserProfile(ctx context.Context, userID string) (*api.UserGetProfileCmdResult, error) {
    result, _, err := c.pkgClient.SendCmdReq(ctx, &api.UserGetProfileCmd{
        UserID: userID,
    }, nil)  // auth header injected automatically by interceptor
    if err != nil {
        return nil, err
    }
    return result.(*api.UserGetProfileCmdResult), nil
}

func (c *AcmeClient) CreateOrder(ctx context.Context, customerID string, items []*api.OrderItem, notes string) (*api.OrderCreateCmdResult, error) {
    result, _, err := c.pkgClient.SendCmdReq(ctx, &api.OrderCreateCmd{
        CustomerID: customerID, Items: items, Notes: notes,
    }, nil)
    if err != nil {
        return nil, err
    }
    return result.(*api.OrderCreateCmdResult), nil
}
```

**Using it:**

```go
func main() {
    client, err := acmeclient.NewAcmeClient(acmeclient.AcmeClientConfig{
        BaseURL:  "http://localhost:8080",
        BasePath: "/api",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    ctx := context.Background()

    // Register — auto-sets auth token
    reg, err := client.RegisterUser(ctx, "alice@example.com", "s3cret", "Alice")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("User ID:", reg.UserID)

    // Subsequent calls include auth token automatically
    profile, err := client.GetUserProfile(ctx, reg.UserID)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Name:", profile.User.Name)

    // Create an order
    order, err := client.CreateOrder(ctx, reg.UserID, []*api.OrderItem{
        {ProductID: "prod-1", Quantity: 2, Price: 29.99},
        {ProductID: "prod-2", Quantity: 1, Price: 49.99},
    }, "Rush delivery")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Order:", order.OrderID, "Total:", order.Total)
}
```

#### Unix Socket Client

For local IPC via Unix sockets, just change the `BaseURL`:

```go
mvpClient, err := client.NewClient(client.ClientConfig{
    BaseURL: "unix:///tmp/acmeapp.sock",
})
```

The client auto-detects the `unix://` scheme and configures the HTTP transport accordingly.

---

## ugo Utilities

`github.com/mainvec/ugo` provides foundational Go utilities used across the MVEP ecosystem.

### `cli` — CLI Framework

Used by generated `cmd/` code. Provides structured command definitions with flags, subcommands, and aliases.

```go
type Command struct {
    Usage, Short, Long string
    Hidden  bool
    Aliases []string
}

type Framework struct {
    DefaultRunner Runner
    Initializers  []Initializer
    Root          *Command
}
```

### `omap` — Ordered Map

`OMap[K, V]` maintains insertion order and supports sorted iteration. Used by the generator for deterministic code generation output.

```go
m := omap.New[string, int]()
m.Set("b", 2)
m.Set("a", 1)

// Iterate in key-sorted order
m.IteratorByKey(func(k string, v int) bool {
    fmt.Println(k, v)  // a 1, b 2
    return true
})
```

### `oencoding` — Encoding Registry

Pluggable encoding interface with global registry. Used by runtime/go for JSON and Protobuf serialization.

```go
type Encoding interface {
    Encode(v any) ([]byte, error)
    Decode(data []byte, v any) error
    MimeType() string
}
```

---

## JavaScript / TypeScript Client Usage

The generated JS/TS code provides everything you need to build a type-safe client for your MVEP API from browser or Node.js applications.

### What Gets Generated (JS side)

```
js/
└── api/
    ├── acmeapp.js              # JS classes with JSDoc — commands, records, constructors
    ├── acmeapp.d.ts            # TypeScript type definitions — interfaces & classes
    └── acmeapp_package.js      # Package utilities — instanceOf(), nameOf(), PACKAGE_NAME
```

### Generated JS Classes (`acmeapp.js`)

Each command and record becomes a JS class inside a namespace:

```javascript
// Code generated. DO NOT EDIT.
export const acmeappns = (() => {
  const ns = {};

  // Record classes
  ns.User = class User {
    static _typeName = 'User';
    constructor(data = {}) {
      /** @type {string} */
      this.id = data.id ?? '';
      /** @type {string} */
      this.email = data.email ?? '';
      /** @type {string} */
      this.name = data.name ?? '';
      /** @type {boolean} */
      this.active = data.active ?? false;
      /** @type {Date} */
      this.createdAt = data.createdAt ?? null;
    }
    static verify(message) { /* validates fields */ }
    static fromObject(obj) { /* creates instance from plain object */ }
    static toObject(message) { /* converts to plain object */ }
    toJSON() { /* serializes to JSON string */ }
  };

  // Command classes
  ns.UserRegisterCmd = class UserRegisterCmd {
    static _typeName = 'UserRegisterCmd';
    constructor(data = {}) {
      /** @type {string} */
      this.email = data.email ?? '';
      /** @type {string} */
      this.password = data.password ?? '';
      /** @type {string} */
      this.name = data.name ?? '';
    }
    // ... verify, fromObject, toObject, toJSON
  };

  ns.UserRegisterCmdResult = class UserRegisterCmdResult {
    static _typeName = 'UserRegisterCmdResult';
    constructor(data = {}) {
      /** @type {string} */
      this.userID = data.userID ?? '';
      /** @type {string} */
      this.token = data.token ?? '';
    }
    // ...
  };

  return ns;
})();
```

### Generated TypeScript Definitions (`acmeapp.d.ts`)

```typescript
// Code generated. DO NOT EDIT.
export declare namespace acmeappns {

  export interface IUser {
    id?: string;
    email?: string;
    name?: string;
    active?: boolean;
    createdAt?: Date | null;
  }

  export class User implements IUser {
    static readonly _typeName: string;
    constructor(properties?: IUser);
    public id?: string;
    public email?: string;
    public name?: string;
    public active?: boolean;
    public createdAt?: Date | null;
    public static verify(message: { [k: string]: any }): string | null;
    public static fromObject(object: { [k: string]: any }): User;
    public static toObject(message: User): { [k: string]: any };
    public toJSON(): string;
  }

  export interface IUserRegisterCmd {
    email?: string;
    password?: string;
    name?: string;
  }

  export class UserRegisterCmd implements IUserRegisterCmd {
    static readonly _typeName: string;
    constructor(properties?: IUserRegisterCmd);
    // ...
  }

  // ... and so on for every command + result + record
}
```

### Generated Package Utilities (`acmeapp_package.js`)

```javascript
// Code generated. DO NOT EDIT.
import { acmeappns } from './acmeapp.js';

export const PACKAGE_NAME = 'acmeappPackage';

// Factory: name → zero-value instance
export function instanceOf(compName) {
  switch (compName) {
    case 'User':             return new acmeappns.User();
    case 'UserRegisterCmd':  return new acmeappns.UserRegisterCmd();
    case 'UserRegisterCmdResult': return new acmeappns.UserRegisterCmdResult();
    // ... one case per command, result, and record
  }
  return null;
}

// Reverse: instance → name
export function nameOf(cmd) {
  if (!cmd || !cmd.constructor) return '';
  return cmd.constructor._typeName ?? '';
}
```

### Building a TypeScript Client with `@mainvec/mvep`

The `@mainvec/mvep` npm package provides the client-side runtime for sending commands to an MVEP server. Projects typically create a typed client wrapper in a `client/` directory alongside the generated code.

#### Package Adapter (`client/acmeapp_package.ts`)

Wraps the generated `acmeapp_package.js` to implement the runtime/ts `Package` interface:

```typescript
import type { Package } from '@mainvec/mvep';
import * as acmeappPkg from '../acmeapp_package.js';

export class AcmeAppPackage implements Package {
  getName(): string {
    return acmeappPkg.PACKAGE_NAME;
  }

  instanceOf(cmdName: string): unknown | undefined {
    return acmeappPkg.instanceOf(cmdName) ?? undefined;
  }

  nameOf(cmd: unknown): string {
    return acmeappPkg.nameOf(cmd);
  }
}
```

#### Typed Client (`client/acmeapp_client.ts`)

A full client with auth token management, interceptors, and typed command methods:

```typescript
import {
  newClient,
  type Client,
  type PackageClient,
  type ClientConfig,
  type ClientInterceptor,
  chainClient,
} from '@mainvec/mvep';
import { AcmeAppPackage } from './acmeapp_package';
import { acmeappns } from '../acmeapp';
import type { acmeappns as types } from '../acmeapp';

// Auth interceptor — injects token into every request
function authHeaderInterceptor(
  tokenProvider: () => string
): ClientInterceptor {
  return async (ctx, req, invoker) => {
    const token = tokenProvider();
    if (token) {
      const headers = req.headers ?? {};
      headers['auth'] = token;       // sent as 'x-mvep-auth' HTTP header
      req.headers = headers;
    }
    return invoker(ctx, req);
  };
}

export interface AcmeClientConfig {
  baseUrl: string;
  basePath?: string;
  storageType?: 'localStorage' | 'sessionStorage' | 'none';
  timeout?: number;
  headers?: Record<string, string>;
}

export class AcmeClient {
  private pkgClient: PackageClient;
  private authToken: string = '';
  private storageType: 'localStorage' | 'sessionStorage' | 'none';

  private constructor(
    pkgClient: PackageClient,
    storageType: 'localStorage' | 'sessionStorage' | 'none',
  ) {
    this.pkgClient = pkgClient;
    this.storageType = storageType;
  }

  static async create(config: AcmeClientConfig): Promise<AcmeClient> {
    const storageType = config.storageType ?? 'localStorage';
    const tokenHolder = { token: '' };

    // Restore token from storage
    if (storageType !== 'none' && typeof window !== 'undefined') {
      const storage = storageType === 'sessionStorage' ? sessionStorage : localStorage;
      tokenHolder.token = storage.getItem('acme_auth_token') ?? '';
    }

    // Create client with auth interceptor
    const interceptor = chainClient(
      authHeaderInterceptor(() => tokenHolder.token)
    );

    const mvpClient = newClient({
      baseUrl: config.baseUrl,
      basePath: config.basePath,
      timeout: config.timeout,
      headers: config.headers,
      interceptor: interceptor ?? undefined,
      fetch: typeof window !== 'undefined' ? window.fetch.bind(window) : undefined,
    });

    // Register the package
    const pkg = new AcmeAppPackage();
    const pkgClient = mvpClient.registerPackage(pkg);

    const client = new AcmeClient(pkgClient, storageType);
    client.authToken = tokenHolder.token;

    // Sync token mutations back to the holder
    const origSet = client.setAuthToken.bind(client);
    client.setAuthToken = (token: string) => {
      origSet(token);
      tokenHolder.token = token;
    };

    return client;
  }

  // Token management
  setAuthToken(token: string): void {
    this.authToken = token;
    if (this.storageType !== 'none' && typeof window !== 'undefined') {
      const storage = this.storageType === 'sessionStorage' ? sessionStorage : localStorage;
      storage.setItem('acme_auth_token', token);
    }
  }

  clearAuthToken(): void {
    this.authToken = '';
    if (this.storageType !== 'none' && typeof window !== 'undefined') {
      const storage = this.storageType === 'sessionStorage' ? sessionStorage : localStorage;
      storage.removeItem('acme_auth_token');
    }
  }

  isAuthenticated(): boolean {
    return this.authToken !== '';
  }

  // Generic command sender
  private async sendCmd<T>(cmd: unknown): Promise<T> {
    return this.pkgClient.sendCmd<T>(cmd);
  }

  // ── Typed command methods ──────────────────────────────────

  async registerUser(
    email: string, password: string, name: string
  ): Promise<types.UserRegisterCmdResult> {
    const cmd = new acmeappns.UserRegisterCmd({ email, password, name });
    const result = await this.sendCmd<types.UserRegisterCmdResult>(cmd);
    // Auto-set auth token on successful registration
    if (result.token) {
      this.setAuthToken(result.token);
    }
    return result;
  }

  async getUserProfile(
    userID: string
  ): Promise<types.UserGetProfileCmdResult> {
    const cmd = new acmeappns.UserGetProfileCmd({ userID });
    return this.sendCmd<types.UserGetProfileCmdResult>(cmd);
  }

  async updateSettings(
    userID: string, settings: Record<string, string>
  ): Promise<types.UserUpdateSettingsCmdResult> {
    const cmd = new acmeappns.UserUpdateSettingsCmd({ userID, settings });
    return this.sendCmd<types.UserUpdateSettingsCmdResult>(cmd);
  }

  async createOrder(
    customerID: string,
    items: types.IOrderItem[],
    notes?: string
  ): Promise<types.OrderCreateCmdResult> {
    const orderItems = items.map(i => new acmeappns.OrderItem(i));
    const cmd = new acmeappns.OrderCreateCmd({ customerID, items: orderItems, notes });
    return this.sendCmd<types.OrderCreateCmdResult>(cmd);
  }
}

// Convenience factory function
export async function newAcmeClient(config: AcmeClientConfig): Promise<AcmeClient> {
  return AcmeClient.create(config);
}
```

#### Barrel Exports (`client/index.ts`)

```typescript
export { AcmeClient, newAcmeClient } from './acmeapp_client';
export type { AcmeClientConfig } from './acmeapp_client';
export { AcmeAppPackage } from './acmeapp_package';
export { acmeappns } from '../acmeapp';
export type { acmeappns as AcmeAppTypes } from '../acmeapp';
```

### Using the Client (Example)

```typescript
import { newAcmeClient } from './mvepapi/js/api/client';

const client = await newAcmeClient({
  baseUrl: 'http://localhost:8080',
  basePath: '/api',
});

// Register — auto-sets auth token
const reg = await client.registerUser('alice@example.com', 's3cret', 'Alice');
console.log('User ID:', reg.userID);

// Subsequent calls include the auth token automatically
const profile = await client.getUserProfile(reg.userID);
console.log('Profile:', profile.user);

// Create an order
const order = await client.createOrder(reg.userID, [
  { productID: 'prod-1', quantity: 2, price: 29.99 },
  { productID: 'prod-2', quantity: 1, price: 49.99 },
], 'Rush delivery please');
console.log('Order:', order.orderID, 'Total:', order.total);

// Token persists across page refreshes (localStorage)
// On next page load, client restores the token automatically
```

### Client-Side Directory Convention

When adding a typed client, the recommended structure is:

```
js/
└── api/
    ├── acmeapp.js                  # ⛔ Generated
    ├── acmeapp.d.ts                # ⛔ Generated
    ├── acmeapp_package.js          # ⛔ Generated
    ├── acmeapp_package.d.ts        # ⛔ Generated
    └── client/                     # ✏️  Hand-written
        ├── acmeapp_client.ts       # Typed client with auth & command methods
        ├── acmeapp_package.ts      # Package adapter (runtime/ts Package interface)
        └── index.ts                # Barrel exports
```

The `client/` directory is **hand-written** (not generated). It wraps the generated code with project-specific concerns like auth token management, storage persistence, and typed convenience methods.

---

## Best Practices

### Field Numbers (`fnum`)

- Every field **must** have a unique `fnum` within its command or record.
- **Never reuse** a field number, even after deleting a field. Assign the next available number.
- Field numbers are **stable** — they map directly to protobuf field numbers and must not change after initial assignment.
- Keep a mental or documented record of the highest `fnum` used per command/record.

### Command Naming

- Use **PascalCase** with a `Cmd` suffix: `UserRegisterCmd`, `OrderCreateCmd`.
- CLI aliases use **snake_case**: `"alias": "register"`, `"alias": "create_order"`.

### Workflow

1. **Edit the spec** (`spec/*.json`) — add/modify commands, fields, or records.
2. **Validate** — run `mvep validate --in ./spec/your-spec.json`.
3. **Regenerate** — run `bash generate_api.sh` from the `mvepapi/` directory.
4. **Implement** — update `*_impl.go` with business logic for new commands.
5. **Protect** — add `// NOMVEP` to `*_impl.go` once you've customized it, so regeneration won't overwrite your work (legacy `// NOMVGEN` / `// NOWOGEN` markers are still honored).

### Format Choice

- **`plain`** — Simpler. Go structs with JSON tags. No protobuf dependency. Good for REST/JSON APIs and getting started.
- **`pb3`** — Full protobuf. Use when you need binary serialization, gRPC compatibility, or strict schema evolution guarantees.

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Editing generated files (not `_impl.go`) | Only edit `*_impl.go`. All other files are regenerated. |
| Reusing field numbers | Always use the next available `fnum`. Never reuse deleted field numbers. |
| Duplicate `fnum` within a command/record | Each `fnum` must be unique within its parent. |
| Missing `$ref` for `recRef` fields | `recRef` fields require `"$ref": "#/recordsDefs/RecordName"`. |
| Case sensitivity in command names | Command names are PascalCase and case-sensitive. |
| Running generate without validating | Always `mvep validate` first to catch spec errors before generating. |
| Forgetting `NOMVEP` on customized files | Add `// NOMVEP` as the first line of any generated file you've customized (legacy `// NOMVGEN` / `// NOWOGEN` still honored). |
| Wrong `go_package` path | Must match your actual Go module path. |
| Naming a command or group `mvep` | `mvep` is reserved for the generated CLI's framework namespace (`svc mvep exec`/`send`/`list`/`describe`). Generation fails with a reserved-name error. |

---

## For AI Agents — Quick Reference

> This section is structured for AI coding agents operating on projects that use MVEP. It can be embedded in a project's `mvepapi/README.md` or `AGENT.md`.

Preferred toolkit implementation in this repository is `mvepapi/cmd/mvep`.

### Identifying an MVEP Project

A project uses MVEP if it has a `mvepapi/` directory containing:
- `spec/*.json` or `spec/*.jsonc` — MVEP specification file(s)
- `generate_api.sh` — Code generation script
- `go/` and/or `js/` — Generated output directories

### Key Rules

1. **NEVER edit generated files** except `*_impl.go`. Look for the header comment `// code generated` to identify generated files.
2. **ONLY edit `*_impl.go`** for command implementations. This is the single file where business logic lives.
3. **Preserve field numbers** — when adding fields, use the next `fnum` after the highest existing one. Never reuse or change existing field numbers.
4. **Regenerate after spec changes** — run `bash generate_api.sh` from the `mvepapi/` directory.
5. **Validate before generating** — run `mvep validate --in ./spec/<name>-spec.json` first.

### Adding a New Command

1. Open the spec file (`mvepapi/spec/*.json`).
2. Add the command under `"commands"`:
   ```json
   "NewCommandCmd": {
     "title": "Description",
     "alias": "new_command",
     "fields": {
       "fieldName": { "fnum": 1, "type": "string" }
     },
     "resultFields": {
       "resultField": { "fnum": 1, "type": "string" }
     }
   }
   ```
3. Regenerate: `cd mvepapi && bash generate_api.sh`
4. Implement in `*_impl.go`: fill in the generated `runNewCommandCmd` stub.

### Adding a Field to an Existing Command

1. Open the spec file.
2. Find the command, check the highest `fnum` in its `fields` or `resultFields`.
3. Add the new field with `fnum` = highest + 1.
4. Regenerate.

### Adding a Record Definition

1. Open the spec file.
2. Add under `"recordsDefs"`:
   ```json
   "MyRecord": {
     "name": "MyRecord",
     "title": "Description",
     "fields": {
       "fieldName": { "fnum": 1, "type": "string" }
     }
   }
   ```
3. Reference it in commands with `"type": "recRef", "$ref": "#/recordsDefs/MyRecord"`.
4. Regenerate.

### File Quick-Reference

| Pattern | Purpose | Edit? |
|---------|---------|-------|
| `spec/*-spec.json` | MVEP specification | Yes — source of truth |
| `generate_api.sh` | Regeneration script | Yes — if paths change |
| `go/*_impl.go` | Command implementations | **Yes** — your business logic |
| `go/*_commands.go` | Command runner factory | No |
| `go/api/*_package.go` | Handler types, dispatch | No |
| `go/api/*.plain.go` | Go struct definitions | No |
| `go/api/*.proto` | Protobuf definitions | No |
| `go/cmd/*/` | CLI entry point | No |
| `js/api/*` | JS/TS classes and types | No |
| `js/api/client/*` | Typed TS client wrapper | **Yes** — hand-written |

### Condensed Template for Project README

Projects can include this in their `mvepapi/README.md`:

```markdown
## MVEP API

This project uses the [Mainvec Platform](https://github.com/mainvec/mvep/toolkit) (MVEP) for API generation.

### Regenerate API Code

    cd mvepapi && bash generate_api.sh

### Spec Location

    mvepapi/spec/<name>-spec.json

### Implementation

Business logic lives in `mvepapi/go/<name>_impl.go`. Do not edit other generated files.
```
