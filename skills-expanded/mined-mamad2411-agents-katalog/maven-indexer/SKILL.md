---
name: maven-indexer
description: Query the local Maven/Gradle artifact index from the terminal. Use when you see an import but cannot find the class definition in the workspace (it likely comes from a compiled internal library), when you need to read the actual implementation of an internal or non-well-known library, or when you need to find which artifact contains a class, discover implementations of an interface, or inspect proto/resource files inside JARs. Do not use for well-known standard libraries (java.util, Spring core, etc.) that the AI already knows.
---

# Maven Indexer

Use `maven-indexer-cli` to search and inspect Java classes, artifacts, and resources from your local Maven/Gradle cache.

## When to activate

**Use this skill when:**
- You see an import (e.g. `com.company.util.Helper`) but cannot find the definition in the workspace — it likely comes from a compiled internal library
- You need to read the actual implementation of an internal or non-well-known library ("Don't guess what the internal library does — read the code")
- You need to find which artifact contains a given class
- You need method signatures, Javadocs, or full source code of a dependency class
- You need to find implementations of an interface or subclasses of a base class (e.g. SPI implementations)
- You need to locate proto files or other resources embedded in JARs

**Skip when:**
- The class is from the standard Java library (`java.util`, `java.io`, etc.) or a well-known public library the AI already knows well
- The source is already present in the current workspace

## Check index first

If the index might be empty or stale, build it first:

```bash
# Quick scan — one best version per artifact (fast, recommended)
maven-indexer-cli refresh-index

# Full scan — all versions of all artifacts
maven-indexer-cli refresh-index --full
```

## Commands

### `search-classes` — Find which artifact contains a class

Essential when you see an import but cannot find the definition. Do not assume the source is local just because the code compiles.

```bash
maven-indexer-cli search-classes <className>
# Examples:
maven-indexer-cli search-classes StringUtils
maven-indexer-cli search-classes com.company.util.Helper
maven-indexer-cli search-classes JsonToXml          # keyword search also works
```

### `get-class` — Read the actual implementation

Use instead of guessing. Prefers source JARs, falls back to decompilation.

```bash
# Method signatures (default)
maven-indexer-cli get-class <className>

# Javadocs + method signatures
maven-indexer-cli get-class <className> --type docs

# Full source code
maven-indexer-cli get-class <className> --type source

# From a specific artifact version
maven-indexer-cli get-class <className> --coordinate groupId:artifactId:version
```

### `search-artifacts` — Find artifacts by coordinate or keyword

```bash
maven-indexer-cli search-artifacts <query>
# Examples:
maven-indexer-cli search-artifacts guava
maven-indexer-cli search-artifacts com.google.guava
```

### `search-implementations` — Find SPI implementations and subclasses

Particularly useful for finding implementations of SPIs or base classes within internal company libraries.

```bash
maven-indexer-cli search-implementations <className>
# Examples:
maven-indexer-cli search-implementations java.util.List
maven-indexer-cli search-implementations com.example.spi.Handler
```

### `search-resources` — Find proto files and other JAR resources

```bash
maven-indexer-cli search-resources <pattern>
# Examples:
maven-indexer-cli search-resources .proto
maven-indexer-cli search-resources log4j.xml
```

## Output

All commands support `--json` for structured output:

```bash
maven-indexer-cli search-classes ImmutableList --json
maven-indexer-cli get-class com.google.common.collect.ImmutableList --json
```

> If `maven-indexer-cli` is not found, install it: `npm install -g maven-indexer-cli`
