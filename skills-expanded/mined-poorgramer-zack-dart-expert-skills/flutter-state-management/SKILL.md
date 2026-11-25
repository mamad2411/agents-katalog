---
name: "flutter-state-management"
description: "State management architecture for Flutter using Riverpod, Provider, and BLoC patterns. Use when choosing a state solution, implementing reactive state, resolving rebuild issues, or structuring MVVM/BLoC architecture."
metadata:
  last_modified: "2026-03-12 11:18:17 (GMT+8)"
---
# State Management Architecture Guide

## Goal
Master the implementation of declarative reactivity inside Flutter applications. Replaces archaic mutable StatefulWidgets with highly testable, globally available, decoupled state management ecosystems (MVVM or BLoC patterns). Accurately determine the exact state architectural deploy depending directly on application complexity.

## Process
### 🚀 High-Level Workflow
Navigating State Management requires understanding explicit UI requirements and data flow directions natively.

### Phase 1: Determining State Scale
- [State Management Overview](./references/state-management-overview.md) - Learn to accurately delineate between Ephemeral (local) state and App (global) state natively. 

### Phase 2: Deploying Framework Implementation
Choose the designated framework strictly corresponding to the project's legacy constraints or architectural requirements:
- [Provider Best Practices (v6.x)](./references/provider.md) - The legacy standard. Essential for maintaining existing massive environments relying natively atop `InheritedWidget` arrays utilizing strict `context.read`/`Consumer` MVVM separation.
- [Riverpod Best Practices (v3.x)](./references/riverpod.md) - Provider's spiritual successor. Employs compile-time safe, context-less global `ProviderContainer` arrays obliterating scoping errors definitively.
- [BLoC Best Practices (v9.x)](./references/bloc.md) - The enterprise standard. Strictly enforces unidirectional event-driven data flows mapping explicit Events to distinct States (amplified dramatically via Freezed Union Types).

---

## 📚 Documentation Library
Consume these highly specialized architectural reference resources sequentially determining data flow structures profoundly:

- [🧠 Core Reactivity Principles](./references/state-management-overview.md)
- [⚙️ Provider Integrations](./references/provider.md)
- [🌊 Riverpod Architectures](./references/riverpod.md)
- [🧱 BLoC Ecosystem Integrations](./references/bloc.md)
