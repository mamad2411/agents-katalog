---
description: 
globs: 
alwaysApply: true
---
# Three.js Development Rules

## Naming Conventions

-   Use **PascalCase** for Three.js classes (e.g., `MeshStandardMaterial`, `PerspectiveCamera`, `Vector3`).
-   Use **camelCase** for instances of Three.js classes, variables, and function names (e.g., `myMaterial`, `mainCamera`, `playerObject`).

## Modularity & Structure

-   **Separate Concerns:** Isolate distinct functionalities. For example:
    -   Scene setup (camera, renderer, basic lights).
    -   Asset loading (models, textures).
    -   Object creation (geometries, materials, meshes).
    -   Animation logic.
    -   Rendering loop.
    -   UI interaction logic.
-   **Scene Graph:** Utilize the `Object3D` hierarchy effectively for grouping objects and managing transformations. Avoid overly deep or flat scene graphs without justification.

## Performance Optimization

-   **Geometry:**
    -   Prefer `BufferGeometry` over the deprecated `Geometry`.
    -   Use `InstancedBufferGeometry` and `InstancedMesh` when rendering many identical or similar objects.
    -   Reuse geometries and materials whenever possible instead of creating new ones. Share materials between meshes if they are identical.
-   **Rendering:**
    -   Optimize the render loop (`requestAnimationFrame`). Only update and render what is necessary each frame.
    -   Consider conditional rendering (only render when the scene changes) for static scenes.
    -   Be mindful of draw calls. Merge geometries (`BufferGeometryUtils.mergeGeometries`) where appropriate, but balance against culling benefits.
-   **Textures:**
    -   Use appropriate texture dimensions (powers of two often preferred, but not strictly required anymore).
    -   Use compressed texture formats (like KTX2 with Basis Universal) suitable for the web (`KTX2Loader`).
    -   Limit texture resolution where high detail isn't necessary.
-   **Materials:** Avoid unnecessary material updates that trigger shader recompilations.
-   **Raycasting:** Optimize raycasting frequency and scope. Raycast against a minimal set of objects if possible.

## Resource Management

-   **Dispose Objects:** Explicitly call `.dispose()` on geometries, materials, textures, render targets, and controls when they are no longer needed to free up GPU and CPU memory.
    ```javascript
    // Example:
    scene.remove(myMesh);
    myMesh.geometry.dispose();
    myMesh.material.dispose();
    // If material uses textures:
    // myMaterial.map.dispose();
    // myMaterial.normalMap.dispose();
    // etc.
    ```
-   **Remove from Scene:** Ensure objects are removed from the scene (`scene.remove(object)`) alongside disposal if they are part of the scene graph.

## API Usage

-   **Loaders:** Use the specific loaders provided by Three.js for different asset types (e.g., `GLTFLoader`, `TextureLoader`, `CubeTextureLoader`). Handle loading errors using callbacks or promises.
-   **Helpers:** Use helpers like `AxesHelper`, `GridHelper`, `CameraHelper`, `DirectionalLightHelper` during development for debugging, but ensure they are removed or conditionally excluded from production builds.
-   **Math:** Use `Vector3`, `Quaternion`, `Euler`, and `Matrix4` correctly for transformations. Prefer Quaternions for rotations to avoid gimbal lock.

## TypeScript Integration

-   Utilize `@types/three` for strong typing of Three.js objects and functions.
-   Define explicit `type` or `interface` definitions for custom data structures interacting with Three.js.

## Framework Integration (e.g., React)

-   Use `useEffect` hooks for setup and teardown of Three.js scenes, renderers, and event listeners within components. Ensure proper cleanup in the return function of `useEffect`.
-   Manage Three.js state (like the renderer, scene, camera instances) carefully. Consider using `useRef` to hold stable references to Three.js objects across renders or manage them outside the React component lifecycle if appropriate for complex applications.
-   Separate Three.js logic from React component rendering logic as much as possible.

