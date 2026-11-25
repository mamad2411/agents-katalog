---
name: portfolio-qa-vision-tester
description: "Guidelines and instructions for taking automated Playwright screenshots of 3D WebGL scenes and analyzing them using Multimodal Vision for Visual Actor-Critic QA loops."
---

# Portfolio QA Vision Tester

When the user or Orchestrator requests a visual QA pass on complex 3D (React Three Fiber) or GSAP animations, you must employ a "Visual Actor-Critic" workflow.

## Standard Operating Procedure

1. **Snapshot Generation:** Use a headless browser framework (e.g., Playwright) to spin up the local development server (or Storybook instance). Navigate to the target component and take a high-resolution screenshot (`.png` or `.jpg`) of the `<Canvas>` or animated element.
2. **Vision Analysis (The Critic):** Pass the generated image back into the Multimodal Vision Model (e.g., Gemini 1.5 Pro). Your prompt must explicitly ask the model to evaluate:
   - **Clipping:** Are any 3D geometries clipping through text or other DOM elements?
   - **Lighting/Materials:** Are the shaders, materials, and lighting rendering as intended (not completely black or blown out)?
   - **Layout:** Does the canvas properly align with the storytelling scroll triggers?
3. **Actionable Feedback:** The Vision Critic must return structured JSON feedback (e.g., `{"status": "fail", "issue": "Cube is clipping into the About Me text.", "recommended_fix": "Adjust camera position z-index or Three.js scale"}`).
4. **Iterate:** Pass this feedback to the `frontend-webgl-engineer` to implement the fix. Loop until the visual output is flawless.
