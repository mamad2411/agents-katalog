---
name: unity-mcp-game-development
description: Build, inspect, debug, test, and ship Unity 2D or 3D projects, using Unity MCP to control the Editor when connected. Covers Unity 6 and version-aware workflows, Unity Assistant MCP setup and security, scenes, GameObjects, components, prefabs, C# gameplay code, Input System, 2D tilemaps and physics, animation, UI Toolkit, audio, particles, testing, profiling, builds, and custom MCP tools. Use for Unity MCP connection or automation requests, learning Unity, creating complete games, implementing gameplay systems, working through the 2D Adventure curriculum, or diagnosing Unity Editor, console, compilation, physics, prefab, scene, or build problems.
---

# Unity MCP Game Development

Operate Unity as an evidence-driven editor workflow. Inspect the project first, make the smallest coherent change, wait for Unity to import or compile, read the Console, test behavior, save intentionally, and report what actually passed.

## Establish the contract

Identify or reasonably default:

- Unity Editor version, render pipeline, template, target platform, input/UI systems, and installed package versions.
- Game type, camera, controls, resolution/aspect targets, performance target, and requested deliverable.
- Existing project versus new project, source-control state, current scene, and whether Unity MCP tools are connected.

Version boundaries matter. The original 2D Adventure course targets 2022.3, its revamped course targets Unity 6.3, and the documented Unity MCP setup requires Unity 6 or later plus `com.unity.ai.assistant` 2.0. Verify the installed version instead of mixing package APIs or menu paths.

Read [references/unity-editor-core.md](references/unity-editor-core.md) for general Unity development. For a 2D adventure game, also read [references/unity-2d-adventure.md](references/unity-2d-adventure.md).

## Connect or discover Unity MCP

1. Inspect available tools dynamically for names and descriptions containing Unity. Do not assume MCP is connected or invent a tool schema.
2. If Unity tools exist, identify read-only versus mutating operations and use the exact exposed names and parameters. Common documented examples include `Unity_ReadConsole`, `Unity_ManageScene`, and `Unity_ManageGameObject`, but the live tool registry is authoritative.
3. If tools do not exist, explain the connection requirement and follow [references/unity-mcp.md](references/unity-mcp.md). Do not claim to have changed the Editor.
4. Confirm the intended Unity instance/project when multiple clients or Editors could be active.

Unity MCP exposes the Editor to an external AI client. It is different from Unity Assistant's MCP Client page, which connects Unity outward to other MCP servers.

## Use the MCP operation loop

### 1. Observe

- Read project/editor version, active scene, selection, hierarchy, relevant assets/components, package state, and Console.
- Inspect existing scripts and prefabs before creating replacements. Respect established naming, namespaces, assembly definitions, folders, serialization, and architecture.
- Prefer stable asset paths and object identifiers over ambiguous display names.

### 2. Plan a reversible slice

- State the intended scene/assets/scripts and acceptance check.
- Split broad requests into vertical slices that can compile and play independently.
- Ask before broad deletion, package upgrades, render-pipeline migration, scene replacement, or changes that could invalidate serialized data.

### 3. Mutate narrowly

- Create or edit one logical group at a time. Save scripts to the existing project convention.
- Let Unity's Asset Database create and manage `.meta` files. Do not regenerate GUIDs or hand-edit scene/prefab YAML while Unity is open unless the project explicitly requires a controlled text merge.
- Use Undo-capable Editor APIs for custom mutating MCP tools. Mark modified objects/scenes dirty and save only when intended.

### 4. Synchronize

- Wait for asset import and script compilation to finish. Treat timeouts during imports/builds as a busy Editor, not immediate proof of failure.
- Read the Console after every script or package change. Fix compilation errors before attempting dependent actions; a compile error can prevent the MCP bridge or custom tools from loading.

### 5. Verify

- Inspect the resulting hierarchy, components, serialized fields, prefab links, scene dirty state, and asset paths.
- Enter Play Mode when behavior is involved. Exercise the exact acceptance scenario, then exit Play Mode and confirm that required changes were authored outside Play Mode.
- Run Edit Mode or Play Mode tests when available. Build and profile on the actual target for performance-sensitive work.

### 6. Report

List changed assets, scenes, components, packages, tests, Console status, Play Mode result, build result, assumptions, and remaining manual checks. Never call a feature complete merely because files compiled.

## Build Unity features correctly

- Compose behavior from focused components. Keep scene objects as wiring and assets/prefabs as reusable definitions.
- Use Prefabs for repeated configured hierarchies and ScriptableObjects for reusable authoring data when appropriate. Preserve prefab links; review overrides deliberately.
- Keep input intent separate from device bindings through Input Actions. Read input in the correct phase and move physics bodies through the physics workflow.
- Make frame-driven behavior time-aware; use `Time.deltaTime` for ordinary per-frame rates and the 2D/3D physics step for physics changes.
- Keep state changes authoritative and update UI, animation, audio, and VFX from that state rather than duplicating gameplay truth.
- Validate serialized references and null behavior. Remember that Play Mode changes usually revert when Play Mode ends.

## Apply Unity MCP safely

- Start with Console/project queries before scene or asset writes.
- Keep only needed tools enabled. External direct clients require explicit approval; review the client before accepting.
- Avoid custom tools that execute arbitrary shell commands, accept unconstrained file paths, or perform broad asset deletion.
- Give custom tools narrow typed parameters, unique names, clear descriptions, structured results, validation, and explicit error messages.
- Prefer a read-only audit tool before building a mutating batch tool. A starter template is available at [assets/ProjectHealthMcpTool.cs.txt](assets/ProjectHealthMcpTool.cs.txt).

Read [references/unity-mcp.md](references/unity-mcp.md) before setting up, extending, or troubleshooting Unity MCP.

## Finish with production gates

1. **Compile:** zero C# compilation errors.
2. **Authoring:** scenes/prefabs/assets are saved intentionally with no broken references or missing scripts.
3. **Behavior:** acceptance path passes in Play Mode with expected input, physics, UI, animation, and game-state transitions.
4. **Tests:** relevant Edit Mode and Play Mode tests pass.
5. **Runtime:** a development build runs on the target platform.
6. **Performance:** profile representative gameplay on target hardware; do not optimize from Editor FPS alone.

Read [references/qa-build-performance.md](references/qa-build-performance.md) for QA, testing, source control, profiling, and builds. Use [references/official-unity-sources.md](references/official-unity-sources.md) to verify exact version-specific behavior against official Unity documentation.
