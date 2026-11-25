---
name: unity-3d-graphics
description: >
  Unity 6000.3 LTS 3D graphics patterns. Covers URP, shaders (HLSL/ShaderGraph),
  lighting (3D lights, probes, baking), materials, rendering pipeline,
  post-processing, and Unity 6000-specific rendering features.
  Trigger: When writing shader code, configuring URP, working with materials,
  lighting scenes, or implementing rendering features in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Writing HLSL shader code (vertex, fragment, geometry shaders)
- Configuring URP (Universal Render Pipeline) assets and shaders
- Creating or modifying materials (Standard, URP Lit, custom)
- Setting up lighting (directional, point, spot, area lights)
- Working with lightmaps, light probes, and reflection probes
- Implementing post-processing effects
- Optimizing rendering performance (batching, instancing, LOD)
- Using Shader Graph or hand-written shaders
- Working with Unity 6000-specific rendering features (Render Graph, GPU Resident Drawer)
- Integrating graphics with physics (see `skills/unity-physics/`)

## Critical Rules

### ShaderLab vs HLSL — Know the Difference

```shaderlab
Shader "Custom/MyShader"
{
    // === ShaderLab: Declarative structure (properties, subshaders, passes) ===
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" "Queue" = "Geometry" }

        Pass
        {
            // === HLSL: Actual shader code inside HLSLPROGRAM/ENDHLSL ===
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            // HLSL code here
            float4 _Color;

            struct appdata {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f {
                float2 uv : TEXCOORD0;
                float4 position : SV_POSITION;
            };

            v2f vert(appdata v) {
                v2f o;
                o.position = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            half4 frag(v2f i) : SV_Target {
                return half4(_Color.rgb, 1.0);
            }
            ENDHLSL
        }
    }

    Fallback "Diffuse"
}
```

**Why:** ShaderLab defines the shader object structure. HLSL (or legacy CG) writes the actual GPU programs. NEVER write HLSL outside `HLSLPROGRAM`/`ENDHLSL` or `CGPROGRAM`/`ENDCG` blocks.

### Surface Shaders are BIRP Only

```shaderlab
// ✅ VALID — Surface shader (Built-in Render Pipeline only)
CGPROGRAM
#pragma surface surf Lambert
ENDCG

// ❌ WRONG — Surface shaders INCOMPATIBLE with HLSLPROGRAM
HLSLPROGRAM
#pragma surface surf Lambert  // ERROR: Surface shaders require CGPROGRAM
ENDHLSL
```

**Why:** Surface Shaders are a Built-in Render Pipeline feature that generates vertex/fragment code automatically. URP and HDRP do NOT support Surface Shaders.

### URP Does NOT Use UnityCG.cginc

```hlsl
// ❌ WRONG in URP — UnityCG.cginc is Built-in RP only
#include "UnityCG.cginc"

// ✅ CORRECT in URP — Use URP shader library
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
```

**Why:** URP has its own shader library (`Packages/com.unity.render-pipelines.universal/ShaderLibrary/`). Using BIRP includes in URP causes compilation errors or undefined symbols.

### SRP Batcher Requires Single CBUFFER

```hlsl
// ✅ CORRECT — All per-material properties in ONE CBUFFER named UnityPerMaterial
CBUFFER_START(UnityPerMaterial)
    float4 _MainTex_ST;
    float4 _Color;
    float _Metallic;
    float _Glossiness;
CBUFFER_END
sampler2D _MainTex;  // Textures/samplers outside CBUFFER

// ❌ WRONG — Multiple CBUFFER blocks breaks SRP Batcher
CBUFFER_START(UnityPerMaterial)
    float4 _Color;
CBUFFER_END
CBUFFER_START(UnityPerMaterial2)  // Different name = different batch!
    float4 _MainTex_ST;
CBUFFER_END
```

**Why:** SRP Batcher caches material property locations. Multiple CBUFFERs with different names or properties outside any CBUFFER prevent batching.

### ZWrite Off for Transparent Objects

```shaderlab
// Opaque (default)
ZWrite On
Blend Off

// Transparent — MUST disable depth write
ZWrite Off
Blend SrcAlpha OneMinusSrcAlpha

// Cutout — alpha test (discards pixels)
Tags { "RenderType" = "TransparentCutout" }
Blend Off
ZWrite On
// In fragment: clip(alpha - _Cutoff);
```

**Why:** Transparent objects don't write to depth buffer. If ZWrite is On, transparent objects block themselves and create depth sorting artifacts.

## ShaderLab Structure

### Full Shader Object Anatomy

```shaderlab
Shader "Category/Name"
{
    // 1. MATERIAL PROPERTIES (optional but almost always needed)
    Properties
    {
        [Optional: attribute] _PropertyName ("Display Name", Type) = default

        // Common types:
        _Color ("Color", Color) = (1, 1, 1, 1)
        _Float ("Float", Float) = 0.5
        _Range ("Range", Range(0, 1)) = 0.5
        _MainTex ("Texture", 2D) = "white" {}
        _Cube ("Cubemap", Cube) = "" {}
        _Vector ("Vector", Vector) = (0, 0, 0, 0)
    }

    // 2. SUBSHADERS (at least one required)
    SubShader
    {
        // Optional: LOD and tags
        LOD 300
        Tags { "RenderType" = "Opaque" "Queue" = "Geometry" }

        // 3. PASSES (at least one)
        Pass
        {
            Name "MyPass"
            Tags { "LightMode" = "ForwardBase" }

            // Render state commands
            Cull Back
            ZTest LEqual
            ZWrite On
            Blend Off

            // HLSL or CG code
            HLSLPROGRAM
            // ... shader code ...
            ENDHLSL
        }

        // Optional: additional passes
        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode" = "ShadowCaster" }
            // ... shadow pass code ...
        }

        // Optional: Fallback if all SubShaders fail
        Fallback "Diffuse"
    }

    // 4. CUSTOM EDITOR (optional)
    CustomEditor "UnityEditor.StandardShaderGUI"
}
```

