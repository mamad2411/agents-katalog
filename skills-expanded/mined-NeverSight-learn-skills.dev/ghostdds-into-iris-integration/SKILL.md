---
name: ghostdds-into-iris-integration
description: "Expert in integrating GhostDDS into an IRIS-like web visualisation platform to enable playback of RTI Connext DDS recording databases without any RTI runtime or licence, while preserving existing live DDS mode. Use when asked about integrating GhostDDS, adding recording playback to IRIS, removing RTI replay dependency, creating a DataBridge abstraction, adding playback endpoints, migrating replay frontend to unified API, or troubleshooting GhostDDS integration issues."
---

# GhostDDS Integration into IRIS

An expert skill for integrating [GhostDDS](https://github.com/your-org/ghostdds) — a C++17 library that reads RTI Recording Service SQLite databases, decodes CDR payloads to JSON using XML type definitions, and provides controllable playback — into the IRIS web platform.

## Purpose

This skill documents the **complete, repeatable process** of integrating GhostDDS into an IRIS-like codebase to achieve:

1. **Recording playback without RTI** — open and play back `.db` recordings with zero RTI software, libraries, or licences
2. **Transparent user experience** — all frontend pages (visualiser, diagnostics, inspector, plotter, replay, monitoring) work identically regardless of data source
3. **Dual-mode operation** — the same `iris_web_service` binary supports both live DDS (via ZMQ bridges) and recording playback (via GhostDDS), selected by configuration
4. **Single-binary playback deployment** — for playback mode, only `iris_web_service` + NGINX are needed

## When to Use This Skill

* Integrating GhostDDS into an IRIS (or IRIS-like) codebase from scratch
* Re-applying the integration after upstream merges or rebases
* Troubleshooting build failures, CDR decode issues, or frontend data flow problems
* Understanding the architecture choices and their rationale
* Extending the integration (e.g., adding new playback features, supporting new topic types)

## GhostDDS Repository Documentation

The GhostDDS repository (`git@github.com:fmg-andrewlaws/ghostdds.git`) contains detailed documentation including examples and example code. **Refer to it during integration** for:

- **Best practices** — idiomatic usage patterns for the playback API, type registry, CDR decoder
- **Overall intent and goals** — what GhostDDS is designed to achieve and the problems it solves
- **Expected usage patterns** — how applications are expected to consume `libghostdds_playback` (callback-based dispatch, type resolution, session lifecycle management)
- **Example applications** — working code demonstrating correct integration

This documentation is the authoritative source for how GhostDDS is meant to be used. When in doubt about API usage, dispatch patterns, or lifecycle management, consult the GhostDDS docs and examples rather than guessing or copying PoC shortcuts.

## What Changed (Summary)

The integration touches these areas:

| Area | Nature of Change |
|------|-----------------|
| Top-level `CMakeLists.txt` | Add GhostDDS via FetchContent; RTI FindModule discovery; -fPIC settings; type XML install |
| `backend/iris_web_service/CMakeLists.txt` | New source files; link `ghostdds_playback`; conditional Crow find |
| `backend/iris_web_service/include/` | New: `data_bridge.hpp`, `playback_bridge.hpp`, `playback_endpoint_handler.hpp` |
| `backend/iris_web_service/src/` | New: `playback_bridge.cpp`, `playback_endpoint_handler.cpp`; modified: `main.cpp`, `web_server.cpp`, `http_endpoint_handler.cpp`, `websocket_stream_handler.cpp` |
| `backend/iris_web_service/include/zmq_client.hpp` | `MultiZMQBridge` extends `DataBridge`; `CachedState` moved to `data_bridge.hpp` |
| `backend/iris_web_service/config/` | New: `iris_web_service_playback_config.json`, `iris_web_service_playback_config_dev.json` |
| `frontend/replay.html` | Complete rewrite targeting unified `/api/recording/*` + `/api/playback/*` endpoints |
| `frontend/static/scripts/replay.js` | Complete rewrite: new API calls, removed old replay-api references |
| `frontend/static/scripts/visualiser.js` | Code reformatting (no functional changes) |
| `config/nginx_iris.conf` | Remove `/replay-api/` proxy block |
| `launch_iris.sh` | Minor port variable cleanup |
| `types/` directory | 808 new XML type definition files gathered from `data_types_provider/` |
| `docs/` | Updated architecture, getting started, quick start, troubleshooting |
| Top-level `CMakeLists.txt` | `iris_replay_service` subdirectory commented out |
| `.devcontainer.json` | Dev container definition with required apt packages |

## Critical Principles

These principles must be followed throughout the integration:

1. **Incremental, testable steps.** Every phase ends with a concrete validation gate. Do not proceed to the next phase until the current phase's gate passes. This prevents problems from compounding into untangleable messes.

2. **Test early, test often.** After each file modification or addition, rebuild and verify. Add targeted tests where possible — even manual curl commands or browser checks count. The cost of finding a bug immediately is 10× less than finding it three phases later.

3. **Documentation travels with code.** When you modify behaviour, update the relevant documentation in the same commit or work session. Do not defer documentation to a "cleanup phase" — it will be forgotten or inconsistent. This includes: `docs/technical_architecture.md`, `docs/quick_start.md`, `docs/getting_started.md`, `docs/troubleshooting.md`, and the README.

4. **Preserve live mode.** Every change must be verified against live mode (ZMQ bridge) as well as playback mode. The DataBridge abstraction exists specifically to prevent regressions — but only if you test both paths.

5. **One concern per commit.** Keep commits focused: build system changes separate from interface changes separate from implementation. This makes bisecting and reverting feasible if something goes wrong.

## Work Order (Phase Sequence)

The phases in `references/integration-steps.md` **must be followed in order**. Each phase builds on the previous one and has a defined validation gate. Skipping ahead causes cascading failures that are expensive to diagnose.

```
Phase 1: Build System Integration
    → Gate: Project compiles with GhostDDS linked (even if unused)
Phase 2: DataBridge Abstraction Layer
    → Gate: Existing live mode still works with refactored interfaces
Phase 3: PlaybackBridge Implementation
    → Gate: Can open a recording and decode samples (unit/manual test)
Phase 4: Playback REST Endpoints
    → Gate: curl commands exercise all endpoints successfully
Phase 5: Main Entry Point — Mode Selection
    → Gate: Binary starts in both modes from config
Phase 6: Configuration Files
    → Gate: Playback mode serves the frontend
Phase 7: Types Directory
    → Gate: TypeRegistry loads all XMLs without errors
Phase 8: NGINX Configuration
    → Gate: Proxy routes work for both modes
Phase 9: Frontend — Replay Page Rewrite
    → Gate: Full UI workflow: browse → open → play → seek → pause
Phase 10: Monitoring Page Support
    → Gate: Monitoring page loads and shows recording data
Phase 11: Development Container
    → Gate: Fresh container builds from scratch
Phase 12: Build & Test
    → Gate: Full end-to-end workflow passes; no warnings with -Werror
```

**Why this order matters:**

- Phases 1-2 are foundational — they establish the abstraction layer without breaking anything
- Phase 2 is the highest-risk refactor (touching every existing handler); completing it first means the rest is additive
- Phases 3-5 are the core implementation — testable in isolation via curl before the frontend exists
- Phase 9 depends on phases 4-5 being stable (the frontend calls those endpoints)
- Phase 12 is the final integration verification — a clean build followed by end-to-end testing. Documentation updates happen continuously throughout (not deferred to the end).

## Detail Levels

This skill provides information at three levels:

1. **Quick reference** — checklist of files to create/modify (this SKILL.md)
2. **Step-by-step guide** — detailed instructions in `references/integration-steps.md`
3. **Architecture rationale** — design decisions and alternatives in `references/architecture-decisions.md`

## Key Architecture Pattern: DataBridge Abstraction

The central design pattern is a **polymorphic DataBridge interface** that both the existing ZMQ bridge (live mode) and the new PlaybackBridge (playback mode) implement:

```cpp
class DataBridge {
    virtual void start() = 0;
    virtual void stop() = 0;
    virtual std::shared_ptr<MessageQueue> subscribeTopic(...) = 0;
    virtual void unsubscribeTopic(...) = 0;
    virtual nlohmann::json latestState(...) const = 0;
    virtual nlohmann::json allLatestStates(...) const = 0;
    virtual nlohmann::json stats() const = 0;
    virtual std::optional<CachedState> waitForUpdate(...) const = 0;
    virtual std::uint64_t currentVersion(...) const = 0;
};
```

This interface is the contract between the data source and the web service. By coding the web server, HTTP endpoint handler, and WebSocket stream handler against `DataBridge*`, the frontend receives data identically regardless of whether it's live or recorded.

## References

* [references/integration-steps.md](references/integration-steps.md) — Complete step-by-step integration checklist
* [references/architecture-decisions.md](references/architecture-decisions.md) — Design rationale, alternatives considered, pitfalls
* [references/api-reference.md](references/api-reference.md) — REST API endpoints added for playback
* [references/build-configuration.md](references/build-configuration.md) — CMake, devcontainer, and dependency details
* [references/frontend-changes.md](references/frontend-changes.md) — Frontend migration guide
* [references/troubleshooting.md](references/troubleshooting.md) — Common problems and solutions
