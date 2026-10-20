---
name: threejs-llms
description: 'Expert guide for generating modern Three.js code using WebGL, WebGPU, and TSL. You MUST load this skill when writing, updating, or debugging Three.js applications.'
license: MIT
---

# Three.js LLMs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Writing, updating, or debugging Three.js code.
- Implementing WebGL or WebGPU renderers for 3D graphics.
- Creating custom shaders or advanced materials using TSL (Three.js Shading Language).
- Setting up new Three.js environments requiring modern ES module imports.

## WHEN NOT TO USE

- General JavaScript/TypeScript web development without 3D or graphical requirements.
- 2D canvas manipulations not utilizing the Three.js library.

## Core Principles

- **Modern Import Maps**: Always use modern import maps (e.g., `import * as THREE from 'three'`) rather than old CDN script tags.
- **Appropriate Renderer Selection**: Use `WebGLRenderer` by default for maximum compatibility, and `WebGPURenderer` only when advanced node-based materials, compute shaders, or TSL are specifically required.
- **Embrace TSL**: For WebGPU and custom shaders, strictly use TSL (Three.js Shading Language) and `NodeMaterial` classes (e.g., `MeshStandardNodeMaterial`) instead of raw GLSL string manipulation.

## Common Pitfalls

- **Outdated Script Inclusion**: Using old `<script src=".../three.min.js">` tags instead of ES modules and import maps leads to module resolution errors.
- **Mixing Renderers and Material Paradigms**: Attempting to use traditional GLSL `ShaderMaterial` with `WebGPURenderer`. Use TSL and node materials on WebGPU.
- **Incorrect TSL Imports**: Importing TSL nodes from incorrect paths. Ensure nodes are sourced correctly from `three/tsl` or `three/webgpu`.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- **Three.js LLMs Overview**
  You MUST read this link to discover the available documentation endpoints and get a quick overview of the library.
  **Headers/Topics**: Introduction, Basic Overview.
  [https://threejs.org/llms.txt](https://threejs.org/llms.txt)

- **Three.js Core Guidelines and API**
  You MUST read this link when starting a new project, setting up a renderer, or looking for core API and module references.
  **Headers/Topics**: Instructions for Large Language Models, Getting Started, Renderer Guides, Core Concepts, Essential API
  (Core, Scenes, Cameras, Renderers, Objects, Materials, Geometries, Lights, Loaders, Controls, Math).
  [https://threejs.org/docs/llms.txt](https://threejs.org/docs/llms.txt)

- **Three.js TSL & Full Code Examples**
  You MUST read this link when implementing TSL, creating node-based materials, using WebGPU, or when you need complete boilerplate examples.
  **Headers/Topics**: Instructions for Large Language Models, Complete Code Examples (WebGLRenderer, WebGPURenderer, GLTFLoader),
  TSL - Complete Reference (TSL Specification, Introduction, Learning TSL, Constants and explicit conversions, Conversions, Uniform, Swizzle,
  Operators, Function, Variables, Array, Varying, Conditional, Loop, Math, Method chaining, Texture, Attributes, Position, Normal, Tangent, Bitangent,
  Camera, Model, Screen, Viewport, Blend Modes, Reflect, UV Utils, Interpolation, Random, Rotate, Oscillator, Timer, Packing, Render Pipeline, Storage,
  Struct, Flow Control, Fog, Color Adjustments, Utilities, NodeMaterial).
  [https://threejs.org/docs/llms-full.txt](https://threejs.org/docs/llms-full.txt)