### Properties Block Reference

```shaderlab
Properties
{
    // === NUMERIC ===
    _Int ("Integer", Integer) = 42           // Real integer (Unity 6000+)
    _Float ("Float", Float) = 0.5
    _Range ("Range [0,1]", Range(0, 1)) = 0.5

    // === TEXTURES ===
    _Tex2D ("2D Texture", 2D) = "white" {}    // Default: white, black, gray, bump, red
    _TexArray ("Texture Array", 2DArray) = "" {}
    _Tex3D ("3D Texture", 3D) = "" {}         // Default: gray
    _Cube ("Cubemap", Cube) = "" {}

    // === COLORS & VECTORS ===
    _Color ("Color", Color) = (1, 0.5, 0.25, 1)
    _Vector4 ("Vector4", Vector) = (0, 0, 0, 0)
    _Vector2 ("Vector2 (x,y only)", Vector, 2) = (0, 0, 0, 0)  // Shows only x,y

    // === ATTRIBUTES ===
    [Gamma] _LinearVal ("Linear Value", Float) = 0.5   // Mark sRGB
    [HDR] _HDRColor ("HDR Color", Color) = (1, 1, 1, 1)
    [HideInInspector] _HiddenProp ("Hidden", Float) = 0
    [MainTexture] _MainTex ("Main", 2D) = "white" {}     // Material.mainTexture
    [MainColor] _Color ("Main", Color) = (1, 1, 1, 1)  // Material.color
    [NoScaleOffset] _Tex ("Tex", 2D) = "white" {}      // Hide Tiling/Offset
    [Normal] _BumpMap ("Normal Map", 2D) = "bump" {}
    [PerRendererData] _ProxyTex ("Per-Renderer", 2D) = "white" {}
}
```

### HLSL Variable Mapping

```hlsl
// ShaderLab Property Type → HLSL Declaration
Color           → fixed4 _Color; (or float4)
Vector          → float4 _Vector;
Float/Range     → float _Float;
2D              → sampler2D _Tex;
Cube            → samplerCUBE _Cube;
3D              → sampler3D _Volume;
2DArray         → UNITY_DECLARE_TEX2DARRAY(_TexArray);

// uniform keyword is optional but explicit
uniform float4 _Color;
```

### Render Queue Reference

| Queue | Value | Use |
|-------|-------|-----|
| `Background` | 1000 | Skybox, background elements |
| `Geometry` | 2000 | Opaque objects (default) |
| `AlphaTest` | 2450 | Alpha tested objects (cutout) |
| `Transparent` | 3000 | Transparent/blended objects |
| `Overlay` | 4000 | UI, Effects on top |

```shaderlab
Tags { "Queue" = "Geometry" }           // Default for opaque
Tags { "Queue" = "Transparent" }        // For transparent/blend
Tags { "Queue" = "AlphaTest" }         // For cutout shaders
```

## HLSL Programming

### Pragma Directives

```hlsl
// === REQUIRED ===
#pragma vertex vert           // Vertex shader function name
#pragma fragment frag         // Fragment shader function name

// === OPTIONAL SHADER STAGES ===
#pragma geometry geom         // Geometry shader (NOT on Metal)
#pragma hull hull             // Hull shader (DX11+)
#pragma domain domain         // Domain shader (DX11+)

// === SURFACE SHADERS (BIRP only) ===
#pragma surface surf Lambert                              // Basic
#pragma surface surf BlinnPhong addshadow fullforwardshadows vertex:disp tessellate:tessFixed

// === KEYWORDS & VARIANTS ===
#pragma multi_compile _ FEATURE_A FEATURE_B      // All variants in build
#pragma multi_compile_local _ LOCAL_FEATURE      // Local scope keyword
#pragma shader_feature _ USE_TEXTURE             // Strip unused variants
#pragma shader_feature_local _ LOCAL_OPTION

// === GPU INSTANCING ===
#pragma multi_compile_instancing
#pragma instancing_options assumeuniformscaling

// === RENDERER FILTERING ===
#pragma only_renderers d3d11 metal vulkan        // Compile only for these
#pragma exclude_renderers glles3 webgpu           // Exclude these APIs

// === SHADER MODEL & FEATURES ===
#pragma target 4.0                               // Minimum for geometry/tessellation
#pragma require integers mrt8                    // Specific GPU features
#pragma hardware_tier_variants d3d11              // BIRP only — tier variants

// === COMPILATION OPTIONS ===
#pragma enable_d3d11_debug_symbols                // Debug symbols (slow!)
#pragma editor_sync_compilation                  // Force sync compile
```

### Built-in Shader Structures

```hlsl
// From UnityCG.cginc (BIRP)
struct appdata_base {
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
};

struct appdata_tan {
    float4 vertex : POSITION;
    float4 tangent : TANGENT;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
};

struct appdata_full {
    float4 vertex : POSITION;
    float4 tangent : TANGENT;
    float3 normal : NORMAL;
    float4 color : COLOR;
    float2 texcoord : TEXCOORD0;
    float2 texcoord1 : TEXCOORD1;
    float2 texcoord2 : TEXCOORD2;
    float2 texcoord3 : TEXCOORD3;
};

struct v2f {
    float4 position : SV_POSITION;
    float2 uv : TEXCOORD0;
    float3 normal : TEXCOORD1;
    float3 worldPos : TEXCOORD2;
};
```

