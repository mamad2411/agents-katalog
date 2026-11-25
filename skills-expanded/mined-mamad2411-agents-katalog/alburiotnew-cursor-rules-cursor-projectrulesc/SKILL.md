---
description: Project Rules
alwaysApply: false
---
title: AlbuRIOT (Unity/Photon) — Pointer Rules

# Canonical Instructions
- Primary project guidance lives in `CLAUDE.md` at repository root.
- Use this rules file as a compact enforcement layer and quick pointer.

# Always Enforce
- Do NOT edit generated/vendor paths unless explicitly requested: `Library/`, `Temp/`, `obj/`, `bin/`, `Packages/`, `Assets/Photon/`, `Assets/TextMesh Pro/`, `Assets/Imported Assets/`, `*.meta`.
- Keep gameplay changes multiplayer-safe for Photon PUN 2.
- Ownership/authority rules:
  - only owners mutate owned state (`photonView.IsMine`)
  - shared authority stays on `PhotonNetwork.IsMasterClient` (or offline)
- For players, never use `FindWithTag("Player")`; use `PlayerRegistry.All` and `PlayerRegistry.GetLocalPlayerTransform()`.
- Keep spawn/transition logic centralized through `PlayerSpawnCoordinator`.
- Keep edits minimal and localized; avoid large formatting/rename churn.

# Unity-Specific Working Rules
- New gameplay code belongs under `Assets/Scripts/`.
- Do not create editor tooling unless explicitly requested.
- If scene/inspector wiring is required, provide a short Unity setup checklist.

# Validation Focus
For network/gameplay/transition edits, verify:
- Unity compile health (no introduced script errors)
- host/client transition consistency
- single local spawn at expected marker
- input/camera restoration after transitions/cutscenes
