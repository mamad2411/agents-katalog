---
name: "architecture-governance-orchestrator"
description: "Orchestrates architectural governance, including ADR management, C4 modeling, and multi-platform architecture design."
version: 1
created: "2026-07-31"
updated: "2026-07-31"
---
## When to Use
Use for architectural planning, decision recording (ADRs), C4 diagram generation, and high-level infrastructure design (Cloud, Kubernetes, Monorepo).

## Procedure
1. Identify the architectural task: Decision Recording (ADR), Visual Modeling (C4), or High-Level Design (Cloud/K8s/Monorepo).
2. For ADRs: Use the MADR format to capture context, decision, and consequences. Maintain the ADR Index.
3. For C4 Modeling: Generate diagrams for Context, Container, Component, or Code levels as needed, ensuring consistent notation.
4. For High-Level Design: Provide architectural blueprints for Cloud (AWS/Azure/GCP), Kubernetes, or Monorepo (Nx/Turborepo) structures.
5. Link all diagrams to relevant ADRs to ensure the 'why' is always discoverable.
6. Validate the architecture against the project's core principles (scalability, maintainability, security).
7. **Memory Sync**: After an architectural decision, formal ADR documentation, or design assessment is completed, you **MUST** trigger the local memory capture. 

   Save the final ADR, RADR, or architectural decision as a Markdown file in the project directory and invoke the capture script: 
   ```bash
   python $MEMORY_SYSTEM_ROOT\capture_knowledge.py <file_path>
   ```
   This ensures that architectural decisions, compliance documentation, and formal records are automatically routed to the correct storage (OKF or ChromaDB).

## Pitfalls
- Never edit an accepted ADR directly; always write a new one to supersede it.
- Ensure C4 diagrams are linked to the corresponding ADRs for rationale.
- Do not skip ADRs for significant technical decisions; an ADR without action is waste.

## Verification
1. Architecture decisions are documented in ADRs with clear rationale.
2. C4 diagrams correctly represent the system boundaries and components.
3. Design choices are consistent across Cloud, K8s, and Monorepo implementations.
4. Architectural decisions and formal records are automatically synced to the memory system.