### Built-in Transform Functions

```hlsl
// Object space → Clip space (MVP)
float4 UnityObjectToClipPos(float3 pos);

// Object space → View space
float3 UnityObjectToViewPos(float3 pos);

// World space direction to camera (not normalized)
float3 WorldSpaceViewDir(float4 v);

// Object space direction to camera
float3 ObjSpaceViewDir(float4 v);

// World space direction to light
float3 WorldSpaceLightDir(float4 v);

// Object space direction to light
float3 ObjSpaceLightDir(float4 v);
```

### Texture Sampling Macros

```hlsl
// Declaration
UNITY_DECLARE_TEX2D(_MainTex);              // Texture + sampler
UNITY_DECLARE_TEX2D_NOSAMPLER(_DataTex);   // Texture only (sampler from another)
UNITY_DECLARE_TEX2DARRAY(_TexArray);       // Texture array

// Sampling
half4 color = UNITY_SAMPLE_TEX2D(_MainTex, uv);
half4 color = UNITY_SAMPLE_TEX2D_SAMPLER(_MainTex, _LinearRepeat, uv);
half4 color = UNITY_SAMPLE_TEX2DARRAY(_TexArray, float3(uv, arrayIndex));

// Explicit LOD
half4 color = UNITY_SAMPLE_TEX2D_LOD(_MainTex, uv, lodLevel);

// Inline samplers (DX11/12, Metal, Vulkan)
SamplerState sampler_linear_repeat;
SamplerState sampler_point_clamp;
SamplerState sampler_trilinear_repeat;
half4 color = _MainTex.Sample(sampler_linear_repeat, uv);
```

### Depth Texture Operations

```hlsl
// In vertex shader — compute eye space depth
COMPUTE_EYEDEPTH(o.vertexDepth);

// In fragment shader — decode depth
float eyeDepth = DECODE_EYEDEPTH(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, uv));
float linear01 = Linear01Depth(depth);
float linearEye = LinearEyeDepth(depth);

// Helper functions
LinearEyeDepth(i)      // Depth → eye space
Linear01Depth(i)       // Depth → 0..1 range
```

### Shadow Sampling Macros

```hlsl
// Declare shadowmap
UNITY_DECLARE_SHADOWMAP(_ShadowMap);

// Sample shadow (returns 0 = shadow, 1 = lit)
float shadow = UNITY_SAMPLE_SHADOW(_ShadowMap, float3(uv.xy, depth));

// Projective shadow sample
float shadow = UNITY_SAMPLE_SHADOW_PROJ(_ShadowMap, float4(uv.xy, depth, 1.0));
```

### Built-in Shader Variables

```hlsl
// === TRANSFORM MATRICES (column-major) ===
unity_ObjectToWorld      // Model matrix
unity_WorldToObject       // Inverse model matrix
UNITY_MATRIX_MVP          // Model * View * Projection
UNITY_MATRIX_MV           // Model * View
UNITY_MATRIX_V            // View
UNITY_MATRIX_P            // Projection
UNITY_MATRIX_VP           // View * Projection

// === CAMERA ===
_WorldSpaceCameraPos      // float3 — camera position
_ProjectionParams         // float4 — (1 or -1, near, far, 1/far)
_ScreenParams             // float4 — (width, height, 1+1/width, 1+1/height)
_ZBufferParams            // float4 — depth buffer linearization

// === TIME ===
_Time                     // float4 — (t/20, t, t*2, t*3)
_SinTime                  // float4 — (t/8, t/4, t/2, t)
_CosTime                  // float4 — (t/8, t/4, t/2, t)
unity_DeltaTime           // float4 — (dt, 1/dt, smoothDt, 1/smoothDt)

// === LIGHTING ===
_LightColor0              // fixed4 — main light color
_WorldSpaceLightPos0      // float4 — (dir, 0) or (pos, 1)
unity_WorldToLight        // float4x4 — world-to-light matrix
unity_WorldToShadow       // float4x4[4] — shadow matrices

// === LOD ===
unity_LODFade             // float4 — (fade, fade*16, 0, 0)
```

### GPU Instancing in Shaders

```hlsl
// Enable instancing
#pragma multi_compile_instancing

// Define per-instance properties
UNITY_INSTANCING_BUFFER_START(Props)
    UNITY_DEFINE_INSTANCED_PROP(float4, _Color)
    UNITY_DEFINE_INSTANCED_PROP(float, _Scale)
UNITY_INSTANCING_BUFFER_END(Props)

// Vertex shader
v2f vert(appdata v, out v2f o)
{
    UNITY_SETUP_INSTANCE_ID(v);
    UNITY_TRANSFER_INSTANCE_ID(v, o);
    // ...
}

// Fragment shader
half4 frag(v2f i) : SV_Target
{
    UNITY_SETUP_INSTANCE_ID(i);
    float4 color = UNITY_ACCESS_INSTANCED_PROP(Props, _Color);
    // ...
}
```

### Shader Variants and Keywords

