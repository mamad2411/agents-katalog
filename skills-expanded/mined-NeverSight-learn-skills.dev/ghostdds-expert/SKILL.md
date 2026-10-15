---
name: ghostdds-expert
description: 'ghostDDS is a C++17 application that reads RTI Connext DDS recordings from SQLite databases and provides controllable playback with filtering, QoS visualization, type decoding, and multiple front-end options. Use when asked about ghostDDS architecture, storage layer, playback engine, CDR decoding (XCDR1, XCDR2/D_CDR2, type evolution, bulk decode), type system, XML type parsing, filtering, QoS inspection, REST API, web server, WebSocket streaming, SSE events, client-side CDR decoding, JavaScript protocol decoders, native GUI, CLI subcommands, recording databases, dat files, metadata.db, discovery.db, CMake build, Debian packaging, static libraries (ghostdds_playback, ghostdds_web), examples, or testing. Explains at any level from non-technical overview to deep technical detail.'
license: 'Proprietary - Fortescue Ltd.'
compatibility: 'C++17, CMake 3.18+, RTK Suite, GCC 10+'
metadata:
  project: ghostDDS
  organization: Fortescue Ltd (FMG Autonomy)
  language: English
  expertise-level: expert
  focus-areas: DDS recording playback, SQLite storage, CDR decoding (XCDR1/XCDR2), type system, QoS, REST API, WebSocket, client-side decoding, filtering, GUI
---

# ghostDDS Expert

ghostDDS reads RTI Connext DDS recordings from SQLite databases and provides controllable playback with filtering, QoS visualization, type decoding, and multiple front-end options. Use this skill to answer questions about ghostDDS at any level.

## When to Use This Skill

* Questions about ghostDDS architecture, design philosophy, or how components connect
* How to build, test, package, or install ghostDDS
* How the storage layer reads RTI recording directories (metadata.db, discovery.db, .dat files)
* How the playback engine works (PlaybackController, PlaybackClock, DataDispatcher)
* Forward and reverse playback, speed control, bounded playback (playFor/playUntil)
* Filtering (topic wildcards, domain IDs, entity-based, type-based, composite)
* QoS inspection, compatibility checking, and troubleshooting mismatches
* Type system: loading RTI XML types, directory-tree loading, constant resolution
* CDR decoding: XCDR1, XCDR2 (D_CDR2 delimited, Plain CDR2), type evolution, bulk numeric decode, enum index lookup, partial decoding, error reporting
* REST API endpoints, JSON responses, SSE event streaming, WebSocket binary streaming
* Web front-end (static HTML/CSS/JS), JavaScript protocol decoders (`ghostdds-cdr.js`, `ghostdds-decoder.js`, `ghostdds-client.js`), client-side CDR decoding, and native GUI (ImGui + SDL2 + OpenGL3)
* CLI subcommands: `info`, `play`, `headless`, `gui`
* Static libraries (`libghostdds_playback.a`, `libghostdds_web.a`) and `find_package(ghostdds_playback)` / `find_package(ghostdds_web)` usage
* Debian packaging (`ghostdds`, `libghostdds-playback-dev`, `libghostdds-web-dev`, `ghostdds-gui`)
* Examples (01–17) and diagnostic utilities
* Code review or modifications to any ghostDDS module
* Assessing whether proposed changes align with the project's design philosophy

## Communication Style

### Adaptive Detail Level

Match the depth of the answer to what the user is actually asking for:

* **Beginner / "what is"**: Plain-language explanation of purpose and relevance. No jargon. One or two sentences may be enough.
* **Overview / "how does"**: Architecture, components, how they connect. Keep it concise, a short paragraph or diagram.
* **Technical / "how do I"**: Specific APIs, data flows, configuration, commands. Actionable and concrete.
* **Deep technical / "explain in detail"**: Code structure, protocol internals, edge cases. Go deep ONLY when explicitly asked.

**Default to concise.** Start with the simplest useful answer. If the user wants more depth, they will ask. Do not front-load every answer with exhaustive detail.

### Philosophy and Intent Awareness

ghostDDS is designed around several core principles:

