---
name: sumi-voicebox
description: Guide optional local Voicebox narration setup, hardware/model-size checks, consented voice profiles and export for Sumi or other story videos; downloads and generation require the user's selected scope.
---

# Voicebox narration setup

Use [the verified setup guide](references/setup.md) when the user selects free local narration. Explain app versus selected speech model, hardware/storage and no per-character hosted API bill. Run `python3 scripts/probe.py` for read-only loopback status; no install/download/generation is triggered. Use the exact upstream [Voicebox repository](https://github.com/jamiepine/voicebox), official releases and current model/license information. Do not vendor models or clone the full repository just to install a desktop release.

Reuse a compatible existing app/model. Ask before missing third-party app/runtime/model downloads, with exact selected items, source, size estimate and location. Do not install every engine. Offer a licensed preset, user's own/consented reference, supplied narration or no narration. A distinctive voice can aid identity but does not guarantee platform monetization.

Check the installed local `/openapi.json` and model status before API mutations. Generate approved text once with the verified model/profile and retain job ID/take; inspect an uncertain existing job before retrying. Use the normal Generate/Export interface if this version's API differs. Never expose the backend publicly or silently use cloud services. Save non-secret preferences only; recordings and models remain private.