```hlsl
// Declare keywords
#pragma multi_compile _ FEATURE_ON FEATURE_OFF
#pragma shader_feature _ USE_TEXTURE

// Conditional compilation
#if defined(FEATURE_ON)
    half4 tex = UNITY_SAMPLE_TEX2D(_MainTex, uv);
#else
    half4 tex = half4(_Color.rgb, 1.0);
#endif

// Enable/disable keywords (C#)
material.EnableKeyword("FEATURE_ON");
material.DisableKeyword("FEATURE_ON");
bool isEnabled = material.IsKeywordEnabled("FEATURE_ON");

// Global keywords
Shader.EnableKeyword("GLOBAL_FEATURE");
Shader.DisableKeyword("GLOBAL_FEATURE");
```

### Unity 6000 — Device Feature Detection

```hlsl
// Runtime GPU feature detection (DX12, Vulkan, Metal)
#pragma multi_compile _ UNITY_DEVICE_SUPPORTS_NATIVE_16BIT
#pragma multi_compile _ UNITY_DEVICE_SUPPORTS_WAVE_32

#if defined(UNITY_DEVICE_SUPPORTS_NATIVE_16BIT)
    // Use 16-bit types (half, min16float)
    min16float4 color;
#else
    // Fallback to 32-bit
    float4 color;
#endif
```

## URP Configuration

### URP Shader Structure

```hlsl
Shader "URP/CustomLit"
{
    Properties
    {
        _BaseMap ("Base Map", 2D) = "white" {}
        _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        _Metallic ("Metallic", Range(0, 1)) = 0
        _Smoothness ("Smoothness", Range(0, 1)) = 0.5
    }

    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" "RenderType" = "Opaque" }

        Pass
        {
            Name "ForwardLit"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            // URP uses Core.hlsl, not UnityCG.cginc
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Input.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            // Required CBUFFER for SRP Batcher
            CBUFFER_START(UnityPerMaterial)
                float4 _BaseMap_ST;
                float4 _BaseColor;
                float _Metallic;
                float _Smoothness;
            CBUFFER_END

            // Texture declarations (outside CBUFFER)
            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            struct Attributes {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float2 uv : TEXCOORD0;
            };

            struct Varyings {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 normalWS : TEXCOORD1;
                float3 positionWS : TEXCOORD2;
            };

            Varyings vert(Attributes input) {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.uv = TRANSFORM_TEX(input.uv, _BaseMap);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);
                return output;
            }

            half4 frag(Varyings input) : SV_Target {
                // Sample base map
                half4 baseMap = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv);
                half3 baseColor = baseMap.rgb * _BaseColor.rgb;

                // Simple PBR-ish lighting
                half3 lightDir = normalize(_MainLightPosition.xyz);
                half NdotL = saturate(dot(input.normalWS, lightDir));
                half3 lighting = NdotL * _MainLightColor.rgb;

                half3 finalColor = baseColor * lighting;
                return half4(finalColor, 1.0);
            }
            ENDHLSL
        }

        // Shadow Caster Pass (URP uses separate passes)
        Pass
        {
            Name "ShadowCaster"
            Tags { "LightMode" = "ShadowCaster" }

            HLSLPROGRAM
            #pragma vertex ShadowVert
            #pragma fragment ShadowFrag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Shadows.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _BaseColor;
            CBUFFER_END

            float4 ShadowVert(float4 positionOS : POSITION) : SV_POSITION {
                return TransformObjectToShadowCaster(positionOS);
            }

            half4 ShadowFrag() : SV_TARGET {
                return 0;
            }
            ENDHLSL
        }
    }
}
```

### URP Input.hlsl Structure

```hlsl
// What Input.hlsl provides:
TEXTURE2D(_BaseMap);
SAMPLER(sampler_BaseMap);
TEXTURE2D(_MetallicGlossMap);
TEXTURE2D(_BumpMap);
TEXTURE2D(_EmissionMap);
// ... many more

// Properties
float4 _BaseMap_ST;
float4 _BaseColor;
float _Metallic;
float _Smoothness;
float _Cutoff;
float _NormalScale;
float _EmissionColor;
// ... many more

// Macros
TRANSFORM_TEX(input.uv, _BaseMap)
```

### URP Lighting.hlsl Structure

```hlsl
// What Lighting.hlsl provides:
float3 _MainLightPosition;    // Direction (w=0) or Position (w=1)
float4 _MainLightColor;
float4 _AdditionalLights[MAX_LOCAL_LIGHTS];
int _AdditionalLightsCount;

// Functions
float3 LightingLambert(float3 lightColor, float3 lightDir, float3 normal);
float3 LightingSpecular(float3 lightColor, float3 lightDir, float3 normal, float3 viewDir, float specularPower);
float3 LightWeight(float3 lighting, float shadow, float NdotL);
```

### URP Shader Library Reference

| File | Purpose |
|------|---------|
| `Core.hlsl` | Basic types, transforms, macros |
| `Input.hlsl` | Texture/sampler declarations, property accessors |
| `Lighting.hlsl` | Lighting functions and light data |
| `Shadows.hlsl` | Shadow transform and sampling functions |
| `SurfaceData.hlsl` | Surface data structures |
| `PBRSpecular.shinc` | PBR specular lighting |
| `Common.hlsl` | Shared utilities |

### Creating URP Lit Shader (Simpler Approach)

```hlsl
// Use URP's built-in Lit shader as reference
// Copy from: Packages/com.unity.render-pipelines.universal/Shaders/Lit.shader

// Or use Shader Graph for visual authoring
// Window > Asset Management > Shader Graph > Create > URP > Lit Shader Graph
```

### URP Render Pipeline Asset

