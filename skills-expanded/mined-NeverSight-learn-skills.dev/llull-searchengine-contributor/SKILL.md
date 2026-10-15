---
name: llull-searchengine-contributor
description: >-
  Guide for contributing to the Llull search engine project. Use this skill
  when the user wants to create data source connectors (Firestore, Postgres,
  MySQL, MongoDB, or custom), build frontend components (React, Flutter), or
  contribute to the Llull search engine. Also triggers on "contribute to
  llull", "llull data source", "llull frontend", "llull component", "extend
  llull", "llull plugin".
---

# Llull Search Engine Contributor

This skill guides you through contributing to the [Llull](https://github.com/2mes4/llull) search engine project. Llull is an Algolia-like search engine for databases, designed to run alongside Firestore, PostgreSQL, MySQL, or MongoDB.

## Project Overview

```
llull/
├── cmd/server/main.go              Entry point
├── internal/
│   ├── engine/                     Core search engine (trie, ranking, fuzzy)
│   ├── api/                        HTTP handlers (chi router)
│   ├── worker/                     Buffered worker pool
│   ├── datasource/                 Data source abstraction layer
│   └── seed/                       Seed data generator
├── data-sources/firestore/         Firebase Extension (push model)
├── data-sources/postgres/          PostgreSQL connector docs
├── data-sources/mysql/             MySQL connector docs
├── data-sources/mongodb/           MongoDB connector docs
├── skills/                         AI skills for contributors
├── ui-components/react/            React component library
├── ui-components/flutter/          Flutter widget library
├── web/                            Built-in Google-style search UI
├── deploy/                         Docker + Kubernetes + docs
└── AGENTS.md                       Agent instructions
```

## Contributing Data Sources

### The Connector Interface

Every data source implements `internal/datasource/datasource.go`:

```go
type Connector interface {
    Name() string
    Connect(ctx context.Context, cfg Config) error
    Sync(ctx context.Context, callback func(Event)) error
    Close() error
}
```

### Step-by-step: Creating a new connector

1. **Create the package**: `internal/datasource/<name>/<name>.go`

2. **Implement `Connector`**:
```go
package <name>
import "github.com/2mes4/llull/internal/datasource"

type Connector struct {
    cfg datasource.Config
}
func (c *Connector) Name() string { return "<name>" }
func (c *Connector) Connect(ctx context.Context, cfg datasource.Config) error {
    c.cfg = cfg
    if cfg.Connection == "" { return fmt.Errorf("<name>: connection required") }
    // establish connection
    return nil
}
func (c *Connector) Sync(ctx context.Context, callback func(datasource.Event)) error {
    for { select {
        case <-ctx.Done(): return ctx.Err()
        case <-time.After(interval):
            // detect changes, emit Events via callback
    }}
}
func (c *Connector) Close() error {
    // release resources
    return nil
}
```

3. **Add database driver** to imports, run `go mod tidy`.

4. **Create docs**: `data-sources/<name>/README.md`

5. **Write tests**: `internal/datasource/<name>/<name>_test.go`

See existing connectors for reference: `internal/datasource/postgres/`, `internal/datasource/mysql/`, `data-sources/firestore/`.

## Contributing Frontend Components

### React

Install from npm:

```bash
npm install llull-search-components
```

Create a component:

```jsx
import { useLlullSearch } from 'llull-search-components';

function MySearch() {
  const { results, search, status } = useLlullSearch({ host: 'http://localhost:8180' });
  return <div>
    <input onChange={e => search(e.target.value)} />
    {results.map(r => <div key={r.id}>{r.score}</div>)}
  </div>;
}
```

### Flutter

Add to pubspec.yaml:

```yaml
dependencies:
  llull_search_components: ^0.1.0
```

Create a widget:

```dart
import 'package:llull_search_components/llull_search_components.dart';

LlullSearchDropdown(
  host: 'http://localhost:8180',
  onSelected: (result) => print(result.id),
)
```

## Build & Test Commands

```bash
# Go
go test ./... -v -race
go build ./...

# React (from ui-components/react)
npm install
npm run build

# Flutter (from ui-components/flutter)
flutter pub get
flutter test
```

## Code Style

- Go: no comments unless requested, follow existing patterns, `sync.RWMutex` for concurrency
- React: functional components with hooks, TypeScript, no class components
- Flutter: widgets with `const` constructors, use `riverpod` or `provider` for state
- All code and docs in English
