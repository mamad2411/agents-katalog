---
name: leeway-component-state-architecture
description: Deterministic component and interaction state architecture covering visual, semantic, asynchronous, degraded and collision states.
license: MIT
---
# LeeWay Component State Architecture
Model DEFAULT, HOVER where applicable, ACTIVE/PRESSED, FOCUS_VISIBLE, DISABLED, LOADING, SKELETON, EMPTY, ERROR, SUCCESS, DEGRADED, OFFLINE, PERMISSION, COLLISION/OVERFLOW and domain states. Use explicit state machines when complexity justifies them; prevent impossible combinations.