```csharp
// Create URP Asset programmatically
var urpAsset = ScriptableObject.CreateInstance<UniversalRenderPipelineAsset>();

// Configure in PlayerSettings
PlayerSettings.defaultScreenWidth = 1920;
PlayerSettings.defaultScreenHeight = 1080;
PlayerSettings.fullscreenMode = FullScreenMode.FullScreenWindow;

// Set URP as active (via GraphicsSettings)
GraphicsSettings.renderPipelineAsset = urpAsset;
GraphicsSettings.useCustomRenderPipeline = true;
```

### URP Volume Framework

```csharp
// Post-processing via Volume
using UnityEngine.Rendering;

public class PostProcessVolume : MonoBehaviour
{
    [SerializeField] private VolumeProfile profile;

    private void Start()
    {
        // Apply to camera
        var volume = gameObject.AddComponent<Volume>();
        volume.profile = profile;
        volume.weight = 1.0f;
        volume.isGlobal = true;
    }
}

// Create VolumeProfile programmatically
var profile = ScriptableObject.CreateInstance<VolumeProfile>();
profile.Add<Bloom>();
profile.Add<ColorAdjustments>();
```

## Materials

### Standard Shader Properties

| Property | Type | Purpose |
|----------|------|---------|
| `_Color` | Color | Albedo tint |
| `_MainTex` | 2D | Albedo texture (RGB) |
| `_Metallic` | Range(0-1) | Metallic workflow value |
| `_MetallicGlossMap` | 2D | R=Metallic, A=Smoothness |
| `_Glossiness` | Range(0-1) | Smoothness (non-metallic) |
| `_BumpMap` | 2D | Tangent space normal map |
| `_BumpScale` | Float | Normal intensity |
| `_ParallaxMap` | 2D | Height map for parallax |
| `_Parallax` | Range | Parallax height scale |
| `_OcclusionMap` | 2D | Ambient occlusion (R) |
| `_EmissionColor` | Color | Emission color |
| `_EmissionMap` | 2D | Emission texture |

### Material API

```csharp
// Get material from renderer
Material mat = renderer.material;      // Creates instance
Material shared = renderer.sharedMaterial;  // Shared (no instance)

// Set properties
mat.color = Color.red;                 // Sets _Color
mat.mainTexture = myTexture;           // Sets _MainTex
mat.SetFloat("_Metallic", 0.8f);
mat.SetColor("_EmissionColor", Color.red);
mat.SetTexture("_MainTex", myTexture);
mat.SetVector("_VectorName", new Vector4(1, 2, 3, 4));

// Check keywords
bool hasEmission = mat.IsKeywordEnabled("_EMISSION");

// Enable/disable keywords
mat.EnableKeyword("_METALLICSPECGLOSSMAP");
mat.DisableKeyword("_METALLICSPECGLOSSMAP");
```

### MaterialPropertyBlock (Per-Instance Without Duplication)

```csharp
// ✅ EFFICIENT — No material duplication
MaterialPropertyBlock block = new MaterialPropertyBlock();
block.SetColor("_MyColor", Color.red);
block.SetTexture("_MainTex", myTexture);
renderer.SetPropertyBlock(block);

// ❌ WASTEFUL — Creates material instance
renderer.material.color = Color.red;
```

### Rendering Mode Reference

```shaderlab
// OPAQUE (default)
Tags { "RenderType" = "Opaque" }
Cull Back
ZTest LEqual
ZWrite On
Blend Off

// CUTOUT (alpha test)
Tags { "RenderType" = "TransparentCutout" }
Cull Back
ZTest LEqual
ZWrite On
Blend Off
// In shader: clip(alpha - _Cutoff);

// FADE (soft transparency)
Tags { "RenderType" = "Transparent" }
Cull Back
ZTest LEqual
ZWrite Off
Blend SrcAlpha OneMinusSrcAlpha

// TRANSPARENT (physical)
Tags { "RenderType" = "Transparent" }
Cull Back
ZTest LEqual
ZWrite Off
Blend One OneMinusSrcAlpha
```

### Material Quick Reference

```csharp
// Create new material from shader
Material mat = new Material(Shader.Find("Standard"));
mat = new Material(myShaderAsset);

// MaterialUpgrade tool for upgrading BIRP → URP
// Edit > Render Pipeline > Universal Render Pipeline > Upgrade Project Materials

// Find materials using specific shader
var materials = Resources.FindObjectsOfTypeAll<Material>()
    .Where(m => m.shader.name == "MyShader");
```

## Lighting

### Light Types and Properties

```csharp
Light light = GetComponent<Light>();

// Types: Directional, Point, Spot, Area, Rectangle
light.type = LightType.Directional;
light.type = LightType.Point;
light.type = LightType.Spot;
light.type = LightType.Area;

// Common properties
light.color = Color.white;
light.intensity = 1.0f;
light.range = 10.0f;              // Point/Spot
light.spotAngle = 60.0f;          // Spot only
light.innerSpotAngle = 45.0f;    // Spot only (for soft edges)
light.shadows = LightShadows.Soft;  // None, Hard, Soft
light.shadowStrength = 1.0f;
light.cookie = cookieTexture;    // Cookie/cutter for light

// Rendering mode
light.renderinglayer = LightRenderingLayer.LightLayerDefault;
light.shadowResolution = ShadowResolution.High;
```

### Forward Rendering Passes

| Pass | Purpose | Contents |
|------|---------|----------|
| `ForwardBase` | Main pass | Ambient, main directional, lightmaps, SH lights, vertex lights |
| `ForwardAdd` | Per-light | Additive per-pixel lights (one invocation per light) |
| `ShadowCaster` | Shadow depth | Renders depth for shadow maps |
| `Deferred` | G-buffer | For deferred shading path (BIRP only) |

