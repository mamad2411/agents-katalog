---
name: semwright-av-production
description: Use when an agent must coordinate verified Motion and audio artifacts into a final audiovisual master through Semwright without bypassing Broker authority.
---

# Semwright AV production

Use this Skill only after its requirements pass against the combined live catalog. A Motion render plus an audio file is not, by itself, a verified AV master.

1. **DISCOVER** current Motion, audio, delivery, decode and artifact capabilities. Describe exact operations before execution.
2. **PLAN TOGETHER** from one shared cue graph, owner/session, delivery profile and exact rational duration. Keep Motion and Audio as separate typed subplans.
3. **APPLY MOTION** through its server-issued Composition plan. Render from frame zero for high-level authoring until checkpoint/seek equivalence is independently certified.
4. **APPLY AUDIO** through the combined build's `semwright-audio-authoring` lifecycle, which is typed orchestration data and grants no authority. Execute its native work only through the public Faust/Ardour/analysis capabilities in the live Broker catalog; never call private helpers or treat the library as a provider.
5. **VERIFY INTERMEDIATES** independently. Motion requires source-bound renderer evidence; audio requires native rendered-artifact analysis. UNKNOWN is not PASS.
6. **TRANSFER** Motion through the verified lossless mezzanine route. For audio, keep `MediaArtifact.reference` path-free; bind the public audio receipt to owner-configured source/delivery roots, then use descriptor-pinned `artifact.handoff` with the exact SHA (current bounded handoff: 64 MiB). The MLT root alias is host configuration, never plan authority.
7. **MUX** through the pinned MLT delivery capability. The current certified A-side route is H.264/AAC MP4 with a 48 kHz stereo final audio mix and applies no extra gain, ducking or normalization.
8. **ANALYZE FINAL AUDIO AGAIN.** Encoding can change padding, sample count, duration or peak behavior; pre-encode audio PASS does not certify the encoded master.
9. **VERIFY SYNC** on the final decoded master using the cue/tolerance specification fixed before rendering. Missing or ambiguous detections remain UNKNOWN/FAIL.
10. **PUBLISH** only after required Motion, audio, final-audio and sync reports all pass for the same AV plan/artifact. Publication is an atomic pointer/file operation, not a distributed rollback of prior app mutations.
11. On stale state, denial, cancellation, partial effects or a lost non-idempotent receipt, stop the remaining graph and reconcile from observation. Never silently retry or choose another provider.
12. Preserve artifact digests, source-plan digests, dependency sets, provider generations, runtime/catalog digests and limitations in the handoff.

Use [coordination and recovery](references/coordination-and-recovery.md) for invalidation/reuse rules. Use the separate semwright-video-production and semwright-audio-production Skills for domain authoring detail; this Skill does not duplicate them.

This Skill does not authorize a promotional video, release, merge to main or R16 closure.
