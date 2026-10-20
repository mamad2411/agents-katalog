---
name: multimedia-production-orchestrator
description: "Orchestrates the complete multimedia production pipeline: from media downloading and brand-aligned editing to HyperFrames rendering and landing page integration. Keywords: video-production, brand-pipeline, hyperframes, landing-page, multimedia-orchestration."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# Multimedia Production Orchestrator - From Raw Clip to Cinematic Landing Page

This skill manages the entire pipeline of turning raw video content into high-quality, branded multimedia assets and interactive web experiences. It ensures consistent branding, professional editing, and seamless web integration.

## When to Use
Use this skill when:
- Creating a viral short-form video from a selfie or screen share.
- Building a cinematic, scroll-driven landing page from a video clip.
- Producing branded marketing content for social media.
- Orchestrating a multi-platform media launch.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Asset Acquisition
1. **Media Downloading**: Invoke `video-downloader` to retrieve high-quality source files from online platforms.

### Phase 2: Branding & Editing
2. **Brand Injection**: Invoke `video-brand-pipeline-orchestrator` to ensure the assets align with the design system tokens.
3. **Professional Editing**: Invoke `video-edit` to perform transcription, captioning, and visual composition.

### Phase 3: Rendering & Web Integration
4. **HyperFrames Composition**: Invoke `hyperframes` to render the edited video into a web-ready format.
5. **Landing Page Integration**: Invoke `video-to-landing-page` to create a cinematic scroll-scrubbing hero section using the rendered assets.

## Freedom Calibration & Constraints
- **Constraint Level: High**
  - **Rigidity**: The sequence of Download $\rightarrow$ Edit $\rightarrow$ Render $\rightarrow$ Deploy is mandatory.
  - **Freedom**: The specific narrative choices, caption styles, and landing page copy are left to the creative direction of the user.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** use unbranded assets | Using raw footage without brand token injection leads to inconsistent identity. | Always run `video-brand-pipeline-orchestrator` first. |
| **NEVER** skip transcription | Failing to transcribe leads to poor captioning and accessibility issues. | Always use `video-edit` for transcription-first captioning. |
| **NEVER** ignore rendering limits | Attempting to serve raw video files instead of HyperFrames renders leads to poor UX. | Always use `hyperframes` for web-based video playback. |

## Verification
1. Source media is successfully downloaded and verified.
2. A branded, captioned video is produced.
3. A HyperFrames composition is generated.
4. A scroll-driven cinematic landing page is deployed.