### Lightmapping

```csharp
// Light component
light.lightmapBakeType = LightmapBakeType.Baked;  // Baked, Mixed, Realtime
light.bounceIntensity = 1.0f;                      // GI bounce multiplier

// Lighting Settings
Lightmapping.bakeGI = true;
Lightmapping.indirectResolution = 50.0f;   // Texels per unit for indirect
Lightmapping.bounceIntensity = 1.0f;
Lightmapping.realtimeGI = false;

// Progressive GPU (Unity 6000)
Lightmapping.progressive = true;
Lightmapping.progressiveHidden = false;
```

### Light Probes

```csharp
// Light probes sample baked GI at runtime
// Dynamic objects automatically use light probes

// LightProbeProxyVolume — for large dynamic objects
var lppv = gameObject.AddComponent<LightProbeProxyVolume>();
lppv.resolution = new Vector3Int(4, 4, 4);
lppv.refreshMode = LightProbeProxyVolume.RefreshMode.EveryFrame;

// Placement tips:
// - Place in areas where dynamic objects travel
// - Group in tetrahedra (4 probes per group)
// - More probes in areas with complex lighting
// - Fewer probes in uniform lighting areas
```

### Reflection Probes

```csharp
ReflectionProbe probe = GetComponent<ReflectionProbe>();

// Configuration
probe.mode = ReflectionProbeMode.Realtime;    // Realtime, Baked, Custom
probe.refreshMode = ReflectionProbeRefreshMode.EveryFrame;  // EveryFrame, ViaScripting
probe.resolution = 128;                       // 16-1024, typical 64-256
probe.hdr = true;                             // HDR cubemap
probe.boxProjection = true;                   // Enable for interior spaces
probe.intensity = 1.0f;
probe.blendDistance = 1.0f;                   // Blend zone between probes
probe.nearClip = 0.3f;
probe.farClip = 1000.0f;
probe.cullingMask = -1;                        // Layer mask

// Update via scripting
probe.RefreshProbe();

// Best practices:
// - Baked probes for static env = best performance
// - Realtime probes sparingly = expensive
// - Box projection for interior spaces
// - Blend distance for smooth transitions
```

### Shadow Configuration

```csharp
// Quality Settings
QualitySettings.shadowResolution = ShadowResolution.High;
QualitySettings.shadowDistance = 150.0f;       // Max cast distance
QualitySettings.shadowCascades = 4;            // 0, 2, or 4 cascades
QualitySettings.shadowNearPlaneOffset = 2.0f;  // Prevent acne

// Per-Light
light.shadowStrength = 1.0f;
light.shadowBias = 0.05f;
light.shadowNormalBias = 0.4f;
light.shadowNearPlane = 0.1f;

// Shadow Cascade splits (directional light)
// 4 cascades = best quality at all distances
// More cascades = more draw calls

// Optimization
QualitySettings.shadowDistance = 100f;  // Reduce if not needed
QualitySettings.shadowCascades = 2;     // vs 4 for better performance
```

### HDR (High Dynamic Range)

```csharp
// HDR allows values > 1.0 for realistic lighting
// Required for: bloom, tonemapping, realistic exposure

// Enable HDR in URP Volume
var volume = GetComponent<Volume>();
volume.profile.TryGet<Bloom>(out var bloom);
bloom.active = true;
bloom.highQualityFiltering = true;

// Mark HDR in shader property
// In Properties: [HDR] _HDRColor ("HDR Color", Color) = (1, 1, 1, 1)

// HDR color picker in Inspector when [HDR] attribute is used
```

## Rendering Pipeline

### Render Pipeline Comparison

| Feature | BIRP | URP | HDRP |
|---------|------|-----|------|
| Surface Shaders | Yes | No | No |
| Shader Graph | No | Yes | Yes |
| SRP Batcher | No | Yes | Yes |
| Forward Rendering | Yes | Yes | Yes |
| Deferred Rendering | Yes | No | Yes |
| GPU Resident Drawer | No | Yes | Yes |
| Ray Tracing | No | No | Yes |
| VRS | No | Yes | Yes |

### Render Pipeline Switching

```csharp
// Project Settings > Graphics > Scriptable Render Pipeline Settings
// Or via script:

// Set URP
var urpAsset = AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(
    "Assets/Settings/URPAsset.asset");
GraphicsSettings.renderPipelineAsset = urpAsset;
GraphicsSettings.useCustomRenderPipeline = true;

// Set HDRP
var hdrpAsset = AssetDatabase.LoadAssetAtPath<HDRenderPipelineAsset>(
    "Assets/Settings/HDRPAsset.asset");
GraphicsSettings.renderPipelineAsset = hdrpAsset;
GraphicsSettings.useCustomRenderPipeline = true;

// Revert to Built-in
GraphicsSettings.useCustomRenderPipeline = false;
GraphicsSettings.renderPipelineAsset = null;
```

### Draw Call Batching

```csharp
// 1. STATIC BATCHING — Mark GameObjects as Static
// In Inspector: Check "Static" > "Contribute GI"
// Or via script:
GameObjectUtility.SetStaticEditorFlags(gameObject, StaticEditorFlags.ContributeGI);

// All static objects sharing materials are batched into single draw call
// Increases memory (combined mesh stored)

// 2. DYNAMIC BATCHING — Automatic for small meshes
// Enabled in Player Settings
// Requirements:
// - Mesh < 900 vertex attributes
// - Objects share same material
// - No scale

// 3. SRP BATCHER — Different from traditional batching
// Doesn't combine meshes
// Caches material property locations
// Works with different materials (same shader)
```

