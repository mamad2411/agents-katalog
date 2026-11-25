---
name: ue-bug-debugging
description: This skill should be used when debugging rendering issues in Unreal Engine, including visual artifacts, missing features, or unexpected behavior in shaders, materials, or lighting. Trigger when the user asks about "why something looks wrong", "debugging a rendering bug", or analyzing GPU captures from RenderDoc.
---

# UE Rendering Bug Debugging

## Overview

This skill provides a systematic workflow for debugging rendering issues in Unreal Engine. It combines RenderDoc GPU capture analysis with UE source code investigation to identify root causes of visual bugs.

## Debugging Workflow

### Phase 1: Observe and Capture

**Goal:** Document the visual difference and capture GPU data.

1. **Describe the symptom**
   - What looks wrong? (too dark, too bright, missing effect, wrong color)
   - Which objects/materials are affected?
   - Is it consistent or intermittent?

2. **Capture with RenderDoc**
   - Use `open_capture` to load an existing capture
   - Or guide user to capture the frame with RenderDoc

3. **Locate the draw call**
   - Use `get_draw_calls` to find relevant draw calls
   - Filter by marker or texture name to narrow down
   - Note the event_id for further analysis

### Phase 2: Analyze GPU Data

**Goal:** Find differences in shader execution or resources.

1. **Compare with working reference**
   - Find a similar object that renders correctly
   - Compare draw call details and pipeline states

2. **Analyze Pixel Shader**
   ```
   get_shader_info(event_id, "pixel")
   ```
   - Look for texture sampling differences
   - Check for missing code sections (labels)
   - Compare instruction count

3. **Check Pipeline State**
   ```
   get_pipeline_state(event_id)
   ```
   - Verify bound resources (textures, buffers)
   - Check shader permutations
   - Compare constant buffer values

4. **Key indicators of problems:**
   - Missing texture bindings (t2, t3, etc.)
   - Fewer shader instructions than expected
   - Code sections optimized away (empty labels)

### Phase 3: Investigate Source Code

**Goal:** Find the code path that causes the GPU behavior.

1. **Search UE Shaders**
   - Location: `E:\UE\UE_5.7\Engine\Shaders\Private\`
   - Search for relevant keywords:
     - ShadingModel names: `SHADINGMODELID_TWOSIDED_FOLIAGE`
     - Feature flags: `TRANSLUCENCY_LIGHTING_VOLUMETRIC_DIRECTIONAL`
     - Function names found in disassembly

2. **Trace the code path**
   - Find where the divergent behavior originates
   - Look for conditional compilation (`#if`, `#ifdef`)
   - Check for runtime branches based on ShadingModelID

3. **Identify the root cause**
   - Missing condition in an `#if` or `if` statement
   - Incorrect shader permutation
   - Feature incompatibility

### Phase 4: Document Findings

**Goal:** Create a clear record for future reference.

1. **Document in skill references**
   - Create or update `.codebuddy/skills/ue-rendering-pipeline/references/`
   - Include source code locations with line numbers
   - Explain the mechanism and impact

2. **Provide solutions**
   - Workarounds for users
   - Source code fixes (if applicable)
   - Alternative approaches

## Common Bug Patterns

### Pattern 1: Conditional Exclusion

**Symptom:** A ShadingModel is missing from a feature's condition check.

**Example (BasePassPixelShader.usf:1547-1556):**
```hlsl
// Bug: TwoSidedFoliage excluded from Volume lighting
#if (MATERIAL_SHADINGMODEL_DEFAULT_LIT || MATERIAL_SHADINGMODEL_SUBSURFACE)
    if (GBuffer.ShadingModelID == SHADINGMODELID_DEFAULT_LIT || 
        GBuffer.ShadingModelID == SHADINGMODELID_SUBSURFACE)
    {
        GetTranslucencyVolumeLighting(...);  // TwoSidedFoliage never reaches here!
    }
#endif
```

**Detection method:**
1. Shader disassembly shows missing code section
2. Fewer texture bindings than working reference
3. Search source for the ShadingModel ID in relevant context

**Solution:** Add the missing ShadingModel to the condition.

### Pattern 2: Shader Permutation Missing

**Symptom:** A combination of features produces broken or incomplete shader.

**Detection method:**
1. Check shader permutation defines
2. Look for mutually exclusive `#if` blocks
3. Compare working vs broken shader permutations

**Solution:** Add missing permutation or avoid incompatible combinations.

### Pattern 3: Feature Incompatibility

**Symptom:** Two features that should work together don't.

**Example:** TwoSidedFoliage + Volumetric Directional + Lumen GI

**Detection method:**
1. Test each feature in isolation
2. Check documentation for known limitations
3. Review shader permutation matrix

**Solution:** Document incompatibility and provide alternatives.

## Useful Search Patterns

### Finding ShadingModel-specific Code
```bash
grep -r "SHADINGMODELID_TWOSIDED_FOLIAGE" Engine/Shaders/Private/
grep -r "MATERIAL_SHADINGMODEL_TWOSIDED_FOLIAGE" Engine/Shaders/Private/
```

### Finding Translucent Lighting Code
```bash
grep -r "TRANSLUCENCY_LIGHTING_VOLUMETRIC" Engine/Shaders/Private/
grep -r "GetTranslucencyVolumeLighting" Engine/Shaders/Private/
```

### Finding Lumen Integration
```bash
grep -r "LumenDirectLighting\|LumenGI" Engine/Shaders/Private/
grep -r "IsLumenTranslucencyGIEnabled" Engine/Shaders/Private/
```

## Resources

### UE Source Locations

| Component | Path |
|-----------|------|
| BasePass Shaders | `Engine/Shaders/Private/BasePassPixelShader.usf` |
| ShadingModels | `Engine/Shaders/Private/ShadingModels.ush` |
| Translucent Volume | `Engine/Shaders/Private/TranslucencyVolumeCommon.ush` |
| Forward Lighting | `Engine/Shaders/Private/ForwardLightingCommon.ush` |
| Indirect Lighting | `Engine/Shaders/Private/DiffuseIndirectComposite.usf` |

### Project Knowledge Base

- `.codebuddy/skills/ue-rendering-pipeline/references/shadingmodel-comparison.md`
- `.codebuddy/skills/ue-rendering-pipeline/references/translucent-lighting.md`
- `.codebuddy/knowledge/ue-api/ue5.7-api-notes.md`