* **Layered architecture** — Clean separation between storage, playback engine, filter/QoS, type system, and presentation. Lower layers have no knowledge of upper layers. The playback engine is a reusable library (`ghostdds_playback`), not coupled to any specific front-end.
* **Facade pattern for storage** — `RecordingDatabase` composes `MetadataParser`, `DatFileReader`, and `DiscoveryReader` into a single API. Consumers never interact with individual readers directly.
* **Observer pattern for dispatch** — `DataDispatcher` decouples sample production (playback loop) from consumption (web server, GUI, CLI). Subscribers register callbacks; the dispatcher invokes them synchronously.
* **Thread safety by design** — All public APIs on `PlaybackController`, `PlaybackClock`, `DataDispatcher`, and filter classes are thread-safe. The playback loop runs on a dedicated thread; controls are called from any thread.
* **Graceful degradation** — The CDR decoder returns partial results with `_error` keys rather than throwing. Type evolution fills missing fields with `null`. Unresolvable XML type references are collected as warnings, not fatal errors. XCDR2 delimited mode gracefully handles payload exhaustion mid-sequence.
* **Composable filters** — Filters are independent, stackable, and dynamically modifiable during playback. `CompositeFilter` applies AND logic across all filter types.
* **Additive type loading** — The `TypeRegistry` accumulates types across multiple `loadFromXml()` and `loadFromDirectory()` calls. Cross-file type references resolve automatically via multi-pass loading (up to 3 additional re-parse passes for deep dependency chains).

When advising on changes, additions, or modifications:

* **Assess suitability** — Advise whether a proposed change aligns with or diverges from these principles. Clearly explain any tension.
* **Recommend approach** — When multiple approaches are possible, recommend the one most consistent with the layered architecture and existing patterns.
* **Carry out changes consistently** — When making modifications, maintain the existing separation of concerns, thread-safety guarantees, and error-handling philosophy.

**Pragmatism over tradition.** These guidelines exist to maintain coherence, not to enforce convention for its own sake. When breaking from the established structure would yield obvious and significant gains, say so and recommend the better path.

### Suggesting Follow-Ups

After answering, suggest 1–3 related topics the user might want to explore next. Frame these as natural follow-on questions. Only suggest follow-ups that are genuinely related to the question asked.

### Knowledge Boundaries

Be honest about limits. If asked about something outside the documented scope:

* Say so clearly
* Point to where the answer might be found (RTI Connext DDS documentation, RTK Suite docs, etc.)
* Do not speculate or fabricate

## System Overview

### What ghostDDS Does

1. **Opens RTI Recording Service directories** — Parses `metadata.db`, `.dat` files, and `discovery.db` to provide a unified query API over recorded DDS data
2. **Provides controllable playback** — Forward/reverse replay with play/pause, seek, step, speed control (0.1x–10.0x), and bounded playback windows with completion callbacks
3. **Filters recorded data** — Topic wildcard matching, domain filtering, entity-based filtering, type-based filtering, and composable filter chains — all dynamically modifiable during playback
4. **Inspects QoS profiles** — Stores and retrieves QoS profiles from discovery data, checks publisher/subscriber compatibility using DDS rules
5. **Decodes CDR payloads** — Loads RTI XML type definitions (single files or directory trees), maps topics to types, and decodes raw CDR bytes into structured JSON with type evolution support. Supports XCDR1 and XCDR2 (D_CDR2 delimited, Plain CDR2). Includes bulk decode fast paths for numeric sequences/arrays and O(1) enum ordinal lookup.
6. **Exposes multiple front-ends** — CLI (info/play/headless), REST API + SSE + WebSocket web server, static web front-end with client-side CDR decoding, and native ImGui GUI

### Architecture Diagram

```text
┌────────────────────────────────────────────────────────┐
│                     Presentation Layer                 │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │ Native   │  │ Web Server   │  │ Headless       │   │
│  │ GUI      │  │ (Crow)       │  │ Service Mode   │   │
│  │ (ImGui)  │  │ + SSE + WS   │  │                │   │
│  └────┬─────┘  └──────┬───────┘  └───────┬────────┘   │
│       │               │                  │            │
├───────┴───────────────┴──────────────────┴────────────┤
│                   Filter / QoS Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  ┌──────────┐  │
│  │ Topic &  │  │ Entity   │  │ Type │  │ QoS      │  │
│  │ Domain   │  │ Filter   │  │Filter│  │ Inspector│  │
│  └──────────┘  └──────────┘  └──────┘  └──────────┘  │
├───────────────────────────────────────────────────────┤
│                    Playback Engine                    │
│  ┌──────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Playback     │  │ Playback │  │ Data           │  │
│  │ Controller   │  │ Clock    │  │ Dispatcher     │  │
│  │ (state       │  │ (timing  │  │ (observer      │  │
│  │  machine)    │  │  mapping)│  │  pattern)      │  │
│  └──────────────┘  └──────────┘  └────────────────┘  │
├───────────────────────────────────────────────────────┤
│                     Type System                      │
│  ┌──────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Type         │  │ XML Type │  │ CDR            │  │
│  │ Registry     │  │ Parser   │  │ Decoder        │  │
│  └──────────────┘  └──────────┘  └────────────────┘  │
├───────────────────────────────────────────────────────┤
│                    Storage Layer                      │
│  ┌──────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Recording    │  │ Metadata │  │ Discovery      │  │
│  │ Database     │  │ Parser   │  │ Reader         │  │
│  │ (facade)     │  │          │  │                │  │
│  └──────┬───────┘  └──────────┘  └────────────────┘  │
│  ┌──────┴───────┐                                    │
│  │ Dat File     │  SQLiteCpp → RTI Recording DBs     │
│  │ Reader       │                                    │
│  └──────────────┘                                    │
└───────────────────────────────────────────────────────┘
```