### GPU Instancing

```csharp
// Enable on Material
material.enableInstancing = true;

// Draw instanced
Graphics.DrawMeshInstanced(mesh, submeshIndex, material, matrices, count);
Graphics.DrawMeshInstanced(mesh, submeshIndex, material, matrices, count, block);

// Draw instanced indirect (GPU-driven)
Graphics.DrawMeshInstancedIndirect(mesh, 0, material, bounds, argsBuffer);

// Example: Draw 100 trees
Matrix4x4[] matrices = new Matrix4x4[100];
for (int i = 0; i < 100; i++)
{
    matrices[i] = Matrix4x4.TRS(positions[i], Quaternion.identity, Vector3.one);
}

MaterialPropertyBlock block = new MaterialPropertyBlock();
block.SetColor("_Color", Color.green);

Graphics.DrawMeshInstanced(treeMesh, 0, treeMaterial, matrices, 100, block);
```

### LOD Group

```csharp
LODGroup lodGroup = GetComponent<LODGroup>();

LOD[] lods = new LOD[4];
lods[0] = new LOD(0.6f, new Renderer[] { highDetail });
lods[1] = new LOD(0.4f, new Renderer[] { mediumDetail });
lods[2] = new LOD(0.2f, new Renderer[] { lowDetail });
lods[3] = new LOD(0.01f, new Renderer[] { billboard });

lodGroup.SetLODs(lods);
lodGroup.RecalculateBounds();

// In shader: unity_LODFade.x = fade (0..1)
```

### Color Space

```csharp
// Project Settings > Player > Other Settings > Color Space
// Or via script:
PlayerSettings.colorSpace = ColorSpace.Linear;   // Recommended
PlayerSettings.colorSpace = ColorSpace.Gamma;    // Legacy

// Linear vs Gamma:
// - Linear: Physically accurate lighting, proper color blending
// - Gamma: Non-linear, simpler, less accurate

// Texture sRGB setting:
// - Color textures (albedo, emission): sRGB = true
// - Data textures (normal, height, metallic): sRGB = false
```

### Texture Compression

| Format | Platform | Quality | Use Case |
|--------|----------|---------|----------|
| ASTC | Mobile, modern GPUs | Excellent | Mobile |
| ETC2 | GLES 3.0 | Good | Android |
| DXT5/BC7 | Desktop (D3D11+) | Excellent | Desktop |
| RGBA Crunched DXT5 | Desktop | Good | Atlas, mobile |
| PVRTC | iOS older | Fair | Legacy mobile |

```csharp
// Texture import settings
TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
importer.textureType = TextureImporterType.Default;
importer.sRGBTexture = true;           // For color textures
importer.mipmapEnabled = true;         // For 3D (disable for UI)
importer.textureCompression = TextureImporterCompression.Compressed;
importer.maxTextureSize = 2048;
```

## Post-Processing

### URP Post-Processing Setup

```csharp
// 1. Add Volume to camera
Camera.main.gameObject.AddComponent<UnityEngine.Rendering.Universal.Volume>();
Volume volume = Camera.main.GetComponent<Volume>();
volume.profile = myVolumeProfile;
volume.isGlobal = true;

// 2. Create Volume Profile
VolumeProfile profile = ScriptableObject.CreateInstance<VolumeProfile>();

// 3. Add effects
profile.Add<Bloom>();
profile.Add<ColorAdjustments>();
profile.Add<Vignette>();
profile.Add<DepthOfField>();
profile.Add<MotionBlur>();
profile.Add<ChromaticAberration>();
profile.Add<FilmGrain>();
profile.Add<AmbientOcclusion>();
```

### Common URP Post-Processing Effects

```csharp
// BLOOM — Glow from bright areas
Bloom bloom = profile.Add<Bloom>();
bloom.active = true;
bloom.intensity = 1.0f;              // Glow intensity
bloom.threshold = 0.9f;              // Brightness threshold
bloom.radius = 0.5f;                 // Blur radius
bloom.highQualityFiltering = true;  // Better quality, more expensive

// COLOR ADJUSTMENTS — Color grading
ColorAdjustments color = profile.Add<ColorAdjustments>();
color.active = true;
color.postExposure = 0.5f;           // Exposure adjustment
color.contrast = 1.1f;               // Contrast
color.colorFilter = new Color(1, 1, 1, 1);
color.hueShift = 0.0f;              // Hue rotation
color.saturation = 1.0f;            // Saturation

// VIGNETTE — Darken edges
Vignette vignette = profile.Add<Vignette>();
vignette.active = true;
vignette.intensity = 0.5f;
vignette.center = new Vector2(0.5f, 0.5f);
vignette.rounded = false;

// DEPTH OF FIELD
DepthOfField dof = profile.Add<DepthOfField>();
dof.active = true;
dof.focusDistance = 10.0f;          // Focus distance (meters)
dof.focalLength = 50.0f;            // Lens focal length (mm)
dof.fStop = 1.4f;                   // Aperture
dof.highQuality = true;

// MOTION BLUR
MotionBlur blur = profile.Add<MotionBlur>();
blur.active = true;
blur.intensity = 1.0f;
blur.quality = MotionBlurQuality.High;

// CHROMATIC ABERRATION
ChromaticAberration ca = profile.Add<ChromaticAberration>();
ca.active = true;
ca.intensity = 0.5f;
ca.highQuality = true;

// FILM GRAIN
FilmGrain grain = profile.Add<FilmGrain>();
grain.active = true;
grain.intensity = 0.5f;
grain.size = 0.5f;

// SCREEN SPACE OCCLUSION
AmbientOcclusion ao = profile.Add<AmbientOcclusion>();
ao.active = true;
ao.intensity = 1.0f;
ao.directLightingStrength = 0.5f;
```

