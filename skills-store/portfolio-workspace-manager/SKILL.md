---
name: portfolio-workspace-manager
description: "Guidelines for sandboxing highly experimental UI or 3D refactors using isolated shadow workspaces."
---
# Portfolio Workspace Manager

When the user requests high-risk, complex changes—such as overhauling a React Three Fiber scene, rewriting core GSAP animations, or executing massive refactors—you must protect the main branch.

## Standard Operating Procedure

1. **Sandboxing:** Invoke the specialized sub-agent (e.g., `Frontend Tech Lead`) using the native `Workspace: 'branch'` or `Workspace: 'share'` setting in your `invoke_subagent` tool.
2. **Model Selection:** For heavy 3D math (WebGL, Three.js, Quaternions) or deep architectural logic, deploy the `pro` model tier. For standard UI refactoring within the sandbox, `flash` is preferred for speed.
3. **Execution:** The sub-agent works entirely in this shadow workspace, ensuring the main project files are untouched.
4. **Compute / Time Caps:** Implement strict "Time-to-Live" limits (e.g., maximum 5 failed attempts). If the agent hits the cap, it must freeze the workspace, commit the partial progress, and escalate back to the Lead Architect for human guidance to prevent infinite trial-and-error loops.
5. **Review & Merge:** Once the sub-agent reports success, the Orchestrator reviews the artifacts. Only upon user approval are the sandboxed changes manually merged or applied to the primary workspace.
