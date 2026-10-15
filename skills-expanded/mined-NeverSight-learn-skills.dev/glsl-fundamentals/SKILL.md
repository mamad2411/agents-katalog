---
name: glsl-fundamentals
description: GLSL fragment shader basics — coordinate systems, data types, uniforms, varyings, precision, swizzling. Use when writing or debugging any GLSL shader code.
---

# GLSL Fundamentals

## Coordinate Systems

### Screen Coordinates → Normalized UVs → Centered UVs

```glsl
// gl_FragCoord: pixel coordinates (origin bottom-left)
// x: [0, width], y: [0, height]

// Normalized UVs: [0, 1]
vec2 uv = gl_FragCoord.xy / uResolution.xy;

// Centered UVs: [-0.5, 0.5]
vec2 cuv = uv - 0.5;

// Centered + aspect-corrected (circles stay round)
vec2 cuv = uv - 0.5;
cuv.x *= uResolution.x / uResolution.y;
```

### Three.js Mesh UVs

In Three.js `ShaderMaterial`, UVs come from the geometry via a varying:

```glsl
// vertex shader
varying vec2 vUv;
void main() {
  vUv = uv; // built-in attribute from Three.js
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// fragment shader
varying vec2 vUv;
void main() {
  // vUv is [0,1] on the mesh surface
  gl_FragColor = vec4(vUv, 0.0, 1.0);
}
```

## Output

### GLSL 1.0 (WebGL1 / default Three.js)

```glsl
void main() {
  gl_FragColor = vec4(r, g, b, a);
}
```

### GLSL 3.0 ES (WebGL2 / `glslVersion: THREE.GLSL3`)

```glsl
out vec4 fragColor;

void main() {
  fragColor = vec4(r, g, b, a);
}
```

Always set `precision highp float;` at the top of fragment shaders for consistent behavior.

## Data Types

```glsl
// Scalars
float f = 1.0;    // always use decimal point
int   i = 1;
bool  b = true;

// Vectors
vec2  v2 = vec2(1.0, 2.0);
vec3  v3 = vec3(1.0, 2.0, 3.0);
vec4  v4 = vec4(v3, 1.0);            // construct from smaller + scalar
ivec2 iv = ivec2(1, 2);              // integer vectors
bvec3 bv = bvec3(true, false, true); // boolean vectors

// Matrices (column-major)
mat2 m2 = mat2(1.0, 0.0,   // col 0
               0.0, 1.0);  // col 1
mat3 m3 = mat3(1.0);       // identity
mat4 m4 = mat4(1.0);       // identity

// Samplers (textures — must be uniforms, never constructed)
uniform sampler2D uTexture;
uniform samplerCube uCubemap;
```

## Swizzling

Access and rearrange vector components using `xyzw`, `rgba`, or `stpq`:

```glsl
vec4 v = vec4(1.0, 2.0, 3.0, 4.0);

vec3 rgb = v.rgb;        // vec3(1.0, 2.0, 3.0)
vec2 xy  = v.xy;         // vec2(1.0, 2.0)
float z  = v.z;          // 3.0
vec3 zzz = v.zzz;        // vec3(3.0, 3.0, 3.0)
vec4 bgra = v.bgra;      // vec4(3.0, 2.0, 1.0, 4.0) — reorder
vec2 yx  = v.yx;         // vec2(2.0, 1.0)

// Write swizzle
v.xy = vec2(5.0, 6.0);   // v is now (5, 6, 3, 4)
```

## Standard Uniforms Across Platforms

| Concept     | ShaderToy         | FragCoord.xyz     | Three.js ShaderMaterial  |
|-------------|-------------------|-------------------|--------------------------|
| Time        | `iTime`           | `time`            | custom `uTime` uniform   |
| Resolution  | `iResolution.xy`  | `resolution`      | custom `uResolution`     |
| Mouse       | `iMouse`          | `mouse`           | custom `uMouse`          |
| Frame       | `iFrame`          | —                 | custom                   |
| Texture     | `iChannel0..3`    | —                 | custom `sampler2D`       |

Three.js does not inject time/resolution/mouse automatically — you declare and update them yourself:

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
  },
  fragmentShader: `...`,
});

// In animation loop:
material.uniforms.uTime.value = clock.getElapsedTime();
```

## Precision Qualifiers

```glsl
precision highp float;   // 32-bit — use for fragment shaders
precision mediump float; // 16-bit — mobile vertex shaders
precision lowp float;    // 8-bit  — rarely useful

// Per-variable override
highp float bigNumber = 1000000.0;
```

Rule of thumb: use `highp` in fragment shaders for desktop/WebGL2. Mobile WebGL1 may default to `mediump` — declare explicitly to avoid surprises.

## Common Patterns

### Passthrough Vertex Shader

Most fragment-only effects use this:

```glsl
varying vec2 vUv;

void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

### Fullscreen Quad (Post-Processing)

```glsl
// vertex
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}

// fragment
uniform sampler2D tDiffuse;
varying vec2 vUv;
void main() {
  vec4 color = texture2D(tDiffuse, vUv);
  gl_FragColor = color;
}
```

### Aspect-Corrected Circle

```glsl
uniform vec2 uResolution;

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution.xy;
  vec2 center = uv - 0.5;
  center.x *= uResolution.x / uResolution.y;
  float d = length(center);
  float circle = smoothstep(0.25, 0.24, d);
  gl_FragColor = vec4(vec3(circle), 1.0);
}
```

### Debug Visualization

```glsl
// Show UVs as color
gl_FragColor = vec4(vUv, 0.0, 1.0);

// Show normals as color
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);

// Show depth as grayscale
float depth = gl_FragCoord.z;
gl_FragColor = vec4(vec3(depth), 1.0);

// Show a value as heat map (blue → red)
float v = someValue; // 0..1
gl_FragColor = vec4(v, 0.0, 1.0 - v, 1.0);
```

## Built-in Variables

| Variable          | Available In | Type   | Description                          |
|-------------------|-------------|--------|--------------------------------------|
| `gl_FragCoord`    | Fragment    | `vec4` | Window-space pixel position          |
| `gl_FrontFacing`  | Fragment    | `bool` | True if front face                   |
| `gl_FragColor`    | Fragment    | `vec4` | Output color (GLSL 1.0)             |
| `gl_PointCoord`   | Fragment    | `vec2` | Point sprite coordinate [0,1]       |
| `gl_Position`     | Vertex      | `vec4` | Clip-space output position           |
| `gl_PointSize`    | Vertex      | `float`| Point primitive size in pixels       |

## Type Conversion

```glsl
float f = 1.0;
int i = int(f);
float g = float(i);
vec3 v = vec3(f);         // (1.0, 1.0, 1.0) — broadcast
vec4 v4 = vec4(v, 1.0);   // extend
vec2 v2 = v4.xy;           // truncate via swizzle
```

## See Also

- `glsl-math` — smoothstep, easing, remap, constants
- `glsl-color` — HSV, palettes, tonemapping
- `glsl-coordinates` — rotation, polar, tiling
- `threejs-shaders` — Three.js ShaderMaterial API and integration