### Local vs Global Volumes

```csharp
// Global — affects entire scene
volume.isGlobal = true;

// Local — affects collider region
volume.isGlobal = false;
volume.blendDistance = 1.0f;  // Blend zone outside collider
// Requires collider on GameObject (box, sphere, mesh)
```

### Volume Stacking

```csharp
// Multiple volumes blend additively
// Priority determines order when volumes overlap
volume.priority = 1;  // Higher = evaluated first

// Weight for additional volume
volume.weight = 0.5f;  // 0 = no effect, 1 = full effect

// Blend between volumes based on distance
// Inside collider: full effect
// Outside collider: 0 effect (unless blendDistance > 0)
```

## Common Mistakes to Prevent

### Shader Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Using `UnityCG.cginc` in URP | BIRP only | Use `Packages/.../ShaderLibrary/Core.hlsl` |
| Surface Shaders in URP | Not supported | Use vertex/fragment or Shader Graph |
| Multiple CBUFFERs for per-material | Breaks SRP Batcher | Single `CBUFFER_START(UnityPerMaterial)` |
| Properties outside CBUFFER | Breaks SRP Batcher | All per-material floats/vectors inside |
| `renderer.material` in Update | Creates instances every frame | Use `sharedMaterial` or `SetPropertyBlock` |
| No mipmaps on 3D textures | Aliasing, cache misses | Enable `mipmapEnabled = true` |

### Rendering Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| ZWrite On for transparent | Depth sorting artifacts | `ZWrite Off` for transparent |
| Alpha blend on opaque | Wrong transparency | Use Cutout or keep Opaque |
| Linear space without HDR | Bloom doesn't work | Enable HDR + Linear space |
| Wrong sRGB on textures | Incorrect colors | Color=sRGB ON, Data=sRGB OFF |
| Realtime reflection probes | Very expensive | Use Baked for static scenes |
| High shadow resolution | GPU cost | Match to game needs |

### Performance Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Too many shader variants | Build size, memory | Use `shader_feature` not `multi_compile` |
| No LOD on detailed meshes | GPU overdraw | Use LODGroup |
| Draw calls > 1000 | CPU bottleneck | Batch, atlas, instancing |
| Full resolution shadows | GPU bottleneck | Reduce `shadowDistance`, cascades |
| Mipmaps off on large textures | Cache thrashing | Enable mipmaps |

### Lighting Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Mixed light with Realtime GI | Performance | Use Baked or disable GI |
| Light probes in static scene | Wasted | Only for dynamic objects |
| Shadow casters > 100 | GPU | Reduce, use cascades |
| Realtime reflection probes every frame | GPU | Use Baked or Custom (scripted) |

## Response Format

When answering Unity graphics questions, follow this structure:

### 1. Quick Answer (When Appropriate)
```
Answer the specific question directly if it's simple.
```

### 2. Code Examples (Always)
```csharp
// C# code with concrete variable names
Material mat = renderer.material;
mat.SetFloat("_Metallic", 0.8f);
```

```hlsl
// HLSL code with proper semantics
float4 frag(v2f i) : SV_Target {
    return float4(_Color.rgb, 1.0);
}
```

### 3. Key Concepts
- Bullet point 1
- Bullet point 2

### 4. Gotchas/Edge Cases
- **Gotcha:** Explanation

### 5. Cross-References
- Related topics or `skills/unity-physics/` integration

### Example Response

**Q: How do I create a custom unlit shader in URP?**

```hlsl
Shader "Custom/Unlit"
{
    Properties
    {
        _BaseMap ("Base Map", 2D) = "white" {}
        _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
    }

    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" "RenderType" = "Opaque" }

        Pass
        {
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _BaseMap_ST;
                float4 _BaseColor;
            CBUFFER_END
            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            struct Attributes {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct Varyings {
                float2 uv : TEXCOORD0;
                float4 positionCS : SV_POSITION;
            };

            Varyings vert(Attributes input) {
                Varyings o;
                o.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                o.uv = TRANSFORM_TEX(input.uv, _BaseMap);
                return o;
            }

            half4 frag(Varyings input) : SV_Target {
                half4 color = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv);
                return color * _BaseColor;
            }
            ENDHLSL
        }
    }
}
```

**Key Points:**
- URP requires `Tags { "RenderPipeline" = "UniversalPipeline" }`
- All per-material properties in `CBUFFER_START(UnityPerMaterial)`
- Textures declared with `TEXTURE2D()` and `SAMPLER()` macros
- Use `TransformObjectToHClip()` instead of `UnityObjectToClipPos()`
- `TRANSFORM_TEX()` handles tiling/offset from `ST` properties

**Common Mistakes:**
- **Forgetting** `Tags { "RenderPipeline" }` = shader compiles in BIRP but not URP
- **Multiple CBUFFERs** = breaks SRP Batcher
- **Using `UnityCG.cginc`** = not available in URP

**See also:** `skills/unity-physics/` for physics-related rendering (colliders affecting visuals, character controllers with graphics).

---

*Source: Unity 6000.3 LTS Documentation — `skills/unity-3d-graphics/references/docs.md`*