### Technology Stack

* **Language:** C++17 (GCC 10)
* **Build:** CMake 3.18 with RTK Suite macros
* **Database:** SQLiteCpp (system package)
* **Formatting:** fmt (system package)
* **JSON encoding:** Custom streaming `JsonWriter` (header-only, no external dependency)
* **JSON decoding:** nlohmann-json (system package, web layer only)
* **HTTP Server:** Crow v1.2.0 (via CMake FetchContent) with WebSocket support
* **XML Parsing:** pugixml (FetchContent, v1.14)
* **GUI:** ImGui + SDL2 + OpenGL3 (system packages, optional)
* **Testing:** Google Test / Google Mock via RTK Suite
* **Documentation:** MkDocs with Material theme
* **Packaging:** Debian (dpkg-buildpackage)

### Key Dependencies

| Dependency | Source | Purpose |
|---|---|---|
| SQLiteCpp | System (`libsqlitecpp-dev`) | SQLite database access for .dat, metadata.db, discovery.db |
| fmt | System (`libfmt-dev`) | String formatting and logging |
| nlohmann-json | System (`nlohmann-json3-dev`) | JSON parsing for incoming REST request bodies (web layer only) |
| Crow | FetchContent (v1.2.0) | HTTP REST server with WebSocket and SSE support |
| pugixml | FetchContent (v1.14) | XML parsing for RTI type definitions |
| SDL2 | System (optional) | Window management for native GUI |
| ImGui | System (optional) | Immediate-mode GUI framework |
| GLEW + OpenGL | System (optional) | GPU rendering for GUI |
| RTK Suite | `find_package(rtk_suite)` | Build environment checks, static analysis, test coverage, Google Test integration |

### Deployment

ghostDDS produces four Debian packages:

| Package | Contents |
|---|---|
| `ghostdds` | CLI binary (`/usr/bin/ghostdds`), static web assets, shared data, MkDocs site |
| `libghostdds-playback-dev` | Static library (`libghostdds_playback.a`), public headers (`include/ghostdds/`), CMake config |
| `libghostdds-web-dev` | Static library (`libghostdds_web.a`), web headers, CMake config, JavaScript protocol decoders |
| `ghostdds-gui` | Native GUI binary (`/usr/bin/ghostdds_gui`), depends on `ghostdds` |

### Static Library

The core playback engine is packaged as `libghostdds_playback.a` for use by other applications:

```cmake
find_package(ghostdds_playback REQUIRED)
target_link_libraries(my_app PRIVATE ghostdds::ghostdds_playback)
```

The library includes storage, playback, filter, QoS, and type system modules. It does NOT include the web server, GUI, or CLI — those are application-level concerns.

The web server layer is packaged as `libghostdds_web.a`:

```cmake
find_package(ghostdds_web REQUIRED)
target_link_libraries(my_server PRIVATE ghostdds::ghostdds_web)
```

The web library includes the Crow HTTP server, WebSocket streaming, SSE, JSON serialisation, and type schema serialiser. It also ships reusable JavaScript protocol decoders (`ghostdds-cdr.js`, `ghostdds-decoder.js`, `ghostdds-client.js`) for building custom web front-ends with client-side CDR decoding.

## References

* [Core Stacks and Components](./references/core-stacks-and-components.md) — Detailed documentation of every module
* [Codebase Structure](./references/codebase-structure.md) — Repository layout, file inventory, and build targets
* [Build, Test, and Deploy](./references/build-test-and-deploy.md) — Build commands, testing, packaging, and installation
* [Troubleshooting](./references/troubleshooting.md) — Common issues and debugging approaches
* [Glossary and Domain Concepts](./references/glossary-and-domain-concepts.md) — DDS terminology, RTI-specific concepts, and project vocabulary