## General

-   **Avoid Global Scope:** Encapsulate Three.js logic within appropriate modules or classes.
-   **Error Handling:** Implement robust error handling, especially for asynchronous operations like asset loading.

## Game Loop Management

-   **Use Delta Time:** Implement delta-time based animations rather than frame-based for consistent speed across devices with different frame rates.
-   **Fixed Timestep:** Consider using a fixed timestep for physics calculations to ensure consistent simulation.
-   **Frame Limiting:** Implement optional frame rate limiting for performance consistency.

## Cannon.js Physics Integration

-   **World Synchronization:** Keep physics world and Three.js scene in sync with consistent scale units.
-   **Fixed Step:** Use a fixed timestep (typically 1/60) for physics calculations, separate from rendering.
-   **Debug Visualization:** Implement debug visualization for physics bodies during development.
-   **Resource Reuse:** Cache and reuse physics materials and shapes when possible.
-   **Collision Filtering:** Group collision filtering with bitmasks for performance.
-   **Compound Shapes:** Use compound shapes instead of multiple bodies when appropriate.
-   **Object Sleeping:** Implement sleeping for static or temporarily inactive objects.
-   **Simplified Collisions:** Consider simplified collision shapes for complex geometries.
-   **Solver Tuning:** Tune solver iterations based on simulation needs and performance requirements.
-   **Connection Pattern:** Use a clear pattern for connecting Cannon.js bodies with Three.js meshes.

## Input Handling (Mouse/Keyboard)

-   **Input Manager:** Implement a centralized input manager to prevent scattered event listeners.
-   **Pointer Lock:** Use pointer lock API for first-person camera controls.
-   **Input Debouncing:** Debounce rapid input events where appropriate.
-   **Configurable Bindings:** Support configurable key bindings rather than hardcoded values.
-   **State Tracking:** Track input state rather than just handling events.
-   **Input Buffering:** Consider input buffering for responsive controls in action games.

## Camera Management

-   **Smooth Transitions:** Implement smooth camera transitions between states (e.g., lerp or spring systems).
-   **Constraints:** Implement constraints for camera movement (min/max angles, boundaries).
-   **Separation of Concerns:** Separate camera logic from player movement logic.

## Game State Management

-   **State Machine:** Implement a state machine for game states (loading, menu, playing, paused, game over).
-   **Clean Transitions:** Keep state transitions clean and predictable.
-   **Persistent State:** Handle saving and loading of game progress appropriately.

## Audio Implementation

-   **Positional Audio:** Use Three.js AudioListener and positional audio for immersive sound.
-   **Audio Pooling:** Implement audio loading, pooling, and unloading efficiently.
-   **Volume Management:** Create systems for managing different audio channels (music, SFX, voice).

## Development Tools

-   **Debug Panel:** Create a debug panel to tweak physics parameters at runtime.
-   **Configuration Save/Load:** Implement save/load for physics configurations during testing.
-   **Visual Indicators:** Add visual indicators for collision events and forces.
-   **Performance Monitoring:** Implement FPS counter and performance metrics for optimization.

## Code Structure and Reuse

-   **Utility Functions:** Create utility functions for common Cannon.js setup patterns.
-   **Component System:** Build reusable physics-based components (vehicles, characters, etc.).
-   **Error Prevention:** Add validation for physics parameters to prevent unstable simulations.
-   **Graceful Fallbacks:** Implement graceful fallbacks for physics failures.

## Memory Management

-   **Object Pooling:** Implement object pooling for frequently created/destroyed objects.
-   **Memory Profiling:** Regularly profile memory usage during development.
-   **Texture Management:** Implement texture atlases for related textures to reduce draw calls.

## Responsive Design

-   **Resize Handling:** Handle window resizing properly with camera aspect ratio updates.
-   **Device Detection:** Implement device capability detection for quality settings.
-   **Adaptive Quality:** Create systems to dynamically adjust quality based on performance. 
