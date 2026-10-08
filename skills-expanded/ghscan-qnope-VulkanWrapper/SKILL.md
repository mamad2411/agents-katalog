# Dev Skill

Implementation guide for VulkanWrapper.

## Sub-Guides

| Topic | File | When to Read |
|-------|------|--------------|
| Memory | [memory-allocation.md](memory-allocation.md) | Creating buffers, images, staging uploads |
| Barriers | [barriers.md](barriers.md) | Synchronizing resources, image transitions |
| Shaders | [shaders.md](shaders.md) | Compiling GLSL, includes, push constants, CMake integration |
| Ray Tracing | [ray-tracing.md](ray-tracing.md) | BLAS/TLAS, RayTracedScene, SBT, GeometryReference |
| Vulkan Setup | [vulkan-features.md](vulkan-features.md) | DeviceFinder, feature negotiation, optional extensions |

## Workflow

1. **Read existing code** in `VulkanWrapper/include/VulkanWrapper/<Module>/` before implementing
2. **Write tests first** (TDD) -- see `/test` skill
3. **Implement** following existing patterns (see sub-guides above and CLAUDE.md Core Patterns)
4. **Validation layers** are on by default via `InstanceBuilder().setDebug()` -- address all errors immediately
5. **Format**: `git diff --cached --name-only -- '*.h' '*.cpp' | xargs -r clang-format -i`
6. **Test**: `cd build-Clang20Debug && ctest --output-on-failure`

## Adding New Code

See CLAUDE.md "Adding New Code" section for file placement and CMake registration.
