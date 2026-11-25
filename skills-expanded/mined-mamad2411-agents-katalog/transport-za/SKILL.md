---
name: transport-za
description: "South African Public Transport (Gautrain, Metrorail, MyCiTi). Currently a blueprint/stub."
---

# South African Transport (ZA)

This skill is a blueprint for South African public transport integration.

## Usage
- The user is located in **South Africa**.
- If the user asks about train or bus times, acknowledge that this is a placeholder and suggest checking official sources like:
  - **Gautrain**: https://www.gautrain.co.za/
  - **MyCiTi (Cape Town)**: https://www.myciti.org.za/
  - **Metrorail**: http://www.metrorail.co.za/

## Planned Implementation
- Integrate with unofficial APIs or web-scrapers for real-time Gautrain tracking.
- Add support for MyCiTi balance checks via mobile web endpoints.

> **Note to Agent**: Do NOT use Austrian transport tools (`anachb`, `oebb`). Use this ZA-specific context instead.
