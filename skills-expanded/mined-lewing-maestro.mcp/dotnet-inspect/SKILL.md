---
name: dotnet-inspect
description: Query .NET APIs across NuGet packages, platform libraries, and local files. Search for types, list API surfaces, compare versions, find extension methods and implementors. Use whenever you need to answer questions about .NET library contents.
confidence: low
source: external (richlander/dotnet-inspect)
---

# dotnet-inspect

Query .NET library APIs — the same commands work across NuGet packages, platform libraries (System.*, Microsoft.AspNetCore.*), and local .dll/.nupkg files.

## When to Use This Skill

- **"What types are in this package?"** — `type` discovers types (terse), `find` searches by pattern
- **"What's the API surface?"** — `type` for discovery, `member` for detailed inspection (docs on)
- **"What changed between versions?"** — `diff` classifies breaking/additive changes
- **"What extends this type?"** — `extensions` finds extension methods/properties
- **"What implements this interface?"** — `implements` finds concrete types
- **"What does this type depend on?"** — `depends` walks the type hierarchy upward
- **"What version/metadata does this have?"** — `package` and `library` inspect metadata

## Examples by Task

### Discover types

```bash
dnx dotnet-inspect -y -- type --package System.Text.Json                   # all types in package
dnx dotnet-inspect -y -- type -t "*Serializer*" --package System.Text.Json # filter by glob
```

### Inspect members

```bash
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json         # members with docs
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json -m Serialize  # filter to member
```

### Search for types

```bash
dnx dotnet-inspect -y -- find "*Handler*" --package System.CommandLine
dnx dotnet-inspect -y -- find "*Logger*"
```

### Compare versions (migrations)

```bash
dnx dotnet-inspect -y -- diff --package System.Text.Json@9.0.0..10.0.0 --breaking
dnx dotnet-inspect -y -- diff JsonSerializer --package System.Text.Json@9.0.0..10.0.0
```

### Find extensions, implementors, and dependencies

```bash
dnx dotnet-inspect -y -- extensions HttpClient
dnx dotnet-inspect -y -- implements Stream
dnx dotnet-inspect -y -- depends 'INumber<TSelf>'
```

### Inspect packages

```bash
dnx dotnet-inspect -y -- package System.Text.Json                # metadata, latest version
dnx dotnet-inspect -y -- package System.Text.Json --versions     # available versions
dnx dotnet-inspect -y -- package search "Azure.AI"               # search NuGet for packages
```

## Command Reference

| Command | Purpose |
| ------- | ------- |
| `type` | **Discover types** — terse output, no docs, use `--shape` for hierarchy |
| `member` | **Inspect members** — docs on by default, supports dotted syntax (`-m Type.Member`) |
| `find` | Search for types by glob pattern across any scope |
| `diff` | Compare API surfaces between versions — breaking/additive classification |
| `extensions` | Find extension methods/properties for a type |
| `implements` | Find types implementing an interface or extending a base class |
| `depends` | Walk the type dependency hierarchy upward (interfaces, base classes) |
| `package` | Package metadata, files, versions, dependencies, `search` for NuGet discovery |
| `library` | Library metadata, symbols, references, dependencies |

## Key Syntax

- **Generic types** need quotes: `'Option<T>'`, `'IEnumerable<T>'`
- **`type` uses `-t`** for type filtering, **`member` uses `-m`** for member filtering
- **Dotted syntax** for `member`: `-m JsonSerializer.Deserialize`
- **Diff ranges** use `..`: `--package System.Text.Json@9.0.0..10.0.0`
- Always use `-y` and `--` to prevent interactive prompts: `dnx dotnet-inspect -y -- <command>`

## Project-Specific Usage

Our PCS client NuGet package:
```bash
dnx dotnet-inspect -y -- type --package Microsoft.DotNet.ProductConstructionService.Client
dnx dotnet-inspect -y -- member ISubscriptions --package Microsoft.DotNet.ProductConstructionService.Client
dnx dotnet-inspect -y -- member TriggerSubscriptionAsync --package Microsoft.DotNet.ProductConstructionService.Client
```
